# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 15 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_18-01#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0941 at 2024-01-20 04:51:55 UTC; sustained deviation from 2024-01-20 04:51:19 UTC (score 165) [re2ob_18-01#0]
- metric anomalies: emailservice_cpu — baseline median 0.2877; peak 19.32 at 2024-01-20 04:52:05 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 151) [re2ob_18-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 33291 at 2024-01-20 04:51:44 UTC; sustained deviation from 2024-01-20 04:51:18 UTC (score 109) [re2ob_18-01#0]
- metric anomalies: emailservice_workload — baseline median 0.867; peak 2.00 at 2024-01-20 04:57:25 UTC; sustained deviation from 2024-01-20 04:57:25 UTC (score 2.45) [re2ob_18-01#3]
- operation latency: currencyservice_Convert — baseline mean 42.75; later mean 41.32 (x0.9673); peak 83.00 at 2024-01-20 04:55:45 UTC [re2ob_18-02#2]
- operation latency: frontendservice_frontend — baseline mean 2.55; later mean 2.43 (x0.9658); peak 21.00 at 2024-01-20 04:56:45 UTC [re2ob_18-02#2]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.41 (x2.41); peak 9.00 at 2024-01-20 04:51:15 UTC [re2ob_18-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 5.70; later mean 6.71 (x1.15); peak 40.00 at 2024-01-20 05:02:00 UTC [re2ob_18-02#0]
- operation latency: shippingservice_ShipOrder — baseline mean 0.1; later mean 0.25 (x1.14); peak 4.00 at 2024-01-20 04:55:45 UTC [re2ob_18-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.05; later mean 0.1786 (x1.12); peak 4.00 at 2024-01-20 05:02:00 UTC [re2ob_18-02#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0704 at 2024-01-20 04:51:55 UTC; sustained deviation from 2024-01-20 04:51:34 UTC (score 90.32) [re2ob_18-01#1]
- metric anomalies: emailservice_socket — baseline median 3.00; peak 10.00 at 2024-01-20 04:51:05 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 87.50) [re2ob_18-01#1]
- metric anomalies: emailservice_mem — baseline median 43184128; peak 55771136 at 2024-01-20 04:56:22 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 15.22) [re2ob_18-01#1]
- metric anomalies: redis_cpu — baseline median 0.3113; peak 0.1177 at 2024-01-20 04:57:49 UTC; sustained deviation from 2024-01-20 04:51:45 UTC (score 3.98) [re2ob_18-01#1]

## Timeline

- 2024-01-20 04:45 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['66VCHSJNUP']' — 7 lines in the baseline, last at 2024-01-20 04:45:14 UTC; log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-b713-4e95-<*>-<*>, productId=66VCHSJNUP, quantity=<*>' — 5 lines in the baseline, last at 2024-01-20 04:45:35 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['LS4PSXUNUM', '6E92ZMYYFZ', 'OLJCESPC7Z', '1YMWWN1N4O', 'L' — 4 lines in the baseline, last at 2024-01-20 04:45:23 UTC [re2ob_18-04#3]
- 2024-01-20 04:48 UTC — log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-feb9-<*>-b925-<*>, productId=L9ECAV7KIM, quantity=<*>' — 6 lines in the baseline, last at 2024-01-20 04:48:09 UTC [re2ob_18-04#3]
- 2024-01-20 04:49 UTC — earliest sustained metric deviation: productcatalogservice_cpu from 2024-01-20 04:49:26 UTC [re2ob_18-06#0]
- 2024-01-20 04:50 UTC — log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-7d33-4bd6-b979-<*>, productId=9SIQT8TOJO, quantity=<*>' — 6 lines, first at 2024-01-20 04:50:09 UTC [re2ob_18-04#2]
- 2024-01-20 04:51 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0941 at 2024-01-20 04:51:55 UTC; sustained deviation from 2024-01-20 04:51:19 UTC (score 165); metric anomalies: redis_diskio — baseline median 0; peak 33291 at 2024-01-20 04:51:44 UTC; sustained deviation from 2024-01-20 04:51:18 UTC (score 109); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0704 at 2024-01-20 04:51:55 UTC; sustained deviation from 2024-01-20 04:51:34 UTC (score 90.32); metric anomalies: emailservice_socket — baseline median 3.00; peak 10.00 at 2024-01-20 04:51:05 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 87.50); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 1.41 (x2.41); peak 9.00 at 2024-01-20 04:51:15 UTC [re2ob_18-01#0, re2ob_18-01#1, re2ob_18-02#0]
- 2024-01-20 04:52 UTC — metric anomalies: emailservice_cpu — baseline median 0.2877; peak 19.32 at 2024-01-20 04:52:05 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 151) [re2ob_18-01#0]
- 2024-01-20 04:53 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.48 at 2024-01-20 04:53:24 UTC; sustained deviation from 2024-01-20 04:53:21 UTC (score 3.30); metric anomalies: paymentservice_latency-90 — baseline median 0.0086; peak 0.0123 at 2024-01-20 04:53:25 UTC; sustained deviation from 2024-01-20 04:53:25 UTC (score 2.81); operation latency: paymentservice_Charge — baseline mean 0.025; later mean 0.0357 (x1.01); peak 1.00 at 2024-01-20 04:53:00 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 12.53; later mean 12.09 (x0.9678); peak 26.00 at 2024-01-20 04:53:45 UTC [re2ob_18-01#2, re2ob_18-02#1]
- 2024-01-20 04:54 UTC — log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['1YMWWN1N4O', '0PUK6V6EV0']' — 11 lines, first at 2024-01-20 04:54:39 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['0PUK6V6EV0', '1YMWWN1N4O']' — 7 lines, first at 2024-01-20 04:54:29 UTC [re2ob_18-04#2]
- 2024-01-20 04:55 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0.1; later mean 0.25 (x1.14); peak 4.00 at 2024-01-20 04:55:45 UTC; operation latency: currencyservice_Convert — baseline mean 42.75; later mean 41.32 (x0.9673); peak 83.00 at 2024-01-20 04:55:45 UTC [re2ob_18-02#0, re2ob_18-02#2]
- 2024-01-20 04:56 UTC — metric anomalies: emailservice_mem — baseline median 43184128; peak 55771136 at 2024-01-20 04:56:22 UTC; sustained deviation from 2024-01-20 04:51:05 UTC (score 15.22); operation latency: cartservice_AddItem — baseline mean 0.05; later mean 0.0536 (x1.00); peak 3.00 at 2024-01-20 04:56:45 UTC; operation latency: frontendservice_frontend — baseline mean 2.55; later mean 2.43 (x0.9658); peak 21.00 at 2024-01-20 04:56:45 UTC [re2ob_18-01#1, re2ob_18-02#1, re2ob_18-02#2]
- 2024-01-20 04:57 UTC — metric anomalies: redis_cpu — baseline median 0.3113; peak 0.1177 at 2024-01-20 04:57:49 UTC; sustained deviation from 2024-01-20 04:51:45 UTC (score 3.98); metric anomalies: emailservice_workload — baseline median 0.867; peak 2.00 at 2024-01-20 04:57:25 UTC; sustained deviation from 2024-01-20 04:57:25 UTC (score 2.45); log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['9SIQT8TOJO', '66VCHSJNUP']' — 9 lines, first at 2024-01-20 04:57:44 UTC [re2ob_18-01#1, re2ob_18-01#3, re2ob_18-04#2]
- 2024-01-20 04:59 UTC — metric anomalies: frontend_cpu — baseline median 7.81; peak 4.92 at 2024-01-20 04:59:18 UTC; sustained deviation from 2024-01-20 04:58:14 UTC (score 3.09); operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.0357 (x1.04); peak 1.00 at 2024-01-20 04:59:00 UTC [re2ob_18-01#2, re2ob_18-02#1]
- 2024-01-20 05:01 UTC — metric anomalies: productcatalogservice_cpu — baseline median 4.01; peak 1.98 at 2024-01-20 05:01:48 UTC; sustained deviation from 2024-01-20 04:49:26 UTC (score 2.83) [re2ob_18-01#2]
- 2024-01-20 05:02 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 5.70; later mean 6.71 (x1.15); peak 40.00 at 2024-01-20 05:02:00 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0.05; later mean 0.1786 (x1.12); peak 4.00 at 2024-01-20 05:02:00 UTC [re2ob_18-02#0]

## Detection: IDS Alerts



## Initial Infection Indicators

- metric anomalies: recommendationservice_cpu — baseline median 2.76; peak 1.48 at 2024-01-20 04:53:24 UTC; sustained deviation from 2024-01-20 04:53:21 UTC (score 3.30) [re2ob_18-01#2]
- metric anomalies: frontend_cpu — baseline median 7.81; peak 4.92 at 2024-01-20 04:59:18 UTC; sustained deviation from 2024-01-20 04:58:14 UTC (score 3.09) [re2ob_18-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 4.01; peak 1.98 at 2024-01-20 05:01:48 UTC; sustained deviation from 2024-01-20 04:49:26 UTC (score 2.83) [re2ob_18-01#2]
- metric anomalies: paymentservice_latency-90 — baseline median 0.0086; peak 0.0123 at 2024-01-20 04:53:25 UTC; sustained deviation from 2024-01-20 04:53:25 UTC (score 2.81) [re2ob_18-01#2]

## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_18-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_18-03#0]
2. operation latency: currencyservice_Convert — baseline mean 42.75; later mean 41.32 (x0.9673); peak 83.00 at 2024-01-20 04:55:45 UTC [re2ob_18-02#2]
3. operation latency: frontendservice_frontend — baseline mean 2.55; later mean 2.43 (x0.9658); peak 21.00 at 2024-01-20 04:56:45 UTC [re2ob_18-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-feb9-<*>-b925-<*>, productId=L9ECAV7KIM, quantity=<*>' — 6 lines in the baseline, last at 2024-01-20 04:48:09 UTC [re2ob_18-04#3]
6. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-b713-4e95-<*>-<*>, productId=66VCHSJNUP, quantity=<*>' — 5 lines in the baseline, last at 2024-01-20 04:45:35 UTC [re2ob_18-04#3]
7. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['LS4PSXUNUM', '6E92ZMYYFZ', 'OLJCESPC7Z', '1YMWWN1N4O', 'L' — 4 lines in the baseline, last at 2024-01-20 04:45:23 UTC [re2ob_18-04#3]
8. Not established from the available artifacts.
