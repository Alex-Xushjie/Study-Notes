# Headroom、Pause风暴与验证

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. Headroom为何存在

发出暂停到上游真正停发有传播、处理、在途帧和管线时延，缓冲需吸收剩余流量。教学数量级400Gb/s×2微秒÷8=100000字节，只表示该时间发送量，不是可直接下发的Headroom值。

实际需考虑速率、线长、MTU、FEC/管线、平台Buffer分配、暂停反应和安全余量；入口Headroom与出口ECN阈值也不是同一对象。共享池、静态/动态阈值按ASIC定义。

## 2. PFC副作用

某优先级的阻塞可能影响同优先级其他流，形成Head-of-line Blocking或拥塞扩散；循环依赖还可能出现严重停顿。PFC Watchdog等机制按平台可检测/处置，但可能丢包或降级，需要业务认可和验证。

| 症状 | 首先核对 |
|---|---|
| 吞吐低、Pause高 | 热点、映射、阈值、端点是否反应 |
| ECN很少但拥塞明显 | 标记路径、Trust、计数语义 |
| 单对正常多对退化 | Incast、公平性、出口和端点 |
| 无Pause但仍重试 | 丢失模式/端点能力，不认为必然无拥塞 |
| 恢复后仍停顿 | 循环、Watchdog、资源和作业状态 |

## 3. 验证方法

单对基线→多对一→多对多→长短消息混合→故障与恢复，固定版本/Rank/参数。记录Pause时间、ECN/CNP、重试/丢弃、队列和端点速率；按窗口差值分析，不机械追求所有计数为0。

## 4. 实验边界

用Soft-RoCE学API不能验证ASIC/PFC；普通TCP打满链路不能替代RDMA端点反馈。参数变更逐项、保存原值和恢复标准，不引用教材数量直接改Headroom。

[RoCE平台文档](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/)、[突发与Buffer基础](../../01-Routing-and-Switching/10-QoS/02-Buffers-Microbursts-and-Validation.md)。
