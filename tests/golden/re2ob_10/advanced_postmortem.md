# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 44 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_10-01#0]
- metric anomalies: frontend-external_error — baseline median 0; peak 11.27 at 2024-01-16 07:20:07 UTC; sustained deviation from 2024-01-16 07:11:22 UTC (score 186) [re2ob_10-01#0]
- metric anomalies: frontend_error — baseline median 0; peak 11.13 at 2024-01-16 07:20:39 UTC; sustained deviation from 2024-01-16 07:11:24 UTC (score 177) [re2ob_10-01#0]
- metric anomalies: currencyservice_socket — baseline median 3.00; peak 46.00 at 2024-01-16 07:14:57 UTC; sustained deviation from 2024-01-16 07:11:44 UTC (score 154) [re2ob_10-01#0]
- metric anomalies: recommendationservice_cpu — baseline median 2.58; peak 0.1542 at 2024-01-16 07:20:22 UTC; sustained deviation from 2024-01-16 07:07:31 UTC (score 20.75) [re2ob_10-01#3]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.4946; peak 16.00 at 2024-01-16 07:17:57 UTC; sustained deviation from 2024-01-16 07:09:27 UTC (score 47.42) [re2ob_10-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.2322; peak 5.50 at 2024-01-16 07:16:07 UTC; sustained deviation from 2024-01-16 07:09:37 UTC (score 45.36) [re2ob_10-01#2]
- metric anomalies: currencyservice_cpu — baseline median 18.71; peak 0.4256 at 2024-01-16 07:14:56 UTC; sustained deviation from 2024-01-16 07:07:18 UTC (score 21.97) [re2ob_10-01#2]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0939; peak 57.00 at 2024-01-16 07:14:57 UTC; sustained deviation from 2024-01-16 07:09:52 UTC (score 21.30) [re2ob_10-01#2]
- metric anomalies: redis_diskio — baseline median 0; peak 33850 at 2024-01-16 07:11:10 UTC; sustained deviation from 2024-01-16 07:10:47 UTC (score 124) [re2ob_10-01#1]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.1861 at 2024-01-16 07:20:03 UTC; sustained deviation from 2024-01-16 07:09:22 UTC (score 109) [re2ob_10-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.4852; peak 55.08 at 2024-01-16 07:14:54 UTC; sustained deviation from 2024-01-16 07:09:24 UTC (score 61.79) [re2ob_10-01#1]
- metric anomalies: currencyservice_mem — baseline median 42074112; peak 185405440 at 2024-01-16 07:15:59 UTC; sustained deviation from 2024-01-16 07:10:03 UTC (score 54.89) [re2ob_10-01#1]

## Timeline

- 2024-01-16 07:07 UTC — earliest sustained metric deviation: productcatalogservice_cpu from 2024-01-16 07:07:01 UTC [re2ob_10-06#0]
- 2024-01-16 07:09 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.1463; later mean 6.73 (x6.75); peak 34.00 at 2024-01-16 07:09:00 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.0244; later mean 2.39 (x3.31); peak 16.00 at 2024-01-16 07:09:00 UTC [re2ob_10-02#0, re2ob_10-02#1]
- 2024-01-16 07:10 UTC — operation latency: adservice_GetAds — baseline mean 0.2195; later mean 1.00 (x1.64); peak 6.00 at 2024-01-16 07:10:30 UTC; operation latency: cartservice_AddItem — baseline mean 0.0488; later mean 0.3273 (x1.27); peak 3.00 at 2024-01-16 07:10:15 UTC [re2ob_10-02#1, re2ob_10-02#2]
- 2024-01-16 07:11 UTC — metric anomalies: redis_diskio — baseline median 0; peak 33850 at 2024-01-16 07:11:10 UTC; sustained deviation from 2024-01-16 07:10:47 UTC (score 124); operation errors: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 523; first error after baseline at 2024-01-16 07:11:15 UTC; operation errors: currencyservice_Convert — baseline mean 0; later mean 65.25; first error after baseline at 2024-01-16 07:11:15 UTC; operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 47.27; first error after baseline at 2024-01-16 07:11:15 UTC; log templates: new after the baseline: 'frontend request error could not retrieve currencies: rpc error: code = Unavailable desc = no healthy upstream' — 2057 lines, first at 2024-01-16 07:11:17 UTC; log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Internal desc = failed to prepare order: failed t' — 99 lines, first at 2024-01-16 07:11:20 UTC; log templates: new after the baseline: 'frontend request error failed to convert currency: rpc error: code = Unavailable desc = no healthy upstream' — 63 lines, first at 2024-01-16 07:11:19 UTC; log templates: new after the baseline: 'frontend request error failed to do currency conversion for product <:*:> rpc error: code = Unavailable desc = no health' — 29 lines, first at 2024-01-16 07:11:19 UTC [re2ob_10-01#1, re2ob_10-03#0, re2ob_10-04#2]
- 2024-01-16 07:12 UTC — operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 0.2653 (x1.15); peak 3.00 at 2024-01-16 07:12:15 UTC [re2ob_10-02#2]
- 2024-01-16 07:13 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 1.05; later mean 9.31 (x5.03); peak 51.00 at 2024-01-16 07:13:15 UTC; operation latency: frontendservice_frontend — baseline mean 0; later mean 3.53 (x4.53); peak 39.00 at 2024-01-16 07:13:45 UTC [re2ob_10-02#0]
- 2024-01-16 07:14 UTC — metric anomalies: currencyservice_socket — baseline median 3.00; peak 46.00 at 2024-01-16 07:14:57 UTC; sustained deviation from 2024-01-16 07:11:44 UTC (score 154); metric anomalies: frontend_latency-90 — baseline median 0.4852; peak 55.08 at 2024-01-16 07:14:54 UTC; sustained deviation from 2024-01-16 07:09:24 UTC (score 61.79); metric anomalies: currencyservice_cpu — baseline median 18.71; peak 0.4256 at 2024-01-16 07:14:56 UTC; sustained deviation from 2024-01-16 07:07:18 UTC (score 21.97); metric anomalies: currencyservice_latency-90 — baseline median 0.0939; peak 57.00 at 2024-01-16 07:14:57 UTC; sustained deviation from 2024-01-16 07:09:52 UTC (score 21.30) [re2ob_10-01#0, re2ob_10-01#1, re2ob_10-01#2]
- 2024-01-16 07:15 UTC — metric anomalies: currencyservice_mem — baseline median 42074112; peak 185405440 at 2024-01-16 07:15:59 UTC; sustained deviation from 2024-01-16 07:10:03 UTC (score 54.89); operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4364 (x1.44); peak 8.00 at 2024-01-16 07:15:30 UTC [re2ob_10-01#1, re2ob_10-02#1]
- 2024-01-16 07:16 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.2322; peak 5.50 at 2024-01-16 07:16:07 UTC; sustained deviation from 2024-01-16 07:09:37 UTC (score 45.36) [re2ob_10-01#2]
- 2024-01-16 07:17 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.4946; peak 16.00 at 2024-01-16 07:17:57 UTC; sustained deviation from 2024-01-16 07:09:27 UTC (score 47.42) [re2ob_10-01#2]
- 2024-01-16 07:18 UTC — operation latency: currencyservice_Convert — baseline mean 0; later mean 5.35 (x6.35); peak 27.00 at 2024-01-16 07:18:30 UTC [re2ob_10-02#0]
- 2024-01-16 07:19 UTC — operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 2.20 (x3.20); peak 44.00 at 2024-01-16 07:19:00 UTC [re2ob_10-02#1]
- 2024-01-16 07:20 UTC — metric anomalies: frontend-external_error — baseline median 0; peak 11.27 at 2024-01-16 07:20:07 UTC; sustained deviation from 2024-01-16 07:11:22 UTC (score 186); metric anomalies: frontend_error — baseline median 0; peak 11.13 at 2024-01-16 07:20:39 UTC; sustained deviation from 2024-01-16 07:11:24 UTC (score 177); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.1861 at 2024-01-16 07:20:03 UTC; sustained deviation from 2024-01-16 07:09:22 UTC (score 109); metric anomalies: recommendationservice_cpu — baseline median 2.58; peak 0.1542 at 2024-01-16 07:20:22 UTC; sustained deviation from 2024-01-16 07:07:31 UTC (score 20.75) [re2ob_10-01#0, re2ob_10-01#1, re2ob_10-01#3]

## Detection: IDS Alerts



## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: cartservice_AddItem — baseline mean 0.0488; later mean 0.3273 (x1.27); peak 3.00 at 2024-01-16 07:10:15 UTC [re2ob_10-02#2]
- operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 0.2653 (x1.15); peak 3.00 at 2024-01-16 07:12:15 UTC [re2ob_10-02#2]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.1463; later mean 6.73 (x6.75); peak 34.00 at 2024-01-16 07:09:00 UTC [re2ob_10-02#0]
- operation latency: currencyservice_Convert — baseline mean 0; later mean 5.35 (x6.35); peak 27.00 at 2024-01-16 07:18:30 UTC [re2ob_10-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 1.05; later mean 9.31 (x5.03); peak 51.00 at 2024-01-16 07:13:15 UTC [re2ob_10-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 3.53 (x4.53); peak 39.00 at 2024-01-16 07:13:45 UTC [re2ob_10-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.0244; later mean 2.39 (x3.31); peak 16.00 at 2024-01-16 07:09:00 UTC [re2ob_10-02#1]
- operation latency: adservice_GetAds — baseline mean 0.2195; later mean 1.00 (x1.64); peak 6.00 at 2024-01-16 07:10:30 UTC [re2ob_10-02#1]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4364 (x1.44); peak 8.00 at 2024-01-16 07:15:30 UTC [re2ob_10-02#1]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'frontend request error could not retrieve currencies: rpc error: code = Unavailable desc = no healthy upstream' — 2057 lines, first at 2024-01-16 07:11:17 UTC [re2ob_10-04#2]
- log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Internal desc = failed to prepare order: failed t' — 99 lines, first at 2024-01-16 07:11:20 UTC [re2ob_10-04#2]
- log templates: new after the baseline: 'frontend request error failed to convert currency: rpc error: code = Unavailable desc = no healthy upstream' — 63 lines, first at 2024-01-16 07:11:19 UTC [re2ob_10-04#2]
- log templates: new after the baseline: 'frontend request error failed to do currency conversion for product <:*:> rpc error: code = Unavailable desc = no health' — 29 lines, first at 2024-01-16 07:11:19 UTC [re2ob_10-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation latency: cartservice_AddItem — baseline mean 0.0488; later mean 0.3273 (x1.27); peak 3.00 at 2024-01-16 07:10:15 UTC [re2ob_10-02#2]
2. operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 0.2653 (x1.15); peak 3.00 at 2024-01-16 07:12:15 UTC [re2ob_10-02#2]
3. log volume: recommendationservice — 554 lines/min in the baseline, 258 lines/min later [re2ob_10-04#1]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2296 lines/min in the baseline, 1116 lines/min later [re2ob_10-04#1]
6. log volume: cartservice — 761 lines/min in the baseline, 390 lines/min later [re2ob_10-04#1]
7. operation latency: recommendationservice_ListRecommendations — baseline mean 0.1463; later mean 6.73 (x6.75); peak 34.00 at 2024-01-16 07:09:00 UTC [re2ob_10-02#0]
8. Not established from the available artifacts.
