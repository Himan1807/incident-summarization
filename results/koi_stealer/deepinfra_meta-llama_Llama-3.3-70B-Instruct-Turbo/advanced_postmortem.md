# Incident Postmortem: Network security incident investigation

## Incident Summary

The affected host is 172.17.0.99, with a hostname of desktop-rnvo9at and a human user account of afletcher. The earliest alert hour is 17:00 UTC, with 31 events. The main C2 candidate is 79.124.78.197, which received 218 connections from the internal client 172.17.0.99. Assessment: The high number of connections to 79.124.78.197 and the presence of high-severity alerts related to malware and suspicious activity suggest potential malware activity on the network. The user account afletcher is linked to 8 events from the source IP 172.17.0.99, further supporting the association of this user with the affected host. [koi_stealer-08#0, koi_stealer-06#3, koi_stealer-06#1, koi_stealer-03#0]

## Affected Host and User

* The IP address of the affected internal host is 172.17.0.99, with a hostname of desktop-rnvo9at and a human user account of afletcher [koi_stealer-08#0].
* The affected host 172.17.0.99 is associated with multiple events and services, including Kerberos and CIFS, with the same IP address and hostname [koi_stealer-04#1].
* Assessment: The consistency of the IP address, hostname, and user account across multiple evidence IDs suggests that 172.17.0.99 is the primary affected host [koi_stealer-08#0].
* The user account afletcher is linked to 8 events from the source IP 172.17.0.99, further supporting the association of this user with the affected host [koi_stealer-03#0].

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

* High-severity malicious signatures include ET MALWARE Win32/Koi Stealer CnC Checkin (GET) with 1 event and ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound with 1 event [koi_stealer-06#1]
* The host 172.17.0.99 was involved in 49 high-severity alerts, primarily associated with the signature ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1 [koi_stealer-06#2]
* The external destination 79.124.78.197 was associated with 49 high-severity alerts, indicating potential malicious activity [koi_stealer-06#1]
* Informational alerts include ET INFO Microsoft Connection Test with 2 events, which is a connection test and not indicative of malicious activity [koi_stealer-06#0]
* Assessment: The presence of Koi Stealer CnC Checkin and Koi Loader/Stealer CnC Config Inbound alerts suggests potential malware activity on the network [koi_stealer-06#1]
* The internal client 172.17.0.99, associated with hostname desktop-rnvo9at and user afletcher, had the most external connections, with 361 events and 35 distinct external destinations [koi_stealer-08#0]

## Initial Infection Indicators

* The domain `79.124.78.197` is marked as suspicious due to 50 download events [koi_stealer-01#0]
* A possible initial infection indicator is the HTTP request to `79.124.78.197:80` for `/foots.php` from `172.17.0.99` [koi_stealer-01#1]
* The download of a file from `20.96.153.111:443` with a unique `fuid` may be a suspicious activity [koi_stealer-01#6]
* The HTTP request to `79.124.78.197:80` for `/index.php?id=&subid=qIOuKk7U` from `172.17.0.99` could be an initial infection vector [koi_stealer-01#2]
* Multiple file transfers from `172.17.0.99` to various IPs on port 443, including `20.189.173.26` and `20.241.44.114`, may indicate suspicious activity [koi_stealer-01#5]
* Assessment: The frequent downloads from `79.124.78.197` and the specific HTTP requests to this IP may indicate a potential initial infection vector [koi_stealer-01#0, koi_stealer-01#1]

## Command-and-Control and Network Activity

* The internal client 172.17.0.99 made the most connections to external destinations, with 361 events and 35 distinct external destinations [koi_stealer-08#0].
* The most-contacted external IP by 172.17.0.99 was 79.124.78.197, with 218 connections [koi_stealer-08#0].
* The Kerberos identity of 172.17.0.99 is associated with the hostname desktop-rnvo9at and human user account afletcher [koi_stealer-08#0].
* Suricata alerts were generated between 17:00 UTC and 18:00 UTC, with the earliest alert at 17:00 UTC and a total of 31 alerts [koi_stealer-08#0].
* The destination of the majority of high-severity alerts was 79.124.78.197, with 49 alerts [koi_stealer-08#0].
* Assessment: The high number of connections to 79.124.78.197 suggests that this IP may be a command and control server [koi_stealer-08#0].
* Assessment: The presence of high-severity alerts associated with 79.124.78.197 further supports the possibility that this IP is involved in malicious activity [koi_stealer-08#0].
* Assessment: The connection to legitimate services such as weathermapdata.blob.core.windows.net and oneclient.sfx.ms suggests that not all connections from 172.17.0.99 are necessarily malicious [koi_stealer-07#1, koi_stealer-07#0]

## Impact Assessment

* The primary CIA component targeted is confidentiality, Assessment: based on the presence of high-severity alerts related to malware and suspicious activity [koi_stealer-06#1].
* The scale of external activity is significant, with 218 connections to a single external IP, 79.124.78.197, and a total of 92 further events to other destinations [koi_stealer-02#0].
* The number of affected hosts is at least one, with possible additional hosts indicated by the presence of 50 high-severity alerts [koi_stealer-06#1].
* The human user account associated with the affected host 172.17.0.99 is afletcher, Assessment: based on derived Kerberos identity information [koi_stealer-08#0].

## Root Cause and Evidence Gaps

* Assessment: The most likely root cause is a compromised internal client (172.17.0.99) making suspicious connections to external destinations, with medium confidence [koi_stealer-08#0]
* The initial infection vector is not established from the available artifacts [koi_stealer-09#0]
* The payload behaviour and potential data exfiltration are not established from the available artifacts [koi_stealer-01#4]
* The queries for suspicious certificates and self-signed certificates did not yield any results, but this does not prove their absence elsewhere [koi_stealer-09#0]
* The internal client 172.17.0.99 made connections to multiple external destinations, including 79.124.78.197, 13.70.79.200, and 20.189.173.1 [koi_stealer-01#4]
* The purpose and content of the file transfers between the internal client and external destinations are not established from the available artifacts [koi_stealer-01#5]

## Corrective and Preventive Actions

* Isolate host 172.17.0.99 from the network to prevent further potential malicious activity [koi_stealer-08#0]
* Reset the account of user afletcher associated with the hostname desktop-rnvo9at [koi_stealer-08#0]
* Block traffic to and from external IP 79.124.78.197, which was the most-contacted external IP by the internal client 172.17.0.99 [koi_stealer-08#0]
* Investigate and potentially block traffic to the external IPs 13.70.79.200, 13.89.179.9, and 20.189.173.1, which were involved in file transfers with the internal client 172.17.0.99 [koi_stealer-01#4]
* Monitor and analyze the activity of the internal client 172.17.0.99, which had multiple connections to various external destinations and triggered Suricata alerts [koi_stealer-01#2]

## Answers to Investigation Questions

* 1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0]
* 2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-08#0]
* 3. The Windows human user account name of the potentially infected machine in the LAN is afletcher [koi_stealer-08#0]
* 8. The single external IP address that received the most connections from the infected hosts is 79.124.78.197, but it is Not established from the available artifacts whether it is a C2 server or a legitimate service [koi_stealer-08#0]

---
Verification note: 4 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
