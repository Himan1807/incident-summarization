# Incident Postmortem: Network security incident investigation

## Incident Summary



## Affected Host and User

- 10.1.17.215 – desktop‑l8c5gsj – user **shutchenson** [fake_auth-09#0]

## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions

- Quarantine the internal host 10.1.17.215 to stop further outbound activity [fake_auth-09#0]
- Block outbound traffic to external IP 5.252.153.241, the most‑contacted destination observed [fake_auth-09#0]
- Block outbound traffic to external IP 185.188.32.26, associated with malicious HTTP requests [fake_auth-01#2]
- Disable or reset the user account shutchenson due to repeated authenticated activity from the compromised host [fake_auth-03#0]
- Add a DNS block for the domain oneclient.sfx.ms, which was queried exclusively by the affected host [fake_auth-08#0]

## Answers to Investigation Questions


