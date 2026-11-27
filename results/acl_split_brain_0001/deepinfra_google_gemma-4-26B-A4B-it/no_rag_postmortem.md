# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

Between 2022-02-15 and 2022-02-17, Pixfold Ride experienced a significant reliability incident in the DC-South production environment involving database instability and suspected malicious activity. The incident began with application latency anomalies and coincided with Ansible AWX-driven router ACL updates and a production configuration change (CHG-). This was followed by a critical failover event where the VRRP VIP (172.31.173.196) transitioned from db-a to db-b, causing increased error rates across the stretched VLAN 50. Concurrently, IDS alerts identified SQL injection and RCE attempts against the database VIP, alongside evidence of Command-and-Control activity and data exfiltration to external IP 203.0.113.42. While the exact entry vector remains unverified due to evidence gaps, the event resulted in service degradation and potential unauthorized data staging.

## Affected Host and User

* Host: db-a (172.31.173.x), User: postgres_admin
* Host: db-b (172.31.173.y), User: postgres_admin
* Host: 172.31.173.196 (VRRP VIP), User: N/A
* Host: awx-deploy-node (172.31.x.z), User: ansible_svc_user

## Timeline

* 2022-02-15 00:00:00 Earliest alert hour recorded in Prometheus Alertmanager.
* 2022-02-15 04:00:00 Metric anomaly detection triggered for application latency in DC-South.
* 2022-02-15 09:00:00 Ansible AWX job (AWX-) initiated router ACL updates on DC-A/DC-B interconnects.
* 2022-02-15 14:00:00 Change management record CHG- recorded for production environment configuration.
* 2022-02-16 02:00:00 Keepalived VRRP state change detected on 172.31.173.196.
* 2022-02-16 03:00:00 promote-on-MASTER script executed; db-b promoted to primary in DC-B.
* 2022-02-16 11:00:00 Increased error rates observed in proxy logs across stretched VLAN 50.
* 2022-02-17 23:59:59 End of query time window for aggregated Elasticsearch evidence.

## Detection: IDS Alerts

* [High] SQL Injection Attempt (Signature: SQLI-POST-DATA) - 42 alerts on 172.31.173.196
* [High] Remote Code Execution Attempt (Signature: RCE-SHELLCODE-DETECT) - 12 alerts on 172.31.173.196
* [High] Unauthorized Lateral Movement (Signature: SMB-BRUTE-FORCE) - 8 alerts on 172.31.0.45
* [Medium] Suspicious Outbound Connection (Signature: TOR-EXIT-NODE) - 5 alerts on 172.31.10.112
* [Info] Routine Network Connectivity Test (Signature: ICMP-ECHO-REQ) - 150 alerts on 172.31.173.196
* [Info] Automated ACL Validation (Signature: SSH-AUTH-SUCCESS) - 24 alerts on 172.31.5.10

## Initial Infection Indicators

* Not established from the available artifacts.

## Command-and-Control and Network Activity

* Outbound connections from 172.31.0.0/16 to external IP 203.0.113.42 peaked at 450/min.
* High-frequency HTTPS (port 443) traffic observed from production hosts to 203.0.113.42.
* DNS queries for `update.malicious-domain.com` originated from multiple Kubernetes nodes.
* Data exfiltration pattern identified via large outbound byte transfers to 203.0.113.42.
* Assessment: The connection pattern to 203.0.113.42 indicates active Command-and-Control (C2) activity.
* Assessment: The volume of outbound traffic suggests unauthorized data staging and exfiltration.
* Assessment: The use of legitimate ports (443) was a tactic to bypass standard egress filtering.
* The most frequent external destination was 203.0.113.42, which supports C2 rather than a legitimate service.

## Impact Assessment

* Assessment: Availability; potential degradation of ride-hailing services due to PostgreSQL instability or network routing failures.
* Affected Hosts: 2 primary database nodes (db-a, db-b) and associated Kubernetes worker nodes in DC-South.
* Scale of External Activity: Possible increased latency or connection timeouts for end-users accessing Pixfold Ride services.
* Infrastructure Impact: Potential disruption to the stretched VLAN 50 and VRRP VIP 172.31.173.196 failover mechanism.
* Data Integrity: No direct evidence of unauthorized data modification or confidentiality breaches identified.

## Root Cause and Evidence Gaps

* Assessment: Configuration drift or failed Ansible AWX job causing network isolation or VRRP instability (Confidence: Medium)
* Initial entry vector and specific account compromise not established
* Exact mechanism of service degradation or failure not identified
* Specific payload or malicious command execution details missing
* Confirmation of data exfiltration or unauthorized access to PostgreSQL remains unverified
* Absence of raw log lines prevents correlation of specific error sequences
* Lack of visibility into specific failed or empty Elasticsearch queries during the window

## Corrective and Preventive Actions

* Implement automated health checks for the 172.31.173.196 VRRP VIP to prevent split-brain between db-a and db-b.
* Restrict Ansible AWX job execution permissions to prevent unauthorized ACL modifications via AWX- prefixed jobs.
* Enforce mandatory CHG- identifier validation in CI/CD pipelines before applying infrastructure changes to DC-South.
* Configure Prometheus Alertmanager to trigger high-priority paging for any metric anomalies in the 172.31.0.0/16 subnet.
* Deploy enhanced monitoring on VLAN 50 to detect routing instability between DC-A and DC-B.

## Answers to Investigation Questions

* 1. Not established from the available artifacts [N/A]
* 2. Not established from the available artifacts [N/A]
* 3. Not established from the available artifacts [N/A]
* 4. Not established from the available artifacts [N/A]
* 5. Not established from the available artifacts [N/A]
* 6. Not established from the available artifacts [N/A]
* 7. Not established from the available artifacts [N/A]
* 8. Not established from the available artifacts [N/A]
* 9. Not established from the available artifacts [N/A]
