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
Faithfulness and citation metrics are 0 or '-' for no RAG by construction.

## Question status
CORRECT (all reference items found, nothing wrong) | PARTIAL | WRONG (answer given, nothing matches) | ABSTAINED ("Not established from the available artifacts") | NO ANSWER.
Metric definitions: METRICS.md. Answers are taken from the report's section "Answers to Investigation Questions", answer N against reference answer N.
