# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

- The root-cause service was `inventory-sync`, which experienced cascading failures due to memory exhaustion on `cache-redis-02`, leading to degraded performance and PostgreSQL connection exhaustion on `inventory-db-01` [cache_stampede_0013-08#0, cache_stampede_0013-06#0].
- The earliest sign of failure was a RedisMemoryHigh warning at 2021-05-08 21:00 UTC, followed by RedisCacheHitRatioLow and PostgresTooManyConnections critical alerts at 2021-05-08 23:00 UTC [cache_stampede_0013-07#0, cache_stampede_0013-07#1].
- The fault type was resource exhaustion, with Redis memory peaking at 100% and PostgreSQL reporting "too many clients" errors [cache_stampede_0013-08#0, cache_stampede_0013-06#0].
- User-facing impact included service unavailability and latency, primarily affecting `booking-web`, which emitted 28,321 failing dependency events [cache_stampede_0013-02#0, cache_stampede_0013-08#0].
- Assessment: The incident was a cascading failure triggered by Redis memory exhaustion, propagating errors to dependent services and disrupting availability for approximately 6 hours [cache_stampede_0013-02#0, cache_stampede_0013-08#0].

## Affected Service and Infrastructure

- The PostgreSQL database `inventory-db-01` experienced 8599 "too many clients already" fatal errors, indicating connection exhaustion [cache_stampede_0013-06#0].
- Assessment: The failure most likely originated in the `inventory-sync` service, supported by 11135 failing dependency events to `inventory-db-01` and "statement timeout" errors. [cache_stampede_0013-02#0, cache_stampede_0013-01#2]
- The `booking-web` service emitted 28321 events with failing dependencies to `inventory-sync`, including "504 Gateway Timeout" errors. [cache_stampede_0013-02#0, cache_stampede_0013-01#2]
- The `reservations-api` service emitted 4761 events with failing dependencies to `inventory-sync`, including "context deadline exceeded" errors. [cache_stampede_0013-02#0, cache_stampede_0013-01#2]

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

- Redis memory usage on cache-redis-02 peaked at 100% (baseline 60%) starting at 2021-05-08 21:00 UTC [cache_stampede_0013-08#0].
- Redis evicted keys rate on cache-redis-02 surged to 2,200/s (baseline 0/s) starting at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0].
- Redis keyspace hit ratio on cache-redis-02 dropped to 9% (baseline 96%) starting at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0].
- CPU utilization on inventory-db-01 reached 100% (baseline 26%) starting at 2021-05-08 23:00 UTC [cache_stampede_0013-08#0].
- Critical alerts for InventorySyncErrorRateHigh were first observed at 2021-05-08 23:00 UTC [cache_stampede_0013-07#1].

## Service Dependencies and Propagation

- The booking-web service emitted 28,321 events with failing dependencies, all pointing to inventory-sync [cache_stampede_0013-02#0].
- The inventory-sync service emitted 11,135 events with failing dependencies, all pointing to inventory-db-01 [cache_stampede_0013-02#0].
- The fares-svc service emitted 97 events with failing dependencies, all pointing to fares-db [cache_stampede_0013-02#0].
- The largest latency increase was observed in the booking-web -> inventory-sync:8080 : GET /v1/inventory operation, with 28,321 failing requests [cache_stampede_0013-01#1].
- Error messages included "upstream inventory-sync: 504 Gateway Timeout" for booking-web and "pq: canceling statement due to statement timeout" for inventory-sync [cache_stampede_0013-01#2].
- Assessment: The inventory-sync service appears to be a bottleneck, propagating errors to dependent services like booking-web and reservations-api [cache_stampede_0013-02#0].
- Assessment: The booking-web service’s latency increase is a downstream symptom, not the root cause, as it depends on inventory-sync [cache_stampede_0013-01#1].

## Impact Assessment

- The primary CIA component affected was availability, as evidenced by service dependencies failing and high error volumes across multiple services [cache_stampede_0013-02#0].
- Services impacted include booking-web, inventory-sync, reservations-api, and fares-svc, with booking-web experiencing the highest error volume (28,321 events). [cache_stampede_0013-02#0, cache_stampede_0013-09#0]
- User-facing latency or errors likely occurred due to Redis cache saturation and PostgreSQL connection exhaustion, as indicated by Redis memory usage peaking at 100% and PostgreSQL reporting "too many clients" errors. [cache_stampede_0013-08#0, cache_stampede_0013-06#0]
- The scale of impact spanned approximately 6 hours, from 2021-05-08 21:00 UTC to 2021-05-09 03:00 UTC, aligning with Redis and PostgreSQL metric anomalies. [cache_stampede_0013-08#0, cache_stampede_0013-09#1]
- Assessment: The incident primarily disrupted service availability, with indirect evidence suggesting possible user-facing latency or errors due to resource exhaustion and dependency failures. [cache_stampede_0013-02#0, cache_stampede_0013-08#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is memory exhaustion on cache-redis-02, leading to Redis evictions and degraded performance, with high confidence [cache_stampede_0013-08#0].
- No evidence of TLS certificate issues (expired, expiring, or self-signed) was found in the queried data [cache_stampede_0013-10#0].
- The inventory-sync service was the top failing dependency for booking-web, indicating a propagation path [cache_stampede_0013-02#0].
- The Redis instance cache-redis-02 was the most-alerted critical instance, with alerts spanning 2021-05-08 18:00 UTC to 2021-05-09 02:00 UTC [cache_stampede_0013-09#0].
- A change (CHG-40338) involving inventory-sync cache warm-up occurred 6 hours before the earliest alert hour [cache_stampede_0013-09#0].
- No evidence of network delay, packet loss, or socket issues was established from the available artifacts.
- No error logs or telemetry gaps were explicitly identified in the evidence.

## Corrective and Preventive Actions

- Increase Redis memory limits on cache-redis-02 to prevent RedisMemoryHigh warnings and RedisCacheHitRatioLow critical alerts [cache_stampede_0013-07#0].
- Implement connection pooling or limit enforcement for PostgreSQL to mitigate PostgresTooManyConnections critical alerts [cache_stampede_0013-07#1].
- Add monitoring and alerting for inventory-sync error rates to detect failures earlier than the InventorySyncErrorRateHigh critical alerts [cache_stampede_0013-07#1].
- Review and optimize the CHG-40338 batch job (inventory-sync cache warm-up) to reduce its impact on Redis and PostgreSQL [cache_stampede_0013-09#0].
- Investigate and resolve the root cause of the TargetDown warning for ancillaries-svc to prevent service unavailability [cache_stampede_0013-07#1].

## Answers to Investigation Questions

1. cache-redis-02 [cache_stampede_0013-09#0]
2. 10.227.167.238 [cache_stampede_0013-05#0]
3. inventory-db-01 [cache_stampede_0013-06#0]
4. 2021-05-08 18:00 UTC [cache_stampede_0013-09#0]
5. Not established from the available artifacts
6. cascading failure [cache_stampede_0013-02#0]
7. availability [cache_stampede_0013-07#1]
8. booking-web; downstream symptom [cache_stampede_0013-09#0]
9. CHG-40380 [cache_stampede_0013-03#0]

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [cache_stampede_0013-01#4].
U2. Not established from the available artifacts [cache_stampede_0013-01#0].
U3. Not established from the available artifacts [cache_stampede_0013-06#0].
