# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: frontend_latency-90 — baseline median 0.2073; peak 1.83 at 2024-01-19 22:07:48 UTC; sustained deviation from 2024-01-19 22:07:03 UTC (score 63.57) [re2ob_08-01#1]
- metric anomalies: frontend_latency-50 — baseline median 0.0534; peak 0.4354 at 2024-01-19 22:09:31 UTC; sustained deviation from 2024-01-19 22:07:31 UTC (score 43.51) [re2ob_08-01#1]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1025; peak 0.7969 at 2024-01-19 22:09:23 UTC; sustained deviation from 2024-01-19 22:07:31 UTC (score 28.35) [re2ob_08-01#1]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0523; peak 0.2259 at 2024-01-19 22:09:16 UTC; sustained deviation from 2024-01-19 22:07:16 UTC (score 22.76) [re2ob_08-01#1]
- metric anomalies: 14 of 76 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_08-01#0]
- metric anomalies: currencyservice_latency-50 — baseline median 0.0041; peak 0.1057 at 2024-01-19 22:09:01 UTC; sustained deviation from 2024-01-19 22:07:46 UTC (score 128) [re2ob_08-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 26623 at 2024-01-19 22:09:53 UTC; sustained deviation from 2024-01-19 22:04:52 UTC (score 125) [re2ob_08-01#0]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2241; peak 2.04 at 2024-01-19 22:09:08 UTC; sustained deviation from 2024-01-19 22:05:53 UTC (score 96.49) [re2ob_08-01#0]
- metric anomalies: recommendationservice_cpu — baseline median 2.95; peak 1.52 at 2024-01-19 22:15:38 UTC; sustained deviation from 2024-01-19 22:14:07 UTC (score 3.89) [re2ob_08-01#3]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 16.66 (x17.66); peak 28.00 at 2024-01-19 22:09:00 UTC [re2ob_08-02#0]
- operation latency: currencyservice_Convert — baseline mean 0; later mean 0.8571 (x1.86); peak 6.00 at 2024-01-19 22:07:00 UTC [re2ob_08-02#0]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-19 22:06:45 UTC [re2ob_08-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.2857 (x1.29); peak 4.00 at 2024-01-19 22:15:45 UTC [re2ob_08-02#0]

## Timeline

- 2024-01-19 22:03 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['6E92ZMYYFZ', '66VCHSJNUP']' — 9 lines in the baseline, last at 2024-01-19 22:03:43 UTC [re2ob_08-04#3]
- 2024-01-19 22:04 UTC — log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['9SIQT8TOJO', '1YMWWN1N4O', 'L9ECAV7KIM', '66VCHSJNUP', '0' — 5 lines, first at 2024-01-19 22:04:55 UTC; log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-25c0-4cce-87bc-<*>, productId=1YMWWN1N4O, quantity=<*>' — 7 lines in the baseline, last at 2024-01-19 22:04:45 UTC; log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-<*>-4cad-8a1f-<*>, productId=LS4PSXUNUM, quantity=<*>' — 6 lines in the baseline, last at 2024-01-19 22:04:47 UTC; log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z']' — 5 lines in the baseline, last at 2024-01-19 22:04:50 UTC; earliest sustained metric deviation: redis_diskio from 2024-01-19 22:04:52 UTC [re2ob_08-04#2, re2ob_08-04#3, re2ob_08-06#0]
- 2024-01-19 22:05 UTC — operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 22:05:00 UTC; operation latency: paymentservice_Charge — baseline mean 0.0488; later mean 0.0357 (x0.9875); peak 1.00 at 2024-01-19 22:05:30 UTC; operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-19 22:05:00 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-2eaf-4d35-8e41-<*>, productId=OLJCESPC7Z, quantity=<*>' — 6 lines, first at 2024-01-19 22:05:26 UTC [re2ob_08-02#1, re2ob_08-04#2]
- 2024-01-19 22:06 UTC — metric anomalies: paymentservice_latency-90 — baseline median 0.0049; peak 0.0081 at 2024-01-19 22:06:55 UTC; sustained deviation from 2024-01-19 22:06:38 UTC (score 4.72); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 0.3393 (x1.34); peak 4.00 at 2024-01-19 22:06:45 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.1951; later mean 0.0536 (x0.8816); peak 1.00 at 2024-01-19 22:06:45 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-ecf0-4a74-88a2-<*>, productId=L9ECAV7KIM, quantity=<*>' — 6 lines, first at 2024-01-19 22:06:39 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-db75-4e74-884a-<*>, productId=0PUK6V6EV0, quantity=<*>' — 5 lines, first at 2024-01-19 22:06:27 UTC [re2ob_08-01#2, re2ob_08-02#0, re2ob_08-02#2, re2ob_08-04#2]
- 2024-01-19 22:07 UTC — metric anomalies: frontend_latency-90 — baseline median 0.2073; peak 1.83 at 2024-01-19 22:07:48 UTC; sustained deviation from 2024-01-19 22:07:03 UTC (score 63.57); operation latency: currencyservice_Convert — baseline mean 0; later mean 0.8571 (x1.86); peak 6.00 at 2024-01-19 22:07:00 UTC [re2ob_08-01#1, re2ob_08-02#0]
- 2024-01-19 22:08 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.70; peak 1.32 at 2024-01-19 22:08:45 UTC; sustained deviation from 2024-01-19 22:04:52 UTC (score 4.56) [re2ob_08-01#2]
- 2024-01-19 22:09 UTC — metric anomalies: currencyservice_latency-50 — baseline median 0.0041; peak 0.1057 at 2024-01-19 22:09:01 UTC; sustained deviation from 2024-01-19 22:07:46 UTC (score 128); metric anomalies: redis_diskio — baseline median 0; peak 26623 at 2024-01-19 22:09:53 UTC; sustained deviation from 2024-01-19 22:04:52 UTC (score 125); metric anomalies: checkoutservice_latency-90 — baseline median 0.2241; peak 2.04 at 2024-01-19 22:09:08 UTC; sustained deviation from 2024-01-19 22:05:53 UTC (score 96.49); metric anomalies: frontend_latency-50 — baseline median 0.0534; peak 0.4354 at 2024-01-19 22:09:31 UTC; sustained deviation from 2024-01-19 22:07:31 UTC (score 43.51); metric anomalies: checkoutservice_latency-50 — baseline median 0.1025; peak 0.7969 at 2024-01-19 22:09:23 UTC; sustained deviation from 2024-01-19 22:07:31 UTC (score 28.35); metric anomalies: currencyservice_latency-90 — baseline median 0.0523; peak 0.2259 at 2024-01-19 22:09:16 UTC; sustained deviation from 2024-01-19 22:07:16 UTC (score 22.76); operation latency: frontendservice_frontend — baseline mean 0; later mean 16.66 (x17.66); peak 28.00 at 2024-01-19 22:09:00 UTC; operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.0179 (x0.9936); peak 1.00 at 2024-01-19 22:09:15 UTC [re2ob_08-01#0, re2ob_08-01#1, re2ob_08-02#0, re2ob_08-02#1]
- 2024-01-19 22:11 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.1071 (x0.9264); peak 2.00 at 2024-01-19 22:11:30 UTC [re2ob_08-02#2]
- 2024-01-19 22:15 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.95; peak 1.52 at 2024-01-19 22:15:38 UTC; sustained deviation from 2024-01-19 22:14:07 UTC (score 3.89); operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.2857 (x1.29); peak 4.00 at 2024-01-19 22:15:45 UTC [re2ob_08-01#3, re2ob_08-02#0]
- 2024-01-19 22:17 UTC — metric anomalies: currencyservice_cpu — baseline median 33.43; peak 6.59 at 2024-01-19 22:17:48 UTC; sustained deviation from 2024-01-19 22:06:11 UTC (score 9.56) [re2ob_08-01#2]
- 2024-01-19 22:18 UTC — metric anomalies: redis_cpu — baseline median 0.2971; peak 0.1726 at 2024-01-19 22:18:03 UTC; sustained deviation from 2024-01-19 22:05:16 UTC (score 4.60) [re2ob_08-01#2]

## Detection: IDS Alerts

- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 22:05:00 UTC [re2ob_08-02#1]
- operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.0179 (x0.9936); peak 1.00 at 2024-01-19 22:09:15 UTC [re2ob_08-02#1]
- operation latency: paymentservice_Charge — baseline mean 0.0488; later mean 0.0357 (x0.9875); peak 1.00 at 2024-01-19 22:05:30 UTC [re2ob_08-02#1]
- operation latency: health_Check — baseline mean 0.0244; later mean 0 (x0.9762); peak 0 at 2024-01-19 22:05:00 UTC [re2ob_08-02#1]

## Initial Infection Indicators

- metric anomalies: currencyservice_cpu — baseline median 33.43; peak 6.59 at 2024-01-19 22:17:48 UTC; sustained deviation from 2024-01-19 22:06:11 UTC (score 9.56) [re2ob_08-01#2]
- metric anomalies: paymentservice_latency-90 — baseline median 0.0049; peak 0.0081 at 2024-01-19 22:06:55 UTC; sustained deviation from 2024-01-19 22:06:38 UTC (score 4.72) [re2ob_08-01#2]
- metric anomalies: redis_cpu — baseline median 0.2971; peak 0.1726 at 2024-01-19 22:18:03 UTC; sustained deviation from 2024-01-19 22:05:16 UTC (score 4.60) [re2ob_08-01#2]
- metric anomalies: productcatalogservice_cpu — baseline median 3.70; peak 1.32 at 2024-01-19 22:08:45 UTC; sustained deviation from 2024-01-19 22:04:52 UTC (score 4.56) [re2ob_08-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.1071 (x0.9264); peak 2.00 at 2024-01-19 22:11:30 UTC [re2ob_08-02#2]
- operation latency: cartservice_EmptyCart — baseline mean 0.1951; later mean 0.0536 (x0.8816); peak 1.00 at 2024-01-19 22:06:45 UTC [re2ob_08-02#2]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_08-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_08-03#0]
2. operation latency: shippingservice_ShipOrder — baseline mean 0.1951; later mean 0.1071 (x0.9264); peak 2.00 at 2024-01-19 22:11:30 UTC [re2ob_08-02#2]
3. operation latency: cartservice_EmptyCart — baseline mean 0.1951; later mean 0.0536 (x0.8816); peak 1.00 at 2024-01-19 22:06:45 UTC [re2ob_08-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-25c0-4cce-87bc-<*>, productId=1YMWWN1N4O, quantity=<*>' — 7 lines in the baseline, last at 2024-01-19 22:04:45 UTC [re2ob_08-04#3]
6. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-<*>-4cad-8a1f-<*>, productId=LS4PSXUNUM, quantity=<*>' — 6 lines in the baseline, last at 2024-01-19 22:04:47 UTC [re2ob_08-04#3]
7. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['OLJCESPC7Z']' — 5 lines in the baseline, last at 2024-01-19 22:04:50 UTC [re2ob_08-04#3]
8. Not established from the available artifacts.
