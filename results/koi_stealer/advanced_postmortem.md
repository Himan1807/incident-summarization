# Incident Postmortem: Network security incident investigation

## Incident Summary

The incident involved a compromised internal host, 172.17.0.99, with hostname desktop-rnvo9at and user account afletcher, which was in contact with 35 distinct external destinations, with the most-contacted external IP being 79.124.78.197. [koi_stealer-08#0] The host was the source of 1 high-severity alert destination and 8 Kerberos TCP (krb_tcp) events. [koi_stealer-04#0, koi_stealer-08#0] High-severity alerts were triggered by the ET MALWARE Win32/Koi Stealer CnC Checkin (GET) signature, with 49 of these alerts targeting the IP address 79.124.78.197 and 1 targeting 172.17.0.99. [koi_stealer-06#1] The affected host made 2 HTTP requests to the IP 79.124.78.197 and 2 HTTP requests to the IP 23.220.251.158. [koi_stealer-01#2] The most likely root cause is a compromised internal client (172.17.0.99) with high external connectivity, possibly due to a malware infection or exploitation of a vulnerability. [koi_stealer-08#0, koi_stealer-04#1]

## Affected Host and User

* The affected internal host is 172.17.0.99, with hostname(s) desktop-rnvo9at and human user account(s) afletcher. [koi_stealer-08#0]
* The host 172.17.0.99 was in contact with 35 distinct external destinations, with the most-contacted external IP being 79.124.78.197. [koi_stealer-08#0]
* The host 172.17.0.99 was the source of 1 high-severity alert destination. [koi_stealer-08#0]
* The host 172.17.0.99 was the source of 8 Kerberos TCP (krb_tcp) events. [koi_stealer-04#0]
* The host 172.17.0.99 was the source of 2 Kerberos ticket-granting ticket (krbtgt) events for the BEPOSITIVE.COM domain. [koi_stealer-04#0]
* The host 172.17.0.99 was the source of 8 client accounts events. [koi_stealer-03#0]
* The host 172.17.0.99 was in contact with 23.45.119.144, 204.79.197.203, 52.113.194.132, and 23.195.212.189, in addition to 79.124.78.197. [koi_stealer-02#0]

## Timeline

* 2024-09-04 17:00 UTC: High severity alerts started, with 31 events reported (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: High severity sources: 79.124.78.197 — 1 events (koi_stealer-06#3). [koi_stealer-06#3]  ⚠ UNVERIFIED: 3
* 2024-09-04 17:00 UTC: High severity signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 17:00 UTC: High severity signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events (koi_stealer-06#2). [koi_stealer-06#3, koi_stealer-06#0]
* 2024-09-04 17:00 UTC: High severity alerts > high severity destinations: 79.124.78.197 — 49 events (koi_stealer-06#1). [koi_stealer-08#0, koi_stealer-06#3]
* 2024-09-04 17:00 UTC: High severity alerts > high severity sources: 172.17.0.99 — 49 events (koi_stealer-06#1). [koi_stealer-08#0]
* 2024-09-04 17:00 UTC: Alert signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events (koi_stealer-06#1). [koi_stealer-06#3]
* 2024-09-04 17:00 UTC: High severity alerts: 50 matching events (koi_stealer-06#1). [koi_stealer-06#3]
* 2024-09-04 17:00 UTC: Alert signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: Alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 5 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: Alert signatures: ET INFO Microsoft Connection Test — 2 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 17:00 UTC: Alert signatures: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events (koi_stealer-06#0). [koi_stealer-06#3]  ⚠ UNVERIFIED: 0
* 2024-09-04 18:00 UTC: High severity alerts > high severity sources: 79.124.78.197 — 26 events (koi_stealer-06#3). [koi_stealer-06#3]  ⚠ UNVERIFIED: 3
* 2024-09-04 18:00 UTC: High severity alerts: 50 matching events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity signatures: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events (koi_stealer-06#2). [koi_stealer-06#3]
* 2024-09-04 18:00 UTC: High severity alerts > high severity destinations: 79.124.78.197 — 1 events (koi_stealer-06#1). [koi_stealer-06#3]

## Detection: IDS Alerts

* 50 high-severity alerts were triggered by the ET MALWARE Win32/Koi Stealer CnC Checkin (GET) signature, with 49 of these alerts targeting the IP address 79.124.78.197 and 1 targeting 172.17.0.99 (koi_stealer-06#1). [koi_stealer-06#1]
* The ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 signature was triggered 48 times, indicating potential malicious activity (koi_stealer-06#0, koi_stealer-06#2). [koi_stealer-06#0]  ⚠ UNVERIFIED: 0
* The ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound signature was triggered 1 time, suggesting a possible command-and-control (C2) communication attempt (koi_stealer-06#2, koi_stealer-06#0). [koi_stealer-06#0]  ⚠ UNVERIFIED: 0
* The IP address 79.124.78.197 was a high-severity destination for 49 high-severity alerts, and a high-severity source for 1 high-severity alert (koi_stealer-06#1, koi_stealer-06#2, koi_stealer-06#3). [koi_stealer-06#1]  ⚠ UNVERIFIED: 3
* The IP address 172.17.0.99 was a high-severity source for 49 high-severity alerts, and a high-severity destination for 1 high-severity alert (koi_stealer-06#1, koi_stealer-06#2). [koi_stealer-06#2, koi_stealer-06#1]
* The host desktop-rnvo9at was involved in 1 event, with the source IP address 172.17.0.99 (koi_stealer-05#0). [koi_stealer-05#0]  ⚠ UNVERIFIED: 0
* The most-contacted external IP address was 79.124.78.197, with 218 connections from the internal client 172.17.0.99 (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The internal client 172.17.0.99 had 361 external connections, with 35 distinct external destinations (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The earliest alert hour was 2024-09-04 17:00 UTC, with 31 alerts triggered during this hour (koi_stealer-08#0, koi_stealer-06#3). [koi_stealer-08#0, koi_stealer-06#3]  ⚠ UNVERIFIED: 0, 3

## Initial Infection Indicators

* Suspicious domains/URLs:
    + 79.124.78.197 (downloaded 50 times) - possible [koi_stealer-01#0]
    + x1.c.lencr.org (downloaded 1 time) - possible [koi_stealer-01#1]
    + 23.220.251.149 (downloaded 2 times) - possible [koi_stealer-01#1]
    + 23.220.251.158 (downloaded 2 times) - possible [koi_stealer-01#2]
    + 184.29.137.96 (downloaded 1 time) - possible [koi_stealer-01#2]
    + 199.232.210.172 (downloaded 2 times) - possible [koi_stealer-01#2]
    + 199.232.214.172 (downloaded 1 time) - possible [koi_stealer-01#3]
    + 23.220.251.47 (downloaded 1 time) - possible [koi_stealer-01#3]
* Downloaded files:
    + Not established from the available artifacts
* Initial infection vector:
    + Not established from the available artifacts

## Command-and-Control and Network Activity

* The affected host 172.17.0.99 made 361 connections to 35 distinct external destinations, with 218 connections to the IP 79.124.78.197. (koi_stealer-08#0) [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The external IP 79.124.78.197 received the most connections from the affected host 172.17.0.99. (koi_stealer-08#0) [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The evidence does not support the presence of a legitimate service, as the connections to 79.124.78.197 are not associated with any known services or domains. (Assessment:) [koi_stealer-08#0, koi_stealer-02#0]
* The affected host 172.17.0.99 made 49 high-severity Suricata alerts to the IP 79.124.78.197. (koi_stealer-08#0) [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The affected host 172.17.0.99 made 2 HTTP requests to the IP 79.124.78.197, with one of the requests being to the URL /index.php?id=&subid=qIOuKk7U. (koi_stealer-01#2) [koi_stealer-01#2]
* The affected host 172.17.0.99 made 2 HTTP requests to the IP 23.220.251.158, with one of the requests being to the URL /connecttest.txt. (koi_stealer-01#2) [koi_stealer-01#2]
* The affected host 172.17.0.99 made connections to multiple external domains, including weathermapdata.blob.core.windows.net, sso.godaddy.com, www.bellantonicioccolato.it, img-s-msn-com.akamaized.net, and oneclient.sfx.ms. (koi_stealer-07#1, koi_stealer-07#0) [koi_stealer-07#0]  ⚠ UNVERIFIED: 0

## Impact Assessment

* The primary CIA component targeted is possible integrity, as evidenced by the presence of Koi Stealer CnC Checkin (GET) alerts (koi_stealer-06#1) and the large number of external connections from 172.17.0.99 (koi_stealer-08#0). [koi_stealer-08#0, koi_stealer-06#2]  ⚠ UNVERIFIED: 0
* The number of affected hosts is at least 1, as indicated by the Kerberos identity of 172.17.0.99 (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* The scale of external activity is significant, with 172.17.0.99 making 361 events to 35 distinct external destinations (koi_stealer-02#0), and the most-contacted external IP being 79.124.78.197 (koi_stealer-08#0). [koi_stealer-08#0, koi_stealer-02#0]  ⚠ UNVERIFIED: 0
* The external IP 79.124.78.197 was contacted by 172.17.0.99 in 218 connections (koi_stealer-08#0), and was also the destination of 49 high-severity alerts (koi_stealer-06#1 and koi_stealer-06#2). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0, 2
* The human user account associated with the compromised host is afletcher (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0

## Root Cause and Evidence Gaps

* Assessment: The most likely root cause is a compromised internal client (172.17.0.99) with high external connectivity, possibly due to a malware infection or exploitation of a vulnerability. Confidence: Medium. [koi_stealer-08#0, koi_stealer-04#1]
* Not established:
    + Initial vector (how the compromise occurred)  ⚠ UNCITED
    + Payload behavior (what actions the malware took after infection)  ⚠ UNCITED
    + Data exfiltration (whether sensitive data was stolen)  ⚠ UNCITED
    + Queries that failed or were empty (any potential gaps in the evidence)  ⚠ UNCITED
    + The specific malware or threat actor involved (only external destinations and file transfers are mentioned)  ⚠ UNCITED

## Corrective and Preventive Actions

* Isolate host 172.17.0.99 from the network to prevent further communication with external destinations, particularly 79.124.78.197, which was contacted 218 times by this host (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* Reset the Kerberos identity of 172.17.0.99, which is associated with the hostname(s) desktop-rnvo9at and human user account(s) afletcher, to prevent potential lateral movement (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* Block the external IP address 79.124.78.197, which was contacted by 172.17.0.99 218 times and was the destination of 49 high-severity Suricata alerts (koi_stealer-08#0). [koi_stealer-08#0]  ⚠ UNVERIFIED: 0
* Investigate the file transfers initiated by 172.17.0.99, which involved multiple external IP addresses, including 13.70.79.200, 13.89.179.9, 20.189.173.1, 20.189.173.26, 20.241.44.114, 20.42.73.28, and 20.96.153.111 (koi_stealer-01#4, koi_stealer-01#5). [koi_stealer-01#5]  ⚠ UNVERIFIED: 4, 5
* Review the HTTP requests initiated by 172.17.0.99, which included requests to multiple external IP addresses, including 23.220.251.158, 79.124.78.197, 184.29.137.96, and 199.232.210.172 (koi_stealer-01#2). [koi_stealer-01#2]

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0].
3. The Windows human user account name of the potentially infected machine in the LAN is afletcher [koi_stealer-08#0].
4. The likely fake or suspicious domains / URLs for initial infection are not established from the available artifacts.
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0].
6. The attacker targets primarily the confidentiality component of the CIA triad, as indicated by the presence of Win32/Koi Stealer CnC Checkin (GET) alerts [koi_stealer-06#2].
7. The first signs of infection activity appeared during the hour of 17:00 UTC on 2024-09-04 [koi_stealer-06#3].  ⚠ UNVERIFIED: 00, 17
8. The single external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0].
