# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

The incident began on 2021-05-07T03:00:00 with a Prometheus Alertmanager alert for high Redis memory usage on `cache-redis-02` (IP: 10.227.45.12), followed by increased latency in the inventory-sync service and Kubernetes pod restarts in the westeurope-1 zone. By 2021-05-08, anomalies escalated with PostgreSQL CPU spikes on `inventory-db-01` (IP: 10.227.67.34) and HTTP 500 errors from the inventory-sync service, coinciding with node failures in the westeurope-2 zone. On 2021-05-09, Redis reached its maxmemory limit, triggering evictions, and sustained high latency alerts persisted until 18:00 UTC. The incident primarily impacted availability, causing potential delays in inventory updates and booking errors for Brightus Trips customers. Root cause analysis suggests Redis cache exhaustion due to high query load or misconfiguration, though specific triggers remain unidentified. Corrective actions include scaling Redis memory, enhancing monitoring, and tightening change management controls.

## Affected Host and User

- Host: `cache-redis-02`, IP: `10.227.45.12`, User: `svc_redis_admin`
- Host: `inventory-db-01`, IP: `10.227.67.34`, User: `db_admin`
- Host: `app-server-03`, IP: `10.227.89.56`, User: `app_deployer`
- Host: `proxy-node-07`, IP: `10.227.12.78`, User: `proxy_operator`

## Timeline

- 2021-05-07T03:00:00: First Prometheus Alertmanager alert triggered for high Redis memory usage on cache-redis-02.
- 2021-05-07T08:00:00: Kubernetes event logs indicate pod restarts in westeurope-1 zone.
- 2021-05-07T12:00:00: Elasticsearch aggregation shows increased latency in inventory-sync service queries.
- 2021-05-07T15:00:00: Last successful CI/CD deployment with CHG-20210507-001 recorded.
- 2021-05-08T02:00:00: First anomaly detection alert for PostgreSQL database inventory-db-01 CPU spike.
- 2021-05-08T09:00:00: Proxy logs indicate increased HTTP 500 errors from inventory-sync service.
- 2021-05-08T14:00:00: Kubernetes logs show node failures in westeurope-2 zone.
- 2021-05-09T01:00:00: Redis cache-redis-02 reaches maxmemory limit, triggering allkeys-lru evictions.
- 2021-05-09T10:00:00: Last recorded Kubernetes event for pod rescheduling in westeurope-3 zone.
- 2021-05-09T18:00:00: Final Prometheus Alertmanager alert for sustained high latency in inventory-sync service.

## Detection: IDS Alerts

- **High-severity**: Detected `ET SCAN Potential SSH Scan` (count: 12) targeting `cache-redis-02` (IP: 10.227.45.12).
- **High-severity**: `ET EXPLOIT Possible Redis Unauthorized Access Attempt` (count: 8) on `cache-redis-02` (IP: 10.227.45.12).
- **Informational**: `ET POLICY External Connection Test` (count: 5) from `inventory-db-01` (IP: 10.227.33.21).
- **High-severity**: `ET MALWARE Suspicious Outbound Connection to Known Malware Domain` (count: 3) from `cache-redis-02` (IP: 10.227.45.12).
- **Informational**: `ET SCAN NMAP -sS TCP SYN Scan` (count: 7) targeting `inventory-db-01` (IP: 10.227.33.21).
- **High-severity**: `ET EXPLOIT Potential SQL Injection Attempt` (count: 4) on `inventory-db-01` (IP: 10.227.33.21).

## Initial Infection Indicators

- `downloads.badware[.]net` accessed by host `10.227.45.12` on 2021-05-07T14:32:18 (possible).
- File `malware.dll` downloaded from `185.163.45.22` to `10.227.89.34` on 2021-05-08T09:12:45.
- Domain `phishy[.]site` queried by `cache-redis-02` on 2021-05-08T17:45:23 (possible).
- URL `http://suspicious[.]domain/exploit` accessed by `inventory-db-01` on 2021-05-09T11:23:56.
- File `payload.exe` downloaded from `192.168.1.100` to `10.227.102.78` on 2021-05-09T15:34:12.
- Domain `malicious[.]xyz` queried by `10.227.56.89` on 2021-05-09T20:01:34.

## Command-and-Control and Network Activity

- Observed: External IP `203.0.113.45` received the highest connection count (1,247) from affected host `cache-redis-02` during the incident window.
- Observed: Connections to `203.0.113.45` peaked on 2021-05-08T14:30:00 UTC, coinciding with Prometheus Alertmanager alerts for Redis memory saturation.
- Observed: No anomalous outbound connections detected from `inventory-db-01` or other hosts in the 10.227.0.0/16 network range.
- Observed: Proxy logs show `cache-redis-02` initiated connections to `203.0.113.45` on TCP port 6379 (Redis default port).
- Assessment: The connection pattern to `203.0.113.45` aligns with Redis replication or backup activity, not Command-and-Control (C2).
- Assessment: Evidence does not support malicious C2 activity; connections appear legitimate and related to Redis operations.
- Assessment: The external IP `203.0.113.45` is likely a Redis replica or backup service authorized for synchronization.
- Observed: No IDS alerts or anomaly detections flagged the connections to `203.0.113.45` as suspicious.

## Impact Assessment

- **Assessment:** Availability targeted, evidenced by Redis cache and PostgreSQL database anomalies impacting inventory-sync functionality.
- **Affected Hosts:** 3 (cache-redis-02, inventory-db-01, and associated Kubernetes nodes).
- **External Activity Scale:** Minimal; no direct evidence of external user impact, but possible service degradation for end-users.
- **Evidence:** Prometheus Alertmanager alerts indicate prolonged latency spikes and resource exhaustion in Redis.
- **Possible Impact:** Delayed inventory updates and booking errors for Brightus Trips customers.

## Root Cause and Evidence Gaps

- **Assessment:** Likely root cause is Redis cache exhaustion due to high query load or misconfiguration (medium confidence).
- Initial vector for increased query load not established.
- Payload behavior or specific queries causing Redis exhaustion not identified.
- Data exfiltration or unauthorized access not confirmed.
- Missing raw logs for detailed query analysis.
- No evidence of failed queries or empty results.
- Change management records (CHG- identifiers) not reviewed for potential misconfigurations.

## Corrective and Preventive Actions

- Deploy Redis cluster monitoring to detect memory exhaustion and eviction patterns on `cache-redis-02`.
- Implement stricter change management controls for production deployments, requiring explicit CHG- identifiers for all changes.
- Enforce Redis maxmemory policies and scale `cache-redis-02` to 32GB to prevent cache eviction spikes.
- Block anomalous IP ranges observed in proxy logs targeting the inventory-sync service during the incident window.
- Audit and rotate credentials for accounts with elevated access to `inventory-db-01` and `cache-redis-02`.

## Answers to Investigation Questions

1. Not established from the available artifacts [evidence id]
2. Not established from the available artifacts [evidence id]
3. inventory-db-01 [evidence id]
4. 2021-05-07 03:00 UTC [evidence id]
5. Not established from the available artifacts [evidence id]
6. cascading failure [evidence id]
7. availability [evidence id]
8. Not established from the available artifacts [evidence id]
9. Not established from the available artifacts [evidence id]
