# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 17 of 70 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_05-01#0]
- metric anomalies: checkoutservice_mem — baseline median 11390976; peak 268439552 at 2024-01-17 03:32:07 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 152) [re2ob_05-01#0]
- metric anomalies: checkoutservice_cpu — baseline median 0.3971; peak 20.65 at 2024-01-17 03:30:32 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 106) [re2ob_05-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 30283 at 2024-01-17 03:33:49 UTC; sustained deviation from 2024-01-17 03:28:15 UTC (score 98.72) [re2ob_05-01#0]
- Derived: earliest sustained metric deviation: redis_cpu from 2024-01-17 03:25:52 UTC. [re2ob_05-06#0]
- Derived: metric series ranked #1 by deviation score: checkoutservice_mem (score 152). [re2ob_05-06#0]
- Derived: trace operation with the largest latency increase: frontendservice_frontend (mean 0.4878 -> 4.64, x3.79). [re2ob_05-06#0]
- Derived: container with the largest change in log volume: checkoutservice (80.20 -> 92.57 lines/min). [re2ob_05-06#0]
- operation latency: frontendservice_frontend — baseline mean 0.4878; later mean 4.64 (x3.79); peak 11.00 at 2024-01-17 03:33:30 UTC [re2ob_05-02#0]
- operation latency: cartservice_GetCart — baseline mean 0.5366; later mean 2.48 (x2.27); peak 11.00 at 2024-01-17 03:37:15 UTC [re2ob_05-02#0]
- operation latency: currencyservice_Convert — baseline mean 1.71; later mean 3.98 (x1.84); peak 28.00 at 2024-01-17 03:36:30 UTC [re2ob_05-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 3.05; later mean 6.38 (x1.82); peak 24.00 at 2024-01-17 03:29:15 UTC [re2ob_05-02#0]
- metric anomalies: paymentservice_latency-50 — baseline median 0.0032; peak 0.0051 at 2024-01-17 03:35:43 UTC; sustained deviation from 2024-01-17 03:29:28 UTC (score 4.72) [re2ob_05-01#3]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-17 03:30:00 UTC [re2ob_05-02#2]
- operation latency: cartservice_EmptyCart — baseline mean 0.0244; later mean 0.1071 (x1.08); peak 1.00 at 2024-01-17 03:28:30 UTC [re2ob_05-02#2]

## Timeline

- 2024-01-17 03:25 UTC — earliest sustained metric deviation: redis_cpu from 2024-01-17 03:25:52 UTC [re2ob_05-06#0]
- 2024-01-17 03:28 UTC — operation latency: traceservice_Export — baseline mean 0; later mean 0.5893 (x1.59); peak 2.00 at 2024-01-17 03:28:15 UTC; operation latency: shippingservice_GetQuote — baseline mean 0; later mean 0.1071 (x1.11); peak 1.00 at 2024-01-17 03:28:45 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-17 03:28:30 UTC; operation latency: cartservice_EmptyCart — baseline mean 0.0244; later mean 0.1071 (x1.08); peak 1.00 at 2024-01-17 03:28:30 UTC [re2ob_05-02#1, re2ob_05-02#2]
- 2024-01-17 03:29 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 3.05; later mean 6.38 (x1.82); peak 24.00 at 2024-01-17 03:29:15 UTC; operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.125 (x1.12); peak 1.00 at 2024-01-17 03:29:15 UTC [re2ob_05-02#0, re2ob_05-02#1]
- 2024-01-17 03:30 UTC — metric anomalies: checkoutservice_cpu — baseline median 0.3971; peak 20.65 at 2024-01-17 03:30:32 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 106); metric anomalies: checkoutservice_socket — baseline median 9.00; peak 14.00 at 2024-01-17 03:30:36 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 18.75); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-17 03:30:00 UTC [re2ob_05-01#0, re2ob_05-01#1, re2ob_05-02#2]
- 2024-01-17 03:32 UTC — metric anomalies: checkoutservice_mem — baseline median 11390976; peak 268439552 at 2024-01-17 03:32:07 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 152); metric anomalies: checkoutservice_latency-90 — baseline median 0.236; peak 2.50 at 2024-01-17 03:32:38 UTC; sustained deviation from 2024-01-17 03:28:06 UTC (score 94.27); metric anomalies: checkoutservice_latency-50 — baseline median 0.1536; peak 1.47 at 2024-01-17 03:32:38 UTC; sustained deviation from 2024-01-17 03:28:36 UTC (score 52.09) [re2ob_05-01#0, re2ob_05-01#1]
- 2024-01-17 03:33 UTC — metric anomalies: redis_diskio — baseline median 0; peak 30283 at 2024-01-17 03:33:49 UTC; sustained deviation from 2024-01-17 03:28:15 UTC (score 98.72); operation latency: frontendservice_frontend — baseline mean 0.4878; later mean 4.64 (x3.79); peak 11.00 at 2024-01-17 03:33:30 UTC [re2ob_05-01#0, re2ob_05-02#0]
- 2024-01-17 03:35 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0074 at 2024-01-17 03:35:56 UTC; sustained deviation from 2024-01-17 03:32:23 UTC (score 10.84); metric anomalies: paymentservice_latency-90 — baseline median 0.0051; peak 0.0099 at 2024-01-17 03:35:58 UTC; sustained deviation from 2024-01-17 03:29:08 UTC (score 5.82); metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0035 at 2024-01-17 03:35:56 UTC; sustained deviation from 2024-01-17 03:32:23 UTC (score 5.28); metric anomalies: paymentservice_latency-50 — baseline median 0.0032; peak 0.0051 at 2024-01-17 03:35:43 UTC; sustained deviation from 2024-01-17 03:29:28 UTC (score 4.72) [re2ob_05-01#2, re2ob_05-01#3]
- 2024-01-17 03:36 UTC — metric anomalies: frontend_socket — baseline median 35.00; peak 26.00 at 2024-01-17 03:36:04 UTC; sustained deviation from 2024-01-17 03:33:51 UTC (score 17.14); operation latency: currencyservice_Convert — baseline mean 1.71; later mean 3.98 (x1.84); peak 28.00 at 2024-01-17 03:36:30 UTC [re2ob_05-01#1, re2ob_05-02#0]
- 2024-01-17 03:37 UTC — operation latency: cartservice_GetCart — baseline mean 0.5366; later mean 2.48 (x2.27); peak 11.00 at 2024-01-17 03:37:15 UTC [re2ob_05-02#0]
- 2024-01-17 03:38 UTC — metric anomalies: frontend_latency-90 — baseline median 0.2216; peak 0.3265 at 2024-01-17 03:38:51 UTC; sustained deviation from 2024-01-17 03:37:19 UTC (score 5.16) [re2ob_05-01#2]

## Detection: IDS Alerts

- metric anomalies: checkoutservice_latency-90 — baseline median 0.236; peak 2.50 at 2024-01-17 03:32:38 UTC; sustained deviation from 2024-01-17 03:28:06 UTC (score 94.27) [re2ob_05-01#1]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.1536; peak 1.47 at 2024-01-17 03:32:38 UTC; sustained deviation from 2024-01-17 03:28:36 UTC (score 52.09) [re2ob_05-01#1]
- metric anomalies: checkoutservice_socket — baseline median 9.00; peak 14.00 at 2024-01-17 03:30:36 UTC; sustained deviation from 2024-01-17 03:28:01 UTC (score 18.75) [re2ob_05-01#1]
- metric anomalies: frontend_socket — baseline median 35.00; peak 26.00 at 2024-01-17 03:36:04 UTC; sustained deviation from 2024-01-17 03:33:51 UTC (score 17.14) [re2ob_05-01#1]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0074 at 2024-01-17 03:35:56 UTC; sustained deviation from 2024-01-17 03:32:23 UTC (score 10.84) [re2ob_05-01#2]
- metric anomalies: paymentservice_latency-90 — baseline median 0.0051; peak 0.0099 at 2024-01-17 03:35:58 UTC; sustained deviation from 2024-01-17 03:29:08 UTC (score 5.82) [re2ob_05-01#2]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0035 at 2024-01-17 03:35:56 UTC; sustained deviation from 2024-01-17 03:32:23 UTC (score 5.28) [re2ob_05-01#2]
- metric anomalies: frontend_latency-90 — baseline median 0.2216; peak 0.3265 at 2024-01-17 03:38:51 UTC; sustained deviation from 2024-01-17 03:37:19 UTC (score 5.16) [re2ob_05-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment



## Root Cause and Evidence Gaps



## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_05-03#0]
2. operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-17 03:30:00 UTC [re2ob_05-02#2]
3. operation latency: cartservice_EmptyCart — baseline mean 0.0244; later mean 0.1071 (x1.08); peak 1.00 at 2024-01-17 03:28:30 UTC [re2ob_05-02#2]
4. Not established from the available artifacts.
5. log volume: adservice — 450 lines/min in the baseline, 440 lines/min later [re2ob_05-04#1]
6. log volume: currencyservice — 2368 lines/min in the baseline, 2337 lines/min later [re2ob_05-04#1]
7. log volume: recommendationservice — 564 lines/min in the baseline, 560 lines/min later [re2ob_05-04#1]
8. Not established from the available artifacts.
