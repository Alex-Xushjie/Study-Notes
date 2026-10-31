# Chapter 11 · BGP & Routing Policy

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-10-ospf-and-is-is/README.md) · [Next chapter](../chapter-12-wan-vpn-and-service-providers/README.md)

## Chapter topics

1. [BGP Peering and Updates](01-peering.md)
2. [Path Attributes and Policy](02-policy.md)

## Say it at work

> The BGP session is established, but the expected prefix is missing.

> Please check the import policy and the received routes.

> Does the export policy allow this prefix to the provider?

> The next hop is unreachable, so the path is not usable.

## Quick review

1. Does an established BGP session guarantee that the intended prefix is installed?
2. What does an ASN identify?
3. What is the difference between import and export policy?
4. Does AS_PATH length alone determine the best path?

**Answers**

1. No; receipt, policy, selection, and next-hop reachability must be checked.
2. An autonomous system.
3. Import applies to received routes; export applies to routes sent to peers.
4. No; BGP selection involves other attributes and implementation settings.

## All chapter entries (40)

- [AS_PATH](entries/as-path.md)
- [autonomous system](entries/autonomous-system.md)
- [autonomous system number](entries/asn.md)
- [BGP address family](entries/bgp-address-family.md)
- [BGP Adj-RIB-In](entries/bgp-adj-rib-in.md)
- [BGP Adj-RIB-Out](entries/bgp-adj-rib-out.md)
- [BGP AS-path prepending](entries/bgp-as-path-prepending.md)
- [BGP best path](entries/bgp-best-path.md)
- [BGP cluster ID](entries/bgp-cluster-id.md)
- [BGP community](entries/bgp-community.md)
- [BGP community attribute](entries/bgp-community-attribute.md)
- [BGP Established state](entries/bgp-established.md)
- [BGP export policy](entries/export-policy.md)
- [BGP import policy](entries/import-policy.md)
- [BGP KEEPALIVE message](entries/bgp-keepalive-message.md)
- [BGP Loc-RIB](entries/bgp-loc-rib.md)
- [BGP LOCAL_PREF](entries/local-preference.md)
- [BGP multi-exit discriminator](entries/med.md)
- [BGP NEXT_HOP](entries/bgp-next-hop.md)
- [BGP NO_EXPORT community](entries/bgp-no-export-community.md)
- [BGP NOTIFICATION message](entries/bgp-notification-message.md)
- [BGP OPEN message](entries/bgp-open-message.md)
- [BGP ORIGIN attribute](entries/bgp-origin-attribute.md)
- [BGP ORIGINATOR_ID](entries/bgp-originator-id.md)
- [BGP path attribute](entries/bgp-path-attribute.md)
- [BGP peer](entries/bgp-peer.md)
- [BGP prefix](entries/bgp-prefix.md)
- [BGP route advertisement](entries/bgp-advertisement.md)
- [BGP route flap](entries/bgp-route-flap.md)
- [BGP route reflector](entries/route-reflector.md)
- [BGP route refresh](entries/bgp-route-refresh.md)
- [BGP route withdrawal](entries/bgp-withdrawal.md)
- [BGP route-reflector client](entries/bgp-route-reflector-client.md)
- [BGP routing policy](entries/bgp-policy.md)
- [BGP session](entries/bgp-session.md)
- [BGP UPDATE message](entries/bgp-update.md)
- [Border Gateway Protocol](entries/bgp.md)
- [external BGP](entries/ebgp.md)
- [internal BGP](entries/ibgp.md)
- [prefix filter](entries/prefix-filter.md)

## Sources

- [RFC 4271: A Border Gateway Protocol 4](https://www.rfc-editor.org/info/rfc4271/)
- [RFC 1997: BGP Communities Attribute](https://www.rfc-editor.org/info/rfc1997/)
- [RFC 4456: BGP Route Reflection](https://www.rfc-editor.org/info/rfc4456/)
- [RFC 8212: Default External BGP Route Propagation Behavior](https://www.rfc-editor.org/info/rfc8212/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
