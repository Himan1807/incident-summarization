# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

Between May 7th and 9th, 2021, Brightus Trips experienced a significant reliability incident characterized by escalating query latency across its production environment. This manifested as high CPU utilization on the `inventory-db-01` host (10.227.0.105), increased pod restarts for the `inventory-sync` Kubernetes service, and elevated query latency within the Elasticsearch aggregation results. Simultaneously, the Redis cache server, `cache-redis-02` (10.227.0.112), reached its maximum memory limit, and suspicious outbound network connections were detected originating from `inventory-db-01` to Google Cloud. While the exact root cause and initial infection vector remain unclear, the incident’s timeline strongly suggests a potential compromise of the `inventory-db-01` host, leading to performance degradation and potentially impacting inventory synchronization. Further investigation is required to determine the precise nature of the attack and whether data exfiltration occurred.

## Affected Host and User

*   inventory-db-01: 10.227.0.105, inventory-db-01, dbadmin
*   cache-redis-02: 10.227.0.112, cache-redis-02, redisadmin
*   VM-WEB-01: 10.227.0.138, VM-WEB-01, webadmin
*   VM-WEB-02: 10.227.0.145, VM-WEB-02, webadmin

## Timeline

* 2021-05-07T01:15:00 - Prometheus Alertmanager: High CPU utilization detected on host inventory-db-01.
* 2021-05-07T02:30:00 - Kubernetes: Increased pod restart count for the `inventory-sync` service.
* 2021-05-07T03:45:00 - Elasticsearch Aggregation: Elevated query latency observed across multiple application logs.
* 2021-05-07T05:00:00 - Redis: Increased memory usage reported for `cache-redis-02`.
* 2021-05-07T06:15:00 - Elasticsearch Aggregation: Query latency continues to rise, impacting inventory synchronization.
* 2021-05-07T07:30:00 - Kubernetes: Elevated CPU usage for the `inventory-sync` service pods.
* 2021-05-07T08:45:00 - Prometheus Alertmanager: Multiple alerts triggered for high CPU on `inventory-db-01`.
* 2021-05-07T09:00:00 - Elasticsearch Aggregation: Query latency now consistently above 500ms.
* 2021-05-07T10:15:00 - Redis: `cache-redis-02` nearing maximum memory limit (16GB).
* 2021-05-07T11:30:00 - Kubernetes: Increased network traffic associated with the `inventory-sync` service.
* 2021-05-07T12:45:00 - Elasticsearch Aggregation: Query latency continues to increase, correlating with database access patterns.
* 2021-05-07T14:00:00 - Prometheus Alertmanager: High memory utilization detected on `inventory-db-01`.
* 2021-05-07T15:15:00 - Elasticsearch Aggregation: Significant increase in slow queries targeting the `inventory-sync` PostgreSQL database.
* 2021-05-07T16:30:00 - Kubernetes: Pods for `inventory-sync` experiencing increased latency.
* 2021-05-07T17:45:00 - Redis: `cache-redis-02` has reached its maximum memory limit.
* 2021-05-07T19:00:00 - Elasticsearch Aggregation: Query latency remains critically high.
* 2021-05-07T20:15:00 - Prometheus Alertmanager: Continued high CPU and memory alerts on `inventory-db-01`.
* 2021-05-07T21:30:00 - Kubernetes: Increased number of failed requests for the `inventory-sync` service.
* 2021-05-07T22:45:00 - Elasticsearch Aggregation: Correlation observed between slow queries and network traffic to 10.227.0.10.
* 2021-05-08T00:00:00 - Elasticsearch Aggregation: Persistent high query latency and elevated database load.
* 2021-05-08T01:15:00 - Prometheus Alertmanager: High CPU utilization on `inventory-db-01` persists.
* 2021-05-08T02:30:00 - Kubernetes: Increased pod restarts for `inventory-sync`.
* 2021-05-08T03:45:00 - Elasticsearch Aggregation: Query latency remains elevated, impacting inventory updates.

## Detection: IDS Alerts

*   AlertManager: Suspicious outbound TCP connection to 94.130.240.235 (count: 12) – Affected Host: inventory-db-01
*   IDS: Multiple failed login attempts (username: “admin”) against inventory-db-01 (count: 34)
*   Prometheus: High rate of HTTP requests to /api/v1/inventory endpoint from 10.227.0.150 (count: 87) – Affected Host: inventory-db-01
*   IDS: Detection of PowerShell script execution (signature: “psExec”) targeting inventory-db-01 (count: 2)
*   AlertManager: Unusual CPU utilization spike on inventory-db-01 (count: 1) – Affected Host: inventory-db-01
*   IDS: DNS query for known malicious domain: “evilcorp.xyz” originating from 10.227.0.150 (count: 1) – Affected Host: inventory-db-01

## Initial Infection Indicators

*   Domain: `api.brightustrips.com` - Download from client IP `10.227.0.123`
*   IP Address: 10.227.0.123 - Multiple outbound connections to `192.168.1.100` (identified as a potential internal proxy)
*   URL: `https://cache-redis-02.westeurope-1.cloudapp.azure.com/scripts/update.sh` - Executed by user account `brightus_admin`
*   File Name: `update.sh` - Downloaded from `api.brightustrips.com`
*   Possible: DNS queries for `maliciousdomain.net` observed originating from `inventory-db-01`
*   Not established from the available artifacts - Initial infection vector.

## Command-and-Control and Network Activity

*   Affected Host: inventory-db-01, IP Address: 10.227.0.123
*   Timeline: Incident occurred primarily between 2021-05-07T02:15:00 UTC and 2021-05-08T09:30:00 UTC.
*   Detection: Prometheus Alertmanager alerts triggered for high CPU utilization on inventory-db-01.
*   Initial Infection Indicators: Elevated outbound connections to 93.184.216.147 (Google Cloud).
*   Command-and-Control and Network Activity: Multiple connections observed from 10.227.0.123 to 93.184.216.147, utilizing TCP port 443.
*   Impact Assessment: Potential data exfiltration suspected due to unusual outbound traffic.
*   Root Cause and Evidence Gaps: The nature of the traffic and the destination IP remain unclear.
*   Assessment: The outbound traffic to 93.184.216.147 is likely a compromised service attempting to exfiltrate data, given the timing and destination.

## Impact Assessment

*   Assessment: Availability – prolonged query times impacting the core inventory-sync service.
*   Affected Host: inventory-db-01 (PostgreSQL database server), cache-redis-02 (Redis cache server).
*   Scale of External Activity: Possible increased network traffic originating from IP address range 10.227.0.0/16 during the incident window.
*   Number of Affected Hosts: 2 (inventory-db-01 and cache-redis-02).
*   Possible Impact: User impact likely involved delayed inventory updates and potential disruptions to the travel booking platform.

## Root Cause and Evidence Gaps

*   Affected Host: inventory-db-01 (IP: 10.227.0.123)
*   Timeline: 2021-05-07T02:17:34 UTC – 2021-05-09T23:59:59 UTC
*   Detection: Prometheus Alertmanager alert – PostgreSQL query latency spike (99th percentile > 100ms)
*   Initial Infection Indicators: No specific IDS alerts detected related to malware or known attack signatures.
*   Command-and-Control and Network Activity: No unusual outbound connections observed from inventory-db-01.
*   Impact Assessment: Slow query times impacting inventory synchronization, potentially delaying trip updates.
*   Root Cause and Evidence Gaps:  Exact database compromise vector, specific query payload, and whether data exfiltration occurred remain unknown.

## Corrective and Preventive Actions

*   Isolate host: inventory-db-01 (IP: 10.227.0.123) based on elevated Prometheus CPU usage spikes during the incident window.
*   Block outbound network traffic from IP: 10.227.0.123 to all external domains.
*   Reset user account: “trip_admin” (associated with inventory-db-01) due to unusual query activity.
*   Review CHG-20210506-001 – the recent PostgreSQL patch deployment on inventory-db-01.
*   Investigate Redis cache-redis-02 (IP: 10.227.0.145) for unusual memory usage patterns.
*   Analyze Kubernetes events for inventory-db-01 for any unauthorized pod creations or modifications.

## Answers to Investigation Questions

1. inventory-db-01 [Evidence ID: Aggregation_Results_001]
2. 10.227.0.123 [Evidence ID: Aggregation_Results_001]
3. inventory-db-01 [Evidence ID: Kubernetes_Events_002]
4. 2021-05-07 02:15 UTC [Evidence ID: Prometheus_Alertmanager_001]
5. Not established from the available artifacts [Evidence ID: Change_Management_Audit_001]
6. Cascading failure [Evidence ID: Kubernetes_Events_002, Prometheus_Alertmanager_001]
7. Availability [Evidence ID: Aggregation_Results_001]
8. Inventory Sync Service [Evidence ID: Aggregation_Results_001] - downstream symptom
9. CHG-20210507-001 [Evidence ID: Change_Management_Audit_001]
