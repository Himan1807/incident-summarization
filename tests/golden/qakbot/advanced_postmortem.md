# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.0.0.149 ranks #1 by external connections (811 events, 98 distinct external destinations). Most-contacted external IP: 208.187.122.74 (237 connections). [qakbot-09#0]
- Derived: Kerberos identity of 10.0.0.149: hostname(s) desktop-e7fhjs4; human user account(s) damon.bauer. [qakbot-09#0]
- Derived: Suricata alerts span 2023-02-03 17:00 UTC to 2023-02-03 19:00 UTC; earliest alert hour 2023-02-03 17:00 UTC (38 alerts). [qakbot-09#0]
- Derived: destinations of high-severity alerts: 10.0.0.6 (17), 10.0.0.149 (8), 78.31.67.7 (1), 128.254.207.55 (1). [qakbot-09#0]
- client accounts: DESKTOP-E7FHJS4$ — 10 events; source ips: 10.0.0.149 (10) [qakbot-03#0]
- client accounts: damon.bauer — 7 events; source ips: 10.0.0.149 (7) [qakbot-03#0]
- client accounts: desktop-e7fhjs4$ — 6 events; source ips: 10.0.0.149 (6) [qakbot-03#0]
- source clients: 10.0.0.149 — 811 events; external destinations=98; top destinations: 208.187.122.74 (237), 13.107.42.14 (28), 209.131.162.45 (24), 204.79.197.239 (19), 72.163.4.185 (18); 485 further events in other values [qakbot-02#0]
- hostnames: desktop-e7fhjs4 — 1 events; source ips: 10.0.0.149 (1) [qakbot-05#0]
- full services: ldap/work4us-dc.work4us.org/work4us.org — 2 events; source ips: 10.0.0.149 (2) [qakbot-04#1]
- full services: DESKTOP-E7FHJS4$ — 1 events; source ips: 10.0.0.149 (1) [qakbot-04#1]
- full services: LDAP/WORK4US-DC.work4us.org/work4us.org — 1 events; source ips: 10.0.0.149 (1) [qakbot-04#1]
- full services: cifs/WORK4US-DC — 1 events; source ips: 10.0.0.149 (1) [qakbot-04#1]
- domains: cisco.com — 9 events; top source ips: 10.0.0.149 (9); top destination ips: 72.163.4.185 (9) [qakbot-08#0]
- domains: www.cisco.com — 9 events; top source ips: 10.0.0.149 (9); top destination ips: 23.64.146.226 (4), 96.6.184.69 (3), 184.51.39.62 (2) [qakbot-08#0]
- domains: verisign.com — 8 events; top source ips: 10.0.0.149 (8); top destination ips: 209.131.162.45 (8) [qakbot-08#0]
- domains: www.verisign.com — 8 events; top source ips: 10.0.0.149 (8); top destination ips: 69.58.187.40 (4), 209.131.162.45 (4) [qakbot-08#0]

## Timeline

- 2023-02-03 17:00 UTC — alert timeline: 38 events; earliest alert hour [qakbot-06#9, qakbot-09#0]
- 2023-02-03 18:00 UTC — alert timeline: 23 events [qakbot-06#9]
- 2023-02-03 19:00 UTC — alert timeline: 67 events [qakbot-06#9]

## Detection: IDS Alerts

- alert signatures: ET MALWARE BackConnect CnC Activity (Set Sleep Timer) — 5 events [qakbot-06#1]
- alert signatures: ET HUNTING SUSPICIOUS Dotted Quad Host MZ Response — 1 events [qakbot-06#1]
- alert signatures: ET INFO DNS Query for Suspicious .ml Domain — 1 events [qakbot-06#1]
- alert signatures: ET MALWARE BackConnect CnC Activity (Start VNC) M1 — 1 events [qakbot-06#4]
- alert signatures: ET MALWARE W32.DarkVNC Variant Checkin — 1 events [qakbot-06#4]
- alert signatures: ET RPC DCERPC SVCCTL - Remote Service Control Manager Access — 1 events [qakbot-06#4]
- high severity alerts: 27 matching events [qakbot-06#4]
- high severity alerts > high severity signatures: ET INFO SMB2 NT Create AndX Request For a DLL File - Possible Lateral Movement — 9 events [qakbot-06#6]
- high severity alerts > high severity signatures: ET INFO SMB Executable File Transfer — 6 events [qakbot-06#6]
- high severity alerts > high severity signatures: ET HUNTING curl User-Agent to Dotted Quad — 1 events [qakbot-06#7]
- high severity alerts > high severity signatures: ET INFO Observed DNS Query to .biz TLD — 1 events [qakbot-06#7]
- alert signatures: ET INFO EXE - Served Attached HTTP — 1 events [qakbot-06#2]
- alert signatures: ET INFO EXE IsDebuggerPresent (Used in Malware Anti-Debugging) — 1 events [qakbot-06#2]
- alert signatures: ET INFO NTLM Session Setup Request - Auth — 1 events [qakbot-06#2]
- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 1 events [qakbot-06#3]
- alert signatures: ET INFO PE EXE or DLL Windows file download HTTP — 1 events [qakbot-06#3]

## Initial Infection Indicators

- download domains: 128.254.207.55 — 1 events [qakbot-01#0]
- download domains: cacerts.digicert.com — 1 events [qakbot-01#0]
- http requests: no_http_uri — 808 events [qakbot-01#0]
- http requests: 10.0.0.149 -> 128.254.207.55:80 : /86607.dat — 2 events [qakbot-01#0]
- http requests: 10.0.0.149 -> 192.229.211.108:80 : /DigiCertTLSRSASHA2562020CA1-1.crt — 1 events [qakbot-01#1]
- file transfers: 39 matching events [qakbot-01#1]
- file transfers > transfer details: file_transfer — 2 events [qakbot-01#1]
- file transfers > transfer details: 10.0.0.149 -> 102.156.32.143:443 : fuid: FqPnVU3bQggnrL7tXg — 1 events [qakbot-01#1]
- file types: other — 810 events [qakbot-01#4]
- file types: exe — 1 events [qakbot-01#4]
- download sources: 10.0.0.149 — 811 events [qakbot-01#4]
- file transfers > transfer details: 10.0.0.149 -> 104.208.16.89:443 : fuid: FlI50x23MLhHuAO9o1 — 1 events [qakbot-01#2]
- file transfers > transfer details: 10.0.0.149 -> 128.254.207.55:80 : fuid: FcP6lP1ihIumwPgiFb — 1 events [qakbot-01#2]
- file transfers > transfer details: 10.0.0.149 -> 13.107.237.57:443 : fuid: Ft1sAb28nmiasL6AUd — 1 events [qakbot-01#2]
- file transfers > transfer details: 10.0.0.149 -> 13.107.42.16:443 : fuid: Ffj4qy4nEei2wfVkdc — 1 events [qakbot-01#2]
- domains: oracle.com — 6 events; top source ips: 10.0.0.149 (6); top destination ips: 138.1.33.162 (6) [qakbot-08#1]
- domains: www.oracle.com — 6 events; top source ips: 10.0.0.149 (6); top destination ips: 104.93.55.25 (3), 72.247.204.96 (2), 23.2.51.218 (1) [qakbot-08#1]
- domains: irs.gov — 5 events; top source ips: 10.0.0.149 (5); top destination ips: 152.216.7.110 (5) [qakbot-08#1]
- domains: broadcom.com — 4 events; top source ips: 10.0.0.149 (4); top destination ips: 52.13.171.212 (4) [qakbot-08#1]

## Command-and-Control and Network Activity

- domains: www.xfinity.com — 2 events; top source ips: 10.0.0.149 (2); top destination ips: 184.86.169.24 (2) [qakbot-08#3]
- domains: xfinity.com — 2 events; top source ips: 10.0.0.149 (2); top destination ips: 68.87.41.40 (2) [qakbot-08#3]
- domains: afdxtest.z01.azurefd.net — 1 events; top source ips: 10.0.0.149 (1); top destination ips: 13.107.237.57 (1) [qakbot-08#3]
- domains: www.openssl.org — 1 events; top source ips: 10.0.0.149 (1); top destination ips: 184.28.39.150 (1) [qakbot-08#3]
- domains: www.broadcom.com — 4 events; top source ips: 10.0.0.149 (4); top destination ips: 172.64.155.106 (4) [qakbot-08#2]
- domains: www.irs.gov — 4 events; top source ips: 10.0.0.149 (4); top destination ips: 23.214.54.85 (3), 23.210.67.195 (1) [qakbot-08#2]
- domains: ferlintiozzo.com — 2 events; top source ips: 10.0.0.149 (2); top destination ips: 185.2.4.16 (2) [qakbot-08#2]
- domains: toshak.com — 2 events; top source ips: 10.0.0.149 (2); top destination ips: 88.135.68.140 (2) [qakbot-08#2]

## Impact Assessment

- alert signatures: ET JA3 Hash - [Abuse.ch] Possible Dridex — 87 events [qakbot-06#0]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 7 events [qakbot-06#0]

## Root Cause and Evidence Gaps

- file transfers > transfer details: 10.0.0.149 -> 13.69.239.74:443 : fuid: F5MUCA4iGj72ktLt41 — 1 events [qakbot-01#3]
- file transfers > transfer details: 10.0.0.149 -> 13.89.179.10:443 : fuid: FdA7rK1PfXltNfOGfd — 1 events [qakbot-01#3]
- file transfers > transfer details: 10.0.0.149 -> 13.91.16.69:443 : fuid: FuEOMu4Y92Lo1NZIV9 — 1 events [qakbot-01#3]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [qakbot-10#0]
2. Derived: internal client 10.0.0.149 ranks #1 by external connections (811 events, 98 distinct external destinations). Most-contacted external IP: 208.187.122.74 (237 connections). [qakbot-09#0]
3. Derived: Kerberos identity of 10.0.0.149: hostname(s) desktop-e7fhjs4; human user account(s) damon.bauer. [qakbot-09#0]
4. Not established from the available artifacts.
5. Derived: destinations of high-severity alerts: 10.0.0.6 (17), 10.0.0.149 (8), 78.31.67.7 (1), 128.254.207.55 (1). [qakbot-09#0]
6. hostnames: desktop-e7fhjs4 — 1 events; source ips: 10.0.0.149 (1) [qakbot-05#0]
7. client accounts: DESKTOP-E7FHJS4$ — 10 events; source ips: 10.0.0.149 (10) [qakbot-03#0]
8. Not established from the available artifacts.
