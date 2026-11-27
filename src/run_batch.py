"""Run the advanced (RAG) pipeline over several scenarios. Thin wrapper around src.run_experiment (kept for old commands).

python -m src.run_batch --root dataset/paper_dataset --scenarios koi_stealer,fake_auth,easy_123 --model llama3.2:3b
python -m src.run_batch --root dataset/paper_dataset            # all scenarios (slow on CPU: ~35-40 min each with the 8B model)

Same as: python -m src.run_experiment --root ... --scenarios ... --models <model> --skip-no-rag [--strict] [--force]
Results go to results/<incident>/<model>/ with all text reports and results/summary.txt (see docs/EXPERIMENTS.md).
"""
import argparse

from src import run_experiment


def to_experiment_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="dataset/paper_dataset")
    ap.add_argument("--scenarios", default=None, help="comma-separated; default: all")
    ap.add_argument("--model", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-run scenarios that already have results")
    a = ap.parse_args(argv)
    out = ["--root", a.root, "--skip-no-rag"]           # run_batch only ever ran the RAG condition
    if a.scenarios:
        out += ["--scenarios", a.scenarios]
    if a.model:
        out += ["--models", a.model]
    if a.strict:
        out.append("--strict")
    if a.force:
        out.append("--force")
    return out


def main(argv=None):
    run_experiment.main(to_experiment_args(argv))


if __name__ == "__main__":
    main()
