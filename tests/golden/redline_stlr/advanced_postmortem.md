# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.7.10.47 ranks #1 by external connections (55 events, 20 distinct external destinations). Most-contacted external IP: 195.161.114.3 (8 connections). [redline_stlr-08#0]
- Derived: Kerberos identity of 10.7.10.47: hostname(s) desktop-9pea63h; human user account(s) rwalters. [redline_stlr-08#0]
- Derived: Suricata alerts span 2023-07-10 22:00 UTC to 2023-07-10 22:00 UTC; earliest alert hour 2023-07-10 22:00 UTC (7 alerts). [redline_stlr-08#0]
- Derived: destinations of high-severity alerts: 194.26.135.119 (4), 195.161.114.3 (1). [redline_stlr-08#0]
- client accounts: DESKTOP-9PEA63H$ — 12 events; source ips: 10.7.10.47 (12) [redline_stlr-03#0]
- client accounts: desktop-9pea63h$ — 8 events; source ips: 10.7.10.47 (8) [redline_stlr-03#0]
- client accounts: rwalters — 6 events; source ips: 10.7.10.47 (6) [redline_stlr-03#0]
- source clients: 10.7.10.47 — 55 events; external destinations=20; top destinations: 195.161.114.3 (8), 92.118.151.9 (5), 204.79.197.200 (5), 13.107.21.200 (3), 20.42.65.88 (3); 31 further events in other values [redline_stlr-02#0]
- full services: krb_tcp — 26 events; source ips: 10.7.10.47 (26) [redline_stlr-04#0]
- full services: krbtgt/COOLWEATHERCOAT.COM — 13 events; source ips: 10.7.10.47 (13) [redline_stlr-04#0]
- full services: LDAP/WIN-S3WT6LGQFVX.coolweathercoat.com/coolweathercoat.com — 2 events; source ips: 10.7.10.47 (2) [redline_stlr-04#0]
- full services: krbtgt/coolweathercoat.com — 2 events; source ips: 10.7.10.47 (2) [redline_stlr-04#0]
- full services: DESKTOP-9PEA63H$ — 1 events; source ips: 10.7.10.47 (1) [redline_stlr-04#1]
- full services: LDAP/WIN-S3WT6LGQFVX.coolweathercoat.com — 1 events; source ips: 10.7.10.47 (1) [redline_stlr-04#1]
- download domains: guiatelefonos.com — 1 events [redline_stlr-01#4]
- file types: other — 55 events [redline_stlr-01#4]

## Timeline

- 2023-07-10 22:00 UTC — alert timeline: 7 events; earliest alert hour [redline_stlr-06#3, redline_stlr-08#0]

## Detection: IDS Alerts

- alert signatures: ET INFO Windows Powershell User-Agent Usage — 2 events [redline_stlr-06#0]
- alert signatures: ET MALWARE Redline Stealer/MetaStealer Family TCP CnC Activity - MSValue (Outbound) — 2 events [redline_stlr-06#0]
- alert signatures: ET INFO Microsoft net.tcp Connection Initialization Activity — 1 events [redline_stlr-06#0]
- alert signatures: ET MALWARE NUMOZYLOD CnC Checkin M2 — 1 events [redline_stlr-06#0]
- alert signatures: ET MALWARE [ANY.RUN] RedLine Stealer/MetaStealer Family Related (MC-NMF Authorization) — 1 events [redline_stlr-06#1]
- high severity alerts: 5 matching events [redline_stlr-06#1]
- high severity alerts > high severity  destinations: 194.26.135.119 — 4 events [redline_stlr-06#1]
- high severity alerts > high severity  destinations: 195.161.114.3 — 1 events [redline_stlr-06#1]
- high severity alerts > high severity sources: 10.7.10.47 — 5 events [redline_stlr-06#3]
- file transfers: 10 matching events [redline_stlr-01#0]
- file transfers > transfer details: file_transfer — 3 events [redline_stlr-01#0]
- file transfers > transfer details: 10.7.10.47 -> 13.107.21.200:443 : fuid: FRHMTH2cDhvYsVZt86 — 1 events [redline_stlr-01#0]
- file transfers > transfer details: 10.7.10.47 -> 195.161.114.3:80 : fuid: FHuY9W2Rb2X336jwT5 — 1 events [redline_stlr-01#0]

## Initial Infection Indicators

- http requests: 10.7.10.47 -> 195.161.114.3:80 : /?status=install — 1 events [redline_stlr-01#3]
- http requests: 10.7.10.47 -> 195.161.114.3:80 : /?status=start&av=Windows Defender — 1 events [redline_stlr-01#3]
- http requests: 10.7.10.47 -> 92.118.151.9:80 : /data/czx.jpg — 1 events [redline_stlr-01#3]
- download domains: 623start.site — 2 events [redline_stlr-01#3]
- file transfers > transfer details: 10.7.10.47 -> 92.118.151.9:80 : fuid: FaY0uO3uabhmTxqaQc — 1 events [redline_stlr-01#2]
- download sources: 10.7.10.47 — 55 events [redline_stlr-01#2]
- http requests: no_http_uri — 49 events [redline_stlr-01#2]
- http requests: 10.7.10.47 -> 195.161.114.3:80 : /?status=start&av=Windows%20Defender — 3 events [redline_stlr-01#2]
- domains: a6d04e539d712e4ef920661af4825316.clo.footprintdns.com — 1 events; top source ips: 10.7.10.47 (1); top destination ips: 13.107.6.163 (1) [redline_stlr-07#0]
- domains: guiatelefonos.com — 1 events; top source ips: 10.7.10.47 (1); top destination ips: 92.118.151.9 (1) [redline_stlr-07#0]
- domains: static-ecst.licdn.com — 1 events; top source ips: 10.7.10.47 (1); top destination ips: 152.199.24.163 (1) [redline_stlr-07#0]
- file transfers > transfer details: 10.7.10.47 -> 20.42.65.88:443 : fuid: Fsp3YN3nMVyuIp9sDk — 1 events [redline_stlr-01#1]
- file transfers > transfer details: 10.7.10.47 -> 204.79.197.200:443 : fuid: FPRwDt3bWAo6siQc7j — 1 events [redline_stlr-01#1]
- file transfers > transfer details: 10.7.10.47 -> 204.79.197.203:443 : fuid: FPQK3hfd9HvSkrIl1 — 1 events [redline_stlr-01#1]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [redline_stlr-09#0]
2. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [redline_stlr-09#0]
3. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [redline_stlr-09#0]
4. Not established from the available artifacts.
5. Derived: Kerberos identity of 10.7.10.47: hostname(s) desktop-9pea63h; human user account(s) rwalters. [redline_stlr-08#0]
6. Derived: Suricata alerts span 2023-07-10 22:00 UTC to 2023-07-10 22:00 UTC; earliest alert hour 2023-07-10 22:00 UTC (7 alerts). [redline_stlr-08#0]
7. Derived: destinations of high-severity alerts: 194.26.135.119 (4), 195.161.114.3 (1). [redline_stlr-08#0]
8. Not established from the available artifacts.
