# AI/HPC：先理解工作负载，再配置“无损”网络

## 1. 修正原计划里的一个前提

GPU 集群可以使用 TCP Ethernet；分布式训练能否达到目标效率，取决于计算/通信比例、collective 模式、CPU 开销、网络延迟、带宽等。RDMA 的价值在于使用 NIC 能力减少数据搬运和协议处理开销，不是“GPU 无法运行 TCP”。不要把某个优化方案当作应用运行的必要条件。

RDMA 提供对已注册内存的高效访问能力，涉及 memory registration、queue pair、completion queue 等概念。先知道应用怎样提交 work request、怎样发现完成即可，不要求本阶段写 verbs 程序。GPUDirect RDMA 还涉及 GPU/NIC/PCIe 拓扑和软件支持，不能等同于任意 RDMA 操作。

## 2. 三个名字分清

| 技术 | 网络基础 | 学习重点 |
|---|---|---|
| InfiniBand | 独立 fabric/协议体系 | 管理、路由与流控不照搬 Ethernet |
| RoCE v1 | 二层 Ethernet | 不具备 RoCEv2 的 IP 路由能力 |
| RoCE v2 | UDP/IP 承载 RDMA，常见目的端口 4791 | IP 可路由，可靠性与拥塞处理不是 TCP |

不能因 RoCEv2 用 UDP 就推导“RDMA 一定不可靠”；可靠性取决于 RDMA transport 类型与 NIC 协议处理。也不能用 TCP iperf 正常证明 RDMA 正常。

## 3. PFC、ECN、CNP、DCQCN 的反馈链

```text
交换队列拥塞 → ECN 标记 → 接收 NIC 产生 CNP → 发送 NIC 调整速率
        |
        +→ 达到流控条件时，PFC 对相邻链路指定优先级发 pause
```

PFC 是逐跳、按优先级的暂停机制；ECN 是包内拥塞信号；CNP 是反馈；DCQCN 是端系统依据反馈调整发送速率的算法。正常目标是尽早缓解拥塞，避免长期靠 PFC 暂停维持运行。DCQCN 背景阅读使用作者的 [Microsoft Research 论文](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/lossless.pdf)，先看问题、控制环和实验设计，不必第一遍推导所有公式。

PFC 可能引入 head-of-line blocking、拥塞扩散，某些条件下可能死锁。没有 pause 计数不代表没有拥塞；有少量 pause 也不自动等于应用故障。应将 ECN/CNP、pause duration、丢包、吞吐和任务完成时间联系起来看。具体 lossless/lossy/拥塞配置按 NIC、交换 ASIC、驱动版本验证，不能把一个平台的推荐值复制到所有设备。参考 [NVIDIA Cumulus RoCE 文档](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/) 的模式与观测项。

## 4. QoS 是一整条映射链

应用流量标记 → NIC DSCP/PCP → switch trust → internal priority → egress queue → ECN/PFC/buffer → 对端 NIC。任意一段映射不一致都可能让 RDMA 流量落到不期望的队列。CNP 与数据流量如何分类也要按部署方案核验。

Buffer 预算包括共享池、队列阈值和用于暂停生效前在途数据的 headroom。简单理解：需要吸收的在途字节与链路速率和反应时间相关；`bytes ≈ bit/s × seconds ÷ 8` 只是估算起点，不能据此生成硬件阈值。真实设置还受线缆、ASIC、MTU、管线和平台机制影响。

Incast 是多发送端同时汇聚到有限出口；平均利用率低也可能有瞬时队列。Elephant flow 指长时间/大体量流，对 ECMP hash 碰撞和公平性敏感。应测多对多、many-to-one，而不只测一对主机。

## 5. 从链路到 collective

NCCL 等通信库执行 AllReduce、AllGather 等 collective。应用迭代常要等待慢节点/慢路径，因此尾部性能和跨节点一致性很重要。链路 400G 不是 AllReduce 一定能跑出 400G；算法通信量、拓扑、GPU/PCIe、NUMA 和消息大小都会影响。

测量分三层：链路与错误计数 → RDMA microbenchmark → collective / 实际训练。NCCL tests 的 `algbw` 和 `busbw` 不是同一个指标，解释时注明 collective 和归一化口径。工具入口：[NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests)。

## 自测

- 为什么“打开 PFC”不等于完成 RoCE 调优？参考：QoS 映射、拥塞控制、队列/缓冲、端系统与业务测量仍缺失。
- ECN 正常但吞吐低，应看什么？参考：CNP、发送端反应、队列映射、NIC/PCIe/GPU、路径与拓扑，不仅调整一个阈值。
- 一条 RDMA 流吞吐不足，为何加 ECMP 链路未必有效？参考：流 hash、多 QP、NIC 能力及拥塞位置。
