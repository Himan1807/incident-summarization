# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 31 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_20-01#0]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.2207 at 2024-01-16 08:49:41 UTC; sustained deviation from 2024-01-16 08:43:26 UTC (score 185) [re2ob_20-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.1755 at 2024-01-16 08:52:26 UTC; sustained deviation from 2024-01-16 08:43:32 UTC (score 172) [re2ob_20-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.2359 at 2024-01-16 08:52:26 UTC; sustained deviation from 2024-01-16 08:43:11 UTC (score 170) [re2ob_20-01#0]
- Derived: earliest sustained metric deviation: redis_cpu from 2024-01-16 08:41:34 UTC. [re2ob_20-06#0]
- Derived: metric series ranked #1 by deviation score: productcatalogservice_latency-90 (score 185). [re2ob_20-06#0]
- Derived: trace operation with the largest latency increase: checkoutservice_PlaceOrder (mean 0.0488 -> 0.3929, x1.33). [re2ob_20-06#0]
- Derived: container with the largest change in log volume: checkoutservice (89.10 -> 62.79 lines/min). [re2ob_20-06#0]
- metric anomalies: productcatalogservice_socket — baseline median 5.00; peak 4.00 at 2024-01-16 08:46:21 UTC; sustained deviation from 2024-01-16 08:46:21 UTC (score 13.33) [re2ob_20-01#3]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.0488; later mean 0.3929 (x1.33); peak 2.00 at 2024-01-16 08:43:15 UTC [re2ob_20-02#0]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.2679 (x1.27); peak 2.00 at 2024-01-16 08:46:15 UTC [re2ob_20-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 0.0893 (x1.09); peak 1.00 at 2024-01-16 08:43:15 UTC [re2ob_20-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-16 08:54:00 UTC [re2ob_20-02#0]

## Timeline

- 2024-01-16 08:41 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-16 08:41:00 UTC; operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-16 08:41:00 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC; operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC; operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC; earliest sustained metric deviation: redis_cpu from 2024-01-16 08:41:34 UTC [re2ob_20-02#1, re2ob_20-02#2, re2ob_20-06#0]
- 2024-01-16 08:43 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0.0488; later mean 0.3929 (x1.33); peak 2.00 at 2024-01-16 08:43:15 UTC; operation latency: frontendservice_frontend — baseline mean 0; later mean 0.0893 (x1.09); peak 1.00 at 2024-01-16 08:43:15 UTC [re2ob_20-02#0]
- 2024-01-16 08:45 UTC — metric anomalies: frontend_latency-90 — baseline median 0.2145; peak 2.30 at 2024-01-16 08:45:42 UTC; sustained deviation from 2024-01-16 08:43:12 UTC (score 85.64) [re2ob_20-01#1]
- 2024-01-16 08:46 UTC — metric anomalies: currencyservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 08:46:39 UTC; sustained deviation from 2024-01-16 08:46:39 UTC (score 16.67); metric anomalies: shippingservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 08:46:27 UTC; sustained deviation from 2024-01-16 08:46:27 UTC (score 16.67); metric anomalies: productcatalogservice_socket — baseline median 5.00; peak 4.00 at 2024-01-16 08:46:21 UTC; sustained deviation from 2024-01-16 08:46:21 UTC (score 13.33); operation latency: traceservice_Export — baseline mean 0; later mean 0.2679 (x1.27); peak 2.00 at 2024-01-16 08:46:15 UTC [re2ob_20-01#2, re2ob_20-01#3, re2ob_20-02#0]
- 2024-01-16 08:47 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.232; peak 2.12 at 2024-01-16 08:47:19 UTC; sustained deviation from 2024-01-16 08:43:19 UTC (score 81.64); metric anomalies: checkoutservice_latency-50 — baseline median 0.1446; peak 0.6944 at 2024-01-16 08:47:34 UTC; sustained deviation from 2024-01-16 08:43:41 UTC (score 29.39) [re2ob_20-01#2]
- 2024-01-16 08:49 UTC — metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.2207 at 2024-01-16 08:49:41 UTC; sustained deviation from 2024-01-16 08:43:26 UTC (score 185); metric anomalies: productcatalogservice_latency-50 — baseline median 0.0018; peak 0.1035 at 2024-01-16 08:49:41 UTC; sustained deviation from 2024-01-16 08:43:56 UTC (score 164) [re2ob_20-01#0, re2ob_20-01#1]
- 2024-01-16 08:51 UTC — metric anomalies: redis_diskio — baseline median 0; peak 41157 at 2024-01-16 08:51:44 UTC; sustained deviation from 2024-01-16 08:41:39 UTC (score 138) [re2ob_20-01#1]
- 2024-01-16 08:52 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.1755 at 2024-01-16 08:52:26 UTC; sustained deviation from 2024-01-16 08:43:32 UTC (score 172); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.2359 at 2024-01-16 08:52:26 UTC; sustained deviation from 2024-01-16 08:43:11 UTC (score 170) [re2ob_20-01#0]
- 2024-01-16 08:53 UTC — metric anomalies: frontend_latency-50 — baseline median 0.055; peak 1.51 at 2024-01-16 08:53:27 UTC; sustained deviation from 2024-01-16 08:43:27 UTC (score 118) [re2ob_20-01#1]
- 2024-01-16 08:54 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-16 08:54:00 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0.0244; later mean 0.0179 (x0.9936); peak 1.00 at 2024-01-16 08:54:15 UTC [re2ob_20-02#0, re2ob_20-02#1]

## Detection: IDS Alerts

- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0018; peak 0.1035 at 2024-01-16 08:49:41 UTC; sustained deviation from 2024-01-16 08:43:56 UTC (score 164) [re2ob_20-01#1]
- metric anomalies: redis_diskio — baseline median 0; peak 41157 at 2024-01-16 08:51:44 UTC; sustained deviation from 2024-01-16 08:41:39 UTC (score 138) [re2ob_20-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.055; peak 1.51 at 2024-01-16 08:53:27 UTC; sustained deviation from 2024-01-16 08:43:27 UTC (score 118) [re2ob_20-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.2145; peak 2.30 at 2024-01-16 08:45:42 UTC; sustained deviation from 2024-01-16 08:43:12 UTC (score 85.64) [re2ob_20-01#1]

## Initial Infection Indicators

- metric anomalies: checkoutservice_latency-90 — baseline median 0.232; peak 2.12 at 2024-01-16 08:47:19 UTC; sustained deviation from 2024-01-16 08:43:19 UTC (score 81.64) [re2ob_20-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1446; peak 0.6944 at 2024-01-16 08:47:34 UTC; sustained deviation from 2024-01-16 08:43:41 UTC (score 29.39) [re2ob_20-01#2]
- metric anomalies: currencyservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 08:46:39 UTC; sustained deviation from 2024-01-16 08:46:39 UTC (score 16.67) [re2ob_20-01#2]
- metric anomalies: shippingservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 08:46:27 UTC; sustained deviation from 2024-01-16 08:46:27 UTC (score 16.67) [re2ob_20-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC [re2ob_20-02#2]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_20-03#0]
2. operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC [re2ob_20-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-16 08:41:00 UTC [re2ob_20-02#2]
4. Not established from the available artifacts.
5. log volume: frontend — 2716 lines/min in the baseline, 2167 lines/min later [re2ob_20-04#1]
6. log volume: cartservice — 782 lines/min in the baseline, 624 lines/min later [re2ob_20-04#1]
7. log volume: recommendationservice — 564 lines/min in the baseline, 455 lines/min later [re2ob_20-04#1]
8. Not established from the available artifacts.
