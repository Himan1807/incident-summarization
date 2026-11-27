# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 15 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_03-01#0]
- metric anomalies: checkoutservice_diskio — no data in the baseline; series appears at 2024-01-16 02:58:58 UTC (first value 4422731761); peak 11464441937 at 2024-01-16 03:07:37 UTC [re2ob_03-01#0]
- metric anomalies: checkoutservice_mem — baseline median 10420224; peak 134213632 at 2024-01-16 03:07:14 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 124) [re2ob_03-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 39727 at 2024-01-16 03:10:16 UTC; sustained deviation from 2024-01-16 02:59:59 UTC (score 115) [re2ob_03-01#0]
- Derived: earliest sustained metric deviation: currencyservice_latency-90 from 2024-01-16 02:56:30 UTC. [re2ob_03-06#0]
- Derived: metric series ranked #1 by deviation score: checkoutservice_mem (score 124). [re2ob_03-06#0]
- Derived: metric series without baseline data that appears during the capture: checkoutservice_diskio (from 2024-01-16 02:58:58 UTC). [re2ob_03-06#0]
- Derived: trace operation with the largest latency increase: emailservice_SendOrderConfirmation (mean 0 -> 1.11, x2.11). [re2ob_03-06#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.11 (x2.11); peak 6.00 at 2024-01-16 03:03:15 UTC [re2ob_03-02#0]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 1.04 (x2.04); peak 8.00 at 2024-01-16 03:03:15 UTC [re2ob_03-02#0]
- operation latency: shippingservice_GetQuote — baseline mean 0.175; later mean 1.18 (x1.85); peak 5.00 at 2024-01-16 03:03:15 UTC [re2ob_03-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 3.55; later mean 5.84 (x1.50); peak 19.00 at 2024-01-16 03:07:15 UTC [re2ob_03-02#0]
- metric anomalies: checkoutservice_cpu — baseline median 0.4083; peak 19.85 at 2024-01-16 03:08:20 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 105) [re2ob_03-01#1]
- metric anomalies: checkoutservice_socket — baseline median 9.00; peak 12.00 at 2024-01-16 02:58:40 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 20.00) [re2ob_03-01#1]
- metric anomalies: frontend_cpu — baseline median 6.71; peak 3.86 at 2024-01-16 02:58:37 UTC; sustained deviation from 2024-01-16 02:58:37 UTC (score 4.50) [re2ob_03-01#1]
- metric anomalies: cartservice_latency-90 — baseline median 0.0048; peak 0.0092 at 2024-01-16 03:05:40 UTC; sustained deviation from 2024-01-16 02:59:25 UTC (score 4.46) [re2ob_03-01#1]

## Timeline

- 2024-01-16 02:56 UTC — earliest sustained metric deviation: currencyservice_latency-90 from 2024-01-16 02:56:30 UTC [re2ob_03-06#0]
- 2024-01-16 02:58 UTC — metric anomalies: checkoutservice_diskio — no data in the baseline; series appears at 2024-01-16 02:58:58 UTC (first value 4422731761); peak 11464441937 at 2024-01-16 03:07:37 UTC; metric anomalies: checkoutservice_socket — baseline median 9.00; peak 12.00 at 2024-01-16 02:58:40 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 20.00); metric anomalies: frontend_cpu — baseline median 6.71; peak 3.86 at 2024-01-16 02:58:37 UTC; sustained deviation from 2024-01-16 02:58:37 UTC (score 4.50); operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.1429 (x1.14); peak 1.00 at 2024-01-16 02:58:30 UTC; operation latency: frontendservice_frontend — baseline mean 3.65; later mean 4.09 (x1.09); peak 20.00 at 2024-01-16 02:58:45 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.35; later mean 0.4107 (x1.04); peak 5.00 at 2024-01-16 02:58:30 UTC; metric series without baseline data that appears during the capture: checkoutservice_diskio (from 2024-01-16 02:58:58 UTC) [re2ob_03-01#0, re2ob_03-01#1, re2ob_03-02#1, re2ob_03-02#2, re2ob_03-06#0]
- 2024-01-16 02:59 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.50; peak 1.18 at 2024-01-16 02:59:06 UTC; sustained deviation from 2024-01-16 02:58:32 UTC (score 2.44) [re2ob_03-01#3]
- 2024-01-16 03:02 UTC — metric anomalies: redis_cpu — baseline median 0.2682; peak 0.1666 at 2024-01-16 03:02:16 UTC; sustained deviation from 2024-01-16 03:01:43 UTC (score 3.31) [re2ob_03-01#2]
- 2024-01-16 03:03 UTC — operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.11 (x2.11); peak 6.00 at 2024-01-16 03:03:15 UTC; operation latency: paymentservice_Charge — baseline mean 0; later mean 1.04 (x2.04); peak 8.00 at 2024-01-16 03:03:15 UTC; operation latency: shippingservice_GetQuote — baseline mean 0.175; later mean 1.18 (x1.85); peak 5.00 at 2024-01-16 03:03:15 UTC [re2ob_03-02#0]
- 2024-01-16 03:04 UTC — operation latency: adservice_GetAds — baseline mean 0.475; later mean 0.6071 (x1.09); peak 4.00 at 2024-01-16 03:04:00 UTC [re2ob_03-02#2]
- 2024-01-16 03:05 UTC — metric anomalies: cartservice_latency-90 — baseline median 0.0048; peak 0.0092 at 2024-01-16 03:05:40 UTC; sustained deviation from 2024-01-16 02:59:25 UTC (score 4.46); operation latency: recommendationservice_ListRecommendations — baseline mean 1.07; later mean 1.52 (x1.21); peak 16.00 at 2024-01-16 03:05:00 UTC [re2ob_03-01#1, re2ob_03-02#1]
- 2024-01-16 03:06 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0065 at 2024-01-16 03:06:19 UTC; sustained deviation from 2024-01-16 03:06:12 UTC (score 4.44); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0033 at 2024-01-16 03:06:19 UTC; sustained deviation from 2024-01-16 03:06:12 UTC (score 4.15); metric anomalies: currencyservice_cpu — baseline median 18.62; peak 10.19 at 2024-01-16 03:06:46 UTC; sustained deviation from 2024-01-16 02:59:17 UTC (score 4.00); operation latency: traceservice_Export — baseline mean 0.05; later mean 0.3393 (x1.28); peak 3.00 at 2024-01-16 03:06:00 UTC [re2ob_03-01#2, re2ob_03-02#1]
- 2024-01-16 03:07 UTC — metric anomalies: checkoutservice_mem — baseline median 10420224; peak 134213632 at 2024-01-16 03:07:14 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 124); operation latency: productcatalogservice_GetProduct — baseline mean 3.55; later mean 5.84 (x1.50); peak 19.00 at 2024-01-16 03:07:15 UTC [re2ob_03-01#0, re2ob_03-02#0]
- 2024-01-16 03:08 UTC — metric anomalies: checkoutservice_cpu — baseline median 0.4083; peak 19.85 at 2024-01-16 03:08:20 UTC; sustained deviation from 2024-01-16 02:58:40 UTC (score 105) [re2ob_03-01#1]
- 2024-01-16 03:10 UTC — metric anomalies: redis_diskio — baseline median 0; peak 39727 at 2024-01-16 03:10:16 UTC; sustained deviation from 2024-01-16 02:59:59 UTC (score 115) [re2ob_03-01#0]

## Detection: IDS Alerts

- operation latency: traceservice_Export — baseline mean 0.05; later mean 0.3393 (x1.28); peak 3.00 at 2024-01-16 03:06:00 UTC [re2ob_03-02#1]
- operation latency: recommendationservice_ListRecommendations — baseline mean 1.07; later mean 1.52 (x1.21); peak 16.00 at 2024-01-16 03:05:00 UTC [re2ob_03-02#1]
- operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.1429 (x1.14); peak 1.00 at 2024-01-16 02:58:30 UTC [re2ob_03-02#1]
- operation latency: frontendservice_frontend — baseline mean 3.65; later mean 4.09 (x1.09); peak 20.00 at 2024-01-16 02:58:45 UTC [re2ob_03-02#1]

## Initial Infection Indicators

- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0065 at 2024-01-16 03:06:19 UTC; sustained deviation from 2024-01-16 03:06:12 UTC (score 4.44) [re2ob_03-01#2]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0033 at 2024-01-16 03:06:19 UTC; sustained deviation from 2024-01-16 03:06:12 UTC (score 4.15) [re2ob_03-01#2]
- metric anomalies: currencyservice_cpu — baseline median 18.62; peak 10.19 at 2024-01-16 03:06:46 UTC; sustained deviation from 2024-01-16 02:59:17 UTC (score 4.00) [re2ob_03-01#2]
- metric anomalies: redis_cpu — baseline median 0.2682; peak 0.1666 at 2024-01-16 03:02:16 UTC; sustained deviation from 2024-01-16 03:01:43 UTC (score 3.31) [re2ob_03-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.50; peak 1.18 at 2024-01-16 02:59:06 UTC; sustained deviation from 2024-01-16 02:58:32 UTC (score 2.44) [re2ob_03-01#3]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: productcatalogservice_ListProducts — baseline mean 0.35; later mean 0.4107 (x1.04); peak 5.00 at 2024-01-16 02:58:30 UTC [re2ob_03-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_03-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_03-03#0]
2. operation latency: adservice_GetAds — baseline mean 0.475; later mean 0.6071 (x1.09); peak 4.00 at 2024-01-16 03:04:00 UTC [re2ob_03-02#2]
3. operation latency: productcatalogservice_ListProducts — baseline mean 0.35; later mean 0.4107 (x1.04); peak 5.00 at 2024-01-16 02:58:30 UTC [re2ob_03-02#2]
4. Not established from the available artifacts.
5. operation latency: recommendationservice_ListRecommendations — baseline mean 1.07; later mean 1.52 (x1.21); peak 16.00 at 2024-01-16 03:05:00 UTC [re2ob_03-02#1]
6. operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.1429 (x1.14); peak 1.00 at 2024-01-16 02:58:30 UTC [re2ob_03-02#1]
7. operation latency: frontendservice_frontend — baseline mean 3.65; later mean 4.09 (x1.09); peak 20.00 at 2024-01-16 02:58:45 UTC [re2ob_03-02#1]
8. Not established from the available artifacts.
