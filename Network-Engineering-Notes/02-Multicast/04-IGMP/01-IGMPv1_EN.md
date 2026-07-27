---
status: en-draft
title: IGMP Version 1
module: 04-IGMP
file: 01-IGMPv1
tags:
  - Multicast
  - IGMP
  - IGMPv1
  - Membership
---

# 01 - IGMPv1

## 1. Chapter Objectives

This chapter covers the fundamentals of IGMP Version 1:

- The problem IGMP solves;
- The roles of receiver hosts and directly connected multicast routers;
- Membership Queries and Membership Reports;
- The receiver join process;
- Random Report Delay and Report Suppression;
- The IGMPv1 host state machine and leave mechanism;
- IGMPv1 limitations.

This chapter discusses only Layer 3 membership between hosts and routers. IGMP Snooping is covered separately in Chapter 05.

---

## 2. What Problem Does IGMP Solve?

A multicast router needs to know:

> Does at least one receiver on a directly connected network want traffic for Group G?

```text
                    Multicast Router
                           │
                     Receiver LAN
                 ┌─────────┼─────────┐
                 │         │         │
              Host A    Host B    Host C
```

Assume a remote source sends to:

```text
239.1.1.1
```

The router must decide:

```text
Should traffic for 239.1.1.1
be forwarded onto this LAN?
```

IGMP communicates group membership between:

```text
Receiver Host
      ↕
Directly Connected Multicast Router
```

IGMPv1 does not aim to give the router an exact receiver list. It confirms:

```text
At least one member exists for Group G
on this directly connected network.
```

---

## 3. Scope of IGMP Responsibilities

IGMP manages receiver membership only on the local subnet. It does not:

- Build multicast distribution trees between routers;
- Discover remote sources or select an RP;
- Perform RPF checks;
- Carry application data;
- Provide retransmission or ordering guarantees;
- Directly determine a switch's Layer 2 forwarding ports.

```text
Host Membership on a Local Subnet
                ↓
               IGMP

Multicast Forwarding Between Routers
                ↓
         Multicast Routing Protocol
```

---

## 4. Source and Receiver Are Independent Roles

A source can send traffic to a group without joining it:

```text
Source IP:      10.1.1.10
Destination IP: 239.1.1.1
```

The source sends data; the receiver expresses demand through IGMP.

> Sending traffic to a group and joining the group as a receiver are two independent operations.

---

## 5. IGMPv1 Participants

### 5.1 Receiver Host

An application asks the operating system through the Socket API to:

```text
Join Group G on Interface I
```

For example:

```text
Join 239.1.1.1 on ens3
```

The operating system then:

- Maintains group membership on the specified interface;
- Sends Membership Reports and receives Membership Queries;
- Runs the Report Delay Timer and performs Report Suppression;
- Removes membership after the last local application leaves.

The basic host-side state is:

```text
Interface + Group
```

### 5.2 Multicast Router

On a directly connected subnet, a multicast router:

- Periodically sends Membership Queries;
- Receives Membership Reports;
- Maintains local group-membership state;
- Decides whether to continue forwarding a group's traffic onto the subnet.

Its primary state is:

```text
Interface + Group
```

For example:

```text
Ethernet0/1 + 239.1.1.1
Membership: Present
```

IGMPv1 normally does not give the router a complete receiver list.

### 5.3 Layer 2 Switch

In the original IGMP model, an ordinary Layer 2 switch is neither an IGMP host nor a multicast router.

With IGMP Snooping enabled, a switch observes Queries and Reports to optimize Layer 2 multicast forwarding.

> IGMP Snooping is a Layer 2 optimization that observes IGMP messages. It is not the original host-to-router IGMP protocol itself.

---

## 6. IGMPv1 Encapsulation

IGMP is encapsulated directly in IPv4:

```text
Ethernet
   ↓
IPv4
   ↓
IGMP
```

It does not use TCP or UDP.

```text
Protocol = 2
TTL      = 1
```

IGMP messages are therefore used only within the current Layer 3 subnet.

---

## 7. IGMPv1 Message Format

An IGMPv1 message is:

```text
8 bytes
```

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |Version| Type  |    Unused     |           Checksum            |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                         Group Address                         |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Length | Description |
|---|---:|---|
| Version | 4 bits | `1` in IGMPv1 |
| Type | 4 bits | Message Type |
| Unused | 8 bits | Set to 0 when sent |
| Checksum | 16 bits | IGMP Message Checksum |
| Group Address | 32 bits | `0.0.0.0` in a Query; the group in a Report |

---

## 8. The Two IGMPv1 Messages

| First Byte | Message |
|---:|---|
| `0x11` | Membership Query |
| `0x12` | Membership Report |

```text
0x11 = Version 1 + Type 1
0x12 = Version 1 + Type 2
```

Modern packet analyzers normally display the complete first-byte value.

---

## 9. Membership Query

### 9.1 Purpose

A multicast router periodically sends Membership Queries to determine which groups still have receivers on the subnet.

IGMPv1 has only:

```text
General Query
```

It has neither Group-Specific Queries nor Group-and-Source-Specific Queries.

### 9.2 Typical Fields

```text
IPv4 Source:      Router interface address
IPv4 Destination: 224.0.0.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Unused:           0
Group Address:    0.0.0.0
```

The destination:

```text
224.0.0.1
```

means:

```text
All Systems on This Subnet
```

---

## 10. Membership Report

### 10.1 Purpose

A receiver host uses a Membership Report to state:

> This interface is a member of Group G.

```text
IPv4 Source:      192.168.10.11
IPv4 Destination: 239.1.1.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x12
Unused:           0
Group Address:    239.1.1.1
```

### 10.2 Why Is a Report Sent to the Group Itself?

An IGMPv1 Report is not sent to the router's unicast address. It is sent directly to the reported group:

```text
Report for 239.1.1.1
        ↓
Destination IP = 239.1.1.1
```

Other hosts in the same LAN that joined the group can hear the Report and perform Report Suppression.

```text
IPv4 Destination Address
          =
IGMP Group Address
```

---

## 11. Receiver Join Process

Assume Host A joins:

```text
239.1.1.1
```

```text
Application
    │
    │ Join 239.1.1.1 on ens3
    ▼
Operating System
    │
    ├── Create Interface + Group Membership
    ├── Send Membership Report immediately
    └── Start a random Report Delay Timer
```

The host sends immediately rather than waiting for the next Query. This is an:

```text
Unsolicited Membership Report
```

It avoids first-reception delay when the host is the subnet's first receiver. To reduce the effect of a lost initial Report, a host may repeat it once or twice after a short random delay.

---

## 12. Random Report Delay

Assume three receivers on one LAN:

```text
Host A
Host B
Host C
```

all join:

```text
239.1.1.1
```

After a General Query, each host starts a random timer for the group. The IGMPv1 maximum delay is:

```text
10 seconds
```

For example:

```text
Host A timer = 2.1 seconds
Host B timer = 6.4 seconds
Host C timer = 8.7 seconds
```

Random delay prevents simultaneous responses and reduces:

```text
Report Implosion
```

---

## 13. Report Suppression

Host A's timer expires first:

```text
Host A timer expires after 2.1 seconds
```

It sends:

```text
IGMPv1 Membership Report
Destination IP: 239.1.1.1
```

Hosts B and C receive the Report and stop their timers:

```text
Host B hears Report → Stop timer
Host C hears Report → Stop timer
```

```text
                  General Query
Router ------------------------------------> 224.0.0.1

Host A: Timer = 2.1 s
Host B: Timer = 6.4 s
Host C: Timer = 8.7 s

                  Membership Report
Host A ------------------------------------> 239.1.1.1

Host B hears Report → Stop timer
Host C hears Report → Stop timer
```

This is:

```text
Report Suppression
```

It reduces duplicate Reports, host/router load, and Report Implosion.

### 13.1 Correct Packet-Capture Interpretation

Seeing only:

```text
192.168.10.11 → 239.1.1.1
```

does not mean:

```text
192.168.10.11 is the only receiver.
```

It means only:

```text
192.168.10.11 won the report-delay race.
```

Other receivers may have suppressed their Reports.

---

## 14. Timer Granularity

The Report Delay Timer is maintained:

```text
Per-Interface + Per-Group
```

```text
ens3 + 239.1.1.1 → 1.8 seconds
ens3 + 239.1.1.2 → 5.2 seconds
ens3 + 239.1.1.3 → 8.1 seconds
```

One IGMPv1 Report reports one group. If a new Query arrives while a group's timer is already running, the host retains the existing timer rather than choosing a new random value.

---

## 15. IGMPv1 Host State Machine

For every:

```text
Interface + Group
```

an IGMPv1 host maintains:

```text
Non-Member
Delaying Member
Idle Member
```

### Non-Member

The host is not a member of the group.

### Delaying Member

The host joined the group and its Report Delay Timer is running.

### Idle Member

The host joined the group but currently has no Report Delay Timer running. `Idle` does not mean the host is not receiving traffic.

### State Transitions

```text
Non-Member
    │
    │ Join Group
    │ Send Report + Start Timer
    ▼
Delaying Member
    │
    ├── Timer expires → Send Report
    │
    └── Hear Report for same Group → Stop Timer
    ▼
Idle Member
    │
    │ Receive Query → Start Timer
    ▼
Delaying Member
```

When leaving:

```text
Delaying Member or Idle Member
              │
              │ Leave Group
              ▼
          Non-Member
```

---

## 16. Special Handling of `224.0.0.1`

Every IPv4 multicast-capable host belongs to:

```text
224.0.0.1
```

which means:

```text
All Systems on This Subnet
```

However, a host does not start a Report Delay Timer or send a Membership Report for `224.0.0.1`.

Normally, therefore, you do not see:

```text
IGMPv1 Membership Report for 224.0.0.1
```

---

## 17. IGMPv1 Leave Process

### 17.1 No Leave Group Message

IGMPv1 has no explicit Leave message. When the last local application leaves:

```text
Application leaves Group G
        ↓
Host removes local membership
        ↓
No IGMP Leave message is sent
```

The host simply enters:

```text
Non-Member
```

### 17.2 How Does a Router Discover That a Group Has No Members?

The router can rely only on:

```text
Periodic General Query
        ↓
No Report for Group G
        ↓
Membership State eventually expires
```

After the last receiver leaves, the router may continue forwarding the group's traffic onto the LAN for some time.

### 17.3 Why Is IGMPv1 Leave Processing Slow?

The delay results from:

```text
Silent Leave
+
Periodic General Query
+
Membership Aging
```

IGMPv1 has no Leave Group, Group-Specific Query, or Last Member Query Process. IGMPv2 specifically improves this behavior.

---

## 18. IGMPv1 and the Querier

IGMPv1 does not define a standardized Querier election. The following rule does not apply:

```text
The router with the lowest IP address becomes the Querier.
```

Lowest-IP Querier election was introduced by IGMPv2.

On a multi-router IGMPv1 LAN, the Query sender may depend on:

- The multicast routing protocol;
- Vendor implementation;
- Device configuration;
- Other router roles.

---

## 19. IGMPv1 Does Not Support Source Filtering

An IGMPv1 receiver can state only:

```text
I want to receive Group G.
```

For example:

```text
Join 239.1.1.1
```

It cannot state:

```text
Receive Group G only from Source S1
```

or:

```text
Receive Group G from all sources except S2
```

IGMPv1 therefore does not support INCLUDE mode, EXCLUDE mode, source lists, or `(S,G)` receiver subscriptions. IGMPv3 provides these capabilities.

---

## 20. Packet-Capture Analysis

### Wireshark

Display all IGMP:

```text
igmp
```

Display only Queries:

```text
igmp.type == 0x11
```

Display only IGMPv1 Reports:

```text
igmp.type == 0x12
```

Display Queries sent to the All Systems group:

```text
ip.dst == 224.0.0.1 and igmp.type == 0x11
```

Display Reports for a specific group:

```text
ip.dst == 239.1.1.1 and igmp.type == 0x12
```

### Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Source | Router interface address |
| IPv4 Destination | `224.0.0.1` |
| IPv4 Protocol | `2` |
| TTL | `1` |
| IGMP Type | `0x11` |
| Unused | `0` |
| Group Address | `0.0.0.0` |
| IGMP Length | `8 bytes` |

### Report Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Source | Host interface address |
| IPv4 Destination | Reported Group |
| IPv4 Protocol | `2` |
| TTL | `1` |
| IGMP Type | `0x12` |
| Unused | `0` |
| Group Address | Reported Group |
| IGMP Length | `8 bytes` |

---

## 21. Common Misconceptions

### A Source Must Join a Group Before Sending Data

Incorrect. Sending to a group and joining it are independent operations.

### An IGMP Report Is Sent to the Router's Unicast Address

Incorrect. An IGMPv1 Report is sent to the reported group.

### One Report Means There Is Only One Receiver

Incorrect. Other receivers may have suppressed their Reports.

### A Host Sends a Leave When It Leaves a Group

Incorrect. IGMPv1 has no Leave Group message.

### IGMPv1 Elects the Lowest IP Address as Querier

Incorrect. IGMPv1 has no standardized Querier election.

### IGMPv1 Supports `(S,G)` Joins

Incorrect. IGMPv1 can express interest only in group `G`.

### Configuring IGMP Guarantees That a Switch Will Not Flood Multicast

Incorrect. IGMP is a Layer 3 host-to-router membership protocol. A switch needs a mechanism such as IGMP Snooping to optimize Layer 2 forwarding.

---

## 22. Major IGMPv1 Limitations

1. No explicit Leave Group message;
2. No Group-Specific Query;
3. No Last Member Query Process;
4. No standardized Querier election;
5. Maximum Report Delay fixed at 10 seconds;
6. No source filtering;
7. Routers normally cannot obtain a complete receiver list;
8. Traffic stops slowly after the last receiver leaves.

---

## 23. How IGMPv1 Leads to IGMPv2

The most visible IGMPv1 problem is:

```text
Receiver leaves silently
        ↓
Router does not know immediately
        ↓
Traffic continues until membership expires
```

IGMPv2 adds:

```text
Leave Group
Group-Specific Query
Max Response Time
Querier Election
```

The next note:

```text
04-IGMP/02-IGMPv2.md
```

examines how IGMPv2 improves leave processing and Querier management.

---

## 24. Chapter Summary

1. IGMP manages membership between receiver hosts and directly connected multicast routers.
2. IGMPv1 confirms only whether at least one group member exists on a local network.
3. IGMP is encapsulated directly in IPv4 with protocol number `2`.
4. IGMPv1 Queries and Reports use TTL `1`.
5. IGMPv1 has only Membership Queries and Membership Reports.
6. A Query uses `0x11` and is sent to `224.0.0.1`.
7. A Report uses `0x12` and is sent to the reported group.
8. A host sends an Unsolicited Report when joining.
9. Random Report Delay prevents Report Implosion.
10. Report Suppression reduces duplicate Reports for the same group.
11. One Report does not prove that only one receiver exists.
12. IGMPv1 host states are Non-Member, Delaying Member, and Idle Member.
13. IGMPv1 has no Leave Group message.
14. A router uses Periodic Queries and membership aging to discover that no members remain.
15. IGMPv1 has no standardized Querier election.
16. IGMPv1 does not support source filtering.
17. IGMPv2 improves IGMPv1 with Leave, Group-Specific Query, and Querier election.

---

## 25. References

- RFC 1112 — Host Extensions for IP Multicasting
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
