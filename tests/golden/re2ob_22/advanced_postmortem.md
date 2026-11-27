# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 49 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_22-01#0]
- metric anomalies: productcatalogservice_error — no data in the baseline; series appears at 2024-01-15 18:22:06 UTC (first value 0); peak 0.667 at 2024-01-15 18:23:51 UTC [re2ob_22-01#0]
- metric anomalies: recommendationservice_socket — baseline median 4.00; peak 35.00 at 2024-01-15 18:25:40 UTC; sustained deviation from 2024-01-15 18:21:24 UTC (score 135) [re2ob_22-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 25515 at 2024-01-15 18:22:59 UTC; sustained deviation from 2024-01-15 18:18:30 UTC (score 129) [re2ob_22-01#0]
- operation latency: adservice_GetAds — baseline mean 0.325; later mean 1.54 (x1.91); peak 25.00 at 2024-01-15 18:29:00 UTC [re2ob_22-02#1]
- operation latency: currencyservice_Convert — baseline mean 2.95; later mean 5.56 (x1.66); peak 44.00 at 2024-01-15 18:28:15 UTC [re2ob_22-02#1]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4151 (x1.42); peak 6.00 at 2024-01-15 18:27:15 UTC [re2ob_22-02#1]
- operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.3962 (x1.40); peak 6.00 at 2024-01-15 18:29:30 UTC [re2ob_22-02#1]
- operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4906; first error after baseline at 2024-01-15 18:27:45 UTC [re2ob_22-03#1]
- operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 45.78; first error after baseline at 2024-01-15 18:21:15 UTC [re2ob_22-03#0]
- operation errors: productcatalogservice_GetProduct — baseline mean 0; later mean 4.15; first error after baseline at 2024-01-15 18:27:45 UTC [re2ob_22-03#0]
- operation errors: productcatalogservice_ListProducts — baseline mean 0; later mean 1.30; first error after baseline at 2024-01-15 18:27:45 UTC [re2ob_22-03#0]
- operation errors: traceservice_Export — baseline mean 0; later mean 1.15; first error after baseline at 2024-01-15 18:20:30 UTC [re2ob_22-03#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 17.94 (x18.94); peak 71.00 at 2024-01-15 18:28:00 UTC [re2ob_22-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 7.28 (x8.28); peak 49.00 at 2024-01-15 18:30:45 UTC [re2ob_22-02#0]
- operation latency: frontendservice_frontend — baseline mean 0; later mean 7.24 (x8.24); peak 50.00 at 2024-01-15 18:25:00 UTC [re2ob_22-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 5.39 (x6.39); peak 22.00 at 2024-01-15 18:23:45 UTC [re2ob_22-02#0]

## Timeline

- 2024-01-15 18:18 UTC — earliest sustained metric deviation: redis_diskio from 2024-01-15 18:18:30 UTC [re2ob_22-06#0]
- 2024-01-15 18:20 UTC — metric anomalies: frontend_socket — baseline median 31.00; peak 59.00 at 2024-01-15 18:20:53 UTC; sustained deviation from 2024-01-15 18:20:40 UTC (score 46.28); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 2.95; later mean 3.69 (x1.19); peak 25.00 at 2024-01-15 18:20:45 UTC; operation errors: traceservice_Export — baseline mean 0; later mean 1.15; first error after baseline at 2024-01-15 18:20:30 UTC; log templates: new after the baseline: 'productcatalogservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc erro' — 31 lines, first at 2024-01-15 18:20:47 UTC [re2ob_22-01#3, re2ob_22-02#2, re2ob_22-03#0, re2ob_22-04#2]
- 2024-01-15 18:21 UTC — operation errors: recommendationservice_ListRecommendations — baseline mean 0; later mean 45.78; first error after baseline at 2024-01-15 18:21:15 UTC; log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 167 lines, first at 2024-01-15 18:21:31 UTC [re2ob_22-03#0, re2ob_22-04#2]
- 2024-01-15 18:22 UTC — metric anomalies: productcatalogservice_error — no data in the baseline; series appears at 2024-01-15 18:22:06 UTC (first value 0); peak 0.667 at 2024-01-15 18:23:51 UTC; metric anomalies: redis_diskio — baseline median 0; peak 25515 at 2024-01-15 18:22:59 UTC; sustained deviation from 2024-01-15 18:18:30 UTC (score 129); metric series without baseline data that appears during the capture: productcatalogservice_error (from 2024-01-15 18:22:06 UTC) [re2ob_22-01#0, re2ob_22-06#0]
- 2024-01-15 18:23 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0072; peak 5.11 at 2024-01-15 18:23:51 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 88.28); operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 5.39 (x6.39); peak 22.00 at 2024-01-15 18:23:45 UTC [re2ob_22-01#1, re2ob_22-02#0]
- 2024-01-15 18:25 UTC — metric anomalies: recommendationservice_socket — baseline median 4.00; peak 35.00 at 2024-01-15 18:25:40 UTC; sustained deviation from 2024-01-15 18:21:24 UTC (score 135); metric anomalies: frontend_latency-90 — baseline median 0.6052; peak 50.86 at 2024-01-15 18:25:47 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 82.11); operation latency: frontendservice_frontend — baseline mean 0; later mean 7.24 (x8.24); peak 50.00 at 2024-01-15 18:25:00 UTC [re2ob_22-01#0, re2ob_22-01#1, re2ob_22-02#0]
- 2024-01-15 18:26 UTC — metric anomalies: recommendationservice_mem — baseline median 46944256; peak 179073024 at 2024-01-15 18:26:09 UTC; sustained deviation from 2024-01-15 18:21:57 UTC (score 95.33) [re2ob_22-01#1]
- 2024-01-15 18:27 UTC — metric anomalies: frontend_latency-50 — baseline median 0.1786; peak 16.42 at 2024-01-15 18:27:02 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 78.44); metric anomalies: productcatalogservice_latency-90 — baseline median 0.0043; peak 18.06 at 2024-01-15 18:27:06 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 70.58); operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4151 (x1.42); peak 6.00 at 2024-01-15 18:27:15 UTC; operation errors: productcatalogservice_GetProduct — baseline mean 0; later mean 4.15; first error after baseline at 2024-01-15 18:27:45 UTC; operation errors: productcatalogservice_ListProducts — baseline mean 0; later mean 1.30; first error after baseline at 2024-01-15 18:27:45 UTC; operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4906; first error after baseline at 2024-01-15 18:27:45 UTC; log templates: new after the baseline: 'frontend request error could not retrieve product: rpc error: code = Unavailable desc = no healthy upstream' — 9 lines, first at 2024-01-15 18:27:46 UTC; log templates: new after the baseline: 'recommendationservice File "/usr/local/lib/python3.<:NUM:>/site-packages/opentelemetry/instrumentation/grpc/ server.py",' — 8 lines, first at 2024-01-15 18:27:46 UTC [re2ob_22-01#2, re2ob_22-02#1, re2ob_22-03#0, re2ob_22-03#1, re2ob_22-04#2]
- 2024-01-15 18:28 UTC — metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 22.96 at 2024-01-15 18:28:06 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 116); metric anomalies: productcatalogservice_latency-50 — baseline median 0.0016; peak 0.9066 at 2024-01-15 18:28:02 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 73.00); metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 18:28:02 UTC; sustained deviation from 2024-01-15 18:28:02 UTC (score 50.00); operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 17.94 (x18.94); peak 71.00 at 2024-01-15 18:28:00 UTC; operation latency: currencyservice_Convert — baseline mean 2.95; later mean 5.56 (x1.66); peak 44.00 at 2024-01-15 18:28:15 UTC; operation latency: traceservice_Export — baseline mean 0; later mean 0.3704 (x1.37); peak 2.00 at 2024-01-15 18:28:15 UTC [re2ob_22-01#1, re2ob_22-01#2, re2ob_22-02#0, re2ob_22-02#1, re2ob_22-02#2]
- 2024-01-15 18:29 UTC — operation latency: adservice_GetAds — baseline mean 0.325; later mean 1.54 (x1.91); peak 25.00 at 2024-01-15 18:29:00 UTC; operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.3962 (x1.40); peak 6.00 at 2024-01-15 18:29:30 UTC [re2ob_22-02#1]
- 2024-01-15 18:30 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 7.28 (x8.28); peak 49.00 at 2024-01-15 18:30:45 UTC [re2ob_22-02#0]

## Detection: IDS Alerts

- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 22.96 at 2024-01-15 18:28:06 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 116) [re2ob_22-01#1]
- metric anomalies: recommendationservice_mem — baseline median 46944256; peak 179073024 at 2024-01-15 18:26:09 UTC; sustained deviation from 2024-01-15 18:21:57 UTC (score 95.33) [re2ob_22-01#1]
- metric anomalies: recommendationservice_latency-50 — baseline median 0.0072; peak 5.11 at 2024-01-15 18:23:51 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 88.28) [re2ob_22-01#1]
- metric anomalies: frontend_latency-90 — baseline median 0.6052; peak 50.86 at 2024-01-15 18:25:47 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 82.11) [re2ob_22-01#1]

## Initial Infection Indicators

- metric anomalies: frontend_latency-50 — baseline median 0.1786; peak 16.42 at 2024-01-15 18:27:02 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 78.44) [re2ob_22-01#2]
- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0016; peak 0.9066 at 2024-01-15 18:28:02 UTC; sustained deviation from 2024-01-15 18:21:17 UTC (score 73.00) [re2ob_22-01#2]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0043; peak 18.06 at 2024-01-15 18:27:06 UTC; sustained deviation from 2024-01-15 18:21:02 UTC (score 70.58) [re2ob_22-01#2]
- metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 8.00 at 2024-01-15 18:28:02 UTC; sustained deviation from 2024-01-15 18:28:02 UTC (score 50.00) [re2ob_22-01#2]
- metric anomalies: frontend_socket — baseline median 31.00; peak 59.00 at 2024-01-15 18:20:53 UTC; sustained deviation from 2024-01-15 18:20:40 UTC (score 46.28) [re2ob_22-01#3]

## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: traceservice_Export — baseline mean 0; later mean 0.3704 (x1.37); peak 2.00 at 2024-01-15 18:28:15 UTC [re2ob_22-02#2]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 2.95; later mean 3.69 (x1.19); peak 25.00 at 2024-01-15 18:20:45 UTC [re2ob_22-02#2]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'frontend failed to get product recommendations rpc error: code = Unavailable desc = no healthy upstream' — 167 lines, first at 2024-01-15 18:21:31 UTC [re2ob_22-04#2]
- log templates: new after the baseline: 'productcatalogservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc erro' — 31 lines, first at 2024-01-15 18:20:47 UTC [re2ob_22-04#2]
- log templates: new after the baseline: 'frontend request error could not retrieve product: rpc error: code = Unavailable desc = no healthy upstream' — 9 lines, first at 2024-01-15 18:27:46 UTC [re2ob_22-04#2]
- log templates: new after the baseline: 'recommendationservice File "/usr/local/lib/python3.<:NUM:>/site-packages/opentelemetry/instrumentation/grpc/ server.py",' — 8 lines, first at 2024-01-15 18:27:46 UTC [re2ob_22-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.4906; first error after baseline at 2024-01-15 18:27:45 UTC [re2ob_22-03#1]
2. pods: adservice-8587fdc599-swwgx on node gke-gke-cluster-default-pool-2e1807ce-xte3 (only in the second inventory snapshot) [re2ob_22-05#3]
3. pods: frontend-59688fbf4b-cgrv9 on node gke-gke-cluster-default-pool-2e1807ce-xte3 (only in the second inventory snapshot) [re2ob_22-05#3]
4. Not established from the available artifacts.
5. operation latency: traceservice_Export — baseline mean 0; later mean 0.3704 (x1.37); peak 2.00 at 2024-01-15 18:28:15 UTC [re2ob_22-02#2]
6. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 2.95; later mean 3.69 (x1.19); peak 25.00 at 2024-01-15 18:20:45 UTC [re2ob_22-02#2]
7. pods: adservice-8587fdc599-54pq7 on node gke-gke-cluster-default-pool-2e1807ce-2969 [re2ob_22-05#0]
8. Not established from the available artifacts.
