---
status: cn-draft
title: IPv4 Multicast Addressing and Scope
chapter: 02
tags:
  - Multicast
  - IPv4
  - SSM
  - ASM
  - Address Planning
---

# 02 - IPv4 Multicast Addressing and Scope

## 1. 组播 IP 地址的本质

### 1.1 组播地址只能作为目的地址

IPv4 组播地址用于标识一个逻辑上的接收组，因此它只能出现在 IPv4 报文头部的目的地址字段中。

合法的组播报文示例：

```text
Source IP:      192.168.10.10
Destination IP: 239.1.1.1
```

不合法的报文示例：

```text
Source IP:      239.1.1.1
Destination IP: 192.168.10.20
```

组播报文的源地址必须是发送端使用的单播 IP 地址。组播地址不能被用作 IPv4 Source Address。

在排查组播业务时，需要同时区分：

```text
Source Address = 谁发送了流量
Group Address  = 流量被发送到哪个逻辑频道
```

二者共同构成组播转发状态：

```text
(S,G)
```

例如：

```text
(192.168.10.10, 239.1.1.1)
```

---

### 1.2 组播地址不是接口地址

单播地址通常配置在具体接口上：

```text
interface Ethernet0
 ip address 192.168.10.20 255.255.255.0
```

组播地址通常不会像单播地址一样被配置为接口的主机地址。

Receiver 应用通过 Socket API 请求在某个接口上加入一个组播组：

```text
Application
    │
    │ Join 239.1.1.1 on ens3
    ▼
Operating System
    │
    ▼
Interface ens3
```

因此，更准确的定义是：

> A multicast group address identifies a logical receiver group rather than a specific host or interface.

需要注意，组播地址本身不属于某个接口，并不代表组播转发是无状态的。组播网络会维护大量状态，例如：

- Host membership state；
- IGMP state；
- IGMP Snooping state；
- `(*,G)` state；
- `(S,G)` state；
- Incoming Interface；
- Outgoing Interface List。

---

### 1.3 Group 与 Channel

在 ASM 中，Receiver 只指定组播组：

```text
G
```

例如：

```text
239.1.1.1
```

这个逻辑对象通常称为：

```text
Multicast Group
```

在 SSM 中，Receiver 同时指定 Source 和 Group：

```text
(S,G)
```

例如：

```text
(10.1.1.10, 232.1.1.1)
```

这个由 Source 和 Group 共同标识的逻辑对象称为：

```text
SSM Channel
```

即使两个 SSM Channel 使用相同的 Group，只要 Source 不同，它们仍然是两个不同的 Channel：

```text
(10.1.1.10, 232.1.1.1)
(10.1.1.20, 232.1.1.1)
```

---

## 2. IPv4 组播地址空间

### 2.1 基本范围

IPv4 组播使用以下地址空间：

```text
224.0.0.0/4
```

完整范围为：

```text
224.0.0.0 - 239.255.255.255
```

该地址空间在传统分类编址中被称为：

```text
Class D Address Space
```

在现代技术文档中，更推荐使用：

```text
IPv4 Multicast Address Space
```

---

### 2.2 二进制结构

所有 IPv4 组播地址的最高 4 位固定为：

```text
1110
```

结构如下：

```text
┌──────────┬────────────────────────────┐
│   1110   │       Remaining 28 bits    │
└──────────┴────────────────────────────┘
  4 bits             28 bits
```

最低地址：

```text
11100000.00000000.00000000.00000000
224.0.0.0
```

最高地址：

```text
11101111.11111111.11111111.11111111
239.255.255.255
```

剩余的 28 位理论上可表示：

```text
2^28 = 268,435,456
```

个不同值。

但是，整个 `224.0.0.0/4` 已经被 IANA 划分成多个具有不同语义的地址块，不能将其中任意地址直接用于生产业务。

---

## 3. 主要 IPv4 组播地址块

### 3.1 地址空间总览

| 地址范围 | 名称 | 主要用途 |
|---|---|---|
| `224.0.0.0/24` | Local Network Control Block | 仅限本地链路的协议控制流量 |
| `224.0.1.0/24` | Internetwork Control Block | 可能跨越三层网络的协议控制流量 |
| `224.0.2.0 - 224.0.255.255` | AD-HOC Block I | IANA 特殊分配 |
| `224.1.0.0/16` | Reserved | 不应用于普通业务 |
| `224.2.0.0/16` | SDP/SAP Block | 会话公告相关应用 |
| `224.3.0.0 - 224.4.255.255` | AD-HOC Block II | IANA 特殊分配 |
| `224.5.0.0 - 231.255.255.255` | Mostly Reserved | 不应用于普通业务 |
| `232.0.0.0/8` | Source-Specific Multicast Block | 标准 IPv4 SSM 地址空间 |
| `233.0.0.0 - 233.251.255.255` | GLOP Block | 基于 16-bit ASN 的历史全局分配机制 |
| `233.252.0.0/24` | MCAST-TEST-NET | 文档和示例代码 |
| `233.252.0.0 - 233.255.255.255` | AD-HOC Block III | IANA 特殊分配，其中首个 `/24` 用作文档地址 |
| `234.0.0.0 - 238.255.255.255` | Reserved | 不应用于普通业务 |
| `239.0.0.0/8` | Administratively Scoped Block | 组织或管理域内部使用 |

> 不应将 `224.0.1.0 - 238.255.255.255` 简单理解为一个统一的“全球可路由组播地址范围”。其中包含多个 Reserved、AD-HOC、SSM、GLOP 和专用地址块。

---

## 4. Local Network Control Block

### 4.1 地址范围

```text
224.0.0.0/24
```

即：

```text
224.0.0.0 - 224.0.0.255
```

这个地址块用于本地链路上的协议控制流量。

核心规则是：

> Traffic sent to the Local Network Control Block is not forwarded off the local link.

也就是说，路由器不会把目的地址属于 `224.0.0.0/24` 的流量转发到其他三层链路。

---

### 4.2 与 TTL 的关系

不能简单地说：

```text
224.0.0.0/24 的 TTL 一定被设备强制设置为 1
```

更准确的理解是：

1. 许多使用该范围的控制协议在发送报文时会使用 TTL 1；
2. 路由器不能将该范围的流量转发离开本地链路；
3. 不可跨链路的限制独立于报文当前的 TTL 值。

因此，即使某个异常报文使用：

```text
Destination: 224.0.0.5
TTL:         10
```

也不意味着路由器可以将它继续转发到其他链路。

TTL 是 IP 层的跳数限制；Local Network Control Block 是地址语义规定的链路范围。两者不能混为一谈。

---

### 4.3 常见地址

| 地址 | 用途 |
|---|---|
| `224.0.0.0` | Base Address，保留 |
| `224.0.0.1` | All Systems on This Subnet |
| `224.0.0.2` | All Routers on This Subnet |
| `224.0.0.5` | OSPF AllSPFRouters |
| `224.0.0.6` | OSPF AllDRouters |
| `224.0.0.9` | RIPv2 Routers |
| `224.0.0.10` | EIGRP Routers |
| `224.0.0.13` | All PIM Routers |
| `224.0.0.18` | VRRP |
| `224.0.0.22` | IGMPv3 Routers |

这些地址由标准协议使用，不应该被企业应用随意占用。

---

### 4.4 排障直觉

看到以下地址：

```text
224.0.0.X
```

应立即想到：

- 它通常属于协议控制流量；
- 它只在本地链路有效；
- 不需要排查远端 RP 或跨网段 PIM Tree；
- 应重点检查本地 VLAN、接口状态、控制平面过滤和协议邻居；
- 不能仅根据 TTL 判断它是否能够跨越路由器。

---

## 5. Internetwork Control Block

### 5.1 地址范围

```text
224.0.1.0/24
```

即：

```text
224.0.1.0 - 224.0.1.255
```

这个地址块同样用于协议控制流量，但与 `224.0.0.0/24` 不同，它的流量在协议和网络设计允许时可以跨越三层链路。

典型示例：

```text
224.0.1.1
```

历史上被分配给 NTP 组播。

---

### 5.2 工程注意事项

“可以被路由”不代表它一定能够在公网或企业网络中正常跨域传播。

实际能否转发仍然取决于：

- 网络是否部署组播路由；
- PIM 是否启用；
- RPF 是否通过；
- 是否存在组播边界；
- ACL 或安全策略是否允许；
- 上下游网络是否提供组播服务。

因此：

> Address semantics permit forwarding, but network configuration determines whether forwarding actually occurs.

---

## 6. Source-Specific Multicast Block

### 6.1 标准范围

IPv4 SSM 的标准地址范围是：

```text
232.0.0.0/8
```

即：

```text
232.0.0.0 - 232.255.255.255
```

其中 IANA 进一步保留：

```text
232.0.0.0
232.0.0.1 - 232.0.0.255
```

普通本地应用分配通常使用：

```text
232.0.1.0 - 232.255.255.255
```

---

### 6.2 地址前缀不会自动建立组播树

看到目的地址属于 `232.0.0.0/8`，网络工程师应想到 SSM，但不能理解成：

```text
只要 Source 发送到 232/8，网络就会自动建立 SPT
```

完整的 SSM 转发仍然需要：

1. Receiver 明确订阅 `(S,G)`；
2. Last-Hop Router 收到 Source-Specific Membership；
3. 网络启用相应的 SSM 行为；
4. PIM `(S,G)` Join 沿 RPF 路径向 Source 传播；
5. 沿途设备建立 `(S,G)` state；
6. Source 的数据到达正确的 RPF 接口。

典型流程：

```text
Receiver
   │
   │ IGMPv3 INCLUDE (S,G)
   ▼
Last-Hop Router
   │
   │ PIM (S,G) Join
   ▼
RPF Path toward Source
   │
   ▼
Source
```

在 SSM 范围内，不使用 ASM 的 `(*,G)` Shared Tree 进行源发现，也不需要 RP 参与 Source Discovery。

---

### 6.3 SSM 不等于低延迟保证

SSM 的主要优势是简化控制面：

- 不需要 RP 进行源发现；
- 不需要 Shared Tree；
- Receiver 明确知道 Source；
- 只建立需要的 `(S,G)` state；
- 更容易限制非授权 Source；
- 故障排查可以围绕明确的 Source 和 Group 展开。

但是，`232/8` 这个地址前缀本身不会：

- 降低 ASIC 的单包转发延迟；
- 保证物理路径最短；
- 消除单播路由绕行；
- 消除 RPF Failure；
- 保证无丢包；
- 保证零收敛时间。

更准确的结论是：

> SSM simplifies source discovery and multicast control-plane state, but forwarding performance still depends on the actual network path and platform implementation.

---

### 6.4 在金融行情网络中的价值

已知、固定的行情 Source 通常非常适合使用 SSM：

```text
Source IP + Group IP + UDP Port
```

例如：

```text
Source: 10.10.10.10
Group:  232.100.1.1
Port:   UDP 12001
```

Receiver 只订阅指定 Source 的流量，可以减少错误 Source 或非授权 Source 对业务的影响。

不过，是否使用 `232/8` 仍然取决于：

- 交易所 Feed Specification；
- 现有地址规划；
- Receiver 是否支持 IGMPv3；
- 设备是否支持 SSM；
- 是否使用 SSM Mapping；
- 是否存在遗留 ASM 业务。

---

## 7. GLOP Block

### 7.1 地址范围

```text
233.0.0.0 - 233.251.255.255
```

GLOP 是一种基于 16-bit ASN 的组播地址分配机制。

假设一个组织的 16-bit ASN 用两个十进制字节表示为：

```text
X.Y
```

它可以得到：

```text
233.X.Y.0/24
```

例如，ASN 64500：

```text
64500 / 256 = 251 remainder 244
```

因此对应：

```text
233.251.244.0/24
```

---

### 7.2 工程定位

GLOP 可以作为历史地址分配机制理解，但不应成为现代企业内部组播规划的默认选择。

对于现代企业或数据中心，通常应优先评估：

- `232/8` SSM；
- `239/8` Administratively Scoped Multicast；
- 已由外部服务提供方明确分配的组播地址。

---

## 8. Documentation Address Block

在技术文档、示例代码和实验说明中，推荐使用：

```text
233.252.0.0/24
```

该地址块被称为：

```text
MCAST-TEST-NET
```

它不应该出现在公共 Internet 中。

例如，文档中的组播示例可以写成：

```text
Source: 192.0.2.10
Group:  233.252.0.10
```

这样可以避免误用现实中已经分配给某个协议或组织的地址。

---

## 9. Administratively Scoped Multicast

### 9.1 地址范围

```text
239.0.0.0/8
```

即：

```text
239.0.0.0 - 239.255.255.255
```

它用于某个管理域或组织内部的组播服务。

它经常被类比为单播中的 RFC 1918 私有地址，但两者的实现机制并不完全相同。

---

### 9.2 地址不会被公网路由器自动丢弃

不能简单地说：

```text
公网路由器看到 239/8 就会无条件丢弃
```

`239/8` 的作用域需要由网络管理员通过组播边界和过滤策略进行控制。

边界可能通过以下机制实现：

- Multicast Boundary；
- Group ACL；
- PIM Boundary；
- TTL Threshold；
- VRF 隔离；
- 防火墙策略；
- 外部网络的路由和服务策略。

如果边界设备配置错误，`239/8` 流量仍然可能被意外转发到不希望到达的位置。

因此，Administratively Scoped Address 不能替代真正的安全控制。

---

### 9.3 RFC 2365 中的重要子范围

#### IPv4 Local Scope

```text
239.255.0.0/16
```

用于较小的本地管理范围。

#### IPv4 Organization Local Scope

```text
239.192.0.0/14
```

范围为：

```text
239.192.0.0 - 239.195.255.255
```

组织在规划私有组播空间时，通常可以优先从 Organization Local Scope 中划分内部业务地址。

其余 `239/8` 空间还包含可用于范围扩展的区域，但不应在没有统一地址规划的情况下随意分配。

---

### 9.4 企业与量化环境中的应用

Administratively Scoped Multicast 可用于：

- 企业内部视频分发；
- 数据中心内部服务发现；
- 内部实时数据流；
- 风控或监控数据分发；
- 内部交易策略数据；
- 不能或不需要跨越组织边界的组播服务。

例如：

```text
239.192.10.0/24  Market Risk Data
239.192.20.0/24  Internal Monitoring
239.192.30.0/24  Backtesting Feeds
```

这只是地址规划示例，不代表地址本身会自动完成业务隔离。实际隔离仍需依赖 VRF、边界、ACL 和组播控制面配置。

---

## 10. Address Scope、TTL 与 Routing Boundary

这三个概念经常被混淆。

### 10.1 TTL

TTL 表示 IPv4 报文还能经过多少次三层转发。

```text
TTL = 4
```

每经过一个路由跳点，TTL 通常减 1。

Layer 2 Switch 不会因为普通二层转发而减少 IPv4 TTL。

---

### 10.2 Address Scope

Address Scope 表示某个地址块在协议语义上被设计用于多大的传播范围。

例如：

```text
224.0.0.0/24
```

属于 Link-Local Control Traffic，不能被路由器转发离开当前链路。

---

### 10.3 Administrative Boundary

Administrative Boundary 是网络管理员实际配置的转发边界。

例如：

```text
239.192.0.0/14
```

属于组织内部使用的地址空间，但必须在组织出口配置边界，才能确保它不会被继续转发。

---

### 10.4 三者的区别

| 概念 | 解决的问题 |
|---|---|
| TTL | 报文最多还能经过多少个三层跳点 |
| Address Scope | 该地址在标准中被定义为什么传播范围 |
| Administrative Boundary | 网络实际在哪个接口或域阻止该流量 |

不要使用 TTL 代替地址边界，也不要认为使用 `239/8` 后就不再需要过滤策略。

---

## 11. SSM 地址范围配置

> 以下命令以 Cisco IOS/IOS XE 为例。具体语法和默认行为取决于设备平台与软件版本。

### 11.1 启用标准 SSM 范围

标准 SSM 范围是：

```text
232.0.0.0/8
```

在 Cisco IOS/IOS XE 上可以使用：

```text
configure terminal
ip pim ssm default
end
```

这里的 `default` 表示使用标准 `232/8` 作为 SSM Range。

需要注意，设备支持 `232/8` 并不等于 SSM 功能一定默认处于启用状态。应以实际配置和平台文档为准。

---

### 11.2 定义自定义 SSM 范围

某些遗留业务或外部 Feed 可能使用非 `232/8` 的组地址，但业务仍然要求按 SSM 模型运行。

例如，将以下两段同时定义为 SSM：

```text
232.0.0.0/8
239.100.0.0/16
```

配置示例：

```text
ip access-list standard QUANT-SSM-RANGE
 permit 232.0.0.0 0.255.255.255
 permit 239.100.0.0 0.0.255.255
!
ip pim ssm range QUANT-SSM-RANGE
```

这里显式保留了标准 `232/8`，同时增加了 `239.100.0.0/16`。

自定义 SSM Range 的含义不是“让数据包自动获得更快的硬件转发”，而是告诉设备：

- 这些 Group 使用 SSM 服务模型；
- 接收端应提供 Source-Specific Membership；
- 网络建立 `(S,G)` state；
- 不对这些 Group 执行 ASM RP Source Discovery。

---

### 11.3 配置前需要确认的事项

在扩大或修改 SSM 范围前，需要确认：

- Receiver 是否使用 IGMPv3 INCLUDE Mode；
- 是否需要 SSM Mapping 兼容 IGMPv1/v2 Receiver；
- 所有 Last-Hop Router 是否使用一致的 SSM Range；
- RP 和 MSDP 策略是否与新范围冲突；
- 地址是否与现有 ASM 服务重叠；
- 设备和软件版本是否支持该配置；
- 变更是否会影响现有 Receiver。

不要仅在一台中间路由器上修改 SSM Range，然后假设端到端服务会自动一致。

---

## 12. 配置与状态验证

不同平台的命令会有所不同，以下为 Cisco IOS/IOS XE 常见检查方向。

### 12.1 检查 SSM 配置

```text
show running-config | include ip pim ssm
```

可能看到：

```text
ip pim ssm default
```

或者：

```text
ip pim ssm range QUANT-SSM-RANGE
```

---

### 12.2 检查 Receiver Membership

```text
show ip igmp groups detail
```

对于 SSM，应重点确认：

- Group；
- Source；
- Interface；
- IGMP Version；
- Include Mode；
- Membership Timer。

---

### 12.3 检查组播路由状态

```text
show ip mroute
```

对于 SSM Group，应重点观察：

```text
(S,G)
```

以及：

- Incoming Interface；
- RPF Neighbor；
- Outgoing Interface List；
- Flags；
- Packet Counter。

不要只看到 Group 地址就认为 SSM 已经正确工作。还需要确认具体 Source 和正确的 RPF 状态。

---

### 12.4 检查 RPF

```text
show ip rpf <source-ip>
```

例如：

```text
show ip rpf 10.10.10.10
```

确认：

- RPF Interface；
- RPF Neighbor；
- Route Source；
- Route Preference；
- 是否与数据实际进入接口一致。

---

### 12.5 检查 RP 相关信息

```text
show ip pim rp mapping
```

对于标准 SSM 业务，不应依赖 RP 完成 Source Discovery。

但仅仅看到某个通配 RP Mapping 覆盖了 `224/4`，不一定表示 SSM 数据会经过 RP。最终仍需要结合：

- SSM Range 配置；
- IGMP Membership；
- `show ip mroute`；
- PIM Join 类型；

进行判断。

---

## 13. 组播地址规划原则

### 13.1 不要将协议保留地址用于应用

以下范围不应该被普通应用随意使用：

```text
224.0.0.0/24
```

也不要从 IANA Reserved Blocks 中随机挑选地址。

---

### 13.2 已知 Source 的业务优先评估 SSM

对于 Source 固定、Receiver 明确订阅的业务，应优先评估：

```text
232.0.0.0/8
```

以及标准的 `(S,G)` Subscription。

SSM 能简化 Source Discovery 和故障排查，但不能替代 QoS、冗余和应用层恢复机制。

---

### 13.3 内部组播应使用统一的管理范围

组织内部使用 ASM 或需要内部 Scope 时，可以从：

```text
239.192.0.0/14
```

等 Administratively Scoped 空间中进行统一规划。

不要让不同团队在整个 `239/8` 中随意选择地址。

---

### 13.4 地址台账应记录完整业务标识

只记录 Group 地址是不够的。

建议至少记录：

| 字段 | 示例 |
|---|---|
| Service Name | HKEX Feed A |
| Source IP | `10.10.10.10` |
| Group IP | `232.100.1.1` |
| UDP Port | `12001` |
| Service Model | SSM |
| Receiver VLAN/VRF | `MARKET-DATA` |
| Scope | Data Center |
| Owner | Market Data Team |
| Redundant Feed | Feed B |
| Recovery Method | TCP Retransmission |
| Status | Production |

尤其在 SSM 中，应将完整的：

```text
Source + Group + UDP Port
```

作为业务标识。

---

### 13.5 地址范围不等于安全策略

无论使用：

```text
232/8
```

还是：

```text
239/8
```

都需要配合：

- Source ACL；
- Group ACL；
- Multicast Boundary；
- VRF；
- Firewall Policy；
- Control-Plane Protection；
- Receiver Access Control。

地址规划用于降低冲突和提高可管理性，但不能单独提供安全保障。

---

## 14. 工程判断直觉

### 14.1 看到 `224.0.0.X`

立即想到：

- 本地链路控制流量；
- 不会被路由器转发离开当前链路；
- 很可能是 OSPF、PIM、VRRP、IGMP 等协议；
- 检查本地接口、VLAN 和控制平面策略；
- 不要将问题直接归因于远端 RP 或跨域 PIM。

---

### 14.2 看到 `232.X.X.X`

立即想到：

- 标准 SSM Range；
- Receiver 应明确指定 Source；
- 期望看到 `(S,G)` state；
- 不需要 RP 进行 Source Discovery；
- 检查 IGMPv3、PIM Join 和 RPF；
- 不代表一定低延迟或无故障。

---

### 14.3 看到 `239.X.X.X`

立即想到：

- Administratively Scoped Multicast；
- 可能是企业内部业务；
- 检查地址规划和边界策略；
- 不要假设公网设备会自动阻止它；
- 确认它被按 ASM 还是自定义 SSM Range 处理。

---

### 14.4 看到 `233.252.0.X`

立即想到：

- 文档和示例地址；
- 不应该出现在真实公网业务中。

---

## 15. 地址分类练习

判断以下地址的主要含义。

### 15.1 `224.0.0.13`

```text
Local Network Control Block
All PIM Routers
Link-local protocol control traffic
```

---

### 15.2 `224.0.1.1`

```text
Internetwork Control Block
Historically assigned to NTP multicast
May be routed when the network permits
```

---

### 15.3 `232.10.20.30`

```text
Standard IPv4 SSM address
Receiver should identify the source
Expected state: (S,G)
```

---

### 15.4 `233.252.0.10`

```text
MCAST-TEST-NET
Suitable for documentation and examples
Not for public production traffic
```

---

### 15.5 `239.192.10.10`

```text
Administratively Scoped
Inside Organization Local Scope
Requires an explicitly designed administrative boundary
```

---

## 16. Chapter Summary

1. IPv4 组播地址使用 `224.0.0.0/4`。
2. 所有 IPv4 组播地址的最高 4 位固定为 `1110`。
3. 组播地址只能作为 Destination IP，不能作为 Source IP。
4. 组播地址表示逻辑 Group，而不是某个具体接口。
5. 在 SSM 中，Source 和 Group 共同标识一个 Channel：`(S,G)`。
6. `224.0.0.0/24` 用于本地链路控制流量，路由器不会将它转发离开本地链路。
7. `224.0.0.0/24` 的链路范围限制不能简单等同于 TTL 1。
8. `224.0.1.0/24` 用于可能跨三层网络的协议控制流量。
9. `232.0.0.0/8` 是标准 IPv4 SSM 地址空间。
10. SSM 需要 Receiver 明确订阅 `(S,G)`，地址前缀本身不会自动建立转发树。
11. SSM 不使用 RP 进行 Source Discovery，但仍然依赖 IGMP、PIM、RPF 和单播路由。
12. SSM 简化控制面，但不会自动保证最低延迟、无丢包或最优物理路径。
13. `239.0.0.0/8` 是 Administratively Scoped 地址空间。
14. Administratively Scoped 流量需要配置明确的网络边界，并不会被所有路由器自动阻止。
15. `239.255.0.0/16` 是 IPv4 Local Scope，`239.192.0.0/14` 是 Organization Local Scope。
16. `233.252.0.0/24` 应用于组播文档和示例。
17. 生产地址规划应记录完整的 Source、Group、UDP Port、Scope、VRF 和业务Owner。
18. 地址规划不能替代 ACL、VRF、组播边界和防火墙策略。

---

## 17. References

- RFC 1112 — Host Extensions for IP Multicasting
- RFC 2365 — Administratively Scoped IP Multicast
- RFC 4607 — Source-Specific Multicast for IP
- RFC 5771 — IANA Guidelines for IPv4 Multicast Address Assignments
- IANA — IPv4 Multicast Address Space
- Cisco IOS IP Multicast Command Reference — `ip pim ssm`