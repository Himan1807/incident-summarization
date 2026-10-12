"""Score any postmortem text file(s) with the same metrics, e.g. baseline vs advanced.

python -m src.compare --input dataset/final_dataset/2025-01-22/rag_input.json \
    --report basic_RAG_output.txt --report results/2025-01-22/advanced_postmortem.md
"""
import argparse
from pathlib import Path

from src.adv_ingestion import load_artifacts
from src.adv_chunking import chunk_artifacts
from src.enrichment import build_enrichment
from src.verify import build_corpus
from src.evaluate import evaluate_report
from config import AdvancedSettings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--report", action="append", required=True)
    a = ap.parse_args()
    inp = Path(a.input)
    data = load_artifacts(str(inp))
    arts = data["artifacts"] + build_enrichment(data["artifacts"], str(inp.parent), data["metadata"].get("scenario", "inc"))
    chunks = chunk_artifacts(arts, AdvancedSettings().items_per_chunk)
    # evidence = raw artifact text as well, so baseline output (which saw raw JSON) is judged fairly
    corpus = build_corpus(chunks, "\n".join(x["raw_text"] for x in data["artifacts"]) + data["description"])
    ids = {c["id"] for c in chunks}
    print(f"{'report':45s} ans_recall overall_recall halluc placeholders cite_rate")
    for r in a.report:
        ev = evaluate_report(Path(r).read_text(encoding="utf-8"), str(inp.parent / "reference_qa.json"), corpus, ids)
        print(f"{r[-45:]:45s} {ev['answerable_entity_recall']!s:10s} {ev['overall_entity_recall']!s:14s} "
              f"{ev['hallucination_rate']!s:7s} {ev['placeholder_count']!s:12s} {ev['citation_rate']}")
        if ev["unsupported_entities"]:
            print("   unsupported:", ev["unsupported_entities"][:8])


if __name__ == "__main__":
    main()
