# Advanced RAG for incident postmortems (CPU-friendly)

Adds a second pipeline next to the baseline. Baseline files are untouched; `config.py` only gains `AdvancedSettings`.

## Run
```powershell
pip install -r requirements.txt
# 1) check retrieval only (no LLM, fast)
python -m src.pipeline_adv --input dataset\final_dataset\2025-01-22\rag_input.json --dry-run
# 2) full run (8 section calls + 1 summary call). On your CPU try the smaller model first:
ollama pull llama3.2:3b
python -m src.pipeline_adv --input dataset\final_dataset\2025-01-22\rag_input.json --model llama3.2:3b
# 3) compare against the baseline output with identical metrics
python -m src.compare --input dataset\final_dataset\2025-01-22\rag_input.json --report basic_RAG_output.txt --report results\2025-01-22\advanced_postmortem.md
```
Options: `--strict` (drop unverified lines), `--no-enrich`, `--sections 2,4` (subset), `--model`.
Outputs: `results/<scenario>/advanced_postmortem.md` and `advanced_run_report.json`.

## What changed vs. baseline (and the baseline problem each part fixes)
| Component | File | Fixes |
|---|---|---|
| Item-level chunking: each domain/IP/download becomes one fact line, grouped 4 per chunk with a contextual header | `adv_chunking.py` | Baseline cut JSON mid-entry by word count |
| Raw-log enrichment: first/last-seen UTC for IOCs, client host-name hint (from dns/http/tls/conn logs) | `enrichment.py` | `[insert date]` placeholders in the timeline |
| BM25 (IP/domain-aware tokenizer) + dense, fused with RRF | `adv_retrieval.py` | Hand-tuned 0.7/0.3 set-overlap score; `rank-bm25` was installed but unused |
| Cross-encoder rerank (MiniLM-L6, 22M params) | `adv_retrieval.py` | Ordering of final chunks |
| Query decomposition: one multi-query retrieval per postmortem section | `sections.py` | One generic query for the whole report |
| Section-wise generation with evidence IDs and mandatory citations | `adv_generation.py` | Generic filler, no grounding; small prompts also suit your CPU |
| Deterministic verification: IPs/domains/URIs/hosts/MACs and citation IDs checked against the evidence; unsupported lines flagged or dropped | `verify.py` | Hallucinated facts |
| Evaluation vs `reference_qa.json` (evaluation-only, never sent to the LLM) | `evaluate.py`, `compare.py` | No measurable comparison |

## Verification (what "flagged" means)
Each section is checked **only against its own retrieved chunks** (plus the incident header). The Incident Summary is checked
against the section lines that survived verification. A line is flagged when it contains:
* an entity (IP, domain, URI, host, MAC, date/timestamp) not in that evidence (trailing punctuation on URIs is stripped first);
* a number (count, bytes, port) not in that evidence. Derived values such as sums are flagged, not recomputed;
* a citation that does not resolve to a chunk retrieved for that section (grouped `[id#1, #3]` is supported);
* an `[insert ...]` placeholder;
* **uncited**: a claim line (>=30 chars, not a heading/"Not established" line) with no valid citation on it or on a parent bullet.
Default: lines are annotated (`⚠ UNVERIFIED`, `⚠ UNCITED`). `--strict` drops them. Truncated sections get a `⚠ TRUNCATED` note;
the Timeline uses `num_predict_long` (900) from `config.py`.

## Metrics
`answerable_entity_recall`, `overall_entity_recall` (reference entities found in the report; "answerable" = present in the evidence),
`hallucination_rate` (report entities not in the evidence), `unsupported_number_count`, `placeholder_count`,
`citation_rate` (cited claim lines / claim lines). Entity-level grounding checks, not full faithfulness.

## Known limits
* Retrieval and the LLM were not run end-to-end on a real model in the development sandbox (no model downloads); the
  pipeline logic, enrichment, chunking, verification and evaluation were tested offline with stand-in embedder/LLM.
* Verification checks entities, numbers and citations, not reasoning, direction of traffic, or whether a cited chunk truly supports the sentence. Assessments still need human review.
* Benign-domain filtering in `enrichment.py` is a small keyword list; extend `BENIGN_HINTS` as needed.
