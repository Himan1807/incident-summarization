import requests

_IP_ROLE_RULE = """- An internal client is the host that makes connections; an external IP or destination is the remote server. Never call a
  private-range IP (10.x, 172.16-31.x, 192.168.x) an external destination or C2 server.
"""
SYSTEM = """You are an incident-response analyst writing ONE section of a postmortem.
Rules:
- Use ONLY the evidence below. Do not invent timestamps, IPs, domains, files, causes or impact.
- Cite evidence after every claim using ONLY the evidence IDs listed under EVIDENCE (they look like {example}). Never invent an ID.
- If the evidence does not support something, write: Not established from the available artifacts.
- Keep observed facts and assessments separate; label assessments 'Assessment:'.
- Every bullet must add NEW information. Never repeat a fact or conclusion already stated in this section, and do not restate
  content that belongs to another section of the report.
- An internal client is the host that makes connections; an external IP or destination is the remote server. Never call a
  private-range IP (10.x, 172.16-31.x, 192.168.x) an external destination or C2 server.
- Cite with square brackets only, once per line, at the end of the line, e.g. {example}. No citations in parentheses.
- Do not start with a title, heading or introduction. Start directly with the bullets. No generic security advice."""


def _system(example: str, profile: str) -> str:
    text = SYSTEM.format(example=example)
    if profile == "security":
        return text
    assert _IP_ROLE_RULE in text                                   # the IP-role rule and 'security advice' are security-specific
    return text.replace(_IP_ROLE_RULE, "").replace("No generic security advice.", "No generic advice.")


def section_prompt(section: dict, evidence: str, header: str, ids: list[str] | None = None,
                   all_sections: list[str] | None = None, profile: str = "security") -> str:
    example = f"[{ids[0]}]" if ids else "[<evidence id>]"
    others = ""
    if all_sections:
        others = ("\nREPORT STRUCTURE (you write ONLY '" + section["name"] + "'; the others are written separately): "
                  + "; ".join(all_sections) + "\n")
    valid = ("\nVALID EVIDENCE IDS: " + ", ".join(ids) + "\n") if ids else ""
    if section.get("max_bullets"):
        valid += f"LENGTH: write AT MOST {section['max_bullets']} bullets, one short line each, then stop.\n"
    return (f"{_system(example, profile)}\n\nINCIDENT CONTEXT:\n{header}\n{others}\nSECTION: {section['name']}\n"
            f"TASK: {section['task']}\n{valid}\nEVIDENCE:\n{evidence}\n\nWrite the section now (Markdown bullets):")


SUMMARY_COVER = {"security": "the affected host and user, the earliest alert hour, the main C2 candidate, and the key ",
                 "service_outage": "the root-cause service with its pod and node, the earliest sign of the failure, the fault type, the user-facing impact, and the key "}


def summary_prompt(header: str, sections_text: str, profile: str = "security") -> str:
    return (f"{_system('[<evidence id>]', profile)}\n\nINCIDENT CONTEXT:\n{header}\n\nBelow are verified postmortem sections.\n"
            f"TASK: Write a 4-6 sentence Incident Summary using ONLY facts stated in these sections. Keep their citations. "
            f"Start directly with the summary (no preamble). Cover: {SUMMARY_COVER[profile]}"
            f"assessment. The query time window is NOT the incident duration: take event times only from the sections.\n\nSECTIONS:\n{sections_text}\n\nIncident Summary:")


def call_llm(prompt, S, num_predict, usage=None):
    """Ollama for plain model names (unchanged); a hosted API for prefixed names such as deepinfra:deepseek-ai/DeepSeek-V3."""
    from src.llm_api import is_api_model, call_api
    if is_api_model(S.ollama_model):
        return call_api(prompt, S.ollama_model, S.temperature, S.api_timeout_seconds, num_predict, usage)
    return call_ollama(prompt, S.ollama_url, S.ollama_model, S.temperature, S.timeout_seconds, S.num_ctx, num_predict)


def call_ollama(prompt, url, model, temperature, timeout, num_ctx=4096, num_predict=450):
    try:
        r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False,
                                     "options": {"temperature": temperature, "num_ctx": num_ctx,
                                                 "num_predict": num_predict}}, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(f"Cannot reach Ollama at {url}. Start it ('ollama serve') and make sure the model is pulled: "
                           f"'ollama pull {model}'.") from exc
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"Ollama returned an error ({exc}). Is the model '{model}' pulled? Try 'ollama pull {model}'.") from exc
    j = r.json()
    return j["response"].strip(), j.get("done_reason") == "length"   # (text, hit_token_cap)
