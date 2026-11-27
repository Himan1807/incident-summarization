# Incident Postmortem: Network security incident investigation

## Incident Summary

- The incident affected the internal host 10.1.17.215, with the hostname desktop-l8c5gsj and the user account shutchenson. [fake_auth-04#2, fake_auth-04#3, fake_auth-03#0]
- The earliest signs of infection activity were detected at 2025-01-22 19:00 UTC. [auto: fake_auth-09#0, fake_auth-06#4]
- The main external IP candidate for command-and-control (C2) activity was 5.252.153.241, with 1196 connections from the internal client. [fake_auth-01#2]
- The key assessment is that the internal client 10.1.17.215 communicated with various external services, but clear evidence of C2 activity is not established. [fake_auth-02#0, fake_auth-08#2, fake_auth-08#3]

## Affected Host and User

- Affected Host: 10.1.17.215, hostname: desktop-l8c5gsj, human user account: shutchenson [fake_auth-09#0, fake_auth-05#0, fake_auth-04#3, fake_auth-04#2, fake_auth-04#0, fake_auth-04#1]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

- ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events [fake_auth-06#1]
- ET INFO Observed UA-CPU Header — 1 events [fake_auth-06#1]
- ET REMOTE_ACCESS TeamViewer RMM Domain (teamviewer .com) in DNS Lookup — 1 events [fake_auth-06#1]
- High severity alerts: 8 matching events [fake_auth-06#1, fake_auth-06#2, fake_auth-06#3, fake_auth-06#4]
- High severity destinations: 5.252.153.241 — 4 events [fake_auth-06#2]
- High severity destinations: 10.1.17.215 — 2 events [fake_auth-06#2]
- High severity destinations: 185.188.32.26 — 2 events [fake_auth-06#2]
- High severity sources: 45.125.66.32 — 1 events [fake_auth-06#4]
- High severity sources: 45.125.66.252 — 1 events [fake_auth-06#4]

## Initial Infection Indicators

- [fake_auth-01#1] Download domains: ctldl.windowsupdate.com, www.msftconnecttest.com, au.download.windowsupdate.com (2, 2, 1 events respectively)
- [fake_auth-01#0] Download domains: 5.252.153.241, master16.teamviewer.com, msedge.b.tlu.dl.delivery.mp.microsoft.com, download.windowsupdate.com (594, 21, 4, 3 events respectively)
- [fake_auth-01#2] HTTP requests: 10.1.17.215 -> 5.252.153.241:80 (584 events)
- [fake_auth-01#4] HTTP requests: 10.1.17.215 -> 185.188.32.26:80 (2 events)
- [fake_auth-01#6] File transfers: 10.1.17.215 -> 13.107.21.239:443, 13.107.42.14:443, 13.71.55.58:443 (1, 1, 1 event respectively)

## Command-and-Control and Network Activity

- Internal client 10.1.17.215 made 1823 external connections, with 119 distinct external destinations. [fake_auth-09#0]
- The most contacted external IP was 5.252.153.241, with 1196 connections. [fake_auth-09#0]
- Suricata alerts were generated between 2025-01-22 19:00 UTC and 2025-01-22 20:00 UTC, with the earliest alert at 2025-01-22 19:00 UTC. [fake_auth-02#0]
- High-severity alerts were directed to 5.252.153.241 (4 alerts), 10.1.17.215 (2 alerts), and 185.188.32.26 (2 alerts). [fake_auth-02#0]
- The domain c.go-mpulse.net was contacted once, with 10.1.17.215 as the source IP and 23.207.164.186 as the destination IP. [fake_auth-08#2]
- The domain dmpsync.3lift.com was contacted once, with 10.1.17.215 as the source IP and 35.71.139.29 as the destination IP. [fake_auth-08#3]
- The domain dpm.demdex.net was contacted once, with 10.1.17.215 as the source IP and 52.32.135.66 as the destination IP. [fake_auth-08#2]
- The domain ds.reson8.com was contacted once, with 10.1.17.215 as the source IP and 104.18.8.76 as the destination IP. [fake_auth-08#2]
- Assessment: The evidence does not provide clear indications of command-and-control activity, but rather suggests that the internal client 10.1.17.215 may be communicating with various external services. [fake_auth-09#0, fake_auth-02#0, fake_auth-08#2, fake_auth-08#3]

## Impact Assessment

- Assessment: The primary CIA component targeted was availability, as evidenced by the high volume of external connections from the internal client 10.1.17.215, which could potentially lead to network congestion or resource exhaustion. [fake_auth-02#0]
- Assessment: The scale of external activity was significant, with 1823 events from the internal client 10.1.17.215 connecting to 119 distinct external IP addresses, primarily targeting 5.252.153.241. [fake_auth-02#0]
- Assessment: The impact on availability was further supported by the presence of high-severity alerts, particularly those related to Spamhaus DROP Listed Traffic Inbound, indicating potential disruptions to network services. [fake_auth-06#2]
- Assessment: The activity spanned a short timeframe, with the earliest alert occurring at 2025-01-22 19:00 UTC and the latest at 2025-01-22 20:00 UTC, suggesting a concentrated period of malicious activity. [fake_auth-06#4]
- Assessment: The domains accessed, such as oneclient.sfx.ms and img-s-msn-com.akamaized.net, indicate potential data exfiltration or command-and-control communications, though direct evidence of such activities is not established from the available artifacts. [fake_auth-08#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is the compromise of the internal client 10.1.17.215, which was likely exploited through a Kerberos authentication mechanism. This is supported by the high number of Kerberos-related alerts and the Kerberos identity of the client. The external connections to 5.252.153.241 and other IPs suggest that the client was used as a vector for further network activity. [auto: fake_auth-09#0, fake_auth-02#0]
- Not established: The initial vector used to compromise 10.1.17.215 is not established.
- Not established: The exact payload or malware used in the attack is not established.
- Not established: The extent of data exfiltration, if any, is not established.
- Not established: The purpose or commands sent to 10.1.17.215 from the external IP addresses are not established.
- Not established: The success or failure of the HTTP requests to external IPs is not established.
- Not established: The full impact on the internal network, including any lateral movement or further compromise of other hosts, is not established.

## Corrective and Preventive Actions

- Isolate host 10.1.17.215 to prevent further external connections and internal propagation. [auto: fake_auth-09#0, fake_auth-08#3]
- Reset the account shutchenson to remove any potential malware or unauthorized access.
- Block the IP address 5.252.153.241 to prevent communication with the identified command-and-control server. [auto: fake_auth-09#0, fake_auth-01#2]
- Monitor and log all HTTP requests from 10.1.17.215 to detect any further malicious activities. [auto: fake_auth-09#0, fake_auth-08#3]

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 10.1.17.215 [fake_auth-09#0].
2. The hostname of the potentially infected machine in the LAN is desktop-l8c5gsj [fake_auth-05#0, fake_auth-04#2, fake_auth-04#3].
3. The Windows human user account name of the potentially infected machine in the LAN is shutchenson [fake_auth-03#0].
4. The likely fake or suspicious domains/URLs for initial infection are c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, and ds.reson8.com [fake_auth-08#2].
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 5.252.153.241, 185.188.32.26, and 45.125.66.32, 45.125.66.252 [fake_auth-06#2, fake_auth-07#0, fake_auth-07#1].
6. The first signs of infection activity appeared during the hour 2025-01-22 19:00 UTC [fake_auth-06#4].
7. Suspicious certificates were observed in the encrypted network traffic. The domain or IP in the certificate is 45.125.66.252 and 45.125.66.32 [fake_auth-07#0, fake_auth-07#1]. Not established from the available artifacts regarding whether the IP 5.252.153.241 or 185.188.32.26 is a C2 server or a legitimate service.

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
