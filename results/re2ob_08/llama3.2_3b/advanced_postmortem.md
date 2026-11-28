# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

Based on the provided log data, the following incident summary can be generated:
**Incident Summary**
* **Incident Type:** Metric Anomalies
* **Services Affected:** Frontend, CheckoutService, CurrencyService
* **Impact:** Significant latency issues for the Frontend service and its dependent services, affecting availability
* **Root Cause:** Not established from the available artifacts
* **Evidence Gaps:** Environment context, fault type, and impact on application functionality or user experience not explicitly stated
* **Corrective and Preventive Actions:**
    + Set resource limits on ProductCatalogService to prevent excessive CPU usage
    + Restart Redis pods to address sustained deviations in redis_cpu and redis_diskio metrics
    + Implement alerting on CurrencyService latency-50 [auto: re2ob_08-06#0, re2ob_08-01#1]
    + Investigate and address sustained deviation in CheckoutService latency-90 [auto: re2ob_08-01#2, re2ob_08-01#1]
    + Review and optimize Frontend latency metrics
**Investigation Questions:**
1. Not established from the available artifacts
2. Not established from the available artifacts
3. Not established from the available artifacts
4. Not established from the available artifacts
5. Not established from the available artifacts
6. Not established from the available artifacts
**Recommendations:**
1. Conduct a thorough investigation to determine the root cause of the incident.
2. Implement alerting on critical metrics to detect potential issues in a timely manner.
3. Review and optimize latency metrics for critical services to ensure they are within acceptable ranges.
4. Investigate and address potential issues with resource allocation and CPU usage for ProductCatalogService.
5. Consider implementing additional monitoring and logging to improve visibility into system performance and reliability.

## Affected Service and Infrastructure

* The emailservice-598f548b4d-gqmtk pod on node gke-gke-cluster-default-pool-2e1807ce-w819 is likely the service where the failure most likely originated.
  [re2ob_08-05#1]
* The frontend-6d8846d9c5-dnnk4 pod on node gke-gke-cluster-default-pool-2e1807ce-cx8g is also affected, indicating a potential propagation of the issue from the emailservice.
  [re2ob_08-05#1]
* The recommendationservice_cpu metric shows a sustained deviation from its baseline median, indicating a potential issue with the service. [auto: re2ob_08-01#3]
  [re2ob_08-01#3]
* The loadgenerator-655bfd9b95-l7gt2 pod on node gke-gke-cluster-default-pool-2e1807ce-0e4z is also affected, suggesting that the issue may be related to external load or stress.
  [re2ob_08-05#1]

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

* The most significant metric deviations are:
  * recommendationservice_cpu: peak 1.52 at 2024-01-19 22:15:38 UTC, sustained deviation from 2024-01-19 22:14:07 UTC (score 3.89) [re2ob_08-01#3]
  * currencyservice_latency-50: peak 0.1057 at 2024-01-19 22:09:01 UTC, sustained deviation from 2024-01-19 22:07:46 UTC (score 128) [re2ob_08-01#0]
  * redis_diskio: peak 26623 at 2024-01-19 22:09:53 UTC, sustained deviation from 2024-01-19 22:04:52 UTC (score 125) [re2ob_08-01#0]
  * checkoutservice_latency-90: peak 2.04 at 2024-01-19 22:09:08 UTC, sustained deviation from 2024-01-19 22:05:53 UTC (score 96.49) [re2ob_08-01#0]
  * paymentservice_latency-90: peak 0.0081 at 2024-01-19 22:06:55 UTC, sustained deviation from 2024-01-19 22:06:38 UTC (score 4.72) [re2ob_08-01#2]
  * productcatalogservice_cpu: peak 1.32 at 2024-01-19 22:08:45 UTC, sustained deviation from 2024-01-19 22:04:52 UTC (score 4.56) [re2ob_08-01#2]

## Service Dependencies and Propagation

* Derived: earliest sustained metric deviation: redis_diskio from 2024-01-19 22:04:52 UTC [re2ob_08-06#0].
* Derived: metric series ranked #1 by deviation score: currencyservice_latency-50 (score 128) [re2ob_08-06#0].
* Assessment: The largest latency increase occurred in the frontendservice_frontend operation, with a mean latency increase of 16.66 (x17.66) [re2ob_08-02#0].
* Assessment: The root cause of the latency increase in frontendservice_frontend is not established from the available artifacts. [Not established from the available artifacts]
* Assessment: The operation latency of frontendservice_frontend is significantly higher than its baseline, indicating a potential issue with the service. [re2ob_08-02#0]
* Operation latency: frontendservice_frontend — baseline mean 0; later mean 16.66 (x17.66); peak 28.00 at 2024-01-19 22:09:00 UTC [re2ob_08-02#0].
* log volume: currencyservice — 2373 lines/min in the baseline, 1579 lines/min later [re2ob_08-04#0].

## Impact Assessment

* The services affected by the incident are the frontend, checkoutservice, and currencyservice, as their latency metrics showed sustained deviations from their baseline values.
* Not established from the available artifacts whether the incident affected the confidentiality or integrity of the system.
* Assessment: The impact assessment suggests that the incident primarily affected the availability of the system, with significant latency issues for the frontend service and its dependent services.

## Root Cause and Evidence Gaps

* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No root cause, impact, or trigger is stated in the evidence.
* Not established from the available artifacts: The environment context, including the services and their interactions, is not explicitly stated.
* Not established from the available artifacts: The specific fault type (CPU, memory, disk, network delay, packet loss, or socket) causing the reliability incident is not identified.
* Not established from the available artifacts: The time at which the reliability incident occurred is not specified.
* Not established from the available artifacts: The impact of the reliability incident on the application's functionality or user experience is not described.
* Not established from the available artifacts: The corrective and preventive actions taken in response to the reliability incident are not documented.

## Corrective and Preventive Actions

* Set resource limits on productcatalogservice to prevent excessive CPU usage, as indicated by sustained deviations from baseline median values [re2ob_08-01#2].
* Restart redis pods to address sustained deviations from baseline median values in redis_cpu and redis_diskio metrics [re2ob_08-01#2, re2ob_08-01#0].
* Implement alerting on currencyservice_latency-50 to detect potential issues with currency service performance [re2ob_08-01#2].
* Investigate and address the sustained deviation from baseline median value in checkoutservice_latency-90, as it may indicate performance issues with the checkout service [re2ob_08-01#0].
* Review and optimize frontend latency metrics to ensure they are within acceptable ranges, as sustained deviations from baseline median values indicate potential performance issues [re2ob_08-01#1].

## Answers to Investigation Questions

1. Not established from the available artifacts [re2ob_08-03#0]
2. Not established from the available artifacts [re2ob_08-05#0]
3. Not established from the available artifacts [re2ob_08-05#1]
4. Not established from the available artifacts, [re2ob_08-01#0, re2ob_08-01#3]
5. Not established from the available artifacts, [re2ob_08-01#0, re2ob_08-01#3]
6. Not established from the available artifacts, [re2ob_08-01#0, re2ob_08-01#3]
7. Not established from the available artifacts, [re2ob_08-01#0, re2ob_08-01#3]
8. Not established from the available artifacts, [re2ob_08-02#0, re2ob_08-02#2]

---
Verification note: 3 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 15 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. The root-cause service that was running is not identified from the available artifacts. [re2ob_08-03#0]
U2. Not established from the available artifacts.
U3. The container image version (tag) of the root-cause service that was running when the failure started is not specified in the evidence.
