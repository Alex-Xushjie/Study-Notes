# 云网络：先画每一跳，再讨论产品

## 1. 将传统网络映射到云

VPC/VNet 是逻辑网络边界，subnet 是地址与部署边界，路由表决定下一跳，SG/NSG/NACL 决定允许哪些通信。不要把云子网当成能随意运行 STP、HSRP 和二层广播的交换机 VLAN。平台提供的默认行为、托管网关和安全策略都是设计输入。

学习时给每个连接写五元组、正向路由、回程路由、过滤规则和 DNS 解析位置。云平台的“connected”标记不能代替端到端业务探测。

## 2. AWS 必备概念

| 对象 | 作用 | 需要回答的问题 |
|---|---|---|
| VPC / Subnet | 地址空间；子网属于单个 AZ | 地址重叠如何影响互联？ |
| Route table | 子网关联的转发决策 | 最长前缀、静态/传播路由怎么选？ |
| Security Group | 资源网络接口层面的有状态允许规则 | 允许连接后返回流量如何处理？ |
| NACL | 子网层面的无状态允许/拒绝规则 | 回程临时端口是否放行？ |
| IGW | VPC 的 Internet 网关 | 实例是否还有公网地址、路由和安全规则？ |
| NAT Gateway | 私网发起访问的地址转换 | AZ 故障、路径和计费怎样设计？ |
| VPC Peering | 两个 VPC 的直接互联 | 为什么 A↔B、B↔C 不自动等于 A↔C？ |
| Transit Gateway | 汇聚多个网络 attachment | 入站 attachment 关联哪个路由表？ |
| PrivateLink | 通过端点私有访问服务 | 需要整个网互通还是仅访问一个服务？ |
| VPN / Direct Connect | 加密隧道 / 专用网络连接 | 私有连接是否满足加密要求？ |

SG 有状态、NACL 无状态是定位回程故障的关键，但中间设备、路由和流量路径也会影响结果。按官方 [VPC 安全入口](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security.html) 继续阅读 SG 与 NACL 规则，记录示例五元组。

TGW 的 **association** 决定从某 attachment 进来的包查哪张 TGW 路由表；**propagation** 决定该 attachment 的路由传播到哪些表。VPC 子网到 TGW 的路由还要独立配置，不能只检查 TGW 侧。TGW 也不会自动解决重叠 CIDR 或 DNS 解析。参考 [TGW 工作原理](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html) 的 route tables 和 attachments。

设计例：生产和开发分别进入不同 TGW 表，两个表都可到共享服务，但彼此没有互访路由；共享服务返回时必须能找到相应网络。若需求允许单向发起但不允许反向发起，需要有状态安全控制，不能只靠缺失回程路由。

## 3. Direct Connect 的正确链路

```text
On-prem CE → DX connection → transit VIF → DX Gateway → Transit Gateway → VPC attachment → subnet
```

这是一种接 TGW 的常见路径，不应把 DX 直接画成一根线插进 TGW 而省略逻辑组件。接 VGW 的方案则涉及不同 VIF/网关选择。分别核验 BGP 收发前缀、允许前缀、VPC/TGW 路由及回程。

HA 看故障域：两条逻辑会话、两台 CE、两个物理接入、两个 DX location、运营商物理路由是不同层级。VPN 备份还要核对带宽、MTU、选路和故障时容量。按 [AWS DX Resiliency Toolkit](https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html) 比较多地点冗余模型；不要仅凭“两条线”写出 SLA 保证。

## 4. Azure 必备概念

| 对象 | 作用 | 与 AWS 类比时的边界 |
|---|---|---|
| VNet / Subnet | 地址与资源组织 | 不把 AWS AZ/subnet 规则直接照搬 |
| NSG | 子网/NIC 上的有状态规则 | 优先级、默认规则须单独核对 |
| UDR | 用户自定义路由 | 与系统路由、BGP 路由共同决定有效路由 |
| VNet Peering | VNet 互联 | 不自动提供任意传递路由 |
| Azure Firewall / NVA | 集中安全检查 | UDR、转发许可、对称性共同决定可达性 |
| Load Balancer | 四层负载分发 | 探测与业务流量是两件事 |
| Application Gateway | HTTP(S) 应用层代理/分发 | 证书、HTTP 路由和后端健康需单独检查 |
| VPN Gateway / ExpressRoute | 混合连接 | 连接、网关、路由与容灾层级分开 |
| Virtual WAN | 托管 hub 与连接组织 | 不等同于手工 hub VNet 的所有行为 |

## 5. Hub-spoke 的隐含条件

Hub 包含共享网络服务，spoke 承载工作负载。Spoke A→Hub→Spoke B 需要明确路由、转发与安全策略，不能因为两个 spoke 都 peer 到 hub 就认为自动互通。通过 NVA/Firewall 转发还要检查 forwarded traffic 和返回路径。Gateway transit / use remote gateways 有具体限制，实施时按所选模型核验。阅读 [Azure Hub-spoke 架构](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke) 中连接与路由建议。

DNS 要同时画出来：本地客户端怎样查询云私有名字？云工作负载怎样查本地域？条件转发方向有没有环路？能用 IP 访问但不能用名字访问时，先检查解析链而非反复修改 BGP。

一条 ExpressRoute circuit 的冗余连接不替代跨接入地点的灾备。两 DC、两云区域还要考虑客户 CE、运营商、peering location、网关与应用故障。官方 [ExpressRoute 灾备设计](https://learn.microsoft.com/en-us/azure/expressroute/designing-for-disaster-recovery-with-expressroute-privatepeering) 可用于核对地域冗余及非对称路径风险。

## 自测参考

- Peering 还是 TGW？先看网络数量、分段、传递路由、集中检查和管理成本；不能只答“TGW 更高级”。
- 专线是否天然加密？私有路径与加密是不同要求，按服务能力与业务需求设计。
- 放通 SG 为何不通？继续查子网路由、NACL、回程、应用监听及中间设备。
- 两条 ER 会话都 Established 能否承诺整个区域故障仍可用？不能，必须验证故障域和应用灾备。
