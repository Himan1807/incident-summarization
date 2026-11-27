# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 172.16.1.66 ranks #1 by external connections (164 events, 38 distinct external destinations). Most-contacted external IP: 23.52.9.222 (22 connections). [dirty_rat-08#0]
- Derived: Kerberos identity of 172.16.1.66: hostname(s) desktop-skbr25f; human user account(s) ccollier. [dirty_rat-08#0]
- Derived: Suricata alerts span 2024-07-30 02:00 UTC to 2024-07-30 02:00 UTC; earliest alert hour 2024-07-30 02:00 UTC (114 alerts). [dirty_rat-08#0]
- Derived: destinations of high-severity alerts: 141.98.10.79 (102), 172.16.1.4 (1), 172.16.1.66 (1), 208.95.112.1 (1). [dirty_rat-08#0]
- client accounts: DESKTOP-SKBR25F$ — 13 events; source ips: 172.16.1.66 (13) [dirty_rat-03#0]
- client accounts: ccollier — 8 events; source ips: 172.16.1.66 (8) [dirty_rat-03#0]
- client accounts: desktop-skbr25f$ — 6 events; source ips: 172.16.1.66 (6) [dirty_rat-03#0]
- full services: host/desktop-skbr25f.wiresharkworkshop.online — 1 events; source ips: 172.16.1.66 (1) [dirty_rat-04#3]
- full services: krbtgt/WIRESHARKWORKSH — 1 events; source ips: 172.16.1.66 (1) [dirty_rat-04#3]
- full services: ldap/wireshark-ws-dc.wiresharkworkshop.online — 1 events; source ips: 172.16.1.66 (1) [dirty_rat-04#3]
- high severity alerts > high severity signatures: ET INFO External IP Lookup Domain in DNS Lookup (ip-api .com) — 1 events [dirty_rat-06#4]
- high severity alerts > high severity signatures: ET INFO External IP Lookup ip-api.com — 1 events [dirty_rat-06#4]
- high severity alerts > high severity sources: 172.16.1.66 — 104 events [dirty_rat-06#4]
- high severity alerts > high severity sources: 141.98.10.79 — 1 events [dirty_rat-06#4]
- source clients: 172.16.1.66 — 164 events; external destinations=38; top destinations: 23.52.9.222 (22), 204.79.197.203 (13), 23.198.7.177 (12), 52.109.20.47 (12), 23.48.203.208 (8); 97 further events in other values [dirty_rat-02#0]
- full services: krb_tcp — 28 events; source ips: 172.16.1.66 (28) [dirty_rat-04#0]
- full services: krbtgt/WIRESHARKWORKSHOP.ONLINE — 10 events; source ips: 172.16.1.66 (10) [dirty_rat-04#0]
- full services: ldap/wireshark-ws-dc.wiresharkworkshop.online/wiresharkworkshop.online — 3 events; source ips: 172.16.1.66 (3) [dirty_rat-04#0]
- full services: LDAP/WIRESHARK-WS-DC.wiresharkworkshop.online/wiresharkworkshop.online — 2 events; source ips: 172.16.1.66 (2) [dirty_rat-04#0]

## Timeline

- 2024-07-30 02:00 UTC — alert timeline: 114 events; earliest alert hour [dirty_rat-06#5, dirty_rat-08#0]

## Detection: IDS Alerts

- alert signatures: ET MALWARE STRRAT CnC Checkin — 102 events [dirty_rat-06#0]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 5 events [dirty_rat-06#0]
- alert signatures: ET DROP Spamhaus DROP Listed Traffic Inbound group 26 — 1 events [dirty_rat-06#0]
- high severity alerts > high severity  destinations: 172.16.1.66 — 1 events [dirty_rat-06#3]
- high severity alerts > high severity  destinations: 208.95.112.1 — 1 events [dirty_rat-06#3]
- alert signatures: ET INFO Microsoft Connection Test — 1 events [dirty_rat-06#1]
- alert signatures: ET INFO NTLM Session Setup Request - Auth — 1 events [dirty_rat-06#1]
- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 1 events [dirty_rat-06#2]
- high severity alerts: 105 matching events [dirty_rat-06#2]
- high severity alerts > high severity  destinations: 141.98.10.79 — 102 events [dirty_rat-06#2]
- high severity alerts > high severity  destinations: 172.16.1.4 — 1 events [dirty_rat-06#2]

## Initial Infection Indicators

- http requests: no_http_uri — 160 events [dirty_rat-01#3]
- http requests: 172.16.1.66 -> 208.95.112.1:80 : /json/ — 2 events [dirty_rat-01#3]
- http requests: 172.16.1.66 -> 23.215.55.140:80 : /connecttest.txt — 2 events [dirty_rat-01#3]
- download domains: ip-api.com — 1 events [dirty_rat-01#3]
- domains: objects.githubusercontent.com — 1 events; top source ips: 172.16.1.66 (1); top destination ips: 185.199.110.133 (1) [dirty_rat-07#2]
- domains: oneclient.sfx.ms — 1 events; top source ips: 172.16.1.66 (1); top destination ips: 23.52.9.140 (1) [dirty_rat-07#2]
- download domains: www.msftconnecttest.com — 1 events [dirty_rat-01#4]
- file types: other — 164 events [dirty_rat-01#4]
- file transfers: 23 matching events [dirty_rat-01#0]
- file transfers > transfer details: file_transfer — 2 events [dirty_rat-01#0]
- file transfers > transfer details: 172.16.1.66 -> 13.69.239.79:443 : fuid: FQyVNG1qSUWl88SPO8 — 1 events [dirty_rat-01#0]
- file transfers > transfer details: 172.16.1.66 -> 20.166.2.191:443 : fuid: FTAoZx1f3vyui6NSY8 — 1 events [dirty_rat-01#0]
- domains: repo1.maven.org — 3 events; top source ips: 172.16.1.66 (3); top destination ips: 199.232.196.209 (3) [dirty_rat-07#0]
- domains: autodiscover-s.outlook.com — 1 events; top source ips: 172.16.1.66 (1); top destination ips: 40.97.199.114 (1) [dirty_rat-07#0]
- domains: default.exp-tas.com — 1 events; top source ips: 172.16.1.66 (1); top destination ips: 13.107.5.93 (1) [dirty_rat-07#0]
- domains: ecn.dev.virtualearth.net — 1 events; top source ips: 172.16.1.66 (1); top destination ips: 23.46.192.165 (1) [dirty_rat-07#0]
- file transfers > transfer details: 172.16.1.66 -> 20.189.173.26:443 : fuid: Fm9YMM3CNdjDmDuB2h — 1 events [dirty_rat-01#1]
- file transfers > transfer details: 172.16.1.66 -> 20.241.44.114:443 : fuid: F7RGOfAJ7v7njmqxc — 1 events [dirty_rat-01#1]
- file transfers > transfer details: 172.16.1.66 -> 20.96.153.111:443 : fuid: FtBrUL3KjJyjPbQ5V8 — 1 events [dirty_rat-01#1]
- file transfers > transfer details: 172.16.1.66 -> 208.95.112.1:80 : fuid: FdlG6pwAk9IIWc546 — 1 events [dirty_rat-01#1]

## Command-and-Control and Network Activity



## Impact Assessment

- file transfers > transfer details: 172.16.1.66 -> 23.194.164.136:443 : fuid: FwX9H2P4ySsBUtJw5 — 1 events [dirty_rat-01#2]
- file transfers > transfer details: 172.16.1.66 -> 23.215.55.140:80 : fuid: FbBtHc4DJvYjRTHKi — 1 events [dirty_rat-01#2]
- file transfers > transfer details: 172.16.1.66 -> 23.221.22.68:443 : fuid: FPikSY3rOlbAkpQ1Wa — 1 events [dirty_rat-01#2]
- download sources: 172.16.1.66 — 164 events [dirty_rat-01#2]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [dirty_rat-09#0]
2. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [dirty_rat-09#0]
3. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [dirty_rat-09#0]
4. Not established from the available artifacts.
5. Derived: Kerberos identity of 172.16.1.66: hostname(s) desktop-skbr25f; human user account(s) ccollier. [dirty_rat-08#0]
6. Derived: Suricata alerts span 2024-07-30 02:00 UTC to 2024-07-30 02:00 UTC; earliest alert hour 2024-07-30 02:00 UTC (114 alerts). [dirty_rat-08#0]
7. Derived: destinations of high-severity alerts: 141.98.10.79 (102), 172.16.1.4 (1), 172.16.1.66 (1), 208.95.112.1 (1). [dirty_rat-08#0]
