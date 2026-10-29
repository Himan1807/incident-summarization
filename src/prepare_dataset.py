"""Convert the paper dataset (neu-nds2/llm-sec-incident-analysis, evaluation/<scenario>/) into this project's format.

    python -m src.prepare_dataset --source path/to/llm-sec-incident-analysis/evaluation --out dataset/paper_dataset

Per scenario it writes:
  rag_input.json       canonical input of the advanced pipeline (artifacts + questions, NO answers)
  starter_input.json   same evidence in the legacy schema read by the basic pipeline (src/pipeline.py)
  reference_qa.json    reference answers (EVALUATION ONLY, never given to retrieval or the LLM)
  cleaning_report.json what was cleaned / skipped for this scenario

Cleaning performed (deterministic, no LLM):
  * IOC refanging: 10.0.19[.]0 -> 10.0.19.0, hxxp -> http (network.txt and answers)
  * leakage removal: scenario headings such as 'Koi Stealer Scenario' and the dataset README description are NOT
    passed to the pipeline; titles are neutral
  * Elasticsearch responses flattened to self-contained fact lines; over-long keys (URIs) truncated at 240 chars
  * empty aggregations merged into ONE 'query coverage' artifact (supports 'Not established' answers)
  * shard failures (response without aggregations) recorded as an evidence gap, never as 'nothing found'
  * questions: '??' -> '?', blank/comment lines removed; answers parsed into atoms (typos kept, flagged)
  * deterministic derived findings (client ranking, IP -> hostname/account join, first alert hour) from the data only
"""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

MAX_KEY = 240
DESCRIPTIONS = {
    "file_downloads": "HTTP file downloads and file transfers: download domains/IPs, requests (client -> server:port : URI), file types and download sources.",
    "high_activity_external_dest": "Internal clients ranked by number of connections to external destinations, with each client's most-contacted destinations.",
    "kerberos_clients": "Kerberos client account names (user accounts) and the source IPs they authenticated from.",
    "kerberos_full_services": "Kerberos services requested (including host and machine account names) per source IP.",
    "kerberos_hostnames": "Host names seen in Kerberos traffic with their source IPs.",
    "suricata_alerts": "Suricata IDS alerts: signatures, high-severity alert destinations and sources, and an hourly alert timeline (UTC).",
    "suspicious_certificates": "TLS certificates that are self-signed, IP-based or short-lived.",
    "suspicious_domains": "Unusual domains with their source and destination IPs, and direct-IP HTTP connections.",
}
TYPES = {"suricata_alerts": "ids_alerts", "kerberos_clients": "authentication", "kerberos_full_services": "authentication",
         "kerberos_hostnames": "authentication"}
SKIP = {"doc_count_error_upper_bound", "sum_other_doc_count", "key", "key_as_string", "doc_count", "buckets",
        "value", "value_as_string", "meta"}


# ----------------------------------------------------------------------------- cleaning helpers
def refang(t: str) -> str:
    t = t.replace("[.]", ".").replace("(.)", ".").replace("[:]", ":").replace("[at]", "@")
    return re.sub(r"\bhxxp(s?)", r"http\1", t, flags=re.I)


def clean_ws(t: str) -> str:
    return re.sub(r"[ \t]+", " ", t).strip()


def human(name: str) -> str:
    return name.replace("_", " ")


def fmt_key(b: dict) -> str:
    k = b.get("key_as_string", b.get("key"))
    k = str(k)
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2}):\d{2}(?:\.\d+)?Z?", k)
    if m:                                             # hourly date-histogram bucket -> '2024-09-04 17:00 UTC'
        k = f"{m.group(1)} {m.group(2)}:{m.group(3)} UTC"
    return k if len(k) <= MAX_KEY else k[:MAX_KEY] + "…[truncated]"


def is_agg(v) -> bool:
    return isinstance(v, dict) and ("buckets" in v or "value" in v or "doc_count" in v)


def sub_aggs(bucket: dict) -> dict:
    return {k: v for k, v in bucket.items() if k not in SKIP and is_agg(v)}


def _inline(name: str, node: dict) -> str | None:
    """One-line rendering of a simple sub-aggregation (terms list or single value)."""
    if "value" in node and "buckets" not in node:
        v = node.get("value_as_string", node["value"])
        return f"{human(name)}={v}"
    if "buckets" in node:
        bs = node["buckets"]
        if not bs:
            return None
        if any(sub_aggs(b) for b in bs):
            return None                               # nested deeper: handled by recursion
        items = ", ".join(f"{fmt_key(b)} ({b['doc_count']})" for b in bs[:6])
        more = f" (+{len(bs) - 6} more)" if len(bs) > 6 else ""
        other = node.get("sum_other_doc_count", 0)
        tail = f"; {other} further events in other values" if other else ""
        return f"{human(name)}: {items}{more}{tail}"
    return None


def flatten(name: str, node: dict, lines: list, empty: list, prefix: str = "") -> None:
    label = f"{prefix}{human(name)}"
    if "buckets" in node:
        if not node["buckets"]:
            empty.append(label); return
        for b in node["buckets"]:
            parts, deeper = [], []
            for sn, sv in sub_aggs(b).items():
                txt = _inline(sn, sv)
                (parts if txt else deeper).append(txt or (sn, sv))
            line = f"{label}: {fmt_key(b)} — {b['doc_count']} events"
            if parts:
                line += "; " + "; ".join(p for p in parts if isinstance(p, str))
            lines.append(line)
            for d in deeper:
                if isinstance(d, tuple):
                    flatten(d[0], d[1], lines, empty, prefix=f"{label} {fmt_key(b)} > ")
    elif "value" in node:
        lines.append(f"{label} = {node.get('value_as_string', node['value'])}")
    elif "doc_count" in node:
        subs = sub_aggs(node)
        if node["doc_count"] == 0 and not any(
                (s.get("buckets") if "buckets" in s else s.get("value")) for s in subs.values()):
            empty.append(label); return
        lines.append(f"{label}: {node['doc_count']} matching events")
        for sn, sv in subs.items():
            flatten(sn, sv, lines, empty, prefix=f"{label} > ")


# ----------------------------------------------------------------------------- scenario parsing
def parse_network(path: Path) -> list[str]:
    out = []
    if not path.exists():
        return out
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln.startswith("-"):                        # bullets only: headings leak scenario / malware names
            out.append(clean_ws(refang(ln.lstrip("- "))))
    return out


def parse_questions(path: Path) -> list[str]:
    qs = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            qs.append(re.sub(r"\?+", "?", clean_ws(ln)))
    return qs


def parse_answers(path: Path) -> dict[int, str]:
    ans, cur = {}, None
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^A(\d+):\s*(.*)$", ln.strip())
        if m:
            cur = int(m.group(1)); ans[cur] = m.group(2).strip(); continue
        if re.match(r"^Q\d+:", ln.strip()) or not ln.strip() or ln.startswith("#"):
            cur = None; continue
        if cur is not None:
            ans[cur] += " " + ln.strip()
    return ans


def split_atoms(answer: str) -> list[str]:
    a = re.sub(r"\([^)]*\)", "", refang(answer))      # drop explanatory parentheses
    return [clean_ws(p) for p in re.split(r"[,;]", a) if clean_ws(p)]


def atom_kind(a: str) -> str:
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", a): return "ip"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}(?: UTC)?", a): return "time"
    if a.lower() in ("c2 server", "legitimate service"): return "label"
    if a.lower() in ("confidentiality", "integrity", "availability"): return "cia"
    if "://" in a: return "url"
    if re.fullmatch(r"(?:DESKTOP|LAPTOP|DEKSTOP)-[A-Z0-9]+", a, re.I): return "hostname"
    if re.search(r"\.[a-z]{2,24}$", a, re.I) and " " not in a: return "domain_or_file"
    return "other"


# ----------------------------------------------------------------------------- derived findings
def derived_findings(raw: dict, dc_ips: set) -> list[str]:
    """Deterministic facts computed ONLY from the query results (no reference answers involved)."""
    L = []
    hi = raw.get("high_activity_external_dest", {})
    clients = (hi.get("source_clients") or {}).get("buckets", [])
    clients = [c for c in clients if c["key"] not in dc_ips]
    names = {}                                          # ip -> {hostnames, accounts}
    for b in (raw.get("kerberos_hostnames", {}).get("hostnames") or {}).get("buckets", []):
        for ip in b.get("source_ips", {}).get("buckets", []):
            names.setdefault(ip["key"], {"hosts": set(), "accts": set()})["hosts"].add(b["key"])
    for b in (raw.get("kerberos_clients", {}).get("client_accounts") or {}).get("buckets", []):
        if str(b["key"]).endswith("$"):
            continue                                    # machine accounts are not human users
        for ip in b.get("source_ips", {}).get("buckets", []):
            names.setdefault(ip["key"], {"hosts": set(), "accts": set()})["accts"].add(b["key"])
    for rank, c in enumerate(clients[:5], 1):
        ip = c["key"]; tops = c.get("top_destinations", {}).get("buckets", [])
        n = names.get(ip, {"hosts": set(), "accts": set()})
        line = (f"Derived: internal client {ip} ranks #{rank} by external connections ({c['doc_count']} events, "
                f"{c.get('external_destinations', {}).get('value', 'n/a')} distinct external destinations).")
        if tops:
            line += f" Most-contacted external IP: {tops[0]['key']} ({tops[0]['doc_count']} connections)."
        L.append(line)
        L.append(f"Derived: Kerberos identity of {ip}: hostname(s) {', '.join(sorted(n['hosts'])) or 'none observed'}; "
                 f"human user account(s) {', '.join(sorted(n['accts'])) or 'none observed'}.")
    al = raw.get("suricata_alerts", {})
    tl = (al.get("alert_timeline") or {}).get("buckets", [])
    if tl:
        L.append(f"Derived: Suricata alerts span {fmt_key(tl[0])} to {fmt_key(tl[-1])}; earliest alert hour {fmt_key(tl[0])} "
                 f"({tl[0]['doc_count']} alerts).")
    hs = (al.get("high_severity_alerts") or {})
    dest = (hs.get("high_severity__destinations") or {}).get("buckets", [])
    if dest:
        L.append("Derived: destinations of high-severity alerts: " + ", ".join(f"{b['key']} ({b['doc_count']})" for b in dest[:5]) + ".")
    return L


# ----------------------------------------------------------------------------- main conversion
def convert(scen_dir: Path, out_root: Path) -> dict:
    scen = scen_dir.name
    rep = {"scenario": scen, "cleaning": [], "skipped": [], "gaps": []}
    raw, art_specs, empty_all, gaps = {}, [], [], []
    win_lo, win_hi = None, None
    for f in sorted((scen_dir / "es_results").glob("*_result.json")):
        qname = f.stem.replace("_result", "")
        d = json.loads(f.read_text(encoding="utf-8"))
        tr = d.get("metadata", {}).get("time_range", {})
        if tr.get("gte"): win_lo = min(filter(None, [win_lo, tr["gte"]]))
        if tr.get("lte"): win_hi = max(filter(None, [win_hi, tr["lte"]]))
        resp = d.get("response", {})
        aggs = resp.get("aggregations")
        if aggs is None or d.get("success") is False:
            sh = resp.get("_shards", {})
            gaps.append(f"Query '{human(qname)}' returned no aggregation results (shards failed: {sh.get('failed', 'unknown')} of "
                        f"{sh.get('total', 'unknown')}). This evidence is UNAVAILABLE; it is not evidence that nothing exists.")
            rep["gaps"].append(qname); continue
        raw[qname] = aggs
        lines, empty = [], []
        for an, av in aggs.items():
            if is_agg(av):
                flatten(an, av, lines, empty)
        empty_all += [f"{human(qname)} / {e}" for e in empty]
        if not lines:
            rep["skipped"].append(f"{qname}: all aggregations empty"); continue
        art_specs.append((qname, TYPES.get(qname, "network_summary"), lines))

    net = parse_network(scen_dir / "config" / "network.txt")
    dc_ips = set(re.findall(r"(?:\d{1,3}\.){3}\d{1,3}", " ".join(l for l in net if "controller" in l.lower() or "gateway" in l.lower()
                                                                  or "broadcast" in l.lower())))
    dlines = derived_findings(raw, dc_ips)
    artifacts, n = [], 0

    def add(atype, subtype, desc, lines, heuristic=False, kind="es_query_result"):
        nonlocal n
        n += 1
        artifacts.append({"artifact_id": f"{scen}-{n:02d}", "artifact_type": atype, "subtype": subtype, "source": subtype,
                          "content": {"description": desc, "facts": lines},
                          "metadata": {"scenario": scen, "source_kind": kind, "heuristic": heuristic}})

    for q, atype, lines in art_specs:
        add(atype, q, DESCRIPTIONS.get(q, f"Elasticsearch query result: {human(q)}."), lines)
    if dlines:
        add("derived_findings", "derived_summary",
            "Deterministic summary computed from the query results above (client ranking, IP-to-hostname/account join, alert timeline).",
            dlines, heuristic=True, kind="derived_from_es_results")
    cov = gaps + [f"No matching results for: {e}. (Absence in this query is not proof of absence elsewhere.)" for e in empty_all]
    if cov:
        add("query_coverage", "evidence_gaps", "Queries that returned nothing or failed; use these to state what is NOT established.", cov)

    year_win = (win_lo or "")[:10], (win_hi or "")[:10]
    desc = ("Network security investigation of a monitored LAN. Evidence consists of Elasticsearch aggregation results over Zeek "
            "and Suricata logs (IDS alerts, Kerberos, HTTP downloads, TLS certificates, domains and external-destination activity). "
            "No root cause, impact or C2 attribution is stated; these must be established from the supplied artifacts. "
            "Network context: " + "; ".join(net) + ".")
    meta = {"incident_id": f"INC-{(win_lo or 'unknown')[:10].replace('-', '')}", "scenario": scen,
            "title": "Network security incident investigation", "source": "neu-nds2/llm-sec-incident-analysis",
            "query_window_start": win_lo, "query_window_end": win_hi,
            "evidence_types": sorted({a["artifact_type"] for a in artifacts}),
            "artifact_scope_note": "Evidence is aggregated query output (not raw packets); it contains no chat/communication records."}
    questions = parse_questions(scen_dir / "config" / "questions.txt")
    rag = {"metadata": meta, "incident_description": desc, "investigation_questions": questions,
           "artifacts": [{**a, "content": json.dumps(a["content"], ensure_ascii=False)} for a in artifacts]}

    # legacy schema for the basic pipeline
    alerts = [a["content"] for a in artifacts if a["artifact_type"] == "ids_alerts"]
    logs = [a["content"] for a in artifacts if a["artifact_type"] != "ids_alerts"]
    starter = {"metadata": meta, "alerts": [json.dumps(x, indent=2) for x in alerts],
               "logs": [json.dumps(x, indent=2) for x in logs], "communications": [], "investigation_notes": [desc]}

    # reference answers (evaluation only)
    ans = parse_answers(scen_dir / "config" / "answers.txt")
    qa = []
    if len(ans) != len(questions):
        rep["cleaning"].append(f"question/answer count mismatch: {len(questions)} questions vs {len(ans)} answers")
    for i, q in enumerate(questions, 1):
        a = refang(ans.get(i, ""))
        if not a:
            rep["cleaning"].append(f"Q{i} has no reference answer"); continue
        atoms = split_atoms(a)
        qa.append({"id": i, "question": q, "answer": a,
                   "atoms": [{"text": t, "kind": atom_kind(t)} for t in atoms]})
    for q in qa:
        for at in q["atoms"]:
            if re.match(r"DEKSTOP-", at["text"], re.I):
                rep["cleaning"].append(f"Q{q['id']}: reference answer contains probable typo '{at['text']}' (DESKTOP?); kept as given")

    out = out_root / scen
    out.mkdir(parents=True, exist_ok=True)
    (out / "rag_input.json").write_text(json.dumps(rag, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "starter_input.json").write_text(json.dumps(starter, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "reference_qa.json").write_text(json.dumps({"source": "answers.txt (paper dataset)", "confidence": "paper ground truth",
                                                       "qa": qa}, indent=2, ensure_ascii=False), encoding="utf-8")
    rep.update(artifacts=len(artifacts), facts=sum(len(a["content"]["facts"]) for a in artifacts),
               empty_aggregations=len(empty_all), questions=len(questions), answers=len(ans), atoms=sum(len(q["atoms"]) for q in qa))
    (out / "cleaning_report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="path to llm-sec-incident-analysis/evaluation")
    ap.add_argument("--out", default="dataset/paper_dataset")
    ap.add_argument("--scenario", default=None, help="convert a single scenario")
    a = ap.parse_args()
    src, out = Path(a.source), Path(a.out)
    dirs = [src / a.scenario] if a.scenario else sorted(p for p in src.iterdir() if (p / "es_results").is_dir())
    for d in dirs:
        r = convert(d, out)
        print(f"{r['scenario']:14s} artifacts={r['artifacts']} facts={r['facts']} atoms={r['atoms']} empty_aggs={r['empty_aggregations']} "
              f"gaps={r['gaps']} notes={len(r['cleaning'])}")
    if not a.scenario:
        write_dataset_report(out)


def write_dataset_report(out: Path) -> None:
    """Data-quality table: how many reference answers can be found in the evidence at all."""
    from src.evaluate import atom_in
    from src.verify import make_evidence
    rows, tot_a, tot_e = [], 0, 0
    for d in sorted(p for p in out.iterdir() if p.is_dir()):
        rag = json.loads((d / "rag_input.json").read_text(encoding="utf-8"))
        qa = json.loads((d / "reference_qa.json").read_text(encoding="utf-8"))["qa"]
        ev = make_evidence(*[a["content"] for a in rag["artifacts"]], rag["incident_description"])
        atoms = [t["text"] for q in qa for t in q["atoms"]]
        inev = [t for t in atoms if atom_in(t, ev.text)]
        rep = json.loads((d / "cleaning_report.json").read_text(encoding="utf-8"))
        tot_a += len(atoms); tot_e += len(inev)
        rows.append(f"| {d.name} | {rep['artifacts']} | {rep['facts']} | {len(qa)} | {len(atoms)} | {len(inev)} "
                    f"({100 * len(inev) // max(len(atoms), 1)}%) | {', '.join(rep['gaps']) or '-'} |")
    md = ["# Dataset report", "",
          "Atoms = individual reference answer items (IP, host, user, domain, time, label). 'In evidence' = atom appears in the artifacts "
          "the pipeline receives; the remainder must be inferred (for example the CIA component or 'C2 server' labels) or is a reference typo.",
          "", "| Scenario | Artifacts | Facts | Questions | Atoms | In evidence | Failed queries |", "|---|---|---|---|---|---|---|", *rows, "",
          f"**Total:** {tot_e}/{tot_a} atoms ({100 * tot_e // max(tot_a, 1)}%) are present in the evidence."]
    (out / "DATASET_REPORT.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
