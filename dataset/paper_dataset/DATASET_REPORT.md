# Dataset report

Atoms = individual reference answer items (IP, host, user, domain, time, label). 'In evidence' = atom appears in the artifacts the pipeline receives; the remainder must be inferred (for example the CIA component or 'C2 server' labels) or is a reference typo.

| Scenario | Artifacts | Facts | Questions | Atoms | In evidence | Failed queries |
|---|---|---|---|---|---|---|
| apr21isc | 8 | 64 | 8 | 14 | 13 (92%) | - |
| burnincandle | 9 | 79 | 7 | 18 | 18 (100%) | suspicious_certificates |
| dec21isc | 10 | 60 | 8 | 11 | 11 (100%) | - |
| dirty_rat | 9 | 76 | 7 | 11 | 10 (90%) | - |
| easy_123 | 9 | 68 | 6 | 7 | 7 (100%) | - |
| fake_auth | 9 | 97 | 8 | 12 | 12 (100%) | - |
| gozi | 9 | 92 | 9 | 23 | 21 (91%) | - |
| iced_id | 9 | 136 | 8 | 12 | 11 (91%) | suspicious_certificates |
| jun21isc | 10 | 163 | 8 | 23 | 23 (100%) | - |
| koi_stealer | 9 | 66 | 8 | 9 | 8 (88%) | - |
| lumma_stealer | 9 | 82 | 7 | 9 | 8 (88%) | - |
| may21isc | 10 | 67 | 7 | 8 | 8 (100%) | - |
| net_rat | 9 | 75 | 7 | 9 | 9 (100%) | - |
| oct21isc | 9 | 142 | 8 | 18 | 17 (94%) | - |
| qakbot | 10 | 102 | 8 | 13 | 11 (84%) | - |
| redline_stlr | 9 | 59 | 8 | 10 | 8 (80%) | - |
| warmcookie | 9 | 85 | 7 | 11 | 10 (90%) | - |

**Total:** 205/218 atoms (94%) are present in the evidence.