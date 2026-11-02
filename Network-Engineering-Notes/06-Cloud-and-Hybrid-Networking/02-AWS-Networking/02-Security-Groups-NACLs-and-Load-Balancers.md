# AWS安全规则、负载均衡与端点判断

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. SG与NACL的差别

Security Group关联到相应资源/网卡，采用允许规则并具有状态跟踪；多个关联SG的允许范围会组合，不是按SG顺序先拒绝后允许。Network ACL作用于子网边界，是无状态、有序的允许/拒绝规则，需要分别处理返回流量。

| 条件 | SG思路 | NACL思路 |
|---|---|---|
| HTTPS入站 | 允许正确来源到服务端口 | 入站服务端口、出站返回临时端口 |
| 客户端出站 | 出站目标/端口及状态 | 出站服务端口、入站临时端口 |
| 修改规则后 | 已有连接可能受跟踪状态影响 | 核对独立方向和命中规则 |

SG引用不是跨网络任意可用的身份标签，支持的连接形态和限制需查平台。中间设备NAT改变源后，服务端看到的来源也可能不同。不要为了省事把源扩大到0.0.0.0/0。

## 2. 应用入口与负载均衡

ALB面向应用层，NLB面向传输层，适用协议、源地址行为、健康检查与目标类型有差异。Internal与Internet-facing影响可达入口；前端可达不等于后端健康。

排错按客户端→LB监听→目标组→后端监听/规则→应用依赖分段。健康检查可能使用与业务不同的端口、路径和来源；后端健康也不证明某个业务URL、登录或依赖正常。

## 3. 源地址与证据

应用日志的客户端地址可能来自连接源，也可能来自受信代理提供的首部；不要把任意X-Forwarded-For当作可信身份。NAT、LB与检查设备前后分别记录五元组，才能关联流日志。

## 4. 故障练习

场景A只漏NACL返回临时端口：TCP建立失败；场景B服务监听127.0.0.1：平台规则正确也不能外部访问；场景C健康检查URL成功但业务依赖数据库失败：LB状态绿仍返回错误。分别提出能区分三者的证据。

规则回退后以新连接与实际事务验证；不要无范围清空生产状态表。拒绝测试也需确认目标与端口正确。

[SG规则与状态](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)、[NACL机制](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)、[ALB工作机制](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)、[NLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)。
