# Chapter 19 · High Availability & Failover

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-18-identity-aaa-and-secure-access/README.md) · [Next chapter](../chapter-20-qos-and-performance/README.md)

## Chapter topics

1. [An Active-Standby Pair](01-pair.md)
2. [Recovery and Redundancy](02-recovery.md)

## Say it at work

> Please confirm the active role, standby health and synchronization state.

> Are the redundant circuits physically diverse and independently powered?

> Measure the service interruption during the planned switchover.

> Is failback automatic, and could it cause another interruption?

## Quick review

1. Does redundancy automatically remove every single point of failure?
2. Is the primary device always currently active?
3. What is the difference between RTO and RPO?
4. Is a heartbeat necessarily the same as state synchronization?

**Answers**

1. No; common dependencies must be examined.
2. Not necessarily; terminology and roles vary.
3. RTO concerns restoration time; RPO concerns acceptable data loss.
4. No; they can use separate mechanisms or paths.

## All chapter entries (24)

- [active-active](entries/active-active.md)
- [active-standby](entries/active-standby.md)
- [BFD for failover](entries/bfd-failover.md)
- [cluster quorum](entries/quorum.md)
- [failback](entries/failback.md)
- [failover](entries/failover.md)
- [failure detection](entries/failure-detection.md)
- [first-hop redundancy](entries/first-hop-redundancy.md)
- [HA heartbeat](entries/heartbeat.md)
- [high availability](entries/high-availability.md)
- [Hot Standby Router Protocol](entries/hsrp.md)
- [mean time to repair](entries/mean-time-to-repair.md)
- [path diversity](entries/path-diversity.md)
- [primary device](entries/primary-device.md)
- [recovery point objective](entries/recovery-point-objective.md)
- [recovery time](entries/recovery-time.md)
- [recovery time objective](entries/recovery-time-objective.md)
- [redundancy](entries/redundancy.md)
- [service availability](entries/availability.md)
- [split-brain](entries/split-brain.md)
- [standby device](entries/standby-device.md)
- [state synchronization](entries/state-synchronization.md)
- [switchover](entries/switchover.md)
- [Virtual Router Redundancy Protocol](entries/vrrp.md)

## Sources

- [RFC 5798: Virtual Router Redundancy Protocol](https://www.rfc-editor.org/info/rfc5798/)
- [RFC 5880: Bidirectional Forwarding Detection](https://www.rfc-editor.org/info/rfc5880/)
- [NIST: Contingency Planning Guide](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
