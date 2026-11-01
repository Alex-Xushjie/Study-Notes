# 链路聚合与LACP：协商、Hash和剩余容量

[路由交换学习目录](../Routing-and-Switching.md)

## 1. 聚合提供什么

LAG/Port-channel把多个物理成员组织为逻辑链路，转发和上层协议通常按逻辑对象使用，但成员仍有各自物理状态、速率和资源。聚合不把所有流量无条件逐包均匀切割，也不保证任一成员失败业务完全无感。

静态聚合缺少LACP的相应协商；LACP交换actor/partner等信息，帮助识别能形成同一聚合的成员。协议存在不替代正确接线与二层/三层配置。

## 2. 协商与转发状态

| 观察 | 需要解释 |
|---|---|
| Actor/Partner System ID | 每端以哪个系统身份参与 |
| Key/聚合归属 | 哪些成员可组成相应逻辑聚合 |
| Selected/Synchronized | 是否选入并同步到可用聚合 |
| Collecting/Distributing | 是否实际允许接收/发送相应聚合流量 |
| Individual/Suspended | 是否独立或暂停，行为依平台配置 |

active会主动发起相应协商，passive响应；两端都passive可能无法启动。静态on与LACP不是同一模式。不一致成员可能被排除，也可能因特定fallback行为产生意外路径，应查看实际状态。

## 3. Hash不等于单流叠加带宽

通常按源/目的MAC、IP、端口或封装字段等hash选择成员。可用字段与内/外层解析由ASIC/NOS决定。同一流常保持在一个成员，避免逐包重排；不同流也可能碰撞在同一成员。

双10G可增加多流总能力，但单流常受10G成员限制。4×25G中一个25G成员坏了，剩余75G是否足够，取决于业务与分布；平均总量低仍可能单成员过载。

不能为了追求表面均衡就盲目修改hash，全网会话可能重新映射。评估是否产生重排、微中断、CPU/网络观测差异，并安排回退。

## 4. min-links与容量目标

min-links可以在活动成员不足时让逻辑聚合不可用，使路由或上层选择其他路径。它是容量/故障策略，不是所有网络的固定值。

例：4×25G聚合承担80G关键流。剩3成员仅75G，此时是允许降级、触发替代100G路径，还是先做业务优先级？先回答，再配置阈值。max-bundle等能力也需核对双方与平台。[Cisco EtherChannel指南](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/etherchannel/etherchannel-configuration-guide/etherchannels.html)

## 5. 怎样验证

Cisco IOS XE只读示例：

~~~text
show etherchannel summary
show lacp neighbor
show etherchannel load-balance
show interfaces port-channel 10
~~~

summary看成员归属与状态，neighbor看对端身份，load-balance看配置的分流依据，逻辑接口看状态与计数。再下钻每成员CRC、丢弃、速率、VLAN/MTU。平台有预测hash工具时，它只覆盖指定字段与当前算法，仍需实际流验证。

## 6. 案例：部分连接超时

把失败按五元组分类，观察是否集中某成员。关闭该成员后恢复支持路径相关，但仍需核对两端VLAN、MTU、聚合状态与物理错误。只有一端显示bundled也不能证明另一端一致。

主机bond模式也要对应：active-backup不等于802.3ad，网工配置LACP前必须确认主机端。Linux概念见[VLAN与bond](../../03-Linux-Networking/03-Namespaces-and-Virtual-Networking/02-VLAN-and-Bonding.md)。

## 7. 验收

交付成员台账、hash依据、N-1/N-2容量、单成员/整组/对端故障记录。自测：成员UP等于Distributing吗？答：不等于。总量60G低于100G能排除某25G成员拥塞吗？答：不能。继续[多机冗余](02-MLAG-and-vPC-Failure-Modes.md)。
