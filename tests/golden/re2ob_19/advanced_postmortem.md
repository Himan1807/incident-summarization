# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 17 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_19-01#0]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0043; peak 0.0499 at 2024-01-15 17:47:47 UTC; sustained deviation from 2024-01-15 17:42:51 UTC (score 140) [re2ob_19-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 25498 at 2024-01-15 17:52:57 UTC; sustained deviation from 2024-01-15 17:42:44 UTC (score 138) [re2ob_19-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0095; peak 0.0732 at 2024-01-15 17:47:47 UTC; sustained deviation from 2024-01-15 17:42:36 UTC (score 97.49) [re2ob_19-01#0]
- metric anomalies: redis_cpu — baseline median 0.2867; peak 0.1397 at 2024-01-15 17:47:38 UTC; sustained deviation from 2024-01-15 17:41:40 UTC (score 3.28) [re2ob_19-01#3]
- Derived: earliest sustained metric deviation: currencyservice_cpu from 2024-01-15 17:40:40 UTC. [re2ob_19-06#0]
- Derived: metric series ranked #1 by deviation score: productcatalogservice_latency-90 (score 140). [re2ob_19-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_GetProduct (mean 0.439 -> 93.02, x65.33). [re2ob_19-06#0]
- Derived: container with the largest change in log volume: currencyservice (2402 -> 2260 lines/min). [re2ob_19-06#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0071; peak 0.0332 at 2024-01-15 17:53:06 UTC; sustained deviation from 2024-01-15 17:43:02 UTC (score 72.28) [re2ob_19-01#1]
- metric anomalies: productcatalogservice_cpu — baseline median 2.84; peak 20.02 at 2024-01-15 17:43:44 UTC; sustained deviation from 2024-01-15 17:42:44 UTC (score 59.63) [re2ob_19-01#1]
- metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 6.00 at 2024-01-15 17:42:26 UTC; sustained deviation from 2024-01-15 17:42:26 UTC (score 28.57) [re2ob_19-01#1]
- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0016; peak 0.0031 at 2024-01-15 17:53:17 UTC; sustained deviation from 2024-01-15 17:43:02 UTC (score 12.91) [re2ob_19-01#1]

## Timeline

- 2024-01-15 17:40 UTC — operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-15 17:40:30 UTC; earliest sustained metric deviation: currencyservice_cpu from 2024-01-15 17:40:40 UTC [re2ob_19-02#2, re2ob_19-06#0]
- 2024-01-15 17:42 UTC — metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 6.00 at 2024-01-15 17:42:26 UTC; sustained deviation from 2024-01-15 17:42:26 UTC (score 28.57) [re2ob_19-01#1]
- 2024-01-15 17:43 UTC — metric anomalies: productcatalogservice_cpu — baseline median 2.84; peak 20.02 at 2024-01-15 17:43:44 UTC; sustained deviation from 2024-01-15 17:42:44 UTC (score 59.63); operation latency: traceservice_Export — baseline mean 0; later mean 0.9286 (x1.93); peak 3.00 at 2024-01-15 17:43:30 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0.1463; later mean 0.125 (x0.9814); peak 2.00 at 2024-01-15 17:43:00 UTC [re2ob_19-01#1, re2ob_19-02#0, re2ob_19-02#1]
- 2024-01-15 17:44 UTC — operation latency: paymentservice_Charge — baseline mean 0.0976; later mean 0.0714 (x0.9762); peak 1.00 at 2024-01-15 17:44:30 UTC [re2ob_19-02#2]
- 2024-01-15 17:45 UTC — metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0094 at 2024-01-15 17:45:36 UTC; sustained deviation from 2024-01-15 17:45:21 UTC (score 5.65) [re2ob_19-01#2]
- 2024-01-15 17:47 UTC — metric anomalies: productcatalogservice_latency-90 — baseline median 0.0043; peak 0.0499 at 2024-01-15 17:47:47 UTC; sustained deviation from 2024-01-15 17:42:51 UTC (score 140); metric anomalies: recommendationservice_latency-90 — baseline median 0.0095; peak 0.0732 at 2024-01-15 17:47:47 UTC; sustained deviation from 2024-01-15 17:42:36 UTC (score 97.49); metric anomalies: currencyservice_cpu — baseline median 19.00; peak 7.82 at 2024-01-15 17:47:59 UTC; sustained deviation from 2024-01-15 17:40:40 UTC (score 5.80); metric anomalies: redis_cpu — baseline median 0.2867; peak 0.1397 at 2024-01-15 17:47:38 UTC; sustained deviation from 2024-01-15 17:41:40 UTC (score 3.28); operation latency: productcatalogservice_ListProducts — baseline mean 0.4146; later mean 3.91 (x3.47); peak 17.00 at 2024-01-15 17:47:00 UTC; operation latency: cartservice_GetCart — baseline mean 2.90; later mean 3.36 (x1.12); peak 22.00 at 2024-01-15 17:47:00 UTC [re2ob_19-01#0, re2ob_19-01#2, re2ob_19-01#3, re2ob_19-02#0, re2ob_19-02#1]
- 2024-01-15 17:50 UTC — metric anomalies: productcatalogservice_mem — baseline median 10174464; peak 15855616 at 2024-01-15 17:50:06 UTC; sustained deviation from 2024-01-15 17:42:26 UTC (score 12.55); operation latency: cartservice_AddItem — baseline mean 0.2439; later mean 0.3571 (x1.09); peak 4.00 at 2024-01-15 17:50:15 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-15 17:50:00 UTC [re2ob_19-01#2, re2ob_19-02#1]
- 2024-01-15 17:51 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.7073; later mean 4.43 (x3.18); peak 18.00 at 2024-01-15 17:51:00 UTC [re2ob_19-02#0]
- 2024-01-15 17:52 UTC — metric anomalies: redis_diskio — baseline median 0; peak 25498 at 2024-01-15 17:52:57 UTC; sustained deviation from 2024-01-15 17:42:44 UTC (score 138); metric anomalies: currencyservice_latency-50 — baseline median 0.0613; peak 0.0379 at 2024-01-15 17:52:49 UTC; sustained deviation from 2024-01-15 17:43:19 UTC (score 5.06); operation latency: productcatalogservice_GetProduct — baseline mean 0.439; later mean 93.02 (x65.33); peak 154 at 2024-01-15 17:52:45 UTC [re2ob_19-01#0, re2ob_19-01#2, re2ob_19-02#0]
- 2024-01-15 17:53 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0071; peak 0.0332 at 2024-01-15 17:53:06 UTC; sustained deviation from 2024-01-15 17:43:02 UTC (score 72.28); metric anomalies: productcatalogservice_latency-50 — baseline median 0.0016; peak 0.0031 at 2024-01-15 17:53:17 UTC; sustained deviation from 2024-01-15 17:43:02 UTC (score 12.91) [re2ob_19-01#1]

## Detection: IDS Alerts

- metric anomalies: productcatalogservice_mem — baseline median 10174464; peak 15855616 at 2024-01-15 17:50:06 UTC; sustained deviation from 2024-01-15 17:42:26 UTC (score 12.55) [re2ob_19-01#2]
- metric anomalies: currencyservice_cpu — baseline median 19.00; peak 7.82 at 2024-01-15 17:47:59 UTC; sustained deviation from 2024-01-15 17:40:40 UTC (score 5.80) [re2ob_19-01#2]
- metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0094 at 2024-01-15 17:45:36 UTC; sustained deviation from 2024-01-15 17:45:21 UTC (score 5.65) [re2ob_19-01#2]
- metric anomalies: currencyservice_latency-50 — baseline median 0.0613; peak 0.0379 at 2024-01-15 17:52:49 UTC; sustained deviation from 2024-01-15 17:43:19 UTC (score 5.06) [re2ob_19-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-15 17:40:30 UTC [re2ob_19-02#2]
- operation latency: paymentservice_Charge — baseline mean 0.0976; later mean 0.0714 (x0.9762); peak 1.00 at 2024-01-15 17:44:30 UTC [re2ob_19-02#2]
- operation latency: productcatalogservice_GetProduct — baseline mean 0.439; later mean 93.02 (x65.33); peak 154 at 2024-01-15 17:52:45 UTC [re2ob_19-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.4146; later mean 3.91 (x3.47); peak 17.00 at 2024-01-15 17:47:00 UTC [re2ob_19-02#0]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.9286 (x1.93); peak 3.00 at 2024-01-15 17:43:30 UTC [re2ob_19-02#0]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_19-03#0]
2. operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-15 17:40:30 UTC [re2ob_19-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0.0976; later mean 0.0714 (x0.9762); peak 1.00 at 2024-01-15 17:44:30 UTC [re2ob_19-02#2]
4. Not established from the available artifacts.
5. log volume: adservice — 434 lines/min in the baseline, 426 lines/min later [re2ob_19-04#1]
6. log volume: frontend — 2584 lines/min in the baseline, 2541 lines/min later [re2ob_19-04#1]
7. log volume: cartservice — 744 lines/min in the baseline, 736 lines/min later [re2ob_19-04#1]
8. Not established from the available artifacts.
