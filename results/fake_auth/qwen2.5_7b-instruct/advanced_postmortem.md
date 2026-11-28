# Incident Postmortem: Network security incident investigation

## Incident Summary

The incident began at 2025-01-22 19:00 UTC, with the earliest alert for the internal host 10.1.17.215, hostname desktop-l8c5gsj, and user account shutchenson. The host made 1823 connections to 119 distinct external destinations, with 5.252.153.241 being the most contacted IP. High-severity alerts were generated, indicating potential compromise and external communication. Assessment: The primary impact was on network availability due to the high volume of external connections. [fake_auth-09#0]

## Affected Host and User

- Affected Host: 10.1.17.215, hostname: desktop-l8c5gsj, human user account: shutchenson [fake_auth-09#0, fake_auth-05#0, fake_auth-04#3, fake_auth-04#2, fake_auth-04#0, fake_auth-04#1]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

- ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events [fake_auth-06#1]
- ET INFO Observed UA-CPU Header — 1 events [fake_auth-06#1]
- ET REMOTE_ACCESS TeamViewer RMM Domain (teamviewer .com) in DNS Lookup — 1 events [fake_auth-06#1]
- ET DROP Spamhaus DROP Listed Traffic Inbound group 5 — 2 events [fake_auth-06#2]
- High severity alerts: 8 matching events [fake_auth-06#2]
- High severity alerts > high severity destinations: 5.252.153.241 — 4 events [fake_auth-06#2]
- High severity alerts > high severity destinations: 10.1.17.215 — 2 events [fake_auth-06#2]
- High severity alerts > high severity destinations: 185.188.32.26 — 2 events [fake_auth-06#2]
- High severity alerts > high severity sources: 45.125.66.32 — 1 events [fake_auth-06#4]
- High severity alerts > high severity sources: 45.125.66.252 — 1 events [fake_auth-06#4]
- High severity alerts > high severity signatures: ET INFO PS1 Powershell File Request — 2 events [fake_auth-06#3]
- High severity alerts > high severity signatures: ET INFO TeamViewer Dyngate User-Agent — 2 events [fake_auth-06#3]

## Initial Infection Indicators

- [fake_auth-01#1] Download domains: ctldl.windowsupdate.com, www.msftconnecttest.com, au.download.windowsupdate.com (2, 2, 1 events respectively)
- [fake_auth-01#0] Download domains: 5.252.153.241, master16.teamviewer.com, msedge.b.tlu.dl.delivery.mp.microsoft.com, download.windowsupdate.com (594, 21, 4, 3 events respectively)
- [fake_auth-01#2] HTTP requests: 10.1.17.215 -> 5.252.153.241:80 (584 events)
- [fake_auth-01#4] HTTP requests: 10.1.17.215 -> 185.188.32.26:80 (2 events)
- [fake_auth-01#6] File transfers: 10.1.17.215 -> 13.107.21.239:443, 13.107.42.14:443, 13.71.55.58:443 (1 event each)

## Command-and-Control and Network Activity

- Internal client 10.1.17.215 made 1823 connections to 119 distinct external destinations, with 5.252.153.241 being the most contacted external IP (1196 connections) [fake_auth-09#0].
- The Kerberos identity of 10.1.17.215 is associated with the hostname desktop-l8c5gsj and the user account shutchenson [fake_auth-09#0, fake_auth-05#0].
- Suricata alerts were generated between 2025-01-22 19:00 UTC and 2025-01-22 20:00 UTC, with the earliest alert occurring at 2025-01-22 19:00 UTC [fake_auth-09#0].
- High-severity alerts were directed to 5.252.153.241, 10.1.17.215, and 185.188.32.26 [fake_auth-09#0].
- The top domains contacted by 10.1.17.215 include c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, and ds.reson8.com, among others [fake_auth-08#2, fake_auth-08#3, fake_auth-08#0].
- Not established from the available artifacts.
- Not established from the available artifacts.
- Not established from the available artifacts.

## Impact Assessment

- Assessment: The primary CIA component targeted was availability, as evidenced by the high number of external connections from the internal client 10.1.17.215, which could potentially lead to bandwidth exhaustion or service degradation. [fake_auth-02#0]
- Assessment: The scale of external activity was significant, with 1823 events from the internal client 10.1.17.215 connecting to 119 distinct external IP addresses, with the most contacted being 5.252.153.241. [fake_auth-02#0]
- Assessment: The availability of the network was impacted by the high-severity alerts, particularly those directed at the IP 5.252.153.241, which received 4 alerts. [fake_auth-06#2]
- Assessment: The impact on availability was further evidenced by the Kerberos identity of the internal client 10.1.17.215, which is associated with the user account shutchenson. [fake_auth-09#0]
- Assessment: The domains accessed by the internal client included oneclient.sfx.ms, img-s-msn-com.akamaized.net, px.owneriq.net, and ag.innovid.com, among others, indicating potential external resource usage. [fake_auth-08#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is the compromise of the internal client 10.1.17.215, which was likely used as a vector to establish external connections and potentially exfiltrate data. The high volume of connections to the external IP 5.252.153.241 and the Kerberos and LDAP activities suggest a compromise of credentials or a backdoor. [auto: fake_auth-09#0, fake_auth-02#0]
- Not established: The initial vector used to compromise 10.1.17.215.
- Not established: The exact payload or malware used in the attack.
- Not established: Whether any data was exfiltrated or the nature of the data.
- Not established: The success or failure of any attempted HTTP requests to external destinations.
- Not established: The specific actions taken by the compromised client, such as file downloads or command execution.
- Not established: The presence of any other compromised hosts within the network.

## Corrective and Preventive Actions

- Isolate host 10.1.17.215 to prevent further external connections and internal propagation. [auto: fake_auth-09#0, fake_auth-08#3]
- Reset the user account shutchenson to remove any potential malware or unauthorized access.
- Block the external IP 5.252.153.241 to prevent communication with the identified command-and-control server. [auto: fake_auth-09#0, fake_auth-01#2]
- Review and update the Kerberos identities associated with desktop-l8c5gsj to ensure proper authentication and authorization. [auto: fake_auth-09#0, fake_auth-03#0]

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 10.1.17.215 [fake_auth-09#0].
2. The hostname of the potentially infected machine in the LAN is desktop-l8c5gsj [fake_auth-05#0].
3. The Windows human user account name of the potentially infected machine in the LAN is shutchenson [fake_auth-03#0].
4. The likely fake or suspicious domains/URLs for initial infection are c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, and ds.reson8.com [fake_auth-08#2].
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 5.252.153.241, 185.188.32.26, and 45.125.66.32 [fake_auth-06#2].
6. The first signs of infection activity appeared during the hour 2025-01-22 19:00 UTC [fake_auth-06#4].
7. Suspicious certificates were observed in the encrypted network traffic. The domain or IP in the certificate is 45.125.66.252 and 45.125.66.32 [fake_auth-07#0].
8. The single external IP address that received the most connections from the infected hosts is 5.252.153.241. It is not identified as a C2 server or a legitimate service [fake_auth-09#0].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [fake_auth-05#0, fake_auth-09#0, fake_auth-06#1, fake_auth-01#2, fake_auth-01#3]
U2. Not established from the available artifacts [fake_auth-05#0, fake_auth-09#0, fake_auth-06#1, fake_auth-01#2, fake_auth-01#3]
U3. Not established from the available artifacts [fake_auth-05#0, fake_auth-09#0, fake_auth-06#1, fake_auth-01#2, fake_auth-01#3]
