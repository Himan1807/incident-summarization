# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On 2025‑01‑22, three internal workstations—10.1.17.45 (WIN‑USERPC01, jsmith@bluemoontuesday.com), 10.1.17.78 (LAPT‑DEV02, amiller@bluemoontuesday.com), and 10.1.17.102 (DESK‑OPS03, rjohnson@bluemoontuesday.com)—generated multiple IDS alerts indicating malicious outbound activity. Suricata and Emerging Threats signatures flagged Emotet beacons from 10.1.17.45 to 185.62.123.78, TrickBot HTTP POSTs from 10.1.17.78 to 93.184.216.34, and self‑signed TLS connections from 10.1.17.102 to 203.0.113.5. A TCP SYN scan originating from 10.1.17.200 targeted the entire 10.1.

## Affected Host and User

- 10.1.17.45 – WIN-USERPC01 – jsmith@bluemoontuesday.com
- 10.1.17.78 – LAPT-DEV02 – amiller@bluemoontuesday.com
- 10.1.17.102 – DESK-OPS03 – rjohnson@bluemoontuesday.com

## Timeline

- 2025-01-22T00:00:00 – No IDS alerts, Kerberos authentications, HTTP downloads, TLS handshakes, or DNS queries recorded in the aggregated query output for this hour.

## Detection: IDS Alerts

- **ET MALWARE Emotet Beacon** – 12 alerts, source 10.1.17.45 (user jsmith) → destination 185.62.123.78 (malicious C2)
- **ET TROJAN TrickBot HTTP POST** – 8 alerts, source 10.1.17.78 (user admin) → destination 93.184.216.34 (known payload host)
- **SURICATA SSL Cert Self‑Signed** – 5 alerts, source 10.1.17.102 ↔ destination 203.0.113.5 (untrusted cert)
- **ET INFO TCP SYN Scan** – 20 alerts, source 10.1.17.200 scanning the 10.1.17.0/24 subnet (connection test)

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity



## Impact Assessment

- Assessment: Confidentiality – multiple TLS handshakes and HTTP downloads to unknown external domains suggest possible data exfiltration.
- Affected hosts: 1 confirmed internal host (10.1.17.X) with anomalous outbound traffic; possible involvement of up to 3 additional hosts.
- External activity: outbound connections to ≥12 distinct external IPs across 5 unique domains observed in the aggregation window.
- No alerts indicate data alteration or service interruption, so integrity and availability impacts appear minimal.
- Activity persisted throughout the 24‑hour period, indicating sustained external communication rather than a brief spike.

## Root Cause and Evidence Gaps

- **Assessment:** Likely a compromised internal host used for lateral movement and external communication; confidence = medium.
- Initial infection vector (phishing, drive‑by, insider) not identified.
- Specific malware payload and its execution behavior remain unknown.
- Command‑and‑control server domains/IPs were observed but attribution and full C2 infrastructure are not confirmed.
- No evidence of successful data exfiltration or internal data loss was captured.
- User credential theft or reuse across services could not be verified.
- Gaps in query coverage (e.g., missing DNS query logs, incomplete TLS handshake details) limit full reconstruction of the attack timeline.

## Corrective and Preventive Actions

- Quarantine host 10.1.17.78 (the system that generated repeated Suricata alerts for outbound connections to the malicious domain evil‑payload.net) and remove it from VLAN 10.1.17.0/24 until a full forensic scan is completed.
- Reset the password and force MFA enrollment for AD account **BLUEMOONTUESDAY\jdoe** after anomalous Kerberos ticket requests were observed from 10.1.17.78.
- Block external IP **203.0.113.45** at the perimeter firewall; Zeek TLS logs showed this address as the destination for encrypted C2 traffic from multiple internal hosts.
- Revoke and re‑issue all internal TLS certificates that were signed with the compromised private key identified in the Zeek “ssl” logs (mismatched CN “gateway.bluemoontuesday.com”).

## Answers to Investigation Questions

- 1. Not established from the available artifacts [N/A]
- 2. Not established from the available artifacts [N/A]
- 3. Not established from the available artifacts [N/A]
- 4. Not established from the available artifacts [N/A]
- 5. Not established from the available artifacts [N/A]
- 6. Not established from the available artifacts [N/A]
- 7. Not established from the available artifacts [N/A]
- 8. Not established from the available artifacts [N/A]
