# 厂商能力映射与平台学习方法

[返回WAN与SD-WAN目录](../WAN-and-SD-WAN.md)

## 1. 先建立通用问题，再学名称

本专题选择Cisco Catalyst SD-WAN与Fortinet作为两种产品实现例子，不做采购排名。目标是能把通用机制映射到实际状态、策略与命令，避免会背架构图却不会定位业务路径。

| 通用对象 | Cisco例子 | Fortinet例子 |
|---|---|---|
| 边缘 | WAN Edge / IOS XE SD-WAN设备 | FortiGate |
| 集中管理 | SD-WAN Manager | FortiManager（部署方式按方案） |
| Overlay路由 | OMP等产品机制 | 常结合BGP等设计，并按版本/拓扑选用 |
| 传输/路径对象 | TLOC、Color等 | SD-WAN Member、Zone、Overlay等 |
| 质量与业务选路 | BFD质量、AAR、SLA Class | Performance SLA、SD-WAN Rule/Service |
| 动态分支互连 | 按产品拓扑/策略形成连接 | ADVPN Shortcut等 |

表格只做学习映射，不表示架构一一等价。不能把FortiManager当作OMP Controller，也不能把Cisco Color当成802.1Q VLAN或DSCP。

## 2. 固定版本与环境

每次实验记录管理/控制/Edge版本、硬件/虚机类型、授权、功能开关、拓扑与Underlay。一个功能出现在最新文档中，不代表旧设备支持；“17.x”“7.6”范围仍可能包含行为差异。

配置方法也要固定：模板、配置组、API或本地CLI的所有权关系。学习时明确哪些本地修改会被集中管理覆盖。不要把vEdge、IOS XE与不同FortiOS版本命令混成一段脚本。

## 3. 六项实操能力

能完成单站点上线，解释控制与数据状态，追踪一条业务路由与会话，验证应用SLA及兜底，定位一个质量退化案例，执行可回退的小范围变更。每项留下对应状态与业务证据，而非截图证明平台登录成功。

先把一家平台学到完整闭环，再用另一家比较差异。没有授权镜像时可以完成架构、策略和故障推演，但不能声称已实操该平台。

## 4. 能力评估表

按“知道机制—能看状态—能配置—能注入故障—能做设计取舍”五级自评；每一级附文件/实验记录。厂商考试可验证部分知识，不能替代业务设计、跨团队协作与运营经验。

## 5. 官方入口

[Cisco设计指南](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html)、[Fortinet SD-WAN规则](https://docs.fortinet.com/document/fortigate/7.6.6/administration-guide/716691/sd-wan-rules)。本教材引用页面在编写时核对，部署前仍需按目标版本查Release Notes和兼容矩阵。
