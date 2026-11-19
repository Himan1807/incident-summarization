# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* Affected Hosts:
  * gke-fintrail-prod-pool-a-3f1c (ip: 10.70.0.14) [db_pool_config-05#0]
  * gke-fintrail-prod-pool-a-7d2e (ip: 10.70.0.15) [db_pool_config-05#0]
  * gke-fintrail-prod-pool-a-9a4b (ip: 10.70.0.17) [db_pool_config-05#0]
  * orders-db (ip: 10.70.8.3)
* Affected User: r.chaudhary
* Earliest Alert Hour: 2022-11-08 15:00 UTC [db_pool_config-09#1, db_pool_config-08#0]
* Main C2 Candidate: 10.70.0.15
* Assessment: The high volume of events from the external IP 10.70.0.15 suggests a potential C2 server, but further analysis is required to confirm this. [db_pool_config-05#0]

## Affected Host and User

* Affected Hosts:
  * gke-fintrail-prod-pool-a-3f1c (ip: 10.70.0.14) [db_pool_config-05#0]
  * gke-fintrail-prod-pool-a-7d2e (ip: 10.70.0.15) [db_pool_config-05#0]
  * gke-fintrail-prod-pool-a-9a4b (ip: 10.70.0.17) [db_pool_config-05#0]
  * orders-db (ip: 10.70.8.3)
* Affected User:
  * r.chaudhary

## Timeline

- 2022-11-08 10:04 UTC — changes: CHG-30398 | deployment | invoice-api chart 2.7.1 -> 2.7.2 | actor: release-bot | 2022-11-08 10:04 UTC | status: completed | approved_by: m.ferreira; PDF template fix — 1 events; earliest alert hour [db_pool_config-03#0, db_pool_config-09#0]
- 2022-11-08 15:00 UTC — metric anomalies: hikaricp_connections_pending on orders-api — baseline 0; peak 187; onset 2022-11-08 15:00 UTC; recovered 2022-11-08 18:00 UTC; metric anomalies: hikaricp_connections_max on orders-api — baseline 200; trough 20; onset 2022-11-08 15:00 UTC; recovered 2022-11-08 18:00 UTC; metric anomalies: cloudsql.googleapis.com/database/postgresql/num_backends on orders-db — baseline ~180; trough 24; onset 2022-11-08 15:00 UTC; recovered 2022-11-08 18:00 UTC; earliest metric anomaly onset 2022-11-08 15:00 UTC (hikaricp_connections_pending on orders-api) [db_pool_config-08#0, db_pool_config-09#1]
- 2022-11-08 15:21 UTC — changes: CHG-30412 | helm_upgrade | orders-api chart 4.12.0 (revision 58) | actor: release-bot | 2022-11-08 15:21 UTC | status: completed | approved_by: r.chaudhary; values: database.pool.maxOpenConns 200 -> 20, logging.level INFO -> DEBUG; values file: values-staging.yaml — 1 events [db_pool_config-03#0]
- 2022-11-08 16:00 UTC — alert timeline: 19 events; metric anomalies: cloudsql.googleapis.com/database/cpu/utilization on orders-db — baseline 41%; trough 19%; onset 2022-11-08 16:00 UTC; recovered 2022-11-08 18:00 UTC; metric anomalies: http 5xx ratio on checkout-api — baseline 0.2%; peak 38%; onset 2022-11-08 16:00 UTC; recovered 2022-11-08 18:00 UTC; earliest alert hour [db_pool_config-07#4, db_pool_config-08#0, db_pool_config-08#1, db_pool_config-09#0]
- 2022-11-08 17:00 UTC — alert timeline: 24 events [db_pool_config-07#4]
- 2022-11-08 18:00 UTC — alert timeline: 7 events [db_pool_config-07#5]
- 2022-11-08 18:02 UTC — changes: CHG-30433 | helm_rollback | orders-api to revision 57 | actor: r.chaudhary | 2022-11-08 18:02 UTC | status: completed | helm rollback orders-api 57 — 1 events [db_pool_config-03#0]
- 2022-11-09 04:00 UTC — alert timeline: 1 events [db_pool_config-07#5]
- 2022-11-09 09:40 UTC — changes: CHG-30451 | deployment | cart-service chart 1.19.0 -> 1.19.1 | actor: release-bot | 2022-11-09 09:40 UTC | status: completed | approved_by: m.ferreira; promo banner flag — 1 events [db_pool_config-03#0]

## Detection: IDS Alerts

* High-severity malicious signature: db_pool_config-07#2, critical alerts > critical instances: checkout-api — 14 events [db_pool_config-07#2]
* High-severity malicious signature: db_pool_config-07#2, critical alerts > critical instances: slo:checkout-availability — 7 events [db_pool_config-07#2]
* Informational signature: db_pool_config-07#5, alert timeline: 2022-11-08 18:00 UTC — 7 events [db_pool_config-07#5]

## Initial Infection Indicators

* No suspicious domain or URL found in the evidence [db_pool_config-06#0, db_pool_config-05#0, db_pool_config-02#0, db_pool_config-10#0]
* No direct IP downloads or hosts named in alerts found in the evidence [db_pool_config-09#1, db_pool_config-06#0, db_pool_config-05#0, db_pool_config-02#0, db_pool_config-10#0]
* No possible initial vector visible in the evidence [db_pool_config-09#1, db_pool_config-06#0, db_pool_config-05#0, db_pool_config-02#0, db_pool_config-10#0]

## Command-and-Control and Network Activity

* The external IP that received the most connections from the affected host(s) is 10.70.0.15. [db_pool_config-05#0]
* Not established from the available artifacts whether the external IP(s) received the connections are for a legitimate service or a Command-and-Control (C2) server.
* Assessment: The high volume of events from the external IP 10.70.0.15 suggests a potential C2 server, but further analysis is required to confirm this. [db_pool_config-05#0]
* Assessment: The majority of error messages from the affected host(s) indicate a timeout or connection issue, which may be related to the C2 server or a legitimate service.
* Assessment: The presence of error messages indicating a retry budget exhausted and context deadline exceeded suggests a potential C2 server, but further analysis is required to confirm this.

## Impact Assessment

* Assessment: Availability was targeted, as indicated by the critical alerts and metric anomalies related to the checkout-api and orders-api services, which are part of the Fintrail SaaS platform. [db_pool_config-07#2, db_pool_config-08#1, db_pool_config-09#1]
* Scale of External Activity: The alert timeline indicates that the critical alerts occurred on November 8th and 9th, with a peak on November 8th at 18:00 UTC. [db_pool_config-07#5]
* Possible Indicators: The earliest metric anomaly onset on orders-api suggests that the issue started around 15:00 UTC on November 8th. [db_pool_config-09#1]
* Not Established: The root cause, impact, and trigger of the incident are not established from the available artifacts.

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but possible root cause: Unhealthy pod events in orders-api service, potentially indicating a scaling issue or resource constraints [db_pool_config-06#0].
* Not established from the available artifacts: Initial vector, payload behavior, data exfiltration, queries that failed or were empty.
* Not established from the available artifacts: Root cause of the unhealthy pod events, potential causes such as resource constraints, scaling issues, or container crashes.
* Not established from the available artifacts: Trigger for the unhealthy pod events, potential causes such as changes in workload, network issues, or configuration errors.
* Not established from the available artifacts: Impact on the orders-api service, potential effects on availability, performance, or data integrity.
* Not established from the available artifacts: Relationship between the unhealthy pod events and the changes recorded in the change-management records (CHG-30398 and CHG-30412).
* Not established from the available artifacts: Potential connection between the orders-api service and the checkout-api service, potential causes for the high error volume in checkout-api.

## Corrective and Preventive Actions

* The CI release bot executed a Helm release for the orders-api chart (revision 58) on 2022-11-08 15:21 UTC, which may have introduced a vulnerability [db_pool_config-09#0].
* The orders-api chart was upgraded from version 4.12.0 to 2.7.2 on 2022-11-08 10:04 UTC, which may have caused errors [db_pool_config-09#0].
* The orders-api service ranks #1 by error volume, with 38914 events, indicating a high error rate [db_pool_config-09#0].
* The critical alert "SLOErrorBudgetBurnFast" was triggered 7 times, indicating a potential issue with the budget burn rate [db_pool_config-07#1].
* The critical alert "CheckoutErrorRateHigh" was triggered 14 times, indicating a potential issue with the checkout API [db_pool_config-07#0].

## Answers to Investigation Questions

1. The origin of the failure is the orders-api service, as indicated by the top dependency in the failing requests: orders-api (21690 events) [db_pool_config-01#2].
2. The change that triggered the incident was a deployment of the invoice-api chart 2.7.1 to 2.7.2, with a change identifier of CHG-30398, executed by the release-bot actor on 2022-11-08 10:04 UTC [db_pool_config-03#0].
3. The account or automation identity that executed the triggering change was the release-bot actor [db_pool_config-04#0].
4. The configuration parameter that was changed by the triggering change was the database.pool.maxOpenConns value, which was set to 20, taken from the values-staging.yaml file [db_pool_config-04#0].
5. The first signs of the failure appeared during the hour of 16:00 UTC on 2022-11-08 [db_pool_config-09#1].
6. The root cause category of the incident is not established from the available artifacts.
7. The failure is not established as isolated or cascading failure from the available artifacts.
8. The CIA component primarily affected is not established from the available artifacts.
9. The single service that emitted the most errors was the checkout-api, which is not established as the root cause or a downstream symptom from the available artifacts.
10. The change that restored normal service is not established from the available artifacts.

---
Verification note: 7 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
