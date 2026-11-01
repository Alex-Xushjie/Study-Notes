# Linux网络与主机性能

[返回笔记总目录](../Contents.md)

## 学习起点与范围

你已有路由交换知识，但Linux从第一次接触开始。先认识系统组件、工具与命令，再读主机数据路径，最后进入硬件与性能。新术语首次出现先解释职责，命令先拆参数再读输出。

本部分10个专题、15篇正文已形成完整初版，另有本学习导航。完成的是文档内容，不代表你已完成实验或取得生产经验。Linux安装部署、全面系统管理、内核/驱动开发与生产级数据面编程不在本部分范围。

## 全部专题与文章

| 专题 | 文章与阅读重点 |
|---|---|
| 01 Linux入门 | [01 系统组件与命令入门](01-Linux-Essentials/01-Linux-Essentials.md)；[02 进程、服务、软件包与配置](01-Linux-Essentials/02-Processes-Services-and-Packages.md) |
| 02 接口、路由与VRF | [01 网卡、地址与普通路由](02-Interfaces-Routing-and-VRF/01-Interfaces-and-Routing.md)；[02 策略路由与VRF进阶](02-Interfaces-Routing-and-VRF/02-Policy-Routing-and-VRF.md)；[03 持久化配置](02-Interfaces-Routing-and-VRF/03-Persistent-Network-Configuration.md) |
| 03 虚拟网络 | [01 Namespace、veth与Bridge](03-Namespaces-and-Virtual-Networking/01-Namespaces-and-Virtual-Networking.md)；[02 VLAN与bond](03-Namespaces-and-Virtual-Networking/02-VLAN-and-Bonding.md) |
| 04 过滤、状态与NAT | [01 Netfilter、nftables、conntrack与NAT](04-Netfilter-Conntrack-and-NAT/01-Netfilter-Conntrack-and-NAT.md) |
| 05 应用收发与协议 | [01 Socket、TCP/UDP与缓冲](05-TCP-UDP-and-Sockets/01-TCP-UDP-and-Sockets.md) |
| 06 观测与排错工具 | [01 抓包、DNS、请求、计数和日志](06-Network-Observation-Tools/01-Network-Observation-Tools.md) |
| 07 网卡与报文处理 | [01 队列、IRQ、SoftIRQ、NAPI与RSS](07-NIC-Queues-and-Packet-Processing/01-NIC-Queues-and-Packet-Processing.md) |
| 08 硬件分工与位置 | [01 Offload、CPU、NUMA与PCIe](08-Offload-CPU-NUMA-and-PCIe/01-Offload-CPU-NUMA-and-PCIe.md) |
| 09 性能分析 | [01 基线、iperf3、吞吐与尾延迟](09-Performance-Analysis/01-Performance-Analysis.md)；[02 六个综合排错案例](09-Performance-Analysis/02-End-to-End-Troubleshooting-Cases.md) |
| 10 专项处理路径 | [01 SR-IOV、eBPF/XDP、AF_XDP与DPDK](10-SRIOV-XDP-eBPF-and-Kernel-Bypass/01-SRIOV-XDP-eBPF-and-Kernel-Bypass.md) |

所有目录分别从01编号，正文在各自专题目录内从01重起。导航使用主题名称，不参与正文编号。

## 建议的三轮学习

第一轮：01入门两篇→02普通网卡/路由→03虚拟网络→04过滤/NAT→05 socket→06工具。先能画出“应用、socket、内核、接口、路由、下一跳”的关系，完成最小可达性排错。

第二轮：回读02策略/VRF与持久化→07队列处理→08硬件分工→09性能。把多出口、虚拟路径、CPU与统计联系起来，不依照名词数量判断理解程度。

第三轮：按实际岗位进入10的机制比较与相应专用实验，结合09综合案例复盘。没有硬件时可以完成认知与设计作业，但硬件操作/性能结果保持未验证。

## 工具准备与使用习惯

命令在Linux中执行，不直接用于Windows PowerShell。先用cat /etc/os-release确认发行版，再用command -v 工具名确认是否安装；软件包与驱动能力按实际系统核验。不要为读笔记一次性安装或切换全套网络管理组件。

观察类命令优先；修改类示例只用于专用实验VM/明确实验对象。每个命令都记录执行环境、接口、版本、时间和结果；错误可能来自权限、缺工具或硬件不支持，不能统一解释为网络故障。

## 配套实践与验收

先按[实验环境](../../Network-Career-Lab/00-Plan/Lab-Environment.md)准备Linux VM，再完成[已有Linux实验L1–L5](../../Network-Career-Lab/01-Linux/02-Labs.md)。现有手册覆盖路由、应用、过滤、MTU、VLAN/bond和策略路由的部分内容，不覆盖本部分所有硬件与加速专题。

本部分新增的namespace最小示例在正文给出建立、观察与清理；其余练习按各篇条件选择。pcap、配置、计数和日志保存在自己的实验记录中；不用教材模拟值填实测栏。

| 阶段 | 应留下的证据 |
|---|---|
| 基础操作 | 发行版/内核/工具版本、服务状态与接口地址 |
| 功能路径 | 正常、故障、恢复三组路由/监听/抓包与解释 |
| 虚拟与安全 | 对象关系图、hook路径、规则计数与精确清理 |
| 性能 | 固定负载、重复测试、两端/每核/队列指标、单变量对比 |
| 专项 | 能力矩阵、路径与观测边界、硬件未验证项或实测记录 |

任选两个综合案例独立完成“观测→假设→区分→修复→恢复”，再逐步增加难度。原理、操作、排错和表达可以分别评估，不能以文件已生成替代能力通过。

## 资料与验证边界

正文在对应位置链接Linux内核、iproute2手册、nftables、systemd、Netplan、iperf3与DPDK等项目资料。latest文档会更新，实际执行应以安装版本与本机帮助为准。

本次完成正文、目录、编号、链接、示例计算与文档结构核对，没有在Linux平台执行配置、抓包、压测、驱动变更或硬件调优。输出与案例明确区分教学示例、模拟数据和需要自行验证的步骤。
