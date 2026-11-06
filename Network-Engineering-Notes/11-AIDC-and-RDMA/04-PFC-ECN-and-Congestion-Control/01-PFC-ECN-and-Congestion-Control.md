# PFC、ECN与拥塞反馈链

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 两种反馈不一样

PFC按链路优先级暂停相应发送，用于缓解相应缓冲压力；ECN在数据报文中标记拥塞，RoCE接收端与发送端可通过CNP/端点算法等形成反馈。PFC是局部逐跳作用，不能画成接收应用直接给源端一个全网Pause。

DSCP、802.1p优先级、Traffic Class/队列、PFC优先级和ECN位不是同一个字段。内外层映射、Trust与重标记需端到端一致，ECN有自己的位与语义。

| 链条 | 应看证据 |
|---|---|
| 业务分类 | NIC标记、交换机信任和队列映射 |
| 排队 | 出口占用、阈值和丢弃 |
| 拥塞通知 | ECN标记、接收端CNP/反馈 |
| 发送反应 | 端点速率/算法状态和性能变化 |
| 局部背压 | PFC收发方向、持续时间与优先级 |

## 2. 算法与平台

DCQCN可作为ECN闭环例子，当前NIC/软件可能支持其他算法。开关、参数、计数器语义和推荐组合随硬件/版本变化，不复制一组阈值到所有交换机。平台所称Lossless/Lossy/Resilient模式需按官方支持与目标业务验证。

## 3. 设计目标

尽量在严重丢弃/长期Pause前让端点有效反应，同时维持公平、利用率与尾部。Pause多不是配置成功的证明，ECN/CNP多也不自动代表业务变好；必须关联队列、端点与作业。

## 4. 练习

画数据、ECN、CNP和PFC方向，故意在纸面把RDMA映到默认队列，说明四处取证。实验仅用隔离Fabric，不在共享GPU集群盲目开全优先级PFC。

[Cumulus RoCE官方说明](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/)、[NVIDIA拥塞机制](https://enterprise-support.nvidia.com/s/article/understanding-rocev2-congestion-management)。
