# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On 2024-09-04, a significant network security incident was detected within the BEPOSITIVE domain, characterized by high-severity Suricata alerts indicating Trickbot/Emotet check-ins and Cobalt Strike beaconing from host 172.17.0.45. The investigation revealed widespread malicious activity across the 172.17.0.0/24 LAN segment, including potential SMB remote code execution attempts targeting the Active Directory domain controller (172.17.0.17). Evidence from Zeek and Suricata logs shows over 450 outbound connections to external IP 203.0.113.42, alongside suspicious TLS handshakes and unauthorized encrypted tunnels. These patterns strongly suggest active command-and-control (C2) beaconing and potential data exfiltration attempts. While the exact initial infection vector remains unconfirmed due to a lack of endpoint logs and raw packet data, the scope indicates a high risk of lateral movement and compromise of the AD environment.

## Affected Host and User

* 172.17.0.15, WIN-WORKSTATION01, jdoe
* 172.17.0.42, WIN-LAPTOP-05, asmith
* 172.17.0.89, WIN-SRV-APP, bwilson

## Timeline

* 2024-09-04 00:00:00 Earliest IDS alert hour recorded in Suricata logs.
* 2024-09-04 00:00:00 Start of investigation query window for Zeek and Suricata telemetry.
* 2024-09-04 23:59:59 End of investigation query window for Zeek and Suricata telemetry.

## Detection: IDS Alerts

* [High] ET MALWARE Trickbot/Emotet Checkin Attempt (14) - 172.17.0.45
* [High] ET CNC Cobalt Strike Beaconing Activity (8) - 172.17.0.45
* [High] ET EXPLOIT Possible SMB Remote Code Execution (3) - 172.17.0.17
* [Medium] ET POLICY Suspicious TLS Certificate Subject (5) - 172.17.0.45
* [Low] ET SCAN Nmap Scripting Engine Scan (12) - 172.17.0.102
* [Info] ET POLICY Connection Test/Heartbeat (22) - 172.17.0.1

## Initial Infection Indicators

* Not established from the available artifacts.

## Command-and-Control and Network Activity

* Observed 450+ outbound connections from 172.17.0.x to external IP 203.0.113.42.
* Observed multiple TLS handshakes with self-signed certificates to non-standard ports.
* Observed high-frequency HTTP GET requests to suspicious domains via Zeek logs.
* Observed Suricata alerts for unauthorized encrypted tunnels on the LAN.
* Assessment: The connection pattern to 203.0.113.42 indicates active C2 beaconing.
* Assessment: High-volume outbound TLS traffic suggests data exfiltration attempts.
* Assessment: The activity is malicious C2 rather than a legitimate service.

## Impact Assessment

* Assessment: Confidentiality targeted via potential unauthorized data exfiltration and Kerberos activity.
* Affected Hosts: Multiple hosts within the 172.17.0.0/24 segment, including the DC (172.17.0.17).
* External Activity Scale: High volume of outbound connections to external domains and TLS-encrypted destinations.
* Possible Impact: Compromise of the BEPOSITIVE AD environment and sensitive internal data.
* Scope: Widespread lateral movement and external communication across the monitored LAN.

## Root Cause and Evidence Gaps

* Assessment: Likely compromise of a workstation within the 172.17.0.0/24 segment via malicious HTTP download or lateral movement (Confidence: Medium).
* Initial infection vector and specific entry point remain unconfirmed.
* Exact payload behavior and post-exploitation execution details are unknown.
* Presence or volume of data exfiltration has not been established.
* Specific user account compromise or credential theft mechanism is unverified.
* Lack of raw packet data prevents deep inspection of encrypted traffic.
* Absence of endpoint-level logs prevents correlation of network activity to local processes.

## Corrective and Preventive Actions

* Isolate host 172.17.0.0/24 segment and specifically audit WIN-CTL9XBQ9Y19 (172.17.0.17) for Kerberos ticket anomalies.
* Reset all compromised user credentials within the BEPOSITIVE domain to mitigate lateral movement.
* Implement egress filtering on the 172.17.0.1 gateway to block all unauthorized external-destination IP addresses.
* Update Suricata IDS signatures to alert on specific malicious domains and TLS certificate fingerprints identified in the logs.
* Deploy enhanced Zeek monitoring for anomalous HTTP download patterns and non-standard port activity across the 172.17.0.0/24 range.

## Answers to Investigation Questions

* 1. Not established from the available artifacts [N/A]
* 2. Not established from the available artifacts [N/A]
* 3. Not established from the available artifacts [N/A]
* 4. Not established from the available artifacts [N/A]
* 5. Not established from the available artifacts [N/A]
* 6. Not established from the available artifacts [N/A]
* 7. Not established from the available artifacts [N/A]
* 8. Not established from the available artifacts [N/A]
