# The sections exactly as the 3B model produced them in the user's run (annotation markers removed).
RAW = {
"Affected Host and User": """### Affected Host and User
* **Affected Host:**
        + 10.2.28.88 (desktop-teyq2nr)
* **Affected User:**
        + brolf""",
"Timeline": """* 2026-02-28 19:00 UTC: First high-severity alerts detected [easy_123-06#2]
* 2026-02-28 20:00 UTC: 119 high-severity alerts detected [easy_123-06#2]
* 2026-02-28 21:00 UTC: 120 high-severity alerts detected [easy_123-06#2]
* 2026-02-28 22:00 UTC: 120 high-severity alerts detected [easy_123-06#3]
* 2026-02-28 23:00 UTC: 120 high-severity alerts detected [easy_123-06#3]
* 2026-03-01 00:00 UTC: 36 high-severity alerts detected [easy_123-06#3]
* 2026-02-28 19:00 UTC: First Suricata alert detected, earliest alert hour [easy_123-08#0]
* 2026-02-28 19:00 UTC: Internal client 10.2.28.88 starts making external connections [easy_123-08#0]
* 2026-02-28 19:00 UTC: Destinations of high-severity alerts: 45.131.214.85 [easy_123-08#0]
* 2026-02-28 19:00 UTC: Kerberos identity of 10.2.28.88: hostname(s) desktop-teyq2nr; human user account(s) brolf [easy_123-08#0]
* 2026-02-28 19:00 UTC: HTTP requests from 10.2.28.88 to external destinations [easy_123-01#4]""",
"Detection: IDS Alerts": """### Detection: IDS Alerts
#### Significant Alert Signatures
* **High-severity malicious signatures:**
        + ET INFO HTTP traffic on port 443 (POST) - 264 events [easy_123-06#1, easy_123-06#0]
        + ET JA3 Hash - Possible SoftEther Windows Client SSTP Traffic - 12 events [easy_123-06#0]
* **Informational signatures:**
        + ET INFO Microsoft Connection Test - 1 event [easy_123-06#1]
        + ET REMOTE_ACCESS NetSupport Remote Admin Checkin - 264 events [easy_123-06#0]
        + ET REMOTE_ACCESS NetSupport Remote Admin Response - 2 events [easy_123-06#0]
#### Hosts Involved
* 10.2.28.88: 1539 events, 264 high-severity alerts [easy_123-08#0, easy_123-06#2]
* 45.131.214.85: 1061 connections, 264 high-severity alerts [easy_123-08#0, easy_123-06#2]
#### Assessment:
* The high-severity alerts are primarily related to HTTP traffic on port 443 (POST) and possible SoftEther Windows Client SSTP Traffic.
* The host 10.2.28.88 is involved in a large number of external connections, with 45.131.214.85 being the most contacted external IP.
* The NetSupport Remote Admin Checkin and Response alerts may indicate legitimate administrative activity, but further investigation is needed to determine their relevance.""",
"Initial Infection Indicators": """### Initial Infection Indicators
* Suspicious domains/URLs:
        + Possible: `23.218.232.183` (6 events) [2025-01-22-03#4]
        + Possible: `23.218.232.142` (9 events) [2025-01-22-03#4]
        + Possible: `45.131.214.85` (264 events) [2025-01-22-03#3]
        + Possible: `23.218.232.148` (11 events) [2025-01-22-03#3]
* Downloaded files:
        + Not established from the available artifacts
* Initial vector:
        + Not established from the available artifacts""",
"Command-and-Control and Network Activity": """### Command-and-Control and Network Activity
#### Observed Facts
* The internal client 10.2.28.88 had the most external connections (1539 events, 95 distinct external destinations) [easy_123-08#0].
* The most-contacted external IP was 45.131.214.85 (1061 connections) [easy_123-08#0].
* The internal client 10.2.28.88 made HTTP requests to multiple external IPs, including 23.218.232.183, 23.218.232.142, and 23.47.50.182 [easy_123-01#4].
* The internal client 10.2.28.88 made connections to 95 distinct external destinations [easy_123-02#0].
* The top destinations for the internal client 10.2.28.88 were 45.131.214.85 (1061), 150.171.28.11 (38), 150.171.27.11 (15), 23.218.232.148 (14), and 23.192.223.17 (13) [easy_123-02#0].
#### Assessment:
* The high number of connections to 45.131.214.85 and the presence of multiple HTTP requests to this IP suggest potential Command-and-Control (C2) activity [easy_123-08#0].
* The HTTP requests to multiple external IPs and the presence of multiple external domains contacted by the internal client 10.2.28.88 suggest potential C2 activity [easy_123-01#4, easy_123-07#0].
* The high number of connections to multiple external destinations and the presence of multiple external domains contacted by the internal client 10.2.28.88 suggest potential C2 activity [easy_123-02#0].
*""",
"Impact Assessment": """### Impact Assessment
* **Primary CIA component targeted:** Assessment: Possible integrity, as the majority of high-severity alerts (264 events) are related to HTTP traffic on port 443 (POST) [easy_123-06#1].
* **Number of affected hosts:** 1 host: 10.2.28.88 [easy_123-08#0].
* **Scale of external activity:** 1539 events to/from 10.2.28.88, with 95 distinct external destinations [easy_123-02#0].
* **External destinations:** 45.131.214.85 was contacted 1061 times [easy_123-02#0].
* **High-severity alerts:** 264 events, all related to HTTP traffic on port 443 (POST) [easy_123-06#1].""",
"Root Cause and Evidence Gaps": """### Root Cause and Evidence Gaps
#### Assessment:
* Root cause: **High** - Compromised Kerberos identity of a client (10.2.28.88) is likely the root cause of the incident. The client's Kerberos identity was used to authenticate to various services, including the domain controller, and made external connections to multiple destinations.
#### Not Established:
* Initial vector
* Payload behavior
* Data exfiltration
* Queries that failed or were empty
* C2 (Command and Control) attribution
* Impact on the network or systems""",
"Corrective and Preventive Actions": """### Corrective and Preventive Actions
* Isolate host 10.2.28.88 from the network to prevent further potential malicious activity.
* Reset the Kerberos identity of host 10.2.28.88, specifically the human user account(s) brolf.
* Block IP 45.131.214.85 to prevent future connections from this IP.
* Investigate and update the TLS certificates and domains accessed by host 10.2.28.88, specifically img-s-msn-com.akamaized.net, assets.adobedtm.com, deff.nelreports.net, and oneclient.sfx.ms.""",
"Answers to Investigation Questions": """### Answers to Investigation Questions
1. What is the IP address of the infected Windows client?
        * 10.2.28.88 [easy_123-03#0]
2. What is the host name of the infected Windows client?
        * desktop-teyq2nr [easy_123-05#0]
3. What is the Windows human user account name (not machine accounts ending in $) of the potentially infected machine in the LAN?
        * brolf [easy_123-08#0]
4. What are the suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication?
        * 45.131.214.85 [easy_123-08#0]
5. During what hour did the first signs of infection activity appear? Provide the earliest date and time in YYYY-MM-DD HH:MM UTC format.
        * 2026-02-28 19:00 UTC [easy_123-06#2]
6. According to the connection volume statistics, what single external IP address received the most connections from the infected hosts? Is it a C2 server or a legitimate service?
        * 45.131.214.85 (C2 server) [easy_123-08#0]""",
}
