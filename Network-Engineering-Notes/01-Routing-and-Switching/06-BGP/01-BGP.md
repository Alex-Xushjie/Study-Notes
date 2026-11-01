# BGP会话、地址族与路由生命周期

[路由交换学习目录](../Routing-and-Switching.md)

## 1. BGP交换的是带策略的可达性

BGP按邻接关系传播前缀与属性，不自动测量每条业务链路的实际质量。eBGP连接不同AS，iBGP在同一AS内传播；一个AS可以跨多站点，但不意味着所有节点天然共享路由表。

BGP会话、某地址族激活、某前缀接收、最佳路径、RIB/FIB与业务成功，至少是六种独立结果。排错必须逐层确认。

## 2. 会话建立与报文

常见基于TCP179建立会话，发起端也会使用相应临时端口，不能把所有方向五元组都限定源/目的179。OPEN协商标识、AS、能力等，KEEPALIVE维护，UPDATE发布/撤销，NOTIFICATION报告相应错误；Route Refresh等属于协商能力扩展。

| FSM状态 | 第一层理解 | 候选检查 |
|---|---|---|
| Idle | 尚未进行有效连接等状态 | 配置、管理关闭、重试原因 |
| Connect/Active | TCP建立相关过程 | 路由、源地址、ACL、端口和重试 |
| OpenSent/OpenConfirm | 协议协商中 | ASN、参数、能力与通知 |
| Established | 会话已建立 | 继续查地址族和目标前缀 |

Active不是“正在健康转发”。Router ID是协议标识，与TCP源地址不是同一对象。Loopback建邻还需明确update-source、回程、多跳与相应安全策略。[BGP RFC4271](https://www.rfc-editor.org/rfc/rfc4271.html)

## 3. 地址族为何重要

AFI/SAFI标识交换何种网络信息，例如IPv4 unicast、IPv6 unicast、EVPN。TCP会话可承载多个地址族，但双方能力与配置需匹配。邻居Established而IPv4前缀为0，可能仅是未激活或被策略过滤，并不自动是传输层故障。

## 4. 从收到前缀到发布出去

可以按接收信息→import策略→可用候选→最佳/多路径→RIB/FIB→export策略→邻居实际接收来跟踪。Adj-RIB-In、Loc-RIB、Adj-RIB-Out是逻辑模型，平台未必把全部原始副本永久保存供CLI读取。

received-routes类视图可能依赖soft-reconfiguration或其他支持，不能为了看输出不评估规模就全网保留所有原始路由。选路还需下一跳可达与策略资格。

## 5. FRR验证命令

在vtysh内：

~~~text
show bgp ipv4 unicast summary
show bgp ipv4 unicast neighbors 192.0.2.2
show bgp ipv4 unicast 198.51.100.0/24
show ip route 198.51.100.0/24
~~~

邻居地址/前缀按隔离实验替换。summary看FSM和相应计数，neighbor看能力、计时与策略，前缀明细看路径与有效性，RIB看实际采用。Linux再查内核路径；硬件设备再查对应FIB/邻接。[FRR BGP文档](https://docs.frrouting.org/en/latest/bgp.html)

## 6. 默认策略与network语句

现代安全设计要求明确import/export，RFC8212规定了相应缺省拒绝原则，实际NOS版本/profile的默认行为仍要验证。不能看到旧实验无策略可交换，就把它当生产默认。[RFC8212](https://www.rfc-editor.org/rfc/rfc8212.html)

network公告通常依赖本地相应精确前缀存在及平台检查条件。仅配置network 203.0.113.0/24，不会替你建立真实业务子网。放Null0使它具备起源条件时，只能验证控制面，不能据此要求业务ping通。

## 7. 案例与验收

邻居Active：先用正确源到对端查询路径/回程，再看TCP与通知；Established但零路由：看地址族、双方公告与策略；有路由不通：继续下一跳与数据面，不反复重建会话。

交付一个前缀从起源到远端实际接收的状态链。私有ASN与文档地址只用于隔离环境。继续[属性与策略](02-Attributes-and-Policy.md)。
