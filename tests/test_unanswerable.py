"""Offline test of RQ4 (--with-unanswerable): no Ollama, stand-in embedder, canned LLM with known answers.
Per incident the canned LLM answers real question 1 with its reference answer and abstains on the other real questions; on the three
unanswerable questions it abstains (U1), invents a value of the asked type (U2) and answers 'Unknown.' (U3). Checked:
  * scores: correct abstention 1/3, invention 1/3, other 1/3; over-abstention = abstained answerable real questions / answerable ones;
  * removed_by_fact_check is true exactly when the invented value is missing from the published section;
  * the real evaluation, run log and report are identical with and without the option (the new section is only appended);
  * results/unanswerable_eval.txt is written with both domains and a McNemar table.   Usage: python tests/test_unanswerable.py"""
import sys, io, re, json, argparse, contextlib, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); __import__("os").chdir(ROOT)
sys.modules["sentence_transformers"] = None
from fakes import HashEmb
from src.pipeline_adv import run
from src.evaluate import answer_blocks
from src.reporting import write_unanswerable_eval

INVENTED = {"sha256": "5d41402abc4b2a76b9719d911017c592a1b2c3d4e5f60718293a4b5c6d7e8f90", "md5": "5d41402abc4b2a76b9719d911017c592",
            "registry_key": "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\\\\updater", "cve": "CVE-2023-23397",
            "email": "it-support@helpdesk-mail.net", "ticket": "INC-48213", "pid": "PID 4242", "version": "v1.4.2", "ipv4": "10.20.30.40",
            "git_commit": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3", "kernel_version": "5.15.0-1049-gke"}


def canned(sc, model):
    ref = json.loads((ROOT / f"dataset/paper_dataset/{sc}/reference_qa.json").read_text(encoding="utf-8"))["qa"]
    uq = json.loads((ROOT / f"dataset/paper_dataset/{sc}/unanswerable_qa.json").read_text(encoding="utf-8"))["questions"]
    def f(prompt, n=450):
        sec = re.search(r"SECTION: (.+)\n", prompt)
        ids = re.findall(r"^\[([^\]\s]+#\d+)\]$", prompt.split("EVIDENCE:")[-1], re.M)
        cite = f" [{ids[0]}]" if ids else ""
        if sec and sec.group(1).strip() == "Answers to Investigation Questions":
            return "\n".join([f"1. {ref[0]['answer']}{cite}"] + [f"{i}. Not established from the available artifacts." for i in range(2, len(ref) + 1)]), False
        if sec and sec.group(1).strip() == "Additional Investigation Questions":
            inv = INVENTED[uq[1]["absent_type"]] if model == "model-a" else "Not established from the available artifacts."
            return f"1. Not established from the available artifacts.\n2. {inv}{cite}\n3. Unknown.", False
        return (f"- Not established from the available artifacts.", False)
    return f


def go(sc, tmp, rq4, model="model-a"):
    a = argparse.Namespace(input=f"dataset/paper_dataset/{sc}/rag_input.json", model=model, results_dir=tmp, dry_run=False, strict=False,
                           annotate=False, no_enrich=False, sections=None, no_postprocess=False, llm_timeline=False,
                           section_profile="auto", with_unanswerable=rq4)
    with contextlib.redirect_stdout(io.StringIO()):
        rep = run(a, embedder=HashEmb(), reranker=None, llm=canned(sc, model))
    j = json.loads((Path(tmp) / sc / model / "advanced_run_report.json").read_text(encoding="utf-8"))
    md = (Path(tmp) / sc / model / "advanced_postmortem.md").read_text(encoding="utf-8")
    return rep, json.loads(re.sub(r'"seconds(_total)?": [0-9.]+', r'"seconds\1": 0', json.dumps(j))), md


with tempfile.TemporaryDirectory() as t0, tempfile.TemporaryDirectory() as t1:
    for sc in ("koi_stealer", "re2ob_01"):
        _, j0, md0 = go(sc, t0, False)
        _, j1, md1 = go(sc, t1, True)
        go(sc, t1, True, model="model-b")                   # a second model that never invents, for the McNemar table
        u = j1.pop("unanswerable")
        assert j0 == j1, f"{sc}: the real evaluation / run log must not change"
        assert md1.startswith(md0) and md1[len(md0):].startswith("## Additional Investigation Questions"), "section only appended"
        assert answer_blocks(md1) == answer_blocks(md0), "U-answers must not be read as real answers"
        st = [q["raw_status"] for q in u["per_question"]]
        print(sc, "| domain", u["domain"], "| statuses", st, "| rates", {k: u[k] for k in ("correct_abstention_rate", "invention_rate",
              "invention_rate_after_fact_check", "invented_removed_by_fact_check", "over_abstention_rate", "answerable_questions")})
        assert st == ["ABSTAINED", "INVENTED", "OTHER"] and u["correct_abstention_rate"] == u["invention_rate"] == u["other_rate"] == 0.333
        q2 = u["per_question"][1]; section = md1[len(md0):]
        assert q2["removed_by_fact_check"] == (INVENTED[q2["absent_type"]].replace("\\\\", "\\") not in section.replace("\\\\", "\\"))
        real = [r for r in j0["evaluation"]["per_question"] if r.get("atoms")]
        ans = [r for r in real if set(r["atoms"]) <= set(r["answerable_from_evidence"])]
        assert u["answerable_questions"] == len(ans) and u["over_abstention_rate"] == round(sum(r["status"] == "ABSTAINED" for r in ans) / len(ans), 3)
        assert ans and ans[0]["id"] != 1 or real[0]["status"] in ("CORRECT", "PARTIAL"), "question 1 is answered, not abstained"
    p = write_unanswerable_eval(t1); txt = Path(p).read_text(encoding="utf-8")
    assert "| model-a" in txt and "security" in txt and "outage" in txt and "B. McNEMAR" in txt and "model-b" in txt
    print("\n".join(l for l in txt.splitlines() if l.startswith("| model-")))
print("OK")
