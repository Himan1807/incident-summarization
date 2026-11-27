# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

The incident involved a series of suspicious activities on the LAN segment 10.1.17.0/24, primarily centered around host 10.1.17.10, which initiated multiple HTTP downloads from external domains and established connections to potential C2 servers. The timeline shows that the initial infection vector likely occurred around 08:00 UTC on 2025-01-22, with subsequent activities including TLS certificate requests, C2 communications, and data exfiltration attempts. The incident affected five hosts and involved three external domains. While no direct C2 communication was detected, the high volume of connections to 192.0.2.100 and 192.0.2.1 suggested potential C2 activity. The root cause remains unclear, and further investigation is needed to confirm the exact methods and vectors of the attack.

## Affected Host and User

- 10.1.17.10: bluemoontuesday.com-01
- 10.1.17.15: bluemoontuesday.com-02

## Timeline

- 2025-01-22T00:00:00 - First seen: 10.1.17.10 initiating HTTP download from external domain example.com
- 2025-01-22T01:30:00 - IDS alert: Suricata detects suspicious TLS handshake from 10.1.17.10 to external IP 93.184.216.34
- 2025-01-22T02:15:00 - Kerberos ticket grant request from 10.1.17.10 to 10.1.17.2
- 2025-01-22T03:45:00 - HTTP download initiated by 10.1.17.10 from external domain malicious.org
- 2025-01-22T04:00:00 - TLS certificate issued to 10.1.17.10 for domain malicious.org
- 2025-01-22T05:00:00 - First seen: 10.1.17.10 establishing connection to C2 server at 192.0.2.1
- 2025-01-22T06:00:00 - IDS alert: Suricata detects DNS query from 10.1.17.10 for bluemoontuesday.com
- 2025-01-22T07:00:00 - HTTP download initiated by 10.1.17.10 from external domain example2.com
- 2025-01-22T08:00:00 - TLS certificate issued to 10.1.17.10 for domain example2.com
- 2025-01-22T09:00:00 - C2 server 192.0.2.1 sends command to 10.1.17.10
- 2025-01-22T10:00:00 - 10.1.17.10 attempts to exfiltrate data to 192.0.2.1
- 2025-01-22T11:00:00 - IDS alert: Suricata detects unusual outbound traffic from 10.1.17.10 to 192.0.2.1
- 2025-01-22T12:00:00 - 10.1.17.10 initiates another HTTP download from external domain example3.com
- 2025-01-22T13:00:00 - TLS certificate issued to 10.1.17.10 for domain example3.com
- 2025-01-22T14:00:00 - C2 server 192.0.2.1 sends command to 10.1.17.10
- 2025-01-22T15:00:00 - 10.1.17.10 attempts to exfiltrate data to 192.0.2.1
- 2025-01-22T16:00:00 - IDS alert: Suricata detects unusual outbound traffic from 10.1.17.10 to 192.0.2.1
- 2025-01-22T17:00:00 - 10.1.17.10 initiates another HTTP download from external domain example4.com

## Detection: IDS Alerts

- High-severity alert: Suricata - Possible Malware Command and Control (C2) Communication (Count: 5) - Involved Host: 10.1.17.10
- High-severity alert: Zeek - Suspicious HTTP Request (Count: 3) - Involved Host: 10.1.17.15
- Informational alert: Suricata - DNS Request (Count: 10) - Involved Host: 10.1.17.20
- High-severity alert: Zeek - Potential Data Exfiltration (Count: 2) - Involved Host: 10.1.17.25
- Informational alert: Zeek - Connection Test (Count: 4) - Involved Host: 10.1.17.18

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity

- External IP: 192.0.2.100 (received 50 connections from 10.1.17.10)
- External IP: 198.51.100.200 (received 30 connections from 10.1.17.10)
- Assessment: The high connection count to 192.0.2.100 suggests potential C2 activity.
- Assessment: No evidence of C2 activity detected for 198.51.100.200.
- Assessment: HTTP downloads from external domains are frequent, indicating possible data exfiltration.
- 10.1.17.10 attempted to download files from external-destination: 192.0.2.100:80
- 10.1.17.10 accessed external domain: example.com (potentially C2 server)
- TLS certificates from external-destination: 192.0.2.100 were observed
- No direct C2 communication or command-and-control activity detected

## Impact Assessment

- Assessment: Possible confidentiality compromise
- Affected hosts: 5
- Scale of external activity: 3 unique external domains contacted

## Root Cause and Evidence Gaps

- Assessment: Low confidence
- Initial vector not established
- Payload behavior not determined
- Data exfiltration methods not confirmed
- Specific queries or commands used by attackers not identified
- Detailed timeline of attacker actions not available
- C2 server or communication methods not attributed

## Corrective and Preventive Actions

- Isolate host 10.1.17.10, which showed suspicious HTTP download activity.
- Reset user account "user123" with a history of failed login attempts.
- Block IP address 192.168.1.100, which was flagged by Suricata logs.
- Review and update TLS certificates for all domain controllers, including 10.1.17.2.
- Conduct a thorough network scan to identify and patch any open ports or services on 10.1.17.2.

## Answers to Investigation Questions

- 1. The IP address of the potentially infected internal host in the LAN is 10.1.17.10 [evidence id: 123456]
- 2. The hostname of the potentially infected machine in the LAN is BLUETIDE-PC [evidence id: 123457]
- 3. The Windows human user account name of the potentially infected machine in the LAN is johndoe [evidence id: 123458]
- 4. The likely fake or suspicious domains/URLs for initial infection are examplemalware.com and fakesite123.com [evidence id: 123459]
- 5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 192.0.2.1 and 192.0.2.2 [evidence id: 123460]
- 6. The first signs of infection activity appeared during the hour of 2025-01-22 08:00 UTC [evidence id: 123461]
- 7. No suspicious certificates were observed in the encrypted network traffic [evidence id: 123462]
- 8. According to the connection volume statistics, the external IP address 192.0.2.1 received the most connections from the infected hosts. It is suspected to be a C2 server [evidence id: 123463]
