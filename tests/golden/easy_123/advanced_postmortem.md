# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 10.2.28.88 ranks #1 by external connections (1539 events, 95 distinct external destinations). Most-contacted external IP: 45.131.214.85 (1061 connections). [easy_123-08#0]
- Derived: Kerberos identity of 10.2.28.88: hostname(s) desktop-teyq2nr; human user account(s) brolf. [easy_123-08#0]
- Derived: Suricata alerts span 2026-02-28 19:00 UTC to 2026-03-01 00:00 UTC; earliest alert hour 2026-02-28 19:00 UTC (28 alerts). [easy_123-08#0]
- Derived: destinations of high-severity alerts: 45.131.214.85 (264). [easy_123-08#0]
- client accounts: brolf — 8 events; source ips: 10.2.28.88 (8) [easy_123-03#0]
- source clients: 10.2.28.88 — 1539 events; external destinations=95; top destinations: 45.131.214.85 (1061), 150.171.28.11 (38), 150.171.27.11 (15), 23.218.232.148 (14), 23.192.223.17 (13); 398 further events in other values [easy_123-02#0]
- file transfers: 598 matching events [easy_123-01#0]
- file transfers > transfer details: file_transfer — 273 events [easy_123-01#0]
- file transfers > transfer details: 10.2.28.88 -> 13.70.79.200:443 : fuid: F95H6kTOV7Ac6bcve — 1 events [easy_123-01#0]
- file transfers > transfer details: 10.2.28.88 -> 13.89.178.27:443 : fuid: Fjm5jt1kCVqVQ0zXsb — 1 events [easy_123-01#0]
- full services: krb_tcp — 8 events; source ips: 10.2.28.88 (8) [easy_123-04#0]
- full services: krbtgt/EASYAS123.TECH — 2 events; source ips: 10.2.28.88 (2) [easy_123-04#0]
- full services: LDAP/EASYAS123-DC.easyas123.tech/easyas123.tech — 1 events; source ips: 10.2.28.88 (1) [easy_123-04#0]
- full services: cifs/EASYAS123-DC — 1 events; source ips: 10.2.28.88 (1) [easy_123-04#0]
- domains: www.fmcsa.dot.gov — 1 events; top source ips: 10.2.28.88 (1); top destination ips: 23.64.147.24 (1) [easy_123-07#1]

## Timeline

- 2026-02-28 19:00 UTC — alert timeline: 28 events; earliest alert hour [easy_123-06#2, easy_123-08#0]
- 2026-02-28 20:00 UTC — alert timeline: 119 events [easy_123-06#2]
- 2026-02-28 21:00 UTC — alert timeline: 120 events [easy_123-06#2]
- 2026-02-28 22:00 UTC — alert timeline: 120 events [easy_123-06#3]
- 2026-02-28 23:00 UTC — alert timeline: 120 events [easy_123-06#3]
- 2026-03-01 00:00 UTC — alert timeline: 36 events [easy_123-06#3]

## Detection: IDS Alerts

- alert signatures: ET INFO HTTP traffic on port 443 (POST) — 264 events [easy_123-06#0]
- alert signatures: ET REMOTE_ACCESS NetSupport Remote Admin Checkin — 264 events [easy_123-06#0]
- alert signatures: ET JA3 Hash - Possible SoftEther Windows Client SSTP Traffic — 12 events [easy_123-06#0]
- alert signatures: ET REMOTE_ACCESS NetSupport Remote Admin Response — 2 events [easy_123-06#0]
- alert signatures: ET INFO Microsoft Connection Test — 1 events [easy_123-06#1]
- high severity alerts: 264 matching events [easy_123-06#1]
- high severity alerts > high severity  destinations: 45.131.214.85 — 264 events [easy_123-06#1]
- high severity alerts > high severity sources: 10.2.28.88 — 264 events [easy_123-06#2]

## Initial Infection Indicators

- download domains: www.msftconnecttest.com — 1 events [easy_123-01#7]
- file types: other — 1539 events [easy_123-01#7]
- download domains: ctldl.windowsupdate.com — 9 events [easy_123-01#6]
- download domains: ocsp.digicert.com — 2 events [easy_123-01#6]
- download domains: acroipm2.adobe.com — 1 events [easy_123-01#6]
- download domains: edge.microsoft.com — 1 events [easy_123-01#6]
- http requests: 10.2.28.88 -> 150.171.27.11:80 : /browsernetworktime/time/1/current?cup2key=2:cHFgppt5zfs9cbgaKCO2n0tk698hI27wU971tyrEQQg&cup2hreq=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 — 1 events [easy_123-01#5]
- http requests: 10.2.28.88 -> 199.232.210.172:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?238f51c2ab526be6 — 1 events [easy_123-01#5]
- download domains: 45.131.214.85 — 264 events [easy_123-01#5]
- download domains: msedge.b.tlu.dl.delivery.mp.microsoft.com — 30 events [easy_123-01#5]
- http requests: no_http_uri — 1230 events [easy_123-01#3]
- http requests: 10.2.28.88 -> 45.131.214.85:443 : http://45.131.214.85/fakeurl.htm — 264 events [easy_123-01#3]
- http requests: 10.2.28.88 -> 23.218.232.148:80 : /filestreamingservice/files/2132f61f-f790-4ae6-a355-8cf9a1533800?P1=1772824359&P2=404&P3=2&P4=JBAPgdPQ5bbXP3YOD9Ig2AVW51pLa6vxUcHeGTEAadbzNEO5DlV3Wra1C9WqE7WnEd5RG1oYpt8saZgMxML1KA== — 11 events [easy_123-01#3]
- http requests: 10.2.28.88 -> 23.218.232.166:80 : /filestreamingservice/files/13d0ef9b-70c8-43c9-9a51-13c752dfb777?P1=1772817857&P2=404&P3=2&P4=NxsPWDqY/PRN4X5tyugkA+dfU9EeHebHQ3SqTAWWr5XPVngvgEZDtSFAEYlah9GHFrc+S/ExNx3X0xGxvdOPow== — 7 events [easy_123-01#3]

## Command-and-Control and Network Activity

- file transfers > transfer details: 10.2.28.88 -> 150.171.27.11:443 : fuid: FPHQiS2gqfclBOrFL9 — 1 events [easy_123-01#2]
- download sources: 10.2.28.88 — 1539 events [easy_123-01#2]

## Impact Assessment

- file transfers > transfer details: 10.2.28.88 -> 13.89.179.14:443 : fuid: F3leWR1jXmw5eIV2n4 — 1 events [easy_123-01#1]
- file transfers > transfer details: 10.2.28.88 -> 13.89.179.9:443 : fuid: FpfWem1XHYB3V7Z3Kb — 1 events [easy_123-01#1]
- file transfers > transfer details: 10.2.28.88 -> 135.234.160.246:443 : fuid: F06TIy3seFMGIoCz69 — 1 events [easy_123-01#1]
- file transfers > transfer details: 10.2.28.88 -> 150.171.22.17:443 : fuid: FApV0N3DxwzTiwATnl — 1 events [easy_123-01#1]
- http requests: 10.2.28.88 -> 23.218.232.183:80 : /filestreamingservice/files/86061e48-63b3-483f-8dac-609df0cbb238?P1=1772824359&P2=404&P3=2&P4=M+r84JmdgFPOKPdw6GuIsCbfL0IaRRxCYqeiJbpH9IpxZr7vLbM4w9K8uMU5Ka6CyN/uMqIEMlyIHqGqCS8/Xg== — 6 events [easy_123-01#4]
- http requests: 10.2.28.88 -> 23.218.232.142:80 : /filestreamingservice/files/0b18f766-7469-4aa3-88b7-99e69c55d14d?P1=1772628813&P2=404&P3=2&P4=P9O/ZqV3zHEog/8GWjY1LjxEXlCShXCmvVwfgCjP6c7Xjf6q9SdV5Cxrlht3k8c6RsZdgDSm48GRm8J1Kej36Q== — 3 events [easy_123-01#4]
- http requests: 10.2.28.88 -> 23.218.232.142:80 : /filestreamingservice/files/ddbf4492-d475-4fe4-bcde-6cbac56f6034?P1=1772824359&P2=404&P3=2&P4=TMSkemQv9LZfDxme9Q9GxU0tc2G9uhdO6d7QU9JVJHOk+a0A4pJYzApqbFnNEQ6bt9QSukbCYOxGUmPIOR1Xgw== — 3 events [easy_123-01#4]
- http requests: 10.2.28.88 -> 23.47.50.182:80 : /connecttest.txt — 2 events [easy_123-01#4]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [easy_123-09#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [easy_123-09#0]
3. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [easy_123-09#0]
4. Not established from the available artifacts.
5. Derived: internal client 10.2.28.88 ranks #1 by external connections (1539 events, 95 distinct external destinations). Most-contacted external IP: 45.131.214.85 (1061 connections). [easy_123-08#0]
6. Derived: Kerberos identity of 10.2.28.88: hostname(s) desktop-teyq2nr; human user account(s) brolf. [easy_123-08#0]
