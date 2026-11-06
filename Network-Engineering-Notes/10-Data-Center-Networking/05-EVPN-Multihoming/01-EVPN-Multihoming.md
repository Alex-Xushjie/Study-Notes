# EVPN多归属、ESI、DF与防环

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 多归属与MLAG不同

EVPN Multihoming通过Ethernet Segment及相关控制信息协调多台边缘设备，服务器可通过相应LACP等方式双接入。MLAG则有具体厂商的Peer/同步机制，二者不能把命令和故障行为互换。

ESI标识Ethernet Segment，不是每端口随意生成的标签；同一ES各节点与不同ES唯一性需按设计一致。All-Active和Single-Active有不同转发约束。

| 机制 | 作用 |
|---|---|
| Type1相关信息 | 多归属可达、批量撤销/别名等 |
| Type4 | ES发现和相关选举 |
| DF | 相应ES/业务范围的指定转发职责 |
| Split-horizon | 避免报文回到来源段形成环路 |
| LACP | 主机与网络的聚合关系，不等于EVPN控制 |

## 2. 不要把DF当全网主设备

DF影响相应范围的转发，尤其网络到多归属段的特定BUM处理；不意味着All-Active下所有已知单播都只能过DF。选举方式、粒度与增强能力按版本核对。

## 3. 故障与收敛

链路/节点失败需协调主机LACP、ES可达、路由撤销和硬件。控制面批量撤销有助收敛，但端到端还需考虑检测、主机重选和队列。跨厂商互通尤其需验证ES模型和支持。

## 4. 练习

双Leaf同ES接一台测试主机，验证已知单播、BUM、链路失败、节点失败和恢复。记录两端角色、LACP、Type1/4与实际流量，避免只看一个DF状态宣布无环无损。

[EVPN RFC7432](https://www.rfc-editor.org/rfc/rfc7432.html)、[DF扩展RFC8584](https://www.rfc-editor.org/rfc/rfc8584.html)。
