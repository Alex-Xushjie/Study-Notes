# 数据中心网络教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分面向已有路由交换经验、需要理解现代数据中心Fabric的工程师。7个专题、15篇正文，覆盖Clos、Underlay、VXLAN、EVPN、IRB、多归属、边界、迁移与排障。目标是能沿业务流解释控制/数据依赖并给出设计与证据，不把BGP路由存在当成业务成功。

## 全部专题与文章

### 01 Clos、Underlay与ECMP

- [01 Clos、Leaf-Spine与Underlay](01-Clos-Underlay-and-ECMP/01-Clos-Underlay-and-ECMP.md)
- [02 超卖、ECMP与N-1容量](01-Clos-Underlay-and-ECMP/02-Oversubscription-ECMP-and-N-1.md)

### 02 VXLAN、VTEP与VNI

- [01 VXLAN封装、VTEP与VNI](02-VXLAN-VTEP-and-VNI/01-VXLAN-VTEP-and-VNI.md)
- [02 MTU、BUM与ARP抑制](02-VXLAN-VTEP-and-VNI/02-MTU-BUM-and-ARP-Suppression.md)

### 03 EVPN控制面

- [01 EVPN路由类型、RD/RT与安装](03-EVPN-Control-Plane/01-EVPN-Control-Plane.md)
- [02 MAC移动、重复地址与控制面排障](03-EVPN-Control-Plane/02-MAC-Mobility-and-Control-Plane-Troubleshooting.md)

### 04 Anycast Gateway与IRB

- [01 Anycast Gateway与对称/非对称IRB](04-Anycast-Gateway-and-IRB/01-Anycast-Gateway-and-IRB.md)
- [02 主机路由、Type5与网关故障案例](04-Anycast-Gateway-and-IRB/02-Host-Routes-Type5-and-Gateway-Cases.md)

### 05 EVPN多归属

- [01 EVPN多归属、ESI、DF与防环](05-EVPN-Multihoming/01-EVPN-Multihoming.md)
- [02 多归属故障矩阵与MLAG取舍](05-EVPN-Multihoming/02-Multihoming-Failure-Matrix-and-MLAG-Comparison.md)

### 06 边界与租户分段

- [01 Border Leaf、租户分段与共享服务](06-Border-Connectivity-and-Tenant-Segmentation/01-Border-Connectivity-and-Tenant-Segmentation.md)
- [02 外部前缀、DCI与路由反馈](06-Border-Connectivity-and-Tenant-Segmentation/02-External-Routes-DCI-and-Loop-Prevention.md)

### 07 设计、迁移与排障

- [01 Fabric设计、分层排障与证据链](07-Design-Migration-and-Troubleshooting/01-Design-Migration-and-Troubleshooting.md)
- [02 传统网络迁移、扩容与回退](07-Design-Migration-and-Troubleshooting/02-Migration-and-Change-Control.md)
- [03 数据中心实验与综合设计](07-Design-Migration-and-Troubleshooting/03-Lab-Guide-and-Data-Center-Capstone.md)

## 推荐使用路径

先01/02确认承载和封装，再03/04建立控制与IRB，05按实际支持深化多归属，06/07完成边界和迁移。企业云/WAN路线重点IRB、租户和Border；量化路线关注ECMP、队列、故障域和测量。实现选择先固定平台/版本，FRR与Linux数据面对象需配合。

## 实验与成果

入口：[综合实验或评审](07-Design-Migration-and-Troubleshooting/03-Lab-Guide-and-Data-Center-Capstone.md)。区分离线推演、软件模拟、硬件实测与生产经历，交付拓扑/对象、正常/异常/恢复、反证与结论边界。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)和[设计模板](../../Network-Career-Lab/08-Portfolio/Design-and-Interview.md)。

配套[数据中心实验D1–D4](../../Network-Career-Lab/05-Data-Center/02-Labs.md)，先最小单Spine闭环再扩冗余；正文较完整拓扑用于后续。软件FRR可验证部分协议/转发，不证明ASIC容量或多厂商硬件特性。

## 关联与约定

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)与[交易低延迟](../09-Trading-and-Low-Latency/Trading-and-Low-Latency.md)提供相关前置。每层目录/正文从01编号，导航按主题命名，不使用README.md。

引用协议、软件项目及厂商原始资料；latest文档不是本地版本。设备/接口/地址、命令执行环境、硬件支持、授权和容量需按实际目标核对，示例不构成通用生产配置或采购清单。

## 本次验证范围

本次检查正文覆盖、编号、本地链接、代码围栏和容量/封装计算；工程容量Python示例完成语法与正常/异常输入离线验证。未运行Fabric、EVPN硬件、GPU/RDMA/NCCL或真实故障注入，未连接生产设备/服务。所有性能数字为给定假设下的教学推导。
