# Chapter 10 · OSPF & IS-IS

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-09-routing-fundamentals-and-static-routes/README.md) · [Next chapter](../chapter-11-bgp-and-routing-policy/README.md)

## Chapter topics

1. [Neighbor Relationships](01-neighbors.md)
2. [From Link State to Routes](02-calculation.md)

## Say it at work

> The OSPF neighbor is visible, but the adjacency is not Full.

> Please confirm the OSPF area and network type on both interfaces.

> Check the link-state database before investigating the calculated route.

> Does the IS-IS adjacency operate at Level 1, Level 2, or both?

## Quick review

1. Does every OSPF neighbor form a Full adjacency?
2. Is an OSPF router ID necessarily an interface address?
3. What does SPF calculate?
4. Does IS-IS LSP always mean an MPLS label-switched path?

**Answers**

1. No; adjacency behavior depends on network type and roles.
2. No; it is a 32-bit identifier.
3. Least-cost paths using topology information and the applicable metrics.
4. No; in IS-IS it means a link-state PDU.

## All chapter entries (42)

- [area border router](entries/area-border-router.md)
- [autonomous system boundary router](entries/autonomous-system-boundary-router.md)
- [Bidirectional Forwarding Detection](entries/bfd.md)
- [Intermediate System to Intermediate System](entries/isis.md)
- [IS-IS complete sequence number PDU](entries/isis-csnp.md)
- [IS-IS designated intermediate system](entries/isis-dis.md)
- [IS-IS Level 1](entries/isis-level-1.md)
- [IS-IS Level 2](entries/isis-level-2.md)
- [IS-IS link-state PDU](entries/isis-lsp.md)
- [IS-IS network entity title](entries/isis-net.md)
- [IS-IS partial sequence number PDU](entries/isis-psnp.md)
- [IS-IS system ID](entries/isis-system-id.md)
- [link-state database](entries/link-state-database.md)
- [link-state routing protocol](entries/link-state-protocol.md)
- [LSA flooding](entries/lsa-flooding.md)
- [Open Shortest Path First](entries/ospf.md)
- [OSPF 2-Way state](entries/ospf-two-way-state.md)
- [OSPF adjacency](entries/ospf-adjacency.md)
- [OSPF area](entries/ospf-area.md)
- [OSPF backbone area](entries/ospf-backbone-area.md)
- [OSPF backup designated router](entries/backup-designated-router.md)
- [OSPF cost](entries/ospf-cost.md)
- [OSPF dead interval](entries/dead-interval.md)
- [OSPF designated router](entries/designated-router.md)
- [OSPF Exchange state](entries/ospf-exchange-state.md)
- [OSPF ExStart state](entries/ospf-exstart-state.md)
- [OSPF external type 1 route](entries/ospf-external-type-one.md)
- [OSPF external type 2 route](entries/ospf-external-type-two.md)
- [OSPF Full state](entries/ospf-full-state.md)
- [OSPF hello interval](entries/hello-interval.md)
- [OSPF hello packet](entries/hello-packet.md)
- [OSPF link-state advertisement](entries/lsa.md)
- [OSPF link-state database](entries/ospf-link-state-database.md)
- [OSPF Loading state](entries/ospf-loading-state.md)
- [OSPF neighbor](entries/ospf-neighbor.md)
- [OSPF neighbor state](entries/ospf-neighbor-state.md)
- [OSPF network LSA](entries/ospf-network-lsa.md)
- [OSPF not-so-stubby area](entries/ospf-nssa.md)
- [OSPF router ID](entries/ospf-router-id.md)
- [OSPF router LSA](entries/ospf-router-lsa.md)
- [OSPF stub area](entries/ospf-stub-area.md)
- [shortest path first](entries/shortest-path-first.md)

## Sources

- [RFC 2328: OSPF Version 2](https://www.rfc-editor.org/info/rfc2328/)
- [RFC 5340: OSPF for IPv6](https://www.rfc-editor.org/info/rfc5340/)
- [RFC 1195: IS-IS for IP and Dual Environments](https://www.rfc-editor.org/info/rfc1195/)
- [RFC 5880: Bidirectional Forwarding Detection](https://www.rfc-editor.org/info/rfc5880/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
