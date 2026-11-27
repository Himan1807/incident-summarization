# Incident Postmortem: Network security incident investigation

## Incident Summary

* The affected host is 10.1.17.215, a desktop-l8c5gsj, with a human user account shutchenson [<evidence id>]. [auto: fake_auth-09#0, fake_auth-05#0]
* The earliest alert hour was 19:00 UTC on 2025-01-22 [<evidence id>]. [auto: fake_auth-09#0, fake_auth-06#4]
* The main C2 candidate is 5.252.153.241 [<evidence id>]. [auto: fake_auth-09#0, fake_auth-06#2]
* Assessment: The high volume of connections to external destinations, particularly to IP addresses that are not part of the private range, suggests potential malicious activity [<evidence id>].

## Affected Host and User

* IP address of affected host: 10.1.17.215 [auto: fake_auth-09#0, fake_auth-05#0]
* Hostname of affected host: desktop-l8c5gsj [auto: fake_auth-09#0, fake_auth-05#0]
* Human user account of affected host: shutchenson [auto: fake_auth-09#0]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

* High-severity malicious alert signatures:
  + ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) — 2 events [auto: fake_auth-09#0, fake_auth-06#4]
  + ET DROP Spamhaus DROP Listed Traffic Inbound group 5 — 2 events [auto: fake_auth-06#2, fake_auth-06#0]
* High-severity malicious destinations:
  + 5.252.153.241 — 4 events
  + 10.1.17.215 — 2 events
  + 185.188.32.26 — 2 events
* High-severity malicious sources:
  + 45.125.66.32 — 1 events
  + 45.125.66.252 — 1 events
* High-severity malicious signatures:
  + ET INFO PS1 Powershell File Request — 2 events [auto: fake_auth-09#0, fake_auth-06#4]
  + ET INFO TeamViewer Dyngate User-Agent — 2 events [auto: fake_auth-09#0, fake_auth-06#4]
* High-severity malicious alert timeline:
  + 2025-01-22 19:00 UTC — 10 events [auto: fake_auth-09#0, fake_auth-06#4]
  + 2025-01-22 20:00 UTC — 2 events [auto: fake_auth-09#0, fake_auth-06#4]

## Initial Infection Indicators

* download domains: ctldl.windowsupdate.com — 2 events [fake_auth-01#1]
* download domains: www.msftconnecttest.com — 2 events [fake_auth-01#1]
* download domains: au.download.windowsupdate.com — 1 events [fake_auth-01#1]
* download domains: 5.252.153.241 — 594 events [fake_auth-01#0]
* file types: other — 1813 events [fake_auth-01#7]
* file transfers > transfer details: 10.1.17.215 -> 13.107.21.239:443 : fuid: F1NJjy3oFAIPDAJDF3 — 1 events [fake_auth-01#4]

## Command-and-Control and Network Activity

* Derived from [fake_auth-09#0], the affected host 10.1.17.215 received 1823 connections from external destinations, with the most contacted external IP being 5.252.153.241, which received 1196 connections.
* Not established from the available artifacts whether the external IP 5.252.153.241 is a C2 server or a legitimate service.
* Derived from [fake_auth-02#0], the top external destinations for the affected host are 5.252.153.241 (1196), 23.207.166.9 (75), 185.188.32.26 (48), 204.79.197.203 (30), and 13.107.246.57 (26).
* Not established from the available artifacts whether these external destinations are C2 servers or legitimate services.
* Derived from [fake_auth-08#0], the affected host made connections to multiple domains, including oneclient.sfx.ms, which received 2 connections from the host.
* Not established from the available artifacts whether the domain oneclient.sfx.ms is a C2 server or a legitimate service.
* Assessment: The high volume of connections to external destinations, particularly to IP addresses that are not part of the private range, suggests potential malicious activity.
* Assessment: The presence of multiple domains in the list of connections, including those that are not typically associated with legitimate services, raises suspicions about potential C2 activity.

## Impact Assessment

* Assessment: The primary CIA component targeted is **confidentiality**, as the majority of the high-severity alerts and external connections are related to external destinations, suggesting potential external access to the network. [fake_auth-02#0]
* Assessment: The scale of external activity is **moderate**, with 119 distinct external destinations and 1196 connections to the most-contacted external IP, 5.252.153.241. [fake_auth-09#0]
* Assessment: The number of affected hosts is **one**, as the majority of the high-severity alerts and external connections are attributed to a single internal client, 10.1.17.215. [fake_auth-09#0]
* Assessment: Not established from the available artifacts whether the incident had a significant impact on the network's availability. [Not established from the available artifacts]
* Assessment: Not established from the available artifacts whether the incident had a significant impact on the network's integrity. [Not established from the available artifacts]

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but most likely root cause: Kerberos authentication exploitation, possibly using stolen or compromised credentials [fake_auth-04#0].
* Not established from the available artifacts: Initial vector (how the initial malicious payload was delivered), payload behavior, data exfiltration methods, queries that failed or were empty [fake_auth-09#0, fake_auth-02#0, fake_auth-04#1, fake_auth-04#0, fake_auth-03#0, fake_auth-01#2].
* Assessment: High confidence, Kerberos identity of 10.1.17.215: hostname(s) desktop-l8c5gsj; human user account(s) shutchenson [fake_auth-09#0].
* Not established from the available artifacts: Root cause of Kerberos identity compromise, whether shutchenson is the actual user or an impersonated account [fake_auth-09#0, fake_auth-03#0].
* Assessment: Low confidence, but most likely root cause: High-severity alert destinations (e.g., 5.252.153.241, 185.188.32.26) may indicate a command-and-control (C2) server or malicious domain [fake_auth-09#0, fake_auth-02#0].
* Not established from the available artifacts: Nature of the C2 server or malicious domain, whether it is related to the initial exploitation or a separate incident [fake_auth-09#0, fake_auth-02#0].
* Not established from the available artifacts: Impact of the incident, including any data exfiltration, lateral movement, or other malicious activities [fake_auth-09#0, fake_auth-02#0, fake_auth-04#1, fake_auth-04#0, fake_auth-03#0, fake_auth-01#2].

## Corrective and Preventive Actions

* Isolate the internal client 10.1.17.215 from the rest of the network to prevent further potential malicious activity. [auto: fake_auth-09#0, fake_auth-08#3]
* Block the external IP address 5.252.153.241 from accessing the internal client's network to prevent further malicious activity. [auto: fake_auth-09#0, fake_auth-01#2]
* Reset the Kerberos identity of 10.1.17.215 to prevent potential future authentication attempts. [auto: fake_auth-09#0, fake_auth-08#3]
* Review and update the network segmentation and access controls to ensure that the internal client 10.1.17.215 is not accessing external destinations that are not part of the approved network segment. [auto: fake_auth-09#0, fake_auth-08#3]

## Answers to Investigation Questions

1. The IP address of the potentially infected internal host in the LAN is 10.1.17.215 [fake_auth-09#0].
2. The hostname of the potentially infected machine in the LAN is desktop-l8c5gsj [fake_auth-05#0, fake_auth-04#2, fake_auth-04#3, fake_auth-03#0].
3. The Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN is shutchenson [fake_auth-03#0, fake_auth-04#1].
4. The likely fake or suspicious domains / URLs for initial infection are:
   * c.go-mpulse.net [fake_auth-08#2]
   * dmpsync.3lift.com [fake_auth-08#2]
   * dpm.demdex.net [fake_auth-08#2]
   * oneclient.sfx.ms [fake_auth-08#0]
   * img-s-msn-com.akamaized.net [fake_auth-08#0]
   * px.owneriq.net [fake_auth-08#0]
   * ag.innovid.com [fake_auth-08#0]
   * google-authenticator.burleson-appliance.net [fake_auth-08#3]
   * jadserve.postrelease.com [fake_auth-08#3]
   * mscom.demdex.net [fake_auth-08#3]
 * play.vidyard.com [fake_auth-08#3, fake_auth-06#4, fake_auth-06#2]
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are:
   * 5.252.153.241 [fake_auth-09#0, fake_auth-06#2]
   * 23.207.164.186 [fake_auth-08#2]
   * 23.207.166.9 [fake_auth-02#0]
   * 23.205.110.12 [fake_auth-08#0]
   * 23.205.110.59 [fake_auth-08#0]
   * 23.199.168.146 [fake_auth-08#0]
   * 104.18.8.76 [fake_auth-08#2]
   * 104.21.64.1 [fake_auth-08#3]
   * 44.237.90.153 [fake_auth-08#3]
   * 35.71.139.29 [fake_auth-08#2]
   * 35.84.233.181 [fake_auth-08#3]
   * 151.101.1.181 [fake_auth-08#3]
   * 45.125.66.32 [fake_auth-06#4]
   * 45.125.66.252 [fake_auth-07#0, fake_auth-07#1]
6. The first signs of infection activity appeared during the hour of 19:00 UTC on 2025-01-22 [fake_auth-09#0, fake_auth-06#4, fake_auth-06#2].
7. Not established from the available artifacts.
8. Not established from the available artifacts.

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
