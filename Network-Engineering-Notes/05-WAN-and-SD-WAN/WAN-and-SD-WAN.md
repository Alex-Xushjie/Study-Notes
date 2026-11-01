# WAN与SD-WAN教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分围绕企业多站点、能源行业广域网和混合云场景，补强从运营商服务边界到路由、隧道、应用选路、隔离和运营的完整能力。9个专题、22篇正文；不重复IP/掩码入门，Linux实验术语在使用时解释。

学习目标是能设计可解释、可回退、可验证的WAN，并独立定位线路、隧道、路由、策略和应用问题。SD-WAN是能力集合，各产品控制与选路机制不同；教材不把一家产品名称当通用标准。

## 全部专题与文章

### 01 运营商接入与服务边界

- [01 运营商接入、产品与责任边界](01-Carrier-Access-and-Service-Boundaries/01-Carrier-Access-and-Service-Boundaries.md)
- [02 SLA、交付验收与运营商协同](01-Carrier-Access-and-Service-Boundaries/02-SLA-Acceptance-and-Carrier-Escalation.md)

### 02 MPLS L3VPN

- [01 MPLS L3VPN的客户视角与逐跳转发](02-MPLS-L3VPN/01-MPLS-L3VPN.md)
- [02 CE–PE路由、防环与混合承载迁移](02-MPLS-L3VPN/02-CE-PE-Routing-and-Hybrid-Migration.md)

### 03 WAN隧道

- [01 WAN隧道、IPsec与NAT穿越](03-WAN-Tunnels/01-WAN-Tunnels.md)
- [02 封装开销、MTU与大包黑洞](03-WAN-Tunnels/02-MTU-MSS-and-Tunnel-Troubleshooting.md)

### 04 多站点路由与冗余

- [01 多站点拓扑、路由与回程设计](04-Multisite-Routing-and-Redundancy/01-Multisite-Routing-and-Redundancy.md)
- [02 故障检测、会话保持与恢复切回](04-Multisite-Routing-and-Redundancy/02-Detection-Stateful-Failover-and-Failback.md)
- [03 混合WAN迁移与路由反馈案例](04-Multisite-Routing-and-Redundancy/03-Migration-and-Route-Feedback-Cases.md)

### 05 SD-WAN架构

- [01 SD-WAN平面、边缘与控制依赖](05-SD-WAN-Architecture/01-SD-WAN-Architecture.md)
- [02 上线、策略发布与控制平台故障](05-SD-WAN-Architecture/02-Onboarding-Policy-and-Control-Failures.md)

### 06 应用SLA与路径选择

- [01 应用SLA、分类与路径选择](06-Application-SLA-and-Path-Selection/01-Application-SLA-and-Path-Selection.md)
- [02 迟滞、QoS与链路修复机制](06-Application-SLA-and-Path-Selection/02-Hysteresis-QoS-and-Remediation.md)

### 07 分段、云与SASE集成

- [01 业务分段、共享服务与安全服务链](07-Segmentation-Cloud-and-SASE-Integration/01-Segmentation-Cloud-and-SASE-Integration.md)
- [02 混合云、SaaS出口与云侧回程](07-Segmentation-Cloud-and-SASE-Integration/02-Cloud-Connectivity-and-SaaS-Egress.md)

### 08 容量、故障切换与运营

- [01 WAN容量、N-1与降级设计](08-Capacity-Failover-and-Operations/01-Capacity-Failover-and-Operations.md)
- [02 可观测性、分层排障与RCA](08-Capacity-Failover-and-Operations/02-Telemetry-Troubleshooting-and-RCA.md)
- [03 变更、升级、灾备与故障演练](08-Capacity-Failover-and-Operations/03-Change-Management-and-Disaster-Recovery.md)
- [04 WAN分阶段实验与企业综合设计](08-Capacity-Failover-and-Operations/04-Lab-Guide-and-Capstone.md)

### 09 厂商平台

- [01 厂商能力映射与平台学习方法](09-Vendor-Platforms/01-Vendor-Platforms.md)
- [02 Cisco Catalyst SD-WAN的OMP、TLOC与排障](09-Vendor-Platforms/02-Cisco-Catalyst-SD-WAN.md)
- [03 Fortinet的Member、SLA、Rule与ADVPN](09-Vendor-Platforms/03-Fortinet-SD-WAN-and-ADVPN.md)

## 推荐学习路径

企业WAN/能源主线：01–04理解服务、承载与路由边界，再读05–08形成策略和运营闭环；09选择一个平台完成实操。偏远站点额外关注供电、蜂窝流量、现场恢复和管理依赖，工业生产控制是否适用需按业务风险另行确定。

SD-WAN深化：05→06→09→08的实验，再回到03/04解释MTU、回程与切换。云互联先读07，再进入独立云网络部分，不能只看隧道UP就跳过云侧路由。

有经验的内容用反例自测：为什么双运营商仍同时断？为什么隧道UP却大文件失败？为什么SLA探测正常而ERP卡？为什么新连接恢复不代表旧连接无损？

## 实验与交付

从[分阶段实验与综合设计](08-Capacity-Failover-and-Operations/04-Lab-Guide-and-Capstone.md)开始，分Linux/FRR逻辑、厂商功能、真实设备线路三个层次验证。现有实验库没有独立完整SD-WAN拓扑，本教材不把其他实验冒充原生平台验证。

建议成果：运营商验收与报障包、多站点路由/回程矩阵、SD-WAN应用SLA与兜底方案、N-1容量与降级表、混合网迁移计划、故障RCA和恢复Runbook。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，区分推演、实测与生产经验。

## 先修与关联

需要[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)中的BGP、VRF、BFD与QoS。主机命令不熟悉时先读[Linux基础](../03-Linux-Networking/01-Linux-Essentials/01-Linux-Essentials.md)。组播业务需单独核对承载能力，不能由WAN单播通推导组播支持，参阅[组播教材](../02-Multicast/Multicast.md)。

## 文件与资料约定

目录和正文各层从01重新编号，导航按主题命名，不使用README.md。Linux Shell、厂商CLI与平台GUI不是同一执行环境；示例地址与接口仅用于隔离实验，禁止把占位参数直接套到现网。

各篇引用RFC、Cisco/Fortinet、AWS/Microsoft及Linux原始资料。产品章节是机制映射与诊断方法，不是跨版本通用一键配置；缺省策略、命令、授权、加密和云路由支持须按实际版本核对。

## 本次验证范围

已检查正文覆盖、编号、本地链接、代码围栏和教学计算；未搭建Linux/FRR或厂商实验环境，未连接运营商、云或生产设备，未实测吞吐、应用选路、IPsec协商或故障恢复。所有性能与时间示例均为给定假设下的推导。
