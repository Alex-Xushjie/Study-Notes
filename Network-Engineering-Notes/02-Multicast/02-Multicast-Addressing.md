---
status: en-draft
title: IPv4 Multicast Addressing and Scope
chapter: 02
tags:
  - Multicast
  - IPv4
  - SSM
  - ASM
  - Address Planning
---

# 02 - IPv4 Multicast Addressing and Scope

## 1. The Nature of Multicast IP Addresses

### 1.1 A Multicast Address Can Only Be a Destination Address

An IPv4 multicast address identifies a logical receiver group, so it can appear only in the destination-address field of an IPv4 header.

Valid multicast packet:

```text
Source IP:      192.168.10.10
Destination IP: 239.1.1.1
```

Invalid packet:

```text
Source IP:      239.1.1.1
Destination IP: 192.168.10.20
```

The source address of a multicast packet must be the sender's unicast IP address. A multicast address cannot be used as an IPv4 source address.

When troubleshooting multicast, distinguish between:

```text
Source Address = Who sent the traffic
Group Address  = Which logical channel received the traffic
```

Together they form multicast forwarding state:

```text
(S,G)
```

For example:

```text
(192.168.10.10, 239.1.1.1)
```

---

### 1.2 A Multicast Address Is Not an Interface Address

A unicast address is normally configured on a specific interface:

```text
interface Ethernet0
 ip address 192.168.10.20 255.255.255.0
```

A multicast address is not normally configured as an interface host address in the same way.

A receiver application uses the Socket API to request that a multicast group be joined on an interface:

```text
Application
    │
    │ Join 239.1.1.1 on ens3
    ▼
Operating System
    │
    ▼
Interface ens3
```

A more precise definition is therefore:

> A multicast group address identifies a logical receiver group rather than a specific host or interface.

The fact that a multicast address does not belong to an interface does not mean multicast forwarding is stateless. A multicast network maintains extensive state, including:

- Host membership state;
- IGMP state;
- IGMP Snooping state;
- `(*,G)` state;
- `(S,G)` state;
- Incoming Interface;
- Outgoing Interface List.

---

### 1.3 Group and Channel

In ASM, a receiver specifies only the multicast group:

```text
G
```

For example:

```text
239.1.1.1
```

This logical object is normally called:

```text
Multicast Group
```

In SSM, a receiver specifies both the source and group:

```text
(S,G)
```

For example:

```text
(10.1.1.10, 232.1.1.1)
```

The logical object identified by both source and group is called:

```text
SSM Channel
```

Even if two SSM channels use the same group, different sources make them different channels:

```text
(10.1.1.10, 232.1.1.1)
(10.1.1.20, 232.1.1.1)
```

---

## 2. IPv4 Multicast Address Space

### 2.1 Basic Range

IPv4 multicast uses:

```text
224.0.0.0/4
```

The complete range is:

```text
224.0.0.0 - 239.255.255.255
```

Traditional classful addressing called this:

```text
Class D Address Space
```

Modern technical documentation preferably uses:

```text
IPv4 Multicast Address Space
```

---

### 2.2 Binary Structure

The four most significant bits of every IPv4 multicast address are fixed at:

```text
1110
```

```text
┌──────────┬────────────────────────────┐
│   1110   │       Remaining 28 bits    │
└──────────┴────────────────────────────┘
  4 bits             28 bits
```

Lowest address:

```text
11100000.00000000.00000000.00000000
224.0.0.0
```

Highest address:

```text
11101111.11111111.11111111.11111111
239.255.255.255
```

The remaining 28 bits can theoretically represent:

```text
2^28 = 268,435,456
```

different values. However, IANA has divided `224.0.0.0/4` into blocks with different meanings, so arbitrary addresses from this space must not be used directly for production services.

---

## 3. Major IPv4 Multicast Address Blocks

### 3.1 Address-Space Overview

| Address Range | Name | Primary Use |
|---|---|---|
| `224.0.0.0/24` | Local Network Control Block | Protocol control traffic limited to the local link |
| `224.0.1.0/24` | Internetwork Control Block | Protocol control traffic that may cross Layer 3 networks |
| `224.0.2.0 - 224.0.255.255` | AD-HOC Block I | Special IANA assignments |
| `224.1.0.0/16` | Reserved | Not for ordinary services |
| `224.2.0.0/16` | SDP/SAP Block | Session-announcement applications |
| `224.3.0.0 - 224.4.255.255` | AD-HOC Block II | Special IANA assignments |
| `224.5.0.0 - 231.255.255.255` | Mostly Reserved | Not for ordinary services |
| `232.0.0.0/8` | Source-Specific Multicast Block | Standard IPv4 SSM address space |
| `233.0.0.0 - 233.251.255.255` | GLOP Block | Historical global allocation based on 16-bit ASNs |
| `233.252.0.0/24` | MCAST-TEST-NET | Documentation and example code |
| `233.252.0.0 - 233.255.255.255` | AD-HOC Block III | Special IANA assignments; the first `/24` is for documentation |
| `234.0.0.0 - 238.255.255.255` | Reserved | Not for ordinary services |
| `239.0.0.0/8` | Administratively Scoped Block | Use within an organization or administrative domain |

> Do not treat `224.0.1.0 - 238.255.255.255` as one uniform globally routable multicast range. It contains Reserved, AD-HOC, SSM, GLOP, and other special-purpose blocks.

---

## 4. Local Network Control Block

### 4.1 Address Range

```text
224.0.0.0/24
```

That is:

```text
224.0.0.0 - 224.0.0.255
```

This block is used for protocol control traffic on the local link.

The core rule is:

> Traffic sent to the Local Network Control Block is not forwarded off the local link.

Routers do not forward traffic destined for `224.0.0.0/24` onto another Layer 3 link.

---

### 4.2 Relationship to TTL

It is inaccurate to simply say:

```text
The device always forces the TTL of 224.0.0.0/24 traffic to 1
```

A more precise understanding is:

1. Many control protocols using this range send packets with TTL 1;
2. Routers cannot forward this traffic off the local link;
3. The link-local restriction applies independently of the packet's current TTL.

Therefore, even an abnormal packet with:

```text
Destination: 224.0.0.5
TTL:         10
```

cannot be forwarded by a router onto another link. TTL is an IP hop limit; the Local Network Control Block has link-local semantics. These concepts must not be confused.

---

### 4.3 Common Addresses

| Address | Purpose |
|---|---|
| `224.0.0.0` | Base Address, reserved |
| `224.0.0.1` | All Systems on This Subnet |
| `224.0.0.2` | All Routers on This Subnet |
| `224.0.0.5` | OSPF AllSPFRouters |
| `224.0.0.6` | OSPF AllDRouters |
| `224.0.0.9` | RIPv2 Routers |
| `224.0.0.10` | EIGRP Routers |
| `224.0.0.13` | All PIM Routers |
| `224.0.0.18` | VRRP |
| `224.0.0.22` | IGMPv3 Routers |

These addresses are used by standard protocols and must not be arbitrarily assigned to enterprise applications.

---

### 4.4 Troubleshooting Intuition

When you see:

```text
224.0.0.X
```

immediately consider that:

- It normally carries protocol control traffic;
- It is valid only on the local link;
- There is no need to troubleshoot a remote RP or cross-subnet PIM tree;
- Focus on the local VLAN, interface state, control-plane filtering, and protocol neighbors;
- TTL alone does not determine whether it can cross a router.

---

## 5. Internetwork Control Block

### 5.1 Address Range

```text
224.0.1.0/24
```

That is:

```text
224.0.1.0 - 224.0.1.255
```

This block also carries protocol control traffic, but unlike `224.0.0.0/24`, it may cross Layer 3 links when allowed by the protocol and network design.

A typical example is:

```text
224.0.1.1
```

It was historically assigned to NTP multicast.

---

### 5.2 Engineering Considerations

Being routable does not mean that traffic will necessarily propagate across the public Internet or an enterprise network.

Actual forwarding still depends on:

- Deployment of multicast routing;
- Whether PIM is enabled;
- Whether RPF succeeds;
- Multicast boundaries;
- ACL and security-policy permissions;
- Multicast service from upstream and downstream networks.

Therefore:

> Address semantics permit forwarding, but network configuration determines whether forwarding actually occurs.

---

## 6. Source-Specific Multicast Block

### 6.1 Standard Range

The standard IPv4 SSM range is:

```text
232.0.0.0/8
```

That is:

```text
232.0.0.0 - 232.255.255.255
```

IANA further reserves:

```text
232.0.0.0
232.0.0.1 - 232.0.0.255
```

Ordinary local application assignments normally use:

```text
232.0.1.0 - 232.255.255.255
```

---

### 6.2 An Address Prefix Does Not Automatically Build a Multicast Tree

An address in `232.0.0.0/8` should suggest SSM, but it does not mean:

```text
As soon as a source sends to 232/8, the network automatically builds an SPT
```

Complete SSM forwarding still requires:

1. A receiver explicitly subscribing to `(S,G)`;
2. The last-hop router receiving source-specific membership;
3. The network enabling the appropriate SSM behavior;
4. A PIM `(S,G)` Join propagating toward the source along the RPF path;
5. Devices along the path building `(S,G)` state;
6. Source data arriving on the correct RPF interface.

Typical flow:

```text
Receiver
   │
   │ IGMPv3 INCLUDE (S,G)
   ▼
Last-Hop Router
   │
   │ PIM (S,G) Join
   ▼
RPF Path toward Source
   │
   ▼
Source
```

Within the SSM range, ASM's `(*,G)` shared tree is not used for source discovery, and an RP does not participate in source discovery.

---

### 6.3 SSM Does Not Guarantee Low Latency

SSM primarily simplifies the control plane:

- No RP is required for source discovery;
- No shared tree is required;
- The receiver explicitly knows the source;
- Only required `(S,G)` state is created;
- Unauthorized sources are easier to restrict;
- Troubleshooting can focus on a specific source and group.

However, the `232/8` prefix itself does not:

- Reduce per-packet ASIC forwarding latency;
- Guarantee the shortest physical path;
- Eliminate unicast-routing detours;
- Eliminate RPF failures;
- Guarantee lossless delivery;
- Guarantee zero convergence time.

More precisely:

> SSM simplifies source discovery and multicast control-plane state, but forwarding performance still depends on the actual network path and platform implementation.

---

### 6.4 Value in Financial Market-Data Networks

Known, fixed market-data sources are often well suited to SSM:

```text
Source IP + Group IP + UDP Port
```

For example:

```text
Source: 10.10.10.10
Group:  232.100.1.1
Port:   UDP 12001
```

A receiver subscribes only to traffic from the specified source, reducing the effect of incorrect or unauthorized sources.

Whether to use `232/8` still depends on:

- The exchange feed specification;
- Existing address planning;
- Receiver support for IGMPv3;
- Device support for SSM;
- Use of SSM mapping;
- Legacy ASM services.

---

## 7. GLOP Block

### 7.1 Address Range

```text
233.0.0.0 - 233.251.255.255
```

GLOP is a multicast address-allocation mechanism based on a 16-bit ASN.

If an organization's 16-bit ASN is represented by two decimal octets:

```text
X.Y
```

it receives:

```text
233.X.Y.0/24
```

For example, ASN 64500:

```text
64500 / 256 = 251 remainder 244
```

corresponds to:

```text
233.251.244.0/24
```

---

### 7.2 Engineering Role

GLOP is useful as a historical address-allocation mechanism, but it should not be the default choice for modern internal enterprise multicast planning.

Modern enterprises and data centers should normally evaluate:

- `232/8` SSM;
- `239/8` Administratively Scoped Multicast;
- Multicast addresses explicitly assigned by an external service provider.

---

## 8. Documentation Address Block

Technical documentation, example code, and lab instructions should use:

```text
233.252.0.0/24
```

This block is called:

```text
MCAST-TEST-NET
```

It must not appear on the public Internet.

For example, documentation can use:

```text
Source: 192.0.2.10
Group:  233.252.0.10
```

This avoids accidentally using an address already assigned to a real protocol or organization.

---

## 9. Administratively Scoped Multicast

### 9.1 Address Range

```text
239.0.0.0/8
```

That is:

```text
239.0.0.0 - 239.255.255.255
```

It is used for multicast services within an administrative domain or organization.

It is often compared to RFC 1918 private unicast space, but the implementation mechanisms are not identical.

---

### 9.2 Public Routers Do Not Automatically Drop These Addresses

It is inaccurate to say:

```text
Public routers unconditionally drop 239/8 traffic
```

The scope of `239/8` must be controlled by administrators through multicast boundaries and filtering policies.

Boundaries may be implemented through:

- Multicast boundaries;
- Group ACLs;
- PIM boundaries;
- TTL thresholds;
- VRF isolation;
- Firewall policies;
- External routing and service policies.

If a boundary device is misconfigured, `239/8` traffic can still be forwarded to unintended locations. Administratively scoped addresses therefore do not replace real security controls.

---

### 9.3 Important RFC 2365 Subranges

#### IPv4 Local Scope

```text
239.255.0.0/16
```

This is intended for a relatively small local administrative scope.

#### IPv4 Organization Local Scope

```text
239.192.0.0/14
```

Range:

```text
239.192.0.0 - 239.195.255.255
```

Organizations can normally prioritize this range when allocating private multicast addresses. The rest of `239/8` includes areas available for scope expansion, but they should not be assigned arbitrarily without a unified address plan.

---

### 9.4 Enterprise and Quantitative-Trading Applications

Administratively Scoped Multicast can be used for:

- Internal enterprise video distribution;
- Service discovery inside a data center;
- Internal real-time data streams;
- Risk-control or monitoring data distribution;
- Internal trading-strategy data;
- Multicast services that cannot or need not cross organizational boundaries.

For example:

```text
239.192.10.0/24  Market Risk Data
239.192.20.0/24  Internal Monitoring
239.192.30.0/24  Backtesting Feeds
```

This is only an address-planning example; the addresses do not automatically isolate services. Actual isolation still depends on VRFs, boundaries, ACLs, and multicast control-plane configuration.

---

## 10. Address Scope, TTL, and Routing Boundary

These three concepts are often confused.

### 10.1 TTL

TTL indicates how many more Layer 3 forwarding hops an IPv4 packet can traverse.

```text
TTL = 4
```

TTL normally decreases by one at each routed hop. A Layer 2 switch does not decrease the IPv4 TTL during ordinary Layer 2 forwarding.

---

### 10.2 Address Scope

Address scope describes the propagation range for which an address block is designed by its protocol semantics.

For example:

```text
224.0.0.0/24
```

is link-local control traffic and cannot be forwarded by a router off the current link.

---

### 10.3 Administrative Boundary

An administrative boundary is an actual forwarding boundary configured by a network administrator.

For example:

```text
239.192.0.0/14
```

is intended for internal organizational use, but a boundary must be configured at the organization's edge to prevent further forwarding.

---

### 10.4 Differences Between the Three

| Concept | Question It Answers |
|---|---|
| TTL | How many more Layer 3 hops can the packet traverse? |
| Address Scope | What propagation range does the standard define for this address? |
| Administrative Boundary | At which actual interface or domain does the network block the traffic? |

Do not use TTL as a substitute for an address boundary, and do not assume that filtering policies are unnecessary after selecting `239/8`.

---

## 11. Configuring the SSM Address Range

> The following commands use Cisco IOS/IOS XE as an example. Exact syntax and default behavior depend on the platform and software version.

### 11.1 Enabling the Standard SSM Range

The standard SSM range is:

```text
232.0.0.0/8
```

On Cisco IOS/IOS XE:

```text
configure terminal
ip pim ssm default
end
```

Here, `default` means using the standard `232/8` SSM range.

Device support for `232/8` does not necessarily mean that SSM is enabled by default. Verify the actual configuration and platform documentation.

---

### 11.2 Defining a Custom SSM Range

Some legacy services or external feeds may use group addresses outside `232/8` while still requiring the SSM service model.

For example, define both of these ranges as SSM:

```text
232.0.0.0/8
239.100.0.0/16
```

Example configuration:

```text
ip access-list standard QUANT-SSM-RANGE
 permit 232.0.0.0 0.255.255.255
 permit 239.100.0.0 0.0.255.255
!
ip pim ssm range QUANT-SSM-RANGE
```

This explicitly retains standard `232/8` while adding `239.100.0.0/16`.

A custom SSM range does not make packets automatically receive faster hardware forwarding. It tells the device that:

- These groups use the SSM service model;
- Receivers should provide source-specific membership;
- The network builds `(S,G)` state;
- ASM RP source discovery is not performed for these groups.

---

### 11.3 Checks Required Before Configuration

Before expanding or changing the SSM range, confirm that:

- Receivers use IGMPv3 INCLUDE mode;
- SSM mapping is or is not required for IGMPv1/v2 receivers;
- All last-hop routers use a consistent SSM range;
- RP and MSDP policies do not conflict with the new range;
- The addresses do not overlap existing ASM services;
- The device and software version support the configuration;
- The change will not disrupt existing receivers.

Do not change the SSM range on only one intermediate router and assume that the end-to-end service will automatically be consistent.

---

## 12. Configuration and State Verification

Commands differ by platform. The following are common Cisco IOS/IOS XE checks.

### 12.1 Checking the SSM Configuration

```text
show running-config | include ip pim ssm
```

Possible output:

```text
ip pim ssm default
```

or:

```text
ip pim ssm range QUANT-SSM-RANGE
```

---

### 12.2 Checking Receiver Membership

```text
show ip igmp groups detail
```

For SSM, focus on:

- Group;
- Source;
- Interface;
- IGMP Version;
- Include Mode;
- Membership Timer.

---

### 12.3 Checking Multicast Routing State

```text
show ip mroute
```

For an SSM group, examine:

```text
(S,G)
```

and:

- Incoming Interface;
- RPF Neighbor;
- Outgoing Interface List;
- Flags;
- Packet Counter.

Seeing the group address alone does not prove that SSM is operating correctly. Confirm the specific source and correct RPF state.

---

### 12.4 Checking RPF

```text
show ip rpf <source-ip>
```

For example:

```text
show ip rpf 10.10.10.10
```

Confirm:

- RPF Interface;
- RPF Neighbor;
- Route Source;
- Route Preference;
- Whether it matches the interface on which data actually arrives.

---

### 12.5 Checking RP Information

```text
show ip pim rp mapping
```

Standard SSM services must not depend on an RP for source discovery.

However, a wildcard RP mapping covering `224/4` does not necessarily mean that SSM data traverses the RP. Make the final determination using:

- SSM range configuration;
- IGMP membership;
- `show ip mroute`;
- PIM Join type.

---

## 13. Multicast Address-Planning Principles

### 13.1 Do Not Use Protocol-Reserved Addresses for Applications

Ordinary applications must not arbitrarily use:

```text
224.0.0.0/24
```

Do not randomly select addresses from IANA Reserved blocks either.

---

### 13.2 Evaluate SSM First for Services with Known Sources

For services with fixed sources and explicit receiver subscriptions, evaluate:

```text
232.0.0.0/8
```

and standard `(S,G)` subscriptions first.

SSM simplifies source discovery and troubleshooting, but it does not replace QoS, redundancy, or application-layer recovery mechanisms.

---

### 13.3 Use a Unified Administrative Range for Internal Multicast

For internal ASM or services requiring internal scope, plan addresses consistently from administratively scoped space such as:

```text
239.192.0.0/14
```

Do not let different teams select arbitrary addresses from the entire `239/8` range.

---

### 13.4 The Address Registry Should Record the Complete Service Identifier

Recording only the group address is insufficient. Record at least:

| Field | Example |
|---|---|
| Service Name | HKEX Feed A |
| Source IP | `10.10.10.10` |
| Group IP | `232.100.1.1` |
| UDP Port | `12001` |
| Service Model | SSM |
| Receiver VLAN/VRF | `MARKET-DATA` |
| Scope | Data Center |
| Owner | Market Data Team |
| Redundant Feed | Feed B |
| Recovery Method | TCP Retransmission |
| Status | Production |

In SSM especially, use the complete combination as the service identifier:

```text
Source + Group + UDP Port
```

---

### 13.5 An Address Range Is Not a Security Policy

Whether using:

```text
232/8
```

or:

```text
239/8
```

also use:

- Source ACLs;
- Group ACLs;
- Multicast boundaries;
- VRFs;
- Firewall policies;
- Control-plane protection;
- Receiver access control.

Address planning reduces conflicts and improves manageability, but it cannot provide security by itself.

---

## 14. Engineering Intuition

### 14.1 When You See `224.0.0.X`

Immediately think of:

- Local-link control traffic;
- Traffic that routers will not forward off the current link;
- Protocols such as OSPF, PIM, VRRP, or IGMP;
- Checking local interfaces, VLANs, and control-plane policies;
- Not attributing the issue directly to a remote RP or interdomain PIM.

---

### 14.2 When You See `232.X.X.X`

Immediately think of:

- The standard SSM range;
- A receiver that should explicitly identify the source;
- Expected `(S,G)` state;
- No RP requirement for source discovery;
- Checking IGMPv3, PIM Joins, and RPF;
- No guarantee of low latency or fault-free operation.

---

### 14.3 When You See `239.X.X.X`

Immediately think of:

- Administratively Scoped Multicast;
- A possible internal enterprise service;
- Checking address planning and boundary policies;
- Not assuming that public-network devices automatically block it;
- Confirming whether it is handled as ASM or as part of a custom SSM range.

---

### 14.4 When You See `233.252.0.X`

Immediately think of:

- A documentation and example address;
- An address that must not appear in real public production traffic.

---

## 15. Address-Classification Exercises

Identify the primary meaning of each address.

### 15.1 `224.0.0.13`

```text
Local Network Control Block
All PIM Routers
Link-local protocol control traffic
```

### 15.2 `224.0.1.1`

```text
Internetwork Control Block
Historically assigned to NTP multicast
May be routed when the network permits
```

### 15.3 `232.10.20.30`

```text
Standard IPv4 SSM address
Receiver should identify the source
Expected state: (S,G)
```

### 15.4 `233.252.0.10`

```text
MCAST-TEST-NET
Suitable for documentation and examples
Not for public production traffic
```

### 15.5 `239.192.10.10`

```text
Administratively Scoped
Inside Organization Local Scope
Requires an explicitly designed administrative boundary
```

---

## 16. Chapter Summary

1. IPv4 multicast uses `224.0.0.0/4`.
2. The four most significant bits of every IPv4 multicast address are fixed at `1110`.
3. A multicast address can be a destination IP but not a source IP.
4. A multicast address represents a logical group, not a specific interface.
5. In SSM, source and group jointly identify a channel: `(S,G)`.
6. `224.0.0.0/24` carries local-link control traffic and is not forwarded off the local link by routers.
7. The link-local restriction of `224.0.0.0/24` must not simply be equated with TTL 1.
8. `224.0.1.0/24` carries protocol control traffic that may cross Layer 3 networks.
9. `232.0.0.0/8` is the standard IPv4 SSM address space.
10. SSM requires a receiver to explicitly subscribe to `(S,G)`; the address prefix does not automatically build a forwarding tree.
11. SSM does not use an RP for source discovery but still depends on IGMP, PIM, RPF, and unicast routing.
12. SSM simplifies the control plane but does not guarantee minimum latency, lossless delivery, or an optimal physical path.
13. `239.0.0.0/8` is administratively scoped address space.
14. Administratively scoped traffic requires explicit network boundaries and is not automatically blocked by every router.
15. `239.255.0.0/16` is IPv4 Local Scope, and `239.192.0.0/14` is Organization Local Scope.
16. `233.252.0.0/24` is intended for multicast documentation and examples.
17. Production address planning should record the complete source, group, UDP port, scope, VRF, and service owner.
18. Address planning does not replace ACLs, VRFs, multicast boundaries, or firewall policies.

---

## 17. References

- RFC 1112 — Host Extensions for IP Multicasting
- RFC 2365 — Administratively Scoped IP Multicast
- RFC 4607 — Source-Specific Multicast for IP
- RFC 5771 — IANA Guidelines for IPv4 Multicast Address Assignments
- IANA — IPv4 Multicast Address Space
- Cisco IOS IP Multicast Command Reference — `ip pim ssm`
