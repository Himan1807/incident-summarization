"""Offline test of the experiment features (no Ollama, no model downloads):
  1) RAG vs no-RAG for the same LLM, 2) per-incident question/answer/reference tables, 3) multi-model comparison.
Two stand-in 'models' are run on koi_stealer; the test checks that all report files are written and contain the expected tables.
Usage: python tests/test_experiment_reports.py"""
import sys, re, argparse, io, contextlib, zlib, shutil
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); __import__("os").chdir(ROOT)
from fixture_koi_model_output import RAW
from src.pipeline_adv import run
from src.no_rag import run_no_rag
from src.reporting import refresh_reports, write_overall_summary

class HashEmb:
    def encode(self, texts, **k):
        out = []
        for t in texts:
            v = np.zeros(512)
            for w in re.findall(r"[\w.\-]+", t.lower()): v[zlib.crc32(w.encode()) % 512] += 1
            out.append(v / (np.linalg.norm(v) + 1e-9))
        return np.array(out)

def rag_llm(good):
    def f(prompt, n=600):
        if "Incident Summary:" in prompt[-40:]: return "The affected host is 172.17.0.99 (desktop-rnvo9at, user afletcher).", False
        name = re.search(r"SECTION: (.+)\n", prompt).group(1).strip()
        if good: return RAW.get(name, "- Not established from the available artifacts."), False
        if name == "Answers to Investigation Questions":
            return "1. 172.17.0.99 [koi_stealer-08#0]\n2. Not established from the available artifacts.\n3. Not established from the available artifacts.", False
        return "- Not established from the available artifacts.", False
    return f

def norag_llm(prompt, n=600):                                   # an LLM without evidence: plausible but invented specifics
    if "Incident Summary:" in prompt[-40:]: return "A Windows client was infected by a stealer and contacted 203.0.113.7.", False
    name = re.search(r"SECTION: (.+)\n", prompt).group(1).strip()
    if name == "Answers to Investigation Questions":
        return ("1. 192.168.1.50\n2. DESKTOP-ABC123\n3. jsmith\n4. malware-download.example.com\n5. 203.0.113.7\n"
                "6. Confidentiality\n7. 2024-09-04 09:00 UTC\n8. 203.0.113.7, a C2 server"), False
    return "- The infected host 192.168.1.50 contacted 203.0.113.7 on port 443.", False

res = ROOT / "results_test"
shutil.rmtree(res, ignore_errors=True)
for model, good in (("model-a", True), ("model-b", False)):
    ns = argparse.Namespace(input=str(ROOT / "dataset/paper_dataset/koi_stealer/rag_input.json"), model=model, results_dir=str(res), dry_run=False,
                            strict=False, annotate=False, no_enrich=False, sections=None, no_postprocess=False)
    with contextlib.redirect_stdout(io.StringIO()):
        run(ns, embedder=HashEmb(), reranker=None, llm=rag_llm(good))
        run_no_rag(ns, llm=norag_llm)
files = {p.relative_to(res).as_posix() for p in res.rglob("*.txt")}
print(sorted(files))
need = {"koi_stealer/model-a/qa_evaluation_rag.txt", "koi_stealer/model-a/qa_evaluation_no_rag.txt", "koi_stealer/model-a/rag_vs_no_rag.txt",
        "koi_stealer/model-b/rag_vs_no_rag.txt", "koi_stealer/model_comparison.txt"}
assert need <= files, f"missing files: {need - files}"
assert (res / "koi_stealer/model-a/no_rag_postmortem.md").exists() and (res / "koi_stealer/model-a/advanced_postmortem.md").exists()
print("summary:", write_overall_summary(str(res)))
for f in ("koi_stealer/model-a/rag_vs_no_rag.txt", "koi_stealer/model_comparison.txt"):
    print("\n----", f); print((res / f).read_text(encoding="utf-8"))
qa = (res / "koi_stealer/model-a/qa_evaluation_rag.txt").read_text(encoding="utf-8")
assert "Reference answer" in qa and "Answer from the report" in qa and "Answer precision" in qa and "172.17.0.99" in qa
cmp_ = (res / "koi_stealer/model_comparison.txt").read_text(encoding="utf-8")
assert all(x in cmp_ for x in ("model-a (RAG)", "model-a (no RAG)", "model-b (RAG)", "model-b (no RAG)", "Best answer F1"))
print("OK")
