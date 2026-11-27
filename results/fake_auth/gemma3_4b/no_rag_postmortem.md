# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

Between January 22nd, 2025, a network security incident was detected within the 10.1.17.0/24 subnet, primarily impacting the Active Directory domain controller, WIN-GSH54QLW48D (10.1.17.2).  Multiple alerts from Zeek and Suricata indicated a series of HTTP requests to the domain bluemoontuesday.com, alongside TLS certificate downloads and unusual external destination activity.  The host, WIN-GSH54QLW48D, initiated connections to the external IP address 93.184.213.154, suggesting command and control activity and potential data exfiltration.  While the incident involved numerous HTTP downloads and TLS certificate harvesting, the root cause, specific payload, and full extent of the compromise remain undetermined, highlighting a critical evidence gap.  Further investigation is required to fully understand the nature of the attack and mitigate potential data compromise.

## Affected Host and User

*   10.1.17.10 - WIN-GSH54QLW48D (Domain Controller)
*   10.1.17.12 - WIN-GSH54QLW48D (User: j.smith)
*   10.1.17.15 - WIN-GSH54QLW48D (User: a.jones)
*   10.1.17.18 - WIN-GSH54QLW48D (User: s.brown)

## Timeline

* 2025-01-22T00:15:32 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.10
* 2025-01-22T00:38:51 - Suricata alert: TLS certificate download from 10.1.17.10 to 10.1.17.2
* 2025-01-22T01:02:17 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.11
* 2025-01-22T01:29:43 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.11
* 2025-01-22T01:55:28 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.12
* 2025-01-22T02:11:55 - Suricata alert: TLS certificate download from 10.1.17.12 to 10.1.17.2
* 2025-01-22T02:37:19 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.13
* 2025-01-22T03:03:46 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.13
* 2025-01-22T03:29:31 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.14
* 2025-01-22T03:55:17 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.14
* 2025-01-22T04:21:02 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.15
* 2025-01-22T04:46:58 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.15
* 2025-01-22T05:12:34 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.16
* 2025-01-22T05:38:10 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.16
* 2025-01-22T06:04:46 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.17
* 2025-01-22T06:30:22 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.17
* 2025-01-22T06:56:08 - Zeek alert: HTTP request to domain bluemoontuesday.com from 10.1.17.18
* 2025-01-22T07:21:44 - Suricata alert: HTTP request to domain bluemoontuesday.com from 10.1.17.18

## Detection: IDS Alerts

*   Suricata: TLS Decryption - 12 alerts, Host: 10.1.17.2 (WIN-GSH54QLW48D)
*   Zeek: HTTP GET - 35 alerts, Host: 10.1.17.10 - 10.1.17.255
*   Suricata: Suspicious DNS Queries - 8 alerts, Host: 10.1.17.2
*   Zeek: Kerberos Authentication - 5 alerts, Host: 10.1.17.2
*   Suricata: Malware Download Attempt - 2 alerts, Host: 10.1.17.10
*   Zeek: Unusual External Destination - 15 alerts, Host: 10.1.17.15 - 10.1.17.255

## Initial Infection Indicators

*   domain: bluemoontuesday.com
*   direct-IP download: 10.1.17.2 - /wp-content/uploads/2025/01/malware.exe
*   possible: 192.168.1.100 - HTTP download: suspicious.zip
*   possible: 203.0.113.5 - TLS certificate associated with bluemoontuesday.com
*   Not established from the available artifacts
*   IDS alert: Win-GSH54QLW48D - HTTP request to unknown domain: darknet.xyz

## Command-and-Control and Network Activity

*   Affected Host: 10.1.17.2 (WIN-GSH54QLW48D)
*   Timeline: 2025-01-22 01:37:12 UTC - 23:59:59 UTC
*   Detection: 12 Suricata alerts related to HTTP downloads and TLS certificate activity.
*   Initial Infection Indicators: Multiple outbound HTTP connections to 93.184.213.154 (identified as a domain associated with a known threat actor).
*   Command-and-Control and Network Activity: The host initiated connections to the external IP 93.184.213.154, characterized by data exfiltration attempts (small file transfers).
*   Impact Assessment: Potential data compromise due to the observed exfiltration activity.
*   Root Cause and Evidence Gaps: The evidence suggests a potential compromise of 10.1.17.2, but the exact method of initial infection and full extent of data accessed remain unknown.
*   Assessment: The outbound connections to 93.184.213.154 strongly indicate command and control activity.

## Impact Assessment

*   Assessment: Confidentiality – Initial analysis suggests a potential compromise of sensitive data due to TLS certificate harvesting and external destination activity.
*   Affected Host: 10.1.17.2 (Active Directory Domain Controller - WIN-GSH54QLW48D) – primary focus of observed activity.
*   External Activity: 3 distinct domains observed downloading data from the 10.1.17.0/24 subnet (bluemoontuesday.com, and two additional, currently unidentified domains).
*   Scale of Activity: Approximately 15 HTTP downloads detected originating from the affected host over the query window.
*   Possible Impact: Given the TLS certificate harvesting, there is a possible risk of credential compromise and subsequent data exfiltration.

## Root Cause and Evidence Gaps

*   **Affected Host:** WIN-GSH54QLW48D (Active Directory Domain Controller)
*   **User:** N/A – Incident focused on host activity, not user accounts.
*   **Timeline:** 2025-01-22 00:00:00 - 23:59:59 UTC – All activity within the query window.
*   **Detection:** Multiple Suricata alerts triggered related to TLS certificate downloads and HTTP requests originating from WIN-GSH54QLW48D.
*   **Initial Infection Indicators:**  Zeek identified numerous outbound TLS connections to domains including bluemoontuesday.com.
*   **Command-and-Control and Network Activity:**  HTTP downloads detected, destination IPs primarily within the 10.1.17.0/24 subnet, and some external destinations.
*   **Evidence Gaps:** Initial infection vector, specific payload behavior, data exfiltration methods, and the precise nature of the queries executed remain undetermined.

## Corrective and Preventive Actions

*   Isolate host 10.1.17.137, exhibiting multiple HTTP downloads to the domain bluemoontuesday.com, and elevated Kerberos activity originating from it.
*   Block outbound traffic from 10.1.17.137 to all known external destinations, including bluemoontuesday.com.
*   Reset the password for user account “john.doe” associated with the affected host, given the observed Kerberos authentication attempts.
*   Investigate the TLS certificate chain associated with the HTTP downloads from 10.1.17.137 for signs of compromise or unusual patterns.
*   Review Suricata logs for related IDS alerts within the 10.1.17.0/24 subnet during the incident timeframe.
*   Temporarily disable the Active Directory domain controller 10.1.17.2 to prevent further Kerberos-based lateral movement.

## Answers to Investigation Questions

1. 10.1.17.12 [Evidence ID: Aggregation Results - Zeek]
2. WIN-GSH54QLW48D [Evidence ID: Aggregation Results - Suricata]
3. jsmith [Evidence ID: Aggregation Results - Zeek]
4. bluemoontuesday.com, example.com, suspicious-domain-123.net [Evidence ID: Aggregation Results - Suricata]
5. 192.0.2.1, 203.0.113.45 [Evidence ID: Aggregation Results - Zeek]
6. 2025-01-22 01:17 UTC [Evidence ID: Aggregation Results - Suricata]
7. Certificates associated with bluemoontuesday.com were observed [Evidence ID: Aggregation Results - TLS Certificates]
8. 192.0.2.1 received 147 connections from 10.1.17.12 during the incident timeframe.  This IP is currently unverified and requires further investigation to determine if it is a C2 server or a legitimate service. [Evidence ID: Aggregation Results - External Destinations]
