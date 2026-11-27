# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.11.26.183 ranks #1 by external connections (472 events, 55 distinct external destinations). Most-contacted external IP: 194.180.191.64 (238 connections). [net_rat-08#0]
- Derived: Kerberos identity of 10.11.26.183: hostname(s) desktop-b8tqk49; human user account(s) oboomwald. [net_rat-08#0]
- Derived: Suricata alerts span 2024-11-26 04:00 UTC to 2024-11-26 05:00 UTC; earliest alert hour 2024-11-26 04:00 UTC (31 alerts). [net_rat-08#0]
- Derived: destinations of high-severity alerts: 194.180.191.64 (58), 104.26.1.231 (1). [net_rat-08#0]
- client accounts: oboomwald — 8 events; source ips: 10.11.26.183 (8) [net_rat-03#0]
- full services: krb_tcp — 8 events; source ips: 10.11.26.183 (8) [net_rat-04#0]
- full services: krbtgt/NEMOTODES.HEALTH — 2 events; source ips: 10.11.26.183 (2) [net_rat-04#0]
- full services: LDAP/NEMOTODES-DC.nemotodes.health/nemotodes.health — 1 events; source ips: 10.11.26.183 (1) [net_rat-04#0]
- full services: cifs/NEMOTODES-DC — 1 events; source ips: 10.11.26.183 (1) [net_rat-04#0]
- source clients: 10.11.26.183 — 472 events; external destinations=55; top destinations: 194.180.191.64 (238), 52.113.194.132 (25), 193.42.38.139 (16), 173.222.49.101 (15), 204.79.197.203 (14); 164 further events in other values [net_rat-02#0]
- full services: cifs/NEMOTODES-DC.nemotodes.health — 1 events; source ips: 10.11.26.183 (1) [net_rat-04#1]
- full services: host/desktop-b8tqk49.nemotodes.health — 1 events; source ips: 10.11.26.183 (1) [net_rat-04#1]
- full services: krbtgt/NEMOTODES — 1 events; source ips: 10.11.26.183 (1) [net_rat-04#1]
- download domains: 194.180.191.64 — 58 events [net_rat-01#0]
- download domains: ctldl.windowsupdate.com — 2 events [net_rat-01#0]
- download domains: acroipm2.adobe.com — 1 events [net_rat-01#0]
- download domains: geo.netsupportsoftware.com — 1 events [net_rat-01#0]

## Timeline

- 2024-11-26 04:00 UTC — alert timeline: 31 events; earliest alert hour [net_rat-06#2, net_rat-08#0]
- 2024-11-26 05:00 UTC — alert timeline: 92 events [net_rat-06#3]

## Detection: IDS Alerts

- alert signatures: ET INFO HTTP traffic on port 443 (POST) — 58 events [net_rat-06#0]
- alert signatures: ET REMOTE_ACCESS NetSupport Remote Admin Checkin — 58 events [net_rat-06#0]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 5 events [net_rat-06#0]
- alert signatures: ET INFO Microsoft Connection Test — 1 events [net_rat-06#0]
- high severity alerts > high severity signatures: ET REMOTE_ACCESS NetSupport GeoLocation Lookup Request — 1 events [net_rat-06#2]
- high severity alerts > high severity sources: 10.11.26.183 — 59 events [net_rat-06#2]
- high severity alerts: 59 matching events [net_rat-06#1]
- high severity alerts > high severity  destinations: 194.180.191.64 — 58 events [net_rat-06#1]
- high severity alerts > high severity  destinations: 104.26.1.231 — 1 events [net_rat-06#1]

## Initial Infection Indicators

- download domains: r10.o.lencr.org — 1 events [net_rat-01#1]
- download domains: www.msftconnecttest.com — 1 events [net_rat-01#1]
- http requests: no_http_uri — 406 events [net_rat-01#1]
- http requests: 10.11.26.183 -> 194.180.191.64:443 : http://194.180.191.64/fakeurl.htm — 58 events [net_rat-01#1]
- http requests: 10.11.26.183 -> 104.117.247.184:80 : /connecttest.txt — 2 events [net_rat-01#2]
- http requests: 10.11.26.183 -> 104.117.247.99:80 : /MFMwUTBPME0wSzAJBgUrDgMCGgUABBRpD+QVZ+1vf7U0RGQGBm8JZwdxcgQUdKR2KRcYVIUxN75n5gZYwLzFBXICEgRSsdGCXQJklJZNbHi669GH4A== — 1 events [net_rat-01#2]
- http requests: 10.11.26.183 -> 104.26.1.231:80 : /location/loca.asp — 1 events [net_rat-01#2]
- http requests: 10.11.26.183 -> 23.53.127.105:80 : /assets/Owner/arm/ProcessMAU.txt — 1 events [net_rat-01#3]
- http requests: 10.11.26.183 -> 23.53.127.200:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?778a0928305752e9 — 1 events [net_rat-01#3]
- http requests: 10.11.26.183 -> 23.53.127.200:80 : /msdownload/update/v3/static/trustedr/en/disallowedcertstl.cab?ce02e9976e1239e1 — 1 events [net_rat-01#3]
- file transfers: 157 matching events [net_rat-01#3]
- file transfers > transfer details: 10.11.26.183 -> 173.222.49.101:443 : fuid: Fcjb5f3T8uL7OfxJE7 — 1 events [net_rat-01#6]
- file types: other — 472 events [net_rat-01#6]
- download sources: 10.11.26.183 — 472 events [net_rat-01#6]
- file transfers > transfer details: file_transfer — 62 events [net_rat-01#4]
- file transfers > transfer details: 10.11.26.183 -> 104.117.247.184:80 : fuid: FS19Ny2ccXfItSAHY5 — 1 events [net_rat-01#4]
- file transfers > transfer details: 10.11.26.183 -> 104.117.247.99:80 : fuid: FY81pL3SoAHblZVNm9 — 1 events [net_rat-01#4]
- file transfers > transfer details: 10.11.26.183 -> 104.26.1.231:80 : fuid: FrDUHo17nOjSeXu4Xi — 1 events [net_rat-01#4]

## Command-and-Control and Network Activity

- domains: modandcrackedapk.com — 8 events; top source ips: 10.11.26.183 (8); top destination ips: 193.42.38.139 (8) [net_rat-07#0]
- domains: fonts.gstatic.com — 4 events; top source ips: 10.11.26.183 (4); top destination ips: 142.250.138.94 (4) [net_rat-07#0]
- domains: classicgrand.com — 2 events; top source ips: 10.11.26.183 (2); top destination ips: 213.246.109.5 (2) [net_rat-07#0]
- domains: confirmsubscription.com — 2 events; top source ips: 10.11.26.183 (2); top destination ips: 13.56.30.207 (1), 52.8.34.0 (1) [net_rat-07#0]
- domains: default.exp-tas.com — 2 events; top source ips: 10.11.26.183 (2); top destination ips: 13.107.5.93 (2) [net_rat-07#1]
- domains: code.jquery.com — 1 events; top source ips: 10.11.26.183 (1); top destination ips: 151.101.66.137 (1) [net_rat-07#1]
- domains: css.createsend1.com — 1 events; top source ips: 10.11.26.183 (1); top destination ips: 18.160.156.103 (1) [net_rat-07#1]
- domains: fa000000002.resources.office.net — 1 events; top source ips: 10.11.26.183 (1); top destination ips: 173.222.49.101 (1) [net_rat-07#1]

## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [net_rat-09#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [net_rat-09#0]
3. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [net_rat-09#0]
4. Not established from the available artifacts.
5. Derived: internal client 10.11.26.183 ranks #1 by external connections (472 events, 55 distinct external destinations). Most-contacted external IP: 194.180.191.64 (238 connections). [net_rat-08#0]
6. Derived: Kerberos identity of 10.11.26.183: hostname(s) desktop-b8tqk49; human user account(s) oboomwald. [net_rat-08#0]
7. Derived: Suricata alerts span 2024-11-26 04:00 UTC to 2024-11-26 05:00 UTC; earliest alert hour 2024-11-26 04:00 UTC (31 alerts). [net_rat-08#0]
