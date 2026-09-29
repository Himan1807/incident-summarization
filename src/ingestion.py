import json
from pathlib import Path
from typing import Any

def load_incident(path: str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)

def artifact_to_documents(incident: dict[str, Any]) -> list[dict[str, Any]]:
    documents = []
    metadata = incident.get("metadata", {})
    artifact_sections = [
        "alerts", "logs", "metrics", "changes",
        "communications", "investigation_notes"
    ]

    for section in artifact_sections:
        values = incident.get(section, [])
        if isinstance(values, str):
            values = [values]

        for index, value in enumerate(values):
            text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            documents.append({
                "text": text,
                "metadata": {
                    "incident_id": metadata.get("incident_id", "unknown"),
                    "artifact_type": section,
                    "artifact_index": index,
                    "service": metadata.get("service", "unknown"),
                    "severity": metadata.get("severity", "unknown"),
                    "timestamp": metadata.get("timestamp", "unknown")
                }
            })

    return documents
