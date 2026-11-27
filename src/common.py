"""Helpers shared by the RAG pipeline (pipeline_adv.py) and the no-RAG condition (no_rag.py)."""


def incident_header(meta: dict, description: str) -> str:
    """Incident context given to the LLM in every prompt: title, capture or query window, scope and the neutral description."""
    lo = meta.get("capture_start") or meta.get("query_window_start")
    hi = meta.get("capture_end") or meta.get("query_window_end")
    label = "Capture window" if meta.get("capture_start") else "Query time window"
    return (f"Title: {meta.get('title')}; {label} (UTC): {lo} to {hi}; "
            f"Scope: {meta.get('artifact_scope_note', '')}\nDescription: {description}")
