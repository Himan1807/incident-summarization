# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 172.17.0.99 ranks #1 by external connections (361 events, 35 distinct external destinations). Most-contacted external IP: 79.124.78.197 (218 connections). [koi_stealer-08#0]
- Derived: Kerberos identity of 172.17.0.99: hostname(s) desktop-rnvo9at; human user account(s) afletcher. [koi_stealer-08#0]
- Derived: Suricata alerts span 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC; earliest alert hour 2024-09-04 17:00 UTC (31 alerts). [koi_stealer-08#0]
- Derived: destinations of high-severity alerts: 79.124.78.197 (49), 172.17.0.99 (1). [koi_stealer-08#0]
- client accounts: afletcher — 8 events; source ips: 172.17.0.99 (8) [koi_stealer-03#0]
- source clients: 172.17.0.99 — 361 events; external destinations=35; top destinations: 79.124.78.197 (218), 23.45.119.144 (18), 204.79.197.203 (14), 52.113.194.132 (10), 23.195.212.189 (9); 92 further events in other values [koi_stealer-02#0]
- full services: krb_tcp — 8 events; source ips: 172.17.0.99 (8) [koi_stealer-04#0]
- full services: krbtgt/BEPOSITIVE.COM — 2 events; source ips: 172.17.0.99 (2) [koi_stealer-04#0]
- full services: LDAP/WIN-CTL9XBQ9Y19.bepositive.com/bepositive.com — 1 events; source ips: 172.17.0.99 (1) [koi_stealer-04#0]
- full services: cifs/WIN-CTL9XBQ9Y19 — 1 events; source ips: 172.17.0.99 (1) [koi_stealer-04#0]
- download domains: 79.124.78.197 — 50 events [koi_stealer-01#0]
- download domains: ctldl.windowsupdate.com — 3 events [koi_stealer-01#0]
- download domains: www.msftconnecttest.com — 2 events [koi_stealer-01#0]
- download domains: acroipm2.adobe.com — 1 events [koi_stealer-01#0]
- download domains: x1.c.lencr.org — 1 events [koi_stealer-01#1]
- http requests: no_http_uri — 301 events [koi_stealer-01#1]
- http requests: 172.17.0.99 -> 79.124.78.197:80 : /foots.php — 48 events [koi_stealer-01#1]
- http requests: 172.17.0.99 -> 23.220.251.149:80 : /connecttest.txt — 2 events [koi_stealer-01#1]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- high severity alerts > high severity signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 48 events [koi_stealer-06#2]
- high severity alerts > high severity signatures: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound — 1 events [koi_stealer-06#2]
- high severity alerts > high severity signatures: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) — 1 events [koi_stealer-06#2]
- high severity alerts > high severity sources: 172.17.0.99 — 49 events [koi_stealer-06#2]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 5 events [koi_stealer-06#0]
- alert signatures: ET INFO Microsoft Connection Test — 2 events [koi_stealer-06#0]
- high severity alerts: 50 matching events [koi_stealer-06#1]
- high severity alerts > high severity  destinations: 79.124.78.197 — 49 events [koi_stealer-06#1]
- high severity alerts > high severity  destinations: 172.17.0.99 — 1 events [koi_stealer-06#1]
- high severity alerts > high severity sources: 79.124.78.197 — 1 events [koi_stealer-06#3]

## Initial Infection Indicators

- domains: weathermapdata.blob.core.windows.net — 1 events [koi_stealer-07#1]
- http requests: 172.17.0.99 -> 23.220.251.158:80 : /connecttest.txt — 2 events [koi_stealer-01#2]
- http requests: 172.17.0.99 -> 79.124.78.197:80 : /index.php?id=&subid=qIOuKk7U — 2 events [koi_stealer-01#2]
- http requests: 172.17.0.99 -> 184.29.137.96:80 : / — 1 events [koi_stealer-01#2]
- http requests: 172.17.0.99 -> 199.232.210.172:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?d7a8a57aa5acd39b — 1 events [koi_stealer-01#2]
- domains: sso.godaddy.com — 3 events [koi_stealer-07#0]
- domains: www.bellantonicioccolato.it — 2 events [koi_stealer-07#0]
- domains: img-s-msn-com.akamaized.net — 1 events [koi_stealer-07#0]
- domains: oneclient.sfx.ms — 1 events [koi_stealer-07#0]
- http requests: 172.17.0.99 -> 199.232.210.172:80 : /msdownload/update/v3/static/trustedr/en/disallowedcertstl.cab?91717f420e6dda94 — 1 events [koi_stealer-01#3]
- http requests: 172.17.0.99 -> 199.232.214.172:80 : /msdownload/update/v3/static/trustedr/en/pinrulesstl.cab?a5fef2ac8502b132 — 1 events [koi_stealer-01#3]
- http requests: 172.17.0.99 -> 23.220.251.47:80 : /assets/Owner/arm/ProcessMAU.txt — 1 events [koi_stealer-01#3]
- file transfers: 123 matching events [koi_stealer-01#3]

## Command-and-Control and Network Activity



## Impact Assessment

- file transfers > transfer details: 172.17.0.99 -> 20.189.173.26:443 : fuid: FhRlFk2pp8tC1dsabb — 1 events [koi_stealer-01#5]
- file transfers > transfer details: 172.17.0.99 -> 20.241.44.114:443 : fuid: FyjT0AzkMPMcF8Uck — 1 events [koi_stealer-01#5]
- file transfers > transfer details: 172.17.0.99 -> 20.42.73.28:443 : fuid: FpR8YU2UKfciamuQTd — 1 events [koi_stealer-01#5]
- file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FSvMjvPqRih6zUFI5 — 1 events [koi_stealer-01#5]

## Root Cause and Evidence Gaps

- file transfers > transfer details: file_transfer — 53 events [koi_stealer-01#4]
- file transfers > transfer details: 172.17.0.99 -> 13.70.79.200:443 : fuid: FU0Kma3jtLVDFQsWRa — 1 events [koi_stealer-01#4]
- file transfers > transfer details: 172.17.0.99 -> 13.89.179.9:443 : fuid: FMvkJInaCxvQDPRv9 — 1 events [koi_stealer-01#4]
- file transfers > transfer details: 172.17.0.99 -> 20.189.173.1:443 : fuid: FLUKDa36wJdASXKgHg — 1 events [koi_stealer-01#4]
- file transfers > transfer details: 172.17.0.99 -> 23.194.68.140:443 : fuid: FYIShP1GoXJB2e2LHc — 1 events [koi_stealer-01#6]
- file types: other — 361 events [koi_stealer-01#6]
- download sources: 172.17.0.99 — 361 events [koi_stealer-01#6]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [koi_stealer-09#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [koi_stealer-09#0]
3. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [koi_stealer-09#0]
4. Not established from the available artifacts.
5. Derived: internal client 172.17.0.99 ranks #1 by external connections (361 events, 35 distinct external destinations). Most-contacted external IP: 79.124.78.197 (218 connections). [koi_stealer-08#0]
6. Derived: Kerberos identity of 172.17.0.99: hostname(s) desktop-rnvo9at; human user account(s) afletcher. [koi_stealer-08#0]
7. Derived: Suricata alerts span 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC; earliest alert hour 2024-09-04 17:00 UTC (31 alerts). [koi_stealer-08#0]
8. Not established from the available artifacts.
