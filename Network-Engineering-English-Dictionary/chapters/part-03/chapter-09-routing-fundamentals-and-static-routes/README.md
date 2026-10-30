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

## All chapter entries (24)

- [administrative distance](entries/administrative-distance.md)
- [black-hole route](entries/black-hole-route.md)
- [default route](entries/default-route.md)
- [destination prefix](entries/destination-prefix.md)
- [directly connected route](entries/directly-connected-route.md)
- [dynamic route](entries/dynamic-route.md)
- [equal-cost multipath](entries/equal-cost-multipath.md)
- [longest prefix match](entries/longest-prefix-match.md)
- [next hop](entries/next-hop.md)
- [outgoing interface](entries/outgoing-interface.md)
- [packet forwarding](entries/forwarding.md)
- [recursive route lookup](entries/recursive-route-lookup.md)
- [return path](entries/return-path.md)
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
- [static route](entries/static-route.md)

## Sources

- [RFC 1812: Requirements for IP Version 4 Routers](https://www.rfc-editor.org/info/rfc1812/)
- [RFC 4632: Classless Inter-domain Routing](https://www.rfc-editor.org/info/rfc4632/)

Original text and simplified conceptual diagrams; technical and language review remain pending. RFCs may have subsequent updates.
