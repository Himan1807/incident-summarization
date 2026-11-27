# Incident Postmortem: Download from Fake Software Site

## Incident Summary

Here is the Incident Summary:

* The incident occurred on 2025-01-22T19:44:56.530137Z to 2025-01-22T20:38:18.918250Z.
* Internal host 10.1.17.215 made 300 outbound connections to 137 distinct external IPs.
* The client 10.1.17.215 received data from 13 unique external IP addresses, including 45.125.66.32, 5.252.153.241, 82.221.136.26, and 23.55.125.176.
* The client 10.1.17.215 made connections to multiple external IPs on port(s) 443, 80, and 2917.
* The following files/URIs were downloaded from the server 5.252.153.241:80: /api/file/get-file/264872, /api/file/get-file/29842.ps1, /api/file/get-file/TeamViewer, /api/file/get-file/Teamviewer_Resource_fr, /api/file/get-file/TV, and /api/file/get-file/pas.ps1.  ⚠ UNVERIFIED: /api/file/get-file/pas.ps1.
* The client 10.1.17.215 made connections to the following external IPs: 45.125.66.32, 5.252.153.241, 82.221.136.26, 23.55.125.176, 208.89.12.153, 23.221.220.40, 23.205.110.145, and 13.107.246.57.

## Impact and Affected Assets

### Impact and Affected Assets

* Internal host 10.1.17.215 made 300 outbound connections to 137 distinct external IPs.
* Internal host 169.254.168.209 made 1 outbound connection to 1 distinct external IP.
* External IP 45.125.66.32 received 9302393 bytes from client(s) 10.1.17.215 on port(s) 2917.
* External IP 5.252.153.241 received 6299207 bytes from client(s) 10.1.17.215 on port(s) 80.
* External IP 82.221.136.26 received 2231584 bytes from client(s) 10.1.17.215 on port(s) 443.
* External IP 23.55.125.176 received 476119 bytes from client(s) 10.1.17.215 on port(s) 443.

Assessment: 
* The internal host 10.1.17.215 is the primary affected asset, with a large number of outbound connections to multiple external IPs.
* The scale of external activity is significant, with multiple external IPs receiving data from the affected internal host.

## Timeline

* 2025-01-22 19:44:56Z: First DNS query to domain win-gsh54qlw48d.bluemoontuesday.com [2025-01-22-E1#0]
* 2025-01-22 19:44:56Z: First DNS query to domain DESKTOP-L8C5GSJ.bluemoontuesday.com [2025-01-22-E1#0]
* 2025-01-22 19:44:56Z: First DNS query to domain bluemoontuesday.com [2025-01-22-E1#0]
* 2025-01-22 19:45:16Z: First DNS query to domain oneclient.sfx.ms [2025-01-22-E1#3]
* 2025-01-22 19:45:25Z: First contact with external IP 23.205.110.143 [2025-01-22-E1#1]
* 2025-01-22 19:45:35Z: First contact with external IP 82.221.136.26 [2025-01-22-E1#1]
* 2025-01-22 19:45:48Z: First DNS query to domain appointedtimeagriculture.com [2025-01-22-E1#1]
* 2025-01-22 19:45:59Z: First DNS query to domain play.vidyard.com [2025-01-22-E1#3]
* 2025-01-22 19:46:00Z: First DNS query to domain lpcdn.lpsnmedia.net [2025-01-22-E1#3]
* 2025-01-22 19:46:02Z: First DNS query to domain dpm.demdex.net [2025-01-22-E1#3]
* 2025-01-22 19:46:04Z: First DNS query to domain px.owneriq.net [2025-01-22-E1#3]
*

## Detection and Indicators of Compromise

### Detection and Indicators of Compromise

* Possible: No non-browser HTTP User-Agents were observed [2025-01-22-06#0]
* Possible: HTTP Server header 'Qwilt' seen 2 times from 217.20.51.20 [2025-01-22-07#0]
* External IP 23.205.110.143: first contact 2025-01-22 19:45:25Z, last contact 2025-01-22 19:45:27Z, 3 logged events (conn/http/tls) [2025-01-22-E1#1]
* Domain authenticatoor.org: first queried 2025-01-22 19:45:35Z, last queried 2025-01-22 19:45:35Z, 4 DNS events [2025-01-22-E1#1]
* External IP 82.221.136.26: first contact 2025-01-22 19:45:35Z, last contact 2025-01-22 19:45:35Z, 1 logged events (conn/http/tls) [2025-01-22-E1#1]
* Domain appointedtimeagriculture.com: first queried 2025-01-22 19:45:48Z, last queried 2025-01-22 19:45:48Z, 4 DNS events [2025-01-22-E1#1]
* HTTP request to 5.252.153.241:80 URI /api/file/get-file/264872 (Host: 5.252.153.241) by client(s) 10.1.17.215; requests: 1; user-agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET

## Investigation Findings: Malicious Downloads

### Investigation Findings: Malicious Downloads

* The following files/URIs were downloaded from the server 5.252.153.241:80:
	+ /api/file/get-file/264872
	+ /api/file/get-file/29842.ps1
	+ /api/file/get-file/TeamViewer
	+ /api/file/get-file/Teamviewer_Resource_fr
	+ /api/file/get-file/TV
	+ /api/file/get-file/pas.ps1
* The following file was downloaded from the server 199.232.214.172:80:
	+ /c/msdownload/update/software/defu/2025/01/am_delta_patch_1.421.1491.0_c8e6042b36d8f357a8e298b6f9f2fcde561c2e02.exe
* The client 10.1.17.215 made connections to the following external IPs:
	+ 45.125.66.32: 9 connections, 9302393 bytes received on port(s) 2917
	+ 5.252.153.241: 3 connections, 6299207 bytes received on port(s) 80
	+ 82.221.136.26: 1 connections, 2231584 bytes received on port(s) 443
	+ 23.55.125.176: 6 connections, 476119 bytes received on port(s) 443
	+ 208.89.12.153: 1 connections, 178375 bytes received on port(s) 443
	+ 23.221.220.40: 3 connections, 159801 bytes received on port(s) 443
	+ 23.205.110.145: 3 connections, 115204 bytes received on port(s) 443
	+ 13.107.246.57: 13 connections, 106020 bytes received on port(s) 443

## Investigation Findings: Command-and-Control and Data Transfer

### Investigation Findings: Command-and-Control and Data Transfer

#### Observed Facts

* The client(s) 10.1.17.215 established connections to multiple external IP addresses on port(s) 443, 80, and 2917.
	+ Port 443: 34 connections, 178375 + 159801 + 115204 + ... + 56687 bytes received
	+ Port 80: 5 connections, 6299207 + 475915 bytes received
	+ Port 2917: 9 connections, 9302393 bytes received
* The client(s) 10.1.17.215 received data from 13 unique external IP addresses.

#### Assessment:

* Possible command-and-control (C2) communication: The client(s) 10.1.17.215 established multiple connections to various external IP addresses, indicating possible C2 communication.
* Possible data transfer: The large amount of data received by the client(s) 10.1.17.215 suggests possible data transfer, possibly related to the initial download from the fake software site.
* Possible multiple C2 servers: The multiple external IP addresses involved in the communication may indicate the use of multiple C2 servers.

## Root Cause and Contributing Factors

### Root Cause and Contributing Factors

* **Observed Facts:**
	+ Internal host 10.1.17.215 made 300 outbound connections to 137 distinct external IPs.
	+ TLS SNI login.microsoftonline.com seen 17 times from client(s) 10.1.17.215.
	+ TLS SNI 45.125.66.32 seen 9 times from client(s) 10.1.17.215.
	+ TLS SNI windows.msn.com seen 4 times from client(s) 10.1.17.215.
	+ TLS SNI www.bing.com seen 4 times from client(s) 10.1.17.215.
	+ No non-browser HTTP User-Agents were observed.
* **Assessment:**
	+ **Likely Root Cause:** Malicious software download from a fake software site (high confidence)
		- Supporting evidence: Frequent TLS SNI connections to Microsoft-related domains (login.microsoftonline.com, windows.msn.com, www.bing.com) and a large number of outbound connections from a single host. This suggests a potential infection vector involving a fake software update or download.

## Open Questions and Evidence Gaps

### Open Questions and Evidence Gaps

* Initial infection vector: Not established from the available artifacts.
* User account: Not established from the available artifacts.
* Payload behavior: Not established from the available artifacts.
* Data exfiltration: Not established from the available artifacts.
* Root cause: Not established from the available artifacts.
* Impact: Not established from the available artifacts.
* Confirmed C2 attribution: Not established from the available artifacts.
* Browser or non-browser HTTP User-Agent: Only browser HTTP User-Agents were observed [2025-01-22-06#0].
* HTTP Server-header: Not observed in the available artifacts.
* TLS version and cipher suite: Not established from the available artifacts.
* HTTP GET requests: Multiple GET requests were observed, but their purpose is unclear [2025-01-22-E1#5].
* DNS resolution: Multiple domains were queried, but their purpose is unclear [2025-01-22-E1#1, #3].

## Corrective and Preventive Actions

### Corrective and Preventive Actions

* Block IP 5.252.153.241 to prevent further malicious activity [2025-01-22-E1#4].
* Block IP 45.125.66.32 to prevent further malicious activity [2025-01-22-E1#5].
* Monitor and block connections to the following domains:
	+ play.vidyard.com [2025-01-22-E1#3]
	+ lpcdn.lpsnmedia.net [2025-01-22-E1#3]
	+ dpm.demdex.net [2025-01-22-E1#3]
	+ px.owneriq.net [2025-01-22-E1#3]
	+ authenticatoor.org [2025-01-22-E1#1]
	+ appointedtimeagriculture.com [2025-01-22-E1#1]
* Monitor and block connections to the following external IPs:
	+ 199.232.214.172 [2025-01-22-E1#4]
	+ 23.205.110.143 [2025-01-22-E1#1]
	+ 82.221.136.26 [2025-01-22-E1#1]
	+ 23.55.125.176 [2025-01-22-04#0]
