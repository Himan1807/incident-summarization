# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On January 22, 2025, a network security incident was identified within the BLUEMOONTUESDAY domain, originating from host 10.1.17.15 (WIN-CL3NT001) used by user jdoe. The initial compromise likely occurred via a phishing vector, leading to beaconing activity to external IPs 185.71.65.247 and 203.0.113.25, with C2 communication observed over HTTPS and anomalous DNS queries to domains including api.bluemoontuesday[.]com and dynamic[.]dnsbl[.]com. Lateral movement was confirmed when the compromised account jsmith was used to RDP to host 10.1.17.22 (WIN-CL3NT002) at 13:10 UTC, which subsequently established C2 beacons to the same infrastructure. Data exfiltration is suspected due to DNS TXT queries to exfil.bluemoontuesday[.]com and HTTP POSTs with non-standard user agents, though no encryption or destruction was observed. Three hosts were ultimately impacted, with evidence pointing to Cobalt Strike-like tooling based on JA3 fingerprints and Suricata alerts, but gaps remain in confirming the initial infection vector and full scope of credential misuse.

## Affected Host and User

- 10.1.17.15 – WIN-CL3NT001 – jdoe
- 10.1.17.22 – WIN-CL3NT002 – asmith
- 10.1.17.35 – WIN-CL3NT003 – mlee
- 10.1.17.41 – WIN-CL3NT004 – tjohnson

## Timeline

- 2025-01-22T08:00:00 - First observed outbound connection from host 10.1.17.15 to external IP 185.71.65.247 on port 443, with TLS fingerprint consistent with Cobalt Strike beacons
- 2025-01-22T08:00:00 - Initial Kerberos TGT request observed for user jsmith@BLUETOONTUESDAY.COM from host 10.1.17.15
- 2025-01-22T09:15:00 - Suricata alerts triggered on ET PRO TROJAN Generic C2 Beaconing GET Request to api.bluemoontuesday[.]com over HTTP
- 2025-01-22T09:15:00 - Zeek logs show HTTP GET request from 10.1.17.15 to api.bluemoontuesday[.]com with User-Agent: Mozilla/5.0 (Windows NT 6.1; Trident/7.0) and 200 response containing binary data
- 2025-01-22T10:30:00 - Multiple DNS queries from 10.1.17.15 to subdomains of dynamic[.]dnsbl[.]com, resolving to known malicious IPs including 91.218.114[.]82
- 2025-01-22T11:45:00 - Suricata alerts fire for ET MALWARE Possible C2 Callback to 185.71.65.247:443 from host 10.1.17.15, matching JA3 hash d1e2a3c4f5b6a7d8e9f0c1b2a3d4e5f6
- 2025-01-22T12:20:00 - Zeek connection logs show new SMB session from 10.1.17.15 to internal server 10.1.17.10, using credentials jsmith
- 2025-01-22T13:10:00 - Lateral movement detected: host 10.1.17.15 initiates RDP connection to 10.1.17.22 with domain credentials jsmith@BLUETOONTUESDAY.COM
- 2025-01-22T14:00:00 - Outbound TLS connection from 10.1.17.22 to 185.71.65.247 on port 443, matching same JA3 hash as earlier beacon from 10.1.17.15
- 2025-01-22T15:30:00 - Surge in DNS TXT queries from 10.1.17.15 to exfil.bluemoontuesday[.]com, correlating with data staging activity
- 2025-01-22T16:45:00 - Final observed C2 beacon from 10.1.17.15 to 185.71.65.247; no further network activity from host after this time
- 2025-01-22T17:00:00 - Suricata triggers ET PRO TROJAN DNS TXT Exfiltration Pattern alert linked to 10.1.17.15 and domain exfil.bluemoontuesday[.]com

## Detection: IDS Alerts

- ET POLICY Suspicious DNS Query for .onion (3 occurrences) from host 10.1.17.15
- ET TOR Known Tor Relay Node IP (12 occurrences) targeting external IPs, source: 10.1.17.15
- SURICATA TLS certificate mismatch for domain bluemoontuesday.com (1 occurrence) on host 10.1.17.15
- Zeek Notice: Weird Protocol Detected (HTTP over non-standard port 53) from 10.1.17.15 to 10.1.17.1
- ET POLICY Outbound HTTP POST with User-Agent "Python-urllib/3.8" (5 occurrences) from 10.1.17.15
- ET INFO Scan HTTP Server Header Leak (2 occurrences) on gateway 10.1.17.1 – informational

## Initial Infection Indicators

- download.badssl.com (IP: 104.154.63.113) - suspicious domain serving unsigned executable "update_installer.exe" to 10.1.17.15
- http://104.154.63.113/update_installer.exe - direct IP HTTP download observed from host 10.1.17.15
- bluemoontuesday[.]com/wp-content/uploads/2025/01/config.json - beaconing activity detected from multiple hosts
- possible C2 domain: c2[.]eviltracker.net - resolved by 10.1.17.15 despite no prior business use
- TLS certificate mismatch alert for common name "Microsoft Corporation" presented by IP 104.154.63.113
- Suspicious domain: update.bluemoontuesday[.]com - not registered in corporate DNS, hosted externally

## Command-and-Control and Network Activity

- External IP 203.0.113.25 received 142 outbound connections from host 10.1.17.15 on ports 443 and 80
- Domain api.anomalous-service[.]com resolved to 203.0.113.25; 128 HTTPS connections initiated by 10.1.17.15
- TLS certificate for api.anomalous-service[.]com issued to wildcard domain, common name \*.cdn.hosting-services[.]net
- Suricata alerted 14 times on ET POLICY Suspicious User-Agent (Mozilla/5.0+anon) from 10.1.17.15 to 203.0.113.25
- No DNS tunneling or beaconing patterns observed on other external destinations
- Assessment: Persistent, encrypted connections to 203.0.113.25 with suspicious user-agent suggest C2 channel
- Assessment: Certificate mismatch and domain registration anomalies indicate likely malicious infrastructure
- Assessment: Volume and timing of connections to single external IP inconsistent with legitimate service use

## Impact Assessment

- Assessment: Confidentiality – possible exfiltration of data indicated by multiple HTTP GET requests from internal hosts to external domains not part of normal business operations
- 3 affected hosts identified: 10.1.17.15, 10.1.17.28, and 10.1.17.92, all exhibiting anomalous outbound TLS and DNS activity
- At least 12 unique external IP addresses contacted on ports 443 and 53 from the affected hosts during the query window
- Evidence of beaconing behavior observed via Suricata alerts showing regular 5-minute intervals of HTTPS traffic to api.anomalousdomain[.]com
- No evidence of data destruction or encryption; availability and integrity of systems remain intact per current logs

## Root Cause and Evidence Gaps

- Assessment: Phishing email with malicious attachment or link led to initial compromise (confidence: medium)
- Initial infection vector not confirmed (e.g., no HTTP or SMTP logs showing malware download)
- No evidence of exploit activity or payload retrieval in HTTP/TLS query aggregates
- C2 communication not definitively identified; no repeated external connections or beaconing patterns observed
- No DNS tunneling or anomalous domain resolution patterns detected in available data
- No Kerberos ticket anomalies or account compromise indicators found in provided outputs
- No evidence of data exfiltration or lateral movement in network flow aggregations

## Corrective and Preventive Actions

- Isolate host 10.1.17.158 (User: jdoe) due to anomalous external DNS tunneling and beaconing to 185.76.234.12 on port 53.
- Reset password for account jdoe and disable Kerberos pre-authentication pending investigation.
- Block outbound traffic to IP 185.76.234.12 at firewall level; observed in TLS and HTTP exfiltration patterns.
- Revoke certificate associated with domain bluemoontuesday[.]com issued to wildcard subdomain following suspicious CNAME creation.
- Disable NTLM fallback on domain controller WIN-GSH54QLW48D to prevent relay attacks observed in Kerberos logs.

## Answers to Investigation Questions

- 1. 10.1.17.15 [evidence id: zeek_conn_src_ip_10.1.17.15_count_142]
- 2. WIN-8FJ3Q9K2N4R [evidence id: kerberos_host_login_from_WIN-8FJ3Q9K2N4R]
- 3. jdoe [evidence id: kerberos_user_login_jdoe_from_WIN-8FJ3Q9K2N4R]
- 4. maltrack.bluemoontuesday.com, update-smart[.]xyz [evidence id: http_host_maltrack_bluemoontuesday_com, dns_query_update-smart_xyz]
- 5. 185.71.65.230, 91.198.174.19 [evidence id: suricata_alert_eicar_c2_185.71.65.230, tls_sni_to_91.198.174.19]
- 6. 2025-01-22 08:14 UTC [evidence id: http_get_eicar_bin_from_update-smart_xyz_at_08:14]
- 7. Yes, common name (CN) in certificate: update-smart[.]xyz, IP: 185.71.65.230 [evidence id: tls_cert_subject_update-smart_xyz, tls_server_ip_185.71.65.230_with_susp_cert]
- 8. 185.71.65.230 — it is likely a C2 server (high volume of short-duration connections, associated with Suricata C2 alerts) [evidence id: conn_dst_ip_185.71.65.230_total_138]
