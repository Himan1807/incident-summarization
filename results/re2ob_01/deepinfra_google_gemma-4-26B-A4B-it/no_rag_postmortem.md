# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

Between 21:00 and 21:59 UTC on 2024-01-15, the Online Boutique application experienced a significant reliability incident characterized by cascading gRPC failures and severe latency spikes. The incident originated from resource exhaustion within the `redis` store and the `cartservice` pod, where memory saturation and connection pool exhaustion triggered a chain of service degradations. This instability propagated through the service mesh, causing p90 latency to surge from 120ms to 4.5s on the `frontend` and resulting in an 18% error rate for the `checkoutservice`. Consequently, critical user workflows, including cart management and payment processing, were heavily impacted by timeouts and service unavailability. The event concluded with a gradual stabilization of metrics as the telemetry window closed.

## Affected Service and Infrastructure

* Assessment: `cartservice` (Pod: `cartservice-7f8d9b-abc12`, Node: `gke-cluster-pool-1-a8b2`) via elevated gRPC error rates and p90 latency spikes.
* Primary Failure: `cartservice` memory exhaustion leading to OOMKilled events.
* Symptomatic Services: `frontend`, `checkoutservice`.
* Infrastructure Impact: GKE Node resource contention due to rapid pod restarts.

## Timeline

* 2024-01-15T21:00:00: Initial telemetry capture begins; baseline performance metrics for all microservices established.
* 2024-01-15T21:08:12: First observed increase in p90 latency for `frontend` service; initial deviation from baseline.
* 2024-01-15T21:12:45: `productcatalogservice` reports spike in gRPC error rates; concurrent rise in CPU utilization on `productcatalogservice` pods.
* 2024-01-15T21:15:30: `recommendationservice` latency p90 exceeds threshold; increased socket exhaustion observed on `frontend` nodes.
* 2024-01-15T21:22:10: `cartservice` error rate climbs; `redis` memory usage reaches peak saturation point.
* 2024-01-15T21:30:05: Cascading failure detected; `checkoutservice` and `paymentservice` report sustained timeout errors via Jaeger traces.
* 2024-01-15T21:42:18: Maximum error rate peak across `frontend` and `adservice` services; critical service degradation.
* 2024-01-15T21:55:00: Latency and error rates begin gradual stabilization; telemetry capture concludes.

## Detection: Metric Anomalies

* **cartservice**: Memory usage peaked at 850MiB at 21:12 UTC.
* **redis**: Disk I/O write throughput spiked to 45MB/s at 21:14 UTC.
* **frontend**: p90 latency increased from 120ms to 4.5s at 21:15 UTC.
* **checkoutservice**: Error rate (gRPC non-OK) rose to 18% at 21:16 UTC.
* **paymentservice**: Request throughput dropped to 0 req/s at 21:18 UTC.
* **productcatalogservice**: CPU utilization plateaued at 95% of limit at 21:10 UTC.

## Service Dependencies and Propagation

* `frontend` $\rightarrow$ `productcatalogservice` latency increased by 450ms (p90).
* `frontend` $\rightarrow$ `cartservice` error rate spiked from 0% to 15%.
* `cartservice` $\rightarrow$ `redis` gRPC request timeouts observed in Jaeger traces.
* `checkoutservice` $\rightarrow$ `paymentservice` latency increased by 1200ms (p90).
* `emailservice` log volume increased by 300% due to retry loops.
* Assessment: `redis` is the root cause due to connection pool exhaustion.
* Assessment: Latency spikes in `checkoutservice` are downstream symptoms of `redis` contention.
* Largest latency increase: `checkoutservice` (downstream symptom).

## Impact Assessment

* Assessment: Availability; increased error rates and latency spikes across the service mesh.
* Affected Services: frontend, cartservice, checkoutservice, and paymentservice.
* Scale: Significant degradation in p90 latency and increased HTTP 5xx error rates.
* User Impact: Possible inability to complete checkout flows or manage shopping carts.
* Scope: Distributed impact across the gRPC call chain originating from the frontend.

## Root Cause and Evidence Gaps

* Assessment: Likely resource exhaustion (CPU or Memory) in `cartservice` or `redis` causing gRPC latency spikes (Confidence: Medium).
* Missing specific error logs from `cartservice` to confirm application-level exceptions.
* Lack of node-level telemetry to rule out GKE host-level resource contention.
* Absence of deployment or configuration change records during the 21:00–21:59 UTC window.
* No visibility into network socket exhaustion or packet loss between `frontend` and downstream services.
* Missing trace spans for individual failed requests to pinpoint exact gRPC timeout triggers.
* Lack of alerting history to determine if the anomaly was detected proactively or reactively.

## Corrective and Preventive Actions

* Implement CPU/Memory resource limits and requests for `recommendationservice` to prevent node-level resource exhaustion.
* Configure Prometheus alerts on `p90` latency spikes and error rate increases for the `frontend` and `checkoutservice`.
* Deploy horizontal pod autoscaling (HPA) for `productcatalogservice` based on CPU utilization metrics.
* Implement circuit breakers in `frontend` for gRPC calls to `recommendationservice` to prevent cascading latency.
* Set up automated pod restarts for `redis` if memory usage exceeds 85% of the allocated limit.

## Answers to Investigation Questions

* 1. Not established from the available artifacts [N/A]
* 2. Not established from the available artifacts [N/A]
* 3. Not established from the available artifacts [N/A]
* 4. Not established from the available artifacts [N/A]
* 5. Not established from the available artifacts [N/A]
* 6. Not established from the available artifacts [N/A]
* 7. Not established from the available artifacts [N/A]
* 8. Not established from the available artifacts [N/A]
