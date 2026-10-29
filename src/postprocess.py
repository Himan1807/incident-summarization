"""Deterministic post-processing of LLM output (no LLM calls).

1. clean_model_output : strips chatty preambles, repeated section titles, turns stray headings into bold labels,
                        removes empty bullets, merges 'N. question? / answer' pairs.
2. attribute_citations: for claim lines the model left uncited, attaches the retrieved chunk(s) that actually contain the
                        line's entities/numbers (or most of its content words). Pure string matching; every attached
                        citation is counted and reported (model_citation_rate vs citation_rate in the run report).
3. dedupe_sections    : removes near-duplicate lines inside a section and across sections (earlier occurrence wins).
"""
import re

from src.verify import (MARKER_RE, analyze_text, content_words, extract_entities, is_claim_line, is_heading, norm_ts,
                        numbers_in, strip_cites, make_evidence, CITE_GROUP_RE)

PREAMBLE_RE = re.compile(r"^\s*(?:here is|here's|here are|sure|certainly|okay|below is|the following is)\b[^\n]*$", re.I)


def _norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def clean_model_output(text: str, section_name: str) -> str:
    lines = text.replace("\t", "    ").splitlines()
    while lines and (not lines[0].strip() or PREAMBLE_RE.match(lines[0])):
        lines.pop(0)
    out = []
    for ln in lines:
        m = re.match(r"^(\s*)#{1,6}\s*(.+?)\s*$", ln)
        if m:
            title = m.group(2).strip("*: ")
            if _norm_title(title) in (_norm_title(section_name), ""):
                continue                                     # model repeated the section title
            ln = f"{m.group(1)}**{title}:**" if not m.group(2).rstrip().endswith("**") else f"{m.group(1)}{m.group(2)}"
        if re.fullmatch(r"\s*[-*+•]\s*", ln):                # lone bullet (often a truncated tail)
            continue
        out.append(ln.rstrip())
    # merge "N. question?" + following answer line into "N. answer"
    merged, i = [], 0
    while i < len(out):
        m = re.match(r"^(\s*)(\d+)[.)]\s+(.*\?.*)$", out[i])
        if m and i + 1 < len(out):
            nxt = MARKER_RE.sub("", out[i + 1]).strip()
            merged.append(f"{m.group(1)}{m.group(2)}. {nxt}")
            i += 2
            continue
        merged.append(out[i]); i += 1
    return "\n".join(merged).strip()


def _best_chunks(line: str, chunks: list[dict], max_ids: int = 2) -> list[str]:
    body = MARKER_RE.sub("", line)
    key = extract_entities(body) | numbers_in(body)
    texts = {c["id"]: norm_ts(c["text"]).lower() for c in chunks}
    scored = []
    if key:
        nums = {c["id"]: numbers_in(c["text"]) for c in chunks}
        for cid, t in texts.items():
            hit = sum((k.lower() in t) if not k.isdigit() else (k in nums[cid]) for k in key)
            scored.append((hit / len(key), hit, cid))
        scored.sort(reverse=True)
        if scored and scored[0][0] >= 0.5:
            best = scored[0][0]
            return [cid for r, _, cid in scored if r >= best][:max_ids]
        return []
    words = content_words(body)
    if len(words) < 3:
        return []
    for cid, t in texts.items():
        ov = len(words & content_words(t))
        scored.append((ov / len(words), ov, cid))
    scored.sort(reverse=True)
    if scored and scored[0][1] >= 3 and scored[0][0] >= 0.4:
        return [scored[0][2]]
    return []


def drop_invalid_citations(text: str, valid_ids: set[str]):
    """Remove citation ids that do not exist in this section's evidence (e.g. an example id copied from the prompt)."""
    removed = 0

    def fix(m):
        nonlocal removed
        items = [i.strip() for i in re.split(r"[;,]", m.group(1)) if i.strip()]
        full, last = [], ""
        for it in items:
            if it.startswith("#") and last:
                it = last + it
            if "#" in it:
                last = it.split("#")[0]
            full.append(it)
        keep = [i for i in full if i in valid_ids]
        removed += len(full) - len(keep)
        return ("[" + ", ".join(keep) + "]") if keep else ""

    return CITE_GROUP_RE.sub(fix, text), removed


def attribute_citations(text: str, chunks: list[dict], valid_ids: set[str]):
    """Returns (new_text, number_of_lines_attributed, invalid_citations_removed)."""
    text, bad = drop_invalid_citations(text, valid_ids)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    ev = make_evidence("")
    rows = analyze_text(text, ev, valid_ids)
    out, n = [], 0
    for r in rows:
        line = r["line"]
        if r["uncited"]:
            ids = _best_chunks(line, chunks)
            if ids:
                line = line.rstrip() + " [" + ", ".join(ids) + "]"
                n += 1
        out.append(line)
    return "\n".join(out), n, bad


def _sig(line: str):
    body = strip_cites(MARKER_RE.sub("", line)).replace("*", "")
    key = frozenset(e.lower() for e in extract_entities(body)) | frozenset(numbers_in(body))
    return key, content_words(body), body


def _jacc(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def dedupe_sections(sections: dict[str, str], protect=("Answers to Investigation Questions",), embed=None,
                    same_sec=0.6, cross_sec=0.75, emb_thr=0.92):
    """Remove near-duplicate lines. Lines with identical entity/number sets and similar wording are duplicates; lines with no
    entities/numbers (pure assessments) need higher similarity. Optional `embed(list[str]) -> unit vectors` adds semantic matching.
    Returns (new_sections, removed) where removed = [(section, line, duplicate_of_section)]."""
    seen: list[tuple[str, frozenset, set, str, object]] = []      # (section, key, words, body, vector)
    out, removed = {}, []
    for name, text in sections.items():
        keep = []
        lines = text.splitlines()
        sigs = [(_sig(l) if (l.strip() and not is_heading(l) and is_claim_line(l)) else None) for l in lines]
        vecs = {}
        if embed is not None:
            idx = [i for i, s in enumerate(sigs) if s]
            if idx:
                for i, v in zip(idx, embed([sigs[i][2] for i in idx])):
                    vecs[i] = v
        for i, l in enumerate(lines):
            s = sigs[i]
            if s is None or name in protect:
                keep.append(l)
                if s is not None:
                    seen.append((name, s[0], s[1], s[2], vecs.get(i)))
                continue
            key, words, body = s
            dup_of = None
            for sec, k2, w2, b2, v2 in seen:
                thr = same_sec if sec == name else cross_sec
                if sec in protect:
                    continue                                   # restating a Q&A answer elsewhere is fine
                j = _jacc(words, w2)
                semantic = (embed is not None and vecs.get(i) is not None and v2 is not None
                            and float(vecs[i] @ v2) >= emb_thr and (key == k2 or (not key and not k2)))
                if (key == k2 and key and j >= 0.5) or (not key and not k2 and j >= thr + 0.1) or semantic or (key == k2 and j >= thr):
                    dup_of = sec; break
            if dup_of:
                removed.append((name, l.strip(), dup_of))
            else:
                keep.append(l)
                seen.append((name, key, words, body, vecs.get(i)))
        # drop parent lines that lost all their children
        final = []
        for j, l in enumerate(keep):
            if l.rstrip().endswith(":") and not is_heading(l) and l.strip():
                ind = len(l) - len(l.lstrip())
                nxt = next((x for x in keep[j + 1:] if x.strip()), None)
                if nxt is None or (len(nxt) - len(nxt.lstrip())) <= ind:
                    removed.append((name, l.strip(), "(orphaned parent)")); continue
            final.append(l)
        out[name] = "\n".join(final)
    return out, removed
