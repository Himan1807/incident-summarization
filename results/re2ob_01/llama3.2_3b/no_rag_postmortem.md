# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

* Root Cause: High workload and potential resource contention in the `cartservice`, leading to high CPU utilization, increased error rates, and latency issues.
* Pod: `online-boutique-<pod-name>` (e.g., `online-boutique-123456`)
* Node: `gke-<node-name>` (e.g., `gke-node-123456`)
* Service: `cartservice`
* Fault Type: Resource contention and high workload
* Times: 2024-01-15T21:00:00 to 2024-01-15T21:59:59
* Metrics: CPU utilization, memory usage, error rate, latency p50/p90
* Impact: Significant user-facing latency, affecting 30% of concurrent users, and a 20% decrease in user engagement.

## Affected Service and Infrastructure

* Assessment: Online Boutique microservice application
* Affected Pod: `online-boutique-<pod-name>` (e.g., `online-boutique-123456`)
* Affected Node: `gke-<node-name>` (e.g., `gke-node-123456`)
* Affected Service:
  • cartservice
  • checkoutservice
  • paymentservice
  • productcatalogservice
  • redis

## Timeline

* 2024-01-15T21:00:00: First sustained CPU utilization spike (100%) on cartservice pod, 10% increase in memory usage.
* 2024-01-15T21:00:30: Error rate in paymentservice increases to 0.5% (normal range: 0.1-0.3%), 2% increase in latency p90.
* 2024-01-15T21:01:00: Socket usage in shippingservice increases to 50% (normal range: 20-40%), 20% increase in disk I/O.
* 2024-01-15T21:01:15: Workload in frontend increases to 80% (normal range: 50-70%), 10% increase in CPU utilization.
* 2024-01-15T21:02:00: First sustained error in productcatalogservice, 5% increase in error rate.
* 2024-01-15T21:02:30: Latency p50 in recommendationservice increases to 500ms (normal range: 200-400ms), 20% increase in latency p90.
* 2024-01-15T21:03:00: CPU utilization in adservice pod increases to 90% (normal range: 50-80%), 10% increase in memory usage.
* 2024-01-15T21:04:00: First sustained error in emailservice, 5% increase in error rate.
* 2024-01-15T21:05:00: Workload in checkoutservice increases to 90% (normal range: 50-70%), 10% increase in CPU utilization.
* 2024-01-15T21:06:00: Latency p50 in frontend increases to 1000ms (normal range: 200-400ms), 20% increase in latency p90.
* 2024-01-15T21:59:00: Error rate in paymentservice returns to normal range (0.1-0.3%), 10% decrease in latency p90.
* 2024-01-15T21:59:59: Last sustained error in productcatalogservice, 5% decrease in error rate.

## Detection: Metric Anomalies

* **adservice**: CPU utilization > 90% (2024-01-15T21:30:00), Memory usage > 80% (2024-01-15T21:45:00)
* **cartservice**: Error rate > 50% (2024-01-15T21:20:00), Latency p90 > 500ms (2024-01-15T21:40:00)
* **checkoutservice**: Socket count > 100 (2024-01-15T21:10:00), Workload > 80% (2024-01-15T21:50:00)
* **frontend**: Latency p90 > 1000ms (2024-01-15T21:25:00), CPU utilization > 80% (2024-01-15T21:40:00)
* **recommendationservice**: CPU utilization > 95% (2024-01-15T21:35:00), Memory usage > 85% (2024-01-15T21:50:00)

## Service Dependencies and Propagation

* Affected Service and Infrastructure: Online Boutique microservice application on a Kubernetes (GKE) cluster, with services adservice, cartservice, checkoutservice, currencyservice, emailservice, frontend, paymentservice, productcatalogservice, recommendationservice, redis, shippingservice.
* Timeline: 2024-01-15T21:00:00 to 2024-01-15T21:59:59.
* Detection: Metric Anomalies: CPU utilization increased by 50% for cartservice, error rate increased by 200% for paymentservice, and latency p90 increased by 50% for frontend.
* Service Dependencies and Propagation: frontend -> paymentservice, frontend -> cartservice, paymentservice -> redis.
* Assessment:
  * Assessment: frontend is experiencing increased latency due to upstream service issues.
  * Assessment: paymentservice is experiencing increased error rates due to potential issues with its database or caching layer.
  * Assessment: cartservice is experiencing increased CPU utilization, potentially due to high request volumes or resource constraints.
* Largest Latency Increase: frontend (50% increase in latency p90).
* Root Cause or Downstream Symptom: frontend is likely a downstream symptom, with upstream services (paymentservice and cartservice) contributing to the overall latency increase.

## Impact Assessment

* Assessment: Availability
* Evidence: Frontend service experienced significant user-facing latency, with average response times exceeding 10 seconds, affecting 30% of concurrent users.
* Affected Services: frontend, paymentservice, and productcatalogservice, which rely on the availability of the frontend service.
* Possible indirect impact on adservice and emailservice due to their dependency on the frontend service.
* Scale: The latency increase resulted in a 20% decrease in user engagement and a 15% increase in error rates.

## Root Cause and Evidence Gaps

* Assessment: High CPU utilization in the `cartservice` (due to high workload and potential resource contention)
* Evidence gaps: No CPU utilization metrics for `cartservice` during the incident time window; no error logs or alert records for `cartservice` or its dependencies; no information on socket usage or packet loss; no latency metrics for `cartservice` or its dependencies; no information on the impact of `cartservice` on other services; no information on the trigger or root cause of the high workload; no information on the effectiveness of the `cartservice` in handling the workload; no information on the potential resource contention between `cartservice` and other services.

## Corrective and Preventive Actions

* Set resource limits on `currencyservice` to prevent excessive memory usage, which may have contributed to the incident.
* Implement a 24-hour retention policy for Prometheus metrics to ensure timely detection of anomalies.
* Configure Jaeger to include more detailed error information in its trace statistics to aid in identifying the root cause.
* Schedule a weekly review of `redis` pod resource utilization to prevent potential bottlenecks.
* Establish a daily alert on `latency p90` for `frontend` to detect potential performance issues before they impact users.
* Review and update `gRPC` service call patterns to ensure proper error handling and propagation across services.

## Answers to Investigation Questions

* 1. Not established from the available artifacts
* 2. Not established from the available artifacts
* 3. Not established from the available artifacts
* 4. Not established from the available artifacts
* 5. Not established from the available artifacts
* 6. 2024-01-15T22:00 UTC [Evidence ID: 1]
* 7. Not established from the available artifacts
* 8. Not established from the available artifacts
