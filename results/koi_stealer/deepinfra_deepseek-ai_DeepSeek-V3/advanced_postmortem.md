# Incident Postmortem: Network security incident investigation

## Incident Summary

- The affected host was 172.17.0.99, identified as desktop-rnvo9at, with the associated user account afletcher [koi_stealer-08#0].
- The earliest alert occurred at 2024-09-04 17:00 UTC, marking the start of high-severity activity involving the host [koi_stealer-08#0].
- The primary candidate for command-and-control activity was external IP 79.124.78.197, which received the majority of connections and high-severity alerts from the host [koi_stealer-08#0, koi_stealer-06#1].
- Assessment: The high volume of suspicious connections and alerts suggests potential command-and-control activity, though further investigation is required to confirm malicious intent [koi_stealer-08#0, koi_stealer-01#2].

## Affected Host and User

- The internal client 172.17.0.99 was identified as an affected host, with the hostname desktop-rnvo9at and the human user account afletcher [koi_stealer-08#0].
- The host 172.17.0.99 initiated 361 external connections to 35 distinct external destinations, with the most-contacted IP being 79.124.78.197 [koi_stealer-02#0].
- Kerberos activity from 172.17.0.99 included interactions with services such as krbtgt/BEPOSITIVE and LDAP/WIN-CTL9XBQ9Y19.bepositive.com [koi_stealer-04#0].
- Suricata alerts associated with 172.17.0.99 occurred between 2024-09-04 17:00 UTC and 2024-09-04 18:00 UTC, with 79.124.78.197 being a primary destination of high-severity alerts [koi_stealer-08#0].

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- High-severity alert "ET MALWARE Win32/Koi Stealer CnC Checkin (GET)" was triggered once, involving internal client 172.17.0.99 and external destination 79.124.78.197 [koi_stealer-06#1].
- High-severity alert "ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1" was triggered 48 times, all involving internal client 172.17.0.99 [koi_stealer-06#2].
- High-severity alert "ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound" was triggered once, involving internal client 172.17.0.99 [koi_stealer-06#2].
- Informational alert "ET INFO Microsoft Connection Test" was triggered twice, with no associated high-severity activity [koi_stealer-06#0].
- High-severity alerts were concentrated between 17:00 UTC and 18:00 UTC, peaking at 17:00 UTC with 31 alerts [koi_stealer-06#3].
- Internal client 172.17.0.99 was the source of 49 high-severity alerts, primarily targeting external destination 79.124.78.197 [koi_stealer-06#1].

## Initial Infection Indicators

- The host 172.17.0.99 downloaded files from 79.124.78.197, which was the most frequent external destination with 50 events [koi_stealer-01#0].
- The host 172.17.0.99 made HTTP requests to 79.124.78.197:80 for `/foots.php` and `/index.php?id=&subid=qIOuKk7U`, which are unusual paths. [koi_stealer-01#1, koi_stealer-01#2]
- The host 172.17.0.99 transferred files to multiple external IPs, including 20.96.153.111:443 and 20.189.173.26:443, with unique file identifiers. [koi_stealer-01#6, koi_stealer-01#5]
- The host 172.17.0.99 made HTTP requests to 23.220.251.149:80 and 23.220.251.158:80 for `/connecttest.txt`, which is a possible suspicious activity. [koi_stealer-01#1, koi_stealer-01#2]
- The host 172.17.0.99 made HTTP requests to 184.29.137.96:80 for `/`, which is an unusual destination with minimal activity [koi_stealer-01#2].
- The host 172.17.0.99 made HTTP requests to 199.232.210.172:80 for `/msdownload/update/v3/static/trustedr/en/authrootstl.cab`, which is a possible suspicious update request [koi_stealer-01#2].

## Command-and-Control and Network Activity

- Internal client 172.17.0.99 initiated 361 connections to 35 distinct external destinations, with the most-contacted external IP being 79.124.78.197 (218 connections) [koi_stealer-08#0].
- The Kerberos identity of 172.17.0.99 was associated with hostname desktop-rnvo9at and user account afletcher [koi_stealer-08#0].
- Suricata alerts involving 172.17.0.99 occurred between 2024-09-04 17:00 UTC and 2024-09-04 18:00 UTC, with 49 high-severity alerts targeting 79.124.78.197 [koi_stealer-08#0].
- HTTP requests from 172.17.0.99 included connections to 79.124.78.197 with the path `/index.php?id=&subid=qIOuKk7U` [koi_stealer-01#2].
- Other external destinations contacted by 172.17.0.99 included 23.45.119.144 (18 connections), 204.79.197.203 (14 connections), and 52.113.194.132 (10 connections) [koi_stealer-02#0].
- Domains accessed by 172.17.0.99 included `weathermapdata.blob.core.windows.net`, `sso.godaddy.com`, and `www.bellantonicioccolato.it`. [koi_stealer-07#1, koi_stealer-07#0]
- Assessment: The high volume of connections to 79.124.78.197, combined with suspicious HTTP requests and high-severity alerts, suggests potential command-and-control activity. [koi_stealer-08#0, koi_stealer-01#2]
- Assessment: Connections to domains like `sso.godaddy.com` and `weathermapdata.blob.core.windows.net` may indicate legitimate activity, but further investigation is required. [koi_stealer-07#0, koi_stealer-07#1]

## Impact Assessment

- High-severity Suricata alerts were triggered by connections from 172.17.0.99 to 79.124.78.197, including signatures for Win32/Koi Stealer CnC Checkin [koi_stealer-06#1].
- Assessment: The primary CIA component targeted was confidentiality, based on evidence of malware-related CnC activity and external connections. [koi_stealer-06#1, koi_stealer-08#0]
- One internal host (172.17.0.99) was affected, with significant external activity focused on 79.124.78.197. [koi_stealer-02#0, koi_stealer-08#0]

## Root Cause and Evidence Gaps

- Assessment: The root cause is likely unauthorized external connections from 172.17.0.99 to multiple external IPs, particularly 79.124.78.197, indicating potential data exfiltration or C2 activity [koi_stealer-08#0].
- The initial infection vector is not established from the available artifacts [koi_stealer-09#0].
- The payload behavior, including whether malicious files were executed or stored, is not established [koi_stealer-01#4].
- Data exfiltration is suspected but not confirmed due to the absence of detailed file transfer content analysis [koi_stealer-01#5].
- The role of Kerberos activity in the incident, such as credential misuse or privilege escalation, is not established [koi_stealer-04#0].
- The absence of suspicious certificates does not rule out their use elsewhere in the network [koi_stealer-09#0].
- The impact of the file transfers to external IPs, including whether sensitive data was compromised, is not established [koi_stealer-01#4].

## Corrective and Preventive Actions

- Isolate host 172.17.0.99 (desktop-rnvo9at) due to excessive external connections and high-severity alerts involving 79.124.78.197 [koi_stealer-08#0].
- Reset credentials for user account afletcher associated with 172.17.0.99 to mitigate potential credential compromise [koi_stealer-08#0].
- Block external IPs 79.124.78.197, 13.70.79.200, and 20.189.173.1 due to suspicious file transfers and HTTP requests originating from 172.17.0.99. [koi_stealer-01#4, koi_stealer-01#2]
- Investigate and audit Kerberos and LDAP services accessed by 172.17.0.99 to identify potential lateral movement or privilege escalation. [koi_stealer-04#1, koi_stealer-04#0]
- Monitor and block additional suspicious external IPs (e.g., 20.96.153.111, 20.42.73.28) involved in file transfers from 172.17.0.99 [koi_stealer-01#5].

## Answers to Investigation Questions

1. 172.17.0.99 [koi_stealer-08#0]
2. desktop-rnvo9at [koi_stealer-08#0]
3. afletcher [koi_stealer-08#0]
4. Not established from the available artifacts.
5. 79.124.78.197, 23.45.119.144, 204.79.197.203, 52.113.194.132, 23.195.212.189 [koi_stealer-02#0]
6. Not established from the available artifacts.
7. 2024-09-04 17:00 UTC [koi_stealer-08#0]
8. 79.124.78.197 [koi_stealer-08#0] Not established from the available artifacts whether it is a C2 server or a legitimate service.
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
