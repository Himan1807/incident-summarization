#!/usr/bin/env python3
"""
Pure-stdlib pcap parser producing Zeek-equivalent logs (conn/dns/http/tls)
plus heuristic suspicious-activity flags (NOT real Suricata signature matches).

No third-party dependencies -- struct + socket only, since this environment
cannot install scapy/dpkt/pyshark/Suricata/Zeek.

Usage: python3 pcap_parser.py <input.pcap> <output_dir> <scenario_name>
"""
import sys
import os
import json
import struct
import socket
from collections import defaultdict

# ---------- pcap reader ----------

def read_pcap(path):
    with open(path, 'rb') as f:
        global_hdr = f.read(24)
        if len(global_hdr) < 24:
            raise ValueError("truncated pcap")
        magic = struct.unpack('<I', global_hdr[:4])[0]
        if magic == 0xa1b2c3d4:
            endian = '<'
            ts_scale = 1_000_000  # microseconds
        elif magic == 0x4d3cb2a1:
            endian = '>'
            ts_scale = 1_000_000
        elif magic == 0xa1b23c4d:
            endian = '<'
            ts_scale = 1_000_000_000  # nanoseconds
        else:
            raise ValueError(f"unsupported pcap magic {hex(magic)}")

        while True:
            rec_hdr = f.read(16)
            if len(rec_hdr) < 16:
                break
            ts_sec, ts_frac, incl_len, orig_len = struct.unpack(endian + 'IIII', rec_hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            ts = ts_sec + ts_frac / ts_scale
            yield ts, data


# ---------- protocol parsers ----------

def parse_ethernet(pkt):
    if len(pkt) < 14:
        return None, None
    eth_type = struct.unpack('!H', pkt[12:14])[0]
    offset = 14
    # Skip 802.1Q VLAN tag(s)
    while eth_type == 0x8100:
        if len(pkt) < offset + 4:
            return None, None
        eth_type = struct.unpack('!H', pkt[offset + 2:offset + 4])[0]
        offset += 4
    return eth_type, offset


def parse_ipv4(pkt, offset):
    if len(pkt) < offset + 20:
        return None
    b0 = pkt[offset]
    ihl = (b0 & 0x0F) * 4
    if len(pkt) < offset + ihl:
        return None
    total_len = struct.unpack('!H', pkt[offset + 2:offset + 4])[0]
    proto = pkt[offset + 9]
    src = socket.inet_ntoa(pkt[offset + 12:offset + 16])
    dst = socket.inet_ntoa(pkt[offset + 16:offset + 20])
    return {
        'proto': proto,
        'src': src,
        'dst': dst,
        'header_len': ihl,
        'total_len': total_len,
        'payload_offset': offset + ihl,
    }


def parse_tcp(pkt, offset):
    if len(pkt) < offset + 20:
        return None
    sport, dport, seq, ack, off_flags = struct.unpack('!HHIIH', pkt[offset:offset + 14])
    data_off = ((off_flags >> 12) & 0xF) * 4
    flags = off_flags & 0x3F
    if len(pkt) < offset + data_off:
        data_off = 20
    return {
        'sport': sport, 'dport': dport, 'seq': seq,
        'flags': flags,
        'payload': pkt[offset + data_off:],
    }


def parse_udp(pkt, offset):
    if len(pkt) < offset + 8:
        return None
    sport, dport, length = struct.unpack('!HHH', pkt[offset:offset + 6])
    return {'sport': sport, 'dport': dport, 'payload': pkt[offset + 8:offset + length] if length >= 8 else pkt[offset + 8:]}


TCP_FIN = 0x01
TCP_SYN = 0x02
TCP_RST = 0x04
TCP_ACK = 0x10


# ---------- DNS ----------

def parse_dns_name(msg, off):
    labels = []
    jumps = 0
    start = off
    while True:
        if off >= len(msg):
            return None, off
        length = msg[off]
        if length == 0:
            off += 1
            break
        if (length & 0xC0) == 0xC0:
            if off + 1 >= len(msg):
                return None, off
            ptr = ((length & 0x3F) << 8) | msg[off + 1]
            if jumps == 0:
                start = off + 2
            jumps += 1
            if jumps > 20:
                return None, off
            off = ptr
            continue
        off += 1
        if off + length > len(msg):
            return None, off
        labels.append(msg[off:off + length].decode('ascii', errors='replace'))
        off += length
    end = off if jumps == 0 else start
    return '.'.join(labels), end


def parse_dns(payload):
    if len(payload) < 12:
        return None
    txid, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', payload[:12])
    is_response = bool(flags & 0x8000)
    off = 12
    questions = []
    for _ in range(qdcount):
        name, off = parse_dns_name(payload, off)
        if name is None or off + 4 > len(payload):
            break
        qtype, qclass = struct.unpack('!HH', payload[off:off + 4])
        off += 4
        questions.append({'name': name, 'qtype': qtype})
    answers = []
    if is_response:
        for _ in range(ancount):
            name, off = parse_dns_name(payload, off)
            if name is None or off + 10 > len(payload):
                break
            rtype, rclass, ttl, rdlen = struct.unpack('!HHIH', payload[off:off + 10])
            off += 10
            if off + rdlen > len(payload):
                break
            rdata = payload[off:off + rdlen]
            off += rdlen
            if rtype == 1 and len(rdata) == 4:  # A
                answers.append({'name': name, 'type': 'A', 'data': socket.inet_ntoa(rdata)})
            elif rtype == 5:  # CNAME
                cname, _ = parse_dns_name(payload, off - rdlen)
                answers.append({'name': name, 'type': 'CNAME', 'data': cname})
    return {'is_response': is_response, 'questions': questions, 'answers': answers}


# ---------- HTTP (best-effort, single-segment) ----------

HTTP_METHODS = (b'GET ', b'POST ', b'HEAD ', b'PUT ', b'OPTIONS ', b'DELETE ')


def _split_head_lines(payload):
    """Split the header block off a payload and into lines, tolerating
    non-conformant implementations that use bare \\n instead of \\r\\n
    (observed e.g. in NetSupport Manager RAT traffic)."""
    if b'\r\n\r\n' in payload:
        head = payload.split(b'\r\n\r\n', 1)[0]
    elif b'\n\n' in payload:
        head = payload.split(b'\n\n', 1)[0]
    else:
        head = payload
    # normalize CRLF to LF, then split on LF, so both styles work uniformly
    return head.replace(b'\r\n', b'\n').split(b'\n')


def try_parse_http_request(payload):
    if not payload.startswith(HTTP_METHODS):
        return None
    try:
        lines = _split_head_lines(payload)
        request_line = lines[0].decode('ascii', errors='replace')
        parts = request_line.split(' ')
        if len(parts) < 3:
            return None
        method, uri, _ = parts[0], parts[1], parts[2]
        headers = {}
        for line in lines[1:]:
            if b':' in line:
                k, v = line.split(b':', 1)
                headers[k.decode('ascii', errors='replace').strip().lower()] = v.decode('ascii', errors='replace').strip()
        return {'method': method, 'uri': uri, 'host': headers.get('host', ''), 'user_agent': headers.get('user-agent', '')}
    except Exception:
        return None


def try_parse_http_response(payload):
    if not payload.startswith(b'HTTP/'):
        return None
    try:
        lines = _split_head_lines(payload)
        status_line = lines[0].decode('ascii', errors='replace')
        headers = {}
        for line in lines[1:]:
            if b':' in line:
                k, v = line.split(b':', 1)
                headers[k.decode('ascii', errors='replace').strip().lower()] = v.decode('ascii', errors='replace').strip()
        return {'status_line': status_line, 'content_type': headers.get('content-type', ''),
                'content_disposition': headers.get('content-disposition', ''),
                'server': headers.get('server', '')}
    except Exception:
        return None


# ---------- TLS SNI ----------

def try_parse_tls_sni(payload):
    try:
        if len(payload) < 6 or payload[0] != 0x16:  # handshake record
            return None
        # record: type(1) version(2) length(2) ; handshake: type(1) length(3)
        pos = 5
        if payload[pos] != 0x01:  # ClientHello
            return None
        pos += 4  # handshake header
        pos += 2  # client version
        pos += 32  # random
        if pos >= len(payload):
            return None
        sess_id_len = payload[pos]
        pos += 1 + sess_id_len
        if pos + 2 > len(payload):
            return None
        cs_len = struct.unpack('!H', payload[pos:pos + 2])[0]
        pos += 2 + cs_len
        if pos >= len(payload):
            return None
        comp_len = payload[pos]
        pos += 1 + comp_len
        if pos + 2 > len(payload):
            return None
        ext_total_len = struct.unpack('!H', payload[pos:pos + 2])[0]
        pos += 2
        end = pos + ext_total_len
        while pos + 4 <= min(end, len(payload)):
            ext_type, ext_len = struct.unpack('!HH', payload[pos:pos + 4])
            pos += 4
            if ext_type == 0x0000:  # server_name
                sni_pos = pos + 2 + 1 + 2  # server_name_list_len, type, name_len
                name_len = struct.unpack('!H', payload[pos + 3:pos + 5])[0]
                name = payload[sni_pos:sni_pos + name_len].decode('ascii', errors='replace')
                return name
            pos += ext_len
        return None
    except Exception:
        return None


# ---------- main analysis ----------

SUSPICIOUS_UA_MARKERS = ['powershell', 'wininet', 'curl/', 'python-requests']
EXECUTABLE_EXT = ('.exe', '.dll', '.ps1', '.bat', '.vbs', '.hta', '.scr', '.jar', '.msi', '.cpl')


def analyze(pcap_path, out_dir, scenario):
    conns = {}  # 5tuple key -> record
    dns_events = []
    http_events = []
    tls_events = []
    packet_count = 0
    first_ts = None
    last_ts = None

    for ts, pkt in read_pcap(pcap_path):
        packet_count += 1
        if first_ts is None:
            first_ts = ts
        last_ts = ts

        eth_type, offset = parse_ethernet(pkt)
        if eth_type != 0x0800:  # only IPv4
            continue
        ip = parse_ipv4(pkt, offset)
        if ip is None:
            continue

        proto = ip['proto']
        payload_off = ip['payload_offset']

        if proto == 6:  # TCP
            tcp = parse_tcp(pkt, payload_off)
            if tcp is None:
                continue
            key = ('tcp', ip['src'], tcp['sport'], ip['dst'], tcp['dport'])
            rkey = ('tcp', ip['dst'], tcp['dport'], ip['src'], tcp['sport'])
            if rkey in conns:
                c = conns[rkey]
                c['resp_bytes'] += len(tcp['payload'])
                c['resp_pkts'] += 1
                direction = 'resp'
            else:
                c = conns.setdefault(key, {
                    'proto': 'tcp', 'orig_h': ip['src'], 'orig_p': tcp['sport'],
                    'resp_h': ip['dst'], 'resp_p': tcp['dport'],
                    'ts_start': ts, 'ts_end': ts,
                    'orig_bytes': 0, 'resp_bytes': 0, 'orig_pkts': 0, 'resp_pkts': 0,
                    'syn': False, 'synack': False, 'fin': False, 'rst': False,
                    'payload_sample_orig': b'', 'payload_sample_resp': b'',
                })
                c['orig_bytes'] += len(tcp['payload'])
                c['orig_pkts'] += 1
                direction = 'orig'
            c['ts_end'] = ts
            if tcp['flags'] & TCP_SYN and tcp['flags'] & TCP_ACK:
                c['synack'] = True
            elif tcp['flags'] & TCP_SYN:
                c['syn'] = True
            if tcp['flags'] & TCP_FIN:
                c['fin'] = True
            if tcp['flags'] & TCP_RST:
                c['rst'] = True

            if tcp['payload']:
                if direction == 'orig' and len(c['payload_sample_orig']) < 4096:
                    c['payload_sample_orig'] += tcp['payload'][:4096 - len(c['payload_sample_orig'])]
                if direction == 'resp' and len(c['payload_sample_resp']) < 4096:
                    c['payload_sample_resp'] += tcp['payload'][:4096 - len(c['payload_sample_resp'])]

            # HTTP
            if tcp['payload'][:8].isascii() if tcp['payload'][:8] else False:
                req = try_parse_http_request(tcp['payload'])
                if req:
                    http_events.append({
                        'ts': ts, 'src_ip': ip['src'], 'src_port': tcp['sport'],
                        'dst_ip': ip['dst'], 'dst_port': tcp['dport'],
                        'direction': 'request', **req,
                    })
                resp = try_parse_http_response(tcp['payload'])
                if resp:
                    http_events.append({
                        'ts': ts, 'src_ip': ip['src'], 'src_port': tcp['sport'],
                        'dst_ip': ip['dst'], 'dst_port': tcp['dport'],
                        'direction': 'response', **resp,
                    })

            # TLS SNI (only worth checking on client->server first data packet, typically dport 443/other)
            if tcp['payload'][:1] == b'\x16':
                sni = try_parse_tls_sni(tcp['payload'])
                if sni:
                    tls_events.append({
                        'ts': ts, 'src_ip': ip['src'], 'src_port': tcp['sport'],
                        'dst_ip': ip['dst'], 'dst_port': tcp['dport'], 'sni': sni,
                    })

        elif proto == 17:  # UDP
            udp = parse_udp(pkt, payload_off)
            if udp is None:
                continue
            key = ('udp', ip['src'], udp['sport'], ip['dst'], udp['dport'])
            rkey = ('udp', ip['dst'], udp['dport'], ip['src'], udp['sport'])
            if rkey in conns:
                c = conns[rkey]
                c['resp_bytes'] += len(udp['payload'])
                c['resp_pkts'] += 1
            else:
                c = conns.setdefault(key, {
                    'proto': 'udp', 'orig_h': ip['src'], 'orig_p': udp['sport'],
                    'resp_h': ip['dst'], 'resp_p': udp['dport'],
                    'ts_start': ts, 'ts_end': ts,
                    'orig_bytes': 0, 'resp_bytes': 0, 'orig_pkts': 0, 'resp_pkts': 0,
                    'syn': False, 'synack': False, 'fin': False, 'rst': False,
                    'payload_sample_orig': b'', 'payload_sample_resp': b'',
                })
                c['orig_bytes'] += len(udp['payload'])
                c['orig_pkts'] += 1
            c['ts_end'] = ts

            if udp['sport'] == 53 or udp['dport'] == 53:
                dns = parse_dns(udp['payload'])
                if dns:
                    dns_events.append({
                        'ts': ts, 'src_ip': ip['src'], 'dst_ip': ip['dst'],
                        'is_response': dns['is_response'],
                        'questions': dns['questions'], 'answers': dns['answers'],
                    })

    # ---- write raw logs (JSON lines, Zeek-equivalent) ----
    os.makedirs(out_dir, exist_ok=True)

    conn_log = []
    for c in conns.values():
        conn_log.append({
            'ts': round(c['ts_start'], 6),
            'duration': round(c['ts_end'] - c['ts_start'], 6),
            'proto': c['proto'],
            'orig_h': c['orig_h'], 'orig_p': c['orig_p'],
            'resp_h': c['resp_h'], 'resp_p': c['resp_p'],
            'orig_bytes': c['orig_bytes'], 'resp_bytes': c['resp_bytes'],
            'orig_pkts': c['orig_pkts'], 'resp_pkts': c['resp_pkts'],
            'syn': c['syn'], 'synack': c['synack'], 'fin': c['fin'], 'rst': c['rst'],
        })

    with open(os.path.join(out_dir, 'conn.log.json'), 'w') as f:
        json.dump(conn_log, f, indent=1)
    with open(os.path.join(out_dir, 'dns.log.json'), 'w') as f:
        json.dump(dns_events, f, indent=1)
    with open(os.path.join(out_dir, 'http.log.json'), 'w') as f:
        json.dump(http_events, f, indent=1)
    with open(os.path.join(out_dir, 'tls.log.json'), 'w') as f:
        json.dump(tls_events, f, indent=1)

    meta = {
        'scenario': scenario,
        'pcap_file': os.path.basename(pcap_path),
        'packet_count': packet_count,
        'first_ts': first_ts, 'last_ts': last_ts,
        'duration_sec': round(last_ts - first_ts, 2) if first_ts else 0,
        'connection_count': len(conns),
        'dns_event_count': len(dns_events),
        'http_event_count': len(http_events),
        'tls_event_count': len(tls_events),
    }
    with open(os.path.join(out_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2)

    print(json.dumps(meta, indent=2))
    return conn_log, dns_events, http_events, tls_events, meta


if __name__ == '__main__':
    pcap_path, out_dir, scenario = sys.argv[1], sys.argv[2], sys.argv[3]
    analyze(pcap_path, out_dir, scenario)
