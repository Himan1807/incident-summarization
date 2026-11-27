# Paper dataset (neu-nds2/llm-sec-incident-analysis) in this project

47 scenarios in `dataset/paper_dataset/<scenario>/`: 17 real incident scenarios from the paper (MTA, Unit 42, SANS ISC) and 30 microservice
failure cases from RCAEval RE2-OB (`re2ob_01` ... `re2ob_30`; see "RCAEval cases" below). 369 questions, 488 reference atoms in total.

## Files per scenario
| File | Used by | Content |
|---|---|---|
| `rag_input.json` | advanced pipeline | metadata, neutral description + network context, `investigation_questions`, artifacts (one per Elasticsearch query result, plus derived findings and a query-coverage artifact) |
| `starter_input.json` | basic pipeline | same evidence in the legacy schema (`alerts` = Suricata, `logs` = the rest) |
| `reference_qa.json` | evaluation only | reference answers split into atoms; never sent to retrieval or the LLM |
| `cleaning_report.json` | you | what was cleaned or flagged |
| `unanswerable_qa.json` | RQ4 evaluation (`--with-unanswerable`) | 3 questions whose answer is provably not in the evidence (`src/check_unanswerable.py`) |

`dataset/paper_dataset/DATASET_REPORT.md` shows, per scenario, how many reference atoms exist in the evidence (94% for the 17 real scenarios, 98% for the 30 RCAEval cases; the rest must be inferred,
e.g. the CIA component, or are reference typos).

## Cleaning applied (deterministic)
refanging (`10.0.19[.]0`), removal of scenario-name headings and the dataset README text (they name the malware family), flattening of
Elasticsearch buckets into one fact per line (URIs cut at 240 chars), empty aggregations merged into one coverage artifact, failed queries
(`burnincandle`, `iced_id`: certificates, shard failure) recorded as evidence gaps, `??` fixed in questions, answer parsing into atoms.
Known data issue kept as given: `jun21isc` reference answer contains the typo `DEKSTOP-A1CTJVY`.

## Commands (PowerShell, from the project root)
```powershell
# results are written to results\<incident>\<model>\ ; see EXPERIMENTS.md for the reports
# regenerate the 17 real scenarios from the paper's repository (optional; already included)
git clone https://github.com/neu-nds2/llm-sec-incident-analysis
python -m src.prepare_dataset --source llm-sec-incident-analysis\evaluation --out dataset\paper_dataset

python tests\smoke_all_scenarios.py                                   # offline sanity check, no Ollama needed
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --dry-run
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --model llama3.2:3b
python -m src.pipeline --input dataset\paper_dataset\koi_stealer\starter_input.json     # basic RAG baseline
python -m src.compare --input dataset\paper_dataset\koi_stealer\rag_input.json --report <basic_output.txt> --report results\koi_stealer\llama3.2_3b\advanced_postmortem.md
python -m src.run_experiment --scenarios koi_stealer,fake_auth,easy_123 --models llama3.2:3b   # RAG + no-RAG, all text reports (see EXPERIMENTS.md)
python tests\test_postprocess_regression.py                         # replays a real model output; no Ollama needed
```
`python -m src.pipeline` prints to the console; save it with `> basic_koi.txt` (PowerShell: `| Out-File -Encoding utf8 basic_koi.txt`).

## RCAEval cases
Source: RCAEval benchmark, suite RE2, system Online Boutique (`RE2-OB.zip`, Zenodo record 14590730, doi:10.5281/zenodo.14590730).
One repetition (instance 1) per root-cause service (checkoutservice, currencyservice, emailservice, productcatalogservice,
recommendationservice) x fault type (cpu, mem, disk, delay, loss, socket) = 30 incidents. Download the zip yourself, then:
```powershell
python -m src.prepare_rcaeval --zip <path>\RE2-OB.zip --out dataset\paper_dataset
```
* Artifacts: metric anomalies vs a baseline of the first 10 minutes of each 24-minute capture (in the `alerts` slot of
  `starter_input.json`), trace latency and errors per operation, log volume per container and log templates that appear or
  disappear, the pod inventory, a derived summary and evidence gaps. The injection time is never used to build the evidence.
* Questions mirror the paper set: root-cause service, its pod and node, fault type (multiple choice), CIA component, first-signs
  minute, RCAEval root-cause indicator (`<service>_<indicator>`), and the largest trace-latency increase with "root cause or downstream
  symptom". Answers 1, 4, 5, 6 and 7 are RCAEval labels, 2 and 3 come from the pod inventory, 8 is derived from the trace statistics.
* Incident names are neutral because chunk ids are built from the name and shown to the LLM; each `cleaning_report.json` names its
  source case.
