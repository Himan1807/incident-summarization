# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.12.3.66 ranks #1 by external connections (164 events, 16 distinct external destinations). Most-contacted external IP: 172.104.227.98 (79 connections). [dec21isc-09#0]
- Derived: Kerberos identity of 10.12.3.66: hostname(s) desktop-luoabv1; human user account(s) darin.figueroa. [dec21isc-09#0]
- Derived: Suricata alerts span 2021-12-03 19:00 UTC to 2021-12-03 20:00 UTC; earliest alert hour 2021-12-03 19:00 UTC (34 alerts). [dec21isc-09#0]
- Derived: destinations of high-severity alerts: 10.12.3.3 (1), 10.12.3.66 (1). [dec21isc-09#0]
- client accounts: darin.figueroa — 6 events; source ips: 10.12.3.66 (6) [dec21isc-03#0]
- source clients: 10.12.3.66 — 164 events; external destinations=16; top destinations: 172.104.227.98 (79), 163.172.50.82 (19), 51.75.33.120 (10), 51.159.35.157 (9), 52.109.8.24 (7); 40 further events in other values [dec21isc-02#0]
- full services: krb_tcp — 7 events; source ips: 10.12.3.66 (7) [dec21isc-04#0]
- full services: krbtgt/FARGREENTECH.COM — 2 events; source ips: 10.12.3.66 (2) [dec21isc-04#0]
- full services: LDAP/FARGREENTECH-DC.fargreentech.com/fargreentech.com — 1 events; source ips: 10.12.3.66 (1) [dec21isc-04#0]
- full services: cifs/FARGREENTECH-DC — 1 events; source ips: 10.12.3.66 (1) [dec21isc-04#0]
- No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [dec21isc-10#0]
- download domains: gamaes.shop — 1 events [dec21isc-01#0]
- download domains: newsaarctech.com — 1 events [dec21isc-01#0]
- http requests: no_http_uri — 251 events [dec21isc-01#0]
- http requests: 10.12.3.66 -> 104.21.29.80:80 : /wp-content/plugins/sSTToaEwCG5VASw/ — 2 events [dec21isc-01#0]

## Timeline

- 2021-12-03 19:00 UTC — alert timeline: 34 events; earliest alert hour [dec21isc-06#4, dec21isc-09#0]
- 2021-12-03 20:00 UTC — alert timeline: 26 events [dec21isc-06#4]

## Detection: IDS Alerts

- alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 50 events [dec21isc-06#0]
- alert signatures: ET INFO Windows Powershell User-Agent Usage — 2 events [dec21isc-06#0]
- alert signatures: ET HUNTING Suspicious Domain Request for Possible COVID-19 Domain M1 — 1 events [dec21isc-06#0]
- alert signatures: ET INFO EXE - Served Attached HTTP — 1 events [dec21isc-06#0]
- alert signatures: ET INFO NTLM Session Setup Request - Auth — 1 events [dec21isc-06#1]
- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 1 events [dec21isc-06#1]
- alert signatures: ET INFO PE EXE or DLL Windows file download HTTP — 1 events [dec21isc-06#1]
- alert signatures: ET INFO Packed Executable Download — 1 events [dec21isc-06#2]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 1 events [dec21isc-06#2]
- high severity alerts: 2 matching events [dec21isc-06#2]
- high severity alerts > high severity  destinations: 10.12.3.3 — 1 events [dec21isc-06#2]
- high severity alerts > high severity  destinations: 10.12.3.66 — 1 events [dec21isc-06#3]
- high severity alerts > high severity sources: 139.59.6.175 — 1 events [dec21isc-06#4]

## Initial Infection Indicators

- file types: other — 254 events [dec21isc-01#4]
- file types: exe — 1 events [dec21isc-01#4]
- download sources: 10.12.3.66 — 255 events [dec21isc-01#4]
- http requests: 10.12.3.66 -> 139.59.6.175:80 : /wp-content/Sx9tvV5/ — 2 events [dec21isc-01#1]
- file transfers: 19 matching events [dec21isc-01#1]
- file transfers > transfer details: file_transfer — 2 events [dec21isc-01#1]
- file transfers > transfer details: 10.12.3.66 -> 104.21.29.80:80 : fuid: Fgt1qpTQKLib5heKg — 1 events [dec21isc-01#1]
- domains: gameplayapi.intel.com — 1 events; top source ips: 10.12.3.66 (1); top destination ips: 23.3.6.28 (1) [dec21isc-08#0]
- file transfers > transfer details: 10.12.3.66 -> 20.72.205.209:443 : fuid: FJFP3C40hex6kT3Ggl — 1 events [dec21isc-01#3]
- file transfers > transfer details: 10.12.3.66 -> 204.79.197.200:443 : fuid: FdlPTh4wos9hySdl7g — 1 events [dec21isc-01#3]
- file transfers > transfer details: 10.12.3.66 -> 204.79.197.203:443 : fuid: F6yvjQ1CPyjn2U59B8 — 1 events [dec21isc-01#3]
- file transfers > transfer details: 10.12.3.66 -> 40.83.240.146:443 : fuid: FzLTB42igmFgNIabdd — 1 events [dec21isc-01#3]

## Command-and-Control and Network Activity

- file transfers > transfer details: 10.12.3.66 -> 139.59.6.175:80 : file: IE7MnYfF4c.dll — 1 events [dec21isc-01#2]
- file transfers > transfer details: 10.12.3.66 -> 163.172.50.82:443 : fuid: FmBkZQ1QW21exVxXkf — 1 events [dec21isc-01#2]
- file transfers > transfer details: 10.12.3.66 -> 172.104.227.98:443 : fuid: FRmn1G3jW4ycHzKCk — 1 events [dec21isc-01#2]
- file transfers > transfer details: 10.12.3.66 -> 20.50.201.200:443 : fuid: Ft93YucvRiDc9VXKa — 1 events [dec21isc-01#2]

## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [dec21isc-10#0]
2. Derived: internal client 10.12.3.66 ranks #1 by external connections (164 events, 16 distinct external destinations). Most-contacted external IP: 172.104.227.98 (79 connections). [dec21isc-09#0]
3. Derived: Kerberos identity of 10.12.3.66: hostname(s) desktop-luoabv1; human user account(s) darin.figueroa. [dec21isc-09#0]
4. Not established from the available artifacts.
5. Derived: destinations of high-severity alerts: 10.12.3.3 (1), 10.12.3.66 (1). [dec21isc-09#0]
6. client accounts: darin.figueroa — 6 events; source ips: 10.12.3.66 (6) [dec21isc-03#0]
7. hostnames: desktop-luoabv1 — 1 events; source ips: 10.12.3.66 (1) [dec21isc-05#0]
8. Not established from the available artifacts.
