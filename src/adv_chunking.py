"""Structure-aware chunking.

The baseline split JSON by word count, cutting entries in half and wasting tokens
on braces/keys. Here each aggregation entry (a domain, a download, an IP...) is
rendered as ONE compact, self-describing fact line, and a few lines are grouped
into a chunk carrying a contextual header (artifact id + what the artifact is).
"""
import json
from typing import Any

BENIGN_NOTE = ""


def _fmt_list(v, limit=4):
    v = list(v or [])
    s = ", ".join(str(x) for x in v[:limit])
    return s + (f" (+{len(v) - limit} more)" if len(v) > limit else "")


def _fact_lines(subtype: str, payload: dict) -> list[str]:
    L: list[str] = []
    facts = payload.get("facts")
    if isinstance(facts, list) and facts and all(isinstance(x, str) for x in facts):
        return facts                      # paper-dataset artifacts: one fact per line already
    if subtype == "internal_host_activity_summary":
        for h in payload.get("hosts", []):
            L.append(f"Internal host {h['internal_ip']} made {h['outbound_connections']} outbound connections "
                     f"to {h['distinct_external_ips_contacted']} distinct external IPs.")
    elif subtype.startswith("dns_query_aggregation"):
        for d in payload.get("domains", []):
            r = _fmt_list(d.get("resolved_ips"))
            L.append(f"DNS domain {d['domain']} queried {d['query_count']} times; resolved to: {r or 'no answer recorded'}.")
    elif subtype == "http_file_download_aggregation":
        for d in payload.get("downloads", []):
            L.append(f"HTTP request to {d['server_ip']}:{d['server_port']} URI {d['uri']} "
                     f"(Host: {d.get('host_header')}) by client(s) {_fmt_list(d.get('client_ips'))}; "
                     f"requests: {d.get('doc_count')}; user-agent: {_fmt_list(d.get('user_agents'), 1) or 'none recorded'}.")
    elif subtype == "external_ip_activity_aggregation":
        for d in payload.get("ips", []):
            L.append(f"External IP {d['ip']}: {d['connection_count']} connections, {d['bytes_from_server']} bytes "
                     f"received by client(s) {_fmt_list(d.get('internal_clients'))} on port(s) {_fmt_list(d.get('ports_used'))}.")
    elif subtype.startswith("tls_sni_aggregation"):
        for d in payload.get("sni_values", []):
            L.append(f"TLS SNI {d['sni']} seen {d['count']} times from client(s) {_fmt_list(d.get('clients'))}.")
    elif subtype == "non_browser_user_agent_aggregation":
        uas = payload.get("user_agents", [])
        if not uas:
            L.append("No non-browser HTTP User-Agents were observed.")
        for d in uas:
            L.append("Non-browser User-Agent: " + json.dumps(d, ensure_ascii=False))
    elif subtype == "http_server_header_aggregation":
        for d in payload.get("servers", []):
            L.append(f"HTTP Server header '{d['server_header']}' seen {d['count']} times from {_fmt_list(d.get('server_ips'))}.")
    elif subtype == "ioc_timeline":
        for e in payload.get("events", []):
            L.append(e["text"])
    elif subtype == "host_identity":
        for e in payload.get("facts", []):
            L.append(e["text"])
    return L


def _generic_lines(payload: Any, raw: str) -> list[str]:
    """Fallback for unseen artifact types (alerts, chats, tickets...): paragraph/line split."""
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return [json.dumps(x, ensure_ascii=False) for x in v]
    parts = [p.strip() for p in raw.replace("\r", "").split("\n") if p.strip()]
    return parts or [raw]


def chunk_artifacts(artifacts: list[dict], items_per_chunk: int = 4) -> list[dict]:
    chunks = []
    for a in artifacts:
        payload = a["payload"]
        lines = _fact_lines(a["subtype"], payload) if isinstance(payload, dict) else []
        if not lines:
            lines = _generic_lines(payload, a["raw_text"])
        desc = payload.get("description", "") if isinstance(payload, dict) else ""
        header = f"[{a['artifact_id']} | {a['artifact_type']}/{a['subtype']}] {desc}".strip()
        for i in range(0, len(lines), items_per_chunk):
            group = lines[i:i + items_per_chunk]
            chunks.append({
                "id": f"{a['artifact_id']}#{i // items_per_chunk}",
                "text": header + "\n" + "\n".join(group),
                "body": "\n".join(group),
                "metadata": {"artifact_id": a["artifact_id"], "artifact_type": a["artifact_type"],
                             "subtype": a["subtype"], "heuristic": a["heuristic"]},
            })
    return chunks
