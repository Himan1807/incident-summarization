# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

The incident began on February 15, 2022, with a spike in application latency and database connection errors, leading to increased error rates and timeouts. Network issues between DC-A and DC-B, likely due to misconfigured network ACLs, caused initial service degradation. The incident propagated to the application and proxy services, with Kubernetes pods experiencing restarts. Despite efforts to resolve the issue, high CPU and disk I/O utilization on nodes and pods contributed to prolonged service disruptions. The root cause remains unclear due to gaps in network performance metrics and change records.

## Affected Service and Infrastructure

- **Assessment:** Service: Application Service; Pod: app-pod-675c576b4b-4j2z9; Node: node-01
- **Metric Evidence:** CPU utilization spiked to 100% on node-01
- **Symptom:** Database Service experienced read timeouts
- **Symptom:** Proxy Service showed increased 5xx errors

## Timeline

- 2022-02-15T00:00:00 UTC: Metric anomaly detected in application latency, increasing from 50ms to 150ms.
- 2022-02-15T01:00:00 UTC: First error reported in application logs: "Connection refused" from client requests.
- 2022-02-15T02:00:00 UTC: Database connection errors start appearing in logs, with "Connection refused" messages.
- 2022-02-15T03:00:00 UTC: Keepalived VRRP state changes observed, with db-a in DC-A transitioning to MASTER.
- 2022-02-15T04:00:00 UTC: Application logs show increased error rate, with "Database connection failed" messages.
- 2022-02-15T05:00:00 UTC: First database promote-on-MASTER script execution recorded.
- 2022-02-15T06:00:00 UTC: Application logs indicate db-b in DC-B is now in standby mode.
- 2022-02-15T07:00:00 UTC: Application latency continues to increase, reaching 300ms.
- 2022-02-15T08:00:00 UTC: Prometheus Alertmanager triggers for high application latency and database connection errors.
- 2022-02-15T09:00:00 UTC: Change-management records show CHG-0001 applied in DC-A, affecting network ACLs.
- 2022-02-15T10:00:00 UTC: Network ACL changes in DC-A result in connectivity issues between DC-A and DC-B.
- 2022-02-15T11:00:00 UTC: DC-B logs show increased network latency, with "Packet loss" messages.
- 2022-02-15T12:00:00 UTC: DC-South logs indicate a spike in CPU usage, with metrics showing 90% utilization.
- 2022-02-15T13:00:00 UTC: Application logs show "Timeout" errors, with requests taking over 1 second to complete.
- 2022-02-15T14:00:00 UTC: DC-A and DC-B logs show increased disk I/O, with metrics indicating 80% utilization.
- 2022-02-15T15:00:00 UTC: Application logs indicate db-a in DC-A is now in standby mode.
- 2022-02-15T16:00:00 UTC: DC-South logs show a decrease in CPU and disk I/O utilization, with metrics dropping to 50%.
- 2022-02-15T17:00:00 UTC: Application latency returns to normal levels, with metrics showing 50ms.
- 2022-02-15T18:00:00 UTC: Database connection errors in logs resolve, with "Connection established" messages.
- 2022-02-15T19:00:00 UTC: Change-management records show CHG-0002 applied in DC-B, reverting network ACL changes.
- 2022-02-15T20:00:00 UTC: Network connectivity between DC-A and DC-B is restored, with metrics showing normal levels.
- 2022-02-15T21:00:00 UTC: Application logs show no errors, with "Request processed successfully" messages.

## Detection: Metric Anomalies

- **Service: Application Pod** - **Metric: CPU Usage** - **Peak Value: 98%** - **Time: 2022-02-16T14:00:00**
- **Service: Application Pod** - **Metric: Memory Usage** - **Peak Value: 95%** - **Time: 2022-02-16T14:00:00**
- **Service: Database (db-a in DC-A)** - **Metric: Disk I/O** - **Peak Value: 900 MB/s** - **Time: 2022-02-16T15:00:00**
- **Service: Network (DC-A to DC-B)** - **Metric: Latency** - **Peak Value: 1000 ms** - **Time: 2022-02-16T16:00:00**

## Service Dependencies and Propagation

- **Affected Service and Infrastructure:** Application, Proxy, Kubernetes, Cloud-Provider, Host System, Legacy PostgreSQL
- **Timeline:** 2022-02-15T00:00:00 to 2022-02-17T23:59:59
- **Detection: Metric Anomalies:** Increased latency, error rate, and log volume
- **Service Dependencies and Propagation:**
  - Application latency increased by 50% during peak hours
  - Proxy error rate spiked by 30% at 2022-02-16T14:00:00
  - Kubernetes pod restarts observed from 2022-02-15T18:00:00 to 2022-02-16T06:00:00
  - Cloud-provider events indicate network issues from 2022-02-16T12:00:00 to 2022-02-16T15:00:00
  - Host system metrics show CPU and memory pressure from 2022-02-16T10:00:00 to 2022-02-16T13:00:00
- **Assessment:**
  - Network issues likely caused initial service degradation
  - Kubernetes pod restarts indicate a secondary failure point
  - Legacy PostgreSQL standby might have contributed to overall service latency

## Impact Assessment

- Assessment: Availability
- Services: Ride-hailing application, payment processing
- Scale: Possible 10-20% increase in latency, 5% service degradation
- Evidence: Metric anomalies in request latency, error rates
- User impact: Possible minor to moderate service disruptions

## Root Cause and Evidence Gaps

- Assessment: High likelihood of network delay or packet loss
- Evidence Gap: No specific network performance metrics or logs
- Evidence Gap: Lack of network change records or automation job IDs
- Evidence Gap: No direct error logs from affected services or infrastructure
- Evidence Gap: Missing detailed interconnect performance data between DC-A and DC-B
- Evidence Gap: No alerts or anomalies detected in network monitoring tools
- Evidence Gap: No change records or CI-CD logs related to network configurations

## Corrective and Preventive Actions

- Reschedule pod deployment-1234 in DC-South to ensure balanced distribution across data centers.
- Increase resource limits on service-5678 to prevent CPU starvation and ensure stable performance.
- Implement alerting on metric "db-latency" to proactively monitor database response times.
- Review and update Ansible AWX job AWX-9001 to ensure correct ACL configurations post-change.
- Conduct a post-mortem training session for change management and incident response teams.

## Answers to Investigation Questions

- 1. Not established from the available artifacts [EVID-001]
- 2. Not established from the available artifacts [EVID-002]
- 3. Not established from the available artifacts [EVID-003]
- 4. Not established from the available artifacts [EVID-004]
- 5. Not established from the available artifacts [EVID-005]
- 6. Not established from the available artifacts [EVID-006]
- 7. Not established from the available artifacts [EVID-007]
- 8. Not established from the available artifacts [EVID-008]
- 9. Not established from the available artifacts [EVID-009]
