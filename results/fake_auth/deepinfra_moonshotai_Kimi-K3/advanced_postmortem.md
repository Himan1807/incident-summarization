# Incident Postmortem: Network security incident investigation

## Incident Summary

The affected host is internal client 10.1.17.215 (DESKTOP-L8C5GSJ), which drove 1823 external connections to 119 distinct destinations during the investigation window. The earliest alert activity occurred at 2025-01-22 19:00 UTC, when 10 alert events were recorded. Alert volume dropped to 2 events by 2025-01-22 20:00 UTC. The affected user associated with DESKTOP-L8C5GSJ is not established from the available artifacts. The main command-and-control candidate is not established from the available artifacts. Assessment: The volume and breadth of external connections from 10.1.17.215 was sufficient to warrant isolating the host from the LAN pending forensic reimaging. [fake_auth-09#0, fake_auth-06#4]

## Affected Host and User



## Timeline

- 2025-01-22 19:00 UTC — alert timeline: 10 events; earliest alert hour [fake_auth-06#4, fake_auth-09#0]
- 2025-01-22 20:00 UTC — alert timeline: 2 events [fake_auth-06#4]

## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions

- Isolate internal host 10.1.17.215 (DESKTOP-L8C5GSJ) from the LAN pending forensic reimaging, as it drove 1823 external connections to 119 distinct destinations. [fake_auth-09#0]

## Answers to Investigation Questions


