"""Unanswerable investigation questions (RQ4): build and prove dataset/<set>/<incident>/unanswerable_qa.json.

python -m src.check_unanswerable                 # check every unanswerable_qa.json; exit 1 if any question is answerable
python -m src.check_unanswerable --write         # (re)write them: 3 per incident from the question pools below

Each question asks for a value of one ABSENT TYPE (a file hash, a registry key, a ticket number, ...). A question is accepted only
when the absent type's pattern matches nothing in the evidence the pipeline can see for that incident: the incident header
(title, window, scope, description), every chunk built from the artifacts (plus the raw-log enrichment where it exists) and the
real investigation questions. A rejected candidate is replaced by the next question in the pool; the report lists both counts.
The same patterns are used by src.evaluate.evaluate_unanswerable to detect invented values. Evaluation only: these files are
never given to retrieval or the LLM unless --with-unanswerable is used, and then only the question text.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from config import AdvancedSettings
from src.adv_chunking import chunk_artifacts
from src.adv_ingestion import load_artifacts
from src.common import incident_header
from src.enrichment import build_enrichment
from src.sections import resolve_profile

ABSENT_TYPES = {   # absent_type -> pattern of a value of that type
    "sha256": re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", re.I),
    "md5": re.compile(r"(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])", re.I),
    "registry_key": re.compile(r"\b(?:HKLM|HKCU|HKCR|HKU|HKEY_[A-Z_]+)[\\/]|CurrentVersion[\\/]+Run", re.I),
    "cve": re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.I),
    "email": re.compile(r"\b[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b"),
    "ticket": re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d{3,}\b"),
    "pid": re.compile(r"\b(?:pid|process id)\b\s*[:=#]?\s*\d+", re.I),
    "version": re.compile(r"(?<![\w.])v?\d+\.\d+\.\d+(?![\w.])", re.I),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "git_commit": re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.I),
    "kernel_version": re.compile(r"\b\d+\.\d+\.\d+-\d+[\w.-]*", re.I),
}
POOLS = {   # per section profile; questions written in the style of the real ones
    "security": [
        ("sha256", "What is the SHA256 hash of the malicious file downloaded by the potentially infected host?", "no file hashes in this incident's evidence"),
        ("registry_key", "Which Windows registry key did the malware modify to persist on the potentially infected host?", "no registry data in this incident's evidence"),
        ("cve", "Which CVE identifier was exploited for the initial infection?", "no CVE identifiers in this incident's evidence"),
        ("email", "What is the email address of the sender of the message that delivered the initial infection?", "no email addresses in this incident's evidence"),
        ("ticket", "Which ticket number was assigned to this incident in the organisation's ticketing system?", "no ticket identifiers in this incident's evidence"),
        ("md5", "What is the MD5 hash of the payload executed on the potentially infected host?", "no file hashes in this incident's evidence"),
        ("pid", "What is the process ID (PID) of the malicious process on the potentially infected host?", "no process data in this incident's evidence"),
    ],
    "service_outage": [
        ("version", "Which container image version (tag) of the root-cause service was running when the failure started?", "no image versions in this incident's evidence"),
        ("ticket", "What is the change ticket ID of the deployment that preceded the failure?", "no change or ticket identifiers in this incident's evidence"),
        ("ipv4", "What is the IP address of the Kubernetes node that hosted the pod of the root-cause service?", "no IP addresses in this incident's evidence"),
        ("email", "What is the email address of the on-call engineer who acknowledged the incident?", "no email addresses in this incident's evidence"),
        ("git_commit", "What is the full 40-character Git commit hash of the build of the root-cause service that was running?", "no commit hashes in this incident's evidence"),
        ("kernel_version", "Which Linux kernel version ran on the node that hosted the pod of the root-cause service?", "no kernel versions in this incident's evidence"),
    ],
}
PER_INCIDENT = 3


def visible_evidence(rag_input: Path) -> str:
    """Everything the pipeline can show the LLM for this incident (original case)."""
    S = AdvancedSettings()
    data = load_artifacts(str(rag_input)); meta = data["metadata"]
    arts = data["artifacts"]
    if S.enable_enrichment:
        arts = arts + build_enrichment(arts, str(rag_input.parent), meta.get("scenario", rag_input.parent.name))
    chunks = chunk_artifacts(arts, S.items_per_chunk)
    return "\n".join([incident_header(meta, data["description"])] + [c["text"] for c in chunks] + list(data.get("questions") or []))


def incidents(root: Path):
    return sorted(p.parent for p in root.glob("*/rag_input.json") if (p.parent / "reference_qa.json").exists())


def build(folder: Path, index: int) -> tuple[dict, int]:
    meta = json.loads((folder / "rag_input.json").read_text(encoding="utf-8"))["metadata"]
    profile = resolve_profile("auto", meta); pool = POOLS[profile]
    ev = visible_evidence(folder / "rag_input.json")
    chosen, rejected = [], 0
    for k in range(len(pool)):                             # rotate through the pool so incidents get different questions
        absent_type, question, why = pool[(index + k) % len(pool)]
        if ABSENT_TYPES[absent_type].search(ev):
            rejected += 1; continue                        # a value of this type exists: the question would be answerable
        chosen.append({"id": f"U{len(chosen) + 1}", "question": question, "answerable": False, "absent_type": absent_type, "why_absent": why})
        if len(chosen) == PER_INCIDENT:
            break
    if len(chosen) < PER_INCIDENT:
        raise SystemExit(f"{folder.name}: only {len(chosen)} provably unanswerable questions in the {profile} pool")
    return {"scenario": meta.get("scenario", folder.name), "section_profile": profile,
            "note": "Evaluation only. Every question asks for a value whose type does not occur anywhere in this incident's evidence "
                    "(checked by src/check_unanswerable.py).", "questions": chosen}, rejected


def check(folder: Path) -> list[str]:
    f = folder / "unanswerable_qa.json"
    if not f.exists():
        return [f"{folder.name}: unanswerable_qa.json missing"]
    ev = visible_evidence(folder / "rag_input.json"); problems = []
    for q in json.loads(f.read_text(encoding="utf-8"))["questions"]:
        m = ABSENT_TYPES[q["absent_type"]].search(ev)
        if q.get("answerable") is not False or m:
            problems.append(f"{folder.name} {q['id']} ({q['absent_type']}): answerable" + (f" - evidence contains {m.group(0)!r}" if m else ""))
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", action="append", help="dataset folder(s); default: dataset/paper_dataset")
    ap.add_argument("--write", action="store_true", help="(re)write unanswerable_qa.json for every incident")
    a = ap.parse_args(argv)
    roots = [Path(r) for r in (a.root or ["dataset/paper_dataset"])]
    folders = [f for r in roots for f in incidents(r)]
    if a.write:
        total_rej = 0; written = 0; by = {}
        for i, folder in enumerate(folders):
            doc, rej = build(folder, i)
            (folder / "unanswerable_qa.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            total_rej += rej; written += len(doc["questions"])
            for q in doc["questions"]:
                by[(doc["section_profile"], q["absent_type"])] = by.get((doc["section_profile"], q["absent_type"]), 0) + 1
            if rej:
                print(f"[unanswerable] {folder.name}: {rej} candidate(s) rejected (value present in the evidence) and replaced")
        print(f"[unanswerable] wrote {written} questions for {len(folders)} incidents; {total_rej} candidates rejected and rewritten")
        print("[unanswerable] by profile/type:", ", ".join(f"{p}/{t}={n}" for (p, t), n in sorted(by.items())))
    problems = [p for f in folders for p in check(f)]
    n = sum(len(json.loads((f / "unanswerable_qa.json").read_text(encoding="utf-8"))["questions"]) for f in folders
            if (f / "unanswerable_qa.json").exists())
    for p in problems:
        print("[unanswerable] FAIL", p)
    print(f"[unanswerable] checked {n} questions in {len(folders)} incidents: {len(problems)} answerable or missing")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
