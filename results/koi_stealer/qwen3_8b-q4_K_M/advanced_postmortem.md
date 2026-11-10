# Incident Postmortem: Network security incident investigation

## Incident Summary

- Internal client 172.17.0.99 (hostname: desktop-rnvo9at, user account: afletcher) initiated unauthorized external connections during the incident [koi_stealer-08#0].
- The earliest detected activity occurred at 17:00 UTC, with 31 IDS alerts logged [koi_stealer-06#3, koi_stealer-08#0].
- Multiple external IPs were contacted, consistent with potential C2 communication from the compromised host [koi_stealer-08#0].
- Assessment: Unauthorized external connections from 172.17.0.99 (user afletcher) to multiple external IPs likely indicate compromised credentials or misconfigured services [koi_stealer-08#0].

## Affected Host and User

- Internal client 172.17.0.99 (hostname: desktop-rnvo9at, user account: afletcher) [koi_stealer-08#0]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

Assessment: Unauthorized external connections from 172.17.0.99 (user afletcher) to multiple external IPs, likely indicating compromised credentials or misconfigured services [koi_stealer-08#0].
Not established: Initial infection vector (no phishing, exploit, or malware artifacts detected) [koi_stealer-01#4].

## Corrective and Preventive Actions



## Answers to Investigation Questions


