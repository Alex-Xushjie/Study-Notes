# VLAN子接口与bond：认识Linux的逻辑网卡

[Linux学习目录](../Linux-Networking.md)

## 1. 先理解父接口、子接口和成员

物理网卡把主机接到链路；VLAN子接口为特定标签提供逻辑端点；bond把多块接口组织为一个逻辑链路。parent表示承载下层，member表示被聚合管理，两种关系不同。

~~~text
ens160 ─┐
         ├─ bond0 ─ bond0.100 ─ 地址10.100.0.10/24
ens192 ─┘
~~~

本例地址位于VLAN100的三层端点bond0.100。不要看到物理成员没地址就认定配置缺失，也不要在所有层重复配置相同子网。

## 2. VLAN子接口名字不一定等于配置

bond0.100是常见命名约定，实际VLAN ID由设备属性决定；一个自定义叫prod的子接口也可能承载VLAN100。用详细查询核对：

~~~bash
ip -d link show
ip -br address show
~~~

-d是details，输出中的vlan id才是标签依据。Linux配置子接口不会自动修改交换机trunk，必须同时核对对端允许VLAN、native/untagged约定、MTU与端口状态。

父口抓不到期望标签时，先确认抓包位置、虚拟化和offload，再判断线上是否缺标签。子接口与父口看到的内容可能不同。

## 3. bond不是一律LACP

| 模式 | 主要用途 | 对端要求与边界 |
|---|---|---|
| active-backup | 一主一备链路切换 | 不应默认要求对端配置LACP；二层可达等条件仍需满足 |
| 802.3ad | 与对端协商聚合、按策略分流 | 两端LACP与相应聚合一致，跨设备需对端支持 |

bond0是自定义名称，802.3ad是聚合模式。miimon等检测参数解决特定链路检测问题，不一定能发现远端上游黑洞。双10G聚合常能提高多流总能力，不能保证单条连接20G。[内核bonding说明](https://docs.kernel.org/networking/bonding.html)

## 4. 用三个观察层次验证

~~~bash
ip -d link show dev bond0
cat /proc/net/bonding/bond0
ip -s link show dev bond0
~~~

第一条看逻辑设备；第二条读内核提供的bond状态文件，关注模式、活动成员/aggregator、成员状态；第三条的-s是statistics，显示相应计数。设备不存在时应先用真实名称，不能照搬bond0。

比较逻辑口与各成员的流量、错误和切换时间；不要把多个层次统计简单相加当独立线上包数。LACP细节还要与交换机两端对照。

## 5. 故障案例

一部分连接通、一部分不通，可能是某成员的VLAN/MTU不一致，也可能是ECMP或其他路径差异。按源/目的与五元组分组，再对比成员计数和对端状态。active-backup切换后短暂丢包还需检查MAC/邻居更新与业务重试。

## 6. 验收

先画清物理成员→bond→VLAN→地址的关系；在专用实验口做单成员故障，记录实际路径、协议状态、业务恢复和是否回切。具体搭建步骤见[实验手册L4](../../../Network-Career-Lab/01-Linux/02-Labs.md)，管理接口不参与实验。

自测：接口名带.100是否足以证明VLAN100？答案：不够，要查属性。active-backup是否等同LACP？答案：不是。成员UP是否证明上游业务可达？答案：不是。
