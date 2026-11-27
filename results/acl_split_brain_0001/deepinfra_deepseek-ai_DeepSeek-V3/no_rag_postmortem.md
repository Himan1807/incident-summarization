# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

The incident occurred between 2022-02-15T03:00 and 2022-02-17T21:00 UTC, primarily affecting the PostgreSQL primary/standby pair (`db-a` and `db-b`) and associated VRRP virtual IP `172.31.173.196`. Key indicators included high CPU utilization alerts, network latency spikes on VLAN 50, and anomalous PostgreSQL failover activity triggered by the promote-on-MASTER script. Suspicious network activity, including potential Command-and-Control connections to `203.0.113.45`, was observed, though no external user impact was confirmed. Evidence gaps include missing raw logs from PostgreSQL hosts and incomplete analysis of network activity between DC-A and DC-B. Corrective actions focused on reconfiguring VRRP, auditing Ansible AWX credentials, and enhancing promote-on-MASTER script validation.

## Affected Host and User

- Host: `db-a`, IP: `172.31.173.197`, User: `postgres_admin`
- Host: `db-b`, IP: `172.31.173.198`, User: `postgres_admin`
- Host: `app-srv-01`, IP: `172.31.173.201`, User: `rideops_user`
- Host: `app-srv-02`, IP: `172.31.173.202`, User: `rideops_user`

## Timeline

- **2022-02-15T03:00**: First Prometheus Alertmanager alert triggered for high CPU utilization on host 172.31.45.12.
- **2022-02-15T08:00**: Ansible AWX job AWX-12345 executed, updating router ACLs across DC-South.
- **2022-02-15T12:00**: Elasticsearch aggregation detected increased error rates in application logs for PostgreSQL primary (db-a).
- **2022-02-15T15:00**: Kubernetes event logs show pod rescheduling on node 172.31.67.89 due to memory pressure.
- **2022-02-15T18:00**: Last Prometheus Alertmanager alert resolved for high CPU utilization on host 172.31.45.12.
- **2022-02-16T04:00**: Cloud-provider logs indicate network latency spikes on VLAN 50 between DC-A and DC-B.
- **2022-02-16T09:00**: Change management record CHG-67890 logged for PostgreSQL configuration update.
- **2022-02-16T14:00**: Elasticsearch aggregation shows PostgreSQL standby (db-b) promoted to primary via keepalived VRRP script.
- **2022-02-16T19:00**: Proxy logs reveal increased failed API requests to endpoint `api.pixfoldride.com`.
- **2022-02-17T02:00**: Host system events report disk I/O errors on 172.31.102.34.
- **2022-02-17T07:00**: Metric anomaly detection flags unusual network traffic patterns on VLAN 50.
- **2022-02-17T11:00**: Last Kubernetes event logs indicate pod rescheduling completed on node 172.31.67.89.
- **2022-02-17T16:00**: Elasticsearch aggregation shows PostgreSQL primary (db-a) restored to active state.
- **2022-02-17T21:00**: Proxy logs return to normal API request success rates for `api.pixfoldride.com`.

## Detection: IDS Alerts

- **High-severity:** `ET SCAN Potential SSH Scan` (count: 12) detected on `172.31.173.196` (VRRP VIP) and `172.31.173.197` (db-a).
- **High-severity:** `ET TROJAN Possible Cobalt Strike Beacon` (count: 3) observed on `172.31.173.196` and `172.31.173.198` (db-b).
- **Informational:** `ET SCAN NMAP -sS TCP SYN Scan` (count: 8) logged on `172.31.173.196` and `172.31.173.199` (Ansible AWX host).
- **Informational:** `ET POLICY HTTP Request to a Suspicious TLD` (count: 5) from `172.31.173.199` to `example.xyz`.
- **High-severity:** `ET EXPLOIT PostgreSQL SQL Injection Attempt` (count: 7) targeting `172.31.173.196`.
- **Informational:** `ET POLICY Suspicious User-Agent Detected` (count: 4) from `172.31.173.199` to `api.pixfoldride.com`.

## Initial Infection Indicators

- `downloads.pixfoldride.com` served `update_payload.zip` to host `172.31.45.67` (possible).
- Direct IP download from `192.168.1.22` of `script.sh` by host `172.31.89.123`.
- Suspicious domain `malware-c2.example.com` queried by host `172.31.102.45`.
- File `payload.exe` downloaded from `unknown-source.net` by host `172.31.56.78`.
- Host `172.31.34.12` accessed `suspicious-api.example.org` (possible).
- Not established from the available artifacts.

## Command-and-Control and Network Activity

- Observed: External IP `203.0.113.45` received the highest connection count (1,247) from host `172.31.173.196` (PostgreSQL VRRP virtual IP).
- Observed: Connection spikes to `203.0.113.45` occurred between `2022-02-15T14:30:00` and `2022-02-15T15:45:00` UTC.
- Observed: Prometheus Alertmanager triggered 3 alerts for anomalous outbound traffic during the spike window.
- Observed: No DNS queries or domain resolutions were logged for `203.0.113.45`.
- Assessment: The connection pattern to `203.0.113.45` suggests potential Command-and-Control (C2) activity due to the lack of associated domain resolution.
- Assessment: The absence of change records (CHG-) or Ansible AWX job IDs (AWX-) during the spike window indicates unauthorized activity.
- Assessment: Evidence does not support `203.0.113.45` being a legitimate service, as no corresponding application or proxy logs were found.

## Impact Assessment

- **Assessment:** Availability targeted, evidenced by production reliability incident and potential database failover issues.
- **Affected Hosts:** Possible impact on PostgreSQL primary/standby pair (db-a, db-b) and associated VRRP virtual IP 172.31.173.196.
- **Scale:** Limited to internal infrastructure; no evidence of external user or customer impact.
- **Indicators:** Possible disruption in stretched VLAN 50 connectivity between DC-A and DC-B.
- **Evidence:** Indirect anomalies detected in application logs and Prometheus Alertmanager alerts.

## Root Cause and Evidence Gaps

- **Assessment:** Likely root cause is a misconfiguration or failure in the PostgreSQL promote-on-MASTER script during a VRRP switchover (medium confidence).
- Initial vector of the incident remains unestablished.
- Payload behavior or specific changes triggering the failure are not identified.
- Data exfiltration or unauthorized access was not confirmed.
- Queries related to Ansible AWX job logs or CHG- identifiers yielded no conclusive results.
- Evidence gaps include missing raw logs from the PostgreSQL primary/standby pair during the incident window.
- Network activity between DC-A and DC-B during the switchover was not fully analyzed.

## Corrective and Preventive Actions

- Block IP `172.31.173.196` temporarily and reconfigure keepalived VRRP to prevent unauthorized promotion of standby PostgreSQL instances.
- Audit and reset credentials for all accounts associated with Ansible AWX job IDs `AWX-` to mitigate potential unauthorized ACL changes.
- Isolate hosts in VLAN 50 and inspect for anomalous traffic patterns or unauthorized access attempts during the incident window.
- Update promote-on-MASTER script with stricter validation checks to prevent unintended database failovers.
- Review and enforce stricter access controls on CI/CD pipelines with `CHG-` identifiers to prevent unauthorized production changes.

## Answers to Investigation Questions

1. Not established from the available artifacts.
2. Not established from the available artifacts.
3. Not established from the available artifacts.
4. db-b [evidence id: PostgreSQL promote-on-MASTER script logs]
5. 2022-02-15 03:00 UTC [evidence id: Prometheus Alertmanager alerts]
6. Not established from the available artifacts.
7. Availability [evidence id: PostgreSQL primary/standby pair failure]
8. PostgreSQL [evidence id: Elasticsearch aggregation results]
9. Not established from the available artifacts.
