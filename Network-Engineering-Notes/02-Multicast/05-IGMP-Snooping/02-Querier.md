---
status: cn-draft
title: IGMP Snooping Querier
module: 05-IGMP-Snooping
file: 02-Querier
tags:
  - Multicast
  - IGMP Snooping
  - Querier
  - Timers
  - High Availability
---

# 02 - IGMP Snooping Querier

## 1. 本章目标

本章学习 Querier 与 IGMP Snooping 的关系，包括：

- 为什么 Snooping 状态需要周期性 Query；
- IGMP Querier 与 Snooping Querier 的区别；
- 没有组播路由器的纯二层 VLAN 如何维持 Membership；
- Querier Election、Version 和 Timer；
- Querier 与 Mrouter Port 的关系；
- 冗余、故障切换和常见配置错误；
- 配置验证与排障方法。

---

## 2. 为什么需要 Querier

Receiver 加组时会主动发送 Report，但动态 Membership 不能只依赖一次 Report 永久存在。

```text
Querier sends periodic General Query
               ↓
Receivers refresh Membership
               ↓
Snooping Switch refreshes Member Ports
```

如果没有 Query：

```text
No periodic Query
       ↓
No periodic Report refresh
       ↓
Dynamic Snooping entries age out
       ↓
Forwarding becomes platform-dependent
```

因此：

> IGMP Snooping 可以被动学习 Report，但稳定的动态状态通常需要 VLAN 中存在持续工作的 Querier。

---

## 3. 谁可以成为 Querier

### 3.1 Multicast Router

当 VLAN 中存在启用 IGMP 的三层接口时，Multicast Router 通常同时承担 Querier：

```text
Receiver VLAN
      │
      └── SVI / Routed Interface
              IGMP Querier
```

它终止 IGMP、维护三层 Membership，并可能通过 PIM 建立上游组播树。

### 3.2 IGMP Snooping Querier

纯二层 VLAN 可能没有启用 Multicast Routing 的三层接口，但交换机仍需要 Query 刷新 Snooping State。

Snooping Querier 可以主动生成 Query：

```text
Layer 2 VLAN
    ├── Receiver A
    ├── Receiver B
    └── Switch Snooping Querier
```

它通常只为二层 Membership Refresh 服务，不一定：

- 执行 PIM；
- 建立跨 Router 的组播树；
- 执行 RPF；
- 转发组播到其他 VLAN；
- 成为应用流量的默认网关。

---

## 4. Snooping 与 Querier 是两个独立功能

```text
IGMP Snooping
→ Listen, learn, and program Layer 2 forwarding

IGMP Querier
→ Generate Queries and maintain membership refresh
```

可能的组合：

| Snooping | Querier | 结果 |
|---:|---:|---|
| Disabled | Absent | 组播通常按普通二层规则 Flood |
| Enabled | Absent | 初始可学习，但动态状态可能老化或行为不稳定 |
| Enabled | External Router | 常见生产模式 |
| Enabled | Snooping Querier | 适合没有外部组播路由器的纯二层 VLAN |

---

## 5. General Query 如何维持状态

典型 IGMPv2 General Query：

```text
IPv4 Source:      Querier address
IPv4 Destination: 224.0.0.1
IGMP Type:        0x11
Group Address:    0.0.0.0
Max Resp Time:    10 seconds
```

Receiver 为每个 Group 启动随机响应计时器。Report 到达时，交换机刷新：

```text
VLAN + Group + Member Port + Timer
```

IGMPv3 Query 还携带 QRV 和 QQIC，Receiver 可以从 Query 获得 Querier 的 Robustness Variable 与 Query Interval 信息。

---

## 6. Querier Election

### 6.1 IGMPv1

IGMPv1 没有标准化的最低 IP Querier Election。

### 6.2 IGMPv2 与 IGMPv3

规则是：

```text
Lowest IPv4 source address wins
```

例如：

```text
Router A: 192.168.10.1
Router B: 192.168.10.2
```

Router A 成为 Querier。

当设备收到 Source IP 更低的 Query 时：

```text
Stop sending periodic Queries
Start Other Querier Present Timer
```

Non-Querier 仍然监听 Query/Report 并维护 Membership State。

---

## 7. Querier Source Address

Querier 应使用目标 VLAN 中稳定、唯一并可比较的 IPv4 Source Address。

需要确认：

- 地址属于正确 VLAN；
- 不与 Host 或其他网络设备重复；
- 多台 Querier 候选设备使用不同地址；
- 地址不会随接口状态异常漂移；
- ACL、CoPP 或安全功能不会阻止该 Source。

`0.0.0.0` 是特殊 Source。RFC 4541 讨论了交换机为拓扑快速收敛而代理 Query 的情况；Source `0.0.0.0` 不应被当作真正的 Multicast Router 来学习 Mrouter Port。

---

## 8. 关键 Timer

IGMPv2 常见默认值：

| Parameter | Default |
|---|---:|
| Robustness Variable | `2` |
| Query Interval | `125 seconds` |
| Query Response Interval | `10 seconds` |
| Group Membership Interval | `260 seconds` |
| Other Querier Present Interval | `255 seconds` |
| Last Member Query Interval | `1 second` |
| Last Member Query Count | `2` |

公式：

```text
Group Membership Interval
= Robustness Variable × Query Interval
+ Query Response Interval
```

```text
Other Querier Present Interval
= Robustness Variable × Query Interval
+ 0.5 × Query Response Interval
```

修改 Query Interval 会影响状态刷新、控制报文频率、老化时间和故障切换速度，不应只修改一项而忽略相关 Timer。

---

## 9. Query Version 的影响

Querier 发送的最低版本 Query 可能迫使 Host 进入兼容模式：

```text
IGMPv3 Host hears IGMPv2 Query
             ↓
Uses IGMPv2-compatible reporting
             ↓
Source Filter information is lost
```

SSM 环境必须确认：

```text
Querier Version = IGMPv3
Receiver Version = IGMPv3
Last-Hop Router supports IGMPv3
No unexpected downgrade
```

仅仅看到 IGMPv3 Receiver 并不能证明当前 VLAN 正按 IGMPv3 运行。

---

## 10. Querier 与 Mrouter Port

Snooping Switch 通常把非 `0.0.0.0` Source 的 Query 到达端口识别为 Mrouter Port：

```text
Query ingress port
        ↓
Dynamic Mrouter Port
```

这使交换机能够把 Receiver Report 转发到 Querier，并把需要交给组播路由基础设施的数据送往该方向。

但要注意：

- Querier 与 Mrouter 是逻辑上不同的概念；
- 某平台的内部 Snooping Querier 未必需要一个物理 Mrouter Port；
- Query 从 Trunk 到达时，Mrouter State 应按 VLAN 维护；
- 错误 Query 可能把错误端口动态标记为 Mrouter Port。

---

## 11. 纯二层 VLAN 设计

典型场景：

```text
Source and Receivers in VLAN 10
No multicast routing across VLANs
IGMP Snooping enabled
```

即使不需要跨 VLAN 路由，仍建议配置一个稳定的 Snooping Querier，以维持动态 Member Port State。

设计时明确：

- 哪台设备是 Primary Querier；
- 是否有 Backup Querier；
- Querier IP 如何分配；
- 使用 IGMPv2 还是 IGMPv3；
- Timer 是否统一；
- 设备故障后谁接管；
- Snooping Querier 是否会被误认为业务网关。

---

## 12. 高可用与故障切换

可以在同一 VLAN 中部署多个 Querier 候选者，让最低 IP 获胜：

```text
Switch A Querier IP: 192.168.10.2
Switch B Querier IP: 192.168.10.3
```

正常时 A 发送 Query；A 故障后，B 等待 Other Querier Present Timer 到期再接管。

需要评估：

- 默认约 255 秒的接管时间是否可接受；
- 平台是否提供更快的检测机制；
- 缩短 Timer 是否会增加控制平面负担；
- MLAG/vPC/Stack 场景中的 Querier 行为；
- SVI、First-Hop Redundancy 和 Snooping Querier 是否重复生成 Query。

---

## 13. 配置示例

Cisco 风格示例：

```text
configure terminal
ip igmp snooping
ip igmp snooping vlan 10
ip igmp snooping vlan 10 querier
ip igmp snooping vlan 10 querier address 192.168.10.2
end
```

部分平台还需要显式设置 Version：

```text
ip igmp snooping vlan 10 querier version 3
```

具体语法和默认状态必须查阅目标平台文档。

---

## 14. 验证方法

### 14.1 控制平面状态

```text
show ip igmp snooping querier
show ip igmp snooping querier vlan 10 detail
show ip igmp snooping vlan 10
```

确认：

- Administrative State；
- Operational State；
- Querier IP；
- Querier Version；
- Query Interval；
- Max Response Time；
- Querier Port；
- Other Querier Present Timer。

### 14.2 抓包

Wireshark：

```text
igmp.type == 0x11
```

检查：

```text
Source IP
Destination IP
IGMP Version
Group Address
Max Resp Code
QRV
QQIC
Arrival Interval
```

### 14.3 Member State

```text
show ip igmp snooping groups vlan 10
```

观察 Query 前后 Report 是否出现，以及 Member Timer 是否刷新。

---

## 15. 常见故障

### 15.1 完全没有 Query

动态状态最终老化。检查是否存在外部 Router、Snooping Querier 是否 Operational、VLAN 是否允许、控制报文是否被 ACL/CoPP 阻止。

### 15.2 两台设备都持续发送 Query

检查 Source IP 是否为 `0.0.0.0`、版本是否兼容、二层是否真正互通、Query 是否被过滤，以及设备是否实现标准 Election。

### 15.3 错误设备成为 Querier

最低 IP 地址可能来自测试设备、虚拟交换机或错误连接的 Router。应检查所有 Query Source，并使用边界策略或 Router Guard 限制非法 Querier。

### 15.4 IGMPv3 降级

抓包寻找 IGMPv1/v2 Query。旧版本 Querier 会让 Host 无法完整报告 Source List。

### 15.5 Querier 存在但 Entry 仍老化

检查 Query 是否到达 Receiver、Receiver 是否响应、Report 是否返回交换机、Timer 是否匹配，以及 Snooping 是否在目标 VLAN Operational。

---

## 16. 常见误解

### “启用 IGMP Snooping 就会自动发送 Query”

错误。Snooping 与 Querier 是独立功能。

### “没有组播路由就不需要 Querier”

错误。纯二层 Snooping 仍需要 Query 刷新动态 Membership。

### “Querier 一定是默认网关”

错误。Snooping Querier 可以只生成 IGMP Query。

### “Querier Election 选择最高 IP”

错误。IGMPv2/v3 使用最低 IPv4 Source Address。

### “看到 Query 就说明 IGMPv3 正常”

错误。还要检查 Query Version、Report Type 和 Source List。

### “Backup Querier 会立即接管”

错误。通常需要等待 Other Querier Present Timer。

---

## 17. Chapter Summary

1. Querier 周期性发送 Query，促使 Receiver 刷新 Membership。
2. Snooping 与 Querier 是独立功能。
3. 有 Multicast Router 时，Router 通常承担 Querier。
4. 纯二层 VLAN 可以使用 Snooping Querier。
5. Snooping Querier 不等于 PIM Router 或默认网关。
6. IGMPv2/v3 使用最低 IPv4 Source Address 选举 Querier。
7. Non-Querier 仍维护 Membership State。
8. Query Version 会影响 Receiver 的兼容模式和 Source Filtering。
9. Query 到达端口通常被动态学习为 Mrouter Port。
10. Source `0.0.0.0` 的特殊 Query 不应被当作真实 Router Source。
11. Query Interval、Membership Interval 和 Other Querier Present Interval 相互关联。
12. 多 Querier 候选可以提供冗余，但接管时间需要设计。
13. 排障时应同时检查 Querier 状态、Query 抓包、Receiver Report 和 Member Timer。

---

## 18. References

- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 4541 — Considerations for IGMP and MLD Snooping Switches
- RFC 9166 — A YANG Data Model for IGMP and MLD Snooping
