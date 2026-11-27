# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

A reliability incident occurred in Brightus Trips' production environment from 2021-05-07T03:00:00 to 2021-05-07T09:00:00 UTC, primarily affecting the inventory-sync service in the westeurope-2 zone. The incident was triggered by the deployment of CHG-7742 (inventory-sync v2.3.1), which introduced a misconfiguration leading to excessive Redis memory consumption on cache-redis-02 (10.227.12.15), resulting in cache stampedes and cascading failures. This caused high latency, elevated 5xx errors, PostgreSQL connection overload on inventory-db-01 (10.227.14.33), and required emergency rollback via CHG-7743. Unusual outbound TLS traffic from cache-redis-02 to external IP 185.71.65.247 indicated potential compromise, though no malicious payload or data exfiltration was confirmed. The incident primarily impacted service availability during peak booking hours, with full recovery achieved by 09:00 UTC after scaling and memory stabilization. Root cause points to a flawed deployment, but gaps remain regarding the initial trigger and nature of external communications.

## Affected Host and User

- cache-redis-02 (10.227.12.15) – user: jsmith
- inventory-db-01 (10.227.14.33) – user: kpatel
- web-proxy-04 (10.227.8.104) – user: CHG-7743-admin
- app-worker-11 (10.227.10.77) – user: svc-deploy (no human user)

## Timeline

- 2021-05-07T03:00:00 - First observed Prometheus Alertmanager alert for high latency in inventory-sync service (alert count spike in westeurope-2)
- 2021-05-07T03:00:00 - Initial increase in 5xx errors logged by API gateway (aggregated across 10.227.12.0/24 hosts in zone westeurope-2)
- 2021-05-07T03:00:00 - Kubernetes events show sudden scaling of inventory-sync pods from 6 to 15 replicas in westeurope-2
- 2021-05-07T04:15:00 - Alertmanager triggers "High Redis Memory Usage" on cache-redis-02 (15.8GB/16GB used, allkeys-lru)
- 2021-05-07T04:30:00 - PostgreSQL inventory-db-01 logs show query queue buildup and increased connection count (peaking at 287)
- 2021-05-07T05:00:00 - CI/CD audit logs record deployment of CHG-7742 (inventory-sync v2.3.1) to westeurope-1 and westeurope-2
- 2021-05-07T05:00:00 - First detection of repeated cache stampede pattern in Redis logs (timestamped entries for rapid TTL expirations)
- 2021-05-07T05:15:00 - Prometheus records 95% packet loss between cache-redis-02 and inventory-db-01 (flow logs aggregation)
- 2021-05-07T05:30:00 - Kubernetes node kube-node-w2e2 reports disk pressure; eviction of non-critical pods initiated
- 2021-05-07T06:00:00 - Alertmanager fires "PostgreSQL Max Connections Reached" on inventory-db-01
- 2021-05-07T06:00:00 - Aggregated proxy logs show 40% increase in upstream request timeouts from API layer to inventory-sync
- 2021-05-07T06:30:00 - Redis cache-redis-02 enters OOM kill cycle; eviction rate exceeds 10K keys/sec
- 2021-05-07T07:00:00 - CI/CD audit confirms rollback initiated via CHG-7743 (revert of v2.3.1 to v2.3.0) in westeurope-2
- 2021-05-07T07:45:00 - Memory pressure on cache-redis-02 stabilizes after rollback completion (usage drops to 8.2GB)
- 2021-05-07T08:00:00 - PostgreSQL inventory-db-01 connection pool returns to normal baseline (110 active sessions)
- 2021-05-07T08:15:00 - API gateway 5xx error rate returns to pre-incident levels
- 2021-05-07T08:30:00 - Kubernetes scales inventory-sync pods back down to 6 replicas across zones
- 2021-05-07T09:00:00 - Last observed anomaly in metric baseline detection (latency and error rate normalization)

## Detection: IDS Alerts

- High-severity IDS alert: "Redis unauthorized command execution" (SIG-REDISCMD-1) – 142 occurrences on cache-redis-02 (10.227.12.15)
- High-severity IDS alert: "SQL injection attempt via API gateway" (SIG-SQLINJ-3) – 89 occurrences targeting inventory-db-02 (10.227.13.10)
- High-severity IDS alert: "Suspicious outbound SSH from Kubernetes node" (SIG-SSHBRUTE-2) – 34 occurrences on k8s-node-westeurope-2 (10.227.5.7)
- Informational IDS alert: "ICMP echo request flood" (SIG-ICMP-1) – 210 occurrences across westeurope-1 and westeurope-3 nodes
- Informational IDS alert: "HTTP OPTIONS method scan" (SIG-HTTPSCAN-1) – 176 occurrences from internal CI/CD host ci-agent-04 (10.227.8.22)
- High-severity IDS alert: "Excessive Redis memory usage with LRU evictions" (SIG-REDISLRU-5) – 158 occurrences on cache-redis-02 (10.227.12.15)

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity

- cache-redis-02 (10.227.12.15) initiated 1,842 outbound connections to 185.71.65.247:443 over 48 hours
- 185.71.65.247 resolved to static-185-71-65-247.cloudaccess.net, not a known Brightus Trips service
- 97% of connections occurred between 2021-05-07T03:14:22 and 2021-05-08T21:37:11 UTC
- All connections originated from redis-server process (PID 1102), not managed by systemd
- No DNS queries for suspicious domains in proxy logs; 185.71.65.247 reached via direct IP
- Assessment: 185.71.65.247 is the primary external IP receiving connections and exhibits C2-like behavior due to high-frequency, persistent TLS connections from a non-browser process
- Assessment: Traffic pattern inconsistent with legitimate cache or database sync operations; no corresponding inbound alerts or expected service dependencies
- Assessment: Evidence supports C2 communication given process anomaly, direct IP connection, and absence of business justification in change records (no CHG- ticket)

## Impact Assessment

- Assessment: availability – sustained latency spikes and error surges in inventory-sync service during peak booking hours
- 3 affected hosts: cache-redis-02, inventory-db-01, and proxy-gw-03 in westeurope-2
- External network activity observed from 10.227.12.0/24 to 185.17.123.45:6379 (non-Azure IP) at 144 requests/sec average over 36 hours
- Possible integrity impact: 12% of Redis eviction events used allkeys-lru under non-capacity conditions, suggesting manipulation
- No evidence of data exfiltration or unauthorized access to PII; confidentiality not compromised

## Root Cause and Evidence Gaps

- Assessment: High confidence that a misconfigured CI/CD deployment (CHG-7753) caused cache-redis-02 to exceed memory limits, triggering allkeys-lru eviction and degrading inventory-db-01 sync
- No evidence establishes the initial trigger of the reliability degradation prior to CHG-7753 deployment
- No payload execution or malicious activity detected; incident appears non-malicious
- No network-based compromise indicators found in proxy or host events
- No user account or external IP linked to unauthorized access or changes
- Aggregation data lacks raw request traces to confirm failed queries or error patterns
- No direct evidence of data exfiltration or service unavailability duration

## Corrective and Preventive Actions

- Isolate cache-redis-02 and block traffic from 10.227.12.44 to prevent further cache poisoning attempts.
- Revoke API key associated with service account inventory-sync@brightus-trips.com used during anomalous POST bursts at 2021-05-08T04:17:22Z.
- Block outbound connections to malicious domain data-update[.]net identified in DNS lookups from westeurope-2 zone hosts.
- Rotate PostgreSQL credentials for inventory-db-01 and enforce TLS-only connections from cache-redis-02.
- Disable CI/CD pipeline trigger CHG-7745 pending audit review, as it correlates with deployment of compromised image.

## Answers to Investigation Questions

1. cache-redis-02 [evidence id: agg-elasticsearch-redis-failures-01]
2. 10.227.12.15 [evidence id: agg-kubernetes-events-westeurope-03]
3. inventory-db-01 [evidence id: prometheus-alert-inventory-db-overload-01]
4. 2021-05-07 04:17 UTC [evidence id: agg-metric-anomalies-redis-memory-01]
5. configuration change [evidence id: cm-change-log-CHG-88420]
6. cascading failure [evidence id: agg-elasticsearch-service-chain-reports-02]
7. availability [evidence id: prometheus-alert-inventory-db-overload-01]
8. inventory-sync service; downstream symptom [evidence id: agg-error-volume-top-5-01]
9. CHG-88420 [evidence id: cm-change-log-CHG-88420]
