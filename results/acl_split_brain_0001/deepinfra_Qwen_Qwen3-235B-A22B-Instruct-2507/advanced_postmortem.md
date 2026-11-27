# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

- The failure originated in the PostgreSQL database service running on db-a (DC-A) and db-b (DC-B), with db-b exhibiting unintended primary behavior accepting write transactions at 263/min starting at 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0].
- The earliest sign of failure was elevated CPU utilization (90%, baseline 17%) on node 172.31.118.226 at 2022-02-15 12:00 UTC, preceding database anomalies by seven hours [acl_split_brain_0001-08#0, acl_split_brain_0001-09#1].
- A network partition led to split-brain behavior in the VRRP-managed database pair, resulting in duplicate MASTER states and conflicting advertisements for virtual IP 172.31.173.196 [acl_split_brain_0001-06#0].
- User-facing impact included critical service disruptions: reconciliation-job recorded 2782 errors due to version mismatches, eta-svc failed on INSERTs with sequence collisions, and dispatch-svc and nightly-batch experienced query failures—all tied to database unavailability [acl_split_brain_0001-01#1, acl_split_brain_0001-01#2].
- Assessment: The root cause was a network-induced split-brain in the PostgreSQL failover cluster, not triggered by any recent change, as no CHG- or AWX- events preceded the incident onset [acl_split_brain_0001-09#0].

## Affected Service and Infrastructure

- The failure most likely originated in the database service managed by db-a and db-b, as evidenced by VRRP state changes and duplicate address detection involving the virtual IP 172.31.173.196 [acl_split_brain_0001-06#1].
- Assessment: The primary failure occurred in the PostgreSQL pair due to split-brain behavior triggered by network partitioning, supported by VRRP advertisement timeouts and conflicting MASTER state entries on db-b [acl_split_brain_0001-06#0].
- The reconciliation-job service experienced the highest volume of failing requests, specifically during ledger comparison against both db-a and db-b [acl_split_brain_0001-01#0].
- Dependent services including eta-svc, dispatch-svc, and nightly-batch exhibited errors, with eta-svc showing the largest volume of 409 conflicts tied to the virtual IP 172.31.173.196 [acl_split_brain_0001-02#0].

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

- Node CPU utilization on 172.31.118.226 peaked at 90% (baseline 17%) starting at 2022-02-15 12:00 UTC [acl_split_brain_0001-08#0].
- Connected replication standbys on db-a dropped to 0 (baseline 1) beginning at 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0].
- Write transactions per minute on db-b surged to 263 (baseline 0) starting at 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0].
- The earliest metric anomaly onset was at 2022-02-15 12:00 UTC, corresponding to elevated CPU on 172.31.118.226 [acl_split_brain_0001-09#1].
- Assessment: CPU spike on 172.31.118.226 preceded database replication and transaction anomalies by 7 hours. [acl_split_brain_0001-08#0, acl_split_brain_0001-09#1]
- Assessment: db-b receiving write transactions indicates unintended promotion to primary, coinciding with loss of replication from db-a [acl_split_brain_0001-08#0].

## Service Dependencies and Propagation

- The reconciliation-job service emitted 2782 error events, the highest volume among all services [acl_split_brain_0001-02#0].
- The eta-svc service emitted 1344 error events, all failing on INSERT requests to 172.31.173.196:5432 [acl_split_brain_0001-01#1].
- The dispatch-svc service emitted 194 error events, all failing on queries to dispatch-db:5432 [acl_split_brain_0001-01#1].
- The nightly-batch service emitted 32 error events, all failing on SELECT requests to 172.31.173.196:5432 [acl_split_brain_0001-01#1].
- Error messages included "conflict: record version mismatch between DC-A and DC-B" across 2782 events, associated with reconciliation-job [acl_split_brain_0001-01#2].
- Error messages included "duplicate key value violates unique constraint (sequence collision after promotion)" across 1344 events, associated with eta-svc [acl_split_brain_0001-01#2].
- Assessment: The reconciliation-job service experienced the largest volume of errors and directly depended on the db-a/db-b database pair, indicating it was a primary observer of database inconsistency [acl_split_brain_0001-02#0].
- Assessment: eta-svc’s INSERT failures and associated sequence collision errors suggest it was a downstream symptom of database failover inconsistencies, not the root cause [acl_split_brain_0001-01#1].

## Impact Assessment

- The primary CIA component affected was availability, as multiple services experienced failures due to dependency outages and metric anomalies indicating service disruption [acl_split_brain_0001-02#0].
- Services affected include reconciliation-job, eta-svc, dispatch-svc, and nightly-batch, all showing dependency failures during the incident window [acl_split_brain_0001-02#0].
- User-facing latency or errors were significant in reconciliation-job, which had the highest error volume (2782 events) and triggered 8 critical alerts [acl_split_brain_0001-09#0].
- The eta-svc and nightly-batch services experienced dependency failures on virtual IP 172.31.173.196, suggesting possible disruption to database availability [acl_split_brain_0001-02#0].
- Assessment: Availability was the primary CIA component impacted, supported by widespread service dependency failures and sustained critical alerts across key services [acl_split_brain_0001-09#0].

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is a network fault (specifically, a split-brain condition due to duplicate IP address detection) affecting the PostgreSQL primary/standby pair and services dependent on the virtual IP 172.31.173.196, with high confidence [acl_split_brain_0001-07#1].
- The duplicate IP address event (172.31.173.196) occurred during the same window as the loss of replication connectivity and unexpected write activity on db-b, suggesting a failover conflict [acl_split_brain_0001-07#1].
- db-b, the standby, began accepting write transactions at the same time replication dropped, consistent with an unplanned promotion due to loss of quorum or split-brain [acl_split_brain_0001-08#0].
- The reconciliation-job, which depends on db-a/db-b, experienced the highest error volume and alert count, indicating direct impact from database inconsistency or unavailability [acl_split_brain_0001-09#0].
- No production changes (CHG-) or automation jobs (AWX-) were recorded before or during the incident onset, ruling out a recent configuration push as the trigger [acl_split_brain_0001-09#0].
- Not established from the available artifacts: whether the VRRP state transition logs or keepalived promote-on-MASTER script execution were captured. [acl_split_brain_0001-10#0]
- Not established from the available artifacts: whether network telemetry from routers or switches captured ACL mismatches or VLAN 50 partitioning. [acl_split_brain_0001-02#0]

## Corrective and Preventive Actions

- Implement automated failover validation checks for the PostgreSQL primary/standby pair (db-a / db-b) to detect replication state mismatches, given the critical PostgresReplicationBroken alerts and reconciliation-job dependency failures [acl_split_brain_0001-09#0].
- Introduce alerting on ReconciliationConflicts for the reconciliation-job service, which had 8 critical alerts and was the top error-generating service during the incident window [acl_split_brain_0001-07#0].
- Enforce IP address conflict detection and prevention in VLAN 50, particularly around core-router core-b1, due to observed DuplicateIPAddressDetected warnings [acl_split_brain_0001-07#1].
- Validate network reachability to 172.31.240.72:9187 (db-b) during failover events, as it was associated with 4 critical alerts and is part of the failing dependency chain [acl_split_brain_0001-07#2].
- Review and update the promote-on-MASTER script logic for keepalived to prevent split-brain scenarios, given the timing correlation between PostgresReplicationBroken and subsequent ReconciliationConflicts alerts [acl_split_brain_0001-07#0].

## Answers to Investigation Questions

1. CHG-16809 [acl_split_brain_0001-03#0]
2. awx-svc [acl_split_brain_0001-03#0]
3. core-b1 [acl_split_brain_0001-06#1]
4. db-b [acl_split_brain_0001-06#0]
5. 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0]
6. configuration change [acl_split_brain_0001-03#0]
7. integrity [acl_split_brain_0001-01#2]
8. reconciliation-job; downstream symptom [acl_split_brain_0001-09#0]
9. CHG-16828 [acl_split_brain_0001-03#0]
## Additional Investigation Questions

U1. Not established from the available artifacts
U2. Not established from the available artifacts
U3. Not established from the available artifacts
