"""Advanced RAG pipeline.

python -m src.pipeline_adv --input dataset/paper_dataset/koi_stealer/rag_input.json
Options: --dry-run (retrieval only) | --model llama3.2:3b | --sections 1,2 | --no-enrich | --no-postprocess
         --annotate (keep unverified lines with visible tags instead of removing them) | --strict (also remove uncited lines)
         --llm-timeline (write the Timeline with the LLM instead of extracting it from timestamped evidence)

Flow per scenario: ingest -> chunk -> hybrid retrieval + rerank per section -> LLM section (Timeline: extractive) -> clean ->
attach citations -> remove duplicates -> verify (unverifiable lines removed, logged) -> summary from verified lines -> evaluate.
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
from src.sections import build_sections
from src.adv_generation import section_prompt, summary_prompt, call_ollama
from src.postprocess import (clean_model_output, attribute_citations, dedupe_sections, drop_partial_tail,
                             drop_orphan_parents)
from src.timeline import build_timeline
from src.verify import make_evidence, sanitize, analyze_text
from src.evaluate import evaluate_report
from src.check_env import preflight
from src.reporting import model_tag, refresh_reports


def _citation_rate(text, ev, ids):
    rows = [r for r in analyze_text(text, ev, ids) if r["is_claim"]]
    return (sum(r["cited"] for r in rows), len(rows))


def run(args, embedder=None, reranker=None, llm=None):
    S = AdvancedSettings()
    if args.model:
        S.ollama_model = args.model
    post = not getattr(args, "no_postprocess", False)
    mode = "strict" if getattr(args, "strict", False) else ("annotate" if getattr(args, "annotate", False) else "drop")
    if llm is None and embedder is None:             # real run: fail early with a clear message instead of a traceback
        preflight(S.ollama_model, S.ollama_url, need_llm=not args.dry_run)
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
    chunk_text = {c["id"]: c["text"] for c in chunks}
    lo = meta.get("capture_start") or meta.get("query_window_start")
    hi = meta.get("capture_end") or meta.get("query_window_end")
    label = "Capture window" if meta.get("capture_start") else "Query time window"
    header = (f"Title: {meta.get('title')}; {label} (UTC): {lo} to {hi}; "
              f"Scope: {meta.get('artifact_scope_note', '')}\nDescription: {data['description']}")
    global_ev = make_evidence("\n".join(c["text"] for c in chunks), header)   # only used for the final evaluation
    print(f"[index] {len(artifacts)} artifacts -> {len(chunks)} chunks")

    retriever = AdvancedRetriever(chunks, S.embedding_model, S.reranker_model, embedder, reranker)
    sections = build_sections(data.get("questions"))
    chosen = sections
    if args.sections:
        keep = {int(x) - 1 for x in args.sections.split(",")}
        chosen = [s for i, s in enumerate(sections) if i in keep]
    names = [s["name"] for s in sections]

    gen = llm or (lambda p, n: call_ollama(p, S.ollama_url, S.ollama_model, S.temperature,
                                           S.timeout_seconds, S.num_ctx, n))
    # ------------------------------------------------------------------ phase 1: retrieve + generate + clean + attribute
    work, run_log = [], []
    for sec in chosen:
        t0 = time.time()
        # ---- extractive timeline: no LLM call
        if sec.get("extractive") == "timeline" and not getattr(args, "llm_timeline", False) and not args.dry_run:
            tl_text, tl_ids = build_timeline(chunks)
            if tl_text:
                tl_chunks = [c for c in chunks if c["id"] in set(tl_ids)]
                work.append({"sec": sec, "text": tl_text, "ids": set(tl_ids),
                             "ev": make_evidence("\n".join(c["text"] for c in tl_chunks), header), "dropped_tail": None})
                run_log.append({"section": sec["name"], "retrieved": tl_ids, "extractive": True, "seconds": 0.0,
                                "claims": tl_text.count("\n") + 1, "model_cited_claims": tl_text.count("\n") + 1})
                print(f"[gen] {sec['name']} (extractive, {len(tl_ids)} chunks, no LLM call)")
                continue
        if sec.get("per_query_k"):                       # one retrieval + rerank PER question, then merge (no crowding out)
            seen, hits, used = set(), [], 0
            for q in sec["queries"]:
                for h in retriever.retrieve([q], q, S.bm25_top_k, S.dense_top_k, S.rrf_k, sec["per_query_k"], 10 ** 9):
                    cid = h["chunk"]["id"]
                    if cid not in seen and used + len(h["chunk"]["text"]) <= sec.get("max_chars", S.max_context_chars):
                        seen.add(cid); hits.append(h); used += len(h["chunk"]["text"])
        else:
            hits = retriever.retrieve(sec["queries"], sec["rerank"], S.bm25_top_k, S.dense_top_k,
                                      S.rrf_k, sec.get("top_k", S.rerank_top_k), sec.get("max_chars", S.max_context_chars))
        ids = [h["chunk"]["id"] for h in hits]
        evidence = "\n\n".join(f"[{h['chunk']['id']}]\n{h['chunk']['body']}" for h in hits)
        entry = {"section": sec["name"], "retrieved": ids}
        if args.dry_run:
            print(f"\n=== {sec['name']} -> {ids}")
            run_log.append(entry); continue
        n_tok = S.num_predict_long if sec.get("long") else S.num_predict
        raw, truncated = gen(section_prompt(sec, evidence, header, ids, names), n_tok)
        sec_chunks = [h["chunk"] for h in hits]
        sec_ev = make_evidence("\n".join(c["text"] for c in sec_chunks), header)
        dropped = None
        if truncated:                                    # remove the unfinished last line instead of showing a half sentence
            raw, dropped = drop_partial_tail(raw)
        text = clean_model_output(raw, sec["name"]) if post else raw
        pre_cited, n_claims = _citation_rate(text, sec_ev, set(ids))
        attributed = bad_cites = 0
        if post:
            text, attributed, bad_cites = attribute_citations(text, sec_chunks, set(ids))
        work.append({"sec": sec, "text": text, "ids": set(ids), "ev": sec_ev, "dropped_tail": dropped})
        entry.update(seconds=round(time.time() - t0, 1), truncated=truncated, dropped_partial_line=dropped,
                     model_cited_claims=pre_cited, claims=n_claims, auto_attributed_lines=attributed,
                     invalid_citations_removed=bad_cites)
        run_log.append(entry)
        print(f"[gen] {sec['name']} ({entry['seconds']}s){' - hit token cap, partial last line dropped' if truncated else ''}")

    if args.dry_run:
        return None

    # ------------------------------------------------------------------ phase 2: dedupe, verify, summary
    texts = {w["sec"]["name"]: w["text"] for w in work}
    removed = []
    if post:
        embed = (lambda xs: retriever.embedder.encode(xs, normalize_embeddings=True, show_progress_bar=False))
        texts, removed = dedupe_sections(texts, embed=embed)
    report_parts, clean_parts, all_flags, used_ids = [], [], [], set()
    for w, entry in zip(work, run_log):
        name = w["sec"]["name"]
        text, flags, clean = sanitize(texts[name], w["ev"], w["ids"], mode=mode)
        if mode == "drop":
            text, clean = drop_orphan_parents(text), drop_orphan_parents(clean)
        used_ids |= w["ids"]
        all_flags += [{"section": name, **f} for f in flags]
        report_parts.append(f"## {name}\n\n{text}\n")
        clean_parts.append(f"## {name}\n{clean}")
        counts = {}
        for f in flags:
            for t in f["types"]:
                counts[t] = counts.get(t, 0) + 1
        entry["flag_counts"] = counts
        print(f"[verified] {name}: {counts or 'no flags'}")

    body = "\n".join(report_parts)
    clean_body = "\n\n".join(clean_parts)
    summ_raw, summ_trunc = gen(summary_prompt(header, clean_body), S.num_predict)
    if summ_trunc:
        summ_raw, _ = drop_partial_tail(summ_raw)
    summ_ev = make_evidence(clean_body, header)
    summ_text = clean_model_output(summ_raw, "Incident Summary") if post else summ_raw
    if post:
        all_chunks = [c for c in chunks if c["id"] in used_ids]
        summ_text, _, _ = attribute_citations(summ_text, all_chunks, used_ids)
    summ, flags, _ = sanitize(summ_text, summ_ev, used_ids, mode=mode)
    all_flags += [{"section": "Incident Summary", **f} for f in flags]

    n_removed = sum(1 for f in all_flags if f["action"] == "removed")
    n_uncited = sum(1 for f in all_flags if "uncited" in f["types"] and f["action"] == "kept")
    foot = ""
    if mode == "drop" and (n_removed or n_uncited):
        foot = (f"\n---\nVerification note: {n_removed} line(s) were removed because their entities, numbers or citations could not be "
                f"verified against the retrieved evidence; {n_uncited} claim(s) remain without a citation. Details: advanced_run_report.json.\n")
    report = f"# Incident Postmortem: {meta.get('title', scenario)}\n\n## Incident Summary\n\n{summ}\n\n{body}{foot}"

    results_dir = getattr(args, "results_dir", "results")
    out_dir = Path(results_dir) / scenario / model_tag(S.ollama_model)      # results/<incident>/<model>/
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "advanced_postmortem.md").write_text(report, encoding="utf-8")
    totals = {}
    for f in all_flags:
        for t in f["types"]:
            totals[t] = totals.get(t, 0) + 1
    mc = sum(e.get("model_cited_claims", 0) for e in run_log)
    nc = sum(e.get("claims", 0) for e in run_log)
    result = {"condition": "rag", "model": S.ollama_model, "scenario": scenario,
              "seconds_total": round(sum(e.get("seconds", 0) for e in run_log), 1),
              "verification_totals": totals, "mode": mode, "removed_unverified_lines": n_removed,
              "postprocessing": {"enabled": post, "model_citation_rate_before_attribution": round(mc / nc, 3) if nc else None,
                                 "auto_attributed_lines": sum(e.get("auto_attributed_lines", 0) for e in run_log),
                                 "invalid_citations_removed": sum(e.get("invalid_citations_removed", 0) for e in run_log),
                                 "partial_lines_dropped": sum(1 for e in run_log if e.get("dropped_partial_line")),
                                 "duplicate_lines_removed": len(removed),
                                 "removed": [{"section": s, "line": l, "duplicate_of": d} for s, l, d in removed]},
              "run_log": run_log, "flagged": all_flags}
    qa = folder / "reference_qa.json"
    if qa.exists():                                        # evaluation only, never given to the LLM
        result["evaluation"] = evaluate_report(report, str(qa), global_ev, valid_ids, chunk_text)
    (out_dir / "advanced_run_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    written = refresh_reports(scenario, results_dir)         # qa_evaluation_*.txt, rag_vs_no_rag.txt, model_comparison.txt
    print(report)
    if "evaluation" in result:
        ev = result["evaluation"]
        keys = ("answer_precision", "answer_recall", "answer_f1", "question_recall", "faithfulness", "grounding_rate",
                "citation_precision", "citation_rate", "hallucination_rate", "unsupported_number_count", "placeholder_count")
        print("\n[eval]", {k: ev[k] for k in keys})
        print("[verify] mode:", mode, "| flagged by type:", totals or "none", "| removed:", n_removed,
              "| model-cited before attribution:", result["postprocessing"]["model_citation_rate_before_attribution"],
              "| auto-attributed:", result["postprocessing"]["auto_attributed_lines"],
              "| duplicates removed:", len(removed))
        print("[reports]", *written, sep="\n   ")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true", help="retrieval only; no LLM calls")
    ap.add_argument("--annotate", action="store_true", help="keep unverified lines with visible tags instead of removing them")
    ap.add_argument("--strict", action="store_true", help="remove every flagged line, including uncited ones")
    ap.add_argument("--llm-timeline", action="store_true", help="write the Timeline with the LLM instead of extracting it")
    ap.add_argument("--no-enrich", action="store_true")
    ap.add_argument("--no-postprocess", action="store_true", help="disable cleaning, citation attribution and de-duplication")
    ap.add_argument("--sections", default=None, help="e.g. 2,4 to run a subset")
    ap.add_argument("--results-dir", default="results", dest="results_dir", help="output folder (default: results)")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
