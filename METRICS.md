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

A *claim line* is a bullet of at least 30 characters that is not a heading, a question, a list label, an absence statement
("Not established ...", or anything under a "Not established / evidence gaps" heading or bullet) or a pure hedged assessment ("The most likely
root cause is a compromised client" with no IP, domain, number or time). Assessments are counted separately (`assessment_lines`).

Limits: precision only counts entities a regex can extract (a user name such as `brolf` is scored for recall but not precision);
derived numbers (sums, ratios) are flagged, not recomputed; reasoning quality is not judged.

## What the post-processing does (and how it is disclosed)
`src/postprocess.py` runs after each LLM section: it removes chatty preambles, repeated titles and question echoes; deletes citation IDs
that do not exist in the section's evidence (for example an example ID copied from the prompt); **attaches** the retrieved chunk that
actually contains an uncited line's entities/numbers (string match only); and removes near-duplicate lines inside and across sections.
Everything it does is counted in `results/<scenario>/advanced_run_report.json` under `postprocessing`
(`model_citation_rate_before_attribution`, `auto_attributed_lines`, `invalid_citations_removed`, `duplicate_lines_removed` and the removed lines).
Report the model's own citation rate (before attribution) next to the final one. `--no-postprocess` switches all of this off.

## Default behaviour of the verification step
* **drop (default):** lines whose entities, numbers or citations cannot be verified in the section's retrieved evidence, placeholders, and role errors
  (a private IP called an external destination / C2 server, or a public IP called the infected internal host) are **removed** and listed in
  `advanced_run_report.json` (`flagged`, `action: removed`). The report ends with a one-line verification note. Uncited claims stay, untagged.
* `--annotate` keeps everything and shows `UNVERIFIED` / `UNCITED` tags. `--strict` also removes uncited lines.
* **Timeline** is extractive: every timestamped evidence line becomes one entry, merged per timestamp, sorted, cited (no LLM call, no invented times).
  `--llm-timeline` restores LLM generation.
* **Token cap:** sections have a bullet limit in the prompt; if the cap is still hit, the unfinished last line is dropped (logged as
  `dropped_partial_line`) instead of printing a half sentence.

## Question status (text reports)
CORRECT = every reference item found and no wrong entity; PARTIAL = some found or wrong entities present; WRONG = answer given, none found;
ABSTAINED = "Not established from the available artifacts"; NO ANSWER = no answer for that question in the report. See EXPERIMENTS.md.
