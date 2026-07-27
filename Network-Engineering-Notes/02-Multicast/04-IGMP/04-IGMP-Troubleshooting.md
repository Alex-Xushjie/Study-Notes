---
status: cn-draft
title: IGMP Troubleshooting
module: 04-IGMP
file: 04-IGMP-Troubleshooting
tags:
  - Multicast
  - IGMP
  - Troubleshooting
  - Packet Capture
  - Membership
---

# 04 - IGMP Troubleshooting

## 1. 本章目标

本章把 IGMPv1、IGMPv2 和 IGMPv3 的协议知识转换为可重复执行的排障方法。

完成本章后，应能够：

- 判断故障是否真的发生在 IGMP；
- 区分 Source、Receiver、二层转发、IGMP Membership 和组播路由故障；
- 从应用、Host、LAN、Querier、Last-Hop Router 五个观察点收集证据；
- 验证 Query、Report、Leave、Group Record 和 Source List；
- 根据定时器判断“尚未收敛”还是“状态异常”；
- 识别版本降级、Querier 异常和 IGMPv3 Source Filtering 错误；
- 解释“有 Report 但没有流量”和“有流量但没有 Report”等现象；
- 使用双点或多点抓包定位报文丢失的位置；
- 建立一套与厂商命令无关的排障思维。

本章主要研究 Host 与直连 Multicast Router 之间的三层 Membership。

以下问题属于相邻故障域：

- 二层交换机如何建立 Member Port 和 Router Port：第 05 章 IGMP Snooping；
- Router 之间如何建立组播树：后续 PIM 章节；
- Source-Specific Multicast 的完整端到端行为：第 09 章 SSM；
- 全网组播故障的系统方法：`13-Multicast-Troubleshooting-Methodology.md`。

---

## 2. 先建立正确的故障模型

一个 Receiver 能收到组播流量，至少依赖以下链路：

```text
Application
    ↓ Socket join / source filter
Receiver OS
    ↓ IGMP Report
Access LAN
    ↓
Last-Hop Router IGMP State
    ↓
Multicast Routing State
    ↓
Upstream Multicast Tree
    ↓
Source Traffic
```

IGMP 只回答：

> Last-Hop Router 的某个直连接口上，是否存在对 Group G，或对特定 `(S,G)` 感兴趣的 Receiver？

IGMP 不证明：

- Source 正在发送；
- Source 地址正确；
- UDP 端口正确；
- RPF Check 成功；
- PIM Join 已经发送；
- RP 或 SPT 正常；
- 二层交换机已把流量送到 Receiver Port；
- Receiver 防火墙允许数据；
- 应用正在读取 Socket。

因此：

```text
No multicast traffic
≠
IGMP failure
```

同样：

```text
Valid IGMP membership
≠
End-to-end multicast must work
```

---

## 3. 排障中的四类状态

不要把所有状态都称为“加组”。至少要区分四层：

| Layer | State | Example |
|---|---|---|
| Application | Socket Subscription | 应用请求 `G` 或 `(S,G)` |
| Host OS | Interface Membership | `Interface + Group + Filter Mode + Source List` |
| Last-Hop Router | IGMP Membership | 接口上存在 `(*,G)` 或 Source Interest |
| Multicast Routing | Forwarding Tree | `(*,G)` 或 `(S,G)` 有正确 IIF/OIF |

排障目标不是立即修改配置，而是先找出：

```text
The first state that is missing or incorrect.
```

---

## 4. 最小测试拓扑

```text
Source S
10.1.1.10
    │
    │ Multicast Routing Domain
    │
Last-Hop Router R1
192.168.10.1
    │
    │ Receiver LAN / VLAN 10
    │
Receiver H1
192.168.10.11
```

测试对象必须写成明确的元组：

```text
Receiver Interface: 192.168.10.11
Group:              239.1.1.1
Source:             10.1.1.10
UDP Port:           5000
IGMP Version:       v2 or v3
Join Type:          ASM or SSM
```

如果只记录“组播不通”，就无法判断两个观察点看到的是否是同一条流。

---

## 5. 排障前必须收集的事实

### 5.1 Receiver 信息

- Receiver IP、Mask、VLAN 和接收接口；
- 应用绑定的本地地址或接口；
- Group Address；
- ASM Join 还是 Source-Specific Join；
- 期望的 Source IP；
- UDP Destination Port；
- Host 操作系统和 IGMP 能力；
- Host Firewall、容器、VRF 或 Network Namespace。

### 5.2 网络信息

- Receiver 的 Default Gateway；
- Last-Hop Router 接口地址；
- 同一 LAN 上所有 Multicast Router；
- 当前 IGMP Querier；
- 配置版本和实际运行版本；
- Query Interval、Max Response Time、Robustness Variable；
- 是否存在 IGMP Snooping；
- 是否配置 Snooping Querier、Proxy、Static Join 或 Immediate Leave。

### 5.3 时间信息

```text
10:00:00 Start capture
10:00:05 Start receiver application
10:00:20 Start source
10:01:00 Stop receiver application
10:01:30 Stop capture
```

IGMP 是定时器驱动的协议。没有时间线，就很容易把正常等待误判为故障。

---

## 6. 一条可重复执行的排障路径

```text
Step 1  Confirm the exact symptom
   ↓
Step 2  Verify application subscription
   ↓
Step 3  Verify Host IGMP transmission
   ↓
Step 4  Verify Query reaches the Host
   ↓
Step 5  Verify Report reaches the Router
   ↓
Step 6  Verify Router membership state
   ↓
Step 7  Verify version, querier and timers
   ↓
Step 8  Verify multicast route and traffic
   ↓
Step 9  Verify Layer 2 forwarding
```

每一步都必须留下证据：

```text
State table
Packet capture
Counter
Timestamp
Configuration
```

---

## 7. Step 1：精确定义故障现象

先回答：

1. 所有 Receiver 都失败，还是只有一台？
2. 所有 Group 都失败，还是只有一个 Group？
3. 所有 Source 都失败，还是只有一个 Source？
4. 首次加组失败，还是运行一段时间后中断？
5. 单向无流量，还是存在丢包、重复、延迟离组？
6. ASM 正常但 SSM 失败，还是两者都失败？
7. 同 VLAN 内失败，还是跨 Router 才失败？

| Symptom | First Checks |
|---|---|
| 一台 Host 的所有 Group 失败 | 应用绑定、Host Firewall、Host Interface |
| 一个 VLAN 的所有 Receiver 失败 | Querier、VLAN、Router Interface、Snooping |
| 一个 Group 失败，其他 Group 正常 | Group State、ACL、组播路由 |
| ASM 正常，SSM 失败 | IGMPv3、Source List、SSM Range |
| 加组后长期无流量 | Report、Router Membership、上游 Tree |
| 离组后仍有流量 | Timer、旧版本 Host、Last Member Query |
| 周期性中断 | Query/Report 丢失、Membership Aging、Querier Flap |

---

## 8. Step 2：验证应用真的请求了 Membership

ASM 应用通常请求：

```text
Join Group G on Interface I
```

IGMPv3 SSM 应用请求：

```text
Join Source S, Group G on Interface I
```

需要检查的不是应用配置文件中的意图，而是操作系统实际 Socket State。

类 Unix 系统可结合：

```text
ip maddr show
```

该命令可能只能证明接口存在 Group Membership，未必完整显示每个 Socket 的 IGMPv3 Source Filter。还应检查 Socket、进程、Network Namespace 和应用日志。

常见应用层错误：

- 应用加入了错误的 Group；
- 配置的是 Source `S1`，实际 Source 是 `S2`；
- 应用绑定了 Loopback 或另一张 NIC；
- 多网卡 Host 选择了错误接口；
- 应用在 Container Namespace 中，而抓包在 Host Namespace；
- 应用加入后立即退出；
- Host Firewall 允许 IGMP，但阻止组播 UDP；
- 应用监听的 UDP Port 与 Source 发送端口不一致。

```text
No local socket membership
→ Do not troubleshoot the router yet.
```

---

## 9. Step 3：验证 Host 是否发送正确的 Report

在 Receiver 接口抓包，并在应用启动前开始捕获：

```text
igmp
```

只查看该 Host：

```text
igmp and ip.src == 192.168.10.11
```

### 9.1 三个版本的检查点

| Version | Type | IPv4 Destination | Membership Detail |
|---|---:|---|---|
| IGMPv1 | `0x12` | Group G | Group G |
| IGMPv2 | `0x16` | Group G | Group G |
| IGMPv3 | `0x22` | `224.0.0.22` | Group Record + Source List |

三者的 IPv4 Protocol 都为 `2`，TTL 通常都为 `1`。

SSM 典型 State-Change Record：

```text
CHANGE_TO_INCLUDE_MODE
Group:  232.1.1.1
Source: 10.1.1.10
```

ASM 典型状态：

```text
CHANGE_TO_EXCLUDE_MODE
Group: 239.1.1.1
Source List: Empty
```

### 9.2 没看到 Report 时

依次检查：

1. 抓包接口是否正确；
2. 抓包是否在应用 Join 之前启动；
3. Host 是否已经存在同一 Interface Membership；
4. 应用 Join 是否成功；
5. Host 是否因旧版本 Querier 而发送 `0x12` 或 `0x16`；
6. 虚拟交换路径是否影响可见性；
7. Host 网络栈或安全策略是否阻止 IGMP。

如果 Group 已被本机另一个应用加入，新应用加入时不一定产生新的接口级状态变化。

---

## 10. Step 4：验证 Host 能否收到 Query

Host 应周期性收到 General Query。

| Field | Expected |
|---|---|
| IPv4 Source | 当前 Querier 接口地址 |
| IPv4 Destination | `224.0.0.1` |
| IPv4 Protocol | `2` |
| TTL | `1` |
| IGMP Type | `0x11` |
| Group Address | `0.0.0.0` |

IGMPv2 常见：

```text
Max Resp Time = 100
→ 10 seconds
```

IGMPv3 还应检查：

```text
QRV
QQIC
S Flag
Number of Sources
```

没有 Query 的可能原因：

- VLAN 中没有 Multicast Router 或 IGMP Querier；
- Querier 接口 Down；
- Router 未启用 Multicast/IGMP；
- VLAN、Trunk 或 QinQ 映射错误；
- 二层安全策略丢弃 `224.0.0.1`；
- Snooping 设备未正确识别 Router Port；
- Querier Election 异常；
- 抓包点不在实际接收接口。

> Host 加组时通常会主动发送 Unsolicited Report，不需要等待 Query。

因此“没有 Query”不一定解释首次 Join 失败，但会造成 Membership 无法长期刷新。

---

## 11. Step 5：使用双点抓包验证 Report 路径

建议同时抓取：

```text
Point A: Receiver-facing access port or Host
Point B: Last-Hop Router receiver interface
```

| Host Capture | Router Capture | Conclusion |
|---:|---:|---|
| No Report | No Report | 应用或 Host 问题 |
| Report | No Report | 二层路径、VLAN、ACL 或 Snooping 问题 |
| Report | Report | 检查 Router 是否接受并安装状态 |
| No Report | Report | 抓包点/镜像配置错误，或其他 Host 发送 |

比较相同 Group、Source IP、IGMP Type、Group Record、Timestamp、IP Identification 和 Checksum。不要仅因两端都出现“一个 IGMP Report”就认定是同一个报文。

---

## 12. Step 6：验证 Router 的 IGMP Membership State

厂商命令不同，但需要获得以下逻辑字段：

```text
Interface
Group
IGMP Version
Filter Mode
Source List
Uptime
Expires / Timer
Reporter
Last Reporter
```

常见命令语义：

```text
show igmp interface
show igmp groups
show igmp groups detail
show igmp traffic
```

这些是通用语义，不是所有平台的精确命令。

IGMPv1/v2 期望状态：

```text
Interface: Receiver VLAN
Group:     239.1.1.1
State:     Present
Expires:   Running
```

IGMPv3 SSM 期望状态：

```text
Interface: Receiver VLAN
Group:     232.1.1.1
Mode:      INCLUDE
Source:    10.1.1.10
```

IGMPv3 ASM 期望状态：

```text
Group:       239.1.1.1
Mode:        EXCLUDE
Source List: Empty
```

Router 收到 Report 但没有状态时，检查：

- Checksum 是否正确；
- Source Address 是否属于直连网段；
- TTL、Router Alert 和目的地址是否符合版本要求；
- Group 是否为合法 IPv4 Multicast Address；
- 接口是否启用 IGMP；
- ACL、CoPP 或硬件 Punt 是否丢弃；
- VRF 是否一致；
- 是否支持该版本和 Group Record；
- 是否达到 Group、Source 或控制面资源上限。

---

## 13. Step 7：验证 Querier

IGMPv2 和 IGMPv3：

```text
Lowest interface IPv4 address wins.
```

IGMPv1 本身没有标准化的最低 IP 选举规则。

抓包过滤：

```text
igmp.type == 0x11
```

检查：

- Query Source 是否稳定；
- 是否有多台设备持续发送 General Query；
- 更低 IP 的设备出现后，原 Querier 是否停止；
- Query Interval 是否符合运行参数；
- 是否出现 Source IP 为 `0.0.0.0` 的特殊 Snooping Querier 行为；
- Query Version 是否导致 Host 降级。

Querier Flap 可能造成：

```text
Query Source changes repeatedly
        ↓
Timers are refreshed inconsistently
        ↓
Membership ages out periodically
        ↓
Traffic becomes intermittent
```

常见原因包括接口 Flap、重复 IP、Snooping Querier 冲突、VLAN 错误延伸和控制面限速。

---

## 14. Step 8：理解并验证定时器

| Parameter | Typical Default |
|---|---:|
| Robustness Variable | `2` |
| Query Interval | `125 seconds` |
| Query Response Interval | `10 seconds` |
| Group Membership Interval | `260 seconds` |
| Other Querier Present Interval | `255 seconds` |
| Last Member Query Interval | `1 second` |
| Last Member Query Count | `2` |

```text
Group Membership Interval
= Robustness Variable × Query Interval
 + Query Response Interval

= 2 × 125 + 10
= 260 seconds
```

```text
Other Querier Present Interval
= Robustness Variable × Query Interval
 + 0.5 × Query Response Interval

= 255 seconds
```

定时器判断：

```text
Membership disappears every ~260 seconds
→ Periodic Query or Report refresh may be missing.
```

```text
Membership remains after expected expiry
→ Check static join, proxy, local receiver,
  snooping state or implementation behavior.
```

始终读取设备运行值。厂商默认值和显式配置都可能不同。

---

## 15. Step 9：验证版本与兼容模式

| Packet | Type / Key Field |
|---|---|
| IGMPv1 Report | `0x12` |
| IGMPv2 Report | `0x16` |
| IGMPv2 Leave | `0x17` |
| IGMPv3 Report | `0x22` |
| Query | `0x11`，需继续检查格式 |

Query 都可能使用 `0x11`，不能只看 Type 判断版本。

典型降级：

```text
IGMPv3 Host
    ↓ hears IGMPv2 Query
Sends IGMPv2 Report
    ↓
Source List can no longer be expressed
```

SSM 故障中必须检查：

```text
Expected: IGMPv3 Report 0x22
Observed: IGMPv2 Report 0x16
```

这可能是网络中存在旧版本 Querier，并不一定是 Host 不支持 IGMPv3。

Router 检测到 IGMPv1 Host 后，相关 Group 可能不能使用快速离组，流量要等待 Membership Aging 才停止。

---

## 16. Step 10：验证 Leave 与 Last Member Query

IGMPv2 正常流程：

```text
Host
  │ Leave 0x17 to 224.0.0.2
  ▼
Querier
  │ Group-Specific Query to Group G
  │ repeated Last Member Query Count times
  ▼
Remaining Receiver
  │ Report, if still interested
  ▼
Keep or remove Membership
```

可能看不到 Leave 的原因：

- Host 不是 Last Reporter；
- 本机还有另一个应用持有 Membership；
- Host 处于 IGMPv1 兼容模式；
- 应用崩溃或接口断开；
- 抓包开始太晚；
- IGMPv3 使用 Group Record 表达状态变化。

```text
Leave
≠
No receivers remain
```

Leave 后流量持续时间异常时，检查旧版本 Host、Last Member Query 参数、其他 Host Report、Static Membership、Snooping State 和本机 Socket。

---

## 17. IGMPv3 Source Filtering 专项检查

必须比较：

```text
Expected:
Group G + Source S + Filter Mode

Observed:
Group G + Source List + Record Type
+ Router Source State
```

### 17.1 INCLUDE 与 EXCLUDE

```text
INCLUDE {S1}
→ Only S1 is wanted.

INCLUDE {}
→ No source is wanted.

EXCLUDE {S2}
→ All sources except S2 are wanted.

EXCLUDE {}
→ All sources are wanted.
```

### 17.2 常见错误

- 把 `INCLUDE {}` 理解为接收所有 Source；
- 把 `EXCLUDE {}` 理解为不接收任何 Source；
- 期望 SSM，Report 却是 `EXCLUDE {}`；
- Source List 中是错误地址；
- 应用请求 `(S1,G)`，实际流量来自 `S2`；
- 多个 Socket 聚合后，接口状态与单一应用不同；
- Router 收到 State-Change，但后续 Current-State 不一致；
- 老版本 Query 使 Source Filtering 丢失。

### 17.3 Group Record

State-Change：

```text
CHANGE_TO_INCLUDE_MODE
CHANGE_TO_EXCLUDE_MODE
ALLOW_NEW_SOURCES
BLOCK_OLD_SOURCES
```

Query Response：

```text
MODE_IS_INCLUDE
MODE_IS_EXCLUDE
```

一次 Report 可能只包含变化量。需要同时观察初始 Join、后续 Query 和 Current-State Report。

---

## 18. “有 Report，但没有流量”

按顺序检查：

```text
1. Router installed IGMP state?
2. Correct group and source?
3. Multicast route exists?
4. Incoming Interface passes RPF?
5. Receiver interface is in OIF list?
6. Packet counters increase?
7. Layer 2 forwards to receiver port?
8. Host receives UDP?
9. Application accepts the UDP port?
```

Router 已有 Membership，但没有对应 Multicast Routing State：

```text
IGMP may be healthy.
Continue with PIM, RP, RPF and source checks.
```

Router OIF Counter 增长，而 Host 抓不到数据：

```text
Focus on receiver LAN, IGMP Snooping,
VLAN path and host filtering.
```

---

## 19. “有流量，但没有看到 Report”

可能原因：

- Report 在抓包开始前已发送；
- 另一个 Host 的 Report 触发 Report Suppression；
- Router 仍保留未到期 Membership；
- Router 上存在 Static Join；
- Router 自身是 Receiver；
- 交换机对未知组播进行 Flood；
- Source 与 Receiver 在同一二层 LAN；
- 抓包位置不在 IGMP 路径；
- IGMP Proxy 或 Snooping Querier 改变了行为。

```text
No Report in a short capture
≠
No Membership exists.
```

至少覆盖一次完整 Query/Response Cycle，或重新启动测试应用。

---

## 20. 周期性中断

建立时间线：

```text
Query timestamp
Report timestamp
Router membership expiry
Multicast route removal
Traffic loss start/end
```

检查：

- Query 是否到达所有 Receiver；
- Report 是否到达 Router；
- Report Delay 是否在 Max Response Time 内；
- Membership 是否按 Group Membership Interval 老化；
- Querier 是否切换；
- CPU 或 CoPP 是否在高负载时丢弃 IGMP；
- Snooping Entry 与 Router Entry 的 Timer 是否不一致；
- 链路聚合路径是否只在部分成员链路丢包。

故障周期与协议定时器相同，通常是极强的定位线索。

---

## 21. 二层交换环境中的边界

IGMP 正常不代表 IGMP Snooping 正常。

```text
Layer 3:
Router IGMP Membership

Layer 2:
Snooping Group Entry
Member Port
Router Port
```

| L3 Membership | L2 Snooping | Result |
|---:|---:|---|
| Correct | Correct | 正常转发 |
| Correct | Missing Member Port | Router 发出，Receiver 收不到 |
| Missing | Correct | 本地二层可能有流量，跨 Router 失败 |
| Missing | Missing | 完全失败或未知组播泛洪 |

本章只把 Snooping 作为故障边界，其状态机在第 05 章研究。

---

## 22. 常见错误配置

### 22.1 接口版本不匹配

```text
Receiver requires IGMPv3 SSM
Router interface forced to IGMPv2
```

结果：Source List 无法表达。

### 22.2 Group Range 错误

```text
Expected SSM Group: 232.0.0.0/8
Actual Group:        239.1.1.1
```

实际 SSM Range 可能被配置修改，必须检查运行配置。

### 22.3 错误接口或 VRF

Membership 出现在另一个 VLAN、VRF 或 Subinterface。

### 22.4 ACL 只允许 UDP

```text
IGMP is IP protocol 2.
It is not UDP port 2.
```

### 22.5 误用 Immediate Leave

共享 LAN 有多个 Receiver 时，第一台 Host 离组可能导致其他 Receiver 被错误断流。

---

## 23. 控制面与资源问题

检查：

- IGMP Input/Output Counter；
- Invalid Checksum、Bad Length、Wrong Version；
- ACL、Control Plane Policing 和 CPU Queue Drop；
- Maximum Groups / Sources Exceeded；
- Hardware Programming Failure；
- Memory 或进程异常。

```text
Packet visible on wire
but input counter does not increase
→ Punt / hardware / ACL path

Input counter increases
but state is absent
→ Validation / resource / software path

State exists
but forwarding entry is absent
→ Multicast routing or hardware programming path
```

不要在没有 Counter 和日志证据时直接归因于“设备 Bug”。

---

## 24. 抓包过滤器速查

```text
All IGMP:       igmp
Query:          igmp.type == 0x11
IGMPv1 Report:  igmp.type == 0x12
IGMPv2 Report:  igmp.type == 0x16
IGMPv2 Leave:   igmp.type == 0x17
IGMPv3 Report:  igmp.type == 0x22
```

```text
igmp and ip.addr == 239.1.1.1
```

```text
ip.dst == 224.0.0.22 and igmp.type == 0x22
```

```text
ip.dst == 224.0.0.1 and igmp.type == 0x11
```

```text
ip.dst == 224.0.0.2 and igmp.type == 0x17
```

复杂 IGMPv3 Source List 最稳妥的方法是先用 `igmp` 缩小范围，再在 Packet Details 中检查 Group Record。

---

## 25. 报文通用检查清单

### 25.1 IPv4 层

- Source 和 Destination Address；
- Protocol `2`；
- TTL `1`；
- Header Checksum；
- Router Alert；
- Fragmentation；
- Checksum Offload 假告警。

### 25.2 IGMP 层

- Type 和 Checksum；
- Group Address；
- Max Resp Time / Code；
- Query Source List；
- Group Record Count 和 Record Type；
- Filter Mode；
- Source Count、Source Address 和报文长度。

### 25.3 上下文

- Join、Query Response 还是 Leave；
- 前序事件；
- 当前 Querier；
- Host 兼容版本；
- Timer 剩余时间。

---

## 26. 三个典型案例

### 26.1 Router 没有 Membership

```text
Host socket state: Present
Host capture:       IGMPv2 Report present
Router capture:     No Report
Router state:       Absent
```

结论：

```text
Fault domain = Receiver LAN between Host and Router
```

检查 VLAN、Trunk、ACL、Port Isolation 和 Snooping。

### 26.2 SSM Receiver 无流量

```text
Application requests: (10.1.1.10, 232.1.1.1)
Capture shows:        IGMPv2 Report for 232.1.1.1
Query source:         IGMPv2 Querier
```

结论：

```text
IGMPv3 Host has downgraded.
Source-specific interest cannot be expressed.
```

### 26.3 离组后流量持续约 260 秒

```text
No Leave observed
IGMPv1 Report previously observed
Group removed after approximately 260 seconds
```

行为符合 IGMPv1 兼容和 Group Membership Aging。

---

## 27. 常见误解

### “看到 Report 就证明组播端到端正常”

错误。Report 只证明 Host 在本地网段表达了 Membership。

### “看不到 Report 就证明没有 Receiver”

错误。可能发生 Report Suppression、抓包开始过晚或已有未到期状态。

### “Router 收到 Leave 后应立即停止流量”

错误。共享 LAN 上还可能存在其他 Receiver。

### “Query Type 是 `0x11`，所以一定是 IGMPv1”

错误。三个版本的 Query 都使用 `0x11`。

### “IGMPv3 Report 中出现 Group 就代表需要所有 Source”

错误。必须同时解释 Filter Mode 和 Source List。

### “IGMP Membership 正常，所以 PIM 一定正常”

错误。两者属于不同协议层。

### “一个 Report 的 Source IP 就是组播 Source”

错误。IGMP Report 的 Source IP 是 Receiver Host。

---

## 28. 故障记录模板

```text
Incident:
Time Window:

Receiver:
  Host IP:
  Interface:
  VLAN/VRF:
  Application:

Flow:
  Source IP:
  Group IP:
  UDP Port:
  ASM/SSM:

IGMP:
  Expected Version:
  Observed Version:
  Querier:
  Query Interval:
  Group Membership Interval:
  Host Report:
  Router Membership:
  Filter Mode:
  Source List:

Packet Capture:
  Host Point:
  Router Point:
  First Missing Packet:

Multicast Routing:
  Route:
  RPF Interface:
  OIF:
  Counters:

Layer 2:
  Snooping Entry:
  Member Port:
  Router Port:

Conclusion:
  First Missing State:
  Fault Domain:
  Evidence:
```

核心原则：

```text
Evidence before conclusion.
```

---

## 29. 最终排障清单

### Receiver

- [ ] 应用加入正确的 `G` 或 `(S,G)`
- [ ] 应用绑定正确接口
- [ ] Host 存在接口级 Membership
- [ ] Host Firewall 允许 IGMP 和组播数据
- [ ] Host 发出正确版本的 Report

### LAN

- [ ] Host 收到 General Query
- [ ] Query Source 是预期 Querier
- [ ] Report 从 Host 到达 Router
- [ ] VLAN 和 VRF 一致
- [ ] 没有 ACL、CoPP 或资源丢弃

### Router

- [ ] Receiver Interface 启用正确版本
- [ ] Group State 存在
- [ ] IGMPv3 Filter Mode 正确
- [ ] IGMPv3 Source List 正确
- [ ] Timer 正常刷新
- [ ] 没有意外版本降级

### End-to-End

- [ ] Source 发送正确 `(S,G,UDP Port)`
- [ ] Multicast Route 存在
- [ ] RPF 正确
- [ ] Receiver Interface 在 OIF List
- [ ] Router Output Counter 增长
- [ ] Snooping Member Port 正确
- [ ] Receiver 抓到数据
- [ ] 应用读取到数据

---

## 30. Chapter Summary

1. IGMP 排障的第一步是确认故障是否属于 Membership。
2. 应用、Host、Router Membership 和 Multicast Route 是四种不同状态。
3. 应从最靠近 Receiver 的应用和 Socket 开始检查。
4. 单点抓包不能证明报文完成了端到端传递。
5. 双点抓包可以快速识别二层路径故障。
6. Router 收到 Report 后还必须成功安装 Membership。
7. IGMPv2/v3 使用最低接口 IPv4 地址选举 Querier。
8. Query Source Flap 可能造成周期性 Membership Aging。
9. 故障周期接近 260 秒时，应检查 Group Membership Interval。
10. 三个版本的 Query Type 都是 `0x11`。
11. 旧版本 Querier 或 Host 可能导致功能降级。
12. SSM 排障必须检查 Filter Mode 和 Source List。
13. `INCLUDE {}` 表示不接收任何 Source。
14. `EXCLUDE {}` 表示接收所有 Source。
15. IGMPv2 Leave 不代表最后一个 Receiver 已离开。
16. IGMPv3 使用 Group Record 表达状态变化。
17. 有 Membership 但无流量时，应检查 PIM、RPF、Source 和 OIF。
18. Router 有输出而 Receiver 无数据时，应检查 Snooping、VLAN 和 Host。
19. 所有结论都应由状态、抓包、Counter 和时间线支持。

---

## 31. References

- RFC 1112 — Host Extensions for IP Multicasting
- RFC 2236 — Internet Group Management Protocol, Version 2
- RFC 3376 — Internet Group Management Protocol, Version 3
- RFC 4607 — Source-Specific Multicast for IP
- RFC 4541 — Considerations for Internet Group Management Protocol Snooping Switches
- IANA — Internet Group Management Protocol (IGMP) Type Numbers
