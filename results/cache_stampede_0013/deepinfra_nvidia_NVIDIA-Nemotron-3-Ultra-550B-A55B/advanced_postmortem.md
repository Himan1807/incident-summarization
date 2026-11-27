# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary



## Affected Host and User



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

## Detection: IDS Alerts



## Initial Infection Indicators

- Not established from the available artifacts [cache_stampede_0013-09#1, cache_stampede_0013-05#0, cache_stampede_0013-06#0, cache_stampede_0013-09#0, cache_stampede_0013-10#0, cache_stampede_0013-02#0]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions


