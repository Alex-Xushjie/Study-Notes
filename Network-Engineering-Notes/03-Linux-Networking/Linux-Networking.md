# Linux网络与主机性能

[返回笔记总目录](../Contents.md)

## 从哪里开始

本部分的学习起点是：你已有路由交换知识，但刚开始使用Linux。网络原理按需要关联，Linux组件、工具、命令与输出从第一次接触讲起。

按下面顺序阅读，先不跳到性能调优：

1. [Linux入门：先认识系统，再学习网络命令](01-Linux-Essentials/01-Linux-Essentials.md)。认识发行版、内核、终端、Shell、进程、服务、权限、文件和命令执行环境。
2. [网卡、地址与普通路由](02-Interfaces-Routing-and-VRF/01-Interfaces-and-Routing.md)。解释接口名、ip工具和输出字段，用一块网卡的场景串起地址、网关和路由。
3. [策略路由与VRF进阶](02-Interfaces-Routing-and-VRF/02-Policy-Routing-and-VRF.md)。能够读懂基础输出后，再进入多网卡、不同路由表与虚拟路由域。

## 后续专题与状态

| 专题 | 阅读时要解决的问题 | 状态 |
|---|---|---|
| [01 Linux入门](01-Linux-Essentials/01-Linux-Essentials.md) | 系统由什么组成，命令在哪里执行、怎样读？ | 已编写 |
| [02 接口、路由与VRF](02-Interfaces-Routing-and-VRF/01-Interfaces-and-Routing.md) | 怎样先读懂普通主机，再分析多出口？ | 入门与进阶已分开 |
| [03 Namespace与虚拟网络](03-Namespaces-and-Virtual-Networking/01-Namespaces-and-Virtual-Networking.md) | 一台主机怎样提供多个独立网络环境和虚拟连接？ | 待编写 |
| [04 Netfilter、Conntrack与NAT](04-Netfilter-Conntrack-and-NAT/01-Netfilter-Conntrack-and-NAT.md) | Linux怎样过滤、记录连接状态和转换地址？ | 待编写 |
| [05 TCP、UDP与Socket](05-TCP-UDP-and-Sockets/01-TCP-UDP-and-Sockets.md) | 应用怎样收发数据，缓冲和协议怎样影响结果？ | 待编写 |
| [06 网络观测工具](06-Network-Observation-Tools/01-Network-Observation-Tools.md) | 怎样逐步使用抓包、连接状态、计数和日志？ | 待编写 |
| [07 NIC队列与报文处理](07-NIC-Queues-and-Packet-Processing/01-NIC-Queues-and-Packet-Processing.md) | 网卡接收后，系统怎样安排处理工作？ | 待编写 |
| [08 Offload、CPU、NUMA与PCIe](08-Offload-CPU-NUMA-and-PCIe/01-Offload-CPU-NUMA-and-PCIe.md) | 硬件分工、处理器和内存位置怎样影响网络？ | 待编写 |
| [09 性能分析](09-Performance-Analysis/01-Performance-Analysis.md) | 怎样区分网络、主机和应用瓶颈？ | 待编写 |
| [10 SR-IOV、XDP/eBPF与内核旁路](10-SRIOV-XDP-eBPF-and-Kernel-Bypass/01-SRIOV-XDP-eBPF-and-Kernel-Bypass.md) | 特殊加速和处理路径解决什么问题？ | 待编写 |

这些名称用于标识后续范围，不要求你在入门前认识全部术语。每个专题正式编写时先介绍所需组件与职责，再进入流程和故障。

## 后续正文的写法

- 新的Linux概念首次出现时，说明它是什么、承担什么职责、与已知网络概念有什么联系。
- 命令先拆成工具、选项、对象、动作和参数，再逐字段读示例输出。
- 先用单网卡与普通路由建立理解，再增加多网卡、隔离和性能复杂度。
- 示例接口名与地址明确标注为示例，说明如何替换为实际值。
- 用自己的输出回答一个问题，再进入下一层；不以复制执行一串命令代表理解。

## 实践环境与实验

命令在Linux中执行，不能直接套到Windows PowerShell。尚无Linux环境时，先读[实验环境说明](../../Network-Career-Lab/00-Plan/Lab-Environment.md)。功能学习可以使用专用Linux VM；硬件性能结论需要相应平台和实际测量。

本目录讲机制、输出和判断；[Linux实验手册](../../Network-Career-Lab/01-Linux/02-Labs.md)提供搭建、注入与恢复步骤。现有手册不是Linux操作入门，先完成此处基础阅读，再挑相应实验。

当前仅编写入门铺垫与第一个专题，其他专题仍为空白。文中的命令输出是教学示例，本次没有在Linux平台运行命令或完成实验验收。
