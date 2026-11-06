# 术语表与容易混淆的边界

[返回本部分学习目录](../Engineering-Reference.md)

## 1. 按层次查术语

| 术语 | 含义与边界 |
|---|---|
| RIB / FIB | 路由选择信息 / 相应转发安装；有RIB不保证FIB |
| VLAN / VRF | 二层逻辑域 / 三层路由上下文；不等于应用授权 |
| RD / RT | 区分VPN路由 / 导入导出控制；用途不同 |
| VTEP / VNI | VXLAN封装端点 / Overlay上下文标识 |
| L2VNI / L3VNI | 相应桥接域 / VRF路由模型的VNI角色 |
| Underlay / Overlay | 端点承载 / 业务逻辑连接；各有路由 |
| ECMP / LAG | 等价路由 / 链路聚合；Hash不保证单流叠加 |
| MLAG / EVPN MH | 平台多机聚合 / EVPN多归属；机制不同 |
| RPF | 组播上游/期望入向判断；区别于单播uRPF |
| ASM / SSM | 任意源模型 / 接收者指定源的频道模型 |
| Querier / PIM DR | 成员查询职责 / PIM指定角色；选举不同 |
| IGMP / Snooping | IPv4成员管理 / 二层监听优化 |
| RSSI / SNR | 信号强度估计 / 信号与噪声的相应差值 |
| SSID / BSSID | 网络名称 / 基本服务集标识 |
| 802.11k/v/r | 相应测量/辅助转移/FT机制；非万能无缝开关 |
| EAP / EAP-TLS | 认证框架 / 一种证书方法；非同义 |
| AAA / NAC | 认证授权审计 / 网络接入控制体系 |
| PKI / MFA | 公钥信任体系 / 多因素验证；各有生命周期 |
| SNAT / DNAT | 源 / 目的地址映射；不是许可或加密 |
| IKE SA / Child SA | 控制保护 / 相应IPsec数据保护 |
| ZTNA / VPN | 资源级接入方式 / 多种隧道接入；适用协议不同 |
| SLA / SLO | 服务约定 / 业务目标；对象与口径需说明 |
| RTO / RPO | 恢复时间目标 / 数据损失范围目标 |
| HLD / LLD / PoC | 高层设计 / 详细实施 / 关键假设验证 |
| Inventory / SoT / Fact | 目标清单 / 治理意图 / 采集事实 |
| Idempotency | 同意图重复操作无不必要变化；非自动安全保证 |
| PASS/FAIL/UNKNOWN/N/A | 符合/违反/证据不足/不适用，不能混用 |
| IRQ / RSS / NUMA | 中断 / NIC接收分流 / 内存与CPU位置关系 |
| PHC / PTP | 硬件时钟 / 时间同步协议体系；位数不等于准确度 |
| RDMA / RoCE / IB | 远程内存能力 / 以太承载族 / InfiniBand体系 |
| QP / MR / CQ | 队列对 / 注册内存 / 完成队列 |
| PFC / ECN | 链路优先级背压 / 显式拥塞标记；反馈范围不同 |
| Rank / Rail | 通信参与者 / 特定拓扑与端点映射的网络组织 |
| algbw / busbw | 工具定义的算法/归一化带宽；非端口实测同义 |

## 2. 不将标签当结论

UP、Connected、Established、Accept、Valid、Reachable各自只证明特定层次。配置意图、控制状态、转发表、真实流量和业务应分别说明；硬件、版本、采样点与时间决定结论边界。

## 3. 练习

从上表选5组，分别写一个“前者正常但后续业务失败”的反例和证据。例如BGP会话正常但前缀被过滤，PTP进程在但PHC未同步，证书有效却名称不匹配。

具体机制和命令返回[全书总目录](../../Contents.md)进入对应部分，本表用来定位概念，不代替协议规范。
