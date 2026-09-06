# 10 天面试冲刺计划

## 先建立唯一主线

```text
Exchange multicast A/B
        |
        v
edge/ULL switch -> feed handler -> normalized book -> strategy
                                               |
                                               v
Exchange ACK/fill <- session/order gateway <- pre-trade risk
        |
        +---- drop copy / reconciliation / surveillance

GNSS -> Grandmaster -> PTP-aware network -> NIC PHC -> host/application
TAP/MetaWatch ---------------------------> recorder / latency analytics
```

你要能沿着一条行情消息走到策略，再沿着一张订单走到撮合引擎并返回 ACK/fill；每一跳都能回答：

- 为什么存在？
- 延迟和抖动来自哪里？
- 如何测量？
- 坏了会怎样？
- 如何切换且不制造更大的事故？

## 每日安排（每天 3～4 小时）

| Day | 输入 | 必须产出的口述/白板结果 |
|---|---|---|
| 1 | Global architecture + MD/OE | 5 分钟画出一个双 venue、双 colo 架构 |
| 2 | Multicast | 从 IGMP join 讲到 gap recovery；排查“单台服务器丢包” |
| 3 | Colo buildout | 从 LOA/CFA、cross-connect 讲到 production certification |
| 4 | WAN/DCI/carrier | 解释 route diversity、latency budget、BGP/BFD 边界 |
| 5 | HA/failure domains | 做 5 个故障演练，明确检测、收敛、业务影响 |
| 6 | Migration/cutover + exchange ecosystem | 写 1 页 MOP，讲清 rollback trigger |
| 7 | Timestamp/PTP/TAP | 画出 t1/t2/t3/t4；区分 TAP、SPAN、NIC/FPGA timestamp |
| 8 | PCAP + routing + physical | 用证据链排查 loss/latency，复习 optics/counters |
| 9 | Linux/NIC/NUMA/kernel bypass + monitoring | 解释调优副作用和可观测性 |
| 10 | 全真模拟 | 90 分钟：自我介绍、8 道知识题、3 道场景题、反问 |

时间只有 3 天时：Day 1 读 Tier 1 的 01/05/06；Day 2 读 02/03/07/08；Day 3 读 Tier 2 全部、速查表并模拟。

## 每章的学习动作

不要只阅读。每章完成以下闭环：

1. 合上笔记画架构图。
2. 用 30 秒给定义，用 2 分钟给设计，用 5 分钟处理追问。
3. 为设计主动说出至少三个 trade-off。
4. 给出一个真实故障和证据链。
5. 不会的厂商命令可以承认，但必须说出 vendor-neutral 的验证对象。

## 面试表达原则

- 不说“零丢包”“瞬时切换”“完全冗余”；说清假设、范围和 measurement point。
- 不把 HA 等同于两台设备。共同光路、共同 PDU、共同控制面仍然是单点。
- 不直接报一个 latency 数字。先限定 frame size、load、direction、percentile、timestamp point。
- 不先调 buffer。先定位 loss 发生在 ingress、fabric、egress、NIC、kernel 还是 application。
- 不把 routing convergence 当成 application recovery。TCP/FIX session、sequence 和订单状态仍需恢复。

## 经验题准备模板（STAR+Evidence）

- **Situation**：业务、venue、规模、约束。
- **Task**：你的责任边界和成功指标。
- **Action**：关键判断、设计/排障动作、与谁协作。
- **Result**：p99/p99.9 latency、loss、RTO、变更时长或 incident reduction。
- **Evidence**：PCAP、hardware timestamp、counter、日志、演练结果。
- **Learning**：以后如何让系统更安全/更可测。

