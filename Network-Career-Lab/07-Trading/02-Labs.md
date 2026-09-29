# 交易网络实验与排错

## T1 从组播链路到业务序号

使用已有 [组播实验手册](../../Network-Engineering-Notes/02-Multicast/14-Lab-Manual/Lab-Manual.md)。本阶段只选择 IGMP/snooping、PIM/RPF、抓包相关实验，限制在本周 5h 实验与排错预算内。

先单 feed：source→L2/路由网络→receiver，确认组成员、mrouter port、组播路由、RPF 和接收接口。再建第二条独立 feed，记录二者是否共享 source、交换机、上联、电源和接收主机。

给测试 UDP 消息定义 `channel, sequence, send_time`。接收端记录接收序号、重复和乱序；不同 feed 必须有明确的业务序列对应关系。制造一个接收端不 join、一个 RPF 选错方向和一个接收应用处理变慢的故障；分别保存网络状态、主机计数器和应用日志。

验收：说明为什么“抓包没看到”可能是抓包丢包；说明 B feed 正常如何帮助业务恢复，但不能证明 A feed 故障位置。没有双物理路径时标记逻辑冗余模拟。

## T2 延迟预算与测量

教学路径：2 km 光纤，3 台交换机，每台处理预算 0.5 µs，100G 链路发送 1500 bytes；主机处理预算 5 µs。先按题目给定模型计算：传播约 10 µs，交换合计 1.5 µs，一次该大小序列化约 0.12 µs，主机 5 µs，总约 16.62 µs。

这只是**题目定义的简化预算**：是否重复计入多跳序列化、交换延迟是否已包含序列化、cut-through 的重叠以及协议开销必须在真实测量中说明，不能把这一个数字视为实际线路结果。

在 Linux 实验端点测 RTT 可先用 ping，测吞吐可用 iperf3，两者都不是交易应用的一跳精密时延。记录样本数量和负载；引入可控竞争流，再比较分位数和丢包。至少重复三次，在相同条件下看结果是否稳定。

## T3 PTP / NIC / CPU 观察

只读基线：

```bash
ethtool -T eth0
ethtool -k eth0
ethtool -l eth0
ethtool -c eth0
cat /proc/interrupts
lscpu
```

`eth0` 替换为实验 NIC。保存 PHC index、支持的收发 timestamp、队列、coalescing、CPU/NUMA。没有硬件时间戳时提交“能力边界说明”，不要承诺精度。

有隔离 PTP 环境时：先确定 GM 与 client 角色、profile/domain/transport，再按 linuxptp 文档配置 `ptp4l`；需要系统时钟与 PHC 同步时配置 `phc2sys`，避免多个服务同时调同一时钟。记录 offset、path delay、port state、GM identity；测试 GM 故障，观察切换和 holdover，而非只看进程活着。

主机进阶：用已知测试程序固定 CPU、固定 NUMA，再逐项改变 coalescing/IRQ。每次保存原值并恢复。普通 VM 的调度抖动可能掩盖效果，此时结论应是“环境不足以证明”。

## T4 完整排错案例

场景：每天开盘几秒内行情 gap 上升，链路平均使用率仅 15%，BGP/PIM 都正常。

调查路径：

1. 从应用确定 channel、序号、时间窗与影响服务器范围。
2. 比较 A/B，以及正常/异常接收机；确定共同点。
3. 查交换机队列丢弃和短时利用率，不能拿 5 分钟平均排除 microburst。
4. 查 NIC ring/error、softnet/socket drop、CPU/NUMA 和应用处理积压。
5. 对齐抓包位置和时间；检查记录器自身丢包。
6. 用实验复现支持某一假设，实施一个变更，再以相同负载比较。

至少列两个可推翻自身假设的证据。交付 RCA：影响、时间线、事实与假设、根因证据、修复、预防、尚未确认的事项。英文结尾练习：*The average link utilization did not rule out a short burst. We correlated queue drops with the affected sequence range before changing the configuration.*

W24 验收：用已有 [白板题](../../Quant%20Trading/90-Interview-Drills/03-Whiteboard-Cases.md) 选一道，30 分钟录制，覆盖需求、拓扑、故障域、测量、运维取舍。不要跳过前六阶段只做面试背诵。
