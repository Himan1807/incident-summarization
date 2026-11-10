# Incident Postmortem: Network security incident investigation

## Incident Summary

The incident affected the internal host 172.17.0.99, with the earliest signs of infection activity appearing at 2024-09-04 17:00 UTC. The host contacted the external IP 79.124.78.197 the most, with 218 connections, which is a likely command-and-control (C2) server. Assessment: The primary target was confidentiality, consistent with the nature of a koi stealer. [koi_stealer-08#0]

## Affected Host and User

- Affected Host: 172.17.0.99, Hostname: desktop-rnvo9at, Human User: afletcher [koi_stealer-08#0, koi_stealer-05#0, koi_stealer-04#1, koi_stealer-04#0, koi_stealer-03#0, koi_stealer-02#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- High-severity alerts: 50 events, signature "ET MALWARE Win32/Koi Stealer CnC Checkin (GET)" from [koi_stealer-06#1].
- High-severity alerts: 48 events, signature "ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1" from [koi_stealer-06#2].
- High-severity alerts: 1 event, signature "ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound" from [koi_stealer-06#2].
- High-severity alerts: 1 event, signature "ET MALWARE Win32/Koi Stealer CnC Checkin (GET)" from [koi_stealer-06#2].
- High-severity alerts: 49 events, source IP 172.17.0.99, destination IP 79.124.78.197 from and. [koi_stealer-06#1, koi_stealer-06#2]
- Informational alerts: 2 events, signature "ET INFO Microsoft Connection Test" from [koi_stealer-06#0].

## Initial Infection Indicators

- [koi_stealer-01#0] download domains: 79.124.78.197 — 50 events
- [koi_stealer-01#1] download domains: x1.c.lencr.org — 1 event
- [koi_stealer-01#2] http requests: 172.17.0.99 -> 23.220.251.158:80 : /connecttest.txt — 2 events
- [koi_stealer-01#3] http requests: 172.17.0.99 -> 199.232.210.172:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?d7a8a57aa5acd39b — 1 event
- [koi_stealer-01#5] file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FSvMjvPqRih6zUFI5 — 1 event

## Command-and-Control and Network Activity

- Internal client 172.17.0.99 made 361 external connections, with 79.124.78.197 being the most contacted external IP (218 connections) [koi_stealer-08#0].
- The client 172.17.0.99 contacted 35 distinct external destinations [koi_stealer-02#0].
- Suricata alerts for 172.17.0.99 span from 2024-09-04 17:00 UTC to 2024-09-04 18:00 UTC, with the earliest alert at 2024-09-04 17:00 UTC [koi_stealer-08#0].
- High-severity alerts were directed to 79.124.78.197 (49 alerts) and 172.17.0.99 (1 alert) [koi_stealer-08#0].
- The client 172.17.0.99 contacted additional external IPs including 23.45.119.144, 204.79.197.203, 52.113.194.132, and 23.195.212.189 [koi_stealer-02#0].
- HTTP requests from 172.17.0.99 were made to 23.220.251.158, 79.124.78.197, 184.29.137.96, and 199.232.210.172 [koi_stealer-01#2].
- The client 172.17.0.99 contacted domains such as sso.godaddy.com, www.bellantonicioccolato.it, img-s-msn-com.akamaized.net, and oneclient.sfx.ms [koi_stealer-07#0].
- No evidence directly supports C2 activity; however, the client contacted a large number of external IPs and domains, which could indicate a legitimate service or a C2 server [Assessment:].
- The Kerberos identity of the client 172.17.0.99 is associated with the hostname desktop-rnvo9at and the user account afletcher [Assessment:]. [koi_stealer-08#0, koi_stealer-05#0]

## Impact Assessment

- Assessment: Confidentiality was primarily targeted, as evidenced by the high number of external connections from the internal client 172.17.0.99 to external servers. The external IP 79.124.78.197 received the most connections (218) from the internal client. [koi_stealer-02#0, koi_stealer-08#0]
- Assessment: The incident affected one internal host, 172.17.0.99, which made 361 external connections [koi_stealer-02#0, koi_stealer-08#0].
- Assessment: There is a possible scale of external activity involving multiple external destinations, with 35 distinct external IPs contacted by the internal client [koi_stealer-02#0, koi_stealer-08#0].
- Assessment: The timeline of high-severity alerts indicates activity spanning from 17:00 UTC to 18:00 UTC on 2024-09-04, with the earliest alert occurring at 17:00 UTC [koi_stealer-06#1, koi_stealer-08#0].

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is the compromise of an internal host (172.17.0.99) by a remote attacker, leading to lateral movement and data exfiltration. [koi_stealer-08#0]
- Not established: The initial infection vector or the specific payload used by the attacker. [koi_stealer-08#0]
- Not established: The exact nature and extent of data exfiltration, including the types of data stolen. [koi_stealer-01#4, koi_stealer-01#5]
- Not established: Whether the attacker used any additional lateral movement techniques beyond the Kerberos and CIFS activities observed. [koi_stealer-04#0, koi_stealer-04#1]
- Not established: The success or failure of any attempted connections to external destinations that did not generate alerts. [koi_stealer-08#0]
- Not established: The presence or absence of any self-signed or short validity certificates used by the attacker. [koi_stealer-09#0]
- Not established: The specific actions taken by the attacker during the time window, such as command execution or further reconnaissance. [koi_stealer-08#0]

## Corrective and Preventive Actions

- Isolate host 172.17.0.99 to prevent further external connections and file transfers. [koi_stealer-08#0, koi_stealer-04#1]
- Reset the user account afletcher to remove any potential access tokens or credentials.
- Block the IP address 79.124.78.197 to prevent communication with the identified external server. [koi_stealer-08#0, koi_stealer-01#2]
- Review and secure the Kerberos service to ensure no unauthorized access attempts.

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0].
3. The Windows human user account name of the potentially infected machine in the LAN is afletcher [koi_stealer-03#0].
4. The likely fake or suspicious domains / URLs for initial infection are Not established from the available artifacts [koi_stealer-09#0].
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-06#2, koi_stealer-06#3, koi_stealer-08#0].
6. The attacker primarily targets confidentiality [Assessment: Based on the nature of a koi stealer, which typically focuses on stealing sensitive information].
7. The first signs of infection activity appeared during the hour 2024-09-04 17:00 UTC [koi_stealer-06#2].
8. According to the connection volume statistics, the single external IP address that received the most connections from the infected hosts is 79.124.78.197, and it is likely a C2 server [koi_stealer-08#0].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
