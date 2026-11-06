# 网络工程参考与实践目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分汇总全书共用的工程方法，6个专题、13篇正文，包含需求/容量、设计与验收、变更/恢复、监控/事故、RCA、命令/术语和学习评审。用于把知识转成可审查、可验证、可恢复的成果，不作为必须先读的抽象基础篇。

## 全部专题与文章

### 01 需求、取舍与容量

- [01 需求访谈、取舍与可验收目标](01-Requirements-Tradeoffs-and-Capacity/01-Requirements-Tradeoffs-and-Capacity.md)
- [02 容量模型、N-1与离线检查](01-Requirements-Tradeoffs-and-Capacity/02-Capacity-Models-and-Offline-Checks.md)

### 02 HLD、LLD、PoC与验收

- [01 HLD、LLD、PoC与验收](02-HLD-LLD-PoC-and-Acceptance/01-HLD-LLD-PoC-and-Acceptance.md)
- [02 可直接复用的设计与验收模板](02-HLD-LLD-PoC-and-Acceptance/02-Reviewable-Design-and-Acceptance-Templates.md)

### 03 迁移、变更与回滚

- [01 迁移、变更与回滚方法](03-Migration-Changes-and-Rollback/01-Migration-Changes-and-Rollback.md)
- [02 实施步骤与Backout模板](03-Migration-Changes-and-Rollback/02-Method-of-Procedure-and-Backout-Template.md)

### 04 监控、Runbook与事故

- [01 监控、告警与值班Runbook](04-Monitoring-Runbooks-and-Incidents/01-Monitoring-Runbooks-and-Incidents.md)
- [02 事故响应、交接与恢复确认](04-Monitoring-Runbooks-and-Incidents/02-Incident-Response-and-Shift-Handover.md)

### 05 RCA与案例

- [01 RCA、证据与可推翻的假设](05-RCA-and-Case-Studies/01-RCA-and-Case-Studies.md)
- [02 跨领域案例与作品证据](05-RCA-and-Case-Studies/02-Cross-Domain-Cases-and-Portfolio-Evidence.md)

### 06 命令、术语与学习评审

- [01 命令索引：按问题和执行环境查找](06-Command-Index-and-Glossary/01-Command-Index-and-Glossary.md)
- [02 术语表与容易混淆的边界](06-Command-Index-and-Glossary/02-Glossary-and-Concept-Boundaries.md)
- [03 学习路径、深耕方向与综合评审](06-Command-Index-and-Glossary/03-Learning-Routes-and-Capstone-Review.md)

## 推荐使用路径

按实际任务查阅：新项目用01/02，实施用03，值班用04，复盘用05，跨领域查词/定位命令用06。不强制按目录从头阅读；各篇表格可复制到独立项目并填写来源、假设、负责人和验证结果。

## 实验与成果

入口：[综合实验或评审](06-Command-Index-and-Glossary/03-Learning-Routes-and-Capstone-Review.md)。区分离线推演、软件模拟、硬件实测与生产经历，交付拓扑/对象、正常/异常/恢复、反证与结论边界。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)和[设计模板](../../Network-Career-Lab/08-Portfolio/Design-and-Interview.md)。

## 关联与约定

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)与[交易低延迟](../09-Trading-and-Low-Latency/Trading-and-Low-Latency.md)提供相关前置。每层目录/正文从01编号，导航按主题命名，不使用README.md。

引用协议、软件项目及厂商原始资料；latest文档不是本地版本。设备/接口/地址、命令执行环境、硬件支持、授权和容量需按实际目标核对，示例不构成通用生产配置或采购清单。

## 本次验证范围

本次检查正文覆盖、编号、本地链接、代码围栏和容量/封装计算；工程容量Python示例完成语法与正常/异常输入离线验证。未运行Fabric、EVPN硬件、GPU/RDMA/NCCL或真实故障注入，未连接生产设备/服务。所有性能数字为给定假设下的教学推导。
