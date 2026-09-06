# 高频问题与场景演练

## 使用方法

每题先 30 秒给结论，再 2 分钟展开：requirements → design → failure → measurement → trade-off。答案提示不是背诵稿；把你自己的项目规模、指标和证据填进去。

## A. 架构题

### 1. Design a global trading network

必须覆盖：按 traffic plane 分区；colo 内 hot path；MD A/B 与 OE/drop copy；routed DCI；carrier/facility diversity；PTP/OOB/capture；容量与 tail；地区故障和业务恢复。

追问：“如果 WAN 断了能继续交易吗？”

> 取决于本地是否拥有足够的新鲜 market data、position/limits 和 authoritative risk state。预先定义 autonomous window、limit、fail-closed 条件及恢复后的 reconciliation，而不是由网络自行决定。

### 2. Build a new exchange colo from zero

商业/端口订单 → LOA/CFA/cross-connect/power → staged golden config → L1/2/3 → feed/session → conformance/rehearsal → latency/failure acceptance → handover。主动提 remote hands、spares、OOB、标签与 as-built。

### 3. L2 or L3 in a low-latency colo?

L2 hop 简单，但 domain/loop/flood 大；L3 可控、可扩展、收敛明确。基于规模和 venue delivery 选择；跨机柜/DC 默认倾向小 L2 + routed boundary。额外 hop 的影响要实测，不用教条。

### 4. Shallow or deep buffer?

Shallow：正常时低 latency，但 microburst 易 loss。Deep：吸收 burst/WAN speed mismatch，但产生 stale queue/tail。按业务对 loss vs stale latency 的代价选择，并设计容量、watermark 和 overload behavior。

## B. Market data / order entry

### 5. How do redundant A/B feeds work?

通常同时接收，按 venue 定义的 sequence 做 first-arrival arbitration 和 de-dup；gap 时先从另一线/缓存补，再 retransmission/snapshot。两线必须跨真实 failure domain。不能把 A/B 简化为 STP active/standby。

### 6. How do you recover a sequence gap?

标记 channel/book stale → 缓存后续增量 → 找缺失范围 → redundant line/retransmission → 过大则 snapshot → 从 snapshot sequence replay → invariant check → healthy。恢复期间策略行为预定义。

### 7. UDP is unreliable. Why use it for market data?

一对多、无 sender head-of-line/慢 receiver 反馈、低 overhead；feed protocol 用 sequence、A/B、retransmission/snapshot 提供应用级恢复。行情更重视所有 receiver 同步收到最新数据，而不是 TCP 对单一慢 receiver 重传旧数据。

### 8. FIX vs binary protocol?

FIX 标准语义、易集成/观察但更冗长，venue implementation 仍不同；native binary 紧凑、固定布局、低解析开销但开发认证成本高。选择由 latency、功能、团队和 venue support 决定。

### 9. OE connection dropped after sending an order. What now?

这是 unknown state；禁止盲目重发。按 venue session recovery/cancel-on-disconnect 语义重连，以 stable client ID、drop copy/open orders 对账，必要时 mass cancel，由风险 owner 确认后恢复。

### 10. Why is drop copy needed?

独立于主 OE session 的订单/成交核对、风险/监控/合规来源。它降低主 session 丢事件的风险，但仍需处理自身延迟、gap、duplicate 和 venue 语义。

## C. Multicast

### 11. Explain IGMP, snooping, PIM and RPF

IGMP 表达 host membership；snooping 在 L2 建 group-to-port；PIM 在 routers 构建 tree；RPF 根据到 source 的反向路由验证入接口。按数据面/控制面画图。

### 12. A server cannot receive one multicast group

限定 `(S,G,VLAN,host,time)` → application bind/join → IGMP report → snooping state/querier → switch ingress/egress replication → PIM `(S,G)`/IIF/OIF/RPF/TTL（如 routed）→ NIC/kernel/app counters。

### 13. Only one server has gaps; others are clean

共同 source/path 概率下降。比较该 server-facing egress capture、switch queue、optic、NIC ring/missed、softnet/socket buffer、IRQ/NUMA、feed-handler backlog；用同时正常 host 作 control。

### 14. Average bandwidth is low, why drops?

Microburst 或 fan-out egress oversubscription。以 µs window PPS/rate、queue watermark 和 discard time correlation 证明；还查 NIC/application 短时停止消费。

## D. Latency / packet analysis

### 15. How do you measure tick-to-trade?

先定义 tick observation 与 order departure；最好用同一时钟域的 NIC/FPGA RX/TX hardware timestamps，验证 PTP/accuracy，按 message correlation 计算 distribution，并同时保留 load、gaps、clock health。

### 16. p50 unchanged but p99.9 doubled

找 intermittent queue/scheduling：按点位分段，对齐 traffic burst、switch watermark、NIC/kernel drop、IRQ/CPU、GC、route/failover、OE throttle。不要用均值或单次 ping。

### 17. TAP, SPAN or hardware timestamp?

TAP 和 SPAN 是复制方式，timestamp 是时间测量方式。TAP fidelity 高但耗 optical budget；SPAN 灵活但 mirror 可 drop/retime；NIC/FPGA timestamp 靠近 wire。选择取决于问题与 measurement point。

### 18. Two captures disagree

先确认 filter、snaplen、capture drop、offload、timestamp clock/point、A/B path 和 metadata trailer；再比较 packet key/sequence。未同步时钟不能直接比较 one-way delta。

## E. HA / routing / carrier

### 19. What is a failure domain?

一个故障能共同影响的边界。除设备外包含 ASIC/linecard、rack/PDU、MMR/entrance、fiber SRLG、carrier、region，以及 software version、automation、AAA/DNS/PTP 等逻辑共同模式。

### 20. How fast will BFD fail over?

先给 detection 估算，再强调 total recovery = detect + protocol/FIB + neighbor + session/state/business。Timer 取决于协商和实现，需测试 false positive/scale，不能承诺配置值即业务 RTO。

### 21. Two carriers means path diversity?

不一定。核对 customer port、MMR、building entrance、conduit/manhole、underlying provider、POP、long-haul route/海缆和目标端；要求 SRLG/route evidence 并通过维护/故障演练验证。

### 22. Why did ECMP not use both links?

ECMP 通常 per-flow hash，单 5-tuple 固定 member；可能 hash polarization、seed/field、member/FIB 状态或 asymmetric return。看实际 flow key 和 hardware counters，不用 aggregate interface average。

### 23. BGP is Established but traffic fails

检查 NLRI/policy/best path、next-hop recursion、RIB/FIB/adjacency、ARP、ACL/uRPF、MTU、actual ECMP member 和 return path。Control session up 不证明 forwarding path。

## F. PTP / physical / host

### 24. Explain PTP in one minute

四 timestamp 算 offset/path delay；硬件打点；GM/BMCA；BC/TC；PHC 到 system/application；asymmetry 误差；监控 offset/GM/holdover；测试 GNSS/GM failover。

### 25. PTP offset jumps after a routing change

可能正反向 path/asymmetry、queue PDV 或 parent/GM 改变。查 GM identity、steps removed、mean path delay、BC/TC port、queue、profile/domain、servo，而不是直接重启 daemon。

### 26. Link is up but errors increase

记录两端 CRC/FEC/PCS/DOM delta；核对 optic/fiber/speed/FEC、清洁/换已知好 patch 或 optic，逐段隔离。FEC corrected 是 margin 预警，uncorrected 会丢数据。

### 27. How would you tune a Linux host?

先 profile；NIC queue/RSS → IRQ/application/memory 同 NUMA → coalescing/ring/socket → offload/busy poll → real load benchmark。一次一个变量，测 tail/loss/CPU 并验证 reboot persistence。

### 28. When would you use kernel bypass?

Profiling 证明 kernel/syscall/scheduler 是关键预算，团队能承担 dedicated CPU、兼容性、可观测和运维成本时。用实际 multicast/TCP、timestamp、burst、failure 基准选择 DPDK/AF_XDP/accelerated sockets。

## G. Migration / behavior

### 29. Your cutover looks bad; when do you roll back?

按预设 abort trigger，不凭情绪：关键 session timeout、sequence gap/stale、drop-copy mismatch、tail latency 退化、PTP 越界。说明 owner、观察窗口、rollback time 和 state reconciliation。

### 30. Tell me about a major incident

必须有 scope/timeline、当时证据、为何选择恢复动作、业务影响和量化结果。避免 hero story；强调如何新增监控、测试、failure isolation 或变更 guardrail 防复发。

## 反问面试官

- Which asset classes and venues are in scope, and where does the network team own the latency budget?
- How do you measure latency today—application, NIC or external FPGA timestamps?
- What are the most important failure domains or migration programs for this role in the next six months?
- How are network, Linux, trading development and exchange operations responsibilities divided during an incident?
- What distinguishes an excellent engineer on this team after the first year?

