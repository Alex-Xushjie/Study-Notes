# 交易网络：数据完整性与尾延迟一起看

## 1. 一条消息和一张订单

```text
Exchange → Feed A/B → cross-connect → network → feed handler → strategy
strategy → risk/order gateway → order-entry session → Exchange
Exchange → ACK/fill → order gateway / reconciliation
```

Market data 发布行情，order entry 提交/撤改单并接收回报；传输协议、恢复机制和 session 行为按交易所接口规范决定，不能把“行情用 UDP，订单一定 TCP”当作所有 venue 的通用保证。

Colo 是部署位置及服务条件，cross-connect 是物理连接服务；两个标签不同的 circuit 可能共用管道、电源或交换设备。A/B feed 是冗余行情来源，接收端可能按序号选择/去重，不是任意把两个 multicast 包流合并就完成业务冗余。

## 2. 组播故障分层

IGMP 表达接收兴趣，snooping 决定二层转发端口，PIM/RPF 决定跨三层的组播路径。RPF 检查方向依赖到源或 RP 的相应路由信息；不能只看接收端到源的 ping。源、组、接口和 VRF 都应进入排错记录。

行情序号 gap 可能来自源端、链路丢包、NIC ring、socket buffer、应用处理或抓包自身丢包。先比较 A/B 同一业务序列的接收情况，再对齐不同观测点。应用协议可能重置序号或按 channel 计数，需要读接口定义。

必读补充：[已有 Market Data / Order Entry 笔记](../../Quant%20Trading/01-Tier-1/05-Market-Data-Order-Entry.md)、[组播笔记](../../Quant%20Trading/01-Tier-1/06-Multicast.md)。只复习与当前实验相关段落，不重新背全部 PIM 命令。

## 3. 延迟预算

总延迟包含传播、序列化、交换处理、排队、NIC/PCIe、内核与应用。序列化用 bits/rate 估算：1500 bytes 在 10 Gbit/s 上是 1.2 µs，在 100 Gbit/s 上是 0.12 µs；这是所选字节数的简化计算，真实 wire time 还涉及 Ethernet 开销。光纤传播可先按约 5 µs/km 做数量级估算，实际取决于介质和物理长度。

Store-and-forward 等待完整帧后再转发，cut-through 可更早开始转发；是否生效还取决于设备模式、端口速率组合和包处理。队列引入的尾部延迟可能大于名义交换延迟，因此要记录 p50/p95/p99/max、包长、pps 和负载。

不要把 RTT/2 当成精确单向时延；非对称路径和端点处理会破坏这个假设。单向时间差必须考虑两端时钟偏差、漂移、timestamp 位置与测量装置误差。

## 4. PTP 与硬件时间戳

PTP 协助同步时钟，Grandmaster、boundary/transparent clock、网卡 PHC 和系统时钟是不同角色。`ptp4l` 与 `phc2sys` 的职责不同，配置须符合网络 transport、profile、domain 和时间戳能力。参考 [linuxptp ptp4l 手册](https://www.linuxptp.org/documentation/ptp4l/) 的 timestamping 和 clock 配置。

先运行 `ethtool -T` 判断 NIC 支持什么；VM 软件时间戳实验不能证明亚微秒硬件精度。offset 小也不能单独证明端到端测量准确，路径不对称可能造成系统性偏差。

已有 [PTP 学习材料](../../Quant%20Trading/02-Tier-2/03-PTP.md) 可继续阅读。保留参考时钟、测量位置、同步状态、时间单位与误差预算。

## 5. Kernel bypass 与主机调优

DPDK 常以用户态 polling 和专用数据面减少部分内核路径开销；Onload 属于另一类加速方案，API、NIC、协议支持与部署条件不同；Solarflare/ExaNIC 等产品不能只按名称视为同一种能力。选型和功能以对应版本官方文档为准。

CPU pinning、NUMA local memory、IRQ affinity、RSS 和 interrupt coalescing 都是实验变量。减少 coalescing 可能降低等待，同时提高 CPU/中断开销。关闭所有 offload 不一定更快；先测基线，单变量测试，比较尾延迟、丢包和 CPU，而不是只看平均时延。

自测：A 有 gap、B 没有 gap，应先做什么？参考：对齐 channel/sequence/time，定位首次出现差异的位置；不能直接把问题归到交换机。
