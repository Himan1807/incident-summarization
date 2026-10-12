"""Raw-log enrichment (deterministic, no LLM).

The aggregated artifacts carry no timestamps, so a baseline LLM writes
"[insert date]". This module looks up each indicator of compromise (IOC) in the
raw Zeek-style logs (dns/http/tls/conn .log.json) and emits NEW artifacts with
first/last-seen UTC timestamps, which become retrievable evidence for the
Timeline / Detection sections.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Only client-style names: server/DC names (WIN-...) are queried BY clients and would be mislabelled.
HOST_RE = re.compile(r"^((?:DESKTOP|LAPTOP)-[A-Z0-9]+)\.(.+)$", re.I)
BENIGN_HINTS = ("microsoft", "msn.com", "bing.com", "windows.", "skype", "msftconnecttest", "live.com",
                "office", "azure", "akamai", "google", "gstatic", "digicert", "_ldap.", "_kerberos.", "wpad.",
                "ntp.org", "nvidia.com", "mshome.net", "edge.")


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def _load(folder: Path, name: str) -> list[dict]:
    p = folder / f"{name}.log.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def _collect_iocs(artifacts: list[dict]):
    ips, domains, urls, client = [], [], [], None
    for a in artifacts:
        p, st = a["payload"], a["subtype"]
        if not isinstance(p, dict):
            continue
        if st == "internal_host_activity_summary" and p.get("hosts"):
            client = p["hosts"][0]["internal_ip"]
        elif st == "external_ip_activity_aggregation":
            ips += [d["ip"] for d in p.get("ips", [])[:6]]
        elif st == "http_file_download_aggregation":
            for d in p.get("downloads", []):
                urls.append((d["server_ip"], d["uri"]))
                ips.append(d["server_ip"])
        elif st.startswith("dns_query_aggregation"):
            domains += [d["domain"] for d in p.get("domains", []) if not any(h in d["domain"].lower() for h in BENIGN_HINTS)][:8]
        elif st == "http_server_header_aggregation":
            ips += [ip for d in p.get("servers", []) for ip in d.get("server_ips", [])]
        elif st.startswith("tls_sni_aggregation"):
            ips += [d["sni"] for d in p.get("sni_values", []) if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", d["sni"])]
            domains += [d["sni"] for d in p.get("sni_values", []) if not any(h in d["sni"].lower() for h in BENIGN_HINTS)][:5]
    uniq = lambda xs: list(dict.fromkeys(xs))
    return client, uniq(ips), uniq(domains), uniq(urls)


def build_enrichment(artifacts: list[dict], logs_dir: str, scenario: str = "inc") -> list[dict]:
    folder = Path(logs_dir)
    dns, http, tls, conn = (_load(folder, n) for n in ("dns", "http", "tls", "conn"))
    if not (dns or http or tls or conn):
        return []
    client, ips, domains, urls = _collect_iocs(artifacts)

    events: list[tuple[float, str]] = []

    # 1) first request per download URL
    for ip, uri in urls:
        hits = [h for h in http if h.get("dst_ip") == ip and h.get("uri") == uri]
        if hits:
            ts = min(h["ts"] for h in hits)
            events.append((ts, f"First seen {_iso(ts)}: HTTP {hits[0].get('method', 'GET')} to {ip}{uri} "
                               f"(Host: {hits[0].get('host')}) from {hits[0].get('src_ip')}; {len(hits)} request(s)."))
    # 2) first/last contact per external IP
    for ip in ips:
        tss = [c["ts"] for c in conn if c.get("resp_h") == ip]
        tss += [h["ts"] for h in http if h.get("dst_ip") == ip]
        tss += [t["ts"] for t in tls if t.get("dst_ip") == ip]
        if tss:
            events.append((min(tss), f"External IP {ip}: first contact {_iso(min(tss))}, last contact {_iso(max(tss))}, "
                                     f"{len(tss)} logged events (conn/http/tls)."))
    # 3) first/last DNS query per domain
    for dom in domains:
        tss = [d["ts"] for d in dns
               if any(q.get("name", "").lower() == dom.lower() for q in d.get("questions", []))]
        if tss:
            events.append((min(tss), f"Domain {dom}: first queried {_iso(min(tss))}, last queried {_iso(max(tss))}, "
                                     f"{len(tss)} DNS events."))
    events.sort()
    out = []
    if events:
        out.append({"artifact_id": f"{scenario}-E1", "artifact_type": "timeline_enrichment", "subtype": "ioc_timeline",
                    "payload": {"description": "Chronological first/last-seen timestamps (UTC) for indicators, derived from raw logs.",
                                "events": [{"text": t} for _, t in events]},
                    "raw_text": "", "heuristic": False})
    # 4) host identity from DNS self-registration of the client
    facts = []
    seen = set()
    for d in dns:
        if client and d.get("src_ip") != client:
            continue
        for q in d.get("questions", []):
            m = HOST_RE.match(q.get("name", ""))
            if m and m.group(1).upper() not in seen:
                seen.add(m.group(1).upper())
                facts.append({"text": f"Client {client} appears to self-register in DNS as host {m.group(1).upper()} "
                                      f"in domain {m.group(2)} (first seen {_iso(d['ts'])})."})
    if facts:
        out.append({"artifact_id": f"{scenario}-E2", "artifact_type": "timeline_enrichment", "subtype": "host_identity",
                    "payload": {"description": "Host identity hints derived from DNS queries of the suspected client.",
                                "facts": facts}, "raw_text": "", "heuristic": True})
    return out
