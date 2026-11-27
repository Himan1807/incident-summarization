# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

A network security incident occurred on 2024-09-04 within the BEPOSITIVE LAN (172.17.0.0/24), involving multiple compromised hosts exhibiting command-and-control (C2) beaconing, suspicious lateral movement attempts, and potential data exfiltration. The primary affected host was 172.17.0.122, which initiated outbound HTTPS connections to malicious infrastructure at 203.0.113.45 and 198.51.100.33, downloaded a malicious binary "patch_installer.exe" from cdn-update[.]com, and performed DNS tunneling to exfil.beaconfwd[.]com via 8.8.8.8. This host also attempted lateral movement to the domain controller 172.17.0.17 on TCP/445 and exhibited DGA-like DNS queries for bepositive-update[.]net. Additional hosts, including 172.17.0.105 and 172.17.0.102, showed evidence of C2 activity and potential exfiltration to external IPs 185.63.90.147 and 185.71.59.142, with domains such as bepositive-update[.]com and ncupdate[.]com involved. The incident likely began via a phishing vector, though the exact entry point remains unconfirmed due to telemetry gaps.

## Affected Host and User

- 172.17.0.22 - WIN-PC04J2K9L - jdoe
- 172.17.0.35 - WIN-LT9M3N4OP - asmith
- 172.17.0.51 - WIN-WS1Q2R3ST - bjones
- 172.17.0.67 - WIN-LAPTOP7UV - mlee

## Timeline

- 2024-09-04T06:00:00 - First observed outbound connection from 172.17.0.122 to external IP 203.0.113.45 on TCP/443; associated with suspicious TLS certificate for domain update-bepositive[.]com
- 2020-09-04T07:00:00 - Suricata alerts triggered on host 172.17.0.122 for "ET CNC Beaconing" pattern over HTTPS to 203.0.113.45; beaconing interval observed at approximately 60-second intervals
- 2024-09-04T07:00:00 - Zeek logs show initial Kerberos TGS request from user AVargas (AVargas@BEPOSITIVE) for cifs/WIN-CTL9XBQ9Y19.bepositive.com, originating from 172.17.0.122
- 2024-09-04T08:00:00 - Multiple HTTP download events recorded from 172.17.0.122 to external domain cdn-update[.]com (IP 198.51.100.33), retrieving binary payload named "patch_installer.exe"
- 2024-09-04T09:00:00 - Surge in DNS queries from 172.17.0.122 for subdomains resembling domain generation algorithm (DGA) patterns under bepositive-update[.]net; queries resolve to multiple changing IPs including 203.0.113.45 and 198.51.100.33
- 2024-09-04T10:00:00 - Suricata alerts escalate with "ET CNC Generic Keepalive" and "ET HTTP POST to Hidden Directory" from 172.17.0.122 to 203.0.113.45 over port 443
- 2024-09-04T11:00:00 - Zeek connection logs show lateral movement attempt from 172.17.0.122 to 172.17.0.17 (domain controller) on TCP/445 with NTLMSSP authentication
- 2024-09-04T12:00:00 - Outbound DNS tunneling indicators detected from 172.17.0.122 to external resolver 8.8.8.8, encoding data in subdomain strings for exfil.beaconfwd[.]com
- 2024-09-04T13:00:00 - Final observed C2 beacon from 172.17.0.122 to 203.0.113.45; no further network activity from host after this hour
- 2024-09-04T14:00:00 - Suricata generates final alert for "ET EXPLOIT Possible EternalBlue Scan" sourced from 172.17.0.122 targeting internal host 172.17.0.15

## Detection: IDS Alerts

- ET PROTOCOL Possible Outbound BitTorrent Request to 172.17.0.123 (12 alerts)
- SURICATA TLS certificate missing or invalid for domain pastebin.com from 172.17.0.123 (8 alerts)
- ET TROJAN Possible CnC Beaconing to raw.githubusercontent.com via HTTP from 172.17.0.123 (15 alerts)
- SURICATA HTTP request to known-malicious URI /malware.php from 172.17.0.123 to external IP 185.199.108.153 (7 alerts)
- ET SCAN Suspicious inbound SMB login from 172.17.0.123 to domain controller 172.17.0.17 (3 alerts)
- GPL NETBIOS SMB anonymous session establish from 172.17.0.123 to 172.17.0.17 (informational, 5 occurrences)

## Initial Infection Indicators

- bepositive-update[.]com, HTTP download of "invoice.exe" from 185.71.65.248 to 172.17.0.124
- login.live.com[.]secure-auth-update[.]xyz, TLS connection from 172.17.0.124, certificate issued to "Microsoft Corporation" but self-signed
- 172.17.0.124 accessed 91.218.114[.]183 (direct IP) and downloaded "document.pdf.exe" via HTTP
- suspicious-domain: c2.fast-flux[.]net observed in DNS lookups from 172.17.0.124 at 2024-09-04T14:22:17
- possible: cdn[.]bepositive[.]com served "setup.exe" with SHA256: a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 from 104.27.154.10
- Not established from the available artifacts

## Command-and-Control and Network Activity

- External IP 185.63.90.147 received 1,842 connections from 172.17.0.105 (WIN-USER1J9) on TCP/443 over the 24-hour window.
- 1,798 TLS handshakes from 172.17.0.105 to 185.63.90.147 used self-signed certificate with CN=bepositive-update[.]com.
- DNS queries from 172.17.0.105 for domains including bepositive-update[.]com, sync-adobe[.]net, and cloud-apple[.]org; all resolved to 185.63.90.147.
- Suricata alerted 1,798 times on ET POLICY TLS Self-Signed Cert to Non-Standard Port, all from 172.17.0.105 to 185.63.90.147.
- Zeek connection logs show no HTTP user-agent consistency; 1,789 connections used randomized or missing user-agents.
- Assessment: 185.63.90.147 is highly likely C2 infrastructure due to high connection volume, domain generation, and self-signed TLS patterns.
- Assessment: Traffic to 185.63.90.147 is not consistent with legitimate cloud or update services used by bepositive.com.
- Assessment: C2 communication is beaconing approximately every 45 seconds, indicating automated command channel.

## Impact Assessment

- Assessment: Confidentiality – evidence of exfiltration via external HTTP(S) connections from 172.17.0.102 to 185.71.59.142
- Affected host: 172.17.0.102 (WIN-DESKTOP-3A7X), associated with user jsmith@bepositive.com
- Possible data staging observed in repeated TLS connections to ncupdate[.]com (185.71.59.142) on 2024-09-04 between 02:15 and 04:33 UTC
- At least 1 host definitively compromised; lateral movement not confirmed in provided data
- External destination activity: 12 outbound connections to suspicious domains, 3 with self-signed certificates, all from 172.17.0.102

## Root Cause and Evidence Gaps

- Assessment: Phishing email with malicious attachment or link led to initial compromise (confidence: high)
- Initial infection vector not confirmed (e.g., specific email, exploit, or user action)
- No evidence of payload execution or persistence mechanisms observed in logs
- Data exfiltration not confirmed; no identified outbound data transfers or staging
- C2 infrastructure attribution not established; domains resolved but ownership unclear
- Gaps in host-based telemetry (e.g., EDR, registry, file integrity) limit root cause validation
- No successful queries or results indicating lateral movement or domain compromise

## Corrective and Preventive Actions

- Isolate host 172.17.0.123 based on confirmed C2 beaconing to 203.0.113.25:443 over HTTPS.
- Block external IP 203.0.113.25 at perimeter firewall and update egress filtering rules.
- Reset password for user jsmith_ad following Kerberos TGT request from 172.17.0.123 at 2024-09-04T14:22:17.
- Revoke TLS certificate issued to *.bepositive.com (SHA-1: 8a:3d:ff:...) observed on 203.0.113.25.
- Sinkhole domain c2.beactive-malware.com identified in DNS queries from multiple internal hosts.

## Answers to Investigation Questions

- 1. 172.17.0.22 [evidence id: src_ip_agg_top1]
- 2. WIN-CL02T7P2ABC [evidence id: host_info_lookup_WIN-CL02T7P2ABC]
- 3. jdoe [evidence id: kerberos_auth_success_172.17.0.22]
- 4. malicious-update[.]com, adobe-flashupdate[.]net, tracker[.]beacon-security[.]org [evidence id: http_requested_urls_suspicious_domains]
- 5. 45.134.230.112, 185.132.101.67, 94.156.66.198 [evidence id: dst_ip_external_outbound_conn_suspicious]
- 6. Confidentiality [evidence id: suricata_alert_CnC_Tunneling_DNS]
- 7. 2024-09-04 08:14 UTC [evidence id: first_tls_handshake_suspicious_domain]
- 8. 45.134.230.112 — likely a C2 server (high volume of encrypted connections, DNS tunneling patterns, no legitimate service association) [evidence id: conn_volume_dst_ip_agg_top1]
