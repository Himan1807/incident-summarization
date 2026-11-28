# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- The adservice pod `adservice-8587fdc599-swwgx` is the likely root cause, supported by its sustained socket metric deviation from baseline [re2ob_01-01#3].
- The earliest sign of failure was observed at 2024-01-15 21:34:06 UTC, marked by sustained deviations in redis_diskio and adservice_socket metrics [re2ob_01-06#0].
- The fault type appears to be a network delay, evidenced by significant latency increases in operations like `shippingservice_GetQuote` [re2ob_01-02#0].
- User-facing impact included increased latency in critical operations such as `productcatalogservice_GetProduct`, which peaked at 43.00 seconds [re2ob_01-02#0].
- Assessment: The primary impact was on availability, driven by latency spikes and sustained deviations in CPU and memory metrics across multiple services [re2ob_01-01#1, re2ob_01-02#0].

## Affected Service and Infrastructure

- The emailservice pod `emailservice-5c77d688f7-wzlg6` was running on node `gke-gke-cluster-default-pool-2e1807ce-w819` during the incident [re2ob_01-05#1].
- The frontend pod `frontend-59688fbf4b-cgrv9` was running on node `gke-gke-cluster-default-pool-2e1807ce-xte3` during the incident [re2ob_01-05#1].
- Assessment: The adservice pod `adservice-8587fdc599-swwgx` likely originated the failure, supported by its sustained socket metric deviation from baseline [re2ob_01-01#3].
- Other affected services include cartservice, checkoutservice, and productcatalogservice, as observed in their pod locations. [re2ob_01-05#0, re2ob_01-05#2]

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

- checkoutservice_cpu peaked at 20.03 at 2024-01-15 21:42:50 UTC, deviating from a baseline median of 0.4139 [re2ob_01-01#0].
- redis_diskio peaked at 46680 at 2024-01-15 21:34:06 UTC, deviating from a baseline median of 0 [re2ob_01-01#0].
- checkoutservice_mem peaked at 16846848 at 2024-01-15 21:37:35 UTC, deviating from a baseline median of 11685888 [re2ob_01-01#1].
- currencyservice_latency-90 peaked at 0.1312 at 2024-01-15 21:34:42 UTC, deviating from a baseline median of 0.0987 [re2ob_01-01#1].
- cartservice_latency-90 peaked at 0.0085 at 2024-01-15 21:37:57 UTC, deviating from a baseline median of 0.0049 [re2ob_01-01#2].
- adservice_socket peaked at 5.00 at 2024-01-15 21:34:06 UTC, deviating from a baseline median of 4.00 [re2ob_01-01#3].

## Service Dependencies and Propagation

- The operation with the largest latency increase was `shippingservice_GetQuote`, with a mean latency increase from 0.0976 to 1.75 (x2.51). [re2ob_01-02#0, re2ob_01-06#0]
- Redis showed the largest change in log volume, decreasing from 1.00 to 0.7143 lines/min [re2ob_01-04#0].
- No operation showed an increase in trace errors compared to its baseline [re2ob_01-03#0].
- The `checkoutservice` had the highest CPU deviation score (121) among all services [re2ob_01-06#0].
- Redis disk I/O deviation was the earliest sustained metric deviation, starting at 2024-01-15 21:34:06 UTC [re2ob_01-06#0].
- Assessment: The latency increase in `shippingservice_GetQuote` is likely a downstream symptom, not the root cause, given the earlier Redis disk I/O deviation [re2ob_01-06#0].
- Assessment: The decrease in Redis log volume suggests reduced activity or potential issues in Redis, which may have propagated to dependent services [re2ob_01-04#0].
- Assessment: The high CPU deviation in `checkoutservice` indicates it was under significant load, potentially exacerbating latency issues in dependent operations [re2ob_01-06#0].

## Impact Assessment

- The currencyservice experienced a sustained CPU deviation, dropping from a baseline median of 18.79 to a peak of 10.33, indicating possible performance degradation [re2ob_01-01#1].
- The shippingservice_GetQuote operation latency increased significantly, with a peak of 8.00 compared to its baseline mean of 0.0976, suggesting possible user-facing delays [re2ob_01-02#0].
- The productcatalogservice_GetProduct operation latency peaked at 43.00, significantly higher than its baseline mean of 5.51, indicating possible user-facing delays [re2ob_01-02#0].
- The redis_cpu metric showed a sustained deviation, dropping from a baseline median of 0.259 to a peak of 0.1088, suggesting possible performance degradation [re2ob_01-01#1].
- Assessment: The primary CIA component affected is availability, as evidenced by increased latency in critical operations and sustained deviations in CPU and memory metrics. [re2ob_01-01#1, re2ob_01-02#0]

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is a network delay affecting shippingservice_GetQuote, evidenced by its significant latency increase (baseline mean 0.0976 to later mean 1.75) and peak latency of 8.00 at 2024-01-15 21:42:00 UTC [re2ob_01-02#0]. Confidence: medium.
- No monitoring alerts or alerting rules were recorded during the capture, leaving gaps in understanding whether alerts were triggered or missed [re2ob_01-07#0].
- No change records or deployment data were captured, making it unclear if recent changes contributed to the incident [re2ob_01-07#0].
- Disk I/O metrics were only available for adservice, emailservice, recommendationservice, and redis, leaving gaps in disk performance data for other services [re2ob_01-07#0].
- No error- or warning-level application logs were recorded, limiting insight into potential application-level faults [re2ob_01-07#0].
- Telemetry for network metrics (e.g., packet loss, bandwidth) is missing, preventing confirmation of network-related issues [re2ob_01-07#0].
- The root cause of latency spikes in other services (e.g., productcatalogservice_GetProduct, traceservice_Export) remains unexplained due to insufficient evidence [re2ob_01-02#0].

## Corrective and Preventive Actions

- Set memory limits on the `checkoutservice` to prevent sustained memory usage spikes observed at 16846848 bytes [re2ob_01-01#1].
- Configure alerts for sustained CPU deviations in the `currencyservice` to detect anomalies like the peak at 10.33 [re2ob_01-01#1].
- Optimize the `shippingservice_GetQuote` operation to reduce latency spikes, which peaked at 8.00 seconds [re2ob_01-02#0].
- Investigate and tune the `productcatalogservice_GetProduct` operation to address the latency peak of 43.00 seconds [re2ob_01-02#0].
- Monitor and analyze the `emailservice_SendOrderConfirmation` operation for potential bottlenecks, given its peak latency of 2.00 seconds [re2ob_01-02#0].

## Answers to Investigation Questions

1. Not established from the available artifacts.
2. Not established from the available artifacts.
3. Not established from the available artifacts.
4. Not established from the available artifacts.
5. Not established from the available artifacts.
6. 2024-01-15 21:34 UTC [re2ob_01-06#0].
7. checkoutservice_cpu [re2ob_01-06#0].
8. shippingservice_GetQuote; not established from the available artifacts [re2ob_01-06#0].
## Additional Investigation Questions

U1. Not established from the available artifacts [re2ob_01-07#0]
U2. Not established from the available artifacts [re2ob_01-07#0]
U3. Not established from the available artifacts [re2ob_01-07#0]
