# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 10 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_14-01#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.2248 at 2024-01-20 06:58:19 UTC; sustained deviation from 2024-01-20 06:49:25 UTC (score 186) [re2ob_14-01#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1239 at 2024-01-20 06:58:19 UTC; sustained deviation from 2024-01-20 06:49:55 UTC (score 164) [re2ob_14-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 27396 at 2024-01-20 06:47:17 UTC; sustained deviation from 2024-01-20 06:47:06 UTC (score 124) [re2ob_14-01#0]
- operation latency: shippingservice_GetQuote — baseline mean 0.2195; later mean 0.2679 (x1.04); peak 2.00 at 2024-01-20 06:47:15 UTC [re2ob_14-02#1]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 12.05; later mean 12.39 (x1.03); peak 21.00 at 2024-01-20 06:50:30 UTC [re2ob_14-02#1]
- operation latency: currencyservice_Convert — baseline mean 39.71; later mean 40.59 (x1.02); peak 68.00 at 2024-01-20 06:51:00 UTC [re2ob_14-02#1]
- operation latency: adservice_GetAds — baseline mean 0.6098; later mean 0.625 (x1.01); peak 3.00 at 2024-01-20 07:00:30 UTC [re2ob_14-02#1]
- operation latency: frontendservice_frontend — baseline mean 1.88; later mean 5.12 (x2.13); peak 16.00 at 2024-01-20 06:54:00 UTC [re2ob_14-02#0]
- operation latency: health_Check — baseline mean 0.1707; later mean 0.2679 (x1.08); peak 3.00 at 2024-01-20 06:55:30 UTC [re2ob_14-02#0]
- operation latency: shippingservice_ShipOrder — baseline mean 0.0976; later mean 0.1607 (x1.06); peak 1.00 at 2024-01-20 06:47:15 UTC [re2ob_14-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0.8537; later mean 0.9464 (x1.05); peak 9.00 at 2024-01-20 06:49:15 UTC [re2ob_14-02#0]
- metric anomalies: frontend_cpu — baseline median 7.90; peak 5.06 at 2024-01-20 06:57:46 UTC; sustained deviation from 2024-01-20 06:50:58 UTC (score 3.13) [re2ob_14-01#2]
- metric anomalies: currencyservice_cpu — baseline median 32.34; peak 18.85 at 2024-01-20 07:00:10 UTC; sustained deviation from 2024-01-20 06:59:29 UTC (score 2.94) [re2ob_14-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.90; peak 2.32 at 2024-01-20 06:55:08 UTC; sustained deviation from 2024-01-20 06:55:08 UTC (score 2.56) [re2ob_14-01#2]

## Timeline

- 2024-01-20 06:45 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['1YMWWN1N4O']' — 18 lines in the baseline, last at 2024-01-20 06:45:27 UTC [re2ob_14-04#3]
- 2024-01-20 06:46 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM']' — 10 lines in the baseline, last at 2024-01-20 06:46:50 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', 'LS4PSXUNUM', '2ZYFJ3GM2N', '66VCHSJNUP', '9' — 5 lines in the baseline, last at 2024-01-20 06:46:54 UTC; log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-68e4-4ea6-9ea9-<*>, productId=66VCHSJNUP, quantity=<*>' — 5 lines in the baseline, last at 2024-01-20 06:46:11 UTC [re2ob_14-04#3]
- 2024-01-20 06:47 UTC — metric anomalies: redis_diskio — baseline median 0; peak 27396 at 2024-01-20 06:47:17 UTC; sustained deviation from 2024-01-20 06:47:06 UTC (score 124); metric anomalies: frontend_socket — baseline median 24.00; peak 26.00 at 2024-01-20 06:47:06 UTC; sustained deviation from 2024-01-20 06:47:06 UTC (score 5.41); operation latency: shippingservice_ShipOrder — baseline mean 0.0976; later mean 0.1607 (x1.06); peak 1.00 at 2024-01-20 06:47:15 UTC; operation latency: shippingservice_GetQuote — baseline mean 0.2195; later mean 0.2679 (x1.04); peak 2.00 at 2024-01-20 06:47:15 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-20 06:47:15 UTC; operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-20 06:47:15 UTC; earliest sustained metric deviation: redis_diskio from 2024-01-20 06:47:06 UTC [re2ob_14-01#0, re2ob_14-01#1, re2ob_14-02#0, re2ob_14-02#1, re2ob_14-02#2, re2ob_14-06#0]
- 2024-01-20 06:49 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.8537; later mean 0.9464 (x1.05); peak 9.00 at 2024-01-20 06:49:15 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['9SIQT8TOJO']' — 11 lines, first at 2024-01-20 06:49:26 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-dff5-4a10-<*>-<*>, productId=66VCHSJNUP, quantity=<*>' — 7 lines, first at 2024-01-20 06:49:06 UTC [re2ob_14-02#0, re2ob_14-04#2]
- 2024-01-20 06:50 UTC — operation latency: currencyservice_GetSupportedCurrencies — baseline mean 12.05; later mean 12.39 (x1.03); peak 21.00 at 2024-01-20 06:50:30 UTC [re2ob_14-02#1]
- 2024-01-20 06:51 UTC — operation latency: currencyservice_Convert — baseline mean 39.71; later mean 40.59 (x1.02); peak 68.00 at 2024-01-20 06:51:00 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['0PUK6V6EV0']' — 10 lines, first at 2024-01-20 06:51:26 UTC [re2ob_14-02#1, re2ob_14-04#2]
- 2024-01-20 06:52 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.2216; peak 0.4898 at 2024-01-20 06:52:27 UTC; sustained deviation from 2024-01-20 06:49:27 UTC (score 19.78); log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['LS4PSXUNUM', '2ZYFJ3GM2N']' — 8 lines, first at 2024-01-20 06:52:20 UTC [re2ob_14-01#1, re2ob_14-04#2]
- 2024-01-20 06:55 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.90; peak 2.32 at 2024-01-20 06:55:08 UTC; sustained deviation from 2024-01-20 06:55:08 UTC (score 2.56); operation latency: health_Check — baseline mean 0.1707; later mean 0.2679 (x1.08); peak 3.00 at 2024-01-20 06:55:30 UTC [re2ob_14-01#2, re2ob_14-02#0]
- 2024-01-20 06:56 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.1; peak 0.359 at 2024-01-20 06:56:42 UTC; sustained deviation from 2024-01-20 06:49:55 UTC (score 10.60) [re2ob_14-01#1]
- 2024-01-20 06:57 UTC — metric anomalies: frontend_cpu — baseline median 7.90; peak 5.06 at 2024-01-20 06:57:46 UTC; sustained deviation from 2024-01-20 06:50:58 UTC (score 3.13) [re2ob_14-01#2]
- 2024-01-20 06:58 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.2248 at 2024-01-20 06:58:19 UTC; sustained deviation from 2024-01-20 06:49:25 UTC (score 186); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1239 at 2024-01-20 06:58:19 UTC; sustained deviation from 2024-01-20 06:49:55 UTC (score 164) [re2ob_14-01#0]
- 2024-01-20 07:00 UTC — metric anomalies: currencyservice_cpu — baseline median 32.34; peak 18.85 at 2024-01-20 07:00:10 UTC; sustained deviation from 2024-01-20 06:59:29 UTC (score 2.94); operation latency: adservice_GetAds — baseline mean 0.6098; later mean 0.625 (x1.01); peak 3.00 at 2024-01-20 07:00:30 UTC [re2ob_14-01#2, re2ob_14-02#1]
- 2024-01-20 07:01 UTC — metric anomalies: redis_cpu — baseline median 0.3036; peak 0.1268 at 2024-01-20 07:01:02 UTC; sustained deviation from 2024-01-20 06:47:39 UTC (score 4.86) [re2ob_14-01#1]

## Detection: IDS Alerts

- metric anomalies: checkoutservice_latency-90 — baseline median 0.2216; peak 0.4898 at 2024-01-20 06:52:27 UTC; sustained deviation from 2024-01-20 06:49:27 UTC (score 19.78) [re2ob_14-01#1]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1; peak 0.359 at 2024-01-20 06:56:42 UTC; sustained deviation from 2024-01-20 06:49:55 UTC (score 10.60) [re2ob_14-01#1]
- metric anomalies: frontend_socket — baseline median 24.00; peak 26.00 at 2024-01-20 06:47:06 UTC; sustained deviation from 2024-01-20 06:47:06 UTC (score 5.41) [re2ob_14-01#1]
- metric anomalies: redis_cpu — baseline median 0.3036; peak 0.1268 at 2024-01-20 07:01:02 UTC; sustained deviation from 2024-01-20 06:47:39 UTC (score 4.86) [re2ob_14-01#1]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-20 06:47:15 UTC [re2ob_14-02#2]
- operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-20 06:47:15 UTC [re2ob_14-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_14-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_14-03#0]
2. operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-20 06:47:15 UTC [re2ob_14-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-20 06:47:15 UTC [re2ob_14-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM']' — 10 lines in the baseline, last at 2024-01-20 06:46:50 UTC [re2ob_14-04#3]
6. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['L9ECAV7KIM', 'LS4PSXUNUM', '2ZYFJ3GM2N', '66VCHSJNUP', '9' — 5 lines in the baseline, last at 2024-01-20 06:46:54 UTC [re2ob_14-04#3]
7. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-68e4-4ea6-9ea9-<*>, productId=66VCHSJNUP, quantity=<*>' — 5 lines in the baseline, last at 2024-01-20 06:46:11 UTC [re2ob_14-04#3]
8. Not established from the available artifacts.
