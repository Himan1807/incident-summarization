# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 14 of 75 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_06-01#0]
- metric anomalies: frontend_error — no data in the baseline; series appears at 2024-01-19 09:24:43 UTC (first value 0); peak 0 at 2024-01-19 09:24:43 UTC [re2ob_06-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 24493 at 2024-01-19 09:32:14 UTC; sustained deviation from 2024-01-19 09:26:58 UTC (score 138) [re2ob_06-01#0]
- metric anomalies: checkoutservice_cpu — baseline median 0.4014; peak 19.60 at 2024-01-19 09:26:09 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 100) [re2ob_06-01#0]
- metric anomalies: frontend_socket — baseline median 19.00; peak 22.00 at 2024-01-19 09:26:36 UTC; sustained deviation from 2024-01-19 09:26:36 UTC (score 10.00) [re2ob_06-01#2]
- metric anomalies: frontend_cpu — baseline median 8.45; peak 4.47 at 2024-01-19 09:32:20 UTC; sustained deviation from 2024-01-19 09:23:15 UTC (score 3.50) [re2ob_06-01#2]
- metric anomalies: currencyservice_cpu — baseline median 33.73; peak 20.40 at 2024-01-19 09:31:37 UTC; sustained deviation from 2024-01-19 09:23:28 UTC (score 2.54) [re2ob_06-01#2]
- metric anomalies: redis_cpu — baseline median 0.3001; peak 0.1722 at 2024-01-19 09:37:12 UTC; sustained deviation from 2024-01-19 09:24:13 UTC (score 2.52) [re2ob_06-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.86; peak 1.67 at 2024-01-19 09:33:48 UTC; sustained deviation from 2024-01-19 09:30:15 UTC (score 2.27) [re2ob_06-01#3]
- metric anomalies: checkoutservice_socket — baseline median 9.00; peak 23.00 at 2024-01-19 09:26:08 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 63.41) [re2ob_06-01#1]
- metric anomalies: checkoutservice_mem — baseline median 10031104; peak 21483520 at 2024-01-19 09:28:31 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 25.24) [re2ob_06-01#1]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2235; peak 0.8409 at 2024-01-19 09:26:08 UTC; sustained deviation from 2024-01-19 09:25:31 UTC (score 22.39) [re2ob_06-01#1]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1079; peak 0.4286 at 2024-01-19 09:26:16 UTC; sustained deviation from 2024-01-19 09:25:53 UTC (score 11.93) [re2ob_06-01#1]

## Timeline

- 2024-01-19 09:17 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', 'L9ECAV7KIM', '2ZYFJ3GM2N', '66VCHSJNUP', '0' — 4 lines in the baseline, last at 2024-01-19 09:17:56 UTC [re2ob_06-04#3]
- 2024-01-19 09:22 UTC — log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-f9c8-4aff-9c7d-<*>, productId=6E92ZMYYFZ, quantity=<*>' — 5 lines in the baseline, last at 2024-01-19 09:22:32 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', '2ZYFJ3GM2N', '1YMWWN1N4O', 'LS4PSXUNUM', '6' — 4 lines in the baseline, last at 2024-01-19 09:22:40 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', '0PUK6V6EV0', '66VCHSJNUP', 'LS4PSXUNUM', 'L' — 4 lines in the baseline, last at 2024-01-19 09:22:18 UTC [re2ob_06-04#3]
- 2024-01-19 09:23 UTC — log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-acec-4a84-b627-<*>, productId=LS4PSXUNUM, quantity=<*>' — 12 lines, first at 2024-01-19 09:23:22 UTC; earliest sustained metric deviation: frontend_cpu from 2024-01-19 09:23:15 UTC [re2ob_06-04#2, re2ob_06-06#0]
- 2024-01-19 09:24 UTC — metric anomalies: frontend_error — no data in the baseline; series appears at 2024-01-19 09:24:43 UTC (first value 0); peak 0 at 2024-01-19 09:24:43 UTC; metric series without baseline data that appears during the capture: frontend_error (from 2024-01-19 09:24:43 UTC) [re2ob_06-01#0, re2ob_06-06#0]
- 2024-01-19 09:25 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.5714 (x1.57); peak 8.00 at 2024-01-19 09:25:30 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3036 (x1.30); peak 3.00 at 2024-01-19 09:25:30 UTC; operation latency: traceservice_Export — baseline mean 0.2439; later mean 0.5179 (x1.22); peak 2.00 at 2024-01-19 09:25:45 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.2143 (x1.21); peak 2.00 at 2024-01-19 09:25:30 UTC [re2ob_06-02#0, re2ob_06-02#1]
- 2024-01-19 09:26 UTC — metric anomalies: checkoutservice_cpu — baseline median 0.4014; peak 19.60 at 2024-01-19 09:26:09 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 100); metric anomalies: checkoutservice_socket — baseline median 9.00; peak 23.00 at 2024-01-19 09:26:08 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 63.41); metric anomalies: checkoutservice_latency-90 — baseline median 0.2235; peak 0.8409 at 2024-01-19 09:26:08 UTC; sustained deviation from 2024-01-19 09:25:31 UTC (score 22.39); metric anomalies: checkoutservice_latency-50 — baseline median 0.1079; peak 0.4286 at 2024-01-19 09:26:16 UTC; sustained deviation from 2024-01-19 09:25:53 UTC (score 11.93); metric anomalies: frontend_socket — baseline median 19.00; peak 22.00 at 2024-01-19 09:26:36 UTC; sustained deviation from 2024-01-19 09:26:36 UTC (score 10.00); operation latency: paymentservice_Charge — baseline mean 0.1; later mean 0.5179 (x1.38); peak 6.00 at 2024-01-19 09:26:45 UTC; operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.2857 (x1.29); peak 4.00 at 2024-01-19 09:26:15 UTC; operation latency: recommendationservice_ListRecommendations — baseline mean 0.5854; later mean 1.02 (x1.27); peak 12.00 at 2024-01-19 09:26:30 UTC; operation latency: frontendservice_frontend — baseline mean 2.51; later mean 3.16 (x1.18); peak 15.00 at 2024-01-19 09:26:30 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['6E92ZMYYFZ', '66VCHSJNUP']' — 8 lines, first at 2024-01-19 09:26:28 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['66VCHSJNUP', '6E92ZMYYFZ']' — 7 lines, first at 2024-01-19 09:26:18 UTC [re2ob_06-01#0, re2ob_06-01#1, re2ob_06-01#2, re2ob_06-02#0, re2ob_06-02#1, re2ob_06-02#2, re2ob_06-04#2]
- 2024-01-19 09:28 UTC — metric anomalies: checkoutservice_mem — baseline median 10031104; peak 21483520 at 2024-01-19 09:28:31 UTC; sustained deviation from 2024-01-19 09:25:20 UTC (score 25.24) [re2ob_06-01#1]
- 2024-01-19 09:30 UTC — log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['2ZYFJ3GM2N']' — 22 lines, first at 2024-01-19 09:30:56 UTC [re2ob_06-04#2]
- 2024-01-19 09:31 UTC — metric anomalies: currencyservice_cpu — baseline median 33.73; peak 20.40 at 2024-01-19 09:31:37 UTC; sustained deviation from 2024-01-19 09:23:28 UTC (score 2.54) [re2ob_06-01#2]
- 2024-01-19 09:32 UTC — metric anomalies: redis_diskio — baseline median 0; peak 24493 at 2024-01-19 09:32:14 UTC; sustained deviation from 2024-01-19 09:26:58 UTC (score 138); metric anomalies: frontend_cpu — baseline median 8.45; peak 4.47 at 2024-01-19 09:32:20 UTC; sustained deviation from 2024-01-19 09:23:15 UTC (score 3.50); operation latency: productcatalogservice_GetProduct — baseline mean 4.10; later mean 5.20 (x1.22); peak 21.00 at 2024-01-19 09:32:45 UTC [re2ob_06-01#0, re2ob_06-01#2, re2ob_06-02#1]
- 2024-01-19 09:33 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.86; peak 1.67 at 2024-01-19 09:33:48 UTC; sustained deviation from 2024-01-19 09:30:15 UTC (score 2.27); operation latency: cartservice_GetCart — baseline mean 0.5366; later mean 0.8571 (x1.21); peak 12.00 at 2024-01-19 09:33:45 UTC [re2ob_06-01#3, re2ob_06-02#2]
- 2024-01-19 09:37 UTC — metric anomalies: redis_cpu — baseline median 0.3001; peak 0.1722 at 2024-01-19 09:37:12 UTC; sustained deviation from 2024-01-19 09:24:13 UTC (score 2.52) [re2ob_06-01#2]

## Detection: IDS Alerts

- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.5714 (x1.57); peak 8.00 at 2024-01-19 09:25:30 UTC [re2ob_06-02#0]
- operation latency: paymentservice_Charge — baseline mean 0.1; later mean 0.5179 (x1.38); peak 6.00 at 2024-01-19 09:26:45 UTC [re2ob_06-02#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3036 (x1.30); peak 3.00 at 2024-01-19 09:25:30 UTC [re2ob_06-02#0]
- operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.2857 (x1.29); peak 4.00 at 2024-01-19 09:26:15 UTC [re2ob_06-02#0]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: cartservice_GetCart — baseline mean 0.5366; later mean 0.8571 (x1.21); peak 12.00 at 2024-01-19 09:33:45 UTC [re2ob_06-02#2]
- operation latency: frontendservice_frontend — baseline mean 2.51; later mean 3.16 (x1.18); peak 15.00 at 2024-01-19 09:26:30 UTC [re2ob_06-02#2]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.5854; later mean 1.02 (x1.27); peak 12.00 at 2024-01-19 09:26:30 UTC [re2ob_06-02#1]
- operation latency: traceservice_Export — baseline mean 0.2439; later mean 0.5179 (x1.22); peak 2.00 at 2024-01-19 09:25:45 UTC [re2ob_06-02#1]
- operation latency: productcatalogservice_GetProduct — baseline mean 4.10; later mean 5.20 (x1.22); peak 21.00 at 2024-01-19 09:32:45 UTC [re2ob_06-02#1]
- operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.2143 (x1.21); peak 2.00 at 2024-01-19 09:25:30 UTC [re2ob_06-02#1]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_06-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_06-03#0]
2. operation latency: cartservice_GetCart — baseline mean 0.5366; later mean 0.8571 (x1.21); peak 12.00 at 2024-01-19 09:33:45 UTC [re2ob_06-02#2]
3. operation latency: frontendservice_frontend — baseline mean 2.51; later mean 3.16 (x1.18); peak 15.00 at 2024-01-19 09:26:30 UTC [re2ob_06-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', 'L9ECAV7KIM', '2ZYFJ3GM2N', '66VCHSJNUP', '0' — 4 lines in the baseline, last at 2024-01-19 09:17:56 UTC [re2ob_06-04#3]
6. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', '2ZYFJ3GM2N', '1YMWWN1N4O', 'LS4PSXUNUM', '6' — 4 lines in the baseline, last at 2024-01-19 09:22:40 UTC [re2ob_06-04#3]
7. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', '0PUK6V6EV0', '66VCHSJNUP', 'LS4PSXUNUM', 'L' — 4 lines in the baseline, last at 2024-01-19 09:22:18 UTC [re2ob_06-04#3]
8. Not established from the available artifacts.
