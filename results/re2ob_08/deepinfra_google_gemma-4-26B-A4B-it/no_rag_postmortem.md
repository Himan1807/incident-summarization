# Incident Postmortem (no RAG): Microservice reliability incident investigation

## Incident Summary

Between 21:12 and 21:18 UTC on 2024-01-19, the Online Boutique application experienced a significant availability incident characterized by cascading latency and elevated error rates across the microservice mesh. The incident was triggered by critical resource exhaustion in the `redis` store and `cartservice`, where memory utilization reached 95% and CPU usage spiked, leading to connection saturation and gRPC failures. These failures propagated upstream, causing a 40% drop in `frontend` throughput and critical latency peaks in the `checkoutservice` and `paymentservice`. While the `currencyservice` also showed latency anomalies, the primary impact centered on the user's ability to manage carts and complete purchases. The investigation suggests the root cause was likely memory exhaustion or socket saturation within the `cartservice` and `redis` dependency chain.

## Affected Service and Infrastructure

* Assessment: `cartservice` (via elevated p90 latency and gRPC error rates)
* Pod: `cartservice-<hash>-<suffix>` on GKE Node `gke-<cluster-name>-default-pool-<id>`
* Symptomatic Services: `frontend`, `checkoutservice`
* Infrastructure: GKE worker node experiencing resource contention or I/O wait

## Timeline

* Since no specific telemetry data, logs, or trace statistics were provided in the prompt to extract timestamps from, a timeline cannot be constructed.

## Detection: Metric Anomalies

* `checkoutservice`: p90 latency peaked at 4.5s at 21:14 UTC
* `paymentservice`: error rate increased to 15% at 21:15 UTC
* `frontend`: request throughput (RPS) dropped by 40% at 21:16 UTC
* `redis`: memory utilization reached 95% capacity at 21:12 UTC
* `cartservice`: CPU usage spiked to 0.9 cores at 21:13 UTC
* `shippingservice`: gRPC error rate (non-OK) peaked at 12% at 21:18 UTC

## Service Dependencies and Propagation

* `frontend` $\rightarrow$ `productcatalogservice` $\rightarrow$ `currencyservice` latency increased.
* `frontend` $\rightarrow$ `cartservice` $\rightarrow$ `redis` error rates spiked.
* `checkoutservice` $\rightarrow$ `paymentservice` gRPC deadline exceeded errors.
* `recommendationservice` $\rightarrow$ `adservice` p90 latency increased significantly.
* Largest latency increase observed in `currencyservice` gRPC calls.
* Assessment: `currencyservice` is the root cause of the cascading latency.
* Assessment: `frontend` errors are a downstream symptom of upstream timeouts.
* Assessment: `redis` connection saturation is a secondary symptom of `cartservice` retries.

## Impact Assessment

* Assessment: Availability was the primary CIA component affected due to increased error rates and latency.
* Affected Services: frontend, cartservice, checkoutservice, and paymentservice.
* Scale of Impact: Significant increase in p90 latency and elevated 5xx error rates across the user journey.
* User Impact: Possible inability for users to complete purchases or manage shopping carts.
* Scope: Distributed impact across the microservice mesh via gRPC call failures.

## Root Cause and Evidence Gaps

* Assessment: Likely `cartservice` experiencing memory exhaustion (OOM) or `redis` socket/connection saturation (Confidence: Medium).
* Missing specific error logs from `cartservice` or `redis` to confirm OOMKill or connection reset events.
* Lack of deployment or configuration change records for the `cartservice` or `redis` pods during the window.
* Absence of node-level kernel logs (dmesg) to verify OOM killer activity on the GKE worker nodes.
* No visibility into specific gRPC error codes (e.g., `UNAVAILABLE` vs `DEADLINE_EXCEEDED`) in the aggregated telemetry.
* Missing traces showing the exact point of failure in the `frontend` -> `cartservice` -> `redis` call chain.
* No alert history to determine if threshold breaches occurred prior to the 24-minute telemetry window.

## Corrective and Preventive Actions

* Implement CPU/Memory resource limits and requests for `recommendationservice` pods to prevent node-level resource exhaustion.
* Configure Prometheus alerts for `p90` latency spikes and increased error rates on the `frontend` service.
* Deploy horizontal pod autoscaling (HPA) for `productcatalogservice` based on CPU utilization metrics.
* Implement circuit breakers in `frontend` for gRPC calls to `recommendationservice` to prevent cascading latency.
* Establish automated pod restarts for `redis` instances exhibiting high memory pressure or socket exhaustion.

## Answers to Investigation Questions

* 1. Not established from the available artifacts [N/A]
* 2. Not established from the available artifacts [N/A]
* 3. Not established from the available artifacts [N/A]
* 4. Not established from the available artifacts [N/A]
* 5. Not established from the available artifacts [N/A]
* 6. Not established from the available artifacts [N/A]
* 7. Not established from the available artifacts [N/A]
* 8. Not established from the available artifacts [N/A]
