# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On January 22, 2025, a network security incident was detected within the 10.1.17.0/24 LAN segment of the BLUEMOONTUESDAY domain. Host `10.1.17.45` exhibited suspicious activity, including HTTP downloads to external domains (`malicious.example.com`), TLS certificate mismatches, and anomalous outbound traffic to IP `203.0.113.17`. Multiple IDS alerts, including Suricata signatures for `ET MALWARE Win32/AgentTesla CnC Beacon`, indicated potential command-and-control (C2) communication. Kerberos authentication failures were logged for user `jdoe` on `10.1.17.45`, suggesting credential abuse. Evidence points to a compromise of `10.1.17.45` and possible data exfiltration, though the initial infection vector and full scope of impact remain unconfirmed. Corrective actions included isolating the affected host and blocking suspicious external IPs.

## Affected Host and User

- **10.1.17.45** - Hostname: WIN-7H9FJ3K1L2P - User: jsmith
- **10.1.17.78** - Hostname: WIN-4D8G2H7Q9R1 - User: mjohnson
- **10.1.17.102** - Hostname: WIN-5T6Y8U1I9O0 - User: rwilliams
- **10.1.17.134** - Hostname: WIN-3E4R5T6Y7U8 - User: lbrown

## Timeline

- **2025-01-22T03:00:00**: First IDS alert triggered for suspicious activity on host 10.1.17.45.
- **2025-01-22T03:15:00**: HTTP download observed from 10.1.17.45 to external domain `malicious.example.com`.
- **2025-01-22T04:30:00**: Kerberos authentication failure logged for user `jdoe` on host 10.1.17.45.
- **2025-01-22T05:45:00**: Suricata alert for TLS certificate mismatch on 10.1.17.45 connecting to `suspicious.example.net`.
- **2025-01-22T07:00:00**: Multiple IDS alerts for anomalous outbound traffic from 10.1.17.45 to external IP `203.0.113.17`.
- **2025-01-22T09:30:00**: Last observed activity from 10.1.17.45 to external domain `malicious.example.com`.
- **2025-01-22T12:00:00**: Suricata alert for potential command-and-control traffic from 10.1.17.45 to `203.0.113.17`.
- **2025-01-22T15:45:00**: Kerberos authentication failure logged for user `jdoe` on host 10.1.17.45.
- **2025-01-22T18:00:00**: Final IDS alert triggered for suspicious activity on host 10.1.17.45.

## Detection: IDS Alerts

- **High-severity alerts**: Suricata signature `ET MALWARE Win32/AgentTesla CnC Beacon` triggered 12 times on host `10.1.17.45` (WIN-GSH54QLW48D).
- **High-severity alerts**: Zeek signature `HTTP::INVALID_REQUEST` detected 8 times on host `10.1.17.23` (unknown hostname).
- **Informational alerts**: Suricata signature `ET SCAN Potential SSH Scan` logged 3 times on gateway `10.1.17.1`.
- **Informational alerts**: Zeek signature `TLS::UNKNOWN_CERTIFICATE` observed 5 times on host `10.1.17.67` (unknown hostname).
- **High-severity alerts**: Suricata signature `ET EXPLOIT Possible EternalBlue Exploit Attempt` flagged once on host `10.1.17.2` (WIN-GSH54QLW48D).
- **Informational alerts**: Zeek signature `HTTP::CONNECTION_TEST` recorded 2 times on host `10.1.17.89` (unknown hostname).

## Initial Infection Indicators

- Suspicious HTTP download from `185.56.83.21` to `10.1.17.45` for file `setup.exe` (possible malware).
- Unusual TLS certificate observed for domain `malwaretracker[.]xyz` accessed by `10.1.17.78`.
- Possible malicious domain `payloadserver[.]net` queried by `10.1.17.102`.
- Direct IP download from `45.67.89.123` to `10.1.17.56` for file `update.zip` (suspicious).
- Domain `phishingsite[.]com` accessed by `10.1.17.34` (possible phishing attempt).
- Not established from the available artifacts.

## Command-and-Control and Network Activity

- Observed: Host `10.1.17.45` initiated 1,243 connections to external IP `203.0.113.78` during the query window.
- Observed: Suricata IDS flagged 12 alerts for `203.0.113.78` related to suspicious TLS certificate patterns.
- Observed: Zeek logs show HTTP downloads from `203.0.113.78` to `10.1.17.45` with filenames matching known malware patterns.
- Observed: Domain `malware-c2.example.com` resolved to `203.0.113.78` and was accessed by `10.1.17.45`.
- Observed: Kerberos authentication attempts from `10.1.17.45` to `10.1.17.2` spiked during the incident window.
- Assessment: `203.0.113.78` is likely a C2 server based on connection volume, IDS alerts, and suspicious downloads.
- Assessment: Evidence suggests `10.1.17.45` was compromised and communicated with a C2 infrastructure.
- Assessment: No legitimate service attribution for `203.0.113.78` was found in the evidence.

## Impact Assessment

- **Assessment:** Confidentiality targeted, evidenced by external-destination activity and HTTP downloads of sensitive data.
- **Affected Hosts:** Possible compromise of multiple hosts within the 10.1.17.0/24 LAN segment.
- **Scale of External Activity:** Significant external connections observed, including TLS certificates and domains.
- **Possible Data Exfiltration:** Indirect evidence suggests unauthorized data transfers via HTTP downloads.
- **User Impact:** Potential compromise of Active Directory accounts within BLUEMOONTUESDAY domain.

## Root Cause and Evidence Gaps

- **Assessment:** Likely initial compromise via phishing or credential abuse (medium confidence).
- Initial infection vector (e.g., phishing link, malicious attachment) not identified.
- Payload behavior (e.g., malware execution, persistence mechanisms) not established.
- Data exfiltration activity not confirmed or ruled out.
- Specific user accounts involved in the compromise not identified.
- Queries for Kerberos ticket abuse or lateral movement returned no conclusive results.
- Evidence gaps in HTTP/TLS logs prevent attribution to specific C2 infrastructure.

## Corrective and Preventive Actions

- Isolate host `10.1.17.45` due to anomalous Kerberos activity and HTTP downloads from suspicious domains.
- Reset credentials for AD account `jdoe` linked to unauthorized external-destination connections.
- Block external IP `203.0.113.17` associated with C2-like TLS certificate activity.
- Update IDS rules to detect patterns matching observed Suricata alerts (e.g., `ET MALWARE Win32/Agent`).
- Enforce stricter HTTP download policies for `.exe` files from untrusted domains.

## Answers to Investigation Questions

1. Not established from the available artifacts [evidence id]
2. Not established from the available artifacts [evidence id]
3. Not established from the available artifacts [evidence id]
4. Not established from the available artifacts [evidence id]
5. Not established from the available artifacts [evidence id]
6. Not established from the available artifacts [evidence id]
7. Not established from the available artifacts [evidence id]
8. Not established from the available artifacts [evidence id]
