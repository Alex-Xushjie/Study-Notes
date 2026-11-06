# 外部前缀、DCI与路由反馈

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 谁拥有前缀

明确本地接入子网、远端租户、外部WAN和默认路由的权威来源。EVPN与外部BGP/OSPF互相重分发时，应有精确导入/导出和来源规则，不能把所有路由无约束来回发布。

教学案例：Border-A把WAN前缀导成EVPN Type5，Border-B又把它导回WAN，被当成新来源；原WAN路由撤销后反馈项可能继续吸流。Tag/Community可辅助，但要验证跨协议/平台是否保留和应用。

## 2. DCI范围

跨机房延伸L2有地址移动等用途，也扩展BUM、故障和时延依赖。L3互联、特定网段延伸、独立Fabric互通是不同方案，按应用/灾备需求选择，不默认全网拉平二层。

## 3. 反例矩阵

| 事件 | 需验证 |
|---|---|
| 外部明细撤销 | 汇总是否黑洞，反馈是否消失 |
| 单Border失效 | 前向/回程、状态设备与容量 |
| DCI分区 | 两侧网关、主机与业务恢复 |
| 重复网段/地址 | 能否被校验拒绝而非错误导入 |
| 恢复/主机移动 | 旧位置清理与安全一致性 |

## 4. 练习

画双Border接同一WAN与两个Fabric的前缀来源矩阵，推演撤销与恢复。只在隔离网络做重分发实验，不发布文档地址到公网。命令成功与Type5存在均不能替代端到端验证。

[EVPN前缀RFC9136](https://www.rfc-editor.org/rfc/rfc9136.html)、[重分发防环](../../01-Routing-and-Switching/04-Routing-and-Forwarding/02-Redistribution-Summarization-and-Loop-Prevention.md)。
