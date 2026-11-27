# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.1.17.215 ranks #1 by external connections (1823 events, 119 distinct external destinations). Most-contacted external IP: 5.252.153.241 (1196 connections). [fake_auth-09#0]
- Derived: Kerberos identity of 10.1.17.215: hostname(s) desktop-l8c5gsj; human user account(s) shutchenson. [fake_auth-09#0]
- Derived: Suricata alerts span 2025-01-22 19:00 UTC to 2025-01-22 20:00 UTC; earliest alert hour 2025-01-22 19:00 UTC (10 alerts). [fake_auth-09#0]
- Derived: destinations of high-severity alerts: 5.252.153.241 (4), 10.1.17.215 (2), 185.188.32.26 (2). [fake_auth-09#0]
- client accounts: shutchenson — 11 events; source ips: 10.1.17.215 (11) [fake_auth-03#0]
- client accounts: DESKTOP-L8C5GSJ$ — 10 events; source ips: 10.1.17.215 (10) [fake_auth-03#0]
- client accounts: desktop-l8c5gsj$ — 4 events; source ips: 10.1.17.215 (4) [fake_auth-03#0]
- full services: netlogon/WIN-GSH54QLW48D.bluemoontuesday.com/bluemoontuesday.com — 1 events; source ips: 10.1.17.215 (1) [fake_auth-04#3]
- source clients: 10.1.17.215 — 1823 events; external destinations=119; top destinations: 5.252.153.241 (1196), 23.207.166.9 (75), 185.188.32.26 (48), 204.79.197.203 (30), 13.107.246.57 (26); 448 further events in other values [fake_auth-02#0]
- hostnames: desktop-l8c5gsj — 1 events; source ips: 10.1.17.215 (1) [fake_auth-05#0]
- full services: ldap/win-gsh54qlw48d.bluemoontuesday.com — 2 events; source ips: 10.1.17.215 (2) [fake_auth-04#1]
- full services: DESKTOP-L8C5GSJ$ — 1 events; source ips: 10.1.17.215 (1) [fake_auth-04#1]
- full services: LDAP/WIN-GSH54QLW48D.bluemoontuesday.com — 1 events; source ips: 10.1.17.215 (1) [fake_auth-04#1]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

- alert signatures: ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events [fake_auth-06#1]
- alert signatures: ET INFO Observed UA-CPU Header — 1 events [fake_auth-06#1]
- alert signatures: ET REMOTE_ACCESS TeamViewer RMM Domain (teamviewer .com) in DNS Lookup — 1 events [fake_auth-06#1]
- high severity alerts: 8 matching events [fake_auth-06#1]
- high severity alerts > high severity signatures: ET INFO PS1 Powershell File Request — 2 events [fake_auth-06#3]
- high severity alerts > high severity signatures: ET INFO TeamViewer Dyngate User-Agent — 2 events [fake_auth-06#3]
- high severity alerts > high severity sources: 10.1.17.215 — 6 events [fake_auth-06#3]
- high severity alerts > high severity sources: 45.125.66.32 — 1 events [fake_auth-06#4]
- high severity alerts > high severity sources: 45.125.66.252 — 1 events [fake_auth-06#4]
- alert signatures: ET DROP Spamhaus DROP Listed Traffic Inbound group 5 — 2 events [fake_auth-06#0]
- alert signatures: ET INFO Microsoft Connection Test — 2 events [fake_auth-06#0]
- high severity alerts > high severity  destinations: 5.252.153.241 — 4 events [fake_auth-06#2]
- high severity alerts > high severity  destinations: 10.1.17.215 — 2 events [fake_auth-06#2]
- high severity alerts > high severity  destinations: 185.188.32.26 — 2 events [fake_auth-06#2]

## Initial Infection Indicators

- download domains: ctldl.windowsupdate.com — 2 events [fake_auth-01#1]
- download domains: www.msftconnecttest.com — 2 events [fake_auth-01#1]
- download domains: au.download.windowsupdate.com — 1 events [fake_auth-01#1]
- http requests: no_http_uri — 1187 events [fake_auth-01#1]
- http requests: 10.1.17.215 -> 5.252.153.241:80 : /1517096937 — 584 events [fake_auth-01#2]
- http requests: 10.1.17.215 -> 5.252.153.241:80 : /api/file/get-file/29842.ps1 — 4 events [fake_auth-01#2]
- http requests: 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=00000000&id=0&client=DynGate&rnd=427975263&p=10000001 — 3 events [fake_auth-01#2]
- http requests: 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=91930119&id=0&client=DynGate&p=10000002 — 3 events [fake_auth-01#2]
- http requests: 10.1.17.215 -> 5.252.153.241:80 : /1517096937?k=script: RunRH, status: OK, message: PS process started — 3 events [fake_auth-01#3]
- http requests: 10.1.17.215 -> 5.252.153.241:80 : /api/file/get-file/264872 — 3 events [fake_auth-01#3]
- http requests: 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=91930135&id=0&client=DynGate&p=10000002 — 2 events [fake_auth-01#3]
- http requests: 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=91930144&id=0&client=DynGate&p=10000002 — 2 events [fake_auth-01#3]
- domains: oneclient.sfx.ms — 4 events; top source ips: 10.1.17.215 (4); top destination ips: 23.212.73.35 (2), 23.41.241.15 (1), 23.55.125.39 (1) [fake_auth-08#0]
- domains: img-s-msn-com.akamaized.net — 2 events; top source ips: 10.1.17.215 (2); top destination ips: 23.205.110.12 (1), 23.205.110.59 (1) [fake_auth-08#0]
- domains: px.owneriq.net — 2 events; top source ips: 10.1.17.215 (2); top destination ips: 23.199.168.146 (2) [fake_auth-08#0]
- domains: ag.innovid.com — 1 events; top source ips: 10.1.17.215 (1); top destination ips: 3.82.67.153 (1) [fake_auth-08#0]
- download domains: 5.252.153.241 — 594 events [fake_auth-01#0]
- download domains: master16.teamviewer.com — 21 events [fake_auth-01#0]
- download domains: msedge.b.tlu.dl.delivery.mp.microsoft.com — 4 events [fake_auth-01#0]
- download domains: download.windowsupdate.com — 3 events [fake_auth-01#0]
- file types: other — 1813 events [fake_auth-01#7]
- file types: exe — 5 events [fake_auth-01#7]
- download sources: 10.1.17.215 — 1823 events [fake_auth-01#7]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- http requests: 10.1.17.215 -> 185.188.32.26:80 : /din.aspx?s=91930165&id=0&client=DynGate&p=10000002 — 2 events [fake_auth-01#4]
- file transfers: 1308 matching events [fake_auth-01#4]
- file transfers > transfer details: file_transfer — 617 events [fake_auth-01#4]
- file transfers > transfer details: 10.1.17.215 -> 13.107.21.239:443 : fuid: F1NJjy3oFAIPDAJDF3 — 1 events [fake_auth-01#4]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. Derived: internal client 10.1.17.215 ranks #1 by external connections (1823 events, 119 distinct external destinations). Most-contacted external IP: 5.252.153.241 (1196 connections). [fake_auth-09#0]
2. Derived: Kerberos identity of 10.1.17.215: hostname(s) desktop-l8c5gsj; human user account(s) shutchenson. [fake_auth-09#0]
3. Derived: Suricata alerts span 2025-01-22 19:00 UTC to 2025-01-22 20:00 UTC; earliest alert hour 2025-01-22 19:00 UTC (10 alerts). [fake_auth-09#0]
4. Not established from the available artifacts.
5. hostnames: desktop-l8c5gsj — 1 events; source ips: 10.1.17.215 (1) [fake_auth-05#0]
6. client accounts: shutchenson — 11 events; source ips: 10.1.17.215 (11) [fake_auth-03#0]
7. client accounts: DESKTOP-L8C5GSJ$ — 10 events; source ips: 10.1.17.215 (10) [fake_auth-03#0]
8. Not established from the available artifacts.
