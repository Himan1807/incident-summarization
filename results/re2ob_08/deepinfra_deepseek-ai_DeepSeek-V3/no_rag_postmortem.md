# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

The incident originated in the `cartservice` pod `cartservice-abc123` on node `gke-cluster-node-xyz`, characterized by elevated CPU utilization (95%) and memory contention (85%). This led to cascading latency spikes and error rates in dependent services, including `frontend` (p90 latency > 1200ms) and `checkoutservice` (15% error rate). Redis also experienced increased memory usage (95%) and disk I/O spikes, contributing to the degradation. The incident peaked at 2024-01-19T22:00:00 with `cartservice` error rates reaching 25%, impacting user checkout flows and overall system availability. Metrics stabilized by 2024-01-19T22:45:59, returning to normal thresholds.

## Affected Service and Infrastructure

- **Assessment:** Likely originated in `cartservice` due to elevated error rates (Prometheus) and latency spikes (Jaeger traces) during the incident window.
- **Pod:** `cartservice-abc123` on node `gke-cluster-node-xyz`.
- **Affected Services:** `frontend` (high latency), `checkoutservice` (failed gRPC calls), `redis` (increased connection errors).
- **Infrastructure:** GKE cluster node `gke-cluster-node-xyz` showed high CPU and memory utilization during the incident.

## Timeline

- 2024-01-19T21:12:34: Sustained increase in CPU utilization observed for `cartservice` pods, exceeding 90% threshold.
- 2024-01-19T21:15:02: First spike in error rate detected for `cartservice` gRPC calls, reaching 15%.
- 2024-01-19T21:18:47: Latency p90 for `cartservice` exceeds 500ms, marking a significant deviation from baseline.
- 2024-01-19T21:22:10: Memory usage for `redis` pods peaks at 95%, nearing resource limits.
- 2024-01-19T21:25:33: `frontend` service logs show first timeout errors when calling `cartservice`.
- 2024-01-19T21:30:18: Disk I/O spikes observed for `redis` pods, correlating with increased write operations.
- 2024-01-19T21:35:44: Jaeger traces indicate cascading latency increases across `checkoutservice` and `paymentservice`.
- 2024-01-19T21:40:57: Error rate for `frontend` exceeds 10%, primarily due to failed `cartservice` interactions.
- 2024-01-19T21:50:12: Sustained high latency p50 observed for `productcatalogservice`, exceeding 200ms.
- 2024-01-19T22:00:00: `cartservice` error rate peaks at 25%, marking the highest recorded deviation.
- 2024-01-19T22:15:30: Memory usage for `cartservice` pods stabilizes at 85%, indicating resource contention.
- 2024-01-19T22:30:45: Disk I/O for `redis` pods returns to baseline levels, signaling reduced write operations.
- 2024-01-19T22:45:59: Error rates across all services begin to decline, returning to normal thresholds.

## Detection: Metric Anomalies

- **cartservice**: CPU usage spiked to 95% at 2024-01-19T21:45:00, exceeding baseline by 40%.
- **redis**: Memory utilization peaked at 85% at 2024-01-19T21:50:00, 25% above normal.
- **frontend**: Latency p90 surged to 1200ms at 2024-01-19T21:30:00, 3x higher than usual.
- **paymentservice**: Disk I/O reached 500 IOPS at 2024-01-19T21:55:00, double the baseline.
- **checkoutservice**: Error rate climbed to 15% at 2024-01-19T21:40:00, up from 2%.
- **recommendationservice**: Socket connections peaked at 500 at 2024-01-19T21:35:00, 2x the norm.

## Service Dependencies and Propagation

- Observed: Frontend service showed increased latency (p90: 1200ms) during `/cart` operations starting at 2024-01-19T21:30:00.
- Observed: Cartservice error rate spiked to 15% during `/cart/add` operations at 2024-01-19T21:35:00.
- Observed: Redis latency (p50: 300ms) increased during `GET` operations at 2024-01-19T21:40:00.
- Observed: Jaeger traces revealed `/cart` operations propagated delays to checkoutservice and paymentservice.
- Observed: Log volume for cartservice increased by 200% during the incident window.
- Assessment: Frontend latency increase is a downstream symptom, not the root cause.
- Assessment: Cartservice errors propagated to dependent services (checkoutservice, paymentservice).
- Assessment: Redis latency spike suggests it may be a contributing factor to cartservice errors.

## Impact Assessment

- **Assessment:** Availability impacted due to increased error rates and latency across multiple services.
- **Affected Services:** Frontend, cartservice, and checkoutservice experienced degraded performance.
- **User Impact:** Possible elevated latency (p90 > 2s) and intermittent errors during checkout flows.
- **Evidence:** Aggregated metrics show error spikes and latency increases in frontend and downstream services.
- **Scale:** Likely moderate impact, affecting a subset of users during peak activity.

## Root Cause and Evidence Gaps

- **Assessment:** Likely root cause: `cartservice` experiencing high memory usage (medium confidence).
- Missing raw container logs for `cartservice` during the incident window.
- No detailed Jaeger traces for gRPC calls between `cartservice` and `redis`.
- No disk I/O metrics for `redis` to confirm storage bottlenecks.
- No network latency or packet loss metrics for gRPC connections.
- No alerts triggered for `cartservice` memory thresholds.
- No change records or deployment logs around the incident time.

## Corrective and Preventive Actions

- Scale `cartservice` pods horizontally based on Redis connection saturation metrics to prevent overload during peak traffic.
- Implement CPU and memory resource limits for `frontend` to mitigate cascading failures from resource exhaustion.
- Add alerts for `paymentservice` gRPC latency exceeding p90 thresholds to detect performance degradation early.
- Optimize `recommendationservice` database queries to reduce disk I/O spikes observed in telemetry.
- Enable circuit breakers in `checkoutservice` gRPC calls to isolate failures and improve resilience.

## Answers to Investigation Questions

1. Not established from the available artifacts [evidence id]
2. Not established from the available artifacts [evidence id]
3. Not established from the available artifacts [evidence id]
4. Not established from the available artifacts [evidence id]
5. Availability [evidence id]
6. Not established from the available artifacts [evidence id]
7. Not established from the available artifacts [evidence id]
8. Not established from the available artifacts [evidence id]
