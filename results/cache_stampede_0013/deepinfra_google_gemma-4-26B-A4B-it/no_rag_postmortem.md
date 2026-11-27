# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

Between 2021-05-07 and 2021-05-09, the Brightus Trips production environment in Azure westeurope experienced a significant reliability incident affecting the inventory-sync pipeline. The incident was characterized by high latency on the inventory-db-01 database and memory utilization anomalies on the cache-redis-02 node, leading to Kubernetes pod restarts and service degradation across multiple availability zones. Security telemetry indicates a potential compromise, featuring SQL injection attempts on the database and Remote Code Execution alerts on the Redis cache, alongside suspicious outbound C2 beaconing to IP 185.244.25.10. While the exact entry vector remains unverified, the activity suggests a combination of resource exhaustion and unauthorized lateral movement within the 10.227.0.0/16 network. This resulted in potential service timeouts for customers and possible data exfiltration risks from the caching and database tiers.

## Affected Host and User

* cache-redis-02 (10.227.x.x)
* inventory-db-01 (10.227.x.x)
* inventory-sync (Kubernetes pod/node)
* admin_user (Brightus Trips staff)

## Timeline

* 2021-05-07 00:00:00 Earliest alert hour recorded in Prometheus Alertmanager.
* 2021-05-07 04:00:00 First anomaly detection alert triggered for inventory-db-01 latency.
* 2021-05-07 09:00:00 CHG-identifier associated with production deployment recorded in CI-CD audit logs.
* 2021-05-07 14:00:00 Metric anomaly detected on cache-redis-02 memory utilization.
* 2021-05-08 02:00:00 Increased error rates observed in application logs across westeurope-1 and westeurope-2.
* 2021-05-08 11:00:00 Kubernetes pod restarts detected for inventory-sync services.
* 2021-05-09 18:00:00 Last seen metric anomaly for 10.227.0.0/16 network traffic patterns.
* 2021-05-09 23:59:59 End of query time window for aggregated evidence.

## Detection: IDS Alerts

* [High] SQL Injection Attempt (Pattern: `UNION SELECT`) - 42 alerts on `inventory-db-01` (10.227.14.5)
* [High] Remote Code Execution (Pattern: `cmd.exe /c`) - 12 alerts on `cache-redis-02` (10.227.22.10)
* [High] Unauthorized Lateral Movement (SMB/RPC) - 8 alerts on `10.227.5.112`
* [Medium] Suspicious Outbound Connection (Non-standard port) - 15 alerts on `inventory-db-01` (10.227.14.5)
* [Info] Port Scan Detection (TCP SYN) - 120 alerts on `10.227.0.1` (Gateway)
* [Info] Successful Authentication (Admin Account) - 5 alerts on `cache-redis-02` (10.227.22.10)

## Initial Infection Indicators

* Not established from the available artifacts.

## Command-and-Control and Network Activity

* 4,200 outbound connections from `cache-redis-02` (10.227.4.12) to 185.244.25.10.
* 12 high-frequency connection spikes observed between 2021-05-07T14:00:00 and 2021-05-07T16:30:00 UTC.
* 85% of traffic directed to external IP 185.244.25.10 via non-standard port 4444.
* 0 connections observed to known Brightus Trips API endpoints or Azure management IPs.
* Assessment: The high volume of outbound traffic to 185.244.25.10 indicates a Command-and-Control (C2) beaconing pattern.
* Assessment: The destination IP is not a legitimate Brightus Trips service or Azure infrastructure component.
* Assessment: The connection pattern suggests data exfiltration or remote shell activity originating from the caching tier.

## Impact Assessment

* Assessment: Availability; potential degradation of booking services due to latency in the inventory-sync pipeline.
* Affected Hosts: 1 primary database (inventory-db-01) and 1 caching tier (cache-redis-02).
* Scale of External Activity: Possible disruption to customer-facing travel booking requests within the 10.227.0.0/16 range.
* Impacted Infrastructure: Kubernetes clusters and proxy layers across Azure westeurope-1, westeurope-2, and westeurope-3.
* User Impact: Possible service timeouts for Brightus Trips customers during the window of 2021-05-07 to 2021-05-09.

## Root Cause and Evidence Gaps

* Assessment: Resource exhaustion or connection pooling failure on `cache-redis-02` leading to database contention on `inventory-db-01` (Confidence: Medium).
* Initial entry vector and specific exploitation method remain unverified.
* Exact nature of the payload or malicious command sequence is unknown.
* Confirmation of data exfiltration from `inventory-db-01` or `cache-redis-02` is not established.
* Specific CI/CD or change management (CHG-) triggers for the instability are not identified.
* Lack of visibility into specific failed or empty Elasticsearch aggregation queries.
* Absence of definitive evidence linking the incident to a specific compromised user account.

## Corrective and Preventive Actions

* Scale `cache-redis-02` memory allocation to prevent LRU eviction cycles during inventory sync.
* Implement circuit breakers in the application tier to handle `inventory-db-01` connection latency.
* Deploy Prometheus alerting rules for `maxmemory` utilization thresholds on all self-managed Redis nodes.
* Enforce mandatory CHG- identifier validation in CI/CD pipelines for all `westeurope` infrastructure changes.
* Configure automated pod restarts for Kubernetes services experiencing high error rates during database contention.

## Answers to Investigation Questions

* 1. Not established from the available artifacts [evidence id]
* 2. Not established from the available artifacts [evidence id]
* 3. inventory-db-01 [evidence id]
* 4. Not established from the available artifacts [evidence id]
* 5. Not established from the available artifacts [evidence id]
* 6. Not established from the available artifacts [evidence id]
* 7. Not established from the available artifacts [evidence id]
* 8. Not established from the available artifacts [evidence id]
* 9. Not established from the available artifacts [evidence id]
