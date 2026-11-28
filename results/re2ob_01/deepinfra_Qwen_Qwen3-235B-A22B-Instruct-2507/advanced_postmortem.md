# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- The adservice, specifically pod adservice-8587fdc599-swwgx on node gke-gke-cluster-default-pool-2e1807ce-xte3, is assessed as the root-cause service due to sustained socket usage deviation starting at 2024-01-15 21:34:06 UTC [re2ob_01-01#3, re2ob_01-05#0].
- The earliest sign of failure was a spike in redis_diskio at 2024-01-15 21:34:06 UTC, coinciding with the adservice_socket deviation [re2ob_01-01#0, re2ob_01-01#3].
- The fault type involved abnormal socket utilization in adservice, accompanied by downstream latency propagation without elevated error rates [re2ob_01-01#3, re2ob_01-03#0].
- User-facing impact included degraded availability, with increased latency observed in frontend and critical operations such as shippingservice_GetQuote (x2.51) and productcatalogservice_GetProduct (x1.27) [re2ob_01-02#0, re2ob_01-01#1].
- Assessment: The incident originated in adservice due to socket-level anomalies, triggering cascading latency across multiple services despite no observed increase in request errors [re2ob_01-01#3, re2ob_01-06#0].

## Affected Service and Infrastructure

- The adservice is assessed as the service where the failure most likely originated, based on sustained socket usage deviation from baseline starting at 2024-01-15 21:34:06 UTC [re2ob_01-01#3].
- The affected pod for adservice is adservice-8587fdc599-swwgx, running on node gke-gke-cluster-default-pool-2e1807ce-xte3 [re2ob_01-05#0].
- Other services including frontend, paymentservice, and recommendationservice show co-located pod deployments on shared nodes, indicating potential infrastructure-level adjacency but not direct symptom propagation. [re2ob_01-05#1, re2ob_01-05#2]
- No operation in the trace data shows elevated errors beyond baseline, suggesting the issue may not have manifested as explicit request failures [re2ob_01-03#0].

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

- checkoutservice_cpu peaked at 20.03 at 2024-01-15 21:42:50 UTC, deviating from a baseline median of 0.4139 [re2ob_01-01#0]
- redis_diskio peaked at 46680 at 2024-01-15 21:34:06 UTC, deviating from a baseline median of 0 [re2ob_01-01#0]
- checkoutservice_mem peaked at 16846848 at 2024-01-15 21:37:35 UTC, deviating from a baseline median of 11685888 [re2ob_01-01#1]
- adservice_socket peaked at 5.00 at 2024-01-15 21:34:06 UTC, deviating from a baseline median of 4.00 [re2ob_01-01#3]
- currencyservice_latency-90 peaked at 0.1312 at 2024-01-15 21:34:42 UTC, deviating from a baseline median of 0.0987 [re2ob_01-01#1]
- cartservice_latency-90 peaked at 0.0085 at 2024-01-15 21:37:57 UTC, deviating from a baseline median of 0.0049 [re2ob_01-01#2]

## Service Dependencies and Propagation

- The shippingservice_GetQuote operation showed the largest latency increase, rising from a baseline mean of 0.0976 to a later mean of 1.75 (x2.51) [re2ob_01-06#0].
- The redis container exhibited a decrease in log volume from 1.00 to 0.7143 lines/min during the incident [re2ob_01-04#0].
- The checkoutservice had the highest metric deviation score, primarily driven by CPU usage changes [re2ob_01-06#0].
- Latency for productcatalogservice_GetProduct increased from a baseline mean of 5.51 to a later mean of 7.27 (x1.27) [re2ob_01-02#0].
- The currencyservice_Convert operation latency increased from a baseline mean of 4.90 to a later mean of 5.73 (x1.14) [re2ob_01-02#1].
- No operation showed an increase in trace errors compared to its baseline [re2ob_01-03#0].
- Assessment: The shippingservice_GetQuote operation experienced the most significant latency degradation, indicating it was heavily impacted, but evidence does not confirm it as the root cause [re2ob_01-06#0].
- Assessment: Reduced log volume in redis, combined with early disk I/O deviations, suggests redis may have been under stress or operating abnormally [re2ob_01-06#0].

## Impact Assessment

- The primary CIA component affected was availability, as latency increases and resource deviations impacted service responsiveness [re2ob_01-01#1].
- Services affected include currencyservice, checkoutservice, redis, shippingservice, emailservice, and productcatalogservice based on metric and operation-level anomalies [re2ob_01-01#1].
- Other operations showed elevated latency, including emailservice_SendOrderConfirmation and productcatalogservice_GetProduct, indicating broad propagation of delays [re2ob_01-02#0].
- Assessment: Availability was degraded; no evidence indicates impact to confidentiality or integrity [re2ob_01-03#0].

## Root Cause and Evidence Gaps

- Assessment: The most likely root cause is elevated latency in the shippingservice, specifically the GetQuote operation, which showed the highest relative increase in mean latency (x2.51) and a peak latency of 8.00 seconds [re2ob_01-02#0].
- Assessment: Confidence in this assessment is medium, as latency increases are observed across multiple services but shippingservice exhibits the most significant deviation [re2ob_01-02#0].
- No error or warning logs are present in the captured data, limiting confirmation of internal service faults [re2ob_01-07#0].
- Disk I/O metrics are unavailable for most services, including key components like paymentservice and cartservice, leaving disk-related issues unruled out [re2ob_01-07#0].
- No change records or deployment data are included in the capture, making it impossible to correlate the latency increase with recent code or configuration changes [re2ob_01-07#0].
- No alerts were recorded in the captured window, though this does not confirm whether alerting was configured or triggered outside the scope [re2ob_01-07#0].
- Not established from the available artifacts whether network delay, packet loss, or socket exhaustion contributed to the observed latency increases.

## Corrective and Preventive Actions

- Increase memory limit for checkoutservice based on sustained memory increase peaking at 16846848 bytes [re2ob_01-01#1].
- Investigate currencyservice for potential underutilization or throttling given sustained CPU deviation despite increased latency in Convert operation. [re2ob_01-01#1, re2ob_01-02#1]
- Optimize or scale redis deployment due to sustained CPU deviation, which may impact cartservice latency. [re2ob_01-01#1, re2ob_01-01#2]
- Review emailservice performance under load, as SendOrderConfirmation began exhibiting non-zero latency with a peak of 2.00 seconds [re2ob_01-02#0].

## Answers to Investigation Questions

1. adservice [re2ob_01-01#3]
2. adservice-8587fdc599-swwgx [re2ob_01-05#0]
3. gke-gke-cluster-default-pool-2e1807ce-xte3 [re2ob_01-05#0]
4. socket [re2ob_01-01#3]
5. availability [re2ob_01-02#0]
6. 2024-01-15 21:34 UTC [re2ob_01-01#3]
7. adservice_socket [re2ob_01-01#3]
8. shippingservice_GetQuote, downstream symptom [re2ob_01-06#0]

---
Verification note: 2 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [re2ob_01-07#0]
U2. Not established from the available artifacts [re2ob_01-07#0]
U3. Not established from the available artifacts [re2ob_01-05#0]
