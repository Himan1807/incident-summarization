# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.4.19.136 ranks #1 by external connections (841 events, 105 distinct external destinations). Most-contacted external IP: 217.199.121.56 (144 connections). [iced_id-08#0]
- Derived: Kerberos identity of 10.4.19.136: hostname(s) desktop-sff9ljf; human user account(s) csilva. [iced_id-08#0]
- Derived: internal client 10.4.19.138 ranks #2 by external connections (522 events, 100 distinct external destinations). Most-contacted external IP: 204.79.197.200 (42 connections). [iced_id-08#0]
- Derived: Kerberos identity of 10.4.19.138: hostname(s) desktop-retp4bu; human user account(s) irichardson. [iced_id-08#0]
- client accounts: DESKTOP-JAL4D68$ — 3 events; source ips: 10.4.19.143 (3) [iced_id-03#1]
- client accounts: DESKTOP-RETP4BU$ — 22 events; source ips: 10.4.19.138 (22) [iced_id-03#0]
- client accounts: irichardson — 14 events; source ips: 10.4.19.138 (14) [iced_id-03#0]
- client accounts: csilva — 12 events; source ips: 10.4.19.136 (12) [iced_id-03#0]
- client accounts: desktop-retp4bu$ — 12 events; source ips: 10.4.19.138 (12) [iced_id-03#0]
- full services: ldap/WIN-GP4JHCK2JMV.boogienights.live — 1 events; source ips: 10.4.19.136 (1) [iced_id-04#4]
- hostnames: desktop-retp4bu — 2 events; source ips: 10.4.19.138 (2) [iced_id-05#0]
- hostnames: desktop-sff9ljf — 1 events; source ips: 10.4.19.136 (1) [iced_id-05#0]
- direct ip connections: 20.54.24.231 — 5 events [iced_id-07#8]
- domains: skansnekssky.com — 69 events [iced_id-07#8]
- domains: ecn.dev.virtualearth.net — 7 events [iced_id-07#8]
- domains: askamoshopsi.com — 3 events [iced_id-07#8]

## Timeline

- 2023-04-19 15:00 UTC — alert timeline: 19 events; earliest alert hour [iced_id-06#4, iced_id-08#1]
- 2023-04-19 16:00 UTC — alert timeline: 3 events [iced_id-06#4]
- 2023-04-19 17:00 UTC — alert timeline: 10 events [iced_id-06#4]
- 2023-04-19 18:00 UTC — alert timeline: 0 events [iced_id-06#4]
- 2023-04-19 19:00 UTC — alert timeline: 0 events [iced_id-06#5]
- 2023-04-19 20:00 UTC — alert timeline: 1 events [iced_id-06#5]

## Detection: IDS Alerts

- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 11 events [iced_id-06#0]
- alert signatures: ET USER_AGENTS Microsoft Device Metadata Retrieval Client User-Agent — 10 events [iced_id-06#0]
- alert signatures: ET INFO OpenSSL Demo CA - Internet Widgits Pty (O) — 4 events [iced_id-06#0]
- alert signatures: ET INFO Windows OS Submitting USB Metadata to Microsoft — 2 events [iced_id-06#0]
- alert signatures: ET MALWARE IcedID CnC Domain in DNS Lookup (askamoshopsi .com) — 2 events [iced_id-06#1]
- alert signatures: ET MALWARE Win32/IcedID Request Cookie — 1 events [iced_id-06#1]
- high severity alerts: 6 matching events [iced_id-06#2]
- high severity alerts > high severity  destinations: 10.4.19.19 — 4 events [iced_id-06#2]
- high severity alerts > high severity  destinations: 192.153.57.233 — 2 events [iced_id-06#2]
- high severity alerts > high severity signatures: ET MALWARE IcedID CnC Domain in DNS Lookup (skigimeetroc .com) — 2 events [iced_id-06#3]
- high severity alerts > high severity signatures: ET MALWARE Win32/IcedID Requesting Encoded Binary M4 — 1 events [iced_id-06#3]
- high severity alerts > high severity sources: 10.4.19.136 — 6 events [iced_id-06#3]

## Initial Infection Indicators

- download domains: 80.77.25.175 — 1 events [iced_id-01#2]
- download domains: adl.windows.com — 1 events [iced_id-01#2]
- http requests: no_http_uri — 1267 events [iced_id-01#2]
- http requests: 10.4.19.136 -> 209.197.3.8:80 : /filestreamingservice/files/2132f61f-f790-4ae6-a355-8cf9a1533800?P1=1682016707&P2=404&P3=2&P4=bPmGMPdgNR86eaOhheHLplWDz2oULkUHk5GXOutBN9Vni2X4wR4KYGXEa29Eei02Ovi2ehAO0li/ToenRewipg== — 11 events [iced_id-01#2]
- http raw ip requests: 1 matching events [iced_id-07#0]
- http raw ip requests > raw ip hosts: 80.77.25.175 — 1 events [iced_id-07#0]
- http raw ip requests > raw ip hosts 80.77.25.175 > uris: /main.php — 1 events; methods: GET (1) [iced_id-07#0]
- direct ip connections: 217.199.121.56 — 75 events [iced_id-07#0]
- domains: spakernakurs.com — 1 events [iced_id-07#11]
- http requests: 10.4.19.136 -> 23.36.63.240:80 : /fwlink/?LinkID=252669&clcid=0x409 — 4 events [iced_id-01#4]
- http requests: 10.4.19.138 -> 23.214.44.116:80 : / — 4 events [iced_id-01#4]
- http requests: 10.4.19.136 -> 192.153.57.233:80 : / — 3 events [iced_id-01#4]
- http requests: 10.4.19.136 -> 209.197.3.8:80 : /filestreamingservice/files/b22f5f18-f7ea-4290-929d-b13c03908334?P1=1682016707&P2=404&P3=2&P4=m8Pa+tI9vb17zDTiBh0mhF3mdLE8FezjFtavTuBrGO0CS37hIRfK+rSm/ZAwuaj+611u9Nam8/OJ+PRiD/H5rA== — 3 events [iced_id-01#4]
- http requests: 10.4.19.136 -> 23.218.232.178:80 : /filestreamingservice/files/c78f9967-7a8c-44b0-ad94-732b63c89638?P1=1682016707&P2=404&P3=2&P4=Jn3RneMfcL1l4h5itf0+XiXmrCmKvBJA0/czzgSgmyhRVLQc7o0mGmYkdhDiFN1sHja45XP5x5jIEs8pTaQ28Q== — 11 events [iced_id-01#3]
- http requests: 10.4.19.136 -> 23.218.232.178:80 : /filestreamingservice/files/f08b21db-8a96-416f-86dc-4301cb9925a1?P1=1682019049&P2=404&P3=2&P4=dPjdSzDYVq47FC0+zqUWWL3Q4oux7Brwx/PazDTq1ffiI/E6kS93ETT/uG3V3i8/7PoI0XbOYAhyuQpwYS24ag== — 10 events [iced_id-01#3]
- http requests: 10.4.19.138 -> 23.218.232.178:80 : /filestreamingservice/files/f08b21db-8a96-416f-86dc-4301cb9925a1?P1=1682020183&P2=404&P3=2&P4=PTBatu4SG0o2AMBfGJ5N+T3VeLSSbR97blFbgMhM8qmvlPv+4cqkEtu7g89BIzfgPL7u6d5Hr7TzkjQy8vB1Jg== — 10 events [iced_id-01#3]
- http requests: 10.4.19.136 -> 20.231.121.79:80 : /metadata.svc — 5 events [iced_id-01#3]

## Command-and-Control and Network Activity

- direct ip connections: 173.223.109.212 — 16 events [iced_id-07#2]
- direct ip connections: 209.197.3.8 — 13 events [iced_id-07#2]
- direct ip connections: 20.231.121.79 — 12 events [iced_id-07#2]
- direct ip connections: 204.79.197.239 — 12 events [iced_id-07#2]
- direct ip connections: 20.54.25.4 — 11 events [iced_id-07#3]
- direct ip connections: 23.218.232.178 — 11 events [iced_id-07#3]
- direct ip connections: 20.242.220.11 — 10 events [iced_id-07#3]
- direct ip connections: 23.37.112.211 — 10 events [iced_id-07#3]
- source clients: 10.4.19.136 — 841 events; external destinations=105; top destinations: 217.199.121.56 (144), 204.79.197.203 (91), 51.104.167.186 (55), 23.218.232.178 (32), 20.231.121.79 (24); 495 further events in other values [iced_id-02#0]
- source clients: 10.4.19.138 — 522 events; external destinations=100; top destinations: 204.79.197.200 (42), 173.223.109.212 (30), 40.83.247.108 (19), 20.242.220.11 (15), 52.185.211.133 (13); 403 further events in other values [iced_id-02#0]
- direct ip connections: 23.36.63.240 — 8 events [iced_id-07#5]
- direct ip connections: 52.113.194.132 — 8 events [iced_id-07#5]
- direct ip connections: 13.89.179.10 — 7 events [iced_id-07#5]
- direct ip connections: 104.168.53.18 — 6 events [iced_id-07#5]
- direct ip connections: 204.79.197.203 — 57 events [iced_id-07#1]
- direct ip connections: 204.79.197.200 — 29 events [iced_id-07#1]
- direct ip connections: 40.83.247.108 — 29 events [iced_id-07#1]
- direct ip connections: 51.104.167.186 — 25 events [iced_id-07#1]

## Impact Assessment

- Derived: Suricata alerts span 2023-04-19 15:00 UTC to 2023-04-19 20:00 UTC; earliest alert hour 2023-04-19 15:00 UTC (19 alerts). [iced_id-08#1]
- Derived: destinations of high-severity alerts: 10.4.19.19 (4), 192.153.57.233 (2). [iced_id-08#1]
- download domains: msedge.b.tlu.dl.delivery.mp.microsoft.com — 47 events [iced_id-01#0]
- download domains: ctldl.windowsupdate.com — 19 events [iced_id-01#0]
- download domains: dmd.metaservices.microsoft.com — 5 events [iced_id-01#0]
- download domains: go.microsoft.com — 5 events [iced_id-01#0]
- download domains: acroipm2.adobe.com — 4 events [iced_id-01#1]
- download domains: x1.c.lencr.org — 4 events [iced_id-01#1]
- download domains: 11.au.download.windowsupdate.com — 2 events [iced_id-01#1]
- download domains: store-images.s-microsoft.com — 2 events [iced_id-01#1]

## Root Cause and Evidence Gaps

- file transfers: 253 matching events [iced_id-01#5]
- file transfers > transfer details: file_transfer — 30 events [iced_id-01#5]
- file transfers > transfer details: 10.4.19.136 -> 104.126.78.161:443 : fuid: FkJ41S2aV2mtdHFq8h — 1 events [iced_id-01#5]
- file transfers > transfer details: 10.4.19.136 -> 104.168.53.18:443 : fuid: FSCOa7uWpkNe7B9yf — 1 events [iced_id-01#5]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. Query 'suspicious certificates' returned no aggregation results (shards failed: 1 of 92). This evidence is UNAVAILABLE; it is not evidence that nothing exists. [iced_id-09#0]
2. client accounts: DESKTOP-JAL4D68$ — 3 events; source ips: 10.4.19.143 (3) [iced_id-03#1]
3. Derived: internal client 10.4.19.136 ranks #1 by external connections (841 events, 105 distinct external destinations). Most-contacted external IP: 217.199.121.56 (144 connections). [iced_id-08#0]
4. Not established from the available artifacts.
5. Derived: internal client 10.4.19.138 ranks #2 by external connections (522 events, 100 distinct external destinations). Most-contacted external IP: 204.79.197.200 (42 connections). [iced_id-08#0]
6. Derived: Kerberos identity of 10.4.19.138: hostname(s) desktop-retp4bu; human user account(s) irichardson. [iced_id-08#0]
7. Derived: Suricata alerts span 2023-04-19 15:00 UTC to 2023-04-19 20:00 UTC; earliest alert hour 2023-04-19 15:00 UTC (19 alerts). [iced_id-08#1]
8. Not established from the available artifacts.
