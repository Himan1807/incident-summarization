"""End-to-end regression on REAL model output (llama3.2:3b on easy_123): the canned LLM returns exactly what the model wrote.
Checks that post-processing removes duplicate headings/question echoes, wrong citation ids and most UNCITED/UNVERIFIED tags.
Usage: python tests/test_postprocess_regression.py   (no Ollama, no model downloads)"""
import sys, re, argparse, json, io, contextlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); __import__("os").chdir(ROOT)
from fixture_easy123_model_output import RAW
from src.pipeline_adv import run

class HashEmb:
    def encode(self, texts, **k):
        out = []
        for t in texts:
            v = np.zeros(512)
            for w in re.findall(r"[\w.\-]+", t.lower()): v[hash(w) % 512] += 1
            out.append(v / (np.linalg.norm(v) + 1e-9))
        return np.array(out)

SUMMARY = ("Here is the Incident Summary:\nThe affected host was 10.2.28.88 (desktop-teyq2nr) with user account brolf. "
           "The earliest alert hour was 2026-02-28T19:00:00 UTC, and 45.131.214.85 was the most contacted external IP (1061 connections).")

def canned(prompt, n=600):
    m = re.search(r"SECTION: (.+)\n", prompt)
    if "Incident Summary:" in prompt[-40:]: return SUMMARY, False
    return RAW.get(m.group(1).strip(), "- Not established from the available artifacts."), False

def go(post):
    a = argparse.Namespace(input=str(ROOT / "dataset/paper_dataset/easy_123/rag_input.json"), model=None, dry_run=False,
                           strict=False, no_enrich=False, sections=None, no_postprocess=not post)
    with contextlib.redirect_stdout(io.StringIO()):
        rep = run(a, embedder=HashEmb(), reranker=None, llm=canned)
    r = json.load(open(ROOT / "results/easy_123/advanced_run_report.json"))
    return rep, r

rep0, r0 = go(False); rep1, r1 = go(True)
keys = ("faithfulness", "grounding_rate", "citation_rate", "answer_precision", "answer_recall", "answer_f1")
print("%-18s %10s %10s" % ("", "raw model", "post-processed"))
for k in keys: print("%-18s %10s %10s" % (k, r0["evaluation"][k], r1["evaluation"][k]))
print("flag totals  raw:", r0["verification_totals"], "\n             post:", r1["verification_totals"])
print("postprocessing:", {k: v for k, v in r1["postprocessing"].items() if k != "removed"})
assert sum(r1["verification_totals"].values()) < sum(r0["verification_totals"].values()) / 2, "post-processing should halve the flags"
assert "2025-01-22" not in rep1, "wrong citation ids must be gone"
print("OK")
