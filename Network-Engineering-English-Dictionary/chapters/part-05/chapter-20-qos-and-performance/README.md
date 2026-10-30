# Chapter 20 · QoS & Performance

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-19-high-availability-and-failover/README.md) · [Next chapter](../../part-06/chapter-21-monitoring-logs-and-telemetry/README.md)

## Chapter topics

1. [Measuring Network Performance](01-measurements.md)
2. [Traffic Treatment](02-qos.md)

## Say it at work

> Please provide the measurement points, direction and test interval.

> The interface average is low, but short bursts may fill the queue.

> Is the traffic shaped or policed at the provider handoff?

> Check whether the packet marking is preserved across the trust boundary.

## Quick review

1. Is bandwidth the same as throughput?
2. Is round-trip time the same as one-way delay?
3. Does DSCP marking guarantee a particular treatment?
4. Does shaping always have no effect on delay?

**Answers**

1. No; bandwidth is capacity, while throughput is a measured transfer rate.
2. No; RTT includes both directions and their conditions.
3. No; the relevant devices must apply a suitable policy.
4. No; buffering can add delay.

## All chapter entries (24)

- [class of service](entries/class-of-service.md)
- [Differentiated Services Code Point](entries/dscp.md)
- [network bandwidth](entries/bandwidth.md)
- [network congestion](entries/congestion.md)
- [network goodput](entries/goodput.md)
- [network latency](entries/latency.md)
- [network queue](entries/queue.md)
- [network throughput](entries/throughput.md)
- [packet delay variation](entries/jitter.md)
- [packet loss](entries/packet-loss.md)
- [packet scheduler](entries/scheduler.md)
- [priority queue](entries/priority-queue.md)
- [QoS trust boundary](entries/trust-boundary.md)
- [quality of service](entries/quality-of-service.md)
- [queue depth](entries/queue-depth.md)
- [queue drop](entries/queue-drop.md)
- [rate limit](entries/rate-limit.md)
- [round-trip time](entries/round-trip-time.md)
- [service-level objective](entries/service-level-objective.md)
- [traffic burst](entries/burst.md)
- [traffic classification](entries/classification.md)
- [traffic marking](entries/marking.md)
- [traffic policing](entries/policing.md)
- [traffic shaping](entries/shaping.md)

## Sources

- [RFC 2474: Differentiated Services Field](https://www.rfc-editor.org/info/rfc2474/)
- [RFC 3393: IP Packet Delay Variation Metric](https://www.rfc-editor.org/info/rfc3393/)
- [RFC 2680: One-way Packet Loss Metric](https://www.rfc-editor.org/info/rfc2680/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
