# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

- The recommendationservice, running on pod recommendationservice-f7497f696-lwmjj located on node gke-gke-cluster-default-pool-2e1807ce-w819, exhibited sustained CPU underutilization, indicating a potential service crash or unresponsiveness [re2ob_08-01#3, re2ob_08-05#2].
- The earliest sign of failure occurred at 2024-01-19 22:03:43 UTC when the last log entry for 'recommendationservice [Recv ListRecommendations]' was recorded, followed by cessation of expected log activity [re2ob_08-04#3].
- The fault type was a lack of responsiveness in recommendationservice, leading to downstream latency propagation without an increase in trace errors [re2ob_08-03#0].
- Assessment: The root cause originated in recommendationservice, whose failure triggered cascading latency increases across dependent services, particularly affecting user-facing operations despite no observed errors [re2ob_08-06#0].

## Affected Service and Infrastructure

- recommendationservice experienced sustained CPU deviation below baseline, with peak at 1.52 compared to median 2.95 during the query window [re2ob_08-01#3].
- The pod recommendationservice-f7497f696-lwmjj was observed on node gke-gke-cluster-default-pool-2e1807ce-w819 [re2ob_08-05#2].
- Assessment: recommendationservice is the most likely origin of failure, supported by sustained CPU underutilization indicating potential service unresponsiveness or crash [re2ob_08-01#3].
- Other services including frontend, paymentservice, and shippingservice were present on affected nodes but showed no direct metric anomalies or trace errors beyond baseline. [re2ob_08-05#1, re2ob_08-05#0, re2ob_08-03#0]

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

- redis_diskio peaked at 26623 with sustained deviation starting at 2024-01-19 22:04:52 UTC [re2ob_08-01#0]
- currencyservice_latency-50 peaked at 0.1057 with sustained deviation starting at 2024-01-19 22:07:46 UTC [re2ob_08-01#0]
- checkoutservice_latency-90 peaked at 2.04 with sustained deviation starting at 2024-01-19 22:05:53 UTC [re2ob_08-01#0]
- frontend_latency-90 peaked at 1.83 with sustained deviation starting at 2024-01-19 22:07:03 UTC [re2ob_08-01#1]
- currencyservice_cpu dropped to a peak of 6.59 with sustained deviation starting at 2024-01-19 22:06:11 UTC [re2ob_08-01#2]
- productcatalogservice_cpu dropped to a peak of 1.32 with sustained deviation starting at 2024-01-19 22:04:52 UTC [re2ob_08-01#2]

## Service Dependencies and Propagation

- The frontendservice_frontend operation showed the largest latency increase, with mean latency rising from 0 to 16.66 (x17.66) [re2ob_08-06#0].
- The currencyservice_Convert operation experienced a latency increase from 0 to 0.8571 (x1.86), peaking at 6.00 at 2024-01-19 22:07:00 UTC [re2ob_08-02#0].
- The currencyservice_GetSupportedCurrencies operation increased in latency from 0 to 0.3393 (x1.34), peaking at 4.00 at 2024-01-19 22:06:45 UTC [re2ob_08-02#0].
- The checkoutservice_PlaceOrder operation showed increased latency from 0 to 0.2857 (x1.29), peaking at 4.00 at 2024-01-19 22:15:45 UTC [re2ob_08-02#0].
- No operation exhibited an increase in trace errors compared to baseline [re2ob_08-03#0].
- Log volume decreased across multiple services, with currencyservice showing the largest drop from 2373 to 1579 lines/min [re2ob_08-06#0].
- Assessment: The frontendservice_frontend operation was the most severely impacted by latency, indicating user-facing degradation [re2ob_08-06#0].
- Assessment: Increased latencies in currencyservice operations suggest it may be a downstream symptom rather than the root cause, given lack of errors and reduced log volume [re2ob_08-06#0].

## Impact Assessment

- The primary CIA component affected was availability, as evidenced by elevated latency across multiple services without a corresponding increase in trace errors [re2ob_08-03#0].
- Frontend, checkoutservice, currencyservice, and recommendationservice experienced latency increases, with p90 latency peaking at 1.83 seconds for frontend [re2ob_08-01#1].
- The cartservice and recommendationservice showed new log patterns during the incident window, indicating possible changes in request flow or behavior [re2ob_08-04#2].
- Assessment: Availability was degraded due to increased latencies across critical user journey services, despite no observed increase in errors [re2ob_08-03#0].

## Root Cause and Evidence Gaps

- Other services, including currencyservice and checkoutservice, showed moderate latency increases, but none exceeded a 2x change in mean [re2ob_08-02#0].
- Latency anomalies in frontend, checkoutservice, and currencyservice began around 2024-01-19 22:07:00 UTC and persisted for several minutes [re2ob_08-01#1].
- No error or warning logs were observed in the captured data, limiting visibility into application-level faults [re2ob_08-07#0].
- Disk I/O metrics were unavailable for shippingservice and productcatalogservice, leaving disk-related issues in those services unobservable [re2ob_08-07#0].
- Assessment: The most likely root cause is increased CPU load or inefficient processing in the frontend service, given its disproportionate latency increase (high confidence).
- Not established from the available artifacts: presence of network packet loss, socket exhaustion, memory pressure, or external change triggers such as deployments or alerts [re2ob_08-07#0].

## Corrective and Preventive Actions

- Increase CPU request for currencyservice to stabilize performance during traffic surges [re2ob_08-01#2].
- Implement autoscaling for redis based on disk I/O activity to handle increased load [re2ob_08-01#0].
- Set latency-based alerts on checkoutservice (p90) to detect early signs of degradation [re2ob_08-01#0].
- Optimize frontend error handling to reduce latency propagation under downstream service stress [re2ob_08-01#1].
- Enforce resource limits on currencyservice to prevent resource starvation affecting latency [re2ob_08-01#0].

## Answers to Investigation Questions

1. currencyservice [re2ob_08-01#0]
2. currencyservice-b647dd94b-f4mcm [re2ob_08-05#0]
3. gke-gke-cluster-default-pool-2e1807ce-cx8g [re2ob_08-05#0]
4. network delay [re2ob_08-02#0]
5. availability [re2ob_08-01#0]
6. 2024-01-19 22:04 UTC [re2ob_08-01#0]
7. currencyservice_latency-50 [re2ob_08-01#0]
8. frontendservice_frontend — downstream symptom [re2ob_08-02#0]

---
Verification note: 3 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 0 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. Not established from the available artifacts [re2ob_08-01#0]
U2. Not established from the available artifacts [re2ob_08-05#0]
U3. Not established from the available artifacts [re2ob_08-04#2]
