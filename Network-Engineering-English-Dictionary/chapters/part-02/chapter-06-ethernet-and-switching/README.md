# Chapter 06 · Ethernet & Switching

[Home](../../../README.md) · [Contents](../../../TABLE-OF-CONTENTS.md) · [Previous chapter](../chapter-05-models-frames-and-packets/README.md) · [Next chapter](../chapter-07-ip-addressing-and-subnetting/README.md)

## Visual pages

1. [VLANs and switch links](01-vlan.md): access ports, trunks, and VLANs.
2. [Ethernet frames](02-frame.md): source and destination addresses and forwarding.

## Say it at work

> Which VLAN is assigned to the access port?

> Please check whether VLAN 20 is allowed on the trunk.

> The destination MAC address is not present in the forwarding table.

> Check the spanning-tree state before connecting the redundant link.

## Quick review

1. Which address does a switch learn from a received frame?
2. What is the difference between an access port and a trunk port?
3. Does an unknown unicast frame have a broadcast destination address?
4. What is the purpose of spanning tree?

**Answers:** 1. The source MAC address. 2. Access ports generally connect a device to an access VLAN; trunks carry multiple VLANs. 3. No. 4. To establish a loop-free active Layer 2 topology.

## All chapter entries (24)

- [access port](entries/access-port.md)
- [broadcast](entries/broadcast.md)
- [broadcast domain](entries/broadcast-domain.md)
- [destination MAC address](entries/destination-mac-address.md)
- [Ethernet](entries/ethernet.md)
- [frame forwarding](entries/frame-forwarding.md)
- [Layer 2 loop](entries/switching-loop.md)
- [Link Aggregation Control Protocol](entries/lacp.md)
- [MAC address](entries/mac-address.md)
- [MAC address aging](entries/mac-address-aging.md)
- [MAC address table](entries/mac-address-table.md)
- [MAC learning](entries/mac-learning.md)
- [multicast](entries/multicast.md)
- [native VLAN](entries/native-vlan.md)
- [port channel](entries/port-channel.md)
- [root bridge](entries/root-bridge.md)
- [source MAC address](entries/source-mac-address.md)
- [Spanning Tree Protocol](entries/spanning-tree-protocol.md)
- [switchport](entries/switchport.md)
- [trunk port](entries/trunk-port.md)
- [unicast](entries/unicast.md)
- [unknown unicast](entries/unknown-unicast.md)
- [virtual LAN](entries/vlan.md)
- [VLAN tag](entries/vlan-tag.md)

## Sources

- [IEEE 802.1Q: Bridges and Bridged Networks](https://1.ieee802.org/maintenance/p802-1q-rev/)
- [Cisco: VLAN Trunks](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html)
- [Cisco: Spanning Tree Protocol](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10556-16.html)

Original text and simplified conceptual diagrams; independent technical and language review remain pending.
