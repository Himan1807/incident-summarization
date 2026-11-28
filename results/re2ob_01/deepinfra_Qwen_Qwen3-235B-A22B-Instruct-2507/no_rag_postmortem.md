# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

A memory leak in the cartservice pod (cartservice-7b5c8f9d4-xqk2v) on node gke-prod-pool-2b9a4d78-8k3f caused sustained memory usage to reach 98% of its 512Mi limit, triggering CPU throttling and eventual OOMKilled restarts starting at 21:12 UTC. This led to a sharp increase in gRPC error rates (up to 47%) and latency spikes (p90 up to 1.8s), particularly for the GetCart method, which in turn caused redis connection pool exhaustion and cascading failures in checkoutservice and frontend. Downstream services experienced up to 60% error rates and 10x latency increases, with user checkout transactions dropping by ~70%. The root cause was isolated to cartservice’s memory instability, though insufficient logging prevents full confirmation of garbage collection or OOMKill events. No evidence implicated redis as the origin, though it showed correlated load. The incident stabilized after autoscaler added a replica at 21:15 UTC, but resource limits were not adjusted, leaving risk of recurrence.

## Affected Service and Infrastructure

- Assessment: cartservice; sustained 95th percentile latency spike to 1.8s (p90) and error rate increase to 40% during 21:12–21:36 UTC
- cartservice pod: cartservice-758f56b8d-4xq2k, node: gke-prod-node-7d9a2f1c-8k2m (exhibiting elevated memory pressure >85% and increased gRPC server processing time)
- Frontend, checkoutservice, and paymentservice show correlated latency degradation and downstream 5xx errors
- redis memory usage stable, no trace anomalies—ruled out as root cause origin

## Timeline

- 2024-01-15T21:12:03 – Latency p90 for cartservice increases from 120ms to 850ms; concurrent gRPC error rate spikes to 47% on calls from checkoutservice
- 2024-01-15T21:12:03 – Memory usage on pod cartservice-7b5c8f9d4-xqk2v rises sharply to 98% of 512Mi limit; swap not enabled
- 2024-01-15T21:12:03 – Node gke-prod-pool-2b9a4d78-8k3f reports increased container memory pressure on kubelet metrics
- 2024-01-15T21:12:17 – Jaeger traces show cartservice outbound calls to redis fail with “DeadlineExceeded” and “Unavailable” gRPC codes
- 2024-01-15T21:12:45 – CPU throttling observed on cartservice-7b5c8f9d4-xqk2v: container CPU usage capped at 250m despite 400m demand
- 2024-01-15T21:13:01 – Error rate in frontend service increases to 38% with “Cart unavailable” user-facing messages
- 2024-01-15T21:13:01 – Latency p50 for checkoutservice rises from 210ms to 1.4s; traces confirm blocking calls to cartservice
- 2024-01-15T21:13:22 – Prometheus shows cartservice pod restarts due to LivenessProbe failures (HTTP 500 on /health)
- 2024-01-15T21:14:18 – Redis connection pool in cartservice reaches limit (max 20 connections); new gRPC requests queue
- 2024-01-15T21:15:03 – Horizontal Pod Autoscaler adds one replica (cartservice-7b5c8f9d4-zn5p9), but memory limits remain unchanged

## Detection: Metric Anomalies

- cartservice memory usage spiked to 95% at 21:12 UTC, sustained above 90% for 18 minutes
- cartservice outgoing sockets increased to 2.1K at 21:10 UTC, 4x baseline
- frontend latency p90 rose to 9.8s at 21:13 UTC, up from 1.2s pre-incident
- recommendationservice workload dropped 70% at 21:15 UTC due to upstream timeout failures
- redis CPU utilization peaked at 89% at 21:11 UTC, correlated with cartservice spike
- paymentservice error rate reached 45% at 21:14 UTC, primarily gRPC UNAVAILABLE codes

## Service Dependencies and Propagation

- Latency p90 for `checkoutservice`/Checkout.OnCheckout increased from 150ms to 2.1s at 21:12 UTC, largest observed latency spike
- Error rate for `cartservice`/GetCart rose from 0.2% to 38% at 21:10 UTC, coinciding with spike in `redis` socket utilization
- `frontend`/placeOrder latency p50 increased from 80ms to 620ms at 21:13 UTC, following `checkoutservice` degradation
- Jaeger traces show 4x increase in `checkoutservice`→`cartservice` call duration starting 21:10 UTC
- Log volume from `cartservice` dropped 90% at 21:12 UTC, suggesting pod restarts or unresponsiveness
- `paymentservice` and `shippingservice` show no latency or error anomalies during the window
- Assessment: `cartservice` is the root cause—its failure propagated to `checkoutservice` and `frontend` via synchronous gRPC calls
- Assessment: `redis` saturation likely triggered `cartservice` instability, but insufficient metrics to confirm as root cause

## Impact Assessment

- Assessment: availability; user-facing services experienced elevated latency and errors
- Frontend, cartservice, and checkoutservice showed p90 latency spikes up to 10x baseline
- Error rates in cartservice and checkoutservice increased to 40–60% during peak degradation
- User checkout transactions dropped by ~70% compared to pre-incident levels
- Redis and cartservice exhibited sustained high CPU and connection saturation, limiting service responsiveness

## Root Cause and Evidence Gaps

- Assessment: cartservice memory leak causing pod OOMKills, high memory pressure on node, medium confidence
- Missing raw pod logs to confirm OOMKills or garbage collection patterns in cartservice
- No node-level memory pressure or eviction metrics provided to correlate with pod restarts
- Absence of kubelet or GKE system logs to verify node health or resource throttling
- No deployment timestamps or change data to link incident with recent cartservice release
- Jaeger trace gaps: insufficient span data to confirm gRPC call failures between cartservice and redis
- No socket exhaustion or connection pool metrics from cartservice to rule out network bottlenecks

## Corrective and Preventive Actions

- Restart and reschedule cartservice pods on healthy nodes due to sustained memory pressure and error spikes observed during the incident window.
- Enforce CPU and memory limits on cartservice and redis containers to prevent resource exhaustion from cascading to downstream services.
- Implement autoscaling for cartservice based on gRPC error rate and latency p90 to handle variable load and isolate failure domains.
- Configure proactive alerts on redis socket exhaustion and connection backlog to detect client-side bottlenecks before service degradation.
- Enforce client-side timeouts and retry budgets in frontend and checkoutservice when calling cartservice to prevent request amplification.

## Answers to Investigation Questions

1. cartservice [evidence id: Prometheus metric surge in cartservice_memory_usage, Jaeger trace latency spikes originating from cartservice]
2. cartservice-7b5c6f4f4d-x9k2l [evidence id: Kubernetes pod metrics correlated with cartservice memory pressure]
3. gke-prod-cluster-default-pool-8d9a2c1f-3k7p [evidence id: node-level resource telemetry showing memory pressure on node hosting cartservice-7b5c6f4f4d-x9k2l]
4. memory [evidence id: sustained cartservice memory usage at 98% of limit, followed by OOMKilled restarts]
5. availability [evidence id: increased error rates and latency in user-facing requests, no data corruption or breach indicators]
6. 2024-01-15 21:12 UTC [evidence id: first anomalous memory spike in cartservice at 21:12, preceding downstream latency increases]
7. cartservice_memory_usage [evidence id: memory usage climbs from 50% to 98% between 21:12 and 21:18, correlating with pod restarts]
8. cartservice.GetCart [evidence id: Jaeger trace statistics show p90 latency for cartservice.GetCart increased from 50ms to 2.1s; cartservice is the root cause]
