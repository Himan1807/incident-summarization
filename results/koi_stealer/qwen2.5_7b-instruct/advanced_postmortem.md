# Incident Postmortem: Network security incident investigation

## Incident Summary

The incident affected the internal host 172.17.0.99, with the hostname desktop-rnvo9at and the user account afletcher. The earliest alert was generated at 2024-09-04 17:00 UTC, with 31 high-severity alerts directed to 79.124.78.197, which is considered a main C2 candidate. The key assessment is that the high volume of external connections, particularly to 79.124.78.197, suggests potential command-and-control activity. [auto: koi_stealer-08#0]

## Affected Host and User

- Affected host: 172.17.0.99, hostname: desktop-rnvo9at, human user account: afletcher [koi_stealer-08#0, koi_stealer-05#0, koi_stealer-04#1, koi_stealer-04#0, koi_stealer-03#0, koi_stealer-02#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- High-severity alerts: 50 events, signature: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) [koi_stealer-06#1]
- High-severity alerts: 48 events, signature: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 [koi_stealer-06#2]
- High-severity alerts: 1 event, signature: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound [koi_stealer-06#2]
- High-severity alerts: 1 event, signature: ET MALWARE Win32/Koi Stealer CnC Checkin (GET) [koi_stealer-06#2]
- Informational alerts: 5 events, signature: GPL NETBIOS SMB IPC$ unicode share access [koi_stealer-06#0]
- Informational alerts: 2 events, signature: ET INFO Microsoft Connection Test [koi_stealer-06#0]

## Initial Infection Indicators

- [koi_stealer-01#0] download domains: 79.124.78.197 — 50 events
- [koi_stealer-01#1] download domains: x1.c.lencr.org — 1 event
- [koi_stealer-01#2] http requests: 172.17.0.99 -> 23.220.251.158:80 : /connecttest.txt — 2 events
- [koi_stealer-01#3] http requests: 172.17.0.99 -> 199.232.210.172:80 : /msdownload/update/v3/static/trustedr/en/authrootstl.cab?d7a8a57aa5acd39b — 1 event
- [koi_stealer-01#5] file transfers > transfer details: 172.17.0.99 -> 20.96.153.111:443 : fuid: FSvMjvPqRih6zUFI5 — 1 event

## Command-and-Control and Network Activity

- Internal client 172.17.0.99 made 361 external connections, with 79.124.78.197 being the most contacted external IP (218 connections) [koi_stealer-08#0].
- The affected host desktop-rnvo9at, with IP 172.17.0.99, generated 31 Suricata alerts between 2024-09-04 17:00 UTC and 2024-09-04 18:00 UTC [koi_stealer-02#0].
- High-severity alerts were directed to 79.124.78.197 (49 alerts) and 172.17.0.99 (1 alert) [koi_stealer-02#0].
- Not established from the available artifacts.
- Assessment: The high volume of connections to 79.124.78.197 suggests potential command-and-control activity, but further analysis is required to confirm. [auto: koi_stealer-08#0, koi_stealer-02#0]
- Assessment: The connections to other external IPs do not strongly indicate C2 activity, as they may be related to legitimate services or data requests.
- Assessment: The HTTP requests to various domains and IPs, including sso.godaddy.com and www.bellantonicioccolato.it, do not provide clear evidence of C2 activity. [auto: koi_stealer-07#0]

## Impact Assessment

- Assessment: Confidentiality was primarily targeted, as evidenced by the high number of external connections from internal host 172.17.0.99 to external servers, and the presence of malware-related alerts. [koi_stealer-02#0, koi_stealer-06#3, koi_stealer-06#1, koi_stealer-08#0]
- Assessment: One internal host, 172.17.0.99, was significantly affected, with 361 external connections. [koi_stealer-08#0]
- Assessment: The scale of external activity was notable, with 35 distinct external destinations contacted by the internal host. [koi_stealer-02#0]
- Assessment: The majority of external connections were directed to the IP 79.124.78.197, indicating a potential command-and-control server. [koi_stealer-02#0, koi_stealer-06#3]
- Assessment: Possible impact on integrity and availability is suggested by the high severity alerts and suspicious POST requests, though direct evidence is not established. [koi_stealer-06#2]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is the compromise of an internal host (172.17.0.99) by a remote attacker, leading to lateral movement and data exfiltration. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]
- Not established: The initial infection vector (e.g., phishing, exploit, or other means) is not established. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]
- Not established: The specific payload or malware used in the attack is not established. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]
- Not established: The extent and nature of data exfiltration, if any, are not established. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]
- Not established: The success or failure of any attempted queries to external destinations that did not result in alerts are not established. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]
- Not established: The presence or absence of self-signed certificates, IP-based certificates, or certificates with short validity periods is not established. [koi_stealer-09#0]
- Not established: The behavior of the payload post-infection, such as command execution or further lateral movement, is not established. [koi_stealer-08#0, koi_stealer-01#4, koi_stealer-04#0, koi_stealer-04#1, koi_stealer-01#5]

## Corrective and Preventive Actions

- Isolate host 172.17.0.99 to prevent further external connections and file transfers. [auto: koi_stealer-08#0, koi_stealer-04#1]
- Reset the user account afletcher to remove any potential access tokens or credentials.
- Block the IP address 79.124.78.197 to prevent communication with the identified external server. [auto: koi_stealer-08#0, koi_stealer-01#2]
- Review and secure the Kerberos service to ensure no unauthorized access attempts.

## Answers to Investigation Questions

1. 172.17.0.99 [koi_stealer-08#0]
2. desktop-rnvo9at [koi_stealer-05#0]
3. afletcher [koi_stealer-03#0]
4. Not established from the available artifacts.
5. 79.124.78.197 [koi_stealer-06#2, koi_stealer-06#3, koi_stealer-08#0]
6. Not established from the available artifacts.
7. 2024-09-04 17:00 UTC [koi_stealer-06#2]
8. 79.124.78.197 received the most connections (218) [koi_stealer-08#0]. This IP address is likely involved in command-and-control (C2) communication.

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [koi_stealer-08#0]
U2. Not established from the available artifacts [koi_stealer-08#0]
U3. Not established from the available artifacts [koi_stealer-08#0]
