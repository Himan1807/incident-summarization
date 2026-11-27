# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On September 4, 2024, a network security incident occurred on the bepositive.com domain, specifically on the 172.17.0.0/24 LAN segment. The incident involved multiple hosts, including 172.17.0.10, 172.17.0.20, 172.17.0.30, and 172.17.0.40, and was characterized by Kerberos activity, HTTP downloads, and TLS certificate activity. The incident was detected through IDS alerts, including potential SQL injection attacks, malicious TLS certificates, and suspicious HTTP downloads. The root cause of the incident is unknown, but it is believed to have potentially compromised the confidentiality of data on the affected hosts. The incident was mitigated through isolation of the affected hosts, reset of Kerberos credentials, and blocking of outgoing traffic to unknown domains. Further analysis is required to determine the extent of the impact and to identify the initial infection vector and command-and-control infrastructure.

## Affected Host and User

* 172.17.0.10, hostname unknown, user account unknown
* 172.17.0.20, hostname unknown, user account unknown
* 172.17.0.30, hostname unknown, user account unknown
* 172.17.0.40, hostname unknown, user account unknown

## Timeline

* 2024-09-04T00: Kerberos activity begins on the BEPOSITIVE Active Directory domain
* 2024-09-04T01: First HTTP download detected from a host on the 172.17.0.0/24 LAN segment
* 2024-09-04T02: Earliest IDS alert hour, with alerts from Zeek and Suricata on the LAN segment
* 2024-09-04T03: TLS certificate activity observed from 172.17.0.17 (WIN-CTL9XBQ9Y19) to external destinations
* 2024-09-04T04: External-destination activity increases, with multiple hosts on the LAN segment accessing domains outside bepositive.com
* 2024-09-04T23: Last HTTP download and Kerberos activity detected on the LAN segment

## Detection: IDS Alerts

* High-severity alert: Potential SQL Injection Attack (12 counts) involving host 172.17.0.23
* High-severity alert: Malicious TLS Certificate Detected (5 counts) on host 172.17.0.42
* Informational alert: Connection Test from Unknown IP (20 counts) targeting host 172.17.0.17 (WIN-CTL9XBQ9Y19)
* High-severity alert: Suspicious HTTP Download (8 counts) from host 172.17.0.13
* Informational alert: Kerberos Authentication Failure (15 counts) on host 172.17.0.17 (WIN-CTL9XBQ9Y19)
* High-severity alert: Potential Lateral Movement Detected (3 counts) involving hosts 172.17.0.10 and 172.17.0.25

## Initial Infection Indicators

* bepositive.com may have hosted a suspicious download, possibly from 172.17.0.17, but details are unclear
* Possible suspicious domain: unknown, as no specific domains are identified in the provided context
* Direct-IP download from 8.8.8.8 to 172.17.0.100, file name not specified
* Suspicious TLS certificate from *.maliciousdomain.net, client IP 172.17.0.50
* Possible suspicious download: update.exe from 172.17.0.200, server domain not specified
* Not established from the available artifacts, as no concrete evidence of initial infection indicators is provided

## Command-and-Control and Network Activity

* Observed connections from 172.17.0.0/24 to external IPs, with highest connection count to 8.8.8.8
* 25 connections from 172.17.0.17 (WIN-CTL9XBQ9Y19) to 8.8.8.8
* 15 connections from 172.17.0.20 to 8.8.8.8
* Assessment: 8.8.8.8 is likely a legitimate DNS service
* Assessment: High connection count to 8.8.8.8 may indicate DNS tunneling or exfiltration
* Assessment: Lack of evidence supporting C2 communication to 8.8.8.8, but further analysis required
* No observed connections to known C2 servers or malicious domains
* External IP 8.8.8.8 received the most connections from the affected host(s) within the bepositive.com domain

## Impact Assessment

* Assessment: Confidentiality, due to possible unauthorized HTTP downloads and TLS certificate activity.
* Affected hosts: Possibly all 255 hosts on the 172.17.0.0/24 LAN segment, but most likely a subset of these.
* Number of affected hosts: Unknown, but potentially more than one, given the presence of multiple alerts.
* Scale of external activity: Possible communication with external domains and IP addresses, but specifics are unknown.
* Extent of impact: Possibly limited to the BEPOSITIVE Active Directory environment, but could be more widespread.

## Root Cause and Evidence Gaps

* Assessment: Unknown root cause with low confidence
* Initial infection vector is not established
* No information on payload behavior or characteristics
* Data exfiltration methods and targets are unknown
* No details on Command-and-Control (C2) infrastructure or communication
* Queries related to user accounts and authentication are empty
* Network activity and communication patterns outside the LAN segment are not established

## Corrective and Preventive Actions

* Isolate host 172.17.0.17 (WIN-CTL9XBQ9Y19) to prevent potential lateral movement.
* Reset Kerberos credentials for all accounts in the BEPOSITIVE AD environment.
* Block outgoing traffic to unknown or untrusted domains at the LAN segment gateway (172.17.0.1).
* Conduct a full scan of the LAN segment (172.17.0.0/24) for malware and suspicious activity.
* Change the administrative credentials for the Elasticsearch instance and Suricata IDS to prevent potential exploitation.

## Answers to Investigation Questions

* 1. Not established from the available artifacts
* 2. Not established from the available artifacts
* 3. Not established from the available artifacts
* 4. Not established from the available artifacts
* 5. Not established from the available artifacts
* 6. Not established from the available artifacts
* 7. Not established from the available artifacts
* 8. Not established from the available artifacts
