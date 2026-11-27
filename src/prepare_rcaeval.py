"""Convert RCAEval RE2-OB failure cases into the incident format used by the pipeline (same four files per incident).

python -m src.prepare_rcaeval --zip <path>/RE2-OB.zip --out dataset/paper_dataset

Source: RCAEval benchmark (Pham et al.), suite RE2, system Online Boutique (RE2-OB.zip from Zenodo record 14590730,
doi:10.5281/zenodo.14590730). One repetition (instance 1) per root-cause service x fault type = 30 incidents.

Per incident:
  rag_input.json       metadata, neutral description, investigation questions, artifacts ({"description", "facts"} strings)
  starter_input.json   same evidence in the legacy schema (alerts = metric anomalies, logs = the rest)
  reference_qa.json    evaluation only: reference answers split into atoms; never given to retrieval or the LLM
  cleaning_report.json source case, labels and what is (not) present in the evidence
and the "RCAEval RE2-OB" section of DATASET_REPORT.md.

Incident names are neutral (re2ob_01 ... re2ob_30): chunk ids are built from the name and shown to the LLM, so a name such as
checkoutservice_cpu would give the answer away. Baselines use the first 10 minutes of each capture, never the injection time.
Only numpy and the standard library are used.
"""
import argparse
import csv
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

SUITE = "RE2-OB"
BASELINE_S = 600                                  # first 10 minutes of every capture = baseline
FAULTS = {  # RCAEval fault -> (answer label, atom, RCAEval indicator; docs/AGENTS.md and RCAEval/benchmark/scoring.py)
    "cpu": ("CPU", "CPU", "cpu"), "mem": ("memory", "memory", "mem"), "disk": ("disk", "disk", "diskio"),
    "delay": ("network delay", "delay", "latency"), "loss": ("packet loss", "loss", "latency"),
    "socket": ("socket", "socket", "socket")}
TRACE_SERVICE = {"frontendservice": "frontend"}   # trace service names that differ from the metric/container names
QUESTIONS = [
    "What is the name of the service where the failure originated (the root-cause service)?",
    "What is the name of the Kubernetes pod of the root-cause service?",
    "On which Kubernetes node did the pod of the root-cause service run?",
    "What type of fault caused the incident: CPU, memory, disk, network delay, packet loss, or socket?",
    "Which of the three CIA components is primarily affected: availability, integrity, or confidentiality?",
    "During what minute did the first signs of the failure appear? Provide the earliest date and time in YYYY-MM-DD HH:MM UTC format.",
    "Which metric of the root-cause service best shows the fault? Give it as <service>_<indicator>, for example cartservice_cpu.",
    "According to the trace latency statistics, which single service operation showed the largest latency increase? "
    "Is its service the root cause or a downstream symptom?",
]


def ts(t: float) -> str:
    return datetime.fromtimestamp(int(t), timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def num(v: float) -> str:
    if not np.isfinite(v):
        return "n/a"
    a = abs(v)
    return f"{v:.0f}" if a >= 100 else f"{v:.2f}" if a >= 1 else f"{v:.4f}".rstrip("0").rstrip(".") if v else "0"


def read_series(z: zipfile.ZipFile, name: str):
    with z.open(name) as fh:
        rows = list(csv.reader(io.TextIOWrapper(fh, encoding="utf-8")))
    hdr = rows[0]
    data = np.array([[float(x) if x not in ("", "nan", "NaN") else np.nan for x in r] for r in rows[1:]], dtype=float)
    return hdr, data


def robust_scores(hdr, data, t0):
    """Per series: baseline median/MAD over the first 10 minutes, deviation score and first sustained deviation after it.
    A series with no baseline samples that appears later (e.g. a disk I/O series that only exists once disk activity starts)
    is reported as 'appears' with its first timestamp instead of a score."""
    t = data[:, 0]; pre = t < t0 + BASELINE_S; out = []
    for j in range(1, len(hdr)):
        x = data[:, j]; b = x[pre & np.isfinite(x)]; p = x[~pre]
        if not np.isfinite(p).any():
            continue
        tp = t[~pre]
        if len(b) < 5:
            fin = np.isfinite(p); k = int(np.nanargmax(np.abs(p)))
            out.append({"name": hdr[j], "appears": float(tp[fin][0]), "first": float(p[fin][0]), "peak": float(p[k]),
                        "peak_t": float(tp[k]), "score": float("inf"), "onset": float(tp[fin][0])})
            continue
        med = float(np.median(b)); mad = float(np.median(np.abs(b - med)))
        scale = 1.4826 * mad + 0.01 * abs(med) + 0.005 * float(np.nanmax(np.abs(x))) + 1e-9   # floors: flat or zero baselines
        zs = np.abs(x - med) / scale
        zp = np.where(np.isfinite(zs[~pre]), zs[~pre], 0.0)
        score = float(np.percentile(zp, 90))
        xp = np.where(np.isfinite(p), p, med)
        onset = None
        for i in range(len(zp) - 2):                  # sustained: 3 consecutive samples above 5 robust deviations
            if zp[i] > 5 and zp[i + 1] > 5 and zp[i + 2] > 5:
                onset = float(tp[i]); break
        k = int(np.argmax(np.abs(xp - med)))
        out.append({"name": hdr[j], "median": med, "peak": float(xp[k]), "peak_t": float(tp[k]), "score": score, "onset": onset})
    return sorted(out, key=lambda r: (-r["score"], r.get("appears", 0), r["name"]))


def template(container: str, message: str) -> str:
    """Log template for cases whose logs.csv has no log_template column: numbers, hex ids and quoted values masked."""
    m = re.sub(r"\b[0-9a-f]{8,}\b|\b\d+(?:\.\d+)?\b", "<*>", message or "")
    return f"{container} " + re.sub(r'"[^"]*"', '"<*>"', m).strip()


def op_service(op: str) -> str:
    s = op.split("_", 1)[0]
    return TRACE_SERVICE.get(s, s)


def convert(z: zipfile.ZipFile, case: str, scen: str, out_root: Path) -> dict:
    service, fault = case.rsplit("_", 1)
    base = f"{SUITE}/{case}/1/"
    inject = int(z.read(base + "inject_time.txt").decode().strip())
    mh, md = read_series(z, base + "simple_metrics.csv"); t0, t1 = float(md[0, 0]), float(md[-1, 0])
    services = sorted(h[:-4] for h in mh[1:] if h.endswith("_cpu"))
    disk_services = sorted(h[:-7] for j, h in enumerate(mh) if h.endswith("_diskio") and np.isfinite(md[:, j]).any())  # columns with data
    arts, notes = [], []

    def add(atype, subtype, desc, facts, kind="rcaeval_telemetry_aggregate", heuristic=False):
        arts.append({"artifact_id": f"{scen}-{len(arts) + 1:02d}", "artifact_type": atype, "subtype": subtype, "source": subtype,
                     "content": json.dumps({"description": desc, "facts": facts}),
                     "metadata": {"scenario": scen, "source_kind": kind, "heuristic": heuristic}})

    # 1) metric anomalies (the alert-like artifact)
    ms = robust_scores(mh, md, t0)
    dev = [r for r in ms if r["onset"] is not None]
    facts = [f"metric anomalies: {len(dev)} of {len(ms)} container metric series deviate from their baseline (first 10 minutes of the capture)"]
    for r in dev[:12]:
        if "appears" in r:
            facts.append(f"metric anomalies: {r['name']} — no data in the baseline; series appears at {ts(r['appears'])} "
                         f"(first value {num(r['first'])}); peak {num(r['peak'])} at {ts(r['peak_t'])}")
        else:
            facts.append(f"metric anomalies: {r['name']} — baseline median {num(r['median'])}; peak {num(r['peak'])} at {ts(r['peak_t'])}; "
                         f"sustained deviation from {ts(r['onset'])} (score {num(r['score'])})")
    add("monitoring_alerts", "metric_anomalies",
        "Container metric series (CPU, memory, disk I/O, sockets, workload, error rate, latency p50/p90 per service) that deviate from "
        "their baseline or appear only after it, ranked by deviation score, with peak value and first sustained deviation (UTC).", facts)
    # 2) trace latency per operation
    lh, ld = read_series(z, base + "tracets_lat.csv"); lt = ld[:, 0]; pre = lt < t0 + BASELINE_S
    lat = []
    for j in range(1, len(lh)):
        a, b = np.nanmean(ld[pre, j]), np.nanmean(ld[~pre, j])
        if np.isfinite(a) and np.isfinite(b):
            k = int(np.nanargmax(ld[~pre, j])) if np.isfinite(ld[~pre, j]).any() else 0
            lat.append({"op": lh[j], "pre": float(a), "post": float(b), "ratio": float((b + 1) / (a + 1)),
                        "peak": float(np.nanmax(ld[~pre, j])), "peak_t": float(lt[~pre][k])})
    lat.sort(key=lambda r: (-r["ratio"], r["op"]))
    add("traces", "latency_by_operation",
        "Trace latency per service operation (mean of 15-second buckets): baseline (first 10 minutes) vs the rest of the capture, with the peak (UTC).",
        [f"operation latency: {r['op']} — baseline mean {num(r['pre'])}; later mean {num(r['post'])} (x{num(r['ratio'])}); "
         f"peak {num(r['peak'])} at {ts(r['peak_t'])}" for r in lat[:10]])
    # 3) trace errors per operation
    eh, ed = read_series(z, base + "tracets_err.csv"); et = ed[:, 0]; epre = et < t0 + BASELINE_S
    efacts = []
    for j in range(1, len(eh)):
        a, b = np.nanmean(ed[epre, j]), np.nanmean(ed[~epre, j])
        if np.isfinite(b) and b > (a if np.isfinite(a) else 0) and b > 0:
            first = et[~epre][np.nan_to_num(ed[~epre, j]) > 0]
            efacts.append((-b, f"operation errors: {eh[j]} — baseline mean {num(a)}; later mean {num(b)}; first error after baseline at {ts(first[0])}"))
    efacts = [f for _, f in sorted(efacts)][:8] or ["operation errors: no operation shows more trace errors than in its baseline"]
    add("traces", "errors_by_operation", "Trace error counts per service operation (15-second buckets): baseline vs the rest of the capture.", efacts)
    # 4) application logs: volume per container and templates that appear or disappear
    vol, tmpl, levels = {}, {}, {}
    with z.open(base + "logs.csv") as fh:
        for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace")):
            tt = int(row["timestamp"]) / 1e9; late = tt >= t0 + BASELINE_S; c = row["container_name"]
            vol.setdefault(c, [0, 0])[late] += 1
            tm = tmpl.setdefault(row.get("log_template") or template(c, row["message"]), [0, 0, None, None]); tm[late] += 1
            if late and tm[2] is None: tm[2] = tt
            if not late: tm[3] = tt
            levels[row["level"].lower() or "(none)"] = levels.get(row["level"].lower() or "(none)", 0) + 1
    span_late = max(t1 - (t0 + BASELINE_S), 1) / 60
    rate = {c: (v[0] / (BASELINE_S / 60), v[1] / span_late) for c, v in vol.items()}
    ch = sorted(rate.items(), key=lambda kv: (-abs(kv[1][1] - kv[1][0]) / (kv[1][0] + 1), kv[0]))
    lfacts = [f"log volume: {c} — {num(a)} lines/min in the baseline, {num(b)} lines/min later" for c, (a, b) in ch[:8]]
    new = sorted(((v[1], k) for k, v in tmpl.items() if v[0] == 0 and v[1] > 0), reverse=True)[:4]
    gone = sorted(((v[0], k) for k, v in tmpl.items() if v[0] > 0 and v[1] == 0), reverse=True)[:4]
    lfacts += [f"log templates: new after the baseline: '{k[:120]}' — {n} lines, first at {ts(tmpl[k][2])}" for n, k in new]
    lfacts += [f"log templates: stopped after the baseline: '{k[:120]}' — {n} lines in the baseline, last at {ts(tmpl[k][3])}" for n, k in gone]
    lfacts.append("log levels: " + ", ".join(f"{k} {v}" for k, v in sorted(levels.items(), key=lambda kv: -kv[1])))
    add("service_logs", "log_volume_by_service",
        "Application log lines per container (lines per minute, baseline vs later) and log templates that appear or disappear after the baseline.", lfacts)
    # 5) pod inventory
    pods = [r for r in csv.reader(io.TextIOWrapper(z.open(base + "pod-node-1.csv"), encoding="utf-8")) if r][1:]
    pods2 = [r for r in csv.reader(io.TextIOWrapper(z.open(base + "pod-node-2.csv"), encoding="utf-8")) if r][1:] \
        if base + "pod-node-2.csv" in z.namelist() else pods
    ifacts = [f"pods: {p} on node {n}" for p, n in sorted(pods)]
    for p, n in sorted(set(map(tuple, pods2)) - set(map(tuple, pods))):
        ifacts.append(f"pods: {p} on node {n} (only in the second inventory snapshot)")
    add("infrastructure_events", "pod_inventory", "Kubernetes pod inventory: pod name and the node it runs on.", ifacts, kind="rcaeval_cluster_info")
    # 6) derived summary
    dfacts = []
    if dev:
        first = min(dev, key=lambda r: (r["onset"], -r["score"]))
        dfacts.append(f"Derived: earliest sustained metric deviation: {first['name']} from {ts(first['onset'])}.")
        scored = [r for r in dev if "appears" not in r]
        if scored:
            dfacts.append(f"Derived: metric series ranked #1 by deviation score: {scored[0]['name']} (score {num(scored[0]['score'])}).")
        for r in (r for r in dev if "appears" in r):
            dfacts.append(f"Derived: metric series without baseline data that appears during the capture: {r['name']} (from {ts(r['appears'])}).")
    if lat:
        dfacts.append(f"Derived: trace operation with the largest latency increase: {lat[0]['op']} (mean {num(lat[0]['pre'])} -> "
                      f"{num(lat[0]['post'])}, x{num(lat[0]['ratio'])}).")
    if ch:
        dfacts.append(f"Derived: container with the largest change in log volume: {ch[0][0]} ({num(ch[0][1][0])} -> {num(ch[0][1][1])} lines/min).")
    add("derived_findings", "derived_summary",
        "Deterministic summary computed from the artifacts above (metric deviation ranking and onset, trace latency ranking, log volume change).",
        dfacts, kind="derived_from_rcaeval_telemetry", heuristic=True)
    # 7) evidence gaps
    gfacts = ["No matching results for: monitoring alerts / alerting rules (no alerts were recorded in this capture). "
              "(Absence in this query is not proof of absence elsewhere.)",
              "No matching results for: change records / deployments (no change-management data in this capture). "
              "(Absence in this query is not proof of absence elsewhere.)",
              f"Disk I/O metrics contain data only for: {', '.join(disk_services)}."]
    if not any(k in levels for k in ("error", "warning", "warn", "fatal", "critical")):
        gfacts.append("No matching results for: error- or warning-level application logs (all log lines are info or debug). "
                      "(Absence in this query is not proof of absence elsewhere.)")
    add("query_coverage", "evidence_gaps", "Queries that returned nothing, and telemetry that is not collected; use these to state what is NOT established.", gfacts)

    # ------------------------------------------------------------------ questions and reference answers
    label, atom, ind = FAULTS[fault]
    rc_pods = sorted((p, n) for p, n in pods if p.startswith(service + "-"))
    top = lat[0] if lat else None
    top_role = ("root cause" if op_service(top["op"]) == service else "downstream symptom") if top else None
    when = datetime.fromtimestamp(inject, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    answers = [
        (service, [(service, "other")], "RCAEval label"),
        (", ".join(p for p, _ in rc_pods), [(p, "hostname") for p, _ in rc_pods], "pod inventory (pod-node-1.csv)"),
        (", ".join(sorted({n for _, n in rc_pods})), [(n, "hostname") for n in sorted({n for _, n in rc_pods})], "pod inventory (pod-node-1.csv)"),
        (label, [(atom, "label")], "RCAEval label"),
        ("availability", [("availability", "cia")], "all RCAEval RE2 faults degrade availability"),
        (when, [(when, "time")], "RCAEval inject_time.txt"),
        (f"{service}_{ind}", [(f"{service}_{ind}", "other")], "RCAEval label (indicator rule in RCAEval/benchmark/scoring.py)"),
        (f"{top['op']}, {top_role}" if top else "", [(top["op"], "other"), (top_role, "label")] if top else [],
         "derived from tracets_lat.csv by src/prepare_rcaeval.py"),
    ]
    lo = datetime.fromtimestamp(int(t0) // 3600 * 3600, timezone.utc); hi = datetime.fromtimestamp(-(-int(t1) // 3600) * 3600 - 1, timezone.utc)
    meta = {"incident_id": f"INC-RE2OB-{scen.rsplit('_', 1)[1]}", "scenario": scen, "title": "Microservice reliability incident investigation",
            "source": "RCAEval RE2-OB (Pham et al.; doi:10.5281/zenodo.14590730)",
            "query_window_start": lo.strftime("%Y-%m-%dT%H:%M:%S"), "query_window_end": hi.strftime("%Y-%m-%dT%H:%M:%S"),
            "evidence_types": sorted({a["artifact_type"] for a in arts}),
            "artifact_scope_note": "Evidence is aggregated query output over a 24-minute telemetry capture (not raw samples or log lines); "
                                   "it contains no chat/communication records."}
    desc = ("Reliability incident investigation of the Online Boutique microservice application on a Kubernetes (GKE) cluster. Evidence "
            "consists of aggregated query output over Prometheus container metrics (CPU, memory, disk I/O, sockets, workload, error rate, "
            "latency p50/p90), application logs and Jaeger trace statistics. No root cause, impact or trigger is stated; these must be "
            "established from the supplied artifacts. Environment context: services: " + ", ".join(services) +
            "; services call each other over gRPC; frontend is the user entry point; redis is the cart store.")
    rag = {"metadata": meta, "incident_description": desc, "investigation_questions": QUESTIONS, "artifacts": arts}
    contents = [json.loads(a["content"]) for a in arts]
    starter = {"metadata": meta, "alerts": [json.dumps(c, indent=2) for a, c in zip(arts, contents) if a["artifact_type"] == "monitoring_alerts"],
               "logs": [json.dumps(c, indent=2) for a, c in zip(arts, contents) if a["artifact_type"] != "monitoring_alerts"],
               "communications": [], "investigation_notes": [desc]}
    qa = {"source": "RCAEval RE2-OB labels (root-cause service, fault, inject time, indicator rule) and pod inventory; "
                    "question 8 is derived from the trace statistics by src/prepare_rcaeval.py",
          "confidence": "benchmark ground truth (1, 4, 5, 6, 7), telemetry lookup (2, 3), derived (8)",
          "qa": [{"id": i + 1, "question": q, "answer": a, "basis": basis, "atoms": [{"text": t, "kind": k} for t, k in at]}
                 for i, (q, (a, at, basis)) in enumerate(zip(QUESTIONS, answers))]}
    blob = (desc + "\n" + "\n".join(QUESTIONS) + "\n" + "\n".join(a["content"] for a in arts)).lower()
    from src.evaluate import atom_in
    present = {t: atom_in(t, blob) for _, at, _ in answers for t, _ in at}
    if not rc_pods:
        notes.append(f"no pod for {service} in pod-node-1.csv")
    if fault == "disk" and service not in disk_services:
        notes.append(f"indicator {service}_diskio has no data in RCAEval (disk I/O data exists only for {', '.join(disk_services)})")
    rep = {"scenario": scen, "source_case": f"{SUITE}/{case}/1", "root_cause_service": service, "fault": fault, "inject_time": ts(inject),
           "artifacts": len(arts), "facts": sum(len(c["facts"]) for c in contents), "questions": len(QUESTIONS),
           "answers": sum(1 for a in answers if a[0]), "atoms": len(present), "atoms_in_evidence": sum(present.values()),
           "atoms_not_in_evidence": sorted(t for t, ok in present.items() if not ok), "notes": notes}
    out = out_root / scen
    out.mkdir(parents=True, exist_ok=True)
    for name, obj, kw in (("rag_input.json", rag, {"indent": 2, "ensure_ascii": False}), ("starter_input.json", starter, {"indent": 2, "ensure_ascii": False}),
                          ("reference_qa.json", qa, {"indent": 2, "ensure_ascii": False}), ("cleaning_report.json", rep, {"indent": 2})):
        (out / name).write_text(json.dumps(obj, **kw) + "\n", encoding="utf-8", newline="\n")
    return rep


def write_report_section(out_root: Path, reps: list[dict]) -> None:
    md = ["# RCAEval RE2-OB (Online Boutique)", "",
          f"{len(reps)} incidents converted by `src/prepare_rcaeval.py` from RCAEval RE2-OB (Zenodo record 14590730): one repetition per "
          "root-cause service x fault type. Incident names are neutral; the source case of each is in its `cleaning_report.json`. "
          "'In evidence' = the atom string appears (case-insensitive, same matching as the evaluator) in the artifacts, questions or description; "
          "multiple-choice labels count as present because the options are in the question.", "",
          "| Scenario | Source case | Artifacts | Facts | Questions | Atoms | In evidence | Not in evidence |", "|---|---|---|---|---|---|---|---|"]
    for r in reps:
        md.append(f"| {r['scenario']} | {r['source_case']} | {r['artifacts']} | {r['facts']} | {r['questions']} | {r['atoms']} | "
                  f"{r['atoms_in_evidence']} ({100 * r['atoms_in_evidence'] // max(r['atoms'], 1)}%) | {', '.join(r['atoms_not_in_evidence']) or '-'} |")
    tot, ok = sum(r["atoms"] for r in reps), sum(r["atoms_in_evidence"] for r in reps)
    md += ["", f"**Total (RCAEval):** {ok}/{tot} atoms ({100 * ok // max(tot, 1)}%) are present in the evidence.", "",
           "Questions mirror the paper set: root-cause service, its pod and node (instead of infected host, hostname and user), fault type "
           "(multiple choice), CIA component, first-signs minute (RCAEval captures last 24 minutes, so the minute is asked instead of the hour), "
           "the RCAEval root-cause indicator `<service>_<indicator>`, and the largest trace-latency increase with 'root cause or downstream "
           "symptom' (instead of 'C2 server or legitimate service'). Question 8's reference is derived from the telemetry, not an RCAEval label."]
    f = out_root / "DATASET_REPORT.md"
    s = f.read_text(encoding="utf-8") if f.exists() else "# Dataset report\n"
    s = re.split(r"\n# RCAEval RE2-OB", s)[0].rstrip("\n") + "\n\n" + "\n".join(md) + "\n"
    f.write_text(s, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True, help="RE2-OB.zip from Zenodo record 14590730")
    ap.add_argument("--out", default="dataset/paper_dataset")
    a = ap.parse_args()
    z = zipfile.ZipFile(a.zip)
    cases = sorted({n.split("/")[1] for n in z.namelist() if n.startswith(SUITE + "/") and n.count("/") >= 3 and f"/{SUITE}/" not in n
                    and n.split("/")[2] == "1"})
    reps = []
    for i, case in enumerate(cases, 1):
        reps.append(convert(z, case, f"re2ob_{i:02d}", Path(a.out)))
        print(f"[rcaeval] {reps[-1]['scenario']} <- {case}: {reps[-1]['facts']} facts, atoms in evidence {reps[-1]['atoms_in_evidence']}/{reps[-1]['atoms']}")
    write_report_section(Path(a.out), reps)


if __name__ == "__main__":
    main()
