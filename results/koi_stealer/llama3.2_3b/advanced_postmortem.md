# Incident Postmortem: Network security incident investigation

## Incident Summary

* Affected host and user: The incident involved the internal client 172.17.0.99, which is associated with the human user account afletcher on the desktop-rnvo9at host. [koi_stealer-08#0, koi_stealer-05#0]
* Earliest alert hour: The first signs of infection activity appeared during the hour of 17:00 UTC on 2024-09-04. [koi_stealer-08#0, koi_stealer-06#3]
* Main C2 candidate: The suspicious external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server. [koi_stealer-08#0, koi_stealer-06#3]
* Key assessment: The primary CIA component targeted is confidentiality, as indicated by the presence of high-severity alerts related to suspicious network activity and malware.

## Affected Host and User

* IP address: 172.17.0.99
* Hostname: desktop-rnvo9at
* Human user account: afletcher
* IP address: 172.17.0.99
* Hostname: desktop-rnvo9at
* Human user account: afletcher
* IP address: 172.17.0.99
* Hostname: desktop-rnvo9at
* Human user account: afletcher

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

* High-severity alert signatures with counts:
  * ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events [koi_stealer-08#0, koi_stealer-06#3]
  * ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events [koi_stealer-06#2, koi_stealer-06#0]
  * ET ATTACK RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events [koi_stealer-08#0, koi_stealer-06#3]
* High-severity alerts > high-severity destinations:
  * 79.124.78.197 — 49 events
  * 172.17.0.99 — 1 events
* High-severity alerts > high-severity sources:
  * 79.124.78.197 — 1 events
  * 172.17.0.99 — 49 events

## Initial Infection Indicators

* download domains: 79.124.78.197 — 50 events [koi_stealer-01#0]
* download domains: ctldl.windowsupdate.com — 3 events [koi_stealer-01#0]
* download domains: www.msftconnecttest.com — 2 events [koi_stealer-01#0]
* http requests: 172.17.0.99 -> 79.124.78.197:80 : /foots.php — 48 events [koi_stealer-01#1]
* file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FwBwUeLMampjgOJ5k — 1 events [koi_stealer-01#6]
* download sources: 172.17.0.99 — 361 events [koi_stealer-01#6]

## Command-and-Control and Network Activity

* Derived: internal client 172.17.0.99 ranks #1 by external connections (361 events, 35 distinct external destinations). Most-contacted external IP: 79.124.78.197 (218 connections). [koi_stealer-08#0]
* Derived: Kerberos identity of 172.17.0.99: hostname(s) desktop-rnvo9at; human user account(s) afletcher. [koi_stealer-08#0]
* Suricata alerts span 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC; earliest alert hour 2024-09-04 17:00 UTC (31 alerts). [koi_stealer-08#0]
* Not established from the available artifacts whether the external IP 79.124.78.197 is a C2 server or a legitimate service.
* Not established from the available artifacts whether the internal client 172.17.0.99 is the source of the high-severity alerts.
* Not established from the available artifacts whether the external IP 23.45.119.144 is a C2 server or a legitimate service.
* Not established from the available artifacts whether the internal client 172.17.0.99 is the source of the HTTP requests to 184.29.137.96:80. [koi_stealer-01#2]

## Impact Assessment

* Assessment: The primary CIA component targeted is confidentiality, as indicated by the presence of high-severity alerts related to suspicious network activity and malware. [koi_stealer-06#3, koi_stealer-08#0]
* Assessment: The scale of external activity is moderate to high, with 35 distinct external destinations and 361 events from a single internal client (172.17.0.99). [koi_stealer-08#0]
* Assessment: The number of affected hosts is at least 1, as indicated by the presence of high-severity alerts related to the internal client 172.17.0.99. [koi_stealer-06#1, koi_stealer-08#0]
* Assessment: The impact assessment is possible, but not established from the available artifacts.
* Assessment: The extent of the impact is unclear, but it appears to be related to the unauthorized access or exfiltration of sensitive data.

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but likely root cause: The presence of suspicious Kerberos activity and internal client connections to external IPs, particularly 79.124.78.197, suggests a potential lateral movement or C2 activity. [koi_stealer-08#0]
* Not established from the available artifacts:
 + Initial vector (e.g., phishing, exploit, or vulnerability)
 + Payload behavior (e.g., encryption, compression, or obfuscation)
 + Data exfiltration methods or destinations
 + Queries that failed or were empty
* Assessment: Medium confidence: The high number of file transfers from 172.17.0.99 to external IPs, including 13.70.79.200, 13.89.179.9, and 20.189.173.1, suggests a potential data exfiltration activity. [koi_stealer-01#4]
* Not established from the available artifacts:
 + Payload contents or types
 + External IP involvement or motivations
* Assessment: High confidence: The presence of full services (e.g., Kerberos, CIFS, and LDAP) from 172.17.0.99 to internal and external destinations, including the AD domain controller and external IPs, suggests a potential C2 activity. [koi_stealer-04#0]
* Not established from the available artifacts:
 + C2 server or command-and-control activity specifics
 + Payload behavior or encryption methods

## Corrective and Preventive Actions

* Isolate the internal client 172.17.0.99 immediately to prevent further lateral movement and potential data exfiltration. [koi_stealer-08#0, koi_stealer-04#1]
* Block the most-contacted external IP, 79.124.78.197, from accessing the internal network to prevent potential command-and-control (C2) communication. [koi_stealer-08#0, koi_stealer-01#2]
* Reset the Kerberos identity of 172.17.0.99 to prevent potential use of compromised credentials for future attacks. [koi_stealer-08#0, koi_stealer-04#1]
* Review and update the network segmentation and access controls to prevent similar incidents in the future, considering the use of a more secure gateway and segment isolation.

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0, koi_stealer-04#1].
3. The Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN is afletcher [koi_stealer-03#0, koi_stealer-04#1].
4. Not established from the available artifacts.
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].
6. Not established from the available artifacts.
7. The first signs of infection activity appeared during the hour of 17:00 UTC on 2024-09-04 [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].
8. The single external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
