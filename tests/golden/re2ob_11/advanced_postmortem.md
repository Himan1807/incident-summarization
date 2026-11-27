# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 26 of 70 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_11-01#0]
- metric anomalies: currencyservice_latency-50 — baseline median 0.0042; peak 0.1337 at 2024-01-17 04:16:51 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 114) [re2ob_11-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 39147 at 2024-01-17 04:08:41 UTC; sustained deviation from 2024-01-17 04:08:16 UTC (score 110) [re2ob_11-01#0]
- metric anomalies: currencyservice_mem — baseline median 44822528; peak 268439552 at 2024-01-17 04:14:51 UTC; sustained deviation from 2024-01-17 04:08:59 UTC (score 97.72) [re2ob_11-01#0]
- Derived: earliest sustained metric deviation: currencyservice_cpu from 2024-01-17 04:07:07 UTC. [re2ob_11-06#0]
- Derived: metric series ranked #1 by deviation score: currencyservice_latency-50 (score 114). [re2ob_11-06#0]
- Derived: trace operation with the largest latency increase: currencyservice_Convert (mean 0 -> 21.89, x22.89). [re2ob_11-06#0]
- Derived: container with the largest change in log volume: adservice (457 -> 398 lines/min). [re2ob_11-06#0]
- metric anomalies: cartservice_latency-50 — baseline median 0.0034; peak 0.0059 at 2024-01-17 04:14:23 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 16.69) [re2ob_11-01#3]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 4.00 at 2024-01-17 04:18:00 UTC [re2ob_11-02#2]
- operation latency: cartservice_AddItem — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-17 04:10:15 UTC [re2ob_11-02#2]
- operation latency: currencyservice_Convert — baseline mean 0; later mean 21.89 (x22.89); peak 60.00 at 2024-01-17 04:08:45 UTC [re2ob_11-02#0]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 21.64 (x22.64); peak 38.00 at 2024-01-17 04:14:00 UTC [re2ob_11-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 6.55 (x7.55); peak 24.00 at 2024-01-17 04:19:15 UTC [re2ob_11-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.439; later mean 7.16 (x5.67); peak 24.00 at 2024-01-17 04:09:15 UTC [re2ob_11-02#0]

## Timeline

- 2024-01-17 04:07 UTC — earliest sustained metric deviation: currencyservice_cpu from 2024-01-17 04:07:07 UTC [re2ob_11-06#0]
- 2024-01-17 04:08 UTC — metric anomalies: redis_diskio — baseline median 0; peak 39147 at 2024-01-17 04:08:41 UTC; sustained deviation from 2024-01-17 04:08:16 UTC (score 110); metric anomalies: frontend_socket — baseline median 26.00; peak 37.00 at 2024-01-17 04:08:48 UTC; sustained deviation from 2024-01-17 04:08:48 UTC (score 24.72); operation latency: currencyservice_Convert — baseline mean 0; later mean 21.89 (x22.89); peak 60.00 at 2024-01-17 04:08:45 UTC [re2ob_11-01#0, re2ob_11-01#2, re2ob_11-02#0]
- 2024-01-17 04:09 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0095; peak 0.0238 at 2024-01-17 04:09:36 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 54.84); operation latency: recommendationservice_ListRecommendations — baseline mean 0.439; later mean 7.16 (x5.67); peak 24.00 at 2024-01-17 04:09:15 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.0244; later mean 2.54 (x3.45); peak 11.00 at 2024-01-17 04:09:15 UTC [re2ob_11-01#1, re2ob_11-02#0, re2ob_11-02#1]
- 2024-01-17 04:10 UTC — operation latency: cartservice_AddItem — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-17 04:10:15 UTC [re2ob_11-02#2]
- 2024-01-17 04:14 UTC — metric anomalies: currencyservice_mem — baseline median 44822528; peak 268439552 at 2024-01-17 04:14:51 UTC; sustained deviation from 2024-01-17 04:08:59 UTC (score 97.72); metric anomalies: cartservice_latency-50 — baseline median 0.0034; peak 0.0059 at 2024-01-17 04:14:23 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 16.69); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 21.64 (x22.64); peak 38.00 at 2024-01-17 04:14:00 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 3.00; later mean 14.91 (x3.98); peak 45.00 at 2024-01-17 04:14:30 UTC [re2ob_11-01#0, re2ob_11-01#3, re2ob_11-02#0, re2ob_11-02#1]
- 2024-01-17 04:16 UTC — metric anomalies: currencyservice_latency-50 — baseline median 0.0042; peak 0.1337 at 2024-01-17 04:16:51 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 114); metric anomalies: currencyservice_latency-90 — baseline median 0.07; peak 0.8346 at 2024-01-17 04:16:49 UTC; sustained deviation from 2024-01-17 04:09:04 UTC (score 77.69); metric anomalies: frontend_latency-90 — baseline median 0.2272; peak 2.30 at 2024-01-17 04:16:51 UTC; sustained deviation from 2024-01-17 04:09:04 UTC (score 74.40); metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-17 04:16:04 UTC; sustained deviation from 2024-01-17 04:08:59 UTC (score 42.86) [re2ob_11-01#0, re2ob_11-01#1, re2ob_11-01#2]
- 2024-01-17 04:17 UTC — metric anomalies: frontend_latency-50 — baseline median 0.0618; peak 0.6111 at 2024-01-17 04:17:06 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 47.00); operation latency: cartservice_GetCart — baseline mean 0.561; later mean 2.95 (x2.53); peak 25.00 at 2024-01-17 04:17:30 UTC [re2ob_11-01#2, re2ob_11-02#1]
- 2024-01-17 04:18 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.2386; peak 3.67 at 2024-01-17 04:18:36 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 55.38); metric anomalies: checkoutservice_latency-50 — baseline median 0.1395; peak 1.54 at 2024-01-17 04:18:53 UTC; sustained deviation from 2024-01-17 04:09:38 UTC (score 27.41); operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 4.00 at 2024-01-17 04:18:00 UTC [re2ob_11-01#1, re2ob_11-01#2, re2ob_11-02#2]
- 2024-01-17 04:19 UTC — operation latency: frontendservice_frontend — baseline mean 0; later mean 6.55 (x7.55); peak 24.00 at 2024-01-17 04:19:15 UTC [re2ob_11-02#0]
- 2024-01-17 04:20 UTC — operation latency: adservice_GetAds — baseline mean 0.7073; later mean 2.48 (x2.04); peak 8.00 at 2024-01-17 04:20:00 UTC [re2ob_11-02#1]

## Detection: IDS Alerts

- metric anomalies: currencyservice_latency-90 — baseline median 0.07; peak 0.8346 at 2024-01-17 04:16:49 UTC; sustained deviation from 2024-01-17 04:09:04 UTC (score 77.69) [re2ob_11-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.2272; peak 2.30 at 2024-01-17 04:16:51 UTC; sustained deviation from 2024-01-17 04:09:04 UTC (score 74.40) [re2ob_11-01#1]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2386; peak 3.67 at 2024-01-17 04:18:36 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 55.38) [re2ob_11-01#1]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0095; peak 0.0238 at 2024-01-17 04:09:36 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 54.84) [re2ob_11-01#1]

## Initial Infection Indicators

- metric anomalies: frontend_latency-50 — baseline median 0.0618; peak 0.6111 at 2024-01-17 04:17:06 UTC; sustained deviation from 2024-01-17 04:09:06 UTC (score 47.00) [re2ob_11-01#2]
- metric anomalies: currencyservice_socket — baseline median 3.00; peak 8.00 at 2024-01-17 04:16:04 UTC; sustained deviation from 2024-01-17 04:08:59 UTC (score 42.86) [re2ob_11-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1395; peak 1.54 at 2024-01-17 04:18:53 UTC; sustained deviation from 2024-01-17 04:09:38 UTC (score 27.41) [re2ob_11-01#2]
- metric anomalies: frontend_socket — baseline median 26.00; peak 37.00 at 2024-01-17 04:08:48 UTC; sustained deviation from 2024-01-17 04:08:48 UTC (score 24.72) [re2ob_11-01#2]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_11-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_11-03#0]
2. operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 4.00 at 2024-01-17 04:18:00 UTC [re2ob_11-02#2]
3. operation latency: cartservice_AddItem — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-17 04:10:15 UTC [re2ob_11-02#2]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2372 lines/min in the baseline, 2087 lines/min later [re2ob_11-04#0]
6. log volume: frontend — 2646 lines/min in the baseline, 2350 lines/min later [re2ob_11-04#0]
7. log volume: recommendationservice — 559 lines/min in the baseline, 498 lines/min later [re2ob_11-04#0]
8. Not established from the available artifacts.
