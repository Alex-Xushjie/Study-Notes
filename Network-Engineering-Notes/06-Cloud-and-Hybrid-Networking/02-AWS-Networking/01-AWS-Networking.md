# AWS VPC、子网路由与Internet路径

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 子网名称不决定路径

VPC覆盖一个区域，子网位于一个AZ。Public/Private常描述路由与访问设计，不是随意起名就生效的属性。IPv4实例直接经Internet Gateway访问公网，需检查子网路由、实例公网IPv4/EIP映射及安全/系统策略；只有默认路由不够。

Private子网可把外网流量交给适当NAT设计，但外部不能因此任意主动连接私有实例。IGW、NAT Gateway、Transit Gateway与VPC Endpoint有不同目的，不能相互替换。

## 2. 路由表逐级判断

子网通过显式关联或主路由表获得路由。先找实际关联，再看目的前缀与下一跳状态。最长匹配是基础原则，但同前缀不同来源、Prefix List、Local路由及特殊转发有平台规则，查官方优先级而不是套传统管理距离。

示例：10.100.0.0/16→TGW，0.0.0.0/0→NAT。发往DC优先匹配更具体路由；如果10.100路由目标失效，不能假定会自动退到默认路由。Blackhole状态与不存在路由的行为要分别确认。

| 测试方向 | 核对项目 |
|---|---|
| 同VPC跨子网 | Local/自定义路由、安全规则、系统与监听 |
| 私网到DC | 子网表、TGW/接入链、DC回程 |
| 私网到公网 | NAT/出口路径、容量、映射及安全 |
| 公网到服务 | 入口LB/公网映射、监听、后端路径和规则 |

## 3. IPv6单独设计

IPv4 NAT不是IPv6默认设计。IPv6路由、地址与安全规则需另核对；Egress-only Internet Gateway用于相应IPv6出站场景，不是IPv4 NAT的另一个名字。双栈应用可能只在一栈成功，日志要注明实际地址族。

## 4. 常见故障

子网误用主表、实例没有预期地址、默认路由指向错误网关、回程走其他出口、NACL漏临时端口，都可能看起来像“VPC不通”。按资源ID检查，不凭控制台显示名称判断。

## 5. 实验

两子网两测试实例，先私网HTTP，再修改一个子网关联验证路径变化；不强制创建收费NAT或公网入口。保存路由与规则前后差异，恢复后验证无回归。

[VPC路由优先级](https://docs.aws.amazon.com/vpc/latest/userguide/route-tables-priority.html)、[Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)、[IPv6 Egress-only IGW](https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html)。
