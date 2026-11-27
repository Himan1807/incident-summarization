# Incident Postmortem: Network security incident investigation

## Incident Summary

- Host 10.1.17.215 (desktop-l8c5gsj), associated with user shutchenson, exhibited suspicious network behavior during the incident window [fake_auth-09#0].
- The earliest detection occurred at 19:00 UTC, marked by a surge of high-severity Suricata alerts originating from this host [fake_auth-06#4].
- The host made extensive connections to 5.252.153.241, the most contacted external IP, which is assessed as a potential C2 server based on traffic patterns and alert correlation [fake_auth-02#0, fake_auth-09#0].
- HTTP downloads from 5.252.153.241 included a PowerShell script, suggesting a likely initial compromise vector involving script-based malware [fake_auth-01#2].
- Assessment: The primary impact is on confidentiality, given the volume of outbound connections and lack of evidence indicating data exfiltration or integrity breaches [fake_auth-02#0, fake_auth-09#0].

## Affected Host and User

- Internal client IP address 10.1.17.215 is associated with hostname desktop-l8c5gsj and human user account shutchenson [fake_auth-09#0].
- Hostname desktop-l8c5gsj resolves to source IP 10.1.17.215 based on Kerberos service request activity [fake_auth-05#0].
- The host made Kerberos requests for services including netlogon, host, krbtgt, and ldap using the domain controller’s FQDN, confirming domain membership and authentication attempts from 10.1.17.215. [fake_auth-04#3, fake_auth-04#2]
- Multiple Kerberos TGS and TGT requests were observed from 10.1.17.215 for services such as krb_tcp, LDAP, cifs, and DESKTOP-L8C5GSJ$, indicating active user and machine authentication activity. [fake_auth-04#0, fake_auth-04#1]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

- ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) was observed in 2 events [fake_auth-06#1].
- ET INFO Observed UA-CPU Header was detected in 1 event [fake_auth-06#1].
- ET DROP Spamhaus DROP Listed Traffic Inbound group 5 triggered 2 high-severity alerts [fake_auth-06#2].
- ET INFO PS1 Powershell File Request and ET INFO TeamViewer Dyngate User-Agent each generated 2 high-severity events [fake_auth-06#3].
- High-severity alerts originated from internal host 10.1.17.215 in 6 events [fake_auth-06#3].

## Initial Infection Indicators

- 10.1.17.215 downloaded a PowerShell script from 5.252.153.241 via HTTP request to /api/file/get-file/29842.ps1 [fake_auth-01#2]
- HTTP requests from 10.1.17.215 to 185.188.32.26 on port 80 included URIs with "client=DynGate", suggesting possible use of a dynamic DNS tunneling tool [fake_auth-01#2]
- 10.1.17.215 initiated multiple connections to IP address 5.252.153.241, a direct IP connection with no domain resolution, transferring files over HTTP [fake_auth-01#0]
- File transfer logs show 10.1.17.215 sent files to external IPs 13.107.21.239, 13.107.42.14, and 13.71.55.58 over HTTPS, indicating possible exfiltration [fake_auth-01#6]
- The file type "powershell" was observed in downloads, with source host 10.1.17.215, suggesting possible malicious script retrieval [fake_auth-01#7]
- Not established from the available artifacts.

## Command-and-Control and Network Activity

- Internal client 10.1.17.215 initiated 1823 external connection events to 119 distinct destinations during the query window [fake_auth-02#0].
- The most-contacted external IP from 10.1.17.215 was 5.252.153.241, with 1196 connections recorded [fake_auth-02#0].
- Suricata high-severity alerts involved external destinations 5.252.153.241 and 185.188.32.26, among others [fake_auth-09#0].
- Multiple domains resolved to external IPs contacted by 10.1.17.215, including tracking and advertising-related domains,,. [fake_auth-08#2, fake_auth-08#3, fake_auth-08#0]
- The domain google-authenticator.burleson-appliance.net resolved to 104.21.64.1 and was contacted by 10.1.17.215 [fake_auth-08#3].
- The domain oneclient.sfx.ms, associated with Microsoft services, was contacted four times and resolved to multiple Akamai-hosted IPs [fake_auth-08#0].
- Assessment: The volume and pattern of connections to 5.252.153.241, combined with Suricata alerts, suggest this IP may be a C2 server or malicious endpoint,. [fake_auth-02#0, fake_auth-09#0]
- Assessment: Connections to advertising and tracking domains do not establish malicious intent but indicate potential browser-based exposure or ad-fraud activity,,. [fake_auth-08#2, fake_auth-08#3, fake_auth-08#0]

## Impact Assessment

- The internal client 10.1.17.215 initiated 1823 external connection events to 119 distinct destinations, with 5.252.153.241 contacted 1196 times [fake_auth-02#0].
- High-severity Suricata alerts were generated involving 10.1.17.215 as source or destination during the incident window, including inbound DROP-listed traffic [fake_auth-06#2].
- Suricata high-severity alerts occurred between 19:00 and 20:00 UTC, with 10 alerts at 19:00 and 2 at 20:00 UTC, indicating concentrated malicious activity [fake_auth-06#4].
- Multiple domains contacted originated from 10.1.17.215, including tracking and telemetry services, with destinations mapped to known content delivery networks. [fake_auth-08#0, fake_auth-08#2]
- Assessment: Confidentiality is the primary CIA component targeted, as evidenced by extensive outbound connections from 10.1.17.215 to external IPs with no indication of data exfiltration volume or integrity violations. [fake_auth-02#0, fake_auth-09#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is execution of a malicious PowerShell script retrieved from an external server, with medium confidence [fake_auth-01#2].
- The initial infection vector is not established from the available artifacts.
- Whether the payload performed additional malicious actions beyond C2 communication is not established from the available artifacts.
- Data exfiltration attempts or success are not established from the available artifacts.
- The method of persistence, if any, is not established from the available artifacts.
- Whether the domain 5.252.153.241 is exclusively controlled by adversaries is not established from the available artifacts.

## Corrective and Preventive Actions

- Isolate host 10.1.17.215 (desktop-l8c5gsj) due to high volume of suspicious external connections and associated high-severity alerts [fake_auth-09#0].
- Reset credentials for user account shutchenson and machine account DESKTOP-L8C5GSJ$ given their association with malicious activity from 10.1.17.215 [fake_auth-03#0].
- Block outbound traffic to IP 5.252.153.241, the most contacted external destination linked to high-severity C2-related HTTP requests [fake_auth-01#2].
- Block outbound traffic to IP 185.188.32.26 due to its involvement in high-severity alerts and C2 traffic on port 80 [fake_auth-09#0].

## Answers to Investigation Questions

1. 10.1.17.215 [fake_auth-09#0]
2. desktop-l8c5gsj [fake_auth-09#0]
3. shutchenson [fake_auth-03#0]
4. google-authenticator.burleson-appliance.net, jadserve.postrelease.com [fake_auth-08#3]
5. 5.252.153.241, 185.188.32.26, 45.125.66.32, 45.125.66.252 [fake_auth-09#0, fake_auth-06#2, fake_auth-06#4]
6. 2025-01-22 19:00 UTC [fake_auth-09#0]
7. 45.125.66.32, 45.125.66.252 [fake_auth-07#0]
8. 5.252.153.241; Not established from the available artifacts [fake_auth-02#0]

---
Verification note: 3 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [fake_auth-05#0]
U2. Not established from the available artifacts [fake_auth-09#0]
U3. Not established from the available artifacts [fake_auth-01#2]
