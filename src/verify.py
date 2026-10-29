"""Deterministic grounding verification (no LLM, CPU-free).

Per line it checks: entities (IPv4, domains, URIs, hosts, MACs, dates/timestamps), numbers, citations (single or grouped,
e.g. [id#1, #3]) and whether a claim line is cited at all. Evidence is supplied PER SECTION by the pipeline.
It also computes claim-level faithfulness: a claim is faithful when everything it states is in the evidence AND in the chunks
it cites. Limits: derived numbers (sums, ratios) are flagged, not recomputed; reasoning quality is not judged.
"""
import re
from dataclasses import dataclass

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_FILE_EXT = ("exe|dll|dat|rar|zip|ps1|json|txt|md|py|js|doc|docx|xls|xlsx|pdf|log|tmp|bat|vbs|msi|jpg|jpeg|png|gif|html|htm|"
             "php|asp|aspx|cab|iso|lnk|sys|ini|cfg|xml|csv|sh|7z|gz|tar|dmp|bin|img|apk|jar")
DOM_RE = re.compile(r"\b(?:[a-z0-9_-]+\.)+(?!(?:" + _FILE_EXT + r")\b)[a-z]{2,24}\b", re.I)
URI_RE = re.compile(r"(?<![\w.])/(?:[\w.\-~%]+/)*[\w.\-~%]+")
HOST_RE = re.compile(r"\b(?:DESKTOP|LAPTOP|WIN)-[A-Z0-9]+\b", re.I)
MAC_RE = re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b", re.I)
TS_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(?:\.\d+)?Z?")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
NUM_RE = re.compile(r"(?<![\w.])\d+(?:,\d{3})*(?:\.\d+)?(?![\w])")
CITE_GROUP_RE = re.compile(r"\[([^\[\]]*#\d+[^\[\]]*)\]")
PLACEHOLDER_RE = re.compile(r"\[insert[^\]]*\]", re.I)
MARKER_RE = re.compile(r"^\s*(?:[-*+•]|\d+[.)])\s+")
URL_RE = re.compile(r"https?://([^/\s]+)(/[^\s]*)?", re.I)
TRAIL = ".,;:)]}'\"!?"
STOP = set("""that this with from have were been which their there also into such more than they them then about other these those
could would should possible potential assessment observed evidence available established events event number total while where
what when whose will being does done each both only over under between within based including shows show suggest suggests indicate
indicates likely probably appears appear""".split())
GAP_WORDS = ("not established", "evidence gap", "gaps", "unknown", "cannot be determined", "unavailable", "not determined")


def refang(text: str) -> str:
    """10.0.0[.]1 -> 10.0.0.1, hxxp -> http (defanged IOCs in the dataset)."""
    text = text.replace("[.]", ".").replace("(.)", ".").replace("[:]", ":")
    return re.sub(r"\bhxxp(s?)", r"http\1", text, flags=re.I)


def _ts(m):
    d, t = m.group(1), m.group(2)
    return f"{d} {t[:5]}" if t.endswith(":00") else f"{d} {t}"      # 19:00:00 == 19:00 (hour buckets)


def norm_ts(text: str) -> str:
    """Refang + normalise timestamps: 2026-02-28T19:00:00.0Z -> '2026-02-28 19:00'."""
    return TS_RE.sub(_ts, refang(text))


def _clean_uri(u: str) -> str:
    return u.rstrip(TRAIL)


def _split_urls(text: str) -> str:
    return URL_RE.sub(lambda m: f" {m.group(1)} {m.group(2) or ''} ", text)


def strip_cites(text: str) -> str:
    return CITE_GROUP_RE.sub(" ", text)


def extract_entities(text: str) -> set[str]:
    text = _split_urls(norm_ts(strip_cites(text)))
    ents = set(re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?::\d{2})?", text))
    ents |= set(DATE_RE.findall(text))
    ents |= {i for i in IP_RE.findall(text) if all(0 <= int(x) <= 255 for x in i.split("."))}
    ents |= {d.lower() for d in DOM_RE.findall(text)}
    ents |= {u for u in map(_clean_uri, URI_RE.findall(text)) if len(u) > 3}
    ents |= {h.upper() for h in HOST_RE.findall(text)}
    ents |= {m.lower() for m in MAC_RE.findall(text)}
    return ents


def numbers_in(text: str) -> set[str]:
    """Numbers left after removing everything already covered by entity/citation checks."""
    t = _split_urls(norm_ts(text))
    for rx in (CITE_GROUP_RE, PLACEHOLDER_RE, MAC_RE):
        t = rx.sub(" ", t)
    t = re.sub(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(?::\d{2})?( UTC)?)?", " ", t)
    for rx in (IP_RE, URI_RE, DOM_RE, HOST_RE):
        t = rx.sub(" ", t)
    return {n.replace(",", "") for n in NUM_RE.findall(t)}


def content_words(text: str) -> set[str]:
    t = strip_cites(refang(text)).lower()
    return {w for w in re.findall(r"[a-z0-9][a-z0-9_\-]{3,}", t) if w not in STOP and not w.isdigit()}


@dataclass
class Evidence:
    text: str            # normalised, lower-cased evidence text
    numbers: set


def make_evidence(*texts: str) -> Evidence:
    raw = "\n".join(texts)
    return Evidence(norm_ts(raw).lower(), numbers_in(raw))


def build_corpus(chunks, extra_text="") -> Evidence:
    return make_evidence("\n".join(c["text"] for c in chunks), extra_text)


def parse_citations(line: str) -> list[str]:
    """Resolve [id#1], [id#1, #3], [a#1; b#2] into full chunk ids."""
    ids = []
    for grp in CITE_GROUP_RE.findall(line):
        last_prefix = ""
        for item in re.split(r"[;,]", grp):
            item = item.strip()
            if not item:
                continue
            if item.startswith("#") and last_prefix:
                item = last_prefix + item
            if "#" in item:
                last_prefix = item.split("#")[0]
                ids.append(item)
    return ids


def is_heading(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or bool(re.fullmatch(r"\*\*[^*]+\*\*:?", s))


def is_claim_line(line: str) -> bool:
    s = MARKER_RE.sub("", line).replace("*", "").strip()
    if len(s) < 30 or s.startswith("#") or s.endswith(":") or s.endswith("?"):
        return False
    low = s.lower()
    return not ("not established" in low or low.startswith(("here is", "here are")))


def analyze_text(text: str, ev: Evidence, valid_ids: set[str]) -> list[dict]:
    """Per-line analysis. A claim line is covered if it, or a less-indented parent bullet, carries a valid citation.
    Claim lines inside a 'Not established / evidence gaps' block are absence statements and are exempt."""
    rows, stack, in_gap = [], [], False
    for line in text.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if is_heading(line):
            in_gap = any(g in line.lower() for g in GAP_WORDS)
        stack = [(i, c) for i, c in stack if i < indent]
        cites = parse_citations(line)
        valid_c = [c for c in cites if c in valid_ids]
        inherited = [x for _, c in stack for x in c]
        body = MARKER_RE.sub("", line)
        ents = extract_entities(body)
        nums = numbers_in(body)
        row = {
            "line": line,
            "entities": sorted(ents),
            "numbers": sorted(nums),
            "unsupported_entities": sorted(e for e in ents if e.lower() not in ev.text),
            "unsupported_numbers": sorted(n for n in nums if n not in ev.numbers),
            "invalid_citations": sorted({c for c in cites if c not in valid_ids}),
            "placeholders": PLACEHOLDER_RE.findall(line),
            "is_claim": is_claim_line(line) and not in_gap and not is_heading(line),
            "cite_ids": valid_c or inherited,
        }
        row["cited"] = bool(row["cite_ids"])
        row["uncited"] = row["is_claim"] and not row["cited"]
        stack.append((indent, valid_c))
        rows.append(row)
    return rows


FLAG_KEYS = ("unsupported_entities", "unsupported_numbers", "invalid_citations", "placeholders")


def sanitize(text: str, ev: Evidence, valid_ids: set[str], strict: bool = False):
    """Annotate (default) or drop (strict) flagged lines. Returns (text, flags, clean_text)."""
    out, clean, flags = [], [], []
    for r in analyze_text(text, ev, valid_ids):
        bad = [x for k in FLAG_KEYS for x in r[k]]
        types = [k for k in FLAG_KEYS if r[k]] + (["uncited"] if r["uncited"] else [])
        if types:
            flags.append({"line": r["line"].strip(), "types": types, **{k: r[k] for k in FLAG_KEYS if r[k]}})
            if strict:
                continue
            note = ("  ⚠ UNVERIFIED: " + ", ".join(bad)) if bad else ""
            note += "  ⚠ UNCITED" if r["uncited"] else ""
            out.append(r["line"] + note)
            if not bad:
                clean.append(r["line"])
        else:
            out.append(r["line"]); clean.append(r["line"])
    return "\n".join(out), flags, "\n".join(clean)


def claim_stats(text: str, ev: Evidence, valid_ids: set[str], chunk_text: dict | None = None) -> dict:
    """Claim-level metrics.
      grounding_rate     claims whose entities/numbers all exist in the evidence (works for ANY report, cited or not)
      citation_precision cited claims whose entities/numbers (or, if none, >=3 content words) are in the chunks they cite
      faithfulness       claims that are grounded AND supported by their own cited chunks (needs citations)"""
    rows = [r for r in analyze_text(text, ev, valid_ids) if r["is_claim"]]
    n = len(rows)
    grounded = cited = cite_ok = faithful = 0
    for r in rows:
        g = not (r["unsupported_entities"] or r["unsupported_numbers"] or r["invalid_citations"] or r["placeholders"])
        grounded += g
        if not r["cite_ids"]:
            continue
        cited += 1
        if chunk_text:
            ct = norm_ts(" ".join(chunk_text.get(c, "") for c in r["cite_ids"])).lower()
            cnum = numbers_in(ct)
            if r["entities"] or r["numbers"]:
                ok = all(e.lower() in ct for e in r["entities"]) and all(x in cnum for x in r["numbers"])
            else:
                ok = len(content_words(r["line"]) & content_words(ct)) >= 3
        else:
            ok = True
        cite_ok += ok
        faithful += (ok and g)
    return {"claims": n, "cited_claims": cited,
            "grounding_rate": round(grounded / n, 3) if n else None,
            "citation_precision": round(cite_ok / cited, 3) if cited else None,
            "faithfulness": round(faithful / n, 3) if n else None,
            "uncited_claims": n - cited}


def verify_text(text: str, ev: Evidence, valid_ids: set[str]) -> dict:
    rows = analyze_text(text, ev, valid_ids)
    ents = sorted({e for r in rows for e in r["entities"]})
    claims = [r for r in rows if r["is_claim"]]
    return {
        "entities": ents,
        "unsupported_entities": sorted({e for r in rows for e in r["unsupported_entities"]}),
        "unsupported_numbers": sorted({n for r in rows for n in r["unsupported_numbers"]}),
        "invalid_citations": sorted({c for r in rows for c in r["invalid_citations"]}),
        "placeholders": [p for r in rows for p in r["placeholders"]],
        "claim_lines": len(claims),
        "uncited_lines": sum(r["uncited"] for r in claims),
    }
