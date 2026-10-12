"""Advanced RAG pipeline.

python -m src.pipeline_adv --input dataset/final_dataset/2025-01-22/rag_input.json
Options: --dry-run (retrieval only, no LLM) | --strict | --model llama3.2:3b | --no-enrich | --sections 1,2
"""
import argparse
import json
import time
from pathlib import Path

from config import AdvancedSettings
from src.adv_ingestion import load_artifacts
from src.adv_chunking import chunk_artifacts
from src.enrichment import build_enrichment
from src.adv_retrieval import AdvancedRetriever
from src.sections import SECTIONS
from src.adv_generation import section_prompt, summary_prompt, call_ollama
from src.verify import build_corpus, sanitize
from src.evaluate import evaluate_report


def run(args, embedder=None, reranker=None, llm=None):
    S = AdvancedSettings()
    if args.model:
        S.ollama_model = args.model
    inp = Path(args.input)
    folder = inp.parent
    data = load_artifacts(str(inp))
    meta, artifacts = data["metadata"], data["artifacts"]
    scenario = meta.get("scenario", folder.name)

    if S.enable_enrichment and not args.no_enrich:
        extra = build_enrichment(artifacts, str(folder), scenario)
        artifacts += extra
        print(f"[enrich] added {len(extra)} artifact(s) from raw logs")

    chunks = chunk_artifacts(artifacts, S.items_per_chunk)
    valid_ids = {c["id"] for c in chunks}
    header = (f"Title: {meta.get('title')}; Capture window (UTC): {meta.get('capture_start')} to {meta.get('capture_end')}; "
              f"Scope: {meta.get('artifact_scope_note', '')}\nDescription: {data['description']}")
    corpus = build_corpus(chunks, header)
    print(f"[index] {len(artifacts)} artifacts -> {len(chunks)} chunks")

    retriever = AdvancedRetriever(chunks, S.embedding_model, S.reranker_model, embedder, reranker)
    chosen = SECTIONS
    if args.sections:
        keep = {int(x) - 1 for x in args.sections.split(",")}
        chosen = [s for i, s in enumerate(SECTIONS) if i in keep]

    gen = llm or (lambda p: call_ollama(p, S.ollama_url, S.ollama_model, S.temperature,
                                        S.timeout_seconds, S.num_ctx, S.num_predict))
    report_parts, run_log, all_flags = [], [], []
    for sec in chosen:
        t0 = time.time()
        hits = retriever.retrieve(sec["queries"], sec["rerank"], S.bm25_top_k, S.dense_top_k,
                                  S.rrf_k, S.rerank_top_k, S.max_context_chars)
        evidence = "\n\n".join(f"[{h['chunk']['id']}]\n{h['chunk']['body']}" for h in hits)
        entry = {"section": sec["name"], "retrieved": [h["chunk"]["id"] for h in hits]}
        if args.dry_run:
            print(f"\n=== {sec['name']} -> {entry['retrieved']}")
            run_log.append(entry); continue
        raw = gen(section_prompt(sec, evidence, header))
        text, flags = sanitize(raw, corpus, valid_ids, strict=args.strict)
        all_flags += [{"section": sec["name"], **f} for f in flags]
        report_parts.append(f"## {sec['name']}\n\n{text}\n")
        entry.update(seconds=round(time.time() - t0, 1), flagged_lines=len(flags))
        run_log.append(entry)
        print(f"[done] {sec['name']} ({entry['seconds']}s, {len(flags)} flagged)")

    if args.dry_run:
        return None
    body = "\n".join(report_parts)
    summ_raw = gen(summary_prompt(header, body))
    summ, flags = sanitize(summ_raw, corpus, valid_ids, strict=args.strict)
    all_flags += [{"section": "Incident Summary", **f} for f in flags]
    report = f"# Incident Postmortem: {meta.get('title', scenario)}\n\n## Incident Summary\n\n{summ}\n\n{body}"

    out_dir = Path("results") / scenario
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "advanced_postmortem.md").write_text(report, encoding="utf-8")
    result = {"run_log": run_log, "flagged": all_flags}
    qa = folder / "reference_qa.json"
    if qa.exists():                                        # evaluation only, never given to the LLM
        result["evaluation"] = evaluate_report(report, str(qa), corpus, valid_ids)
    (out_dir / "advanced_run_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(report)
    if "evaluation" in result:
        ev = result["evaluation"]
        print("\n[eval]", {k: ev[k] for k in ("answerable_entity_recall", "overall_entity_recall",
                                              "hallucination_rate", "placeholder_count", "citation_rate")})
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true", help="retrieval only; no LLM calls")
    ap.add_argument("--strict", action="store_true", help="drop unverified lines instead of flagging")
    ap.add_argument("--no-enrich", action="store_true")
    ap.add_argument("--sections", default=None, help="e.g. 2,4 to run a subset")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
