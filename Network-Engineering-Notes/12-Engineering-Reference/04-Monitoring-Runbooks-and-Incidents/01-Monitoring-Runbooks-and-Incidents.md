# 监控、告警与值班Runbook

[返回本部分学习目录](../Engineering-Reference.md)

## 1. 三层可观测性

组件健康查看接口/进程/节点；路径健康查看路由、隧道、质量和容量；业务健康查看真实事务、完整性与成功率。上层可能失败而下层全绿，所以监控要按依赖关联，不能只收SNMP端口利用率。

| 层次 | 示例 |
|---|---|
| 组件 | NIC错误、CPU/内存、设备角色与进程 |
| 路径 | RPF、BFD、VPN、队列/丢弃与MTU |
| 服务 | DHCP/DNS/AAA、证书与时钟 |
| 业务 | HTTP事务、行情gap、应用延迟与恢复 |
| 变更 | 配置/版本/身份/路由事件 |

## 2. 告警设计

每条告警有对象、条件/窗口、严重性、影响、去重/依赖、负责人与Runbook。失联不自动等于设备死，可能采集器/权限/管理路径失败。数据过期应告警UNKNOWN，不静默保留旧绿灯。

抑制维护噪声要有范围和期限，不能永久静音。一次上联故障引起几十条隧道失效，需关联根依赖，但保留业务受影响信息。

## 3. Runbook结构

入口症状→影响判断→只读证据→候选分支→授权恢复→业务确认→升级/接管→收尾。每一步说明预期与不符时下一步，不写一串没有解释的clear/restart命令。

## 4. 容量与日志

采集频率、日志级别、保留、敏感信息和成本纳入设计。逐包TRACE/全量抓包可能影响待观察系统，采用有限窗口、聚合与采集健康指标。记录器自己丢样本时不能继续给绝对完整性结论。

## 5. 练习

为BGP前缀缺失、无线AAA失败和行情gap各写告警/Runbook，标哪些依赖共用。模拟采集器失败，验证不会被错报成全部业务同时坏。

[自动化UNKNOWN](../../04-Network-Automation/07-Backup-Compliance-and-Safe-Changes/02-Health-Checks-Unknown-and-Expected-State.md)、[Linux观测](../../03-Linux-Networking/06-Network-Observation-Tools/01-Network-Observation-Tools.md)。
