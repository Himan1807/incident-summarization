# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

- The incident began on May 7, 2021, with high CPU usage alerts on cache-redis-02 and a network traffic spike.
- A recent change (CHG-000456789) to the Redis configuration was noted, followed by a rollback.
- On May 8, cache-redis-02 showed signs of command-and-control activity, with 1,200 connections to an external IP and domain.
- The incident lasted 24 hours, causing service downtime during peak usage and potential DDoS activity.
- The root cause remains unclear, with gaps in evidence regarding the initial vector and payload behavior.

## Affected Host and User

- cache-redis-02: 10.227.1.5
- inventory-db-01: 10.227.0.10
- web-app-01: 10.227.2.3
- web-app-02: 10.227.2.4

## Timeline

- 2021-05-07T00:00:00: First alert from Prometheus Alertmanager indicating high CPU usage on cache-redis-02.
- 2021-05-07T01:00:00: Change-management record CHG-000456789 indicates a recent update to the Redis configuration.
- 2021-05-07T02:00:00: Elasticsearch aggregation shows increased query latency on the inventory-sync application.
- 2021-05-07T03:00:00: Cloud-provider events log shows a network traffic spike from 10.227.1.10 to 10.227.0.5.
- 2021-05-07T04:00:00: Kubernetes events indicate a pod restart on inventory-sync-01.
- 2021-05-08T05:00:00: Alertmanager triggers a new alert for high memory usage on cache-redis-02.
- 2021-05-08T06:00:00: Network logs show a new destination IP 10.227.1.15 communicating with cache-redis-02.
- 2021-05-08T07:00:00: Change-management record CHG-000456789 notes a rollback of the Redis configuration changes.
- 2021-05-09T08:00:00: Elasticsearch aggregation shows a decrease in query latency on the inventory-sync application.
- 2021-05-09T09:00:00: Cloud-provider events log indicates a network traffic decrease from 10.227.1.10 to 10.227.0.5.
- 2021-05-09T10:00:00: Alertmanager no longer triggers alerts for high CPU or memory usage on cache-redis-02.

## Detection: IDS Alerts

- High-severity: `Malware Command and Control Communication` - 3 alerts, involved hosts: `web-01`, `web-02`, `api-01`
- High-severity: `Unusual Network Traffic` - 2 alerts, involved hosts: `cache-redis-02`, `inventory-db-01`
- Informational: `Connection Test to Known Good IP` - 5 alerts, involved hosts: `web-01`, `web-02`, `api-01`, `cache-redis-02`, `inventory-db-01`
- Informational: `Regular Heartbeat` - 10 alerts, involved hosts: `web-01`, `web-02`, `api-01`, `cache-redis-02`, `inventory-db-01`

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity

- Affected Host: `cache-redis-02`
- IP Address: `104.47.244.123` (Assessment: Potentially C2 server)
- Domain: `update.brightus-trips.com` (Assessment: Likely C2 domain)
- Time: `2021-05-08T14:30:00` to `2021-05-08T15:30:00` (Assessment: High activity period)
- Connection Count: 1,200 connections to `104.47.244.123`
- Alert Count: 50 IDS alerts triggered
- Assessment: The external IP `104.47.244.123` is likely a Command-and-Control server.
- Assessment: The domain `update.brightus-trips.com` is likely being used for C2 communications.
- Assessment: The high connection count and alert activity suggest a significant C2 interaction.

## Impact Assessment

- Assessment: Availability
- Affected Hosts: 3 (cache-redis-02, inventory-db-01, web-app-01)
- Scale of External Activity: Possible DDoS attack based on traffic spikes
- Duration: 24 hours (May 7-8)
- Impact: Service downtime for 2 hours during peak usage

## Root Cause and Evidence Gaps

- Assessment: Low confidence
- Initial vector not established
- Payload behavior not established
- Data exfiltration not established
- Queries that failed or were empty not identified
- Specific attack vector not determined
- Exact time of initial compromise not known
- Detailed command-and-control communications not available

## Corrective and Preventive Actions

- Isolate cache-redis-02 to prevent potential lateral movement
- Reset user credentials for CHG-12345 associated with the incident
- Block IP address 192.0.2.100, identified as a source of malicious activity
- Review and update network security groups to restrict access to inventory-db-01
- Conduct a thorough audit of all recent changes with CHG- identifiers to identify any potential vulnerabilities

## Answers to Investigation Questions

- 1. Not established from the available artifacts
- 2. Not established from the available artifacts
- 3. inventory-db-01
- 4. 2021-05-07 02:00 UTC
- 5. Not established from the available artifacts
- 6. cascading failure
- 7. availability
- 8. Not established from the available artifacts
- 9. Not established from the available artifacts
