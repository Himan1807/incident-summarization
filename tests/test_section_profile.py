"""Offline test of --section-profile (no Ollama, no model downloads).
  * auto picks 'service_outage' for every RCAEval incident and 'security' for every security incident;
  * a security incident gives exactly the default output under auto (only the recorded 'section_profile' field is added);
  * an RCAEval incident gets the outage section plan, and none of its RAG or no-RAG prompts mention C2.
Usage: python tests/test_section_profile.py"""
import sys, io, re, json, glob, argparse, contextlib, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); __import__("os").chdir(ROOT)
sys.modules["sentence_transformers"] = None
from fakes import HashEmb
from src.pipeline_adv import run
from src.no_rag import run_no_rag
from src.sections import resolve_profile, OUTAGE_SECTIONS, SECTIONS


def echo(calls):
    def f(prompt, n=450):
        calls.append(prompt)
        ev = prompt.split("EVIDENCE:")[-1].split("Write the section now")[0] if "EVIDENCE:" in prompt else ""
        ids = re.findall(r"^\[([^\]\s]+#\d+)\]\n(.*?)(?=\n\[|\Z)", ev, re.S | re.M)
        return ("\n".join(f"- {l} [{c}]" for c, b in ids for l in b.strip().splitlines()) or "- Not established from the available artifacts."), False
    return f


def rag(sc, profile):
    calls = []
    with tempfile.TemporaryDirectory() as tmp:
        a = argparse.Namespace(input=f"dataset/paper_dataset/{sc}/rag_input.json", model="t", results_dir=tmp, dry_run=False, strict=False,
                               annotate=False, no_enrich=False, sections=None, no_postprocess=False, llm_timeline=False, section_profile=profile)
        with contextlib.redirect_stdout(io.StringIO()):
            report = run(a, embedder=HashEmb(), reranker=None, llm=echo(calls))
        rep = json.loads(next(Path(tmp).rglob("advanced_run_report.json")).read_text(encoding="utf-8"))
    rep = json.loads(re.sub(r'"seconds(_total)?": [0-9.]+', r'"seconds\1": 0', json.dumps(rep)))
    return report, rep, calls


def norag(sc, profile):
    calls = []
    with tempfile.TemporaryDirectory() as tmp:
        a = argparse.Namespace(input=f"dataset/paper_dataset/{sc}/rag_input.json", model="t", results_dir=tmp, section_profile=profile)
        with contextlib.redirect_stdout(io.StringIO()):
            run_no_rag(a, llm=lambda p, n=450: (calls.append(p), ("- Not established from the available artifacts.", False))[1])
    return calls


picked = {}
for f in sorted(glob.glob("dataset/*/*/rag_input.json")):
    meta = json.loads(Path(f).read_text(encoding="utf-8"))["metadata"]
    picked[f] = resolve_profile("auto", meta)
rca = {f: p for f, p in picked.items() if "/re2ob_" in f.replace("\\", "/")}
print("auto picks:", {p: sum(v == p for v in picked.values()) for p in set(picked.values())})
assert rca and all(p == "service_outage" for p in rca.values())
assert all(p == "security" for f, p in picked.items() if f not in rca)
assert resolve_profile(None, {}) == "security" and resolve_profile("service_outage", {}) == "service_outage"

r0, j0, c0 = rag("koi_stealer", None); r1, j1, c1 = rag("koi_stealer", "auto")
assert j1.pop("section_profile") == "security"
assert r0 == r1 and c0 == c1 and j0 == j1, "security incident must be unchanged under auto"
print("koi_stealer under auto: report, prompts and run JSON identical to the default")

r, j, calls = rag("re2ob_01", "auto")
names = [e["section"] for e in j["run_log"]]
assert names[:len(OUTAGE_SECTIONS)] == [s["name"] for s in OUTAGE_SECTIONS], names
assert j["section_profile"] == "service_outage" and "evaluation" in j
assert not any(re.search(r"\bC2\b|command-and-control", p, re.I) for p in calls), "no C2 wording for outages"
assert "root-cause service with its pod and node" in calls[-1]
assert not any(s["name"] in r for s in SECTIONS if s["name"] not in ("Timeline", "Impact Assessment", "Root Cause and Evidence Gaps",
                                                                        "Corrective and Preventive Actions"))
nr = norag("re2ob_01", "auto")
assert not any(re.search(r"\bC2\b|IP addresses, domains", p) for p in nr) and "Service Dependencies and Propagation" in nr[0]
print("re2ob_01 under auto: sections", names)
print("OK")
