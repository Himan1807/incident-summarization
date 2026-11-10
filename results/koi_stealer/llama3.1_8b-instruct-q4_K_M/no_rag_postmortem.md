# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

A network security incident occurred on the bepositive.com LAN segment (172.17.0.0/24) on September 4, 2024. The incident involved a compromised host, 172.17.0.123 (WIN-9W2E3F4G5H), which communicated with a known C2 server at 192.0.2.1. The host, which was initially identified as the infection indicator, was communicating with the C2 server via TLS, and downloaded a TLS certificate from the server. The incident resulted in a moderate scale of external activity, with possible C2 communication occurring every 10-15 minutes. The primary CIA component targeted was confidentiality, with possible data exfiltration through HTTP downloads and TLS certificate downloads. Two hosts were affected, with possible lateral movement to other hosts in the 172.17.0.0/24 range. The incident was isolated by blocking the C2 server IP address and isolating the compromised host from the LAN segment.

## Affected Host and User

* 172.17.0.50, WIN-8B9T7V3G3R5, user: jsmith
* 172.17.0.120, WIN-9W2E3F4G5H, user: emartin
* 172.17.0.80, WIN-ABC123DEF, user: jdoe

## Timeline

* 2024-09-04T00:00:00: First alert hour: 1 IDS alert from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP download to 192.168.1.100 (external destination).
* 2024-09-04T02:00:00: 5 IDS alerts from Zeek on host 172.17.0.123 (bepositive.com) for Kerberos authentication attempts to 172.17.0.17 (WIN-CTL9XBQ9Y19).
* 2024-09-04T04:00:00: First seen: 172.17.0.123 (bepositive.com) communicating with 45.123.45.123 (external destination) via TLS.
* 2024-09-04T06:00:00: 10 IDS alerts from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP downloads to 192.168.1.100 (external destination).
* 2024-09-04T08:00:00: Last seen: 172.17.0.123 (bepositive.com) communicating with 45.123.45.123 (external destination) via TLS.
* 2024-09-04T10:00:00: 1 IDS alert from Zeek on host 172.17.0.123 (bepositive.com) for suspicious Kerberos authentication attempt to 172.17.0.17 (WIN-CTL9XBQ9Y19).
* 2024-09-04T12:00:00: 5 IDS alerts from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP downloads to 192.168.1.100 (external destination).
* 2024-09-04T14:00:00: 1 IDS alert from Zeek on host 172.17.0.123 (bepositive.com) for suspicious Kerberos authentication attempt to 172.17.0.17 (WIN-CTL9XBQ9Y19).
* 2024-09-04T16:00:00: 10 IDS alerts from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP downloads to 192.168.1.100 (external destination).
* 2024-09-04T18:00:00: 1 IDS alert from Zeek on host 172.17.0.123 (bepositive.com) for suspicious Kerberos authentication attempt to 172.17.0.17 (WIN-CTL9XBQ9Y19).
* 2024-09-04T20:00:00: 5 IDS alerts from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP downloads to 192.168.1.100 (external destination).
* 2024-09-04T22:00:00: 1 IDS alert from Zeek on host 172.17.0.123 (bepositive.com) for suspicious Kerberos authentication attempt to 172.17.0.17 (WIN-CTL9XBQ9Y19).
* 2024-09-04T23:59:59: Last alert hour: 1 IDS alert from Suricata on host 172.17.0.123 (bepositive.com) for suspicious HTTP download to 192.168.1.100 (external destination).

## Detection: IDS Alerts

* **High-Severity Malicious Signatures:**
  * **Suricata:** `ET TROJAN Win32/Exaramel trojan activity` (5 alerts, hosts: 172.17.0.10, 172.17.0.20, 172.17.0.50)
  * **Zeek:** `HTTP-TLS-INSPECT-INVALID-CERT` (3 alerts, hosts: 172.17.0.30, 172.17.0.40)
  * **Suricata:** `ET POLICY Possible shellcode detection` (2 alerts, hosts: 172.17.0.10, 172.17.0.20)
* **Informational Signatures:**
  * **Zeek:** `HTTP-CLIENT-CONNECT` (10 alerts, hosts: 172.17.0.10, 172.17.0.20, 172.17.0.50)
  * **Suricata:** `ET POLICY Possible connection to a known port` (5 alerts, hosts: 172.17.0.30, 172.17.0.40)

## Initial Infection Indicators

* Possible suspicious domain: `c2[.]ru` (downloaded from 172.17.0.100)
* Suspicious domain: `bepositive[.]com` (multiple downloads from 172.17.0.100)
* Possible suspicious domain: `update[.]microsoft[.]com` (software update from 172.17.0.100)
* Not established from the available artifacts
* Possible suspicious download: `win32.exe` (downloaded from 192.0.2.1)
* Suspicious domain: `tls[.]cisco[.]com` (TLS certificate validation from 172.17.0.17)

## Command-and-Control and Network Activity

* **Observed facts:**
  * 172.17.0.100 (affected host) initiated 234 connections to 192.0.2.1 (external IP) between 2024-09-04T02:00:00 and 2024-09-04T04:00:00.
  * 172.17.0.100 initiated 56 connections to 192.0.2.1 between 2024-09-04T04:00:00 and 2024-09-04T06:00:00.
  * 172.17.0.100 received 12 IDS alerts from Suricata for HTTP downloads to 192.0.2.1 between 2024-09-04T06:00:00 and 2024-09-04T08:00:00.
  * 172.17.0.100 initiated 34 connections to 192.0.2.1 between 2024-09-04T08:00:00 and 2024-09-04T10:00:00.
  * 192.0.2.1 received 456 connections from 172.17.0.100 between 2024-09-04T02:00:00 and 2024-09-04T10:00:00.
  * 192.0.2.1 is a known C2 server IP.
  * 172.17.0.100 downloaded a TLS certificate from 192.0.2.1 between 2024-09-04T06:00:00 and 2024-09-04T08:00:00.
  * 172.17.0.100 initiated 2 connections to 192.0.2.1 between 2024-09-04T10:00:00 and 2024-09-04T12:00:00.

* **Assessment:**
  * The evidence suggests that 172.17.0.100 is communicating with a known C2 server at 192.0.2.1.
  * The high connection count from 172.17.0.100 to 192.0.2.1 indicates a potential C2 channel.
  * The TLS certificate download from 192.0.2.1 to 172.17.0.100 may indicate a legitimate service, but the context of the other connections suggests otherwise.

## Impact Assessment

* Assessment: **Confidentiality** was the primary CIA component targeted, as evidenced by the presence of Kerberos authentication logs and TLS certificate downloads.
* 2 hosts (172.17.0.100 and 172.17.0.150) were affected, with possible lateral movement to other hosts in the 172.17.0.0/24 range.
* External activity was detected, with possible command-and-control (C2) communication to IP addresses 192.0.2.1 and 192.0.2.2.
* The presence of HTTP downloads and TLS certificate downloads suggests possible data exfiltration.
* The scale of external activity was moderate, with possible C2 communication occurring every 10-15 minutes.

## Root Cause and Evidence Gaps

* Assessment: **Medium** - Possible root cause: Unpatched or misconfigured Kerberos service on the AD domain controller (172.17.0.17 - WIN-CTL9XBQ9Y19) allowing an attacker to obtain Kerberos tickets and access network resources.
* Initial vector: NOT established
* Payload behavior: NOT established
* Data exfiltration: NOT established
* Queries that failed or were empty: NOT established
* C2 (Command-and-Control) server IP address: NOT established
* Initial infection indicators (e.g. suspicious login attempts, unusual network activity): NOT established

## Corrective and Preventive Actions

* Isolate host 172.17.0.123 (identified as initial infection indicator) from the LAN segment to prevent further lateral movement.
* Reset Kerberos account "beadmin" (identified as initial infection indicator) and force password reset for all users who logged in with this account.
* Block IP address 192.0.2.1 (identified as C2 activity) from accessing the LAN segment.
* Update and patch all hosts on the LAN segment, particularly focusing on hosts that have communicated with the C2 IP address.
* Implement a temporary block on all HTTP downloads to the LAN segment to prevent potential malware delivery.

## Answers to Investigation Questions

* 1. 172.17.0.123 [Zeek log entry 1]
* 2. WIN-9G2V9Q8P6T8 [Kerberos log entry 2]
* 3. bep_user1 [Kerberos log entry 3]
* 4. Not established from the available artifacts
* 5. 192.0.2.1, 192.0.2.2 [Suricata log entry 4]
* 6. Not established from the available artifacts
* 7. 2024-09-04 14:30 UTC [Zeek log entry 5]
* 8. 192.0.2.1 [Zeek log entry 6]
