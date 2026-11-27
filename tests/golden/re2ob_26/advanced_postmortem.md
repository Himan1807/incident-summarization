# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: checkoutservice_latency-90 — baseline median 0.2333; peak 0.3375 at 2024-01-16 10:25:41 UTC; sustained deviation from 2024-01-16 10:17:41 UTC (score 2.72) [re2ob_26-01#3]
- metric anomalies: 19 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_26-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.4537 at 2024-01-16 10:20:26 UTC; sustained deviation from 2024-01-16 10:19:47 UTC (score 184) [re2ob_26-01#0]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.2577 at 2024-01-16 10:23:41 UTC; sustained deviation from 2024-01-16 10:20:11 UTC (score 173) [re2ob_26-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 36468 at 2024-01-16 10:22:04 UTC; sustained deviation from 2024-01-16 10:21:50 UTC (score 110) [re2ob_26-01#0]
- Derived: earliest sustained metric deviation: checkoutservice_latency-90 from 2024-01-16 10:17:41 UTC. [re2ob_26-06#0]
- Derived: metric series ranked #1 by deviation score: recommendationservice_latency-90 (score 184). [re2ob_26-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_ListProducts (mean 0 -> 0.2857, x1.29). [re2ob_26-06#0]
- Derived: container with the largest change in log volume: redis (1.00 -> 0.7143 lines/min). [re2ob_26-06#0]
- operation latency: traceservice_Export — baseline mean 0.2195; later mean 0.1607 (x0.9518); peak 1.00 at 2024-01-16 10:20:30 UTC [re2ob_26-02#2]
- operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.125 (x0.9413); peak 2.00 at 2024-01-16 10:30:00 UTC [re2ob_26-02#2]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.1071 (x1.01); peak 2.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#1]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-16 10:17:45 UTC [re2ob_26-02#1]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0.0488; later mean 0.0357 (x0.9875); peak 1.00 at 2024-01-16 10:19:15 UTC [re2ob_26-02#1]
- operation latency: cartservice_EmptyCart — baseline mean 0.0488; later mean 0.0179 (x0.9705); peak 1.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#1]

## Timeline

- 2024-01-16 10:17 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-16 10:17:45 UTC; earliest sustained metric deviation: checkoutservice_latency-90 from 2024-01-16 10:17:41 UTC [re2ob_26-02#1, re2ob_26-06#0]
- 2024-01-16 10:19 UTC — operation latency: emailservice_SendOrderConfirmation — baseline mean 0.0488; later mean 0.0357 (x0.9875); peak 1.00 at 2024-01-16 10:19:15 UTC [re2ob_26-02#1]
- 2024-01-16 10:20 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.4537 at 2024-01-16 10:20:26 UTC; sustained deviation from 2024-01-16 10:19:47 UTC (score 184); metric anomalies: paymentservice_cpu — baseline median 0.6142; peak 1.11 at 2024-01-16 10:20:49 UTC; sustained deviation from 2024-01-16 10:20:49 UTC (score 2.88); operation latency: traceservice_Export — baseline mean 0.2195; later mean 0.1607 (x0.9518); peak 1.00 at 2024-01-16 10:20:30 UTC [re2ob_26-01#0, re2ob_26-01#2, re2ob_26-02#2]
- 2024-01-16 10:22 UTC — metric anomalies: redis_diskio — baseline median 0; peak 36468 at 2024-01-16 10:22:04 UTC; sustained deviation from 2024-01-16 10:21:50 UTC (score 110); metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 10:22:52 UTC; sustained deviation from 2024-01-16 10:22:52 UTC (score 16.67); metric anomalies: frontend_cpu — baseline median 8.57; peak 5.04 at 2024-01-16 10:22:21 UTC; sustained deviation from 2024-01-16 10:22:11 UTC (score 3.66); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 2.00 at 2024-01-16 10:22:45 UTC [re2ob_26-01#0, re2ob_26-01#1, re2ob_26-01#2, re2ob_26-02#0]
- 2024-01-16 10:23 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.2577 at 2024-01-16 10:23:41 UTC; sustained deviation from 2024-01-16 10:20:11 UTC (score 173) [re2ob_26-01#0]
- 2024-01-16 10:24 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 0.2857 (x1.29); peak 5.00 at 2024-01-16 10:24:45 UTC; operation latency: frontendservice_frontend — baseline mean 0.439; later mean 0.5536 (x1.08); peak 11.00 at 2024-01-16 10:24:45 UTC; operation latency: cartservice_AddItem — baseline mean 0.122; later mean 0.1607 (x1.03); peak 4.00 at 2024-01-16 10:24:45 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0.0976; later mean 0.1071 (x1.01); peak 2.00 at 2024-01-16 10:24:45 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.0488; later mean 0.0179 (x0.9705); peak 1.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#0, re2ob_26-02#1]
- 2024-01-16 10:25 UTC — metric anomalies: frontend_latency-50 — baseline median 0.0548; peak 0.3691 at 2024-01-16 10:25:11 UTC; sustained deviation from 2024-01-16 10:19:57 UTC (score 47.09); metric anomalies: frontend_latency-90 — baseline median 0.2123; peak 0.7774 at 2024-01-16 10:25:27 UTC; sustained deviation from 2024-01-16 10:19:56 UTC (score 30.40); metric anomalies: redis_cpu — baseline median 0.3181; peak 0.1703 at 2024-01-16 10:25:41 UTC; sustained deviation from 2024-01-16 10:19:06 UTC (score 4.18); metric anomalies: checkoutservice_latency-90 — baseline median 0.2333; peak 0.3375 at 2024-01-16 10:25:41 UTC; sustained deviation from 2024-01-16 10:17:41 UTC (score 2.72) [re2ob_26-01#1, re2ob_26-01#2, re2ob_26-01#3]
- 2024-01-16 10:26 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.62; peak 2.04 at 2024-01-16 10:26:25 UTC; sustained deviation from 2024-01-16 10:25:48 UTC (score 3.49) [re2ob_26-01#2]
- 2024-01-16 10:30 UTC — metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0048 at 2024-01-16 10:30:32 UTC; sustained deviation from 2024-01-16 10:20:41 UTC (score 5.07); operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.125 (x0.9413); peak 2.00 at 2024-01-16 10:30:00 UTC [re2ob_26-01#1, re2ob_26-02#2]

## Detection: IDS Alerts

- metric anomalies: frontend_latency-50 — baseline median 0.0548; peak 0.3691 at 2024-01-16 10:25:11 UTC; sustained deviation from 2024-01-16 10:19:57 UTC (score 47.09) [re2ob_26-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.2123; peak 0.7774 at 2024-01-16 10:25:27 UTC; sustained deviation from 2024-01-16 10:19:56 UTC (score 30.40) [re2ob_26-01#1]
- metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 3.00 at 2024-01-16 10:22:52 UTC; sustained deviation from 2024-01-16 10:22:52 UTC (score 16.67) [re2ob_26-01#1]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0048 at 2024-01-16 10:30:32 UTC; sustained deviation from 2024-01-16 10:20:41 UTC (score 5.07) [re2ob_26-01#1]
- metric anomalies: redis_cpu — baseline median 0.3181; peak 0.1703 at 2024-01-16 10:25:41 UTC; sustained deviation from 2024-01-16 10:19:06 UTC (score 4.18) [re2ob_26-01#2]
- metric anomalies: frontend_cpu — baseline median 8.57; peak 5.04 at 2024-01-16 10:22:21 UTC; sustained deviation from 2024-01-16 10:22:11 UTC (score 3.66) [re2ob_26-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.62; peak 2.04 at 2024-01-16 10:26:25 UTC; sustained deviation from 2024-01-16 10:25:48 UTC (score 3.49) [re2ob_26-01#2]
- metric anomalies: paymentservice_cpu — baseline median 0.6142; peak 1.11 at 2024-01-16 10:20:49 UTC; sustained deviation from 2024-01-16 10:20:49 UTC (score 2.88) [re2ob_26-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 0.2857 (x1.29); peak 5.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#0]
- operation latency: frontendservice_frontend — baseline mean 0.439; later mean 0.5536 (x1.08); peak 11.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#0]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0357 (x1.04); peak 2.00 at 2024-01-16 10:22:45 UTC [re2ob_26-02#0]
- operation latency: cartservice_AddItem — baseline mean 0.122; later mean 0.1607 (x1.03); peak 4.00 at 2024-01-16 10:24:45 UTC [re2ob_26-02#0]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_26-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_26-03#0]
2. operation latency: traceservice_Export — baseline mean 0.2195; later mean 0.1607 (x0.9518); peak 1.00 at 2024-01-16 10:20:30 UTC [re2ob_26-02#2]
3. operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.125 (x0.9413); peak 2.00 at 2024-01-16 10:30:00 UTC [re2ob_26-02#2]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2410 lines/min in the baseline, 2207 lines/min later [re2ob_26-04#0]
6. log volume: adservice — 461 lines/min in the baseline, 424 lines/min later [re2ob_26-04#0]
7. log volume: frontend — 2683 lines/min in the baseline, 2502 lines/min later [re2ob_26-04#0]
8. Not established from the available artifacts.
