# Incident Postmortem: Network security incident investigation

## Incident Summary

- Host 172.17.0.99 (desktop-rnvo9at), associated with user afletcher, exhibited suspicious network behavior during the incident window [koi_stealer-08#0].
- The earliest detection occurred at 17:00 UTC on 2024-09-04, marked by a surge in alerts including a Koi Stealer CnC check-in [koi_stealer-06#3, koi_stealer-08#0].
- External IP 79.124.78.197 was the most contacted destination from 172.17.0.99, with 218 connections and associated high-severity alerts indicating potential C2 activity [koi_stealer-02#0, koi_stealer-06#1].
- Assessment: The host demonstrated command-and-control behavior consistent with malware infection, primarily threatening confidentiality through data exfiltration attempts [koi_stealer-06#2, koi_stealer-08#0].

## Affected Host and User

- Internal client 172.17.0.99 is associated with hostname desktop-rnvo9at and user account afletcher [koi_stealer-08#0].
- Host 172.17.0.99 initiated 361 external connections to 35 distinct destinations, with the most contacted being 79.124.78.197 [koi_stealer-02#0].
- Kerberos activity from 172.17.0.99 shows user afletcher as the client account in 8 events [koi_stealer-03#0].
- Hostname desktop-rnvo9at is linked to source IP 172.17.0.99 in one event [koi_stealer-05#0].

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- ET MALWARE Win32/Koi Stealer CnC Checkin (GET) triggered 1 event, involving internal client 172.17.0.99 [koi_stealer-06#1].
- ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 generated 48 high-severity alerts from source 172.17.0.99 [koi_stealer-06#2].
- ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound produced 1 high-severity alert, linked to source 172.17.0.99 [koi_stealer-06#2].
- High-severity alerts were directed to external IP 79.124.78.197 in 49 instances, indicating potential C2 communication [koi_stealer-06#1].
- One high-severity alert originated from external IP 79.124.78.197, suggesting inbound malicious activity or response [koi_stealer-06#3].
- ET INFO Microsoft Connection Test and GPL NETBIOS SMB IPC$ unicode share access were observed but classified as informational, not malicious [koi_stealer-06#0].

## Initial Infection Indicators

- 172.17.0.99 connected to 79.124.78.197 on port 80 requesting /foots.php, associated with 48 download events [koi_stealer-01#1]
- 172.17.0.99 requested /index.php?id=&subid=qIOuKk7U from 79.124.78.197:80 [koi_stealer-01#2]
- 172.17.0.99 initiated an outbound file transfer to 20.96.153.111:443 with fuid FwBwUeLMampjgOJ5k [koi_stealer-01#6]
- 172.17.0.99 transferred a file to 20.189.173.26:443 with fuid FhRlFk2pp8tC1dsabb [koi_stealer-01#5]
- 172.17.0.99 transferred a file to 20.241.44.114:443 with fuid FyjT0AzkMPMcF8Uck [koi_stealer-01#5]
- 172.17.0.99 transferred a file to 20.42.73.28:443 with fuid FpR8YU2UKfciamuQTd [koi_stealer-01#5]

## Command-and-Control and Network Activity

- Internal client 172.17.0.99 initiated 361 network connections to 35 distinct external destinations [koi_stealer-02#0].
- The most-contacted external IP from 172.17.0.99 was 79.124.78.197, with 218 connections [koi_stealer-08#0].
- HTTP requests from 172.17.0.99 to 79.124.78.197 included a URI path "/index.php?id=&subid=qIOuKk7U" [koi_stealer-01#2].
- Suricata alerts associated with 79.124.78.197 totaled 49 high-severity events during the incident window [koi_stealer-08#0].
- Additional HTTP connections from 172.17.0.99 were observed to 23.220.251.158, 184.29.137.96, and 199.232.210.172 [koi_stealer-01#2].
- Domains accessed include sso.godaddy.com, www.bellantonicioccolato.it, and weathermapdata.blob.core.windows.net [koi_stealer-07#0].
- Assessment: The volume and pattern of connections to 79.124.78.197, including URI structure and alert severity, suggest potential C2 communication. [koi_stealer-08#0, koi_stealer-01#2]
- Assessment: Connections to Microsoft-related domains (e.g., blob.core.windows.net, oneclient.sfx.ms) may indicate legitimate traffic, but require further validation. [koi_stealer-07#1, koi_stealer-07#0]

## Impact Assessment

- Internal client 172.17.0.99 established 361 connections to 35 external destinations, with 218 connections to 79.124.78.197 [koi_stealer-02#0].
- High-severity alerts include 48 instances of suspicious POST requests to IP addresses using fake browser headers, indicating data exfiltration activity [koi_stealer-06#2].
- One high-severity alert identified a Koi Stealer CnC check-in via HTTP GET, confirming malware communication behavior [koi_stealer-06#1].
- The host 172.17.0.99 was the source of 49 out of 50 high-severity alerts, indicating it was the primary compromised system [koi_stealer-06#2].
- Assessment: Confidentiality was the primary CIA component targeted, as evidenced by malware CnC traffic and suspicious outbound POST requests consistent with data theft. [koi_stealer-06#1, koi_stealer-06#2]

## Root Cause and Evidence Gaps

- Assessment: The root cause was likely credential compromise or malware execution on host 172.17.0.99, leading to external command-and-control communications and internal reconnaissance; confidence is medium [koi_stealer-08#0].
- Not established from the available artifacts whether the initial infection vector was phishing, exploit, or insider action [koi_stealer-09#0].
- Not established whether the file transfers to external IPs contained exfiltrated data or were benign HTTPS sessions [koi_stealer-01#4].
- Not established if the malware used encryption, packing, or persistence mechanisms on the host [koi_stealer-09#0].
- Not established whether lateral movement beyond 172.17.0.99 occurred within the LAN segment [koi_stealer-04#1].
- Not established if the connections to 79.124.78.197 involved malicious payloads or data staging [koi_stealer-08#0].
- Not established whether the Kerberos and LDAP activity from 172.17.0.99 was part of automated attack tooling or manual interaction [koi_stealer-04#0].

## Corrective and Preventive Actions

- Isolate host 172.17.0.99 (desktop-rnvo9at) due to excessive external connections and suspicious activity [koi_stealer-08#0].
- Reset credentials for user afletcher, as their account was active on the compromised host 172.17.0.99 [koi_stealer-08#0].
- Block outbound traffic to IP 79.124.78.197, which received 218 connections from 172.17.0.99 and was linked to high-severity alerts [koi_stealer-08#0].
- Block outbound traffic to IPs 13.70.79.200, 13.89.179.9, 20.189.173.1, 20.189.173.26, 20.241.44.114, 20.42.73.28, and 20.96.153.111 due to file transfers from 172.17.0.99,. [koi_stealer-01#4, koi_stealer-01#5]
- Investigate and disable any persistence mechanisms associated with Kerberos ticket-granting requests for krbtgt/BEPOSITIVE from 172.17.0.99 [koi_stealer-04#0].

## Answers to Investigation Questions

1. 172.17.0.99 [koi_stealer-08#0]
2. desktop-rnvo9at [koi_stealer-08#0]
3. afletcher [koi_stealer-08#0]
4. Not established from the available artifacts
5. 79.124.78.197 [koi_stealer-08#0]
6. confidentiality [koi_stealer-06#2]
7. 2024-09-04 17:00 UTC [koi_stealer-08#0]
8. 79.124.78.197; It is likely a C2 server [koi_stealer-02#0]
## Additional Investigation Questions

U1. Not established from the available artifacts
U2. Not established from the available artifacts
U3. Not established from the available artifacts
