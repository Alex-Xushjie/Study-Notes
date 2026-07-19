---
status: cn-draft
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

## 1. 本章目标

本章学习 IGMP Version 1 的基础机制，包括：

- IGMP 解决什么问题；
- Receiver Host 与直连 Multicast Router 的角色；
- Membership Query 与 Membership Report；
- Receiver 加组流程；
- Random Report Delay；
- Report Suppression；
- IGMPv1 Host State Machine；
- IGMPv1 的离组机制；
- IGMPv1 的限制。

本章只讨论 Host 与 Router 之间的三层成员关系。

IGMP Snooping 将在第 05 章中单独、详细研究。

---

## 2. IGMP 解决什么问题

Multicast Router 需要知道：

> 在某个直连网段中，是否至少存在一个 Receiver 希望接收 Group G 的流量？

例如：

```text
                    Multicast Router
                           │
                     Receiver LAN
                 ┌─────────┼─────────┐
                 │         │         │
              Host A    Host B    Host C
```

假设远端 Source 正在向以下 Group 发送数据：

```text
239.1.1.1
```

Router 必须判断：

```text
Should traffic for 239.1.1.1
be forwarded onto this LAN?
```

IGMP 用于在以下设备之间传递 Group Membership：

```text
Receiver Host
      ↕
Directly Connected Multicast Router
```

IGMPv1 的目标不是让 Router 精确记录所有 Receiver，而是确认：

```text
At least one member exists for Group G
on this directly connected network.
```

---

## 3. IGMP 的职责边界

IGMP 只负责本地网段上的 Receiver Membership。

它不负责：

- 在 Router 之间建立组播分发树；
- 发现远端 Source；
- 选择 RP；
- 执行 RPF Check；
- 传输应用数据；
- 提供重传和顺序保证；
- 直接决定交换机的二层转发端口。

可以将职责划分为：

```text
Host Membership on a Local Subnet
                ↓
               IGMP

Multicast Forwarding Between Routers
                ↓
         Multicast Routing Protocol
```

---

## 4. Source 与 Receiver 是独立角色

Source 可以向 Group 发送流量，而不需要加入该 Group。

例如：

```text
Source IP:      10.1.1.10
Destination IP: 239.1.1.1
```

Source 只负责发送数据。

Receiver 才需要通过 IGMP 表达接收需求。

因此：

> Sending traffic to a group and joining the group as a receiver are two independent operations.

---

## 5. IGMPv1 的参与者

### 5.1 Receiver Host

应用通过 Socket API 请求操作系统：

```text
Join Group G on Interface I
```

例如：

```text
Join 239.1.1.1 on ens3
```

操作系统随后负责：

- 在指定接口上维护 Group Membership；
- 发送 Membership Report；
- 接收 Membership Query；
- 运行 Report Delay Timer；
- 执行 Report Suppression；
- 在本地最后一个应用离组后删除 Membership。

Host 端的基本状态粒度是：

```text
Interface + Group
```

---

### 5.2 Multicast Router

Multicast Router 在直连网段上：

- 周期性发送 Membership Query；
- 接收 Membership Report；
- 维护本地 Group Membership State；
- 判断是否继续向该网段转发某个 Group 的流量。

Router 主要维护：

```text
Interface + Group
```

例如：

```text
Ethernet0/1 + 239.1.1.1
Membership: Present
```

IGMPv1 通常不会让 Router 获得完整的 Receiver List。

---

### 5.3 Layer 2 Switch

在原始 IGMP 模型中，普通二层交换机不是 IGMP Host，也不是 Multicast Router。

启用 IGMP Snooping 后，交换机会监听 Query 和 Report，并据此优化二层组播转发。

但是：

> IGMP Snooping is a Layer 2 optimization that observes IGMP messages. It is not the original host-to-router IGMP protocol itself.

---

## 6. IGMPv1 报文封装

IGMP 直接封装在 IPv4 中：

```text
Ethernet
   ↓
IPv4
   ↓
IGMP
```

它不使用 TCP 或 UDP。

IPv4 Header 中：

```text
Protocol = 2
TTL      = 1
```

因此，IGMP 报文只在当前三层网段内使用。

---

## 7. IGMPv1 报文格式

IGMPv1 报文长度为：

```text
8 bytes
```

格式如下：

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
| Version | 4 bits | IGMPv1 中为 `1` |
| Type | 4 bits | Message Type |
| Unused | 8 bits | 发送时置 0 |
| Checksum | 16 bits | IGMP Message Checksum |
| Group Address | 32 bits | Query 中为 `0.0.0.0`，Report 中为 Group |

---

## 8. IGMPv1 的两种报文

IGMPv1 只有两种核心报文：

| First Byte | Message |
|---:|---|
| `0x11` | Membership Query |
| `0x12` | Membership Report |

其中：

```text
0x11 = Version 1 + Type 1
0x12 = Version 1 + Type 2
```

现代抓包工具通常直接显示整个第一个字节的值。

---

## 9. Membership Query

### 9.1 作用

Multicast Router 周期性发送 Membership Query，用于确认当前网段中哪些 Group 仍然存在 Receiver。

IGMPv1 只有：

```text
General Query
```

它没有：

- Group-Specific Query；
- Group-and-Source-Specific Query。

### 9.2 典型字段

```text
IPv4 Source:      Router interface address
IPv4 Destination: 224.0.0.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x11
Unused:           0
Group Address:    0.0.0.0
```

目的地址：

```text
224.0.0.1
```

表示：

```text
All Systems on This Subnet
```

---

## 10. Membership Report

### 10.1 作用

Receiver Host 使用 Membership Report 表示：

> This interface is a member of Group G.

例如：

```text
IPv4 Source:      192.168.10.11
IPv4 Destination: 239.1.1.1
IPv4 Protocol:    2
IPv4 TTL:         1

IGMP Type:        0x12
Unused:           0
Group Address:    239.1.1.1
```

### 10.2 Report 为什么发送到 Group 本身

IGMPv1 Report 不发送到 Router 的单播地址。

它直接发送到所报告的 Group：

```text
Report for 239.1.1.1
        ↓
Destination IP = 239.1.1.1
```

这样，同一 LAN 中加入该 Group 的其他 Host 也能听到 Report，并执行 Report Suppression。

有效 Report 应满足：

```text
IPv4 Destination Address
          =
IGMP Group Address
```

---

## 11. Receiver 加入 Group 的流程

假设 Host A 加入：

```text
239.1.1.1
```

处理过程：

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

Host 不会等待下一次 Query，而是立即发送 Report。

这种 Report 称为：

```text
Unsolicited Membership Report
```

立即发送的原因是：

- Host 可能是该网段中的第一个 Receiver；
- Router 需要尽快知道该 Group 已经有成员；
- 等待下一次 Periodic Query 会增加首次接收延迟。

为了降低首次 Report 丢失的影响，Host 可以在短暂随机延迟后再重复发送一次或两次 Report。

---

## 12. Random Report Delay

假设同一 LAN 中有三个 Receiver：

```text
Host A
Host B
Host C
```

它们都加入：

```text
239.1.1.1
```

Router 发送 General Query 后，每台 Host 都会为该 Group 启动随机 Timer。

IGMPv1 的最大延迟为：

```text
10 seconds
```

例如：

```text
Host A timer = 2.1 seconds
Host B timer = 6.4 seconds
Host C timer = 8.7 seconds
```

随机延迟用于避免所有 Host 同时响应 Query，从而减少：

```text
Report Implosion
```

---

## 13. Report Suppression

Host A 的 Timer 最先到期：

```text
Host A timer expires after 2.1 seconds
```

Host A 发送：

```text
IGMPv1 Membership Report
Destination IP: 239.1.1.1
```

Host B 和 Host C 也会收到该 Report。

因为它们属于同一个 Group，所以停止自己的 Timer：

```text
Host B hears Report → Stop timer
Host C hears Report → Stop timer
```

完整流程：

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

这就是：

```text
Report Suppression
```

它的作用是：

- 减少重复 Report；
- 降低 Host 与 Router 的处理开销；
- 避免 Report Implosion。

---

### 13.1 抓包时的正确理解

如果只看到：

```text
192.168.10.11 → 239.1.1.1
```

不能说明：

```text
192.168.10.11 is the only receiver.
```

只能说明：

```text
192.168.10.11 won the report-delay race.
```

其他 Receiver 可能已经抑制了自己的 Report。

---

## 14. Timer 的粒度

Report Delay Timer 是：

```text
Per-Interface + Per-Group
```

例如：

```text
ens3 + 239.1.1.1 → 1.8 seconds
ens3 + 239.1.1.2 → 5.2 seconds
ens3 + 239.1.1.3 → 8.1 seconds
```

IGMPv1 的一个 Report 只报告一个 Group。

如果某个 Group 的 Timer 已经运行，又收到新的 Query，Host 保留现有 Timer，不重新随机。

---

## 15. IGMPv1 Host State Machine

IGMPv1 Host 对每个：

```text
Interface + Group
```

维护三个状态：

```text
Non-Member
Delaying Member
Idle Member
```

### Non-Member

Host 不是该 Group 的成员。

### Delaying Member

Host 已加入 Group，并且 Report Delay Timer 正在运行。

### Idle Member

Host 已加入 Group，但当前没有运行 Report Delay Timer。

这里的 `Idle` 不表示 Host 没有接收流量，只表示当前没有等待发送 Report。

### 状态转换

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

离组时：

```text
Delaying Member or Idle Member
              │
              │ Leave Group
              ▼
          Non-Member
```

---

## 16. `224.0.0.1` 的特殊处理

所有支持 IPv4 Multicast 的 Host 都属于：

```text
224.0.0.1
```

即：

```text
All Systems on This Subnet
```

但 Host 不会：

- 为 `224.0.0.1` 启动 Report Delay Timer；
- 发送 `224.0.0.1` 的 Membership Report。

因此，正常情况下不会看到：

```text
IGMPv1 Membership Report for 224.0.0.1
```

---

## 17. IGMPv1 的离组过程

### 17.1 没有 Leave Group Message

IGMPv1 没有显式 Leave 报文。

当本地最后一个应用离组时：

```text
Application leaves Group G
        ↓
Host removes local membership
        ↓
No IGMP Leave message is sent
```

Host 只是进入：

```text
Non-Member
```

### 17.2 Router 如何发现 Group 已无成员

Router 只能依靠：

```text
Periodic General Query
        ↓
No Report for Group G
        ↓
Membership State eventually expires
```

因此，最后一个 Receiver 离开后，Router 可能继续向该 LAN 转发该 Group 的流量一段时间。

### 17.3 为什么 IGMPv1 离组较慢

IGMPv1 的离组延迟来自：

```text
Silent Leave
+
Periodic General Query
+
Membership Aging
```

它没有：

- Leave Group；
- Group-Specific Query；
- Last Member Query Process。

这正是 IGMPv2 重点改进的问题。

---

## 18. IGMPv1 与 Querier

IGMPv1 没有定义标准化的 Querier Election。

因此，不能把下面的规则应用到 IGMPv1：

```text
The router with the lowest IP address becomes the Querier.
```

最低 IP 地址选举 Querier 是 IGMPv2 引入的机制。

在多 Router 的 IGMPv1 LAN 中，哪台 Router 发送 Query 可能取决于：

- Multicast Routing Protocol；
- 厂商实现；
- 设备配置；
- 其他 Router 角色。

---

## 19. IGMPv1 不支持 Source Filtering

IGMPv1 Receiver 只能表达：

```text
I want to receive Group G.
```

例如：

```text
Join 239.1.1.1
```

它不能表达：

```text
Receive Group G only from Source S1
```

也不能表达：

```text
Receive Group G from all sources except S2
```

因此，IGMPv1 不支持：

- INCLUDE Mode；
- EXCLUDE Mode；
- Source List；
- `(S,G)` Receiver Subscription。

这些能力由 IGMPv3 提供。

---

## 20. 抓包分析

### Wireshark

显示所有 IGMP：

```text
igmp
```

只显示 Query：

```text
igmp.type == 0x11
```

只显示 IGMPv1 Report：

```text
igmp.type == 0x12
```

查看发往 All Systems Group 的 Query：

```text
ip.dst == 224.0.0.1 and igmp.type == 0x11
```

查看某个 Group 的 Report：

```text
ip.dst == 239.1.1.1 and igmp.type == 0x12
```

### Query 检查点

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

### Report 检查点

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

## 21. 常见误解

### Source 必须加入 Group 才能发送数据

错误。发送到 Group 和加入 Group 是独立操作。

### IGMP Report 发送给 Router 的单播地址

错误。IGMPv1 Report 发送到被报告的 Group。

### 一个 Report 代表只有一个 Receiver

错误。其他 Receiver 可能因为 Report Suppression 没有发送 Report。

### Host 离组时会发送 Leave

错误。IGMPv1 没有 Leave Group Message。

### IGMPv1 使用最低 IP 地址选举 Querier

错误。IGMPv1 本身没有标准化 Querier Election。

### IGMPv1 支持 `(S,G)` 加组

错误。IGMPv1 只能表达对 Group `G` 的兴趣。

### 配置 IGMP 后，交换机一定不会泛洪组播

错误。IGMP 是 Host 与 Router 之间的三层成员协议。交换机需要 IGMP Snooping 等机制优化二层转发。

---

## 22. IGMPv1 的主要限制

1. 没有显式 Leave Group Message；
2. 没有 Group-Specific Query；
3. 没有 Last Member Query Process；
4. 没有标准化 Querier Election；
5. Maximum Report Delay 固定为 10 秒；
6. 不支持 Source Filtering；
7. Router 通常不能获得完整 Receiver List；
8. 最后一个 Receiver 离组后，流量停止较慢。

---

## 23. IGMPv1 如何引出 IGMPv2

IGMPv1 最明显的问题是：

```text
Receiver leaves silently
        ↓
Router does not know immediately
        ↓
Traffic continues until membership expires
```

IGMPv2 增加：

```text
Leave Group
Group-Specific Query
Max Response Time
Querier Election
```

下一篇笔记：

```text
04-IGMP/02-IGMPv2.md
```

将重点研究 IGMPv2 如何改进离组处理和 Querier 管理。

---

## 24. Chapter Summary

1. IGMP 用于 Receiver Host 与直连 Multicast Router 之间的成员关系管理。
2. IGMPv1 只确认某个本地网络中是否至少存在一个 Group Member。
3. IGMP 直接封装在 IPv4 中，Protocol Number 为 `2`。
4. IGMPv1 Query 和 Report 的 TTL 都是 `1`。
5. IGMPv1 只有 Membership Query 和 Membership Report。
6. Query 使用 `0x11`，发送到 `224.0.0.1`。
7. Report 使用 `0x12`，发送到被报告的 Group。
8. Host 加组时会主动发送 Unsolicited Report。
9. Random Report Delay 用于避免 Report Implosion。
10. Report Suppression 用于减少同一 Group 的重复 Report。
11. 一个 Report 不能证明该 Group 只有一个 Receiver。
12. IGMPv1 Host 状态包括 Non-Member、Delaying Member 和 Idle Member。
13. IGMPv1 没有 Leave Group Message。
14. Router 依靠 Periodic Query 和 Membership Aging 发现 Group 已无成员。
15. IGMPv1 没有标准化 Querier Election。
16. IGMPv1 不支持 Source Filtering。
17. IGMPv2 通过 Leave、Group-Specific Query 和 Querier Election 改进 IGMPv1。

---

## 25. References

- RFC 1112 — Host Extensions for IP Multicasting
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
