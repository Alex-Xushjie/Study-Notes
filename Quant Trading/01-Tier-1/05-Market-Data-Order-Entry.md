# Market Data / Order Entry Architecture

## 1. 两条数据路径、三个真相来源

```text
PUBLIC PATH
MD A/B -> NIC -> feed handler -> book builder -> normalized API -> strategy
                    |                 |
                    + gap recovery    + stale/health state

PRIVATE PATH
strategy -> risk -> order gateway -> exchange session -> matching engine
   ^                    |
   +-- ACK/reject/fill -+----> drop copy -> reconciliation/risk
```

- Public market data 告诉所有人市场发生了什么。
- Private order session 告诉你自己的订单状态。
- Drop copy/clearing record 是独立核对来源，但不一定与主 session 同时到达。

**核心原则**：不要从 market data 推断自己订单的最终状态，也不要只靠主 OE session 做账。

## 2. Market data pipeline

### 2.1 Feed 类型

- **MBO (Market by Order)**：每个可见订单事件；能构建最细 book，量大且状态复杂。
- **MBP (Market by Price)**：按价格档聚合；处理简单但看不到队列内个体订单。
- **Top of Book**：最佳 bid/ask 和 last trade；带宽低、信息少。
- **Reference data**：symbol/instrument ID、tick size、trading status、channel mapping；不是旁枝，是正确解析的前置条件。

### 2.2 Incremental book state machine

1. 载入当日 reference data/channel mapping。
2. 建立 A/B 接收并按 sequence 做 line arbitration/de-duplication。
3. 从已知初始状态或 snapshot 开始。
4. 按序应用 add/modify/delete/execute/trade/status。
5. 发现 gap：标记受影响 channel/book stale，缓存后续增量，发 retransmission 或重取 snapshot。
6. 恢复连续状态后才对策略宣告 healthy。

不能说“UDP 丢了就从 B 线补”作为通用答案。A/B 到达顺序、sequence space、恢复服务和 snapshot 规则由 venue 定义。

### 2.3 Gap handling

```text
expected=105, received=108
  -> record gap [105..107]
  -> try missing messages from redundant line/cache
  -> if unavailable, request retransmission
  -> if range too large/timeout, obtain snapshot
  -> replay buffered incrementals after snapshot sequence
  -> validate book invariants, mark healthy
```

监控：gap count/range/recovery time、out-of-order、duplicate、channel lag、socket drop、NIC drop、book stale duration、A/B skew。

## 3. Order entry pipeline

### 3.1 FIX 与 native binary

| FIX | Native binary |
|---|---|
| 标准语义、可读、生态成熟 | 固定/紧凑编码、解析快、venue-specific |
| 常经 gateway 转换 | 更接近交易所 native path |
| 易集成但字段/版本仍各 venue 不同 | 开发和认证成本更高 |

不要说 TCP“绝不丢包”。TCP 提供有序可靠字节流，但应用仍会遇到连接断开、未确认状态、sequence reset、重复提交和 session recovery。

### 3.2 订单状态必须可相关

为每个请求保留稳定 correlation：client order ID/token、venue order ID、session、sequence、send timestamp。处理：

- New → ACK/reject；Cancel/replace → ACK/reject；partial/full fill。
- TCP 断开时存在 **unknown order state**：请求可能已到 exchange，但 ACK 未回来。
- 恢复应依 venue 的 open-order query/drop copy/reconciliation/cancel-on-disconnect 语义，不能盲目重发。

### 3.3 Inline risk

典型检查：price collar/fat finger、max quantity/notional、position/credit limit、message rate、duplicate ID、market state、restricted instrument、self-trade prevention。还要有 exchange/firm kill switch、mass cancel 和独立 drop copy。

取舍：风险检查越多越可能增加延迟，但“绕过风控”不是网络优化。常见方法是将必要规则本地化、预计算、hardware accelerate，并把非关键分析放到异步路径。

## 4. Network 设计要点

- MD 通常 UDP multicast；OE 通常 TCP unicast/session oriented，监控和故障语义完全不同。
- MD burst 容量按 channel 峰值和复制扇出；OE 按 session/throttle 和 ACK burst。
- 对 market data，浅 buffer 可降低正常延迟但 burst 时更易丢；deep buffer 能吸收突发但可能增加排队和 conceal congestion。
- QoS 不是制造带宽。优先做物理/队列隔离、容量和 fan-out 设计。
- Capture 点至少覆盖 exchange-facing 与 server-facing；时间戳源必须一致或可校准。

## 5. 端到端 latency 分解

常见指标必须先定义：

- **wire-to-user**：NIC wire arrival → application sees message。
- **tick-to-trade**：market event observation → order leaves client NIC。
- **order RTT**：client TX → exchange ACK RX。
- **market-data loop**：自己的 order TX → observable market event RX（不等同 ACK）。

报告 percentile 和条件：p50/p99/p99.9/max、frame size、load、trading phase、hardware/software timestamp、measurement points。

## 6. 故障场景

### MD sequence gaps 增多但 switch 无 discard

检查 exchange source/A-B 是否都缺；NIC `rx_missed_errors`/ring、socket `RcvbufErrors`、CPU调度、feed handler backlog、capture point 是否在 NIC 前。交换机“无丢包”只能排除其已统计到的一部分路径。

### OE RTT p99 突升但 p50 正常

按 timestamp 分段：client queue/NIC → network → exchange → return；关联 message burst、TCP retransmission、switch queue、microburst、CPU steal/IRQ、session throttle/venue load。不要先改 routing。

### Session 断开后订单状态不明

停止产生可能重复的订单，按 venue 语义重连/恢复 sequence，使用 drop copy/open-order 状态核对，执行 cancel-on-disconnect 或 mass cancel 策略，由风险/交易 owner 决定恢复交易。

## 7. 2 分钟回答模板

> I treat market data as a replicated state machine and order entry as a private transactional session. The feed handler receives redundant multicast lines, arbitrates by sequence, builds the book only from ordered events, and exposes an explicit stale state during gap recovery. The order path applies mandatory pre-trade risk, maintains client-to-venue correlation, and reconciles ACKs and fills with an independent drop copy. A TCP reconnect is not sufficient because orders may be in an unknown state. Network capacity is designed for bursts and packets per second, with separate observability for switch, NIC, kernel and application drops. Latency metrics have named boundaries and synchronized hardware timestamps so we can distinguish feed, host, strategy, gateway, network and exchange delay.

## 8. 官方实例

- [Nasdaq OUCH](https://classic.nasdaqtrader.com/Trader.aspx?id=ouch) 是高效 native order entry 的实例。
- [CME Globex reference guide](https://www.cmegroup.com/content/dam/cmegroup/globex/files/GlobexRefGd.pdf) 将 iLink、MDP 3.0 等放在一个体系中。
- [Cboe technical library](https://www.cboe.com/markets/us/options/support/technical/) 展示 BOE/FIX、PITCH/TOP、risk spec 等分层文档。
- [HKEX OMD FAQ](https://www.hkex.com.hk/Global/Exchange/FAQ/Market-Data/Getting-Market-Data/Orion-Market-Data-Platform-Securities-Market-OMDC?sc_lang=en) 是 line arbitration、retransmission、refresh 分工的实际例子。

