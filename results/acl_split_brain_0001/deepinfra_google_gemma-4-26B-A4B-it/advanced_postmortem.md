# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

The failure originated in the PostgreSQL database layer involving db-a and db-b. The earliest sign of the failure was a metric anomaly where node_cpu utilisation on 172.31.118.226 peaked at 90% starting at 2022-02-15 12:00 UTC. Assessment: The fault was a split-brain scenario between data centers caused by network delay or packet loss. This resulted in an impact on availability for reconciliation-job, eta-svc, dispatch-svc, and nightly-batch. Assessment: The reconciliation-job experienced the largest error volume as a downstream symptom of the database failures. [acl_split_brain_0001-06#0, acl_split_brain_0001-08#0, acl_split_brain_0001-09#1, acl_split_brain_0001-02#0, acl_split_brain_0001-07#1, acl_split_brain_0001-09#0]

## Affected Service and Infrastructure

* Assessment: The failure originated in the PostgreSQL database layer, supported by Keepalived VRRP state changes and a postgres promote request on db-b [acl_split_brain_0001-06#0].
* Affected services: reconciliation-job [acl_split_brain_0001-02#0].
* Affected services: eta-svc [acl_split_brain_0001-01#3].
* Affected services: dispatch-svc and nightly-batch. [acl_split_brain_0001-01#3]

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

* node_cpu utilisation on 172.31.118.226 peaked at 90% starting 2022-02-15 12:00 UTC [acl_split_brain_0001-08#0, acl_split_brain_0001-09#1]
* connected replication standbys on db-a dropped to a trough of 0 starting 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0]
* write transactions per minute on db-b peaked at 263/min starting 2022-02-15 19:00 UTC [acl_split_brain_0001-08#0]

## Service Dependencies and Propagation

* reconciliation-job experienced 2782 events failing the 'compare ledgers' operation via db-a / db-b [acl_split_brain_0001-01#0, acl_split_brain_0001-02#0].
* eta-svc experienced 1344 events failing 'INSERT' requests to 172.31.173.196:5432 [acl_split_brain_0001-01#1, acl_split_brain_0001-02#0].
* dispatch-svc experienced 194 events failing 'query' requests to dispatch-db:5432 [acl_split_brain_0001-01#1, acl_split_brain_0001-02#0].
* nightly-batch experienced 32 events failing 'SELECT totals' requests to 172.31.173.196:5432 [acl_split_brain_0001-01#1, acl_split_brain_0001-02#0].
* Assessment: reconciliation-job is the service with the largest error volume, but the evidence does not specify latency increases [acl_split_brain_0001-09#0].
* Assessment: The reconciliation-job is a downstream symptom of failures involving db-a / db-b [acl_split_brain_0001-02#0].
* Assessment: The error 'conflict: record version mismatch between DC-A and DC-B' suggests a split-brain state between data centers [acl_split_brain_0001-01#1].

## Impact Assessment

* Assessment: Availability [acl_split_brain_0001-09#0, acl_split_brain_0001-02#0].
* Affected services include reconciliation-job, eta-svc, dispatch-svc, and nightly-batch [acl_split_brain_0001-02#0].
* The reconciliation-job experienced 2782 error events [acl_split_brain_0001-09#0, acl_split_brain_0001-02#0].
* The eta-svc experienced 1344 error events [acl_split_brain_0001-02#0].
* The dispatch-svc experienced 194 error events [acl_split_brain_0001-02#0].

## Root Cause and Evidence Gaps

* Assessment: Network delay or packet loss causing a split-brain scenario between db-a and db-b (Medium confidence) [acl_split_brain_0001-02#0, acl_split_brain_0001-07#1, acl_split_brain_0001-08#0].
* Not established: The specific cause of the DuplicateIPAddressDetected warning [acl_split_brain_0001-07#1].
* Not established: The identity of host 172.31.118.226 [acl_split_brain_0001-08#0].
* Not established: The host-inventory entry for the reconciliation-job instance [acl_split_brain_0001-09#0].
* Not established: The specific reason for the loss of connected replication standbys on db-a [acl_split_brain_0001-08#0].
* Not established: Any recorded changes during the incident window [acl_split_brain_0001-09#0].

## Corrective and Preventive Actions

* Resolve the ReconciliationConflicts critical alerts for the reconciliation-job service [acl_split_brain_0001-07#0].
* Investigate and remediate the PostgresReplicationBroken critical alerts affecting the postgres service [acl_split_brain_0001-07#2].
* Address the DuplicateIPAddressDetected warning alerts within the network service [acl_split_brain_0001-07#1].
* Fix the dependency errors between reconciliation-job and the db-a / db-b hosts [acl_split_brain_0001-09#0].
* Resolve the KubeJobFailed warning alerts for the batch service [acl_split_brain_0001-07#0].

## Answers to Investigation Questions

1. AWX-54207 [acl_split_brain_0001-03#0]
2. awx-svc [acl_split_brain_0001-03#0]
3. core-b1 [acl_split_brain_0001-06#1]
4. db-b [acl_split_brain_0001-06#0]
5. 2022-02-15 12:00 UTC [acl_split_brain_0001-09#1]
6. automation error [acl_split_brain_0001-03#0]
7. Not established from the available artifacts.
8. reconciliation-job; it is a downstream symptom [acl_split_brain_0001-09#0]
9. CHG-16828 [acl_split_brain_0001-03#0]
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
