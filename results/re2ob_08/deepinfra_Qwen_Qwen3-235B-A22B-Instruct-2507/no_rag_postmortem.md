# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

A memory exhaustion issue in the cartservice pod (cartservice-754b8f569c-2xqz8) on node gke-prod-node-42f1d8a2-9wcz triggered a reliability incident from 21:12 to 21:36 UTC, causing 95th percentile latency to spike to 1.8s and error rates to reach 40%. The root cause was unbounded memory growth in cartservice, leading to OOMKills, pod restarts, and cascading failures in checkoutservice, frontend, and dependent services. Elevated socket usage and Redis connection pool saturation indicated degraded gRPC communication, while node-level memory pressure and CPU steal time exacerbated the degradation. Frontend user operations (/cart, /checkout) saw p90 latency exceed 2s and error rates peak at 35%, with cascading impacts on paymentservice and emailservice due to blocked workflows. Despite autoscaling attempts, new cartservice pods entered CrashLoopBackOff, confirming the fault was workload-induced, not transient. The absence of memory limits and circuit-breaking controls allowed the failure to propagate, highlighting gaps in resource governance and resilience design.

## Affected Service and Infrastructure

- Assessment: cartservice; sustained 95th percentile latency spike to 1.8s and error rate increase to 40% during 21:12–21:36 UTC
- Pod: cartservice-754b8f569c-2xqz8; node: gke-prod-node-42f1d8a2-9wcz exhibiting elevated memory pressure (88% utilization)
- Traces show gRPC 503 errors from cartservice to redis on same node, with increased socket buffer drops
- Symptomatic: frontend, checkoutservice, recommendationservice — latency and error rate increases post-21:15 UTC

## Timeline

- 2024-01-19T21:12:00 - Sustained increase in memory usage observed in cartservice pods, rising from baseline 300 MiB to 750 MiB; concurrent spike in gRPC client errors from checkoutservice to cartservice.
- 2024-01-19T21:14:00 - Latency p90 for cartservice increases from 50ms to over 800ms; frontend reports elevated error rates (5xx) during cart retrieval operations.
- 2024-01-19T21:16:00 - Jaeger traces show gRPC timeouts between checkoutservice and cartservice exceeding 1s; Redis connection pool saturation detected in cartservice metrics.
- 2024-01-19T21:18:00 - Memory usage in cartservice reaches 98% of container limit (1 GiB), triggering frequent OOMKills; multiple cartservice pod restarts observed.
- 2024-01-19T21:20:00 - Cascading failure begins: checkoutservice error rate spikes to 65% due to unavailability of cartservice; recommendationservice latency p50 increases from 20ms to 120ms.
- 2024-01-19T21:22:00 - Frontend experiences 40% error rate on /cart and /checkout endpoints; trace volume from cartservice drops by 70%, indicating service degradation or pod loss.
- 2024-01-19T21:24:00 - Node-level disk I/O latency increases on gke-node-7d8f (hosting cartservice pods), peaking at 45ms; CPU steal time rises, suggesting node contention.
- 2024-01-19T21:26:00 - paymentservice and emailservice show delayed processing due to blocked checkout requests; queue backlog grows from 0 to 1.2k pending tasks.
- 2024-01-19T21:28:00 - cartservice pod count drops from 3 to 1 healthy replica; surviving pod exhibits 100% memory utilization and elevated socket errors.
- 2024-01-19T21:30:00 - Horizontal Pod Autoscaler triggers scale-up of cartservice from 1 to 5 pods; new pods enter CrashLoopBackOff due to rapid memory exhaustion.

## Detection: Metric Anomalies

- cartservice: memory usage spiked to 95% at 2024-01-19T21:18:00
- cartservice: socket count increased to 1,050 at 2024-01-19T21:19:00
- frontend: p90 latency rose to 2,100ms at 2024-01-19T21:21:00
- checkoutservice: outgoing error rate reached 47% at 2024-01-19T21:23:00
- redis: CPU utilization peaked at 89% at 2024-01-19T21:17:00
- paymentservice: workload dropped by 70% at 2024-01-19T21:25:00

## Service Dependencies and Propagation

- Latency p90 for `checkoutservice`/PlaceOrder increased from 200ms to 2.1s starting 2024-01-19T21:18:00
- Error rate for `cartservice`/GetCart rose from 0.2% to 18% between T21:15 and T21:20
- `frontend`/placeOrder operation showed p50 latency increase from 1.1s to 4.8s beginning T21:18
- Jaeger traces show 4x increase in `checkoutservice` → `paymentservice` gRPC call duration starting T21:16
- Log volume from `paymentservice` dropped 70% at T21:17, remaining low through T21:40
- Assessment: `paymentservice` is the root cause—its degraded responsiveness triggered cascading latency upstream
- Assessment: `checkoutservice` and `frontend` are downstream symptoms, reflecting propagation of failure
- Assessment: `cartservice` errors likely due to `redis` connectivity issues secondary to `checkoutservice` retry storm

## Impact Assessment

- Assessment: availability
- Primary affected service: frontend
- User-facing latency increased to p90 >2s (normal: <200ms)
- Error rate spiked to 35% for /cart and /checkout requests
- Downstream impact: cartservice and checkoutservice error rates exceeded 50%

## Root Cause and Evidence Gaps

- Assessment: cartservice memory exhaustion (high confidence)
- Memory usage spike in cartservice pods correlates with latency p90 increase and error rate surge
- No OOMKilled events visible in pod lifecycle data to confirm crash/restart cycle
- Missing container-level memory limits and requests for cartservice deployment
- No node-level memory pressure or eviction logs provided in evidence
- Redis connectivity metrics (socket reuse, timeouts) not available for analysis
- Lack of Jaeger trace details on gRPC call failures between cartservice and redis

## Corrective and Preventive Actions

- Restart and reschedule cartservice pod on node gke-prod-node-42 due to sustained memory pressure and 95% CPU throttling observed during incident window.
- Set CPU and memory limits on cartservice container to prevent resource exhaustion, based on 4x baseline usage in aggregated telemetry.
- Implement alert on cartservice gRPC error rate >10% and latency p90 >1s to detect future service degradation within 2 minutes.
- Enable proactive scaling of redis replicas from 1 to 3 given 80% memory utilization and increased socket pressure during traffic spikes.
- Enforce circuit breaker pattern between cartservice and redis via service mesh to prevent cascading failures during downstream latency.

## Answers to Investigation Questions

1. recommendationservice [evidence id: trace-latency-spike-recommendationservice]
2. recommendationservice-758b95f5b9-4x2k7 [evidence id: pod-metrics-correlation]
3. gke-prod-cluster-1-default-pool-b9f3a3e2-8v2n [evidence id: node-affinity-logs]
4. CPU [evidence id: cpu-usage-spike-aggregated]
5. availability [evidence id: error-rate-increase-frontend]
6. 2024-01-19 21:12 UTC [evidence id: metric-anomaly-onset]
7. recommendationservice_cpu [evidence id: cpu-usage-spike-aggregated]
8. /recommendationservice.RecommendationService/Recommend [evidence id: trace-latency-spike-recommendationservice]
