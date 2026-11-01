# 组播教材与学习目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有路由交换经验、希望深入行情组播与企业分发网络的工程师。9个专题、20篇正文，按机制、状态、证据、设计和排障组织；Linux相关术语在使用时解释，并链接主机教材。

先理解成员关系、树与实际转发的区别，再深入PIM/RPF和应用序列号。不把组播视作天然可靠、低延迟、授权或无损服务。

## 全部专题与文章

### 01 转发与地址

- [01 组播转发模型与地址规划](01-Forwarding-and-Addressing/01-Forwarding-and-Addressing.md)
- [02 逐跳报文与四层状态](01-Forwarding-and-Addressing/02-Packet-Walk-and-State.md)

### 02 IGMP

- [01 IGMP成员管理、版本与查询器](02-IGMP/01-IGMP.md)
- [02 源过滤与Linux主机成员关系](02-IGMP/02-Source-Filters-and-Host-Membership.md)

### 03 IGMP Snooping

- [01 IGMP Snooping与二层复制](03-IGMP-Snooping/01-IGMP-Snooping.md)
- [02 离组优化、拓扑变化与间歇故障](03-IGMP-Snooping/02-Leaves-Topology-and-Failure-Cases.md)

### 04 RPF与组播路由

- [01 RPF检查、MRIB与组播转发](04-RPF-and-Multicast-Routing/01-RPF-and-Multicast-Routing.md)
- [02 ECMP、VRF与非对称路径](04-RPF-and-Multicast-Routing/02-ECMP-VRF-and-Asymmetric-Paths.md)

### 05 PIM

- [01 PIM邻接、DR与ASM建树](05-PIM/01-PIM.md)
- [02 Register、SPT切换与Assert排错](05-PIM/02-Register-SPT-and-Assert.md)

### 06 RP与冗余

- [01 RP映射、发现与冗余设计](06-RP-and-Redundancy/01-RP-and-Redundancy.md)
- [02 RP故障与冷启动验收](06-RP-and-Redundancy/02-Failover-and-Cold-Start-Validation.md)

### 07 SSM

- [01 SSM频道模型与源发现](07-SSM/01-SSM.md)
- [02 ASM到SSM迁移与频道运营](07-SSM/02-ASM-Migration-and-Channel-Operations.md)

### 08 IPv6与MLD

- [01 IPv6组播、作用域与MLDv2](08-IPv6-and-MLD/01-IPv6-and-MLD.md)
- [02 双栈组播与控制边界](08-IPv6-and-MLD/02-Dual-Stack-and-Control-Boundaries.md)

### 09 设计、排障与实验

- [01 组播设计与分层排障](09-Design-and-Troubleshooting/01-Design-and-Troubleshooting.md)
- [02 量化行情分发、A/B Feed与容量](09-Design-and-Troubleshooting/02-Market-Data-and-Redundant-Feeds.md)
- [03 丢包定位、抓包可信度与RCA](09-Design-and-Troubleshooting/03-Loss-Localization-and-RCA.md)
- [04 组播分阶段实验与综合验收](09-Design-and-Troubleshooting/04-Lab-Guide-and-Review.md)

## 推荐阅读路径

基础转发主线：01→02→03→04→05，能独立解释成员口、RPF与建树方向后，再看06/07。量化行情重点：04–07与09，连接Linux NIC/Socket、队列和后续低延迟专题；不要跳过IGMP与二层接入。企业视频/园区重点：01–06、08/09，尤其查询器、共享端口与跨域边界。

IPv6可单独按08专题验证，但不能用IPv4测试结果代替。每个专题以正文的练习完成一次状态与数据对照，已掌握内容可通过反例自测后跳过。

## 实验与成果

当前有效的组播实验从[分阶段实验指引](09-Design-and-Troubleshooting/04-Lab-Guide-and-Review.md)开始，包含低速ASM收发示例、Snooping、跨路由及SSM验收条件。[交易实验](../../Network-Career-Lab/07-Trading/02-Labs.md)可用于后续A/B Feed和完整性分析；其中旧归档组播手册已不作为本教材依赖。

建议交付：频道目录、逐跳转发图、RP冷启动/冗余矩阵、三类故障RCA、A/B共享风险与容量分析。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)，区分教学推演、个人实测与生产经历。

## 文件与版本约定

每个新目录层级从01编号，专题内正文从01重新开始。导航按主题命名，不使用README.md。Linux命令在Linux执行，FRR命令在vtysh执行，Python代码需保存后在实验端点运行；它们不属于同一段Shell脚本。

各篇链接RFC与官方文档。IGMPv3采用RFC9776，MLDv2采用RFC9777，分别替代3376与3810。Snooping、MLAG、ECMP、计时器缺省与硬件资源因平台/版本不同，实施时核对支持与实际状态。

## 本次验证范围

本次检查正文覆盖、编号、本地链接、代码围栏与教学计算；未启动Linux/FRR实验拓扑或真实交换设备，未实测组播收敛、丢包率、微秒时延及ASIC复制性能。正文程序和步骤需在隔离环境按实际版本执行验收。
