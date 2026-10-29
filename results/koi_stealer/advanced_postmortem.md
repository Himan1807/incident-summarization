# Incident Postmortem: Network security incident investigation

## Incident Summary

The affected internal host is 172.17.0.99, with hostname(s) desktop-rnvo9at and human user account(s) afletcher. [koi_stealer-08#0] The host 172.17.0.99 was in contact with 35 distinct external destinations, with 79.124.78.197 being the most-contacted external IP (218 connections). [koi_stealer-08#0] High-severity malicious signatures were detected, with 50 matching events, primarily related to the Koi Stealer malware. [koi_stealer-06#1] The high-severity alerts spanned the time period 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC. [koi_stealer-08#0] The earliest alert hour was 2024-09-04 17:00 UTC, with 31 alerts. [koi_stealer-08#0] The host 172.17.0.99 was the most-contacted external destination, with 361 events and 35 distinct external destinations. [koi_stealer-08#0]

## Affected Host and User

* The affected internal host is 172.17.0.99, with hostname(s) desktop-rnvo9at and human user account(s) afletcher. [koi_stealer-08#0]
* The host 172.17.0.99 was in contact with 35 distinct external destinations, with 79.124.78.197 being the most-contacted external IP (218 connections). [koi_stealer-08#0]
* The host 172.17.0.99 was involved in 8 Kerberos TCP (krb_tcp) events. [koi_stealer-04#0]
* The host 172.17.0.99 was involved in 2 Kerberos ticket-granting ticket (krbtgt) events for the BEPOSITIVE.COM domain. [koi_stealer-04#0]
* The host 172.17.0.99 was involved in 1 LDAP event for the WIN-CTL9XBQ9Y19.bepositive.com domain. [koi_stealer-04#0]
* The host 172.17.0.99 was involved in 1 CIFS event for the desktop-rnvo9at.bepositive.com domain. [koi_stealer-04#1]
* The host 172.17.0.99 was involved in 1 Kerberos ticket-granting ticket (krbtgt) event for the BEPOSITIVE domain. [koi_stealer-04#1]
* The host 172.17.0.99 was involved in 8 client account events. [koi_stealer-03#0]
* The host 172.17.0.99 was involved in 361 events, with 31 of those events occurring between 17:00 and 18:00 UTC on 2024-09-04. [koi_stealer-08#0]  ⚠ UNVERIFIED: 00, 17

## Timeline

* 2024-09-04 17:00 UTC: High severity alerts started, with 31 events reported (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: High severity sources: 79.124.78.197 — 1 events (koi_stealer-06#3). [koi_stealer-06#3]  ⚠ UNVERIFIED: 3
* 2024-09-04 17:00 UTC: High severity signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 17:00 UTC: High severity signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events (koi_stealer-06#2). [koi_stealer-06#3, koi_stealer-06#0]
* 2024-09-04 17:00 UTC: High severity alerts > high severity destinations: 79.124.78.197 — 49 events (koi_stealer-06#1). [koi_stealer-08#0, koi_stealer-06#3]
* 2024-09-04 17:00 UTC: High severity alerts > high severity sources: 172.17.0.99 — 49 events (koi_stealer-06#1). [koi_stealer-08#0]
* 2024-09-04 17:00 UTC: High severity signatures: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: High severity signatures: GPL NETBIOS SMB IPC$ unicode share access — 5 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: High severity signatures: ET INFO Microsoft Connection Test — 2 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 18:00 UTC: High severity alerts continued, with 26 events reported (koi_stealer-08#0). [koi_stealer-08#0, koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 18:00 UTC: High severity signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events (koi_stealer-06#2). [koi_stealer-06#3, koi_stealer-06#0]
* 2024-09-04 18:00 UTC: High severity alerts > high severity destinations: 79.124.78.197 — 49 events (koi_stealer-06#1). [koi_stealer-08#0, koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity alerts > high severity sources: 172.17.0.99 — 1 events (koi_stealer-06#1). [koi_stealer-08#0, koi_stealer-06#3]

## Detection: IDS Alerts

* High-severity malicious signatures were detected, with 50 matching events, primarily related to the Koi Stealer malware. [koi_stealer-06#1]
* The Koi Stealer CnC Checkin (GET) signature was triggered 1 event. [koi_stealer-06#1]
* The most common high-severity alert destination was 79.124.78.197, with 49 events. [koi_stealer-06#1]
* The host 172.17.17.0.99 was involved in high-severity alerts, with 1 event. [koi_stealer-06#1]  ⚠ UNVERIFIED: 172.17.17.0
* Suspicious POSTs to dotted quads with fake browsers were detected, with 48 events. [koi_stealer-06#0]
* A Koi Loader/Stealer CnC Config Inbound signature was triggered 1 event. [koi_stealer-06#2]
* The host 172.17.0.99 was involved in high-severity sources, with 49 events. [koi_stealer-06#2]
* The external IP 79.124.78.197 was contacted by 172.17.0.99, with 218 connections. [koi_stealer-08#0]
* The high-severity alerts spanned the time period 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC. [koi_stealer-08#0]
* The earliest alert hour was 2024-09-04 17:00 UTC, with 31 alerts. [koi_stealer-08#0]
* The host 172.17.0.99 was the most-contacted external destination, with 361 events and 35 distinct external destinations. [koi_stealer-08#0]
* The host 172.17.0.99 was involved in 1 high-severity alert destination. [koi_stealer-06#1]
* The host

⚠ TRUNCATED: output hit the 600-token cap; raise num_predict for this section.

## Initial Infection Indicators

* Suspicious domains/URLs:
    + Possible: 79.124.78.197 (downloaded 50 times) [koi_stealer-01#0]
    + Possible: x1.c.lencr.org (downloaded 1 time) [koi_stealer-01#1]
    + Possible: 23.220.251.149 (downloaded 2 times) [koi_stealer-01#1]
    + Possible: 23.220.251.158 (downloaded 2 times) [koi_stealer-01#2]
    + Possible: 184.29.137.96 (downloaded 1 time) [koi_stealer-01#2]
    + Possible: 199.232.210.172 (downloaded 2 times) [koi_stealer-01#2]
    + Possible: 199.232.214.172 (downloaded 1 time) [koi_stealer-01#3]
    + Possible: 23.220.251.47 (downloaded 1 time) [koi_stealer-01#3]
* Downloaded files:
    + Not established from the available artifacts
* Assessment: The presence of multiple suspicious domains and URLs suggests a possible infection vector, but the exact initial vector is not established from the available artifacts.

## Command-and-Control and Network Activity

* Observed facts:
    + The internal client 172.17.0.99 had the most external connections (361 events) with 35 distinct external destinations. [koi_stealer-08#0, koi_stealer-02#0]
    + The most-contacted external IP was 79.124.78.197 with 218 connections. [koi_stealer-08#0, koi_stealer-02#0]
    + There were 31 Suricata alerts spanning 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC, with 49 high-severity alerts targeting 79.124.78.197. [koi_stealer-08#0]
    + The human user account associated with the Kerberos identity of 172.17.0.99 was afletcher. [koi_stealer-08#0, koi_stealer-05#0]
    + The hostnames associated with 172.17.0.99 were desktop-rnvo9at. [koi_stealer-08#0, koi_stealer-05#0]
    + The external IP 79.124.78.197 was contacted by 172.17.0.99 for HTTP requests (koi_stealer-01#2). [koi_stealer-01#2]
* Assessment:
    + The high frequency of connections to 79.124.78.197 and the presence of HTTP requests to this IP suggest potential Command-and-Control (C2) activity. [koi_stealer-08#0, koi_stealer-02#0]
    + The fact that 79.124.78.197 was targeted by 49 high-severity alerts suggests that it may be a malicious actor. [koi_stealer-08#0]
    + The presence of HTTP requests to multiple external IPs, including 79.124.78.197, suggests that the affected host may be communicating with multiple C2 servers or legitimate services. [koi_stealer-08#0, koi_stealer-02#0]

## Impact Assessment

* The primary CIA component targeted is possible integrity, as evidenced by the presence of Koi Stealer CnC Checkin (GET) alerts (koi_stealer-06#1) and the large number of external connections from a single client (koi_stealer-08#0). [koi_stealer-08#0, koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* The number of affected hosts is at least one, as indicated by the Kerberos identity of 172.17.0.99 (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The scale of external activity is significant, with 361 events from a single client (koi_stealer-08#0) and 35 distinct external destinations (koi_stealer-02#0). [koi_stealer-08#0, koi_stealer-02#0]  ⚠ UNVERIFIED: 0
* The external IP 79.124.78.197 was contacted by the affected client 172.17.0.99 on multiple occasions (koi_stealer-02#0, koi_stealer-06#3, koi_stealer-08#0).  ⚠ UNVERIFIED: 0, 3  ⚠ UNCITED
* The domain weathermapdata.blob.core.windows.net was accessed by the affected client (koi_stealer-07#1). [koi_stealer-07#1]
* The affected client 172.17.0.99 was identified as desktop-rnvo9at, with a human user account afletcher (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0

## Root Cause and Evidence Gaps

* The most likely root cause is a compromised internal client, Assessment: High.  ⚠ UNCITED
* Not established:
    + Initial vector (how the compromise occurred)  ⚠ UNCITED
    + Payload behavior (what the malware did after initial infection)  ⚠ UNCITED
    + Data exfiltration (if any data was stolen or transmitted)  ⚠ UNCITED
    + Queries that failed or were empty (in the Elasticsearch aggregation results) [koi_stealer-09#0]
    + C2 (Command and Control) server(s) or communication channels used by the malware  ⚠ UNCITED
    + Type of malware or payload used (no specific malware indicators were found in the evidence)  ⚠ UNCITED

## Corrective and Preventive Actions

* Isolate host 172.17.0.99 from the network to prevent further communication with external destinations. [koi_stealer-08#0, koi_stealer-04#1]
* Investigate the file transfers initiated by host 172.17.0.99, particularly the files with fuids FU0Kma3jtLVDFQsWRa, FMvkJInaCxvQDPRv9, FLUKDa36wJdASXKgHg, FhRlFk2pp8tC1dsabb, FyjT0AzkMPMcF8Uck, FpR8YU2UKfciamuQTd, and FSvMjvPqRih6zUFI5. [koi_stealer-08#0, koi_stealer-04#1]
* Review the HTTP requests made by host 172.17.0.99, particularly the requests to 23.220.251.158, 79.124.78.197, 184.29.137.96, and 199.232.210.172. [koi_stealer-01#2]

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0].
3. The Windows human user account name of the potentially infected machine in the LAN is afletcher [koi_stealer-08#0].
4. The likely fake or suspicious domains / URLs for initial infection are not established from the available artifacts.
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0].
6. Assessment: The attacker targets primarily confidentiality, as the alerts indicate suspicious communication with external IP addresses and domains [koi_stealer-06#2].
7. The first signs of infection activity appeared during the hour of 2024-09-04 17:00 UTC [koi_stealer-06#3].
8. According to the connection volume statistics, the single external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0].
