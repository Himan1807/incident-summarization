# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* Affected Host: db-mysql-01 (ip: 10.30.2.15, role: mysql-primary, zone: eu-central-1b) [az_ebs_degraded-05#0, az_ebs_degraded-09#0]
* Affected User: k.weber
* Earliest Alert Hour: 2025-02-17 06:00 UTC [az_ebs_degraded-09#1, az_ebs_degraded-07#4]
* Main C2 Candidate: Not established from the available artifacts
* Key Assessment: The high volume of events on the affected hosts suggests a significant increase in network activity, which may indicate a command-and-control (C2) communication, but further investigation is required to determine the root cause of the high network activity.

## Affected Host and User

* Affected Hosts:
  * app-web-03 (ip: 10.30.13.21, role: web-frontend, zone: eu-central-1c) [az_ebs_degraded-05#1]
  * app-content-02 (ip: 10.30.12.40, role: content-api, zone: eu-central-1b) [az_ebs_degraded-05#1]
  * app-content-01 (ip: 10.30.11.40, role: content-api, zone: eu-central-1a) [az_ebs_degraded-05#1]
  * db-mysql-01 (ip: 10.30.2.15, role: mysql-primary, zone: eu-central-1b) [az_ebs_degraded-09#0, az_ebs_degraded-05#0]
  * db-mysql-02 (ip: 10.30.3.15, role: mysql-replica, zone: eu-central-1c) [az_ebs_degraded-05#0]
  * app-web-02 (ip: 10.30.12.21, role: web-frontend, zone: eu-central-1b) [az_ebs_degraded-05#0]
  * app-web-01 (ip: 10.30.11.21, role: web-frontend, zone: eu-central-1a) [az_ebs_degraded-05#0]
* Affected User:
  * k.weber

## Timeline

- 2025-02-17 04:40 UTC — changes: CHG-7759 | deployment | web-frontend 2025.02.16-2 | actor: jenkins-deploy | 2025-02-17 04:40 UTC | status: completed | CSS bundle and article template change — 1 events; earliest alert hour [az_ebs_degraded-03#0, az_ebs_degraded-09#0]
- 2025-02-17 06:00 UTC — alert timeline: 8 events; metric anomalies: node_disk await (nvme1n1) on db-mysql-01 — baseline 0.6 ms; peak 2,840 ms; onset 2025-02-17 06:00 UTC; recovered 2025-02-17 09:00 UTC; metric anomalies: aws_ebs VolumeQueueLength (vol-0a91c3e5f27d4b8e1) on db-mysql-01 — baseline 0.8; peak 311; onset 2025-02-17 06:00 UTC; recovered 2025-02-17 09:00 UTC; metric anomalies: mysql_global_status_threads_running on db-mysql-01 — baseline 12; peak 1,024; onset 2025-02-17 06:00 UTC; recovered 2025-02-17 08:00 UTC; metric anomalies: mysql_slave_status_seconds_behind_master on db-mysql-02 — baseline 0 s; peak 1,860 s; onset 2025-02-17 06:00 UTC; recovered 2025-02-17 08:00 UTC; earliest alert hour; earliest metric anomaly onset 2025-02-17 06:00 UTC (node_disk await (nvme1n1) on db-mysql-01) [az_ebs_degraded-07#4, az_ebs_degraded-08#0, az_ebs_degraded-09#0, az_ebs_degraded-09#1]
- 2025-02-17 06:38 UTC — cloud health events: AWS_EBS_DEGRADED_VOLUME_PERFORMANCE (eu-central-1b) opened 2025-02-17 06:38 UTC, closed 2025-02-17 09:51 UTC — 3 events; top objects: vol-0a91c3e5f27d4b8e1 (i-0c4f2e9a71b3d5c08) (1), vol-04be7d21c9a0f3e66 (i-0e1a9c3b5d7f20a14) (1), vol-0d3f5a8c2e1b7094f (i-07b2d4f6a8c0e1359) (1) [az_ebs_degraded-06#0]
- 2025-02-17 07:00 UTC — alert timeline: 22 events [az_ebs_degraded-07#4]
- 2025-02-17 08:00 UTC — alert timeline: 12 events [az_ebs_degraded-07#4]
- 2025-02-17 08:12 UTC — changes: CHG-7781 | manual_failover | MySQL primary db-mysql-01 -> db-mysql-02 | actor: k.weber | 2025-02-17 08:12 UTC | status: completed | promote replica db-mysql-02 — 1 events [az_ebs_degraded-03#0]
- 2025-02-17 08:14 UTC — changes: CHG-7790 | config_push | proxysql mysql_servers | actor: k.weber | 2025-02-17 08:14 UTC | status: completed | writer hostgroup 10: db-mysql-01 -> db-mysql-02 — 1 events [az_ebs_degraded-03#0]
- 2025-02-17 09:00 UTC — alert timeline: 4 events [az_ebs_degraded-07#4]
- 2025-02-17 10:00 UTC — alert timeline: 2 events [az_ebs_degraded-07#5]
- 2025-02-17 10:30 UTC — changes: CHG-7764 | deployment | image-resizer 4.0.7 -> 4.1.0 | actor: jenkins-deploy | 2025-02-17 10:30 UTC | status: completed | libvips upgrade — 1 events [az_ebs_degraded-03#0]
- 2025-02-18 10:05 UTC — changes: CHG-7802 | ebs_volume_replace | db-mysql-01 data volume | actor: m.santos | 2025-02-18 10:05 UTC | status: completed | new gp3 volume restored from snapshot; db-mysql-01 rebuilt as replica — 1 events [az_ebs_degraded-03#1]

## Detection: IDS Alerts

* Informational signatures:
  * az_ebs_degraded-07#1: MySQLReplicationLag (warning) — 6 events [az_ebs_degraded-09#0, az_ebs_degraded-07#1]
  * az_ebs_degraded-07#4: alert timeline: 2025-02-17 06:00 UTC — 8 events [az_ebs_degraded-07#4]
  * az_ebs_degraded-07#4: alert timeline: 2025-02-17 07:00 UTC — 22 events [az_ebs_degraded-07#4]
  * az_ebs_degraded-07#4: alert timeline: 2025-02-17 08:00 UTC — 12 events [az_ebs_degraded-07#4]
  * az_ebs_degraded-07#4: alert timeline: 2025-02-17 09:00 UTC — 4 events [az_ebs_degraded-07#4]

## Initial Infection Indicators

* az_ebs_degraded-05#1, hosts: app-web-03 — 86 events; ip: 10.30.13.21; role: web-frontend; zone: eu-central-1c [az_ebs_degraded-05#1]
* az_ebs_degraded-06#1, system messages: kernel: nvme nvme0: I/O 87 QID 1 timeout, aborting — 4 events; top objects: app-web-02 (3), app-content-02 (1) [az_ebs_degraded-06#1]

## Command-and-Control and Network Activity

* Assessment: The high volume of events on the affected hosts suggests a significant increase in network activity, which may indicate a command-and-control (C2) communication.
* Assessment: The majority of events on the affected hosts are related to services emitting services (e.g., web-frontend, content-api), which may suggest a legitimate service rather than a C2 communication.
* Assessment: The presence of error messages such as SQLSTATE[HY000]: General error: 2006 and PHP Fatal error: Maximum execution time of 30 seconds exceeded suggests that the affected hosts may have experienced technical issues, but the high volume of events does not support a legitimate service. [az_ebs_degraded-01#3, az_ebs_degraded-01#2]
* The affected hosts are part of a Kubernetes cluster, with multiple zones (eu-central-1a/1b/1c) and a VPC range (10.30.0.0/16) that suggests a distributed environment.
* The evidence does not support the presence of a C2 server or a malicious actor, but further investigation is required to determine the root cause of the high network activity.

## Impact Assessment

* Assessment: The primary CIA component targeted was availability, as the evidence suggests a degradation in storage performance, leading to potential downtime and impact on the organization's news publishing operations.
* Assessment: The scale of external activity was limited, with no indication of lateral movement or exploitation of vulnerabilities.
* Assessment: The earliest metric anomaly onset was on 2025-02-17 06:00 UTC, indicating a potential trigger for the incident. [az_ebs_degraded-09#1, az_ebs_degraded-07#4]
* Assessment: Not established from the available artifacts whether the incident had a direct impact on the organization's operations or if it was contained and resolved without significant disruption.

## Root Cause and Evidence Gaps

* Assessment: Low Confidence - Not established from the available artifacts.
* Initial Infection Indicators: Not established from the available artifacts.
* Command-and-Control and Network Activity: Not established from the available artifacts.
* Data Exfiltration: Not established from the available artifacts.
* Queries that failed or were empty: Not established from the available artifacts.
* Payload Behaviour: Not established from the available artifacts.

## Corrective and Preventive Actions

* Isolate the host with the highest error volume, identified as 10.30.2.15:9100, which maps to hostname db-mysql-01, role mysql-primary, and zone eu-central-1b, to prevent further propagation of potential issues. [az_ebs_degraded-09#0]
* Reset the account associated with the most-failed dependency, content-api, to its default settings to prevent further errors.
* Block the IP address associated with the highest CPU load, 10.30.2.15, to prevent potential lateral movement. [az_ebs_degraded-09#0, az_ebs_degraded-07#1]
* Investigate and address the high disk I/O latency alert on db-mysql-01, as indicated by 19 events, to prevent potential data corruption or loss. [az_ebs_degraded-09#0]
* Review and update the deployment history for the web-frontend service, specifically the deployment with CHG-7759, to ensure that the changes were properly tested and validated before being applied. [az_ebs_degraded-09#0]

## Answers to Investigation Questions

1. The hostname of the host or node where the failure originated is db-mysql-01 [az_ebs_degraded-05#0].
2. The IP address of the host or node where the failure originated is 10.30.2.15 [az_ebs_degraded-05#0].
3. The availability zone affected by the cloud provider event is eu-central-1b [az_ebs_degraded-06#0].
4. Not established from the available artifacts.
5. The first signs of the failure appeared during the hour of 06:00 UTC on 2025-02-17 [az_ebs_degraded-09#1].
6. Not established from the available artifacts.
7. Not established from the available artifacts.
8. The service that emitted the most errors is web-frontend, which is not the root cause but a downstream symptom [az_ebs_degraded-02#0].
9. The change that restored normal service is CHG-7802, which involved replacing the EBS volume of db-mysql-01 with a new gp3 volume [az_ebs_degraded-03#1].

---
Verification note: 10 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 3 claim(s) remain without a citation. Details: advanced_run_report.json.
