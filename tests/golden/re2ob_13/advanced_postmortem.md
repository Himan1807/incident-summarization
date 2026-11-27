# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 13 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_13-01#0]
- metric anomalies: emailservice_cpu — baseline median 0.2842; peak 20.04 at 2024-01-15 20:28:23 UTC; sustained deviation from 2024-01-15 20:22:57 UTC (score 154) [re2ob_13-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 41093 at 2024-01-15 20:24:10 UTC; sustained deviation from 2024-01-15 20:23:44 UTC (score 119) [re2ob_13-01#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0168 at 2024-01-15 20:25:19 UTC; sustained deviation from 2024-01-15 20:23:12 UTC (score 104) [re2ob_13-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0143 at 2024-01-15 20:28:33 UTC; sustained deviation from 2024-01-15 20:28:22 UTC (score 0.7383) [re2ob_13-01#3]
- Derived: earliest sustained metric deviation: currencyservice_cpu from 2024-01-15 20:21:35 UTC. [re2ob_13-06#0]
- Derived: metric series ranked #1 by deviation score: emailservice_cpu (score 154). [re2ob_13-06#0]
- Derived: trace operation with the largest latency increase: recommendationservice_ListRecommendations (mean 1.20 -> 2.21, x1.46). [re2ob_13-06#0]
- Derived: container with the largest change in log volume: checkoutservice (76.50 -> 82.93 lines/min). [re2ob_13-06#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0613 at 2024-01-15 20:25:12 UTC; sustained deviation from 2024-01-15 20:23:12 UTC (score 53.80) [re2ob_13-01#1]
- metric anomalies: emailservice_mem — baseline median 43741184; peak 49856512 at 2024-01-15 20:27:39 UTC; sustained deviation from 2024-01-15 20:22:57 UTC (score 8.82) [re2ob_13-01#1]
- metric anomalies: currencyservice_cpu — baseline median 18.73; peak 7.69 at 2024-01-15 20:24:56 UTC; sustained deviation from 2024-01-15 20:21:35 UTC (score 4.09) [re2ob_13-01#1]
- metric anomalies: frontend_cpu — baseline median 6.62; peak 3.52 at 2024-01-15 20:31:58 UTC; sustained deviation from 2024-01-15 20:23:59 UTC (score 3.36) [re2ob_13-01#1]
- operation latency: adservice_GetAds — baseline mean 0.9; later mean 0.9107 (x1.01); peak 6.00 at 2024-01-15 20:31:15 UTC [re2ob_13-02#2]
- operation latency: cartservice_AddItem — baseline mean 0.125; later mean 0.1071 (x0.9841); peak 3.00 at 2024-01-15 20:26:00 UTC [re2ob_13-02#2]

## Timeline

- 2024-01-15 20:21 UTC — operation latency: traceservice_Export — baseline mean 0.15; later mean 0.1964 (x1.04); peak 1.00 at 2024-01-15 20:21:30 UTC; earliest sustained metric deviation: currencyservice_cpu from 2024-01-15 20:21:35 UTC [re2ob_13-02#1, re2ob_13-06#0]
- 2024-01-15 20:22 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0.1; later mean 0.1786 (x1.07); peak 1.00 at 2024-01-15 20:22:15 UTC [re2ob_13-02#1]
- 2024-01-15 20:24 UTC — metric anomalies: redis_diskio — baseline median 0; peak 41093 at 2024-01-15 20:24:10 UTC; sustained deviation from 2024-01-15 20:23:44 UTC (score 119); metric anomalies: currencyservice_cpu — baseline median 18.73; peak 7.69 at 2024-01-15 20:24:56 UTC; sustained deviation from 2024-01-15 20:21:35 UTC (score 4.09); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-15 20:24:30 UTC; operation latency: health_Check — baseline mean 0; later mean 0.0714 (x1.07); peak 1.00 at 2024-01-15 20:24:15 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.125; later mean 0.1429 (x1.02); peak 2.00 at 2024-01-15 20:24:30 UTC [re2ob_13-01#0, re2ob_13-01#1, re2ob_13-02#0, re2ob_13-02#1]
- 2024-01-15 20:25 UTC — metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0168 at 2024-01-15 20:25:19 UTC; sustained deviation from 2024-01-15 20:23:12 UTC (score 104); metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0613 at 2024-01-15 20:25:12 UTC; sustained deviation from 2024-01-15 20:23:12 UTC (score 53.80); metric anomalies: recommendationservice_cpu — baseline median 2.55; peak 1.19 at 2024-01-15 20:25:36 UTC; sustained deviation from 2024-01-15 20:25:36 UTC (score 3.05); metric anomalies: productcatalogservice_cpu — baseline median 3.41; peak 2.06 at 2024-01-15 20:25:11 UTC; sustained deviation from 2024-01-15 20:25:11 UTC (score 2.31) [re2ob_13-01#0, re2ob_13-01#1, re2ob_13-01#2]
- 2024-01-15 20:27 UTC — metric anomalies: emailservice_mem — baseline median 43741184; peak 49856512 at 2024-01-15 20:27:39 UTC; sustained deviation from 2024-01-15 20:22:57 UTC (score 8.82) [re2ob_13-01#1]
- 2024-01-15 20:28 UTC — metric anomalies: emailservice_cpu — baseline median 0.2842; peak 20.04 at 2024-01-15 20:28:23 UTC; sustained deviation from 2024-01-15 20:22:57 UTC (score 154); metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.2434 at 2024-01-15 20:28:27 UTC; sustained deviation from 2024-01-15 20:28:22 UTC (score 1.26); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0143 at 2024-01-15 20:28:33 UTC; sustained deviation from 2024-01-15 20:28:22 UTC (score 0.7383); operation latency: recommendationservice_ListRecommendations — baseline mean 1.20; later mean 2.21 (x1.46); peak 17.00 at 2024-01-15 20:28:00 UTC; operation latency: cartservice_GetCart — baseline mean 2.77; later mean 3.11 (x1.09); peak 31.00 at 2024-01-15 20:28:00 UTC [re2ob_13-01#0, re2ob_13-01#2, re2ob_13-01#3, re2ob_13-02#0]
- 2024-01-15 20:30 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0.675; later mean 0.7679 (x1.06); peak 10.00 at 2024-01-15 20:30:30 UTC [re2ob_13-02#1]
- 2024-01-15 20:31 UTC — metric anomalies: frontend_cpu — baseline median 6.62; peak 3.52 at 2024-01-15 20:31:58 UTC; sustained deviation from 2024-01-15 20:23:59 UTC (score 3.36); metric anomalies: redis_cpu — baseline median 0.2643; peak 0.1283 at 2024-01-15 20:31:33 UTC; sustained deviation from 2024-01-15 20:25:53 UTC (score 3.15); operation latency: adservice_GetAds — baseline mean 0.9; later mean 0.9107 (x1.01); peak 6.00 at 2024-01-15 20:31:15 UTC [re2ob_13-01#1, re2ob_13-01#2, re2ob_13-02#2]

## Detection: IDS Alerts

- operation latency: recommendationservice_ListRecommendations — baseline mean 1.20; later mean 2.21 (x1.46); peak 17.00 at 2024-01-15 20:28:00 UTC [re2ob_13-02#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-15 20:24:30 UTC [re2ob_13-02#0]
- operation latency: cartservice_GetCart — baseline mean 2.77; later mean 3.11 (x1.09); peak 31.00 at 2024-01-15 20:28:00 UTC [re2ob_13-02#0]
- operation latency: health_Check — baseline mean 0; later mean 0.0714 (x1.07); peak 1.00 at 2024-01-15 20:24:15 UTC [re2ob_13-02#0]

## Initial Infection Indicators

- metric anomalies: redis_cpu — baseline median 0.2643; peak 0.1283 at 2024-01-15 20:31:33 UTC; sustained deviation from 2024-01-15 20:25:53 UTC (score 3.15) [re2ob_13-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.55; peak 1.19 at 2024-01-15 20:25:36 UTC; sustained deviation from 2024-01-15 20:25:36 UTC (score 3.05) [re2ob_13-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.41; peak 2.06 at 2024-01-15 20:25:11 UTC; sustained deviation from 2024-01-15 20:25:11 UTC (score 2.31) [re2ob_13-01#2]
- metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.2434 at 2024-01-15 20:28:27 UTC; sustained deviation from 2024-01-15 20:28:22 UTC (score 1.26) [re2ob_13-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: shippingservice_ShipOrder — baseline mean 0.1; later mean 0.1786 (x1.07); peak 1.00 at 2024-01-15 20:22:15 UTC [re2ob_13-02#1]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.675; later mean 0.7679 (x1.06); peak 10.00 at 2024-01-15 20:30:30 UTC [re2ob_13-02#1]
- operation latency: traceservice_Export — baseline mean 0.15; later mean 0.1964 (x1.04); peak 1.00 at 2024-01-15 20:21:30 UTC [re2ob_13-02#1]
- operation latency: cartservice_EmptyCart — baseline mean 0.125; later mean 0.1429 (x1.02); peak 2.00 at 2024-01-15 20:24:30 UTC [re2ob_13-02#1]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_13-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation latency: adservice_GetAds — baseline mean 0.9; later mean 0.9107 (x1.01); peak 6.00 at 2024-01-15 20:31:15 UTC [re2ob_13-02#2]
2. operation latency: cartservice_AddItem — baseline mean 0.125; later mean 0.1071 (x0.9841); peak 3.00 at 2024-01-15 20:26:00 UTC [re2ob_13-02#2]
3. operation errors: no operation shows more trace errors than in its baseline [re2ob_13-03#0]
4. Not established from the available artifacts.
5. log volume: frontend — 2568 lines/min in the baseline, 2530 lines/min later [re2ob_13-04#1]
6. log volume: shippingservice — 438 lines/min in the baseline, 434 lines/min later [re2ob_13-04#1]
7. log volume: cartservice — 743 lines/min in the baseline, 736 lines/min later [re2ob_13-04#1]
8. Not established from the available artifacts.
