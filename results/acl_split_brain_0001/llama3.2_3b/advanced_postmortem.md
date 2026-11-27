# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* Affected host: rider-07 and rider-07-2, both running the rider-app-bff host role, with IP addresses 172.31.118.16 and 172.31.118.226, respectively. [acl_split_brain_0001-05#0]
* Earliest alert hour: 16:00 UTC on 2022-02-15. [acl_split_brain_0001-09#1, acl_split_brain_0001-09#0]
* Main C2 candidate: The external IP 172.31.46.142, associated with the core-router role in zone DC-B. [acl_split_brain_0001-05#0]
* Assessment: The high volume of connections (9728 events) from the external IP 172.31.46.142 to the core-router role in zone DC-B suggests a potential command and control (C2) activity. [acl_split_brain_0001-05#0]

## Affected Host and User

* hosts: rider-07 — 35 events; ip: 172.31.118.16; role: rider-app-bff host; zone: rack M33 [acl_split_brain_0001-05#1]
* hosts: rider-07-2 — 59 events; ip: 172.31.118.226; role: rider-app-bff host; zone: rack M26 [acl_split_brain_0001-05#0]
* hosts: core-a1 — 51 events; ip: 172.31.160.153; role: core-router; zone: DC-A [acl_split_brain_0001-05#1]
* hosts: db-b — 136 events; ip: 172.31.240.72; role: postgres-standby; zone: DC-B [acl_split_brain_0001-05#0]

## Timeline

- 2022-02-15 12:00 UTC — metric anomalies: node_cpu utilisation on 172.31.118.226 — baseline 17%; peak 90%; onset 2022-02-15 12:00 UTC; recovered 2022-02-15 14:00 UTC; earliest metric anomaly onset 2022-02-15 12:00 UTC (node_cpu utilisation on 172.31.118.226) [acl_split_brain_0001-08#0, acl_split_brain_0001-09#1]
- 2022-02-15 16:00 UTC — alert names: TargetDown (warning) — 4 events; service: rider-app-bff; first seen in hour 2022-02-15 16:00 UTC; last seen in hour 2022-02-15 18:00 UTC; alert timeline: 1 events; earliest alert hour [acl_split_brain_0001-07#1, acl_split_brain_0001-07#3, acl_split_brain_0001-09#0]
- 2022-02-15 17:00 UTC — alert timeline: 1 events [acl_split_brain_0001-07#3]
- 2022-02-15 18:00 UTC — alert timeline: 2 events [acl_split_brain_0001-07#3]
- 2022-02-15 18:04 UTC — changes: CHG-16809 | deployment | promotions-api 8.21.6 -> 8.21.7 | actor: ansible-deploy | 2022-02-15 18:04 UTC | status: completed | minor bug fixes — 1 events [acl_split_brain_0001-03#0]
- 2022-02-15 19:00 UTC — alert names: PostgresReplicationBroken (critical) — 4 events; service: postgres; first seen in hour 2022-02-15 19:00 UTC; last seen in hour 2022-02-15 20:00 UTC; alert timeline: 3 events; metric anomalies: connected replication standbys on db-a — baseline 1; trough 0; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 04:00 UTC; metric anomalies: write transactions per minute on db-b — baseline 0 (standby); peak 263/min; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 03:00 UTC [acl_split_brain_0001-07#0, acl_split_brain_0001-07#4, acl_split_brain_0001-08#0]
- 2022-02-15 19:53 UTC — changes: AWX-54207 | network_automation | job template interconnect-acl-hardening | actor: awx-svc | 2022-02-15 19:53 UTC | status: successful | devices core-a1, core-b1; ACL INTERCONNECT-IN v28 -> v29; rendered permits: tcp/22,179,443 udp/53,123 (allowed_protocols_extra undefined: entries for protocol 112 and tcp/5432 not rendered) — 1 events [acl_split_brain_0001-03#0]
- 2022-02-15 20:00 UTC — alert names: DuplicateIPAddressDetected (warning) — 3 events; service: network; first seen in hour 2022-02-15 20:00 UTC; last seen in hour 2022-02-15 21:00 UTC; alert timeline: 3 events [acl_split_brain_0001-07#1, acl_split_brain_0001-07#4]
- 2022-02-15 21:00 UTC — alert timeline: 1 events [acl_split_brain_0001-07#4]
- 2022-02-16 00:00 UTC — alert names: ReconciliationConflicts (critical) — 8 events; service: reconciliation-job; first seen in hour 2022-02-16 00:00 UTC; last seen in hour 2022-02-16 02:00 UTC; alert timeline: 2 events [acl_split_brain_0001-07#0, acl_split_brain_0001-07#4]
- 2022-02-16 01:00 UTC — alert timeline: 3 events [acl_split_brain_0001-07#5]
- 2022-02-16 02:00 UTC — alert timeline: 3 events [acl_split_brain_0001-07#5]
- 2022-02-16 02:30 UTC — changes: CHG-16828 | network_change | ACL INTERCONNECT-IN on core-a1, core-b1 | actor: m.singh | 2022-02-16 02:30 UTC | status: completed | rollback to v28 — 1 events [acl_split_brain_0001-03#0]
- 2022-02-16 03:12 UTC — changes: CHG-16846 | db_recovery | db-b | actor: m.singh | 2022-02-16 03:12 UTC | status: completed | fence db-b; export divergent transactions; rebuild standby from db-a — 1 events [acl_split_brain_0001-03#0]

## Detection: IDS Alerts

* Informational signatures:
  * acl_split_brain_0001-07#6: alert timeline: 2022-02-16 15:00 UTC — 1 events [acl_split_brain_0001-09#0, acl_split_brain_0001-07#6]

## Initial Infection Indicators

* Possible suspicious domain: Not established from the available artifacts
* Possible suspicious IP: 172.31.118.16 [acl_split_brain_0001-05#1]
* Possible suspicious IP: 172.31.118.226 [acl_split_brain_0001-05#0]
* Possible suspicious IP: 172.31.173.196 [acl_split_brain_0001-06#0]
* Possible suspicious network device log: %ACL-6-LOG: INTERCONNECT-IN denied tcp 172.31.173.231(5432) -> 172.31.240.72 — 3013 events [acl_split_brain_0001-06#1]

## Command-and-Control and Network Activity

* The affected host(s) received the most connections from the external IP 172.31.46.142, which is associated with the core-router role in zone DC-B. [acl_split_brain_0001-05#0]
* Not established from the available artifacts whether the external IP 172.31.46.142 is a C2 server or a legitimate service.
* Assessment: The high volume of connections (9728 events) from the external IP 172.31.46.142 to the core-router role in zone DC-B suggests a potential command and control (C2) activity. [acl_split_brain_0001-05#0]
* Assessment: The presence of duplicate addresses on Vlan50 (54 events) and the high volume of denied INTERCONNECT-IN traffic (3013 events) suggests a potential split-brain scenario. [acl_split_brain_0001-06#1]
* Assessment: The error messages indicating a conflict between DC-A and DC-B (2782 events) suggest a potential root cause related to the split-brain scenario. [acl_split_brain_0001-01#1]
* The external IP 172.31.173.196 received a significant number of connections from the affected host(s), but it is not clear whether this is a C2 server or a legitimate service. [acl_split_brain_0001-06#1, acl_split_brain_0001-01#1]
* Not established from the available artifacts whether the affected host(s) are the source or target of the connections.

## Impact Assessment

* Assessment: The primary CIA component targeted was availability, as the incident resulted in a reliability issue with the production environment, causing disruptions to the ride-hailing service. [acl_split_brain_0001-05#1]
* Assessment: The scale of external activity was limited, with no evidence of external IP or destination involvement. [acl_split_brain_0001-05#0]
* Assessment: The incident was not related to a known vulnerability or exploit, and no evidence of command-and-control activity was found. [acl_split_brain_0001-03#2]
* Assessment: The root cause of the incident is not established from the available artifacts, and further investigation is required to determine the cause. [acl_split_brain_0001-03#1]

## Root Cause and Evidence Gaps

* Assessment: Low confidence; the root cause is not established from the available artifacts.
* Initial vector: Not established from the available artifacts.
* Payload behavior: Not established from the available artifacts.
* Data exfiltration: Not established from the available artifacts.
* Queries that failed or were empty: Not established from the available artifacts.
* Timeframe of critical alerts: Not established from the available artifacts.

## Corrective and Preventive Actions

* Isolate the core-router host (172.31.46.142) and its associated zone (DC-B) from the rest of the network to prevent further propagation of potential issues. [acl_split_brain_0001-05#0]
* Investigate and resolve the duplicate IP address detected on the rider-app-bff host (172.31.118.226) to prevent potential security vulnerabilities. [acl_split_brain_0001-09#1, acl_split_brain_0001-05#0]
* Run a thorough analysis on the reconciliation-job service to identify the root cause of the 2782 errors and 8 critical alerts, and take corrective actions to resolve the issues. [acl_split_brain_0001-09#0]
* Review and update the Ansible AWX job IDs (AWX-) to ensure that router ACLs are properly configured and up-to-date.
* Monitor the PostgreSQL primary/standby pair (db-a in DC-A, db-b in DC-B) and the keepalived VRRP virtual IP (172.31.173.196) for any signs of instability or misconfiguration.

## Answers to Investigation Questions

1. CHG-16855 [acl_split_brain_0001-03#2]
* CHG-16809 [acl_split_brain_0001-03#0]
* AWX-54207 [acl_split_brain_0001-03#0]
* CHG-16846 [acl_split_brain_0001-04#0]
2. ansible-deploy [acl_split_brain_0001-03#1]
* m.singh [acl_split_brain_0001-04#0]
* awx-svc [acl_split_brain_0001-04#0]
3. core-b1 [acl_split_brain_0001-06#1]
4. db-b [acl_split_brain_0001-04#0]
5. 16:00 UTC [acl_split_brain_0001-09#0]
6. Not established from the available artifacts
7. Not established from the available artifacts
8. reconciliation-job [acl_split_brain_0001-09#0]
9. Not established from the available artifacts

---
Verification note: 9 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
