"""Artifact-generic ingestion for the advanced pipeline.

Reads the canonical `rag_input.json` (explicit `artifacts` list) and falls back
to the legacy `starter_input.json` schema (alerts/logs/... sections).
`reference_qa.json` is NEVER read here: it is evaluation-only.
"""
import json
from pathlib import Path
from typing import Any


def _parse_json(text: Any):
    if isinstance(text, (dict, list)):
        return text
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return None


def load_artifacts(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    meta = data.get("metadata", {})
    artifacts: list[dict[str, Any]] = []

    if "artifacts" in data:                      # rag_input.json
        for a in data["artifacts"]:
            artifacts.append({
                "artifact_id": a["artifact_id"],
                "artifact_type": a.get("artifact_type", "unknown"),
                "subtype": a.get("subtype", a.get("source", "unknown")),
                "payload": _parse_json(a["content"]) if a.get("content") is not None else None,
                "raw_text": a["content"] if isinstance(a.get("content"), str) else json.dumps(a.get("content")),
                "heuristic": a.get("metadata", {}).get("heuristic", False),
            })
        description = data.get("incident_description", "")
    else:                                        # starter_input.json
        description = ""
        idx = 0
        for section in ["alerts", "logs", "metrics", "changes", "communications", "investigation_notes"]:
            vals = data.get(section, [])
            vals = [vals] if isinstance(vals, str) else vals
            for v in vals:
                payload = _parse_json(v)
                if section == "investigation_notes" and payload is None:
                    description = v
                    continue
                idx += 1
                subtype = payload.get("chunk_type", section) if isinstance(payload, dict) else section
                artifacts.append({
                    "artifact_id": f"{meta.get('scenario', 'inc')}-{idx:02d}",
                    "artifact_type": section, "subtype": subtype,
                    "payload": payload, "raw_text": v if isinstance(v, str) else json.dumps(v),
                    "heuristic": False,
                })
    return {"metadata": meta, "description": description, "artifacts": artifacts,
            "questions": data.get("investigation_questions", [])}
