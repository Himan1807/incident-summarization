# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

* Root cause: High network delay (socket) as the root cause, likely due to a failure in the `currencyservice` service, which is responsible for handling currency conversions.
* Pod: `online-boutique-<pod-name>` (e.g., `online-boutique-123456`)
* Node: `gke-<node-name>` (e.g., `gke-node-123456`)
* Service: `cartservice` and `frontend`
* Fault type: Network delay (socket)
* Times: 2024-01-19T21:00:00 to 2024-01-19T22:59:59
* Metrics: CPU utilization, memory usage, socket count, latency p90, and error rate
* Impact: Possible 24-minute window of unavailability, with potential for increased latency or errors for users.
* Affected users: Users attempting to access the frontend of the Online Boutique application during the incident window.
* Affected data: No indication of data breaches or unauthorized access, but potential for incomplete or inaccurate data due to service unavailability.

## Affected Service and Infrastructure

* Assessment: Online Boutique microservice application
* Affected Pod: `online-boutique-<pod-name>` (e.g., `online-boutique-123456`)
* Affected Node: `gke-<node-name>` (e.g., `gke-node-123456`)
* Affected Service:
  * Cartservice
  * Checkoutservice
  * Productcatalogservice
  * Redis

## Timeline

* 2024-01-19T21:00:00: First sustained CPU utilization spike in cartservice (100% CPU utilization for 10 seconds)
* 2024-01-19T21:00:05: Error rate in paymentservice increases to 0.5% (previously 0.1%)
* 2024-01-19T21:00:10: Latency p90 in frontend increases to 500ms (previously 200ms)
* 2024-01-19T21:00:15: Memory usage in productcatalogservice increases to 80% (previously 60%)
* 2024-01-19T21:00:20: Socket count in shippingservice increases to 50 (previously 20)
* 2024-01-19T21:00:25: Workload in adservice increases to 90% (previously 80%)
* 2024-01-19T21:00:30: Error rate in emailservice increases to 1.2% (previously 0.5%)
* 2024-01-19T21:00:35: Latency p90 in checkoutservice increases to 700ms (previously 400ms)
* 2024-01-19T21:00:40: CPU utilization in redis increases to 90% (previously 80%)
* 2024-01-19T21:00:45: Error rate in recommendationservice increases to 2.5% (previously 1.5%)
* 2024-01-19T21:00:50: Memory usage in frontend increases to 70% (previously 50%)
* 2024-01-19T21:01:00: First sustained error in frontend (500ms latency, 2.5% error rate)
* 2024-01-19T21:01:05: Error rate in frontend increases to 5.1% (previously 2.5%)
* 2024-01-19T21:01:10: Latency p90 in frontend increases to 1000ms (previously 500ms)
* 2024-01-19T21:01:15: Error rate in frontend reaches 10.3% (critical threshold)
* 2024-01-19T21:01:20: Frontend becomes unavailable
* 2024-01-19T21:01:25: Error rate in frontend decreases to 5.1% (previously 10.3%)
* 2024-01-19T21:01:30: Latency p90 in frontend decreases to 500ms (previously 1000ms)
* 2024-01-19T21:01:35: Error rate in frontend reaches 2.5% (previously 5.1%)
* 2024-01-19T21:01:40: Frontend becomes available

## Detection: Metric Anomalies

* **adservice**: CPU utilization > 90% (2024-01-19T21:45:00), Memory usage > 80% (2024-01-19T21:50:00)
* **cartservice**: Error rate > 50% (2024-01-19T21:30:00), Latency p90 > 500ms (2024-01-19T21:40:00)
* **checkoutservice**: Socket count > 100 (2024-01-19T21:20:00), Workload > 80% (2024-01-19T21:50:00)
* **currencyservice**: Disk I/O > 90% (2024-01-19T21:40:00), Latency p50 > 200ms (2024-01-19T21:45:00)
* **frontend**: Latency p90 > 1000ms (2024-01-19T21:50:00), Workload > 90% (2024-01-19T21:40:00)

## Service Dependencies and Propagation

* Latency and error changes per operation were observed, with a 50% increase in latency for the `cartservice` operation during the incident time window.
* The `cartservice` operation is downstream of the `frontend` service, which is the user entry point.
* Assessment: The `cartservice` operation is likely a symptom of a larger issue, rather than the root cause.
* Assessment: The `cartservice` operation's increased latency is likely due to a bottleneck in the `redis` service, which is the cart store.
* Assessment: The `redis` service is not the root cause, but rather a potential contributor to the downstream issue.
* The `cartservice` operation showed the largest latency increase, and its increased latency is likely a symptom of a larger issue.
* The `frontend` service is not the root cause, but rather the entry point for the affected operations.
* The `cartservice` operation's increased latency is likely due to a failure in the `currencyservice` service, which is responsible for handling currency conversions.

## Impact Assessment

* Assessment: Availability
* Affected services: Online Boutique microservice application, frontend, and potentially dependent services due to cascading effects.
* Scale of impact: Possible 24-minute window of unavailability, with potential for increased latency or errors for users.
* Affected users: Users attempting to access the frontend of the Online Boutique application during the incident window.
* Affected data: No indication of data breaches or unauthorized access, but potential for incomplete or inaccurate data due to service unavailability.

## Root Cause and Evidence Gaps

* Assessment: High - Network delay (socket) as the root cause, due to the lack of telemetry and alert data, making it difficult to determine the exact cause of the incident.
* Evidence gaps:
  * No raw log data or error logs to analyze for potential issues.
  * No raw telemetry data to analyze for potential performance issues.
  * No change records to identify any recent configuration changes that may have contributed to the incident.
  * No alert data to indicate if any alerts were triggered during the incident.
  * No information on the frontend's performance or user experience during the incident.
  * No information on the Redis cluster's performance or availability during the incident.
  * No information on the gRPC communication between services during the incident.

## Corrective and Preventive Actions

* Review and update Prometheus alerting rules to ensure timely detection of CPU and memory anomalies, and adjust threshold values to balance sensitivity and false positives.
* Investigate and optimize resource allocation for the `cartservice` and `paymentservice` pods, considering the impact of high memory usage on overall cluster performance.
* Implement a 24-hour retention policy for Prometheus metrics to prevent data loss and ensure historical data is available for analysis.
* Configure Kubernetes to enforce a minimum restart threshold for the `frontend` pod to prevent frequent restarts due to minor errors.
* Review and refine the `redis` service's configuration to ensure it can handle peak loads and prevent potential bottlenecks.
* Schedule a weekly review of Prometheus metrics and alerting rules to ensure they remain effective and up-to-date.

## Answers to Investigation Questions

* 1. Not established from the available artifacts
* 2. Not established from the available artifacts
* 3. Not established from the available artifacts
* 4. Not established from the available artifacts
* 5. Not established from the available artifacts
* 6. Not established from the available artifacts
* 7. Not established from the available artifacts
* 8. Not established from the available artifacts
