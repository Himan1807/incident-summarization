# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 17 of 70 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_29-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 1.58 at 2024-01-17 02:33:36 UTC; sustained deviation from 2024-01-17 02:24:06 UTC (score 176) [re2ob_29-01#0]
- metric anomalies: recommendationservice_mem — baseline median 43892736; peak 471867392 at 2024-01-17 02:26:41 UTC; sustained deviation from 2024-01-17 02:24:00 UTC (score 147) [re2ob_29-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.0822 at 2024-01-17 02:26:28 UTC; sustained deviation from 2024-01-17 02:24:28 UTC (score 138) [re2ob_29-01#0]
- metric anomalies: frontend_cpu — baseline median 8.57; peak 4.79 at 2024-01-17 02:35:46 UTC; sustained deviation from 2024-01-17 02:22:08 UTC (score 3.65) [re2ob_29-01#3]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 15.41 (x16.41); peak 41.00 at 2024-01-17 02:33:30 UTC [re2ob_29-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 11.98 (x12.98); peak 33.00 at 2024-01-17 02:33:30 UTC [re2ob_29-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 1.88 (x2.88); peak 12.00 at 2024-01-17 02:26:00 UTC [re2ob_29-02#0]
- operation latency: cartservice_GetCart — baseline mean 0.9268; later mean 1.43 (x1.26); peak 16.00 at 2024-01-17 02:24:00 UTC [re2ob_29-02#0]
- Derived: earliest sustained metric deviation: frontend_cpu from 2024-01-17 02:22:08 UTC. [re2ob_29-06#0]
- Derived: metric series ranked #1 by deviation score: recommendationservice_latency-90 (score 176). [re2ob_29-06#0]
- Derived: trace operation with the largest latency increase: recommendationservice_ListRecommendations (mean 0 -> 15.41, x16.41). [re2ob_29-06#0]
- Derived: container with the largest change in log volume: currencyservice (2402 -> 2264 lines/min). [re2ob_29-06#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.1429 (x1.04); peak 4.00 at 2024-01-17 02:22:00 UTC [re2ob_29-02#2]
- operation latency: productcatalogservice_GetProduct — baseline mean 5.15; later mean 5.38 (x1.04); peak 36.00 at 2024-01-17 02:32:45 UTC [re2ob_29-02#2]

## Timeline

- 2024-01-17 02:22 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.1429 (x1.04); peak 4.00 at 2024-01-17 02:22:00 UTC; earliest sustained metric deviation: frontend_cpu from 2024-01-17 02:22:08 UTC [re2ob_29-02#2, re2ob_29-06#0]
- 2024-01-17 02:24 UTC — operation latency: cartservice_GetCart — baseline mean 0.9268; later mean 1.43 (x1.26); peak 16.00 at 2024-01-17 02:24:00 UTC; operation latency: cartservice_AddItem — baseline mean 0; later mean 0.0536 (x1.05); peak 2.00 at 2024-01-17 02:24:00 UTC; operation latency: health_Check — baseline mean 0; later mean 0.0536 (x1.05); peak 1.00 at 2024-01-17 02:24:00 UTC [re2ob_29-02#0, re2ob_29-02#1]
- 2024-01-17 02:25 UTC — operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.125 (x1.10); peak 2.00 at 2024-01-17 02:25:45 UTC [re2ob_29-02#1]
- 2024-01-17 02:26 UTC — metric anomalies: recommendationservice_mem — baseline median 43892736; peak 471867392 at 2024-01-17 02:26:41 UTC; sustained deviation from 2024-01-17 02:24:00 UTC (score 147); metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.0822 at 2024-01-17 02:26:28 UTC; sustained deviation from 2024-01-17 02:24:28 UTC (score 138); metric anomalies: frontend_latency-50 — baseline median 0.0702; peak 0.1711 at 2024-01-17 02:26:21 UTC; sustained deviation from 2024-01-17 02:24:21 UTC (score 11.78); metric anomalies: paymentservice_latency-90 — baseline median 0.0089; peak 0.021 at 2024-01-17 02:26:08 UTC; sustained deviation from 2024-01-17 02:25:23 UTC (score 6.49); operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 1.88 (x2.88); peak 12.00 at 2024-01-17 02:26:00 UTC [re2ob_29-01#0, re2ob_29-01#2, re2ob_29-02#0]
- 2024-01-17 02:28 UTC — metric anomalies: redis_diskio — baseline median 0; peak 29118 at 2024-01-17 02:28:28 UTC; sustained deviation from 2024-01-17 02:23:00 UTC (score 79.72) [re2ob_29-01#1]
- 2024-01-17 02:30 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.72; peak 21.02 at 2024-01-17 02:30:59 UTC; sustained deviation from 2024-01-17 02:24:00 UTC (score 58.59) [re2ob_29-01#1]
- 2024-01-17 02:31 UTC — metric anomalies: redis_cpu — baseline median 0.3019; peak 0.1509 at 2024-01-17 02:31:20 UTC; sustained deviation from 2024-01-17 02:25:29 UTC (score 3.72) [re2ob_29-01#2]
- 2024-01-17 02:32 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 5.15; later mean 5.38 (x1.04); peak 36.00 at 2024-01-17 02:32:45 UTC [re2ob_29-02#2]
- 2024-01-17 02:33 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 1.58 at 2024-01-17 02:33:36 UTC; sustained deviation from 2024-01-17 02:24:06 UTC (score 176); metric anomalies: frontend_socket — baseline median 27.00; peak 35.00 at 2024-01-17 02:33:39 UTC; sustained deviation from 2024-01-17 02:24:42 UTC (score 14.68); operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 15.41 (x16.41); peak 41.00 at 2024-01-17 02:33:30 UTC; operation latency: frontendservice_frontend — baseline mean 0; later mean 11.98 (x12.98); peak 33.00 at 2024-01-17 02:33:30 UTC [re2ob_29-01#0, re2ob_29-01#1, re2ob_29-02#0]
- 2024-01-17 02:34 UTC — metric anomalies: frontend_latency-90 — baseline median 0.2329; peak 1.34 at 2024-01-17 02:34:19 UTC; sustained deviation from 2024-01-17 02:24:21 UTC (score 50.40) [re2ob_29-01#1]
- 2024-01-17 02:35 UTC — metric anomalies: currencyservice_cpu — baseline median 30.43; peak 15.08 at 2024-01-17 02:35:38 UTC; sustained deviation from 2024-01-17 02:22:44 UTC (score 3.74); metric anomalies: frontend_cpu — baseline median 8.57; peak 4.79 at 2024-01-17 02:35:46 UTC; sustained deviation from 2024-01-17 02:22:08 UTC (score 3.65); operation latency: traceservice_Export — baseline mean 0.0488; later mean 0.25 (x1.19); peak 2.00 at 2024-01-17 02:35:00 UTC [re2ob_29-01#2, re2ob_29-01#3, re2ob_29-02#1]

## Detection: IDS Alerts

- metric anomalies: redis_diskio — baseline median 0; peak 29118 at 2024-01-17 02:28:28 UTC; sustained deviation from 2024-01-17 02:23:00 UTC (score 79.72) [re2ob_29-01#1]
- metric anomalies: recommendationservice_cpu — baseline median 2.72; peak 21.02 at 2024-01-17 02:30:59 UTC; sustained deviation from 2024-01-17 02:24:00 UTC (score 58.59) [re2ob_29-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.2329; peak 1.34 at 2024-01-17 02:34:19 UTC; sustained deviation from 2024-01-17 02:24:21 UTC (score 50.40) [re2ob_29-01#1]
- metric anomalies: frontend_socket — baseline median 27.00; peak 35.00 at 2024-01-17 02:33:39 UTC; sustained deviation from 2024-01-17 02:24:42 UTC (score 14.68) [re2ob_29-01#1]
- operation latency: traceservice_Export — baseline mean 0.0488; later mean 0.25 (x1.19); peak 2.00 at 2024-01-17 02:35:00 UTC [re2ob_29-02#1]
- operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.125 (x1.10); peak 2.00 at 2024-01-17 02:25:45 UTC [re2ob_29-02#1]
- operation latency: cartservice_AddItem — baseline mean 0; later mean 0.0536 (x1.05); peak 2.00 at 2024-01-17 02:24:00 UTC [re2ob_29-02#1]
- operation latency: health_Check — baseline mean 0; later mean 0.0536 (x1.05); peak 1.00 at 2024-01-17 02:24:00 UTC [re2ob_29-02#1]

## Initial Infection Indicators

- metric anomalies: frontend_latency-50 — baseline median 0.0702; peak 0.1711 at 2024-01-17 02:26:21 UTC; sustained deviation from 2024-01-17 02:24:21 UTC (score 11.78) [re2ob_29-01#2]
- metric anomalies: paymentservice_latency-90 — baseline median 0.0089; peak 0.021 at 2024-01-17 02:26:08 UTC; sustained deviation from 2024-01-17 02:25:23 UTC (score 6.49) [re2ob_29-01#2]
- metric anomalies: currencyservice_cpu — baseline median 30.43; peak 15.08 at 2024-01-17 02:35:38 UTC; sustained deviation from 2024-01-17 02:22:44 UTC (score 3.74) [re2ob_29-01#2]
- metric anomalies: redis_cpu — baseline median 0.3019; peak 0.1509 at 2024-01-17 02:31:20 UTC; sustained deviation from 2024-01-17 02:25:29 UTC (score 3.72) [re2ob_29-01#2]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_29-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_29-03#0]
2. operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.1429 (x1.04); peak 4.00 at 2024-01-17 02:22:00 UTC [re2ob_29-02#2]
3. operation latency: productcatalogservice_GetProduct — baseline mean 5.15; later mean 5.38 (x1.04); peak 36.00 at 2024-01-17 02:32:45 UTC [re2ob_29-02#2]
4. Not established from the available artifacts.
5. log volume: frontend — 2670 lines/min in the baseline, 2541 lines/min later [re2ob_29-04#0]
6. log volume: adservice — 449 lines/min in the baseline, 430 lines/min later [re2ob_29-04#0]
7. log volume: paymentservice — 55.40 lines/min in the baseline, 53.14 lines/min later [re2ob_29-04#0]
8. Not established from the available artifacts.
