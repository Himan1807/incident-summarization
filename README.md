# Incident RAG: incident summarization and postmortem generation

Retrieval-augmented generation of incident postmortems from incident artifacts (alerts, logs, query results), evaluated against reference
answers. Two pipelines:

* **Basic pipeline** (`src/pipeline.py`): chunk the artifacts, dense retrieval + keyword overlap, one generic postmortem prompt to Ollama.
* **Advanced pipeline** (`src/pipeline_adv.py`): item-level chunking, BM25 + dense retrieval fused with RRF, cross-encoder rerank,
  section-wise generation with citations, deterministic verification and evaluation. See [docs/ADVANCED_RAG.md](docs/ADVANCED_RAG.md).

Dataset: `dataset/paper_dataset/`, 47 incidents (17 real security incidents from the paper, 30 microservice failures from RCAEval RE2-OB),
369 questions.
See [docs/DATASETS.md](docs/DATASETS.md).

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull llama3.2:3b
```

## Run

```powershell
# basic pipeline (prints the postmortem)
python -m src.pipeline --input data/raw/sample_incident.json
# advanced pipeline on one incident: retrieval only, then a full run
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --dry-run
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --model llama3.2:3b
# experiments: RAG and no-RAG for each incident x model, with all text reports
python -m src.run_experiment --scenarios koi_stealer --models llama3.2:3b
python -m src.run_experiment --reports-only
# RQ4 (unanswerable questions): RAG runs also answer unanswerable_qa.json; writes results/unanswerable_eval.txt
python -m src.run_experiment --models llama3.2:3b,qwen2.5:7b-instruct,llama3.1:8b-instruct-q4_K_M --with-unanswerable --section-profile auto
```

Results are written to `results/<incident>/<model>/`; older runs in the previous layout are kept in `results/archive/`.
The reference answers (`reference_qa.json`) are used only for evaluation and are never given to retrieval or the LLM.

## Offline tests (no Ollama, no model downloads)

```powershell
python tests\test_koi_regression.py
python tests\test_postprocess_regression.py
python tests\test_experiment_reports.py
python tests\smoke_all_scenarios.py
python tests\test_prepare_rcaeval.py    # RCAEval converter on a tiny fake case
python tests\test_fair_norag.py         # --fair-norag-evidence
python tests\test_section_profile.py     # --section-profile
python tests\test_unanswerable.py        # RQ4 scoring and --with-unanswerable
python -m src.check_unanswerable         # proves every unanswerable question has no answer in its incident's evidence
python tests\golden_snapshot.py      # compares the advanced pipeline's outputs with the frozen baseline in tests\golden\
```

## Documentation

| File | Content |
|---|---|
| [docs/ADVANCED_RAG.md](docs/ADVANCED_RAG.md) | Advanced pipeline: components, options, verification |
| [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) | Experiment commands, result files, the no-RAG condition |
| [docs/METRICS.md](docs/METRICS.md) | Metric definitions, post-processing and verification defaults |
| [docs/DATASETS.md](docs/DATASETS.md) | Datasets in the project |
| [docs/DATASET_PAPER.md](docs/DATASET_PAPER.md) | The paper dataset: files, cleaning, commands |
| [examples/](examples/) | Sample console output of the basic and the advanced pipeline |
