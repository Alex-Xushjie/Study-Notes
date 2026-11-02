# BGP、路由传播与云侧回程

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 用四个动词排错

收到、选中、安装、发布分别代表不同状态。CE从云网关收到前缀，不证明工作负载子网有回程；云路由表出现传播项，不证明检查设备允许；本地发布成功，不证明远端接受并用于转发。

对每个前缀写“权威来源—接收点—传播范围—查表入口—下一跳—返回路径”。多云与多区域不要默认所有路由自动传递。

## 2. 优先级不能跨平台照搬

最长匹配、路由来源、静态/传播、平台保留或特例，决定云侧选择。传统设备的管理距离、BGP属性与云路由表优先级并不是同一层概念。Local Preference通常影响本地BGP域，不能保证对端云回程。

教学例：主路径发布10.100.0.0/16，备路径发布10.100.10.0/24。到10.100.10.10可能优先走备路径，即使主线设计为“更优”。先查前缀长度，再查同前缀选择依据。

## 3. 传播与默认路由

云侧传播可简化更新，但应控制导入范围和默认路由来源。跨本地、云Transit、SD-WAN与旧MPLS互相重分发时，防止前缀返回原域再次变成有效来源。

默认路由到集中防火墙可能改变Internet出口，却未必覆盖更具体的云服务路径；相反错误汇总可把未存在的网段吸入黑洞。对缺失明细和平台特殊路径做反例验证。

## 4. 回程台账

| 流量 | 正向入口/表 | 返回入口/表 | 状态点 |
|---|---|---|---|
| DC→Prod | CE→云接入→Transit→子网 | 子网→Transit→DC连接 | 边界防火墙 |
| Prod→Shared | 业务表→Transit | Shared业务表→Transit | 共享服务检查 |
| 云→Internet | 子网→出口 | NAT映射→原子网 | NAT/代理 |

实际填资源ID而不是抽象名称。某个Peering、TGW或Hub能到达另一端，不表示工作负载关联到正确表。

## 5. 练习

依次删除本地发布、云传播、子网回程和检查许可，记录四种失败的不同证据。再让主路撤销但静态项仍在，验证是否发生Blackhole。只在纸面或隔离实验进行，不清现网路由。

[AWS优先级](https://docs.aws.amazon.com/vpc/latest/userguide/route-tables-priority.html)、[Azure路由](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)、[BGP属性基础](../../01-Routing-and-Switching/06-BGP/02-Attributes-and-Policy.md)。
