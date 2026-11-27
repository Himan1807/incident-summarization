# Incident Postmortem: Network security incident investigation

## Incident Summary



## Affected Host and User

- Affected internal host: 172.17.0.99, the top internal client by external connections (361 events, 35 distinct external destinations). [koi_stealer-08#0]
- Hostname of 172.17.0.99: desktop-rnvo9at. [koi_stealer-05#0]
- Human user account on 172.17.0.99: afletcher (8 Kerberos client events). [koi_stealer-03#0]
- Kerberos service requests from 172.17.0.99 (krbtgt/BEPOSITIVE, LDAP and CIFS to WIN-CTL9XBQ9Y19) confirm the host and user were active in the BEPOSITIVE AD domain; no other affected internal host is identified in the artifacts. [koi_stealer-04#1]

## Timeline

- 2024-09-04 17:00 UTC — alert timeline: 31 events; earliest alert hour [koi_stealer-06#3, koi_stealer-08#0]
- 2024-09-04 18:00 UTC — alert timeline: 26 events [koi_stealer-06#3]

## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions


