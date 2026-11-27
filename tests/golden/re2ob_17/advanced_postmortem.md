# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 11 of 71 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_17-01#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 2.15 at 2024-01-17 07:21:38 UTC; sustained deviation from 2024-01-17 07:12:08 UTC (score 193) [re2ob_17-01#0]
- metric anomalies: emailservice_cpu — baseline median 0.3125; peak 20.87 at 2024-01-17 07:13:39 UTC; sustained deviation from 2024-01-17 07:12:00 UTC (score 159) [re2ob_17-01#0]
- metric anomalies: emailservice_mem — baseline median 43528192; peak 268439552 at 2024-01-17 07:14:16 UTC; sustained deviation from 2024-01-17 07:12:00 UTC (score 127) [re2ob_17-01#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.75 at 2024-01-17 07:21:38 UTC; sustained deviation from 2024-01-17 07:12:23 UTC (score 115) [re2ob_17-01#1]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2311; peak 2.20 at 2024-01-17 07:16:53 UTC; sustained deviation from 2024-01-17 07:12:06 UTC (score 98.98) [re2ob_17-01#1]
- metric anomalies: redis_diskio — baseline median 0; peak 36791 at 2024-01-17 07:19:33 UTC; sustained deviation from 2024-01-17 07:13:57 UTC (score 88.82) [re2ob_17-01#1]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1469; peak 0.875 at 2024-01-17 07:14:53 UTC; sustained deviation from 2024-01-17 07:13:51 UTC (score 17.89) [re2ob_17-01#1]
- metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.33 at 2024-01-17 07:20:32 UTC; sustained deviation from 2024-01-17 07:10:28 UTC (score 3.95) [re2ob_17-01#2]
- metric anomalies: redis_cpu — baseline median 0.2944; peak 0.1615 at 2024-01-17 07:21:09 UTC; sustained deviation from 2024-01-17 07:10:26 UTC (score 3.57) [re2ob_17-01#2]
- metric anomalies: currencyservice_cpu — baseline median 29.64; peak 15.57 at 2024-01-17 07:23:04 UTC; sustained deviation from 2024-01-17 07:12:59 UTC (score 3.56) [re2ob_17-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.60; peak 1.98 at 2024-01-17 07:14:55 UTC; sustained deviation from 2024-01-17 07:12:51 UTC (score 3.12) [re2ob_17-01#2]

## Timeline

- 2024-01-17 07:10 UTC — earliest sustained metric deviation: redis_cpu from 2024-01-17 07:10:26 UTC [re2ob_17-06#0]
- 2024-01-17 07:13 UTC — metric anomalies: emailservice_cpu — baseline median 0.3125; peak 20.87 at 2024-01-17 07:13:39 UTC; sustained deviation from 2024-01-17 07:12:00 UTC (score 159) [re2ob_17-01#0]
- 2024-01-17 07:14 UTC — metric anomalies: emailservice_mem — baseline median 43528192; peak 268439552 at 2024-01-17 07:14:16 UTC; sustained deviation from 2024-01-17 07:12:00 UTC (score 127); metric anomalies: checkoutservice_latency-50 — baseline median 0.1469; peak 0.875 at 2024-01-17 07:14:53 UTC; sustained deviation from 2024-01-17 07:13:51 UTC (score 17.89); metric anomalies: productcatalogservice_cpu — baseline median 3.60; peak 1.98 at 2024-01-17 07:14:55 UTC; sustained deviation from 2024-01-17 07:12:51 UTC (score 3.12); operation latency: adservice_GetAds — baseline mean 0.9; later mean 0.9821 (x1.04); peak 4.00 at 2024-01-17 07:14:45 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 8.75; later mean 9.04 (x1.03); peak 20.00 at 2024-01-17 07:14:45 UTC [re2ob_17-01#0, re2ob_17-01#1, re2ob_17-01#2, re2ob_17-02#1, re2ob_17-02#2]
- 2024-01-17 07:15 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.0536 (x1.05); peak 1.00 at 2024-01-17 07:15:45 UTC [re2ob_17-02#1]
- 2024-01-17 07:16 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.2311; peak 2.20 at 2024-01-17 07:16:53 UTC; sustained deviation from 2024-01-17 07:12:06 UTC (score 98.98); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.25 (x2.25); peak 5.00 at 2024-01-17 07:16:30 UTC [re2ob_17-01#1, re2ob_17-02#0]
- 2024-01-17 07:17 UTC — operation latency: frontendservice_frontend — baseline mean 1.00; later mean 3.27 (x2.13); peak 13.00 at 2024-01-17 07:17:30 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-17 07:17:30 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 6.15; later mean 6.38 (x1.03); peak 28.00 at 2024-01-17 07:17:30 UTC [re2ob_17-02#0, re2ob_17-02#1]
- 2024-01-17 07:19 UTC — metric anomalies: redis_diskio — baseline median 0; peak 36791 at 2024-01-17 07:19:33 UTC; sustained deviation from 2024-01-17 07:13:57 UTC (score 88.82) [re2ob_17-01#1]
- 2024-01-17 07:20 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.33 at 2024-01-17 07:20:32 UTC; sustained deviation from 2024-01-17 07:10:28 UTC (score 3.95); operation latency: currencyservice_Convert — baseline mean 42.45; later mean 45.12 (x1.06); peak 85.00 at 2024-01-17 07:20:45 UTC [re2ob_17-01#2, re2ob_17-02#1]
- 2024-01-17 07:21 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 2.15 at 2024-01-17 07:21:38 UTC; sustained deviation from 2024-01-17 07:12:08 UTC (score 193); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.75 at 2024-01-17 07:21:38 UTC; sustained deviation from 2024-01-17 07:12:23 UTC (score 115); metric anomalies: redis_cpu — baseline median 0.2944; peak 0.1615 at 2024-01-17 07:21:09 UTC; sustained deviation from 2024-01-17 07:10:26 UTC (score 3.57); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-17 07:21:30 UTC [re2ob_17-01#0, re2ob_17-01#1, re2ob_17-01#2, re2ob_17-02#2]
- 2024-01-17 07:22 UTC — operation latency: shippingservice_GetQuote — baseline mean 0.175; later mean 0.3929 (x1.19); peak 3.00 at 2024-01-17 07:22:00 UTC [re2ob_17-02#0]
- 2024-01-17 07:23 UTC — metric anomalies: currencyservice_cpu — baseline median 29.64; peak 15.57 at 2024-01-17 07:23:04 UTC; sustained deviation from 2024-01-17 07:12:59 UTC (score 3.56) [re2ob_17-01#2]

## Detection: IDS Alerts

- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.25 (x2.25); peak 5.00 at 2024-01-17 07:16:30 UTC [re2ob_17-02#0]
- operation latency: frontendservice_frontend — baseline mean 1.00; later mean 3.27 (x2.13); peak 13.00 at 2024-01-17 07:17:30 UTC [re2ob_17-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-17 07:17:30 UTC [re2ob_17-02#0]
- operation latency: currencyservice_Convert — baseline mean 42.45; later mean 45.12 (x1.06); peak 85.00 at 2024-01-17 07:20:45 UTC [re2ob_17-02#1]
- operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.0536 (x1.05); peak 1.00 at 2024-01-17 07:15:45 UTC [re2ob_17-02#1]
- operation latency: adservice_GetAds — baseline mean 0.9; later mean 0.9821 (x1.04); peak 4.00 at 2024-01-17 07:14:45 UTC [re2ob_17-02#1]
- operation latency: productcatalogservice_GetProduct — baseline mean 6.15; later mean 6.38 (x1.03); peak 28.00 at 2024-01-17 07:17:30 UTC [re2ob_17-02#1]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 8.75; later mean 9.04 (x1.03); peak 20.00 at 2024-01-17 07:14:45 UTC [re2ob_17-02#2]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-17 07:21:30 UTC [re2ob_17-02#2]
- No matching results for: monitoring alerts / alerting rules (no alerts were recorded in this capture). (Absence in this query is not proof of absence elsewhere.) [re2ob_17-07#0]
- No matching results for: change records / deployments (no change-management data in this capture). (Absence in this query is not proof of absence elsewhere.) [re2ob_17-07#0]
- Disk I/O metrics contain data only for: adservice, emailservice, recommendationservice, redis. [re2ob_17-07#0]
- No matching results for: error- or warning-level application logs (all log lines are info or debug). (Absence in this query is not proof of absence elsewhere.) [re2ob_17-07#0]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_17-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_17-03#0]
2. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 8.75; later mean 9.04 (x1.03); peak 20.00 at 2024-01-17 07:14:45 UTC [re2ob_17-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-17 07:21:30 UTC [re2ob_17-02#2]
4. Not established from the available artifacts.
5. log volume: shippingservice — 436 lines/min in the baseline, 448 lines/min later [re2ob_17-04#0]
6. log volume: currencyservice — 2326 lines/min in the baseline, 2368 lines/min later [re2ob_17-04#0]
7. log volume: adservice — 454 lines/min in the baseline, 447 lines/min later [re2ob_17-04#0]
8. Not established from the available artifacts.
