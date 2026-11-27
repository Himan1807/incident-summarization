# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.0.19.14 ranks #1 by external connections (683 events, 50 distinct external destinations). Most-contacted external IP: 157.245.142.66 (267 connections). [burnincandle-08#0]
- Derived: Kerberos identity of 10.0.19.14: hostname(s) desktop-5qs3d5d; human user account(s) patrick.zimmerman. [burnincandle-08#0]
- Derived: Suricata alerts span 2022-03-21 20:00 UTC to 2022-03-22 03:00 UTC; earliest alert hour 2022-03-21 20:00 UTC (10 alerts). [burnincandle-08#0]
- Derived: destinations of high-severity alerts: 10.0.19.9 (22), 188.166.154.118 (4). [burnincandle-08#0]
- client accounts: patrick.zimmerman — 12 events; source ips: 10.0.19.14 (12) [burnincandle-03#0]
- client accounts: DESKTOP-5QS3D5D$ — 7 events; source ips: 10.0.19.14 (7) [burnincandle-03#0]
- client accounts: desktop-5qs3d5d$ — 2 events; source ips: 10.0.19.14 (2) [burnincandle-03#0]
- full services: ldap/BURNINCANDLE-DC.burnincandle.com — 1 events; source ips: 10.0.19.14 (1) [burnincandle-04#2]
- source clients: 10.0.19.14 — 683 events; external destinations=50; top destinations: 157.245.142.66 (267), 91.193.16.181 (175), 40.83.240.146 (20), 52.183.220.149 (20), 52.185.211.133 (20); 181 further events in other values [burnincandle-02#0]
- download domains: ctldl.windowsupdate.com — 12 events [burnincandle-01#0]
- download domains: x1.c.lencr.org — 4 events [burnincandle-01#0]
- download domains: oceriesfornot.top — 1 events [burnincandle-01#0]
- download domains: r3.i.lencr.org — 1 events [burnincandle-01#0]
- full services: cifs/BURNINCANDLE-DC — 1 events; source ips: 10.0.19.14 (1) [burnincandle-04#1]
- full services: desktop-5qs3d5d$ — 1 events; source ips: 10.0.19.14 (1) [burnincandle-04#1]
- full services: host/desktop-5qs3d5d.burnincandle.com — 1 events; source ips: 10.0.19.14 (1) [burnincandle-04#1]
- full services: krbtgt/BURNINCANDLE — 1 events; source ips: 10.0.19.14 (1) [burnincandle-04#1]

## Timeline

- 2022-03-21 20:00 UTC — alert timeline: 10 events; earliest alert hour [burnincandle-06#4, burnincandle-08#0]
- 2022-03-21 21:00 UTC — alert timeline: 13 events [burnincandle-06#4]
- 2022-03-21 22:00 UTC — alert timeline: 12 events [burnincandle-06#5]
- 2022-03-21 23:00 UTC — alert timeline: 11 events [burnincandle-06#5]
- 2022-03-22 00:00 UTC — alert timeline: 60 events [burnincandle-06#5]
- 2022-03-22 01:00 UTC — alert timeline: 63 events [burnincandle-06#5]
- 2022-03-22 02:00 UTC — alert timeline: 60 events [burnincandle-06#6]
- 2022-03-22 03:00 UTC — alert timeline: 18 events [burnincandle-06#6]

## Detection: IDS Alerts

- alert signatures: ET HUNTING Request to .TOP Domain with Minimal Headers — 1 events [burnincandle-06#1]
- alert signatures: ET INFO HTTP Request to a *.top domain — 1 events [burnincandle-06#1]
- alert signatures: ET INFO Observed Abused File Sharing Domain in TLS SNI (filebin .net) — 1 events [burnincandle-06#1]
- alert signatures: ET MALWARE Win32/IcedID Request Cookie — 1 events [burnincandle-06#1]
- high severity alerts: 26 matching events [burnincandle-06#2]
- high severity alerts > high severity  destinations: 10.0.19.9 — 22 events [burnincandle-06#2]
- high severity alerts > high severity  destinations: 188.166.154.118 — 4 events [burnincandle-06#2]
- high severity alerts > high severity signatures: ET MALWARE Win32/IcedID Requesting Encoded Binary M4 — 1 events [burnincandle-06#4]
- high severity alerts > high severity sources: 10.0.19.14 — 26 events [burnincandle-06#4]
- alert signatures: ET INFO OpenSSL Demo CA - Internet Widgits Pty (O) — 216 events [burnincandle-06#0]
- alert signatures: ET DNS Query to a *.top domain - Likely Hostile — 22 events [burnincandle-06#0]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 3 events [burnincandle-06#0]

## Initial Infection Indicators

- http requests: no_http_uri — 661 events [burnincandle-01#1]
- http requests: 10.0.19.14 -> 104.80.96.219:80 : / — 5 events [burnincandle-01#1]
- http requests: 10.0.19.14 -> 188.166.154.118:80 : / — 5 events [burnincandle-01#1]
- http requests: 10.0.19.14 -> 209.197.3.8:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?c6c9c220471a286c — 1 events [burnincandle-01#1]
- file transfers > transfer details: 10.0.19.14 -> 157.245.142.66:443 : fuid: FE8HqU2VXjUR5N7Hu1 — 1 events [burnincandle-01#6]
- file types: other — 683 events [burnincandle-01#6]
- download sources: 10.0.19.14 — 683 events [burnincandle-01#6]
- http requests: 10.0.19.14 -> 68.142.107.1:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?c66ea67221454a2e — 1 events [burnincandle-01#3]
- http requests: 10.0.19.14 -> 68.142.107.1:80 : /msdownload/update/v3/static/trustedr/en/pinrulesstl.cab?416ee1a6826abea5 — 1 events [burnincandle-01#3]
- file transfers: 55 matching events [burnincandle-01#3]
- file transfers > transfer details: file_transfer — 2 events [burnincandle-01#3]
- http requests: 10.0.19.14 -> 209.197.3.8:80 : /msdownload/update/v3/static/trustedr/en/pinrulesstl.cab?36a063424dfa7851 — 1 events [burnincandle-01#2]
- http requests: 10.0.19.14 -> 23.219.38.10:80 : /msdownload/update/v3/static/trustedr/en/disallowedcertstl.cab?8fd0590036de0ddd — 1 events [burnincandle-01#2]
- http requests: 10.0.19.14 -> 68.142.107.129:80 : /msdownload/update/v3/static/trustedr/en/pinrulesstl.cab?d1adc478adff0d72 — 1 events [burnincandle-01#2]
- file transfers > transfer details: 10.0.19.14 -> 13.69.239.74:443 : fuid: Fv3eyH1ZHebL3IA9f — 1 events [burnincandle-01#5]
- file transfers > transfer details: 10.0.19.14 -> 13.89.179.10:443 : fuid: FuKuuXxzeF3KeH3a9 — 1 events [burnincandle-01#5]
- file transfers > transfer details: 10.0.19.14 -> 13.89.179.9:443 : fuid: FsmyaS1IbV3icPlSef — 1 events [burnincandle-01#5]

## Command-and-Control and Network Activity

- domains: suncoastpinball.com — 5 events; top source ips: 10.0.19.14 (5); top destination ips: 160.153.32.99 (5) [burnincandle-07#1]
- domains: filebin.net — 1 events; top source ips: 10.0.19.14 (1); top destination ips: 185.47.40.36 (1) [burnincandle-07#1]
- domains: situla.bitbit.net — 1 events; top source ips: 10.0.19.14 (1); top destination ips: 87.238.33.8 (1) [burnincandle-07#1]

## Impact Assessment

- file transfers > transfer details: 10.0.19.14 -> 104.80.96.219:80 : fuid: FXJkhP2Z2m8vw4ukM6 — 1 events [burnincandle-01#4]
- file transfers > transfer details: 10.0.19.14 -> 13.107.42.16:443 : fuid: FJoV2T1Wg9qRybhxf2 — 1 events [burnincandle-01#4]
- file transfers > transfer details: 10.0.19.14 -> 13.69.116.104:443 : fuid: FOGdMEmtC3nLDsbVd — 1 events [burnincandle-01#4]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. Query 'suspicious certificates' returned no aggregation results (shards failed: 1 of 111). This evidence is UNAVAILABLE; it is not evidence that nothing exists. [burnincandle-09#0]
2. Derived: internal client 10.0.19.14 ranks #1 by external connections (683 events, 50 distinct external destinations). Most-contacted external IP: 157.245.142.66 (267 connections). [burnincandle-08#0]
3. Derived: Kerberos identity of 10.0.19.14: hostname(s) desktop-5qs3d5d; human user account(s) patrick.zimmerman. [burnincandle-08#0]
4. Not established from the available artifacts.
5. Derived: destinations of high-severity alerts: 10.0.19.9 (22), 188.166.154.118 (4). [burnincandle-08#0]
6. hostnames: desktop-5qs3d5d — 1 events; source ips: 10.0.19.14 (1) [burnincandle-05#0]
7. client accounts: patrick.zimmerman — 12 events; source ips: 10.0.19.14 (12) [burnincandle-03#0]
