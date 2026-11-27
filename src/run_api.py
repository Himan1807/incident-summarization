"""Run incidents x HOSTED models (DeepInfra) x conditions (RAG and no RAG) and build every text report.
Local Ollama models are run separately with:  python -m src.run_experiment --models llama3.2:3b

Needs the environment variable DEEPINFRA_API_KEY. Model ids are the DeepInfra ids from https://deepinfra.com/models
(the 'deepinfra:' prefix is optional). Every option of run_experiment works the same here.

python -m src.run_api --scenarios koi_stealer,re2ob_01 --models deepseek-ai/DeepSeek-V3
python -m src.run_api --models deepseek-ai/DeepSeek-V3,anthropic/claude-sonnet-4-6 --with-unanswerable --section-profile auto

Results go to the same results/<incident>/<model>/ tree (folder deepinfra_<org>_<model>), so the reports compare local and hosted models.
"""
from src import run_experiment


def main(argv=None):
    run_experiment.main(argv, backend="api")


if __name__ == "__main__":
    main()
