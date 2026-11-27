# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 11 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_12-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 40643 at 2024-01-17 08:24:40 UTC; sustained deviation from 2024-01-17 08:19:23 UTC (score 116) [re2ob_12-01#0]
- metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-17 08:21:27 UTC; sustained deviation from 2024-01-17 08:21:27 UTC (score 71.43) [re2ob_12-01#0]
- metric anomalies: currencyservice_mem — baseline median 43917312; peak 51490816 at 2024-01-17 08:23:12 UTC; sustained deviation from 2024-01-17 08:22:53 UTC (score 5.18) [re2ob_12-01#0]
- Derived: earliest sustained metric deviation: redis_cpu from 2024-01-17 08:19:21 UTC. [re2ob_12-06#0]
- Derived: metric series ranked #1 by deviation score: redis_diskio (score 116). [re2ob_12-06#0]
- Derived: trace operation with the largest latency increase: cartservice_GetCart (mean 0.3659 -> 2.30, x2.42). [re2ob_12-06#0]
- Derived: container with the largest change in log volume: redis (1.00 -> 1.07 lines/min). [re2ob_12-06#0]
- operation latency: cartservice_GetCart — baseline mean 0.3659; later mean 2.30 (x2.42); peak 23.00 at 2024-01-17 08:28:45 UTC [re2ob_12-02#0]
- operation latency: frontendservice_frontend — baseline mean 1.49; later mean 3.61 (x1.85); peak 27.00 at 2024-01-17 08:28:45 UTC [re2ob_12-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.7561; later mean 1.30 (x1.31); peak 8.00 at 2024-01-17 08:27:15 UTC [re2ob_12-02#0]
- operation latency: adservice_GetAds — baseline mean 0.7073; later mean 1.00 (x1.17); peak 5.00 at 2024-01-17 08:30:30 UTC [re2ob_12-02#0]
- metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.54 at 2024-01-17 08:32:59 UTC; sustained deviation from 2024-01-17 08:22:04 UTC (score 4.25) [re2ob_12-01#1]
- metric anomalies: redis_cpu — baseline median 0.2929; peak 0.1464 at 2024-01-17 08:19:21 UTC; sustained deviation from 2024-01-17 08:19:21 UTC (score 3.92) [re2ob_12-01#1]
- metric anomalies: currencyservice_cpu — baseline median 29.91; peak 16.31 at 2024-01-17 08:29:11 UTC; sustained deviation from 2024-01-17 08:19:27 UTC (score 3.46) [re2ob_12-01#1]
- metric anomalies: productcatalogservice_cpu — baseline median 3.66; peak 1.62 at 2024-01-17 08:27:54 UTC; sustained deviation from 2024-01-17 08:27:54 UTC (score 2.54) [re2ob_12-01#1]

## Timeline

- 2024-01-17 08:19 UTC — metric anomalies: redis_cpu — baseline median 0.2929; peak 0.1464 at 2024-01-17 08:19:21 UTC; sustained deviation from 2024-01-17 08:19:21 UTC (score 3.92); earliest sustained metric deviation: redis_cpu from 2024-01-17 08:19:21 UTC [re2ob_12-01#1, re2ob_12-06#0]
- 2024-01-17 08:21 UTC — metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-17 08:21:27 UTC; sustained deviation from 2024-01-17 08:21:27 UTC (score 71.43); metric anomalies: frontend_cpu — baseline median 8.46; peak 3.80 at 2024-01-17 08:21:24 UTC; sustained deviation from 2024-01-17 08:21:24 UTC (score 2.49); metric anomalies: recommendationservice_socket — baseline median 4.00; peak 6.00 at 2024-01-17 08:21:04 UTC; sustained deviation from 2024-01-17 08:21:04 UTC (score 0); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 7.80; later mean 8.41 (x1.07); peak 43.00 at 2024-01-17 08:21:00 UTC [re2ob_12-01#0, re2ob_12-01#2, re2ob_12-02#1]
- 2024-01-17 08:22 UTC — operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.1071 (x1.08); peak 3.00 at 2024-01-17 08:22:15 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 6.61; later mean 7.18 (x1.07); peak 34.00 at 2024-01-17 08:22:15 UTC [re2ob_12-02#1]
- 2024-01-17 08:23 UTC — metric anomalies: currencyservice_mem — baseline median 43917312; peak 51490816 at 2024-01-17 08:23:12 UTC; sustained deviation from 2024-01-17 08:22:53 UTC (score 5.18); operation latency: traceservice_Export — baseline mean 0.2683; later mean 0.3455 (x1.06); peak 2.00 at 2024-01-17 08:23:00 UTC [re2ob_12-01#0, re2ob_12-02#2]
- 2024-01-17 08:24 UTC — metric anomalies: redis_diskio — baseline median 0; peak 40643 at 2024-01-17 08:24:40 UTC; sustained deviation from 2024-01-17 08:19:23 UTC (score 116) [re2ob_12-01#0]
- 2024-01-17 08:26 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0.1463; later mean 0.2909 (x1.13); peak 4.00 at 2024-01-17 08:26:45 UTC; operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.0364 (x1.04); peak 1.00 at 2024-01-17 08:26:45 UTC [re2ob_12-02#1, re2ob_12-02#2]
- 2024-01-17 08:27 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.66; peak 1.62 at 2024-01-17 08:27:54 UTC; sustained deviation from 2024-01-17 08:27:54 UTC (score 2.54); metric anomalies: checkoutservice_latency-90 — baseline median 0.2363; peak 0.5625 at 2024-01-17 08:27:38 UTC; sustained deviation from 2024-01-17 08:27:36 UTC (score 1.91); operation latency: recommendationservice_ListRecommendations — baseline mean 0.7561; later mean 1.30 (x1.31); peak 8.00 at 2024-01-17 08:27:15 UTC [re2ob_12-01#1, re2ob_12-01#2, re2ob_12-02#0]
- 2024-01-17 08:28 UTC — operation latency: cartservice_GetCart — baseline mean 0.3659; later mean 2.30 (x2.42); peak 23.00 at 2024-01-17 08:28:45 UTC; operation latency: frontendservice_frontend — baseline mean 1.49; later mean 3.61 (x1.85); peak 27.00 at 2024-01-17 08:28:45 UTC [re2ob_12-02#0]
- 2024-01-17 08:29 UTC — metric anomalies: currencyservice_cpu — baseline median 29.91; peak 16.31 at 2024-01-17 08:29:11 UTC; sustained deviation from 2024-01-17 08:19:27 UTC (score 3.46); metric anomalies: frontend_latency-90 — baseline median 0.2216; peak 0.3312 at 2024-01-17 08:29:06 UTC; sustained deviation from 2024-01-17 08:21:21 UTC (score 2.19) [re2ob_12-01#1, re2ob_12-01#2]
- 2024-01-17 08:30 UTC — operation latency: adservice_GetAds — baseline mean 0.7073; later mean 1.00 (x1.17); peak 5.00 at 2024-01-17 08:30:30 UTC [re2ob_12-02#0]
- 2024-01-17 08:32 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.54 at 2024-01-17 08:32:59 UTC; sustained deviation from 2024-01-17 08:22:04 UTC (score 4.25) [re2ob_12-01#1]

## Detection: IDS Alerts

- operation latency: checkoutservice_PlaceOrder — baseline mean 0.1463; later mean 0.2909 (x1.13); peak 4.00 at 2024-01-17 08:26:45 UTC [re2ob_12-02#1]
- operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.1071 (x1.08); peak 3.00 at 2024-01-17 08:22:15 UTC [re2ob_12-02#1]
- operation latency: productcatalogservice_GetProduct — baseline mean 6.61; later mean 7.18 (x1.07); peak 34.00 at 2024-01-17 08:22:15 UTC [re2ob_12-02#1]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 7.80; later mean 8.41 (x1.07); peak 43.00 at 2024-01-17 08:21:00 UTC [re2ob_12-02#1]

## Initial Infection Indicators

- metric anomalies: frontend_cpu — baseline median 8.46; peak 3.80 at 2024-01-17 08:21:24 UTC; sustained deviation from 2024-01-17 08:21:24 UTC (score 2.49) [re2ob_12-01#2]
- metric anomalies: frontend_latency-90 — baseline median 0.2216; peak 0.3312 at 2024-01-17 08:29:06 UTC; sustained deviation from 2024-01-17 08:21:21 UTC (score 2.19) [re2ob_12-01#2]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2363; peak 0.5625 at 2024-01-17 08:27:38 UTC; sustained deviation from 2024-01-17 08:27:36 UTC (score 1.91) [re2ob_12-01#2]
- metric anomalies: recommendationservice_socket — baseline median 4.00; peak 6.00 at 2024-01-17 08:21:04 UTC; sustained deviation from 2024-01-17 08:21:04 UTC (score 0) [re2ob_12-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: traceservice_Export — baseline mean 0.2683; later mean 0.3455 (x1.06); peak 2.00 at 2024-01-17 08:23:00 UTC [re2ob_12-02#2]
- operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.0364 (x1.04); peak 1.00 at 2024-01-17 08:26:45 UTC [re2ob_12-02#2]
- No matching results for: monitoring alerts / alerting rules (no alerts were recorded in this capture). (Absence in this query is not proof of absence elsewhere.) [re2ob_12-07#0]
- No matching results for: change records / deployments (no change-management data in this capture). (Absence in this query is not proof of absence elsewhere.) [re2ob_12-07#0]
- Disk I/O metrics contain data only for: adservice, emailservice, recommendationservice, redis. [re2ob_12-07#0]
- No matching results for: error- or warning-level application logs (all log lines are info or debug). (Absence in this query is not proof of absence elsewhere.) [re2ob_12-07#0]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_12-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_12-03#0]
2. operation latency: traceservice_Export — baseline mean 0.2683; later mean 0.3455 (x1.06); peak 2.00 at 2024-01-17 08:23:00 UTC [re2ob_12-02#2]
3. operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.0364 (x1.04); peak 1.00 at 2024-01-17 08:26:45 UTC [re2ob_12-02#2]
4. Not established from the available artifacts.
5. log volume: recommendationservice — 567 lines/min in the baseline, 558 lines/min later [re2ob_12-04#0]
6. log volume: shippingservice — 452 lines/min in the baseline, 447 lines/min later [re2ob_12-04#0]
7. log volume: checkoutservice — 86.70 lines/min in the baseline, 85.93 lines/min later [re2ob_12-04#0]
8. Not established from the available artifacts.
