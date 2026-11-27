# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.10.22.156 ranks #1 by external connections (761 events, 80 distinct external destinations). Most-contacted external IP: 201.137.10.225 (70 connections). [oct21isc-09#0]
- Derived: Kerberos identity of 10.10.22.156: hostname(s) desktop-cfa3367; human user account(s) agnes.warren. [oct21isc-09#0]
- Derived: internal client 10.10.22.158 ranks #2 by external connections (315 events, 45 distinct external destinations). Most-contacted external IP: 194.15.112.173 (65 connections). [oct21isc-09#0]
- Derived: Kerberos identity of 10.10.22.158: hostname(s) desktop-87wce26; human user account(s) kevin.henderson. [oct21isc-09#0]
- client accounts: marcus.cobb — 6 events; source ips: 10.10.22.157 (6) [oct21isc-03#2]
- client accounts: DESKTOP-87WCE26$ — 13 events; source ips: 10.10.22.158 (13) [oct21isc-03#0]
- client accounts: DESKTOP-CFA3367$ — 11 events; source ips: 10.10.22.156 (11) [oct21isc-03#0]
- client accounts: DESKTOP-NZ875R4$ — 10 events; source ips: 10.10.22.157 (10) [oct21isc-03#0]
- client accounts: desktop-87wce26$ — 8 events; source ips: 10.10.22.158 (8) [oct21isc-03#0]
- client accounts: kevin.henderson — 7 events; source ips: 10.10.22.158 (7) [oct21isc-03#1]
- client accounts: agnes.warren — 6 events; source ips: 10.10.22.156 (6) [oct21isc-03#1]
- client accounts: desktop-cfa3367$ — 6 events; source ips: 10.10.22.156 (6) [oct21isc-03#1]
- client accounts: desktop-nz875r4$ — 6 events; source ips: 10.10.22.157 (6) [oct21isc-03#1]
- Derived: internal client 10.10.22.157 ranks #3 by external connections (88 events, 24 distinct external destinations). Most-contacted external IP: 52.185.211.133 (8 connections). [oct21isc-09#1]
- Derived: Kerberos identity of 10.10.22.157: hostname(s) desktop-nz875r4; human user account(s) marcus.cobb. [oct21isc-09#1]
- Derived: Suricata alerts span 2021-10-22 14:00 UTC to 2021-10-22 16:00 UTC; earliest alert hour 2021-10-22 14:00 UTC (285 alerts). [oct21isc-09#1]
- Derived: destinations of high-severity alerts: 37.0.10.22 (597), 8.8.8.8 (308), 130.61.64.122 (14), 10.10.22.22 (6), 172.67.139.101 (3). [oct21isc-09#1]
- full services: krb_tcp — 76 events; source ips: 10.10.22.158 (29), 10.10.22.156 (24), 10.10.22.157 (23) [oct21isc-04#0]
- full services: krbtgt/ENEMYWATCH.NET — 32 events; source ips: 10.10.22.158 (12), 10.10.22.156 (10), 10.10.22.157 (10) [oct21isc-04#0]
- full services: LDAP/ENEMYWATCH-DC.enemywatch.net/enemywatch.net — 6 events; source ips: 10.10.22.158 (3), 10.10.22.156 (2), 10.10.22.157 (1) [oct21isc-04#0]
- full services: krbtgt/enemywatch.net — 6 events; source ips: 10.10.22.156 (2), 10.10.22.157 (2), 10.10.22.158 (2) [oct21isc-04#0]

## Timeline

- 2021-10-22 14:00 UTC — alert timeline: 285 events; earliest alert hour [oct21isc-06#9, oct21isc-09#1]
- 2021-10-22 15:00 UTC — alert timeline: 728 events [oct21isc-06#9]
- 2021-10-22 16:00 UTC — alert timeline: 38 events [oct21isc-06#9]

## Detection: IDS Alerts

- alert signatures: ET MALWARE VNCStartServer BOT Variant CnC Beacon — 1 events [oct21isc-06#4]
- high severity alerts: 934 matching events [oct21isc-06#4]
- high severity alerts > high severity  destinations: 37.0.10.22 — 597 events [oct21isc-06#4]
- alert signatures: ET MALWARE NanoCore RAT CnC 7 — 597 events [oct21isc-06#0]
- alert signatures: ET DYN_DNS DNS Query to DynDNS Domain *.ddns .net — 308 events [oct21isc-06#0]
- alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 65 events [oct21isc-06#0]
- alert signatures: ET INFO External IP Address Lookup Domain (ipify .org) in TLS SNI — 27 events [oct21isc-06#0]
- high severity alerts > high severity signatures: ET MALWARE NanoCore RAT CnC 7 — 597 events [oct21isc-06#6]
- high severity alerts > high severity signatures: ET HUNTING Observed DNS Query for EmerDNS TLD (.bazar) — 15 events [oct21isc-06#6]
- high severity alerts > high severity signatures: ET RPC DCERPC SVCCTL - Remote Service Control Manager Access — 3 events [oct21isc-06#6]
- high severity alerts > high severity sources: 10.10.22.156 — 8 events [oct21isc-06#9]
- high severity alerts > high severity signatures: ET INFO IP Check Domain (myexternalip .com in TLS SNI) — 1 events [oct21isc-06#8]
- high severity alerts > high severity sources: 10.10.22.157 — 905 events [oct21isc-06#8]
- high severity alerts > high severity sources: 10.10.22.158 — 21 events [oct21isc-06#8]
- high severity alerts > high severity signatures: ET DNS Query for .cc TLD — 2 events [oct21isc-06#7]
- high severity alerts > high severity signatures: ET HUNTING Request to .TOP Domain with Minimal Headers — 2 events [oct21isc-06#7]

## Initial Infection Indicators

- download sources: 10.10.22.157 — 88 events [oct21isc-01#8]
- domains: www.openssl.org — 1 events; top source ips: 10.10.22.156 (1); top destination ips: 72.247.207.22 (1) [oct21isc-08#4]
- download domains: 190.14.37.244 — 1 events [oct21isc-01#1]
- download domains: 194.36.191.35 — 1 events [oct21isc-01#1]
- download domains: www.kqzyfj.com — 1 events [oct21isc-01#1]
- http requests: no_http_uri — 1145 events [oct21isc-01#1]
- http requests: 10.10.22.158 -> 172.67.139.101:80 : /034g100/index.php — 4 events [oct21isc-01#2]
- http requests: 10.10.22.156 -> 104.94.77.31:80 : / — 2 events [oct21isc-01#2]
- http requests: 10.10.22.156 -> 178.23.190.8:80 : /44491.6090605324.dat — 1 events [oct21isc-01#2]
- http requests: 10.10.22.156 -> 190.14.37.244:80 : /44491.6090605324.dat — 1 events [oct21isc-01#2]
- http requests: 10.10.22.156 -> 8.253.156.120:80 : /msdownload/update/v3/static/trustedr/en/pinrulesstl.cab?88af6d736a9e15f4 — 1 events [oct21isc-01#4]
- file transfers: 93 matching events [oct21isc-01#4]
- file transfers > transfer details: file_transfer — 6 events [oct21isc-01#4]
- file transfers > transfer details: 10.10.22.156 -> 104.208.16.88:443 : fuid: Fjxw103NNNaUXuRei — 1 events [oct21isc-01#4]
- http requests: 10.10.22.156 -> 194.36.191.35:80 : /44491.6090605324.dat — 1 events [oct21isc-01#3]
- http requests: 10.10.22.156 -> 8.253.156.120:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?29290d2fe073e937 — 1 events [oct21isc-01#3]
- http requests: 10.10.22.156 -> 8.253.156.120:80 : /msdownload/update/v3/static/trustedr/en/disallowedcertstl.cab?84945a395c830399 — 1 events [oct21isc-01#3]

## Command-and-Control and Network Activity

- alert signatures: ET INFO External IP Lookup Domain (ipify .org) in DNS Lookup — 10 events [oct21isc-06#1]
- alert signatures: ET INFO NTLM Session Setup Request - Auth — 5 events [oct21isc-06#1]
- alert signatures: ET INFO HTTP Request to a *.top domain — 1 events [oct21isc-06#3]
- alert signatures: ET INFO Observed DNS Query to .biz TLD — 1 events [oct21isc-06#3]

## Impact Assessment

- source clients: 10.10.22.156 — 761 events; external destinations=80; top destinations: 201.137.10.225 (70), 207.246.112.221 (34), 73.52.50.32 (32), 209.210.95.228 (32), 54.243.29.214 (30); 563 further events in other values [oct21isc-02#0]
- source clients: 10.10.22.158 — 315 events; external destinations=45; top destinations: 194.15.112.173 (65), 204.79.197.200 (28), 13.107.21.200 (23), 83.223.99.191 (14), 107.161.180.34 (14); 171 further events in other values [oct21isc-02#0]
- source clients: 10.10.22.157 — 88 events; external destinations=24; top destinations: 52.185.211.133 (8), 104.46.162.226 (7), 20.189.173.7 (6), 13.64.180.106 (5), 13.107.21.200 (5); 57 further events in other values [oct21isc-02#0]
- download domains: ctldl.windowsupdate.com — 7 events [oct21isc-01#0]
- download domains: x1.c.lencr.org — 3 events [oct21isc-01#0]
- download domains: sobolpand.top — 2 events [oct21isc-01#0]
- download domains: 178.23.190.8 — 1 events [oct21isc-01#0]

## Root Cause and Evidence Gaps

- file transfers > transfer details: 10.10.22.156 -> 104.208.16.94:443 : fuid: FJxyIt3XkQZYEKg2r4 — 1 events [oct21isc-01#5]
- file transfers > transfer details: 10.10.22.156 -> 140.82.49.12:443 : fuid: Fc7Nl6kEzt63AmJP6 — 1 events [oct21isc-01#5]
- file transfers > transfer details: 10.10.22.156 -> 162.210.220.137:443 : fuid: F3n9EU1Oe7rLUk0jUb — 1 events [oct21isc-01#5]
- file transfers > transfer details: 10.10.22.156 -> 178.23.190.8:80 : file: 44491.6090605324.dat — 1 events [oct21isc-01#5]

## Corrective and Preventive Actions

- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 5 events [oct21isc-06#2]
- alert signatures: ET DNS Query for .cc TLD — 2 events [oct21isc-06#2]

## Answers to Investigation Questions

1. Derived: internal client 10.10.22.156 ranks #1 by external connections (761 events, 80 distinct external destinations). Most-contacted external IP: 201.137.10.225 (70 connections). [oct21isc-09#0]
2. Derived: Kerberos identity of 10.10.22.156: hostname(s) desktop-cfa3367; human user account(s) agnes.warren. [oct21isc-09#0]
3. Derived: internal client 10.10.22.158 ranks #2 by external connections (315 events, 45 distinct external destinations). Most-contacted external IP: 194.15.112.173 (65 connections). [oct21isc-09#0]
4. Not established from the available artifacts.
5. client accounts: marcus.cobb — 6 events; source ips: 10.10.22.157 (6) [oct21isc-03#2]
6. Derived: internal client 10.10.22.157 ranks #3 by external connections (88 events, 24 distinct external destinations). Most-contacted external IP: 52.185.211.133 (8 connections). [oct21isc-09#1]
7. Derived: Kerberos identity of 10.10.22.157: hostname(s) desktop-nz875r4; human user account(s) marcus.cobb. [oct21isc-09#1]
8. Not established from the available artifacts.
