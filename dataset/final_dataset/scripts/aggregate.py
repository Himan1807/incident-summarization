#!/usr/bin/env python3
"""
Build compact, semantically-meaningful aggregated JSON 'chunks' from the raw
conn/dns/http/tls logs -- mirroring the paper's aggregation style (e.g. their
'Suricata High-Severity Alert Aggregation', 'File Download Aggregation').

Since we don't have a real Suricata ruleset, 'suspicious' flags here are
transparent heuristics (documented inline), not signature-engine alerts.

Usage: python3 aggregate.py <logs_dir> <out_dir> <scenario_name>
"""
import sys, os, json, ipaddress
from collections import defaultdict, Counter

EXEC_EXT = ('.exe', '.dll', '.ps1', '.bat', '.vbs', '.hta', '.scr', '.jar', '.msi', '.cpl', '.js')
BENIGN_HOST_SUBSTR = (
    'microsoft.com', 'windowsupdate.com', 'msftconnecttest.com', 'live.com',
    'office.com', 'office365.com', 'akamai', 'akadns', 'cloudflare', 'google.com',
    'gstatic.com', 'googleapis.com', 'mozilla.com', 'mozilla.org', 'digicert.com',
    'apple.com', 'ubuntu.com', 'debian.org', 'nist.gov',
)


def is_private(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


def load(logs_dir, name):
    with open(os.path.join(logs_dir, name)) as f:
        return json.load(f)


def build(logs_dir, out_dir, scenario):
    conn = load(logs_dir, 'conn.log.json')
    dns = load(logs_dir, 'dns.log.json')
    http = load(logs_dir, 'http.log.json')
    tls = load(logs_dir, 'tls.log.json')
    meta = load(logs_dir, 'meta.json')

    os.makedirs(out_dir, exist_ok=True)
    chunks = []

    # ---- 1. Internal host activity summary (identify likely infected host) ----
    internal_activity = Counter()
    internal_dest_diversity = defaultdict(set)
    for c in conn:
        if is_private(c['orig_h']) and not is_private(c['resp_h']):
            internal_activity[c['orig_h']] += 1
            internal_dest_diversity[c['orig_h']].add(c['resp_h'])
    top_internal = internal_activity.most_common(5)
    chunk = {
        'chunk_type': 'internal_host_activity_summary',
        'description': 'Internal (private-IP) hosts ranked by number of distinct outbound connections to external IPs.',
        'hosts': [
            {'internal_ip': ip, 'outbound_connections': n, 'distinct_external_ips_contacted': len(internal_dest_diversity[ip])}
            for ip, n in top_internal
        ],
    }
    chunks.append(chunk)

    # ---- 2. DNS query aggregation, flagging domains never seen resolving to Microsoft/known-CDN infra ----
    domain_counter = Counter()
    domain_to_ips = defaultdict(set)
    domain_by_client = defaultdict(set)
    for e in dns:
        for q in e['questions']:
            qname = q['name'].rstrip('.')
            if not qname:
                continue
            domain_counter[qname] += 1
            domain_by_client[qname].add(e['src_ip'] if is_private(e['src_ip']) else e['dst_ip'])
        for a in e.get('answers', []):
            if a['type'] == 'A' and a.get('data'):
                domain_to_ips[a['name'].rstrip('.')].add(a['data'])

    suspicious_domains = []
    for dom, cnt in domain_counter.most_common(200):
        if any(b in dom.lower() for b in BENIGN_HOST_SUBSTR):
            continue
        ips = sorted(domain_to_ips.get(dom, []))
        suspicious_domains.append({'domain': dom, 'query_count': cnt, 'resolved_ips': ips[:5]})
    chunk = {
        'chunk_type': 'dns_query_aggregation_non_benign',
        'description': 'Domains queried, excluding well-known Microsoft/CDN/OS-vendor infrastructure, ranked by query count.',
        'domains': suspicious_domains[:40],
    }
    chunks.append(chunk)

    # ---- 3. HTTP file download aggregation (executable-looking requests) ----
    downloads = []
    for e in http:
        if e['direction'] != 'request':
            continue
        uri = e.get('uri', '')
        low = uri.lower()
        if low.endswith(EXEC_EXT) or any(seg in low for seg in ('/get-file', '/download', '.php?', 'gate.php')):
            downloads.append({
                'ts': e['ts'], 'client_ip': e['src_ip'], 'server_ip': e['dst_ip'], 'server_port': e['dst_port'],
                'host_header': e.get('host', ''), 'uri': uri, 'user_agent': e.get('user_agent', ''),
            })
    # group by (server_ip, uri) for compactness
    grouped = defaultdict(lambda: {'doc_count': 0, 'client_ips': set(), 'user_agents': set()})
    for d in downloads:
        key = (d['server_ip'], d['server_port'], d['uri'])
        g = grouped[key]
        g['doc_count'] += 1
        g['client_ips'].add(d['client_ip'])
        g['user_agents'].add(d['user_agent'])
        g['host_header'] = d['host_header']
    file_download_chunk = {
        'chunk_type': 'http_file_download_aggregation',
        'description': 'HTTP requests to executable-looking paths or common malware-delivery patterns, grouped by server+URI.',
        'downloads': [
            {
                'server_ip': k[0], 'server_port': k[1], 'uri': k[2],
                'host_header': v.get('host_header', ''),
                'doc_count': v['doc_count'],
                'client_ips': sorted(v['client_ips']),
                'user_agents': sorted(u for u in v['user_agents'] if u),
            }
            for k, v in grouped.items()
        ],
    }
    chunks.append(file_download_chunk)

    # ---- 4. High-value external IP aggregation (repeated contact + file activity) ----
    ext_ip_stats = defaultdict(lambda: {'conn_count': 0, 'bytes_from_server': 0, 'internal_clients': set(), 'ports': set()})
    for c in conn:
        if is_private(c['orig_h']) and not is_private(c['resp_h']):
            s = ext_ip_stats[c['resp_h']]
            s['conn_count'] += 1
            s['bytes_from_server'] += c['resp_bytes']
            s['internal_clients'].add(c['orig_h'])
            s['ports'].add(c['resp_p'])
    ranked_ext = sorted(ext_ip_stats.items(), key=lambda kv: (-kv[1]['bytes_from_server'], -kv[1]['conn_count']))
    external_ip_chunk = {
        'chunk_type': 'external_ip_activity_aggregation',
        'description': 'External IPs ranked by bytes received by internal clients (server->client), a proxy for payload/data delivery.',
        'ips': [
            {'ip': ip, 'connection_count': s['conn_count'], 'bytes_from_server': s['bytes_from_server'],
             'internal_clients': sorted(s['internal_clients']), 'ports_used': sorted(s['ports'])}
            for ip, s in ranked_ext[:20]
        ],
    }
    chunks.append(external_ip_chunk)

    # ---- 5. TLS SNI aggregation ----
    sni_counter = Counter()
    sni_clients = defaultdict(set)
    for e in tls:
        sni_counter[e['sni']] += 1
        sni_clients[e['sni']].add(e['src_ip'])
    non_benign_sni = [
        {'sni': s, 'count': c, 'clients': sorted(sni_clients[s])}
        for s, c in sni_counter.most_common(100)
        if not any(b in s.lower() for b in BENIGN_HOST_SUBSTR)
    ]
    chunks.append({
        'chunk_type': 'tls_sni_aggregation_non_benign',
        'description': 'TLS ClientHello SNI values seen, excluding well-known vendor/CDN infrastructure.',
        'sni_values': non_benign_sni[:40],
    })

    # ---- 6. Non-browser User-Agent aggregation (heuristic, not a real signature match) ----
    # Rather than matching a fixed keyword list (which silently misses anything
    # not on the list -- e.g. 'NetSupport Manager/1.3'), report every UA that
    # doesn't look like a real browser or a small set of well-known OS-vendor
    # update agents, and let the analyst/LLM judge it. This trades precision
    # for not hiding unknown tools.
    BROWSER_MARKERS = ('mozilla/', 'opera/')
    KNOWN_OS_AGENTS = ('microsoft bits', 'microsoft-cryptoapi', 'microsoft ncsi',
                       'microsoft-delivery-optimization', 'windows-update-agent')
    ua_hits = defaultdict(lambda: {'count': 0, 'hosts': set(), 'servers': set()})
    for e in http:
        if e['direction'] != 'request':
            continue
        ua_raw = e.get('user_agent') or ''
        ua = ua_raw.lower()
        if not ua_raw:
            continue
        if any(m in ua for m in BROWSER_MARKERS):
            continue
        if any(m in ua for m in KNOWN_OS_AGENTS):
            continue
        ua_hits[ua_raw]['count'] += 1
        ua_hits[ua_raw]['hosts'].add(e['src_ip'])
        ua_hits[ua_raw]['servers'].add(e['dst_ip'])
    chunks.append({
        'chunk_type': 'non_browser_user_agent_aggregation',
        'description': 'Every distinct HTTP User-Agent that is not a recognizable browser or common OS-vendor update agent. Deliberately broad (not a fixed malware-keyword list) so unfamiliar tool identifiers are not silently dropped -- includes both malicious and benign findings (e.g. legitimate remote-support/update tools) for human/LLM triage.',
        'user_agents': [
            {'user_agent': ua, 'count': v['count'], 'client_ips': sorted(v['hosts']), 'server_ips': sorted(v['servers'])}
            for ua, v in sorted(ua_hits.items(), key=lambda kv: -kv[1]['count'])
        ],
    })

    # ---- 7. Server header aggregation (identifies server-side software, e.g. 'NetSupport Gateway/1.92') ----
    server_hits = defaultdict(lambda: {'count': 0, 'servers': set()})
    for e in http:
        if e['direction'] != 'response':
            continue
        srv = e.get('server', '')
        if srv:
            server_hits[srv]['count'] += 1
            server_hits[srv]['servers'].add(e['src_ip'])
    chunks.append({
        'chunk_type': 'http_server_header_aggregation',
        'description': 'Distinct HTTP Server: response headers seen, with the responding IP(s). Useful for identifying C2 server software (e.g. RAT gateway banners) even when the client-side request looked otherwise unremarkable.',
        'servers': [
            {'server_header': srv, 'count': v['count'], 'server_ips': sorted(v['servers'])}
            for srv, v in sorted(server_hits.items(), key=lambda kv: -kv[1]['count'])
        ],
    })

    with open(os.path.join(out_dir, 'chunks.json'), 'w') as f:
        json.dump({'scenario': scenario, 'meta': meta, 'chunks': chunks}, f, indent=2)

    print(f"{scenario}: wrote {len(chunks)} chunks -> {out_dir}/chunks.json")
    return chunks


if __name__ == '__main__':
    logs_dir, out_dir, scenario = sys.argv[1], sys.argv[2], sys.argv[3]
    build(logs_dir, out_dir, scenario)
