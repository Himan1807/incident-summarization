# Incident RAG: incident summarization and postmortem generation

This project writes incident postmortems from incident evidence (alerts, logs, metrics, query results) with a language model, and
scores them against reference answers. It compares:

* **RAG**: the model gets the evidence retrieved for each section of the report (the advanced pipeline, `src/pipeline_adv.py`);
* **no RAG**: the same model and questions without any evidence;
* **RQ4**: whether the model admits "not established" when the answer is not in the evidence, or invents one.

Models can be **local** (Ollama, on your computer) or **hosted** (DeepInfra, over the internet with an API key, e.g. DeepSeek or Claude).
Local and hosted models are run with **two separate commands**, and all results land in the same `results` folder so the reports
compare them side by side.

Dataset: `dataset/paper_dataset/`, 47 incidents (17 real security incidents from the paper, 30 microservice failures from RCAEval
RE2-OB), 369 questions. Details: [docs/DATASETS.md](docs/DATASETS.md).

---

## Which command do I need?

| I want to ... | Command (run in the project folder) |
|---|---|
| run **local** models (Ollama) | `python -m src.run_experiment --models llama3.2:3b` |
| run **hosted** models (DeepInfra) | `python -m src.run_api --models deepseek-ai/DeepSeek-V3` |
| check that a model is ready | `python -m src.check_env --model llama3.2:3b` or `--model deepinfra:deepseek-ai/DeepSeek-V3` |
| rebuild all reports without any model | `python -m src.run_experiment --reports-only` |
| check the code without any model | the offline tests at the end of this page |

All commands below are for **Windows PowerShell**, run from the project folder (the one that contains this README).

---

## Step 1: one-time setup

1. Install **Python 3.10 or newer** from https://www.python.org (tick "Add python.exe to PATH" in the installer).
2. Open PowerShell in the project folder and create a virtual environment with the packages:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.
3. Every time you open a new PowerShell window, activate the environment again first: `.\.venv\Scripts\Activate.ps1`
   (the prompt then starts with `(.venv)`).
4. Optional sanity check that needs no model at all: `python tests\smoke_all_scenarios.py` (it should end with a `MEAN ...` line).

The first real run downloads two small retrieval models (sentence-transformers, about 100 MB) once.

---

## Step 2: local models (Ollama)

1. Install Ollama from https://ollama.com and start it (the Ollama app runs in the background).
2. Download the models you want to use, for example:

   ```powershell
   ollama pull llama3.2:3b
   ollama pull qwen2.5:7b-instruct
   ollama pull llama3.1:8b-instruct-q4_K_M
   ```

3. Check that a model is ready: `python -m src.check_env --model llama3.2:3b` (prints `Environment OK ...`).
4. Try two incidents first (one security incident, one RCAEval failure):

   ```powershell
   python -m src.run_experiment --scenarios koi_stealer,re2ob_01 --models llama3.2:3b --section-profile auto --with-unanswerable
   ```

5. Run everything (all 47 incidents; several models are separated by commas, without spaces):

   ```powershell
   python -m src.run_experiment --models llama3.2:3b,qwen2.5:7b-instruct,llama3.1:8b-instruct-q4_K_M --section-profile auto --with-unanswerable
   ```

Local models are slow on a CPU (tens of minutes per incident and model for an 8B model). Runs are **resumable**: if you stop with
Ctrl+C or the computer sleeps, run the same command again and finished runs are skipped.

`run_experiment` only accepts local models. If you give it a hosted model it stops and prints the `run_api` command to use instead.

---

## Step 3: hosted models (DeepInfra)

### 3.1 Get your API key (once)

1. Sign in at https://deepinfra.com and open the dashboard's **API keys** page. Create a key and copy it.
2. Add credit or a payment method in the dashboard's billing page (requests fail with "payment required" otherwise).
3. Keep the key private: never paste it into a file of this project, into a commit or into a chat.

### 3.2 Give the key to the project

The project reads the key from the environment variable `DEEPINFRA_API_KEY`. Choose one:

```powershell
# only for the current PowerShell window
$env:DEEPINFRA_API_KEY = "paste-your-key-here"

# or permanently for your Windows user (then close and reopen PowerShell)
setx DEEPINFRA_API_KEY "paste-your-key-here"
```

To check that it is set (shows only the first characters): `$env:DEEPINFRA_API_KEY.Substring(0,6)`.
To remove the permanent key later: `[Environment]::SetEnvironmentVariable("DEEPINFRA_API_KEY", $null, "User")`.

### 3.3 Pick the models

Open https://deepinfra.com/models, click a model and copy its **model id** shown on the page, for example:

| Model | DeepInfra model id |
|---|---|
| DeepSeek V3 | `deepseek-ai/DeepSeek-V3` |
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` |

Check each model before a long run (this sends one tiny request and costs a negligible fraction of a cent):

```powershell
python -m src.check_env --model deepinfra:deepseek-ai/DeepSeek-V3
python -m src.check_env --model deepinfra:anthropic/claude-sonnet-4-6
```

### 3.4 Run them

Try two incidents first, then run everything:

```powershell
python -m src.run_api --scenarios koi_stealer,re2ob_01 --models deepseek-ai/DeepSeek-V3 --section-profile auto --with-unanswerable
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6 --section-profile auto --with-unanswerable
```

`run_api` only runs hosted models and never contacts Ollama. Like `run_experiment` it checks every model before it starts and is resumable.

### 3.5 Different models with the same API key

**One DeepInfra key works for every model on DeepInfra.** You never need a second key: the model is chosen only by the id you pass
to `--models`. Some ways to use that:

```powershell
# several models in one command (each one is run on every incident, one after the other)
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6 --section-profile auto --with-unanswerable

# or one model per command, e.g. today DeepSeek, tomorrow Claude (both use the same key and the same results folder)
python -m src.run_api --models deepseek-ai/DeepSeek-V3 --section-profile auto --with-unanswerable
python -m src.run_api --models anthropic/claude-sonnet-4-6 --section-profile auto --with-unanswerable

# add another model later: only the new model is run, finished runs of the others are skipped
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6,<another model id> --section-profile auto --with-unanswerable
```

Each model gets its own results folder (`deepinfra_deepseek-ai_DeepSeek-V3`, `deepinfra_anthropic_claude-sonnet-4-6`, ...), and the
reports compare all of them, local and hosted. The DeepInfra dashboard shows the spending per model, all billed to the same account.

### 3.6 What it costs

A full run of all 47 incidents (RAG + no RAG + the unanswerable questions, about 940 requests) uses roughly **1.0 million input and
0.2-0.6 million output tokens per model**. With the prices listed on DeepInfra in November 2026 that is about:

| Model | Price per 1M tokens (input / output) | Full run, one model |
|---|---|---|
| `deepseek-ai/DeepSeek-V3` | about $0.32 / $0.89 | under $1 |
| `anthropic/claude-sonnet-4-6` | about $3 / $15 | about $6-12 |

Prices change; check the model's page. After a run, each `advanced_run_report.json` / `no_rag_run_report.json` of a hosted model has an
`llm_usage` entry with the tokens used (and DeepInfra's cost estimate when it returns one).

Hosted models get exactly the same prompt, temperature (0.1) and length limits as the local models, so the comparison is fair. The
incident evidence is sent to DeepInfra (for Claude models, served by Anthropic); the datasets in this project are public.

---

## Step 4: results and reports

Everything is written to the `results` folder:

| File | What it shows |
|---|---|
| `results\<incident>\<model>\advanced_postmortem.md` | the postmortem written with RAG |
| `results\<incident>\<model>\no_rag_postmortem.md` | the same model without evidence |
| `results\<incident>\<model>\qa_evaluation_rag.txt` | each question: reference answer, the model's answer, status, metrics |
| `results\<incident>\<model>\rag_vs_no_rag.txt` | RAG and no RAG side by side |
| `results\<incident>\model_comparison.txt` | all models (local and hosted) on one incident |
| `results\summary.txt` | every incident x model x condition, with means per model |
| `results\unanswerable_eval.txt` | RQ4: correct abstention, invention and over-abstention per model, security vs outage, McNemar tests |

The reports are rebuilt after every run. To rebuild them by hand (no model needed): `python -m src.run_experiment --reports-only`.
Metric definitions: [docs/METRICS.md](docs/METRICS.md). Older runs in the previous folder layout are kept in `results\archive\`.

---

## Options (the same for `run_experiment` and `run_api`)

| Option | Meaning |
|---|---|
| `--models a,b,c` | models to run, comma-separated without spaces (Ollama names for `run_experiment`, DeepInfra ids for `run_api`) |
| `--scenarios x,y` | only these incidents (folder names in `dataset\paper_dataset`), e.g. `koi_stealer,re2ob_01`; default: all 47 |
| `--section-profile auto` | report sections that fit each incident: security sections for the security incidents, outage sections for the RCAEval failures (recommended) |
| `--with-unanswerable` | also ask the 3 unanswerable questions per incident (RQ4) and write `results\unanswerable_eval.txt` |
| `--skip-no-rag` / `--skip-rag` | run only one of the two conditions |
| `--force` | run again even if a result already exists |
| `--results <folder>` | write to another results folder (the reports then only compare the models in that folder) |
| `--fair-norag-evidence` | score no RAG against exactly the same evidence as RAG (only matters for incidents with raw logs) |
| `--reports-only` | only rebuild the reports from stored results |

---

## Troubleshooting

| Message | What to do |
|---|---|
| `running scripts is disabled on this system` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate the environment again |
| `No module named ...` / `missing package` | activate the environment (`.\.venv\Scripts\Activate.ps1`) and run `pip install -r requirements.txt` |
| `Ollama is not reachable` | start the Ollama app |
| `Ollama does not have the model` | `ollama pull <model>` with the exact name |
| `no API key for deepinfra` | set the key (Step 3.2) in this window, or reopen PowerShell after `setx` |
| `rejected the API key (HTTP 401/403)` | the key is wrong or deleted: create a new one in the DeepInfra dashboard |
| `payment required (HTTP 402)` | add credit or a payment method in the DeepInfra dashboard |
| `refused the request for model ...` | the model id is misspelled or not offered: copy it again from the model's page |
| `this command runs local Ollama models only` | you passed a hosted model to `run_experiment`: use the `run_api` command it prints |
| rate limit (HTTP 429) or a network error | nothing to do: requests are retried automatically; if the run still stops, run the same command again |

---

## Other commands

```powershell
# basic pipeline (prints the postmortem)
python -m src.pipeline --input data/raw/sample_incident.json
# advanced pipeline on one incident: retrieval only, then a full run (a hosted model: --model deepinfra:deepseek-ai/DeepSeek-V3)
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --dry-run
python -m src.pipeline_adv --input dataset\paper_dataset\koi_stealer\rag_input.json --model llama3.2:3b
# prove that every unanswerable question really has no answer in its incident's evidence
python -m src.check_unanswerable
# rebuild the 30 RCAEval incidents from RE2-OB.zip (Zenodo record 14590730)
python -m src.prepare_rcaeval --zip <path>\RE2-OB.zip --out dataset\paper_dataset
```

The reference answers (`reference_qa.json`, `unanswerable_qa.json`) are used only for evaluation and are never given to retrieval or
the model (with `--with-unanswerable` only the question text is asked).

## Offline tests (no Ollama, no API key, no model downloads)

```powershell
python tests\test_koi_regression.py
python tests\test_postprocess_regression.py
python tests\test_experiment_reports.py
python tests\smoke_all_scenarios.py
python tests\test_prepare_rcaeval.py    # RCAEval converter on a tiny fake case
python tests\test_fair_norag.py         # --fair-norag-evidence
python tests\test_section_profile.py     # --section-profile
python tests\test_unanswerable.py        # RQ4 scoring and --with-unanswerable
python tests\test_llm_api.py            # hosted models, against a fake local API server
python tests\test_run_commands.py       # run_experiment = local only, run_api = hosted only
python tests\golden_snapshot.py      # compares the advanced pipeline's outputs with the frozen baseline in tests\golden\
```

## Documentation

| File | Content |
|---|---|
| [docs/ADVANCED_RAG.md](docs/ADVANCED_RAG.md) | Advanced pipeline: components, options, verification |
| [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) | Experiment commands, result files, the no-RAG condition, section plans, RQ4, hosted models |
| [docs/METRICS.md](docs/METRICS.md) | Metric definitions, post-processing and verification defaults, RQ4 metrics |
| [docs/DATASETS.md](docs/DATASETS.md) | Datasets in the project |
| [docs/DATASET_PAPER.md](docs/DATASET_PAPER.md) | The paper dataset and the RCAEval cases: files, cleaning, commands |
| [examples/](examples/) | Sample console output of the basic and the advanced pipeline |
