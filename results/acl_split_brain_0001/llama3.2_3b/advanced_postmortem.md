# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* The root cause of the incident is likely related to the reconciliation-job service, as it has the highest number of failing dependencies and error events.
* The earliest sign of the failure was during the hour of 16:00 UTC on 2022-02-15, with a warning/critical alert span from 2022-02-15 16:00 UTC to 2022-02-16 15:00 UTC. [auto: acl_split_brain_0001-09#0]
* The fault type is likely a distributed system issue, with a conflict between DC-A and DC-B, as indicated by the error messages and most-failed dependency between db-a and db-b.
* The user-facing impact was high, with significant latency and errors in services such as reconciliation-job, eta-svc, dispatch-svc, and nightly-batch. [auto: acl_split_brain_0001-02#0]
* Assessment: The incident's impact was likely due to the stretched VLAN 50 and the legacy PostgreSQL primary/standby pair, which may have contributed to the replication and write transaction issues.

## Affected Service and Infrastructure

* The failure most likely originated in the PostgreSQL database service, specifically in the db-b instance in DC-B, as indicated by the Keepalived VRRP virtual IP 172.31.173.196 being in the MASTER STATE and the promote-on-MASTER script being executed. [acl_split_brain_0001-06#0]
* The Kubernetes pod and node affected by this failure are not explicitly stated in the provided evidence, but the top dependencies for services such as eta-svc, dispatch-svc, and nightly-batch are 172.31.173.196, suggesting a connection to the database service. [acl_split_brain_0001-02#0]
* The error messages indicating a sequence collision after promotion and a duplicate key value violate unique constraint suggest a database-related issue. [acl_split_brain_0001-01#2]
* The error events and failing requests for the reconciliation-job service also point towards a database-related problem, specifically with the compare ledgers operation. [acl_split_brain_0001-01#0]

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

## Detection: Metric Anomalies

* Metric anomalies: connected replication standbys on db-a — baseline 1; trough 0; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 04:00 UTC [acl_split_brain_0001-08#0]
* Metric anomalies: write transactions per minute on db-b — baseline 0 (standby); peak 263/min; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 03:00 UTC [acl_split_brain_0001-08#0]
* Derived: earliest metric anomaly onset 2022-02-15 12:00 UTC (node_cpu utilisation on 172.31.118.226) [acl_split_brain_0001-09#1]
* Derived: warning/critical alerts span 2022-02-15 16:00 UTC to 2022-02-16 15:00 UTC; earliest alert hour 2022-02-15 16:00 UTC (1 alerts) [acl_split_brain_0001-09#0]
* Derived: most-failed dependency: db-a / db-b (2782 errors) [acl_split_brain_0001-09#0]

## Service Dependencies and Propagation

* The largest latency increase occurred in the reconciliation-job service, with a top dependency of db-a / db-b, showing 2782 events of failing dependencies. [auto: acl_split_brain_0001-09#0, acl_split_brain_0001-02#0]
* Assessment: The root cause of the incident is likely related to the reconciliation-job service, as it has the highest number of failing dependencies and error events.
* Assessment: The service dependencies and propagation of the incident suggest that the issue is not isolated to a single service, but rather affects multiple services, including eta-svc, dispatch-svc, and nightly-batch.
* Assessment: The error messages indicate a conflict between DC-A and DC-B, suggesting a distributed system issue.
* The most-failed dependency of db-a / db-b has 2782 errors, indicating a significant issue with the database replication or synchronization. [auto: acl_split_brain_0001-09#0, acl_split_brain_0001-02#0]
* The earliest alert hour for the reconciliation-job service was 2022-02-15 16:00 UTC, with a warning/critical alert span from 2022-02-15 16:00 UTC to 2022-02-16 15:00 UTC. [auto: acl_split_brain_0001-09#0]
* The incident occurred during a period of no changes recorded from 6 hours before the earliest alert hour to its end, suggesting a potential lack of monitoring or detection during this time. [auto: acl_split_brain_0001-09#0]

## Impact Assessment

* Assessment: Availability is the primary CIA component affected, as the incident resulted in service unavailability and latency.
* Services affected: reconciliation-job, eta-svc, dispatch-svc, and nightly-batch. [auto: acl_split_brain_0001-02#0]
* Scale of user-facing latency or errors: High, with a significant number of events indicating service failures and dependencies.
* Assessment: The incident's impact was likely due to the stretched VLAN 50 and the legacy PostgreSQL primary/standby pair, which may have contributed to the replication and write transaction issues.
* Assessment: The root cause of the incident is not established from the available artifacts, and further investigation is required to determine the exact cause.

## Root Cause and Evidence Gaps

* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No root cause, impact or trigger is stated in the evidence.
* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No error logs or change records are present in the evidence.
* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No telemetry or monitoring data is available for the affected services.
* Assessment: Not established from the available artifacts.

## Corrective and Preventive Actions

* The reconciliation-job service should be restarted to resolve the critical ReconciliationConflicts and PostgresReplicationBroken alerts, as indicated by the high error volume and most-failed dependency between db-a and db-b [acl_split_brain_0001-09#0].
* The alertmanager service should be checked for continuous firing, as indicated by the Watchdog (info) alert, and addressed to prevent further alerts [acl_split_brain_0001-07#0].
* The rider-app-bff service should be checked for duplicate IP addresses, as indicated by the DuplicateIPAddressDetected (warning) alert, and addressed to prevent further alerts [acl_split_brain_0001-07#1].
* The PostgreSQL replication should be checked for issues, as indicated by the PostgresReplicationBroken (critical) alert, and addressed to prevent further alerts [acl_split_brain_0001-07#2].
* The reconciliation-job service should be checked for critical instances, as indicated by the critical alerts > critical instances reconciliation-job — 8 events [acl_split_brain_0001-07#2].

## Answers to Investigation Questions

1. The change that triggered the incident is CHG-16846, a database recovery change on db-b, executed by m.singh on 2022-02-16 03:12 UTC [acl_split_brain_0001-04#0].
2. The account or automation identity that executed the change is m.singh [acl_split_brain_0001-04#0].
3. Not established from the available artifacts.
4. Not established from the available artifacts.
5. The first signs of the failure appeared during the hour of 16:00 UTC on 2022-02-15 [acl_split_brain_0001-09#1].
6. Not established from the available artifacts.
7. Not established from the available artifacts.
8. The service that emitted the most errors is reconciliation-job, which is the root cause [acl_split_brain_0001-09#0].
9. Not established from the available artifacts.

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 3 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. The on-call engineer who acknowledged the incident is not identified in the evidence. [acl_split_brain_0001-05#0]
U2. Not established from the available artifacts.
U3. The Linux kernel version ran on the node that hosted the pod of the root-cause service is not specified in the evidence. [acl_split_brain_0001-05#1]
U5. The email address of the on-call engineer who acknowledged the incident is not present in the evidence. [acl_split_brain_0001-05#0]
U6. Not established from the available artifacts.
U7. Not established from the available artifacts.
