# AIDC与RDMA教材目录

[返回笔记总目录](../Contents.md)

## 学习定位

本部分按既定职业规划作为拓宽方向，重点学习AI通信需求、端点拓扑、RDMA与拥塞反馈、容量和联合排障。6个专题、13篇正文，不替代GPU算法/完整HPC课程，也不要求先投入大量资源转岗。没有真实硬件时有明确离线学习与证据边界。

## 全部专题与文章

### 01 AI通信与Collective

- [01 训练与推理通信：先认识Rank和Collective](01-AI-Communication-and-Collectives/01-AI-Communication-and-Collectives.md)
- [02 通信模式、算法带宽与总线带宽](01-AI-Communication-and-Collectives/02-Communication-Patterns-and-Bandwidth-Metrics.md)

### 02 GPU、NIC、PCIe与NUMA

- [01 GPU、NIC、PCIe与NUMA拓扑](02-GPU-NIC-PCIe-and-NUMA/01-GPU-NIC-PCIe-and-NUMA.md)
- [02 GPUDirect RDMA与实际数据路径](02-GPU-NIC-PCIe-and-NUMA/02-GPUDirect-RDMA-and-Data-Paths.md)

### 03 RDMA、RoCE与InfiniBand

- [01 RDMA、RoCE与InfiniBand基础](03-RDMA-RoCE-and-InfiniBand/01-RDMA-RoCE-and-InfiniBand.md)
- [02 QP、MR、CQ与RDMA排障](03-RDMA-RoCE-and-InfiniBand/02-QP-MR-CQ-and-Transport-Troubleshooting.md)

### 04 PFC、ECN与拥塞

- [01 PFC、ECN与拥塞反馈链](04-PFC-ECN-and-Congestion-Control/01-PFC-ECN-and-Congestion-Control.md)
- [02 Headroom、Pause风暴与验证](04-PFC-ECN-and-Congestion-Control/02-Headroom-Pause-Storms-and-Validation.md)

### 05 Rail、容量与光互联

- [01 Rail、容量与故障后的通信](05-Rails-Capacity-and-Optical-Interconnects/01-Rails-Capacity-and-Optical-Interconnects.md)
- [02 光互联、FEC、Breakout与BOM核对](05-Rails-Capacity-and-Optical-Interconnects/02-Optics-FEC-Breakout-and-BOM.md)

### 06 测试、性能分析与实验

- [01 RDMA、NCCL测试与指标解释](06-RDMA-NCCL-and-Performance-Analysis/01-RDMA-NCCL-and-Performance-Analysis.md)
- [02 作业挂起、慢Rank与跨层RCA](06-RDMA-NCCL-and-Performance-Analysis/02-Hangs-Slow-Ranks-and-Cross-Layer-RCA.md)
- [03 AIDC分档实验与能力边界](06-RDMA-NCCL-and-Performance-Analysis/03-Lab-Guide-and-AIDC-Capstone.md)

## 推荐使用路径

先01/02理解业务与服务器，03建立RDMA资源/传输概念，再04/05分析反馈和容量，06按硬件档位验证。主线仍优先此前确定的组播/低延迟/Linux或WAN/云/安全；AIDC取得真实项目/硬件后再深化，不用纸面方案替代生产经验。

## 实验与成果

入口：[综合实验或评审](06-RDMA-NCCL-and-Performance-Analysis/03-Lab-Guide-and-AIDC-Capstone.md)。区分离线推演、软件模拟、硬件实测与生产经历，交付拓扑/对象、正常/异常/恢复、反证与结论边界。使用[实验报告模板](../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)和[设计模板](../../Network-Career-Lab/08-Portfolio/Design-and-Interview.md)。

配套[AI/HPC实验H1–H4](../../Network-Career-Lab/06-AI-HPC/02-Design-and-Labs.md)，包含明确假设的1000GPU容量题。不能以Soft-RoCE证明硬件拥塞或GDR，也不以单机NCCL证明跨节点RDMA。

## 关联与约定

[路由交换](../01-Routing-and-Switching/Routing-and-Switching.md)、[组播](../02-Multicast/Multicast.md)、[Linux](../03-Linux-Networking/Linux-Networking.md)、[自动化](../04-Network-Automation/Network-Automation.md)、[云网络](../06-Cloud-and-Hybrid-Networking/Cloud-and-Hybrid-Networking.md)与[交易低延迟](../09-Trading-and-Low-Latency/Trading-and-Low-Latency.md)提供相关前置。每层目录/正文从01编号，导航按主题命名，不使用README.md。

引用协议、软件项目及厂商原始资料；latest文档不是本地版本。设备/接口/地址、命令执行环境、硬件支持、授权和容量需按实际目标核对，示例不构成通用生产配置或采购清单。

## 本次验证范围

本次检查正文覆盖、编号、本地链接、代码围栏和容量/封装计算；工程容量Python示例完成语法与正常/异常输入离线验证。未运行Fabric、EVPN硬件、GPU/RDMA/NCCL或真实故障注入，未连接生产设备/服务。所有性能数字为给定假设下的教学推导。
