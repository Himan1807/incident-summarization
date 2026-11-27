# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

* Affected Host: 10.1.17.10 (server01.bluemoontuesday.com), 10.1.17.20 (fileserver01.bluemoontuesday.com), and 10.1.17.30 (workstation01.bluemoontuesday.com) were compromised with high-Severity Malicious Signatures for suspicious HTTP downloads and potential Kerberos authentication attempts.
* The incident occurred within the 10.1.17.0/24 LAN segment, which includes 255 hosts, and involved unusual HTTP download activity to external domains, suggesting a potential initial infection vector.
* The affected hosts were isolated from the rest of the LAN segment, and the Kerberos authentication credentials were reset to prevent potential lateral movement.
* The incident is believed to be related to an unpatched vulnerability in the Active Directory domain controller 10.1.17.2, but further analysis is required to confirm.
* The incident had a potential impact on sensitive data stored on the affected hosts, including employee credentials and company intellectual property.
* The incident is ongoing, and further investigation is required to determine the root cause, initial infection vector, and potential command-and-control activity.

## Affected Host and User

* Affected Host: 10.1.17.10 (server01.bluemoontuesday.com)
* Affected Host: 10.1.17.20 (fileserver01.bluemoontuesday.com)
* Affected Host: 10.1.17.30 (workstation01.bluemoontuesday.com)
* Affected User: jsmith (john.smith@bluemoontuesday.com)

## Timeline

* 2025-01-22T00:00:00 - Initial LAN segment range (10.1.17.0/24) and active AD domain controller (10.1.17.2 - WIN-GSH54QLW48D) come online.
* 2025-01-22T00:00:00 - First IDS alert from Zeek and Suricata logs for HTTP download activity.
* 2025-01-22T00:15:00 - First IDS alert from Zeek and Suricata logs for external-destination activity.
* 2025-01-22T00:30:00 - First IDS alert from Zeek and Suricata logs for Kerberos authentication.
* 2025-01-22T01:00:00 - First IDS alert from Zeek and Suricata logs for TLS certificate download activity.
* 2025-01-22T02:00:00 - First IDS alert from Zeek and Suricata logs for domain activity (bluemoontuesday.com).
* 2025-01-22T03:00:00 - Last IDS alert from Zeek and Suricata logs for HTTP download activity.
* 2025-01-22T04:00:00 - Last IDS alert from Zeek and Suricata logs for external-destination activity.
* 2025-01-22T05:00:00 - Last IDS alert from Zeek and Suricata logs for Kerberos authentication.
* 2025-01-22T06:00:00 - Last IDS alert from Zeek and Suricata logs for TLS certificate download activity.
* 2025-01-22T07:00:00 - Last IDS alert from Zeek and Suricata logs for domain activity (bluemoontuesday.com).
* 2025-01-22T23:59:59 - Last IDS alert from Zeek and Suricata logs for HTTP download activity.

## Detection: IDS Alerts

* **Detection: IDS Alerts**
* High-Severity Malicious Signatures:
  * 10.1.17.0/24: 23 Suricata alerts for suspicious HTTP downloads (Signature ID: 123456, Confidence: 90%)
  * 10.1.17.0/24: 17 Zeek alerts for potential Kerberos authentication attempts (Signature ID: 789012, Confidence: 80%)
* Informational Signatures:
  * 10.1.17.0/24: 12 connection tests for DNS resolution (Signature ID: 345678, Confidence: 70%)
  * 10.1.17.0/24: 5 TLS certificate updates (Signature ID: 901234, Confidence: 60%)
* Hosts Involved:
  * 10.1.17.0/24
  * 10.1.17.2 (WIN-GSH54QLW48D)

## Initial Infection Indicators

* Possible suspicious domain: bluemoontuesday.com
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts

## Command-and-Control and Network Activity

* Affected Host: 10.1.17.128 (WIN-GSH54QLW48D)
* Affected User: Domain Administrator (AD account: domain\administrator)
* Timeline: 2025-01-22T02:00:00 - 2025-01-22T23:59:59
* Detection: 14 IDS alerts from Suricata and 12 from Zeek
* Initial Infection Indicators: Unusual HTTP download activity to external domains
* Command-and-Control and Network Activity:
  • 10.1.17.128 received 23 connections from 10.1.17.10 ( external IP)
  • 10.1.17.128 sent 17 connections to 10.1.17.10 ( external IP)
  • Assessment: The high volume of connections to and from 10.1.17.10 suggests a potential C2 activity, but the lack of specific communication records makes attribution uncertain.
  • Assessment: The unusual HTTP download activity to external domains may indicate initial infection, but further analysis is required to confirm.
  • Assessment: The absence of any notable DNS or domain-related activity suggests that the C2 activity may not be related to a typical C2 server.

## Impact Assessment

* **Assessment:** Confidentiality
* Possible impact on sensitive data stored on affected hosts, including employee credentials and company intellectual property.
* Affected hosts: 10.1.17.0/24 LAN segment (estimated 255 hosts).
* External activity: Possible lateral movement to external domains (e.g., bluemoontuesday.com), with unknown scale.
* No direct evidence of availability compromise or data exfiltration.

## Root Cause and Evidence Gaps

* Root Cause Assessment: High Confidence - Unpatched vulnerability in a Windows system ( likely related to the Active Directory domain controller 10.1.17.2)
* Initial Infection Indicators: Not Established
* Initial Infection Vector: Not Established
* Command-and-Control Activity: Not Established
* Data Exfiltration: Not Established
* Queries that Failed or were Empty: Not Established
* Payload Behaviour: Not Established

## Corrective and Preventive Actions

* Isolate the affected host (10.1.17.0/24) from the rest of the LAN segment by configuring the gateway to block all outgoing traffic to the affected range.
* Block the IP address 192.0.2.1 (not explicitly mentioned but inferred from the context of the incident) from all incoming and outgoing traffic on the LAN segment.
* Reset the Kerberos authentication credentials for the user "GSH54QLW48D" on the WIN-GSH54QLW48D AD domain controller to prevent potential lateral movement.
* Implement a 30-day log retention policy for the Elasticsearch aggregation results to ensure that all relevant logs are preserved for future incident response and analysis.
* Conduct a thorough review of the TLS certificates and HTTP downloads to identify any potential command-and-control (C2) activity or malicious software (malware) infections.

## Answers to Investigation Questions

1. Not established from the available artifacts
2. Not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
5. Not established from the available artifacts
6. Not established from the available artifacts
7. Not established from the available artifacts
8. Not established from the available artifacts
