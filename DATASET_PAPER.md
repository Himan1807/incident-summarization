# Paper dataset (neu-nds2/llm-sec-incident-analysis) in this project

17 real incident scenarios (MTA, Unit 42, SANS ISC). Prepared copies are in `dataset/paper_dataset/<scenario>/`.

## Files per scenario
| File | Used by | Content |
|---|---|---|
| `rag_input.json` | advanced pipeline | metadata, neutral description + network context, `investigation_questions`, artifacts (one per Elasticsearch query result, plus derived findings and a query-coverage artifact) |
| `starter_input.json` | basic pipeline | same evidence in the legacy schema (`alerts` = Suricata, `logs` = the rest) |
| `reference_qa.json` | evaluation only | reference answers split into atoms; never sent to retrieval or the LLM |
| `cleaning_report.json` | you | what was cleaned or flagged |

`dataset/paper_dataset/DATASET_REPORT.md` shows, per scenario, how many reference atoms exist in the evidence (94% overall; the rest must be inferred, e.g. the CIA component, or are reference typos).

## Cleaning applied (deterministic)
refanging (`10.0.19[.]0`), removal of scenario-name headings and the dataset README text (they name the malware family), flattening of
Elasticsearch buckets into one fact per line (URIs cut at 240 chars), empty aggregations merged into one coverage artifact, failed queries
(`burnincandle`, `iced_id`: certificates, shard failure) recorded as evidence gaps, `??` fixed in questions, answer parsing into atoms.
Known data issue kept as given: `jun21isc` reference answer contains the typo `DEKSTOP-A1CTJVY`.

## Commands (PowerShell, from the project root)
```powershell
# regenerate the prepared dataset (optional; already included)
git clone https://github.com/neu-nds2/llm-sec-incident-analysis
python -m src.prepare_dataset --source llm-sec-incident-analysis\evaluation --out dataset\paper_dataset

python tests\smoke_all_scenarios.py                                   # offline sanity check, no Ollama needed
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --dry-run
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --model llama3.2:3b
python -m src.pipeline --input dataset\paper_dataset\koi_stealer\starter_input.json     # basic RAG baseline
python -m src.compare --input dataset\paper_dataset\koi_stealer\rag_input.json --report <basic_output.txt> --report results\koi_stealer\advanced_postmortem.md
python -m src.run_batch --scenarios koi_stealer,fake_auth,easy_123 --model llama3.2:3b   # several scenarios + results\summary.md
python tests\test_postprocess_regression.py                         # replays a real model output; no Ollama needed
```
`python -m src.pipeline` prints to the console; save it with `> basic_koi.txt` (PowerShell: `| Out-File -Encoding utf8 basic_koi.txt`).
