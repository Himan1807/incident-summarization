# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 21 of 75 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_07-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 22696 at 2024-01-19 16:53:42 UTC; sustained deviation from 2024-01-19 16:48:18 UTC (score 126) [re2ob_07-01#0]
- metric anomalies: currencyservice_latency-50 — baseline median 0.004; peak 0.0519 at 2024-01-19 16:52:40 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 102) [re2ob_07-01#0]
- metric anomalies: currencyservice_socket — baseline median 4.00; peak 6.00 at 2024-01-19 16:47:12 UTC; sustained deviation from 2024-01-19 16:47:12 UTC (score 28.57) [re2ob_07-01#0]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1054; peak 0.25 at 2024-01-19 16:49:38 UTC; sustained deviation from 2024-01-19 16:48:38 UTC (score 4.62) [re2ob_07-01#3]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0.2927; later mean 4.00 (x3.87); peak 17.00 at 2024-01-19 16:47:30 UTC [re2ob_07-02#0]
- operation latency: frontendservice_frontend — baseline mean 1.05; later mean 5.77 (x3.30); peak 28.00 at 2024-01-19 16:47:15 UTC [re2ob_07-02#0]
- operation latency: currencyservice_Convert — baseline mean 0.439; later mean 2.68 (x2.56); peak 13.00 at 2024-01-19 16:49:00 UTC [re2ob_07-02#0]
- operation latency: cartservice_GetCart — baseline mean 1.51; later mean 2.66 (x1.46); peak 21.00 at 2024-01-19 16:47:15 UTC [re2ob_07-02#0]
- metric anomalies: frontend_latency-50 — baseline median 0.0507; peak 0.1743 at 2024-01-19 16:48:03 UTC; sustained deviation from 2024-01-19 16:47:31 UTC (score 27.98) [re2ob_07-01#1]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2271; peak 0.75 at 2024-01-19 16:51:31 UTC; sustained deviation from 2024-01-19 16:47:46 UTC (score 20.55) [re2ob_07-01#1]
- metric anomalies: cartservice_latency-90 — baseline median 0.0048; peak 0.0095 at 2024-01-19 16:48:08 UTC; sustained deviation from 2024-01-19 16:47:46 UTC (score 17.59) [re2ob_07-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.2024; peak 0.4958 at 2024-01-19 16:48:03 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 13.74) [re2ob_07-01#1]

## Timeline

- 2024-01-19 16:39 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['9SIQT8TOJO', 'L9ECAV7KIM', '6E92ZMYYFZ', 'LS4PSXUNUM', '0' — 4 lines in the baseline, last at 2024-01-19 16:39:45 UTC [re2ob_07-04#3]
- 2024-01-19 16:40 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z', '9SIQT8TOJO', '6E92ZMYYFZ', '0PUK6V6EV0', 'L' — 4 lines in the baseline, last at 2024-01-19 16:40:38 UTC [re2ob_07-04#3]
- 2024-01-19 16:43 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', '66VCHSJNUP', '6E92ZMYYFZ', 'LS4PSXUNUM', 'O' — 4 lines in the baseline, last at 2024-01-19 16:43:00 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', '66VCHSJNUP', '0PUK6V6EV0', '6E92ZMYYFZ', '9' — 4 lines in the baseline, last at 2024-01-19 16:43:29 UTC [re2ob_07-04#3]
- 2024-01-19 16:45 UTC — log templates: new after the baseline: 'paymentservice Transaction processed: visa ending <*> Amount: CAD139.<*>' — 5 lines, first at 2024-01-19 16:45:41 UTC; earliest sustained metric deviation: redis_cpu from 2024-01-19 16:45:14 UTC [re2ob_07-04#2, re2ob_07-06#0]
- 2024-01-19 16:46 UTC — operation latency: cartservice_AddItem — baseline mean 0.122; later mean 0.1786 (x1.05); peak 2.00 at 2024-01-19 16:46:00 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-d0a1-492f-9b0a-<*>, productId=66VCHSJNUP, quantity=<*>' — 5 lines, first at 2024-01-19 16:46:24 UTC [re2ob_07-02#2, re2ob_07-04#2]
- 2024-01-19 16:47 UTC — metric anomalies: currencyservice_socket — baseline median 4.00; peak 6.00 at 2024-01-19 16:47:12 UTC; sustained deviation from 2024-01-19 16:47:12 UTC (score 28.57); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0.2927; later mean 4.00 (x3.87); peak 17.00 at 2024-01-19 16:47:30 UTC; operation latency: frontendservice_frontend — baseline mean 1.05; later mean 5.77 (x3.30); peak 28.00 at 2024-01-19 16:47:15 UTC; operation latency: cartservice_GetCart — baseline mean 1.51; later mean 2.66 (x1.46); peak 21.00 at 2024-01-19 16:47:15 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.2927; later mean 0.6786 (x1.30); peak 4.00 at 2024-01-19 16:47:15 UTC [re2ob_07-01#0, re2ob_07-02#0, re2ob_07-02#1]
- 2024-01-19 16:48 UTC — metric anomalies: frontend_latency-50 — baseline median 0.0507; peak 0.1743 at 2024-01-19 16:48:03 UTC; sustained deviation from 2024-01-19 16:47:31 UTC (score 27.98); metric anomalies: cartservice_latency-90 — baseline median 0.0048; peak 0.0095 at 2024-01-19 16:48:08 UTC; sustained deviation from 2024-01-19 16:47:46 UTC (score 17.59); metric anomalies: frontend_latency-90 — baseline median 0.2024; peak 0.4958 at 2024-01-19 16:48:03 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 13.74); metric anomalies: currencyservice_latency-90 — baseline median 0.0504; peak 0.0916 at 2024-01-19 16:48:31 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 5.93); log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-d0a1-492f-9b0a-<*>, productId=6E92ZMYYFZ, quantity=<*>' — 6 lines, first at 2024-01-19 16:48:52 UTC [re2ob_07-01#1, re2ob_07-01#2, re2ob_07-04#2]
- 2024-01-19 16:49 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.1054; peak 0.25 at 2024-01-19 16:49:38 UTC; sustained deviation from 2024-01-19 16:48:38 UTC (score 4.62); operation latency: currencyservice_Convert — baseline mean 0.439; later mean 2.68 (x2.56); peak 13.00 at 2024-01-19 16:49:00 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0.0732; later mean 0.1429 (x1.06); peak 1.00 at 2024-01-19 16:49:00 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0.1463; later mean 0.2143 (x1.06); peak 4.00 at 2024-01-19 16:49:00 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['66VCHSJNUP', '2ZYFJ3GM2N', 'LS4PSXUNUM']' — 5 lines, first at 2024-01-19 16:49:32 UTC [re2ob_07-01#3, re2ob_07-02#0, re2ob_07-02#1, re2ob_07-04#2]
- 2024-01-19 16:51 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.2271; peak 0.75 at 2024-01-19 16:51:31 UTC; sustained deviation from 2024-01-19 16:47:46 UTC (score 20.55); metric anomalies: redis_cpu — baseline median 0.2984; peak 0.1356 at 2024-01-19 16:51:53 UTC; sustained deviation from 2024-01-19 16:45:14 UTC (score 6.51) [re2ob_07-01#1, re2ob_07-01#2]
- 2024-01-19 16:52 UTC — metric anomalies: currencyservice_latency-50 — baseline median 0.004; peak 0.0519 at 2024-01-19 16:52:40 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 102) [re2ob_07-01#0]
- 2024-01-19 16:53 UTC — metric anomalies: redis_diskio — baseline median 0; peak 22696 at 2024-01-19 16:53:42 UTC; sustained deviation from 2024-01-19 16:48:18 UTC (score 126) [re2ob_07-01#0]
- 2024-01-19 16:54 UTC — operation latency: cartservice_EmptyCart — baseline mean 0; later mean 0.0714 (x1.07); peak 2.00 at 2024-01-19 16:54:45 UTC [re2ob_07-02#1]
- 2024-01-19 16:56 UTC — operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0536 (x1.03); peak 2.00 at 2024-01-19 16:56:15 UTC [re2ob_07-02#2]
- 2024-01-19 16:58 UTC — metric anomalies: paymentservice_latency-90 — baseline median 0.0049; peak 0.0081 at 2024-01-19 16:58:25 UTC; sustained deviation from 2024-01-19 16:46:23 UTC (score 9.24); metric anomalies: currencyservice_cpu — baseline median 33.28; peak 50.07 at 2024-01-19 16:58:44 UTC; sustained deviation from 2024-01-19 16:45:43 UTC (score 8.45) [re2ob_07-01#2]

## Detection: IDS Alerts



## Initial Infection Indicators

- metric anomalies: paymentservice_latency-90 — baseline median 0.0049; peak 0.0081 at 2024-01-19 16:58:25 UTC; sustained deviation from 2024-01-19 16:46:23 UTC (score 9.24) [re2ob_07-01#2]
- metric anomalies: currencyservice_cpu — baseline median 33.28; peak 50.07 at 2024-01-19 16:58:44 UTC; sustained deviation from 2024-01-19 16:45:43 UTC (score 8.45) [re2ob_07-01#2]
- metric anomalies: redis_cpu — baseline median 0.2984; peak 0.1356 at 2024-01-19 16:51:53 UTC; sustained deviation from 2024-01-19 16:45:14 UTC (score 6.51) [re2ob_07-01#2]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0504; peak 0.0916 at 2024-01-19 16:48:31 UTC; sustained deviation from 2024-01-19 16:47:33 UTC (score 5.93) [re2ob_07-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: cartservice_AddItem — baseline mean 0.122; later mean 0.1786 (x1.05); peak 2.00 at 2024-01-19 16:46:00 UTC [re2ob_07-02#2]
- operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0536 (x1.03); peak 2.00 at 2024-01-19 16:56:15 UTC [re2ob_07-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_07-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_07-03#0]
2. operation latency: cartservice_AddItem — baseline mean 0.122; later mean 0.1786 (x1.05); peak 2.00 at 2024-01-19 16:46:00 UTC [re2ob_07-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0536 (x1.03); peak 2.00 at 2024-01-19 16:56:15 UTC [re2ob_07-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', '66VCHSJNUP', '6E92ZMYYFZ', 'LS4PSXUNUM', 'O' — 4 lines in the baseline, last at 2024-01-19 16:43:00 UTC [re2ob_07-04#3]
6. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', '66VCHSJNUP', '0PUK6V6EV0', '6E92ZMYYFZ', '9' — 4 lines in the baseline, last at 2024-01-19 16:43:29 UTC [re2ob_07-04#3]
7. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['9SIQT8TOJO', 'L9ECAV7KIM', '6E92ZMYYFZ', 'LS4PSXUNUM', '0' — 4 lines in the baseline, last at 2024-01-19 16:39:45 UTC [re2ob_07-04#3]
8. Not established from the available artifacts.
