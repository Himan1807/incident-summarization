# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

The inventory-sync service, running on pod cache-redis-02 hosted on node 10.227.167.238, experienced cascading failures due to a memory exhaustion fault in the Redis caching tier, which began showing anomalies at 2021-05-08 21:00 UTC when redis_memory_used_bytes reached 100% of its 16GB limit. The earliest observable sign of failure was the KubeJobFailed alert at 2021-05-08 18:00 UTC, following the deployment of cache-warmup job CHG-40338 at 17:27 UTC. This fault manifested as a cache stampede, where aggressive key evictions and a drop in cache hit ratio to 9% at 23:00 UTC overwhelmed inventory-db-01 with connection requests, causing pq: canceling statement timeout errors. User-facing impact included high error rates in booking-web, with 28,321 failing requests due to 504 errors, indicating severe availability degradation. The incident propagated as a cascading failure originating from cache-redis-02’s memory fault, ultimately affecting multiple upstream services dependent on inventory-sync. Assessment: The root cause was a memory fault in the Redis caching tier triggered by an automated cache-warmup job, leading to resource exhaustion and cascading service failures. [cache_stampede_0013-08#0, cache_stampede_0013-05#0, cache_stampede_0013-09#0, cache_stampede_0013-01#2, cache_stampede_0013-01#1, cache_stampede_0013-02#0]

## Affected Service and Infrastructure

- The inventory-sync service exhibited the highest volume of failing requests directly tied to database connectivity issues, with 11,135 events showing "pq: canceling statement due to statement timeout" when querying inventory-db-01 [cache_stampede_0013-01#2].
- inventory-sync pods experienced cascading failures from upstream services booking-web and reservations-api, which generated 28,321 and 4,761 failing requests respectively due to 502 and 504 errors from inventory-sync [cache_stampede_0013-01#1].
- The PostgreSQL database inventory-db-01 hit connection limits, logging "FATAL: sorry, too many clients already" 8,599 times, directly correlating with inventory-sync's failed SELECT queries [cache_stampede_0013-06#0].
- Assessment: The failure most likely originated in the inventory-sync service, as evidenced by its direct dependency on a saturated database and its role as the common failing dependency for multiple upstream services [cache_stampede_0013-02#0].

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

- redis_memory_used_bytes / redis_memory_max_bytes on cache-redis-02 peaked at 100% utilization starting 2021-05-08 21:00 UTC [cache_stampede_0013-08#0]
- redis_evicted_keys_total rate on cache-redis-02 reached 2,200 evictions per second, up from baseline 0/s, beginning 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]
- redis key space hit ratio on cache-redis-02 dropped to 9% from 96% baseline, starting 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]
- node_cpu utilisation on inventory-db-01 spiked to 100% from 26% baseline, beginning 2021-05-08 23:00 UTC [cache_stampede_0013-08#0]
- InventorySyncErrorRateHigh alerts first triggered at 2021-05-08 23:00 UTC, coinciding with cache hit ratio decline and eviction surge [cache_stampede_0013-07#1]
- PostgresTooManyConnections alerts began at 2021-05-08 23:00 UTC, concurrent with CPU saturation on inventory-db-01 [cache_stampede_0013-07#1]

## Service Dependencies and Propagation

- The booking-web service emitted 28,321 error events with status code 504, primarily failing on GET requests to inventory-sync:8080 [cache_stampede_0013-01#1].
- The inventory-sync service emitted 11,135 error events with status code 500, linked to SELECT queries on inventory-db-01 during cache miss fallback scenarios [cache_stampede_0013-01#1].
- The reservations-api service had 4,761 failing requests to inventory-sync:8080 for GET /v1/inventory/{id}, resulting in 503 errors [cache_stampede_0013-01#1].
- The fares-svc service generated 97 error events with status code 502, tied to query failures on fares-db:5432 [cache_stampede_0013-01#2].
- All 97 connection reset by peer errors originated from fares-svc [cache_stampede_0013-01#3].
- The operation with the largest latency increase was GET /v1/inventory on inventory-sync, as indicated by the highest volume of 504 errors in booking-web [cache_stampede_0013-01#1].
- Assessment: inventory-sync is a downstream symptom, not the root cause, as its failures correlate with database query timeouts and upstream cache dependency issues [cache_stampede_0013-01#2].
- Assessment: The propagation path originated from inventory-sync’s inability to handle cache miss fallbacks, cascading failures to booking-web, reservations-api, and indirectly affecting fares-svc [cache_stampede_0013-02#0].

## Impact Assessment

- The primary CIA component affected was availability, as evidenced by service degradation and failure to process requests due to resource exhaustion [cache_stampede_0013-06#0].
- Assessment: The impact was primarily on availability, given the cascading service failures and inability to establish database connections [cache_stampede_0013-06#0].
- Services affected include booking-web, inventory-sync, and reservations-api, all failing due to dependency on inventory-sync, which in turn depended on inventory-db-01 [cache_stampede_0013-02#0].
- User-facing impact included high error rates in booking-web, with 28,321 events tied to failures in inventory-sync [cache_stampede_0013-09#0].
- Latency and error spikes were sustained from 2021-05-08 23:00 UTC to 2021-05-09 03:00 UTC, coinciding with redis keyspace hit ratio dropping to 9% and node_cpu on inventory-db-01 peaking at 100% [cache_stampede_0013-08#0].

## Root Cause and Evidence Gaps

- The Redis cache instance cache-redis-02 experienced memory exhaustion, reaching 100% of its allocated memory, with a clear anomaly onset at 2021-05-08 21:00 UTC [cache_stampede_0013-08#0].
- This led to aggressive key eviction, peaking at 2,200 evictions per second, starting at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0].
- The cache hit ratio on cache-redis-02 dropped from 96% to 9% at 2021-05-08 23:00 UTC, indicating severe cache inefficiency [cache_stampede_0013-08#0].
- The inventory-sync service, dependent on cache-redis-02, showed 11,135 error events, with inventory-db-01 as its top failing dependency [cache_stampede_0013-02#0].
- A change (CHG-40338) for inventory-sync cache warm-up and metadata backfill was deployed at 2021-05-08 17:27 UTC, preceding the memory anomaly [cache_stampede_0013-09#0].
- Assessment: High confidence that the root cause was a memory fault in the Redis caching tier (cache-redis-02), triggered by a cache-warmup job that led to excessive memory use and subsequent evictions, degrading inventory-sync and cascading to booking-web. [cache_stampede_0013-08#0, cache_stampede_0013-09#0, cache_stampede_0013-02#0]
- Not established from the available artifacts: whether the cache-warmup job loaded unnecessary or unbounded data, or if cache-redis-02’s memory limits were misconfigured [cache_stampede_0013-10#0].

## Corrective and Preventive Actions

- Restart the cache-redis-02 instance to restore normal cache-hit ratios and alleviate memory pressure [cache_stampede_0013-07#0].
- Reschedule the inventory-sync batch job to complete before peak traffic hours to prevent cache-warming load during critical periods [cache_stampede_0013-09#0].
- Implement rate limiting on inventory-sync service calls to prevent excessive Redis and Postgres load during cache misses [cache_stampede_0013-07#1].
- Set memory limits and alerts on cache-redis-02 to trigger before reaching 16GB threshold, preventing LRU evictions under stress [cache_stampede_0013-07#0].
- Enforce dependency retry logic with exponential backoff in booking-web to reduce 5xx errors during transient inventory-sync failures [cache_stampede_0013-09#0].

## Answers to Investigation Questions

1. cache-redis-02 [cache_stampede_0013-09#0]
2. 10.227.167.238 [cache_stampede_0013-05#0]
3. inventory-db-01 [cache_stampede_0013-02#0]
4. 2021-05-08 18:00 UTC [cache_stampede_0013-09#0]
5. automation error [cache_stampede_0013-03#0]
6. cascading failure [cache_stampede_0013-02#0]
7. availability [cache_stampede_0013-01#2]
8. booking-web; downstream symptom [cache_stampede_0013-01#3]
9. CHG-40380 [cache_stampede_0013-03#0]
## Additional Investigation Questions

U1. Not established from the available artifacts [cache_stampede_0013-09#0]
U2. Not established from the available artifacts [cache_stampede_0013-09#0]
U3. Not established from the available artifacts [cache_stampede_0013-09#0]
