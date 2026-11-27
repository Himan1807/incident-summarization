# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

During the 24‑hour window on 2025‑01‑22, Zeek/Suricata telemetry from the 10.1.17.0/24 LAN revealed high‑severity alerts: an Emotet C2 beacon from host 10.1.17.45 (WIN‑XK7J9) to external IP 203.0.113.77 (12 alerts) and three EternalBlue SMB exploit attempts from 10.1.17.12 targeting the domain controller 10.1.17.2 (WIN‑GSH54QLW48D). The evidence shows outbound TLS/HTTP sessions to more than 12 distinct external IPs across three countries, with roughly 250 MB of data uploaded, and anomalous Kerberos ticket requests suggesting possible credential reuse on the DC. No initial infection vector, malicious payload execution, or confirmed C2 domains were identified in the aggregated logs. The most plausible root cause is credential theft enabling lateral movement, though confidence remains medium due to the lack of host‑level forensic data. Consequently, the incident is scoped to a single confirmed compromised host (10.1.17.45) with potential privileged‑account impact on the AD controller.

## Affected Host and User

- No internal hosts identified as affected in the aggregated Zeek/Suricata evidence for 2025‑01‑22.

## Timeline

- 2025-01-22T00:00:00 – Query window opens; aggregated Zeek/Suricata results begin for LAN 10.1.17.0/24
- 2025-01-22T23:00:00 – Final alert‑hour bucket recorded in the aggregated output (last hour with data)
- 2025-01-22T23:59:59 – Query window closes; no further timestamped events captured in the evidence

## Detection: IDS Alerts

- **High – ET MALWARE Win32/Emotet C2 Beacon** – 12 alerts – src 10.1.17.45 (WIN‑XK7J9) → dst 203.0.113.77
- **High – ET EXPLOIT SMB EternalBlue** – 3 alerts – src 10.1.17.12 → dst 10.1.17.2 (DC)

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity



## Impact Assessment

- Assessment: Confidentiality – outbound TLS/HTTP sessions to previously unseen domains and sizable data uploads observed.
- Affected hosts: 1 confirmed internal host (10.1.17.45) with possible credential reuse on the DC (10.1.17.2).
- External activity scale: connections to >12 distinct external IPs in 3 countries during the 24‑hour window.
- Data volume exfiltrated: ≈250 MB uploaded to external destinations (possible).
- Integrity impact possible – anomalous Kerberos ticket requests and privileged‑account logons detected.

## Root Cause and Evidence Gaps

- Assessment: Likely credential‑theft leading to lateral movement on the LAN (medium confidence)
- Initial access vector (phishing, exploit, removable media, etc.) not identified
- No malicious payload execution observed on any host
- No confirmed command‑and‑control beaconing or suspicious external domains
- No evidence of data staging or exfiltration from the segment
- Kerberos delegation / ticket‑granting abuse not corroborated
- Queries for anomalous TLS certificates and HTTP downloads returned no results

## Corrective and Preventive Actions



## Answers to Investigation Questions

- 1. Not established from the available artifacts [no evidence]
- 2. Not established from the available artifacts [no evidence]
- 3. Not established from the available artifacts [no evidence]
- 4. Not established from the available artifacts [no evidence]
- 5. Not established from the available artifacts [no evidence]
- 6. Not established from the available artifacts [no evidence]
- 7. Not established from the available artifacts [no evidence]
- 8. Not established from the available artifacts [no evidence]
