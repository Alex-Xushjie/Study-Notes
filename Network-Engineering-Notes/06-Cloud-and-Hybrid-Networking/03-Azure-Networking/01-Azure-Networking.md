# Azure VNet、UDR、NSG与有效状态

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 资源组织

Tenant、Subscription、Resource Group分别涉及身份/组织、订阅与资源管理，VNet/子网涉及网络结构。资源组不同不代表网络不通，同一订阅也不表示自动互通。VNet为区域级，子网不限定单一AZ，跨AZ部署需另确认工作负载与网关能力。

Azure提供系统路由，用户可通过UDR（用户定义路由）及适用的BGP学习路由改变路径。先查业务网卡/子网的有效路由，而不是只看自己创建的Route Table对象。

## 2. 路由选择

基本上先比较目的前缀长度；同前缀通常UDR优于BGP，BGP优于系统路由，但存在VNet/Peering/Service Endpoint等平台特例。默认路由不会压过更具体路由，禁用传播也不等于消除所有系统路径。

10.60.0.0/16→Virtual Appliance用于把App到Data送给防火墙；还要核对防火墙转发与Data返回。下一跳填写了一个私网IP，不代表该设备具有转发和安全服务能力。

## 3. NSG

NSG有优先级与允许/拒绝规则，具有状态跟踪，可关联子网或NIC。若两处都存在适用规则，要满足两处约束；不能只查NIC规则就忽略子网。有效安全规则辅助整合实际作用对象。

Service Tag和Application Security Group是组织规则的工具，含义与更新方式不同，不能当成AWS SG引用的完全同义实现。规则变更后旧会话行为也不能只用一次新连接推断。

## 4. 显式出口

出站公网能力应显式设计为NAT Gateway、合适的LB出站、Firewall/NVA或其他支持方式。不要依赖历史上某些部署的隐式默认出站；默认行为随创建方式和平台更新变化。入口、出口及回程要独立描述。

## 5. 实验

两测试子网查看NIC有效路由/安全规则，然后加一条只针对测试目的的UDR，比较配置对象、有效状态与HTTP结果。下一跳无服务时失败应符合预期；恢复后检查路由关联也恢复，而不是只删一条显示出来的路由。

[Azure路由及特例](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)、[NSG](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)、[默认出站与显式迁移](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access)。
