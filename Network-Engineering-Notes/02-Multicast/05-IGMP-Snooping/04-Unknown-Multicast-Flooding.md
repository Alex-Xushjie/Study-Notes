---
status: cn-draft
title: Unknown Multicast Flooding
module: 05-IGMP-Snooping
file: 04-Unknown-Multicast-Flooding
tags:
  - Multicast
  - IGMP Snooping
  - Unknown Multicast
  - Flooding
  - Security
---

# 04 - Unknown Multicast Flooding

## 1. 本章目标

本章学习 Unknown Multicast 的转发行为，包括：

- Known、Unknown 与 Unregistered Multicast 的区别；
- 为什么启用 IGMP Snooping 后仍可能 Flood；
- RFC 4541 对普通组播、控制组和未知 IGMP 报文的考虑；
- Flood、Drop、Router-only Forwarding 等策略；
- 状态建立前、老化后和资源不足时的瞬态行为；
- 32:1 MAC 重叠与 Unknown Multicast 的区别；
- 生产环境中的安全、容量和排障方法。

---

## 2. 基本术语

### 2.1 Known Multicast

交换机已有匹配的 Snooping/Multicast Forwarding Entry：

```text
VLAN 10
Group 239.1.1.1
Member Ports: Ethernet1/1, Ethernet1/2
```

数据按复制列表转发。

### 2.2 Unknown Multicast

组播数据到达时，交换机没有可用于精确转发的匹配状态：

```text
Multicast frame arrives
        ↓
No matching forwarding entry
        ↓
Unknown Multicast Policy
```

### 2.3 Unregistered Multicast

许多厂商用 `Unregistered Multicast` 表示 VLAN 中没有 Receiver Membership 的 Group。不同平台可能区分：

- 完全没有 Group Entry；
- 有 Group Entry 但没有 Member Port；
- 只有 Mrouter Port；
- MAC Entry 与 IP Group Entry 不一致。

阅读命令和文档时必须确认厂商定义。

---

## 3. 为什么 Unknown Multicast 会出现

常见原因：

1. Source 在 Receiver 加组前已经开始发送；
2. Receiver 从未加入 Group；
3. Snooping Entry 已老化；
4. VLAN 中没有 Querier；
5. Report 被 ACL、Storm Control、CPU Protection 或链路故障阻断；
6. Report 到达错误 VLAN；
7. IGMP Version 或 Source Filter 不兼容；
8. STP/MLAG 切换后状态尚未恢复；
9. ASIC/TCAM/Replication Resource 不足；
10. 平台无法解析报文、Fragment 或封装；
11. 软件状态尚未下发到硬件。

---

## 4. 默认 Flood 模型

传统二层交换把未知目的流量 Flood 到同一 VLAN 的其他 Forwarding Ports。Unknown Multicast 常采用类似行为：

```text
Source → Unknown Group G
            │
            ▼
          Switch
      ├── Port 1
      ├── Port 2
      ├── Port 3
      └── Mrouter Port
```

优点：

- Receiver 在控制状态尚未建立时仍可能收到数据；
- 避免因 Snooping 学习失败造成完全黑洞；
- 兼容不发送 IGMP 的旧设备或特殊应用。

缺点：

- 高带宽流量扩散到所有端口；
- NIC、CPU 和 Kernel 处理无关报文；
- 低延迟业务出现 Jitter；
- 形成信息泄露和 DoS 风险；
- 多个 Unknown Feed 可耗尽 VLAN 带宽。

---

## 5. Drop Unknown 模型

某些平台允许丢弃没有 Membership 的组播：

```text
Unknown Group G
      ↓
Drop on host-facing ports
```

优点：

- 严格限制未订阅流量；
- 减少无关带宽与 Host 负载；
- 适合高带宽、低延迟和严格订阅环境。

风险：

- Source 先发、Receiver 后加组时，初始报文丢失；
- Querier 或 Snooping 故障会把业务变成黑洞；
- 静态 Receiver、特殊协议或不标准应用可能失效；
- 状态恢复期间产生短暂中断；
- 错误配置可能同时阻断控制流量。

启用 Drop Unknown 前必须验证完整控制平面和故障恢复路径。

---

## 6. Router-only Forwarding

部分平台可把 Unknown Multicast 仅送往 Mrouter Ports，而不 Flood 到所有 Host Ports：

```text
Unknown Multicast
      ├── Drop on non-member host ports
      └── Forward to Mrouter Ports
```

这允许 Router 继续处理或路由流量，同时保护本地无关 Host。

具体行为高度依赖平台，必须确认：

- 是否保留 Source Port；
- 是否转发到所有 Mrouter Ports；
- 是否区分 IPv4 Group 与 Multicast MAC；
- 是否对保留控制组例外；
- 硬件资源不足时是否回退到 Flood。

---

## 7. RFC 4541 的重要考虑

对于目的 IP 不属于 `224.0.0.X` 的非 IGMP 组播数据，RFC 4541 建议：

- 根据 Group-based Port Membership Table 转发；
- 同时转发到 Multicast Router Ports。

对没有 Membership State 的流量，具体 Flood/Drop 行为仍可能受到平台设计和管理策略影响。

RFC 4541 是 Informational 文档，厂商实现并不完全一致。因此：

> 不要只根据通用术语推断实际数据平面；应查阅设备文档并执行抓包验证。

---

## 8. `224.0.0.X` 控制组

Local Network Control Block：

```text
224.0.0.0/24
```

包含 OSPF、PIM、VRRP、IGMP 等本地链路控制流量。Snooping Switch 通常不能像普通应用组播一样只按 Receiver Membership 限制这些报文。

例如：

```text
224.0.0.1  All Systems
224.0.0.2  All Routers
224.0.0.13 All PIM Routers
224.0.0.22 IGMPv3 Routers
```

错误 Drop 可能破坏协议邻居、Querier、Membership 和高可用控制平面。

需要结合：

- RFC 行为；
- 平台保留组策略；
- Control-plane ACL；
- Router Guard；
- 实际协议需求。

---

## 9. 未知 IGMP Message

无法识别的 IGMP Message Type 与 Unknown Multicast Data 不是同一概念。

RFC 4541 建议 Snooping Switch 对无法识别的 IGMP 报文：

- Flood 到其他端口；
- 不越过 Network Layer Header 使用未知字段做决策。

这样可避免新版本或扩展报文被旧交换机错误阻断。

---

## 10. 状态建立前的瞬态流量

Source 和 Receiver 的启动顺序会影响初始行为。

### 10.1 Receiver 先加入

```text
Receiver Report
      ↓
Snooping Entry installed
      ↓
Source starts
      ↓
Known Multicast Forwarding
```

### 10.2 Source 先发送

```text
Source starts
      ↓
No Snooping Entry yet
      ↓
Flood or Drop Unknown
      ↓
Receiver later joins
```

金融行情等持续 UDP Feed 通常 Source 不等待 Receiver，因此必须明确初始 Unknown Policy 是否会造成无关 Flood 或首包丢失。

---

## 11. Entry 老化后的行为

```text
Member Entry exists
      ↓
No Query / No Report refresh
      ↓
Entry ages out
      ↓
Next packet becomes Unknown
```

如果策略是 Flood，症状可能是“运行一段时间后所有端口突然收到流量”。

如果策略是 Drop，症状可能是“运行一段时间后 Receiver 突然中断”。

这类问题首先检查 Querier、Timer 和 Report Path，而不是立即怀疑 Source。

---

## 12. 硬件资源不足与降级

Snooping State 最终需要使用 ASIC/TCAM/Replication Resource。资源不足时，平台可能：

- 拒绝新 Entry；
- 将新 Group 置于软件转发；
- 对超出部分 Flood；
- Drop 超出部分；
- 合并为 MAC-based Entry；
- 产生 Syslog/Trap；
- 静默降级。

容量规划应统计：

```text
Number of VLANs
Number of Groups per VLAN
Number of (S,G) states
Number of Member Ports
Replication fan-out
Reserved system entries
```

不要只检查控制平面 Snooping Table 的数量，还要检查硬件利用率。

---

## 13. 32:1 MAC 重叠不是 Unknown Multicast

两个不同 Group 可能映射到同一 MAC：

```text
232.1.1.1 → 01:00:5e:01:01:01
239.1.1.1 → 01:00:5e:01:01:01
```

如果平台按 Group IP 或 `(S,G)` 转发，两者仍可分别是 Known Multicast。

如果平台按 Multicast MAC 转发，它们可能共享复制列表并导致 Over-Forwarding。

因此应区分：

```text
Unknown Multicast
→ No usable matching forwarding state

MAC Overlap
→ Multiple IP Groups share one Ethernet MAC
```

---

## 14. 安全风险

攻击者或错误应用可以持续发送随机 Group：

```text
239.1.1.1
239.1.1.2
239.1.1.3
...
```

可能造成：

- Unknown Multicast Flood；
- VLAN 带宽耗尽；
- Host NIC/CPU 压力；
- Snooping/TCAM State Exhaustion；
- Control-plane 事件和日志风暴；
- 数据泄露到未授权端口。

防护手段包括：

- Source ACL；
- Group ACL；
- Unknown Multicast Drop；
- Storm Control；
- Rate Limit；
- Multicast Boundary；
- VLAN/VRF 隔离；
- Receiver Access Control；
- 硬件资源监控。

---

## 15. 设计决策

### 15.1 适合 Flood 的场景

- 小型、低带宽、兼容性优先的 VLAN；
- Receiver 不稳定或不能正确发送 IGMP；
- 业务允许无关端口看到流量；
- 控制平面故障时宁可过度转发也不能中断。

### 15.2 适合 Drop 的场景

- 高频 Market Data；
- 高带宽视频或遥测；
- 严格订阅和安全隔离；
- Host 对无关报文和 Jitter 敏感；
- Querier、Membership、冗余和监控都已完善。

### 15.3 生产建议

不要全局盲目选择。应按 VLAN 和业务分类，记录：

```text
Unknown Policy
Expected Querier
Expected Mrouter Ports
Allowed Sources
Allowed Groups
Failure Behavior
Owner
```

---

## 16. 配置示例

厂商语法差异很大，以下仅为概念示例：

```text
ip igmp snooping vlan 10
ip igmp snooping vlan 10 drop-unknown
```

或者：

```text
unknown-multicast flood
unknown-multicast drop
unknown-multicast router-port-only
```

应用前必须查阅目标平台文档，并确认是否对 `224.0.0.0/24`、IGMP、PIM 和静态 Group 做例外处理。

---

## 17. 验证实验

### 17.1 无 Receiver

1. 清除动态 Snooping Entry；
2. Source 向测试 Group 发送低速 UDP；
3. 在多个 Host Port 抓包；
4. 记录 Flood、Drop 或 Router-only 行为。

### 17.2 Receiver 加组

1. Receiver 发送 Report；
2. 确认 Snooping Entry；
3. 确认数据只到 Member Port 与必要的 Mrouter Port。

### 17.3 Receiver 离组或状态老化

1. 停止 Receiver；
2. 等待 Leave Process 或 Timer；
3. 观察 Entry 删除后的数据行为。

### 17.4 Querier 故障

1. 停止 Query；
2. 观察 Member Timer；
3. 记录 Entry 老化后是 Flood 还是 Drop；
4. 恢复 Querier并确认状态重建。

测试必须使用受控低带宽流量，避免在生产 VLAN 制造 Flood。

---

## 18. 排障命令与抓包

```text
show ip igmp snooping vlan 10
show ip igmp snooping groups vlan 10
show ip igmp snooping mrouter vlan 10
show ip igmp snooping querier vlan 10
show hardware profile multicast
show platform hardware capacity
```

Wireshark：

```text
ip.dst == 239.1.1.1
igmp
eth.dst[0] & 1 == 1
```

比较：

```text
Source ingress count
Member egress count
Non-member egress count
Mrouter egress count
Drop counter
```

---

## 19. 排障流程

1. 明确 Group、Source、VLAN 和预期 Receiver；
2. 确认数据是否属于 IPv4 Multicast，而不是其他 Ethernet Group Traffic；
3. 检查 Snooping 是否在目标 VLAN Operational；
4. 检查 Group 是否 Known；
5. 检查 Member Port 与 Mrouter Port；
6. 检查 Querier 和 Timer；
7. 确认 Unknown Policy；
8. 检查 ACL、Storm Control、Boundary 和 Router Guard；
9. 检查 ASIC/TCAM/Replication Resource；
10. 在 Member、Non-Member 和 Router Port 同时抓包；
11. 复现 Join、Leave、Aging 和 Failover 全过程。

---

## 20. 常见误解

### “Unknown Multicast 一定会 Flood”

错误。平台可能 Drop 或只送往 Mrouter Port。

### “启用 Snooping 后 Unknown Multicast 一定会 Drop”

错误。Snooping Enabled 与 Unknown Policy 是不同配置。

### “没有 Receiver 就不应该把数据送到 Router Port”

错误。Router 可能需要把数据路由给其他网络的 Receiver。

### “`224.0.0.X` 可以按普通应用 Group 丢弃”

错误。它包含关键本地控制协议，通常需要特殊处理。

### “Unknown Multicast 与 32:1 MAC Collision 是同一问题”

错误。一个是缺少可用转发状态，一个是多个 IP Group 映射同一 MAC。

### “软件表有 Entry，就一定不是 Unknown”

错误。硬件下发失败时，数据平面仍可能按 Unknown Policy 处理。

---

## 21. Chapter Summary

1. Known Multicast 有可用的组播转发状态，Unknown Multicast 没有。
2. Unregistered Multicast 的厂商定义可能不同。
3. Unknown Policy 可以是 Flood、Drop 或 Router-only Forwarding。
4. Flood 提高兼容性，但增加带宽、Host 负载和安全风险。
5. Drop 提高隔离性，但控制平面故障时可能造成黑洞。
6. Source 先于 Receiver 启动时会出现瞬态 Unknown Traffic。
7. Snooping Entry 老化后，后续数据重新进入 Unknown Policy。
8. `224.0.0.0/24` 控制流量通常需要特殊处理。
9. 未知 IGMP Message 不等于未知组播数据。
10. Mrouter Port 通常仍需要接收组播数据。
11. ASIC 资源不足可能触发 Flood、Drop、软件转发或状态合并。
12. 32:1 MAC 重叠与 Unknown Multicast 是不同问题。
13. Unknown Policy 应按 VLAN 和业务风险设计，而不是全局盲目配置。
14. 排障必须同时检查 Querier、Membership、软件表、硬件表和实际抓包。

---

## 22. References

- RFC 4541 — Considerations for IGMP and MLD Snooping Switches
- RFC 1112 — Host Extensions for IP Multicasting
- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 5771 — IANA Guidelines for IPv4 Multicast Address Assignments
- RFC 9166 — A YANG Data Model for IGMP and MLD Snooping
