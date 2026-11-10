# Incident Postmortem: Network security incident investigation

## Incident Summary

* The affected host is 172.17.0.99, a desktop-rnvo9at machine, and the human user account is afletcher. [koi_stealer-08#0, koi_stealer-05#0]
* The earliest alert hour is 17:00 UTC on 2024-09-04. [koi_stealer-08#0, koi_stealer-06#3]
* The main C2 candidate is 79.124.78.197. [koi_stealer-08#0, koi_stealer-06#3]
* Assessment: The incident appears to be an internal threat actor using a Koi Stealer malware, with a focused attack window from 17:00 UTC to 18:00 UTC on 2024-09-04, indicating potential availability and lateral movement within the LAN. [koi_stealer-08#0, koi_stealer-06#3]

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
  + ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events [koi_stealer-08#0, koi_stealer-06#3]
  + ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events [koi_stealer-06#2, koi_stealer-06#0]
  + ET ATTACK RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events [koi_stealer-08#0, koi_stealer-06#3]
* High-severity alerts > high-severity destinations:
  + 79.124.78.197 — 49 events
  + 172.17.0.99 — 1 events
* Hosts involved:
  + 172.17.0.99
  + desktop-rnvo9at
* External destinations:
  + 79.124.78.197 (35 distinct external destinations) [koi_stealer-08#0]

## Initial Infection Indicators

* download domains: 79.124.78.197 — 50 events [koi_stealer-01#0]
* download domains: ctldl.windowsupdate.com — 3 events [koi_stealer-01#0]
* download domains: www.msftconnecttest.com — 2 events [koi_stealer-01#0]
* possible download domains: x1.c.lencr.org — 1 events [koi_stealer-01#1]
* http requests: 172.17.0.99 -> 79.124.78.197:80 : /foots.php — 48 events [koi_stealer-01#1]
* file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FwBwUeLMampjgOJ5k — 1 events [koi_stealer-01#6]

## Command-and-Control and Network Activity

* 172.17.0.99 ranks #1 by external connections with 361 events, most-contacted external IP being 79.124.78.197 with 218 connections [koi_stealer-08#0].
* The affected host, 172.17.0.99, has a Kerberos identity of hostname "desktop-rnvo9at" and human user account "afletcher" [koi_stealer-08#0].
* High-severity alerts span from 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC, with 31 alerts during this time frame [koi_stealer-08#0].
* Destinations of high-severity alerts include 79.124.78.197 (49) and 172.17.0.99 (1) [koi_stealer-08#0].
* The host 172.17.0.99 has made connections to multiple external IPs, including 79.124.78.197, 23.45.119.144, 204.79.197.203, 52.113.194.132, and 23.195.212.189 [koi_stealer-02#0].
* The host 172.17.0.99 has made HTTP requests to multiple external IPs, including 23.220.251.158, 79.124.78.197, 184.29.137.96, 199.232.210.172, and 23.195.212.189 [koi_stealer-01#2].
* The host 172.17.0.99 has made connections to domains such as weathermapdata.blob.core.windows.net, sso.godaddy.com, www.bellantonicioccolato.it, img-s-msn-com.akamaized.net, and oneclient.sfx.ms [koi_stealer-07#0].

## Impact Assessment

* Assessment: The primary CIA component targeted appears to be availability, as the incident involved a significant amount of network activity and potential data exfiltration [koi_stealer-02#0].
* The number of affected hosts is at least 1, as indicated by the high-severity alerts related to internal client 172.17.0.99 [koi_stealer-06#1, koi_stealer-08#0].
* The scale of external activity is significant, with 35 distinct external destinations and 361 events from internal client 172.17.0.99 [koi_stealer-08#0].
* The most-contacted external IP is 79.124.78.197, with 218 connections from internal client 172.17.0.99 [koi_stealer-08#0].
* The high-severity alerts span a short time frame, from 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC, suggesting a focused attack window [koi_stealer-08#0].

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but likely root cause: The presence of suspicious Kerberos identity and high-severity alerts from Suricata, pointing to internal client 172.17.0.99, suggests an internal threat actor. [koi_stealer-08#0, koi_stealer-04#1]
* Not established from the available artifacts: Initial vector, payload behavior, data exfiltration, queries that failed or were empty.
* Assessment: Medium confidence: The high number of external connections from internal client 172.17.0.99 and the presence of suspicious file transfers to external IPs suggest a potential C2 activity. [koi_stealer-08#0, koi_stealer-04#1]
* Not established from the available artifacts: C2 server attribution, payload type, command execution.
* Assessment: Low confidence: The absence of chat/communication records and no clear indication of data exfiltration suggests that the impact might be limited to internal activities.
* Not established from the available artifacts: Full extent of impact, data exfiltration, or lateral movement.
* Not established from the available artifacts: Root cause attribution, initial infection vector, or persistence mechanism.

## Corrective and Preventive Actions

* Isolate the internal client 172.17.0.99 from the rest of the network immediately to prevent further potential malicious activity. [koi_stealer-08#0, koi_stealer-04#1]
* Block the external IP address 79.124.78.197 from accessing the internal network to prevent further malicious connections. [koi_stealer-08#0, koi_stealer-01#2]
* Reset the Kerberos identity of 172.17.0.99 to prevent potential future authentication attempts. [koi_stealer-08#0, koi_stealer-04#1]
* Review and update the network segmentation and access controls to ensure that the internal client 172.17.0.99 does not have excessive external connections. [koi_stealer-08#0, koi_stealer-04#1]
* Investigate and address the potential vulnerabilities in the Active Directory environment, specifically the Kerberos configuration, to prevent similar incidents in the future.

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0, koi_stealer-04#1].
3. The Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN is afletcher [koi_stealer-03#0].
4. The likely fake or suspicious domains / URLs for initial infection are weathermapdata.blob.core.windows.net, sso.godaddy.com, www.bellantonicioccolato.it, img-s-msn-com.akamaized.net, and oneclient.sfx.ms. [koi_stealer-07#1, koi_stealer-07#0]
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].
6. Not established from the available artifacts.
7. The first signs of infection activity appeared during the hour of 17:00 UTC on 2024-09-04 [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].
8. According to the connection volume statistics, the single external IP address that received the most connections from the infected hosts is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0, koi_stealer-06#2, koi_stealer-06#3, koi_stealer-06#1].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
