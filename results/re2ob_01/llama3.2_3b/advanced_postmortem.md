# Incident Postmortem: Microservice reliability incident investigation

## Incident Summary

* The root-cause service is not established from the available artifacts.
* The root-cause service is running on a Kubernetes pod named emailservice-5c77d688f7-wzlg6 on node gke-gke-cluster-default-pool-2e1807ce-w819. [auto: re2ob_01-05#1]
* The earliest sign of the failure appeared at 2024-01-15 21:34:06 UTC. [re2ob_01-01#3, re2ob_01-04#2, re2ob_01-05#1, re2ob_01-05#2, re2ob_01-05#0]
* The primary CIA component affected is availability, as the incident resulted in user-facing latency and errors in multiple services.
* The single service operation with the largest latency increase is shippingservice_GetQuote, which is not the root cause but a downstream symptom. [re2ob_01-06#0]

## Affected Service and Infrastructure

* The failure most likely originated in the `adservice` service, as indicated by the metric anomaly [re2ob_01-01#3], which shows a sustained deviation in socket metrics starting at 2024-01-15 21:34:06 UTC.
* The `adservice` service is running on a Kubernetes pod named `adservice-8587fdc599-swwgx` on node `gke-gke-cluster-default-pool-2e1807ce-xte3` [re2ob_01-05#0].
* The `adservice` service is not listed as an affected service in the symptoms, suggesting it may be the root cause of the incident.
* No other services are listed as being affected by the incident, suggesting that the failure may be isolated to the `adservice` service.

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

* adservice_socket — baseline median 4.00; peak 5.00 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 0) [re2ob_01-01#3]
* checkoutservice_cpu — baseline median 0.4139; peak 20.03 at 2024-01-15 21:42:50 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 121) [re2ob_01-01#0]
* redis_diskio — baseline median 0; peak 46680 at 2024-01-15 21:34:06 UTC; sustained deviation from 2024-01-15 21:34:06 UTC (score 103) [re2ob_01-01#0]
* checkoutservice_socket — baseline median 9.00; peak 11.00 at 2024-01-15 21:36:20 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 13.79) [re2ob_01-01#0]
* checkoutservice_mem — baseline median 11685888; peak 16846848 at 2024-01-15 21:37:35 UTC; sustained deviation from 2024-01-15 21:36:20 UTC (score 11.83) [re2ob_01-01#1]
* currencyservice_latency-90 — baseline median 0.0987; peak 0.1312 at 2024-01-15 21:34:42 UTC; sustained deviation from 2024-01-15 21:34:37 UTC (score 2.85) [re2ob_01-01#1]

## Service Dependencies and Propagation

* Operation shippingservice_GetQuote showed the largest latency increase, with a mean latency of 1.75 (x2.51) compared to the baseline mean of 0.0976. [auto: re2ob_01-06#0, re2ob_01-02#0]
* Assessment: The root cause of the latency increase in shippingservice_GetQuote is not established from the available artifacts.
* Assessment: The latency increase in shippingservice_GetQuote appears to be a downstream symptom, as it is not the only service experiencing latency changes.
* Assessment: The service dependencies and propagation of the latency increase are not clear from the available evidence.

## Impact Assessment

* Assessment: The primary CIA component affected is availability, as the incident resulted in user-facing latency and errors in multiple services.
* Affected services: checkoutservice, currencyservice, shippingservice, and productcatalogservice.
* Assessment: The latency spikes in shippingservice_GetQuote and productcatalogservice_GetProduct indicate that these services were under heavy load or experienced issues with their underlying infrastructure.
* Assessment: The sustained deviation in metric anomalies for currencyservice_cpu and redis_cpu suggests that these services experienced CPU utilization issues, which may have contributed to the overall availability impact.

## Root Cause and Evidence Gaps

* Assessment: Not established from the available artifacts.
* Not established from the available artifacts: No root cause, impact or trigger is stated; these must be established from the supplied artifacts.
* Not established from the available artifacts: The absence of alerts, change records, error logs, or telemetry data does not prove the absence of these in other contexts.
* Not established from the available artifacts: The provided latency statistics do not indicate a specific service or fault type.
* Not established from the available artifacts: The absence of warning-level application logs does not prove that no issues were encountered.
* Not established from the available artifacts: The provided telemetry data does not contain any information about packet loss, socket issues, or network delays.
* Not established from the available artifacts: The provided telemetry data does not contain any information about memory or disk I/O issues.

## Corrective and Preventive Actions

* Investigate and address the sustained latency deviation in the productcatalogservice_GetProduct operation, as indicated by metric anomaly re2ob_01-02#0 [re2ob_01-02#0].
* Review and optimize the shippingservice_GetQuote operation to reduce latency, as indicated by metric anomaly re2ob_01-02#0 [re2ob_01-02#0].

## Answers to Investigation Questions

1. The root-cause service is not established from the available artifacts. [re2ob_01-03#0]
2. The Kubernetes pod of the root-cause service is emailservice-5c77d688f7-wzlg6 on node gke-gke-cluster-default-pool-2e1807ce-w819 [re2ob_01-05#1]
3. The Kubernetes node where the emailservice-5c77d688f7-wzlg6 pod runs is node gke-gke-cluster-default-pool-2e1807ce-w819 [re2ob_01-05#1]
4. Not established from the available artifacts.
5. Not established from the available artifacts.
6. The first signs of the failure appeared at 2024-01-15 21:34:06 UTC [re2ob_01-01#0, re2ob_01-01#3, re2ob_01-04#2, re2ob_01-05#1, re2ob_01-05#2, re2ob_01-05#0]
7. The metric that best shows the fault for the root-cause service is not established from the available artifacts.
8. The single service operation with the largest latency increase is shippingservice_GetQuote, which is not the root cause but a downstream symptom [re2ob_01-02#0, re2ob_01-06#0]

---
Verification note: 4 line(s) were removed because their entities, numbers or citations could not be verified against the retrieved evidence; 4 claim(s) remain without a citation. Details: advanced_run_report.json.
## Additional Investigation Questions

U1. The email address of the on-call engineer who acknowledged the incident is Not established from the available artifacts.
U3. The Linux kernel version ran on the node that hosted the pod of the root-cause service is Not established from the available artifacts.
