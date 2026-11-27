# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: recommendationservice_socket — baseline median 5.00; peak 4.00 at 2024-01-15 20:46:04 UTC; sustained deviation from 2024-01-15 20:46:04 UTC (score 13.33) [re2ob_16-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.2468; peak 0.7308 at 2024-01-15 20:55:37 UTC; sustained deviation from 2024-01-15 20:48:27 UTC (score 7.86) [re2ob_16-01#2]
- metric anomalies: checkoutservice_latency-90 — baseline median 0.6542; peak 6.88 at 2024-01-15 20:53:57 UTC; sustained deviation from 2024-01-15 20:48:07 UTC (score 7.08) [re2ob_16-01#2]
- metric anomalies: currencyservice_latency-90 — baseline median 0.0971; peak 0.1878 at 2024-01-15 20:47:37 UTC; sustained deviation from 2024-01-15 20:47:07 UTC (score 5.02) [re2ob_16-01#2]
- metric anomalies: 17 of 72 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_16-01#0]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1857 at 2024-01-15 20:50:27 UTC; sustained deviation from 2024-01-15 20:49:04 UTC (score 132) [re2ob_16-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 38032 at 2024-01-15 20:54:02 UTC; sustained deviation from 2024-01-15 20:48:48 UTC (score 122) [re2ob_16-01#0]
- metric anomalies: emailservice_socket — baseline median 3.00; peak 10.00 at 2024-01-15 20:50:26 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 87.50) [re2ob_16-01#0]
- metric anomalies: currencyservice_cpu — baseline median 18.51; peak 11.83 at 2024-01-15 20:56:38 UTC; sustained deviation from 2024-01-15 20:47:22 UTC (score 3.52) [re2ob_16-01#3]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.05; later mean 5.30 (x1.04); peak 18.00 at 2024-01-15 20:47:15 UTC [re2ob_16-02#2]
- operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.1429 (x1.02); peak 1.00 at 2024-01-15 20:45:30 UTC [re2ob_16-02#2]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.1429 (x1.14); peak 4.00 at 2024-01-15 20:47:45 UTC [re2ob_16-02#1]
- operation latency: shippingservice_GetQuote — baseline mean 0.1463; later mean 0.3036 (x1.14); peak 5.00 at 2024-01-15 20:58:15 UTC [re2ob_16-02#1]
- operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.1429 (x1.12); peak 2.00 at 2024-01-15 20:58:00 UTC [re2ob_16-02#1]
- operation latency: frontendservice_frontend — baseline mean 3.02; later mean 3.20 (x1.04); peak 15.00 at 2024-01-15 20:47:15 UTC [re2ob_16-02#1]

## Timeline

- 2024-01-15 20:45 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.1429 (x1.02); peak 1.00 at 2024-01-15 20:45:30 UTC; earliest sustained metric deviation: frontend_socket from 2024-01-15 20:45:12 UTC [re2ob_16-02#2, re2ob_16-06#0]
- 2024-01-15 20:46 UTC — metric anomalies: recommendationservice_socket — baseline median 5.00; peak 4.00 at 2024-01-15 20:46:04 UTC; sustained deviation from 2024-01-15 20:46:04 UTC (score 13.33) [re2ob_16-01#2]
- 2024-01-15 20:47 UTC — metric anomalies: currencyservice_latency-90 — baseline median 0.0971; peak 0.1878 at 2024-01-15 20:47:37 UTC; sustained deviation from 2024-01-15 20:47:07 UTC (score 5.02); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.2143 (x1.21); peak 3.00 at 2024-01-15 20:47:45 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0; later mean 0.1429 (x1.14); peak 4.00 at 2024-01-15 20:47:45 UTC; operation latency: frontendservice_frontend — baseline mean 3.02; later mean 3.20 (x1.04); peak 15.00 at 2024-01-15 20:47:15 UTC; operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.05; later mean 5.30 (x1.04); peak 18.00 at 2024-01-15 20:47:15 UTC; operation errors: emailservice_SendOrderConfirmation — baseline mean 0; later mean 8.25; first error after baseline at 2024-01-15 20:47:45 UTC; log templates: new after the baseline: 'checkoutservice failed to send order confirmation to "someone@example.com": rpc error: code = Unavailable desc = no heal' — 33 lines, first at 2024-01-15 20:47:52 UTC [re2ob_16-01#2, re2ob_16-02#0, re2ob_16-02#1, re2ob_16-02#2, re2ob_16-03#0, re2ob_16-04#2]
- 2024-01-15 20:48 UTC — log templates: new after the baseline: 'emailservice starting the email service in dummy mode.' — 5 lines, first at 2024-01-15 20:48:09 UTC; log templates: new after the baseline: 'emailservice listening on port: <:NUM:>' — 5 lines, first at 2024-01-15 20:48:09 UTC [re2ob_16-04#2]
- 2024-01-15 20:49 UTC — operation latency: productcatalogservice_ListProducts — baseline mean 0.3902; later mean 0.75 (x1.26); peak 6.00 at 2024-01-15 20:49:30 UTC [re2ob_16-02#0]
- 2024-01-15 20:50 UTC — metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.1857 at 2024-01-15 20:50:27 UTC; sustained deviation from 2024-01-15 20:49:04 UTC (score 132); metric anomalies: emailservice_socket — baseline median 3.00; peak 10.00 at 2024-01-15 20:50:26 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 87.50); log templates: new after the baseline: 'emailservice Transient error StatusCode.DEADLINE EXCEEDED encountered while exporting traces to jaeger-collector.telemet' — 6 lines, first at 2024-01-15 20:50:35 UTC [re2ob_16-01#0, re2ob_16-04#2]
- 2024-01-15 20:52 UTC — operation latency: recommendationservice_ListRecommendations — baseline mean 0.7561; later mean 1.62 (x1.49); peak 12.00 at 2024-01-15 20:52:45 UTC [re2ob_16-02#0]
- 2024-01-15 20:53 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 6.75 at 2024-01-15 20:53:57 UTC; sustained deviation from 2024-01-15 20:48:12 UTC (score 36.11); metric anomalies: checkoutservice_latency-90 — baseline median 0.6542; peak 6.88 at 2024-01-15 20:53:57 UTC; sustained deviation from 2024-01-15 20:48:07 UTC (score 7.08) [re2ob_16-01#1, re2ob_16-01#2]
- 2024-01-15 20:54 UTC — metric anomalies: redis_diskio — baseline median 0; peak 38032 at 2024-01-15 20:54:02 UTC; sustained deviation from 2024-01-15 20:48:48 UTC (score 122) [re2ob_16-01#0]
- 2024-01-15 20:55 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.2468; peak 0.7308 at 2024-01-15 20:55:37 UTC; sustained deviation from 2024-01-15 20:48:27 UTC (score 7.86); operation latency: productcatalogservice_GetProduct — baseline mean 5.80; later mean 6.84 (x1.15); peak 39.00 at 2024-01-15 20:55:45 UTC [re2ob_16-01#2, re2ob_16-02#0]
- 2024-01-15 20:56 UTC — metric anomalies: currencyservice_cpu — baseline median 18.51; peak 11.83 at 2024-01-15 20:56:38 UTC; sustained deviation from 2024-01-15 20:47:22 UTC (score 3.52) [re2ob_16-01#3]
- 2024-01-15 20:57 UTC — metric anomalies: frontend_socket — baseline median 59.00; peak 30.00 at 2024-01-15 20:57:05 UTC; sustained deviation from 2024-01-15 20:45:12 UTC (score 32.77) [re2ob_16-01#1]
- 2024-01-15 20:58 UTC — metric anomalies: emailservice_mem — baseline median 43921408; peak 131764224 at 2024-01-15 20:58:53 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 78.33); metric anomalies: emailservice_cpu — baseline median 0.288; peak 3.38 at 2024-01-15 20:58:01 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 17.98); operation latency: shippingservice_GetQuote — baseline mean 0.1463; later mean 0.3036 (x1.14); peak 5.00 at 2024-01-15 20:58:15 UTC; operation latency: cartservice_AddItem — baseline mean 0.0244; later mean 0.1429 (x1.12); peak 2.00 at 2024-01-15 20:58:00 UTC [re2ob_16-01#1, re2ob_16-02#1]

## Detection: IDS Alerts

- metric anomalies: emailservice_mem — baseline median 43921408; peak 131764224 at 2024-01-15 20:58:53 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 78.33) [re2ob_16-01#1]
- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 6.75 at 2024-01-15 20:53:57 UTC; sustained deviation from 2024-01-15 20:48:12 UTC (score 36.11) [re2ob_16-01#1]
- metric anomalies: frontend_socket — baseline median 59.00; peak 30.00 at 2024-01-15 20:57:05 UTC; sustained deviation from 2024-01-15 20:45:12 UTC (score 32.77) [re2ob_16-01#1]
- metric anomalies: emailservice_cpu — baseline median 0.288; peak 3.38 at 2024-01-15 20:58:01 UTC; sustained deviation from 2024-01-15 20:48:19 UTC (score 17.98) [re2ob_16-01#1]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: recommendationservice_ListRecommendations — baseline mean 0.7561; later mean 1.62 (x1.49); peak 12.00 at 2024-01-15 20:52:45 UTC [re2ob_16-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0.3902; later mean 0.75 (x1.26); peak 6.00 at 2024-01-15 20:49:30 UTC [re2ob_16-02#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.2143 (x1.21); peak 3.00 at 2024-01-15 20:47:45 UTC [re2ob_16-02#0]
- operation latency: productcatalogservice_GetProduct — baseline mean 5.80; later mean 6.84 (x1.15); peak 39.00 at 2024-01-15 20:55:45 UTC [re2ob_16-02#0]

## Root Cause and Evidence Gaps

- log templates: new after the baseline: 'checkoutservice failed to send order confirmation to "someone@example.com": rpc error: code = Unavailable desc = no heal' — 33 lines, first at 2024-01-15 20:47:52 UTC [re2ob_16-04#2]
- log templates: new after the baseline: 'emailservice Transient error StatusCode.DEADLINE EXCEEDED encountered while exporting traces to jaeger-collector.telemet' — 6 lines, first at 2024-01-15 20:50:35 UTC [re2ob_16-04#2]
- log templates: new after the baseline: 'emailservice starting the email service in dummy mode.' — 5 lines, first at 2024-01-15 20:48:09 UTC [re2ob_16-04#2]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: emailservice_SendOrderConfirmation — baseline mean 0; later mean 8.25; first error after baseline at 2024-01-15 20:47:45 UTC [re2ob_16-03#0]
2. operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.05; later mean 5.30 (x1.04); peak 18.00 at 2024-01-15 20:47:15 UTC [re2ob_16-02#2]
3. operation latency: shippingservice_ShipOrder — baseline mean 0.122; later mean 0.1429 (x1.02); peak 1.00 at 2024-01-15 20:45:30 UTC [re2ob_16-02#2]
4. Not established from the available artifacts.
5. log templates: new after the baseline: 'emailservice Transient error StatusCode.DEADLINE EXCEEDED encountered while exporting traces to jaeger-collector.telemet' — 6 lines, first at 2024-01-15 20:50:35 UTC [re2ob_16-04#2]
6. log templates: new after the baseline: 'emailservice starting the email service in dummy mode.' — 5 lines, first at 2024-01-15 20:48:09 UTC [re2ob_16-04#2]
7. log templates: new after the baseline: 'emailservice listening on port: <:NUM:>' — 5 lines, first at 2024-01-15 20:48:09 UTC [re2ob_16-04#2]
8. Not established from the available artifacts.
