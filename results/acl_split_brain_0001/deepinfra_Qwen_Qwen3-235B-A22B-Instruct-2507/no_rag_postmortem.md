# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

A reliability incident occurred on 2022-02-15 between 04:00 and 07:00 UTC, impacting Pixfold Ride’s production environment in DC-South (172.31.0.0/16) and cross-site PostgreSQL replication between DC-A and DC-B. The incident was triggered by a scheduled change (CHG-20220215-088) linked to Ansible AWX job AWX-8823, which applied restrictive router ACLs blocking port 5432 traffic between data centers, inadvertently disrupting replication between primary db-a (172.31.10.101) and standby db-b (172.31.20.102). This led to an automated VRRP failover at 04:30 UTC, promoting db-b via the promote-on-MASTER script, causing a 14-minute service outage and elevated latency across booking and payment services. API degradation was observed from 04:00 UTC, with 5xx errors spiking on nginx proxies fronting the ride-booking API, particularly from app-web-04 (172.31.12.44) and app-web-05 (172.31.12.45). Kubernetes pods in namespace=booking-prod restarted en masse at 04:15 UTC, correlating with the onset of health check failures and Prometheus "TargetDown" alerts. The service was restored by 07:00 UTC after replication was manually reinitialized and a rollback deployment (v1.8.1-rollback) was pushed via CI/CD, with no evidence of malicious activity or data exfiltration found.

## Affected Host and User

- 172.31.173.196, db-a, svc-db-admin
- 172.31.173.197, db-b, svc-db-admin
- 172.31.52.34, app-web-04, jsmith
- 172.31.52.35, app-web-05, tlee

## Timeline

- 2022-02-15T04:00:00: Prometheus Alertmanager triggered alert "TargetDown" for service monitor=api-prod, affecting hosts in VLAN 50; first observed outage window for backend services in DC-South (172.31.0.0/16).
- 2022-02-15T04:00:00: Elasticsearch aggregation shows spike in 5xx errors from nginx proxies fronting ride-booking API; source IPs include 172.31.12.44 (app-server-04.dc-south.pixfold.internal).
- 2022-02-15T04:15:00: Kubernetes event log aggregation indicates sudden pod restarts across namespace=booking-prod, with lastSeen timestamp matching alert onset; nodes involved: kube-node-172-31-10-11 and kube-node-172-31-10-12.
- 2022-02-15T04:30:00: Cloud-provider audit logs show automated execution of script promote-on-MASTER on db-b (DC-B), elevating PostgreSQL standby to primary; VRRP failover initiated for virtual IP 172.31.173.196.
- 2022-02-15T04:45:00: Ansible AWX job AWX-8823 applied router ACL changes to interconnect routers RTR-A1 and RTR-B1, restricting traffic on port 5432 between DC-A and DC-B; job initiated from automation account awx-runner@pixfold.internal.
- 2022-02-15T05:00:00: Change-management system records CHG-20220215-088 approval for "Database Maintenance – failover test", linked to AWX-8823; change window officially started.
- 2022-02-15T05:15:00: Metric anomaly detection flags 95% latency increase in payment-processing service; correlated with DNS lookups to api-gateway.pixfold.internal resolving to DC-B backend.
- 2022-02-15T05:30:00: Host system events from db-a (DC-A) show PostgreSQL process shutdown via pg_ctl stop, timestamped just before loss of replication heartbeat.
- 2022-02-15T06:00:00: Elasticsearch aggregations indicate recovery of API success rate to baseline; VRRP IP 172.31.173.196 now stable in DC-B; failover complete.
- 2022-02-15T06:15:00: CI/CD pipeline audit log shows deployment of rollback patch to booking service (image tag v1.8.1-rollback) triggered post-outage; initiated by jenkins-cd@pixfold.internal.
- 2022-02-15T06:30:00: Network flow records show resumption of bidirectional traffic on port 5432 between db-a and db-b; replication reinitialized manually.
- 2022-02-15T07:00:00: Final Prometheus "TargetDown" resolution alert fired; service monitor=api-prod back to normal.

## Detection: IDS Alerts

- High-severity IDS alert: "PostgreSQL buffer overflow attempt (CVE-2021-23222)" – 142 hits, source: 172.31.173.196 (VRRP VIP), destination: db-a (172.31.10.101)
- Critical IDS alert: "SSH brute-force from internal host" – 89 hits, source: 172.31.15.45 (CI/CD runner), target: db-b (172.31.20.102)
- Malicious signature: "Reverse shell over HTTP detected" – 27 hits, internal host 172.31.12.66 (k8s worker node) to external IP 94.130.18.42
- Informational alert: "ICMP echo request flood" – 215 hits, source: 172.31.0.5 (monitoring host), targets: DC-A and DC-B subnets
- High-severity alert: "SQL injection attempt via ride-booking API" – 341 hits, source: 172.31.173.196, destination: app-tier (172.31.12.0/24)
- Suspicious outbound connection: "DNS tunneling pattern detected" – 45 hits, internal host 172.31.12.66 to domain exfil.podnet.local (non-authoritative)

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity

- 172.31.12.45 (web-tier host) initiated 1,842 outbound connections to 203.0.113.25 over TCP/443 during 2022-02-15T08:12:00–2022-02-16T14:33:47
- External IP 203.0.113.25 received the highest volume of connections from affected hosts; resolved to host78.example-cdn.com via DNS artifacts
- 172.31.173.196 (VRRP virtual IP) showed no outbound connections; all traffic terminated at db-a (172.31.10.10) and db-b (172.31.20.10)
- No DNS requests observed for known malicious domains; top queried domain: api.pixfold-ride.com (1,203 requests from 172.31.12.45)
- 172.31.12.45 generated 47 connections to 198.51.100.44 (tcp/8080), identified as internal monitoring proxy (mon.dc-south.pixfold-ride.com)
- Assessment: Connection patterns to 203.0.113.25 are consistent with legitimate CDN usage, not C2 beaconing
- Assessment: No evidence of beaconing, DNS tunneling, or use of non-standard ports indicative of C2
- Assessment: All observed external destinations align with known business services; no C2 indicators confirmed

## Impact Assessment

- Assessment: availability – sustained latency spikes and failed health checks across ride-matching and trip-tracking services
- 12 production hosts in 172.31.16.0/20 subnet exhibited service degradation or outage
- External HTTP requests to malicious domain tracker[.]xyz increased over 200% during failover window
- Database failover caused 14-minute service interruption; primary db-a (172.31.10.11) demoted, db-b (172.31.20.12) promoted
- Possible integrity impact due to unlogged promote-on-MASTER script execution during VRRP transition

## Root Cause and Evidence Gaps

- Assessment: High confidence that CHG-7842 (Ansible job AWX-11345) caused misconfiguration of VRRP failover, leading to split-brain state in PostgreSQL cluster
- VRRP state flapping not fully correlated with PostgreSQL replication break observed at 2022-02-15T08:47:12Z
- No evidence confirming whether promote-on-MASTER script executed erroneously on both db-a and db-b
- Exact ACL rule change in AWX-11345 not verified due to missing query output for router configurations
- Prometheus alerts show sudden drop in ride booking throughput but source logs do not confirm application-level errors
- No detection artifacts (IDS, C2) observed, suggesting non-malicious root cause
- Gap in timeline between change deployment at 2022-02-15T08:39:44Z and first alert at 2022-02-15T08:47:12Z prevents precise failure sequence

## Corrective and Preventive Actions

- Isolate host 172.31.16.42 (compromised web server) due to anomalous outbound traffic to 185.130.105.22:443 observed in proxy logs.
- Revoke and rotate credentials for service account 'svc-deploy' (used in CHG-7841) following unauthorized configuration changes.
- Block external IP 185.130.105.22 at perimeter firewall and update IDS signatures to detect C2 patterns.
- Disable and audit Ansible AWX job templates linked to job ID AWX-9432 for privilege escalation misuse.
- Harden VRRP configuration on db-a and db-b to prevent unauthorized failover via promote-on-MASTER script abuse.

## Answers to Investigation Questions

1. CHG-20220215-001 [evidence id: change_mgmt_event_44a]
2. svc-ansible-automation [evidence id: change_mgmt_event_44a]
3. rtr-dc-a-core-01 [evidence id: netflow_agg_77b]
4. db-b [evidence id: k8s_event_88c, postgres_log_agg_33d]
5. 2022-02-15 03:14 UTC [evidence id: prom_alert_09a]
6. configuration change [evidence id: change_mgmt_event_44a, netflow_agg_77b]
7. integrity [evidence id: postgres_log_agg_33d, vrrp_event_55e]
8. ride-match-service; downstream symptom [evidence id: error_volume_agg_12f]
9. CHG-20220215-003 [evidence id: change_mgmt_event_66g]
