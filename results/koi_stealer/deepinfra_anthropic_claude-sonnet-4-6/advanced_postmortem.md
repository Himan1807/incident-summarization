# Incident Postmortem: Network security incident investigation

## Incident Summary

- On 2024-09-04, host 172.17.0.99 (DESKTOP-RNVO9AT), operated by domain user afletcher (BEPOSITIVE), was identified as the sole affected internal client, generating 361 outbound connection events to 35 distinct external destinations during the investigation window [koi_stealer-02#0, koi_stealer-08#0]
- The earliest alert activity was recorded at 2024-09-04 17:00 UTC, when 31 high-severity IDS events fired, followed by 26 further events at 18:00 UTC [koi_stealer-06#3, koi_stealer-08#0]
- The primary C2 candidate is external IP 79.124.78.197, which received 218 of the 361 total outbound connections from 172.17.0.99 and was the target of 49 high-severity Suricata alerts, including signatures for "ET MALWARE Win32/Koi Stealer CnC Checkin (GET)" and "ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound" [koi_stealer-02#0, koi_stealer-06#1, koi_stealer-06#2]
- Assessment: The combination of a confirmed C2 check-in alert, an inbound C2 configuration response, and 48 suspicious POST events to 79.124.78.197 collectively indicate active Koi Stealer command-and-control communication originating from afletcher's workstation [koi_stealer-06#2, koi_stealer-06#3]
- Assessment: Confidentiality is the primary CIA component at risk; Koi Stealer is a credential and data-harvesting family, and the confirmed C2 check-in and config-inbound signatures indicate that data was possibly exfiltrated from afletcher's account on 172.17.0.99, though successful exfiltration is not established from the available artifacts [koi_stealer-06#1, koi_stealer-06#2, koi_stealer-08#0]

## Affected Host and User

- **IP Address:** 172.17.0.99 [koi_stealer-08#0]
- **Hostname:** DESKTOP-RNVO9AT [koi_stealer-05#0]
- **Human user account:** afletcher (domain: BEPOSITIVE) [koi_stealer-03#0]
- **Scope:** Only one internal host is identified as affected; no other internal hosts appear in the evidence as clients generating alerts or anomalous traffic. [koi_stealer-08#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts

- **High-severity: ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1** fired 48 times, with 172.17.0.99 as the source in all 49 high-severity events directed toward external destination 79.124.78.197 [koi_stealer-06#2]
- **High-severity: ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound** fired 1 time, with inbound traffic recorded from 79.124.78.197 to 172.17.0.99 [koi_stealer-06#2]
- **High-severity: ET MALWARE Win32/Koi Stealer CnC Checkin (GET)** fired 1 time, sourced from 172.17.0.99 toward 79.124.78.197 [koi_stealer-06#1]
- All 50 high-severity alerts were concentrated in two one-hour windows: 31 events at 2024-09-04 17:00 UTC and 26 events at 2024-09-04 18:00 UTC [koi_stealer-06#3]
- **Informational: GPL NETBIOS SMB IPC$ unicode share access** fired 5 times and **ET INFO Microsoft Connection Test** fired 2 times; these are lower-severity signatures not directly indicative of malware activity [koi_stealer-06#0]
- Assessment: The combination of a CnC checkin alert, an inbound CnC config response, and 48 suspicious POST events to a dotted-quad IP collectively indicate active Koi Stealer command-and-control communication from host 172.17.0.99 (desktop-rnvo9at) [koi_stealer-06#2, koi_stealer-05#0]

## Initial Infection Indicators

- Host 172.17.0.99 made 48 HTTP requests to the bare IP 79.124.78.197 on port 80 targeting the path `/foots.php`, a direct-IP download with no associated domain name and a non-standard PHP endpoint strongly inconsistent with legitimate software distribution [koi_stealer-01#1]
- The same host also queried 79.124.78.197 with the path `/index.php?id=&subid=qIOuKk7U`, a parameterised PHP request to a raw IP across 2 events, reinforcing the suspicious nature of this server [koi_stealer-01#2]
- 79.124.78.197 was the single dominant download source for 172.17.0.99, accounting for 50 download events — far exceeding all other recorded download destinations combined [koi_stealer-01#0]
- 172.17.0.99 fetched `/assets/Owner/arm/ProcessMAU.txt` from 23.220.251.47 over plain HTTP; the path structure (owner/arm subdirectory, `.txt` extension for a binary-style resource) is unusual and warrants scrutiny as a possible secondary payload retrieval [koi_stealer-01#3]
- Assessment: The combination of repeated PHP-endpoint requests to a bare external IP (79.124.78.197) over unencrypted HTTP constitutes the strongest candidate for the initial infection download vector visible in the artifacts [koi_stealer-01#1, koi_stealer-01#0]
- A single HTTP request from 172.17.0.99 to 184.29.137.96:80 at path `/` was recorded; its purpose is not explained by surrounding context and is flagged as a possible additional suspicious contact [koi_stealer-01#2]

## Command-and-Control and Network Activity

- Internal host 172.17.0.99 (desktop-rnvo9at / user afletcher) generated 361 total external connection events to 35 distinct external destinations on 2024-09-04 [koi_stealer-02#0]
- The single most-contacted external IP was 79.124.78.197, receiving 218 of those 361 connections from 172.17.0.99 [koi_stealer-02#0]
- 49 high-severity Suricata alerts were directed toward 79.124.78.197, and 1 high-severity alert was directed toward 172.17.0.99 itself [koi_stealer-08#0]
- 172.17.0.99 issued two HTTP GET requests to 79.124.78.197:80 for the URI `/index.php?id=&subid=qIOuKk7U` [koi_stealer-01#2]
- Other observed external HTTP activity from 172.17.0.99 includes requests to 23.220.251.158:80 (`/connecttest.txt`, 2 events) and 199.232.210.172:80 for a Microsoft trusted-root certificate bundle [koi_stealer-01#2]
- DNS resolutions observed from the host include sso.godaddy.com (3 events), www.bellantonicioccolato.it (2 events), oneclient.sfx.ms (1 event), and img-s-msn-com.akamaized.net (1 event) [koi_stealer-07#0]
- One DNS resolution was observed for weathermapdata.blob.core.windows.net [koi_stealer-07#1]
**Assessment:**
- The parameterized URI pattern `/index.php?id=&subid=qIOuKk7U` on port 80 to 79.124.78.197, combined with 218 connections and 49 high-severity alerts to that same IP, is consistent with C2 beacon activity rather than a legitimate service [koi_stealer-01#2, koi_stealer-08#0]
- The domain www.bellantonicioccolato.it is not attributable to any known legitimate enterprise service in this environment and warrants further scrutiny as a possible secondary staging or redirect point [koi_stealer-07#0]

## Impact Assessment

- One internal host, 172.17.0.99 (desktop-rnvo9at, user afletcher), is the sole confirmed affected client, generating 361 outbound connection events to 35 distinct external destinations during the investigation window [koi_stealer-02#0]
- The dominant external destination was 79.124.78.197, receiving 218 of those connections and accounting for 49 of 50 high-severity IDS alerts directed outbound [koi_stealer-06#1, koi_stealer-08#0]
- Alert signatures indicate inbound C2 configuration delivery ("ET ATTACK_RESPONSE Koi Loader/Stealer CnC Config Inbound") and outbound credential/data check-in ("ET MALWARE Win32/Koi Stealer CnC Checkin (GET)"), pointing to exfiltration of data from the host [koi_stealer-06#2]
- Assessment: Confidentiality is the primary CIA component targeted; Koi Stealer is a credential and data harvesting family, and the confirmed C2 check-in and config-inbound signatures provide direct evidence that data was possibly exfiltrated from afletcher's account on 172.17.0.99 [koi_stealer-06#1, koi_stealer-06#2]
- External activity scale was limited to a single internal source host; 48 high-severity "suspicious POST to dotted quad" events indicate sustained outbound data transfer attempts concentrated in the 17:00–18:00 UTC hour [koi_stealer-06#2, koi_stealer-06#3]

## Root Cause and Evidence Gaps

- Assessment (medium confidence): The most likely root cause is a malware infection on host 172.17.0.99 (desktop-rnvo9at, user afletcher) that established persistent outbound communication, with 79.124.78.197 being the primary suspect external destination given it received 218 connections and was the target of 49 high-severity Suricata alerts concentrated in the 17:00–18:00 UTC window [koi_stealer-08#0]
- The precise initial infection vector (e.g., phishing, drive-by download, malicious document) is not established from the available artifacts [koi_stealer-08#0]
- The nature and content of the 53 file transfers originating from 172.17.0.99 to multiple external destinations over port 443 are unknown; whether these represent data exfiltration, payload staging, or legitimate cloud traffic cannot be determined from the evidence [koi_stealer-01#4, koi_stealer-01#5]
- Whether the Kerberos service requests (including LDAP and CIFS queries to WIN-CTL9XBQ9Y19) represent malware-driven AD reconnaissance or normal domain activity is not established from the available artifacts [koi_stealer-04#0, koi_stealer-04#1]
- TLS certificate analysis returned no results for self-signed, IP-based, or short-validity certificates, leaving the nature of the encrypted channels to 79.124.78.197 and other destinations uncharacterised [koi_stealer-09#0]
- Payload behaviour post-infection (e.g., credential harvesting, lateral movement, persistence mechanisms) is not established from the available artifacts [koi_stealer-08#0]
- Whether any data was successfully exfiltrated to any of the 35 distinct external destinations contacted by 172.17.0.99 is not established from the available artifacts [koi_stealer-08#0]

## Corrective and Preventive Actions

- Isolate host **172.17.0.99** (desktop-rnvo9at) from the LAN immediately to halt the 361 ongoing external connections, particularly the 218 connections to 79.124.78.197 which is the destination of 49 high-severity Suricata alerts [koi_stealer-08#0]
- Reset credentials for AD account **afletcher**, whose Kerberos tickets (including krbtgt/BEPOSITIVE and krbtgt/BEPOSITIVE.COM) were issued from the compromised host 172.17.0.99 during the incident window [koi_stealer-04#0, koi_stealer-04#1]
- Block outbound traffic to **79.124.78.197** at the perimeter firewall and review firewall rules for the URI pattern `/index.php?id=&subid=qIOuKk7U` observed in HTTP requests from 172.17.0.99 [koi_stealer-01#2]
- Audit and revoke any CIFS/SMB sessions that 172.17.0.99 established against the domain controller **WIN-CTL9XBQ9Y19** (cifs/WIN-CTL9XBQ9Y19.bepositive.com and cifs/WIN-CTL9XBQ9Y19) to determine whether AD resources were accessed or exfiltrated [koi_stealer-04#0, koi_stealer-04#1]
- Investigate the 53 file-transfer events from 172.17.0.99 to external destinations including 13.70.79.200, 13.89.179.9, 20.189.173.1, 20.189.173.26, 20.241.44.114, 20.42.73.28, and 20.96.153.111 (all port 443) to determine whether sensitive data was exfiltrated [koi_stealer-01#4, koi_stealer-01#5]

## Answers to Investigation Questions

1. 172.17.0.99 [koi_stealer-08#0]
2. DESKTOP-RNVO9AT [koi_stealer-05#0]
3. afletcher [koi_stealer-03#0]
4. www.bellantonicioccolato.it (2 events, no clear legitimate business relationship with the environment) and weathermapdata.blob.core.windows.net (1 event, atypical Azure Blob Storage subdomain pattern); Assessment: both domains are assessed as likely delivery or staging vectors given their anomalous presence in the traffic record alongside confirmed Koi Stealer alerts [koi_stealer-07#0, koi_stealer-07#1]
5. 79.124.78.197, which received 49 high-severity alert hits including "ET MALWARE Win32/Koi Stealer CnC Checkin (GET)" and "ET HUNTING GENERIC SUSPICIOUS POST to Dotted Quad with Fake Browser 1" signatures; Assessment: 79.124.78.197 is the primary suspected C2 endpoint [koi_stealer-06#2, koi_stealer-06#1]
6. Confidentiality; Assessment: the malware family identified is Koi Stealer, a credential and data-theft tool, making confidentiality the primary CIA component targeted [koi_stealer-06#2]
7. 2024-09-04 17:00 UTC [koi_stealer-06#3]
8. 79.124.78.197 received the most connections (218 out of 361 total external connections from 172.17.0.99); Assessment: it is assessed as a C2 server based on corroborating Suricata signatures identifying Koi Stealer check-in and inbound C2 config traffic directed to that IP [koi_stealer-02#0, koi_stealer-06#1]
