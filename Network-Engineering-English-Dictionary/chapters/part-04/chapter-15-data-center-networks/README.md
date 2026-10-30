# Chapter 15 · Data Center Networks

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-14-wireless-networks/README.md) · [Next chapter](../chapter-16-cloud-and-hybrid-connectivity/README.md)

## Chapter topics

1. [A Leaf-Spine Fabric](01-fabric.md)
2. [Overlay Concepts](02-overlay.md)

## Say it at work

> Which leaf and spine devices carry the affected traffic?

> The underlay is reachable, but the endpoint is missing from the overlay.

> Please verify the VNI, VRF and route-target mappings.

> The inter-site path is available; we are checking the service-specific routing.

## Quick review

1. Is EVPN the same thing as VXLAN?
2. What does a VTEP do?
3. Does a VRF replace every security control?
4. What is a route target used for?

**Answers**

1. No; EVPN is a control-plane technology and VXLAN is an encapsulation.
2. It encapsulates and decapsulates VXLAN traffic.
3. No; it provides a separate routing context.
4. To control route import and export into VPN or service contexts.

## All chapter entries (24)

- [anycast gateway](entries/anycast-gateway.md)
- [BGP route target](entries/route-target.md)
- [data center interconnect](entries/data-center-interconnect.md)
- [data center network](entries/data-center-network.md)
- [east-west traffic](entries/east-west-traffic.md)
- [end-of-row switching](entries/end-of-row.md)
- [Ethernet VPN](entries/evpn.md)
- [EVPN route](entries/evpn-route.md)
- [fabric overlay](entries/fabric-overlay.md)
- [fabric underlay](entries/fabric-underlay.md)
- [leaf switch](entries/leaf-switch.md)
- [leaf-spine topology](entries/leaf-spine.md)
- [multi-chassis link aggregation](entries/mlag.md)
- [network fabric](entries/fabric.md)
- [network oversubscription](entries/oversubscription.md)
- [network tenant](entries/tenant.md)
- [north-south traffic](entries/north-south-traffic.md)
- [route distinguisher](entries/route-distinguisher.md)
- [spine switch](entries/spine-switch.md)
- [top-of-rack switching](entries/top-of-rack.md)
- [Virtual Extensible LAN](entries/vxlan.md)
- [virtual routing and forwarding](entries/vrf.md)
- [VXLAN network identifier](entries/vni.md)
- [VXLAN tunnel endpoint](entries/vtep.md)

## Sources

- [RFC 7348: VXLAN](https://www.rfc-editor.org/info/rfc7348/)
- [RFC 7432: BGP MPLS-Based Ethernet VPN](https://www.rfc-editor.org/info/rfc7432/)
- [RFC 8365: EVPN Overlay](https://www.rfc-editor.org/info/rfc8365/)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
