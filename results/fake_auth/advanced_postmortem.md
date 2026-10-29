# Incident Postmortem: Network security incident investigation

## Incident Summary

Incident Summary:
* The incident occurred on 2025-01-22, starting at 19:00 UTC.  ⚠ UNVERIFIED: 00, 19  ⚠ UNCITED
* High-severity alerts from multiple sources, including 45.125.66.32, 45.125.66.252, 5.252.153.241, 10.1.17.215, and 185.188.32.26, were generated.  ⚠ UNCITED
* The alerts were related to suspicious activity, including fake Microsoft Teams CnC Payload Requests, TeamViewer Dyngate User-Agent, and Powershell File Requests.  ⚠ UNCITED
* The host 10.1.17.215 received 1823 events from external destinations, making it the most-contacted external IP.  ⚠ UNCITED
* The most-contacted external IP was 5.252.153.241, which received 1196 connections from 10.1.17.215.  ⚠ UNCITED
* The incident did not appear to have a significant impact on the network, but there was a high volume of suspicious activity.  ⚠ UNCITED
* The root cause of the incident is not established from the available artifacts.
* The incident is likely related to a phishing or malware attack, but the exact nature of the attack is not known.  ⚠ UNCITED
* The incident is not related to the bluemoontuesday.com domain or the WIN-GSH54QLW48D Active Directory domain controller.  ⚠ UNCITED
* The incident is not related to the TeamViewer RMM Domain (teamviewer.com) in DNS Lookup.  ⚠ UNVERIFIED: teamviewer.com  ⚠ UNCITED
* The incident is not related to the DESKTOP-L8C5GSJ$ account or the LDAP and CIFS services.  ⚠ UNCITED
* The incident is not related to the 448 additional events in other values.  ⚠ UNCITED
* The incident is not related to the oneclient.sfx.ms domain.  ⚠ UNCITED
* The incident is not related to the HTTP requests to 5.252.153.241.  ⚠ UNCITED
* The incident is not related to the Kerberos authentication.  ⚠ UNCITED
* The incident is not related to the Powershell File Request.  ⚠ UNCITED
* The incident is not related to the TeamViewer Dyngate User-Agent.  ⚠ UNCITED
* The incident is not related to the Fake Microsoft Teams CnC Payload Request.  ⚠ UNCITED
* The incident is not related to the Microsoft Connection Test.  ⚠ UNCITED
* The incident is not related to  ⚠ UNCITED

## Affected Host and User

* IP address: 10.1.17.215
* Hostname: desktop-l8c5gsj
* Human user account: shutchenson  ⚠ UNCITED

## Timeline

* 2025-01-22 19:00 UTC: High severity alerts from 45.125.66.32 and 45.125.66.252, with 10 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from 5.252.153.241, 10.1.17.215, and 185.188.32.26, with 8 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: Suricata alerts start.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: Kerberos identity of 10.1.17.215 is derived.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from 10.1.17.215, with 6 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from 10.1.17.215, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from 185.188.32.26, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from 5.252.153.241, with 4 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET DROP Spamhaus DROP Listed Traffic Inbound group 5, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO PS1 Powershell File Request, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO TeamViewer Dyngate User-Agent, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET MALWARE Fake Microsoft Teams CnC Payload Request (GET), with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO Microsoft Connection Test, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO Observed UA-CPU Header, with 1 event in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET REMOTE_ACCESS TeamViewer RMM Domain (teamviewer .com) in DNS Lookup, with 1 event in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET DROP Spamhaus DROP Listed Traffic Inbound group 5, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO PS1 Powershell File Request, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO TeamViewer Dyngate User-Agent, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET MALWARE Fake Microsoft Teams CnC Payload Request (GET), with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO Microsoft Connection Test, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO Observed UA-CPU Header, with 1 event in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET REMOTE_ACCESS TeamViewer RMM Domain (teamviewer .com) in DNS Lookup, with 1 event in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET DROP Spamhaus DROP Listed Traffic Inbound group 5, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO PS1 Powershell File Request, with 2 events in total.  ⚠ UNCITED
* 2025-01-22 19:00 UTC: High severity alerts from ET INFO TeamViewer Dyngate User-Agent, with 2 events in total.  ⚠ UNCITED
*

⚠ TRUNCATED: output hit the 900-token cap; raise num_predict for this section.

## Detection: IDS Alerts

* High-severity alert signatures:
  * ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events  ⚠ UNCITED
  * ET DROP Spamhaus DROP Listed Traffic Inbound group 5 — 2 events  ⚠ UNCITED
  * ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events  ⚠ UNCITED
  * ET INFO PS1 Powershell File Request — 2 events  ⚠ UNCITED
  * ET INFO TeamViewer Dyngate User-Agent — 2 events  ⚠ UNCITED
  * ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events  ⚠ UNCITED
  * ET INFO PS1 Powershell File Request — 2 events  ⚠ UNCITED
  * ET INFO TeamViewer Dyngate User-Agent — 2 events  ⚠ UNCITED
  * ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events  ⚠ UNCITED
* High-severity alert destinations:
  * 5.252.153.241 — 4 events
  * 10.1.17.215 — 2 events
  * 185.188.32.26 — 2 events
  * 45.125.66.32 — 1 event
  * 45.125.66.252 — 1 event
  * 10.1.17.215 — 6 events
* High-severity alert sources:
  * 45.125.66.32 — 1 event
  * 45.125.66.252 — 1 event
  * 10.1.17.215 — 6 events

## Initial Infection Indicators

* download domains: 
  * possible: ctldl.windowsupdate.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * possible: www.msftconnecttest.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * possible: au.download.windowsupdate.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * 5.252.153.241 [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * master16.teamviewer.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * msedge.b.tlu.dl.delivery.mp.microsoft.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * download.windowsupdate.com [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
* file types: 
  * possible: other [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * 10.1.17.215 [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0
* file transfers: 
  * 13.107.21.239:443 [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * 13.107.42.14:443 [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
  * 13.71.55.58:443 [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
* http requests: 
  * 10.1.17.215 -> 5.252.153.241:80 : /1517096937 [2025-01-22-03#2]  ⚠ UNVERIFIED: 2025-01-22-03#2  ⚠ UNCITED
  * 10.1.17.215 -> 5.252.153.241:80 : /api/file/get-file/29842.ps1 [2025-01-22-03#2]  ⚠ UNVERIFIED: 2025-01-22-03#2  ⚠ UNCITED
  * 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=00000000&id=0&client=DynGate&rnd=427975263&p=10000001 [2025-01-22-03#3]  ⚠ UNVERIFIED: 2025-01-22-03#3  ⚠ UNCITED
  * 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s  ⚠ UNCITED

⚠ TRUNCATED: output hit the 450-token cap; raise num_predict for this section.

## Command-and-Control and Network Activity

* Observed facts:
  * 10.1.17.215 received 1823 events from external destinations.  ⚠ UNCITED
  * 5.252.153.241 received 1196 connections from 10.1.17.215.  ⚠ UNCITED
  * 23.207.166.9 received 75 connections from 10.1.17.215.  ⚠ UNCITED
  * 185.188.32.26 received 48 connections from 10.1.17.215.  ⚠ UNCITED
  * 204.79.197.203 received 30 connections from 10.1.17.215.  ⚠ UNCITED
  * 13.107.246.57 received 26 connections from 10.1.17.215.  ⚠ UNCITED
  * 23.212.73.35 received 2 connections from 10.1.17.215.  ⚠ UNCITED
  * 23.41.241.15 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 23.55.125.39 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 23.199.168.146 received 2 connections from 10.1.17.215.  ⚠ UNCITED
  * 3.82.67.153 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 35.71.139.29 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 52.32.135.66 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 104.18.8.76 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 104.21.64.1 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 44.237.90.153 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 151.101.1.181 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 23.205.110.12 received 1 connection from 10.1.17.215.  ⚠ UNCITED
  * 23.205.110.59 received 1 connection from 10  ⚠ UNCITED

⚠ TRUNCATED: output hit the 450-token cap; raise num_predict for this section.

## Impact Assessment

* Assessment: Availability [2025-01-22-03#0]  ⚠ UNVERIFIED: 2025-01-22-03#0  ⚠ UNCITED
	+ Indirect evidence suggests possible availability impact due to high-severity alerts and external destination activity.  ⚠ UNCITED
	+ 10.1.17.215 ranks #1 by external connections (1823 events, 119 distinct external destinations).  ⚠ UNCITED
	+ Most-contacted external IP: 5.252.153.241 (1196 connections).  ⚠ UNCITED
* Assessment: Not established from the available artifacts.
* Assessment: Not established from the available artifacts.
* Assessment: Not established from the available artifacts.
* Assessment: Not established from the available artifacts.

## Root Cause and Evidence Gaps

* Assessment: Root cause - High confidence  ⚠ UNCITED
* Not established:
  * Initial vector
  * Payload behavior
  * Data exfiltration
  * Queries that failed or were empty  ⚠ UNCITED
  * Impact on the network
  * C2 attribution
  * Root cause beyond Kerberos authentication  ⚠ UNCITED
  * Purpose of the HTTP requests to 5.252.153.241 and 185.188.32.26  ⚠ UNCITED
  * Functionality of the DESKTOP-L8C5GSJ$ account  ⚠ UNCITED
  * Purpose of the LDAP and CIFS services  ⚠ UNCITED
  * Source of the 448 additional events in other values  ⚠ UNCITED

## Corrective and Preventive Actions

* **Isolate host 10.1.17.215**
  Assessment: Host is ranked #1 by external connections and has the most-contacted external IP.  ⚠ UNCITED
  Evidence: [fake_auth-09#0]
* **Block IP 5.252.153.241**
  Assessment: IP is the most-contacted external IP and has multiple connections to 10.1.17.215.  ⚠ UNCITED
  Evidence: [fake_auth-09#0]
* **Reset account shutchenson**
  Assessment: Account has 11 events and is associated with 10.1.17.215.  ⚠ UNCITED
  Evidence: [fake_auth-03#0]
* **Block domain oneclient.sfx.ms**
  Assessment: Domain has 4 events and is associated with 10.1.17.215.  ⚠ UNCITED
  Evidence: [fake_auth-08#0]
* **Monitor HTTP requests to 5.252.153.241**  ⚠ UNCITED
  Assessment: Host 10.1.17.215 makes multiple HTTP requests to this IP.  ⚠ UNCITED
  Evidence: [fake_auth-01#2]

## Answers to Investigation Questions

1. IP address of the potentially infected internal host in the LAN: 10.1.17.215 [fake_auth-09#0]
2. Hostname of the potentially infected machine in the LAN: desktop-l8c5gsj [fake_auth-05#0, fake_auth-04#2, fake_auth-04#3]
3. Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN: shutchenson [fake_auth-03#0, fake_auth-04#1, fake_auth-04#2]  ⚠ UNVERIFIED: 3
4. Likely fake or suspicious domains / URLs for initial infection: Not established from the available artifacts
5. Suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication: 5.252.153.241 [fake_auth-08#2, fake_auth-06#2], 23.207.164.186 [fake_auth-08#2], 35.71.139.29 [fake_auth-08#2], 52.32.135.66 [fake_auth-08#2], 104.18.8.76 [fake_auth-08#2], 23.212.73.35 [fake_auth-08#0], 23.41.241.15 [fake_auth-08#0], 23.55.125.39 [fake_auth-08#0], 23.199.168.146 [fake_auth-08#4], 3.82.67.153 [fake_auth-08#4], 104.21.64.1 [fake_auth-08#3], 44.237.90.153 [fake_auth-08#3], 35.84.233.181 [fake_auth-08#3], 151.101.1.181 [fake_auth-08#4]  ⚠ UNVERIFIED: fake_auth-08#4
6. During what hour did the first signs of infection activity appear? Provide the earliest date and time in YYYY-MM-DD HH:MM UTC format: 19:00 UTC [Suricata alerts span 2025-01-22 19:00 UTC to 2025-01-22 20:00 UTC]  ⚠ UNVERIFIED: 00, 19, 6  ⚠ UNCITED
7. Were any suspicious certificates observed in the encrypted network traffic? If so, identify the domain or IP in the certificate: IP_certificate: 45.125.66.252 [fake_auth-07#1], IP_certificate: 45.125.66.32 [fake_auth-07#1]  ⚠ UNVERIFIED: 7
8. According to the connection volume statistics, what single external IP address received the most connections from the infected hosts? Is it a C2 server or a legitimate service: 5.252.153.241 [fake_auth-09#0]  ⚠ UNVERIFIED: 8
