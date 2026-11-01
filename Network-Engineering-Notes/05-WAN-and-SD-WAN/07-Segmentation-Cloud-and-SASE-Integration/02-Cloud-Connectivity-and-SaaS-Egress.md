# 混合云、SaaS出口与云侧回程

[返回WAN与SD-WAN目录](../WAN-and-SD-WAN.md)

## 1. 区分三种目的

企业访问云中私有业务、访问SaaS和访问公网服务，是三种不同路径。云专线、站点VPN、SD-WAN虚拟Edge及安全PoP可能组合使用，但每增加一层就增加路由、状态、MTU与费用边界。

| 方案 | 常见目的 | 关键检查 |
|---|---|---|
| 云专用连接 | 稳定的私网互联 | 接入位置、双连接故障域、加密需求 |
| Internet IPsec | 快速接入/备份 | 网关能力、隧道、路由、带宽与抖动 |
| 云中SD-WAN Edge | 统一Overlay策略 | 虚机/网卡、HA、授权、云路由与转发设置 |
| 本地DIA/SASE | SaaS就近访问 | DNS、出口IP、身份、安全PoP与回程 |

云专线默认加密与否要查具体服务，不能因为不经公网就假定已加密。例如ExpressRoute默认流量不加密，MACsec或IPsec有不同保护范围与支持条件。

## 2. 云侧路由不自动跟随

边缘学到VPC/VNet前缀，不代表云工作负载的子网路由表已指向正确出口。云侧可能涉及网关、Transit/Hub路由表、传播、关联、静态路由、NVA转发设置及安全策略。按具体云平台逐项检查，不混用AWS与Azure术语。

状态设备前后路由不一致会造成非对称。多区Edge、双隧道和网关HA也可能存在吞吐、会话和路由限制，部署两台虚机本身不是完整高可用方案。

## 3. 专线加VPN备份

必须分别设计企业到云和云到企业的优选，核对前缀长度、路由来源和云侧选路规则。不同产品对静态/动态、传播/显式路由的优先关系不同，不能统一写“BGP Local Preference会控制所有回程”。

备份只承载关键业务还是全部业务要在容量和策略中落实。1Gb/s专线故障后改走100Mb/s VPN，路由成功不等于业务目标仍满足。

## 4. SaaS体验

本地出口减少绕总部，不保证更快：DNS解析位置、CDN/服务端入口、安全检查、ISP互联和用户所在地共同决定。切出口可能改变公网IP，导致白名单、条件访问或会话重新认证。

测量用实际HTTPS事务、登录与核心动作，不只ping域名。DNS、TCP/TLS、首字节和完整事务时间分开记录，必要时对照不同出口的解析结果。

## 5. 验收

对主/备路径分别验证企业→云、云→企业、共享服务、拒绝访问、MTU、大文件和长会话。云资源与专线可能计费，教材不自动创建资源；实验先在已有隔离环境完成逻辑设计。

[Azure专线与VPN备份](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/hybrid-networking/expressroute)、[ExpressRoute加密](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-about-encryption)、[AWS Direct Connect韧性工具](https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html)、[AWS VPN路由选项](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNRoutingTypes.html)。
