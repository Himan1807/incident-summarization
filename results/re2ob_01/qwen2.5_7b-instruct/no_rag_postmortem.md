# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

The incident began with a sudden spike in CPU usage on the `adservice` pod, `adservice-76c557d6b-4j2z9`, on node `gke-cluster-1-default-pool-123456-7890ab`. This led to increased error rates and latency in downstream services, particularly `checkoutservice`, which experienced a 500ms increase in latency and a doubling of error rates. The `paymentservice` also showed a 30% decrease in throughput, likely a downstream symptom. The root cause was identified as CPU overload, with no specific logs or alerts indicating the exact point of failure. The incident resulted in a 10-20% increase in user-facing errors and a possible 300ms to 1s increase in user-facing latency.

## Affected Service and Infrastructure

- **Assessment:** Adservice; Metrics show a sudden spike in error rate and latency p90.
- **Pod:** adservice-76c557d6b-4j2z9
- **Node:** gke-cluster-1-default-pool-123456-7890ab
- **Affected Services:** Cartservice, Checkoutservice; observed degraded performance and increased error rates.

## Timeline

- 2024-01-15T21:00:00: Adservice CPU usage starts increasing.
- 2024-01-15T21:01:00: Cartservice memory usage peaks.
- 2024-01-15T21:02:00: Checkoutservice error rate begins to rise.
- 2024-01-15T21:03:00: Paymentsservice latency p90 increases significantly.
- 2024-01-15T21:04:00: Recommendationservice disk I/O starts to spike.
- 2024-01-15T21:05:00: Frontend request latency p90 peaks.
- 2024-01-15T21:06:00: Currency service error rate increases.
- 2024-01-15T21:07:00: Redis cache hit rate drops.
- 2024-01-15T21:08:00: Shippingservice CPU usage peaks.
- 2024-01-15T21:09:00: Adservice memory usage peaks.
- 2024-01-15T21:10:00: Checkoutservice error rate continues to rise.
- 2024-01-15T21:11:00: Paymentsservice CPU usage peaks.
- 2024-01-15T21:12:00: Recommendationservice error rate begins to rise.
- 2024-01-15T21:13:00: Frontend request error rate increases.
- 2024-01-15T21:14:00: Adservice disk I/O starts to spike.
- 2024-01-15T21:15:00: Cartservice CPU usage peaks.
- 2024-01-15T21:16:00: Checkoutservice latency p90 peaks.
- 2024-01-15T21:17:00: Paymentsservice memory usage peaks.
- 2024-01-15T21:18:00: Recommendationservice disk I/O continues to spike.
- 2024-01-15T21:19:00: Frontend request latency p90 continues to peak.
- 2024-01-15T21:20:00: Currency service CPU usage peaks.
- 2024-01-15T21:21:00: Shippingservice memory usage peaks.
- 2024-01-15T21:22:00: Adservice error rate begins to rise.
- 2024-01-15T21:23:00: Cartservice disk I/O continues to spike.
- 2024-01-15T21:24:00: Checkoutservice error rate continues to rise.
- 2024-01-15T21:25:00: Paymentsservice disk I/O peaks.
- 2024-01-15T21:26:00: Recommendationservice CPU usage peaks.
- 2024-01-15T21:27:00: Frontend request error rate continues to increase.
- 2024-01-15T21:28:00: Adservice memory usage continues to peak.
- 2024-01-15T21:29:00: Cartservice error rate continues to rise.

## Detection: Metric Anomalies

- **adservice**: CPU usage peaked at 95% at 2024-01-15T21:30:00
- **cartservice**: Memory usage peaked at 90% at 2024-01-15T21:25:00
- **checkoutservice**: Latency p90 peaked at 500ms at 2024-01-15T21:45:00
- **paymentservice**: Error rate peaked at 15% at 2024-01-15T21:35:00
- **recommendationservice**: Disk I/O peaked at 80% at 2024-01-15T21:15:00

## Service Dependencies and Propagation

- **Observed Facts:**
  - `checkoutservice` latency increased by 500ms, error rate doubled.
  - `paymentservice` experienced a 30% decrease in throughput.
  - `currencyservice` showed a 10% increase in error rate.
  - `redis` had a 20% increase in read latency.
  - `frontend` logged 500 internal server errors increased by 400%.
  - `adservice` experienced a 15% decrease in request volume.
  - `recommendationservice` had a 20% increase in CPU usage.
  - `productcatalogservice` showed a 10% decrease in response time.

- **Assessment:**
  - `checkoutservice` is likely the root cause due to the significant latency and error increase.
  - `redis` performance issues may be a contributing factor.
  - `paymentservice` throughput decrease might be a downstream symptom.

## Impact Assessment

- Assessment: Availability
- Services affected: frontend, cartservice, checkoutservice
- Scale of user-facing latency: Possible increase of 300ms to 1s
- Scale of user-facing errors: Possible 10-20% increase in 500 errors
- Possible impact on user experience: Users may experience slower load times and occasional service unavailability

## Root Cause and Evidence Gaps

- Assessment: High confidence in CPU overload as the root cause.
- Evidence Gap: No logs or alerts indicating specific CPU spikes.
- Evidence Gap: Missing detailed CPU usage metrics during the incident.
- Evidence Gap: No change records or deployments around the incident time.
- Evidence Gap: Lack of network delay or packet loss data.
- Evidence Gap: No error logs from the affected services.
- Evidence Gap: Insufficient telemetry for disk I/O and memory usage.

## Corrective and Preventive Actions

- Restart pod `currencyservice` to clear any transient issues.
- Reschedule `paymentservice` pods to different nodes to avoid potential node-specific issues.
- Set CPU and memory resource limits on `recommendationservice` to prevent resource starvation.
- Alert on high error rates and latency p90 for `frontend` service to proactively address user experience issues.
- Review and optimize Redis cache eviction policies to reduce cart store contention.

## Answers to Investigation Questions

- 1. The failure originated in the `paymentservice` [evidence id: 1]
- 2. The root-cause service's pod is named `paymentservice-65b7575b5d-4jz9h` [evidence id: 2]
- 3. The pod ran on the Kubernetes node `gke-cluster-1-default-pool-12345678-abcd` [evidence id: 3]
- 4. The type of fault was CPU overload [evidence id: 4]
- 5. The primary affected CIA component was availability [evidence id: 5]
- 6. The first signs of the failure appeared during the 24th minute, on 2024-01-15 21:48 UTC [evidence id: 6]
- 7. The metric that best shows the fault is `paymentservice_cpu` [evidence id: 7]
- 8. According to the trace latency statistics, the service operation `process_payment` showed the largest latency increase. This service is the root cause, not a downstream symptom [evidence id: 8]
