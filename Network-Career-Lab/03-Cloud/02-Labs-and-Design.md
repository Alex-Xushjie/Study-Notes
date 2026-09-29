# 云网络实验与设计作业

核心作业 C1–C3 不需要云账户，交付的是可评审设计。C4 是可选实机实验，单独记录平台结果。

## C1 三 VPC 与本地数据中心

地址计划：Prod 10.10.0.0/16，Dev 10.20.0.0/16，Shared 10.30.0.0/16，DC 10.100.0.0/16。要求 Prod/Dev 只能访问 Shared 和 DC，不能互访；DC 能访问各云网；每条流都能返回。

步骤：

1. 画 VPC attachment、TGW、DXGW、transit VIF、CE 及 VPN 备份，标注 AZ 和物理故障域。
2. 建 TGW route table `workload`、`shared`、`dc`；Prod/Dev 关联 workload，Shared 关联 shared，DC 连接关联 dc。说明实际 attachment 类型与传播能力。
3. workload 只学 Shared/DC；shared 学 Prod/Dev/DC；dc 学 Prod/Dev/Shared。写清哪些是传播、哪些是静态，以及网关约束。
4. 每个 VPC 的业务子网表添加相关目标指向 TGW；补充各安全策略。
5. 用下表逐跳演算，记录“不通”的预期是否由路由或安全策略造成。

| 源→目的 | workload 表 | 目的侧回程 | 预期 |
|---|---|---|---|
| Prod→Shared | Shared attachment | shared 表有 Prod | 通，仍须安全策略放行 |
| Dev→Prod | 不应有 Prod 路由 | 不适用 | 不通 |
| DC→Dev | 查 dc 表的 Dev | workload 表有 DC | 通 |

故障注入（纸面）：删除 Shared→Prod 的返回路由；把 Dev 误关联 shared 表；发布重叠 CIDR；DX 主路由撤销。每次写“控制面变化、正向路径、回程路径、业务结果、恢复动作”。

验收：20 分钟白板讲清一条 Prod→DC 流量和返回；指出 association 与 propagation 配错会产生什么差异。

## C2 Azure Hub-spoke 与集中检查

Hub 10.40.0.0/16、App 10.50.0.0/16、Data 10.60.0.0/16。业务要求 App→Data TCP 5432 必须经 hub 防火墙，其余跨 spoke 流量拒绝。为 App、Data 的业务子网分别写目标网段 UDR→防火墙私网 IP，再核对 peer 转发选项、NSG、Firewall policy 和有效路由。

交付一张“子网、前缀、下一跳、来源、优先级依据”表。故障：只给 App 配 UDR，Data 侧有另一条直达路径。推演为什么可能绕过同一状态检查点，不以“两个网段能 ping”为通过标准。

DNS 扩展：定义 `app.lab.internal` 的私有解析，画 DC 与 hub 的条件转发方向。查询失败时分辨查询没到 resolver、没有该记录、转发环路和网络过滤。

## C3 两数据中心、两 Azure 区域

需求：任意一条接入线路或一个接入地点故障后，核心服务仍可达；吞吐与恢复时间阈值由你列成明确假设。不要凭空保证业务零中断。

设计两个 CE 故障域、两个 ER peering locations、两个区域的 hub/gateway 和本地出口策略。分析：单链路、单 CE、整站、区域故障；再分析 BGP 活着但应用不可用的情况。写出主备选路依据、BFD 的检测范围、备用容量和状态防火墙对称性。

验收：用 [设计模板](../08-Portfolio/Design-and-Interview.md) 完成 HLD，并回答 *How would you keep connectivity available if an entire peering location fails?* 参考答案必须包含位置多样性、客户侧/运营商路径、有效路由与实测切换，不能只说“双 BGP”。

## C4 可选：小规模云实机

只选 AWS 或 Azure 一个平台，避免同时搭两套收费环境。

1. 建专用测试 VPC/VNet 和两子网，放两台小型 Linux 测试实例，记录区域、地址、实例与网卡 ID。
2. 用私网 IP 启动临时 HTTP 服务，限测试源访问；抓包与查看有效路由/安全规则。
3. 每次只改一个条件：监听地址、安全规则、子网路由；预测后验证，再恢复。
4. AWS 可额外创建第二 VPC 验证 peering 与双向路由；Azure 可建第二 VNet 做同类练习。不强制启用 NAT/TGW/Firewall/ER。
5. 保存命令与控制台证据；结束后按依赖关系清理测试实例、网卡、网关、端点、公网地址、磁盘及日志资源，并查看剩余资源清单。

离线设计不能证明云服务的具体故障行为；C4 也不能证明真实专线的 SLA。
