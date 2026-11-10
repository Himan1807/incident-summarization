"""Environment pre-flight check.   python -m src.check_env [--model llama3.2:3b]

Verifies the Python packages and, optionally, that Ollama is running and has the model, and prints the exact fix for anything missing.
"""
import argparse
import importlib

REQUIRED = {"numpy": "numpy", "requests": "requests", "sentence_transformers": "sentence-transformers"}
OPTIONAL = {"rank_bm25": "rank-bm25 (a built-in fallback is used if missing)", "sklearn": "scikit-learn (only the basic pipeline)"}


def check_packages() -> list[str]:
    problems = []
    for mod, pkg in REQUIRED.items():
        try:
            importlib.import_module(mod)
        except Exception as exc:
            problems.append(f"missing package '{pkg}' ({exc.__class__.__name__}). Fix:  pip install {pkg}")
    for mod, pkg in OPTIONAL.items():
        try:
            importlib.import_module(mod)
        except Exception:
            print(f"[note] optional package not installed: {pkg}")
    return problems


def check_ollama(url: str, model: str) -> list[str]:
    import requests
    base = url.split("/api/")[0]
    try:
        tags = requests.get(base + "/api/tags", timeout=5).json().get("models", [])
    except Exception:
        return [f"Ollama is not reachable at {base}. Start the Ollama app (or run 'ollama serve' in another window)."]
    names = {m.get("name", "") for m in tags}
    if model not in names and f"{model}:latest" not in names:
        have = ", ".join(sorted(names)) or "none"
        return [f"Ollama does not have the model '{model}' (installed: {have}). Fix:  ollama pull {model}"]
    return []


def preflight(model: str, url: str, need_llm: bool = True) -> None:
    problems = check_packages()
    if need_llm:
        problems += check_ollama(url, model)
    if problems:
        raise SystemExit("\nSetup problem(s):\n  - " + "\n  - ".join(problems) +
                         "\nAfter fixing, run the same command again. (Tip: 'pip install -r requirements.txt' installs all packages.)")


def main():
    from config import AdvancedSettings
    S = AdvancedSettings()
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=S.ollama_model)
    a = ap.parse_args()
    preflight(a.model, S.ollama_url, need_llm=True)
    print(f"Environment OK (packages present; Ollama running with '{a.model}').")


if __name__ == "__main__":
    main()
