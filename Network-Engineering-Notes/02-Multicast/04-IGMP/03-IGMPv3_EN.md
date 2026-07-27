---
status: en-draft
title: IGMP Version 3
module: 04-IGMP
file: 03-IGMPv3
tags:
  - Multicast
  - IGMP
  - IGMPv3
  - Source Filtering
  - SSM
---

# 03 - IGMPv3

## 1. Chapter Objectives

This chapter covers IGMPv3 extensions over IGMPv2: source filtering; INCLUDE/EXCLUDE modes; source lists; three Query types; Membership Reports and Group Records; Current-State and State-Change Records; SSM; multi-application aggregation; version compatibility; and packet-capture checkpoints.

It discusses only Layer 3 membership between receiver hosts and directly connected multicast routers. Chapter 05 covers IGMP Snooping handling of IGMPv3 source lists.

---

## 2. Why Is IGMPv3 Needed?

IGMPv1/v2 can state:

```text
I want to receive Group G.
```

```text
Join 239.1.1.1
```

but not:

```text
Receive Group G only from Source S1.
```

or:

```text
Receive Group G from all sources except S2.
```

One group may have multiple sources:

```text
Source A ─┐
          ├── Group 239.1.1.1
Source B ─┘
```

A receiver may need only Source A. IGMPv3 therefore adds:

```text
Source Filtering
```

The receiver reports:

```text
Filter Mode + Group + Source List
```

---

## 3. INCLUDE Mode

INCLUDE means receiving Group G traffic only from sources in the source list.

```text
Mode:   INCLUDE
Group:  232.1.1.1
Source:
- 10.1.1.10
- 10.1.1.20
```

```text
Receive:
(10.1.1.10, 232.1.1.1)
(10.1.1.20, 232.1.1.1)

Do not receive other sources for 232.1.1.1.
```

```text
INCLUDE {S1,S2} for G
```

### 3.1 Empty INCLUDE List

```text
INCLUDE {}
```

means:

```text
Receive no source for Group G.
```

It normally means the interface no longer wants the group.

---

## 4. EXCLUDE Mode

EXCLUDE means receiving Group G traffic from every source except those listed.

```text
Mode:   EXCLUDE
Group:  239.1.1.1
Source:
- 10.1.1.20
```

```text
Receive all sources for 239.1.1.1
except 10.1.1.20.
```

```text
EXCLUDE {S2} for G
```

### 4.1 Empty EXCLUDE List

```text
EXCLUDE {}
```

means:

```text
Receive Group G from all sources.
```

This is equivalent to traditional ASM group membership.

---

## 5. INCLUDE Versus EXCLUDE

| Mode | Meaning of Source List | Example |
|---|---|---|
| INCLUDE | Receive only listed sources | `INCLUDE {S1,S2}` |
| EXCLUDE | Receive all sources except those listed | `EXCLUDE {S3}` |

```text
INCLUDE {}
→ Receive nothing

EXCLUDE {}
→ Receive from all sources
```

---

## 6. IGMPv3 with ASM and SSM

### 6.1 ASM

An ASM receiver specifies a group but no source. In IGMPv3 this normally appears as:

```text
EXCLUDE {}
```

```text
Group: 239.1.1.1
Mode:  EXCLUDE
List:  Empty
```

```text
Receive 239.1.1.1 from any source.
```

### 6.2 SSM

An SSM receiver specifies:

```text
(S,G)
```

```text
Source: 10.1.1.10
Group:  232.1.1.1
```

IGMPv3 expresses this as:

```text
INCLUDE {10.1.1.10}
for Group 232.1.1.1
```

> IGMPv3 provides the standard receiver-membership mechanism for SSM.

IGMPv3 expresses source-specific interest from the receiver to the last-hop router. Building an inter-router `(S,G)` tree belongs to multicast routing.

---

## 7. IGMPv3 Encapsulation

```text
Ethernet
   ↓
IPv4
   ↓
IGMP
```

```text
Protocol = 2
TTL      = 1
```

IGMPv3 should carry:

```text
IPv4 Router Alert Option
```

Common destinations:

```text
General Query:
224.0.0.1

Group-Specific Query:
Group G

Group-and-Source-Specific Query:
Group G

IGMPv3 Membership Report:
224.0.0.22
```

---

## 8. IGMPv3 Query Format

```text
Type = 0x11
```

```text
  0                   1                   2                   3
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Type = 0x11 | Max Resp Code |           Checksum            |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                         Group Address                         |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 | Resv  |S| QRV |     QQIC      |     Number of Sources (N)     |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Source Address [1]                      |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                              ...                              |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Meaning |
|---|---|
| Type | Query, fixed at `0x11` |
| Max Resp Code | Maximum receiver response time |
| Group Address | Target group |
| S | Suppress Router-side Processing |
| QRV | Querier's Robustness Variable |
| QQIC | Querier's Query Interval Code |
| Number of Sources | Source-list count |
| Source Address List | Queried sources |

---

## 9. Max Resp Code, QRV, and QQIC

### 9.1 Max Resp Code

For values below 128:

```text
Max Response Time
=
Max Resp Code × 0.1 second
```

```text
100 → 10 seconds
```

Values of 128 or more use floating-point encoding.

### 9.2 QRV

```text
QRV = Querier's Robustness Variable
```

Default:

```text
2
```

### 9.3 QQIC

```text
QQIC = Querier's Query Interval Code
```

The default Query Interval is normally:

```text
125 seconds
```

---

## 10. The Three IGMPv3 Queries

### 10.1 General Query

Queries all group and source-filter state on an interface.

```text
IPv4 Destination: 224.0.0.1
Group Address:    0.0.0.0
Number of Sources: 0
```

### 10.2 Group-Specific Query

Checks whether receivers still want Group G.

```text
IPv4 Destination: Group G
Group Address:    Group G
Number of Sources: 0
```

### 10.3 Group-and-Source-Specific Query

Checks whether receivers still need specific sources within Group G.

```text
IPv4 Destination: Group G
Group Address:    Group G
Number of Sources: N
Source List:
- S1
- S2
```

This is a key IGMPv3 extension over IGMPv2.

---

## 11. IGMPv3 Membership Report

```text
Type = 0x22
```

IPv4 destination:

```text
224.0.0.22
```

Unlike IGMPv1/v2, the Report is not sent to the reported group, can contain multiple Group Records, and each record can contain a source list.

---

## 12. IGMPv3 Report Format

```text
  0                   1                   2                   3
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Type = 0x22 |    Reserved   |           Checksum            |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |           Reserved            |  Number of Group Records (M)  |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Group Record [1]                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                              ...                              |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Group Record [M]                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

One Report can contain multiple Group Records.

---

## 13. Group Record Format

```text
  0                   1                   2                   3
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Record Type  | Aux Data Len  |     Number of Sources (N)     |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Multicast Address                       |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Source Address [1]                      |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                              ...                              |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Meaning |
|---|---|
| Record Type | Current state or state change |
| Aux Data Len | Auxiliary Data length |
| Number of Sources | Source count |
| Multicast Address | Group G |
| Source Address List | Source list |

---

## 14. Six Group Record Types

| Value | Record Type |
|---:|---|
| `1` | MODE_IS_INCLUDE |
| `2` | MODE_IS_EXCLUDE |
| `3` | CHANGE_TO_INCLUDE_MODE |
| `4` | CHANGE_TO_EXCLUDE_MODE |
| `5` | ALLOW_NEW_SOURCES |
| `6` | BLOCK_OLD_SOURCES |

They divide into:

```text
Current-State Record
State-Change Record
```

---

## 15. Current-State Record

Used in Query responses to report current filter state.

### 15.1 MODE_IS_INCLUDE

```text
MODE_IS_INCLUDE {Source List}
```

The current state is INCLUDE.

### 15.2 MODE_IS_EXCLUDE

```text
MODE_IS_EXCLUDE {Source List}
```

The current state is EXCLUDE.

```text
MODE_IS_EXCLUDE
Group: 239.1.1.1
Sources: Empty
```

means receiving the group from all sources.

---

## 16. State-Change Record

Notifies a router that receiver filter state changed:

```text
CHANGE_TO_INCLUDE_MODE
CHANGE_TO_EXCLUDE_MODE
ALLOW_NEW_SOURCES
BLOCK_OLD_SOURCES
```

### 16.1 CHANGE_TO_INCLUDE_MODE

Changes state to:

```text
INCLUDE {Source List}
```

### 16.2 CHANGE_TO_EXCLUDE_MODE

Changes state to:

```text
EXCLUDE {Source List}
```

### 16.3 ALLOW_NEW_SOURCES

Adds desired sources:

```text
Before:
INCLUDE {S1}

After:
INCLUDE {S1,S2}
```

It can send:

```text
ALLOW_NEW_SOURCES {S2}
```

### 16.4 BLOCK_OLD_SOURCES

Stops requesting sources:

```text
Before:
INCLUDE {S1,S2}

After:
INCLUDE {S1}
```

It can send:

```text
BLOCK_OLD_SOURCES {S2}
```

---

## 17. Current-State Versus State-Change

| Category | Record Type | Typical Use |
|---|---|---|
| Current-State | MODE_IS_INCLUDE / MODE_IS_EXCLUDE | Respond to a Query |
| State-Change | CHANGE_TO_* / ALLOW_NEW_SOURCES / BLOCK_OLD_SOURCES | Join, Leave, or source-list change |

```text
MODE_IS_*
→ What is my current state?

CHANGE_TO_*
ALLOW_NEW_SOURCES
BLOCK_OLD_SOURCES
→ What has changed?
```

---

## 18. SSM Join Process

Assume an application wants:

```text
Source: 10.1.1.10
Group:  232.1.1.1
```

The host creates:

```text
INCLUDE {10.1.1.10}
for 232.1.1.1
```

and sends:

```text
Destination: 224.0.0.22
Type:        0x22

Group Record:
CHANGE_TO_INCLUDE_MODE

Group:
232.1.1.1

Source:
10.1.1.10
```

Later Query responses use:

```text
MODE_IS_INCLUDE
Group: 232.1.1.1
Source: 10.1.1.10
```

---

## 19. ASM Join Process

An application wants:

```text
239.1.1.1
```

from all sources. The host creates:

```text
EXCLUDE {}
```

and sends:

```text
CHANGE_TO_EXCLUDE_MODE
Group: 239.1.1.1
Source List: Empty
```

Later Query responses report:

```text
MODE_IS_EXCLUDE
Group: 239.1.1.1
Source List: Empty
```

---

## 20. Leaving with IGMPv3

### 20.1 Leaving an SSM Channel

Current state:

```text
INCLUDE {S1}
```

After leaving:

```text
INCLUDE {}
```

The host can send:

```text
CHANGE_TO_INCLUDE_MODE
Group: G
Source List: Empty
```

### 20.2 Leaving an ASM Group

Current state:

```text
EXCLUDE {}
```

After leaving it also becomes:

```text
INCLUDE {}
```

IGMPv3 uses Group Records to express leaving and source-list changes rather than a new standalone Leave message.

---

## 21. Multi-Application State Aggregation

Applications on one host may request different sources for the same group:

```text
Application A:
INCLUDE {S1}

Application B:
INCLUDE {S2}
```

The operating system may aggregate the interface state as:

```text
INCLUDE {S1,S2}
```

Distinguish:

```text
Per-Socket Filter State
```

from:

```text
Per-Interface Filter State
```

IGMP Reports reflect the aggregated interface state.

---

## 22. Router-Side Membership State

An IGMPv3 router maintains more than:

```text
Interface + Group
```

It maintains:

```text
Interface
+ Group
+ Filter Mode
+ Source State
```

```text
Interface: Ethernet0/1
Group:     232.1.1.1
Mode:      INCLUDE
Sources:
- 10.1.1.10
- 10.1.1.20
```

It may maintain group filter mode, group and per-source timers, source lists, and older-version host state.

---

## 23. IGMPv3 Querier Election

IGMPv3 retains the IGMPv2 rule:

```text
Lowest IPv4 address wins.
```

A Non-Querier still listens to Queries and Reports, maintains membership, and runs the Other Querier Present Timer. The IGMP Querier and PIM DR are different roles.

---

## 24. IGMPv1/v2/v3 Compatibility

An IGMPv3 host enters compatibility mode after hearing an older Query.

### 24.1 Hearing an IGMPv2 Query

The host uses:

```text
IGMPv2 Membership Report
Type = 0x16
```

and cannot fully express source-filter state.

### 24.2 Hearing an IGMPv1 Query

The host uses:

```text
IGMPv1 Membership Report
Type = 0x12
```

and likewise cannot express source filtering.

### 24.3 Router Discovers an Older Host

After receiving an older Report, an IGMPv3 router maintains Older-Version Host Present State for the group. This can degrade source filtering and fast leave, and make group behavior follow the lowest version.

For SSM, confirm:

```text
Receiver supports IGMPv3
Last-Hop Router supports IGMPv3
No version downgrade is occurring
```

---

## 25. IGMPv3 and Report Suppression

The classic IGMPv1/v2 model is:

```text
One host reports
Other hosts suppress their reports
```

In IGMPv3, hosts may have different source lists:

```text
Host A:
INCLUDE {S1}

Host B:
INCLUDE {S2}
```

One host's state cannot fully represent another's. The simple IGMPv1/v2 Suppression model therefore does not apply to every IGMPv3 Report. State-Change Reports in particular must reliably report the local host's changes.

---

## 26. Packet-Capture Analysis

### 26.1 Wireshark Filters

All IGMP:

```text
igmp
```

Queries:

```text
igmp.type == 0x11
```

IGMPv3 Reports:

```text
igmp.type == 0x22
```

Reports to the IGMPv3 Router group:

```text
ip.dst == 224.0.0.22 and igmp.type == 0x22
```

### 26.2 General Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | `224.0.0.1` |
| Protocol | `2` |
| TTL | `1` |
| Router Alert | Present |
| Type | `0x11` |
| Group Address | `0.0.0.0` |
| Number of Sources | `0` |

### 26.3 Group-Specific Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| Type | `0x11` |
| Group Address | Group G |
| Number of Sources | `0` |

### 26.4 Group-and-Source-Specific Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| Type | `0x11` |
| Group Address | Group G |
| Number of Sources | Greater than `0` |
| Source List | Target Sources |

### 26.5 IGMPv3 Report Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | `224.0.0.22` |
| Protocol | `2` |
| TTL | `1` |
| Router Alert | Present |
| Type | `0x22` |
| Number of Group Records | One or more |
| Record Type | `1` to `6` |
| Multicast Address | Group G |
| Source List | Depends on Filter State |

---

## 27. Common Misconceptions

### “IGMPv3 Simply Means Joining `(S,G)`”

Incomplete. IGMPv3 supports INCLUDE and EXCLUDE and can also express ASM membership.

### “An Empty INCLUDE List Means All Sources”

Incorrect.

```text
INCLUDE {}
→ Receive nothing
```

### “An Empty EXCLUDE List Means No Sources”

Incorrect.

```text
EXCLUDE {}
→ Receive from all sources
```

### “An IGMPv3 Report Is Sent to the Group Itself”

Incorrect. It is sent to:

```text
224.0.0.22
```

### “One IGMPv3 Report Can Report Only One Group”

Incorrect. One Report can carry multiple Group Records.

### “MODE_IS_INCLUDE Indicates a State Change”

Incorrect. It is a Current-State Record.

### “IGMPv3 Alone Can Build an Inter-Router `(S,G)` Tree”

Incorrect. IGMPv3 only expresses receiver interest.

### “An IGMPv3 Host Must Be Using SSM”

Incorrect. It can express ASM with `EXCLUDE {}`.

---

## 28. Evolution Across the Three Versions

| Version | What the Receiver Can Express |
|---|---|
| IGMPv1 | “I need Group G.” |
| IGMPv2 | “I am joining or leaving Group G.” |
| IGMPv3 | “I need or exclude specific sources within Group G.” |

```text
IGMPv1:
Group Membership

IGMPv2:
Group Membership + Faster Leave

IGMPv3:
Group Membership + Source Filtering
```

---

## 29. Chapter Summary

1. IGMPv3's core capability is source filtering.
2. Receivers express demand with filter mode, group, and source list.
3. INCLUDE receives only listed sources; EXCLUDE receives all except listed sources.
4. `INCLUDE {}` receives nothing; `EXCLUDE {}` receives all sources.
5. SSM normally uses `INCLUDE {S}`; ASM normally uses `EXCLUDE {}`.
6. IGMPv3 Query remains Type `0x11` and supports General, Group-Specific, and Group-and-Source-Specific Queries.
7. IGMPv3 Report is Type `0x22` and is sent to `224.0.0.22`.
8. One Report can contain multiple Group Records.
9. Current-State Records are MODE_IS_INCLUDE and MODE_IS_EXCLUDE.
10. State-Change Records are CHANGE_TO_INCLUDE_MODE, CHANGE_TO_EXCLUDE_MODE, ALLOW_NEW_SOURCES, and BLOCK_OLD_SOURCES.
11. Group Records express joins, leaves, and source-list changes.
12. A host aggregates multiple socket requests into interface-level filter state.
13. A router maintains group mode and source state.
14. The lowest IPv4 address remains Querier.
15. Older hosts or Queriers may degrade functionality.
16. IGMPv3 expresses receiver interest but does not build inter-router multicast trees.
17. Chapter 05 covers IGMP Snooping handling of IGMPv3 source lists.

---

## 30. References

- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 4607 — Source-Specific Multicast for IP
- RFC 2236 — Internet Group Management Protocol, Version 2
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
