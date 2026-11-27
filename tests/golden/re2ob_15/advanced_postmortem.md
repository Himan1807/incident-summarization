# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 14 of 73 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_15-01#0]
- metric anomalies: emailservice_diskio — baseline median 0; peak 11573551770 at 2024-01-16 01:56:34 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 190) [re2ob_15-01#0]
- metric anomalies: emailservice_cpu — baseline median 0.2869; peak 19.70 at 2024-01-16 02:02:51 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 160) [re2ob_15-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 40215 at 2024-01-16 02:00:12 UTC; sustained deviation from 2024-01-16 01:54:48 UTC (score 128) [re2ob_15-01#0]
- Derived: earliest sustained metric deviation: currencyservice_cpu from 2024-01-16 01:52:55 UTC. [re2ob_15-06#0]
- Derived: metric series ranked #1 by deviation score: emailservice_diskio (score 190). [re2ob_15-06#0]
- Derived: trace operation with the largest latency increase: health_Check (mean 0.0732 -> 0.2857, x1.20). [re2ob_15-06#0]
- Derived: container with the largest change in log volume: checkoutservice (80.10 -> 72.43 lines/min). [re2ob_15-06#0]
- metric anomalies: shippingservice_cpu — baseline median 0.2373; peak 0.1146 at 2024-01-16 02:00:51 UTC; sustained deviation from 2024-01-16 02:00:51 UTC (score 2.02) [re2ob_15-01#3]
- operation latency: health_Check — baseline mean 0.0732; later mean 0.2857 (x1.20); peak 2.00 at 2024-01-16 01:54:15 UTC [re2ob_15-02#0]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-16 02:01:15 UTC [re2ob_15-02#0]
- operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-16 01:57:45 UTC [re2ob_15-02#0]
- operation latency: adservice_GetAds — baseline mean 0.7805; later mean 0.75 (x0.9829); peak 7.00 at 2024-01-16 01:56:30 UTC [re2ob_15-02#0]
- operation latency: checkoutservice_PlaceOrder — baseline mean 0.2927; later mean 0.1786 (x0.9117); peak 2.00 at 2024-01-16 01:56:30 UTC [re2ob_15-02#2]
- operation latency: cartservice_GetCart — baseline mean 3.44; later mean 2.95 (x0.889); peak 16.00 at 2024-01-16 01:57:30 UTC [re2ob_15-02#2]

## Timeline

- 2024-01-16 01:52 UTC — earliest sustained metric deviation: currencyservice_cpu from 2024-01-16 01:52:55 UTC [re2ob_15-06#0]
- 2024-01-16 01:53 UTC — metric anomalies: currencyservice_cpu — baseline median 18.63; peak 10.96 at 2024-01-16 01:53:34 UTC; sustained deviation from 2024-01-16 01:52:55 UTC (score 3.12); operation latency: traceservice_Export — baseline mean 0.1951; later mean 0.1607 (x0.9712); peak 2.00 at 2024-01-16 01:53:00 UTC [re2ob_15-01#1, re2ob_15-02#1]
- 2024-01-16 01:54 UTC — operation latency: health_Check — baseline mean 0.0732; later mean 0.2857 (x1.20); peak 2.00 at 2024-01-16 01:54:15 UTC [re2ob_15-02#0]
- 2024-01-16 01:56 UTC — metric anomalies: emailservice_diskio — baseline median 0; peak 11573551770 at 2024-01-16 01:56:34 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 190); operation latency: adservice_GetAds — baseline mean 0.7805; later mean 0.75 (x0.9829); peak 7.00 at 2024-01-16 01:56:30 UTC; operation latency: checkoutservice_PlaceOrder — baseline mean 0.2927; later mean 0.1786 (x0.9117); peak 2.00 at 2024-01-16 01:56:30 UTC [re2ob_15-01#0, re2ob_15-02#0, re2ob_15-02#2]
- 2024-01-16 01:57 UTC — metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0235 at 2024-01-16 01:57:12 UTC; sustained deviation from 2024-01-16 01:55:12 UTC (score 112); metric anomalies: emailservice_mem — baseline median 43098112; peak 134217728 at 2024-01-16 01:57:03 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 81.77); operation latency: paymentservice_Charge — baseline mean 0; later mean 0.0179 (x1.02); peak 1.00 at 2024-01-16 01:57:45 UTC; operation latency: cartservice_GetCart — baseline mean 3.44; later mean 2.95 (x0.889); peak 16.00 at 2024-01-16 01:57:30 UTC [re2ob_15-01#1, re2ob_15-02#0, re2ob_15-02#2]
- 2024-01-16 01:58 UTC — operation latency: shippingservice_GetQuote — baseline mean 0.3902; later mean 0.2857 (x0.9248); peak 3.00 at 2024-01-16 01:58:30 UTC; operation latency: cartservice_AddItem — baseline mean 0.2439; later mean 0.1429 (x0.9188); peak 3.00 at 2024-01-16 01:58:45 UTC [re2ob_15-02#1]
- 2024-01-16 02:00 UTC — metric anomalies: redis_diskio — baseline median 0; peak 40215 at 2024-01-16 02:00:12 UTC; sustained deviation from 2024-01-16 01:54:48 UTC (score 128); metric anomalies: shippingservice_cpu — baseline median 0.2373; peak 0.1146 at 2024-01-16 02:00:51 UTC; sustained deviation from 2024-01-16 02:00:51 UTC (score 2.02) [re2ob_15-01#0, re2ob_15-01#3]
- 2024-01-16 02:01 UTC — operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0893 (x1.09); peak 2.00 at 2024-01-16 02:01:15 UTC [re2ob_15-02#0]
- 2024-01-16 02:02 UTC — metric anomalies: emailservice_cpu — baseline median 0.2869; peak 19.70 at 2024-01-16 02:02:51 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 160) [re2ob_15-01#0]
- 2024-01-16 02:03 UTC — metric anomalies: recommendationservice_cpu — baseline median 2.49; peak 0.865 at 2024-01-16 02:03:06 UTC; sustained deviation from 2024-01-16 02:00:00 UTC (score 2.06) [re2ob_15-01#2]
- 2024-01-16 02:05 UTC — metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0156 at 2024-01-16 02:05:04 UTC; sustained deviation from 2024-01-16 01:55:27 UTC (score 99.42) [re2ob_15-01#1]
- 2024-01-16 02:06 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.37; peak 1.72 at 2024-01-16 02:06:22 UTC; sustained deviation from 2024-01-16 01:53:23 UTC (score 3.12); metric anomalies: redis_cpu — baseline median 0.2671; peak 0.157 at 2024-01-16 02:06:43 UTC; sustained deviation from 2024-01-16 01:56:11 UTC (score 3.04); metric anomalies: frontend_cpu — baseline median 6.69; peak 4.36 at 2024-01-16 02:06:44 UTC; sustained deviation from 2024-01-16 01:56:29 UTC (score 2.93); operation latency: shippingservice_ShipOrder — baseline mean 0.1707; later mean 0.0893 (x0.9304); peak 2.00 at 2024-01-16 02:06:45 UTC [re2ob_15-01#2, re2ob_15-02#1]

## Detection: IDS Alerts

- metric anomalies: emailservice_latency-90 — baseline median 0.0046; peak 0.0235 at 2024-01-16 01:57:12 UTC; sustained deviation from 2024-01-16 01:55:12 UTC (score 112) [re2ob_15-01#1]
- metric anomalies: emailservice_latency-50 — baseline median 0.003; peak 0.0156 at 2024-01-16 02:05:04 UTC; sustained deviation from 2024-01-16 01:55:27 UTC (score 99.42) [re2ob_15-01#1]
- metric anomalies: emailservice_mem — baseline median 43098112; peak 134217728 at 2024-01-16 01:57:03 UTC; sustained deviation from 2024-01-16 01:55:01 UTC (score 81.77) [re2ob_15-01#1]
- metric anomalies: currencyservice_cpu — baseline median 18.63; peak 10.96 at 2024-01-16 01:53:34 UTC; sustained deviation from 2024-01-16 01:52:55 UTC (score 3.12) [re2ob_15-01#1]
- metric anomalies: productcatalogservice_cpu — baseline median 3.37; peak 1.72 at 2024-01-16 02:06:22 UTC; sustained deviation from 2024-01-16 01:53:23 UTC (score 3.12) [re2ob_15-01#2]
- metric anomalies: redis_cpu — baseline median 0.2671; peak 0.157 at 2024-01-16 02:06:43 UTC; sustained deviation from 2024-01-16 01:56:11 UTC (score 3.04) [re2ob_15-01#2]
- metric anomalies: frontend_cpu — baseline median 6.69; peak 4.36 at 2024-01-16 02:06:44 UTC; sustained deviation from 2024-01-16 01:56:29 UTC (score 2.93) [re2ob_15-01#2]
- metric anomalies: recommendationservice_cpu — baseline median 2.49; peak 0.865 at 2024-01-16 02:03:06 UTC; sustained deviation from 2024-01-16 02:00:00 UTC (score 2.06) [re2ob_15-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: traceservice_Export — baseline mean 0.1951; later mean 0.1607 (x0.9712); peak 2.00 at 2024-01-16 01:53:00 UTC [re2ob_15-02#1]
- operation latency: shippingservice_ShipOrder — baseline mean 0.1707; later mean 0.0893 (x0.9304); peak 2.00 at 2024-01-16 02:06:45 UTC [re2ob_15-02#1]
- operation latency: shippingservice_GetQuote — baseline mean 0.3902; later mean 0.2857 (x0.9248); peak 3.00 at 2024-01-16 01:58:30 UTC [re2ob_15-02#1]
- operation latency: cartservice_AddItem — baseline mean 0.2439; later mean 0.1429 (x0.9188); peak 3.00 at 2024-01-16 01:58:45 UTC [re2ob_15-02#1]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_15-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_15-03#0]
2. operation latency: checkoutservice_PlaceOrder — baseline mean 0.2927; later mean 0.1786 (x0.9117); peak 2.00 at 2024-01-16 01:56:30 UTC [re2ob_15-02#2]
3. operation latency: cartservice_GetCart — baseline mean 3.44; later mean 2.95 (x0.889); peak 16.00 at 2024-01-16 01:57:30 UTC [re2ob_15-02#2]
4. Not established from the available artifacts.
5. log volume: currencyservice — 2284 lines/min in the baseline, 2257 lines/min later [re2ob_15-04#1]
6. log volume: cartservice — 731 lines/min in the baseline, 723 lines/min later [re2ob_15-04#1]
7. log volume: frontend — 2531 lines/min in the baseline, 2510 lines/min later [re2ob_15-04#1]
8. Not established from the available artifacts.
