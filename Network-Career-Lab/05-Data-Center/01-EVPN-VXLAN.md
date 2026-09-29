# 现代数据中心：Underlay 与 Overlay 分开证明

## 1. 为什么先学 Clos

Leaf 接服务器，spine 互联各 leaf。两层 Clos 中 leaf 经 spine 到另一 leaf，多个等价路径可用 ECMP 分担流量。通常按流 hash，单个流不会自动吃满所有链路。端口 radix、上下行比例、故障后容量和布线决定可扩展性，而不只是交换机数量。

传统 STP 用于限制二层环路；L3 leaf-spine 用三层路由消除跨 fabric 的大二层依赖。仍需二层邻接的业务可以通过 overlay 承载，但不要把 overlay 当作取消容量与故障域约束的理由。

## 2. 各组件解决什么问题

| 对象 | 作用 | 常见混淆 |
|---|---|---|
| Underlay eBGP | 宣告 VTEP/loopback 可达性 | IP 通不等于 overlay 完整 |
| MP-BGP EVPN | 分发租户 MAC/IP、前缀和成员等信息 | 邻居 Established 不等于路由被导入 |
| VXLAN | 用 UDP/IP 封装二层帧 | VXLAN 本身不是 BGP 路由协议 |
| VTEP | 封装/解封装端点 | VTEP 源地址必须在 underlay 可达 |
| L2VNI | 对应二层广播域 | VNI 与本地 VLAN ID 不必相等 |
| L3VNI / VRF | 支撑租户三层转发 | symmetric IRB 与 asymmetric IRB 资源需求不同 |
| RD | 区分 VPN 路由标识 | 不是导入策略 |
| RT | 控制路由导入/导出 | RT 错误可造成隔离或泄漏 |

参考 [RFC 8365](https://www.rfc-editor.org/rfc/rfc8365) 的 overlay 框架。IPv4 VXLAN 常见封装增加约 50 字节，以外层 Ethernet/IP/UDP/VXLAN 的计算口径为例，不含额外 VLAN/FCS；实际 MTU 设计要按平台定义的 L2/L3 MTU、外层 IPv6 和标签数量重新计算。

## 3. Route Type 从转发问题记忆

Type 2 宣告 MAC，通常可带 IP 绑定，帮助远端定位主机；Type 3 IMET 描述广播域中的复制参与信息，用于 BUM 处理。Type 5 宣告 IP 前缀，适合发布汇总/外部路由等；其下一跳解析与 IRB 模型需结合实现，不能说“所有跨子网通信都必须靠 Type 5”。阅读 [RFC 9136](https://www.rfc-editor.org/rfc/rfc9136) 的 IP Prefix route 和 gateway 解析示例。

一台 H1 访问远端同子网 H2：H1 发帧→本地 leaf 查 MAC→查远端 VTEP→查 underlay 下一跳→VXLAN 封装→远端解封装→H2。逐层都有独立状态；抓包只能验证经过的观测点，不能代替 EVPN RIB 与 MAC/FDB 表。

跨子网时：H1 先发给默认网关，leaf 在租户 VRF 查目的前缀，再根据 IRB 模型转发。Anycast Gateway 在多 leaf 上提供一致的网关 IP/MAC，需保证平台配置与租户映射一致；不是把同一个任意地址配置在多台普通路由器上就得到 EVPN anycast。

## 4. ARP suppression 和 BUM

ARP suppression 使用已知 MAC/IP 绑定在本地代理响应，减少泛洪；绑定缺失、过期或错误仍需处理。已学习路由不代表主机永远不需要 ARP。BUM 包括 broadcast、unknown unicast、multicast；ingress replication 在入口复制给远端 VTEP，资源开销随参与端点与流量增长。底层 multicast 是另一种复制方案，选型取决于规模和运维能力。

## 5. MLAG 与 EVPN multihoming

MLAG 用厂商双机协同呈现聚合；EVPN multihoming 用 Ethernet Segment/ESI 等控制多归属。两者实现和故障行为不同。ESI 标识以太网段，DF 决定特定广播域上的相关 BUM 转发职责；不是“所有单播只有 DF 能发”。需要同时理解 Type 1 Ethernet A-D、Type 4 ES 路由、split horizon、aliasing 和 mass withdrawal。DF 算法及支持能力按设备版本核对。

双归属保护服务器接入，不能自动保护服务器 OS、应用或整机架电源。解释故障时区分 member link、leaf、peer-link/ES 控制面、spine 和 uplink。

## 6. 两种架构比较

Enterprise DC：EVPN/VXLAN 保留租户二层/三层隔离，防火墙与负载均衡需明确部署位置及对称路径。Large-scale DC：L3 to server 将路由延伸到主机/机架边界，减少二层范围，但要求主机路由、自动化和运维生态支持。不是“规模大就一定必须 BGP everywhere”。

设计题：为同一业务分别画 L2 overlay 和 L3 to server，列出移动性、地址管理、故障域、运维、硬件资源与迁移代价。选择其中一个，并写出不满足哪项条件时会改选另一种。
