# Incident Postmortem: Infrastructure reliability incident investigation

## Incident Summary

* Affected host: cf-node-03, cf-node-07, cf-node-11, vault-01, with high event counts indicating potential impact on the Kubernetes cluster [cert_expiry_mtls-05#0]
* Earliest alert hour: 2024-09-30 12:00 UTC, with a high volume of error messages and metric anomalies [cert_expiry_mtls-07#5, cert_expiry_mtls-10#0]
* Main C2 candidate: The external IP 10.44.1.13, with a high volume of connections from the affected hosts, suggesting potential C2 activity [cert_expiry_mtls-05#0]
* Key assessment: The incident appears to have impacted the availability of the production environment, with potential service disruptions and increased error volumes, and the root cause is likely related to the expired CA certificate and the istiod failed to sign CSR [cert_expiry_mtls-09#0, cert_expiry_mtls-05#0]

## Affected Host and User

* hosts: cf-node-03 — 110 events; ip: 10.44.1.13; role: k8s-worker; zone: rack F2 [cert_expiry_mtls-05#0]
* hosts: cf-node-07 — 104 events; ip: 10.44.1.17; role: k8s-worker; zone: rack F2 [cert_expiry_mtls-05#0]
* hosts: cf-node-11 — 99 events; ip: 10.44.2.21; role: k8s-worker; zone: rack F3 [cert_expiry_mtls-05#0]
* hosts: vault-01 — 38 events; ip: 10.44.9.10; role: vault; zone: rack F1 [cert_expiry_mtls-05#0]

## Timeline

- 2024-09-29 00:00 UTC — alert timeline: 1 events; earliest alert hour [cert_expiry_mtls-07#3, cert_expiry_mtls-10#0]
- 2024-09-29 06:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#4]
- 2024-09-29 09:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#4]
- 2024-09-29 12:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#4]
- 2024-09-29 15:20 UTC — changes: CHG-5598 | deployment | rate-engine 4.4.0 -> 4.4.1 | actor: argocd | 2024-09-29 15:20 UTC | status: Synced/Healthy | fuel surcharge table — 1 events [cert_expiry_mtls-03#0]
- 2024-09-29 18:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#4]
- 2024-09-30 00:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#5]
- 2024-09-30 06:00 UTC — alert timeline: 1 events [cert_expiry_mtls-07#5]
- 2024-09-30 10:30 UTC — changes: CHG-5602 | deployment | tracking-api 6.0.2 -> 6.1.0 | actor: argocd | 2024-09-30 10:30 UTC | status: Synced/Healthy | ETA model v3 — 1 events [cert_expiry_mtls-03#0]
- 2024-09-30 12:00 UTC — error messages: x509: certificate has expired or is not yet valid: current time is after 2024-09-30T12:00:00Z — 42847 events; alert timeline: 15 events; metric anomalies: istio_requests_total{response_code=503} rate on mesh — baseline ~1/s; peak 780/s; onset 2024-09-30 12:00 UTC; recovered 2024-09-30 13:00 UTC; metric anomalies: certmanager_certificate_expiration_timestamp_seconds - time() on istio-system/cf-mesh-intermediate — baseline > 30 days; trough 0 (expired); onset 2024-09-30 12:00 UTC; recovered 2024-09-30 13:00 UTC; expired certificates > certificate details: CN=cf-mesh-intermediate,O=Calderon Freight | issuer: CN=cf-root-ca,O=Calderon Freight | not_after: 2024-09-30 12:00:00 UTC | seen on: istio-system/istio-ca-secret (istiod) — 1844 events; expiring within 7 days > certificate details: CN=cf-mesh-intermediate,O=Calderon Freight | issuer: CN=cf-root-ca,O=Calderon Freight | not_after: 2024-09-30 12:00:00 UTC | seen on: istio-system/istio-ca-secret (istiod) — 3120 events; earliest metric anomaly onset 2024-09-30 12:00 UTC (istio_requests_total{response_code=503} rate on mesh) [cert_expiry_mtls-01#2, cert_expiry_mtls-07#5, cert_expiry_mtls-08#0, cert_expiry_mtls-09#0, cert_expiry_mtls-10#1]
- 2024-09-30 13:00 UTC — alert timeline: 14 events [cert_expiry_mtls-07#5]
- 2024-09-30 13:05 UTC — changes: CHG-5611 | vault_policy | policy cert-manager-pki | actor: h.mueller | 2024-09-30 13:05 UTC | status: applied | add capabilities [create, update] on pki_int/sign/mesh-intermediate — 1 events [cert_expiry_mtls-03#0]
- 2024-09-30 13:09 UTC — changes: CHG-5612 | certificate_renewal | certificate istio-system/cf-mesh-intermediate | actor: h.mueller | 2024-09-30 13:09 UTC | status: Ready | cmctl renew; new not_after 2025-09-30 13:09:41 UTC — 1 events [cert_expiry_mtls-03#0]
- 2024-09-30 13:20 UTC — changes: CHG-5613 | rollout_restart | istiod and mesh workloads | actor: h.mueller | 2024-09-30 13:20 UTC | status: completed | restart istiod and workloads to reissue workload certificates — 1 events [cert_expiry_mtls-03#1]

## Detection: IDS Alerts

* High-severity malicious signatures:
  * cert_expiry_mtls-07#1: 28 critical alerts, critical alerts > critical instances: booking-api (8 events), critical alerts > critical instances: istio-ingressgateway (8 events) [cert_expiry_mtls-07#1]
* Informational signatures:
  * cert_expiry_mtls-07#4: 4 events (alert timeline: 2024-09-29 06:00 UTC) [cert_expiry_mtls-07#4]
  * cert_expiry_mtls-07#2: 4 events (critical alerts > critical instances: mesh) [cert_expiry_mtls-07#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity

* The external IP that received the most connections from the affected host(s) is 10.44.1.13, with 110 connections. [cert_expiry_mtls-05#0]
* Not established from the available artifacts whether these connections are related to a legitimate service or a Command-and-Control (C2) activity.
* Assessment: The high volume of connections to 10.44.1.13 suggests a potential C2 activity, but the lack of additional information makes it difficult to confirm. [cert_expiry_mtls-05#0]
* The istiod logs indicate that the CA certificate expired, which may be related to the C2 activity, but the exact connection to the external IP is unclear. [cert_expiry_mtls-06#0]
* Assessment: The expired CA certificate may be a contributing factor to the C2 activity, but more evidence is needed to establish a clear connection.
* The cert-manager logs show failing requests to Vault, which may be related to the C2 activity, but the exact nature of the request is unclear. [cert_expiry_mtls-01#2]

## Impact Assessment

* Assessment: The primary CIA component targeted is availability, as the incident appears to have impacted the reliability of the production environment, leading to potential service disruptions.
* Assessment: The scale of external activity is possible, as there are indications of increased error volumes and failing dependencies on the istio-ingressgateway service, with a total of 92410 events and 2 failing dependencies. [cert_expiry_mtls-10#0, cert_expiry_mtls-02#0]
* Assessment: The number of affected hosts is possible, as multiple hosts (cf-node-03, cf-node-07, cf-node-11, vault-01) are listed with high event counts, indicating potential impact on the Kubernetes cluster. [cert_expiry_mtls-05#0]
* Assessment: The incident may have been triggered by a change management event, as changes were made to deployments and certificates, with the most recent change (CHG-5612) occurring on 2024-09-30 13:09 UTC. [cert_expiry_mtls-03#0]
* Assessment: The root cause and evidence gaps are not established from the available artifacts, and further investigation is required to determine the exact cause of the incident.

## Root Cause and Evidence Gaps

* Assessment: Low confidence, but most likely root cause: istiod failed to sign CSR due to expired CA certificate [cert_expiry_mtls-09#0].
* Not established from the available artifacts:
 + Initial vector (how the initial compromise occurred)
 + Payload behavior (what was the payload of the initial compromise)
 + Data exfiltration (if any data was exfiltrated)
 + Queries that failed or were empty (without context, it's unclear what this refers to)

## Corrective and Preventive Actions

* Isolate the host with the most-failed dependency, booking-api, and ensure it is properly patched and monitored.
* Block the IP address associated with the host cf-node-03, which has 110 events, to prevent potential lateral movement. [cert_expiry_mtls-05#0]
* Investigate and address the certificate expiration issue for the workload certificates, as indicated by the alert "CertManagerCertNotReady" with 7 events. [cert_expiry_mtls-07#0]
* Review and update the Kubernetes node configuration to ensure that the node range 10.44.0.0/16 is properly secured and monitored.
* Implement additional monitoring and alerting for the Istio MTLS handshake errors, as indicated by the alert "IstioMTLSHandshakeErrors" with 12 events. [cert_expiry_mtls-07#0]

## Answers to Investigation Questions

1. expired certificates: 1844 matching events [cert_expiry_mtls-09#0]
2. not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
6. Not established from the available artifacts
7. Not established from the available artifacts
8. istio-ingressgateway ranks #1 by error volume (92410 events, 2 failing dependencies) [cert_expiry_mtls-10#0]
9. CHG-5598 | deployment | rate-engine 4.4.0 -> 4.4.1 [cert_expiry_mtls-03#0]

---
Verification note: 12 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
