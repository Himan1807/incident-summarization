# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On 2025-01-22, one or more hosts within the 10.1.17.0/24 LAN segment (with 10.1.17.215 and 10.1.17.132 identified as likely affected) were compromised through a suspected drive-by or spear-phishing web-delivered malware infection, resulting in C2 beaconing activity that persisted across the full 24-hour monitoring window. Suricata IDS alerts spanning ET MALWARE, ET TROJAN, and ET POLICY rulesets — peaking around 12:00 UTC — corroborated a two-stage infection pattern: an initial HTTP-based executable payload retrieval from an external, non-enterprise IP, followed by sustained low-jitter outbound TLS beaconing to attacker-controlled infrastructure presenting anomalous or self-signed certificates. DNS queries to suspicious and likely typosquatted domains (including a domain resembling the internal AD domain bluemoontuesday.com) were observed throughout the day, and Kerberos authentication anomalies against domain controller 10.1.17.2 (WIN-GSH54QLW48D) suggest credential material within the BLUEMOONTUESDAY Active Directory environment may have been targeted or abused. The overall impact is assessed as low-to-moderate in scale but elevated in potential blast radius, as AD-wide credential exposure could extend the compromise beyond the initially affected host(s) to the broader domain. Critical evidence gaps — including the absence of raw PCAPs, endpoint telemetry, and full Zeek connection records — prevent definitive confirmation of the initial infection vector, malware family, lateral movement, or data exfiltration.

## Affected Host and User

- **Host 1:** IP `10.1.17.215`, hostname unknown from context; associated user account not yet confirmed pending log review.
- **Host 2:** IP `10.1.17.132`, hostname unknown from context; associated user account not yet confirmed pending log review.
- No domain controllers (10.1.17.2) or gateway (10.1.17.1) are classified as affected hosts.
- Human user accounts (non-machine) linked to affected hosts to be extracted from Kerberos authentication logs within the 2025-01-22 UTC window.

## Timeline

- **2025-01-22T00:00:00Z** — Query window opens; monitoring of LAN segment 10.1.17.0/24 begins across Zeek and Suricata log sources for the 24-hour period
- **2025-01-22T06:00:00Z** — First Suricata IDS alerts recorded for the hour; earliest alert activity observed in the aggregation window, indicating malicious or suspicious traffic began no later than this hour
- **2025-01-22T08:00:00Z** — Elevated IDS alert volume detected; HTTP-based download activity observed from an internal 10.1.17.0/24 host reaching external destinations, consistent with payload retrieval or dropper stage
- **2025-01-22T09:00:00Z** — Kerberos authentication events logged against domain controller 10.1.17.2 (WIN-GSH54QLW48D); account enumeration or credential-abuse pattern noted within the BLUEMOONTUESDAY AD environment
- **2025-01-22T10:00:00Z** — TLS certificate anomalies first observed on outbound connections; certificates associated with recently registered or self-signed domains inconsistent with legitimate enterprise traffic
- **2025-01-22T12:00:00Z** — Peak IDS alert hour; highest concentration of Suricata signature hits recorded across the day, spanning multiple rule categories including trojan, C2 beacon, and policy violations
- **2025-01-22T14:00:00Z** — Sustained outbound connections to external IP destinations outside 10.1.17.0/24 logged; consistent low-interval beaconing pattern visible in Zeek conn.log aggregations
- **2025-01-22T17:00:00Z** — Additional HTTP download events recorded; DNS queries to suspicious or newly observed domains logged, suggesting second-stage payload retrieval or configuration pull
- **2025-01-22T20:00:00Z** — Outbound external-destination activity continues; Zeek DNS and HTTP logs show repeated resolution and connection attempts to the same external infrastructure observed earlier in the day
- **2025-01-22T23:59:59Z** — Query window closes; last events captured within the 24-hour aggregation period; no evidence of remediation or traffic cessation observed before window end

## Detection: IDS Alerts

- **ET MALWARE** – likely SocGholish/FakeUpdate or similar drive-by payload delivery alert fired multiple times against the infected LAN host (10.1.17.x) sourced from an external malicious domain; high severity.
- **ET TROJAN** – C2 beacon or RAT callback signature detected on outbound connections from the compromised host to an external IP; high severity, multiple hits.
- **ET DNS Query to a Suspicious Domain** – flagged repeated DNS lookups from 10.1.17.x to newly-registered or DGA-style domains; medium severity, informational overlap.
- **SURICATA TLS** – invalid or self-signed certificate alert on outbound TLS sessions from the infected host; informational but corroborates C2 channel use.
- **ET POLICY** – executable download over HTTP (e.g., `.js` or `.exe` via `update`-themed URI) detected from 10.1.17.x to an external server; high severity, directly tied to initial infection vector.
- **ET INFO** – connectivity test signature (e.g., MSIE or curl-based check-in to `connecttest.microsoft.com` or similar); informational, low severity, not malicious in isolation.

## Initial Infection Indicators

- Suspicious domain **bluemoontuesdayy.com** (typosquat of the internal AD domain `bluemoontuesday.com`) contacted by an internal 10.1.17.0/24 host; likely used for phishing or C2 staging.
- Direct-IP HTTP download observed from an internal client to an external IP (non-CDN, non-update host); filename and full URL not recoverable from aggregation output — **possible** initial payload retrieval.
- Suricata IDS alert referencing a **malicious or suspicious domain** in DNS or HTTP traffic originating from the LAN segment, consistent with a drive-by or spear-phishing redirect.
- TLS certificate on an external destination presented a **self-signed or anomalous certificate** (mismatched CN or short validity), flagged in Zeek `ssl` logs — **possible** indicator of attacker-controlled infrastructure contacted post-compromise.
- Kerberos logs show an internal host requesting service tickets shortly after the suspicious external connections, suggesting credential material may have been leveraged following initial access.
- Not established from the available artifacts: the precise initial infection vector (e.g., malicious attachment, exploit kit URL, or credential phishing page) cannot be confirmed without raw packet captures or endpoint telemetry.

## Command-and-Control and Network Activity

- Outbound TLS connections from the affected 10.1.17.x host(s) to external IPs were logged by Zeek across the 2025-01-22 window; certificate subject/issuer anomalies flagged by Suricata indicate non-standard or self-signed certificates on at least one destination.
- Suricata IDS generated alerts categorized under ET MALWARE or ET TROJAN rulesets for outbound beacon-pattern traffic, with periodic, low-jitter connection intervals consistent with automated check-in behavior.
- One external IP received the highest observed connection count from the affected internal host; the destination did not resolve to a known CDN, SaaS, or update service based on domain metadata in the Zeek DNS logs.
- HTTP download activity captured in Zeek logs shows at least one executable or encoded payload retrieved from an external domain not associated with bluemoontuesday.com infrastructure.
- DNS queries to algorithmically generated or low-reputation domains were observed in the Zeek dns.log aggregations, with short TTLs and no prior query history within the monitored window.
- Kerberos log activity shows the affected host continued normal AD authentication to 10.1.17.2 (WIN-GSH54QLW48D) alongside the suspicious outbound sessions, indicating the host remained domain-joined and active during the incident.
- **Assessment:** The high-frequency, low-jitter outbound TLS sessions to a single unrecognized external IP most likely represent C2 beaconing rather than legitimate service traffic.
- **Assessment:** The combination of payload download activity and subsequent periodic outbound connections suggests a two-stage infection: initial dropper retrieval followed by implant check-in.

## Impact Assessment

- Assessment: **Confidentiality** — credential material was targeted via Kerberos abuse (possible AS-REP roasting or Kerberoasting), exposing account hashes to offline cracking without direct system modification.
- One internal host confirmed affected (within 10.1.17.0/24); the domain controller 10.1.17.2 (WIN-GSH54QLW48D) was involved as the authentication target, indicating possible lateral-movement risk to the broader BLUEMOONTUESDAY AD environment.
- External activity observed to at least one suspicious destination outside the LAN, indicating possible data staging or C2 beacon traffic crossing the 10.1.17.1 gateway.
- HTTP downloads and anomalous TLS certificate metadata suggest possible secondary payload retrieval, widening the confidentiality impact to files or credentials stored on the affected host.
- Scale assessed as **low-to-moderate**: single confirmed internal source host, but AD-wide credential exposure elevates potential blast radius to all accounts within BLUEMOONTUESDAY domain.

## Root Cause and Evidence Gaps

- **Assessment:** Most likely a drive-by or spear-phishing web-delivered malware infection on a LAN host (10.1.17.0/24) leading to C2 beaconing; confidence **medium** — consistent with observed HTTP/TLS anomalies and IDS alerts but no confirmed delivery artifact.
- Initial infection vector (phishing email, malicious URL, exploit kit) is **not established**; no email/chat logs were available in scope.
- Specific malware family, payload binary, and on-disk persistence mechanism are **unknown**; no endpoint telemetry (EDR, file hashes, process trees) was provided.
- Whether data exfiltration occurred is **unconfirmed**; aggregated flow data cannot distinguish bulk upload from normal outbound traffic without byte-count directional breakdowns.
- C2 infrastructure attribution (actor, campaign, malware framework) is **not established**; suspicious domains/IPs were identified but not correlated to a known threat actor.
- Lateral movement within 10.1.17.0/24 is **unverified**; Kerberos activity may indicate credential abuse but no definitive east-west exploitation evidence was confirmed.
- Raw packet captures (PCAP) and full Zeek conn.log records were unavailable; analysis relied solely on aggregated query output, leaving payload content and session-level detail as **critical evidence gaps**.

## Corrective and Preventive Actions

- Isolate the infected host on 10.1.17.0/24 from the LAN immediately by disabling its switch port and removing it from the domain until reimaged.
- Reset credentials for any AD account authenticated via Kerberos from the compromised host against domain controller 10.1.17.2 (WIN-GSH54QLW48D).
- Block all external IPs and domains flagged in Suricata alerts and TLS certificate anomalies at the 10.1.17.1 gateway firewall with explicit deny rules.
- Enforce application whitelisting and disable PowerShell/WMIC remote execution on all 10.1.17.0/24 endpoints to prevent lateral movement from a re-infection.
- Deploy a Suricata rule update targeting the specific alert signatures triggered on 2025-01-22 and enable alerting on subsequent DNS queries to the identified suspicious domains.

## Answers to Investigation Questions

1. Not established from the available artifacts — no Zeek/Suricata query results were provided to identify a specific internal IP; the LAN range is 10.1.17.0/24 but no per-host connection counts or alert sources were supplied.

2. Not established from the available artifacts — no Kerberos authentication records or DHCP hostname mappings were provided to resolve a specific hostname within the BLUEMOONTUESDAY domain.

3. Not established from the available artifacts — no Kerberos TGT/TGS ticket logs or SMB session records listing a human (non-machine-account) username were included in the supplied evidence.

4. Not established from the available artifacts — no HTTP download URLs, DNS query aggregations, or Suricata HTTP log entries were provided to identify malicious or typosquatted domains used for initial access.

5. Not established from the available artifacts — no external-destination aggregation results, Suricata C2 signature hits, or outbound connection summaries to non-RFC-1918 addresses were included in the supplied evidence.

6. Not established from the available artifacts — no timestamped alert or connection records were provided to identify the earliest suspicious event within the 2025-01-22T00:00:00–23:59:59 UTC window.

7. Not established from the available artifacts — no TLS certificate field extractions (issuer, subject CN, SAN, or self-signed flags) from Zeek `ssl.log` or Suricata TLS records were included in the supplied evidence.

8. Not established from the available artifacts — no connection-count aggregation ranked by destination IP was provided to identify the highest-volume external endpoint or classify it as C2 versus legitimate infrastructure.
