#!/usr/bin/env python3
"""Write reference Q&A json files per scenario, built from facts independently
extracted by pcap_parser.py/aggregate.py/DHCP-option parsing, cross-checked
against the published exercise questions and (for 2025-01-22 only) the paper's
own worked example in Section 4.4, since that scenario is demonstrably the
same underlying capture."""
import json, os

OUT = '/home/claude/dataset_work/qa'
os.makedirs(OUT, exist_ok=True)

scenarios = {
    "2025-01-22": {
        "source": "malware-traffic-analysis.net 2025-01-22, 'Download from Fake Software Site' "
                   "(same underlying capture as the paper's Section 4.4 worked example)",
        "confidence": "high - independently re-derived AND cross-checked against the paper's published answer",
        "qa": [
            {"question": "What is the IP address of the infected Windows client?",
             "answer": "10.1.17.215",
             "evidence": "Highest-volume internal host by outbound connections (300 connections to 137 distinct external IPs); matches paper Section 4.4."},
            {"question": "What is the MAC address of the infected Windows client?",
             "answer": "00:d0:b7:26:4a:74",
             "evidence": "Ethernet source address on packets originating from 10.1.17.215."},
            {"question": "What is the host name of the infected Windows client?",
             "answer": "DESKTOP-L8C5GSJ",
             "evidence": "DHCP option 12 (Host Name) and option 81 (Client FQDN: DESKTOP-L8C5GSJ.bluemoontuesday.com) from the client's DHCP lease request; also seen as a DNS self-registration query. Matches paper Section 4.4."},
            {"question": "What is the user account name from the infected Windows client?",
             "answer": "shutchenson (per published paper answer; not independently re-derived here -- this dataset's parser does not decode Kerberos, which is where this was originally attributed)",
             "evidence": "Cited from Cadet et al. Section 4.4, not re-derived by this pipeline."},
            {"question": "What are the IP addresses used for C2 servers for this infection?",
             "answer": "5.252.153.241 (port 80, confirmed: served /api/file/get-file/29842.ps1 and related payloads). 45.125.66.32 is a secondary high-volume external IP (9.3 MB delivered over the non-standard TCP port 2917) worth further review as a possible second-stage channel.",
             "evidence": "http_file_download_aggregation and external_ip_activity_aggregation chunks."},
            {"question": "What malicious files were downloaded, and from where?",
             "answer": "Multiple files fetched from 5.252.153.241 over HTTP: /api/file/get-file/29842.ps1, /api/file/get-file/pas.ps1, /api/file/get-file/264872, plus TeamViewer-named paths (/api/file/get-file/TeamViewer, /Teamviewer_Resource_fr, /TV) suggesting a remote-monitoring tool was also staged.",
             "evidence": "http_file_download_aggregation chunk."},
            {"question": "What domain name was used for the fake Google Authenticator page?",
             "answer": "Not confirmed by this pipeline -- the initial malvertising redirect chain (Bing ad click) was not captured or not distinguishable from benign Bing/Microsoft traffic in this pass. Flagged as an open item.",
             "evidence": "None found; documented as a known gap rather than guessed."},
        ],
    },
    "2025-06-13": {
        "source": "malware-traffic-analysis.net 2025-06-13, Active Directory environment traffic exercise",
        "confidence": "medium - independently derived by this pipeline; no official answer key was accessible (distributed as a password-protected PDF this pipeline cannot open)",
        "qa": [
            {"question": "What is the IP address of the infected Windows client?",
             "answer": "10.6.13.133",
             "evidence": "Only internal host observed with sustained external beaconing (169 outbound connections to 72 distinct external IPs)."},
            {"question": "What is the MAC address of the infected Windows client?",
             "answer": "24:77:03:ac:97:df",
             "evidence": "Ethernet source address on packets from 10.6.13.133."},
            {"question": "What is the host name of the infected Windows client?",
             "answer": "DESKTOP-5AVE44C",
             "evidence": "DHCP option 12/81 (FQDN DESKTOP-5AVE44C.massfriction.com); also seen as a DNS self-registration query."},
            {"question": "What is the user account name from the infected Windows client?",
             "answer": "Not determined -- requires Kerberos/SMB authentication log parsing, which this lightweight parser does not implement.",
             "evidence": "Known gap."},
            {"question": "What is the Active Directory domain and domain controller?",
             "answer": "Domain: massfriction.com. Domain controller: WIN-DQL4WFWJXQ4.massfriction.com.",
             "evidence": "LDAP SRV record queries (_ldap._tcp...massfriction.com) and direct DNS query for WIN-DQL4WFWJXQ4.massfriction.com."},
            {"question": "What C2 infrastructure did the infected host communicate with?",
             "answer": "Two rotating C2 fronts, both proxied through Cloudflare: windows-msgas.com (typosquat of Windows telemetry domains; resolves to Cloudflare anycast IPs 104.21.16.1/104.21.80.1/104.21.64.1/104.21.96.1/104.21.112.1) and varying-rentals-calgary-predict.trycloudflare.com (an explicit Cloudflare Tunnel subdomain; resolves to 104.16.230.132/104.16.231.132). Both received periodic HTTP POST requests every ~30-90 seconds with randomized token-like URI paths and no User-Agent header -- a beaconing pattern consistent with a C2 implant using Cloudflare Tunnel to hide its true origin.",
             "evidence": "http_file_download_aggregation / raw http.log.json request pattern; dns_query_aggregation_non_benign chunk."},
            {"question": "What is the likely initial access vector?",
             "answer": "Not conclusively determined. hillcoweb.com and www.truglomedspa.com appear as one-off DNS lookups shortly before the beaconing begins and may be part of a malvertising/redirect chain, but this pipeline could not confirm a download event tied to them.",
             "evidence": "dns_query_aggregation_non_benign chunk; flagged as a hypothesis, not a confirmed finding."},
        ],
    },
    "2026-02-28": {
        "source": "malware-traffic-analysis.net 2026-02-28, 'Easy As 123' (published narrative: NetSupport Manager RAT calling back to 45.131.214.85 over TCP/443)",
        "confidence": "medium-high - independently derived and consistent with the site's published scenario narrative; official written answer key not accessible (password-protected PDF)",
        "qa": [
            {"question": "What is the IP address of the infected Windows client?",
             "answer": "10.2.28.88",
             "evidence": "Only internal host with sustained external activity (186 connections to 98 distinct external IPs), including the long-lived C2 session below."},
            {"question": "What is the MAC address of the infected Windows client?",
             "answer": "00:19:d1:b2:4d:ad",
             "evidence": "Ethernet source address on packets from 10.2.28.88. Note: a second, unrelated device (mac 00:e0:4c:68:08:00, DHCP hostname 'brads-MBP') is also present on the network segment but shows no malicious activity."},
            {"question": "What is the host name of the infected Windows client?",
             "answer": "DESKTOP-TEYQ2NR",
             "evidence": "DHCP option 12/81 (FQDN DESKTOP-TEYQ2NR.easyas123.tech)."},
            {"question": "What is the user account name / full name from the infected system?",
             "answer": "Not determined -- requires authentication/SMB log parsing not implemented by this pipeline.",
             "evidence": "Known gap."},
            {"question": "What are the C2 indicators for this infection?",
             "answer": "Domain vadusa.xyz resolves to 45.131.214.85. The infected host queried vadusa.xyz at 19:55:51 UTC and, within the same second, opened a TCP session to 45.131.214.85:443 that stayed open for the rest of the capture (~4.3 hours, 276 packets each direction, only ~63 KB sent / ~2 KB received) -- a low-bandwidth, long-lived pattern consistent with a remote-access-tool control channel (matches the published NetSupport Manager RAT narrative for this exercise) rather than a real TLS/HTTPS session.",
             "evidence": "dns.log.json (A record vadusa.xyz -> 45.131.214.85) and conn.log.json entry for the 10.2.28.88:51912 <-> 45.131.214.85:443 session."},
            {"question": "What is the Active Directory domain and domain controller?",
             "answer": "Domain: easyas123.tech. Domain controller: EASYAS123-DC.easyas123.tech.",
             "evidence": "LDAP SRV queries and direct DNS query for EASYAS123-DC.easyas123.tech."},
        ],
    },
}

for name, obj in scenarios.items():
    with open(os.path.join(OUT, f'{name}.json'), 'w') as f:
        json.dump(obj, f, indent=2)
    print(f"wrote {name}.json ({len(obj['qa'])} Q&A pairs)")
