# OSPF建邻与邻接：从Hello走到Full

[路由交换学习目录](../Routing-and-Switching.md)

## 1. 先区分三个结果

Neighbor表示发现了邻居，Adjacency表示建立了同步链路状态数据库所需的邻接，Route表示计算并采用了到某前缀的路径。它们按依赖相连，但不能互相替代。

本篇以OSPFv2/IPv4为主。OSPF使用IP协议号89，不使用TCP/UDP端口；组播与单播使用方式取决于网络类型。Router ID是32位标识，不要求当前数据路径必须使用它作为实际源地址，但应稳定且避免域内冲突。

## 2. 网络类型决定邻接模型

| 类型 | 常见对象 | 重点 |
|---|---|---|
| Point-to-Point | 两端互联 | 通常无DR/BDR，核对两端模型 |
| Broadcast | 多接入以太网 | DR/BDR与DROTHER关系 |
| NBMA/Point-to-Multipoint | 特定多点接入 | 发现方式、计时、下一跳与设计 |

物理以太网不代表只能使用broadcast OSPF类型；接口类型是协议配置的一部分。改类型会影响邻接、LSA和路径，不能只为消除2-Way而修改。

## 3. 邻居状态逐步回答什么

Down/Attempt与发现条件相关；Init表示已收到对方Hello但尚未看到双向确认；2-Way表示在对方信息里看到了自己。之后是否建立完整邻接要按网络类型和角色决定。

ExStart协商数据库交换角色与序列等，Exchange交换数据库描述，Loading请求缺少信息，Full表示相应数据库同步完成。DBD是数据库描述，LSR是请求，LSU携带更新，LSAck确认；这些报文不是用户业务流。

同一broadcast网段中，两个DROTHER维持2-Way通常正常；它们与DR/BDR建立相应完整邻接。不能要求全网每对邻居都Full。[OSPF规范](https://www.rfc-editor.org/rfc/rfc2328.html)

## 4. DR/BDR选择与非抢占

参与资格和比较涉及接口优先级、Router ID及现有选举状态。优先级0表示不参与相应选举。DR/BDR选择通常不因为后来加入更高优先级设备就立即抢占，不能只看配置预期决定当前DR。

选举减少多接入网段的同步关系，不表示所有单播业务必须经DR转发。改优先级前写清当前状态、是否需计划重选及影响。

## 5. 建邻条件清单

核对接口地址/二层可达、区域与区域类型、认证、Hello/Dead计时、网络类型、Router ID、策略与MTU相关交换条件。不同网络类型对掩码等检查不同，不把一个以太网检查表机械套给所有链路。

链路UP但Init：双向Hello路径可能不通；卡ExStart/Exchange：MTU、重复RID、协商与链路丢包等值得调查；Loading反复：查看LSR/LSU重传和具体缺失对象。状态是线索，不能仅凭一项就确定根因。

## 6. FRR最小配置读法

先在两台隔离实验VM准备FRR、启用zebra/ospfd并配置实际接口。假设R1/R2互联192.0.2.1/30、192.0.2.2/30，分别有10.1.1.1/32与10.2.2.2/32实验loopback，转发条件已按拓扑准备。

R1在vtysh配置模式中的示例：

~~~text
router ospf
 ospf router-id 10.255.0.1
 network 192.0.2.0/30 area 0.0.0.0
 network 10.1.1.1/32 area 0.0.0.0
~~~

R2对应使用RID10.255.0.2和loopback10.2.2.2/32。network语句用于匹配并启用相应接口参与区域，并非凭空生成任意不存在的网络。接口地址、进程启用与操作系统持久化不由这段配置自动完成。[FRR OSPF文档](https://docs.frrouting.org/en/latest/ospfd.html)

## 7. 验证与作业

~~~text
show ip ospf
show ip ospf interface
show ip ospf neighbor
show ip route ospf
~~~

分别看实例、接口类型/计时/区域、邻居状态和路由。再验证loopback前缀与真实主机的正反路径，不能只截邻居截图。

作业：同一broadcast网段放四台路由器，解释两台DROTHER为何2-Way；再比较两端P2P模型。记录实际平台与状态，示例不是本次实跑。继续[LSA与区域](02-LSA-Areas-and-NSSA.md)。
