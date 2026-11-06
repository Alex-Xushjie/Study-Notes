# 网络工程进阶笔记：总目录

## 定位与最终目标

这份笔记面向已有路由交换经验、希望扩大知识面并深耕2–3个方向的网络工程师，不从IP地址/掩码等已掌握基础重写。Linux与编程按初学者需要解释组件、命令与运行环境，其他部分以机制、路径、设计取舍、排障证据和工程交付为核心。

目标是能独立解释和验证业务路径，形成可审查设计、正常/故障/恢复实验、受控变更和RCA，并如实表达个人能力。教材与实验手册分工：本目录讲知识与方法，配套Network-Career-Lab提供已有项目/实验；阅读完成不等于实测通过或生产经历。

当前中文初版包含 **12个部分、102个专题、224篇正文**，另有12份部分导航和本总目录。

## 全书目录

| 部分 | 范围 | 专题 / 正文 |
|---|---|---|
| [01 路由交换与互联网边界](01-Routing-and-Switching/Routing-and-Switching.md) | 转发、冗余、OSPF/BGP、VRF、IPv6、QoS与出口 | 11 / 25 |
| [02 组播](02-Multicast/Multicast.md) | IGMP/MLD、Snooping、RPF、PIM、RP、SSM与行情排障 | 9 / 20 |
| [03 Linux网络](03-Linux-Networking/Linux-Networking.md) | 系统组件、接口/路由、虚拟网络、Socket、观测、NIC/NUMA与性能 | 10 / 15 |
| [04 网络自动化](04-Network-Automation/Network-Automation.md) | Python、数据/API、SoT、模板、并发、健康检查与安全发布 | 8 / 22 |
| [05 WAN与SD-WAN](05-WAN-and-SD-WAN/WAN-and-SD-WAN.md) | 运营商、MPLS、隧道、跨站路由、SD-WAN、SLA与运营 | 9 / 22 |
| [06 云与混合网络](06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md) | AWS/Azure、私有服务、路由、DNS、治理、容灾与费用 | 8 / 23 |
| [07 园区与无线](07-Campus-and-Wireless/Campus-and-Wireless.md) | 园区/PoE、基础服务、RF、接入、控制器、勘测、漫游与分区 | 9 / 18 |
| [08 网络安全与接入](08-Network-Security-and-Access/Network-Security-and-Access.md) | 防火墙/NAT、HA、IPsec、远程VPN、AAA/NAC、PKI/MFA与ZTNA | 9 / 18 |
| [09 交易与低延迟](09-Trading-and-Low-Latency/Trading-and-Low-Latency.md) | 行情/订单边界、A/B与序号、路径/队列、PTP、采集和Linux | 10 / 20 |
| [10 数据中心网络](10-Data-Center-Networking/Data-Center-Networking.md) | Clos、VXLAN/EVPN、IRB、多归属、边界、迁移与排障 | 7 / 15 |
| [11 AIDC与RDMA](11-AIDC-and-RDMA/AIDC-and-RDMA.md) | Collective、GPU/NIC拓扑、RDMA、PFC/ECN、Rail、光互联与测试 | 6 / 13 |
| [12 工程参考](12-Engineering-Reference/Engineering-Reference.md) | 需求/容量、HLD/LLD/PoC、变更/回退、Runbook、RCA与术语 | 6 / 13 |

## 按职业方向使用

量化/交易路线：01补转发/队列/冗余细节，02深入组播，03从Linux组件逐步进入主机性能，再用09贯通行情完整性、路径、时钟与采集；04提供自动化和可复核报告，08提供接入/身份边界。选其中2–3项形成深耕作品，不需先完整重读所有理论。

企业/能源路线：01→05→06，深入路由、WAN/SD-WAN和混合云，结合08建立安全/远程接入与身份，04支持运维闭环。07覆盖办公园区，10用于数据中心场景。实际生产控制网络的承载和云接入须另按业务与组织要求评审，不把通用方案视为自动适用。

办公网络路线：07与08围绕终端、RF、AAA、VPN和授权，结合01、03、05/06解决上联、主机、出口与服务依赖。无线覆盖、容量、漫游和兼容需真实终端/现场验证。

10是数据中心深化，11是拓宽方向。按此前不以明显降薪换零经验转岗的约束，AIDC先学习通信/网络与协作诊断，取得真实资源或项目后再深化，不抢占当前主线。12按项目阶段查阅，不作为必须先读的抽象基础篇。

## 每个主题的学习闭环

1. 画具体业务流，标对象、角色、地址/身份、正向和返回。
2. 解释机制与正常依赖，选一个能推翻理解的反例。
3. 在已授权隔离环境做最小正常/异常/恢复；无环境时明确纸面推演。
4. 对照配置意图、控制状态、实际转发/数据与应用结果。
5. 交付证据、结论边界、修复/回退与复测，更新能力台账。

不要求按顺序重读已掌握内容。遇到前置不懂时回到对应章节，例如先认识IRQ、PHC、Socket，再看低延迟参数，而不是先复制命令。

## 实验与成果入口

| 主题 | 当前入口与边界 |
|---|---|
| Linux | [已有Linux实验](../Network-Career-Lab/01-Linux/02-Labs.md)，软件功能不证明ASIC性能 |
| 自动化 | [离线检查与渲染项目](../Network-Career-Lab/02-Automation/02-Project.md)，实机Adapter需另验证 |
| 组播 | [分阶段指引](02-Multicast/09-Design-and-Troubleshooting/04-Lab-Guide-and-Review.md) |
| WAN | [综合实验](05-WAN-and-SD-WAN/08-Capacity-Failover-and-Operations/04-Lab-Guide-and-Capstone.md) |
| 云 | [云设计C1–C4](../Network-Career-Lab/03-Cloud/02-Labs-and-Design.md)，离线作业不需账号 |
| 园区无线 | [实验与勘测](07-Campus-and-Wireless/09-Wireless-Troubleshooting/02-Lab-Guide-and-Campus-Capstone.md) |
| 安全接入 | [策略、VPN、AAA与HA](08-Network-Security-and-Access/09-Vendor-Platforms/02-Lab-Guide-and-Security-Capstone.md) |
| 交易低延迟 | [分档实验](09-Trading-and-Low-Latency/10-Opening-Load-Changes-and-Incidents/02-Lab-Guide-and-Low-Latency-Capstone.md) |
| 数据中心 | [D1–D4](../Network-Career-Lab/05-Data-Center/02-Labs.md)，先最小闭环再冗余 |
| AIDC | [H1–H4](../Network-Career-Lab/06-AI-HPC/02-Design-and-Labs.md)，模型有明确假设 |

统一使用[实验报告模板](../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)和[设计/作品模板](../Network-Career-Lab/08-Portfolio/Design-and-Interview.md)。既有实验库可能仍有旧归档引用，以本总目录和各部分新导航为当前入口；本次未重写整个实验仓库。

## 文件、版本与证据约定

目录与正文每一新层级从01重新编号；导航使用主题文件名，不使用README.md。代码块有环境与前置，Linux、PowerShell、NOS/vtysh、云CLI和Python不能混用；文档地址和占位接口不是已部署对象。

各篇引用协议、内核、软件项目和厂商原始资料。最新网页不等于本地版本，命令/硬件/授权/法规/配额需按目标部署核对；价格和性能不固定为永久结论。生产凭据、私钥、真实敏感配置和可复用Token不放入笔记。

图表和结果区分教学推演、离线代码、软件拓扑、设备/射频/硬件实测和生产。未测写未测，失败保留证据，UNKNOWN不判为PASS。

## 当前完成与验证边界

12部分正文与学习导航均已填充，已检查全书编号、空文件、本地链接与代码围栏，并校验相应教学计算。部分标准库Python示例做了离线正常/异常测试，详见各部分验证说明；这不表示全部第三方代码、设备配置或实验已运行。

本次没有搭建真实Fabric、GPU/RDMA、无线、VPN/HA或交易所环境，没有测得实际吞吐、收敛、精度或生产SLA。后续按选定主线逐篇阅读和实测修订，不把初版教材标为生产验证完成。
