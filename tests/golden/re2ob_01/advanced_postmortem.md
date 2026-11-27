# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 13 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_01-01#0]
- metric anomalies: checkoutservice_cpu — baseline median 0.4139; peak 20.03 at 2024-01-15 21:42:50 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 121) [re2ob_01-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 46680 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 103) [re2ob_01-01#0]
- metric anomalies: checkoutservice_socket — baseline median 9.00; peak 11.00 at 2024-01-15 21:36:20 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 13.79) [re2ob_01-01#0]
- metric anomalies: checkoutservice_mem — baseline median 11685888; peak 16846848 at 2024-01-15 21:37:35 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 11.83) [re2ob_01-01#1]
- metric anomalies: currencyservice_cpu — baseline median 18.79; peak 10.33 at 2024-01-15 21:39:31 UTC; sustained deviation from 2024-01-15 21:34:34 UTC (score 4.68) [re2ob_01-01#1]
- metric anomalies: redis_cpu — baseline median 0.259; peak 0.1088 at 2024-01-15 21:35:17 UTC; sustained deviation from 2024-01-15 21:35:17 UTC (score 3.93) [re2ob_01-01#1]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0987; peak 0.1312 at 2024-01-15 21:34:42 UTC; sustained deviation from 2024-01-15 21:34:37 UTC (score 2.85) [re2ob_01-01#1]
- operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 1.75 (x2.51); peak 8.00 at 2024-01-15 21:42:00 UTC [re2ob_01-02#0]
- operation latency: traceservice_Export — baseline mean 0.0488; later mean 0.4643 (x1.40); peak 4.00 at 2024-01-15 21:47:45 UTC [re2ob_01-02#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3929 (x1.39); peak 2.00 at 2024-01-15 21:37:00 UTC [re2ob_01-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 5.51; later mean 7.27 (x1.27); peak 43.00 at 2024-01-15 21:44:45 UTC [re2ob_01-02#0]

## Timeline

- 2024-01-15 21:34 UTC — metric anomalies: redis_diskio — baseline median 0; peak 46680 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 103); metric anomalies: currencyservice_latency-90 — baseline median 0.0987; peak 0.1312 at 2024-01-15 21:34:42 UTC; sustained deviation from 2024-01-15 21:34:37 UTC (score 2.85); metric anomalies: emailservice_cpu — baseline median 0.2885; peak 0.1659 at 2024-01-15 21:34:43 UTC; sustained deviation from 2024-01-15 21:34:43 UTC (score 2.62); metric anomalies: adservice_socket — baseline median 4.00; peak 5.00 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 0); operation latency: frontendservice_frontend — baseline mean 3.51; later mean 3.79 (x1.06); peak 12.00 at 2024-01-15 21:34:15 UTC; earliest sustained metric deviation: redis_diskio from 2024-01-15 21:34:06 UTC [re2ob_01-01#0, re2ob_01-01#1, re2ob_01-01#2, re2ob_01-01#3, re2ob_01-02#1, re2ob_01-06#0]
- 2024-01-15 21:35 UTC — metric anomalies: redis_cpu — baseline median 0.259; peak 0.1088 at 2024-01-15 21:35:17 UTC; sustained deviation from 2024-01-15 21:35:17 UTC (score 3.93); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.07; later mean 5.36 (x1.05); peak 16.00 at 2024-01-15 21:35:30 UTC [re2ob_01-01#1, re2ob_01-02#2]
- 2024-01-15 21:36 UTC — metric anomalies: checkoutservice_socket — baseline median 9.00; peak 11.00 at 2024-01-15 21:36:20 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 13.79); operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.0714 (x1.07); peak 1.00 at 2024-01-15 21:36:45 UTC [re2ob_01-01#0, re2ob_01-02#1]
- 2024-01-15 21:37 UTC — metric anomalies: checkoutservice_mem — baseline median 11685888; peak 16846848 at 2024-01-15 21:37:35 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 11.83); metric anomalies: frontend_cpu — baseline median 6.44; peak 4.07 at 2024-01-15 21:37:29 UTC; sustained deviation from 2024-01-15 21:35:25 UTC (score 2.05); metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0085 at 2024-01-15 21:37:57 UTC; sustained deviation from 2024-01-15 21:34:25 UTC (score 1.97); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3929 (x1.39); peak 2.00 at 2024-01-15 21:37:00 UTC [re2ob_01-01#1, re2ob_01-01#2, re2ob_01-02#0]
- 2024-01-15 21:39 UTC — metric anomalies: currencyservice_cpu — baseline median 18.79; peak 10.33 at 2024-01-15 21:39:31 UTC; sustained deviation from 2024-01-15 21:34:34 UTC (score 4.68); metric anomalies: recommendationservice_cpu — baseline median 2.53; peak 1.32 at 2024-01-15 21:39:07 UTC; sustained deviation from 2024-01-15 21:38:04 UTC (score 2.47) [re2ob_01-01#1, re2ob_01-01#2]
- 2024-01-15 21:40 UTC — operation latency: currencyservice_Convert — baseline mean 4.90; later mean 5.73 (x1.14); peak 17.00 at 2024-01-15 21:40:30 UTC; operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0714 (x1.05); peak 1.00 at 2024-01-15 21:40:15 UTC [re2ob_01-02#1, re2ob_01-02#2]
- 2024-01-15 21:42 UTC — metric anomalies: checkoutservice_cpu — baseline median 0.4139; peak 20.03 at 2024-01-15 21:42:50 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 121); operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 1.75 (x2.51); peak 8.00 at 2024-01-15 21:42:00 UTC [re2ob_01-01#0, re2ob_01-02#0]
- 2024-01-15 21:44 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 5.51; later mean 7.27 (x1.27); peak 43.00 at 2024-01-15 21:44:45 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.7561; later mean 0.8571 (x1.06); peak 7.00 at 2024-01-15 21:44:45 UTC [re2ob_01-02#0, re2ob_01-02#1]
- 2024-01-15 21:47 UTC — operation latency: traceservice_Export — baseline mean 0.0488; later mean 0.4643 (x1.40); peak 4.00 at 2024-01-15 21:47:45 UTC [re2ob_01-02#0]

## Detection: IDS Alerts



## Initial Infection Indicators

- metric anomalies: adservice_socket — baseline median 4.00; peak 5.00 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 0) [re2ob_01-01#3]
- metric anomalies: emailservice_cpu — baseline median 0.2885; peak 0.1659 at 2024-01-15 21:34:43 UTC; sustained deviation from 2024-01-15 21:34:43 UTC (score 2.62) [re2ob_01-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.53; peak 1.32 at 2024-01-15 21:39:07 UTC; sustained deviation from 2024-01-15 21:38:04 UTC (score 2.47) [re2ob_01-01#2]
- metric anomalies: frontend_cpu — baseline median 6.44; peak 4.07 at 2024-01-15 21:37:29 UTC; sustained deviation from 2024-01-15 21:35:25 UTC (score 2.05) [re2ob_01-01#2]
- metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0085 at 2024-01-15 21:37:57 UTC; sustained deviation from 2024-01-15 21:34:25 UTC (score 1.97) [re2ob_01-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.07; later mean 5.36 (x1.05); peak 16.00 at 2024-01-15 21:35:30 UTC [re2ob_01-02#2]
- operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0714 (x1.05); peak 1.00 at 2024-01-15 21:40:15 UTC [re2ob_01-02#2]
- operation latency: currencyservice_Convert — baseline mean 4.90; later mean 5.73 (x1.14); peak 17.00 at 2024-01-15 21:40:30 UTC [re2ob_01-02#1]
- operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.0714 (x1.07); peak 1.00 at 2024-01-15 21:36:45 UTC [re2ob_01-02#1]
- operation latency: frontendservice_frontend — baseline mean 3.51; later mean 3.79 (x1.06); peak 12.00 at 2024-01-15 21:34:15 UTC [re2ob_01-02#1]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.7561; later mean 0.8571 (x1.06); peak 7.00 at 2024-01-15 21:44:45 UTC [re2ob_01-02#1]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_01-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_01-03#0]
2. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.07; later mean 5.36 (x1.05); peak 16.00 at 2024-01-15 21:35:30 UTC [re2ob_01-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0714 (x1.05); peak 1.00 at 2024-01-15 21:40:15 UTC [re2ob_01-02#2]
4. Not established from the available artifacts.
5. log volume: frontend — 2553 lines/min in the baseline, 2548 lines/min later [re2ob_01-04#1]
6. log volume: recommendationservice — 539 lines/min in the baseline, 538 lines/min later [re2ob_01-04#1]
7. log volume: adservice — 432 lines/min in the baseline, 432 lines/min later [re2ob_01-04#1]
8. Not established from the available artifacts.
