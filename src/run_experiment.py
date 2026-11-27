"""Run incidents x models x conditions (RAG and no RAG) and build every text report.

python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b
python -m src.run_experiment --scenarios koi_stealer,easy_123 --models llama3.2:3b,llama3.1:8b-instruct-q4_K_M
python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b --skip-no-rag      # RAG only
python -m src.run_experiment --reports-only                                                  # rebuild text reports, no LLM
python -m src.run_experiment --models llama3.2:3b,qwen2.5:7b-instruct --with-unanswerable --section-profile auto   # RQ4

Results are stored in results/<incident>/<model>/ and are resumable: finished runs are skipped unless --force is given.
Reports: results/<incident>/<model>/{qa_evaluation_rag.txt, qa_evaluation_no_rag.txt, rag_vs_no_rag.txt},
         results/<incident>/model_comparison.txt, results/summary.txt
"""
import argparse
import json
import traceback
from pathlib import Path

from config import AdvancedSettings
from src.check_env import check_ollama, check_packages
from src.no_rag import run_no_rag
from src.pipeline_adv import run
from src.reporting import model_tag, refresh_reports, write_overall_summary, write_unanswerable_eval


def _has_rq4(path: Path) -> bool:                        # a finished RAG run without RQ4 answers is re-run with --with-unanswerable
    try:
        return "unanswerable" in json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False


def main(argv=None):
    S = AdvancedSettings()
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="dataset/paper_dataset")
    ap.add_argument("--results", default="results")
    ap.add_argument("--scenarios", default=None, help="comma-separated incidents (default: all in --root)")
    ap.add_argument("--models", default=S.ollama_model, help="comma-separated Ollama models, e.g. llama3.2:3b,llama3.1:8b-instruct-q4_K_M")
    ap.add_argument("--skip-rag", action="store_true")
    ap.add_argument("--skip-no-rag", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-run finished runs")
    ap.add_argument("--reports-only", action="store_true", help="only rebuild the text reports from stored results")
    ap.add_argument("--annotate", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--fair-norag-evidence", action="store_true", help="score no-RAG against the same evidence as RAG (with enrichment)")
    ap.add_argument("--with-unanswerable", action="store_true",
                    help="RQ4: RAG runs also answer unanswerable_qa.json in a separate section; writes results/unanswerable_eval.txt")
    ap.add_argument("--section-profile", default=None, choices=["auto", "security", "service_outage"],
                    help="section plan for RAG and no-RAG; auto = service_outage for operational incidents (e.g. RCAEval); default: security")
    a = ap.parse_args(argv)
    root, results = Path(a.root), Path(a.results)
    names = a.scenarios.split(",") if a.scenarios else sorted(p.name for p in root.iterdir() if (p / "rag_input.json").exists())
    models = [m.strip() for m in a.models.split(",") if m.strip()]

    if not a.reports_only:                                  # fail early, before hours of generation
        problems = check_packages()
        for m in models:
            problems += check_ollama(S.ollama_url, m)
        if problems:
            raise SystemExit("\nSetup problem(s):\n  - " + "\n  - ".join(problems))
        for sc in names:
            for m in models:
                out = results / sc / model_tag(m)
                ns = argparse.Namespace(input=str(root / sc / "rag_input.json"), model=m, dry_run=False, strict=a.strict, annotate=a.annotate,
                                        llm_timeline=False, no_enrich=False, no_postprocess=False, sections=None, results_dir=a.results,
                                        fair_norag_evidence=a.fair_norag_evidence, section_profile=a.section_profile,
                                        with_unanswerable=a.with_unanswerable)
                for cond, skip, fname, fn in (("RAG", a.skip_rag, "advanced_run_report.json", run),
                                              ("no RAG", a.skip_no_rag, "no_rag_run_report.json", run_no_rag)):
                    if skip:
                        continue
                    if (out / fname).exists() and not a.force and not (cond == "RAG" and a.with_unanswerable and not _has_rq4(out / fname)):
                        print(f"[skip] {sc} / {m} / {cond} (finished; use --force to re-run)"); continue
                    print(f"\n########## {sc} | {m} | {cond}")
                    try:
                        fn(ns)
                    except Exception:                       # one failing run must not stop the whole experiment
                        print(f"[error] {sc} / {m} / {cond} failed:\n{traceback.format_exc()}")
    for sc in names:
        for w in refresh_reports(sc, a.results):
            print("[report]", w)
    for w in (write_overall_summary(a.results), write_unanswerable_eval(a.results)):
        if w:
            print("[report]", w)


if __name__ == "__main__":
    main()
