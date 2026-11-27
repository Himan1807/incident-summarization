# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.1.21.58 ranks #1 by external connections (312 events, 57 distinct external destinations). Most-contacted external IP: 153.92.1.49 (91 connections). [lumma_stealer-08#0]
- Derived: Kerberos identity of 10.1.21.58: hostname(s) desktop-es9f3ml; human user account(s) gwyatt. [lumma_stealer-08#0]
- Derived: Suricata alerts span 2026-01-27 23:00 UTC to 2026-01-27 23:00 UTC; earliest alert hour 2026-01-27 23:00 UTC (70 alerts). [lumma_stealer-08#0]
- Derived: destinations of high-severity alerts: 10.1.21.2 (26), 153.92.1.49 (23), 10.1.21.58 (1), 62.72.32.156 (1). [lumma_stealer-08#0]
- client accounts: gwyatt — 8 events; source ips: 10.1.21.58 (8) [lumma_stealer-03#0]
- full services: krb_tcp — 8 events; source ips: 10.1.21.58 (8) [lumma_stealer-04#0]
- full services: krbtgt/WIN11OFFICE.COM — 2 events; source ips: 10.1.21.58 (2) [lumma_stealer-04#0]
- full services: LDAP/WIN-LU4L24X3UB7.win11office.com/win11office.com — 1 events; source ips: 10.1.21.58 (1) [lumma_stealer-04#0]
- full services: cifs/WIN-LU4L24X3UB7 — 1 events; source ips: 10.1.21.58 (1) [lumma_stealer-04#0]
- source clients: 10.1.21.58 — 312 events; external destinations=57; top destinations: 153.92.1.49 (91), 142.251.116.95 (34), 150.171.28.11 (14), 52.109.0.142 (10), 23.222.241.141 (6); 157 further events in other values [lumma_stealer-02#0]
- file transfers: 31 matching events [lumma_stealer-01#0]
- file transfers > transfer details: file_transfer — 8 events [lumma_stealer-01#0]
- file transfers > transfer details: 10.1.21.58 -> 104.208.16.95:443 : fuid: FUwNUi3lIgrBDgnrnb — 1 events [lumma_stealer-01#0]
- file transfers > transfer details: 10.1.21.58 -> 142.250.115.113:80 : file: json.txt — 1 events [lumma_stealer-01#0]
- file transfers > transfer details: 10.1.21.58 -> 150.171.28.11:443 : fuid: FS8Yw11fhIRcqzQsli — 1 events [lumma_stealer-01#2]
- download sources: 10.1.21.58 — 312 events [lumma_stealer-01#2]

## Timeline

- 2026-01-27 23:00 UTC — alert timeline: 70 events; earliest alert hour [lumma_stealer-06#6, lumma_stealer-08#0]

## Detection: IDS Alerts

- alert signatures: ET INFO HTTP Request to .su TLD (Soviet Union) Often Malware Related — 6 events [lumma_stealer-06#1]
- alert signatures: ET DNS Query for .cc TLD — 4 events [lumma_stealer-06#1]
- alert signatures: ET MALWARE Win32/Lumma Stealer Related CnC Domain in DNS Lookup (whooptm .cyou) — 2 events [lumma_stealer-06#1]
- alert signatures: ET DROP Spamhaus DROP Listed Traffic Inbound group 10 — 1 events [lumma_stealer-06#1]
- alert signatures: ET JA3 Hash - Possible SoftEther Windows Client SSTP Traffic — 18 events [lumma_stealer-06#0]
- alert signatures: ET MALWARE Observed Win32/Lumma Stealer Related Domain (whitepepper .su) in TLS SNI — 16 events [lumma_stealer-06#0]
- alert signatures: ET DNS Query for .su TLD (Soviet Union) Often Malware Related — 10 events [lumma_stealer-06#0]
- alert signatures: ET MALWARE Win32/Lumma Stealer Related CnC Domain in DNS Lookup (whitepepper .su) — 10 events [lumma_stealer-06#0]
- alert signatures: ET INFO Microsoft Connection Test — 1 events [lumma_stealer-06#2]
- alert signatures: ET MALWARE Lumma Stealer Victim Fingerprinting Activity — 1 events [lumma_stealer-06#2]
- alert signatures: ET MALWARE Observed Win32/Lumma Stealer Related Domain (whooptm .cyou) in TLS SNI — 1 events [lumma_stealer-06#2]
- high severity alerts: 51 matching events [lumma_stealer-06#2]
- high severity alerts > high severity sources: 10.1.21.58 — 50 events [lumma_stealer-06#6]
- high severity alerts > high severity sources: 80.97.160.24 — 1 events [lumma_stealer-06#6]
- high severity alerts > high severity signatures: ET DNS Query for .cc TLD — 4 events [lumma_stealer-06#5]

## Initial Infection Indicators

- http requests: no_http_uri — 296 events [lumma_stealer-01#3]
- http requests: 10.1.21.58 -> 153.92.1.49:80 : /api/set_agent?id=3BF67EC05320C5729578BE4C0ADF174C&token=842e2802df0f0a06b4ed51f12f4387e761523b&description=&agent=Chrome — 4 events [lumma_stealer-01#3]
- http requests: 10.1.21.58 -> 153.92.1.49:80 : /favicon.ico — 4 events [lumma_stealer-01#3]
- http requests: 10.1.21.58 -> 153.92.1.49:80 : /api/set_agent?id=3BF67EC05320C5729578BE4C0ADF174C&token=842e2802df0f0a06b4ed51f12f4387e761523b&description=&agent=Edge — 3 events [lumma_stealer-01#3]
- file transfers > transfer details: 10.1.21.58 -> 150.171.22.17:443 : fuid: FaDmmHcV5jyduC2qe — 1 events [lumma_stealer-01#1]
- file transfers > transfer details: 10.1.21.58 -> 150.171.27.11:443 : fuid: F9LinC1gk6l6ZiHI1h — 1 events [lumma_stealer-01#1]
- domains: communicationfirewall-security.cc — 2 events; top source ips: 10.1.21.58 (2); top destination ips: 104.21.9.36 (2) [lumma_stealer-07#1]
- domains: img-s-msn-com.akamaized.net — 2 events; top source ips: 10.1.21.58 (2); top destination ips: 23.55.178.217 (2) [lumma_stealer-07#1]
- domains: holiday-forever.cc — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 80.97.160.24 (1) [lumma_stealer-07#1]
- domains: media.megafilehub4.lat — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 104.21.48.156 (1) [lumma_stealer-07#1]
- download domains: whitepepper.su — 6 events [lumma_stealer-01#5]
- download domains: clients2.google.com — 1 events [lumma_stealer-01#5]
- download domains: www.msftconnecttest.com — 1 events [lumma_stealer-01#5]
- file types: other — 312 events [lumma_stealer-01#5]

## Command-and-Control and Network Activity

- domains: ssl.gstatic.com — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 172.217.72.94 (1) [lumma_stealer-07#2]
- domains: static.cloudflareinsights.com — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 104.16.79.73 (1) [lumma_stealer-07#2]
- domains: whooptm.cyou — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 62.72.32.156 (1) [lumma_stealer-07#2]
- domains: www.gstatic.com — 1 events; top source ips: 10.1.21.58 (1); top destination ips: 142.251.116.94 (1) [lumma_stealer-07#2]
- domains: whitepepper.su — 16 events; top source ips: 10.1.21.58 (16); top destination ips: 153.92.1.49 (16) [lumma_stealer-07#0]
- domains: assets.adobedtm.com — 2 events; top source ips: 10.1.21.58 (2); top destination ips: 184.29.31.84 (2) [lumma_stealer-07#0]
- domains: cdnjs.cloudflare.com — 2 events; top source ips: 10.1.21.58 (2); top destination ips: 104.17.25.14 (2) [lumma_stealer-07#0]
- domains: cloudflare-ech.com — 2 events; top source ips: 10.1.21.58 (2); top destination ips: 104.21.22.231 (1), 104.21.46.67 (1) [lumma_stealer-07#0]

## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [lumma_stealer-09#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [lumma_stealer-09#0]
3. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [lumma_stealer-09#0]
4. Not established from the available artifacts.
5. Derived: internal client 10.1.21.58 ranks #1 by external connections (312 events, 57 distinct external destinations). Most-contacted external IP: 153.92.1.49 (91 connections). [lumma_stealer-08#0]
6. Derived: Kerberos identity of 10.1.21.58: hostname(s) desktop-es9f3ml; human user account(s) gwyatt. [lumma_stealer-08#0]
7. Derived: Suricata alerts span 2026-01-27 23:00 UTC to 2026-01-27 23:00 UTC; earliest alert hour 2026-01-27 23:00 UTC (70 alerts). [lumma_stealer-08#0]
