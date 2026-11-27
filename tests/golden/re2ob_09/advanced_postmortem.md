# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 26 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_09-01#0]
- metric anomalies: currencyservice_diskio — no data in the baseline; series appears at 2024-01-16 06:31:33 UTC (first value 1491095689); peak 5061175758 at 2024-01-16 06:34:26 UTC [re2ob_09-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 50264 at 2024-01-16 06:36:01 UTC; sustained deviation from 2024-01-16 06:30:38 UTC (score 110) [re2ob_09-01#0]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0945; peak 0.9265 at 2024-01-16 06:40:12 UTC; sustained deviation from 2024-01-16 06:31:22 UTC (score 106) [re2ob_09-01#0]
- Derived: earliest sustained metric deviation: shippingservice_cpu from 2024-01-16 06:29:12 UTC. [re2ob_09-06#0]
- Derived: metric series ranked #1 by deviation score: redis_diskio (score 110). [re2ob_09-06#0]
- Derived: metric series without baseline data that appears during the capture: currencyservice_diskio (from 2024-01-16 06:31:33 UTC). [re2ob_09-06#0]
- Derived: trace operation with the largest latency increase: currencyservice_Convert (mean 0 -> 26.62, x27.62). [re2ob_09-06#0]
- metric anomalies: currencyservice_latency-50 — baseline median 0.0576; peak 0.3694 at 2024-01-16 06:33:12 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 61.73) [re2ob_09-01#1]
- metric anomalies: currencyservice_mem — baseline median 41283584; peak 134209536 at 2024-01-16 06:43:00 UTC; sustained deviation from 2024-01-16 06:31:21 UTC (score 48.33) [re2ob_09-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.171; peak 0.9202 at 2024-01-16 06:43:09 UTC; sustained deviation from 2024-01-16 06:31:39 UTC (score 44.95) [re2ob_09-01#1]
- metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-16 06:31:21 UTC; sustained deviation from 2024-01-16 06:31:21 UTC (score 42.86) [re2ob_09-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.5181; peak 3.73 at 2024-01-16 06:40:39 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 30.63) [re2ob_09-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.2366; peak 2.50 at 2024-01-16 06:41:27 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 27.35) [re2ob_09-01#2]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0168 at 2024-01-16 06:41:48 UTC; sustained deviation from 2024-01-16 06:32:22 UTC (score 22.47) [re2ob_09-01#2]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.5333; peak 4.50 at 2024-01-16 06:41:27 UTC; sustained deviation from 2024-01-16 06:31:22 UTC (score 22.30) [re2ob_09-01#2]

## Timeline

- 2024-01-16 06:29 UTC — earliest sustained metric deviation: shippingservice_cpu from 2024-01-16 06:29:12 UTC [re2ob_09-06#0]
- 2024-01-16 06:31 UTC — metric anomalies: currencyservice_diskio — no data in the baseline; series appears at 2024-01-16 06:31:33 UTC (first value 1491095689); peak 5061175758 at 2024-01-16 06:34:26 UTC; metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-16 06:31:21 UTC; sustained deviation from 2024-01-16 06:31:21 UTC (score 42.86); metric series without baseline data that appears during the capture: currencyservice_diskio (from 2024-01-16 06:31:33 UTC) [re2ob_09-01#0, re2ob_09-01#1, re2ob_09-06#0]
- 2024-01-16 06:32 UTC — operation latency: currencyservice_Convert — baseline mean 0; later mean 26.62 (x27.62); peak 126 at 2024-01-16 06:32:45 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 12.43 (x13.43); peak 54.00 at 2024-01-16 06:32:45 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 3.95; later mean 15.00 (x3.23); peak 75.00 at 2024-01-16 06:32:45 UTC [re2ob_09-02#0]
- 2024-01-16 06:33 UTC — metric anomalies: currencyservice_latency-50 — baseline median 0.0576; peak 0.3694 at 2024-01-16 06:33:12 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 61.73); operation latency: adservice_GetAds — baseline mean 0.6341; later mean 1.18 (x1.33); peak 6.00 at 2024-01-16 06:33:30 UTC [re2ob_09-01#1, re2ob_09-02#1]
- 2024-01-16 06:35 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.8537; later mean 2.50 (x1.89); peak 12.00 at 2024-01-16 06:35:45 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.3171; later mean 1.25 (x1.71); peak 8.00 at 2024-01-16 06:35:45 UTC [re2ob_09-02#1]
- 2024-01-16 06:36 UTC — metric anomalies: redis_diskio — baseline median 0; peak 50264 at 2024-01-16 06:36:01 UTC; sustained deviation from 2024-01-16 06:30:38 UTC (score 110); operation latency: shippingservice_GetQuote — baseline mean 0.2927; later mean 0.6607 (x1.28); peak 3.00 at 2024-01-16 06:36:45 UTC [re2ob_09-01#0, re2ob_09-02#2]
- 2024-01-16 06:39 UTC — operation latency: frontendservice_frontend — baseline mean 0; later mean 8.75 (x9.75); peak 27.00 at 2024-01-16 06:39:45 UTC [re2ob_09-02#0]
- 2024-01-16 06:40 UTC — metric anomalies: currencyservice_latency-90 — baseline median 0.0945; peak 0.9265 at 2024-01-16 06:40:12 UTC; sustained deviation from 2024-01-16 06:31:22 UTC (score 106); metric anomalies: frontend_latency-90 — baseline median 0.5181; peak 3.73 at 2024-01-16 06:40:39 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 30.63); operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.5 (x1.50); peak 6.00 at 2024-01-16 06:40:30 UTC; operation latency: cartservice_AddItem — baseline mean 0.1463; later mean 0.4464 (x1.26); peak 5.00 at 2024-01-16 06:40:15 UTC [re2ob_09-01#0, re2ob_09-01#2, re2ob_09-02#1, re2ob_09-02#2]
- 2024-01-16 06:41 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.2366; peak 2.50 at 2024-01-16 06:41:27 UTC; sustained deviation from 2024-01-16 06:31:37 UTC (score 27.35); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0168 at 2024-01-16 06:41:48 UTC; sustained deviation from 2024-01-16 06:32:22 UTC (score 22.47); metric anomalies: checkoutservice_latency-90 — baseline median 0.5333; peak 4.50 at 2024-01-16 06:41:27 UTC; sustained deviation from 2024-01-16 06:31:22 UTC (score 22.30); metric anomalies: frontend_socket — baseline median 34.00; peak 44.00 at 2024-01-16 06:41:38 UTC; sustained deviation from 2024-01-16 06:32:52 UTC (score 17.86) [re2ob_09-01#2, re2ob_09-01#3]
- 2024-01-16 06:43 UTC — metric anomalies: currencyservice_mem — baseline median 41283584; peak 134209536 at 2024-01-16 06:43:00 UTC; sustained deviation from 2024-01-16 06:31:21 UTC (score 48.33); metric anomalies: frontend_latency-50 — baseline median 0.171; peak 0.9202 at 2024-01-16 06:43:09 UTC; sustained deviation from 2024-01-16 06:31:39 UTC (score 44.95) [re2ob_09-01#1]

## Detection: IDS Alerts



## Initial Infection Indicators

- metric anomalies: frontend_socket — baseline median 34.00; peak 44.00 at 2024-01-16 06:41:38 UTC; sustained deviation from 2024-01-16 06:32:52 UTC (score 17.86) [re2ob_09-01#3]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: shippingservice_GetQuote — baseline mean 0.2927; later mean 0.6607 (x1.28); peak 3.00 at 2024-01-16 06:36:45 UTC [re2ob_09-02#2]
- operation latency: cartservice_AddItem — baseline mean 0.1463; later mean 0.4464 (x1.26); peak 5.00 at 2024-01-16 06:40:15 UTC [re2ob_09-02#2]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.8537; later mean 2.50 (x1.89); peak 12.00 at 2024-01-16 06:35:45 UTC [re2ob_09-02#1]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.3171; later mean 1.25 (x1.71); peak 8.00 at 2024-01-16 06:35:45 UTC [re2ob_09-02#1]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.5 (x1.50); peak 6.00 at 2024-01-16 06:40:30 UTC [re2ob_09-02#1]
- operation latency: adservice_GetAds — baseline mean 0.6341; later mean 1.18 (x1.33); peak 6.00 at 2024-01-16 06:33:30 UTC [re2ob_09-02#1]
- operation latency: currencyservice_Convert — baseline mean 0; later mean 26.62 (x27.62); peak 126 at 2024-01-16 06:32:45 UTC [re2ob_09-02#0]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 12.43 (x13.43); peak 54.00 at 2024-01-16 06:32:45 UTC [re2ob_09-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 8.75 (x9.75); peak 27.00 at 2024-01-16 06:39:45 UTC [re2ob_09-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 3.95; later mean 15.00 (x3.23); peak 75.00 at 2024-01-16 06:32:45 UTC [re2ob_09-02#0]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_09-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation latency: shippingservice_GetQuote — baseline mean 0.2927; later mean 0.6607 (x1.28); peak 3.00 at 2024-01-16 06:36:45 UTC [re2ob_09-02#2]
2. operation latency: cartservice_AddItem — baseline mean 0.1463; later mean 0.4464 (x1.26); peak 5.00 at 2024-01-16 06:40:15 UTC [re2ob_09-02#2]
3. operation errors: no operation shows more trace errors than in its baseline [re2ob_09-03#0]
4. Not established from the available artifacts.
5. log volume: cartservice — 757 lines/min in the baseline, 632 lines/min later [re2ob_09-04#1]
6. log volume: currencyservice — 2306 lines/min in the baseline, 1934 lines/min later [re2ob_09-04#1]
7. log volume: shippingservice — 441 lines/min in the baseline, 370 lines/min later [re2ob_09-04#1]
8. Not established from the available artifacts.
