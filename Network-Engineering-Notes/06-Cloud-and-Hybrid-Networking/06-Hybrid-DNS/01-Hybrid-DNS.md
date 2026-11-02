# 混合DNS、私有区与条件转发

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 名称解析是独立服务路径

DNS不是网络通后自动存在的附属品。查询从客户端到递归解析器，再按权威区或条件转发取得回答；解析结果所在地址的业务路径是另一条链。专线通但DNS查错区，应用仍会失败。

权威区保存记录，递归解析器替客户端查找，条件转发把特定后缀送到指定解析点。私有区的可见范围由VPC关联、VNet链接或规则等决定，不因在同一个组织账号体系就自动共享。

## 2. 两个方向分开

| 需求 | 一般设计方向 |
|---|---|
| 本地查云私有名 | 本地条件转发→云入站解析端点→关联私有区 |
| 云查本地内部名 | 云转发规则→出站解析路径→本地DNS |
| 云间共享私有区 | 按支持方式关联/链接和共享规则 |
| 访问私有服务 | 正常服务名→适当CNAME/私有记录→私有端点 |

AWS Route53 VPC Resolver的Inbound/Outbound Endpoint与规则属于各自对象；不要把VPC内预留解析地址当作本地可随意直连的通用DNS服务器。Azure Private Resolver的Inbound Endpoint、Outbound Endpoint与Ruleset也有不同用途。

## 3. 避免转发环路

若本地把cloud.example.com交云，云又把同一后缀交回本地，就可能反复转发直至超时。为每个后缀指定权威与转发出口，明确更具体后缀优先关系，避免把整个公共服务域粗暴覆盖。

私有区存在但缺少记录时，不能默认自动转去公网找答案；平台规则、私有区权威与回退选项需核对。创建过宽的私有区可能使同域其他服务突然NXDOMAIN。

## 4. 可靠性与安全

DNS端点需符合多AZ/子网要求，线路、网络规则、UDP/TCP53、转发目标及容量都要检查。较大回答、截断或DNSSEC等场景可能需要TCP，不能只放UDP53。

日志保存查询来源、后缀、结果与时间，评估是否包含敏感内部名称。DNS可见性不能替代应用授权，也不应将内部服务名误发布公网。

## 5. 练习

设计corp.example.com由本地权威、cloud.example.com由云私有区管理，画双向查询链与返回。再引入一个托管服务私有端点，按该服务官方DNS表配置，不能套一个通用privatelink后缀。

[AWS VPC Resolver](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html)、[Azure Private Resolver](https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview)、[Azure私有端点DNS](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns)。
