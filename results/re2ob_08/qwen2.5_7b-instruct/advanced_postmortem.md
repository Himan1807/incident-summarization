# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

**Overview:**
On 2024-01-19, a series of metric anomalies and service latency issues were observed across multiple services in the system. The primary impact was on availability, with significant increases in frontend latency. The root cause appears to be related to the `currencyservice` experiencing high CPU usage, which propagated to other services. [auto: re2ob_08-06#0, re2ob_08-04#3]
**Key Metrics and Anomalies:**
1. **recommendationservice_cpu**:
   - Baseline median: 2.95
   - Peak: 1.52 at 2024-01-19 22:15:38 UTC [auto: re2ob_08-01#3]
   - Sustained deviation from 2024-01-19 22:14:07 UTC (score 3.89) [auto: re2ob_08-01#3]
2. **currencyservice_cpu**:
   - Baseline median: 33.43
   - Peak: 6.59 at 2024-01-19 22:17:48 UTC [auto: re2ob_08-01#2]
   - Sustained deviation from 2024-01-19 22:06:11 UTC (score 9.56) [auto: re2ob_08-01#2]
3. **redis_cpu**:
   - Baseline median: 0.2971
   - Peak: 0.1726 at 2024-01-19 22:18:03 UTC [auto: re2ob_08-01#2]
   - Sustained deviation from 2024-01-19 22:05:16 UTC (score 4.60) [auto: re2ob_08-01#2]
4. **checkoutservice_PlaceOrder**:
   - Baseline mean: 0
   - Later mean: 0.2857 (x1.29)
   - Peak: 4.00 at 2024-01-19 22:15:45 UTC [auto: re2ob_08-02#0]
**Service Dependencies and Propagation:**
- **redis_diskio**:
  - Baseline median: 0
  - Peak: 26623 at 2024-01-19 22:09:53 UTC [auto: re2ob_08-01#0]
  - Sustained deviation from 2024-01-19 22:04:52 UTC [auto: re2ob_08-06#0, re2ob_08-01#2]
- **currencyservice_Convert**:
  - Baseline mean: 0
  - Later mean: 0.8571 (x1.86)
- **cartservice_EmptyCart**:
  - Baseline mean: 0.1951
  - Later mean: 0.0536 (x0.8816)
**Impact Assessment:**

## Affected Service and Infrastructure

- Assessment: The failure most likely originated in the `recommendationservice`. The metric `recommendationservice_cpu` showed a significant deviation from its baseline, with a peak value of 1.52 at 2024-01-19 22:15:38 UTC, indicating a potential issue [re2ob_08-05#2].
- pods: recommendationservice-f7497f696-lwmjj on node gke-gke-cluster-default-pool-2e1807ce-w819 [auto: re2ob_08-05#2]
- Assessment: The `emailservice` also experienced issues, as evidenced by the presence of its pods on multiple nodes [re2ob_08-05#1].

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

- recommendationservice_cpu — baseline median 2.95; peak 1.52 at 2024-01-19 22:15:38 UTC; sustained deviation from 2024-01-19 22:14:07 UTC [re2ob_08-01#3]
- currencyservice_latency-50 — baseline median 0.0041; peak 0.1057 at 2024-01-19 22:09:01 UTC; sustained deviation from 2024-01-19 22:07:46 UTC [re2ob_08-01#0]
- redis_diskio — baseline median 0; peak 26623 at 2024-01-19 22:09:53 UTC; sustained deviation from 2024-01-19 22:04:52 UTC [re2ob_08-01#0]
- checkoutservice_latency-90 — baseline median 0.2241; peak 2.04 at 2024-01-19 22:09:08 UTC; sustained deviation from 2024-01-19 22:05:53 UTC [re2ob_08-01#0]

## Service Dependencies and Propagation

- [re2ob_08-06#0] The earliest sustained metric deviation was observed in `redis_diskio` starting from 2024-01-19 22:04:52 UTC.
- [re2ob_08-02#0] The `frontendservice_frontend` operation showed the largest latency increase, with a mean latency of 0 increasing to 16.66 (x17.66).
- [re2ob_08-02#1] The `currencyservice_Convert` operation had a significant latency increase, from a baseline mean of 0 to 0.8571 (x1.86).
- [re2ob_08-02#2] The `cartservice_EmptyCart` operation experienced a decrease in latency, from a baseline mean of 0.1951 to 0.0536 (x0.8816).
- [re2ob_08-03#0] No operation showed more trace errors than its baseline.
- [re2ob_08-02#0] The `currencyservice_GetSupportedCurrencies` operation had a latency increase from a baseline mean of 0 to 0.3393 (x1.34).
- The `frontendservice_frontend` operation, showing the largest latency increase, is a strong candidate for the root cause or a downstream symptom, given its central role as the user entry point.
- The `currencyservice` operations, particularly `Convert` and `GetSupportedCurrencies`, experienced significant latency increases, indicating potential issues within this service or its dependencies.

## Impact Assessment

- Assessment: Availability was primarily affected, evidenced by the sustained deviation in frontend latency [re2ob_08-01#1]. The peak frontend latency reached 1.83 seconds, a significant increase from the baseline median of 0.2073 seconds, indicating a degradation in service availability.
- Assessment: The impact extended to other services, including checkoutservice and currencyservice, as evidenced by the peak latencies of 0.7969 seconds and 0.2259 seconds, respectively, compared to their baseline medians [re2ob_08-01#1].
- Assessment: The recommendationservice also showed signs of reduced availability, with a peak CPU usage of 1.52, though this was a sustained deviation rather than a peak error rate [re2ob_08-01#3].
- Assessment: User-facing errors were not directly observed, as no service showed a higher error rate than its baseline [re2ob_08-03#0].
- Assessment: The logs indicate increased activity in the cartservice and recommendationservice, with multiple calls logged around the time of the incident, suggesting potential service propagation [re2ob_08-04#2].

## Root Cause and Evidence Gaps

- Not established: No evidence of CPU or memory pressure [re2ob_08-07#0].
- Not established: No disk I/O issues were observed [re2ob_08-07#0].
- Not established: No evidence of socket-related issues [re2ob_08-07#0].
- Not established: No change records or deployments were found [re2ob_08-07#0].
- Not established: No error or warning-level application logs were found [re2ob_08-07#0].

## Corrective and Preventive Actions

- Restart the `currencyservice` pod to address the observed CPU and latency anomalies [re2ob_08-01#1, re2ob_08-01#2].
- Set resource limits on the `paymentservice` to prevent similar latency issues [re2ob_08-01#2].
- Monitor `redis` disk I/O to prevent future spikes that could impact other services [re2ob_08-01#2].
- Alert on `frontend` latency metrics to quickly identify and mitigate issues [re2ob_08-01#1].

## Answers to Investigation Questions

1. The service where the failure originated (the root-cause service) is currencyservice [re2ob_08-01#0].
2. The name of the Kubernetes pod of the root-cause service is currencyservice-b647dd94b-f4mcm [re2ob_08-05#0].
3. The pod of the root-cause service ran on the Kubernetes node gke-gke-cluster-default-pool-2e1807ce-cx8g [re2ob_08-05#0].
4. The type of fault caused the incident is CPU [re2ob_08-01#1, re2ob_08-01#2].
5. The CIA component primarily affected is availability [re2ob_08-01#1, re2ob_08-01#2].
6. The first signs of the failure appeared during the minute starting at 2024-01-19 22:06:11 UTC [re2ob_08-01#2].
7. The metric of the root-cause service that best shows the fault is currencyservice_cpu [re2ob_08-01#1, re2ob_08-01#2].
8. According to the trace latency statistics, the single service operation that showed the largest latency increase is currencyservice_Convert, which is not the root cause but a downstream symptom [re2ob_08-02#0].

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 2 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [re2ob_08-03#0]
U2. Not established from the available artifacts [re2ob_08-05#0]
U3. Not established from the available artifacts [re2ob_08-05#0]
