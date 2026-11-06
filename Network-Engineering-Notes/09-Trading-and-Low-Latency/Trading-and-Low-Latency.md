# 交易与低延迟教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向量化/交易网络方向的工程能力深化。10个专题、20篇正文，串联外部交付、行情组播、序号/恢复、交换/队列、主机、时钟和采集。目标是用同一业务标识和测量契约定位完整性与尾延迟问题，不把空载最小延迟当生产能力。

## 全部专题与文章

### 01 交易基础设施

- [01 交易基础设施与业务流边界](01-Trading-Infrastructure/01-Trading-Infrastructure.md)
- [02 延迟预算、测量契约与尾延迟](01-Trading-Infrastructure/02-Latency-Budgets-and-Measurement-Contracts.md)

### 02 交易所托管与连接

- [01 交易所托管、交叉连接与交付验收](02-Exchange-Colocation-and-Connectivity/01-Exchange-Colocation-and-Connectivity.md)
- [02 交易边界路由、访问与变更窗口](02-Exchange-Colocation-and-Connectivity/02-Routing-Boundaries-and-Operational-Controls.md)

### 03 行情分发

- [01 行情频道、组播与复制路径](03-Market-Data-Distribution/01-Market-Data-Distribution.md)
- [02 包、消息、会话与解析完整性](03-Market-Data-Distribution/02-Packet-Message-and-Session-Semantics.md)

### 04 Feed冗余、序号与恢复

- [01 A/B Feed、去重、缺口与恢复](04-Feed-Redundancy-Sequences-and-Recovery/01-Feed-Redundancy-Sequences-and-Recovery.md)
- [02 离线序号分析与反例验证](04-Feed-Redundancy-Sequences-and-Recovery/02-Offline-Sequence-Analysis-and-Tests.md)

### 05 低延迟交换与路径

- [01 交换路径、Cut-through与尾延迟](05-Low-Latency-Switching-and-Paths/01-Low-Latency-Switching-and-Paths.md)
- [02 ECMP、LAG与路径确定性](05-Low-Latency-Switching-and-Paths/02-ECMP-LAG-and-Determinism.md)

### 06 微突发与丢包

- [01 微突发、Buffer与丢包定位](06-Microbursts-and-Packet-Loss/01-Microbursts-and-Packet-Loss.md)
- [02 突发复现、计数器关联与反证](06-Microbursts-and-Packet-Loss/02-Burst-Reproduction-and-Counter-Correlation.md)

### 07 PTP与硬件时间戳

- [01 PTP、时钟角色、PHC与系统时钟](07-PTP-and-Hardware-Timestamping/01-PTP-and-Hardware-Timestamping.md)
- [02 时间戳位置、精度与链路不对称](07-PTP-and-Hardware-Timestamping/02-Timestamp-Points-Accuracy-and-Asymmetry.md)

### 08 TAP、Packet Broker与采集

- [01 TAP、SPAN、Packet Broker与采集容量](08-TAP-Packet-Brokers-and-Capture/01-TAP-Packet-Brokers-and-Capture.md)
- [02 抓包过滤、丢样本与证据关联](08-TAP-Packet-Brokers-and-Capture/02-Capture-Filters-Drops-and-Correlation.md)

### 09 Linux低延迟实践

- [01 Linux收包链、IRQ、队列与NUMA入门](09-Linux-Low-Latency-Practice/01-Linux-Low-Latency-Practice.md)
- [02 受控调优、轮询与Kernel Bypass](09-Linux-Low-Latency-Practice/02-Controlled-Tuning-and-Kernel-Bypass.md)

### 10 开盘负载、变更与事故

- [01 开盘负载、变更与事故处置](10-Opening-Load-Changes-and-Incidents/01-Opening-Load-Changes-and-Incidents.md)
- [02 低延迟实验、统计与综合作品](10-Opening-Load-Changes-and-Incidents/02-Lab-Guide-and-Low-Latency-Capstone.md)

## 推荐学习路径

先01建立业务与测量语言，再02–04掌握交付、组播与序列语义；05/06深化路径与突发；07/08建立时钟和采集可信度；09按Linux前置知识开展单变量实践；10完成综合作品。Linux新手先读关联主机章节，不跳到驱动解绑、绑核和全局参数修改。

## 实验与成果

入口：[分阶段实验与综合设计](10-Opening-Load-Changes-and-Incidents/02-Lab-Guide-and-Low-Latency-Capstone.md)。每篇练习区分离线推演、软件模拟、设备/射频/硬件实测和生产经历，不能将教学数值填写成自己的测量结果。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，交付拓扑、状态台账、允许/拒绝或完整性矩阵、故障时间线、反证与恢复方案。

交易建议成果：频道/session台账、A/B共同依赖图、序号/Recovery模型、延迟预算、PTP误差说明、抓包链容量、单变量调优与开盘Runbook。连接[现有交易实验](../../Network-Career-Lab/07-Trading/02-Labs.md)，其旧归档组播手册不作为本教材依赖。

## 先修与关联

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[WAN](../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)与[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)提供对应机制和操作前置。跨专题按链接阅读，不将不同Shell/NOS/协议命令混成一个脚本。

## 文件与资料约定

每层目录与专题内正文从01重新编号，导航按主题命名，不使用README.md。示例接口、地址、域名和数据仅用于隔离实验；有运行前提的命令不代表本次已执行。各篇引用协议、内核或厂商原始资料，法规/地区频谱、软件版本、设备型号、授权和支持矩阵按目标环境复核。

## 本次验证范围

已检查文章覆盖、编号、本地链接、代码围栏和教学计算。交易部分两段Python完成语法、正常与异常输入离线检查；本部分没有执行真实网络、无线、VPN/AAA/HA、交换ASIC、PTP、NIC调参或故障注入，也没有连接交易所或生产服务。
