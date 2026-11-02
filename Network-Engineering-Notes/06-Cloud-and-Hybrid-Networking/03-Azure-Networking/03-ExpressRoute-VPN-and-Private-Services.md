# ExpressRoute、VPN与Azure私有服务

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 连接层次

ExpressRoute电路、对等类型、接入位置、Gateway/连接、VNet路由分别属于不同层次。Private Peering用于相应私网场景，不能把所有Microsoft服务访问都归到同一私网路径。S2S VPN依赖公网承载与IPsec，P2S则面向客户端接入，目的不同。

双BGP/双连接可能仍共享一个接入位置、运营商最后一公里或客户设备。任一接入位置失效的目标需要位置与客户侧/承载侧的多样性，而不只是会话数量。

## 2. 主备与回程

设计专线主、VPN备时，两端都需按实际路由规则优选。更具体前缀会影响选择，不能只改本地Local Preference就推断Azure回程。网关、传播、UDR和架构特例需结合有效路由查证。

VPN带宽、MTU、时延和会话恢复可能与主路径不同。Microsoft Peering流量不能直接套用Private Peering的VPN备份结论。按业务前缀和服务类型逐项验收。

## 3. 加密

ExpressRoute默认不加密。可适用的MACsec只保护相应物理链路范围，IPsec保护范围由隧道端点决定。需要端到端业务保护时，还应考虑应用TLS，不能把任一层加密等同所有层安全。

## 4. Private Endpoint与Service Endpoint

Private Endpoint为特定服务资源提供VNet中的私有接入对象/地址，需要DNS把正常服务名解析到正确私有目标。Service Endpoint是另一种服务访问与网络身份约束机制，并不等于给服务生成同样的私有NIC/IP；也不能默认让本地经专线像访问Private Endpoint一样使用。

专线通、域名仍解析公网，是常见故障组合。Private Endpoint建立不会自动替所有本地DNS服务器创建正确转发；服务公网入口是否禁用也要单独设置并验证。

## 5. 验收

从云VM和本地客户端分别验证解析、TLS主机名、端口与权限，再验证专线切VPN、两地接入及恢复。报告服务资源/子资源、私有地址、DNS区、VNet链接与路径；不同PaaS服务的端点和DNS细节需查对应文档。

[ER与VPN备份](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/hybrid-networking/expressroute)、[ER加密](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-encryption)、[Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)、[Service Endpoint](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)。
