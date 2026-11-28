# Incident Postmortem: Network security incident investigation

## Incident Summary

* The affected host is 172.17.0.99, an internal client with a high volume of external connections (361 events) and distinct external destinations (35), with the most-contacted external IP being 79.124.78.197. [auto: koi_stealer-08#0, koi_stealer-02#0]
* The earliest alert hour is 2024-09-04 17:00 UTC, with a total of 31 events during this time. [auto: koi_stealer-08#0, koi_stealer-06#3]
* The main C2 candidate is 79.124.78.197, an external IP address that received the most connections from the infected host. [koi_stealer-06#2, koi_stealer-06#3]
* Assessment: The high volume of connections to 79.124.78.197, combined with the presence of Kerberos identity and Suricata alerts, suggests a potential Command-and-Control (C2) connection, but the lack of concrete evidence makes this assessment uncertain. [auto: koi_stealer-08#0, koi_stealer-06#3]

## Affected Host and User

* 172.17.0.99 is an internal client that ranks #1 by external connections with 361 events and 35 distinct external destinations, with the most-contacted external IP being 79.124.78.197. [auto: koi_stealer-08#0]
* The Kerberos identity of 172.17.0.99 is afletcher, a human user account. [auto: koi_stealer-08#0, koi_stealer-05#0]
* The hostnames associated with 172.17.0.99 are desktop-rnvo9at. [auto: koi_stealer-08#0, koi_stealer-05#0]
* The source IP of 172.17.0.99 is also listed as 172.17.0.99 in some of the evidence, indicating it may be a misattribution or a case of the same host presenting itself under different names. [auto: koi_stealer-08#0, koi_stealer-05#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

* High-severity malicious signatures:
  * ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events [auto: koi_stealer-08#0, koi_stealer-06#3]
  * ET ATTACK RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events [auto: koi_stealer-08#0, koi_stealer-06#3]
  * ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 49 events [auto: koi_stealer-08#0, koi_stealer-06#2]
* High-severity alerts > high-severity destinations:
  * 79.124.78.197 — 50 events
  * 172.17.0.99 — 50 events
* High-severity alerts > high-severity sources:
  * 172.17.0.99 — 50 events
  * 79.124.78.197 — 50 events
* Informational alerts:
  * ET INFO Microsoft Connection Test — 2 events [auto: koi_stealer-06#0]
  * GPL NETBIOS SMB IPC$ unicode share access — 5 events [auto: koi_stealer-06#0]
  * ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events ( duplicate, not established as new)
  * ET ATTACK RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events (duplicate, not established as new)
  * ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events (duplicate, not established as new)

## Initial Infection Indicators

* download domains: 79.124.78.197 — 50 events [koi_stealer-01#0]
* download domains: ctldl.windowsupdate.com — 3 events [koi_stealer-01#0]
* download domains: www.msftconnecttest.com — 2 events [koi_stealer-01#0]
* http requests: 172.17.0.99 -> 79.124.78.197:80 : /foots.php — 48 events [koi_stealer-01#1]
* file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FwBwUeLMampjgOJ5k — 1 events [koi_stealer-01#6]
* download sources: 172.17.0.99 — 361 events [koi_stealer-01#6]

## Command-and-Control and Network Activity

* Derived: internal client 172.17.0.99 ranks #1 by external connections (361 events, 35 distinct external destinations). Most-contacted external IP: 79.124.78.197 (218 connections). [auto: koi_stealer-08#0]
* Derived: Kerberos identity of 172.17.0.99: hostname(s) desktop-rnvo9at; human user account(s) afletcher. [auto: koi_stealer-08#0, koi_stealer-05#0]
* Derived: Suricata alerts span 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC; earliest alert hour 2024-09-04 17:00 UTC (31 alerts). [auto: koi_stealer-08#0]
* Derived: destinations of high-severity alerts: 79.124.78.197 (49), 172.17.0.99 (1). [auto: koi_stealer-08#0]
* Assessment: The high volume of connections to 79.124.78.197 suggests a potential Command-and-Control (C2) server, but not established from the available artifacts.
* Assessment: The presence of multiple high-severity alerts from the same external IP address (79.124.78.197) raises suspicions of malicious activity, but further analysis is required to confirm. [auto: koi_stealer-08#0, koi_stealer-02#0]
* Assessment: The Kerberos identity of 172.17.0.99 indicates a legitimate user account, but the unusual volume of connections to an external IP address complicates this assessment. [auto: koi_stealer-08#0, koi_stealer-05#0]

## Impact Assessment

* Assessment: The primary CIA component targeted is **confidentiality**, as indicated by the high volume of high-severity alerts related to suspicious network activity and malware connections. [koi_stealer-06#3]
* Assessment: The scale of external activity is **possible** to be significant, given the large number of external connections (361 events) and distinct external destinations (35) from a single internal client (172.17.0.99). [koi_stealer-08#0]
* Assessment: The majority of high-severity alerts (49 out of 50) are related to the same external IP (79.124.78.197), suggesting a high level of coordination between the malware and the external server. [koi_stealer-06#1]
* Assessment: The Kerberos identity of 172.17.0.99 suggests that the malware has gained access to the internal network, potentially compromising the confidentiality of sensitive data. [koi_stealer-08#0]

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but likely root cause: The presence of suspicious certificates and short validity certs in the Elasticsearch aggregation results suggests potential malware activity, but this is not conclusive evidence.
* Not established from the available artifacts: Initial vector (how the malware entered the network), payload behavior, data exfiltration methods, and queries that failed or were empty.
* Assessment: Medium confidence: The high number of external connections from internal client 172.17.0.99 and the presence of Kerberos identity and Suricata alerts suggest a potential C2 connection, but the lack of concrete evidence makes this assessment uncertain. [auto: koi_stealer-08#0, koi_stealer-04#1]
* Not established from the available artifacts: Command-and-control server IP or domain, C2 server activity, and the nature of the malware's communication with the C2 server.
* Assessment: Low confidence: The file transfer events from 172.17.0.99 to external IP addresses suggest potential data exfiltration, but the lack of concrete evidence makes this assessment uncertain. [auto: koi_stealer-08#0, koi_stealer-04#1]
* Not established from the available artifacts: The nature of the data being exfiltrated, the destination of the data, and the duration of the data exfiltration.
* Not established from the available artifacts: The impact of the malware on the network or the affected host.

## Corrective and Preventive Actions

* Isolate the internal client 172.17.0.99 from the rest of the network immediately to prevent further potential damage or lateral movement. [auto: koi_stealer-08#0, koi_stealer-04#1]
* Block the external IP address 79.124.78.197 from accessing the internal network to prevent further malicious activity. [auto: koi_stealer-08#0, koi_stealer-01#2]
* Reset the Kerberos identity of 172.17.0.99 to prevent potential future exploitation. [auto: koi_stealer-08#0, koi_stealer-04#1]
* Review and update the network segmentation and access controls to ensure that the internal client 172.17.0.99 does not have excessive external connections. [auto: koi_stealer-08#0, koi_stealer-04#1]
* Conduct a thorough review of the AD environment and ensure that all Kerberos tickets are properly revoked and cleaned up to prevent potential future attacks.

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0, koi_stealer-04#1].
3. The Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN is afletcher [koi_stealer-03#0, koi_stealer-08#0].
4. The likely fake or suspicious domains / URLs for initial infection are weathermapdata.blob.core.windows.net, sso.godaddy.com, www.bellantonicioccolato.it, img-s-msn-com.akamaized.net, and oneclient.sfx.ms. [koi_stealer-07#1, koi_stealer-07#0]
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].
6. Not established from the available artifacts.
7. The first signs of infection activity appeared during the hour of 17:00 UTC on 2024-09-04 [koi_stealer-08#0, koi_stealer-06#3, koi_stealer-06#1].
8. According to the connection volume statistics, the single external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
