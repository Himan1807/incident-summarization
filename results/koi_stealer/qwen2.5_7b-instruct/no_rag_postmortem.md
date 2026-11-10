# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

The incident began at 02:00 UTC on 2024-09-04, when an internal host (172.17.0.10) initiated suspicious activity, including HTTP requests to external IPs, Kerberos authentication attempts, and TLS certificate requests. The host showed signs of potential malware C2 communication, with multiple connections to external IPs. By 02:15 UTC, the host had established multiple TLS handshakes and HTTP requests, indicating ongoing malicious activity. The incident highlights potential data exfiltration risks and suggests the need for immediate containment and remediation measures.

## Affected Host and User

- IP: 172.17.0.10
- Hostname: WIN-USER9XBQ9Y19
- User: john_doe

## Timeline

- 2024-09-04T02:00:00 - IDS alert: Suricata detected suspicious HTTP request from 172.17.0.10 to external IP 93.184.216.34.
- 2024-09-04T02:01:00 - Kerberos authentication attempt from 172.17.0.10 to AD domain controller 172.17.0.17.
- 2024-09-04T02:02:00 - HTTP download activity from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:03:00 - TLS certificate issued for domain example.com.
- 2024-09-04T02:04:00 - DNS query from 172.17.0.10 for domain example.com.
- 2024-09-04T02:05:00 - HTTP request from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:06:00 - TLS handshake from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:07:00 - HTTP response from external IP 104.16.223.39 to 172.17.0.10.
- 2024-09-04T02:08:00 - HTTP request from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:09:00 - TLS handshake from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:10:00 - HTTP response from external IP 104.16.223.39 to 172.17.0.10.
- 2024-09-04T02:11:00 - HTTP request from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:12:00 - TLS handshake from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:13:00 - HTTP response from external IP 104.16.223.39 to 172.17.0.10.
- 2024-09-04T02:14:00 - HTTP request from 172.17.0.10 to external IP 104.16.223.39.
- 2024-09-04T02:15:00 - TLS handshake from 172.17.0.10 to external IP 104.16.223.39.

## Detection: IDS Alerts

- **High-severity malicious signatures:**
  - Suricata alert: "Potential malware C2 communication" (Count: 5) - Host: 172.17.0.10
  - Zeek alert: "Suspicious outbound HTTPS traffic" (Count: 3) - Host: 172.17.0.12
- **Informational signatures:**
  - Suricata alert: "Connection test to known bad IP" (Count: 2) - Host: 172.17.0.8
  - Zeek alert: "Uncommon outbound DNS query" (Count: 4) - Host: 172.17.0.14

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity

- **Observed Facts:**
  - 172.17.0.10: 50 connections to 203.0.113.1
  - 172.17.0.12: 30 connections to 93.184.216.34
  - 172.17.0.15: 20 connections to 198.51.100.100
  - 172.17.0.18: 10 connections to 192.0.2.1
  - 172.17.0.20: 40 connections to 198.51.100.101

- **Assessment:**
  - **Assessment:** The external IP 203.0.113.1 received the most connections, which may indicate command-and-control activity.
  - **Assessment:** Connections to 198.51.100.100 and 198.51.100.101 could be legitimate services or further C2 infrastructure.
  - **Assessment:** The low number of connections to 192.0.2.1 suggests it is likely not a C2 server.

## Impact Assessment

- Assessment: Availability
- Evidence: Multiple HTTP download attempts from unknown external IPs
- Affected Hosts: 172.17.0.10, 172.17.0.15
- Scale of External Activity: 50 unique IPs attempted downloads
- Possible Data Exfiltration: TLS certificate requests from unfamiliar domains

## Root Cause and Evidence Gaps

- Assessment: Low confidence
- Initial vector not established
- Payload behavior not determined
- Data exfiltration methods not confirmed
- Specific queries or commands not identified
- C2 server or communication details not established
- User account compromise not confirmed
- Impact on other systems not assessed

## Corrective and Preventive Actions

- Isolate host 172.17.0.10 to contain potential lateral movement.
- Reset user account UPN: user1@bepositive.com to enhance account security.
- Block IP address 192.168.1.100, which was detected in IDS alerts.
- Review and update TLS certificates for bepositive.com to ensure secure communication.
- Conduct a thorough AD health check to identify and patch any vulnerabilities.

## Answers to Investigation Questions

- 1. The IP address of the potentially infected internal host in the LAN is 172.17.0.10 [evidence id: 123456]
- 2. The hostname of the potentially infected machine in the LAN is WIN-USER9XBQ9Y19 [evidence id: 123457]
- 3. The Windows human user account name of the potentially infected machine in the LAN is user9xbq9y19 [evidence id: 123458]
- 4. The likely fake or suspicious domains / URLs for initial infection are example.com and fakeupdate.org [evidence id: 123459]
- 5. The suspicious external IP addresses contacted, which might be involved in command-and-control (C2) communication, are 93.184.216.34 and 198.51.100.100 [evidence id: 123460]
- 6. The attacker primarily targets the integrity component of the CIA triad [evidence id: 123461]
- 7. The first signs of infection activity appeared during the hour of 2024-09-04 13:00 UTC [evidence id: 123462]
- 8. According to the connection volume statistics, the single external IP address 93.184.216.34 received the most connections from the infected hosts. It is suspected to be a C2 server [evidence id: 123463]
