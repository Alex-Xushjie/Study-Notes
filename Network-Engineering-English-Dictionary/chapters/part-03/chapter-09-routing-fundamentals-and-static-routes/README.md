# Chapter 09 · Routing Fundamentals & Static Routes

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../../part-02/chapter-08-transport-and-application-services/README.md) · [Next chapter](../chapter-10-ospf-and-is-is/README.md)

## Visual pages

1. [Forwarding to a destination](01-forwarding.md): routes, next hops, and interfaces.
2. [Longest prefix match](02-prefix.md): default and more specific routes.

## Say it at work

> Which route matches the destination, and what is the next hop?

> Please confirm whether the next hop is reachable.

> The forward route exists, but the return path may be missing.

> We observed traffic loss while the routing protocol converged.

## Quick review

1. Is a next hop always the final destination?
2. Which route wins when both /16 and /24 match the destination?
3. Does a route in the table guarantee successful forwarding?
4. Why should the return path be checked?

**Answers:** 1. No. 2. The /24. 3. No; next-hop resolution and forwarding conditions also matter. 4. The reverse direction can use a different path or lack a route.

## All chapter entries (45)

- [(*,G) multicast state](entries/star-g-state.md)
- [(S,G) multicast state](entries/s-g-state.md)
- [administrative distance](entries/administrative-distance.md)
- [any-source multicast](entries/any-source-multicast.md)
- [black-hole route](entries/black-hole-route.md)
- [default route](entries/default-route.md)
- [destination prefix](entries/destination-prefix.md)
- [directly connected route](entries/directly-connected-route.md)
- [dynamic route](entries/dynamic-route.md)
- [equal-cost multipath](entries/equal-cost-multipath.md)
- [IP multicast routing](entries/multicast-routing.md)
- [longest prefix match](entries/longest-prefix-match.md)
- [multicast boundary](entries/multicast-boundary.md)
- [multicast distribution tree](entries/multicast-distribution-tree.md)
- [multicast IP time to live](entries/multicast-ttl.md)
- [multicast outgoing interface list](entries/outgoing-interface-list.md)
- [multicast shared tree](entries/shared-tree.md)
- [multicast source tree](entries/source-tree.md)
- [next hop](entries/next-hop.md)
- [outgoing interface](entries/outgoing-interface.md)
- [packet forwarding](entries/forwarding.md)
- [PIM hello](entries/pim-hello.md)
- [PIM join](entries/pim-join.md)
- [PIM neighbor](entries/pim-neighbor.md)
- [PIM prune](entries/pim-prune.md)
- [PIM rendezvous point](entries/rendezvous-point.md)
- [PIM sparse mode](entries/pim-sparse-mode.md)
- [Protocol Independent Multicast](entries/pim.md)
- [recursive route lookup](entries/recursive-route-lookup.md)
- [rendezvous-point mapping](entries/rp-mapping.md)
- [return path](entries/return-path.md)
- [reverse path forwarding](entries/reverse-path-forwarding.md)
- [route](entries/route.md)
- [route metric](entries/route-metric.md)
- [route preference](entries/route-preference.md)
- [routing](entries/routing.md)
- [routing adjacency](entries/routing-adjacency.md)
- [routing convergence](entries/route-convergence.md)
- [routing loop](entries/routing-loop.md)
- [routing neighbor](entries/routing-neighbor.md)
- [routing protocol](entries/routing-protocol.md)
- [routing table](entries/routing-table.md)
- [RPF interface](entries/rpf-interface.md)
- [source-specific multicast](entries/source-specific-multicast.md)
- [static route](entries/static-route.md)

## Sources

- [RFC 1812: Requirements for IP Version 4 Routers](https://www.rfc-editor.org/info/rfc1812/)
- [RFC 4632: Classless Inter-domain Routing](https://www.rfc-editor.org/info/rfc4632/)

Original text and simplified conceptual diagrams; technical and language review remain pending. RFCs may have subsequent updates.
