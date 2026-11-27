"""Offline test: local and hosted models have separate commands (no Ollama, no API calls; the runs are intercepted).
  python -m src.run_experiment  -> Ollama models only; a hosted model is refused with the run_api command to use
  python -m src.run_api         -> DeepInfra models only; plain ids get the 'deepinfra:' prefix; --models is required
Usage: python tests/test_run_commands.py"""
import sys, io, os, contextlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
sys.modules["sentence_transformers"] = None
from src import run_experiment as rx, run_api

calls, checked = [], []
rx.check_packages = lambda: []
rx.check_model = lambda url, m: checked.append(m) or []
rx.run = lambda ns: calls.append(("RAG", ns.model))
rx.run_no_rag = lambda ns: calls.append(("no RAG", ns.model))
rx.refresh_reports = lambda *a, **k: []
rx.write_overall_summary = rx.write_unanswerable_eval = lambda *a, **k: None


def go(fn, argv):
    calls.clear(); checked.clear(); err = io.StringIO()
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            fn(argv + ["--results", "results_cmdtest", "--force"])
        return None
    except SystemExit:
        return err.getvalue()


assert go(rx.main, ["--scenarios", "koi_stealer", "--models", "llama3.2:3b,qwen2.5:7b-instruct"]) is None
assert checked == ["llama3.2:3b", "qwen2.5:7b-instruct"] and {m for _, m in calls} == {"llama3.2:3b", "qwen2.5:7b-instruct"}
e = go(rx.main, ["--scenarios", "koi_stealer", "--models", "llama3.2:3b,deepinfra:deepseek-ai/DeepSeek-V3"])
print("run_experiment with a hosted model ->", e.strip().splitlines()[-1])
assert "python -m src.run_api --models deepseek-ai/DeepSeek-V3" in e and not calls
assert go(run_api.main, ["--scenarios", "koi_stealer", "--models", "deepseek-ai/DeepSeek-V3,deepinfra:anthropic/claude-sonnet-4-6"]) is None
print("run_api models ->", sorted({m for _, m in calls}))
assert checked == ["deepinfra:deepseek-ai/DeepSeek-V3", "deepinfra:anthropic/claude-sonnet-4-6"]
assert {m for _, m in calls} == set(checked) and {c for c, _ in calls} == {"RAG", "no RAG"}
e = go(run_api.main, ["--scenarios", "koi_stealer"])
print("run_api without --models ->", e.strip().splitlines()[-1]); assert "--models is required" in e
assert go(run_api.main, ["--reports-only"]) is None and not calls
print("OK")
