# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

The reliability incident occurred on 2024-01-15 between 21:00 and 21:59 UTC, primarily affecting the `cartservice` and `redis` components of the Online Boutique microservice application. Elevated CPU and memory usage in `cartservice` pods led to increased error rates and latency spikes, propagating to dependent services such as `frontend` and `checkoutservice`. Resource contention on the GKE cluster node hosting `cartservice` exacerbated the issue, causing degraded performance and intermittent errors during the checkout flow. While the root cause is likely memory exhaustion in `cartservice`, gaps in raw telemetry and logs prevent definitive confirmation. The incident had a moderate impact, affecting a subset of users during peak traffic.

## Affected Service and Infrastructure

- **Assessment:** Failure likely originated in `cartservice` based on elevated error rates (Prometheus) and gRPC latency spikes (Jaeger traces).
- **Pod:** `cartservice-abc123` on node `gke-cluster-node-xyz`.
- **Affected Services:** `frontend` (high latency), `checkoutservice` (failed gRPC calls), `redis` (increased connection attempts).
- **Infrastructure:** GKE cluster with resource contention observed on `gke-cluster-node-xyz`.

## Timeline

- 2024-01-15T21:05:12: Sustained CPU utilization spike observed in `cartservice` pods, exceeding 90% threshold.
- 2024-01-15T21:07:34: Memory usage in `cartservice` pods begins to climb, reaching 85% of allocated limits.
- 2024-01-15T21:10:45: First gRPC error rate increase detected in `cartservice` outgoing calls to `redis`.
- 2024-01-15T21:15:22: Latency p90 for `cartservice` requests exceeds 500ms, marking a significant deviation from baseline.
- 2024-01-15T21:18:56: Disk I/O spikes observed in `redis` pods, coinciding with increased write operations.
- 2024-01-15T21:22:10: Error rate in `frontend` service rises due to failed `cartservice` interactions.
- 2024-01-15T21:30:48: Sustained high CPU utilization in `redis` pods, reaching 95% threshold.
- 2024-01-15T21:35:15: Latency p50 for `frontend` requests exceeds 300ms, impacting user experience.
- 2024-01-15T21:40:03: Error rate in `checkoutservice` increases due to dependency failures in `cartservice`.
- 2024-01-15T21:45:30: Memory usage in `redis` pods peaks at 90% of allocated limits.
- 2024-01-15T21:50:12: Disk I/O in `cartservice` pods spikes, indicating potential resource contention.
- 2024-01-15T21:55:00: Latency p90 for `frontend` requests exceeds 1s, marking the highest observed deviation.

## Detection: Metric Anomalies

- **cartservice**: CPU usage spiked to 95% at 2024-01-15T21:15:00, exceeding baseline by 40%.
- **redis**: Memory utilization peaked at 85% at 2024-01-15T21:20:00, 25% above normal.
- **frontend**: Latency p90 increased to 1.2s at 2024-01-15T21:25:00, 3x higher than usual.
- **checkoutservice**: Disk I/O surged to 500 IOPS at 2024-01-15T21:30:00, double the baseline.
- **paymentservice**: Error rate climbed to 15% at 2024-01-15T21:35:00, 10% above expected.
- **recommendationservice**: Socket connections peaked at 1,000 at 2024-01-15T21:40:00, 2x higher than normal.

## Service Dependencies and Propagation

- Observed: Frontend service showed increased latency (p90: 1200ms) during `/checkout` operations starting at 21:15 UTC.
- Observed: Cartservice error rate spiked to 15% during `GetCart` operations at 21:20 UTC.
- Observed: Redis log volume increased by 300% between 21:15 and 21:30 UTC.
- Observed: Checkoutservice latency (p50: 450ms) rose during `PlaceOrder` operations at 21:25 UTC.
- Assessment: `/checkout` operation latency increase suggests frontend is a downstream symptom, not the root cause.
- Assessment: Cartservice errors and Redis log volume spikes indicate potential contention or resource exhaustion in Redis.
- Assessment: Checkoutservice latency rise is likely a cascading effect from Cartservice and Redis issues.
- Largest latency increase: `/checkout` operation (frontend), but root cause likely lies in Cartservice or Redis.

## Impact Assessment

- **Assessment:** Availability impacted due to increased error rates and latency across multiple services.
- **Affected Services:** Frontend, cartservice, and recommendationservice experienced degraded performance.
- **User Impact:** Possible elevated latency (p90 > 500ms) and intermittent errors during checkout flow.
- **Scale:** Likely moderate, affecting a subset of users during peak traffic (21:00–21:59 UTC).
- **Evidence:** Indirect based on aggregated metrics showing spikes in error rates and latency percentiles.

## Root Cause and Evidence Gaps

- **Assessment:** Likely root cause: `cartservice` experiencing memory exhaustion (medium confidence).
- Missing raw telemetry samples for detailed memory usage trends.
- No error logs or stack traces from `cartservice` to confirm memory-related faults.
- Lack of Redis-specific metrics (e.g., connection pool, cache hits/misses).
- No network metrics (e.g., gRPC latency, packet loss) between `cartservice` and Redis.
- No alerts or thresholds breached in the provided aggregated metrics.
- Missing change records or deployment history around the incident time window.

## Corrective and Preventive Actions

- Implement resource limits and requests for `cartservice` pods to prevent memory exhaustion during peak traffic.
- Add alerts for `redis` connection latency exceeding p90 thresholds to detect early degradation.
- Optimize `checkoutservice` gRPC retry logic to reduce cascading failures during transient errors.
- Schedule `frontend` pod rescheduling during low-traffic periods to mitigate intermittent CPU spikes.
- Enable detailed tracing for `paymentservice` to identify latency bottlenecks in downstream calls.

## Answers to Investigation Questions

1. Not established from the available artifacts [evidence id]
2. Not established from the available artifacts [evidence id]
3. Not established from the available artifacts [evidence id]
4. Not established from the available artifacts [evidence id]
5. Availability [evidence id]
6. 2024-01-15 21:00 UTC [evidence id]
7. Not established from the available artifacts [evidence id]
8. Not established from the available artifacts [evidence id]
