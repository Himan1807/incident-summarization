# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

• Affected Host and User: The affected hosts are ancillaries-06, cache-redis-02, inventory-db-01, and ancillaries-03, with the majority of events coming from cache-redis-02 and ancillaries-06. [auto: cache_stampede_0013-05#0]
• Earliest Alert Hour: The earliest alert hour was 2021-05-08 18:00 UTC. [auto: cache_stampede_0013-09#0, cache_stampede_0013-07#5]
• Main C2 Candidate: Not established from the available artifacts. [<evidence id>]
• Key Assessment: The primary CIA component targeted is availability, as the incident resulted in a caching tier becoming unavailable, leading to potential delays in inventory-sync operations. [cache_stampede_0013-07#1, cache_stampede_0013-07#7]

## Affected Host and User

* Affected Host and User:
  • ancillaries-06: 10.227.92.243, ancillaries-svc host, westeurope-1 [auto: cache_stampede_0013-05#0]
  • cache-redis-02: 10.227.167.238, redis-cache, westeurope-2 [auto: cache_stampede_0013-09#0, cache_stampede_0013-05#0]
  • inventory-db-01: 10.227.29.156, postgres-primary, westeurope-1 [auto: cache_stampede_0013-05#0]
  • ancillaries-03: 10.227.92.233, ancillaries-svc host, westeurope-2 [auto: cache_stampede_0013-05#0]

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

* High-severity malicious signatures:
  + InventorySyncErrorRateHigh (critical) — 10 events [auto: cache_stampede_0013-07#7, cache_stampede_0013-07#1]
  + PostgresTooManyConnections (critical) — 8 events [auto: cache_stampede_0013-07#1]
  + BookingWeb5xxHigh (critical) — 11 events [auto: cache_stampede_0013-07#0]
* Informational signatures:
  + Watchdog (info) — 72 events
  + KubeJobFailed (warning) — 4 events [auto: cache_stampede_0013-07#1]
  + TargetDown (warning) — 1 events [auto: cache_stampede_0013-09#0, cache_stampede_0013-07#1]
  + RedisCacheHitRatioLow (critical) — 13 events [auto: cache_stampede_0013-09#0, cache_stampede_0013-07#0]
  + RedisMemoryHigh (warning) — 12 events [auto: cache_stampede_0013-07#0]
* Hosts involved:
  + cache-redis-02
  + inventory-db-01
  + booking-web
  + alertmanager
  + batch
  + ancillaries-svc
  + postgres

## Initial Infection Indicators

* Derived: earliest metric anomaly onset 2021-05-08 21:00 UTC (redis_memory_used_bytes / redis_memory_max_bytes on cache-redis-02) [cache_stampede_0013-09#1]
* hosts: cache-redis-02 — 184 events; ip: 10.227.167.238; role: redis-cache; zone: westeurope-2 [cache_stampede_0013-05#0]
* Derived: most-failed dependency: inventory-sync (28321 errors) [cache_stampede_0013-09#0]
* Derived: warning/critical alerts span 2021-05-08 18:00 UTC to 2021-05-09 02:00 UTC; earliest alert hour 2021-05-08 18:00 UTC (2 alerts) [cache_stampede_0013-09#0]
* services: booking-web — 28321 events; failing dependencies=1; top dependencies: inventory-sync (28321) [cache_stampede_0013-02#0]
* Derived: changes recorded from 6 hours before the earliest alert hour to its end: CHG-40338 (batch_job, inventory-sync cache warm-up / metadata backfill, azure-pipelines, 2021-05-08 17:27 UTC) [cache_stampede_0013-09#0]

## Command-and-Control and Network Activity

* The affected host(s) received a total of 198 events from the Redis cache, with the majority coming from the `ancillaries-06` host. [auto: cache_stampede_0013-05#0]
* The Redis cache received 184 events from the `cache-redis-02` host. [auto: cache_stampede_0013-05#0]
* The PostgreSQL database `inventory-db-01` received 142 events, with the majority coming from the Redis cache. [auto: cache_stampede_0013-05#0]
* The Redis cache experienced a system message indicating "sorry, too many clients already" with 8599 events, pointing to the `inventory-db-01` host. [auto: cache_stampede_0013-06#0]
* The `failing requests` metric showed 28321 events for the `booking-web` service attempting to connect to the `inventory-sync` service. [auto: cache_stampede_0013-01#3, cache_stampede_0013-01#1]
* The `error events` metric showed 44314 events, with the majority coming from status codes 504, 500, and 503. [auto: cache_stampede_0013-01#0]
* The external IP that received the most connections from the affected host(s) is 10.227.92.243, which is associated with the `ancillaries-06` host. [auto: cache_stampede_0013-05#0]
* Not established from the available artifacts whether the evidence supports a Command-and-Control (C2) activity or a legitimate service.

## Impact Assessment

* Assessment: The primary CIA component targeted is availability, as the incident resulted in a caching tier becoming unavailable, leading to potential delays in inventory-sync operations.
* Evidence: and show that the inventory-sync service experienced high error rates, while indicates a sudden increase in alerts around 01:00 UTC. [cache_stampede_0013-04#0, cache_stampede_0013-07#1, cache_stampede_0013-07#7]
* Affected Hosts: 4 hosts were affected, including ancillaries-06, cache-redis-02, inventory-db-01, and ancillaries-03. [auto: cache_stampede_0013-05#0]
* Scale of External Activity: The incident involved 198 events from ancillaries-06, 184 events from cache-redis-02, and 142 events from inventory-db-01, indicating a significant amount of activity. [auto: cache_stampede_0013-05#0]

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but possible root cause: Not established from the available artifacts.
* Initial infection indicators: Not established from the available artifacts.
* Command-and-Control and Network Activity: Not established from the available artifacts.
* Impact Assessment: Not established from the available artifacts.
* Root Cause and Evidence Gaps:
  * Not established from the available artifacts.
  * Not established from the available artifacts.
  * Not established from the available artifacts.
  * Not established from the available artifacts.
  * Not established from the available artifacts.

## Corrective and Preventive Actions

* Isolate the Redis cache server (cache-redis-02) to prevent further potential issues with its high memory usage and low cache hit ratio. [auto: cache_stampede_0013-09#0, cache_stampede_0013-05#0]
* Investigate and address the inventory-sync service's high error rate and its impact on the booking-web service, which is currently experiencing a high volume of 5xx errors. [auto: cache_stampede_0013-09#0]
* Review and update the Azure-pipelines changes recorded from 6 hours before the earliest alert hour to ensure that the recent changes (CHG-40338) are properly tested and validated. [auto: cache_stampede_0013-09#0]
* Check the Prometheus Alertmanager alerts for any potential false positives or misconfigurations that may be contributing to the high alert volume.
* Run a thorough analysis of the Kubernetes job failures to identify any potential issues with the batch service and its dependencies.

## Answers to Investigation Questions

1. The hostname of the host or node where the failure originated is cache-redis-02 [cache_stampede_0013-09#0].
2. The IP address of the host or node where the failure originated is 10.227.167.238 [cache_stampede_0013-09#0].
3. The database host that became overloaded as a consequence of the initial failure is inventory-db-01 [cache_stampede_0013-06#0].
4. The first signs of the failure appeared during the hour of 18:00 UTC on 2021-05-08 [cache_stampede_0013-09#0].
5. Not established from the available artifacts.
6. The failure is a cascading failure [cache_stampede_0013-09#0].
7. The CIA component primarily affected is availability [cache_stampede_0013-09#0].
8. The single service that emitted the most errors is booking-web, which is the root cause [cache_stampede_0013-01#3].
9. The change that restored normal service is CHG-40380, which increased the maxmemory of cache-redis-02 from 16gb to 32gb [cache_stampede_0013-03#0].

---
Verification note: 0 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
