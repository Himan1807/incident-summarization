# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 16 of 75 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_02-01#0]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.224 at 2024-01-19 12:21:07 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 186) [re2ob_02-01#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1202 at 2024-01-19 12:21:07 UTC; sustained deviation from 2024-01-19 12:16:37 UTC (score 168) [re2ob_02-01#0]
- metric anomalies: shippingservice_latency-90 — baseline median 0.0046; peak 0.1577 at 2024-01-19 12:26:53 UTC; sustained deviation from 2024-01-19 12:15:53 UTC (score 163) [re2ob_02-01#0]
- metric anomalies: redis_cpu — baseline median 0.2978; peak 0.1609 at 2024-01-19 12:23:48 UTC; sustained deviation from 2024-01-19 12:13:44 UTC (score 3.01) [re2ob_02-01#3]
- metric anomalies: paymentservice_latency-90 — baseline median 0.005; peak 0.2229 at 2024-01-19 12:26:38 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 141) [re2ob_02-01#1]
- metric anomalies: paymentservice_latency-50 — baseline median 0.0032; peak 0.1143 at 2024-01-19 12:26:38 UTC; sustained deviation from 2024-01-19 12:16:25 UTC (score 136) [re2ob_02-01#1]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.2216; peak 4.69 at 2024-01-19 12:22:01 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 124) [re2ob_02-01#1]
- metric anomalies: redis_diskio — baseline median 0; peak 26965 at 2024-01-19 12:18:05 UTC; sustained deviation from 2024-01-19 12:17:39 UTC (score 106) [re2ob_02-01#1]
- operation latency: currencyservice_Convert — baseline mean 0.4146; later mean 21.89 (x16.18); peak 43.00 at 2024-01-19 12:22:45 UTC [re2ob_02-02#0]
- operation latency: shippingservice_GetQuote — baseline mean 0; later mean 6.32 (x7.32); peak 13.00 at 2024-01-19 12:22:45 UTC [re2ob_02-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 1.56; later mean 16.39 (x6.79); peak 34.00 at 2024-01-19 12:19:15 UTC [re2ob_02-02#0]
- operation latency: frontendservice_frontend — baseline mean 0.2195; later mean 6.34 (x6.02); peak 13.00 at 2024-01-19 12:22:45 UTC [re2ob_02-02#0]

## Timeline

- 2024-01-19 12:08 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['0PUK6V6EV0', 'L9ECAV7KIM']' — 5 lines in the baseline, last at 2024-01-19 12:08:22 UTC [re2ob_02-04#3]
- 2024-01-19 12:12 UTC — log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['1YMWWN1N4O', '0PUK6V6EV0', 'OLJCESPC7Z', '2ZYFJ3GM2N', 'L' — 5 lines in the baseline, last at 2024-01-19 12:12:20 UTC; log templates: stopped after the baseline: 'paymentservice Transaction processed: visa ending <*> Amount: CAD266.<*>' — 5 lines in the baseline, last at 2024-01-19 12:12:44 UTC; log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-ecf0-4a74-88a2-<*>, productId=OLJCESPC7Z, quantity=<*>' — 5 lines in the baseline, last at 2024-01-19 12:12:12 UTC [re2ob_02-04#3]
- 2024-01-19 12:13 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC; operation latency: paymentservice_Charge — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-c9ad-<*>-abfd-<*>, productId=LS4PSXUNUM, quantity=<*>' — 6 lines, first at 2024-01-19 12:13:27 UTC; log templates: new after the baseline: 'cartservice AddItemAsync called with userId=<*>-<*>-4f72-962f-<*>, productId=L9ECAV7KIM, quantity=<*>' — 6 lines, first at 2024-01-19 12:13:21 UTC; earliest sustained metric deviation: emailservice_cpu from 2024-01-19 12:13:24 UTC [re2ob_02-02#1, re2ob_02-02#2, re2ob_02-04#2, re2ob_02-06#0]
- 2024-01-19 12:16 UTC — log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['6E92ZMYYFZ', '9SIQT8TOJO', 'L9ECAV7KIM', 'LS4PSXUNUM', 'O' — 6 lines, first at 2024-01-19 12:16:29 UTC [re2ob_02-04#2]
- 2024-01-19 12:17 UTC — operation latency: traceservice_Export — baseline mean 0; later mean 0.5179 (x1.52); peak 2.00 at 2024-01-19 12:17:00 UTC; log templates: new after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['2ZYFJ3GM2N', '6E92ZMYYFZ', 'LS4PSXUNUM', '0PUK6V6EV0', 'O' — 6 lines, first at 2024-01-19 12:17:08 UTC [re2ob_02-02#1, re2ob_02-04#2]
- 2024-01-19 12:18 UTC — metric anomalies: redis_diskio — baseline median 0; peak 26965 at 2024-01-19 12:18:05 UTC; sustained deviation from 2024-01-19 12:17:39 UTC (score 106); metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0079 at 2024-01-19 12:18:35 UTC; sustained deviation from 2024-01-19 12:18:05 UTC (score 11.11); metric anomalies: currencyservice_cpu — baseline median 33.17; peak 18.52 at 2024-01-19 12:18:59 UTC; sustained deviation from 2024-01-19 12:18:45 UTC (score 3.61); operation latency: health_Check — baseline mean 0.2195; later mean 0.2857 (x1.05); peak 2.00 at 2024-01-19 12:18:00 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.0244; later mean 0.0357 (x1.01); peak 1.00 at 2024-01-19 12:18:00 UTC [re2ob_02-01#1, re2ob_02-01#2, re2ob_02-02#1]
- 2024-01-19 12:19 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 1.56; later mean 16.39 (x6.79); peak 34.00 at 2024-01-19 12:19:15 UTC [re2ob_02-02#0]
- 2024-01-19 12:21 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.224 at 2024-01-19 12:21:07 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 186); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1202 at 2024-01-19 12:21:07 UTC; sustained deviation from 2024-01-19 12:16:37 UTC (score 168) [re2ob_02-01#0]
- 2024-01-19 12:22 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.2216; peak 4.69 at 2024-01-19 12:22:01 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 124); metric anomalies: checkoutservice_latency-50 — baseline median 0.1037; peak 2.81 at 2024-01-19 12:22:01 UTC; sustained deviation from 2024-01-19 12:15:46 UTC (score 57.58); operation latency: currencyservice_Convert — baseline mean 0.4146; later mean 21.89 (x16.18); peak 43.00 at 2024-01-19 12:22:45 UTC; operation latency: shippingservice_GetQuote — baseline mean 0; later mean 6.32 (x7.32); peak 13.00 at 2024-01-19 12:22:45 UTC; operation latency: frontendservice_frontend — baseline mean 0.2195; later mean 6.34 (x6.02); peak 13.00 at 2024-01-19 12:22:45 UTC [re2ob_02-01#1, re2ob_02-01#2, re2ob_02-02#0]
- 2024-01-19 12:23 UTC — metric anomalies: redis_cpu — baseline median 0.2978; peak 0.1609 at 2024-01-19 12:23:48 UTC; sustained deviation from 2024-01-19 12:13:44 UTC (score 3.01) [re2ob_02-01#3]
- 2024-01-19 12:26 UTC — metric anomalies: shippingservice_latency-90 — baseline median 0.0046; peak 0.1577 at 2024-01-19 12:26:53 UTC; sustained deviation from 2024-01-19 12:15:53 UTC (score 163); metric anomalies: paymentservice_latency-90 — baseline median 0.005; peak 0.2229 at 2024-01-19 12:26:38 UTC; sustained deviation from 2024-01-19 12:15:23 UTC (score 141); metric anomalies: paymentservice_latency-50 — baseline median 0.0032; peak 0.1143 at 2024-01-19 12:26:38 UTC; sustained deviation from 2024-01-19 12:16:25 UTC (score 136); metric anomalies: shippingservice_latency-50 — baseline median 0.0029; peak 0.0034 at 2024-01-19 12:26:53 UTC; sustained deviation from 2024-01-19 12:20:46 UTC (score 4.79) [re2ob_02-01#0, re2ob_02-01#1, re2ob_02-01#2]

## Detection: IDS Alerts

- metric anomalies: checkoutservice_latency-50 — baseline median 0.1037; peak 2.81 at 2024-01-19 12:22:01 UTC; sustained deviation from 2024-01-19 12:15:46 UTC (score 57.58) [re2ob_02-01#2]
- metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0079 at 2024-01-19 12:18:35 UTC; sustained deviation from 2024-01-19 12:18:05 UTC (score 11.11) [re2ob_02-01#2]
- metric anomalies: shippingservice_latency-50 — baseline median 0.0029; peak 0.0034 at 2024-01-19 12:26:53 UTC; sustained deviation from 2024-01-19 12:20:46 UTC (score 4.79) [re2ob_02-01#2]
- metric anomalies: currencyservice_cpu — baseline median 33.17; peak 18.52 at 2024-01-19 12:18:59 UTC; sustained deviation from 2024-01-19 12:18:45 UTC (score 3.61) [re2ob_02-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC [re2ob_02-02#2]

## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_02-03#0]
2. operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC [re2ob_02-02#2]
3. operation latency: paymentservice_Charge — baseline mean 0; later mean 0 (x1.00); peak 0 at 2024-01-19 12:13:15 UTC [re2ob_02-02#2]
4. Not established from the available artifacts.
5. log templates: stopped after the baseline: 'recommendationservice [Recv ListRecommendations] product_ids=['0PUK6V6EV0', 'L9ECAV7KIM']' — 5 lines in the baseline, last at 2024-01-19 12:08:22 UTC [re2ob_02-04#3]
6. log templates: stopped after the baseline: 'paymentservice Transaction processed: visa ending <*>     Amount: CAD266.<*>' — 5 lines in the baseline, last at 2024-01-19 12:12:44 UTC [re2ob_02-04#3]
7. log templates: stopped after the baseline: 'cartservice AddItemAsync called with userId=<*>-ecf0-4a74-88a2-<*>, productId=OLJCESPC7Z, quantity=<*>' — 5 lines in the baseline, last at 2024-01-19 12:12:12 UTC [re2ob_02-04#3]
8. Not established from the available artifacts.
