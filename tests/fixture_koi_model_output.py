# Representative lines from the real llama3.2:3b koi_stealer run (parenthetical citations, role error, bad IP, truncated tail, clock times).
RAW = {
"Affected Host and User": """* The affected internal host is 172.17.0.99, with hostname(s) desktop-rnvo9at and human user account(s) afletcher. [koi_stealer-08#0]
* The host 172.17.0.99 was involved in 8 Kerberos TCP (krb_tcp) events. [koi_stealer-04#0]
* The host 172.17.0.99 was involved in 361 events, with 31 of those events occurring between 17:00 and 18:00 UTC on 2024-09-04. [koi_stealer-08#0]""",
"Detection: IDS Alerts": """* High-severity malicious signatures were detected, with 50 matching events, primarily related to the Koi Stealer malware. [koi_stealer-06#1]
* The most common high-severity alert destination was 79.124.78.197, with 49 events. [koi_stealer-06#1]
* The host 172.17.17.0.99 was involved in high-severity alerts, with 1 event. [koi_stealer-06#1]
* The host 172.17.0.99 was the most-contacted external destination, with 361 events and 35 distinct external destinations. [koi_stealer-08#0]
* The earliest alert hour was 2024-09-04 17:00 UTC, with 31 alerts. [koi_stealer-08#0]
* The host""",
"Impact Assessment": """* The primary CIA component targeted is possible integrity, as evidenced by the presence of Koi Stealer CnC Checkin (GET) alerts (koi_stealer-06#1) and the large number of external connections from a single client (koi_stealer-08#0). [koi_stealer-08#0, koi_stealer-06#3]
* The scale of external activity is significant, with 361 events from a single client (koi_stealer-08#0) and 35 distinct external destinations (koi_stealer-02#0). [koi_stealer-08#0, koi_stealer-02#0]
* The external IP 79.124.78.197 was contacted by the affected client 172.17.0.99 on multiple occasions (koi_stealer-02#0, koi_stealer-06#3, koi_stealer-08#0).""",
"Root Cause and Evidence Gaps": """* The most likely root cause is a compromised internal client, Assessment: High.
* Not established:
    + Initial vector (how the compromise occurred)
    + Payload behavior (what the malware did after initial infection)
    + Data exfiltration (if any data was stolen or transmitted)""",
"Answers to Investigation Questions": """1. The IP address of the potentially infected internal host in the LAN is 172.17.0.99 [koi_stealer-08#0].
2. The hostname of the potentially infected machine in the LAN is desktop-rnvo9at [koi_stealer-05#0].
3. The Windows human user account name of the potentially infected machine in the LAN is afletcher [koi_stealer-08#0].
4. The likely fake or suspicious domains / URLs for initial infection are www.bellantonicioccolato.it [koi_stealer-07#0].
5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 79.124.78.197 [koi_stealer-08#0].
6. Assessment: The attacker targets primarily confidentiality, as the alerts indicate suspicious communication [koi_stealer-06#2].
7. The first signs of infection activity appeared during the hour of 2024-09-04 17:00 UTC [koi_stealer-06#3].
8. The single external IP address that received the most connections is 79.124.78.197, which is likely a C2 server [koi_stealer-08#0].""",
}
