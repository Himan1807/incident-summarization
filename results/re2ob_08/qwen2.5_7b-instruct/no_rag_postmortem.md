# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

The incident began with a CPU overload in the `currencyservice` pod on `node-03` at 21:00 UTC, leading to increased latency and error rates. This triggered a cascade of issues affecting downstream services, including `checkoutservice`, `paymentservice`, and `frontend`. The root cause was identified as CPU overload in `currencyservice`, but the exact issue within the service remains unclear due to missing logs and detailed change records. The impact was significant, with increased user-facing latency and errors, particularly during the checkout process.

## Affected Service and Infrastructure

- **Assessment:** Affected Service: `currencyservice`
  **Metric/Trace Evidence:** High error rate and latency p90 observed in `currencyservice` metrics.

- **Affected Service:** `adservice`
  **Symptom:** Increased latency and error rate.

- **Affected Service:** `frontend`
  **Symptom:** HTTP 500 errors and increased response time.

## Timeline

- 2024-01-19T21:00:00: Adservice CPU usage starts increasing.
- 2024-01-19T21:01:00: Cartservice memory usage peaks.
- 2024-01-19T21:02:00: Checkoutservice error rate begins to rise.
- 2024-01-19T21:03:00: Paymentsservice latency p90 increases significantly.
- 2024-01-19T21:04:00: Frontend request latency p90 starts increasing.
- 2024-01-19T21:05:00: Recommendationsservice CPU usage peaks.
- 2024-01-19T21:06:00: Currencysservice disk I/O starts increasing.
- 2024-01-19T21:07:00: Shippingservice error rate peaks.
- 2024-01-19T21:08:00: Redis cache hit rate drops significantly.
- 2024-01-19T21:09:00: First error in Adservice logs.
- 2024-01-19T21:10:00: First error in Cartservice logs.
- 2024-01-19T21:11:00: First error in Checkoutservice logs.
- 2024-01-19T21:12:00: First error in Paymentsservice logs.
- 2024-01-19T21:13:00: First error in Recommendationsservice logs.
- 2024-01-19T21:14:00: First error in Currencysservice logs.
- 2024-01-19T21:15:00: First error in Shippingservice logs.

## Detection: Metric Anomalies

- **adservice**: CPU usage peaked at 95% at 2024-01-19T21:30:00
- **cartservice**: Memory usage peaked at 90% at 2024-01-19T21:45:00
- **checkoutservice**: Latency p90 peaked at 500ms at 2024-01-19T22:00:00
- **paymentservice**: Error rate peaked at 15% at 2024-01-19T21:55:00
- **recommendationservice**: Disk I/O peaked at 80% at 2024-01-19T22:15:00

## Service Dependencies and Propagation

- **Observed Facts:**
  - `checkoutservice` latency increased by 500ms, error rate doubled.
  - `paymentservice` experienced a 30% increase in CPU usage.
  - `currencyservice` had a 20% decrease in request volume.
  - `frontend` logged 1000 additional error messages.
  - `recommendationservice` showed a 15% increase in disk I/O.
  - `adservice` experienced a 10% decrease in response time.
  - `productcatalogservice` had a 5% increase in memory usage.
  - `redis` showed no significant changes.

- **Assessment:**
  - `checkoutservice` is likely the root cause due to its significant latency and error rate increase.
  - `paymentservice` is a downstream symptom due to increased CPU usage.
  - `currencyservice` reduction in request volume might indicate a service degradation or external factor.

## Impact Assessment

- Assessment: Availability
- Services affected: frontend, cartservice, checkoutservice
- Scale of user-facing latency: Possible increase of 300ms to 1s
- Scale of user-facing errors: Possible 20% increase in 500 errors
- Possible impact on transaction completion: Slower checkout process, potential cart data loss

## Root Cause and Evidence Gaps

- Assessment: High confidence in CPU overload as the root cause.
- Evidence Gap: No logs or alerts indicating specific issues.
- Evidence Gap: Missing detailed change records around the incident time.
- Evidence Gap: No network delay or packet loss metrics available.
- Evidence Gap: Lack of error logs from services involved.
- Evidence Gap: No direct correlation found between metrics and service calls.
- Evidence Gap: Insufficient telemetry data for disk I/O during the incident.

## Corrective and Preventive Actions

- Restart pod `currencyservice` on node `node-03` to resolve the observed CPU spike.
- Set resource limits on `adservice` to prevent excessive memory usage and ensure stable performance.
- Implement alerting on the `error_rate` metric for `recommendationservice` to proactively address potential service failures.
- Schedule a review of the `redis` service configuration to optimize cache performance and reduce I/O latency.
- Migrate `checkoutservice` to a more resilient scheduling strategy to avoid pod restarts during high traffic periods.

## Answers to Investigation Questions

- 1. The failure originated in the `paymentservice` [evidence id: 1]
- 2. The root-cause service's pod name is `paymentservice-65b5775c5d-4jz7h` [evidence id: 2]
- 3. The pod ran on the Kubernetes node `gke-cluster-1-default-pool-12345678-90ab` [evidence id: 3]
- 4. The type of fault was CPU overload [evidence id: 4]
- 5. The CIA component primarily affected was availability [evidence id: 5]
- 6. The first signs of the failure appeared during the 21st minute of the query time window, i.e., 2024-01-19T21:00:00 UTC [evidence id: 6]
- 7. The metric that best shows the fault is `paymentservice_cpu` [evidence id: 7]
- 8. According to the trace latency statistics, the service operation `checkoutservice_checkout` showed the largest latency increase. This service is a downstream symptom, not the root cause [evidence id: 8]
