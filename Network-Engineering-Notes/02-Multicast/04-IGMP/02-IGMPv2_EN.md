---
status: en-draft
title: IGMP Version 2
module: 04-IGMP
file: 02-IGMPv2
tags:
  - Multicast
  - IGMP
  - IGMPv2
  - Membership
  - Querier
---

# 02 - IGMPv2

## 1. Chapter Objectives

This chapter covers IGMPv2 improvements over IGMPv1:

- Membership Query, Membership Report, and Leave Group;
- Group-Specific Query and Last Member Query Process;
- Max Response Time and Querier election;
- Key IGMPv2 timers;
- IGMPv1/v2 compatibility;
- IGMPv2 limitations and how they lead to IGMPv3.

It still covers only Layer 3 membership between hosts and directly connected multicast routers. Later material covers IGMPv3 source filtering, complete IGMP troubleshooting, IGMP Snooping, and PIM distribution trees.

---

## 2. Why Is IGMPv2 Needed?

IGMPv1's main problem is silent receiver departure:

```text
Receiver leaves silently
        ↓
Router does not know immediately
        ↓
Traffic continues until membership expires
```

IGMPv1 has no Leave Group, Group-Specific Query, Last Member Query Process, or standardized Querier election. A router must wait for periodic Queries and membership aging after the last receiver leaves.

IGMPv2 adds:

```text
Leave Group
Group-Specific Query
Last Member Query Process
Max Response Time
Querier Election
```

---

## 3. Core Differences Between IGMPv1 and IGMPv2

| Capability | IGMPv1 | IGMPv2 |
|---|---:|---:|
| General Query | Yes | Yes |
| Group-Specific Query | No | Yes |
| Membership Report | Yes | Yes |
| Leave Group | No | Yes |
| Max Response Time | Fixed | Carried in Query |
| Querier Election | Not standardized | Lowest IP address |
| Fast Leave Verification | No | Yes |
| Source Filtering | No | No |

IGMPv2 can still express only:

```text
Join Group G
```

not:

```text
Join (S,G)
```

Source filtering is an IGMPv3 capability.

---

## 4. IGMPv2 Encapsulation

IGMPv2 is encapsulated directly in IPv4:

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

It is used only on the current Layer 3 subnet. IGMPv2 messages should carry the IPv4 Router Alert Option so routers process them in the control plane.

---

## 5. IGMPv2 Message Format

Query, Report, and Leave headers are:

```text
8 bytes
```

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |      Type     | Max Resp Time |           Checksum            |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                         Group Address                         |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| Field | Length | Description |
|---|---:|---|
| Type | 8 bits | IGMP Message Type |
| Max Resp Time | 8 bits | Maximum receiver response time in 0.1-second units |
| Checksum | 16 bits | IGMP Message Checksum |
| Group Address | 32 bits | Target group according to message type |

For Reports and Leaves, Max Resp Time is sent as 0 and ignored on receipt.

---

## 6. IGMPv2 Message Types

| Type | Message |
|---:|---|
| `0x11` | Membership Query |
| `0x12` | IGMPv1 Membership Report |
| `0x16` | IGMPv2 Membership Report |
| `0x17` | Leave Group |

An IGMPv2 router must recognize `0x12` for compatibility with IGMPv1 hosts.

---

## 7. Membership Query

IGMPv2 defines:

```text
General Query
Group-Specific Query
```

### 7.1 General Query

It asks which groups still have receivers on the interface.

```text
IPv4 Source:      Querier interface address
IPv4 Destination: 224.0.0.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Max Resp Time:    100
Group Address:    0.0.0.0
```

```text
Max Resp Time = 100
```

means:

```text
100 × 0.1 second = 10 seconds
```

Receivers choose a random delay from 0 through 10 seconds.

### 7.2 Group-Specific Query

It asks whether any receiver still needs Group G.

```text
Group G = 239.1.1.1
```

```text
IPv4 Source:      Querier interface address
IPv4 Destination: 239.1.1.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Max Resp Time:    10
Group Address:    239.1.1.1
```

```text
Max Resp Time = 10
```

means:

```text
1 second
```

Only receivers for that group start timers.

### 7.3 Differences Between the Queries

| Field | General Query | Group-Specific Query |
|---|---|---|
| IPv4 Destination | `224.0.0.1` | Group G |
| Group Address | `0.0.0.0` | Group G |
| Scope | All groups | One specific group |
| Typical Use | Periodic membership refresh | Check for members after a Leave |

---

## 8. Max Response Time

IGMPv2 redefines IGMPv1's unused second byte as:

```text
Max Response Time
```

in units of:

```text
0.1 second
```

```text
100 = 10 seconds
10  = 1 second
```

Receivers choose:

```text
0 ≤ Delay ≤ Max Response Time
```

```text
General Query
→ Longer response window

Group-Specific Query
→ Shorter response window
```

---

## 9. IGMPv2 Membership Report

Its Type is:

```text
0x16
```

```text
IPv4 Source:      Host interface address
IPv4 Destination: Group G
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x16
Max Resp Time:    0
Group Address:    Group G
```

For example:

```text
IPv4 Source:      192.168.10.11
IPv4 Destination: 239.1.1.1
IGMP Group:       239.1.1.1
```

```text
IPv4 Destination == IGMP Group Address
```

The Report is sent to the group itself, enabling other LAN members to perform Report Suppression.

---

## 10. Receiver Join Process

When an application joins:

```text
239.1.1.1
```

the host performs:

```text
Application
    │
    │ Join 239.1.1.1 on Interface I
    ▼
Operating System
    │
    ├── Create Interface + Group Membership
    ├── Send IGMPv2 Membership Report
    └── Start an unsolicited-report timer
```

It immediately sends a `0x16` Report rather than waiting for a Periodic Query, and normally repeats it after a short random delay to tolerate initial loss.

---

## 11. Random Report Delay and Report Suppression

IGMPv2 retains:

```text
Random Report Delay
+
Report Suppression
```

If three hosts join:

```text
239.1.1.1
```

they may choose:

```text
Host A timer = 1.8 seconds
Host B timer = 5.4 seconds
Host C timer = 8.2 seconds
```

After Host A reports, B and C stop their timers. In a compatible environment, both Report types suppress Reports for the same group:

```text
IGMPv1 Report  Type 0x12
IGMPv2 Report  Type 0x16
```

Seeing only one host Report does not mean only one receiver exists.

---

## 12. Leave Group

### 12.1 Message Format

IGMPv2 adds:

```text
Type = 0x17
```

```text
IPv4 Source:      Host interface address
IPv4 Destination: 224.0.0.2
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x17
Max Resp Time:    0
Group Address:    Group G
```

The destination:

```text
224.0.0.2
```

means:

```text
All Routers on This Subnet
```

### 12.2 When Does a Host Send a Leave?

Normally only when both conditions hold:

1. The last local application leaves the group;
2. The host believes it is the group's Last Reporter.

---

## 13. Last Reporter

A host maintains a flag for each:

```text
Interface + Group
```

called:

```text
Last Reporter
```

```text
Last Reporter = True
```

after it reports, and:

```text
Last Reporter = False
```

after hearing another host report for the same group.

```text
If Last Reporter = True
    Send Leave

If Last Reporter = False
    Do not send Leave
```

> Last Reporter means that this host sent the most recently observed Report; it does not mean that the host is necessarily the last receiver.

A router therefore cannot stop traffic immediately after a Leave.

---

## 14. Last Member Query Process

Assume Host A is Last Reporter for `239.1.1.1`:

```text
Host A
  │
  │ Leave Group for 239.1.1.1
  ▼
Querier
  │
  │ Group-Specific Query for 239.1.1.1
  ▼
Remaining Receivers
```

If another receiver exists, it reports:

```text
Remaining Host
      │
      │ Membership Report
      ▼
Querier keeps Group State
```

If no Report arrives before the process ends, the Querier removes group-membership state.

### 14.1 Default Parameters

```text
Last Member Query Interval = 1 second
Last Member Query Count    = 2
```

Thus:

```text
1 second × 2 = 2 seconds
```

which is much faster than waiting for the normal Group Membership Interval.

---

## 15. IGMPv2 Querier Election

### 15.1 Why Is Election Needed?

One LAN may have multiple multicast routers:

```text
Router A ─┐
          ├── Receiver LAN
Router B ─┘
```

IGMPv2 standardizes election so all routers do not send Queries indefinitely.

### 15.2 Lowest IP Address Wins

```text
Lowest interface IPv4 address wins
```

```text
Router A = 192.168.10.1
Router B = 192.168.10.2
```

Router A becomes Querier.

### 15.3 Election Process

Each router initially considers itself Querier. On receiving a Query from a lower source IP, it performs:

```text
Stop acting as Querier
Start Other Querier Present Timer
```

A Query from a higher source IP does not displace it. A Non-Querier still listens to IGMP, maintains membership, monitors the Querier, and participates again if the Querier disappears.

---

## 16. Other Querier Present Timer

```text
Other Querier Present Interval
=
Robustness Variable × Query Interval
+
0.5 × Query Response Interval
```

Defaults:

```text
Robustness Variable     = 2
Query Interval          = 125 seconds
Query Response Interval = 10 seconds
```

```text
2 × 125 + 0.5 × 10
= 255 seconds
```

If no further Query from a lower-IP router arrives within 255 seconds, the Non-Querier becomes Querier again.

---

## 17. Key IGMPv2 Timers

| Parameter | Default |
|---|---:|
| Robustness Variable | `2` |
| Query Interval | `125 seconds` |
| Query Response Interval | `10 seconds` |
| Group Membership Interval | `260 seconds` |
| Other Querier Present Interval | `255 seconds` |
| Startup Query Interval | `31.25 seconds` |
| Startup Query Count | `2` |
| Last Member Query Interval | `1 second` |
| Last Member Query Count | `2` |
| Last Member Query Time | `2 seconds` |

### 17.1 Group Membership Interval

```text
Group Membership Interval
=
Robustness Variable × Query Interval
+
Query Response Interval
```

```text
2 × 125 + 10 = 260 seconds
```

### 17.2 Startup Query

```text
Startup Query Interval = Query Interval / 4
                       = 31.25 seconds

Startup Query Count = Robustness Variable
                    = 2
```

Devices may allow these parameters to be changed; troubleshoot using operational values, not only defaults.

---

## 18. IGMPv1 and IGMPv2 Compatibility

### 18.1 IGMPv2 Host with an IGMPv1 Router

Both versions use:

```text
Type = 0x11
```

An IGMPv1 Query has a zero second byte. When an IGMPv2 host receives:

```text
Type = 0x11
Max Response Time = 0
```

it assumes an IGMPv1 Querier exists. While the Older Version Querier Present Timer is active, the host uses IGMPv1 Report `0x12`, sends no IGMPv2 Leave `0x17`, and operates as IGMPv1.

### 18.2 IGMPv2 Router with an IGMPv1 Host

When an IGMPv2 router receives an IGMPv1 Report for a group:

```text
Type = 0x12
```

it starts the Version 1 Host Present Timer for that group. While active, it uses compatible behavior and cannot depend on fast IGMPv2 leave processing.

### 18.3 Why Compatibility Slows Leave Processing

An IGMPv1 host sends no Leave, does not understand fast-leave semantics, and may still need the group. Its presence therefore degrades leave processing for that group.

---

## 19. IGMPv2 Still Does Not Support Source Filtering

It can express only:

```text
Join Group G
```

not:

```text
Receive Group G only from Source S1
```

It supports neither INCLUDE/EXCLUDE modes, source lists, source-specific membership, nor Group-and-Source-Specific Queries. IGMPv3 provides these capabilities.

---

## 20. Packet-Capture Analysis

### 20.1 Wireshark Filters

```text
igmp
```

Query:

```text
igmp.type == 0x11
```

IGMPv1 Report:

```text
igmp.type == 0x12
```

IGMPv2 Report:

```text
igmp.type == 0x16
```

Leave:

```text
igmp.type == 0x17
```

Leave to All Routers:

```text
ip.dst == 224.0.0.2 and igmp.type == 0x17
```

### 20.2 General Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Source | Querier interface address |
| IPv4 Destination | `224.0.0.1` |
| IPv4 Protocol | `2` |
| TTL | `1` |
| IGMP Type | `0x11` |
| Max Resp Time | Usually `100` |
| Group Address | `0.0.0.0` |

### 20.3 Group-Specific Query Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| IGMP Type | `0x11` |
| Group Address | Group G |
| Max Resp Time | Usually based on Last Member Query Interval |

### 20.4 Report Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| IGMP Type | `0x16` |
| Group Address | Group G |

### 20.5 Leave Checkpoints

| Field | Expected Value |
|---|---|
| IPv4 Destination | `224.0.0.2` |
| IGMP Type | `0x17` |
| Group Address | Group G |

---

## 21. Common Misconceptions

### “A Router Stops Forwarding Immediately After Receiving a Leave”

Incorrect. It first uses a Group-Specific Query to check for other receivers.

### “Last Reporter Means Last Receiver”

Incorrect. It means only that the host sent the most recently observed Report.

### “Every Host Sends a Leave When Leaving”

Incorrect. Normally it sends one only when the last local application leaves and the host believes it is Last Reporter.

### “A Group-Specific Query Is Sent to `224.0.0.1`”

Incorrect. It is sent to target Group G.

### “IGMPv2 Elects the Highest IP Address as Querier”

Incorrect. The lowest interface IPv4 address wins.

### “A Non-Querier Does Not Maintain Membership”

Incorrect. It still observes IGMP and maintains state; it simply does not periodically send General Queries.

### “Max Response Time Is Measured in Seconds”

Incorrect. IGMPv2 uses 0.1-second units.

### “IGMPv2 Supports Source Filtering”

Incorrect. It expresses only group membership.

### “IGMP Querier Election Is the Same as PIM DR Election”

Incorrect. Their responsibilities and election rules differ.

---

## 22. Major IGMPv2 Limitations

1. Expresses interest only in Group `G`;
2. No source filtering or INCLUDE/EXCLUDE modes;
3. No Group-and-Source-Specific Query;
4. Report Suppression normally prevents a complete receiver list;
5. Older-version compatibility can degrade fast leave;
6. A router cannot determine which sources a receiver wants.

---

## 23. How IGMPv2 Leads to IGMPv3

IGMPv2 answers:

```text
How does a receiver join or leave Group G?
```

but not:

```text
Which sources inside Group G does the receiver want?
```

IGMPv3 adds:

```text
Source List
INCLUDE Mode
EXCLUDE Mode
Group Record
Group-and-Source-Specific Query
```

The next note:

```text
04-IGMP/03-IGMPv3.md
```

examines source-specific receiver membership.

---

## 24. Chapter Summary

1. IGMPv2 improves IGMPv1 leave speed and Querier management.
2. It defines General and Group-Specific Queries.
3. Query Type is `0x11`; IGMPv2 Report is `0x16`.
4. Leave Group is `0x17` and is sent to `224.0.0.2`.
5. Max Response Time uses 0.1-second units.
6. A General Query uses Group Address `0.0.0.0`; a Group-Specific Query uses Group G as destination and Group Address.
7. A host normally sends a Leave only when it is Last Reporter; this does not mean last receiver.
8. A router performs the Last Member Query Process after a Leave, normally for about two seconds by default.
9. The lowest interface IP address becomes IGMPv2 Querier.
10. A Non-Querier monitors the Querier with the Other Querier Present Timer.
11. Default Group Membership and Other Querier Present intervals are 260 and 255 seconds.
12. IGMPv2 must remain compatible with IGMPv1 hosts and routers, which may degrade fast leave.
13. IGMPv2 does not support source filtering.
14. IGMPv3 adds INCLUDE, EXCLUDE, and source lists.

---

## 25. References

- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 1112 — Host Extensions for IP Multicasting
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
