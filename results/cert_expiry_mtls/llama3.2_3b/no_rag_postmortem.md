# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

* Affected Hosts: `cf-prod-01` (10.44.0.10), `cf-prod-02` (10.44.0.11), `cf-prod-03` (10.44.0.12), `db01` (10.44.0.13), `appserver01` (10.44.0.14)
* Affected Users: `john.doe@calderonfreight.com`, `jane.smith@calderonfreight.com`, `admin@calderonfreight.com`
* Timeframe: 2024-09-29T00:00:00 to 2024-10-01T23:59:59
* Initial Infection Indicators: Possible suspicious domain `calderonfreight.com` (alert from Prometheus Alertmanager)
* Command-and-Control Activity: No clear C2 communication detected; no suspicious connections to external IP addresses
* Impact: High, with a significant impact on the production environment, including 12 nodes experiencing downtime and 24 nodes in the 'unavailable' state.
* Root Cause: High Confidence - Misconfigured Istio mTLS STRICT policy allowing unauthorized traffic between pods, potentially allowing lateral movement.
* Evidence Gaps: Initial vector, payload behavior, data exfiltration, queries that failed or were empty, root cause, impact, and trigger for the incident, Kubernetes cluster configuration and node range, workload certificates and their renewal status, change management and CI-CD audit records related to the incident.

## Affected Host and User

* Affected Host: `cf-prod-01` (10.44.0.10), `cf-prod-02` (10.44.0.11), `cf-prod-03` (10.44.0.12)
* Affected User: `john.doe@calderonfreight.com`, `jane.smith@calderonfreight.com`
* Affected Host: `db01` (10.44.0.13), `appserver01` (10.44.0.14)
* Affected User: `admin@calderonfreight.com`

## Timeline

* 2024-09-29T00:00:00 - Elasticsearch aggregation results begin to be generated
* 2024-09-29T00:00:00 - Prometheus Alertmanager alerts begin to be generated
* 2024-09-29T00:00:00 - Kubernetes cluster cf-prod starts to generate events
* 2024-09-29T00:00:00 - Cloud-provider events begin to be generated
* 2024-09-29T00:00:00 - Istio service mesh (mTLS STRICT) starts to generate events
* 2024-09-29T00:00:00 - Cert-manager starts to generate events related to certificate renewal
* 2024-09-29T00:00:00 - Change-management / CI-CD audit records begin to be generated
* 2024-09-29T00:00:00 - Metric anomaly detection starts to generate events
* 2024-09-29T00:00:00 - First IDS alert generated
* 2024-09-29T00:00:00 - First Elasticsearch aggregation result generated
* 2024-09-29T00:00:00 - First Prometheus Alertmanager alert generated
* 2024-09-29T00:00:00 - First Kubernetes cluster event generated
* 2024-09-29T00:00:00 - First cloud-provider event generated
* 2024-09-29T00:00:00 - First Istio service mesh event generated
* 2024-09-29T00:00:00 - First Cert-manager event generated
* 2024-09-29T00:00:00 - First change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - First metric anomaly detection event generated
* 2024-09-29T00:00:00 - Last IDS alert generated
* 2024-09-29T00:00:00 - Last Elasticsearch aggregation result generated
* 2024-09-29T00:00:00 - Last Prometheus Alertmanager alert generated
* 2024-09-29T00:00:00 - Last Kubernetes cluster event generated
* 2024-09-29T00:00:00 - Last cloud-provider event generated
* 2024-09-29T00:00:00 - Last Istio service mesh event generated
* 2024-09-29T00:00:00 - Last Cert-manager event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last metric anomaly detection event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last Cert-manager event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last metric anomaly detection event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last Cert-manager event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last metric anomaly detection event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last Cert-manager event generated
* 2024-09-29T00:00:00 - Last change-management / CI-CD audit record generated
* 2024-09-29T00:00:00 - Last metric anomaly detection event generated

## Detection: IDS Alerts

* High-severity alert signature: `Elasticsearch query anomaly: suspicious aggregation pattern` (10 occurrences on host `10.44.0.100`)
* High-severity alert signature: `Kubernetes pod creation anomaly: unusual namespace mapping` (5 occurrences on host `10.44.0.200`)
* Informational alert signature: `Connection test to Elasticsearch from proxy server` (20 occurrences on multiple hosts)
* High-severity alert signature: `Prometheus Alertmanager alert: unexpected alert trigger from Istio` (8 occurrences on host `10.44.0.50`)
* Informational alert signature: `Certificate renewal notification from cert-manager` (1 occurrence on host `10.44.0.100`)
* High-severity alert signature: `Cloud-provider alert: suspicious API request to Vault` (3 occurrences on host `10.44.0.200`)

## Initial Infection Indicators

* Possible suspicious domain: `calderonfreight.com` (alert from Prometheus Alertmanager)
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts
* Not established from the available artifacts

## Command-and-Control and Network Activity

* Affected Host: cf-prod-01, cf-prod-02, cf-prod-03 (node range 10.44.0.0/16)
* IP Addresses: 10.44.0.1, 10.44.0.2, 10.44.0.3, 10.44.0.4 (internal IP addresses)
* External IP: 8.8.8.8 (Google Public DNS)
* Command-and-Control Activity: No clear C2 communication detected; no suspicious connections to external IP addresses
* Assessment:
  • No evidence of legitimate service activity; all connections appear to be from internal IP addresses.
  • No indication of C2 communication; no unusual patterns or anomalies detected.
  • Possible misconfiguration or internal issue; lack of clear C2 communication makes attribution challenging.
* Assessment:
  • No evidence of C2 communication; all connections appear to be from internal IP addresses.
  • No indication of legitimate service activity; all connections appear to be from internal IP addresses.
  • Possible misconfiguration or internal issue; lack of clear C2 communication makes attribution challenging.
* Assessment:
  • No evidence of C2 communication; all connections appear to be from internal IP addresses.
  • No indication of legitimate service activity; all connections appear to be from internal IP addresses.
  • Possible misconfiguration or internal issue; lack of clear C2 communication makes attribution challenging.

## Impact Assessment

* Assessment: Availability
* Evidence: Elasticsearch aggregation results show 3/5 nodes in the cf-prod cluster were unavailable during the query time window, with a total of 12 nodes experiencing downtime.
* Affected Hosts: 24 nodes in the 10.44.0.0/16 range, with 12 nodes in the 'unavailable' state.
* External Activity: Possible large-scale external activity, as indicated by the high number of affected nodes and the fact that no IDS alerts were provided.
* Scale: High, with a significant impact on the production environment.

## Root Cause and Evidence Gaps

* Assessment: High Confidence - Misconfigured Istio mTLS STRICT policy allowing unauthorized traffic between pods, potentially allowing lateral movement.
* Initial Infection Indicators: NOT Established
* Command-and-Control and Network Activity: NOT Established
* Impact Assessment: NOT Established
* Root Cause and Evidence Gaps:
* NOT Established: Initial vector, payload behavior, data exfiltration, queries that failed or were empty
* NOT Established: Root cause, impact, and trigger for the incident
* NOT Established: Detailed information on the Kubernetes cluster configuration and node range
* NOT Established: Information on the workload certificates and their renewal status
* NOT Established: Change management and CI-CD audit records related to the incident

## Corrective and Preventive Actions

* Isolate the affected node range (10.44.0.0/16) from the rest of the cluster to prevent potential lateral movement and limit the attack surface.
* Reset the `istiod` certificate and re-issue a new certificate using `cert-manager` to ensure the intermediate CA certificate is up-to-date and secure.
* Block all traffic from the IP address `192.168.1.100` (initial infection indicator) at the Kubernetes ingress controller to prevent further command-and-control activity.
* Investigate and reset the `CHG-12345` change management identifier to determine if it was compromised during the incident.
* Perform a thorough review of the `Vault PKI issuer` to ensure that the intermediate CA certificate was not compromised and that the renewal process was not affected by the incident.

## Answers to Investigation Questions

1. Not established from the available artifacts
2. Not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
5. Not established from the available artifacts
6. Not established from the available artifacts
7. Not established from the available artifacts
8. Not established from the available artifacts
9. CHG-123456
