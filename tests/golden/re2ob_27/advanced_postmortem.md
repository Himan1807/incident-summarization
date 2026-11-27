# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 16 of 73 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_27-01#0]
- metric anomalies: recommendationservice_diskio — baseline median 0; peak 10872393729 at 2024-01-16 01:05:39 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 193) [re2ob_27-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.2047 at 2024-01-16 01:02:07 UTC; sustained deviation from 2024-01-16 00:55:33 UTC (score 153) [re2ob_27-01#0]
- metric anomalies: recommendationservice_mem — baseline median 44298240; peak 471859200 at 2024-01-16 00:57:46 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 149) [re2ob_27-01#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0057 at 2024-01-16 01:07:04 UTC; sustained deviation from 2024-01-16 01:06:42 UTC (score 2.77) [re2ob_27-01#3]
- Derived: earliest sustained metric deviation: frontend_cpu from 2024-01-16 00:53:27 UTC. [re2ob_27-06#0]
- Derived: metric series ranked #1 by deviation score: recommendationservice_diskio (score 193). [re2ob_27-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_ListProducts (mean 0 -> 14.48, x15.48). [re2ob_27-06#0]
- Derived: container with the largest change in log volume: redis (1.00 -> 1.07 lines/min). [re2ob_27-06#0]
- metric anomalies: redis_diskio — baseline median 0; peak 35310 at 2024-01-16 00:55:07 UTC; sustained deviation from 2024-01-16 00:54:45 UTC (score 113) [re2ob_27-01#1]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0388 at 2024-01-16 01:04:52 UTC; sustained deviation from 2024-01-16 00:55:52 UTC (score 95.15) [re2ob_27-01#1]
- metric anomalies: recommendationservice_cpu — baseline median 2.53; peak 20.00 at 2024-01-16 01:06:29 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 65.23) [re2ob_27-01#1]
- metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0083 at 2024-01-16 00:55:42 UTC; sustained deviation from 2024-01-16 00:54:10 UTC (score 10.09) [re2ob_27-01#1]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 01:03:00 UTC [re2ob_27-02#2]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 00:55:00 UTC [re2ob_27-02#2]

## Timeline

- 2024-01-16 00:53 UTC — earliest sustained metric deviation: frontend_cpu from 2024-01-16 00:53:27 UTC [re2ob_27-06#0]
- 2024-01-16 00:54 UTC — metric anomalies: redis_cpu — baseline median 0.2683; peak 0.1686 at 2024-01-16 00:54:24 UTC; sustained deviation from 2024-01-16 00:57:45 UTC (score 3.45); metric anomalies: frontend_cpu — baseline median 6.75; peak 4.12 at 2024-01-16 00:54:06 UTC; sustained deviation from 2024-01-16 00:53:27 UTC (score 3.22); operation latency: cartservice_AddItem — baseline mean 0.0488; later mean 0.2321 (x1.17); peak 3.00 at 2024-01-16 00:54:45 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 6.02; later mean 6.68 (x1.09); peak 45.00 at 2024-01-16 00:54:00 UTC [re2ob_27-01#2, re2ob_27-02#0, re2ob_27-02#1]
- 2024-01-16 00:55 UTC — metric anomalies: redis_diskio — baseline median 0; peak 35310 at 2024-01-16 00:55:07 UTC; sustained deviation from 2024-01-16 00:54:45 UTC (score 113); metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0083 at 2024-01-16 00:55:42 UTC; sustained deviation from 2024-01-16 00:54:10 UTC (score 10.09); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 00:55:00 UTC [re2ob_27-01#1, re2ob_27-02#2]
- 2024-01-16 00:57 UTC — metric anomalies: recommendationservice_mem — baseline median 44298240; peak 471859200 at 2024-01-16 00:57:46 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 149) [re2ob_27-01#0]
- 2024-01-16 00:58 UTC — metric anomalies: currencyservice_cpu — baseline median 18.87; peak 7.48 at 2024-01-16 00:58:55 UTC; sustained deviation from 2024-01-16 00:54:03 UTC (score 6.27); operation latency: health_Check — baseline mean 0.0732; later mean 0.1429 (x1.06); peak 2.00 at 2024-01-16 00:58:15 UTC [re2ob_27-01#2, re2ob_27-02#1]
- 2024-01-16 01:00 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 14.48 (x15.48); peak 32.00 at 2024-01-16 01:00:45 UTC; operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 5.30 (x6.30); peak 24.00 at 2024-01-16 01:00:45 UTC [re2ob_27-02#0]
- 2024-01-16 01:02 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.2047 at 2024-01-16 01:02:07 UTC; sustained deviation from 2024-01-16 00:55:33 UTC (score 153); metric anomalies: adservice_diskio — baseline median 61490; peak 227796 at 2024-01-16 01:02:11 UTC; sustained deviation from 2024-01-16 01:02:04 UTC (score 3.08) [re2ob_27-01#0, re2ob_27-01#2]
- 2024-01-16 01:03 UTC — operation latency: cartservice_GetCart — baseline mean 2.17; later mean 2.54 (x1.12); peak 21.00 at 2024-01-16 01:03:15 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 01:03:00 UTC [re2ob_27-02#1, re2ob_27-02#2]
- 2024-01-16 01:04 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0388 at 2024-01-16 01:04:52 UTC; sustained deviation from 2024-01-16 00:55:52 UTC (score 95.15) [re2ob_27-01#1]
- 2024-01-16 01:05 UTC — metric anomalies: recommendationservice_diskio — baseline median 0; peak 10872393729 at 2024-01-16 01:05:39 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 193); operation latency: checkoutservice_PlaceOrder — baseline mean 0.1463; later mean 0.2857 (x1.12); peak 4.00 at 2024-01-16 01:05:45 UTC [re2ob_27-01#0, re2ob_27-02#0]
- 2024-01-16 01:06 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.53; peak 20.00 at 2024-01-16 01:06:29 UTC; sustained deviation from 2024-01-16 00:55:35 UTC (score 65.23); operation latency: frontendservice_frontend — baseline mean 3.41; later mean 3.62 (x1.05); peak 14.00 at 2024-01-16 01:06:30 UTC [re2ob_27-01#1, re2ob_27-02#1]
- 2024-01-16 01:07 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0057 at 2024-01-16 01:07:04 UTC; sustained deviation from 2024-01-16 01:06:42 UTC (score 2.77) [re2ob_27-01#3]

## Detection: IDS Alerts

- operation latency: cartservice_GetCart — baseline mean 2.17; later mean 2.54 (x1.12); peak 21.00 at 2024-01-16 01:03:15 UTC [re2ob_27-02#1]
- operation latency: productcatalogservice_GetProduct — baseline mean 6.02; later mean 6.68 (x1.09); peak 45.00 at 2024-01-16 00:54:00 UTC [re2ob_27-02#1]
- operation latency: health_Check — baseline mean 0.0732; later mean 0.1429 (x1.06); peak 2.00 at 2024-01-16 00:58:15 UTC [re2ob_27-02#1]
- operation latency: frontendservice_frontend — baseline mean 3.41; later mean 3.62 (x1.05); peak 14.00 at 2024-01-16 01:06:30 UTC [re2ob_27-02#1]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 14.48 (x15.48); peak 32.00 at 2024-01-16 01:00:45 UTC [re2ob_27-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 5.30 (x6.30); peak 24.00 at 2024-01-16 01:00:45 UTC [re2ob_27-02#0]
- operation latency: cartservice_AddItem — baseline mean 0.0488; later mean 0.2321 (x1.17); peak 3.00 at 2024-01-16 00:54:45 UTC [re2ob_27-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.1463; later mean 0.2857 (x1.12); peak 4.00 at 2024-01-16 01:05:45 UTC [re2ob_27-02#0]

## Initial Infection Indicators

- metric anomalies: currencyservice_cpu — baseline median 18.87; peak 7.48 at 2024-01-16 00:58:55 UTC; sustained deviation from 2024-01-16 00:54:03 UTC (score 6.27) [re2ob_27-01#2]
- metric anomalies: redis_cpu — baseline median 0.2683; peak 0.1686 at 2024-01-16 00:54:24 UTC; sustained deviation from 2024-01-16 00:57:45 UTC (score 3.45) [re2ob_27-01#2]
- metric anomalies: frontend_cpu — baseline median 6.75; peak 4.12 at 2024-01-16 00:54:06 UTC; sustained deviation from 2024-01-16 00:53:27 UTC (score 3.22) [re2ob_27-01#2]
- metric anomalies: adservice_diskio — baseline median 61490; peak 227796 at 2024-01-16 01:02:11 UTC; sustained deviation from 2024-01-16 01:02:04 UTC (score 3.08) [re2ob_27-01#2]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_27-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_27-03#0]
2. operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 01:03:00 UTC [re2ob_27-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-16 00:55:00 UTC [re2ob_27-02#2]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2264 lines/min in the baseline, 2244 lines/min later [re2ob_27-04#1]
6. log volume: cartservice — 741 lines/min in the baseline, 736 lines/min later [re2ob_27-04#1]
7. log volume: adservice — 435 lines/min in the baseline, 432 lines/min later [re2ob_27-04#1]
8. Not established from the available artifacts.
