# Global Trading Network Architecture

## 1. 先从业务而不是设备型号开始

典型全球交易网络不是一个扁平网络，而是多个用途不同的 plane：

| Plane | 流量 | 核心目标 |
|---|---|---|
| Market data | exchange raw feed、normalized feed | loss visibility、低 jitter、可恢复 |
| Execution | order、cancel、ACK、fill | 确定性、会话完整性、风控 |
| Strategy | feed handler ↔ strategy ↔ gateway | 极低延迟、NUMA locality、容量隔离 |
| Control/risk | reference data、limits、kill switch | 正确性、强审计、不能被交易洪峰饿死 |
| Time | PTP/NTP、GNSS | 可证明的共同时间基准 |
| Capture/telemetry | TAP copies、counters、logs | 不能干扰 production path |
| Management | OOB、AAA、automation | 独立故障域和可恢复访问 |

## 2. 参考架构

```text
                    Region A / Metro A
 Exchange 1 ---- Colo A1 ----+                 +---- Core DC A
 Exchange 2 ---- Colo A2 ----+---- Metro DCI ---+    research/risk
          \       |   |      +                 +---- office/backtest
           \      |   +-- diverse carrier/path
            \  strategy + feed + OE
             \
              ===== protected global WAN =====
                            |
                    Region B / Metro B
 Exchange 3 ---- Colo B1 ---+---- Core DC B / DR
```

一个成熟设计通常把：

- **hot path 留在 colo**：raw feed → strategy → order gateway → exchange；避免跨 WAN 决策。
- **state/risk 明确落点**：哪些风险检查必须 inline，哪些可异步；谁拥有 authoritative order state。
- **global WAN 用于必要状态**：positions、limits、signals、drop copy、operations，而不是假设它永不抖动。
- **OOB 独立**：独立 console server、管理网络、认证路径和远程访问，不依赖故障中的 production fabric。

## 3. 设计步骤

### 3.1 收集需求

至少问清：venue/asset class、交易时段、native feed/protocol、峰值与 burst、线路交付方式、策略对单向延迟和 jitter 的预算、丢包恢复模式、session 数、法规时间精度、RTO/RPO、容量增长、预算和支持覆盖。

### 3.2 做 latency budget

```text
T_tick_to_trade = T_exchange_egress
                + T_link + T_switch
                + T_NIC_RX + T_feed_handler
                + T_strategy
                + T_gateway + T_NIC_TX
                + T_link + T_exchange_ingress
```

网络工程师不能控制每一项，但必须定义 measurement boundary。光在真空约 3.3 µs/km，在光纤约 5 µs/km（单程粗略值）；同 metro 绕路几公里就可能比换一台交换机影响更大。

### 3.3 做 capacity 和 burst budget

- 同时计算 Gbps、pps、messages/s；小包场景往往先碰 PPS。
- 使用交易日峰值、开收盘/宏观事件 burst 和增长系数，不用日均值。
- 检查 oversubscription、microburst、egress queue、NIC ring 和应用消费速率。
- Market data A/B 都要按完整 feed 容量设计，不能假设一半流量。

### 3.4 明确边界

- L2 故障域尽量小；跨机柜/colo 优先 L3，减少 STP 和 unknown multicast 风险。
- production、management、capture、PTP 逻辑/物理隔离程度由故障风险决定。
- 定义 exchange demarc、carrier demarc、cross-connect、switch port、server port 的 owner。

## 4. 常见取舍

| 选择 | 优点 | 风险/代价 |
|---|---|---|
| 单层超低延迟交换 | hop 少、jitter 小 | 端口/规模有限，故障域可能变大 |
| Leaf-spine L3 | 扩展和 ECMP 好 | hop、hash、收敛复杂度增加 |
| L1 switch/patch | 极低且确定 | 无 buffering/routing，排障能力取决于旁路监控 |
| Active/active | 利用两条路径、快速 | 重复包、乱序、会话/状态复杂 |
| Active/standby | 行为清楚 | standby 漂移、切换慢、资源闲置 |
| Inline security | 策略集中 | 延迟、jitter、新单点；交易热路径常需专门设计 |
| Shared fabric | 成本低 | noisy neighbor、变更 blast radius 大 |

## 5. 关键原则

- **Determinism beats a pretty average**：p50 很低但 p99.99 抖动会伤害策略。
- **Fast failure is not always safe failure**：过敏的 BFD 可能造成 flap；错误切换比短暂中断更糟。
- **Market data 与 order state 的一致性优先**：feed stale 时继续下单可能比停机危险。
- **每条冗余路径都要可独立运行并被真实演练**。
- **所有图都画 demarc 和 owner**，否则故障时没人知道该找谁。

## 6. 2 分钟回答模板

> I start by separating traffic classes and defining latency, loss, capacity and recovery requirements per venue. The latency-sensitive path remains inside each exchange colo: redundant raw feeds enter feed handlers, strategies consume a validated book, and orders go through inline risk and native gateways. I keep management, timing and capture independent so an observability or control-plane failure cannot affect trading. Between colos I prefer small L2 domains and routed, carrier-diverse DCI, with explicit route and facility diversity. Redundancy is designed by failure domain—not device count—and tested from optics and PDUs through carriers and application sessions. Finally, I validate p50 through p99.99 latency and packet loss with synchronized hardware timestamps, and document failover and rollback behavior.

## 7. 面试追问

- 为什么不把所有 colo 拉成一个大二层？
- A/B market data 是 active/standby 还是 line arbitration？
- WAN 断 30 秒，本地策略可以继续交易吗？谁决定？
- 两条电路不同 carrier 但走同一 conduit，算冗余吗？
- 哪些设备应该 deep buffer，哪些应该 cut-through？

