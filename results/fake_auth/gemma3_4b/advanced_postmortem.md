# Incident Postmortem: Network security incident investigation

## Incident Summary



## Affected Host and User

*   Internal client 10.1.17.215 is associated with the human user account shutchenson [fake_auth-09#0].
* The host desktop-l8c5gsj is associated with the human user account shutchenson,. [fake_auth-09#0, fake_auth-05#0]
*   10.1.17.215 initiated connections to 5.252.153.241 [fake_auth-09#0].
*   The host 10.1.17.215 exhibited high-severity alerts targeting 5.252.153.241, 10.1.17.215, and 185.188.32.26 [fake_auth-09#0].

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts

*   Two events of a malicious alert signature, “ET MALWARE Fake Microsoft Teams CnC Payload Request (GET),” were detected [fake_auth-06#1].
*   One event of an informational alert signature, “ET INFO Observed UA-CPU Header,” was detected [fake_auth-06#2].
*   Four events of a high-severity destination, 5.252.153.241, were detected [fake_auth-06#2].
*   Six events of a high-severity source, 10.1.17.215, were detected [fake_auth-06#3].
*   The internal client 10.1.17.215 initiated 1196 connections to the external IP 5.252.153.241 [fake_auth-09#0].
*   Two events of the alert signature “ET DROP Spamhaus DROP Listed Traffic Inbound group 5” were detected [fake_auth-06#0].

## Initial Infection Indicators

* Download events occurred to ctldl.windowsupdate.com and www.msftconnecttest.com, with a total of 2 + 2 = 4 events. [fake_auth-01#1]
* The host 10.1.17.215 initiated HTTP requests to 5.252.153.241 with 594 events. [fake_auth-01#7, fake_auth-01#0]
* HTTP requests were observed from 10.1.17.215 to 5.252.153.241 including /1517096937 and /api/file/get-file/29842.ps1. [fake_auth-01#2, fake_auth-01#0]
* File transfers were detected from 10.1.17.215 to 13.107.21.239:443 with the fuid F1NJjy3oFAIPDAJDF3. [fake_auth-01#4, fake_auth-01#6]
* File transfers were detected from 10.1.17.215 to 13.107.42.14:443 with the fuid F4zRqw2DUGjBIBdRvh. [fake_auth-01#6]
* File transfers were detected from 10.1.17.215 to 13.71.55.58:443 with the fuid FH1h2Z2c3UICAAcBMb. [fake_auth-01#6]

## Command-and-Control and Network Activity

*   Internal client 10.1.17.215 initiated 1823 connections, with 5.252.153.241 receiving the most connections (1196). [fake_auth-09#0]
*   The Kerberos identity for 10.1.17.215 was desktop-l8c5gsj, and the user account was shutchenson. [fake_auth-05#0]
*   Suricata alerts occurred between 19:00 and 20:00 UTC on 2025-01-22, with 10 alerts detected. [fake_auth-02#0]
*   High-severity alerts targeted 5.252.153.241 (4), 10.1.17.215 (2), and 185.188.32.26 (2). [fake_auth-02#0]
*   Connections to 5.252.153.241 were associated with domain lookups for c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, and ds.reson8.com. [fake_auth-08#2]
*   Connections to 10.1.17.215 were associated with domain lookups for google-authenticator.burleson-appliance.net, jadserve.postrelease.com, mscom.demdex.net, and play.vidyard.com. [fake_auth-08#3]
*   The most frequent destination IP address for connections originating from 10.1.17.215 was 23.207.166.9 (75 events). [fake_auth-02#0]
*   Connections to oneclient.sfx.ms (4 events) were directed to 23.212.73.35 (2) and 23.41.241.15 (1). [fake_auth-08#0]

## Impact Assessment

*   Assessment: The primary CIA component targeted appears to be confidentiality, evidenced by the high volume of HTTP downloads and TLS certificate activity [fake_auth-02#0, fake_auth-08#0].
*   The host 10.1.17.215 initiated 1823 external connections, with 5.252.153.241 being the most contacted external IP address [fake_auth-09#0].
*   Four high-severity alerts originating from 10.1.17.215 targeted destinations including 5.252.153.241, 10.1.17.215 and 185.188.32.26 [fake_auth-06#2, fake_auth-09#0].
*   The domain oneclient.sfx.ms was accessed from 10.1.17.215, with multiple connections to 23.212.73.35 [fake_auth-08#0].

## Root Cause and Evidence Gaps

Assessment: The most likely root cause is unauthorized access originating from client 10.1.17.215, utilizing Kerberos and SMB protocols to interact with the domain controller WIN-GSH54QLW48D and external destinations. [auto: fake_auth-04#1, fake_auth-04#0]
*   10.1.17.215 was the primary source of all observed activity, generating 1823 events and connecting to 119 distinct external destinations [fake_auth-09#0].
*   High-severity alerts focused on connections to 5.252.153.241, 10.1.17.215, and 185.188.32.26 [fake_auth-09#0].
*   Multiple services involving LDAP and SMB protocols were initiated by 10.1.17.215 against the domain controller [fake_auth-04#1, fake_auth-04#0].
*   The client account ‘shutchenson’ exhibited a high volume of activity [fake_auth-03#0].
*   HTTP requests from 10.1.17.215 targeted 5.252.153.241, including a PowerShell script download [fake_auth-01#2].
*   Not established: The specific nature of the PowerShell script, the purpose of the DynGate requests, and the overall command-and-control infrastructure are not established from the available artifacts. [Not established]

## Corrective and Preventive Actions

*   Isolate client account 10.1.17.215 [fake_auth-09#0].
*   Block external IP address 5.252.153.241 [fake_auth-09#0].
*   Block domain oneclient.sfx.ms [fake_auth-08#0].
*   Block HTTP requests originating from 10.1.17.215 to 5.252.153.241 [fake_auth-01#2].
*   Reset user account shutchenson [fake_auth-09#0].

## Answers to Investigation Questions

* 1. The IP address of the potentially infected internal host in the LAN is 10.1.17.215 [fake_auth-09#0].
* 2. The hostname of the potentially infected machine in the LAN is desktop-l8c5gsj [fake_auth-05#0, fake_auth-09#0].
* 4. Likely fake or suspicious domains / URLs for initial infection include c.go-mpulse.net, dmpsync.3lift.com, dpm.demdex.net, oneclient.sfx.ms, google-authenticator.burleson-appliance.net, and px.owneriq.net. [fake_auth-08#2, fake_auth-08#0, fake_auth-08#3]
* 5. Suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication include 5.252.153.241, 23.207.164.186, 35.71.139.29, 104.18.8.76, 23.212.73.35, 23.41.241.15, 23.55.125.39, 45.125.66.32, 45.125.66.252, 45.125.66.32, and 104.21.64.1. [fake_auth-09#0, fake_auth-08#2, fake_auth-08#0, fake_auth-06#4, fake_auth-07#0, fake_auth-08#3]

---
Verification note: 6 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
