"""Run the advanced pipeline over several scenarios and write results/summary.md (resumable).

python -m src.run_batch --root dataset/paper_dataset --scenarios koi_stealer,fake_auth,easy_123 --model llama3.2:3b
python -m src.run_batch --root dataset/paper_dataset            # all scenarios (slow on CPU: ~35-40 min each with the 8B model)
"""
import argparse
import json
import traceback
from pathlib import Path

from src.pipeline_adv import run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="dataset/paper_dataset")
    ap.add_argument("--scenarios", default=None, help="comma-separated; default: all")
    ap.add_argument("--model", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-run scenarios that already have results")
    a = ap.parse_args()
    root = Path(a.root)
    names = a.scenarios.split(",") if a.scenarios else sorted(p.name for p in root.iterdir() if (p / "rag_input.json").exists())
    for sc in names:
        rep = Path("results") / sc / "advanced_run_report.json"
        if rep.exists() and not a.force:
            print(f"[skip] {sc} (results exist; use --force)"); continue
        print(f"\\n########## {sc}")
        ns = argparse.Namespace(input=str(root / sc / "rag_input.json"), model=a.model, dry_run=False, strict=a.strict,
                                no_enrich=False, sections=None)
        try:
            run(ns)
        except Exception:                                  # keep going: one failing scenario must not stop the batch
            print(f"[error] {sc} failed:\\n{traceback.format_exc()}")
    rows, keys = [], ("answer_precision", "answer_recall", "answer_f1", "question_recall", "faithfulness", "grounding_rate",
                      "citation_precision", "citation_rate", "hallucination_rate", "unsupported_number_count", "placeholder_count")
    for sc in names:
        f = Path("results") / sc / "advanced_run_report.json"
        if f.exists():
            ev = json.loads(f.read_text(encoding="utf-8")).get("evaluation")
            if ev:
                rows.append((sc, [ev[k] for k in keys]))
    if rows:
        md = ["| Scenario | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
        md += [f"| {sc} | " + " | ".join(str(v) for v in vals) + " |" for sc, vals in rows]
        means = [sum(float(r[1][i] or 0) for r in rows) / len(rows) for i in range(len(keys))]   # None counts as 0
        md.append("| **mean** | " + " | ".join(f"{m:.3f}" for m in means) + " |")
        Path("results").mkdir(exist_ok=True)
        Path("results/summary.md").write_text("\\n".join(md), encoding="utf-8")
        print("\\n" + "\\n".join(md))


if __name__ == "__main__":
    main()
