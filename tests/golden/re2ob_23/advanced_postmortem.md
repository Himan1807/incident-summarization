# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 43 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_23-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0097; peak 2.20 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:18 UTC (score 188) [re2ob_23-01#0]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0045; peak 1.80 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:22 UTC (score 187) [re2ob_23-01#0]
- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0024; peak 0.0774 at 2024-01-15 22:30:48 UTC; sustained deviation from 2024-01-15 22:27:39 UTC (score 156) [re2ob_23-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.9028 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:48 UTC (score 43.05) [re2ob_23-01#3]
- operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 66.25 (x67.25); peak 120 at 2024-01-15 22:34:45 UTC [re2ob_23-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 21.34 (x22.34); peak 41.00 at 2024-01-15 22:38:00 UTC [re2ob_23-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 13.05 (x14.05); peak 53.00 at 2024-01-15 22:30:30 UTC [re2ob_23-02#0]
- operation latency: currencyservice_Convert — baseline mean 4.22; later mean 15.39 (x3.14); peak 47.00 at 2024-01-15 22:37:15 UTC [re2ob_23-02#0]
- metric anomalies: productcatalogservice_mem — baseline median 10268672; peak 134234112 at 2024-01-15 22:30:27 UTC; sustained deviation from 2024-01-15 22:27:13 UTC (score 124) [re2ob_23-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.1936; peak 3.31 at 2024-01-15 22:30:39 UTC; sustained deviation from 2024-01-15 22:27:37 UTC (score 102) [re2ob_23-01#1]
- metric anomalies: redis_diskio — baseline median 0; peak 39142 at 2024-01-15 22:34:20 UTC; sustained deviation from 2024-01-15 22:29:00 UTC (score 85.51) [re2ob_23-01#1]
- metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 10.00 at 2024-01-15 22:29:00 UTC; sustained deviation from 2024-01-15 22:27:13 UTC (score 55.56) [re2ob_23-01#1]

## Timeline

- 2024-01-15 22:25 UTC — earliest sustained metric deviation: redis_cpu from 2024-01-15 22:25:02 UTC [re2ob_23-06#0]
- 2024-01-15 22:28 UTC — operation latency: shippingservice_GetQuote — baseline mean 0.1951; later mean 0.9643 (x1.64); peak 10.00 at 2024-01-15 22:28:15 UTC [re2ob_23-02#1]
- 2024-01-15 22:30 UTC — metric anomalies: productcatalogservice_latency-50 — baseline median 0.0024; peak 0.0774 at 2024-01-15 22:30:48 UTC; sustained deviation from 2024-01-15 22:27:39 UTC (score 156); metric anomalies: productcatalogservice_mem — baseline median 10268672; peak 134234112 at 2024-01-15 22:30:27 UTC; sustained deviation from 2024-01-15 22:27:13 UTC (score 124); metric anomalies: frontend_latency-50 — baseline median 0.1936; peak 3.31 at 2024-01-15 22:30:39 UTC; sustained deviation from 2024-01-15 22:27:37 UTC (score 102); metric anomalies: recommendationservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 22:30:55 UTC; sustained deviation from 2024-01-15 22:30:55 UTC (score 50.00); operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 13.05 (x14.05); peak 53.00 at 2024-01-15 22:30:30 UTC; operation latency: frontendservice_frontend — baseline mean 0; later mean 2.07 (x3.07); peak 14.00 at 2024-01-15 22:30:45 UTC; operation latency: cartservice_AddItem — baseline mean 0.2195; later mean 0.6429 (x1.35); peak 6.00 at 2024-01-15 22:30:45 UTC; operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 12.00; first error after baseline at 2024-01-15 22:30:30 UTC; log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 37 lines, first at 2024-01-15 22:30:39 UTC; log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = upstream connect error or disconnect' — 9 lines, first at 2024-01-15 22:30:43 UTC; log templates: new after the baseline: 'recommendationservice product catalog address: productcatalogservice:<:NUM:>' — 1 lines, first at 2024-01-15 22:30:46 UTC; log templates: new after the baseline: 'recommendationservice listening on port: <:NUM:>' — 1 lines, first at 2024-01-15 22:30:46 UTC [re2ob_23-01#0, re2ob_23-01#1, re2ob_23-01#2, re2ob_23-02#0, re2ob_23-02#1, re2ob_23-02#2, re2ob_23-03#0, re2ob_23-04#2]
- 2024-01-15 22:31 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0097; peak 2.20 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:18 UTC (score 188); metric anomalies: productcatalogservice_latency-90 — baseline median 0.0045; peak 1.80 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:22 UTC (score 187); metric anomalies: frontend_latency-90 — baseline median 0.7167; peak 6.58 at 2024-01-15 22:31:09 UTC; sustained deviation from 2024-01-15 22:27:22 UTC (score 51.83); metric anomalies: productcatalogservice_cpu — baseline median 3.54; peak 20.97 at 2024-01-15 22:31:27 UTC; sustained deviation from 2024-01-15 22:27:13 UTC (score 50.06); metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.9028 at 2024-01-15 22:31:07 UTC; sustained deviation from 2024-01-15 22:27:48 UTC (score 43.05); operation latency: traceservice_Export — baseline mean 0; later mean 0.7321 (x1.73); peak 3.00 at 2024-01-15 22:31:30 UTC [re2ob_23-01#0, re2ob_23-01#2, re2ob_23-01#3, re2ob_23-02#1]
- 2024-01-15 22:34 UTC — metric anomalies: redis_diskio — baseline median 0; peak 39142 at 2024-01-15 22:34:20 UTC; sustained deviation from 2024-01-15 22:29:00 UTC (score 85.51); operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 66.25 (x67.25); peak 120 at 2024-01-15 22:34:45 UTC; operation latency: adservice_GetAds — baseline mean 0.3415; later mean 2.82 (x2.85); peak 16.00 at 2024-01-15 22:34:15 UTC [re2ob_23-01#1, re2ob_23-02#0, re2ob_23-02#1]
- 2024-01-15 22:35 UTC — metric anomalies: recommendationservice_mem — baseline median 45326336; peak 90517504 at 2024-01-15 22:35:18 UTC; sustained deviation from 2024-01-15 22:30:55 UTC (score 48.36) [re2ob_23-01#2]
- 2024-01-15 22:37 UTC — operation latency: currencyservice_Convert — baseline mean 4.22; later mean 15.39 (x3.14); peak 47.00 at 2024-01-15 22:37:15 UTC [re2ob_23-02#0]
- 2024-01-15 22:38 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 21.34 (x22.34); peak 41.00 at 2024-01-15 22:38:00 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 3.07; later mean 4.12 (x1.26); peak 16.00 at 2024-01-15 22:38:00 UTC [re2ob_23-02#0, re2ob_23-02#2]

## Detection: IDS Alerts



## Initial Infection Indicators

- metric anomalies: frontend_latency-90 — baseline median 0.7167; peak 6.58 at 2024-01-15 22:31:09 UTC; sustained deviation from 2024-01-15 22:27:22 UTC (score 51.83) [re2ob_23-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.54; peak 20.97 at 2024-01-15 22:31:27 UTC; sustained deviation from 2024-01-15 22:27:13 UTC (score 50.06) [re2ob_23-01#2]
- metric anomalies: recommendationservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 22:30:55 UTC; sustained deviation from 2024-01-15 22:30:55 UTC (score 50.00) [re2ob_23-01#2]
- metric anomalies: recommendationservice_mem — baseline median 45326336; peak 90517504 at 2024-01-15 22:35:18 UTC; sustained deviation from 2024-01-15 22:30:55 UTC (score 48.36) [re2ob_23-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: cartservice_AddItem — baseline mean 0.2195; later mean 0.6429 (x1.35); peak 6.00 at 2024-01-15 22:30:45 UTC [re2ob_23-02#2]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 3.07; later mean 4.12 (x1.26); peak 16.00 at 2024-01-15 22:38:00 UTC [re2ob_23-02#2]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 2.07 (x3.07); peak 14.00 at 2024-01-15 22:30:45 UTC [re2ob_23-02#1]
- operation latency: adservice_GetAds — baseline mean 0.3415; later mean 2.82 (x2.85); peak 16.00 at 2024-01-15 22:34:15 UTC [re2ob_23-02#1]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.7321 (x1.73); peak 3.00 at 2024-01-15 22:31:30 UTC [re2ob_23-02#1]
- operation latency: shippingservice_GetQuote — baseline mean 0.1951; later mean 0.9643 (x1.64); peak 10.00 at 2024-01-15 22:28:15 UTC [re2ob_23-02#1]
- operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 12.00; first error after baseline at 2024-01-15 22:30:30 UTC [re2ob_23-03#0]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 37 lines, first at 2024-01-15 22:30:39 UTC [re2ob_23-04#2]
- log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = upstream connect error or disconnect' — 9 lines, first at 2024-01-15 22:30:43 UTC [re2ob_23-04#2]
- log templates: new after the baseline: 'recommendationservice product catalog address: productcatalogservice:<:NUM:>' — 1 lines, first at 2024-01-15 22:30:46 UTC [re2ob_23-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 12.00; first error after baseline at 2024-01-15 22:30:30 UTC [re2ob_23-03#0]
2. operation latency: cartservice_AddItem — baseline mean 0.2195; later mean 0.6429 (x1.35); peak 6.00 at 2024-01-15 22:30:45 UTC [re2ob_23-02#2]
3. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 3.07; later mean 4.12 (x1.26); peak 16.00 at 2024-01-15 22:38:00 UTC [re2ob_23-02#2]
4. Not established from the available artifacts.
5. operation latency: adservice_GetAds — baseline mean 0.3415; later mean 2.82 (x2.85); peak 16.00 at 2024-01-15 22:34:15 UTC [re2ob_23-02#1]
6. operation latency: traceservice_Export — baseline mean 0; later mean 0.7321 (x1.73); peak 3.00 at 2024-01-15 22:31:30 UTC [re2ob_23-02#1]
7. operation latency: shippingservice_GetQuote — baseline mean 0.1951; later mean 0.9643 (x1.64); peak 10.00 at 2024-01-15 22:28:15 UTC [re2ob_23-02#1]
8. Not established from the available artifacts.
