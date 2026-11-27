# Incident Postmortem (no RAG): Infrastructure reliability incident investigation

## Incident Summary

Between 2022-02-15 and 2022-02-17 (UTC), Pixfold Ride suffered a production availability incident affecting its ride-hailing service in DC-South when the legacy PostgreSQL primary/standby pair (db-a in DC-A, db-b in DC-B) behind keepalived VIP 172.31.173.196 underwent an unintended failover with suspected split-brain. The most probable trigger was an Ansible AWX ACL push (AWX-/CHG- change records) that disrupted VRRP traffic (IP protocol 112 / 224.0.0.18) across the DC-A/DC-B routed interconnect on stretched VLAN 50, causing the promote-on-MASTER script to promote db-b while db-a remained writable. Impact was confined to availability and potential data integrity — divergent writes on db-a and db-b during VRRP MASTER transitions — with no confidentiality impact, no external/C2 activity, and no malware or intrusion indicators identified. No specific human user account or internal host compromise was confirmed; the only implicated identities are automation (AWX jobs) and the database hosts themselves. Remediation centers on rebuilding db-b via pg_basebackup from db-a after verifying timeline/LSN divergence, replacing the promote-on-MASTER script with quorum-based fencing (Patroni/etcd or pg_auto_failover), and auditing/reverting the AWX ACL jobs with a pre-push rule blocking any ACL that denies VRRP on VLAN 50. Evidence gaps remain because the supplied artifacts are aggregated query output without raw logs, so exact failover timestamps, the specific AWX job ID, and the full count of affected application hosts in 172.31.0.0/16 could not be determined.

## Affected Host and User

- No affected internal host could be confirmed: the supplied context contains no aggregated evidence (logs, alerts, or query results) identifying a specific affected IP or hostname.
- Hosts in scope but not confirmed affected: PostgreSQL primary db-a (DC-A) and standby db-b (DC-B) behind keepalived VIP 172.31.173.196, within server range 172.31.0.0/16.
- No human user account (non-machine, not ending in $) is identifiable from the supplied artifacts; only automation identities are implied (Ansible AWX job IDs AWX-, change records CHG-).
- Per scope, domain controllers and gateways (including the DC-A/DC-B routed interconnect and VLAN 50 infrastructure) are excluded as affected hosts.

## Timeline



## Detection: IDS Alerts



## Initial Infection Indicators

- Not established from the available artifacts.
- No suspicious-domain hits, direct-IP downloads, or alert-named hosts appear in the supplied context for 2022-02-15 – 2022-02-17 (UTC).
- No file names, server IPs/domains, or client hosts (172.31.0.0/16) are flagged as delivery vectors in the aggregated evidence described.
- Context indicates an infrastructure reliability event (PostgreSQL db-a/db-b, keepalived VIP 172.31.173.196, AWX ACL pushes) rather than a malware intrusion; no initial-infection vector is identifiable.

## Command-and-Control and Network Activity



## Impact Assessment

- **Assessment:** Availability was the primary CIA component impacted — loss of the PostgreSQL VIP 172.31.173.196 and db-a/db-b failover disruption interrupted ride-hailing service in DC-South.
- **Integrity (possible):** possible split-brain writes on db-a and db-b during VRRP MASTER transitions (promote-on-MASTER script), risking divergent database state.
- **Affected hosts:** 2 database servers (db-a, DC-A; db-b, DC-B) plus dependent application hosts in 172.31.0.0/16 reaching the VIP; exact app-tier count not determinable from aggregates.
- **External activity:** none observed — no C2 domains, exfiltration, or external IPs in scope; activity confined to internal VLAN 50 interconnect and AWX/CHG change paths.
- **Scale/duration:** service degradation spanning the 2022-02-15 to 2022-02-17 UTC window; confidentiality impact assessed as none-to-minimal (no data-access evidence).

## Root Cause and Evidence Gaps

- Assessment: unintended PostgreSQL failover/split-brain — keepalived VRRP for VIP 172.31.

## Corrective and Preventive Actions

- Rebuild db-b from a fresh pg_basebackup off db-a and verify timeline/LSN divergence before rejoining it as standby behind VIP 172.31.173.196.
- Replace the keepalived promote-on-MASTER script with quorum-checked fencing (Patroni/etcd or pg_auto_failover) so a VRRP MASTER event alone cannot trigger promotion.
- Revert/audit the AWX ACL job(s) executed in the window and add a pre-push validation rule blocking any ACL that denies VRRP (IP protocol 112 / 224.0.0.18) on VLAN 50 interconnects.

## Answers to Investigation Questions


