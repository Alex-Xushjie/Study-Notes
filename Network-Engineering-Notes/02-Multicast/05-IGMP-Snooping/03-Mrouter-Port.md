---
status: cn-draft
title: Multicast Router Port
module: 05-IGMP-Snooping
file: 03-Mrouter-Port
tags:
  - Multicast
  - IGMP Snooping
  - Mrouter Port
  - Router Port
  - Layer 2
---

# 03 - Mrouter Port

## 1. 本章目标

本章学习 IGMP Snooping 中的 Multicast Router Port，包括：

- Mrouter Port 的定义与必要性；
- 动态与静态学习方法；
- Query、Report 和组播数据在 Mrouter Port 上的转发；
- Trunk、STP、MLAG 和多交换机拓扑中的状态传播；
- 错误 Mrouter Port 对流量和安全的影响；
- Router Guard、静态配置和排障方法。

---

## 2. 什么是 Mrouter Port

Mrouter Port 是 Snooping Switch 认为通向 Multicast Router 或组播路由基础设施的二层端口。

```text
Receivers
   │
   ▼
Access Switch
   │ Mrouter Port
   ▼
Multicast Router / Querier
```

常见名称：

```text
Mrouter Port
Multicast Router Port
Router Port
Router-facing Port
```

它不是普通单播默认网关端口的同义词，而是 IGMP Snooping 的组播控制状态。

---

## 3. 为什么需要 Mrouter Port

### 3.1 Report 必须到达 Router

Receiver Report 由 Host 发给 Multicast Router。Snooping Switch 学习 Member Port 后仍必须把 Report 送到 Router-facing Direction：

```text
Receiver
   │ Report
   ▼
Switch
   │ Mrouter Port
   ▼
Last-Hop Router
```

否则 Router 无法建立三层 Membership，也不会向上游发送 PIM Join。

### 3.2 数据必须到达 Router

Router Port 可能通向其他下游网络。RFC 4541 要求普通组播数据除按 Member Table 转发外，也送往 Router Ports，使 Router 能继续路由给其他感兴趣网络。

### 3.3 Query 从 Router 进入 VLAN

Query 到达端口为交换机提供动态识别 Router-facing Direction 的依据。

---

## 4. 动态学习方法

RFC 4541 列出多种构建 Router Port List 的方式，平台可组合使用。

### 4.1 监听 IGMP Query

最常见的方法：

```text
Receive IGMP Query
Source IP != 0.0.0.0
        ↓
Learn ingress port as Mrouter Port
```

状态通常按 VLAN 维护：

```text
VLAN 10 + Ethernet1/48 + Dynamic Mrouter Timer
```

### 4.2 监听 PIM

部分平台通过监听 PIM Hello 等控制报文识别 Router Port：

```text
Destination: 224.0.0.13
Protocol:    PIM
```

是否支持、监听哪些 PIM Message，取决于平台。

### 4.3 监听 DVMRP 或 MRDISC

某些平台可通过 DVMRP、Multicast Router Discovery Advertisement/Solicitation 学习 Router Port。这些机制在现代企业网中较少见，但排障时需要知道其可能存在。

### 4.4 静态配置

管理员可以显式配置：

```text
VLAN 10
Ethernet1/48
Static Mrouter Port
```

静态方式适用于：

- 动态控制报文无法被可靠监听；
- Querier 位于特殊拓扑；
- 需要确定性转发；
- 设备互通存在厂商差异；
- 生产环境不允许 Router Port 因 Timer 老化消失。

---

## 5. Source `0.0.0.0` 的特殊情况

某些 Snooping Switch 为 STP 拓扑变化快速收敛而代理 General Query，并使用：

```text
IPv4 Source: 0.0.0.0
```

这个 Query 不表示发送端是真正的 Multicast Router。因此：

```text
Query Source = 0.0.0.0
→ Do not automatically learn ingress as a real Mrouter Port
```

否则交换机可能把普通交换机方向错误加入所有组播复制列表。

---

## 6. Mrouter Port 上的控制报文转发

### 6.1 Membership Report

Report 应从 Member-facing Direction 送往所有相关 Mrouter Ports。

### 6.2 Leave Group

IGMPv2 Leave 发往 `224.0.0.2`，必须到达 Querier/Router，才能触发 Last Member Query Process。

### 6.3 IGMPv3 Report

IGMPv3 Report 发往 `224.0.0.22`，必须送往 IGMPv3-capable Routers。

### 6.4 Query

Query 从 Mrouter Port 到达后，需要向 VLAN 内 Receiver-facing Ports 分发。不能仅向当前已有 Member Port 发送 General Query，否则尚未建立状态的新 Receiver 可能无法参与正确刷新。

---

## 7. 组播数据转发到 Mrouter Port

假设本地只有 Port 1 加入 Group：

```text
Group 239.1.1.1
Member Port: Ethernet1/1
Mrouter Port: Ethernet1/48
```

数据复制列表可能是：

```text
Ethernet1/1
Ethernet1/48
```

即使 Router 本身不是 Host Receiver，也需要看到数据，以便向其他网络转发。

这也是为什么把某个端口错误标记为 Mrouter Port 会带来显著额外流量：该端口可能收到大量 Group 的数据。

---

## 8. Dynamic Mrouter Timer

动态 Mrouter Port 不是永久状态。它由新的 Query、PIM 或其他识别报文刷新，并在 Timer 到期后删除。

```text
Control packet received
        ↓
Create / refresh Mrouter Timer
        ↓
No further control packet
        ↓
Timer expires
        ↓
Remove dynamic Mrouter Port
```

排障时检查：

- 学习来源；
- Remaining Timer；
- VLAN；
- Last Update；
- Dynamic 或 Static；
- 是否因 STP/Link Event 被清除。

---

## 9. 多交换机拓扑

```text
Router
  │
SW1
  │ Trunk
SW2
  ├── Receiver A
  └── Receiver B
```

SW1 直接连接 Router，其 Router-facing Port 是 Mrouter Port。

SW2 从 Trunk 收到 Query，因此 Trunk 也成为 SW2 的 Mrouter Port：

```text
SW2 Receiver Report
       ↓
SW2 Mrouter Port / Trunk
       ↓
SW1
       ↓
Router
```

每一台 Snooping Switch 都需要在自己的 VLAN 视角建立正确的上游方向。

---

## 10. STP 与拓扑变化

STP Blocking/Forwarding 变化会改变 Query 和 Report 的实际路径。

风险包括：

- 原 Mrouter Port 进入 Blocking；
- 新路径尚未学习为 Mrouter Port；
- Dynamic State 等待 Timer 才收敛；
- 短暂 Report 或数据丢失；
- 临时 Flood。

某些平台会在拓扑变化后发送 Proxy Query 或主动刷新 Snooping State。必须根据平台文档理解其 Source IP 和学习行为。

---

## 11. MLAG、vPC 与 Stack

双机或逻辑堆叠环境需要确认：

- Peer Link 是否被视为 Mrouter Port；
- Router 连接在一侧还是两侧；
- Snooping State 是否跨 Peer 同步；
- Orphan Port Receiver 的 Report 如何到达 Router；
- 双活链路是否产生重复复制；
- Failover 后 Mrouter State 是否立即恢复；
- 控制平面显示与 ASIC State 是否一致。

不要假设单机上正确的 Router Port 状态会自动同步到另一台设备。

---

## 12. 错误 Mrouter Port 的影响

### 12.1 False Positive

普通 Host Port 被错误标记为 Mrouter Port：

- 多个 Group 的数据被过度转发到该端口；
- 无关 NIC 带宽和 CPU 增加；
- 安全边界被削弱；
- 低延迟业务出现 Jitter。

### 12.2 False Negative

真正的 Router Port 未被学习：

- Report 无法到达 Router；
- Router Membership State 缺失；
- PIM Join 不会建立；
- 远端 Source 流量无法引入；
- 跨网段 Receiver 中断。

---

## 13. Router Guard

Router Guard 用于阻止不可信 Host Port 因发送 Query/PIM 等报文而被学习成 Mrouter Port。

适用位置：

```text
User Access Port
Server Access Port without router role
Untrusted Edge Port
```

不要在真正连接 Router、Querier 或下游 Snooping Switch 的端口上错误启用，否则会阻断合法控制平面。

Router Guard 是控制平面保护，不替代 ACL、DHCP Snooping、DAI、Port Security 或 CoPP。

---

## 14. 静态 Mrouter Port

Cisco 风格示例：

```text
configure terminal
ip igmp snooping vlan 10 mrouter interface Ethernet1/48
end
```

静态配置前确认：

- 端口确实通向组播路由器；
- VLAN 在 Trunk 上允许；
- STP 状态为 Forwarding；
- 双机拓扑中不会形成不必要的重复方向；
- 变更后检查所有 Group 的复制流量。

---

## 15. 验证命令

```text
show ip igmp snooping mrouter
show ip igmp snooping mrouter vlan 10
show ip igmp snooping querier vlan 10
show ip igmp snooping groups vlan 10
show interfaces trunk
show spanning-tree vlan 10
```

输出至少应回答：

```text
Which VLAN?
Which port?
Dynamic or static?
How was it learned?
How much timer remains?
Is the port operationally forwarding?
```

---

## 16. 抓包验证

在候选 Mrouter Port 上检查：

```text
IGMP Query
IGMPv2 Leave
IGMPv3 Report to 224.0.0.22
PIM Hello to 224.0.0.13
Multicast data for active groups
```

Wireshark：

```text
igmp or pim
```

比较 Receiver Port、Trunk 和 Router Port 的报文方向，确认学习与复制符合预期。

---

## 17. 排障流程

1. 确认 VLAN 与物理拓扑；
2. 找到真正的 Querier/Multicast Router；
3. 在每台交换机上检查 Mrouter Port；
4. 抓取 Query，确认 Source IP 与 Ingress Port；
5. 确认 Report 能沿 Mrouter Direction 到达 Router；
6. 确认 Router 建立 IGMP Membership；
7. 确认数据被复制到 Member Port 和必要的 Mrouter Port；
8. 检查 STP、Trunk、MLAG 和 Timer；
9. 检查静态配置、Router Guard 和硬件表项。

---

## 18. 常见误解

### “Mrouter Port 就是默认网关端口”

错误。它是 Snooping 识别的组播路由方向。

### “只有 Report 需要发往 Mrouter Port”

错误。组播数据也通常需要送往 Router Port。

### “收到任何 Source 的 Query 都应学习 Mrouter Port”

错误。Source `0.0.0.0` 是重要特殊情况，平台还有安全策略。

### “静态 Mrouter Port 永远优于动态学习”

错误。静态方式更确定，但拓扑变化时可能留下错误复制方向。

### “看到 Querier 就一定有正确 Mrouter Port”

错误。还要检查每台交换机、每个 VLAN 的实际学习状态。

---

## 19. Chapter Summary

1. Mrouter Port 是 Snooping Switch 通向组播路由基础设施的端口。
2. Receiver Report 必须通过 Mrouter Port 到达 Router。
3. 组播数据通常也需要复制到 Mrouter Port。
4. Query Ingress Port 是最常见的动态学习来源。
5. Source `0.0.0.0` 的 Proxy Query 不应被当作真实 Router Source。
6. 平台还可能监听 PIM、DVMRP 或 MRDISC。
7. Mrouter State 通常按 VLAN 维护并带有老化 Timer。
8. 多交换机拓扑中的每台设备都要学习自己的上游方向。
9. STP、MLAG 和 Trunk 变化会影响 Router Port 收敛。
10. False Positive 会导致过度转发，False Negative 会阻断 Membership 和数据路径。
11. Router Guard 可阻止不可信端口伪装为 Router Port。
12. 静态配置提供确定性，但必须随拓扑维护。
13. 排障要同时验证 Query、Report、Router State、数据复制和硬件表。

---

## 20. References

- RFC 4541 — Considerations for IGMP and MLD Snooping Switches
- RFC 4286 — Multicast Router Discovery
- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 9166 — A YANG Data Model for IGMP and MLD Snooping
