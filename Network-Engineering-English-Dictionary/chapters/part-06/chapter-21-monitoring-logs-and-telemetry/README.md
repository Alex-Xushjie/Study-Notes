# Chapter 21 · Monitoring, Logs & Telemetry

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../../part-05/chapter-20-qos-and-performance/README.md) · [Next chapter](../chapter-22-troubleshooting-methods-and-tools/README.md)

## Chapter topics

1. [From Measurements to a Dashboard](01-telemetry.md)
2. [Events and Alerts](02-events.md)

## Say it at work

> When did the alert start, and what time zone do the logs use?

> Please record the interface counters and their timestamps on both ends.

> Is the telemetry collector receiving current data from the device?

> Correlate the alert with the reported service impact before drawing conclusions.

## Quick review

1. Is an alert the same as a confirmed root cause?
2. Can polling miss a short event between samples?
3. Is an error count the same as an error rate?
4. Does a packet capture show the whole network?

**Answers**

1. No; it is a signal to investigate.
2. Yes.
3. No; a rate also needs a defined interval or denominator.
4. No; it shows what was observed at the capture point.

## All chapter entries (23)

- [event timestamp](entries/timestamp.md)
- [interface counter](../../part-01/chapter-03-network-hardware-and-interfaces/entries/interface-counter.md) — see Chapter 03
- [interface error rate](entries/error-rate.md)
- [log severity](entries/log-severity.md)
- [monitoring agent](entries/monitoring-agent.md)
- [monitoring alert](entries/alert.md)
- [monitoring dashboard](entries/dashboard.md)
- [monitoring data retention](entries/data-retention.md)
- [monitoring event](entries/event.md)
- [monitoring metric](entries/metric.md)
- [monitoring polling](entries/polling.md)
- [monitoring threshold](entries/threshold.md)
- [network alarm](entries/alarm.md)
- [network monitoring](entries/network-monitoring.md)
- [network observability](entries/observability.md)
- [network telemetry](entries/telemetry.md)
- [packet capture](entries/packet-capture.md)
- [performance baseline](entries/baseline.md)
- [Simple Network Management Protocol](entries/snmp.md)
- [SNMP trap](entries/snmp-trap.md)
- [streaming telemetry](entries/streaming-telemetry.md)
- [Syslog](entries/syslog.md)
- [system log](entries/log.md)
- [telemetry collector](entries/collector.md)

## Sources

- [RFC 3411: SNMP Management Framework](https://www.rfc-editor.org/info/rfc3411/)
- [RFC 5424: Syslog Protocol](https://www.rfc-editor.org/info/rfc5424/)
- [RFC 8639: Subscribed Notifications](https://www.rfc-editor.org/info/rfc8639/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
