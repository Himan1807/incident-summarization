# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- client accounts: laptop-x9naq2eu$ — 32 events; source ips: 192.168.5.125 (32) [apr21isc-02#0]
- client accounts: wilmer.coughlin — 3 events; source ips: 192.168.5.125 (3) [apr21isc-02#0]
- full services: cifs/Clockwater-DC.clockwater.net — 1 events; source ips: 192.168.5.125 (1) [apr21isc-03#1]
- No matching results for: high activity external dest / source clients. (Absence in this query is not proof of absence elsewhere.) [apr21isc-08#0]
- No matching results for: kerberos hostnames / hostnames. (Absence in this query is not proof of absence elsewhere.) [apr21isc-08#0]
- http requests: 192.168.5.125 -> 52.20.197.7:80 : / — 3 events [apr21isc-01#5]
- http requests: 192.168.5.125 -> 172.67.75.172:80 : /ip — 2 events [apr21isc-01#5]
- http requests: 192.168.5.125 -> 176.111.174.53:80 : /campo/r/r1 — 2 events [apr21isc-01#5]
- file transfers: 1944 matching events [apr21isc-01#5]
- download domains: sv.symcd.com — 1 events [apr21isc-01#3]
- http requests: no_http_uri — 2126 events [apr21isc-01#3]
- http requests: 192.168.5.125 -> 217.12.218.46:80 : /preload?manifest=wac — 1856 events [apr21isc-01#3]
- http requests: 192.168.5.125 -> 217.12.218.46:80 : /sa — 143 events [apr21isc-01#3]
- Derived: Suricata alerts span 2021-03-29 22:00 UTC to 2021-03-29 22:00 UTC; earliest alert hour 2021-03-29 22:00 UTC (2 alerts). [apr21isc-07#0]
- Derived: destinations of high-severity alerts: 192.168.5.125 (2). [apr21isc-07#0]

## Timeline

- 2021-03-29 22:00 UTC — alert timeline: 2 events; earliest alert hour [apr21isc-04#1, apr21isc-07#0]

## Detection: IDS Alerts

- alert signatures: ET MALWARE Observed Malicious SSL Cert (BazaLoader CnC) — 1 events [apr21isc-04#0]
- high severity alerts: 2 matching events [apr21isc-04#0]
- high severity alerts > high severity  destinations: 192.168.5.125 — 2 events [apr21isc-04#0]
- high severity alerts > high severity signatures: ET MALWARE Observed Malicious SSL Cert (Bazar Backdoor) — 1 events [apr21isc-04#1]
- high severity alerts > high severity sources: 54.184.119.29 — 2 events [apr21isc-04#1]
- download domains: onedrive.live.com — 1071 events [apr21isc-01#0]
- download domains: store-images.s-microsoft.com — 12 events [apr21isc-01#0]
- download domains: checkip.amazonaws.com — 7 events [apr21isc-01#0]
- download domains: ts-ocsp.ws.symantec.com — 3 events [apr21isc-01#0]
- download domains: veso2.xyz — 3 events [apr21isc-01#1]
- download domains: ocsp.verisign.com — 2 events [apr21isc-01#1]
- download domains: 217.12.218.46 — 1 events [apr21isc-01#1]
- download domains: admin.yougleeindia.in — 1 events [apr21isc-01#1]

## Initial Infection Indicators

- http requests: 192.168.5.125 -> 107.21.162.206:80 : / — 12 events [apr21isc-01#4]
- http requests: 192.168.5.125 -> 34.193.115.2:80 : / — 4 events [apr21isc-01#4]
- http requests: 192.168.5.125 -> 52.204.109.97:80 : / — 4 events [apr21isc-01#4]
- http requests: 192.168.5.125 -> 3.224.94.38:80 : / — 3 events [apr21isc-01#4]
- file transfers > transfer details: 192.168.5.125 -> 13.107.42.23:443 : fuid: FeRbvb2Sh63zJEufub — 1 events [apr21isc-01#8]
- file transfers > transfer details: 192.168.5.125 -> 168.62.200.169:443 : fuid: FDESeU16jOwEDIKEP3 — 1 events [apr21isc-01#8]
- file types: other — 4174 events [apr21isc-01#8]
- file types: exe — 5 events [apr21isc-01#8]

## Command-and-Control and Network Activity

- domains: gtmers.xyz — 9 events; top source ips: 192.168.5.125 (9); top destination ips: 8.209.100.246 (9) [apr21isc-06#0]
- domains: fonts.gstatic.com — 4 events; top source ips: 192.168.5.125 (4); top destination ips: 142.250.138.94 (4) [apr21isc-06#0]
- domains: img-prod-cms-rt-microsoft-com.akamaized.net — 1 events; top source ips: 192.168.5.125 (1); top destination ips: 23.47.52.180 (1) [apr21isc-06#0]

## Impact Assessment

- file transfers > transfer details: 192.168.5.125 -> 107.21.162.206:80 : fuid: FYscFL3F9zWamVdQkb — 1 events [apr21isc-01#7]
- file transfers > transfer details: file_transfer — 961 events [apr21isc-01#6]
- file transfers > transfer details: 192.168.5.125 -> 104.21.74.174:80 : fuid: F9pkCk47eaobtnKKJ — 1 events [apr21isc-01#6]

## Root Cause and Evidence Gaps

- download domains: api.ip.sb — 1 events [apr21isc-01#2]
- download domains: ctldl.windowsupdate.com — 1 events [apr21isc-01#2]
- download domains: s.symcd.com — 1 events [apr21isc-01#2]
- download domains: s2.symcb.com — 1 events [apr21isc-01#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. Derived: Suricata alerts span 2021-03-29 22:00 UTC to 2021-03-29 22:00 UTC; earliest alert hour 2021-03-29 22:00 UTC (2 alerts). [apr21isc-07#0]
2. Derived: destinations of high-severity alerts: 192.168.5.125 (2). [apr21isc-07#0]
3. No matching results for: high activity external dest / source clients. (Absence in this query is not proof of absence elsewhere.) [apr21isc-08#0]
4. Not established from the available artifacts.
5. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [apr21isc-08#0]
6. client accounts: laptop-x9naq2eu$ — 32 events; source ips: 192.168.5.125 (32) [apr21isc-02#0]
7. client accounts: wilmer.coughlin — 3 events; source ips: 192.168.5.125 (3) [apr21isc-02#0]
8. Not established from the available artifacts.
