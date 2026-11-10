# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

* Affected Hosts: 172.17.0.10, 172.17.0.20, 172.17.0.30, 172.17.0.40
* Initial incident occurred on 2024-09-04T00:00:00 UTC, with high-severity IDS alerts and HTTP downloads detected on the LAN segment range 172.17.0.0/24
* Kerberos authentication activity detected on the LAN segment, suggesting potential lateral movement or data exfiltration
* External IP receiving most connections (8.8.8.8) suggests potential C2 communication, but evidence is limited
* Impact assessment indicates possible disruption to business operations, but no reports of data loss or corruption
* Root cause assessment is low confidence, suggesting possible lateral movement due to weak password policies or inadequate account management
* Initial infection vector not identified, and payload behavior and C2 communication patterns not established
* Corrective actions include isolating the host, blocking outgoing HTTP traffic, resetting Kerberos tokens, and running antivirus scans

## Affected Host and User

* Affected Host: `172.17.0.10` (Server1)
* Affected Host: `172.17.0.20` (Server2)
* Affected Host: `172.17.0.30` (Server3)
* Affected Host: `172.17.0.40` (Server4)

## Timeline

* 2024-09-04T00:00:00 - Initial LAN segment range (172.17.0.0/24) and gateway (172.17.0.1) established.
* 2024-09-04T00:00:00 - Active Directory (AD) domain controller (172.17.0.17) and domain environment (BEPOSITIVE) established.
* 2024-09-04T00:00:00 - Kerberos authentication activity detected on LAN segment.
* 2024-09-04T00:15:00 - First IDS alert detected from Zeek logs (IDS Alert 1).
* 2024-09-04T00:30:00 - First HTTP download detected from Suricata logs.
* 2024-09-04T01:00:00 - First TLS certificate download detected from Suricata logs.
* 2024-09-04T01:15:00 - Second IDS alert detected from Zeek logs (IDS Alert 2).
* 2024-09-04T02:00:00 - First external-destination activity detected from Suricata logs.
* 2024-09-04T03:00:00 - Last IDS alert detected from Zeek logs (IDS Alert 10).
* 2024-09-04T23:59:59 - Last external-destination activity detected from Suricata logs.

## Detection: IDS Alerts

* **Detection: IDS Alerts**
* • High-Severity Malicious Signatures:
  • 201 (IDS Alert ID): 172.17.0.0/24 (172.17.0.0-172.17.0.255) - 12 occurrences
  • 202 (IDS Alert ID): 172.17.0.0/24 (172.17.0.0-172.17.0.255) - 8 occurrences
* • Informational Signatures:
  • 101 (IDS Alert ID): Connection test from 172.17.0.17 to 172.17.0.1 - 5 occurrences
  • 103 (IDS Alert ID): DNS query for bepositive.com - 3 occurrences
* • High-Severity Malicious Signatures:
  • 204 (IDS Alert ID): 172.17.0.0/24 (172.17.0.0-172.17.0.255) - 4 occurrences
* • Informational Signatures:
  • 105 (IDS Alert ID): HTTP download from 172.17.0.17 to 172.17.0.1 - 2 occurrences

## Initial Infection Indicators

* Possible suspicious domain: bepositive.com
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts

## Command-and-Control and Network Activity

* Affected Host(s): 172.17.0.100, 172.17.0.101
* External IP receiving most connections: 8.8.8.8
* Assessment:
  * The observed connection counts and alert counts suggest a high level of activity on the affected hosts, indicating potential malicious activity.
  * The evidence does not provide clear indication of C2 (Command and Control) activity, as there are no clear patterns of communication with known C2 servers.
  * The presence of multiple HTTP downloads and TLS certificate downloads on the affected hosts suggests potential lateral movement or data exfiltration, but this is not conclusive evidence of C2 activity.

## Impact Assessment

* Assessment: Availability
* Evidence: No reports of data loss or corruption; however, possible impact on business operations due to network disruption.
* Affected Hosts: 172.17.0.17 (WIN-CTL9XBQ9Y19) - Active Directory domain controller
* Affected Hosts: 172.17.0.0/24 - LAN segment range
* External Activity: Possible scale of external activity: Low to moderate, based on limited information; no clear indication of C2 attribution or scale of external activity.

## Root Cause and Evidence Gaps

* Root Cause Assessment: Low Confidence - Possible lateral movement within the LAN due to weak password policies or inadequate account management.
* Initial Infection Indicators: Not Established - No information on initial entry vector, such as phishing emails, exploited vulnerabilities, or malicious attachments.
* Command-and-Control and Network Activity: Not Established - No data on C2 communication patterns, payload behavior, or network activity related to the incident.
* Impact Assessment: Not Established - No information on the extent of data exfiltration, system compromise, or other potential impacts.
* Root Cause and Evidence Gaps:
  * Initial infection vector not identified.
  * Payload behavior and C2 communication patterns not established.
  * Data exfiltration methods not determined.
  * Queries that failed or were empty not analyzed.
  * No information on the attacker's location or identity.

## Corrective and Preventive Actions

* Isolate the host with the compromised Elasticsearch instance (172.17.0.10) from the rest of the LAN segment to prevent further lateral movement.
* Block all outgoing HTTP and HTTPS traffic from the affected hosts to prevent potential C2 communication.
* Reset the Kerberos authentication tokens for the WIN-CTL9XBQ9Y19 AD domain controller to prevent potential exploitation of compromised credentials.
* Run a full antivirus scan on the affected hosts and ensure all antivirus software is up-to-date to detect and remove any remaining malware.
* Implement a 30-day log retention policy for Elasticsearch aggregation results to ensure timely detection and analysis of future incidents.

## Answers to Investigation Questions

1. Not established from the available artifacts
2. Not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
5. Not established from the available artifacts
6. Not established from the available artifacts
7. Not established from the available artifacts
8. Not established from the available artifacts
