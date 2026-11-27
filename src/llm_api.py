"""Hosted LLMs over an OpenAI-compatible chat-completions API (DeepInfra), next to the local Ollama models.

Select a hosted model with a provider prefix; names without a prefix keep using Ollama exactly as before:
    --model  deepinfra:deepseek-ai/DeepSeek-V3
    --models llama3.2:3b,deepinfra:deepseek-ai/DeepSeek-V3,deepinfra:anthropic/claude-sonnet-4-6
The model id after the prefix is the one shown on the model's page at https://deepinfra.com/models.

API key: environment variable DEEPINFRA_API_KEY (DEEPINFRA_TOKEN is also accepted). It is read at call time and never written to
any file. Optional: DEEPINFRA_BASE_URL (default https://api.deepinfra.com/v1/openai).

The request mirrors the Ollama call for a fair comparison: the same single prompt (one user message), the same temperature and the
same token cap (max_tokens = num_predict). A reply cut off by the cap is reported like Ollama's done_reason == 'length'. Rate limits
and server errors are retried with backoff. A leading <think>...</think> block (reasoning models) is removed from the reply.
"""
import os
import re
import time

import requests

PROVIDERS = {
    "deepinfra": {"base_url": "https://api.deepinfra.com/v1/openai", "base_url_env": "DEEPINFRA_BASE_URL",
                  "key_env": ("DEEPINFRA_API_KEY", "DEEPINFRA_TOKEN"), "models_page": "https://deepinfra.com/models"},
}
RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
THINK_RE = re.compile(r"^\s*<think>.*?</think>\s*", re.S | re.I)


def split_model(model: str | None) -> tuple[str | None, str | None]:
    """'deepinfra:org/name' -> ('deepinfra', 'org/name'); Ollama names such as 'llama3.2:3b' -> (None, 'llama3.2:3b')."""
    if model and ":" in model:
        prefix, rest = model.split(":", 1)
        if prefix.lower() in PROVIDERS and rest:
            return prefix.lower(), rest
    return None, model


def is_api_model(model: str | None) -> bool:
    return split_model(model)[0] is not None


def _key(provider: str) -> str | None:
    for name in PROVIDERS[provider]["key_env"]:
        v = os.environ.get(name, "").strip()
        if v:
            return v
    return None


def _url(provider: str) -> str:
    p = PROVIDERS[provider]
    return (os.environ.get(p["base_url_env"], "").strip() or p["base_url"]).rstrip("/") + "/chat/completions"


def call_api(prompt: str, model: str, temperature: float, timeout: int, max_tokens: int, usage: dict | None = None,
             retries: int = 5) -> tuple[str, bool]:
    """Returns (text, hit_token_cap), like call_ollama. Adds token counts to `usage` when given."""
    provider, name = split_model(model)
    key = _key(provider)
    if not key:
        raise RuntimeError(f"No API key for {provider}. Set the environment variable {PROVIDERS[provider]['key_env'][0]} "
                           f"(PowerShell:  $env:{PROVIDERS[provider]['key_env'][0]} = \"<your key>\") and run the command again.")
    body = {"model": name, "messages": [{"role": "user", "content": prompt}], "temperature": temperature, "max_tokens": max_tokens}
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(_url(provider), headers={"Authorization": f"Bearer {key}"}, json=body, timeout=timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            last = f"{exc.__class__.__name__}"
            if attempt < retries:
                time.sleep(min(60, 2 * 2 ** attempt)); continue
            raise RuntimeError(f"Cannot reach {provider} ({last}). Check the internet connection and try again.") from exc
        if r.status_code in RETRY_STATUS and attempt < retries:
            try:
                wait = float(r.headers.get("Retry-After", ""))
            except ValueError:
                wait = min(60, 2 * 2 ** attempt)
            time.sleep(max(0.0, wait)); continue
        if r.status_code in (401, 403):
            raise RuntimeError(f"{provider} rejected the API key (HTTP {r.status_code}). Check {PROVIDERS[provider]['key_env'][0]}.")
        if r.status_code in (400, 404, 422):
            raise RuntimeError(f"{provider} refused the request for model '{name}' (HTTP {r.status_code}: {r.text[:300]}). "
                               f"Check the model id at {PROVIDERS[provider]['models_page']}.")
        if r.status_code == 402:
            raise RuntimeError(f"{provider}: payment required (HTTP 402). Add credit or a payment method to your account.")
        r.raise_for_status()
        j = r.json()
        choice = j["choices"][0]
        text = THINK_RE.sub("", (choice.get("message") or {}).get("content") or "").strip()
        if usage is not None:
            u = j.get("usage") or {}
            usage["provider"] = provider
            usage["calls"] = usage.get("calls", 0) + 1
            usage["retries"] = usage.get("retries", 0) + attempt
            for k in ("prompt_tokens", "completion_tokens"):
                usage[k] = usage.get(k, 0) + int(u.get(k) or 0)
            if u.get("estimated_cost") is not None:
                usage["estimated_cost_usd"] = round(usage.get("estimated_cost_usd", 0.0) + float(u["estimated_cost"]), 6)
        return text, choice.get("finish_reason") == "length"
    raise RuntimeError(f"{provider}: no answer after {retries + 1} attempts")


def check_api(model: str) -> list[str]:
    """Pre-flight: key present, and a 1-token request for the model succeeds (costs a negligible fraction of a cent)."""
    provider, name = split_model(model)
    if not _key(provider):
        return [f"no API key for {provider}: set {PROVIDERS[provider]['key_env'][0]} "
                f"(PowerShell:  $env:{PROVIDERS[provider]['key_env'][0]} = \"<your key>\")"]
    try:
        call_api("Reply with OK.", model, 0.0, 60, 1, retries=1)
    except Exception as exc:                                       # message never contains the key
        return [f"{model}: {exc}"]
    return []
