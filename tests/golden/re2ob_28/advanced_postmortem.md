# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 56 of 73 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_28-01#0]
- metric anomalies: productcatalogservice_error — no data in the baseline; series appears at 2024-01-15 19:36:02 UTC (first value 0); peak 0.6 at 2024-01-15 19:37:02 UTC [re2ob_28-01#0]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 27.82 at 2024-01-15 19:43:19 UTC; sustained deviation from 2024-01-15 19:34:19 UTC (score 166) [re2ob_28-01#0]
- metric anomalies: recommendationservice_socket — baseline median 4.00; peak 35.00 at 2024-01-15 19:42:34 UTC; sustained deviation from 2024-01-15 19:34:48 UTC (score 121) [re2ob_28-01#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 8.00 at 2024-01-15 19:44:15 UTC [re2ob_28-02#2]
- operation latency: cartservice_GetCart — baseline mean 1.88; later mean 2.55 (x1.23); peak 22.00 at 2024-01-15 19:45:15 UTC [re2ob_28-02#2]
- operation latency: productcatalogservice_GetProduct — baseline mean 0.4146; later mean 25.12 (x18.47); peak 310 at 2024-01-15 19:35:45 UTC [re2ob_28-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 7.18 (x8.18); peak 48.00 at 2024-01-15 19:36:30 UTC [re2ob_28-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 6.04 (x7.04); peak 46.00 at 2024-01-15 19:36:30 UTC [re2ob_28-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 4.25 (x5.25); peak 30.00 at 2024-01-15 19:34:15 UTC [re2ob_28-02#0]
- operation latency: adservice_GetAds — baseline mean 0.122; later mean 3.68 (x4.17); peak 26.00 at 2024-01-15 19:40:00 UTC [re2ob_28-02#1]
- operation latency: currencyservice_Convert — baseline mean 3.80; later mean 17.20 (x3.79); peak 231 at 2024-01-15 19:44:15 UTC [re2ob_28-02#1]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 2.15; later mean 6.41 (x2.36); peak 68.00 at 2024-01-15 19:44:15 UTC [re2ob_28-02#1]
- operation latency: shippingservice_GetQuote — baseline mean 0.0488; later mean 0.7143 (x1.63); peak 7.00 at 2024-01-15 19:35:00 UTC [re2ob_28-02#1]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0984; peak 0.7 at 2024-01-15 19:44:48 UTC; sustained deviation from 2024-01-15 19:39:19 UTC (score 46.56) [re2ob_28-01#3]

## Timeline

- 2024-01-15 19:32 UTC — earliest sustained metric deviation: frontend_cpu from 2024-01-15 19:32:16 UTC [re2ob_28-06#0]
- 2024-01-15 19:33 UTC — metric anomalies: redis_diskio — baseline median 0; peak 39248 at 2024-01-15 19:33:44 UTC; sustained deviation from 2024-01-15 19:33:30 UTC (score 109) [re2ob_28-01#1]
- 2024-01-15 19:34 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 4.25 (x5.25); peak 30.00 at 2024-01-15 19:34:15 UTC; operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 543; first error after baseline at 2024-01-15 19:34:00 UTC; log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 2033 lines, first at 2024-01-15 19:34:08 UTC [re2ob_28-02#0, re2ob_28-03#0, re2ob_28-04#2]
- 2024-01-15 19:35 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 0.4146; later mean 25.12 (x18.47); peak 310 at 2024-01-15 19:35:45 UTC; operation latency: shippingservice_GetQuote — baseline mean 0.0488; later mean 0.7143 (x1.63); peak 7.00 at 2024-01-15 19:35:00 UTC [re2ob_28-02#0, re2ob_28-02#1]
- 2024-01-15 19:36 UTC — metric anomalies: productcatalogservice_error — no data in the baseline; series appears at 2024-01-15 19:36:02 UTC (first value 0); peak 0.6 at 2024-01-15 19:37:02 UTC; metric anomalies: frontend_socket — baseline median 30.00; peak 59.00 at 2024-01-15 19:36:54 UTC; sustained deviation from 2024-01-15 19:34:11 UTC (score 48.74); operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 7.18 (x8.18); peak 48.00 at 2024-01-15 19:36:30 UTC; operation latency: frontendservice_frontend — baseline mean 0; later mean 6.04 (x7.04); peak 46.00 at 2024-01-15 19:36:30 UTC; metric series without baseline data that appears during the capture: productcatalogservice_error (from 2024-01-15 19:36:02 UTC) [re2ob_28-01#0, re2ob_28-01#2, re2ob_28-02#0, re2ob_28-06#0]
- 2024-01-15 19:38 UTC — metric anomalies: recommendationservice_mem — baseline median 45305856; peak 223887360 at 2024-01-15 19:38:35 UTC; sustained deviation from 2024-01-15 19:34:48 UTC (score 84.27) [re2ob_28-01#1]
- 2024-01-15 19:40 UTC — operation latency: adservice_GetAds — baseline mean 0.122; later mean 3.68 (x4.17); peak 26.00 at 2024-01-15 19:40:00 UTC; operation errors: currencyservice_GetSupportedCurrencies — baseline mean 0; later mean 156; first error after baseline at 2024-01-15 19:40:00 UTC; operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 26.93; first error after baseline at 2024-01-15 19:40:00 UTC; operation errors: currencyservice_Convert — baseline mean 0; later mean 8.25; first error after baseline at 2024-01-15 19:40:00 UTC; log templates: new after the baseline: 'frontend request error could not retrieve currencies: rpc error: code = Unavailable desc = no healthy upstream' — 626 lines, first at 2024-01-15 19:40:10 UTC [re2ob_28-02#1, re2ob_28-03#0, re2ob_28-03#1, re2ob_28-04#2]
- 2024-01-15 19:41 UTC — metric anomalies: currencyservice_socket — baseline median 3.00; peak 7.00 at 2024-01-15 19:41:31 UTC; sustained deviation from 2024-01-15 19:41:17 UTC (score 61.54); metric anomalies: shippingservice_socket — baseline median 3.00; peak 6.00 at 2024-01-15 19:41:35 UTC; sustained deviation from 2024-01-15 19:41:02 UTC (score 50.00) [re2ob_28-01#1, re2ob_28-01#2]
- 2024-01-15 19:42 UTC — metric anomalies: recommendationservice_socket — baseline median 4.00; peak 35.00 at 2024-01-15 19:42:34 UTC; sustained deviation from 2024-01-15 19:34:48 UTC (score 121); metric anomalies: frontend_latency-50 — baseline median 0.1842; peak 1.40 at 2024-01-15 19:42:05 UTC; sustained deviation from 2024-01-15 19:34:34 UTC (score 48.44) [re2ob_28-01#0, re2ob_28-01#2]
- 2024-01-15 19:43 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 27.82 at 2024-01-15 19:43:19 UTC; sustained deviation from 2024-01-15 19:34:19 UTC (score 166); metric anomalies: frontend_latency-90 — baseline median 0.6661; peak 23.94 at 2024-01-15 19:43:05 UTC; sustained deviation from 2024-01-15 19:34:20 UTC (score 60.33); operation errors: cartservice_GetCart — baseline mean 0; later mean 65.75; first error after baseline at 2024-01-15 19:43:15 UTC; operation errors: productcatalogservice_GetProduct — baseline mean 0; later mean 55.75; first error after baseline at 2024-01-15 19:43:15 UTC; operation errors: productcatalogservice_ListProducts — baseline mean 0; later mean 14.25; first error after baseline at 2024-01-15 19:43:15 UTC; operation errors: cartservice_AddItem — baseline mean 0; later mean 8.50; first error after baseline at 2024-01-15 19:43:45 UTC; log templates: new after the baseline: 'frontend request error could not retrieve <:*:> rpc error: code = Unavailable desc = no healthy upstream' — 515 lines, first at 2024-01-15 19:43:16 UTC; log templates: new after the baseline: 'frontend request error failed to add to cart: rpc error: code = Unavailable desc = no healthy upstream' — 34 lines, first at 2024-01-15 19:43:48 UTC [re2ob_28-01#0, re2ob_28-01#1, re2ob_28-03#0, re2ob_28-03#1, re2ob_28-04#2]
- 2024-01-15 19:44 UTC — metric anomalies: cartservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 19:44:22 UTC; sustained deviation from 2024-01-15 19:44:22 UTC (score 50.00); metric anomalies: currencyservice_latency-90 — baseline median 0.0984; peak 0.7 at 2024-01-15 19:44:48 UTC; sustained deviation from 2024-01-15 19:39:19 UTC (score 46.56); operation latency: currencyservice_Convert — baseline mean 3.80; later mean 17.20 (x3.79); peak 231 at 2024-01-15 19:44:15 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 2.15; later mean 6.41 (x2.36); peak 68.00 at 2024-01-15 19:44:15 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 8.00 at 2024-01-15 19:44:15 UTC [re2ob_28-01#2, re2ob_28-01#3, re2ob_28-02#1, re2ob_28-02#2]
- 2024-01-15 19:45 UTC — operation latency: cartservice_GetCart — baseline mean 1.88; later mean 2.55 (x1.23); peak 22.00 at 2024-01-15 19:45:15 UTC [re2ob_28-02#2]

## Detection: IDS Alerts

- metric anomalies: redis_diskio — baseline median 0; peak 39248 at 2024-01-15 19:33:44 UTC; sustained deviation from 2024-01-15 19:33:30 UTC (score 109) [re2ob_28-01#1]
- metric anomalies: recommendationservice_mem — baseline median 45305856; peak 223887360 at 2024-01-15 19:38:35 UTC; sustained deviation from 2024-01-15 19:34:48 UTC (score 84.27) [re2ob_28-01#1]
- metric anomalies: currencyservice_socket — baseline median 3.00; peak 7.00 at 2024-01-15 19:41:31 UTC; sustained deviation from 2024-01-15 19:41:17 UTC (score 61.54) [re2ob_28-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.6661; peak 23.94 at 2024-01-15 19:43:05 UTC; sustained deviation from 2024-01-15 19:34:20 UTC (score 60.33) [re2ob_28-01#1]

## Initial Infection Indicators

- metric anomalies: cartservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 19:44:22 UTC; sustained deviation from 2024-01-15 19:44:22 UTC (score 50.00) [re2ob_28-01#2]
- metric anomalies: shippingservice_socket — baseline median 3.00; peak 6.00 at 2024-01-15 19:41:35 UTC; sustained deviation from 2024-01-15 19:41:02 UTC (score 50.00) [re2ob_28-01#2]
- metric anomalies: frontend_socket — baseline median 30.00; peak 59.00 at 2024-01-15 19:36:54 UTC; sustained deviation from 2024-01-15 19:34:11 UTC (score 48.74) [re2ob_28-01#2]
- metric anomalies: frontend_latency-50 — baseline median 0.1842; peak 1.40 at 2024-01-15 19:42:05 UTC; sustained deviation from 2024-01-15 19:34:34 UTC (score 48.44) [re2ob_28-01#2]

## Command-and-Control and Network Activity



## Impact Assessment

- log volume: cartservice — 726 lines/min in the baseline, 532 lines/min later [re2ob_28-04#1]
- log volume: paymentservice — 49.40 lines/min in the baseline, 37.36 lines/min later [re2ob_28-04#1]
- log volume: emailservice — 24.70 lines/min in the baseline, 18.57 lines/min later [re2ob_28-04#1]
- log volume: productcatalogservice — 0 lines/min in the baseline, 0.2143 lines/min later [re2ob_28-04#1]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 2033 lines, first at 2024-01-15 19:34:08 UTC [re2ob_28-04#2]
- log templates: new after the baseline: 'frontend request error could not retrieve currencies: rpc error: code = Unavailable desc = no healthy upstream' — 626 lines, first at 2024-01-15 19:40:10 UTC [re2ob_28-04#2]
- log templates: new after the baseline: 'frontend request error could not retrieve <:*:> rpc error: code = Unavailable desc = no healthy upstream' — 515 lines, first at 2024-01-15 19:43:16 UTC [re2ob_28-04#2]
- log templates: new after the baseline: 'frontend request error failed to add to cart: rpc error: code = Unavailable desc = no healthy upstream' — 34 lines, first at 2024-01-15 19:43:48 UTC [re2ob_28-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.3929 (x1.39); peak 8.00 at 2024-01-15 19:44:15 UTC [re2ob_28-02#2]
2. operation latency: cartservice_GetCart — baseline mean 1.88; later mean 2.55 (x1.23); peak 22.00 at 2024-01-15 19:45:15 UTC [re2ob_28-02#2]
3. pods: shippingservice-5987fc9db-mxb7x on node gke-gke-cluster-default-pool-2e1807ce-0e4z (only in the second inventory snapshot) [re2ob_28-05#4]
4. Not established from the available artifacts.
5. pods: currencyservice-6f7df68d87-52cpc on node gke-gke-cluster-default-pool-2e1807ce-0e4z (only in the second inventory snapshot) [re2ob_28-05#3]
6. pods: paymentservice-56744787b7-ljsn7 on node gke-gke-cluster-default-pool-2e1807ce-0e4z (only in the second inventory snapshot) [re2ob_28-05#3]
7. pods: productcatalogservice-674b96c48f-fzttv on node gke-gke-cluster-default-pool-2e1807ce-cx8g (only in the second inventory snapshot) [re2ob_28-05#3]
8. Not established from the available artifacts.
