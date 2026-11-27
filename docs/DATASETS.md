# Datasets in this project

| Dataset | Folder | Incidents | Evidence | Reference | Details |
|---|---|---|---|---|---|
| Paper dataset | `dataset/paper_dataset/` | 47: 17 real network-security incidents (neu-nds2/llm-sec-incident-analysis) and 30 microservice failure cases from RCAEval RE2-OB (`re2ob_01` ... `re2ob_30`, converted by `src/prepare_rcaeval.py`); 369 questions, 488 reference atoms | Security: query results (Suricata, Kerberos, HTTP, TLS, DNS) flattened to facts. RCAEval: aggregated Prometheus metrics, application logs, trace latency/error statistics and the pod inventory | Reference answers split into atoms (RCAEval: benchmark labels; question 8 derived) | DATASET_PAPER.md, `dataset/paper_dataset/DATASET_REPORT.md` |
| Synthetic starter incidents (original) | `dataset/final_dataset/` | 3 (`2025-01-22`, `2025-06-13`, `2026-02-28`), with raw Zeek logs used by enrichment | Aggregated network artifacts | Q&A | ADVANCED_RAG.md |

Every incident folder has the same files (`rag_input.json`, `starter_input.json`, `reference_qa.json`, `cleaning_report.json`), so all commands work on any of
them: pass `--root <dataset folder>` to `run_experiment`, or `--input <folder>\<incident>\rag_input.json` to `pipeline_adv` / `no_rag`.
Every incident currently uses the same section plan (`src/sections.py`). Add a new dataset by writing the same four files.
Metrics: METRICS.md. Experiments and reports: EXPERIMENTS.md.
