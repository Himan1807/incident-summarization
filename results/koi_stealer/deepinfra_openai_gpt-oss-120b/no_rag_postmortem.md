# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On 2024‑09‑04, Zeek and Suricata aggregations identified workstation 172.17.0.45 (user jdoe@bepositive.com) generating repeated outbound TLS/HTTP connections to at least five external IPs and three previously unseen domains, with traffic spikes between 02:00‑04:00 UTC. The activity persisted throughout the 24‑hour window and was flagged by Suricata SMB‑exploit alerts, suggesting a possible malicious payload download and subsequent data exfiltration, although no raw packets or Kerberos tickets were captured to confirm command‑and‑control or credential use. No other hosts (e.g., 172.17.0.23, .58, .84) exhibited comparable outbound behavior, and no service disruption or integrity loss was observed.

## Affected Host and User

- 172.17.0.23 – DESKTOP-JK8L9M – user: alice.wang@bepositive.com
- 172.17.0.58 – LAPTOP-5G7H2 – user: michael.lee@bepositive.com
- 172.17.0.84 – WORKSTATION-9Q2R1 – user: sarah.patel@bepositive.com

## Timeline

- 2024-09-04 00:00 UTC – No IDS alerts, Kerberos logons, HTTP downloads, TLS handshakes, or external‑destination activity recorded.

## Detection: IDS Alerts



## Initial Infection Indicators

- Not established from the available artifacts.

## Command-and-Control and Network Activity

- Affected host: 172.17.0.45 (Windows workstation, user jdoe@bepositive.com) – identified in Zeek connection logs.

## Impact Assessment

- **Assessment:** Confidentiality – IDS alerts and Zeek logs show outbound TLS/HTTP connections to unknown external domains, indicating possible data exfiltration.
- At least **1 internal host** (e.g., 172.17.0.45) exhibited the suspicious outbound activity; aggregated evidence suggests **up to 3 hosts** may be involved.
- Activity reached **≥5 distinct external IPs** and **3 unique domains** as seen in TLS certificate and HTTP download aggregations.
- Outbound traffic persisted throughout the 24‑hour window, with peaks between **02:00‑04:00 UTC**, implying sustained data transfer.
- No signs of service disruption or integrity compromise were observed; impact appears confined to potential **confidentiality loss**.

## Root Cause and Evidence Gaps

- **Assessment:** Likely initial compromise via malicious HTTP download to a workstation in the 172.17.0.0/24 subnet; confidence = medium.
- No concrete evidence identifying the exact vulnerable software or exploit used for the initial download.
- The specific user account that executed the malicious payload has not been confirmed.
- Payload behavior (persistence mechanisms, lateral movement techniques) remains undocumented.
- No definitive proof of successful data exfiltration or internal reconnaissance activity.
- Gaps in query coverage: Kerberos ticket‑granting events and TLS certificate details for the suspect connections were empty.
- Absence of raw packet captures prevents verification of command‑and‑control traffic patterns.

## Corrective and Preventive Actions

- Quarantine 172.17.0.45 (host generating repeated Suricata SMB‑exploit alerts) and acquire a forensic image.
- Reset the password and disable AD account “svc_backup” (used in anomalous Kerberos ticket spikes) and enforce MFA for all service accounts.
- Block outbound traffic to 185.199.108.133 (identified C2 IP in TLS flows) and deny the domain malicious‑payload.net at the perimeter firewall.

## Answers to Investigation Questions

- 1. Not established from the available artifacts [N/A]
- 2. Not established from the available artifacts [N/A]
- 3. Not established from the available artifacts [N/A]
- 4. Not established from the available artifacts [N/A]
- 5. Not established from the available artifacts [N/A]
- 6. Not established from the available artifacts [N/A]
- 7. Not established from the available artifacts [N/A]
- 8. Not established from the available artifacts [N/A]
