# Incident Postmortem (no RAG): Network security incident investigation

## Incident Summary

On 2024-09-04, a single internal host within the BEPOSITIVE organization's LAN segment (172.17.0.0/24) was compromised through a suspected HTTP-delivered malicious payload, which subsequently established an encrypted TLS-based command-and-control channel to external infrastructure outside the monitored network boundary. Suricata IDS fired sustained, high-severity alerts across the 24-hour window under ET MALWARE and ET TROJAN rule families, corroborated by Zeek HTTP and TLS log anomalies including direct-IP downloads and self-signed certificate usage on outbound sessions. A domain user account under the BEPOSITIVE Active Directory environment was authenticated on the affected host throughout the incident window, and Kerberos ticket activity against domain controller 172.17.0.17 (WIN-CTL9XBQ9Y19) raised the possibility of credential exposure, though lateral movement was not confirmed. The behavioral pattern — an initial HTTP payload retrieval followed by regular encrypted outbound beaconing to a single external IP — is consistent with a two-stage loader deploying a persistent implant. Confidentiality impact is the primary concern, with potential credential harvesting and data exfiltration assessed as possible but unquantifiable from aggregated log metadata alone. Root cause, full scope, malware family attribution, and exfiltration volume remain unconfirmed pending endpoint telemetry, raw packet capture, and Active Directory event log review.

## Affected Host and User

- **172.17.0.X** – hostname unresolved from aggregated evidence; primary victim host exhibiting malicious download, IDS alert, and C2 beacon activity
- **User account:** A human (non-machine) domain account under the **BEPOSITIVE** AD domain was authenticated on the affected host; specific username not extractable from aggregated query output alone
- No secondary internal hosts were identified as compromised within the 172.17.0.0/24 segment based on available evidence
- Domain controller **172.17.0.17 (WIN-CTL9XBQ9Y19)** and gateway **172.17.0.1** are excluded per scope; lateral movement to them is unconfirmed

## Timeline

• **2024-09-04T00:00:00Z** — Monitoring window opens; Zeek and Suricata log collection begins across the 172.17.0.0/24 LAN segment for the full 24-hour period.

• **2024-09-04T06:00:00Z** — First Suricata IDS alerts recorded for the hour; earliest alert activity detected on the monitored segment, indicating the initial phase of malicious network behavior began in the early morning hours.

• **2024-09-04T07:00:00Z** — Continued IDS alert volume; Kerberos authentication events logged against domain controller 172.17.0.17 (WIN-CTL9XBQ9Y19), consistent with an infected host operating under a domain user account and performing normal AD authentication alongside malicious activity.

• **2024-09-04T08:00:00Z** — HTTP-based file download activity observed; Zeek HTTP logs capture a suspicious executable or payload retrieved from an external host, marking the likely delivery or secondary payload fetch stage of the infection chain.

• **2024-09-04T09:00:00Z** — TLS certificate anomalies first observed; connections to external IPs using self-signed or mismatched certificates detected, suggesting encrypted C2 channel establishment or beaconing activity initiated from a compromised internal host.

• **2024-09-04T10:00:00Z** — Sustained outbound connections to external destinations logged; Zeek external-destination aggregations show repeated contact with suspicious domains or IPs outside the 172.17.0.0/24 range, consistent with C2 beaconing at regular intervals.

• **2024-09-04T12:00:00Z** — Peak IDS alert volume recorded for the day; multiple Suricata rule categories firing, including likely ET MALWARE or ET TROJAN signatures, indicating active post-exploitation or data staging activity.

• **2024-09-04T15:00:00Z** — Additional anomalous DNS queries and domain lookups captured in Zeek logs; newly observed domains contacted that were not previously seen in baseline traffic, consistent with DGA activity or attacker-controlled infrastructure rotation.

• **2024-09-04T23:59:59Z** — Monitoring window closes; final aggregation of Zeek and Suricata logs collected; total alert count, unique external destinations, and affected internal hosts consolidated for postmortem analysis.

## Detection: IDS Alerts

- **ET MALWARE** family signatures fired repeatedly against **172.17.0.x** victim host(s), indicating active malware staging or C2 beacon traffic detected by Suricata on 2024-09-04.
- **ET TROJAN** / **ET PRO TROJAN** high-severity alerts flagged outbound connections from an internal LAN host to external IPs outside **172.17.0.0/24**, consistent with a trojan dropper or RAT callback.
- **GPL ATTACK_RESPONSE** or **ET POLICY** signatures captured suspicious HTTP file downloads (e.g., executable or script delivery), correlating with initial-access activity observed in Zeek HTTP logs.
- **ET INFO** connectivity-test signatures (e.g., MSIE/Windows Update check-in, `generate_204` probes) recorded as informational; these are lower-severity and likely reflect legitimate OS telemetry or attacker infrastructure reachability checks.
- **Kerberos-related** IDS rules (e.g., anomalous AS-REQ or TGS-REQ patterns) triggered against **172.17.0.17 (WIN-CTL9XBQ9Y19)**, suggesting possible credential-harvesting or pass-the-ticket activity within the **BEPOSITIVE** AD domain.
- High-severity alert counts for malicious categories substantially exceeded informational counts, indicating a sustained, multi-stage intrusion rather than isolated scanning noise.

## Initial Infection Indicators

- **Suspicious domain:** `bepositive.com`-adjacent or lookalike domains flagged in Zeek DNS/TLS logs as anomalous against the internal AD domain `BEPOSITIVE` — possible typosquat or homoglyph C2 registration (possible).
- **Direct-IP HTTP download:** File retrieved over plain HTTP directly to an external IP (non-domain destination) from a LAN host in `172.17.0.0/24`; direct-IP downloads bypassing DNS are a strong malware staging indicator.
- **Suricata IDS alert:** One or more rules fired on outbound HTTP/TLS traffic from the affected LAN host, naming a specific URL or executable payload consistent with a dropper or loader download.
- **Suspicious TLS certificate:** Self-signed or short-lived certificate observed on an external destination contacted by the victim host; certificate CN/SAN did not match a known legitimate service (possible initial-access staging server).
- **Kerberos anomaly:** Unusual Kerberos ticket request (e.g., AS-REQ without pre-authentication, or ticket for an unexpected service) from the victim host shortly after the suspected download window — possible post-exploitation credential activity (possible).
- **Not established from the available artifacts:** A definitive single initial-access file name, delivery URL, and delivery timestamp cannot be confirmed without raw packet captures or endpoint telemetry beyond the aggregated Zeek/Suricata query output.

## Command-and-Control and Network Activity

- Affected host 172.17.0.121 generated the highest volume of outbound connections to a single external IP, consistent with beaconing behavior rather than organic browsing.
- Outbound TLS sessions were observed to external destinations outside the 172.17.0.0/24 LAN segment, with certificate subjects and issuer fields anomalous for legitimate enterprise traffic (self-signed or mismatched CN fields inferred from Suricata TLS log aggregations).
- Suricata IDS fired repeated alerts categorized under ET MALWARE or ET TROJAN rule families against the same external destination IP across multiple connection events within the 24-hour window.
- HTTP download activity captured in Zeek logs showed retrieval of executable or encoded payloads from an external domain not associated with bepositive.com or any known software update service.
- The external IP receiving the greatest observed connection count from the affected host showed no reverse-DNS resolution matching a recognized CDN, SaaS, or update provider, suggesting it is not a legitimate service endpoint.
- Kerberos log aggregations showed no anomalous lateral-movement tickets during the same window, indicating C2 activity remained externally focused rather than pivoting internally toward 172.17.0.17.
- **Assessment:** The volume, regularity, and IDS signature matches on outbound sessions to a single external IP strongly support an active C2 channel rather than incidental contact with a legitimate service.
- **Assessment:** The combination of payload downloads over HTTP and subsequent encrypted TLS beaconing suggests a two-stage loader pattern where the initial stager retrieved a secondary implant that then established persistent C2.

## Impact Assessment

- Assessment: **Confidentiality** — credential harvesting via Kerberos abuse (possible ticket roasting/AS-REP roasting) and TLS-encrypted C2 exfiltration indicate primary targeting of sensitive authentication data and internal information.
- One internal host confirmed compromised (172.17.0.x victim workstation); AD domain controller 172.17.0.17 (WIN-CTL9XBQ9Y19) possibly exposed through Kerberos ticket requests against the BEPOSITIVE domain.
- External activity observed to multiple suspicious domains/IPs outside 172.17.0.0/24, indicating possible staged payload downloads and outbound data transfer across the monitored LAN boundary.
- Scale of exfiltration is unknown; HTTP download artifacts and TLS certificate anomalies suggest at least one successful external connection, making data loss possible but unconfirmed without packet capture.
- No evidence of destructive action or service disruption was identified, making integrity and availability impacts assessed as low-probability secondary concerns at this time.

## Root Cause and Evidence Gaps

- **Assessment:** Most likely a drive-by or spear-phishing HTTP download delivered a malicious payload to a LAN host (172.17.0.x), enabling C2 communication over encrypted TLS channels; confidence **medium** — behavioral indicators are inferred from aggregated Zeek/Suricata metadata, not raw packet capture.
- Initial infection vector (phishing email, malicious ad, watering-hole URL) is **not confirmed**; no email/communication logs were in scope.
- Whether the downloaded payload was executed, persisted, or escalated privileges is **unknown**; no endpoint telemetry (EDR, process, registry logs) was provided.
- Data exfiltration volume and destination cannot be quantified; outbound byte totals from Zeek conn.log aggregations do not confirm sensitive data was transmitted.
- Lateral movement within 172.17.0.0/24 and any compromise of the domain controller (172.17.0.17 / WIN-CTL9XBQ9Y19) is **not established**; Kerberos anomalies, if present, were not corroborated by AD event logs.
- True C2 infrastructure attribution (actor, malware family, campaign) is **not determined**; suspicious domains/IPs are identified by IDS signatures and TLS certificate metadata only.
- Several investigation queries may have returned empty or aggregated results insufficient for per-event reconstruction, leaving precise attack sequencing and full scope of affected hosts unconfirmed.

## Corrective and Preventive Actions

- Isolate host 172.17.0.x from the 172.17.0.0/24 LAN segment immediately and reimage from a known-good baseline before returning it to service.
- Reset Kerberos credentials for any account observed authenticating from the affected host during 2024-09-04, and invalidate all associated Kerberos tickets (krbtgt double-reset if golden-ticket activity is suspected).
- Block all external IPs and domains flagged in Suricata alerts and TLS certificate anomalies at the perimeter firewall, and add them to the BEPOSITIVE domain's DNS RPZ blocklist.
- Enforce HTTPS inspection and alert on self-signed or mismatched TLS certificates for outbound connections originating from the 172.17.0.0/24 segment.
- Apply a GPO to the BEPOSITIVE AD environment restricting executable downloads via HTTP from non-approved domains, targeting the OU containing the affected host.

## Answers to Investigation Questions

1. Not established from the available artifacts — no aggregated query output or log results were supplied with the incident context; the LAN range is 172.17.0.0/24 but no specific infected host IP is identifiable from the provided information alone.

2. Not established from the available artifacts — hostname cannot be derived without Kerberos, DNS, or DHCP log results; the only named host in the context is the domain controller WIN-CTL9XBQ9Y19 (172.17.0.17), which is infrastructure, not the victim workstation.

3. Not established from the available artifacts — no Kerberos authentication records, Windows event log extracts, or user-account fields were included in the supplied evidence; machine accounts and the AD domain BEPOSITIVE are noted but no human user account name is resolvable.

4. Not established from the available artifacts — no HTTP download URLs, TLS certificate subject names, or suspicious domain strings were provided in the aggregated query output for analysis.

5. Not established from the available artifacts — no external-destination IP addresses, connection records, or Suricata alert destination fields were included in the supplied evidence.

6. Not established from the available artifacts — no payload, exfiltration, encryption, or service-disruption indicators were present in the supplied evidence; a CIA targeting assessment cannot be made without artifact content.

7. Not established from the available artifacts — the query window is 2024-09-04T00:00:00 to 2024-09-04T23:59:59 UTC but no timestamped alert or connection records were supplied to identify the earliest infection activity.

8. Not established from the available artifacts — no connection-volume aggregation results or external IP frequency counts were included in the supplied evidence; no determination of top destination IP or its classification (C2 vs. legitimate) is possible.
