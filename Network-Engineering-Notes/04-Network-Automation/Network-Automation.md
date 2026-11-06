# 网络自动化教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有网络经验、编程与控制端基础尚需补齐的工程师。8个专题、22篇正文，从Python运行和离线数据处理开始，逐步连接设备接口、数据模型、模板、并发、健康检查和安全变更。不会把Python语言、HTTP协议和SSH服务混为同一个概念。

目标是建立可追溯、可测试、明确失败边界的自动化闭环，先解决巡检/报告/生成，再学习受控发布。能批量发送命令不等于具备可靠的网络自动化能力。

## 全部专题与文章

### 01 Python基础

- [01 从网络任务认识Python与运行环境](01-Python-Fundamentals/01-Python-Fundamentals.md)
- [02 数据类型、循环、函数与输入验证](01-Python-Fundamentals/02-Types-Loops-Functions-and-Validation.md)
- [03 文件、参数与可维护脚本结构](01-Python-Fundamentals/03-Files-Arguments-and-Project-Structure.md)

### 02 数据文件与解析

- [01 JSON、YAML、CSV与数据契约](02-Data-Files-and-Parsing/01-Data-Files-and-Parsing.md)
- [02 CLI解析、状态归一化与计数器](02-Data-Files-and-Parsing/02-CLI-Parsing-Normalization-and-Counters.md)

### 03 设备接入与API

- [01 SSH与Netmiko：从单设备只读开始](03-Device-Access-and-APIs/01-Device-Access-and-APIs.md)
- [02 HTTP API、认证、分页与超时](03-Device-Access-and-APIs/02-HTTP-REST-and-API-Contracts.md)
- [03 NETCONF、RESTCONF、YANG与遥测](03-Device-Access-and-APIs/03-NETCONF-RESTCONF-YANG-and-Telemetry.md)

### 04 Inventory、SoT与数据模型

- [01 Inventory、Source of Truth与事实状态](04-Inventory-Source-of-Truth-and-Data-Models/01-Inventory-Source-of-Truth-and-Data-Models.md)
- [02 模型校验、配置漂移与变更归属](04-Inventory-Source-of-Truth-and-Data-Models/02-Schema-Validation-and-Drift-Ownership.md)

### 05 Jinja2与Ansible

- [01 Jinja2模板、严格变量与离线渲染](05-Jinja2-and-Ansible/01-Jinja2-and-Ansible.md)
- [02 Ansible清单、Playbook与连接方式](05-Jinja2-and-Ansible/02-Ansible-Inventory-Playbooks-and-Connections.md)
- [03 资源模块、幂等与Check Mode边界](05-Jinja2-and-Ansible/03-Resource-Modules-Idempotency-and-Check-Mode.md)

### 06 并发、错误与凭据

- [01 并发、超时、重试与部分失败](06-Concurrency-Errors-and-Credentials/01-Concurrency-Errors-and-Credentials.md)
- [02 凭据、端点信任与审计日志](06-Concurrency-Errors-and-Credentials/02-Secrets-Trust-and-Audit-Logging.md)

### 07 备份、合规与安全变更

- [01 配置备份、基线与可恢复性](07-Backup-Compliance-and-Safe-Changes/01-Backup-Compliance-and-Safe-Changes.md)
- [02 健康检查、预期集合与UNKNOWN](07-Backup-Compliance-and-Safe-Changes/02-Health-Checks-Unknown-and-Expected-State.md)
- [03 变更前检、灰度、后检与回滚](07-Backup-Compliance-and-Safe-Changes/03-Prechecks-Canary-Postchecks-and-Rollback.md)

### 08 Git、测试、CI与综合实验

- [01 Git、可审查差异与依赖复现](08-Git-Testing-and-CI/01-Git-Testing-and-CI.md)
- [02 离线测试、Fixture与设备集成验证](08-Git-Testing-and-CI/02-Offline-Tests-Fixtures-and-Device-Validation.md)
- [03 CI流水线、生成物与发布关口](08-Git-Testing-and-CI/03-CI-Pipelines-Artifacts-and-Release-Gates.md)
- [04 自动化分阶段实验与综合项目](08-Git-Testing-and-CI/04-Lab-Guide-and-Capstone.md)

## 推荐学习路径

初学主线：01→02→03的单设备只读→04→05离线生成→06→07→08。每阶段先运行正常示例，再跑缺失、超时、错类型、空数据等反例。已会Python可用练习自测后直接进入设备适配与模型。

企业WAN/云网络：重点输入治理、API分页、期望集合、模板所有权、灰度/后检；量化/低延迟运维：重点时间与单位、接口/协议状态、采样差值、并发压力与证据链。自动化不能替代对应网络机制理解。

## 示例运行约定

python代码保存为指定.py文件，再由已确认的解释器运行；PowerShell/bash/text块有各自环境和前置条件。不同篇章的教学数据并非天然同一Schema，复用前按契约转换。标准库示例可先离线运行；第三方库按项目选定版本安装到虚拟环境，不要求全局安装。

设备脚本只给单目标只读示例，文档IP不是可登录设备。SSH主机密钥、TLS证书与最小权限是明确前置条件。网络命令、配置片段、设备语法与API字段都需按目标版本验证。

## 实验与交付

入口：[分阶段实验与综合项目](08-Git-Testing-and-CI/04-Lab-Guide-and-Capstone.md)。连接[已有自动化项目](../../Network-Career-Lab/02-Automation/02-Project.md)，它提供可运行的BGP离线检查、测试和教学配置渲染；12项巡检仍是扩展目标，不把计划当已实现。

成果包括脱敏Inventory/Schema、采集Adapter、反例Fixture、JSON/CSV与退出码、确定性生成/Diff、实验变更记录和失败恢复设计。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，区分模拟、实验设备和生产经历。

## 先修与关联

[Linux基础](../03-Linux-Networking/01-Linux-Essentials/01-Linux-Essentials.md)帮助理解文件、进程、Shell和环境；[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)提供BGP/OSPF等健康判断；[WAN](../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)和[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)提供具体业务与API场景。

本部分不是完整软件工程或所有厂商SDK手册；NETCONF/RESTCONF/gNMI先掌握模型、能力与事务边界，再选实际平台深化。

## 文件与资料约定

目录和正文在每个新层级从01编号；导航按主题命名，不使用README.md。各篇引用Python、Jinja、Ansible、Netmiko、NetBox与协议原始资料。latest页面不等于本地版本，项目记录依赖/Collection与NOS支持矩阵。

## 本次验证范围

已检查章节覆盖、编号、本地链接、代码围栏、JSON示例及9段Python语法；实际执行了标准库基础/计数/并发模拟、错误输入、4个非法VLAN反例和5项BGP规则测试。第三方Jinja2、Netmiko、Requests与Ansible运行及设备接口/事务未实测；没有安装依赖、连接设备或发布配置。
