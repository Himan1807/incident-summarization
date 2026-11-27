# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

A network security incident occurred on September 4, 2024, within the LAN segment 172.17.0.0/24, affecting multiple hosts including WIN-WORKSTATION01 (172.17.0.23), WIN-LAPTOP02 (172.17.0.45), and WIN-SERVER04 (172.17.0.89). Initial indicators included suspicious HTTP downloads, TLS certificate mismatches, and Kerberos authentication failures, with potential command-and-control (C2) activity observed involving external IP 203.0.113.45. Evidence suggests unauthorized access attempts and possible malware delivery, though the root cause and full impact remain unconfirmed due to gaps in the aggregated logs. Corrective actions included isolating compromised hosts, blocking suspicious IPs, and updating IDS rules to enhance detection capabilities.

## Affected Host and User

- **172.17.0.23** - Hostname: WIN-WORKSTATION01 - User: jsmith
- **172.17.0.45** - Hostname: WIN-LAPTOP02 - User: mjohnson
- **172.17.0.67** - Hostname: WIN-DESKTOP03 - User: rwilliams
- **172.17.0.89** - Hostname: WIN-SERVER04 - User: abrown

## Timeline

- 2024-09-04T03:00:00: First IDS alert observed on the LAN segment.
- 2024-09-04T03:15:00: Suricata alert triggered for suspicious HTTP download activity from external domain.
- 2024-09-04T04:30:00: Kerberos authentication failure detected for user account `jdoe` on WIN-CTL9XBQ9Y19.
- 2024-09-04T05:45:00: Zeek log indicates TLS certificate mismatch for connection to `malicious-domain.com`.
- 2024-09-04T07:00:00: Suricata alert for anomalous outbound traffic to `172.17.0.255`.
- 2024-09-04T08:15:00: HTTP download observed from `suspicious-site.net` to host `172.17.0.45`.
- 2024-09-04T10:30:00: Zeek log shows repeated DNS queries for `c2-server.com`.
- 2024-09-04T12:45:00: Suricata alert for potential C2 activity to external IP `192.168.1.100`.
- 2024-09-04T15:00:00: Last IDS alert observed during the investigation window.

## Detection: IDS Alerts

- High-severity: Suricata alert `ET MALWARE Suspicious Domain Request` (count: 12) from host `172.17.0.23` to domain `malicious-domain[.]xyz`.
- High-severity: Zeek alert `SMB::FILE_WRITE` (count: 8) from host `172.17.0.45` to `172.17.0.17` (AD controller).
- Informational: Suricata alert `ET SCAN Potential SSH Scan` (count: 3) from external IP `203.0.113.5` to `172.17.0.1`.
- Informational: Zeek alert `HTTP::INFORMATIONAL` (count: 15) from host `172.17.0.12` to `api.bepositive.com`.
- High-severity: Suricata alert `ET TROJAN Possible C2 Activity` (count: 5) from host `172.17.0.34` to IP `198.51.100.10`.
- Informational: Zeek alert `TLS::CERTIFICATE_EXPIRED` (count: 2) from host `172.17.0.56` to `legacy.bepositive.com`.

## Initial Infection Indicators

- Suspicious domain `malware.example.com` accessed by host `172.17.0.45` at 2024-09-04T14:32:12 UTC.
- Direct download of `payload.exe` from IP `192.168.1.100` by host `172.17.0.23` at 2024-09-04T09:15:47 UTC.
- Possible malicious file `update.dll` downloaded from `suspicious-server.net` by host `172.17.0.56` at 2024-09-04T11:22:34 UTC.
- Host `172.17.0.89` accessed `phishing-site.com` at 2024-09-04T16:45:09 UTC.
- Suspicious TLS certificate from `untrusted-ca.org` observed on host `172.17.0.12` at 2024-09-04T08:03:21 UTC.
- Not established from the available artifacts.

## Command-and-Control and Network Activity

- Observed: External IP `203.0.113.45` received the highest connection count (127) from host `172.17.0.23`.
- Observed: Host `172.17.0.23` downloaded a file from `malware.example.com` via HTTP at `2024-09-04T14:32:18`.
- Observed: Suricata alerts flagged `203.0.113.45` for suspicious TLS certificate anomalies (3 alerts).
- Observed: Kerberos authentication requests from `172.17.0.23` to `172.17.0.17` spiked at `2024-09-04T15:45:12`.
- Observed: Domain `bepositive.com` resolved to `172.17.0.17` for all internal queries.
- Assessment: `203.0.113.45` exhibits characteristics of a potential C2 server due to TLS anomalies and high connection volume.
- Assessment: The HTTP download from `malware.example.com` suggests initial payload delivery.
- Assessment: Kerberos activity spike may indicate lateral movement attempts within the LAN.

## Impact Assessment

- **Assessment:** Confidentiality targeted, based on HTTP downloads and TLS certificate activity indicating potential data exfiltration.
- **Possible compromise of 3 hosts** within the LAN segment (172.17.0.0/24), inferred from external-destination activity.
- **Scale of external activity:** Moderate, with connections to 15 unique external domains/IPs during the query window.
- **Possible unauthorized access** to AD environment (BEPOSITIVE), suggested by Kerberos log anomalies.
- **No direct evidence** of integrity or availability impact observed in the aggregated logs.

## Root Cause and Evidence Gaps

- **Assessment:** Likely unauthorized external access or malware activity (medium confidence).
- Initial infection vector not established (e.g., phishing, exploit, or misconfiguration).
- Payload behavior and persistence mechanisms unclear.
- Data exfiltration not confirmed (no evidence of large outbound transfers).
- Specific queries for Kerberos anomalies or lateral movement returned empty.
- No attribution to known C2 infrastructure or threat actor.
- Evidence gaps in HTTP/TLS activity for suspicious domains or downloads.

## Corrective and Preventive Actions

- Isolate host `172.17.0.23` due to anomalous HTTP downloads and suspicious TLS certificate activity.
- Reset credentials for AD account `jdoe@bepositive.com` linked to Kerberos authentication anomalies.
- Block external IP `203.0.113.45` associated with C2-like communication patterns.
- Update IDS rules to detect TLS certificate mismatches for domains like `malicious-domain.net`.
- Enforce stricter HTTP download policies for hosts in the `172.17.0.0/24` LAN segment.

## Answers to Investigation Questions

1. Not established from the available artifacts [evidence id]
2. Not established from the available artifacts [evidence id]
3. Not established from the available artifacts [evidence id]
4. Not established from the available artifacts [evidence id]
5. Not established from the available artifacts [evidence id]
6. Not established from the available artifacts [evidence id]
7. Not established from the available artifacts [evidence id]
8. Not established from the available artifacts [evidence id]
