# 园区与无线教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有路由交换经验、希望补齐办公园区与无线运维的工程师。9个专题、18篇正文，从业务与故障域到RF、接入、控制、身份、容量、漫游和RCA。目标是解释真实用户路径，完成可验证设计和分层排障，不以信号格或AP在线代替业务验收。

## 全部专题与文章

### 01 园区架构

- [01 园区分层、故障域与业务路径](01-Campus-Architecture/01-Campus-Architecture.md)
- [02 接入口、PoE与维护恢复](01-Campus-Architecture/02-Access-Ports-PoE-and-Resilience.md)

### 02 DHCP、DNS、NTP与IPAM

- [01 DHCP、DNS、NTP与地址台账](02-DHCP-DNS-NTP-and-IPAM/01-DHCP-DNS-NTP-and-IPAM.md)
- [02 基础服务保护与恢复风暴](02-DHCP-DNS-NTP-and-IPAM/02-Service-Protection-and-Recovery.md)

### 03 无线射频

- [01 射频、RSSI、SNR与传播](03-Wireless-RF/01-Wireless-RF.md)
- [02 信道宽度、干扰与空间复用](03-Wireless-RF/02-Channel-Width-Interference-and-Reuse.md)

### 04 802.11接入与性能

- [01 802.11接入过程与性能开销](04-80211-Access-and-Performance/01-Access-and-Performance.md)
- [02 Airtime、WMM与无线组播](04-80211-Access-and-Performance/02-Airtime-QoS-and-Multicast.md)

### 05 AP、控制器与转发

- [01 AP上线、控制器与转发模式](05-AP-Controllers-and-Forwarding/01-AP-Controllers-and-Forwarding.md)
- [02 控制失联、HA与无线升级](05-AP-Controllers-and-Forwarding/02-WAN-Outage-HA-and-Upgrades.md)

### 06 覆盖、容量与勘测

- [01 覆盖、容量与现场勘测](06-Coverage-Capacity-and-Site-Surveys/01-Coverage-Capacity-and-Site-Surveys.md)
- [02 高密度容量测试与验收](06-Coverage-Capacity-and-Site-Surveys/02-High-Density-and-Acceptance.md)

### 07 漫游与移动性

- [01 漫游决策、802.11k/v/r与移动性](07-Roaming-and-Mobility/01-Roaming-and-Mobility.md)
- [02 漫游排障与语音连续性](07-Roaming-and-Mobility/02-Roaming-Troubleshooting-and-Voice.md)

### 08 员工、访客、BYOD与IoT

- [01 员工、访客、BYOD与IoT分区](08-Employee-Guest-BYOD-and-IoT/01-Employee-Guest-BYOD-and-IoT.md)
- [02 终端入网、隔离与生命周期](08-Employee-Guest-BYOD-and-IoT/02-Onboarding-Isolation-and-Lifecycle.md)

### 09 无线排障与实验

- [01 无线分层排障与证据链](09-Wireless-Troubleshooting/01-Wireless-Troubleshooting.md)
- [02 园区无线实验与综合设计](09-Wireless-Troubleshooting/02-Lab-Guide-and-Campus-Capstone.md)

## 推荐学习路径

先01/02建立园区与服务依赖，再03/04理解RF和空口，05/06连接转发与现场设计，07/08深化移动和终端角色，09完成综合实验。已有经验可通过每篇反例自测后跳过。办公运维重点关注供电、地址/身份、客户端兼容和故障恢复；RF不能仅靠虚拟控制器验证。

## 实验与成果

入口：[分阶段实验与综合设计](09-Wireless-Troubleshooting/02-Lab-Guide-and-Campus-Capstone.md)。每篇练习区分离线推演、软件模拟、设备/射频/硬件实测和生产经历，不能将教学数值填写成自己的测量结果。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，交付拓扑、状态台账、允许/拒绝或完整性矩阵、故障时间线、反证与恢复方案。

园区建议成果：PoE与N-1预算、RF勘测/容量方案、漫游测量、终端入网矩阵与三类RCA。没有现场RF条件时明确热力图与覆盖假设，不能证明真实容量。

## 先修与关联

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[WAN](../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)与[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)提供对应机制和操作前置。跨专题按链接阅读，不将不同Shell/NOS/协议命令混成一个脚本。

## 文件与资料约定

每层目录与专题内正文从01重新编号，导航按主题命名，不使用README.md。示例接口、地址、域名和数据仅用于隔离实验；有运行前提的命令不代表本次已执行。各篇引用协议、内核或厂商原始资料，法规/地区频谱、软件版本、设备型号、授权和支持矩阵按目标环境复核。

## 本次验证范围

已检查文章覆盖、编号、本地链接、代码围栏和教学计算。交易部分两段Python完成语法、正常与异常输入离线检查；本部分没有执行真实网络、无线、VPN/AAA/HA、交换ASIC、PTP、NIC调参或故障注入，也没有连接交易所或生产服务。
