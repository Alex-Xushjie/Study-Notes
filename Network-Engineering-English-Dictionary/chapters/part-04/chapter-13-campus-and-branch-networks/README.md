# Chapter 13 · Campus & Branch Networks

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../../part-03/chapter-12-wan-vpn-and-service-providers/README.md) · [Next chapter](../chapter-14-wireless-networks/README.md)

## Chapter topics

1. [Campus Architecture](01-campus.md)
2. [Power and Resilience](02-resilience.md)

## Say it at work

> Please confirm the access switch, uplinks and distribution devices.

> Do the redundant links use separate physical paths and power sources?

> The access point is connected, but the switch reports insufficient PoE budget.

> Check the default gateway and policy between the two VLANs.

## Quick review

1. What does the access layer connect?
2. Does a redundant uplink guarantee independent failure protection?
3. What is the difference between a PSE and a powered device?
4. Is a VLAN the same as a complete security policy?

**Answers**

1. End devices such as workstations and access points.
2. No; shared power, equipment and cabling can create common failures.
3. A PSE supplies PoE power; a powered device receives it.
4. No; policy and enforcement are separate design considerations.

## All chapter entries (24)

- [access layer](entries/access-layer.md)
- [branch network](entries/branch-network.md)
- [campus network](entries/campus-network.md)
- [collapsed core](entries/collapsed-core.md)
- [core layer](entries/core-layer.md)
- [default gateway redundancy](entries/default-gateway-redundancy.md)
- [distribution layer](entries/distribution-layer.md)
- [downlink](entries/downlink.md)
- [failure domain](entries/failure-domain.md)
- [inter-VLAN routing](entries/inter-vlan-routing.md)
- [logical topology](entries/logical-topology.md)
- [network outlet](entries/network-outlet.md)
- [network segmentation](entries/network-segmentation.md)
- [network topology](entries/network-topology.md)
- [physical topology](entries/physical-topology.md)
- [PoE power budget](entries/poe-budget.md)
- [Power over Ethernet](entries/power-over-ethernet.md)
- [power sourcing equipment](entries/power-sourcing-equipment.md)
- [powered device](entries/powered-device.md)
- [redundant link](entries/redundant-link.md)
- [single point of failure](entries/single-point-of-failure.md)
- [site resilience](entries/site-resilience.md)
- [switch stack](entries/access-switch-stack.md)
- [uplink](entries/uplink.md)

## Sources

- [IEEE 802.3 Ethernet standards](https://www.ieee802.org/3/)
- [Cisco: Campus Network Design](https://www.cisco.com/c/en/us/solutions/enterprise-networks/campus-network-design/index.html)

Original text and simplified conceptual diagrams; independent technical and language review remain pending. References may have subsequent updates.
