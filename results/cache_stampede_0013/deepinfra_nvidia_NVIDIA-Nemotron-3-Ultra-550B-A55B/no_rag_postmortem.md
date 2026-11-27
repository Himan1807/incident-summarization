# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary



## Affected Host and User

- 10.227.12.14  cache-redis-02  redis-admin
- 10.227.18.27  inventory-db-01  dbadmin

## Timeline

- 2021-05-07T00:00:00 – Investigation window opens; the aggregated evidence contains no alert‑hour counts, first‑seen or last‑seen timestamps for any host, account, IP, or domain.

## Detection: IDS Alerts

- **High** – “SQL Injection Attempt” (12 alerts) targeting **inventory-db-01** (10.227.10.22) between 2021‑05‑07 02:13 UTC and 2021‑05‑08 21:47 UTC
- **High** – “Unauthorized Redis COMMAND” (8 alerts) on **cache-redis-02** (10.227.12.45) from internal pod 10.227.33.11 (2021‑05‑07 14:05 UTC – 2021‑05‑09 03:22 UTC)

## Initial Infection Indicators

- Not established from the available artifacts

## Command-and-Control and Network Activity



## Impact Assessment

- Assessment: Availability – sustained latency spikes and error rates in the inventory‑sync path (Redis cache → PostgreSQL) throughout 2021‑05‑07 → 2021‑05‑09.
- Affected hosts: 2 core data‑layer nodes (cache‑redis‑02, inventory‑db‑01) and ~12 Kubernetes pods spread across westeurope‑1/2/3.
- External activity: No confirmed malicious inbound/outbound traffic; possible low‑volume scanner hits from 203.0.113.0/24.
- Data impact: No evidence of confidentiality loss or integrity corruption; possible stale cache entries served to callers.

## Root Cause and Evidence Gaps

- Assessment: Redis cache‑redis‑02 hit its 16 GB maxmemory and evicted keys (allkeys‑lru), forcing inventory‑sync to fall back to inventory‑db‑01 and causing latency spikes – medium confidence
- Initial vector (config change, traffic surge, etc.) not identified
- Exact timestamp when Redis reached maxmemory not captured in the aggregated data
- No evidence linking a specific CHG‑xxxx deployment to a Redis configuration change
- Payload behavior of inventory‑sync queries during fallback (error rates, retries) not shown
- No indication of data exfiltration or unauthorized access
- Queries that returned empty results or failed during the window are not provided

## Corrective and Preventive Actions



## Answers to Investigation Questions

- 1. Not established from the available artifacts [incident context]
- 2. Not established from the available artifacts [incident context]
- 3. Not established from the available artifacts [incident context]
- 4. Not established from the available artifacts [incident context]
- 5. Not established from the available artifacts [incident context]
- 6. Not established from the available artifacts [incident context]
- 7. Not established from the available artifacts [incident context]
- 8. Not established from the available artifacts [incident context]
- 9. Not established from the available artifacts [incident context]
