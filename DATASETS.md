# Datasets in this project

| Dataset | Folder | Incidents | Evidence | Reference | Section profile | Details |
|---|---|---|---|---|---|---|
| Paper dataset (neu-nds2/llm-sec-incident-analysis) | `dataset/paper_dataset/` | 17 network-security incidents | Elasticsearch query results (Suricata, Kerberos, HTTP, TLS, DNS) flattened to facts | Reference answers (gold, from the paper) | `network_security` (default) | DATASET_PAPER.md |
| postmortems.app (icco/postmortems) | `dataset/postmortems_dataset/` | 208 incidents: cloud, config changes, cascading failures, hardware, automation, time, security | Incident narrative split into sentences | Front matter turned into questions + reference summary (silver) | `service_outage` | DATASET_POSTMORTEMS.md |
| Synthetic starter incidents (original) | `dataset/final_dataset/` | 3 | Aggregated network artifacts | Q&A | `network_security` | ADVANCED_RAG.md |

Every incident folder has the same files (`rag_input.json`, `starter_input.json`, `reference_qa.json`, `cleaning_report.json`), so all commands work on any of
them: pass `--root <dataset folder>` to `run_experiment`, or `--input <folder>\<incident>\rag_input.json` to `pipeline_adv` / `no_rag`.
The section plan is chosen per incident by `metadata.section_profile`; add a new dataset by writing the same four files and, if its domain differs, a profile
in `src/sections.py`. Metrics: METRICS.md. Experiments and reports: EXPERIMENTS.md.
