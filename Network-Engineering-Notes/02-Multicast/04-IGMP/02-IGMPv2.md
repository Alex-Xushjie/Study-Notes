---
status: cn-draft
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

## 1. 本章目标

本章学习 IGMP Version 2 相比 IGMPv1 的主要改进，包括：

- Membership Query、Membership Report 和 Leave Group；
- Group-Specific Query；
- Last Member Query Process；
- Max Response Time；
- Querier Election；
- IGMPv2 的关键定时器；
- IGMPv1 与 IGMPv2 的兼容机制；
- IGMPv2 的限制，以及这些限制如何引出 IGMPv3。

本章仍然只讨论 Host 与直连 Multicast Router 之间的三层 Membership。

以下内容将在后续章节中展开：

- `03-IGMPv3.md`：Source Filtering、INCLUDE 和 EXCLUDE；
- `04-IGMP-Troubleshooting.md`：完整的 IGMP 排障流程；
- 第 05 章：IGMP Snooping、Router Port 和 Member Port；
- 后续 PIM 章节：Router 之间如何建立组播分发树。

---

## 2. 为什么需要 IGMPv2

IGMPv1 最大的问题是 Receiver 离组时不会发送任何报文：

```text
Receiver leaves silently
        ↓
Router does not know immediately
        ↓
Traffic continues until membership expires
```

IGMPv1 没有：

- Leave Group；
- Group-Specific Query；
- Last Member Query Process；
- 标准化 Querier Election。

因此，最后一个 Receiver 离开后，Router 只能等待周期性 Query 和 Membership Aging。

IGMPv2 通过以下机制改善这一问题：

```text
Leave Group
Group-Specific Query
Last Member Query Process
Max Response Time
Querier Election
```

---

## 3. IGMPv1 与 IGMPv2 的核心差异

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

IGMPv2 仍然只能表达：

```text
Join Group G
```

它不能表达：

```text
Join (S,G)
```

Source Filtering 是 IGMPv3 的能力。

---

## 4. IGMPv2 报文封装

IGMPv2 直接封装在 IPv4 中：

```text
Ethernet
   ↓
IPv4
   ↓
IGMP
```

IPv4 Header 中：

```text
Protocol = 2
TTL      = 1
```

因此，IGMPv2 报文只在当前三层网段内使用。

IGMPv2 报文应携带 IPv4 Router Alert Option，用于提醒 Router 对该报文进行控制面处理。

---

## 5. IGMPv2 报文格式

IGMPv2 Query、Report 和 Leave 的 IGMP Header 都是：

```text
8 bytes
```

格式如下：

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
| Max Resp Time | 8 bits | Receiver 最长响应时间，单位为 0.1 秒 |
| Checksum | 16 bits | IGMP Message Checksum |
| Group Address | 32 bits | 根据报文类型表示目标 Group |

对于 Report 和 Leave，Max Resp Time 字段发送时置 0，接收时忽略。

---

## 6. IGMPv2 Message Types

| Type | Message |
|---:|---|
| `0x11` | Membership Query |
| `0x12` | IGMPv1 Membership Report |
| `0x16` | IGMPv2 Membership Report |
| `0x17` | Leave Group |

IGMPv2 Router 仍然需要识别 `0x12`，以兼容 IGMPv1 Host。

---

## 7. Membership Query

IGMPv2 定义两种 Query：

```text
General Query
Group-Specific Query
```

### 7.1 General Query

General Query 用于询问：

> 当前接口上，哪些 Group 仍然存在 Receiver？

典型字段：

```text
IPv4 Source:      Querier interface address
IPv4 Destination: 224.0.0.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Max Resp Time:    100
Group Address:    0.0.0.0
```

其中：

```text
Max Resp Time = 100
```

表示：

```text
100 × 0.1 second = 10 seconds
```

Receiver 在 0 到 10 秒之间选择随机响应延迟。

### 7.2 Group-Specific Query

Group-Specific Query 用于询问：

> 当前接口上，是否还有 Receiver 需要 Group G？

例如：

```text
Group G = 239.1.1.1
```

典型字段：

```text
IPv4 Source:      Querier interface address
IPv4 Destination: 239.1.1.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Max Resp Time:    10
Group Address:    239.1.1.1
```

这里：

```text
Max Resp Time = 10
```

表示：

```text
1 second
```

Group-Specific Query 只针对一个 Group，不会让其他 Group 的 Receiver 启动 Timer。

### 7.3 两种 Query 的区别

| Field | General Query | Group-Specific Query |
|---|---|---|
| IPv4 Destination | `224.0.0.1` | Group G |
| Group Address | `0.0.0.0` | Group G |
| Scope | 所有 Group | 一个特定 Group |
| Typical Use | 周期性刷新 Membership | Leave 后确认是否还有成员 |

---

## 8. Max Response Time

IGMPv2 将 IGMPv1 中未使用的第二个字节重新定义为：

```text
Max Response Time
```

单位为：

```text
0.1 second
```

例如：

```text
100 = 10 seconds
10  = 1 second
```

Receiver 在以下范围中随机选择 Timer：

```text
0 ≤ Delay ≤ Max Response Time
```

这让 Router 可以根据场景控制响应速度：

```text
General Query
→ Longer response window

Group-Specific Query
→ Shorter response window
```

---

## 9. IGMPv2 Membership Report

IGMPv2 Membership Report 的 Type 为：

```text
0x16
```

典型字段：

```text
IPv4 Source:      Host interface address
IPv4 Destination: Group G
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x16
Max Resp Time:    0
Group Address:    Group G
```

例如：

```text
IPv4 Source:      192.168.10.11
IPv4 Destination: 239.1.1.1
IGMP Group:       239.1.1.1
```

有效 Report 应满足：

```text
IPv4 Destination == IGMP Group Address
```

Report 发送到 Group 本身，使同一 LAN 中其他成员可以执行 Report Suppression。

---

## 10. Receiver 加组流程

当应用加入：

```text
239.1.1.1
```

Host 执行：

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

Host 不等待 Periodic Query，而是立即发送 `0x16` Report。

为了降低首次 Report 丢失的影响，Host 通常还会在短暂随机延迟后重复发送 Report。

---

## 11. Random Report Delay 与 Report Suppression

IGMPv2 继续使用 IGMPv1 的基本机制：

```text
Random Report Delay
+
Report Suppression
```

假设三个 Host 都加入：

```text
239.1.1.1
```

收到 General Query 后：

```text
Host A timer = 1.8 seconds
Host B timer = 5.4 seconds
Host C timer = 8.2 seconds
```

Host A 最先发送 Report 后，Host B 和 Host C 停止自己的 Timer。

在兼容环境中，以下两种 Report 都可以触发同一 Group 的 Suppression：

```text
IGMPv1 Report  Type 0x12
IGMPv2 Report  Type 0x16
```

因此，一个抓包中只出现一台 Host 的 Report，不代表该 Group 只有一台 Receiver。

---

## 12. Leave Group

### 12.1 报文格式

IGMPv2 新增 Leave Group：

```text
Type = 0x17
```

典型字段：

```text
IPv4 Source:      Host interface address
IPv4 Destination: 224.0.0.2
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x17
Max Resp Time:    0
Group Address:    Group G
```

目的地址：

```text
224.0.0.2
```

表示：

```text
All Routers on This Subnet
```

### 12.2 Host 什么时候发送 Leave

Host 通常只有在以下条件同时满足时才发送 Leave：

1. 本地最后一个应用离开该 Group；
2. Host 认为自己是该 Group 的 Last Reporter。

---

## 13. Last Reporter

Host 为每个：

```text
Interface + Group
```

维护一个逻辑标志：

```text
Last Reporter
```

当 Host 自己发送 Report 时：

```text
Last Reporter = True
```

当 Host 听到另一台 Host 对同一 Group 发送 Report 时：

```text
Last Reporter = False
```

离组时：

```text
If Last Reporter = True
    Send Leave

If Last Reporter = False
    Do not send Leave
```

需要特别注意：

> Last Reporter 表示最近观察到的 Report 由本机发送，不表示本机一定是最后一个 Receiver。

因此，Router 收到 Leave 后不能立即停止流量。

---

## 14. Last Member Query Process

假设 Host A 是 `239.1.1.1` 的 Last Reporter。

Host A 离组时：

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

如果还有其他 Receiver，它们会发送 Membership Report。

```text
Remaining Host
      │
      │ Membership Report
      ▼
Querier keeps Group State
```

如果 Last Member Query Process 结束前没有收到 Report，Querier 删除该 Group Membership State。

### 14.1 默认参数

```text
Last Member Query Interval = 1 second
Last Member Query Count    = 2
```

因此默认 Last Member Query Time 为：

```text
1 second × 2 = 2 seconds
```

这比等待普通 Group Membership Interval 快得多。

---

## 15. IGMPv2 Querier Election

### 15.1 为什么需要选举

同一个 LAN 可能连接多个 Multicast Router：

```text
Router A ─┐
          ├── Receiver LAN
Router B ─┘
```

IGMPv2 定义标准化 Querier Election，避免所有 Router 长期发送 Query。

### 15.2 Lowest IP Address Wins

规则是：

```text
Lowest interface IPv4 address wins
```

例如：

```text
Router A = 192.168.10.1
Router B = 192.168.10.2
```

则 Router A 成为 Querier。

### 15.3 选举过程

每台 Router 初始都认为自己是 Querier。

当 Router 收到 Source IP 更低的 Query 时：

```text
Stop acting as Querier
Start Other Querier Present Timer
```

如果收到 Source IP 更高的 Query，则继续作为 Querier。

Non-Querier 仍然：

- 监听 Query 和 Report；
- 维护 Membership State；
- 监控当前 Querier；
- 在 Querier 消失后重新参与选举。

---

## 16. Other Querier Present Timer

默认公式：

```text
Other Querier Present Interval
=
Robustness Variable × Query Interval
+
0.5 × Query Response Interval
```

使用默认值：

```text
Robustness Variable     = 2
Query Interval          = 125 seconds
Query Response Interval = 10 seconds
```

计算：

```text
2 × 125 + 0.5 × 10
= 255 seconds
```

如果在 255 秒内没有再收到更低 IP Router 的 Query，Non-Querier 会重新成为 Querier。

---

## 17. IGMPv2 关键定时器

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

默认：

```text
2 × 125 + 10 = 260 seconds
```

### 17.2 Startup Query

Querier 启动时会更快发送 Query：

```text
Startup Query Interval = Query Interval / 4
                       = 31.25 seconds

Startup Query Count = Robustness Variable
                    = 2
```

实际设备可能允许修改这些参数，排障时应检查运行值而不是只依赖默认值。

---

## 18. IGMPv1 与 IGMPv2 兼容

### 18.1 IGMPv2 Host 遇到 IGMPv1 Router

IGMPv1 和 IGMPv2 Query 都使用：

```text
Type = 0x11
```

IGMPv1 Query 的第二个字节为 0。

IGMPv2 Host 收到：

```text
Type = 0x11
Max Response Time = 0
```

时，会认为当前网络存在 IGMPv1 Querier。

在 Older Version Querier Present Timer 有效期间，Host：

- 使用 IGMPv1 Report `0x12`；
- 不发送 IGMPv2 Leave `0x17`；
- 按 IGMPv1 方式运行。

### 18.2 IGMPv2 Router 遇到 IGMPv1 Host

当 IGMPv2 Router 收到某 Group 的 IGMPv1 Report：

```text
Type = 0x12
```

它会为该 Group 启动 Version 1 Host Present Timer。

在 Timer 有效期间，Router 对该 Group 采用兼容行为，不能依赖 IGMPv2 的快速离组流程。

### 18.3 为什么兼容会降低离组速度

如果一个 Group 中仍有 IGMPv1 Host，Router 必须保守处理，因为 IGMPv1 Host：

- 不发送 Leave；
- 不理解 IGMPv2 的快速离组语义；
- 可能仍然需要该 Group。

因此，旧版本 Host 会让相关 Group 的离组行为退化。

---

## 19. IGMPv2 仍然不支持 Source Filtering

IGMPv2 Receiver 仍然只能表达：

```text
Join Group G
```

它不能表达：

```text
Receive Group G only from Source S1
```

因此，IGMPv2 不支持：

- INCLUDE Mode；
- EXCLUDE Mode；
- Source List；
- Source-Specific Membership；
- Group-and-Source-Specific Query。

这些能力由 IGMPv3 提供。

---

## 20. 抓包分析

### 20.1 Wireshark 过滤器

```text
igmp
```

Query：

```text
igmp.type == 0x11
```

IGMPv1 Report：

```text
igmp.type == 0x12
```

IGMPv2 Report：

```text
igmp.type == 0x16
```

Leave：

```text
igmp.type == 0x17
```

Leave to All Routers：

```text
ip.dst == 224.0.0.2 and igmp.type == 0x17
```

### 20.2 General Query 检查点

| Field | Expected Value |
|---|---|
| IPv4 Source | Querier interface address |
| IPv4 Destination | `224.0.0.1` |
| IPv4 Protocol | `2` |
| TTL | `1` |
| IGMP Type | `0x11` |
| Max Resp Time | Usually `100` |
| Group Address | `0.0.0.0` |

### 20.3 Group-Specific Query 检查点

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| IGMP Type | `0x11` |
| Group Address | Group G |
| Max Resp Time | Usually based on Last Member Query Interval |

### 20.4 Report 检查点

| Field | Expected Value |
|---|---|
| IPv4 Destination | Group G |
| IGMP Type | `0x16` |
| Group Address | Group G |

### 20.5 Leave 检查点

| Field | Expected Value |
|---|---|
| IPv4 Destination | `224.0.0.2` |
| IGMP Type | `0x17` |
| Group Address | Group G |

---

## 21. 常见误解

### “收到 Leave 后 Router 会立即停止转发”

错误。Router 必须先通过 Group-Specific Query 确认是否还有其他 Receiver。

### “Last Reporter 就是最后一个 Receiver”

错误。它只表示最近一次观察到的 Report 由该 Host 发送。

### “所有 Host 离组时都会发送 Leave”

错误。通常只有本地最后一个应用离组，并且 Host 认为自己是 Last Reporter 时才发送 Leave。

### “Group-Specific Query 发送到 `224.0.0.1`”

错误。它发送到目标 Group G。

### “IGMPv2 使用最高 IP 地址成为 Querier”

错误。最低接口 IPv4 地址成为 Querier。

### “Non-Querier 不维护 Membership”

错误。Non-Querier 仍然监听 IGMP 并维护状态，只是不周期性发送 General Query。

### “Max Response Time 的单位是秒”

错误。IGMPv2 中单位是 0.1 秒。

### “IGMPv2 支持 Source Filtering”

错误。IGMPv2 仍然只能表达 Group Membership。

### “IGMP Querier Election 就是 PIM DR Election”

错误。两者职责和选举规则不同。

---

## 22. IGMPv2 的主要限制

1. 仍然只能表达对 Group `G` 的兴趣；
2. 不支持 Source Filtering；
3. 不支持 INCLUDE 和 EXCLUDE Mode；
4. 不支持 Group-and-Source-Specific Query；
5. Report Suppression 使 Router 通常仍无法获得完整 Receiver List；
6. 旧版本兼容可能让快速离组退化；
7. Router 无法通过 IGMPv2 判断 Receiver 想接收哪些 Source。

---

## 23. IGMPv2 如何引出 IGMPv3

IGMPv2 解决了：

```text
How does a receiver join or leave Group G?
```

但没有解决：

```text
Which sources inside Group G does the receiver want?
```

IGMPv3 因此增加：

```text
Source List
INCLUDE Mode
EXCLUDE Mode
Group Record
Group-and-Source-Specific Query
```

下一篇笔记：

```text
04-IGMP/03-IGMPv3.md
```

将重点研究 Receiver 如何表达 Source-Specific Membership。

---

## 24. Chapter Summary

1. IGMPv2 重点改进了 IGMPv1 的离组速度和 Querier 管理。
2. IGMPv2 定义 General Query 和 Group-Specific Query。
3. Query Type 为 `0x11`。
4. IGMPv2 Membership Report Type 为 `0x16`。
5. Leave Group Type 为 `0x17`，发送到 `224.0.0.2`。
6. Max Response Time 的单位是 0.1 秒。
7. General Query 的 Group Address 为 `0.0.0.0`。
8. Group-Specific Query 的 Destination 和 Group Address 都是 Group G。
9. Host 通常只有在自己是 Last Reporter 时才发送 Leave。
10. Last Reporter 不代表最后一个 Receiver。
11. Router 收到 Leave 后执行 Last Member Query Process。
12. 默认 Last Member Query Time 通常约为 2 秒。
13. IGMPv2 使用最低接口 IP 地址选举 Querier。
14. Non-Querier 使用 Other Querier Present Timer 监控 Querier。
15. 默认 Group Membership Interval 为 260 秒。
16. 默认 Other Querier Present Interval 为 255 秒。
17. IGMPv2 必须兼容 IGMPv1 Host 和 Router。
18. Group 中存在 IGMPv1 Host 时，快速离组能力可能退化。
19. IGMPv2 仍然不支持 Source Filtering。
20. IGMPv3 通过 INCLUDE、EXCLUDE 和 Source List 扩展 Membership。

---

## 25. References

- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 1112 — Host Extensions for IP Multicasting
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
