# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

Assessment: inventory-db-01 is the likely origin of failure. The earliest sign of the failure was the KubeJobFailed warning at 2021-05-08 18:00 UTC. Assessment: the incident was a cascading failure. The incident impacted availability, including 28,321 events for booking-web and 8,599 "too many clients already" errors on inventory-db-01. Assessment: the most likely root cause was memory exhaustion on cache-redis-02 leading to high eviction rates and cache misses. Not established from the available artifacts: the Kubernetes pod and node for the originating service. [cache_stampede_0013-06#0, cache_stampede_0013-07#1, cache_stampede_0013-07#5, cache_stampede_0013-09#0, cache_stampede_0013-02#0, cache_stampede_0013-08#0]

## Affected Service and Infrastructure

* Assessment: inventory-db-01 is the likely origin of failure based on "postgres: FATAL: sorry, too many clients already" errors [cache_stampede_0013-06#0].
* Affected services: booking-web, inventory-sync, reservations-api, and fares-svc [cache_stampede_0013-02#0].
* Not established from the available artifacts: Kubernetes pod and node for the originating service.

## Timeline

- 2021-05-08 17:27 UTC — changes: CHG-40338 | batch_job | inventory-sync cache warm-up / metadata backfill | actor: azure-pipelines | 2021-05-08 17:27 UTC | status: completed | backfill wrote 64k new cache keys — 1 events; earliest alert hour [cache_stampede_0013-03#0, cache_stampede_0013-09#0]
- 2021-05-08 18:00 UTC — alert names: KubeJobFailed (warning) — 4 events; service: batch; first seen in hour 2021-05-08 18:00 UTC; last seen in hour 2021-05-08 20:00 UTC; alert timeline: 2 events; earliest alert hour [cache_stampede_0013-07#1, cache_stampede_0013-07#5, cache_stampede_0013-09#0]
- 2021-05-08 19:00 UTC — alert timeline: 1 events [cache_stampede_0013-07#5]
- 2021-05-08 20:00 UTC — alert timeline: 1 events [cache_stampede_0013-07#5]
- 2021-05-08 21:00 UTC — alert names: RedisMemoryHigh (warning) — 12 events; service: redis; first seen in hour 2021-05-08 21:00 UTC; last seen in hour 2021-05-09 02:00 UTC; alert names: TargetDown (warning) — 1 events; service: ancillaries-svc; first seen in hour 2021-05-08 21:00 UTC; last seen in hour 2021-05-08 21:00 UTC; alert timeline: 4 events; metric anomalies: redis_memory_used_bytes / redis_memory_max_bytes on cache-redis-02 — baseline 60%; peak 100%; onset 2021-05-08 21:00 UTC; recovered 2021-05-09 03:00 UTC; earliest metric anomaly onset 2021-05-08 21:00 UTC (redis_memory_used_bytes / redis_memory_max_bytes on cache-redis-02) [cache_stampede_0013-07#0, cache_stampede_0013-07#1, cache_stampede_0013-07#6, cache_stampede_0013-08#0, cache_stampede_0013-09#1]
- 2021-05-08 21:29 UTC — changes: CHG-40346 | deployment | loyalty-api 11.30.1 -> 11.30.2 | actor: azure-pipelines | 2021-05-08 21:29 UTC | status: Synced/Healthy | feature flag cleanup — 1 events [cache_stampede_0013-03#0]
- 2021-05-08 22:00 UTC — alert timeline: 1 events [cache_stampede_0013-07#6]
- 2021-05-08 23:00 UTC — alert names: RedisCacheHitRatioLow (critical) — 13 events; service: redis; first seen in hour 2021-05-08 23:00 UTC; last seen in hour 2021-05-09 02:00 UTC; alert names: BookingWeb5xxHigh (critical) — 11 events; service: booking-web; first seen in hour 2021-05-08 23:00 UTC; last seen in hour 2021-05-09 02:00 UTC; alert names: InventorySyncErrorRateHigh (critical) — 10 events; service: inventory-sync; first seen in hour 2021-05-08 23:00 UTC; last seen in hour 2021-05-09 02:00 UTC; alert names: PostgresTooManyConnections (critical) — 8 events; service: postgres; first seen in hour 2021-05-08 23:00 UTC; last seen in hour 2021-05-09 02:00 UTC; alert timeline: 12 events; metric anomalies: redis_evicted_keys_total rate on cache-redis-02 — baseline 0/s; peak 2,200/s; onset 2021-05-08 23:00 UTC; recovered 2021-05-09 03:00 UTC; metric anomalies: redis keyspace hit ratio on cache-redis-02 — baseline 96%; trough 9%; onset 2021-05-08 23:00 UTC; recovered 2021-05-09 03:00 UTC; metric anomalies: node_cpu utilisation on inventory-db-01 — baseline 26%; peak 100%; onset 2021-05-08 23:00 UTC; recovered 2021-05-09 03:00 UTC [cache_stampede_0013-07#0, cache_stampede_0013-07#1, cache_stampede_0013-07#6, cache_stampede_0013-08#0]
- 2021-05-09 00:00 UTC — alert timeline: 13 events [cache_stampede_0013-07#6]
- 2021-05-09 01:00 UTC — alert timeline: 15 events [cache_stampede_0013-07#7]
- 2021-05-09 02:00 UTC — alert timeline: 10 events [cache_stampede_0013-07#7]
- 2021-05-09 02:13 UTC — changes: CHG-40380 | config_push | cache-redis-02 redis.conf | actor: s.mueller | 2021-05-09 02:13 UTC | status: completed | CONFIG SET maxmemory 16gb -> 32gb; CONFIG REWRITE — 1 events [cache_stampede_0013-03#0]
- 2021-05-09 12:36 UTC — changes: CHG-40388 | deployment | fares-svc 11.25.3 -> 11.26.0 | actor: azure-pipelines | 2021-05-09 12:36 UTC | status: completed | minor bug fixes — 1 events [cache_stampede_0013-03#0]

## Detection: Metric Anomalies

* cache-redis-02: redis_memory_used_bytes / redis_memory_max_bytes peaked at 100% at 2021-05-08 21:00 UTC [cache_stampede_0013-08#0, cache_stampede_0013-09#1]
* cache-redis-02: redis_evicted_keys_total rate peaked at 2,200/s at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]
* cache-redis-02: redis keyspace hit ratio reached a trough of 9% at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]
* inventory-db-01: node_cpu utilisation peaked at 100% at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]

## Service Dependencies and Propagation

* booking-web experienced 28321 504 Gateway Timeout errors on GET /v1/inventory requests to inventory-sync [cache_stampede_0013-01#2, cache_stampede_0013-01#1].
* inventory-sync recorded 11135 500 errors during SELECT (cache miss fallback) operations to inventory-db-01 [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
* reservations-api generated 4761 503 errors for GET /v1/inventory/{id} requests to inventory-sync [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
* fares-svc produced 97 502 errors for query requests to fares-db [cache_stampede_0013-01#0, cache_stampede_0013-01#1, cache_stampede_0013-01#2].
* inventory-sync reported 11135 instances of pq: canceling statement due to statement timeout [cache_stampede_0013-01#2].
* Assessment: The inventory-sync service is the primary point of failure for the majority of error-emitting services [cache_stampede_0013-02#0].
* Assessment: The inventory-sync service is a downstream symptom of issues occurring at the inventory-db-01 layer [cache_stampede_0013-02#0, cache_stampede_0013-01#1].
* Assessment: The largest latency increase is associated with the inventory-sync service's database queries [cache_stampede_0013-01#2].

## Impact Assessment

* Assessment: Availability [cache_stampede_0013-02#0, cache_stampede_0013-06#0].
* Infrastructure impact includes cache-redis-02 and inventory-db-01 [cache_stampede_0013-05#0, cache_stampede_0013-08#0].
* Scale of impact includes 28,321 events for booking-web and 8,599 "too many clients already" errors on inventory-db-01 [cache_stampede_0013-02#0, cache_stampede_0013-06#0].

## Root Cause and Evidence Gaps

* Assessment: Most likely root cause is memory exhaustion on cache-redis-02 leading to high eviction rates and cache misses [cache_stampede_0013-08#0].
* Assessment: High confidence that CHG-40338 (inventory-sync cache warm-up / metadata backfill) triggered the incident [cache_stampede_0013-09#0].
* Not established: The specific fault type (CPU, network delay, packet loss, or socket) for the inventory-db-01 CPU spike [cache_stampede_0013-08#0].
* Not established: The exact mechanism by which the cache warm-up caused the memory peak [cache_stampede_0013-09#0].
* Not established: Presence or absence of error logs for the failing dependencies [cache_stampede_0013-02#0].

## Corrective and Preventive Actions

* Investigate the impact of CHG-40338 inventory-sync cache warm-up/metadata backfill on system stability [cache_stampede_0013-09#0].
* Address the RedisCacheHitRatioLow and RedisMemoryHigh alerts observed on cache-redis-02 [cache_stampede_0013-07#0, cache_stampede_0013-09#0].
* Resolve the PostgresTooManyConnections critical alerts affecting inventory-db-01 [cache_stampede_0013-07#1].
* Mitigate the InventorySyncErrorRateHigh and BookingWeb5xxHigh critical alerts [cache_stampede_0013-07#0, cache_stampede_0013-07#1].

## Answers to Investigation Questions

1. cache-redis-02 [cache_stampede_0013-09#0]
2. 10.227.167.238 [cache_stampede_0013-05#0]
3. inventory-db-01 [cache_stampede_0013-02#0]
4. 2021-05-08 18:00 UTC [cache_stampede_0013-09#0]
5. Not established from the available artifacts.
6. cascading failure [cache_stampede_0013-02#0]
7. Not established from the available artifacts.
8. booking-web; it is a downstream symptom [cache_stampede_0013-09#0]
9. CHG-40380 [cache_stampede_0013-03#0]
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
