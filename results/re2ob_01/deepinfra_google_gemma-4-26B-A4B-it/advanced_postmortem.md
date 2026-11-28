# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

The root cause is assessed to be the redis service on pod redis-cart-6d88d76d78-rgpr4 and node gke-gke-cluster-default-pool-2e1807ce-xte3. The earliest sign of failure was a sustained deviation in redis_diskio starting at 2024-01-15 21:34:06 UTC. The fault type is identified as disk. User-facing impact included availability issues across multiple services, including checkoutservice, currencyservice, redis, shippingservice, traceservice, emailservice, and productcatalogservice. Assessment: The root cause is not established from the available artifacts [Root Cause and Evidence Gaps]. [re2ob_01-05#2, re2ob_01-06#0, re2ob_01-01#0, re2ob_01-01#1, re2ob_01-02#0]

## Affected Service and Infrastructure

* Assessment: adservice (pod adservice-8587fdc599-swwgx on node gke-gke-cluster-default-pool-2e1807ce-xte3) based on adservice_socket metric anomalies [re2ob_01-05#0, re2ob_01-01#3].
* Other affected services: Not established from the available artifacts.

## Timeline

- 2024-01-15 21:34 UTC — metric anomalies: redis_diskio — baseline median 0; peak 46680 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 103); metric anomalies: currencyservice_latency-90 — baseline median 0.0987; peak 0.1312 at 2024-01-15 21:34:42 UTC; sustained deviation from 2024-01-15 21:34:37 UTC (score 2.85); metric anomalies: emailservice_cpu — baseline median 0.2885; peak 0.1659 at 2024-01-15 21:34:43 UTC; sustained deviation from 2024-01-15 21:34:43 UTC (score 2.62); metric anomalies: adservice_socket — baseline median 4.00; peak 5.00 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 0); operation latency: frontendservice_frontend — baseline mean 3.51; later mean 3.79 (x1.06); peak 12.00 at 2024-01-15 21:34:15 UTC; earliest sustained metric deviation: redis_diskio from 2024-01-15 21:34:06 UTC [re2ob_01-01#0, re2ob_01-01#1, re2ob_01-01#2, re2ob_01-01#3, re2ob_01-02#1, re2ob_01-06#0]
- 2024-01-15 21:35 UTC — metric anomalies: redis_cpu — baseline median 0.259; peak 0.1088 at 2024-01-15 21:35:17 UTC; sustained deviation from 2024-01-15 21:35:17 UTC (score 3.93); operation latency: currencyservice_GetSupportedCurrencies — baseline mean 5.07; later mean 5.36 (x1.05); peak 16.00 at 2024-01-15 21:35:30 UTC [re2ob_01-01#1, re2ob_01-02#2]
- 2024-01-15 21:36 UTC — metric anomalies: checkoutservice_socket — baseline median 9.00; peak 11.00 at 2024-01-15 21:36:20 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 13.79); operation latency: shippingservice_ShipOrder — baseline mean 0; later mean 0.0714 (x1.07); peak 1.00 at 2024-01-15 21:36:45 UTC [re2ob_01-01#0, re2ob_01-02#1]
- 2024-01-15 21:37 UTC — metric anomalies: checkoutservice_mem — baseline median 11685888; peak 16846848 at 2024-01-15 21:37:35 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 11.83); metric anomalies: frontend_cpu — baseline median 6.44; peak 4.07 at 2024-01-15 21:37:29 UTC; sustained deviation from 2024-01-15 21:35:25 UTC (score 2.05); metric anomalies: cartservice_latency-90 — baseline median 0.0049; peak 0.0085 at 2024-01-15 21:37:57 UTC; sustained deviation from 2024-01-15 21:34:25 UTC (score 1.97); operation latency: emailservice_SendOrderConfirmation — baseline mean 0; later mean 0.3929 (x1.39); peak 2.00 at 2024-01-15 21:37:00 UTC [re2ob_01-01#1, re2ob_01-01#2, re2ob_01-02#0]
- 2024-01-15 21:39 UTC — metric anomalies: currencyservice_cpu — baseline median 18.79; peak 10.33 at 2024-01-15 21:39:31 UTC; sustained deviation from 2024-01-15 21:34:34 UTC (score 4.68); metric anomalies: recommendationservice_cpu — baseline median 2.53; peak 1.32 at 2024-01-15 21:39:07 UTC; sustained deviation from 2024-01-15 21:38:04 UTC (score 2.47) [re2ob_01-01#1, re2ob_01-01#2]
- 2024-01-15 21:40 UTC — operation latency: currencyservice_Convert — baseline mean 4.90; later mean 5.73 (x1.14); peak 17.00 at 2024-01-15 21:40:30 UTC; operation latency: paymentservice_Charge — baseline mean 0.0244; later mean 0.0714 (x1.05); peak 1.00 at 2024-01-15 21:40:15 UTC [re2ob_01-02#1, re2ob_01-02#2]
- 2024-01-15 21:42 UTC — metric anomalies: checkoutservice_cpu — baseline median 0.4139; peak 20.03 at 2024-01-15 21:42:50 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 121); operation latency: shippingservice_GetQuote — baseline mean 0.0976; later mean 1.75 (x2.51); peak 8.00 at 2024-01-15 21:42:00 UTC [re2ob_01-01#0, re2ob_01-02#0]
- 2024-01-15 21:44 UTC — operation latency: productcatalogservice_GetProduct — baseline mean 5.51; later mean 7.27 (x1.27); peak 43.00 at 2024-01-15 21:44:45 UTC; operation latency: productcatalogservice_ListProducts — baseline mean 0.7561; later mean 0.8571 (x1.06); peak 7.00 at 2024-01-15 21:44:45 UTC [re2ob_01-02#0, re2ob_01-02#1]
- 2024-01-15 21:47 UTC — operation latency: traceservice_Export — baseline mean 0.0488; later mean 0.4643 (x1.40); peak 4.00 at 2024-01-15 21:47:45 UTC [re2ob_01-02#0]

## Detection: Metric Anomalies

* redis_diskio peak 46680 at 2024-01-15 21:34:06 UTC [re2ob_01-01#0]
* checkoutservice_cpu peak 20.03 at 2024-01-15 21:42:50 UTC [re2ob_01-01#0]
* checkoutservice_mem peak 16846848 at 2024-01-15 21:37:35 UTC [re2ob_01-01#1]
* checkoutservice_socket peak 11.00 at 2024-01-15 21:36:20 UTC [re2ob_01-01#0]
* adservice_socket peak 5.00 at 2024-01-15 21:34:06 UTC [re2ob_01-01#3]
* currencyservice_latency-90 peak 0.1312 at 2024-01-15 21:34:42 UTC [re2ob_01-01#1]

## Service Dependencies and Propagation

* shippingservice_GetQuote showed the largest latency increase [re2ob_01-06#0].
* shippingservice_GetQuote mean latency increased from 0.0976 to 1.75 [re2ob_01-02#0].
* productcatalogservice_GetProduct peak latency reached 43.00 [re2ob_01-02#0].
* traceservice_Export peak latency reached 4.00 [re2ob_01-02#0].
* emailservice_SendOrderConfirmation peak latency reached 2.00 [re2ob_01-02#0].
* No operation shows more trace errors than in its baseline [re2ob_01-03#0].
* Assessment: shippingservice_GetQuote is a downstream symptom rather than the root cause [Not established from the available artifacts].
* Assessment: The latency increases are not driven by an increase in error rates [re2ob_01-03#0].

## Impact Assessment

* Assessment: Availability [re2ob_01-01#1, re2ob_01-02#0].
* Affected services include checkoutservice, currencyservice, redis, shippingservice, traceservice, emailservice, and productcatalogservice [re2ob_01-01#1, re2ob_01-02#0].
* Scale of errors is not established from the available artifacts, as no operation shows more trace errors than its baseline [re2ob_01-03#0].

## Root Cause and Evidence Gaps

* Assessment: Root cause is not established from the available artifacts.
* Monitoring alerts and alerting rules are not present in the capture [re2ob_01-07#0].
* Change records and deployment data are not present in the capture [re2ob_01-07#0].
* Error-level or warning-level application logs are not present in the capture [re2ob_01-07#0].
* Disk I/O metrics are missing for most services, provided only for adservice, emailservice, recommendationservice, and redis [re2ob_01-07#0].

## Corrective and Preventive Actions

* Implement memory limits for checkoutservice to address the peak of 16846848 [re2ob_01-01#1].
* Configure alerts for checkoutservice_mem sustained deviations [re2ob_01-01#1].
* Set alerts for currencyservice_latency-90 deviations [re2ob_01-01#1].
* Monitor shippingservice_GetQuote for latency spikes exceeding the 1.75 mean [re2ob_01-02#0].
* Establish alerting for productcatalogservice_GetProduct latency peaks [re2ob_01-02#0].

## Answers to Investigation Questions

1. redis [re2ob_01-06#0]
2. redis-cart-6d88d76d78-rgpr4 [re2ob_01-05#2]
3. gke-gke-cluster-default-pool-2e1807ce-xte3 [re2ob_01-05#2]
4. disk [re2ob_01-06#0]
5. Not established from the available artifacts.
6. 2024-01-15 21:34 UTC [re2ob_01-06#0]
7. redis_diskio [re2ob_01-06#0]
8. shippingservice_GetQuote; downstream symptom [re2ob_01-02#0, re2ob_01-06#0]
## Additional Investigation Questions

U1. Not established from the available artifacts.
U2. Not established from the available artifacts.
U3. Not established from the available artifacts.
