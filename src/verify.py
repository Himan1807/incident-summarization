"""Deterministic grounding verification (no LLM, CPU-free).

Extracts checkable entities (IPv4, domains, URI paths, host names, MACs) and
citation IDs from generated text and checks them against the evidence corpus.
"""
import re

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOM_RE = re.compile(r"\b(?:[a-z0-9_-]+\.)+(?:com|net|org|io|tech|info|xyz|ru|cn|co|ms|edu|gov|dev|app|cloud|top|site|online|us|uk|de|fr|in)\b", re.I)
URI_RE = re.compile(r"(?<![\w.])/(?:[\w.\-~%]+/)*[\w.\-~%]+")
HOST_RE = re.compile(r"\bDESKTOP-[A-Z0-9]+\b|\bLAPTOP-[A-Z0-9]+\b")
MAC_RE = re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b", re.I)
CITE_RE = re.compile(r"\[([^\[\]\s]+#\d+|[\w\-]+-E\d+#\d+)\]")
PLACEHOLDER_RE = re.compile(r"\[insert[^\]]*\]", re.I)


def extract_entities(text: str) -> set[str]:
    ents = set(IP_RE.findall(text))
    ents |= {d.lower() for d in DOM_RE.findall(text)}
    ents |= {u for u in URI_RE.findall(text) if len(u) > 3}
    ents |= set(HOST_RE.findall(text))
    ents |= {m.lower() for m in MAC_RE.findall(text)}
    return ents


def _ip_valid(s):
    return all(0 <= int(x) <= 255 for x in s.split("."))


def build_corpus(chunks, extra_text="") -> str:
    return ("\n".join(c["text"] for c in chunks) + "\n" + extra_text).lower()


def verify_text(text: str, corpus_lower: str, valid_ids: set[str]) -> dict:
    ents = {e for e in extract_entities(text) if not (IP_RE.fullmatch(e) and not _ip_valid(e))}
    unsupported = sorted(e for e in ents if e.lower() not in corpus_lower)
    cites = CITE_RE.findall(text)
    bad_cites = sorted({c for c in cites if c not in valid_ids})
    return {"entities": sorted(ents), "unsupported_entities": unsupported,
            "citations": cites, "invalid_citations": bad_cites,
            "placeholders": PLACEHOLDER_RE.findall(text)}


def sanitize(text: str, corpus_lower: str, valid_ids: set[str], strict: bool = False):
    """Annotate (or, in strict mode, drop) lines containing unsupported entities / bad citations."""
    out, flagged = [], []
    for line in text.splitlines():
        r = verify_text(line, corpus_lower, valid_ids)
        bad = r["unsupported_entities"] or r["invalid_citations"] or r["placeholders"]
        if bad:
            flagged.append({"line": line.strip(), **{k: r[k] for k in ("unsupported_entities", "invalid_citations", "placeholders")}})
            if strict:
                continue
            line = line + "  ⚠ UNVERIFIED: " + ", ".join(r["unsupported_entities"] + r["invalid_citations"] + r["placeholders"])
        out.append(line)
    return "\n".join(out), flagged
