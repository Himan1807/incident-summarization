# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- Not established from the available artifacts.

## Affected Host and User

- metric anomalies: 18 of 73 container metric series deviate from their baseline (first 10 minutes of the capture) [re2ob_21-01#0]
- metric anomalies: productcatalogservice_diskio — no data in the baseline; series appears at 2024-01-15 23:18:44 UTC (first value 2527383617); peak 10079837146 at 2024-01-15 23:22:55 UTC [re2ob_21-01#0]
- metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0802 at 2024-01-15 23:21:09 UTC; sustained deviation from 2024-01-15 23:18:39 UTC (score 161) [re2ob_21-01#0]
- metric anomalies: redis_diskio — baseline median 0; peak 40420 at 2024-01-15 23:19:39 UTC; sustained deviation from 2024-01-15 23:19:13 UTC (score 128) [re2ob_21-01#0]
- Derived: earliest sustained metric deviation: emailservice_socket from 2024-01-15 23:17:01 UTC. [re2ob_21-06#0]
- Derived: metric series ranked #1 by deviation score: productcatalogservice_latency-90 (score 161). [re2ob_21-06#0]
- Derived: metric series without baseline data that appears during the capture: productcatalogservice_diskio (from 2024-01-15 23:18:44 UTC). [re2ob_21-06#0]
- Derived: trace operation with the largest latency increase: productcatalogservice_GetProduct (mean 0 -> 162, x163). [re2ob_21-06#0]
- metric anomalies: cartservice_latency-90 — baseline median 0.005; peak 0.0097 at 2024-01-15 23:24:25 UTC; sustained deviation from 2024-01-15 23:24:22 UTC (score 4.26) [re2ob_21-01#3]
- metric anomalies: productcatalogservice_mem — baseline median 10622976; peak 134217728 at 2024-01-15 23:29:03 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 120) [re2ob_21-01#1]
- metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0648 at 2024-01-15 23:21:07 UTC; sustained deviation from 2024-01-15 23:18:37 UTC (score 102) [re2ob_21-01#1]
- metric anomalies: productcatalogservice_cpu — baseline median 3.36; peak 20.02 at 2024-01-15 23:26:01 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 47.16) [re2ob_21-01#1]
- metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 7.00 at 2024-01-15 23:18:33 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 40.00) [re2ob_21-01#1]
- operation latency: cartservice_AddItem — baseline mean 0.1707; later mean 0.25 (x1.07); peak 2.00 at 2024-01-15 23:23:30 UTC [re2ob_21-02#2]
- operation latency: shippingservice_ShipOrder — baseline mean 0.0976; later mean 0.125 (x1.02); peak 4.00 at 2024-01-15 23:25:30 UTC [re2ob_21-02#2]

## Timeline

- 2024-01-15 23:17 UTC — earliest sustained metric deviation: emailservice_socket from 2024-01-15 23:17:01 UTC [re2ob_21-06#0]
- 2024-01-15 23:18 UTC — metric anomalies: productcatalogservice_diskio — no data in the baseline; series appears at 2024-01-15 23:18:44 UTC (first value 2527383617); peak 10079837146 at 2024-01-15 23:22:55 UTC; metric anomalies: productcatalogservice_socket — baseline median 4.00; peak 7.00 at 2024-01-15 23:18:33 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 40.00); operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 22.46 (x23.46); peak 49.00 at 2024-01-15 23:18:45 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 12.86 (x13.86); peak 27.00 at 2024-01-15 23:18:45 UTC; operation latency: traceservice_Export — baseline mean 0; later mean 0.2321 (x1.23); peak 1.00 at 2024-01-15 23:18:15 UTC; metric series without baseline data that appears during the capture: productcatalogservice_diskio (from 2024-01-15 23:18:44 UTC) [re2ob_21-01#0, re2ob_21-01#1, re2ob_21-02#0, re2ob_21-02#1, re2ob_21-06#0]
- 2024-01-15 23:19 UTC — metric anomalies: redis_diskio — baseline median 0; peak 40420 at 2024-01-15 23:19:39 UTC; sustained deviation from 2024-01-15 23:19:13 UTC (score 128); operation latency: adservice_GetAds — baseline mean 0.4878; later mean 0.7143 (x1.15); peak 14.00 at 2024-01-15 23:19:15 UTC [re2ob_21-01#0, re2ob_21-02#1]
- 2024-01-15 23:20 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 162 (x163); peak 288 at 2024-01-15 23:20:45 UTC; operation latency: frontendservice_frontend — baseline mean 2.12; later mean 2.98 (x1.28); peak 19.00 at 2024-01-15 23:20:30 UTC [re2ob_21-02#0, re2ob_21-02#1]
- 2024-01-15 23:21 UTC — metric anomalies: productcatalogservice_latency-90 — baseline median 0.0044; peak 0.0802 at 2024-01-15 23:21:09 UTC; sustained deviation from 2024-01-15 23:18:39 UTC (score 161); metric anomalies: recommendationservice_latency-90 — baseline median 0.0096; peak 0.0648 at 2024-01-15 23:21:07 UTC; sustained deviation from 2024-01-15 23:18:37 UTC (score 102); metric anomalies: productcatalogservice_latency-50 — baseline median 0.0021; peak 0.0043 at 2024-01-15 23:21:12 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 19.66); metric anomalies: frontend_latency-50 — baseline median 0.1847; peak 0.3859 at 2024-01-15 23:21:24 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 12.72); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0714 (x1.07); peak 2.00 at 2024-01-15 23:21:45 UTC [re2ob_21-01#0, re2ob_21-01#1, re2ob_21-01#2, re2ob_21-02#1]
- 2024-01-15 23:23 UTC — operation latency: cartservice_AddItem — baseline mean 0.1707; later mean 0.25 (x1.07); peak 2.00 at 2024-01-15 23:23:30 UTC [re2ob_21-02#2]
- 2024-01-15 23:24 UTC — metric anomalies: checkoutservice_latency-50 — baseline median 0.2483; peak 0.4706 at 2024-01-15 23:24:12 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 4.74); metric anomalies: cartservice_latency-90 — baseline median 0.005; peak 0.0097 at 2024-01-15 23:24:25 UTC; sustained deviation from 2024-01-15 23:24:22 UTC (score 4.26); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 3.90; later mean 6.82 (x1.60); peak 18.00 at 2024-01-15 23:24:30 UTC [re2ob_21-01#2, re2ob_21-01#3, re2ob_21-02#0]
- 2024-01-15 23:25 UTC — operation latency: shippingservice_ShipOrder — baseline mean 0.0976; later mean 0.125 (x1.02); peak 4.00 at 2024-01-15 23:25:30 UTC [re2ob_21-02#2]
- 2024-01-15 23:26 UTC — metric anomalies: productcatalogservice_cpu — baseline median 3.36; peak 20.02 at 2024-01-15 23:26:01 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 47.16) [re2ob_21-01#1]
- 2024-01-15 23:28 UTC — metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0121 at 2024-01-15 23:28:48 UTC; sustained deviation from 2024-01-15 23:19:03 UTC (score 19.66) [re2ob_21-01#2]
- 2024-01-15 23:29 UTC — metric anomalies: productcatalogservice_mem — baseline median 10622976; peak 134217728 at 2024-01-15 23:29:03 UTC; sustained deviation from 2024-01-15 23:18:33 UTC (score 120) [re2ob_21-01#1]

## Detection: IDS Alerts

- metric anomalies: recommendationservice_latency-50 — baseline median 0.0074; peak 0.0121 at 2024-01-15 23:28:48 UTC; sustained deviation from 2024-01-15 23:19:03 UTC (score 19.66) [re2ob_21-01#2]
- metric anomalies: productcatalogservice_latency-50 — baseline median 0.0021; peak 0.0043 at 2024-01-15 23:21:12 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 19.66) [re2ob_21-01#2]
- metric anomalies: frontend_latency-50 — baseline median 0.1847; peak 0.3859 at 2024-01-15 23:21:24 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 12.72) [re2ob_21-01#2]
- metric anomalies: checkoutservice_latency-50 — baseline median 0.2483; peak 0.4706 at 2024-01-15 23:24:12 UTC; sustained deviation from 2024-01-15 23:18:52 UTC (score 4.74) [re2ob_21-01#2]

## Initial Infection Indicators



## Command-and-Control and Network Activity



## Impact Assessment

- operation latency: productcatalogservice_GetProduct — baseline mean 0; later mean 162 (x163); peak 288 at 2024-01-15 23:20:45 UTC [re2ob_21-02#0]
- operation latency: recommendationservice_ListRecommendations — baseline mean 0; later mean 22.46 (x23.46); peak 49.00 at 2024-01-15 23:18:45 UTC [re2ob_21-02#0]
- operation latency: productcatalogservice_ListProducts — baseline mean 0; later mean 12.86 (x13.86); peak 27.00 at 2024-01-15 23:18:45 UTC [re2ob_21-02#0]
- operation latency: currencyservice_GetSupportedCurrencies — baseline mean 3.90; later mean 6.82 (x1.60); peak 18.00 at 2024-01-15 23:24:30 UTC [re2ob_21-02#0]
- operation latency: frontendservice_frontend — baseline mean 2.12; later mean 2.98 (x1.28); peak 19.00 at 2024-01-15 23:20:30 UTC [re2ob_21-02#1]
- operation latency: traceservice_Export — baseline mean 0; later mean 0.2321 (x1.23); peak 1.00 at 2024-01-15 23:18:15 UTC [re2ob_21-02#1]
- operation latency: adservice_GetAds — baseline mean 0.4878; later mean 0.7143 (x1.15); peak 14.00 at 2024-01-15 23:19:15 UTC [re2ob_21-02#1]
- operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0714 (x1.07); peak 2.00 at 2024-01-15 23:21:45 UTC [re2ob_21-02#1]

## Root Cause and Evidence Gaps

- operation errors: no operation shows more trace errors than in its baseline [re2ob_21-03#0]

## Corrective and Preventive Actions



## Answers to Investigation Questions

1. operation errors: no operation shows more trace errors than in its baseline [re2ob_21-03#0]
2. operation latency: cartservice_AddItem — baseline mean 0.1707; later mean 0.25 (x1.07); peak 2.00 at 2024-01-15 23:23:30 UTC [re2ob_21-02#2]
3. operation latency: shippingservice_ShipOrder — baseline mean 0.0976; later mean 0.125 (x1.02); peak 4.00 at 2024-01-15 23:25:30 UTC [re2ob_21-02#2]
4. Not established from the available artifacts.
5. operation latency: traceservice_Export — baseline mean 0; later mean 0.2321 (x1.23); peak 1.00 at 2024-01-15 23:18:15 UTC [re2ob_21-02#1]
6. operation latency: adservice_GetAds — baseline mean 0.4878; later mean 0.7143 (x1.15); peak 14.00 at 2024-01-15 23:19:15 UTC [re2ob_21-02#1]
7. operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.0714 (x1.07); peak 2.00 at 2024-01-15 23:21:45 UTC [re2ob_21-02#1]
8. Not established from the available artifacts.
