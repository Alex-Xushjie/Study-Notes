# AWS Transit Gateway、Peering与混合连接

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. Peering不自动提供Transit

A与B、B与C分别Peering，不表示A可经B到C。每侧需配置相应路由与安全策略，地址重叠等限制另查。需要多网集中互联时，应选择支持相应Transit能力的架构，不用更多Peering连线掩盖非传递性。

TGW通过Attachment连接VPC及其他支持的连接。VPC子网路由与TGW路由表是两层对象，云内路由不是只改一张表。

## 2. Association与Propagation

Association决定流量从某Attachment进入TGW后使用哪张TGW路由表；Propagation决定某连接的路由被发布到哪些表。一个Attachment通常关联一张表，却可按支持范围向多张表传播；部分类型如Peering需静态等专门配置，不能默认所有Attachment都自动传播。

示例：Prod/Dev入口关联workload表，只含Shared/DC；Shared入口关联shared表，含Prod/Dev/DC。Prod→Shared先查Prod子网表，再查workload；返回查Shared子网表与shared。Dev要到Prod时workload不应有可达路径，仍需防止Shared主机/代理变成未授权中转。

## 3. DX与VPN

Direct Connect连接、VIF、DX Gateway、TGW与VPN Attachment不是同一资源。对照实际接入类型、允许前缀和关联关系逐级检查。BGP建立只证明对应控制连接，仍要核对子网路由、TGW查表、回程和安全。

主专线/备VPN的云侧优选受前缀长度、路由来源和具体服务规则约束。静态路由可能比传播路由优先并在故障后保留，不应把一条静态当成自动备份而不验证。

## 4. 可用区与检查路径

为VPC Attachment选择的子网/AZ影响资源如何使用TGW。中央检查还涉及防火墙与对称路径，必要时采用适配的Appliance Mode等能力；它不是一开就解决所有NAT、路由与设备HA问题。

## 5. 实验交付

完整填写Prod/Dev/Shared/DC的“入口Attachment—关联表—目的前缀—出口Attachment—返回表”。再误关联Dev到shared，说明隔离为什么可能被破坏；恢复后用拒绝与允许流验证。

[TGW路由表](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-route-tables.html)、[TGW工作机制与限制](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html)、[VPC Peering路由](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-routing.html)。
