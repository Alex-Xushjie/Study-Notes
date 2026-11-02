# 私有服务访问与公网暴露边界

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 私有访问的四个问题

谁能解析到服务？谁能路由到入口？谁被网络规则允许？谁有应用/IAM权限？四者缺一都可能失败；同时四者也应按最小权限设计。私有地址不是身份验证，创建端点也不是禁用公网的同义操作。

| 机制 | 学习重点 |
|---|---|
| AWS Interface Endpoint | 服务对应的端点ENI/私有地址、安全规则、DNS与策略 |
| AWS Gateway Endpoint | 支持服务的路由表集成，和Interface模型不同 |
| Azure Private Endpoint | 服务资源/子资源、私有IP、审批及私有DNS |
| Azure Service Endpoint | 服务侧网络约束与访问路径，不是私有IP替身 |

AWS Gateway Endpoint主要用于支持的S3/DynamoDB场景，不应推断为本地经VPN/DX通往服务的通用入口。Interface Endpoint是否可从本地/其他网络访问，取决于实际服务、路由、DNS和策略。

## 2. Endpoint Policy与服务权限

某些端点支持策略限制可访问资源/主体，但不会自动授予服务权限。资源策略、身份权限、端点策略与网络约束应综合判断。能连TCP443但被服务拒绝，不应该继续放宽SG试图修复权限。

## 3. 名称与TLS

应用通常仍使用服务域名，不要永久写死端点IP。直接用IP访问HTTPS可能导致证书主机名错误、SNI不匹配或打到错误虚拟主机。排错用指定解析的方式保留正常主机名，不把关闭证书验证作为最终修复。

## 4. 暴露面复核

检查公网入口是否仍可达、公共访问设置、端点审批、路由与DNS可见性、日志是否可追踪主体。一个资源同时有私有和公网入口时，要分别验收，不能因为私网请求成功就宣布已关闭公网。

## 5. 练习

设计一个云存储私有访问：云工作负载、本地运维和第三方访问各有路径与权限。分别制造解析公网、私网不可达、网络许可但IAM拒绝三种故障，提交能区分的证据链。

[AWS私有服务访问](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html)、[AWS Gateway Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)、[Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)。
