# Metrics and verification (advanced pipeline)

All metrics are computed by string matching against the evidence and the reference answers (`reference_qa.json`, evaluation only). No LLM judge.

| Metric | Definition | Why |
|---|---|---|
| **answer_precision** | Entities (IPs, domains, hosts, URLs, times) in the Q&A answer N that occur in reference answer N / all entities in answer N (micro-average) | Penalises extra or wrong answers |
| **answer_recall** | Reference answer items found in answer N / all reference items | Did it find what the reference contains? |
| **answer_f1** | Harmonic mean of the two | Single answer-quality score |
| question_recall | Mean over questions of (reference items found anywhere in the report / items) | Paper-style recall, report-wide |
| answerable_entity_recall / overall_entity_recall | Same, restricted to items present in the evidence / all items | Separates retrieval+generation from reasoning |
| **faithfulness** | Claim lines whose facts are in the evidence AND in the chunks they cite / all claim lines | Is every claim supported by its own citation? |
| grounding_rate | Claim lines whose entities and numbers all exist in the evidence (works for any report, cited or not) | Fair comparison with uncited baselines |
| citation_precision | Cited claim lines actually supported by the chunks they cite | Are citations correct, not just present? |
| citation_rate | Cited claim lines / claim lines | Coverage of citations |
| hallucination_rate | Report entities absent from the evidence / all report entities | Invented IPs, domains, times |
| unsupported_number_count, placeholder_count | Numbers absent from the evidence; `[insert ...]` | |

A *claim line* is a bullet of at least 30 characters that is not a heading, a question, a list label or an absence statement
("Not established ...", or anything under a "Not established / evidence gaps" heading).

Limits: precision only counts entities a regex can extract (a user name such as `brolf` is scored for recall but not precision);
derived numbers (sums, ratios) are flagged, not recomputed; reasoning quality is not judged.

## What the post-processing does (and how it is disclosed)
`src/postprocess.py` runs after each LLM section: it removes chatty preambles, repeated titles and question echoes; deletes citation IDs
that do not exist in the section's evidence (for example an example ID copied from the prompt); **attaches** the retrieved chunk that
actually contains an uncited line's entities/numbers (string match only); and removes near-duplicate lines inside and across sections.
Everything it does is counted in `results/<scenario>/advanced_run_report.json` under `postprocessing`
(`model_citation_rate_before_attribution`, `auto_attributed_lines`, `invalid_citations_removed`, `duplicate_lines_removed` and the removed lines).
Report the model's own citation rate (before attribution) next to the final one. `--no-postprocess` switches all of this off.
