---
status: cn-draft
title: IGMP Snooping Mechanism
module: 05-IGMP-Snooping
file: 01-Snooping-Mechanism
tags:
  - Multicast
  - IGMP Snooping
  - Layer 2
  - Membership
  - Forwarding
---

# 01 - IGMP Snooping Mechanism

## 1. 本章目标

本章学习 IGMP Snooping 的基础机制，包括：

- 为什么普通二层交换机会 Flood 组播；
- Snooping 如何监听 IGMP Query、Report 和 Leave；
- Member Port 与 Mrouter Port 的区别；
- 二层组播状态如何建立、刷新和老化；
- IGMPv1、IGMPv2 和 IGMPv3 对 Snooping 的影响；
- 控制平面状态如何转换为硬件复制列表；
- Snooping 能解决什么，以及不能解决什么；
- 常见验证命令和排障顺序。

Querier、Mrouter Port 和 Unknown Multicast 将在后续三篇笔记中分别展开。

---

## 2. 为什么需要 IGMP Snooping

普通二层交换机根据 Destination MAC Address 查找 MAC Address Table。IPv4 组播在 Ethernet 中使用组播目的 MAC，例如：

```text
Group IP:        239.1.1.1
Destination MAC: 01:00:5e:01:01:01
```

普通单播 MAC 学习不会建立这个地址对应的 Receiver Port 列表。没有组播感知能力时，交换机通常只能 Flood：

```text
Source Port
    │
    ▼
Switch
    ├── Receiver A
    ├── Receiver B
    ├── Non-Receiver C
    └── Non-Receiver D
```

无关流量会消耗端口带宽、NIC、Host Receive Queue、Kernel Packet Processing 和监控资源。

IGMP Snooping 的目标是：

> 监听 Host 与 Router 之间的 IGMP 控制报文，学习哪些二层端口真正需要某个 Group，并建立按端口复制的组播转发表。

---

## 3. Snooping 的本质

`Snooping` 表示交换机在不作为 IGMP 协议终点的情况下检查经过的 IGMP 报文。

```text
Receiver Host
      │ IGMP Report
      ▼
Layer 2 Switch ─── Observe and learn
      │
      ▼
Multicast Router
```

经典 IGMP 的协议关系仍然是：

```text
Receiver Host ↔ Multicast Router
```

Snooping Switch 使用三层 IGMP 信息优化二层转发，是一种跨层优化，而不是新的 Membership Protocol。

---

## 4. 核心状态对象

### 4.1 VLAN 或 Bridge Domain

状态属于二层广播域。相同 Group 在不同 VLAN 中是独立对象：

```text
VLAN 10 + Group 239.1.1.1
VLAN 20 + Group 239.1.1.1
```

### 4.2 Member Port

连接 Receiver，或者下游仍存在 Receiver 的端口：

```text
VLAN 10
Group 239.1.1.1
Member Ports: Ethernet1/1, Ethernet1/3
```

### 4.3 Mrouter Port

连接 Multicast Router、Querier，或者通向组播路由基础设施的端口。详细机制见 `03-Mrouter-Port.md`。

### 4.4 Group 与 Source State

IGMPv1/v2 主要产生：

```text
VLAN + Group + Member Port
```

IGMPv3 还可能产生：

```text
VLAN + Group + Source List + Member Port
```

实际硬件使用 MAC、Group IP 或 `(S,G)` 作为 Key，取决于平台实现。

---

## 5. 控制平面学习流程

假设：

```text
Receiver A -- Ethernet1/1
Receiver B -- Ethernet1/2
Router     -- Ethernet1/48
Group      -- 239.1.1.1
```

### 5.1 Query 到达

Router 从 Ethernet1/48 发送：

```text
IPv4 Destination: 224.0.0.1
IGMP Type:        0x11
```

交换机通常会识别 Query、把 Ethernet1/48 学习为动态 Mrouter Port、向 Host-facing Ports 转发 Query，并刷新控制状态。

### 5.2 Report 到达

Receiver A 加组：

```text
Ethernet1/1 receives IGMP Report for 239.1.1.1
```

交换机建立：

```text
VLAN 10
Group 239.1.1.1
Member Port Ethernet1/1
```

Report 还必须转发到 Mrouter Port，使真正终止 IGMP 的 Router 能维护三层 Membership。

### 5.3 第二个 Receiver 加入

```text
VLAN 10
Group 239.1.1.1
Member Ports:
- Ethernet1/1
- Ethernet1/2
```

### 5.4 数据转发

硬件复制列表通常包含：

```text
Ethernet1/1
Ethernet1/2
Mrouter Port as required
```

无关 Host Port 不接收该流量。

---

## 6. 数据平面的复制模型

Snooping 不会把组播转换为多个单播，而是建立受控 Replication List：

```text
One ingress multicast frame
            │
            ▼
      Hardware lookup
            │
            ▼
Replication List
    ├── Port 1
    ├── Port 2
    └── Mrouter Port
```

应区分：

```text
Control-plane Snooping State
            ↓
Hardware Multicast Entry
            ↓
Egress Replication
```

软件显示正确不代表硬件一定已正确编程；排障时需要验证软件状态、硬件状态和实际抓包。

---

## 7. IGMP 版本的影响

### 7.1 IGMPv1

IGMPv1 没有 Leave：

```text
Host leaves silently
        ↓
No Leave message
        ↓
Snooping entry remains until aging
```

Member Port 删除较慢，并依赖 Query/Report 周期和老化计时器。Report Suppression 也可能隐藏其他 Receiver。

### 7.2 IGMPv2

IGMPv2 增加 Leave 和 Group-Specific Query：

```text
Host sends Leave
        ↓
Querier sends Group-Specific Query
        ↓
Member reports, or state expires quickly
```

交换机不能看到 Leave 就无条件删除端口，因为端口后面可能还有其他 Receiver。Fast Leave 只适用于能确认端口后面只有一个 Receiver 的场景。

### 7.3 IGMPv3

IGMPv3 Report 发往 `224.0.0.22`，可携带多个 Group Record 和 Source List。交换机需要理解六种 Record Type。

对于 SSM：

```text
INCLUDE {10.1.1.10}
Group 232.1.1.1
```

理想状态是：

```text
(10.1.1.10, 232.1.1.1) → Receiver Port
```

但平台可能只在软件中保存 Source List，硬件仍按 Group 或 Multicast MAC 转发。IGMPv3 不采用 IGMPv1/v2 的经典 Host Report Suppression，更有利于学习每个 Host/Port 的状态。

---

## 8. 状态刷新与老化

动态 Entry 可由 Report、Current-State Record、State-Change Record 和 Query/Response 周期刷新。

状态可能因以下事件删除：

- Membership Timer 到期；
- Last Member Query Process 无响应；
- Fast Leave；
- 接口 Down 或 VLAN 删除；
- STP 拓扑变化；
- 管理员清除动态状态。

没有 Querier 时，动态状态可能老化而无法被周期性重建。详见 `02-Querier.md`。

---

## 9. Report 的转发原则

Snooping Switch 不能只学习 Report 而把它吞掉：

```text
Receiver Port
      │ Report
      ▼
Snooping Switch
      │
      └── Forward toward Mrouter Port
```

Proxy Reporting 会汇总下游状态再向上游报告，属于额外功能，不应与基础 Snooping 混为一谈。

对于无法识别的 IGMP Message Type，RFC 4541 建议 Flood 到其他端口，而不是使用未知字段做错误决策。

---

## 10. 能力边界

### 10.1 Snooping 可以

- 减少无关 Host Port 上的组播；
- 建立 Group-to-Port 或 Source/Group-to-Port 状态；
- 优化 VLAN 内的二层复制；
- 降低高带宽 Feed 对无关主机的影响；
- 提供 Member Port、Mrouter Port 和 Timer 可观测性。

### 10.2 Snooping 不能

- 建立 Router 之间的 PIM Tree；
- 修复 RPF Failure 或发现远端 Source；
- 替代 RP、PIM、单播路由、ACL、VRF 或 Multicast Boundary；
- 保证 UDP 无丢包；
- 自动限制非法 Source；
- 保证 ASIC 资源永远充足；
- 在没有 Querier 时永久维持动态状态。

---

## 11. 配置与验证

以下为 Cisco 风格示例，具体语法取决于平台：

```text
configure terminal
ip igmp snooping
ip igmp snooping vlan 10
end
```

```text
show ip igmp snooping
show ip igmp snooping vlan 10
show ip igmp snooping groups vlan 10
show ip igmp snooping mrouter vlan 10
show ip igmp snooping querier vlan 10
```

不要只确认全局为 Enabled，还要确认目标 VLAN 的 Operational State。

---

## 12. 基础排障流程

1. 在 Host 与 Switch Ingress 抓包，确认 Receiver 发送 Report；
2. 确认交换机学习 `VLAN + Group + Member Port`；
3. 确认存在周期性 Query，并检查 Version、Source IP 和 Timer；
4. 确认 Mrouter Port 正确；
5. 对比软件表与 ASIC/TCAM/Replication Entry；
6. 在 Source-facing、Receiver-facing、Non-receiver-facing 和 Mrouter-facing 方向抓包。

---

## 13. 常见误解

### “启用 Snooping 后所有组播都会停止 Flood”

错误。Unknown Multicast、保留控制组、状态尚未建立、资源不足和厂商策略都可能导致 Flood。

### “Snooping Switch 就是 IGMP Querier”

错误。监听 IGMP 与主动生成 Query 是两个功能。

### “收到一个 Report 就知道具体有几个 Receiver”

错误。Report Suppression 和下游交换机聚合会隐藏 Host 数量。

### “收到 Leave 就可以立即删除端口”

错误。端口后面可能仍有其他成员。

### “控制平面显示 Group IP，ASIC 就一定按 IP 转发”

错误。硬件 Key 取决于平台实现。

### “Snooping 可以替代 PIM”

错误。Snooping 只优化本地二层域。

---

## 14. Chapter Summary

1. IGMP Snooping 通过监听 IGMP 优化 VLAN 内的二层组播复制。
2. 它不是 Host-to-Router IGMP 协议的终点。
3. Snooping State 至少关联 VLAN、Group 和 Member Port。
4. Mrouter Port 通向 Querier 或组播路由基础设施。
5. Report 用于学习 Member Port，并必须继续送往 Mrouter Port。
6. Query 帮助识别 Mrouter Port 并维持 Membership Refresh。
7. IGMPv1 离组依赖老化；IGMPv2 可使用 Leave 和 Group-Specific Query。
8. Fast Leave 只适用于单 Receiver 端口。
9. IGMPv3 可携带 Filter Mode、Group Record 和 Source List。
10. 软件保存 Source State 不代表硬件一定按 `(S,G)` 转发。
11. Snooping State 最终需要编程为硬件 Replication List。
12. 没有 Querier 时，动态状态可能老化。
13. 排障应同时验证抓包、软件状态、硬件表和数据路径。

---

## 15. References

- RFC 4541 — Considerations for IGMP and MLD Snooping Switches
- RFC 1112 — Host Extensions for IP Multicasting
- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 9166 — A YANG Data Model for IGMP and MLD Snooping
