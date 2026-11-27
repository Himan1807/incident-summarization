# Experiments: RAG vs no RAG, per-incident tables, multi-model comparison

## Commands (PowerShell, project root, venv active)
```powershell
# One incident, one model: RAG run + no-RAG run + all reports
python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b

# One incident on several models (each is run with RAG and without)
python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b,llama3.1:8b-instruct-q4_K_M

# Several incidents; RAG only; re-run finished runs; rebuild text reports without any LLM
python -m src.run_experiment --scenarios koi_stealer,easy_123,fake_auth --models llama3.2:3b --skip-no-rag
python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b --force
python -m src.run_experiment --reports-only
```
Single runs still work: `python -m src.pipeline_adv --input ... --model ...` (RAG) and `python -m src.no_rag --input ... --model ...` (no RAG).
Every model must be pulled first (`ollama pull <model>`); `run_experiment` checks all models before it starts. Runs are resumable.

## Where the files are
```
results/<incident>/<model>/advanced_postmortem.md        RAG report
results/<incident>/<model>/no_rag_postmortem.md          same LLM without retrieved evidence
results/<incident>/<model>/qa_evaluation_rag.txt         questions | reference answers | answers from the RAG report | metrics (table)
results/<incident>/<model>/qa_evaluation_no_rag.txt      the same for the no-RAG report
results/<incident>/<model>/rag_vs_no_rag.txt             RAG vs no RAG: metrics side by side + answers per question
results/<incident>/model_comparison.txt                  all models and conditions for the incident: metrics + status per question
results/summary.txt                                      every incident x model x condition, with means
```
(`*_run_report.json` next to each report holds the raw numbers, removed/flagged lines and timings.)

## What "no RAG" means
Same LLM, same section plan, same questions, same incident context (neutral description, network context, query window) but **no logs, alerts or
query results**. The output is only formatted (preambles and repeated titles removed), not verified, de-duplicated or given citations. It is scored against the
real evidence with the same evaluator, so its hallucination rate, grounding rate and answer precision/recall are directly comparable with RAG.
Faithfulness is 0 or '-' for no RAG by construction.

By default the no-RAG report is scored against the incident's artifacts only. `--fair-norag-evidence` (on `run_experiment` or `no_rag`) scores it
against exactly the evidence the RAG run is scored against (artifacts plus the raw-log enrichment, which exists only for incidents with raw
logs, e.g. `dataset/final_dataset/`). The run JSON then records `evaluation_evidence`. Off by default, so stored results stay comparable.

## Section plans
By default every incident uses the security section plan of the paper (affected host, IDS alerts, infection indicators, C2, ...).
`--section-profile auto` (on `run_experiment`, `pipeline_adv` and `no_rag`) gives operational incidents such as the RCAEval cases a service-outage
plan (affected service and infrastructure, metric anomalies, service dependencies and propagation, impact, root cause, actions) and an outage
summary prompt without the C2 wording; security incidents keep exactly the default output. `--section-profile security|service_outage` forces one plan.
RAG and no-RAG use the same plan. The run JSON records `section_profile` when the option is given.
```powershell
python -m src.run_experiment --scenarios re2ob_01,re2ob_02 --models llama3.2:3b --section-profile auto --results results_outage_plan
```

## Question status
CORRECT (all reference items found, nothing wrong) | PARTIAL | WRONG (answer given, nothing matches) | ABSTAINED ("Not established from the available artifacts") | NO ANSWER.
Metric definitions: METRICS.md. Answers are taken from the report's section "Answers to Investigation Questions", answer N against reference answer N.

## RQ4: unanswerable questions
Does the system say the answer is not in the evidence, or invent one? Every incident has `unanswerable_qa.json`: 3 questions in the style
of the real ones that ask for a value of a type that occurs nowhere in that incident's evidence (security: file hashes, registry keys,
CVE ids, sender e-mail, ticket numbers, PIDs; outages: image version, change ticket, node IP, on-call e-mail, commit hash, kernel version).
`python -m src.check_unanswerable` proves it against the exact evidence the pipeline can show the LLM (header, all chunks incl. enrichment,
the real questions); `--write` rebuilds the files and reports how many candidates were rejected because a value of that type existed.
```powershell
python -m src.check_unanswerable
python -m src.run_experiment --models llama3.2:3b,qwen2.5:7b-instruct,llama3.1:8b-instruct-q4_K_M --with-unanswerable --section-profile auto
```
With `--with-unanswerable` the questions get a separate Q&A call built like the real one (same task, per-question retrieval, budget and token
cap) and the answers go to a separate section "Additional Investigation Questions" (U1-U3) at the end of the postmortem. The real Q&A,
its context, the summary and every existing score stay as without the option. Finished RAG runs without RQ4 answers are re-run.
`results/unanswerable_eval.txt`: per model and domain (security / outage) the correct-abstention rate, the invention rate of the model's
answers and after the fact-check (how many inventions the fact-check removed), and over-abstention (real questions whose reference
answer is fully in the evidence but which were answered 'Not established'); exact McNemar tests on correct abstention between models on
the same questions; and every question with its answer and status. The fact-check verifies IPs, domains, hosts, URLs, times and numbers,
so an invented hash, version or ticket id is not removed by it; "invention after check" measures exactly that.
