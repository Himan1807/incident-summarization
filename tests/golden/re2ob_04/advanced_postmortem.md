# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 20 of 74 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_04-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 40935 at 2024-01-16 03:40:36 UTC; sustained deviation from 2024-01-16 03:35:46 UTC (score 122) [re2ob_04-01#0]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.6625; peak 51.00 at 2024-01-16 03:49:22 UTC; sustained deviation from 2024-01-16 03:38:07 UTC (score 62.05) [re2ob_04-01#0]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.239; peak 22.00 at 2024-01-16 03:49:22 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 56.04) [re2ob_04-01#0]
- operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:45:00 UTC [re2ob_04-02#2]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.2182 (x1.22); peak 1.00 at 2024-01-16 03:37:45 UTC [re2ob_04-02#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.62; peak 1.37 at 2024-01-16 03:40:43 UTC; sustained deviation from 2024-01-16 03:39:58 UTC (score 3.72) [re2ob_04-01#3]
- metric anomalies: paymentservice_latency-90 — baseline median 0.0076; peak 0.3375 at 2024-01-16 03:49:08 UTC; sustained deviation from 2024-01-16 03:39:38 UTC (score 12.53) [re2ob_04-01#2]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0039 at 2024-01-16 03:46:49 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 11.56) [re2ob_04-01#2]
- metric anomalies: paymentservice_latency-50 — baseline median 0.0035; peak 0.0092 at 2024-01-16 03:49:23 UTC; sustained deviation from 2024-01-16 03:39:38 UTC (score 8.00) [re2ob_04-01#2]
- metric anomalies: currencyservice_cpu — baseline median 18.82; peak 8.98 at 2024-01-16 03:42:42 UTC; sustained deviation from 2024-01-16 03:37:32 UTC (score 4.24) [re2ob_04-01#2]

## Timeline

- 2024-01-16 03:35 UTC — earliest sustained metric deviation: redis_diskio from 2024-01-16 03:35:46 UTC [re2ob_04-06#0]
- 2024-01-16 03:37 UTC — operation latency: traceservice_Export — baseline mean 0; later mean 0.2182 (x1.22); peak 1.00 at 2024-01-16 03:37:45 UTC [re2ob_04-02#2]
- 2024-01-16 03:38 UTC — metric anomalies: frontend-external_error — baseline median 0; peak 0.6 at 2024-01-16 03:38:37 UTC; sustained deviation from 2024-01-16 03:38:22 UTC (score 22.33); operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 7.25; first error after baseline at 2024-01-16 03:38:00 UTC; operation errors: traceservice_Export — baseline mean 0; later mean 1.56; first error after baseline at 2024-01-16 03:38:15 UTC; log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Unavailable desc = no healthy upstream' — 27 lines, first at 2024-01-16 03:38:10 UTC; log templates: new after the baseline: 'checkoutservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc error: cod' — 2 lines, first at 2024-01-16 03:38:29 UTC [re2ob_04-01#1, re2ob_04-03#0, re2ob_04-04#2]
- 2024-01-16 03:39 UTC — operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.6607 (x1.66); peak 6.00 at 2024-01-16 03:39:15 UTC [re2ob_04-02#1]
- 2024-01-16 03:40 UTC — metric anomalies: redis_diskio — baseline median 0; peak 40935 at 2024-01-16 03:40:36 UTC; sustained deviation from 2024-01-16 03:35:46 UTC (score 122); metric anomalies: recommendationservice_cpu — baseline median 2.62; peak 1.37 at 2024-01-16 03:40:43 UTC; sustained deviation from 2024-01-16 03:39:58 UTC (score 3.72); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.3455 (x1.35); peak 3.00 at 2024-01-16 03:40:15 UTC [re2ob_04-01#0, re2ob_04-01#3, re2ob_04-02#1]
- 2024-01-16 03:42 UTC — metric anomalies: currencyservice_cpu — baseline median 18.82; peak 8.98 at 2024-01-16 03:42:42 UTC; sustained deviation from 2024-01-16 03:37:32 UTC (score 4.24) [re2ob_04-01#2]
- 2024-01-16 03:44 UTC — log templates: new after the baseline: 'checkoutservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc error: cod' — 4 lines, first at 2024-01-16 03:44:31 UTC [re2ob_04-04#2]
- 2024-01-16 03:45 UTC — metric anomalies: checkoutservice_socket — baseline median 9.00; peak 18.00 at 2024-01-16 03:45:46 UTC; sustained deviation from 2024-01-16 03:45:46 UTC (score 50.00); metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0088 at 2024-01-16 03:45:34 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 37.71); operation latency: frontendservice_frontend — baseline mean 0; later mean 2.23 (x3.23); peak 9.00 at 2024-01-16 03:45:30 UTC; operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:45:00 UTC; log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Unavailable desc = upstream connect error or disc' — 2 lines, first at 2024-01-16 03:45:30 UTC [re2ob_04-01#1, re2ob_04-02#0, re2ob_04-02#2, re2ob_04-04#2]
- 2024-01-16 03:46 UTC — metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0039 at 2024-01-16 03:46:49 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 11.56); operation latency: currencyservice_Convert — baseline mean 0.0244; later mean 2.23 (x3.16); peak 10.00 at 2024-01-16 03:46:15 UTC; operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 1.64 (x2.64); peak 11.00 at 2024-01-16 03:46:15 UTC; operation latency: cartservice_GetCart — baseline mean 0; later mean 0.4286 (x1.43); peak 5.00 at 2024-01-16 03:46:00 UTC [re2ob_04-01#2, re2ob_04-02#0, re2ob_04-02#1]
- 2024-01-16 03:48 UTC — operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.75 (x1.75); peak 13.00 at 2024-01-16 03:48:45 UTC [re2ob_04-02#0]
- 2024-01-16 03:49 UTC — metric anomalies: checkoutservice_latency-90 — baseline median 0.6625; peak 51.00 at 2024-01-16 03:49:22 UTC; sustained deviation from 2024-01-16 03:38:07 UTC (score 62.05); metric anomalies: checkoutservice_latency-50 — baseline median 0.239; peak 22.00 at 2024-01-16 03:49:22 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 56.04); metric anomalies: checkoutservice_mem — baseline median 11350016; peak 22167552 at 2024-01-16 03:49:42 UTC; sustained deviation from 2024-01-16 03:45:31 UTC (score 23.37); metric anomalies: paymentservice_latency-90 — baseline median 0.0076; peak 0.3375 at 2024-01-16 03:49:08 UTC; sustained deviation from 2024-01-16 03:39:38 UTC (score 12.53); metric anomalies: paymentservice_latency-50 — baseline median 0.0035; peak 0.0092 at 2024-01-16 03:49:23 UTC; sustained deviation from 2024-01-16 03:39:38 UTC (score 8.00); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:49:15 UTC [re2ob_04-01#0, re2ob_04-01#1, re2ob_04-01#2, re2ob_04-02#1]

## Detection: IDS Alerts

- metric anomalies: checkoutservice_socket — baseline median 9.00; peak 18.00 at 2024-01-16 03:45:46 UTC; sustained deviation from 2024-01-16 03:45:46 UTC (score 50.00) [re2ob_04-01#1]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0088 at 2024-01-16 03:45:34 UTC; sustained deviation from 2024-01-16 03:38:27 UTC (score 37.71) [re2ob_04-01#1]
- metric anomalies: checkoutservice_mem — baseline median 11350016; peak 22167552 at 2024-01-16 03:49:42 UTC; sustained deviation from 2024-01-16 03:45:31 UTC (score 23.37) [re2ob_04-01#1]
- metric anomalies: frontend-external_error — baseline median 0; peak 0.6 at 2024-01-16 03:38:37 UTC; sustained deviation from 2024-01-16 03:38:22 UTC (score 22.33) [re2ob_04-01#1]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: frontendservice_frontend — baseline mean 0; later mean 2.23 (x3.23); peak 9.00 at 2024-01-16 03:45:30 UTC [re2ob_04-02#0]
- operation latency: currencyservice_Convert — baseline mean 0.0244; later mean 2.23 (x3.16); peak 10.00 at 2024-01-16 03:46:15 UTC [re2ob_04-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 1.64 (x2.64); peak 11.00 at 2024-01-16 03:46:15 UTC [re2ob_04-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.75 (x1.75); peak 13.00 at 2024-01-16 03:48:45 UTC [re2ob_04-02#0]
- operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.6607 (x1.66); peak 6.00 at 2024-01-16 03:39:15 UTC [re2ob_04-02#1]
- operation latency: cartservice_GetCart — baseline mean 0; later mean 0.4286 (x1.43); peak 5.00 at 2024-01-16 03:46:00 UTC [re2ob_04-02#1]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:49:15 UTC [re2ob_04-02#1]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.3455 (x1.35); peak 3.00 at 2024-01-16 03:40:15 UTC [re2ob_04-02#1]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Unavailable desc = no healthy upstream' — 27 lines, first at 2024-01-16 03:38:10 UTC [re2ob_04-04#2]
- log templates: new after the baseline: 'checkoutservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc error: cod' — 4 lines, first at 2024-01-16 03:44:31 UTC [re2ob_04-04#2]
- log templates: new after the baseline: 'frontend request error failed to complete the order: rpc error: code = Unavailable desc = upstream connect error or disc' — 2 lines, first at 2024-01-16 03:45:30 UTC [re2ob_04-04#2]
- log templates: new after the baseline: 'checkoutservice <:NUM:>/<:NUM:>/<:NUM:> <:NUM:>:<:NUM:>:<:NUM:> traces export: context deadline exceeded: rpc error: cod' — 2 lines, first at 2024-01-16 03:38:29 UTC [re2ob_04-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:45:00 UTC [re2ob_04-02#2]
2. operation latency: traceservice_Export — baseline mean 0; later mean 0.2182 (x1.22); peak 1.00 at 2024-01-16 03:37:45 UTC [re2ob_04-02#2]
3. operation errors: checkoutservice_PlaceOrder — baseline mean 0; later mean 7.25; first error after baseline at 2024-01-16 03:38:00 UTC [re2ob_04-03#0]
4. Not established from the available artifacts.
5. operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.6607 (x1.66); peak 6.00 at 2024-01-16 03:39:15 UTC [re2ob_04-02#1]
6. operation latency: cartservice_GetCart — baseline mean 0; later mean 0.4286 (x1.43); peak 5.00 at 2024-01-16 03:46:00 UTC [re2ob_04-02#1]
7. operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3455 (x1.35); peak 6.00 at 2024-01-16 03:49:15 UTC [re2ob_04-02#1]
8. Not established from the available artifacts.
