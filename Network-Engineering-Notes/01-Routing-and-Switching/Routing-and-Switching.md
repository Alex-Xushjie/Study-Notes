# 路由交换与互联网边界

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有路由交换经验的工程师，补强机制细节、状态依赖、设计取舍、验证与排错，不从IP地址/掩码的零基础课程重写。11个专题、25篇正文构成当前完整初版，另有本学习导航。

文档完成不代表你已完成实验、达到某个职级或具有生产经历。不同厂商、NOS、ASIC与版本的命令、缺省策略和故障保护存在差异，正文使用的例子要按实际平台验证。

## 全部专题与文章

| 专题 | 文章 |
|---|---|
| 01 以太网与VLAN | [01 转发状态与VLAN](01-Ethernet-and-VLAN/01-Ethernet-and-VLAN.md)；[02 逐跳报文与二层故障](01-Ethernet-and-VLAN/02-Packet-Walk-and-L2-Cases.md) |
| 02 生成树 | [01 STP/RSTP](02-STP/01-STP.md)；[02 MSTP与保护机制](02-STP/02-MSTP-and-Protection.md) |
| 03 聚合与多机冗余 | [01 LACP、Hash与容量](03-Link-Aggregation-and-Multichassis/01-Link-Aggregation-and-Multichassis.md)；[02 MLAG/vPC故障域](03-Link-Aggregation-and-Multichassis/02-MLAG-and-vPC-Failure-Modes.md) |
| 04 路由与转发 | [01 RIB/FIB、递归与ECMP](04-Routing-and-Forwarding/01-Routing-and-Forwarding.md)；[02 重分发、汇总与防环](04-Routing-and-Forwarding/02-Redistribution-Summarization-and-Loop-Prevention.md) |
| 05 OSPF | [01 建邻与邻接](05-OSPF/01-OSPF.md)；[02 LSA、区域与NSSA](05-OSPF/02-LSA-Areas-and-NSSA.md)；[03 选路与收敛](05-OSPF/03-Path-Selection-and-Convergence.md)；[04 综合排错](05-OSPF/04-OSPF-Troubleshooting.md) |
| 06 BGP | [01 会话与地址族](06-BGP/01-BGP.md)；[02 属性与策略](06-BGP/02-Attributes-and-Policy.md)；[03 iBGP、RR与规模](06-BGP/03-iBGP-Route-Reflectors-and-Scale.md)；[04 排错与变更](06-BGP/04-BGP-Troubleshooting-and-Changes.md) |
| 07 VRF与路由互通 | [01 隔离、RD/RT、泄漏与回程](07-VRF-and-Route-Leaking/01-VRF-and-Route-Leaking.md) |
| 08 高可用与故障检测 | [01 VRRP/HSRP与Tracking](08-High-Availability-and-Failure-Detection/01-High-Availability-and-Failure-Detection.md)；[02 BFD与恢复测量](08-High-Availability-and-Failure-Detection/02-BFD-and-Convergence-Measurement.md) |
| 09 IPv6 | [01 地址、ND、RA与SLAAC](09-IPv6/01-IPv6.md)；[02 双栈与PMTU排错](09-IPv6/02-Dual-Stack-and-Troubleshooting.md) |
| 10 QoS | [01 分类、队列与速率控制](10-QoS/01-QoS.md)；[02 Buffer、Microburst与验收](10-QoS/02-Buffers-Microbursts-and-Validation.md) |
| 11 Internet Edge | [01 互联、路由范围与运营](11-Internet-Edge/01-Internet-Edge.md)；[02 授权、ROV与DDoS处置](11-Internet-Edge/02-RPKI-Filtering-and-DDoS.md) |

每层目录从01编号，正文在所属专题内从01重新开始。导航文件按主题命名，不参与正文编号。

## 三条阅读路径

企业/WAN/混合云：先确认01–04的转发与冗余，再深入05/06、07/08和09；10/11用于容量、出口和运营边界。主机与安全设备出现时，连接Linux和后续安全专题。

量化/低延迟：优先01–04、06/08、10/11，随后连接独立组播与Linux性能部分。不能只熟悉BGP会话却跳过包长、hash、队列与主机消费。

园区运维：重点01–05、07–10，再连接无线、身份、安全和远程接入。拓扑图应同时包含VLAN、三层网关、身份与基础服务依赖。

不按目录顺序强制重读已掌握内容。每个主题至少用一个反例确认理解：为什么接口UP仍失败，为什么2-Way可以正常，为什么Valid仍不能证明无泄漏。

## 机制与证据的统一要求

先写业务流与正常路径，再对照协议、RIB、FIB、邻接和实际应用。配置表示意图，状态表示当前机制，数据与应用结果表示实际行为。

每个案例区分事实、假设、区分实验和结论边界。恢复业务与确认根因可分阶段，不能因shutdown某链路后恢复就省略因果验证。

所有示例使用实验私网/文档地址与相应隔离ASN。不要向公网或真实运营商发布测试前缀、黑洞或FlowSpec；本文桌面演练不代表已执行运营操作。

## 实验与作品集

| 范围 | 当前可用入口 | 可证明与待补边界 |
|---|---|---|
| Linux三层、回程与MTU | [Linux实验L1–L5](../../Network-Career-Lab/01-Linux/02-Labs.md) | 主机/软件功能；不替代ASIC与设备协议实验 |
| BGP双出口与发布边界 | [FRR边界E1–E3](../../Network-Career-Lab/04-Internet-Edge/02-Labs.md) | 属性、过滤与故障逻辑；Null0阶段不证明业务可达 |
| OSPF | 本部分05专题的双节点/多区域推导与验证要求 | 需自行准备相应FRR/NOS拓扑并记录实测 |
| STP、LACP、多机冗余 | 02/03专题的故障矩阵 | 需支持相关功能的设备/镜像，不以Linux桥接代替全部厂商行为 |
| VRF、IPv6、QoS | 相应专题的矩阵、公式与负载验证 | 根据实际平台完成；软件功能不等于硬件性能 |

每阶段留下一份拓扑/地址/版本台账、正常与异常/恢复状态、实际流量证据、单变量变更和复盘。引用[实验记录模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，不要把教材数值抄成自己实测。

建议代表成果：双出口与防泄漏方案、多区域OSPF故障报告、园区多机冗余矩阵、QoS与N-1容量验证。项目是否生产实施应如实注明。

## 资料与版本

各篇链接协议RFC、FRR、Cisco与Arista等原始资料。RFC可能被更新，实施时核对更新关系与实际支持；例如VRRPv3本版引用RFC9568，未继续把RFC5798作为最新规范。

FRR命令在vtysh中，Cisco/Arista命令在相应NOS中，Linux命令在Linux中。不能把所有代码块当同一个Shell脚本执行；配置片段也不自动准备接口、进程、对端、回程和持久化。

## 本次验证范围

已检查正文覆盖、文件编号、本地链接、代码围栏与示例计算。所有输出、拓扑和案例为教学设计或推演；本次未在FRR、交换设备、真实ISP、ASIC队列或IPv6环境执行实验，未产生实测收敛或性能结论。
