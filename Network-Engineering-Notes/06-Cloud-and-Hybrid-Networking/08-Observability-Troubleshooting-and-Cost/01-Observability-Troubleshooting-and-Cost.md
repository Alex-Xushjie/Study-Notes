# 云网络可观测性与证据边界

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 工具回答不同问题

| 工具/数据 | 可回答 | 不能独自证明 |
|---|---|---|
| 有效路由/规则 | 当前计算出的平台配置 | 应用正在监听或实际数据已成功 |
| 路径分析 | 支持对象内的配置可达性/阻断点 | 真正发包、时延和全部动态依赖 |
| Flow Log | 支持范围内流量元数据与许可/拒绝 | 完整报文内容、所有流量或应用成功 |
| 指标 | 网关/NAT/端点负载与错误 | 精确根因与某个请求全路径 |
| 抓包/应用日志 | 具体观察点的数据与事务 | 其他观察点无故障 |
| 审计日志 | 谁何时修改对象 | 配置变化一定造成该故障 |

AWS Reachability Analyzer主要做配置分析，不主动以业务包测量性能。云流日志有采集范围、聚合、延迟和遗漏限制；ACCEPT不意味着应用响应成功。

## 2. Azure日志版本变化

新设计优先核对Virtual Network Flow Logs。NSG Flow Logs有创建限制和退役计划，不能继续把旧教程当新环境的默认方案；具体迁移时间与支持以官方文档为准。已有日志的保留、费用和迁移也要纳入计划。

## 3. 统一证据键

保存账号/订阅、区域/AZ、网卡/资源ID、源/目的及端口、NAT前后地址、UTC或明确时区、采样窗口与配置版本。按请求/会话ID把LB、应用、身份和网络日志关联，而不是依靠肉眼比较不同图表。

日志权限和数据保留需符合组织要求。全量日志可能包含内部地址、身份和业务访问模式，导出到作品集时用脱敏数据与明确说明。

## 4. 排错顺序

从真实事务和时间窗出发，先解析与目标，再查源端、平台路由/安全、接入/Transit、目标端和回程。对累计计数取差值；保存变更事件。探测正常但应用异常时，核对探测协议、目标、包长、身份与路径是否代表业务。

## 5. 练习

选一条DC到云HTTPS请求，给出配置分析、流日志、目标主机抓包和应用响应四类证据。解释哪些缺口仍存在，不能把同一张“Reachable”截图重复作为全部证据。

[AWS Reachability Analyzer](https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html)、[AWS Flow Log限制](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-limitations.html)、[Azure VNet Flow Logs](https://learn.microsoft.com/en-us/azure/network-watcher/vnet-flow-logs-overview)、[NSG日志迁移](https://learn.microsoft.com/en-us/azure/network-watcher/nsg-flow-logs-migrate)。
