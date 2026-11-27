# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

The root cause of the incident originated from the `inventory-sync` service, running on the `cache-redis-02` pod, which experienced memory pressure leading to a cache stampede. The first signs of the failure appeared during the hour 2021-05-08 18:00 UTC, and the failure cascaded across services, primarily affecting the `booking-web` service with significant user-facing latency and errors. The incident category is capacity exhaustion, and the CIA component primarily affected is availability. [cache_stampede_0013-08#0, cache_stampede_0013-09#0, cache_stampede_0013-01#0, cache_stampede_0013-01#1, cache_stampede_0013-06#0]

## Affected Service and Infrastructure

- Assessment: The failure most likely originated from the `inventory-sync` service. This is supported by the high number of failing dependencies reported by the `booking-web` and `reservations-api` services, with `inventory-sync` being the top dependency for both [cache_stampede_0013-02#0].
- The `inventory-sync` service is running on a Kubernetes pod that is part of the `inventory-sync` deployment. This is inferred from the service name and the high volume of failing requests it receives [cache_stampede_0013-01#1].
- The `booking-web` service is also affected, with a significant number of failing requests to `inventory-sync` [cache_stampede_0013-01#1].
- The `reservations-api` service is another affected service, experiencing failing requests to `inventory-sync` [cache_stampede_0013-01#1].

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

- [cache_stampede_0013-08#0] Redis memory usage on cache-redis-02 peaked at 100% of the maximum capacity on 2021-05-08 21:00 UTC.
- [cache_stampede_0013-08#0] The rate of evicted keys on cache-redis-02 spiked to 2,200/s on 2021-05-08 23:00 UTC.
- [cache_stampede_0013-08#0] The keyspace hit ratio on cache-redis-02 dropped to 9% on 2021-05-08 23:00 UTC.
- [cache_stampede_0013-08#0] Node CPU utilization on inventory-db-01 peaked at 100% on 2021-05-08 23:00 UTC.
- Not established from the available artifacts.

## Service Dependencies and Propagation

- booking-web showed the largest increase in latency and error events, with 28,321 failing requests and 28,321 error messages [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
- inventory-sync experienced a significant number of errors, with 11,135 failing requests and 11,135 error messages, indicating it is a critical downstream service [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
- reservations-api had the smallest number of failing requests and error messages, with 4,761 each, suggesting it may be less impacted or a less critical service in the chain [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
- Assessment: The largest latency increase and the highest number of error events were observed in booking-web, indicating it may be the root cause or a critical point in the service chain [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
- Assessment: inventory-sync's high error rate and dependency on inventory-db-01 suggest it is a key service that may be experiencing issues, potentially causing downstream failures [cache_stampede_0013-01#0, cache_stampede_0013-01#1].
- Assessment: The observed pattern of errors and failing requests indicates a potential issue with the caching mechanism, possibly leading to a cache stampede scenario [cache_stampede_0013-01#0, cache_stampede_0013-01#1].

## Impact Assessment

- Assessment: Availability was primarily affected, with significant user-facing latency and errors observed. indicates a FATAL error in the PostgreSQL database, suggesting a critical availability issue. shows that the `inventory-sync` service experienced the highest number of failing dependencies, impacting downstream services such as `booking-web`. confirms that the `booking-web` service ranked first in error volume, with 28,321 events, indicating widespread availability issues. Not established from the available artifacts. [cache_stampede_0013-06#0, cache_stampede_0013-02#0, cache_stampede_0013-09#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is memory pressure on the Redis cache, leading to a cache stampede. This is supported by the metrics showing a peak in memory usage and evicted keys, indicating a cache miss situation. [cache_stampede_0013-08#0, cache_stampede_0013-09#0]
- Not established: The exact trigger for the cache stampede is not established [cache_stampede_0013-09#0].
- Not established: Whether the Redis cache was configured to handle the load effectively [cache_stampede_0013-08#0].
- Not established: The presence or absence of error logs from the affected services [cache_stampede_0013-09#0].
- Not established: The impact on other services beyond the direct dependencies [cache_stampede_0013-09#0].
- Not established: The effectiveness of the change management process in preventing the incident [cache_stampede_0013-09#0].
- Not established: The configuration and health of the PostgreSQL database [cache_stampede_0013-08#0].

## Corrective and Preventive Actions

- Restart the `cache-redis-02` pod in the `westeurope-2` zone to clear any potential memory issues indicated by the `RedisMemoryHigh` alert [cache_stampede_0013-07#0].
- Schedule a `inventory-sync` cache warm-up process during off-peak hours to prevent similar issues in the future, based on the `CHG-40338` change record [cache_stampede_0013-09#0].
- Set resource limits on the `inventory-sync` service to prevent excessive memory usage and ensure stable operation [cache_stampede_0013-07#1].
- Monitor the `RedisCacheHitRatioLow` alert and investigate the root cause to optimize cache usage and reduce load on the PostgreSQL database [cache_stampede_0013-07#0].

## Answers to Investigation Questions

1. The hostname of the host or node where the failure originated is cache-redis-02 [cache_stampede_0013-05#0].
2. The IP address of the host or node where the failure originated is 10.227.167.238 [cache_stampede_0013-05#0].
3. The database host that became overloaded as a consequence of the initial failure is inventory-db-01 [cache_stampede_0013-06#0].
4. The first signs of the failure appeared during the hour 2021-05-08 18:00 UTC [cache_stampede_0013-09#0].
5. The root cause category of the incident is capacity exhaustion [cache_stampede_0013-09#0].
6. The failure cascaded across services [cache_stampede_0013-02#0].
7. The CIA component primarily affected is availability [cache_stampede_0013-06#0].
8. The single service that emitted the most errors is booking-web, which is not the root cause but a downstream symptom [cache_stampede_0013-01#3].
9. The change that restored normal service is CHG-40380 [cache_stampede_0013-03#0].
## Additional Investigation Questions

U1. Not established from the available artifacts [cache_stampede_0013-01#4]
U2. Not established from the available artifacts [cache_stampede_0013-01#4]
U3. Not established from the available artifacts [cache_stampede_0013-05#0]
