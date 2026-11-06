# 网络安全与接入教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分围绕企业防火墙、VPN、身份和资源接入。9个专题、18篇正文，连接会话、NAT、路由、HA、IPsec、远程用户、802.1X、证书/MFA及ZTNA。目标是把认证、授权、转发和真实业务分别验证，建立最小权限、可恢复、可审计的操作能力。

## 全部专题与文章

### 01 有状态防火墙与策略

- [01 有状态防火墙、会话与策略](01-Stateful-Firewall-and-Policies/01-Stateful-Firewall-and-Policies.md)
- [02 规则生命周期、日志与策略排障](01-Stateful-Firewall-and-Policies/02-Rule-Lifecycle-and-Troubleshooting.md)

### 02 NAT、路由与非对称

- [01 SNAT、DNAT、Hairpin与路由](02-NAT-Routing-and-Asymmetry/01-NAT-Routing-and-Asymmetry.md)
- [02 会话容量、端口耗尽与非对称路径](02-NAT-Routing-and-Asymmetry/02-Session-Capacity-and-Path-Asymmetry.md)

### 03 HA与状态同步

- [01 防火墙HA、状态同步与故障域](03-HA-and-State-Synchronization/01-HA-and-State-Synchronization.md)
- [02 HA倒换、升级与会话验收](03-HA-and-State-Synchronization/02-Failover-Measurement-and-Upgrades.md)

### 04 IPsec、IKE与站点VPN

- [01 IPsec、IKEv2、身份与安全关联](04-IPsec-IKE-and-Site-to-Site-VPN/01-IPsec-IKE-and-Site-to-Site-VPN.md)
- [02 站点VPN路由、Rekey与排障](04-IPsec-IKE-and-Site-to-Site-VPN/02-VPN-Routing-Rekey-and-Troubleshooting.md)

### 05 远程接入VPN

- [01 远程接入VPN、地址、DNS与授权](05-Remote-Access-VPN/01-Remote-Access-VPN.md)
- [02 远程接入运营、故障与离职撤权](05-Remote-Access-VPN/02-Remote-Access-Operations-and-Failure-Cases.md)

### 06 802.1X、EAP、AAA与NAC

- [01 802.1X、EAP、RADIUS与授权](06-8021X-EAP-AAA-and-NAC/01-8021X-EAP-AAA-and-NAC.md)
- [02 NAC、CoA、例外设备与AAA故障](06-8021X-EAP-AAA-and-NAC/02-NAC-CoA-Exceptions-and-Outages.md)

### 07 PKI、证书与MFA

- [01 PKI、证书链、名称与生命周期](07-PKI-Certificates-and-MFA/01-PKI-Certificates-and-MFA.md)
- [02 MFA、身份提供方与撤权](07-PKI-Certificates-and-MFA/02-MFA-Identity-and-Revocation.md)

### 08 ZTNA与SASE

- [01 ZTNA、SSE、SASE与资源级接入](08-ZTNA-and-SASE/01-ZTNA-and-SASE.md)
- [02 接入迁移、安全服务链与验收](08-ZTNA-and-SASE/02-Migration-Service-Chains-and-Validation.md)

### 09 厂商平台与实验

- [01 安全平台映射与版本化诊断](09-Vendor-Platforms/01-Vendor-Platforms.md)
- [02 安全接入实验与综合验收](09-Vendor-Platforms/02-Lab-Guide-and-Security-Capstone.md)

## 推荐学习路径

先01–03掌握包流程、地址和状态；04/05分别学习站点与远程用户；06/07补身份和信任；08判断资源级接入适用性；09选择合法平台做完整闭环。不同厂商的NAT/策略顺序、HA同步和VPN支持不可照搬，优先学清通用问题再映射产品对象。

## 实验与成果

入口：[分阶段实验与综合设计](09-Vendor-Platforms/02-Lab-Guide-and-Security-Capstone.md)。每篇练习区分离线推演、软件模拟、设备/射频/硬件实测和生产经历，不能将教学数值填写成自己的测量结果。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，交付拓扑、状态台账、允许/拒绝或完整性矩阵、故障时间线、反证与恢复方案。

安全建议成果：五元组/NAT/回程图、规则生命周期、HA新旧会话矩阵、VPN与身份故障包、证书撤权及资源级访问迁移。真实凭据、Token、私钥与敏感备份不写入本笔记。

## 先修与关联

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[WAN](../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)与[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)提供对应机制和操作前置。跨专题按链接阅读，不将不同Shell/NOS/协议命令混成一个脚本。

## 文件与资料约定

每层目录与专题内正文从01重新编号，导航按主题命名，不使用README.md。示例接口、地址、域名和数据仅用于隔离实验；有运行前提的命令不代表本次已执行。各篇引用协议、内核或厂商原始资料，法规/地区频谱、软件版本、设备型号、授权和支持矩阵按目标环境复核。

## 本次验证范围

已检查文章覆盖、编号、本地链接、代码围栏和教学计算。交易部分两段Python完成语法、正常与异常输入离线检查；本部分没有执行真实网络、无线、VPN/AAA/HA、交换ASIC、PTP、NIC调参或故障注入，也没有连接交易所或生产服务。
