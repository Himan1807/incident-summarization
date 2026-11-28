# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* The root-cause service is inventory-sync, running on a Kubernetes pod and node in the westeurope-2 zone [cache_stampede_0013-01#4, cache_stampede_0013-02#0].
* The earliest sign of the failure was a high number of events and failing dependencies in the Elasticsearch aggregation results [cache_stampede_0013-02#0].
* The fault type is a cache-related issue, with high memory usage and evicted keys, leading to timeouts and connection resets [cache_stampede_0013-08#0, cache_stampede_0013-07#0].
* The user-facing impact is latency and errors in the booking-web service, with a high error volume and failing dependency [cache_stampede_0013-09#0, cache_stampede_0013-02#0].
* Assessment: The incident resulted in a cascading failure, with the booking-web service experiencing the most significant impact, followed by inventory-sync and other downstream services [cache_stampede_0013-09#0].

## Affected Service and Infrastructure

* The failure most likely originated in the `inventory-sync` service, as indicated by the high number of events and failing dependencies in the Elasticsearch aggregation results [cache_stampede_0013-02#0].
* The `inventory-sync` service is running on a Kubernetes pod and node that is part of the `westeurope-2` zone, as indicated by the zone information in the Kubernetes events [cache_stampede_0013-01#4].
* The `inventory-sync` service is failing to connect to the `inventory-db-01` PostgreSQL database, as indicated by the error messages and failing requests in the Elasticsearch aggregation results [cache_stampede_0013-01#1, cache_stampede_0013-01#2].
* The `inventory-db-01` PostgreSQL database is experiencing a high number of connections, exceeding its maximum capacity, as indicated by the system messages [cache_stampede_0013-06#0].

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

* The most significant metric anomalies are:
  + redis_memory_used_bytes / redis_memory_max_bytes on cache-redis-02, with a peak value of 100% and onset on 2021-05-08 21:00 UTC. [auto: cache_stampede_0013-08#0]
  + redis_evicted_keys_total rate on cache-redis-02, with a peak value of 2,200/s and onset on 2021-05-08 23:00 UTC. [auto: cache_stampede_0013-08#0]
  + redis keyspace hit ratio on cache-redis-02, with a trough value of 9% and onset on 2021-05-08 23:00 UTC. [auto: cache_stampede_0013-08#0]
  + node_cpu utilisation on inventory-db-01, with a peak value of 100% and onset on 2021-05-08 23:00 UTC. [auto: cache_stampede_0013-08#0]
* These anomalies occurred in the Redis caching tier, which is in front of the inventory-sync PostgreSQL database.
* The Redis anomalies started on 2021-05-08 21:00 UTC and recovered by 2021-05-09 03:00 UTC. [auto: cache_stampede_0013-08#0]
* The inventory-db-01 CPU anomaly started on 2021-05-08 23:00 UTC and recovered by 2021-05-09 03:00 UTC. [auto: cache_stampede_0013-08#0]
* The booking-web service experienced a high error volume, with 28321 events and 1 failing dependency, which maps to the inventory-sync service. [auto: cache_stampede_0013-09#0, cache_stampede_0013-02#0]
* The earliest metric anomaly onset was on 2021-05-08 21:00 UTC, according to [cache_stampede_0013-09#1].

## Service Dependencies and Propagation

* The largest latency increase was observed in the booking-web service, with a latency increase of 28321 events. [auto: cache_stampede_0013-02#0, cache_stampede_0013-01#3]
* Assessment: The root cause of the latency increase in booking-web is likely related to its dependency on inventory-sync, given the high volume of events and failing dependencies reported for inventory-sync.
* Assessment: The inventory-sync service is experiencing issues with its connection to inventory-db-01, as indicated by the 504 Gateway Timeout error messages and failing requests. [auto: cache_stampede_0013-01#2, cache_stampede_0013-01#0]
* Assessment: The fares-svc service is not the root cause of the latency increase, as it is not listed as a failing dependency for any of the affected services.
* The inventory-sync service is experiencing issues with its connection to inventory-db-01, which is a downstream service. [auto: cache_stampede_0013-02#0, cache_stampede_0013-01#4]
* The booking-web service is experiencing issues with its connection to inventory-sync, which is a critical dependency.
* The error messages indicate that the issues are related to timeouts and connection resets, suggesting a problem with the underlying infrastructure or configuration.

## Impact Assessment

* Assessment: Availability is the primary CIA component affected, as the incident resulted in user-facing latency and errors.
* Evidence: [cache_stampede_0013-08#0] shows metric anomalies on cache-redis-02 starting from 2021-05-08 21:00 UTC, with peak values on 2021-05-08 23:00 UTC.
* Services affected: booking-web, inventory-sync, reservations-api, and fares-svc. [auto: cache_stampede_0013-02#0]
* Scale of latency/errors: booking-web ranks #1 by error volume (28321 events, 1 failing dependency), with inventory-sync being the most-failed dependency (28321 errors). [auto: cache_stampede_0013-09#0, cache_stampede_0013-02#0]
* Not established from the available artifacts: the root cause, trigger, or impact on confidentiality or integrity.

## Root Cause and Evidence Gaps

* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No root cause, impact or trigger is stated in the evidence.
* Not established from the available artifacts: The exact nature of the service failures (e.g., which specific dependencies are failing) is not specified.
* Not established from the available artifacts: The cause of the Redis memory usage spike is not indicated.
* Not established from the available artifacts: The relationship between the Redis memory usage spike and the Redis evicted keys total rate is not clear.
* Assessment: Not established from the available artifacts: The impact of the incident on the organization's operations is not described.
* Not established from the available artifacts: The specific changes made to the inventory-sync PostgreSQL database inventory-db-01 are not detailed.

## Corrective and Preventive Actions

* The Elasticsearch aggregation results indicate that the inventory-sync service experienced a high error rate (28321 events, 1 failing dependency) and a low cache hit ratio (13 events) for the Redis cache, with the most-failed dependency being inventory-sync. [auto: cache_stampede_0013-09#0]
* The Prometheus Alertmanager alerts suggest that the inventory-sync service had a high error rate (10 events) and a high number of connections to the Postgres database (8 events), with the earliest alert hour being 2021-05-08 18:00 UTC. [auto: cache_stampede_0013-07#1]
* The Redis cache experienced a high memory usage warning (12 events) and a low cache hit ratio (13 events) during the same time period, with the earliest alert hour being 2021-05-08 21:00 UTC. [auto: cache_stampede_0013-07#0]
* The Kubernetes job failed (4 events) and the ancillaries-svc target went down (1 event) during the same time period, with the earliest alert hour being 2021-05-08 18:00 UTC. [auto: cache_stampede_0013-07#1]
* The change-management records indicate that a change (CHG-40338) was recorded 6 hours before the earliest alert hour, which may be related to the inventory-sync cache warm-up / metadata backfill. [auto: cache_stampede_0013-09#0]

## Answers to Investigation Questions

1. The hostname of the host or node where the failure originated is cache-redis-02 [cache_stampede_0013-09#0].
2. The IP address of the host or node where the failure originated is 10.227.167.238 [cache_stampede_0013-09#0].
3. Not established from the available artifacts.
4. The first signs of the failure appeared during the hour of 2021-05-08 18:00 UTC [cache_stampede_0013-09#0].
5. Not established from the available artifacts.
6. Cascading failure [cache_stampede_0013-09#0].
7. Not established from the available artifacts.
8. The service that emitted the most errors is booking-web [cache_stampede_0013-01#3].
9. The change that restored normal service is CHG-40346 | deployment | loyalty-api 11.30.1 -> 11.30.2 [cache_stampede_0013-03#0].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 3 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. The on-call engineer who acknowledged the incident is not specified in the evidence. [cache_stampede_0013-01#4]
U2. Not established from the available artifacts.
U3. The Linux kernel version ran on the node that hosted the pod of the root-cause service is not specified in the evidence. [cache_stampede_0013-05#0]
U4. The email address of the on-call engineer who acknowledged the incident is not specified in the evidence. [cache_stampede_0013-01#4]
U6. The earliest metric anomaly onset was 2021-05-08 21:00 UTC. [cache_stampede_0013-09#1]
U7. The most-failed dependency was inventory-sync with 28321 errors. [cache_stampede_0013-09#0]
U8. The hostname that maps to the most-alerted critical instance is cache-redis-02. [cache_stampede_0013-09#0]
U9. The earliest alert hour was 2021-05-08 18:00 UTC. [cache_stampede_0013-09#0]
U10. The warning/critical alerts spanned from 2021-05-08 18:00 UTC to 2021-05-09 02:00 UTC. [cache_stampede_0013-09#0]
