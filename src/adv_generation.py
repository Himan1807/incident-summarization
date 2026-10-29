import requests

SYSTEM = """You are an incident-response analyst writing ONE section of a postmortem.
Rules:
- Use ONLY the evidence below. Do not invent timestamps, IPs, domains, files, causes or impact.
- Cite evidence after every claim using ONLY the evidence IDs listed under EVIDENCE (they look like {example}). Never invent an ID.
- If the evidence does not support something, write: Not established from the available artifacts.
- Keep observed facts and assessments separate; label assessments 'Assessment:'.
- Every bullet must add NEW information. Never repeat a fact or conclusion already stated in this section, and do not restate
  content that belongs to another section of the report.
- Do not start with a title, heading or introduction. Start directly with the bullets. No generic security advice."""


def section_prompt(section: dict, evidence: str, header: str, ids: list[str] | None = None,
                   all_sections: list[str] | None = None) -> str:
    example = f"[{ids[0]}]" if ids else "[<evidence id>]"
    others = ""
    if all_sections:
        others = ("\nREPORT STRUCTURE (you write ONLY '" + section["name"] + "'; the others are written separately): "
                  + "; ".join(all_sections) + "\n")
    valid = ("\nVALID EVIDENCE IDS: " + ", ".join(ids) + "\n") if ids else ""
    return (f"{SYSTEM.format(example=example)}\n\nINCIDENT CONTEXT:\n{header}\n{others}\nSECTION: {section['name']}\n"
            f"TASK: {section['task']}\n{valid}\nEVIDENCE:\n{evidence}\n\nWrite the section now (Markdown bullets):")


def summary_prompt(header: str, sections_text: str) -> str:
    return (f"{SYSTEM.format(example='[<evidence id>]')}\n\nINCIDENT CONTEXT:\n{header}\n\nBelow are verified postmortem sections.\n"
            f"TASK: Write a 4-6 sentence Incident Summary using ONLY facts stated in these sections. Keep their citations. "
            f"Start directly with the summary (no preamble). The query time window is NOT the incident duration: take event times "
            f"only from the sections.\n\nSECTIONS:\n{sections_text}\n\nIncident Summary:")


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
