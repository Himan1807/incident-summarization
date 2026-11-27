# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 17 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_30-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.2679 at 2024-01-16 09:45:11 UTC; sustained deviation from 2024-01-16 09:44:32 UTC (score 149) [re2ob_30-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 40046 at 2024-01-16 09:47:12 UTC; sustained deviation from 2024-01-16 09:42:02 UTC (score 127) [re2ob_30-01#0]
- metric anomalies: recommendationservice_socket — baseline median 4.00; peak 29.00 at 2024-01-16 09:50:12 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 124) [re2ob_30-01#0]
- Derived: earliest sustained metric deviation: redis_diskio from 2024-01-16 09:42:02 UTC. [re2ob_30-06#0]
- Derived: metric series ranked #1 by deviation score: recommendationservice_latency-50 (score 149). [re2ob_30-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_ListProducts (mean 0 -> 5.52, x6.52). [re2ob_30-06#0]
- Derived: container with the largest change in log volume: cartservice (771 -> 424 lines/min). [re2ob_30-06#0]
- metric anomalies: frontend_cpu — baseline median 8.48; peak 4.83 at 2024-01-16 09:51:48 UTC; sustained deviation from 2024-01-16 09:45:39 UTC (score 2.86) [re2ob_30-01#3]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 1.37 at 2024-01-16 09:45:32 UTC; sustained deviation from 2024-01-16 09:44:17 UTC (score 104) [re2ob_30-01#1]
- metric anomalies: recommendationservice_cpu — baseline median 2.92; peak 20.02 at 2024-01-16 09:45:49 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 55.64) [re2ob_30-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.0499; peak 0.265 at 2024-01-16 09:45:12 UTC; sustained deviation from 2024-01-16 09:44:26 UTC (score 37.34) [re2ob_30-01#1]
- metric anomalies: recommendationservice_mem — baseline median 44093440; peak 76591104 at 2024-01-16 09:47:54 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 34.45) [re2ob_30-01#1]

## Timeline

- 2024-01-16 09:42 UTC — operation latency: cartservice_EmptyCart — baseline mean 0.0732; later mean 0 (x0.9318); peak 0 at 2024-01-16 09:42:15 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0.1463; later mean 0.0536 (x0.9191); peak 1.00 at 2024-01-16 09:42:45 UTC; earliest sustained metric deviation: redis_diskio from 2024-01-16 09:42:02 UTC [re2ob_30-02#2, re2ob_30-06#0]
- 2024-01-16 09:43 UTC — operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 09:43:15 UTC [re2ob_30-02#1]
- 2024-01-16 09:44 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 4.61 (x5.61); peak 49.00 at 2024-01-16 09:44:15 UTC [re2ob_30-02#0]
- 2024-01-16 09:45 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0075; peak 0.2679 at 2024-01-16 09:45:11 UTC; sustained deviation from 2024-01-16 09:44:32 UTC (score 149); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 1.37 at 2024-01-16 09:45:32 UTC; sustained deviation from 2024-01-16 09:44:17 UTC (score 104); metric anomalies: recommendationservice_cpu — baseline median 2.92; peak 20.02 at 2024-01-16 09:45:49 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 55.64); metric anomalies: frontend_latency-50 — baseline median 0.0499; peak 0.265 at 2024-01-16 09:45:12 UTC; sustained deviation from 2024-01-16 09:44:26 UTC (score 37.34); metric anomalies: frontend_latency-90 — baseline median 0.21; peak 0.9757 at 2024-01-16 09:45:26 UTC; sustained deviation from 2024-01-16 09:44:26 UTC (score 27.98); operation latency: frontendservice_frontend — baseline mean 0.5122; later mean 3.09 (x2.70); peak 40.00 at 2024-01-16 09:45:00 UTC; operation latency: health_Check — baseline mean 0; later mean 0.0364 (x1.04); peak 1.00 at 2024-01-16 09:45:15 UTC; operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-16 09:45:45 UTC [re2ob_30-01#0, re2ob_30-01#1, re2ob_30-01#2, re2ob_30-02#0, re2ob_30-02#1]
- 2024-01-16 09:46 UTC — operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.1429 (x1.12); peak 2.00 at 2024-01-16 09:46:00 UTC [re2ob_30-02#0]
- 2024-01-16 09:47 UTC — metric anomalies: redis_diskio — baseline median 0; peak 40046 at 2024-01-16 09:47:12 UTC; sustained deviation from 2024-01-16 09:42:02 UTC (score 127); metric anomalies: recommendationservice_mem — baseline median 44093440; peak 76591104 at 2024-01-16 09:47:54 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 34.45) [re2ob_30-01#0, re2ob_30-01#1]
- 2024-01-16 09:48 UTC — metric anomalies: paymentservice_latency-50 — baseline median 0.0034; peak 0.0045 at 2024-01-16 09:48:04 UTC; sustained deviation from 2024-01-16 09:47:58 UTC (score 3.14); operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 5.52 (x6.52); peak 33.00 at 2024-01-16 09:48:45 UTC [re2ob_30-01#2, re2ob_30-02#0]
- 2024-01-16 09:49 UTC — metric anomalies: redis_cpu — baseline median 0.3218; peak 0.1483 at 2024-01-16 09:49:22 UTC; sustained deviation from 2024-01-16 09:45:45 UTC (score 3.77) [re2ob_30-01#2]
- 2024-01-16 09:50 UTC — metric anomalies: recommendationservice_socket — baseline median 4.00; peak 29.00 at 2024-01-16 09:50:12 UTC; sustained deviation from 2024-01-16 09:44:11 UTC (score 124) [re2ob_30-01#0]
- 2024-01-16 09:51 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.59; peak 1.61 at 2024-01-16 09:51:02 UTC; sustained deviation from 2024-01-16 09:51:02 UTC (score 3.64); metric anomalies: frontend_cpu — baseline median 8.48; peak 4.83 at 2024-01-16 09:51:48 UTC; sustained deviation from 2024-01-16 09:45:39 UTC (score 2.86) [re2ob_30-01#2, re2ob_30-01#3]
- 2024-01-16 09:55 UTC — operation latency: traceservice_Export — baseline mean 0.1951; later mean 0.2364 (x1.03); peak 2.00 at 2024-01-16 09:55:15 UTC [re2ob_30-02#1]

## Detection: IDS Alerts

- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 5.52 (x6.52); peak 33.00 at 2024-01-16 09:48:45 UTC [re2ob_30-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 4.61 (x5.61); peak 49.00 at 2024-01-16 09:44:15 UTC [re2ob_30-02#0]
- operation latency: frontendservice_frontend — baseline mean 0.5122; later mean 3.09 (x2.70); peak 40.00 at 2024-01-16 09:45:00 UTC [re2ob_30-02#0]

## Initial Infection Indicators



## Command-and-Control and Network Activity

- metric anomalies: frontend_latency-90 — baseline median 0.21; peak 0.9757 at 2024-01-16 09:45:26 UTC; sustained deviation from 2024-01-16 09:44:26 UTC (score 27.98) [re2ob_30-01#2]
- metric anomalies: redis_cpu — baseline median 0.3218; peak 0.1483 at 2024-01-16 09:49:22 UTC; sustained deviation from 2024-01-16 09:45:45 UTC (score 3.77) [re2ob_30-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.59; peak 1.61 at 2024-01-16 09:51:02 UTC; sustained deviation from 2024-01-16 09:51:02 UTC (score 3.64) [re2ob_30-01#2]
- metric anomalies: paymentservice_latency-50 — baseline median 0.0034; peak 0.0045 at 2024-01-16 09:48:04 UTC; sustained deviation from 2024-01-16 09:47:58 UTC (score 3.14) [re2ob_30-01#2]

## Impact Assessment

- operation latency: cartservice_EmptyCart — baseline mean 0.0732; later mean 0 (x0.9318); peak 0 at 2024-01-16 09:42:15 UTC [re2ob_30-02#2]
- operation latency: shippingservice_ShipOrder — baseline mean 0.1463; later mean 0.0536 (x0.9191); peak 1.00 at 2024-01-16 09:42:45 UTC [re2ob_30-02#2]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_30-03#0]
2. operation latency: cartservice_EmptyCart — baseline mean 0.0732; later mean 0 (x0.9318); peak 0 at 2024-01-16 09:42:15 UTC [re2ob_30-02#2]
3. operation latency: shippingservice_ShipOrder — baseline mean 0.1463; later mean 0.0536 (x0.9191); peak 1.00 at 2024-01-16 09:42:45 UTC [re2ob_30-02#2]
4. Not established from the available artifacts.
5. log volume: paymentservice — 57.00 lines/min in the baseline, 31.14 lines/min later [re2ob_30-04#1]
6. log volume: shippingservice — 439 lines/min in the baseline, 243 lines/min later [re2ob_30-04#1]
7. log volume: currencyservice — 2365 lines/min in the baseline, 1320 lines/min later [re2ob_30-04#1]
8. Not established from the available artifacts.
