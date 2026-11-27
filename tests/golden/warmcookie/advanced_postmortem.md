# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.8.15.133 ranks #1 by external connections (1570 events, 66 distinct external destinations). Most-contacted external IP: 72.5.43.29 (1235 connections). [warmcookie-08#0]
- Derived: Kerberos identity of 10.8.15.133: hostname(s) desktop-h8alzbv; human user account(s) plucero. [warmcookie-08#0]
- Derived: Suricata alerts span 2024-08-15 00:00 UTC to 2024-08-15 00:00 UTC; earliest alert hour 2024-08-15 00:00 UTC (314 alerts). [warmcookie-08#0]
- Derived: destinations of high-severity alerts: 72.5.43.29 (309), 10.8.15.133 (3). [warmcookie-08#0]
- client accounts: DESKTOP-H8ALZBV$ — 11 events; source ips: 10.8.15.133 (11) [warmcookie-03#0]
- client accounts: plucero — 8 events; source ips: 10.8.15.133 (8) [warmcookie-03#0]
- client accounts: desktop-h8alzbv$ — 6 events; source ips: 10.8.15.133 (6) [warmcookie-03#0]
- full services: ldap/win-jegjix7q9rs.lafontainebleu.org — 1 events; source ips: 10.8.15.133 (1) [warmcookie-04#3]
- full services: ldap/win-jegjix7q9rs.lafontainebleu.org/lafontainebleu.org — 1 events; source ips: 10.8.15.133 (1) [warmcookie-04#3]
- full services: krb_tcp — 25 events; source ips: 10.8.15.133 (25) [warmcookie-04#0]
- full services: krbtgt/LAFONTAINEBLEU.ORG — 10 events; source ips: 10.8.15.133 (10) [warmcookie-04#0]
- full services: LDAP/WIN-JEGJIX7Q9RS.lafontainebleu.org/lafontainebleu.org — 2 events; source ips: 10.8.15.133 (2) [warmcookie-04#0]
- full services: cifs/WIN-JEGJIX7Q9RS.lafontainebleu.org — 2 events; source ips: 10.8.15.133 (2) [warmcookie-04#0]
- source clients: 10.8.15.133 — 1570 events; external destinations=66; top destinations: 72.5.43.29 (1235), 204.79.197.203 (27), 23.220.103.18 (24), 23.33.138.184 (22), 23.220.103.8 (21); 241 further events in other values [warmcookie-02#0]
- full services: krbtgt/lafontainebleu.org — 2 events; source ips: 10.8.15.133 (2) [warmcookie-04#1]
- full services: DESKTOP-H8ALZBV$ — 1 events; source ips: 10.8.15.133 (1) [warmcookie-04#1]
- full services: cifs/WIN-JEGJIX7Q9RS — 1 events; source ips: 10.8.15.133 (1) [warmcookie-04#1]

## Timeline

- 2024-08-15 00:00 UTC — alert timeline: 314 events; earliest alert hour [warmcookie-06#4, warmcookie-08#0]

## Detection: IDS Alerts

- alert signatures: ET MALWARE BadSpace/WarmCookie CnC Activity (GET) M1 — 303 events [warmcookie-06#0]
- alert signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 3 events [warmcookie-06#0]
- alert signatures: ET MALWARE W32/Badspace.Backdoor CnC Activity (POST) — 3 events [warmcookie-06#0]
- alert signatures: ET HUNTING SUSPICIOUS Dotted Quad Host MZ Response — 1 events [warmcookie-06#0]
- high severity alerts > high severity signatures: ET INFO PE EXE or DLL Windows file download HTTP — 1 events [warmcookie-06#3]
- high severity alerts > high severity signatures: ET MALWARE Possible Windows executable sent when remote host claims to send html content — 1 events [warmcookie-06#4]
- high severity alerts > high severity sources: 10.8.15.133 — 309 events [warmcookie-06#4]
- high severity alerts > high severity sources: 72.5.43.29 — 3 events [warmcookie-06#4]
- alert signatures: ET INFO Microsoft Connection Test — 1 events [warmcookie-06#1]
- alert signatures: ET INFO Packed Executable Download — 1 events [warmcookie-06#1]
- high severity alerts: 312 matching events [warmcookie-06#2]
- high severity alerts > high severity  destinations: 72.5.43.29 — 309 events [warmcookie-06#2]
- high severity alerts > high severity  destinations: 10.8.15.133 — 3 events [warmcookie-06#2]

## Initial Infection Indicators

- http requests: 10.8.15.133 -> 23.220.251.208:80 : /assets/Owner/arm/ProcessMAU.txt — 1 events [warmcookie-01#5]
- download domains: 72.5.43.29 — 308 events [warmcookie-01#5]
- download domains: msedge.b.tlu.dl.delivery.mp.microsoft.com — 10 events [warmcookie-01#5]
- download domains: acroipm2.adobe.com — 1 events [warmcookie-01#5]
- http requests: 10.8.15.133 -> 23.205.110.48:80 : /connecttest.txt — 2 events [warmcookie-01#4]
- http requests: 10.8.15.133 -> 72.5.43.29:80 : /data/0f60a3e7baecf2748b1c8183ed37d1e4 — 2 events [warmcookie-01#4]
- http requests: 10.8.15.133 -> 104.21.55.70:80 : /managements?16553a25e45250a41fd5&endeds=MIGpq&JStx=59bf050d37df88a9-ade43358-eaa1220b-0571422b-0f33e6aa150e86bafd0ed4&Ld=9d7502d88d752a27b1d00587309184b5a215 — 1 events [warmcookie-01#4]
- http requests: 10.8.15.133 -> 204.79.197.203:80 : /ocsp/MFQwUjBQME4wTDAJBgUrDgMCGgUABBR2JNtr0JxEvYySpbyBWaqBmealCgQUzhUWO+oCo6Zr2tkr/eWMUr56UKgCEzMAPnPpacmgFoSqVQMAAAA+c+k= — 1 events [warmcookie-01#4]
- http requests: no_http_uri — 942 events [warmcookie-01#3]
- http requests: 10.8.15.133 -> 72.5.43.29:80 : / — 611 events [warmcookie-01#3]
- http requests: 10.8.15.133 -> 199.232.210.172:80 : /filestreamingservice/files/8f2381c2-652d-48a2-86f6-19cb7757f5dc?P1=1724113284&P2=404&P3=2&P4=QwGPFdJVa+Bw71q1beBnqYWdAtr86AnZ79l2/NOX9l1PkiMLSVObKUK4QmaPqxVAgCpCljWyTVtZO9mpmuJNlQ== — 5 events [warmcookie-01#3]
- http requests: 10.8.15.133 -> 199.232.210.172:80 : /filestreamingservice/files/f37dd878-a1b9-4f21-a8c9-65c3dd00f7a6?P1=1724225867&P2=404&P3=2&P4=IaxXE3ikzdIKvQz1E1qPcLRRfyHtwqWgjE0YDO8CsvKt6Jcq94KnSHhjEOc1Vkk62+udS1LrVl+tTvm0Hctz+A== — 5 events [warmcookie-01#3]
- file types: exe — 1 events [warmcookie-01#7]
- download domains: oneocsp.microsoft.com — 1 events [warmcookie-01#6]
- download domains: quote.checkfedexexp.com — 1 events [warmcookie-01#6]
- download domains: www.msftconnecttest.com — 1 events [warmcookie-01#6]
- file types: other — 1569 events [warmcookie-01#6]
- file transfers: 661 matching events [warmcookie-01#0]
- file transfers > transfer details: file_transfer — 313 events [warmcookie-01#0]
- file transfers > transfer details: 10.8.15.133 -> 104.21.55.70:80 : file: Invoice 876597035_003.zip — 1 events [warmcookie-01#0]
- file transfers > transfer details: 10.8.15.133 -> 13.107.21.239:443 : fuid: Fq2eaB3mes5OTBfh11 — 1 events [warmcookie-01#0]

## Command-and-Control and Network Activity

- file transfers > transfer details: 10.8.15.133 -> 20.125.209.212:443 : fuid: FTdK8xWfbfKNOp2Pa — 1 events [warmcookie-01#2]
- file transfers > transfer details: 10.8.15.133 -> 20.189.173.9:443 : fuid: FGIG8s1floME1LLqVj — 1 events [warmcookie-01#2]
- file transfers > transfer details: 10.8.15.133 -> 20.241.44.114:443 : fuid: FNlgaK3cZscpKjdHM2 — 1 events [warmcookie-01#2]
- download sources: 10.8.15.133 — 1570 events [warmcookie-01#2]
- domains: sb.scorecardresearch.com — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 18.160.156.115 (1) [warmcookie-07#2]
- domains: weathermapdata.blob.core.windows.net — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 20.60.228.1 (1) [warmcookie-07#2]
- domains: bzib.nelreports.net — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 23.215.55.139 (1) [warmcookie-07#1]
- domains: default.exp-tas.com — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 13.107.5.93 (1) [warmcookie-07#1]
- domains: ecn-us.dev.virtualearth.net — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 23.43.244.167 (1) [warmcookie-07#1]
- domains: ow1.res.office365.com — 1 events; top source ips: 10.8.15.133 (1); top destination ips: 23.53.13.205 (1) [warmcookie-07#1]

## Impact Assessment



## Root Cause and Evidence Gaps

- file transfers > transfer details: 10.8.15.133 -> 13.85.23.206:443 : fuid: FxGb9x3qQx6uw4IeK3 — 1 events [warmcookie-01#1]
- file transfers > transfer details: 10.8.15.133 -> 199.232.210.172:80 : fuid: FSh8n54COleagDNY7c — 1 events [warmcookie-01#1]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [warmcookie-09#0]
2. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [warmcookie-09#0]
3. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [warmcookie-09#0]
4. Not established from the available artifacts.
5. Derived: Kerberos identity of 10.8.15.133: hostname(s) desktop-h8alzbv; human user account(s) plucero. [warmcookie-08#0]
6. Derived: Suricata alerts span 2024-08-15 00:00 UTC to 2024-08-15 00:00 UTC; earliest alert hour 2024-08-15 00:00 UTC (314 alerts). [warmcookie-08#0]
7. Derived: destinations of high-severity alerts: 72.5.43.29 (309), 10.8.15.133 (3). [warmcookie-08#0]
