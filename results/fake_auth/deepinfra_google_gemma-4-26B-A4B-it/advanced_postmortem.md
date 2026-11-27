# Incident Postmortem: Network security incident investigation

## Incident Summary

The host desktop-l8c5gsj (10.1.17.215) and user account shutchenson were affected by this incident. The earliest alert hour was 2025-01-22 19:00 UTC. The external IP 5.252.153.241 is the main C2 candidate due to receiving 1,196 connections and high-severity Suricata alerts. Assessment: The host was likely compromised via a PowerShell script download from 5.252.153.241. Assessment: There is a possible compromise of confidentiality due to high-volume connections to multiple external IPs and domains. [fake_auth-09#0, fake_auth-06#4, fake_auth-02#0, fake_auth-08#0, fake_auth-08#2]

## Affected Host and User

* IP address 10.1.17.215 [fake_auth-09#0]
* Hostname desktop-l8c5gsj [fake_auth-09#0]
* Human user account shutchenson [fake_auth-09#0]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

* ET MALWARE Fake Microsoft Teams CnC Payload Request (GET): 2 events involving 10.1.17.215 [fake_auth-06#1, fake_auth-06#3].
* ET DROP Spamhaus DROP Listed Traffic Inbound group 5: 2 events [fake_auth-06#2, fake_auth-06#0].
* ET INFO PS1 Powershell File Request: 2 events [fake_auth-06#3, fake_auth-06#0].
* ET INFO TeamViewer Dyngate User-Agent: 2 events [fake_auth-06#3, fake_auth-06#0].
* ET INFO Microsoft Connection Test: 2 events [fake_auth-06#0].
* ET INFO Observed UA-CPU Header: 1 event [fake_auth-06#1].

## Initial Infection Indicators

* Possible suspicious HTTP requests to 185.188.32.26 from 10.1.17.215 [fake_auth-01#2].
* Assessment: 5.252.153.241 is a suspicious download domain based on high event volume from 10.1.17.215 [fake_auth-01#0].

## Command-and-Control and Network Activity

* Internal client 10.1.17.215 generated 1823 events across 119 distinct external destinations [fake_auth-02#0].
* The external IP receiving the most connections from 10.1.17.215 is 5.252.153.241 with 1196 connections [fake_auth-09#0].
* High-severity Suricata alerts were directed to 5.252.153.241 (4), 10.1.17.215 (2), and 185.188.32.26 (2) [fake_auth-09#0].
* Assessment: The high volume of connections to 5.252.153.241 combined with high-severity alerts suggests this IP is a C2 server [fake_auth-09#0].
* Assessment: The presence of multiple domains such as google-authenticator.burleson-appliance.net and play.vidyard.com indicates a mix of legitimate and potentially suspicious network traffic [fake_auth-08#3].
* Assessment: Not established from the available artifacts.

## Impact Assessment

* One host (10.1.17.215) is identified as the primary source of activity [fake_auth-02#0].
* The scale of external activity includes 1,823 events directed to 119 distinct external destinations [fake_auth-02#0].
* Assessment: Possible compromise of confidentiality due to high-volume connections to multiple external IPs and domains [fake_auth-02#0, fake_auth-08#0, fake_auth-08#2].

## Root Cause and Evidence Gaps

* Assessment: Compromise of host 10.1.17.215 via a PowerShell script download from 5.252.153.241 (Medium confidence). [auto: fake_auth-09#0, fake_auth-02#0]
* Initial infection vector is not established from the available artifacts.
* Payload behavior and specific post-exploitation actions are not established from the available artifacts.
* Data exfiltration is not established from the available artifacts.
* The specific mechanism of the Suricata alerts is not established from the available artifacts.

## Corrective and Preventive Actions

* Isolate host 10.1.17.215 (desktop-l8c5gsj) [fake_auth-09#0].
* Reset credentials for the shutchenson account [fake_auth-09#0].
* Block external IP 5.252.153.241 [fake_auth-09#0].
* Block external IP 185.188.32.26 [fake_auth-09#0].

## Answers to Investigation Questions

1. 10.1.17.215 [fake_auth-09#0]
2. desktop-l8c5gsj [fake_auth-09#0]
3. shutchenson [fake_auth-09#0]
4. Not established from the available artifacts.
5. 5.252.153.241, 185.188.32.26, 45.125.66.32, 45.125.66.252 [fake_auth-09#0, fake_auth-06#4, fake_auth-07#0]
6. 2025-01-22 19:00 UTC [fake_auth-09#0]
7. 45.125.66.252 and 45.125.66.32 [fake_auth-07#0]
8. 5.252.153.241; Assessment: Not established from the available artifacts. [fake_auth-09#0, fake_auth-02#0]

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
