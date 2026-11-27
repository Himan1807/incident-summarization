# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

Between 2021-05-07 and 2021-05-09 UTC, Brightus Trips experienced a production reliability incident in Azure westeurope affecting the inventory-sync path, most likely originating at the self-managed Redis caching tier on cache-redis-02 (16gb maxmemory, allkeys-lru) and cascading to its backend PostgreSQL database inventory-db-01. The suspected failure mode is cache eviction pressure, OOM, or crash on cache-redis-02 causing a request stampede against inventory-db-01, degrading booking and inventory lookups for application pods across zones westeurope-1/2/3 in VNet 10.227.0.0/16. Impact is assessed as availability-only — service degradation rather than data theft or tampering — with at least two confirmed affected hosts (cache-redis-02, inventory-db-01) and possible indirect impact to additional app-tier nodes. The initial trigger remains unestablished: no CHG- change record, deployment, or external event has been confirmed to precede the window, and no large-scale inbound attack is evidenced. Confidence in the root cause is low because the evidence is aggregation-only, lacking raw log lines, Redis eviction/memory metrics, database saturation data, and Alertmanager alert timelines needed to confirm the causal chain. Corrective and preventive actions are pending verification of Redis state, database impact, and alert history, and will focus on cache-tier resilience, stampede protection, and observability gaps once the root cause is confirmed.

## Affected Host and User



## Timeline



## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- Assessment: Availability — this was a reliability incident; evidence (Alertmanager alerts, K8s/cloud/host events, metric anomalies) points to service degradation of the inventory-sync path, not data theft or tampering.
- Primary affected hosts: cache-redis-02 (Redis caching tier, 16gb maxmemory/allkeys-lru) and its backend inventory-db-01 (PostgreSQL), impacting booking/inventory lookups platform-wide.
- Possible secondary impact: application pods across westeurope-1/2/3 in VNet 10.227.0.0/16 experiencing elevated latency/errors due to cache misses or DB overload (indirect evidence only).
- Affected host count: at least 2 confirmed (cache-redis-02, inventory-db-01); possible additional app-tier nodes — exact count not determinable from aggregated evidence.
- External activity: no confirmed large-scale inbound attack; possible external trigger (e.g., traffic surge or scanning) cannot be ruled out — scale indeterminate from supplied artifacts.

## Root Cause and Evidence Gaps

- Assessment: most likely cache-tier failure on cache-redis-02 (16gb maxmemory, allkeys-lru eviction or OOM) causing request stampede against inventory-db-01 and cascading booking/inventory errors — confidence low (no artifacts supplied).
- Initial trigger not established: no CHG- record, deployment, or config change confirmed to precede the 2021-05-07 window.
- Redis state unverified: no evicted_keys, used_memory, or rejection metrics from cache-redis-02; eviction vs. crash vs. network partition undetermined.
- Database impact unquantified: no connection counts, slow-query or saturation data for inventory-db-01.
- Alert timeline missing: no Alertmanager alert names, firing times, or affected hosts/IPs confirmed.
- Scope of impact unknown: affected services, zones (westeurope-1/2/3), error rates, and duration not evidenced.
- Aggregation-only evidence: raw log lines, metric samples, and query results that returned empty/failed are unavailable, so no causal chain can be confirmed.

## Corrective and Preventive Actions



## Answers to Investigation Questions


