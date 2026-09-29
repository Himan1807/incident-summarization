import requests

SYSTEM_INSTRUCTION = """You are an incident-response analyst.
Generate a factual postmortem only from the supplied incident artifacts.
Do not invent timestamps, services, causes, actions, or metrics.
If evidence is missing, write 'Not established from the available artifacts'.
Clearly separate observed evidence from inferred root cause.
"""

def build_prompt(context: str) -> str:
    return f"""{SYSTEM_INSTRUCTION}

Use this structure:
1. Incident Summary
2. Impact
3. Timeline
4. Detection
5. Investigation Findings
6. Root Cause
7. Contributing Factors
8. Resolution and Recovery
9. Corrective and Preventive Actions
10. Open Questions

Incident artifacts:
{context}

Return a clear, professional postmortem in Markdown.
"""

def generate_postmortem(
    prompt: str,
    ollama_url: str,
    model: str,
    temperature: float,
    timeout: int
) -> str:
    response = requests.post(
        ollama_url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        },
        timeout=timeout
    )
    response.raise_for_status()
    return response.json()["response"]
