# Incident Postmortem: Network security incident investigation

## Incident Summary

- The affected host was 10.1.17.215 (desktop-l8c5gsj), associated with the user shutchenson [fake_auth-09#0].
- The earliest alert occurred at 2025-01-22 19:00 UTC, marking the start of high-severity Suricata alerts [fake_auth-09#0].
- The primary C2 candidate was external IP 5.252.153.241, which received the majority of connections from 10.1.17.215 and triggered multiple high-severity alerts [fake_auth-09#0].
- Assessment: The high volume of connections to 5.252.153.241, combined with suspicious HTTP requests and file downloads, suggests potential unauthorized external communication, though further analysis is required to confirm C2 activity [fake_auth-09#0].

## Affected Host and User

- Internal client 10.1.17.215, with hostname desktop-l8c5gsj, was associated with the human user account shutchenson [fake_auth-09#0].
- The host 10.1.17.215 initiated 1823 external connections to 119 distinct external destinations, with the most-contacted external IP being 5.252.153.241 [fake_auth-09#0].
- Kerberos activity from 10.1.17.215 included services such as krbtgt/BLUEMOONTUESDAY and LDAP/WIN-GSH54QLW48D.bluemoontuesday.com [fake_auth-04#0].
- Suricata alerts involving 10.1.17.215 occurred between 2025-01-22 19:00 UTC and 2025-01-22 20:00 UTC, with high-severity alerts targeting 5.252.153.241 and 185.188.32.26 [fake_auth-09#0].

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

- High-severity alerts included ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) with 2 events and ET DROP Spamhaus DROP Listed Traffic Inbound group 5 with 2 events. [fake_auth-06#1, fake_auth-06#4]
- Internal client 10.1.17.215 was involved in 6 high-severity alerts, including ET MALWARE Fake Microsoft Teams CnC Payload Request (GET) and ET INFO PS1 Powershell File Request [fake_auth-06#3].
- External IPs 5.252.153.241 and 185.188.32.26 were destinations for high-severity alerts, with 4 and 2 events respectively. [fake_auth-06#2, fake_auth-09#0]
- Informational alerts included ET INFO Observed UA-CPU Header (1 event) and ET INFO Microsoft Connection Test (2 events). [fake_auth-06#1, fake_auth-06#0]
- Suricata alerts peaked at 2025-01-22 19:00 UTC with 10 events, spanning until 20:00 UTC. [fake_auth-06#4, fake_auth-09#0]
- External sources 45.125.66.32 and 45.125.66.252 triggered high-severity alerts, each with 1 event [fake_auth-06#4].

## Initial Infection Indicators

- Host 10.1.17.215 made repeated HTTP requests to external IP 185.188.32.26 with suspicious query parameters (`/din.aspx?s=...`) [fake_auth-01#2].
- Host 10.1.17.215 initiated multiple file transfers to external IPs 13.107.21.239, 13.107.42.14, and 13.71.55.58 over HTTPS [fake_auth-01#6].
- Possible suspicious activity: Host 10.1.17.215 downloaded files directly from external IP 5.252.153.241 without a domain name [fake_auth-01#0].
- Host 10.1.17.215 was the source of 1823 download events, including 5 `.exe` and 5 PowerShell files [fake_auth-01#7].
- No initial infection vector is visible from the available artifacts.

## Command-and-Control and Network Activity

- Internal client 10.1.17.215 initiated 1823 external connections to 119 distinct destinations, with the most connections (1196) directed to external IP 5.252.153.241 [fake_auth-09#0].
- Suricata alerts associated with 10.1.17.215 occurred between 2025-01-22 19:00 UTC and 2025-01-22 20:00 UTC, with 10 alerts in the earliest hour [fake_auth-09#0].
- High-severity Suricata alerts were triggered for connections to 5.252.153.241 (4 alerts), 10.1.17.215 (2 alerts), and 185.188.32.26 (2 alerts) [fake_auth-09#0].
- External destinations contacted by 10.1.17.215 included domains such as c.go-mpulse.net, dmpsync.3lift.com, and dpm.demdex.net, each with a single connection [fake_auth-08#2].
- Additional domains contacted by 10.1.17.215 included google-authenticator.burleson-appliance.net, jadserve.postrelease.com, and mscom.demdex.net, each with a single connection [fake_auth-08#3].
- Domains such as oneclient.sfx.ms and img-s-msn-com.akamaized.net were contacted multiple times by 10.1.17.215, with 4 and 2 connections respectively [fake_auth-08#0].
- Assessment: The high volume of connections to 5.252.153.241, combined with high-severity alerts, suggests potential suspicious activity, but further analysis is required to confirm C2 activity [fake_auth-09#0].
- Assessment: The domains contacted by 10.1.17.215 appear to include legitimate services, but the presence of high-severity alerts warrants investigation into potential misuse or compromise. [fake_auth-08#2, fake_auth-08#3]

## Impact Assessment

- High-severity IDS alerts were triggered for external destinations 5.252.153.241 (4 events), 185.188.32.26 (2 events), and internal client 10.1.17.215 (2 events). [fake_auth-06#2, fake_auth-09#0]
- Internal client 10.1.17.215 contacted domains such as oneclient.sfx.ms (4 events), img-s-msn-com.akamaized.net (2 events), and px.owneriq.net (2 events) [fake_auth-08#0].
- Additional domains contacted by 10.1.17.215 include c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, and ds.reson8.com, each with 1 event [fake_auth-08#2].
- Assessment: The primary CIA component targeted was confidentiality, based on the high volume of external connections and domain queries from 10.1.17.215, with possible data exfiltration activity. [fake_auth-02#0, fake_auth-09#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is unauthorized external communication initiated by 10.1.17.215 (desktop-l8c5gsj, user shutchenson) to 5.252.153.241, supported by high-volume HTTP requests and Suricata alerts (medium confidence). [fake_auth-09#0, fake_auth-01#2]
- Not established: The initial infection vector or payload delivery mechanism is not identified from the available artifacts.
- Not established: The behavior or purpose of the downloaded file `/api/file/get-file/29842.ps1` is unclear [fake_auth-01#2].
- Not established: Evidence of data exfiltration or lateral movement within the LAN is not present.
- Not established: The role of 185.188.32.26 in the incident, beyond HTTP requests, is not determined [fake_auth-01#2].
- Not established: The Kerberos activity involving DESKTOP-L8C5GSJ$ and LDAP services is not linked to malicious intent. [fake_auth-04#1, fake_auth-04#0]
- Not established: The full scope of external destinations contacted by 10.1.17.215 beyond the top IPs is not documented [fake_auth-02#0].

## Corrective and Preventive Actions

- Isolate host 10.1.17.215 due to its high volume of external connections and involvement in high-severity alerts [fake_auth-09#0].
- Reset credentials for user account `shutchenson` and machine account `DESKTOP-L8C5GSJ$` due to their association with suspicious activity [fake_auth-03#0].
- Block external IP 5.252.153.241 to prevent further communication with the compromised host. [fake_auth-09#0, fake_auth-01#2]
- Investigate and block domains `oneclient.sfx.ms` and `google-authenticator.burleson-appliance.net` due to their connection to suspicious activity. [fake_auth-08#0, fake_auth-08#3]
- Review and restrict HTTP requests to `/api/file/get-file/29842.ps1` and `/din.aspx` paths to prevent potential payload delivery [fake_auth-01#2].

## Answers to Investigation Questions

1. 10.1.17.215 [fake_auth-09#0]
2. desktop-l8c5gsj [fake_auth-09#0]
3. shutchenson [fake_auth-09#0]
4. Not established from the available artifacts.
5. 5.252.153.241, 185.188.32.26 [fake_auth-09#0]
6. 2025-01-22 19:00 UTC [fake_auth-09#0]
7. 45.125.66.252, 45.125.66.32 [fake_auth-07#0]
8. 5.252.153.241 [fake_auth-09#0]

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 1 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
