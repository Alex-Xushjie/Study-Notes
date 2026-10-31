# VLANs and Switch Links

**CHAPTER 06 · VISUAL VOCABULARY**

[Chapter](README.md) · [Ethernet frame](02-frame.md)

![Two switches connect hosts in VLAN 10 and VLAN 20. A trunk carries both VLANs across the switches.](../../../assets/chapter06-vlan-topology-v1.svg)

*Example topology; blue and orange indicate logical VLAN membership. The trunk is one physical link.*

## Picture words

| No. | Word | Meaning |
| --- | --- | --- |
| 1 | [switch](../../part-01/chapter-01-network-rooms-and-facilities/entries/network-switch.md) | A device that forwards frames between connections. |
| 2 | [access port](entries/access-port.md) | A switch port configured for an access VLAN. |
| 3 | [trunk port](entries/trunk-port.md) | A switch port that carries traffic for multiple VLANs. |
| 4 | [virtual LAN](entries/vlan.md) | A logical Layer 2 segmentation. |

## Examples and usage

> The workstation is connected to an access port in VLAN 10.

> The trunk carries VLANs 10 and 20 between the switches.

> Verify the allowed VLAN list on both ends of the trunk.

> Check the MAC address table in the correct VLAN.

## More words

[VLAN tag](entries/vlan-tag.md) · [Native VLAN](entries/native-vlan.md) · [Broadcast domain](entries/broadcast-domain.md) · [Spanning Tree Protocol](entries/spanning-tree-protocol.md) · [Port channel](entries/port-channel.md) · [LACP](entries/lacp.md)


## Follow the VLANs

Hosts A and B are in VLAN 10; hosts C and D are in VLAN 20. Their switch-facing links are access links in this example. The switches carry both VLANs across one trunk, subject to the allowed VLAN configuration and forwarding state.

VLANs create separate Layer 2 broadcast domains. Communication between VLAN 10 and VLAN 20 requires routing or another Layer 3 function, which is not shown here. Native VLAN handling, tagging and voice VLAN features depend on the configuration and platform.
