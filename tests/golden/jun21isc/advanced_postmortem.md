# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.6.15.119 ranks #1 by external connections (43437 events, 124 distinct external destinations). Most-contacted external IP: 65.60.35.141 (42522 connections). [jun21isc-09#0]
- Derived: Kerberos identity of 10.6.15.119: hostname(s) desktop-niee9lp; human user account(s) tommy.vega. [jun21isc-09#0]
- Derived: internal client 10.6.15.93 ranks #2 by external connections (376 events, 65 distinct external destinations). Most-contacted external IP: 23.47.49.179 (61 connections). [jun21isc-09#0]
- Derived: Kerberos identity of 10.6.15.93: hostname(s) dekstop-a1ctjvy; human user account(s) raquel.anderson. [jun21isc-09#0]
- client accounts: desktop-ys6fz2g$ — 4 events; source ips: 10.6.15.187 (4) [jun21isc-03#2]
- client accounts: horace.maddox — 6 events; source ips: 10.6.15.187 (6) [jun21isc-03#1]
- client accounts: raquel.anderson — 6 events; source ips: 10.6.15.93 (6) [jun21isc-03#1]
- client accounts: dekstop-a1ctjvy$ — 4 events; source ips: 10.6.15.93 (4) [jun21isc-03#1]
- client accounts: desktop-niee9lp$ — 4 events; source ips: 10.6.15.119 (4) [jun21isc-03#1]
- client accounts: tommy.vega — 13 events; source ips: 10.6.15.119 (13) [jun21isc-03#0]
- client accounts: DEKSTOP-A1CTJVY$ — 10 events; source ips: 10.6.15.93 (10) [jun21isc-03#0]
- client accounts: DESKTOP-NIEE9LP$ — 10 events; source ips: 10.6.15.119 (10) [jun21isc-03#0]
- client accounts: DESKTOP-YS6FZ2G$ — 10 events; source ips: 10.6.15.187 (10) [jun21isc-03#0]
- Derived: internal client 10.6.15.187 ranks #3 by external connections (365 events, 75 distinct external destinations). Most-contacted external IP: 52.183.220.149 (18 connections). [jun21isc-09#1]
- Derived: Kerberos identity of 10.6.15.187: hostname(s) desktop-ys6fz2g; human user account(s) horace.maddox. [jun21isc-09#1]
- Derived: Suricata alerts span 2021-06-16 14:00 UTC to 2021-06-16 17:00 UTC; earliest alert hour 2021-06-16 14:00 UTC (1699 alerts). [jun21isc-09#1]
- Derived: destinations of high-severity alerts: 65.60.35.141 (14155), 194.226.60.15 (78), 185.66.15.228 (2), 50.19.92.227 (1), 54.225.78.40 (1). [jun21isc-09#1]
- hostnames: desktop-niee9lp — 2 events; source ips: 10.6.15.119 (2) [jun21isc-05#0]
- hostnames: dekstop-a1ctjvy — 1 events; source ips: 10.6.15.93 (1) [jun21isc-05#0]
- hostnames: desktop-ys6fz2g — 1 events; source ips: 10.6.15.187 (1) [jun21isc-05#0]

## Timeline

- 2021-06-16 14:00 UTC — alert timeline: 1699 events; earliest alert hour [jun21isc-06#7, jun21isc-09#1]
- 2021-06-16 15:00 UTC — alert timeline: 5715 events [jun21isc-06#7]
- 2021-06-16 16:00 UTC — alert timeline: 5624 events [jun21isc-06#8]
- 2021-06-16 17:00 UTC — alert timeline: 1243 events [jun21isc-06#8]

## Detection: IDS Alerts

- alert signatures: ET MALWARE Cobalt Strike Beacon Observed — 14137 events [jun21isc-06#0]
- alert signatures: ET MALWARE Tordal/Hancitor/Chanitor Checkin — 78 events [jun21isc-06#0]
- alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 25 events [jun21isc-06#0]
- alert signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 9 events [jun21isc-06#0]
- high severity alerts > high severity signatures: ET INFO HTTP traffic on port 443 (POST) — 9 events [jun21isc-06#5]
- alert signatures: ET INFO Packed Executable Download — 1 events [jun21isc-06#3]
- alert signatures: ET MALWARE AgentTesla Exfil Via SMTP — 1 events [jun21isc-06#3]
- high severity alerts: 14238 matching events [jun21isc-06#3]
- high severity alerts > high severity  destinations: 65.60.35.141 — 14155 events [jun21isc-06#3]
- alert signatures: ET INFO External IP Lookup Domain (ipify .org) in DNS Lookup — 2 events [jun21isc-06#2]
- alert signatures: ET MALWARE Win32/Ficker Stealer Activity M3 — 2 events [jun21isc-06#2]
- alert signatures: ET INFO External IP Lookup (ipify .org) — 1 events [jun21isc-06#2]
- alert signatures: ET INFO External IP Lookup api.ipify.org — 1 events [jun21isc-06#2]
- high severity alerts > high severity sources: 10.6.15.119 — 14237 events [jun21isc-06#7]
- high severity alerts > high severity sources: 10.6.15.93 — 1 events [jun21isc-06#7]

## Initial Infection Indicators

- download domains: ctldl.windowsupdate.com — 12 events [jun21isc-01#1]
- download domains: au.download.windowsupdate.com — 6 events [jun21isc-01#1]
- download domains: 2.au.download.windowsupdate.com — 4 events [jun21isc-01#1]
- download domains: 9.au.download.windowsupdate.com — 3 events [jun21isc-01#1]
- download domains: 65.60.35.141:443 — 13991 events [jun21isc-01#0]
- download domains: 65.60.35.141 — 155 events [jun21isc-01#0]
- download domains: hadevatjulps.com — 78 events [jun21isc-01#0]
- download domains: download.windowsupdate.com — 48 events [jun21isc-01#0]
- http requests: 10.6.15.119 -> 54.225.78.40:80 : /?format=xml — 2 events [jun21isc-01#6]
- http requests: 10.6.15.187 -> 205.185.216.10:80 : /c/msdownload/update/software/defu/2021/06/am_delta_patch_1.341.846.0_64568a48100a64111aefee77d2dbd189a20c751e.exe — 2 events [jun21isc-01#6]
- file transfers: 565 matching events [jun21isc-01#6]
- file transfers > transfer details: file_transfer — 165 events [jun21isc-01#6]
- http requests: 10.6.15.119 -> 65.60.35.141:443 : /g.pixel — 27966 events [jun21isc-01#4]
- http requests: no_http_uri — 15725 events [jun21isc-01#4]
- http requests: 10.6.15.119 -> 65.60.35.141:80 : /pixel — 310 events [jun21isc-01#4]
- http requests: 10.6.15.119 -> 194.226.60.15:80 : /8/forum.php — 78 events [jun21isc-01#4]
- download domains: srand04rf.ru — 3 events [jun21isc-01#2]
- download domains: ststephenskisugu.church — 3 events [jun21isc-01#2]
- download domains: api.ipify.org — 2 events [jun21isc-01#2]
- download domains: ocsp.digicert.com — 2 events [jun21isc-01#2]
- download sources: 10.6.15.119 — 43437 events [jun21isc-01#10]
- download sources: 10.6.15.93 — 376 events [jun21isc-01#10]
- download sources: 10.6.15.187 — 365 events [jun21isc-01#10]

## Command-and-Control and Network Activity

- source clients: 10.6.15.119 — 43437 events; external destinations=124; top destinations: 65.60.35.141 (42522), 194.226.60.15 (390), 72.21.81.200 (30), 52.185.211.133 (23), 204.79.197.200 (16); 456 further events in other values [jun21isc-02#0]
- source clients: 10.6.15.93 — 376 events; external destinations=65; top destinations: 23.47.49.179 (61), 52.185.211.133 (30), 13.107.42.23 (21), 52.242.211.89 (18), 52.183.220.149 (13); 233 further events in other values [jun21isc-02#0]
- source clients: 10.6.15.187 — 365 events; external destinations=75; top destinations: 52.183.220.149 (18), 52.242.211.89 (17), 52.185.211.133 (15), 23.207.19.11 (14), 23.47.49.156 (13); 288 further events in other values [jun21isc-02#0]

## Impact Assessment



## Root Cause and Evidence Gaps

- download domains: solarwindsonline.com — 2 events [jun21isc-01#3]
- download domains: 162.244.83.95 — 1 events [jun21isc-01#3]
- download domains: 162.244.83.95:443 — 1 events [jun21isc-01#3]
- download domains: feedproxy.google.com — 1 events [jun21isc-01#3]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. Derived: internal client 10.6.15.119 ranks #1 by external connections (43437 events, 124 distinct external destinations). Most-contacted external IP: 65.60.35.141 (42522 connections). [jun21isc-09#0]
2. Derived: Kerberos identity of 10.6.15.119: hostname(s) desktop-niee9lp; human user account(s) tommy.vega. [jun21isc-09#0]
3. Derived: internal client 10.6.15.93 ranks #2 by external connections (376 events, 65 distinct external destinations). Most-contacted external IP: 23.47.49.179 (61 connections). [jun21isc-09#0]
4. Not established from the available artifacts.
5. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [jun21isc-10#0]
6. Derived: internal client 10.6.15.187 ranks #3 by external connections (365 events, 75 distinct external destinations). Most-contacted external IP: 52.183.220.149 (18 connections). [jun21isc-09#1]
7. Derived: Kerberos identity of 10.6.15.187: hostname(s) desktop-ys6fz2g; human user account(s) horace.maddox. [jun21isc-09#1]
8. Not established from the available artifacts.
