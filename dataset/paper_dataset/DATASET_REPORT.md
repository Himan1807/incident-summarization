# Dataset report

Atoms = individual reference answer items (IP, host, user, domain, time, label). 'In evidence' = atom appears in the artifacts the pipeline receives; the remainder must be inferred (for example the CIA component or 'C2 server' labels) or is a reference typo.

| Scenario | Artifacts | Facts | Questions | Atoms | In evidence | Failed queries |
|---|---|---|---|---|---|---|
| apr21isc | 8 | 64 | 8 | 14 | 13 (92%) | - |
| burnincandle | 9 | 79 | 7 | 18 | 18 (100%) | suspicious_certificates |
| dec21isc | 10 | 60 | 8 | 11 | 11 (100%) | - |
| dirty_rat | 9 | 76 | 7 | 11 | 10 (90%) | - |
| easy_123 | 9 | 68 | 6 | 7 | 7 (100%) | - |
| fake_auth | 9 | 97 | 8 | 12 | 12 (100%) | - |
| gozi | 9 | 92 | 9 | 23 | 21 (91%) | - |
| iced_id | 9 | 136 | 8 | 12 | 11 (91%) | suspicious_certificates |
| jun21isc | 10 | 163 | 8 | 23 | 23 (100%) | - |
| koi_stealer | 9 | 66 | 8 | 9 | 8 (88%) | - |
| lumma_stealer | 9 | 82 | 7 | 9 | 8 (88%) | - |
| may21isc | 10 | 67 | 7 | 8 | 8 (100%) | - |
| net_rat | 9 | 75 | 7 | 9 | 9 (100%) | - |
| oct21isc | 9 | 142 | 8 | 18 | 17 (94%) | - |
| qakbot | 10 | 102 | 8 | 13 | 11 (84%) | - |
| redline_stlr | 9 | 59 | 8 | 10 | 8 (80%) | - |
| warmcookie | 9 | 85 | 7 | 11 | 10 (90%) | - |

**Total:** 205/218 atoms (94%) are present in the evidence.


# Ops / infrastructure expansion (synthetic)

20 synthetic scenarios covering non-security reliability incidents. They use the same four files per scenario, the same JSON schema, the same artifact content format (`{"description", "facts"}` aggregation strings), the same `derived_summary` and `evidence_gaps` conventions, and the same atom kinds as the paper scenarios above. 'In evidence' is computed the same way: the atom string appears (case-insensitive) in the artifacts, questions or description; labels such as the root-cause category are counted as present because the category list is in the question.

| Scenario | Artifacts | Facts | Questions | Atoms | In evidence | Failed queries |
|---|---|---|---|---|---|---|
| gw_ratelimit | 10 | 83 | 9 | 11 | 11 (100%) | - |
| coredns_forward | 10 | 81 | 10 | 13 | 13 (100%) | - |
| db_pool_config | 10 | 80 | 10 | 12 | 12 (100%) | - |
| az_ebs_degraded | 10 | 80 | 9 | 10 | 10 (100%) | - |
| objstore_503 | 10 | 72 | 8 | 9 | 9 (100%) | - |
| cloud_lb_502 | 10 | 59 | 10 | 11 | 11 (100%) | - |
| cache_stampede | 9 | 85 | 9 | 10 | 10 (100%) | change_actors |
| retry_storm | 10 | 80 | 10 | 11 | 11 (100%) | - |
| kafka_disk_full | 10 | 89 | 9 | 10 | 10 (100%) | - |
| raid_disk_failure | 10 | 80 | 9 | 10 | 10 (100%) | - |
| ecc_memory_panic | 10 | 82 | 9 | 10 | 10 (100%) | - |
| transceiver_flap | 9 | 70 | 10 | 11 | 11 (100%) | metric_anomalies |
| retention_anonymize | 10 | 83 | 9 | 10 | 10 (100%) | - |
| node_recycler_drain | 10 | 76 | 8 | 9 | 9 (100%) | - |
| ansible_acl_split_brain | 10 | 67 | 10 | 11 | 11 (100%) | - |
| dst_double_billing | 10 | 72 | 9 | 10 | 9 (90%) | - |
| cert_expiry_mtls | 10 | 79 | 9 | 10 | 10 (100%) | - |
| memleak_release | 10 | 66 | 9 | 10 | 10 (100%) | - |
| payment_provider_outage | 11 | 68 | 9 | 10 | 10 (100%) | - |
| conntrack_exhaustion | 10 | 63 | 9 | 10 | 10 (100%) | - |

**Total (expansion):** 207/208 atoms (100%) are present in the evidence.

## Scenario categories

| Scenario | Category | Incident date |
|---|---|---|
| gw_ratelimit | configuration change | 2024-03-12 |
| coredns_forward | configuration change | 2023-09-19 |
| db_pool_config | configuration change (cascading) | 2022-11-08 |
| az_ebs_degraded | cloud provider failure | 2025-02-17 |
| objstore_503 | cloud provider failure | 2026-04-22 |
| cloud_lb_502 | cloud provider failure | 2021-08-03 |
| cache_stampede | cascading failure (capacity exhaustion) | 2024-12-02 |
| retry_storm | cascading failure (software defect) | 2025-09-09 |
| kafka_disk_full | cascading failure (capacity exhaustion) | 2023-05-15 |
| raid_disk_failure | hardware failure | 2022-07-26 |
| ecc_memory_panic | hardware failure | 2026-01-13 |
| transceiver_flap | hardware failure | 2021-10-05 |
| retention_anonymize | automation error | 2024-06-18 |
| node_recycler_drain | automation error | 2025-04-08 |
| ansible_acl_split_brain | automation error | 2023-02-14 |
| dst_double_billing | automation error | 2025-11-02 |
| cert_expiry_mtls | certificate expiry | 2024-09-29 |
| memleak_release | software defect | 2026-07-07 |
| payment_provider_outage | third-party dependency failure | 2022-04-26 |
| conntrack_exhaustion | capacity exhaustion | 2023-11-24 |

## How the security schema maps to ops evidence

| Paper artifact (security) | Expansion artifact (ops) | `artifact_type` / `subtype` |
|---|---|---|
| Suricata IDS alerts (hourly timeline) | Alertmanager alerts (hourly timeline of warning + critical) | `monitoring_alerts` / `alertmanager_alerts` |
| HTTP file downloads | Application / proxy error logs | `service_logs` / `error_logs` |
| High-activity external destinations | Services ranked by error volume with failing dependencies | `service_logs` / `error_volume_by_service` |
| Kerberos services / clients | Change log and change actors (CI/CD, kubectl, automation runs) | `change_records` / `change_log`, `change_actors` |
| Kerberos hostnames | Host inventory (hostname, IP, role, zone/rack) | `infrastructure_events` / `host_inventory` |
| Suspicious domains | Kubernetes, cloud-health, kernel and hardware events | `infrastructure_events` / `platform_events` |
| (none) | Metric anomalies vs 7-day baseline | `resource_metrics` / `metric_anomalies` |
| Suspicious certificates | Expired / expiring / self-signed TLS certificates | `network_summary` / `tls_certificates` |
| Derived summary | Derived summary (error ranking, instance-to-host join, alert span, change correlation, earliest metric onset) | `derived_findings` / `derived_summary` |
| Evidence gaps | Evidence gaps (empty vs failed queries, same wording) | `query_coverage` / `evidence_gaps` |

As in the paper set, `starter_input.json` puts the alert artifact in `alerts`, every other artifact in `logs`, the incident description in `investigation_notes`, and leaves `communications` empty.

## Question set

The paper's recurring questions are mirrored for ops incidents: failure-origin host/IP (instead of infected host/IP), triggering change and executing account/automation identity (instead of user account), first-signs hour (same wording and format), root-cause category (the multiple-choice label, in place of malware family), CIA component (same wording), and "which single service emitted the most errors: root cause or downstream symptom?" (in place of "C2 server or legitimate service"). Scenario-specific questions cover the changed parameter, failed disk serial, affected availability zone, expired certificate, provider incident ID, and so on.

## Design notes

- Every scenario includes at least one red herring: an unrelated deployment just before onset, an earlier unrelated alert, a top error emitter that is only a downstream symptom, or a mitigation that did not help.
- In 6 scenarios the first signs come before the first alert (from a metric anomaly or a low-severity warning), or the earliest alert is unrelated to the incident. The `derived_summary` reports both the earliest alert hour and the earliest metric onset, so the pipeline must reason rather than copy one value.
- Two scenarios include failed queries (`cache_stampede`: change_actors; `transceiver_flap`: metric_anomalies), using the paper's wording for unavailable evidence. Two include non-empty certificate evidence (`cert_expiry_mtls` and, as a red herring, `payment_provider_outage`).
- CIA answers: availability in 17 scenarios and integrity in 3 (`retention_anonymize`, `ansible_acl_split_brain`, `dst_double_billing`).
- Root-cause categories are labelled by the defect that started the incident. "Automation error" means an automated job or controller performed the damaging action. Cascading scenarios also have a propagation question (isolated vs cascading).
- All names, IPs, change IDs and provider incident IDs are fictional. The only real ones are well-known public API hostnames used as external dependencies.
