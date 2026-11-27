# Incident Postmortem: Network security incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: internal client 172.16.1.137 ranks #1 by external connections (311 events, 50 distinct external destinations). Most-contacted external IP: 62.173.138.138 (26 connections). [gozi-08#0]
- Derived: Kerberos identity of 172.16.1.137: hostname(s) desktop-3gjl3pv; human user account(s) sherita.kolb. [gozi-08#0]
- Derived: Suricata alerts span 2023-03-07 02:00 UTC to 2023-03-07 02:00 UTC; earliest alert hour 2023-03-07 02:00 UTC (72 alerts). [gozi-08#0]
- Derived: destinations of high-severity alerts: 62.173.138.138 (12), 46.8.19.86 (6), 46.8.19.233 (6), 62.173.140.76 (6), 62.173.149.243 (6). [gozi-08#0]
- source clients: 172.16.1.137 — 311 events; external destinations=50; top destinations: 62.173.138.138 (26), 20.190.159.70 (24), 104.106.121.142 (18), 62.173.149.243 (15), 46.8.19.233 (12); 216 further events in other values [gozi-02#0]
- download domains: unapromo.com — 1 events [gozi-01#3]
- download domains: x1.c.lencr.org — 1 events [gozi-01#3]
- http requests: no_http_uri — 212 events [gozi-01#3]
- http requests: 172.16.1.137 -> 62.173.138.138:80 : /drew/uyoXjOLPocMIEKrQlytVaWB/N_2BJo4B1_/2BB8gjy1qo0bUbbKw/vIwLAJ4RuKN1/oCn1JQTfr8y/h_2BXw2JtDeVTV/csllhDtxntvdGZ0FyWsDv/fSjE8DiuaKWiQWY0/KObd8_2FyOCBEgg/RVIw8Nxnyvxjh6Qphy/yOa05BVTB/myKLdYqv5xhF3cKw_2Bk/…[truncated] — 9 events [gozi-01#3]
- client accounts: desktop-3gjl3pv$ — 12 events; source ips: 172.16.1.137 (12) [gozi-03#0]
- client accounts: DESKTOP-3GJL3PV$ — 11 events; source ips: 172.16.1.137 (11) [gozi-03#0]
- client accounts: sherita.kolb — 8 events; source ips: 172.16.1.137 (8) [gozi-03#0]
- full services: cifs/PCAPWORKSHOP-DC.pcapworkshop.net — 2 events; source ips: 172.16.1.137 (2) [gozi-04#1]
- full services: krbtgt/PCAPWORKSHOP — 2 events; source ips: 172.16.1.137 (2) [gozi-04#1]
- full services: ldap/pcapworkshop-dc.pcapworkshop.net/pcapworkshop.net — 2 events; source ips: 172.16.1.137 (2) [gozi-04#1]
- full services: LDAP/PCAPWORKSHOP-DC.pcapworkshop.net — 1 events; source ips: 172.16.1.137 (1) [gozi-04#1]
- domains: fonts.gstatic.com — 2 events; top source ips: 172.16.1.137 (2); top destination ips: 142.251.143.163 (2) [gozi-07#0]
- domains: www.gstatic.com — 1 events; top source ips: 172.16.1.137 (1); top destination ips: 142.251.143.195 (1) [gozi-07#0]

## Timeline

- 2023-03-07 02:00 UTC — alert timeline: 72 events; earliest alert hour [gozi-06#6, gozi-08#0]

## Detection: IDS Alerts

- alert signatures: ET MALWARE Ursnif Variant CnC Data Exfil — 2 events [gozi-06#2]
- alert signatures: ET INFO NTLMv1 Session Setup Response - Challenge — 1 events [gozi-06#2]
- alert signatures: ET MALWARE Ursnif Payload Request (cook32.rar) — 1 events [gozi-06#2]
- alert signatures: ET MALWARE Ursnif Variant CnC Beacon - URI Struct M1 (_2B) — 25 events [gozi-06#0]
- alert signatures: ET MALWARE Ursnif Variant CnC Beacon - URI Struct M2 (_2F) — 23 events [gozi-06#0]
- alert signatures: GPL NETBIOS SMB IPC$ unicode share access — 6 events [gozi-06#0]
- alert signatures: ET INFO Dotted Quad Host RAR Request — 4 events [gozi-06#0]
- alert signatures: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 — 3 events [gozi-06#1]
- alert signatures: ET INFO NTLM Session Setup Request - Auth — 2 events [gozi-06#1]
- alert signatures: ET MALWARE Ursnif Variant CnC Beacon 3 — 2 events [gozi-06#1]
- high severity alerts > high severity signatures: ET MALWARE Ursnif Payload Request (cook64.rar) — 1 events [gozi-06#6]
- high severity alerts > high severity sources: 172.16.1.137 — 61 events [gozi-06#6]

## Initial Infection Indicators

- download domains: 62.173.138.138 — 6 events [gozi-01#0]
- download domains: 46.8.19.233 — 4 events [gozi-01#0]
- download domains: 62.173.149.243 — 4 events [gozi-01#0]
- download domains: 46.8.19.86 — 3 events [gozi-01#0]
- download domains: 62.173.140.103 — 3 events [gozi-01#1]
- download domains: 62.173.140.76 — 3 events [gozi-01#1]
- download domains: 62.173.140.94 — 3 events [gozi-01#1]
- download domains: 31.41.44.49 — 2 events [gozi-01#1]
- download domains: 31.41.44.60 — 2 events [gozi-01#2]
- download domains: 5.44.45.201 — 2 events [gozi-01#2]
- download domains: 89.116.236.41 — 2 events [gozi-01#2]
- download domains: ctldl.windowsupdate.com — 2 events [gozi-01#2]
- http requests: 172.16.1.137 -> 62.173.149.243:80 : /stilak32.rar — 7 events [gozi-01#4]
- http requests: 172.16.1.137 -> 62.173.140.103:80 : /drew/Q0EmvhskDMeV_2B/hlZqNxHPY3pA7HNxtL/9pXV5RDXP/1ncHG7VUfpdi2hExi3M2/zb3SUbdKsAKR2OShwxw/qjnkZ5oqJv4hT6UPNNZkp1/2f6D94TlCm0xb/gmA0CcmM/phrug73V9foNtM3B11vM5jg/rA7X6ZhzBR/p4_2FAte6kcuk_2Bm/Xtm1EnGCcDgj/…[truncated] — 6 events [gozi-01#4]
- http requests: 172.16.1.137 -> 46.8.19.233:80 : /drew/KU4sSnNPGqF6dYVU/zMqg5LcUpXWHQk4/p13TzrSaxnS204Iq07/xA1Orx2tR/0Mx7AucADFBXLarjDT_2/F6QVzfPmw6J4yJohUa_/2FwRbcVk37yP9QCm8T_2FY/tqTLVPzL1l9MI/Hp0oDTGP/yycBFCiKitaSE7y0P_2FF9B/WAmReIx3ov/DMiE0A8aFFKYTDfeS…[truncated] — 5 events [gozi-01#4]
- http requests: 172.16.1.137 -> 46.8.19.86:80 : /drew/87Kol3wsW64/XzUI9sN5W8mEJo/Ry4an4JvksM8Ymx60M6o5/PQtzODDyH1TG1TtY/8vNIghEJJhKHPdL/gvYCzkuSkLZDTME_2B/cpQiO3HFc/1uU4Badum_2FGmMnE2Sm/jmTcOwcinRYLnKFzinH/QZDuBdGarUZTBgmcGsNyb0/qJGDHvwvJi7TX/u7kjTOlL/jXSV…[truncated] — 5 events [gozi-01#4]
- file transfers: 67 matching events [gozi-01#6]
- file transfers > transfer details: file_transfer — 14 events [gozi-01#6]
- file transfers > transfer details: 172.16.1.137 -> 104.106.107.237:443 : fuid: FzQMvC25dCy0cXTFie — 1 events [gozi-01#6]
- file transfers > transfer details: 172.16.1.137 -> 104.106.121.142:443 : fuid: F080o93E1PwtbhTVEe — 1 events [gozi-01#6]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- file transfers > transfer details: 172.16.1.137 -> 104.126.37.131:443 : fuid: FRA5P832XpFo1sZ939 — 1 events [gozi-01#8]
- file transfers > transfer details: 172.16.1.137 -> 104.126.37.139:443 : fuid: Fo3nAE7DATNDRmwKl — 1 events [gozi-01#8]
- file types: other — 306 events [gozi-01#8]

## Corrective and Preventive Actions

- full services: krb_tcp — 31 events; source ips: 172.16.1.137 (31) [gozi-04#0]
- full services: krbtgt/PCAPWORKSHOP.NET — 14 events; source ips: 172.16.1.137 (14) [gozi-04#0]
- full services: krbtgt/pcapworkshop.net — 4 events; source ips: 172.16.1.137 (4) [gozi-04#0]
- full services: DESKTOP-3GJL3PV$ — 2 events; source ips: 172.16.1.137 (2) [gozi-04#0]

## Answers to Investigation Questions

1. No matching results for: suspicious certificates / self signed analysis. (Absence in this query is not proof of absence elsewhere.) [gozi-09#0]
2. No matching results for: suspicious certificates / ip based certificates. (Absence in this query is not proof of absence elsewhere.) [gozi-09#0]
3. No matching results for: suspicious certificates / short validity certs. (Absence in this query is not proof of absence elsewhere.) [gozi-09#0]
4. Not established from the available artifacts.
5. Derived: Kerberos identity of 172.16.1.137: hostname(s) desktop-3gjl3pv; human user account(s) sherita.kolb. [gozi-08#0]
6. Derived: Suricata alerts span 2023-03-07 02:00 UTC to 2023-03-07 02:00 UTC; earliest alert hour 2023-03-07 02:00 UTC (72 alerts). [gozi-08#0]
7. Derived: destinations of high-severity alerts: 62.173.138.138 (12), 46.8.19.86 (6), 46.8.19.233 (6), 62.173.140.76 (6), 62.173.149.243 (6). [gozi-08#0]
8. Not established from the available artifacts.
9. client accounts: desktop-3gjl3pv$ — 12 events; source ips: 172.16.1.137 (12) [gozi-03#0]
