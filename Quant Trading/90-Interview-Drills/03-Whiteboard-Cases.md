# 白板场景题

## Case 1：双交易所、双 colo 架构

### 题目

在同一个 metro 接入 Exchange A/B；策略需要两边行情并在两边下单，另一个地区是 DR。设计网络。

### 10 分钟白板顺序

1. 写需求假设：feed/session/peak、latency、RTO/RPO、data residency。
2. 画每个 exchange 的 MD A/B、OE A/B、drop copy 和 demarc。
3. 画 colo 内 feed/strategy/risk/gateway，以及 PTP/capture/OOB。
4. 两 colo 之间 routed diverse DCI；标出 physical route/SRLG。
5. DR 只同步必要 state，标注 consistency/RPO 和 resume authority。
6. 列故障：一条 feed、一个 switch、一个 carrier、整个 colo、PTP fault。
7. 写 measurement：sequence health、OE RTT、tick-to-trade、PTP、queue/loss。

### 面试官会挑的洞

- A/B 是否同一 line card/PDU/MMR？
- OE active-active 如何防 duplicate/超限？
- Metro partition 后两个站点是否 split brain？
- DR 数据是否足够新，谁允许重新交易？

## Case 2：每天开盘时 market data gaps

### 已知

- 09:30 附近持续 2 秒；平时无问题。
- Switch 端口日均利用率 20%。
- 两台 server 只有一台报告 gaps。

### 答题路径

1. 先以风险策略保护 stale book，不直接改网络。
2. 以 sequence 定时间窗；另一台 server 是 control。
3. 查 bad server egress queue、optic/NIC ring/softnet/socket/app backlog。
4. 用 µs/ms 级 rate 和 watermark 找 microburst，不能用 5 分钟平均。
5. 对比 server-facing TAP 与 NIC hardware timestamp/counter 定位边界。
6. 若 NIC 前完整、应用缺：检查 RSS/IRQ/NUMA/coalescing/ring/socket/feed handler。
7. 修复后在 replay/开盘等价 burst 下验证 p99.9、gap 和 CPU。

### 不合格答案

“加带宽”“换交换机”“调大 buffer”，但没有证据、边界或副作用。

## Case 3：Carrier failover 后 RTT 增加 3ms

### 答题路径

- 先确认这是预期 backup physical route 还是异常绕路；获取 path/SRLG 和 baseline。
- 看 BFD/BGP event、best path/FIB、实际 flow member、forward/return asymmetry。
- 分清传播变化、queue/policing、MTU/retransmission、application reconnect。
- 判断新延迟是否仍在 degraded SLO；必要时降低/停特定策略而非频繁 flap 回去。
- 与 carrier 升级证据：circuit ID、UTC time、direction、percentiles、packet size/load、path trace。

## Case 4：PTP GM 切换时 latency 图出现负值

### 答题路径

- 负 one-way latency 首先指向 clock discontinuity/offset，而非“网络穿越时间”。
- 查 GM identity/change、clock class、offset/mean path delay、servo step/slew、holdover、leap/UTC-TAI。
- 对比同 clock domain RTT 或单设备时间戳；暂停依赖不可信时钟的业务判断。
- 验证备用 GM priority、antenna/reference independence、BMCA、最大允许 step；加入 GM change annotation/alarm。

## Case 5：迁移后 OE TCP 建连但 Logon 拒绝

### 答题路径

- TCP 成功只到 L4；检查新的 source NAT/IP 是否在 exchange allowlist。
- 核对 CompID/session ID、credentials、sequence/reset、trading environment、TLS/cert（若有）、时间窗。
- 查 exchange reject reason 和 portal/session owner，不盲目 retry 触发 lock/throttle。
- 未达到业务 checkpoint，不迁移更多 session；超过 abort window 执行已验证回退。
- 对旧/新 session 的 outstanding orders 和 drop copy 做 reconciliation。

## Case 6：一次错误自动化同时改坏 A/B

### 设计改进

- 物理 A/B 不解决逻辑 correlated failure。
- Typed source of truth、schema/invariant（禁止同时触碰同一 service 的所有 failure domains）。
- Dry-run diff、two-person approval、canary、batch health gate、automatic stop。
- A/B 使用 staggered software/config cohort；OOB 与 last-known-good rollback 独立。
- Post-check 使用 feed/order/PTP 业务指标；审计记录能重建完整 timeline。

