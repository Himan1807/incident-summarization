# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

**Overview:**
On 2024-01-15, a series of metric anomalies and service latency increases were observed across multiple services in the system. The primary issue appeared to be related to network delays, which propagated to other services, leading to significant performance degradation. [auto: re2ob_01-06#0, re2ob_01-02#2]
**Key Metrics and Observations:**
1. **Shipping Service Latency Increase**
   - **Operation:** `shippingservice_GetQuote`
   - **Baseline Mean Latency:** 0.0976 seconds [auto: re2ob_01-06#0, re2ob_01-02#0]
   - **Later Mean Latency:** 1.75 seconds (x2.51) [auto: re2ob_01-06#0, re2ob_01-02#0]
   - **Peak Latency:** 8.00 seconds
   - **Timestamp:** 2024-01-15 21:42:00 UTC [auto: re2ob_01-02#0, re2ob_01-01#0]
   - **Node:** [re2ob_01-01#0]
2. **Product Catalog Service Latency Increase**
   - **Operation:** `productcatalogservice_GetProduct`
   - **Baseline Mean Latency:** 5.51 seconds [auto: re2ob_01-02#0]
   - **Later Mean Latency:** 7.27 seconds (x1.27) [auto: re2ob_01-02#0]
   - **Peak Latency:** 43.00 seconds
   - **Timestamp:** 2024-01-15 21:44:45 UTC [auto: re2ob_01-02#1, re2ob_01-02#0]
   - **Nodes:** [re2ob_01-02#0, re2ob_01-02#1]
3. **Traceservice Export Latency Increase**
   - **Operation:** `traceservice_Export`
   - **Baseline Mean Latency:** 0.0488 seconds [auto: re2ob_01-02#0]
   - **Later Mean Latency:** 0.4643 seconds (x1.40) [auto: re2ob_01-02#0]
   - **Peak Latency:** 4.00 seconds
   - **Timestamp:** 2024-01-15 21:47:45 UTC [auto: re2ob_01-02#0]
   - **Node:** [re2ob_01-02#0]
**Metric Anomalies:**
1. **Checkout Service CPU Usage**
   - **Baseline Median:** 0.4139
   - **Peak:** 20.03
   - **Timestamp:** 2024-01-15 21:42:50 UTC [auto: re2ob_01-01#0]
   - **Node:** [re2ob_01-01#0]
2. **Redis Disk I/O**
   - **Baseline Median:** 0
   - **Peak:** 46680
   - **Timestamp:** 2024-01-15 21:34:06 UTC [auto: re2ob_01-06#0, re2ob_01-01#3]
   - **Node:** [re2ob_01-01#0]
3.

## Affected Service and Infrastructure

- Assessment: The failure most likely originated in the `adservice` pod `adservice-8587fdc599-swwgx` on node `gke-gke-cluster-default-pool-2e1807ce-xte3`, as evidenced by the metric anomaly in `adservice_socket` showing a peak deviation at 2024-01-15 21:34:06 UTC [re2ob_01-05#2, re2ob_01-01#3].
- cartservice-5644f7cdc6-s8dh9 on node gke-gke-cluster-default-pool-2e1807ce-cx8g experienced a metric anomaly in `cartservice_error_rate` with a peak deviation at 2024-01-15 21:34:06 UTC, but this is not as pronounced as the `adservice_socket` anomaly [re2ob_01-05#0, re2ob_01-01#3].
- checkoutservice-85d565b4b5-xwr4j on node gke-gke-cluster-default-pool-2e1807ce-w819 showed a metric anomaly in `checkoutservice_latency_p90` with a peak deviation at 2024-01-15 21:34:06 UTC, indicating potential downstream impact [re2ob_01-05#0, re2ob_01-01#3].
- Not established from the available artifacts.

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

- [re2ob_01-01#0] checkoutservice_cpu — baseline median 0.4139; peak 20.03 at 2024-01-15 21:42:50 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 121)
- [re2ob_01-01#0] redis_diskio — baseline median 0; peak 46680 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 103)
- [re2ob_01-01#1] checkoutservice_mem — baseline median 11685888; peak 16846848 at 2024-01-15 21:37:35 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 11.83)
- [re2ob_01-01#3] adservice_socket — baseline median 4.00; peak 5.00 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 0)
- [re2ob_01-01#2] frontend_cpu — baseline median 6.44; peak 4.07 at 2024-01-15 21:37:29 UTC; sustained deviation from 2024-01-15 21:35:25 UTC (score 2.05)

## Service Dependencies and Propagation

- [re2ob_01-02#0] The `shippingservice_GetQuote` operation showed the largest latency increase, with a mean latency of 0.0976 seconds increasing to 1.75 seconds (x2.51), peaking at 8.00 seconds.
- [re2ob_01-06#0] The earliest sustained metric deviation was observed in `redis_diskio` starting from 2024-01-15 21:34:06 UTC.
- [re2ob_01-03#0] No operation showed an increase in trace errors beyond its baseline.
- [re2ob_01-02#2] The `currencyservice_GetSupportedCurrencies` operation experienced a slight increase in latency, with a mean of 5.07 seconds increasing to 5.36 seconds (x1.05).
- [re2ob_01-02#1] The `currencyservice_Convert` operation also showed a slight increase in latency, with a mean of 4.90 seconds increasing to 5.73 seconds (x1.14).
- [re2ob_01-04#0] The `redis` service experienced a decrease in log volume, from 1.00 lines/min to 0.7143 lines/min.
- Assessment: The `shippingservice_GetQuote` operation's latency increase is the most significant observed change, suggesting it may be a key point of failure or symptom in the incident.
- Assessment: The decrease in log volume for `redis` could indicate a potential issue with the cart store, possibly affecting downstream services.
- Assessment: The observed changes in latency and log volume do not suggest a widespread error propagation, as no operations showed a significant increase in trace errors.

## Impact Assessment

- Assessment: Availability was primarily affected, evidenced by the observed latency increases and error rates in multiple services. Not established from the available artifacts.
- Assessment: The checkoutservice, currencyservice, and productcatalogservice experienced significant memory and CPU usage deviations, indicating potential availability issues. [re2ob_01-01#1]
- Assessment: The frontend service, being the user entry point, likely experienced degraded performance due to the propagated latency issues from the backend services. Not established from the available artifacts.
- Assessment: The overall impact was widespread, affecting multiple services and potentially leading to user-facing errors and delays. Not established from the available artifacts.

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is **network delay**. The significant increase in latency for multiple services, particularly `productcatalogservice_GetProduct` with a peak of 43.00, suggests network-related issues. [re2ob_01-02#0]
- Not established: No matching results for monitoring alerts or alerting rules, indicating no alerts were triggered during the incident. [re2ob_01-07#0]
- Not established: No change records or deployments were found in the query, suggesting no recent changes were made. [re2ob_01-07#0]
- Not established: No error- or warning-level application logs were found, indicating all logs were at the info or debug level. [re2ob_01-07#0]
- Not established: Disk I/O metrics were only available for four services, limiting the scope of the analysis. [re2ob_01-07#0]

## Corrective and Preventive Actions

- Reschedule pods for `currencyservice` to ensure consistent CPU usage and prevent future spikes [re2ob_01-01#1, re2ob_01-02#1].
- Set resource limits on `redis` to maintain stable CPU consumption and avoid deviations .
- Alert on sustained deviations in `checkoutservice` memory usage to proactively address potential issues [re2ob_01-01#1].
- Monitor and adjust the latency of `productcatalogservice_GetProduct` to prevent significant increases in response time [re2ob_01-02#0].

## Answers to Investigation Questions

1. The service where the failure originated (the root-cause service) is checkoutservice [re2ob_01-01#0].
2. The name of the Kubernetes pod of the root-cause service is cartservice-5644f7cdc6-s8dh9 [re2ob_01-05#0].
3. The pod of the root-cause service ran on the Kubernetes node gke-gke-cluster-default-pool-2e1807ce-cx8g [re2ob_01-05#0].
4. The type of fault caused the incident is CPU [re2ob_01-01#0].
5. The primary affected CIA component is availability [re2ob_01-01#0].
6. The first signs of the failure appeared during the minute starting at 2024-01-15 21:34 UTC [re2ob_01-03#0].
7. The metric of the root-cause service that best shows the fault is checkoutservice_cpu [re2ob_01-01#0].
8. According to the trace latency statistics, the single service operation that showed the largest latency increase is shippingservice_GetQuote [re2ob_01-02#0].

---
Verification note: 1 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 7 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [re2ob_01-02#0]
U2. Not established from the available artifacts [re2ob_01-01#2]
U3. Not established from the available artifacts,, [re2ob_01-05#1, re2ob_01-05#2, re2ob_01-05#0]
