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
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6 --with-unanswerable --section-profile auto
```
With `--with-unanswerable` the questions get a separate Q&A call built like the real one (same task, per-question retrieval, budget and token
cap) and the answers go to a separate section "Additional Investigation Questions" (U1-U3) at the end of the postmortem. The real Q&A,
its context, the summary and every existing score stay as without the option. Finished RAG runs without RQ4 answers are re-run.
`results/unanswerable_eval.txt`: per model and domain (security / outage) the correct-abstention rate, the invention rate of the model's
answers and after the fact-check (how many inventions the fact-check removed), and over-abstention (real questions whose reference
answer is fully in the evidence but which were answered 'Not established'); exact McNemar tests on correct abstention between models on
the same questions; and every question with its answer and status. The fact-check verifies IPs, domains, hosts, URLs, times and numbers,
so an invented hash, version or ticket id is not removed by it; "invention after check" measures exactly that.

## Hosted models (DeepInfra)
Local and hosted models are run with separate commands that take the same options and write to the same `results/` tree:
```powershell
python -m src.run_experiment --models llama3.2:3b,qwen2.5:7b-instruct ...          # local Ollama models only
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6 ...   # hosted DeepInfra models only
```
`run_experiment` refuses hosted models (and prints the `run_api` command to use); `run_api` takes DeepInfra model ids, adds the
`deepinfra:` prefix itself and never contacts Ollama. `src/llm_api.py` calls DeepInfra's OpenAI-compatible chat-completions API; single
runs (`pipeline_adv --model`, `no_rag --model`, `check_env --model`) select it with a `deepinfra:<model id>` name.
* Key: environment variable `DEEPINFRA_API_KEY` (or `DEEPINFRA_TOKEN`). It is only read from the environment, never stored in the repo.
* Same conditions as Ollama: one user message with the identical prompt, temperature 0.1, `max_tokens` = the section's token cap (600 / 900);
  a reply cut off by the cap is handled like Ollama's. A leading `<think>...</think>` block of reasoning models is removed.
* HTTP 429 and 5xx are retried with backoff (`Retry-After` respected); a wrong key, unknown model id or missing credit stops with a clear message.
  `run_api` checks every model before it starts (the key and a 1-token request), as `run_experiment` does for Ollama.
* Results: `results/<incident>/deepinfra_<org>_<model>/`, compared with the local models in every report. `llm_usage` in the run JSON:
  calls, retries, prompt/completion tokens and DeepInfra's cost estimate when the API returns one.
* Size of a full run (47 incidents: RAG + no-RAG + RQ4, about 940 calls): about 1.0M input and 0.2-0.6M output tokens per model.
  Multiply by the model's price per 1M tokens on its DeepInfra page. Try two incidents first.
* The incident evidence is sent to DeepInfra (and, for Claude models, served by Anthropic through DeepInfra). The datasets here are public.
