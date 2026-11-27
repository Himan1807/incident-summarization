# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 22 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_24-01#0]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0992 at 2024-01-16 08:07:04 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 170) [re2ob_24-01#0]
- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0019; peak 0.074 at 2024-01-16 08:06:49 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 160) [re2ob_24-01#0]
- metric anomalies: productcatalogservice_socket — baseline median 5.00; peak 51.00 at 2024-01-16 08:04:26 UTC; sustained deviation from 2024-01-16 08:03:56 UTC (score 144) [re2ob_24-01#0]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0655; peak 0.0095 at 2024-01-16 08:14:56 UTC; sustained deviation from 2024-01-16 08:04:38 UTC (score 10.46) [re2ob_24-01#3]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.075 at 2024-01-16 08:12:17 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 140) [re2ob_24-01#1]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0983 at 2024-01-16 08:11:47 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 136) [re2ob_24-01#1]
- metric anomalies: redis_diskio — baseline median 0; peak 35193 at 2024-01-16 08:06:22 UTC; sustained deviation from 2024-01-16 08:01:53 UTC (score 121) [re2ob_24-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.0556; peak 0.6531 at 2024-01-16 08:06:42 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 63.84) [re2ob_24-01#1]
- Derived: earliest sustained metric deviation: redis_diskio from 2024-01-16 08:01:53 UTC. [re2ob_24-06#0]
- Derived: metric series ranked #1 by deviation score: productcatalogservice_latency-90 (score 170). [re2ob_24-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_GetProduct (mean 0 -> 20.89, x21.89). [re2ob_24-06#0]
- Derived: container with the largest change in log volume: redis (1.00 -> 0.7143 lines/min). [re2ob_24-06#0]

## Timeline

- 2024-01-16 08:01 UTC — earliest sustained metric deviation: redis_diskio from 2024-01-16 08:01:53 UTC [re2ob_24-06#0]
- 2024-01-16 08:04 UTC — metric anomalies: productcatalogservice_socket — baseline median 5.00; peak 51.00 at 2024-01-16 08:04:26 UTC; sustained deviation from 2024-01-16 08:03:56 UTC (score 144); operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 3.04 (x4.04); peak 12.00 at 2024-01-16 08:04:15 UTC; operation latency: traceservice_Export — baseline mean 0; later mean 0.1964 (x1.20); peak 1.00 at 2024-01-16 08:04:15 UTC [re2ob_24-01#0, re2ob_24-02#0, re2ob_24-02#2]
- 2024-01-16 08:06 UTC — metric anomalies: productcatalogservice_latency-50 — baseline median 0.0019; peak 0.074 at 2024-01-16 08:06:49 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 160); metric anomalies: redis_diskio — baseline median 0; peak 35193 at 2024-01-16 08:06:22 UTC; sustained deviation from 2024-01-16 08:01:53 UTC (score 121); metric anomalies: frontend_latency-50 — baseline median 0.0556; peak 0.6531 at 2024-01-16 08:06:42 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 63.84); metric anomalies: productcatalogservice_mem — baseline median 10113024; peak 39383040 at 2024-01-16 08:06:59 UTC; sustained deviation from 2024-01-16 08:03:56 UTC (score 50.88); operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 20.89 (x21.89); peak 79.00 at 2024-01-16 08:06:30 UTC [re2ob_24-01#0, re2ob_24-01#1, re2ob_24-01#2, re2ob_24-02#0]
- 2024-01-16 08:07 UTC — metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0992 at 2024-01-16 08:07:04 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 170) [re2ob_24-01#0]
- 2024-01-16 08:08 UTC — metric anomalies: frontend_latency-90 — baseline median 0.2226; peak 0.9718 at 2024-01-16 08:08:57 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 36.53); operation latency: cartservice_AddItem — baseline mean 0.0976; later mean 0.3929 (x1.27); peak 4.00 at 2024-01-16 08:08:15 UTC [re2ob_24-01#2, re2ob_24-02#1]
- 2024-01-16 08:09 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.67; peak 20.03 at 2024-01-16 08:09:08 UTC; sustained deviation from 2024-01-16 08:04:13 UTC (score 50.90); metric anomalies: checkoutservice_latency-90 — baseline median 0.2314; peak 0.9643 at 2024-01-16 08:09:04 UTC; sustained deviation from 2024-01-16 08:04:34 UTC (score 43.81); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 08:09:45 UTC [re2ob_24-01#2, re2ob_24-02#2]
- 2024-01-16 08:11 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0983 at 2024-01-16 08:11:47 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 136); operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 4.95 (x5.95); peak 17.00 at 2024-01-16 08:11:15 UTC [re2ob_24-01#1, re2ob_24-02#0]
- 2024-01-16 08:12 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.075 at 2024-01-16 08:12:17 UTC; sustained deviation from 2024-01-16 08:04:26 UTC (score 140) [re2ob_24-01#1]
- 2024-01-16 08:14 UTC — metric anomalies: currencyservice_latency-90 — baseline median 0.0655; peak 0.0095 at 2024-01-16 08:14:56 UTC; sustained deviation from 2024-01-16 08:04:38 UTC (score 10.46); operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.3571 (x1.24); peak 4.00 at 2024-01-16 08:14:15 UTC [re2ob_24-01#3, re2ob_24-02#1]
- 2024-01-16 08:15 UTC — operation latency: frontendservice_frontend — baseline mean 0.0976; later mean 1.95 (x2.68); peak 10.00 at 2024-01-16 08:15:45 UTC; operation latency: cartservice_GetCart — baseline mean 1.51; later mean 2.70 (x1.47); peak 17.00 at 2024-01-16 08:15:15 UTC; operation latency: shippingservice_GetQuote — baseline mean 0.1951; later mean 0.5893 (x1.33); peak 5.00 at 2024-01-16 08:15:00 UTC [re2ob_24-02#0, re2ob_24-02#1]

## Detection: IDS Alerts

- metric anomalies: productcatalogservice_cpu — baseline median 3.67; peak 20.03 at 2024-01-16 08:09:08 UTC; sustained deviation from 2024-01-16 08:04:13 UTC (score 50.90) [re2ob_24-01#2]
- metric anomalies: productcatalogservice_mem — baseline median 10113024; peak 39383040 at 2024-01-16 08:06:59 UTC; sustained deviation from 2024-01-16 08:03:56 UTC (score 50.88) [re2ob_24-01#2]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2314; peak 0.9643 at 2024-01-16 08:09:04 UTC; sustained deviation from 2024-01-16 08:04:34 UTC (score 43.81) [re2ob_24-01#2]
- metric anomalies: frontend_latency-90 — baseline median 0.2226; peak 0.9718 at 2024-01-16 08:08:57 UTC; sustained deviation from 2024-01-16 08:04:11 UTC (score 36.53) [re2ob_24-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 20.89 (x21.89); peak 79.00 at 2024-01-16 08:06:30 UTC [re2ob_24-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 4.95 (x5.95); peak 17.00 at 2024-01-16 08:11:15 UTC [re2ob_24-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 3.04 (x4.04); peak 12.00 at 2024-01-16 08:04:15 UTC [re2ob_24-02#0]
- operation latency: frontendservice_frontend — baseline mean 0.0976; later mean 1.95 (x2.68); peak 10.00 at 2024-01-16 08:15:45 UTC [re2ob_24-02#0]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.1964 (x1.20); peak 1.00 at 2024-01-16 08:04:15 UTC [re2ob_24-02#2]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 08:09:45 UTC [re2ob_24-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_24-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_24-03#0]
2. operation latency: traceservice_Export — baseline mean 0; later mean 0.1964 (x1.20); peak 1.00 at 2024-01-16 08:04:15 UTC [re2ob_24-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 08:09:45 UTC [re2ob_24-02#2]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2380 lines/min in the baseline, 2104 lines/min later [re2ob_24-04#0]
6. log volume: shippingservice — 461 lines/min in the baseline, 408 lines/min later [re2ob_24-04#0]
7. log volume: frontend — 2682 lines/min in the baseline, 2402 lines/min later [re2ob_24-04#0]
8. Not established from the available artifacts.
