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

# RCAEval RE2-OB (Online Boutique)

30 incidents converted by `src/prepare_rcaeval.py` from RCAEval RE2-OB (Zenodo record 14590730): one repetition per root-cause service x fault type. Incident names are neutral; the source case of each is in its `cleaning_report.json`. 'In evidence' = the atom string appears (case-insensitive, same matching as the evaluator) in the artifacts, questions or description; multiple-choice labels count as present because the options are in the question.

| Scenario | Source case | Artifacts | Facts | Questions | Atoms | In evidence | Not in evidence |
|---|---|---|---|---|---|---|---|
| re2ob_01 | RE2-OB/checkoutservice_cpu/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_02 | RE2-OB/checkoutservice_delay/1 | 7 | 61 | 8 | 9 | 9 (100%) | - |
| re2ob_03 | RE2-OB/checkoutservice_disk/1 | 7 | 54 | 8 | 9 | 9 (100%) | - |
| re2ob_04 | RE2-OB/checkoutservice_loss/1 | 7 | 57 | 8 | 9 | 9 (100%) | - |
| re2ob_05 | RE2-OB/checkoutservice_mem/1 | 7 | 53 | 8 | 9 | 8 (88%) | 2024-01-17 03:27 UTC |
| re2ob_06 | RE2-OB/checkoutservice_socket/1 | 7 | 62 | 8 | 9 | 9 (100%) | - |
| re2ob_07 | RE2-OB/currencyservice_cpu/1 | 7 | 61 | 8 | 9 | 9 (100%) | - |
| re2ob_08 | RE2-OB/currencyservice_delay/1 | 7 | 61 | 8 | 9 | 9 (100%) | - |
| re2ob_09 | RE2-OB/currencyservice_disk/1 | 7 | 54 | 8 | 9 | 9 (100%) | - |
| re2ob_10 | RE2-OB/currencyservice_loss/1 | 7 | 58 | 8 | 9 | 9 (100%) | - |
| re2ob_11 | RE2-OB/currencyservice_mem/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_12 | RE2-OB/currencyservice_socket/1 | 7 | 52 | 8 | 9 | 9 (100%) | - |
| re2ob_13 | RE2-OB/emailservice_cpu/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_14 | RE2-OB/emailservice_delay/1 | 7 | 59 | 8 | 9 | 9 (100%) | - |
| re2ob_15 | RE2-OB/emailservice_disk/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_16 | RE2-OB/emailservice_loss/1 | 7 | 56 | 8 | 9 | 9 (100%) | - |
| re2ob_17 | RE2-OB/emailservice_mem/1 | 7 | 52 | 8 | 9 | 8 (88%) | 2024-01-17 07:11 UTC |
| re2ob_18 | RE2-OB/emailservice_socket/1 | 7 | 61 | 8 | 9 | 9 (100%) | - |
| re2ob_19 | RE2-OB/productcatalogservice_cpu/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_20 | RE2-OB/productcatalogservice_delay/1 | 7 | 53 | 8 | 9 | 8 (88%) | 2024-01-16 08:42 UTC |
| re2ob_21 | RE2-OB/productcatalogservice_disk/1 | 7 | 54 | 8 | 9 | 9 (100%) | - |
| re2ob_22 | RE2-OB/productcatalogservice_loss/1 | 7 | 64 | 8 | 9 | 9 (100%) | - |
| re2ob_23 | RE2-OB/productcatalogservice_mem/1 | 7 | 56 | 8 | 9 | 8 (88%) | 2024-01-15 22:26 UTC |
| re2ob_24 | RE2-OB/productcatalogservice_socket/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_25 | RE2-OB/recommendationservice_cpu/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_26 | RE2-OB/recommendationservice_delay/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_27 | RE2-OB/recommendationservice_disk/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_28 | RE2-OB/recommendationservice_loss/1 | 7 | 69 | 8 | 9 | 9 (100%) | - |
| re2ob_29 | RE2-OB/recommendationservice_mem/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |
| re2ob_30 | RE2-OB/recommendationservice_socket/1 | 7 | 53 | 8 | 9 | 9 (100%) | - |

**Total (RCAEval):** 266/270 atoms (98%) are present in the evidence.

Questions mirror the paper set: root-cause service, its pod and node (instead of infected host, hostname and user), fault type (multiple choice), CIA component, first-signs minute (RCAEval captures last 24 minutes, so the minute is asked instead of the hour), the RCAEval root-cause indicator `<service>_<indicator>`, and the largest trace-latency increase with 'root cause or downstream symptom' (instead of 'C2 server or legitimate service'). Question 8's reference is derived from the telemetry, not an RCAEval label.
