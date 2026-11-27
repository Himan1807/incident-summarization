# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

- The PostgreSQL primary/standby pair (db-a in DC-A, db-b in DC-B) experienced a split-brain condition, leading to replication failure and service disruptions [acl_split_brain_0001-02#0, acl_split_brain_0001-08#0].
- The earliest sign of failure was a spike in node CPU utilization on 172.31.118.226, peaking at 90% at 2022-02-15 12:00 UTC [acl_split_brain_0001-08#0].
- User-facing impact included 2782 errors in reconciliation-job due to failing dependencies on db-a/db-b, along with errors in eta-svc, dispatch-svc, and nightly-batch [acl_split_brain_0001-02#0, acl_split_brain_0001-09#0].
- Assessment: The incident was likely caused by a network fault (split-brain scenario) affecting the PostgreSQL pair, with medium confidence [acl_split_brain_0001-02#0, acl_split_brain_0001-08#0].

## Affected Service and Infrastructure

- The PostgreSQL database pair (db-a in DC-A, db-b in DC-B) behind the VRRP virtual IP 172.31.173.196 experienced a split-brain condition, evidenced by duplicate address logs and promote request messages. [acl_split_brain_0001-06#1, acl_split_brain_0001-06#0]
- Assessment: The failure most likely originated in the PostgreSQL service, supported by the reconciliation-job's failing dependency on db-a/db-b and sequence collision errors. [acl_split_brain_0001-02#0, acl_split_brain_0001-01#2]
- Other affected services include eta-svc, dispatch-svc, and nightly-batch, which experienced dependency failures on the virtual IP 172.31.173.196 [acl_split_brain_0001-02#0].
- Reconciliation-job emitted 2782 error events due to failing compare ledgers requests to db-a/db-b, indicating a direct impact on downstream services [acl_split_brain_0001-01#0].

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

- Connected replication standbys on db-a dropped from a baseline of 1 to 0, starting at 2022-02-15 19:00 UTC and recovering by 2022-02-16 04:00 UTC [acl_split_brain_0001-08#0].
- Write transactions per minute on db-b spiked from a baseline of 0 (standby) to 263/min, beginning at 2022-02-15 19:00 UTC and resolving by 2022-02-16 03:00 UTC [acl_split_brain_0001-08#0].
- Node CPU utilization on 172.31.118.226 surged from a baseline of 17% to 90%, starting at 2022-02-15 12:00 UTC and recovering by 2022-02-15 14:00 UTC [acl_split_brain_0001-08#0].
- Reconciliation-job experienced 2782 errors, primarily due to dependencies on db-a and db-b, with alerts spanning from 2022-02-15 16:00 UTC to 2022-02-16 15:00 UTC [acl_split_brain_0001-09#0].
- Eta-svc emitted 1344 events with errors related to "duplicate key value violates unique constraint," indicating sequence collisions after promotion [acl_split_brain_0001-01#2].
- Dispatch-svc logged 194 events with errors stating "redis: i/o timeout," suggesting connectivity issues [acl_split_brain_0001-01#2].

## Service Dependencies and Propagation

- The reconciliation-job service experienced 2782 failing requests, all dependent on db-a / db-b [acl_split_brain_0001-02#0].
- The eta-svc service had 1344 failing requests, all dependent on the virtual IP 172.31.173.196 [acl_split_brain_0001-02#0].
- The dispatch-svc service encountered 194 failing requests, all dependent on dispatch-db [acl_split_brain_0001-02#0].
- The nightly-batch service recorded 32 failing requests, all dependent on the virtual IP 172.31.173.196 [acl_split_brain_0001-02#0].
- The largest latency increase was observed in reconciliation-job, with 2782 failing requests due to "conflict: record version mismatch between DC-A and DC-B" [acl_split_brain_0001-01#1].
- Error messages included "duplicate key value violates unique constraint" for eta-svc, "redis: i/o timeout" for dispatch-svc, and "checksum mismatch for nightly batch" for nightly-batch [acl_split_brain_0001-01#2].
- Assessment: The reconciliation-job service is likely a downstream symptom, as its errors stem from dependency failures on db-a / db-b [acl_split_brain_0001-09#0].
- Assessment: The virtual IP 172.31.173.196 appears to be a critical dependency for eta-svc and nightly-batch, suggesting potential upstream issues [acl_split_brain_0001-02#0].

## Impact Assessment

- The primary CIA component affected was availability, as evidenced by service reconciliation-job ranking #1 by error volume with 2782 events and failing dependencies on db-a / db-b [acl_split_brain_0001-09#0].
- Reconciliation-job experienced the highest error volume (2782 events) due to failing dependencies on db-a / db-b, indicating significant service disruption [acl_split_brain_0001-02#0].
- Eta-svc and nightly-batch services also experienced errors (1344 and 32 events respectively) due to dependencies on 172.31.173.196, suggesting broader service impact [acl_split_brain_0001-02#0].
- Metric anomalies show replication standbys on db-a dropped to 0 and write transactions on db-b peaked at 263/min, indicating database availability issues [acl_split_brain_0001-08#0].
- Warning/critical alerts spanned from 2022-02-15 16:00 UTC to 2022-02-16 15:00 UTC, with reconciliation-job being the most-alerted critical instance [acl_split_brain_0001-09#0].

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is a network fault (split-brain scenario) affecting the PostgreSQL primary/standby pair (db-a/db-b), leading to replication failure and service disruptions, with medium confidence. [acl_split_brain_0001-02#0, acl_split_brain_0001-08#0]
- Not established: Whether expired or expiring TLS certificates contributed to the incident [acl_split_brain_0001-10#0].
- Not established: The root cause of the CPU utilization spike on 172.31.118.226 and its connection to the incident. [acl_split_brain_0001-08#0, acl_split_brain_0001-09#1]
- Not established: The source or impact of the DuplicateIPAddressDetected alerts during the incident window [acl_split_brain_0001-07#1].
- Not established: Whether changes to router ACLs or other network configurations occurred during the incident [acl_split_brain_0001-09#0].
- Not established: The exact trigger for the replication failure between db-a and db-b [acl_split_brain_0001-08#0].
- Not established: The full scope of missing telemetry or logs that could clarify the incident timeline. [acl_split_brain_0001-09#0, acl_split_brain_0001-07#1]

## Corrective and Preventive Actions

- Implement automated failover testing for the PostgreSQL primary/standby pair (db-a/db-b) to ensure replication stability and reduce reconciliation-job errors [acl_split_brain_0001-09#0].
- Add host-inventory entries for reconciliation-job instances to ensure proper monitoring and alerting coverage [acl_split_brain_0001-09#0].
- Configure alerts for PostgresReplicationBroken events to trigger immediate investigation and remediation [acl_split_brain_0001-07#0].
- Investigate and resolve the DuplicateIPAddressDetected warnings to prevent network conflicts [acl_split_brain_0001-07#1].
- Review and optimize the reconciliation-job logic to reduce dependency failures and critical alerts [acl_split_brain_0001-07#2].

## Answers to Investigation Questions

1. CHG-16828 [acl_split_brain_0001-03#0]
2. m.singh [acl_split_brain_0001-03#0]
3. core-b1 [acl_split_brain_0001-06#1]
4. db-b [acl_split_brain_0001-06#0]
5. 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0]
6. Not established from the available artifacts
7. Not established from the available artifacts
8. reconciliation-job [acl_split_brain_0001-09#0]
9. CHG-16846 [acl_split_brain_0001-03#0]
## Additional Investigation Questions

U1. Not established from the available artifacts. [acl_split_brain_0001-06#1]
U2. Not established from the available artifacts. [acl_split_brain_0001-05#0]
U3. Not established from the available artifacts. [acl_split_brain_0001-01#2]
