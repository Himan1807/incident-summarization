"""Replays koi_stealer model output (with its typical defects) through the full pipeline in default mode.
Asserts: no warning tags, no TRUNCATED text, the bad IP / role error / half sentence are gone, citations are bracketed,
the Timeline is extractive (the LLM is never asked for it).   Usage: python tests/test_koi_regression.py"""
import sys, re, argparse, json, io, contextlib, zlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); __import__("os").chdir(ROOT)
from fixture_koi_model_output import RAW
from src.pipeline_adv import run

class HashEmb:
    def encode(self, texts, **k):
        out = []
        for t in texts:
            v = np.zeros(512)
            for w in re.findall(r"[\w.\-]+", t.lower()): v[zlib.crc32(w.encode()) % 512] += 1
            out.append(v / (np.linalg.norm(v) + 1e-9))
        return np.array(out)

asked = []
def canned(prompt, n=600):
    m = re.search(r"SECTION: (.+)\n", prompt)
    if "Incident Summary:" in prompt[-40:]:
        return ("The affected host is 172.17.0.99 (desktop-rnvo9at, user afletcher); the earliest alert hour was 2024-09-04 17:00 UTC "
                "and 79.124.78.197 is the main C2 candidate.", False)
    name = m.group(1).strip(); asked.append(name)
    return RAW.get(name, "- Not established from the available artifacts."), name == "Detection: IDS Alerts"   # Detection hits the token cap

a = argparse.Namespace(input=str(ROOT / "dataset/paper_dataset/koi_stealer/rag_input.json"), model="test-model", results_dir=str(ROOT / "results_test"), dry_run=False, strict=False,
                       annotate=False, no_enrich=False, sections=None, no_postprocess=False)
with contextlib.redirect_stdout(io.StringIO()):
    rep = run(a, embedder=HashEmb(), reranker=None, llm=canned)
r = json.load(open(ROOT / "results_test/koi_stealer/test-model/advanced_run_report.json"))
print(rep[:1600]); print("..."); print("eval:", {k: r["evaluation"][k] for k in ("answer_precision", "answer_recall", "faithfulness", "grounding_rate", "citation_rate")})
print("postprocessing:", {k: v for k, v in r["postprocessing"].items() if k != "removed"}, "| removed lines:", r["removed_unverified_lines"])
assert "⚠" not in rep and "TRUNCATED" not in rep, "no warning tags / truncation notes expected"
assert "172.17.17.0" not in rep, "malformed IP line must be removed"
assert "was the most-contacted external destination" not in rep, "role error must be removed"
assert not re.search(r"\(koi_stealer-\d+#\d+", rep), "citations must be bracketed"
assert "The host\n" not in rep and not rep.rstrip().endswith("The host"), "half sentence must be dropped"
assert "Timeline" not in asked, "timeline must be extractive"
assert "- 2024-09-04 17:00 UTC" in rep, "timeline entry expected"
print("OK")
