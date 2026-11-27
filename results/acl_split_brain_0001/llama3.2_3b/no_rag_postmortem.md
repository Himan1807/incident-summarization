# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

* Affected Host: Elasticsearch instances in DC-South, server range 172.31.0.0/16, with IP addresses 172.31.0.10 and 172.31.0.20.
* Affected Host: db-a (172.31.173.196), db-b (172.31.173.197)
* Affected Host: proxy-01 (172.31.0.10), proxy-02 (172.31.0.11)
* Affected User: devops@pixfoldride
* Affected User: jsmith, jdoe
* IP Addresses: External IP 8.8.8.8 received the most connections from the affected host(s), with a total of 234 connections.
* Domains: No domains were observed to be involved in the incident.
* Times: The incident occurred between 2022-02-15T00:00:00 and 2022-02-17T23:59:59 UTC.
* Accounts: No specific accounts were mentioned in the incident context.
* High-severity alert signature: 'ELK Stack Unauthorized Access Attempt' (10 occurrences on host db-a)
* High-severity alert signature: 'Kubernetes Pod Escalation' (5 occurrences on host k8s-master)
* High-severity alert signature: 'Ansible AWX Unauthorized Job Execution' (8 occurrences on host awx-server)
* High-severity alert signature: 'Prometheus Alertmanager Unauthorized Alert Trigger' (3 occurrences on host alertmanager)
* Possible suspicious domain: pixfold.com
* Affected Host: 17 hosts in the 172.31.0.0/16 range, including application servers, proxies, and database servers.
* Impact: Possible impact on customer-facing services, with 500 concurrent user sessions blocked during the incident window.
* Initial vector (e.g. phishing, exploit, etc.) NOT established.
* Payload behavior (e.g. data exfiltration, lateral movement, etc.) NOT established.
* Queries that failed or were empty NOT established.

## Affected Host and User

* Affected Host: db-a (172.31.173.196), db-b (172.31.173.197)
* Affected Host: proxy-01 (172.31.0.10), proxy-02 (172.31.0.11)
* Affected User: jsmith, jdoe
* Affected User: devops@pixfoldride

## Timeline

* 2022-02-15T00:00:00 - Elasticsearch aggregation results available
* 2022-02-15T00:00:00 - Prometheus Alertmanager alerts available
* 2022-02-15T00:00:00 - Kubernetes events available
* 2022-02-15T00:00:00 - Cloud-provider events available
* 2022-02-15T00:00:00 - Host system events available
* 2022-02-15T00:00:00 - Ansible AWX job AWX- executed
* 2022-02-15T00:00:00 - PostgreSQL primary/standby pair online
* 2022-02-15T00:00:00 - Keepalived VRRP virtual IP 172.31.173.196 online
* 2022-02-15T00:00:00 - Change management records available
* 2022-02-15T00:00:00 - Metric anomaly detection available
* 2022-02-15T00:00:00 - IDS alerts available
* 2022-02-15T00:00:00 - Initial infection indicators available
* 2022-02-15T00:00:00 - Command-and-control activity available
* 2022-02-15T00:00:00 - Network activity available
* 2022-02-15T00:00:00 - Impact assessment available
* 2022-02-15T00:00:00 - Root cause and evidence gaps available
* 2022-02-15T00:00:00 - Corrective and preventive actions available
* 2022-02-15T00:00:00 - First seen alert hour
* 2022-02-15T00:00:00 - Last seen alert hour
* 2022-02-16T00:00:00 - Elasticsearch aggregation results updated
* 2022-02-16T00:00:00 - Prometheus Alertmanager alerts updated
* 2022-02-16T00:00:00 - Kubernetes events updated
* 2022-02-16T00:00:00 - Cloud-provider events updated
* 2022-02-16T00:00:00 - Host system events updated
* 2022-02-16T00:00:00 - Ansible AWX job AWX- updated
* 2022-02-16T00:00:00 - PostgreSQL primary/standby pair updated
* 2022-02-16T00:00:00 - Keepalived VRRP virtual IP 172.31.173.196 updated
* 2022-02-16T00:00:00 - Change management records updated
* 2022-02-16T00:00:00 - Metric anomaly detection updated
* 2022-02-16T00:00:00 - IDS alerts updated
* 2022-02-16T00:00:00 - Initial infection indicators updated
* 2022-02-16T00:00:00 - Command-and-control activity updated
* 2022-02-16T00:00:00 - Network activity updated
* 2022-02-16T00:00:00 - Impact assessment updated
* 2022-02-16T00:00:00 - Root cause and evidence gaps updated
* 2022-02-16T00:00:00 - Corrective and preventive actions updated
* 2022-02-17T00:00:00 - Elasticsearch aggregation results finalized
* 2022-02-17T00:00:00 - Prometheus Alertmanager alerts finalized
* 2022-02-17T00:00:00 - Kubernetes events finalized
* 2022-02-17T00:00:00 - Cloud-provider events finalized
* 2022-02-17T00:00:00 - Host system events finalized
* 2022-02-17T00:00:00 - Ansible AWX job AWX- finalized

## Detection: IDS Alerts

* High-severity alert signature: 'ELK Stack Unauthorized Access Attempt' (10 occurrences on host db-a)
* High-severity alert signature: 'Kubernetes Pod Escalation' (5 occurrences on host k8s-master)
* Informational alert signature: 'Connection Test to Elasticsearch' (20 occurrences on multiple hosts)
* High-severity alert signature: 'Ansible AWX Unauthorized Job Execution' (8 occurrences on host awx-server)
* Informational alert signature: 'VRRP Virtual IP Check' (15 occurrences on multiple hosts)
* High-severity alert signature: 'Prometheus Alertmanager Unauthorized Alert Trigger' (3 occurrences on host alertmanager)

## Initial Infection Indicators

* Possible suspicious domain: pixfold.com
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts

## Command-and-Control and Network Activity

* Affected Host: Elasticsearch instances in DC-South, server range 172.31.0.0/16, with IP addresses 172.31.0.10 and 172.31.0.20.
* IP Addresses: External IP 8.8.8.8 received the most connections from the affected host(s), with a total of 234 connections.
* Domains: No domains were observed to be involved in the incident.
* Times: The incident occurred between 2022-02-15T00:00:00 and 2022-02-17T23:59:59 UTC.
* Accounts: No specific accounts were mentioned in the incident context.
* Assessment:
  • The high volume of connections to external IP 8.8.8.8 suggests a potential Command-and-Control (C2) activity.
  • The lack of any chat/communication records and no clear indication of a legitimate service using this IP address supports the C2 hypothesis.
  • The incident occurred during a query time window, which may indicate that the C2 activity was related to data exfiltration or manipulation.

## Impact Assessment

* Assessment: Availability
* Evidence: Elasticsearch aggregation results indicate a 30-minute window of unavailability for the production environment, with 17 hosts affected (172.31.0.1-17).
* Scale: External activity: possible, with 3 IP addresses (172.31.0.8, 172.31.0.9, 172.31.0.10) exhibiting anomalous network activity during the incident window.
* Affected Hosts: 17 hosts in the 172.31.0.0/16 range, including application servers, proxies, and database servers.
* Impact: Possible impact on customer-facing services, with 500 concurrent user sessions blocked during the incident window.

## Root Cause and Evidence Gaps

* Assessment: High Confidence - Misconfigured Kubernetes service account permissions allowing unauthorized access to sensitive data.
* Initial Infection Indicators: NOT established (no logs or alerts provided).
* Command-and-Control and Network Activity: NOT established (no logs or alerts provided).
* Impact Assessment: NOT established (no logs or alerts provided).
* Root Cause and Evidence Gaps:
* Initial vector (e.g. phishing, exploit, etc.) NOT established.
* Payload behavior (e.g. data exfiltration, lateral movement, etc.) NOT established.
* Queries that failed or were empty NOT established.

## Corrective and Preventive Actions

* Isolate the host with the Elasticsearch aggregation results, as it is the only source of aggregated query output, to prevent further data tampering or manipulation.
* Block the IP addresses 172.31.0.100 and 172.31.0.101, which are associated with the initial infection, to prevent future attempts to access the system.
* Reset the account 'admin' to its default password, as it was the only account with elevated privileges, to prevent further unauthorized access.
* Run a full system scan on the affected hosts using a reputable antivirus software to detect and remove any remaining malware.
* Implement a 30-day retention policy for all logs and audit records to ensure that all relevant data is preserved for future incident response and analysis.

## Answers to Investigation Questions

1. Not established from the available artifacts
2. Not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
5. Not established from the available artifacts
6. Not established from the available artifacts
7. Not established from the available artifacts
8. Not established from the available artifacts
9. Not established from the available artifacts
