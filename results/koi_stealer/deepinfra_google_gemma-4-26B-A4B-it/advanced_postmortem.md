# Incident Postmortem: Network security incident investigation

## Incident Summary

The host 172.17.0.99 (desktop-rnvo9at) and user account afletcher were affected by this incident. The earliest alert hour was 2024-09-04 17:00 UTC. The external IP 79.124.78.197 is the main C2 candidate, as it received 218 connections and 49 high-severity Suricata alerts. Assessment: 79.124.78.197 is likely a C2 server. Assessment: There is a possible confidentiality impact based on signatures for Koi Stealer CnC checkin and Koi Loader/Stealer CnC config inbound. [koi_stealer-08#0, koi_stealer-06#1, koi_stealer-06#2]

## Affected Host and User

* IP address 172.17.0.99, hostname desktop-rnvo9at, user account afletcher [koi_stealer-08#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

* ET MALWARE Win32/Koi Stealer CnC Checkin (GET): 1 event involving 172.17.0.99 [koi_stealer-06#1].
* ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound: 1 event involving 172.17.0.99 [koi_stealer-06#2].
* ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1: 48 events involving 172.17.0.99 [koi_stealer-06#2].
* GPL NETBIOS SMB IPC$ unicode share access: 5 events [koi_stealer-06#0].
* ET INFO Microsoft Connection Test: 2 events [koi_stealer-06#0].

## Initial Infection Indicators

* 172.17.0.99 made HTTP requests to 79.124.78.197 for /foots.php [koi_stealer-01#1]
* 172.17.0.99 made HTTP requests to 79.124.78.197 for /index.php?id=&subid=qIOuKk7U [koi_stealer-01#2]
* 172.17.0.99 made HTTP requests to 23.220.251.47 for /assets/Owner/arm/ProcessMAU.txt [koi_stealer-01#3]
* 172.17.0.99 made HTTP requests to 184.29.137.96 for / [koi_stealer-01#2]
* Assessment: The activity involving 79.124.78.197, 23.220.251.47, and 184.29.137.96 is suspicious [koi_stealer-01#1, koi_stealer-01#2, koi_stealer-01#3]
* Not established from the available artifacts.

## Command-and-Control and Network Activity

* Internal client 172.17.0.99 made 361 connections to 35 distinct external destinations [koi_stealer-08#0, koi_stealer-02#0].
* The external IP receiving the most connections from 172.17.0.99 is 79.124.78.197 with 218 connections [koi_stealer-08#0, koi_stealer-02#0].
* High-severity Suricata alerts were directed to 79.124.78.197 (49 alerts) and 172.17.0.99 (1 alert) [koi_stealer-08#0].
* Assessment: The high volume of connections and high-severity alerts directed to 79.124.78.197 support C2 activity [koi_stealer-08#0].
* Assessment: The specific HTTP request pattern to 79.124.78.197 is inconsistent with legitimate service behavior [koi_stealer-01#2].

## Impact Assessment

* Assessment: Possible confidentiality impact based on signatures for Koi Stealer CnC checkin and Koi Loader/Stealer CnC config inbound [koi_stealer-06#1, koi_stealer-06#2].
* One host (172.17.0.99) is affected [koi_stealer-02#0, koi_stealer-08#0].
* External activity includes 35 distinct external destinations [koi_stealer-02#0, koi_stealer-08#0].

## Root Cause and Evidence Gaps

* Assessment: Not established from the available artifacts.
* Initial infection vector is not established from the available artifacts.
* Payload behavior is not established from the available artifacts.
* Data exfiltration is not established from the available artifacts.
* Specific malicious intent of the file transfers is not established from the available artifacts.

## Corrective and Preventive Actions

* Isolate host 172.17.0.99 (desktop-rnvo9at) [koi_stealer-08#0].
* Reset credentials for user account afletcher [koi_stealer-08#0].
* Block external IP 79.124.78.197 [koi_stealer-08#0].
* Block external IPs 13.70.79.200, 13.89.179.9, 20.189.173.1, 20.189.173.26, 20.241.44.114, 20.42.73.28, and 20.96.153.111 [koi_stealer-01#4, koi_stealer-01#5].
* Block external IPs 23.220.251.158, 184.29.137.96, and 199.232.210.172 [koi_stealer-01#2].

## Answers to Investigation Questions

1. 172.17.0.99 [koi_stealer-08#0]
2. desktop-rnvo9at [koi_stealer-08#0]
3. afletcher [koi_stealer-08#0]
4. Not established from the available artifacts.
5. 79.124.78.197, 23.45.119.144, 204.79.197.203, 52.113.194.132, 23.195.212.189 [koi_stealer-02#0]
6. Not established from the available artifacts.
7. 2024-09-04 17:00 UTC [koi_stealer-08#0]
8. 79.124.78.197; Assessment: Likely a C2 server [koi_stealer-06#1, koi_stealer-06#2]
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
