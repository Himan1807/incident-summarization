# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- The `recommendationservice` pod `recommendationservice-f7497f696-lwmjj` on node `gke-gke-cluster-default-pool-2e1807ce-w819` exhibited a sustained CPU deviation, peaking at 1.52 at 2024-01-19 22:15:38 UTC [re2ob_08-01#3].
- The earliest sign of failure was a sustained deviation in `redis_diskio` starting at 2024-01-19 22:04:52 UTC, followed by anomalies in `frontend_latency-90` and `frontendservice_frontend` latency [re2ob_08-06#0, re2ob_08-01#1, re2ob_08-02#0].
- The fault type was a network delay, evidenced by significant latency increases in `frontend_latency-90` (peaking at 1.83 seconds) and `frontendservice_frontend` (peaking at 28.00) [re2ob_08-01#1, re2ob_08-02#0].
- User-facing impact included potential delays, as `frontend_latency-90` deviated significantly from its baseline median of 0.2073 seconds [re2ob_08-01#1].
- Assessment: The `recommendationservice` CPU anomaly and `redis_diskio` deviation suggest a cascading effect, with the frontend latency increase likely being a downstream symptom [re2ob_08-01#3, re2ob_08-06#0].

## Affected Service and Infrastructure

- The `recommendationservice` pod `recommendationservice-f7497f696-lwmjj` on node `gke-gke-cluster-default-pool-2e1807ce-w819` exhibited a sustained CPU deviation from its baseline median of 2.95, peaking at 1.52 at 2024-01-19 22:15:38 UTC [re2ob_08-01#3].
- Assessment: The `recommendationservice` is the most likely origin of the failure, based on its sustained CPU deviation anomaly [re2ob_08-01#3].
- Other affected services include `frontend`, `paymentservice`, and `checkoutservice`, as their pods were active during the incident window. [re2ob_08-05#1, re2ob_08-05#0]
- No operation errors exceeded baseline levels across any service, indicating no direct trace errors were observed [re2ob_08-03#0].

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

## Detection: Metric Anomalies

- The currencyservice_latency-50 metric peaked at 0.1057, significantly deviating from its baseline median of 0.0041 at 2024-01-19 22:09:01 UTC [re2ob_08-01#0].
- The redis_diskio metric reached a peak of 26623, deviating from its baseline median of 0 at 2024-01-19 22:09:53 UTC [re2ob_08-01#0].
- The checkoutservice_latency-90 metric peaked at 2.04, deviating from its baseline median of 0.2241 at 2024-01-19 22:09:08 UTC [re2ob_08-01#0].
- The frontend_latency-90 metric peaked at 1.83, deviating from its baseline median of 0.2073 at 2024-01-19 22:07:48 UTC [re2ob_08-01#1].
- The currencyservice_cpu metric peaked at 6.59, deviating from its baseline median of 33.43 at 2024-01-19 22:17:48 UTC [re2ob_08-01#2].
- The recommendationservice_cpu metric peaked at 1.52, deviating from its baseline median of 2.95 at 2024-01-19 22:15:38 UTC [re2ob_08-01#3].

## Service Dependencies and Propagation

- The operation with the largest latency increase was `frontendservice_frontend`, rising from a baseline mean of 0 to 16.66 (x17.66) [re2ob_08-06#0].
- `currencyservice_Convert` showed the second-largest latency increase, rising from a baseline mean of 0 to 0.8571 (x1.86) [re2ob_08-02#0].
- No operation showed an increase in trace errors compared to its baseline [re2ob_08-03#0].
- Log volume decreased for `currencyservice` from 2373 to 1579 lines/min, the largest reduction among services [re2ob_08-04#0].
- `redis_diskio` was the earliest metric to show sustained deviation, starting at 2024-01-19 22:04:52 UTC [re2ob_08-06#0].
- `cartservice_AddItem` latency decreased slightly from a baseline mean of 0.0244 to 0.0179 (x0.9936) [re2ob_08-02#1].
- `shippingservice_ShipOrder` latency decreased from a baseline mean of 0.1951 to 0.1071 (x0.9264) [re2ob_08-02#2].
- Assessment: The latency increase in `frontendservice_frontend` is likely a downstream symptom, not the root cause, given the earlier deviation in `redis_diskio` and the lack of error increases. [re2ob_08-06#0, re2ob_08-03#0]

## Impact Assessment

- The primary CIA component affected is availability, as evidenced by sustained latency deviations in frontend, checkoutservice, and currencyservice metrics [re2ob_08-01#1].
- Frontend latency (p90) peaked at 1.83 seconds, a significant increase from the baseline median of 0.2073 seconds, indicating possible user-facing delays [re2ob_08-01#1].
- Cartservice logs show repeated AddItemAsync calls, suggesting increased activity but no direct evidence of errors or failures [re2ob_08-04#2].
- Recommendationservice CPU usage dropped below baseline, but no direct impact on user-facing latency or errors is established [re2ob_08-01#3].
- No operation errors exceeded baseline levels, indicating no direct integrity or confidentiality impact [re2ob_08-03#0].

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is a network delay affecting the frontend service, as evidenced by a significant increase in latency metrics (frontend_latency-90 and frontend_latency-50) and operation latency (frontendservice_frontend). Confidence: medium. [re2ob_08-01#1, re2ob_08-02#0]
- No monitoring alerts were recorded during the incident, leaving gaps in understanding whether alerting rules were triggered or configured correctly [re2ob_08-07#0].
- Change records or deployment data are missing, making it unclear if recent changes contributed to the incident [re2ob_08-07#0].
- Disk I/O metrics are incomplete, with no data for shippingservice and checkoutservice, limiting visibility into potential disk-related issues [re2ob_08-07#0].
- No error- or warning-level application logs were found, leaving gaps in identifying specific faults or exceptions [re2ob_08-07#0].
- The sustained deviation in frontend latency metrics suggests a prolonged issue, but the exact trigger remains unestablished [re2ob_08-01#1].
- Operation latency spikes in currencyservice and checkoutservice occurred concurrently with frontend latency anomalies, but their relationship to the root cause is unclear [re2ob_08-02#0].

## Corrective and Preventive Actions

- Implement resource limits for `currencyservice` to prevent CPU spikes and latency degradation [re2ob_08-01#2].
- Optimize `redis` disk I/O handling to mitigate peak usage observed at 22:09:53 UTC [re2ob_08-01#0].
- Review and tune `checkoutservice` gRPC call handling to reduce latency spikes observed at 22:09:08 UTC [re2ob_08-01#0].
- Monitor `productcatalogservice` CPU usage for sustained deviations and adjust resource allocation accordingly [re2ob_08-01#2].

## Answers to Investigation Questions

1. Not established from the available artifacts.
2. Not established from the available artifacts.
3. Not established from the available artifacts.
4. Not established from the available artifacts.
5. Not established from the available artifacts.
6. 2024-01-19 22:04 UTC [re2ob_08-01#2].
7. currencyservice_latency-50 [re2ob_08-01#0].
8. frontendservice_frontend; downstream symptom [re2ob_08-02#0].

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts. [re2ob_08-03#0]
U2. Not established from the available artifacts. [re2ob_08-05#1]
U3. Not established from the available artifacts. [re2ob_08-04#2]
