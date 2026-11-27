"""Offline test of --fair-norag-evidence (no Ollama). The canned no-RAG answer states a first-contact time that exists only in the
raw-log enrichment of dataset/final_dataset/2025-01-22. Without the flag (default) that time is unsupported; with the flag the
no-RAG report is scored against the same evidence as RAG, so the time is supported.   Usage: python tests/test_fair_norag.py"""
import sys, io, json, argparse, contextlib, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); __import__("os").chdir(ROOT)
from src.no_rag import run_no_rag

INP = "dataset/final_dataset/2025-01-22/rag_input.json"
LINE = "- External IP 5.252.153.241 was first contacted at 2025-01-22 19:45:56 UTC."   # time only in the enrichment


def run(fair: bool) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        a = argparse.Namespace(input=INP, model="test-model", results_dir=tmp, fair_norag_evidence=fair)
        with contextlib.redirect_stdout(io.StringIO()):
            run_no_rag(a, llm=lambda prompt, n=450: (LINE, False))
        return json.loads(next(Path(tmp).rglob("no_rag_run_report.json")).read_text(encoding="utf-8"))


off, on = run(False), run(True)
eo, en = off["evaluation"], on["evaluation"]
print("default : unsupported", eo["unsupported_entities"], "| hallucination", eo["hallucination_rate"], "| grounding", eo["grounding_rate"])
print("fair    : unsupported", en["unsupported_entities"], "| hallucination", en["hallucination_rate"], "| grounding", en["grounding_rate"])
assert "evaluation_evidence" not in off and on["evaluation_evidence"].startswith("same as RAG")
assert any("19:45:56" in e for e in eo["unsupported_entities"]), "default: enrichment-only time must be unsupported"
assert not any("19:45:56" in e for e in en["unsupported_entities"]), "fair: the time is in the RAG evidence"
assert en["hallucination_rate"] < eo["hallucination_rate"] and en["grounding_rate"] > eo["grounding_rate"]
print("OK")
