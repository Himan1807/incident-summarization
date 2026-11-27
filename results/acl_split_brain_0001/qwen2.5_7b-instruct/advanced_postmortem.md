# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

The root cause of the incident originated in the `reconciliation-job` service, evidenced by the high number of events and failing dependencies. The earliest sign of the failure was a metric anomaly on node_cpu utilisation on 172.31.118.226, peaking at 90%. The fault type was likely a network delay or packet loss, impacting the `reconciliation-job` and subsequently affecting the `eta-svc` and `dispatch-svc` services. The user-facing impact was significant, with the `reconciliation-job` experiencing 2782 events and availability issues. [acl_split_brain_0001-01#0, acl_split_brain_0001-09#1, acl_split_brain_0001-08#0, acl_split_brain_0001-02#0, acl_split_brain_0001-09#0]

## Affected Service and Infrastructure

- Assessment: The failure most likely originated in the `reconciliation-job` service, as evidenced by the high number of events and failing dependencies associated with it [acl_split_brain_0001-01#0, acl_split_brain_0001-02#0].
- The `eta-svc` and `dispatch-svc` services were also affected, with the `eta-svc` showing the most significant impact [acl_split_brain_0001-02#0, acl_split_brain_0001-01#2].
- The `nightly-batch` service experienced issues but to a lesser extent compared to the other services [acl_split_brain_0001-01#0, acl_split_brain_0001-01#2].

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

- [acl_split_brain_0001-08#0] Metric anomalies: connected replication standbys on db-a — baseline 1; trough 0; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 04:00 UTC
- [acl_split_brain_0001-08#0] Metric anomalies: write transactions per minute on db-b — baseline 0 (standby); peak 263/min; onset 2022-02-15 19:00 UTC; recovered 2022-02-16 03:00 UTC

## Service Dependencies and Propagation

- reconciliation-job showed the largest latency increase and had the highest error volume with 2782 events, indicating it may be the root cause or a critical downstream service [acl_split_brain_0001-02#0, acl_split_brain_0001-09#0].
- eta-svc had 1344 failing dependency events, primarily due to issues with the virtual IP 172.31.173.196 [acl_split_brain_0001-02#0].
- dispatch-svc had 194 failing dependency events, mostly related to database queries [acl_split_brain_0001-02#0].
- nightly-batch had 32 failing dependency events, all related to database SELECT operations [acl_split_brain_0001-02#0].
- The most-failed dependency for reconciliation-job was db-a / db-b, with 2782 error events [acl_split_brain_0001-09#0].
- The largest number of error messages were related to conflict: record version mismatch between DC-A and DC-B [acl_split_brain_0001-01#1].
- The most critical error messages were duplicate key value violations and Redis I/O timeouts [acl_split_brain_0001-01#2].
- No changes were recorded from 6 hours before the earliest alert hour to its end, suggesting no recent changes impacted the system [acl_split_brain_0001-09#0].

## Impact Assessment

- Assessment: Availability was primarily affected, evidenced by the high volume of events related to the `reconciliation-job` service and the critical alerts triggered. The `reconciliation-job` service experienced 2782 events, indicating significant operational issues. [acl_split_brain_0001-09#0]
- Assessment: The `eta-svc` and `dispatch-svc` services also experienced availability issues, with 1344 and 194 events respectively, highlighting the propagation of the incident across multiple services. [acl_split_brain_0001-02#0]
- Assessment: The `db-a` and `db-b` PostgreSQL instances showed metric anomalies, with `db-b` experiencing a peak of 263 write transactions per minute, indicating a potential load imbalance. [acl_split_brain_0001-08#0]
- Assessment: The `node_cpu` utilisation on host `172.31.118.226` peaked at 90%, suggesting a resource bottleneck that could have contributed to the overall availability issues. [acl_split_brain_0001-09#1]
- Assessment: The `reconciliation-job` service had the highest error volume, with 2782 events, and the most-failed dependency being the `db-a` and `db-b` PostgreSQL instances, indicating a critical impact on the service's availability. [acl_split_brain_0001-09#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is a network delay or packet loss, given the significant increase in write transactions on the standby database [acl_split_brain_0001-08#0].
- Not established: The exact nature of the network issue, such as whether it was a temporary glitch or a persistent problem, is not established [acl_split_brain_0001-08#0].
- Not established: Whether the high CPU utilization on a specific node [acl_split_brain_0001-08#0] was a contributing factor or a result of the network issue.
- Not established: The presence or absence of error logs related to the network or database operations during the incident period [acl_split_brain_0001-09#0].
- Not established: The exact timing and duration of the network issue relative to the metric anomalies observed [acl_split_brain_0001-08#0].
- Not established: The impact of the network issue on other services beyond the reconciliation-job [acl_split_brain_0001-02#0].
- Not established: The root cause of the TLS certificate checks, as no relevant evidence was found [acl_split_brain_0001-10#0].

## Corrective and Preventive Actions

- Restart the `reconciliation-job` service to clear any potential job conflicts or errors [acl_split_brain_0001-09#0].
- Monitor and alert on `PostgresReplicationBroken` critical alerts to prevent future database replication issues [acl_split_brain_0001-07#0].
- Investigate and resolve any duplicate IP address detection warnings to avoid network conflicts [acl_split_brain_0001-07#1].
- Schedule regular health checks for the `db-a` and `db-b` PostgreSQL instances to ensure primary/standby replication is functioning correctly [acl_split_brain_0001-05#0].

## Answers to Investigation Questions

1. CHG-16846 [acl_split_brain_0001-03#0]
2. m.singh [acl_split_brain_0001-03#0]
3. core-b1 [acl_split_brain_0001-06#1]
4. db-b [acl_split_brain_0001-05#0]
5. 2022-02-15 12:00 UTC [acl_split_brain_0001-09#1]
6. Not established from the available artifacts
7. availability [acl_split_brain_0001-09#0]
8. reconciliation-job, a downstream symptom [acl_split_brain_0001-09#0]
9. Not established from the available artifacts
## Additional Investigation Questions

U1. Not established from the available artifacts [acl_split_brain_0001-06#1]
U2. Not established from the available artifacts [acl_split_brain_0001-06#1]
U3. Not established from the available artifacts [acl_split_brain_0001-06#1]
