# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 172.17.4.206 ranks #1 by external connections (451 events, 36 distinct external destinations). Most-contacted external IP: 45.32.211.207 (61 connections). [may21isc-09#0]
- Derived: Kerberos identity of 172.17.4.206: hostname(s) desktop-v0feh1l; human user account(s) alfonso.paternoster. [may21isc-09#0]
- Derived: Suricata alerts span 2021-05-04 22:00 UTC to 2021-05-04 23:00 UTC; earliest alert hour 2021-05-04 22:00 UTC (12 alerts). [may21isc-09#0]
- client accounts: DESKTOP-V0FEH1L$ — 11 events; source ips: 172.17.4.206 (11) [may21isc-03#0]
- client accounts: alfonso.paternoster — 6 events; source ips: 172.17.4.206 (6) [may21isc-03#0]
- client accounts: desktop-v0feh1l$ — 6 events; source ips: 172.17.4.206 (6) [may21isc-03#0]
- full services: ldap/nutmegcrazy-dc.nutmeg-station.com/nutmeg-station.com — 1 events; source ips: 172.17.4.206 (1) [may21isc-04#3]
- source clients: 172.17.4.206 — 451 events; external destinations=36; top destinations: 45.32.211.207 (61), 54.225.155.255 (51), 24.179.77.148 (43), 23.47.169.154 (40), 72.21.81.240 (28); 228 further events in other values [may21isc-02#0]
- download domains: store-images.s-microsoft.com — 14 events [may21isc-01#0]
- download domains: download.windowsupdate.com — 12 events [may21isc-01#0]
- download domains: au.download.windowsupdate.com — 3 events [may21isc-01#0]
- download domains: ctldl.windowsupdate.com — 3 events [may21isc-01#0]
- download domains: 185.183.99.115 — 1 events [may21isc-01#1]
- http requests: no_http_uri — 418 events [may21isc-01#1]
- http requests: 172.17.4.206 -> 8.249.131.254:80 : /c/msdownload/update/software/defu/2021/05/am_delta_patch_1.337.600.0_f8fd1ab601622aa5111bab3b497be9d8ce1b22a6.exe — 2 events [may21isc-01#1]
- http requests: 172.17.4.206 -> 185.183.99.115:80 : /44313,6048108796.dat — 1 events [may21isc-01#1]

## Timeline

- 2021-05-04 22:00 UTC — alert timeline: 12 events; earliest alert hour [may21isc-06#1, may21isc-09#0]
- 2021-05-04 23:00 UTC — alert timeline: 72 events [may21isc-06#1]

## Detection: IDS Alerts

- alert signatures: ET INFO NTLM Session Setup Request - Negotiate — 1 events [may21isc-06#1]
- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 1 events [may21isc-06#1]
- alert signatures: ET INFO External IP Address Lookup Domain (ipify .org) in TLS SNI — 41 events [may21isc-06#0]
- alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 34 events [may21isc-06#0]
- alert signatures: ET INFO External IP Lookup Domain (ipify .org) in DNS Lookup — 6 events [may21isc-06#0]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.11693.14503766937567901.176691f4-19f9-48ef-a75c-2af62972b059.04097907-d16b-47f1-b1a6-83fbc59bb15c?w=172&h=258 — 1 events [may21isc-01#2]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.13825.14369454977035291.312a1827-6832-45f4-885d-562c4148d669.5c931ffa-b74a-45a6-a9cb-082c7d9cddd9?w=172&h=258 — 1 events [may21isc-01#2]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.15387.13812021519099434.2bf8d983-bebb-467e-9b6a-e52bb2610650.46530b30-f947-46d5-ae2e-dd024af3da59?w=172&h=258 — 1 events [may21isc-01#2]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.15459.14018880429702282.f227304a-b5a1-43b5-a5ef-c3a2eafb2c2d.9871105b-6b54-4a8b-9295-e4197c93988e?w=172&h=258 — 1 events [may21isc-01#2]

## Initial Infection Indicators

- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.15792.14098991041572765.f2e8d44f-55f2-4b91-b7c9-5fe108fe9c1a.f803e6b2-b8a5-47bb-98f1-9843909974ce?w=172&h=258 — 1 events [may21isc-01#3]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.45464.14137276003875252.d1d6dd04-81e9-424d-a1b6-7a81e52dfeef.656ba41f-9220-4ebf-9cf4-a685da2f558d?w=172&h=258 — 1 events [may21isc-01#3]
- http requests: 172.17.4.206 -> 23.47.169.154:80 : /image/apps.57047.14380149729470603.1aef82b1-76c1-46e9-b3a7-bfea4ea54b01.ed79b095-68f1-4190-9ff1-74e2fbf0103a?w=172&h=258 — 1 events [may21isc-01#3]
- file transfers: 92 matching events [may21isc-01#3]
- domains: api.ipify.org — 41 events; top source ips: 172.17.4.206 (41); top destination ips: 54.225.155.255 (17), 23.21.48.44 (9), 54.235.175.90 (8), 50.19.216.111 (7) [may21isc-08#0]
- domains: img-prod-cms-rt-microsoft-com.akamaized.net — 1 events; top source ips: 172.17.4.206 (1); top destination ips: 23.47.52.180 (1) [may21isc-08#0]
- domains: www.openssl.org — 1 events; top source ips: 172.17.4.206 (1); top destination ips: 104.93.49.229 (1) [may21isc-08#0]
- download sources: 172.17.4.206 — 451 events [may21isc-01#7]

## Command-and-Control and Network Activity



## Impact Assessment

- file transfers > transfer details: file_transfer — 29 events [may21isc-01#4]
- file transfers > transfer details: 172.17.4.206 -> 104.93.49.229:443 : fuid: F2YugI1hndkt6JD5Ne — 1 events [may21isc-01#4]
- file transfers > transfer details: 172.17.4.206 -> 13.107.246.66:443 : fuid: FEtVKF2lotN7Jqmc5 — 1 events [may21isc-01#4]

## Root Cause and Evidence Gaps

- file transfers > transfer details: 172.17.4.206 -> 13.107.42.23:443 : fuid: Frp4qe2vODf6xkENH8 — 1 events [may21isc-01#6]
- file types: other — 445 events [may21isc-01#6]
- file types: exe — 6 events [may21isc-01#6]

## Corrective and Preventive Actions

- full services: krb_tcp — 24 events; source ips: 172.17.4.206 (24) [may21isc-04#0]
- full services: krbtgt/NUTMEG-STATION.COM — 11 events; source ips: 172.17.4.206 (11) [may21isc-04#0]
- full services: LDAP/NutmegCrazy-DC.nutmeg-station.com/nutmeg-station.com — 3 events; source ips: 172.17.4.206 (3) [may21isc-04#0]
- full services: DESKTOP-V0FEH1L$ — 1 events; source ips: 172.17.4.206 (1) [may21isc-04#0]

## Answers to Investigation Questions

1. No matching results for: suricata alerts / high severity alerts. (Absence in this query is not proof of absence elsewhere.) [may21isc-10#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [may21isc-10#0]
3. Derived: internal client 172.17.4.206 ranks #1 by external connections (451 events, 36 distinct external destinations). Most-contacted external IP: 45.32.211.207 (61 connections). [may21isc-09#0]
4. Not established from the available artifacts.
5. Derived: Suricata alerts span 2021-05-04 22:00 UTC to 2021-05-04 23:00 UTC; earliest alert hour 2021-05-04 22:00 UTC (12 alerts). [may21isc-09#0]
6. alert signatures: ET INFO External IP Address Lookup Domain (ipify .org) in TLS SNI — 41 events [may21isc-06#0]
7. alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 34 events [may21isc-06#0]
