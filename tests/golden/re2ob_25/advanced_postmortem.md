# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- Derived: earliest sustained metric deviation: frontend_cpu from 2024-01-15 19:07:37 UTC. [re2ob_25-06#0]
- Derived: metric series ranked #1 by deviation score: recommendationservice_latency-90 (score 135). [re2ob_25-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_ListProducts (mean 0.0488 -> 29.88, x29.44). [re2ob_25-06#0]
- Derived: container with the largest change in log volume: paymentservice (53.20 -> 55.71 lines/min). [re2ob_25-06#0]
- metric anomalies: 15 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_25-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.098 at 2024-01-15 19:12:19 UTC; sustained deviation from 2024-01-15 19:09:44 UTC (score 135) [re2ob_25-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 35861 at 2024-01-15 19:19:00 UTC; sustained deviation from 2024-01-15 19:08:21 UTC (score 131) [re2ob_25-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0716 at 2024-01-15 19:10:19 UTC; sustained deviation from 2024-01-15 19:09:59 UTC (score 130) [re2ob_25-01#0]
- metric anomalies: currencyservice_cpu — baseline median 18.77; peak 11.29 at 2024-01-15 19:15:36 UTC; sustained deviation from 2024-01-15 19:10:39 UTC (score 4.06) [re2ob_25-01#2]
- metric anomalies: frontend_cpu — baseline median 6.60; peak 2.71 at 2024-01-15 19:07:42 UTC; sustained deviation from 2024-01-15 19:07:37 UTC (score 3.83) [re2ob_25-01#2]
- metric anomalies: redis_cpu — baseline median 0.265; peak 0.1359 at 2024-01-15 19:10:12 UTC; sustained deviation from 2024-01-15 19:09:08 UTC (score 2.85) [re2ob_25-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 2.85; peak 1.37 at 2024-01-15 19:17:00 UTC; sustained deviation from 2024-01-15 19:10:59 UTC (score 2.83) [re2ob_25-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.50; peak 20.02 at 2024-01-15 19:18:24 UTC; sustained deviation from 2024-01-15 19:09:37 UTC (score 71.53) [re2ob_25-01#1]
- metric anomalies: recommendationservice_mem — baseline median 44298240; peak 51240960 at 2024-01-15 19:20:16 UTC; sustained deviation from 2024-01-15 19:09:37 UTC (score 8.80) [re2ob_25-01#1]
- metric anomalies: frontend_socket — baseline median 27.00; peak 30.00 at 2024-01-15 19:11:46 UTC; sustained deviation from 2024-01-15 19:11:46 UTC (score 7.14) [re2ob_25-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.1831; peak 0.2827 at 2024-01-15 19:10:20 UTC; sustained deviation from 2024-01-15 19:10:19 UTC (score 6.25) [re2ob_25-01#1]

## Timeline

- 2024-01-15 19:07 UTC — metric anomalies: frontend_cpu — baseline median 6.60; peak 2.71 at 2024-01-15 19:07:42 UTC; sustained deviation from 2024-01-15 19:07:37 UTC (score 3.83); operation latency: shippingservice_GetQuote — baseline mean 0.1951; later mean 0.1429 (x0.9563); peak 2.00 at 2024-01-15 19:07:45 UTC; earliest sustained metric deviation: frontend_cpu from 2024-01-15 19:07:37 UTC [re2ob_25-01#2, re2ob_25-02#1, re2ob_25-06#0]
- 2024-01-15 19:09 UTC — metric anomalies: adservice_diskio — baseline median 57867; peak 228499 at 2024-01-15 19:09:57 UTC; sustained deviation from 2024-01-15 19:09:48 UTC (score 1.51) [re2ob_25-01#3]
- 2024-01-15 19:10 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0716 at 2024-01-15 19:10:19 UTC; sustained deviation from 2024-01-15 19:09:59 UTC (score 130); metric anomalies: frontend_latency-50 — baseline median 0.1831; peak 0.2827 at 2024-01-15 19:10:20 UTC; sustained deviation from 2024-01-15 19:10:19 UTC (score 6.25); metric anomalies: redis_cpu — baseline median 0.265; peak 0.1359 at 2024-01-15 19:10:12 UTC; sustained deviation from 2024-01-15 19:09:08 UTC (score 2.85); operation latency: cartservice_AddItem — baseline mean 0.2683; later mean 0.3036 (x1.03); peak 2.00 at 2024-01-15 19:10:45 UTC [re2ob_25-01#0, re2ob_25-01#1, re2ob_25-01#2, re2ob_25-02#0]
- 2024-01-15 19:11 UTC — metric anomalies: frontend_socket — baseline median 27.00; peak 30.00 at 2024-01-15 19:11:46 UTC; sustained deviation from 2024-01-15 19:11:46 UTC (score 7.14); operation latency: currencyservice_Convert — baseline mean 7.02; later mean 7.32 (x1.04); peak 38.00 at 2024-01-15 19:11:30 UTC; operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0179 (x0.9936); peak 1.00 at 2024-01-15 19:11:45 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.0714 (x0.955); peak 1.00 at 2024-01-15 19:11:00 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 4.73; later mean 4.45 (x0.9502); peak 21.00 at 2024-01-15 19:11:30 UTC [re2ob_25-01#1, re2ob_25-02#0, re2ob_25-02#1, re2ob_25-02#2]
- 2024-01-15 19:12 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.098 at 2024-01-15 19:12:19 UTC; sustained deviation from 2024-01-15 19:09:44 UTC (score 135) [re2ob_25-01#0]
- 2024-01-15 19:15 UTC — metric anomalies: currencyservice_cpu — baseline median 18.77; peak 11.29 at 2024-01-15 19:15:36 UTC; sustained deviation from 2024-01-15 19:10:39 UTC (score 4.06) [re2ob_25-01#2]
- 2024-01-15 19:16 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.0976; later mean 3.93 (x4.49); peak 22.00 at 2024-01-15 19:16:00 UTC [re2ob_25-02#0]
- 2024-01-15 19:18 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.50; peak 20.02 at 2024-01-15 19:18:24 UTC; sustained deviation from 2024-01-15 19:09:37 UTC (score 71.53); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-15 19:18:15 UTC [re2ob_25-01#1, re2ob_25-02#1]
- 2024-01-15 19:19 UTC — metric anomalies: redis_diskio — baseline median 0; peak 35861 at 2024-01-15 19:19:00 UTC; sustained deviation from 2024-01-15 19:08:21 UTC (score 131); operation latency: health_Check — baseline mean 0.0244; later mean 0.0179 (x0.9936); peak 1.00 at 2024-01-15 19:19:45 UTC [re2ob_25-01#0, re2ob_25-02#1]
- 2024-01-15 19:20 UTC — metric anomalies: recommendationservice_mem — baseline median 44298240; peak 51240960 at 2024-01-15 19:20:16 UTC; sustained deviation from 2024-01-15 19:09:37 UTC (score 8.80); operation latency: productcatalogservice_ListProducts — baseline mean 0.0488; later mean 29.88 (x29.44); peak 48.00 at 2024-01-15 19:20:45 UTC [re2ob_25-01#1, re2ob_25-02#0]

## Detection: IDS Alerts

- operation latency: productcatalogservice_ListProducts — baseline mean 0.0488; later mean 29.88 (x29.44); peak 48.00 at 2024-01-15 19:20:45 UTC [re2ob_25-02#0]
- operation latency: currencyservice_Convert — baseline mean 7.02; later mean 7.32 (x1.04); peak 38.00 at 2024-01-15 19:11:30 UTC [re2ob_25-02#0]
- operation latency: cartservice_AddItem — baseline mean 0.2683; later mean 0.3036 (x1.03); peak 2.00 at 2024-01-15 19:10:45 UTC [re2ob_25-02#0]

## Initial Infection Indicators

- metric anomalies: adservice_diskio — baseline median 57867; peak 228499 at 2024-01-15 19:09:57 UTC; sustained deviation from 2024-01-15 19:09:48 UTC (score 1.51) [re2ob_25-01#3]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.0714 (x0.955); peak 1.00 at 2024-01-15 19:11:00 UTC [re2ob_25-02#2]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 4.73; later mean 4.45 (x0.9502); peak 21.00 at 2024-01-15 19:11:30 UTC [re2ob_25-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_25-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_25-03#0]
2. operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.0714 (x0.955); peak 1.00 at 2024-01-15 19:11:00 UTC [re2ob_25-02#2]
3. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 4.73; later mean 4.45 (x0.9502); peak 21.00 at 2024-01-15 19:11:30 UTC [re2ob_25-02#2]
4. Not established from the available artifacts.
5. log volume: frontend — 2578 lines/min in the baseline, 2548 lines/min later [re2ob_25-04#1]
6. log volume: shippingservice — 429 lines/min in the baseline, 434 lines/min later [re2ob_25-04#1]
7. log volume: adservice — 432 lines/min in the baseline, 428 lines/min later [re2ob_25-04#1]
8. Not established from the available artifacts.
