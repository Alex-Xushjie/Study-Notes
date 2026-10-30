# Chapter 12 · WAN, VPN & Service Providers

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-11-bgp-and-routing-policy/README.md) · [Next chapter](../../part-04/chapter-13-campus-and-branch-networks/README.md)

## Chapter topics

1. [Provider Connectivity](01-provider.md)
2. [Tunnels and VPNs](02-vpn.md)

## Say it at work

> Please confirm the circuit ID, handoff type and demarcation point.

> The physical circuit is up, but the VPN tunnel is down.

> Can the provider test the service to the agreed demarcation point?

> The tunnel is established; we are checking routes and security policy.

## Quick review

1. Does every VPN encrypt its traffic?
2. What is a demarcation point?
3. Does an active tunnel prove end-to-end application reachability?
4. What is the underlay?

**Answers**

1. No; encryption depends on the specific VPN technology and configuration.
2. The agreed boundary between provider and customer responsibility.
3. No; routes, policy and endpoints must also be verified.
4. The underlying network providing transport for the overlay or tunnel.

## All chapter entries (24)

- [carrier circuit](entries/carrier-circuit.md)
- [circuit ID](entries/circuit-id.md)
- [customer edge](entries/customer-edge.md)
- [customer-premises equipment](entries/customer-premises-equipment.md)
- [demarcation point](entries/demarcation-point.md)
- [encryption](entries/encryption.md)
- [Internet Protocol Security](entries/ipsec.md)
- [IPsec security association](entries/security-association.md)
- [label-switched path](entries/label-switched-path.md)
- [last mile](entries/last-mile.md)
- [leased line](entries/leased-line.md)
- [MPLS label](entries/mpls-label.md)
- [Multiprotocol Label Switching](entries/mpls.md)
- [network handoff](entries/handoff.md)
- [network overlay](entries/overlay.md)
- [network tunnel](entries/tunnel.md)
- [network underlay](entries/underlay.md)
- [provider edge](entries/provider-edge.md)
- [service provider](entries/service-provider.md)
- [service-level agreement](entries/service-level-agreement.md)
- [site-to-site VPN](entries/site-to-site-vpn.md)
- [tunnel endpoint](entries/tunnel-endpoint.md)
- [virtual private network](entries/virtual-private-network.md)
- [wide area network](entries/wide-area-network.md)

## Sources

- [RFC 3031: Multiprotocol Label Switching Architecture](https://www.rfc-editor.org/info/rfc3031/)
- [RFC 4301: Security Architecture for the Internet Protocol](https://www.rfc-editor.org/info/rfc4301/)
- [RFC 4364: BGP/MPLS IP Virtual Private Networks](https://www.rfc-editor.org/info/rfc4364/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
