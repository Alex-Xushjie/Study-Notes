# Azure Hub-Spoke、Peering与集中检查

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. Peering是连接，不是完整Hub服务

Hub与App、Data分别Peering，不会仅因Hub存在就自动提供Spoke之间的传递转发。集中防火墙/NVA、网关Transit或托管Virtual WAN是不同架构，路径规则和管理对象也不同。

Peering涉及双侧连接状态及允许虚拟网络访问、转发流量、网关Transit/使用远端网关等相关选项。启用网关共享不等于自动插入防火墙；允许转发流量也不会替你创建UDR。

## 2. 集中检查推导

要求App 10.50.0.0/16访问Data 10.60.0.0/16的TCP5432必须经Hub防火墙。App业务子网需相应目的UDR，Data业务子网需相应返回路径，Hub设备还需转发、规则和路由。若有直连Peering等更具体路径，检查是否绕开设计检查点。

| 位置 | 要确认 |
|---|---|
| App | UDR关联、目标前缀、下一跳与有效路由 |
| Peering | 连接状态和所需转发选项 |
| Firewall/NVA | 许可、会话、转发、SNAT与下一跳 |
| Data | NSG/监听、返回UDR与有效路由 |
| 故障路径 | 备用检查点是否保持对称和隔离 |

不要机械对GatewaySubnet等平台专用子网套0/0到防火墙。托管服务有路由与子网限制，错误配置可能影响网关控制或数据路径。

## 3. Azure Firewall与NVA

托管Firewall与第三方NVA在HA、扩缩、状态、路由和许可方面不同。NVA需核对云NIC转发设置、操作系统转发、供应商部署模板与健康检查；仅有VM UP不代表支持Transit。

安全检查设计必须定义哪些流量被检查、何处NAT、谁保存原源地址，以及DNS和身份是否也经同一链。集中出口与Spoke互访可共享设备，但不能混为一条规则。

## 4. Virtual WAN识别范围

Virtual WAN采用托管Hub和相关路由/连接机制，不是传统Hub VNet的别名。选择时比较运维、连接形态、隔离、检查、费用与支持限制，避免把两种架构配置混用。

## 5. 练习

分别推导App→Data允许、App→Data其他端口拒绝、Data返回、单检查节点故障。只给App配置UDR制造非对称，用有效路由和防火墙日志证明原因，不用ping成功替代业务与检查验收。

[Peering与网关Transit](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview)、[Hub-Spoke参考](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke)。
