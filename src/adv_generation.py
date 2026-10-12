import requests

SYSTEM = """You are an incident-response analyst writing ONE section of a postmortem.
Rules:
- Use ONLY the evidence below. Do not invent timestamps, IPs, domains, files, causes or impact.
- Cite the evidence ID in square brackets after every claim, e.g. [2025-01-22-03#0].
- If the evidence does not support something, write: Not established from the available artifacts.
- Keep observed facts and assessments separate; label assessments 'Assessment:'.
- Be concise: bullet points, no preamble, no generic security advice."""


def section_prompt(section: dict, evidence: str, header: str) -> str:
    return (f"{SYSTEM}\n\nINCIDENT CONTEXT:\n{header}\n\nSECTION: {section['name']}\n"
            f"TASK: {section['task']}\n\nEVIDENCE:\n{evidence}\n\nWrite the section now (Markdown bullets):")


def summary_prompt(header: str, sections_text: str) -> str:
    return (f"{SYSTEM}\n\nINCIDENT CONTEXT:\n{header}\n\nBelow are verified postmortem sections.\n"
            f"TASK: Write a 4-6 sentence Incident Summary using ONLY facts stated in these sections. Keep the citations.\n\n"
            f"SECTIONS:\n{sections_text}\n\nIncident Summary:")


def call_ollama(prompt, url, model, temperature, timeout, num_ctx=4096, num_predict=450) -> str:
    r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False,
                                 "options": {"temperature": temperature, "num_ctx": num_ctx,
                                             "num_predict": num_predict}}, timeout=timeout)
    r.raise_for_status()
    return r.json()["response"].strip()
