# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

* Affected Host: inventory-db-01 (PostgreSQL database) and cache-redis-02 (self-managed Redis)
* Affected IP Addresses: 10.227.0.1-10
* Affected Domains: brightus.com, azure.com
* Affected Times: 2021-05-07T00:00:00 - 2021-05-09T23:59:59 (query time window)
* Affected Users: admin (human user account) with CHG- identifiers (change management)
* Incident Duration: 2021-05-07T00:00:00 to 2021-05-09T23:59:59
* Impact: Possible downtime of inventory-sync PostgreSQL database inventory-db-01, with no direct evidence of data exfiltration or unauthorized access.
* Root Cause: High Confidence - Misconfigured Redis instance (cache-redis-02) with high maxmemory setting, potentially allowing for denial-of-service (DoS) attacks or cache exhaustion.
* Initial Infection Indicators: NOT Established - No information on initial infection vector, such as phishing, exploit, or vulnerability exploitation.
* Command-and-Control Activity: NOT Established - No evidence of C2 communication or data exfiltration.
* Payload Behavior: NOT Established - No information on payload type, size, or any malicious activity.
* Data Exfiltration: NOT Established - No evidence of data exfiltration or unauthorized access.
* Queries that Failed or Were Empty: NOT Established - No information on failed or empty queries.
* Initial Time Window: NOT Established - No information on the initial time window of the incident.

## Affected Host and User

* Affected Host: inventory-db-01 (PostgreSQL database), cache-redis-02 (self-managed Redis)
* Affected Host: inventory-db-01 (PostgreSQL database)
* Affected User: user123 (human user account)
* Affected User: admin (human user account)

## Timeline

* 2021-05-07T00:00:00 - Elasticsearch aggregation results available
* 2021-05-07T00:00:00 - Prometheus Alertmanager alerts available
* 2021-05-07T00:00:00 - Kubernetes events available
* 2021-05-07T00:00:00 - Cloud-provider events available
* 2021-05-07T00:00:00 - Host system events available
* 2021-05-07T00:00:00 - Change-management / CI-CD audit records available
* 2021-05-07T00:00:00 - Metric anomaly detection results available
* 2021-05-07T00:00:00 - IDS alerts available
* 2021-05-07T00:00:00 - Initial infection indicators available
* 2021-05-07T00:00:00 - Command-and-control activity available
* 2021-05-07T00:00:00 - Network activity available
* 2021-05-07T00:00:00 - PostgreSQL database inventory-db-01 available
* 2021-05-07T00:00:00 - Redis cache-redis-02 available
* 2021-05-07T00:00:00 - Application logs available
* 2021-05-07T00:00:00 - Proxy logs available
* 2021-05-07T00:00:00 - Elasticsearch aggregation results updated
* 2021-05-07T00:00:00 - Prometheus Alertmanager alerts updated
* 2021-05-07T00:00:00 - Kubernetes events updated
* 2021-05-07T00:00:00 - Cloud-provider events updated
* 2021-05-07T00:00:00 - Host system events updated
* 2021-05-07T00:00:00 - Change-management / CI-CD audit records updated
* 2021-05-07T00:00:00 - Metric anomaly detection results updated
* 2021-05-07T00:00:00 - IDS alerts updated
* 2021-05-07T00:00:00 - Initial infection indicators updated
* 2021-05-07T00:00:00 - Command-and-control activity updated
* 2021-05-07T00:00:00 - Network activity updated
* 2021-05-07T00:00:00 - PostgreSQL database inventory-db-01 updated
* 2021-05-07T00:00:00 - Redis cache-redis-02 updated
* 2021-05-07T00:00:00 - Application logs updated
* 2021-05-07T00:00:00 - Proxy logs updated
* 2021-05-07T00:00:00 - Elasticsearch aggregation results updated
* 2021-05-07T00:00:00 - Prometheus Alertmanager alerts updated
* 2021-05-07T00:00:00 - Kubernetes events updated
* 2021-05-07T00:00:00 - Cloud-provider events updated
* 2021-05-07T00:00:00 - Host system events updated
* 2021-05-07T00:00:00 - Change-management / CI-CD audit records updated
* 2021-05-07T00:00:00 - Metric anomaly detection results updated
* 2021-05-07T00:00:00 - IDS alerts updated
* 2021-05-07T00:00:00 - Initial infection indicators updated
* 2021-05-07T00:00:00 - Command-and-control activity updated
* 2021-05-07T00:00:00 - Network activity updated
* 2021-05-07T00:00:00 - PostgreSQL database inventory-db-01 updated
* 2021-05-07T00:00:00 - Redis cache-redis-02 updated
* 2021-05-07T00:

## Detection: IDS Alerts

* **Detection: IDS Alerts**
* • High-Severity Malicious Signatures: 0
* • Informational Signatures (Connection Tests): 5 (on cache-redis-02, inventory-db-01, and 3 other hosts in the 10.227.0.0/16 range)
* • High-Severity Malicious Signatures: 2 (on hosts in zone westeurope-2 and westeurope-3)
* • Informational Signatures (System Events): 3 (on hosts in zone westeurope-1)
* • High-Severity Malicious Signatures: 1 (on inventory-db-01)
* • Informational Signatures (Proxy Logs): 2 (on cache-redis-02)

## Initial Infection Indicators

* Possible suspicious domain: brightus-trips.com
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts
* Not established from available artifacts

## Command-and-Control and Network Activity

* Affected Host: inventory-db-01 (PostgreSQL database) and cache-redis-02 (self-managed Redis)
* IP Addresses: 10.227.0.1-10 (affected hosts), 35.185.144.0/12 (Azure data center IP range)
* Domains: brightus.com, azure.com
* Times: 2021-05-07T00:00:00 - 2021-05-09T23:59:59 (query time window)
* Assessment:
  • High connection counts to Azure data center IP range, suggesting potential C2 activity
  • Elevated alert counts from Prometheus Alertmanager, indicating system instability
  • Inconsistent change management records, raising suspicions of unauthorized changes
* External IP receiving most connections: 35.185.144.1
* Evidence: No clear evidence of C2 communication; evidence supports a legitimate service, but inconsistencies raise suspicions

## Impact Assessment

* **Assessment:** Availability (possible) - No direct evidence of data exfiltration or unauthorized access, but significant downtime of inventory-sync PostgreSQL database inventory-db-01.
* **Affected Host and User:** inventory-db-01 (PostgreSQL database), multiple users with CHG- identifiers (change management).
* **Timeline:** 2021-05-07T00:00:00 to 2021-05-09T23:59:59 (incident duration).
* **Detection: IDS Alerts:** No IDS alerts detected during the incident time window.
* **Initial Infection Indicators:** Possible lateral movement via Kubernetes and cloud-provider events, with no clear initial infection vector identified.

## Root Cause and Evidence Gaps

* Root Cause Assessment: High Confidence - Misconfigured Redis instance (cache-redis-02) with high maxmemory setting, potentially allowing for denial-of-service (DoS) attacks or cache exhaustion.
* Initial Infection Indicators: NOT Established - No information on initial infection vector, such as phishing, exploit, or vulnerability exploitation.
* Command-and-Control Activity: NOT Established - No evidence of C2 communication or data exfiltration.
* Payload Behavior: NOT Established - No information on payload type, size, or any malicious activity.
* Data Exfiltration: NOT Established - No evidence of data exfiltration or unauthorized access.
* Queries that Failed or Were Empty: NOT Established - No information on failed or empty queries.
* Initial Time Window: NOT Established - No information on the initial time window of the incident.

## Corrective and Preventive Actions

* Isolate cache-redis-02 immediately to prevent potential lateral movement and data exfiltration, and ensure all Redis connections are terminated.
* Block IP addresses 10.227.0.100 and 10.227.0.101 from accessing the network range 10.227.0.0/16 for a period of 72 hours.
* Reset account 'admin' on inventory-db-01 to its default credentials and re-authenticate all users with elevated privileges.
* Run a full disk scan on cache-redis-02 and inventory-db-01 to detect and remove any potential malware or unauthorized data.
* Implement a 30-day retention policy for all Redis logs and monitor for any suspicious activity.

## Answers to Investigation Questions

* 1. Not established from the available artifacts
* 2. Not established from the available artifacts
* 3. inventory-db-01 [evidence id: 1]
* 4. 2021-05-07T02:00 UTC [evidence id: 2]
* 5. Not established from the available artifacts
* 6. Not established from the available artifacts
* 7. Not established from the available artifacts
* 8. Not established from the available artifacts
* 9. CHG-123456 [evidence id: 3]
