# 云与混合网络教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有路由交换经验、希望掌握企业混合云网络的工程师。8个专题、23篇正文，以AWS与Azure为主线，连接WAN、主机、DNS与安全；GCP仅用于理解对象范围差异，不宣称提供完整第三平台教材。

目标是解释并验证业务的DNS、双向路由、安全、身份和应用路径，能完成多网络分段、混合接入、私有服务、容灾与排障设计。云控制台对象创建成功不能替代业务验收。

## 全部专题与文章

### 01 云网络对象与设计模型

- [01 云网络对象与传统网络思维转换](01-Cloud-Networking-Objects/01-Cloud-Networking-Objects.md)
- [02 逐跳流量模型与设计输入](01-Cloud-Networking-Objects/02-Packet-Walk-and-Design-Inputs.md)

### 02 AWS网络

- [01 AWS VPC、子网路由与Internet路径](02-AWS-Networking/01-AWS-Networking.md)
- [02 AWS安全规则、负载均衡与端点判断](02-AWS-Networking/02-Security-Groups-NACLs-and-Load-Balancers.md)
- [03 AWS Transit Gateway、Peering与混合连接](02-AWS-Networking/03-Transit-Gateway-and-Connectivity.md)

### 03 Azure网络

- [01 Azure VNet、UDR、NSG与有效状态](03-Azure-Networking/01-Azure-Networking.md)
- [02 Azure Hub-Spoke、Peering与集中检查](03-Azure-Networking/02-Hub-Spoke-Peering-and-Inspection.md)
- [03 ExpressRoute、VPN与Azure私有服务](03-Azure-Networking/03-ExpressRoute-VPN-and-Private-Services.md)

### 04 私有访问、出口与检查

- [01 私有服务访问与公网暴露边界](04-Private-Access-Egress-and-Inspection/01-Private-Access-Egress-and-Inspection.md)
- [02 出站设计、SNAT与IPv6](04-Private-Access-Egress-and-Inspection/02-Egress-NAT-and-IPv6.md)
- [03 集中检查、对称路径与NVA高可用](04-Private-Access-Egress-and-Inspection/03-Stateful-Inspection-and-Symmetric-Paths.md)

### 05 混合地址、路由与分段

- [01 混合云IPAM、地址重叠与分段](05-Hybrid-Addressing-Routing-and-Segmentation/01-Hybrid-Addressing-Routing-and-Segmentation.md)
- [02 BGP、路由传播与云侧回程](05-Hybrid-Addressing-Routing-and-Segmentation/02-BGP-Propagation-and-Return-Paths.md)
- [03 专线与VPN备份、混合迁移边界](05-Hybrid-Addressing-Routing-and-Segmentation/03-Private-Circuit-VPN-and-Migration.md)

### 06 混合DNS

- [01 混合DNS、私有区与条件转发](06-Hybrid-DNS/01-Hybrid-DNS.md)
- [02 DNS排障、缓存与私有端点案例](06-Hybrid-DNS/02-DNS-Troubleshooting-and-Private-Endpoint-Cases.md)

### 07 多账号、多区域与韧性

- [01 多账号、订阅与网络治理](07-Multiaccount-Multiregion-and-Resilience/01-Multiaccount-Multiregion-and-Resilience.md)
- [02 AZ、区域与混合接入故障域](07-Multiaccount-Multiregion-and-Resilience/02-AZ-Region-and-Connectivity-Failure-Domains.md)
- [03 故障演练、RTO与恢复Runbook](07-Multiaccount-Multiregion-and-Resilience/03-Failover-Testing-and-Recovery-Runbooks.md)

### 08 可观测性、排障、费用与实验

- [01 云网络可观测性与证据边界](08-Observability-Troubleshooting-and-Cost/01-Observability-Troubleshooting-and-Cost.md)
- [02 四类云网络故障与RCA](08-Observability-Troubleshooting-and-Cost/02-Troubleshooting-Cases-and-RCA.md)
- [03 网络费用、配额与架构取舍](08-Observability-Troubleshooting-and-Cost/03-Cost-Quotas-and-Design-Tradeoffs.md)
- [04 云网络分阶段实验与综合设计](08-Observability-Troubleshooting-and-Cost/04-Lab-Guide-and-Capstone.md)

## 推荐学习路径

先读01建立对象和逐跳思维，再从02/03选一家平台完整学习，随后读04–06的服务访问、混合路由和DNS，最后完成07/08的治理、容灾与实验。第二平台重点比较差异，不照搬术语与优先级。

企业/能源路线关注IPAM、Prod/Dev/Shared隔离、双接入位置、云侧回程、共享服务和恢复Runbook。生产控制系统能否上云/使用相关承载需另按业务与安全要求评审。办公/远程接入场景还需连接后续安全与身份专题。

遇到Linux命令，先理解ip、ss、dig、curl、tcpdump各回答什么，再执行隔离实验。教材解释云网络，不重复从IP地址和掩码开始写。

## 实验与交付

入口：[分阶段实验与综合设计](08-Observability-Troubleshooting-and-Cost/04-Lab-Guide-and-Capstone.md)。离线设计不需云账号；云实测只选一个平台的小规模隔离环境，不强制新建TGW、NAT、Firewall、Resolver或专线等收费资源。

[已有云实验C1–C4](../../Network-Career-Lab/03-Cloud/02-Labs-and-Design.md)提供三网+DC、Azure集中检查、双区域和可选小实验。交付逐跳路径、地址/资源台账、路由与权限矩阵、DNS链、故障RCA、恢复与费用模型，使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。

## 关联与边界

先修：[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)中的BGP、VRF和状态路径；[WAN与SD-WAN](../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)提供接入、隧道、MTU与运营；主机命令参考[Linux基础](../03-Linux-Networking/01-Linux-Essentials/01-Linux-Essentials.md)。

本部分不代替Kubernetes/CNI、完整云安全/IAM课程、所有托管数据库网络细节或真实运营商SLA验证。服务专用子网、配额、区域/SKU和默认行为需核对目标部署。

## 文件与资料约定

各目录层级与专题内文章从01重新编号，导航按主题命名，不使用README.md。Linux Shell、AWS CLI、Azure CLI和平台对象各有前置条件；示例不是一键部署脚本。

引用官方AWS、Microsoft、Google与相关原始资料。编写时核对了Azure显式出口、流日志迁移与私有DNS等变化；不固定实时价格/配额，也不把某平台最长匹配之外的选路特例泛化到其他平台。

## 本次验证范围

已检查章节覆盖、编号、本地链接、代码围栏与教学计算；未登录云账号、创建资源、启动混合拓扑或执行CLI/故障演练。所有示例路径和恢复场景为教学设计，不代表实际吞吐、可用率或生产经历。
