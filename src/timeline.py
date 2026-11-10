"""Extractive timeline (no LLM): built from every evidence line that carries its own timestamp.

An LLM tends to copy one timestamp onto unrelated facts (host identity, signature counts) and costs several minutes on a CPU.
Here each timestamped evidence line becomes one entry, entries sharing a timestamp are merged, and everything is sorted
chronologically and cited with the chunk it came from. Use --llm-timeline to generate this section with the LLM instead.
"""
import re
from collections import OrderedDict

from src.verify import norm_ts

TS = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})(?::\d{2})?")


def _describe(line: str, ts: str) -> str:
    low = line.lower()
    if "earliest alert hour" in low:
        return "earliest alert hour"
    m = re.match(r"^\s*([a-z0-9 _>]+?):\s*" + re.escape(ts), low)
    n = re.search(r"[—-]\s*(\d+)\s+events?", line)
    if m and n:                                                            # '<label>: <ts> UTC — N events'
        return f"{m.group(1).strip()}: {n.group(1)} events"
    text = re.sub(r"^\s*(?:Derived:\s*)?", "", line)
    return re.sub(r"\s+", " ", text).strip().rstrip(".")


def build_timeline(chunks: list[dict], max_entries: int = 14):
    """Returns (markdown_text, chunk_ids_used). Empty text if the evidence has no timestamps."""
    entries: "OrderedDict[str, list]" = OrderedDict()
    for c in chunks:
        for line in c["body"].splitlines():
            n = norm_ts(line)
            ms = list(TS.finditer(n))
            if not ms:
                continue
            low = line.lower()
            # 'Derived: alerts span A to B; earliest alert hour A (n alerts)' -> the earliest hour is the LAST timestamp on the line
            ts = ms[-1].group(1) if ("span" in low and "earliest alert hour" in low) else ms[0].group(1)
            desc = _describe(line, ts)
            entries.setdefault(ts, [])
            if not any(desc == d for d, _ in entries[ts]):
                entries[ts].append((desc, c["id"]))
    if not entries:
        return "", []
    used, out = [], []
    for ts in sorted(entries)[:max_entries]:
        descs = "; ".join(d for d, _ in entries[ts])
        ids = list(dict.fromkeys(i for _, i in entries[ts]))
        used += ids
        out.append(f"- {ts} UTC — {descs} [{', '.join(ids)}]")
    return "\n".join(out), list(dict.fromkeys(used))
