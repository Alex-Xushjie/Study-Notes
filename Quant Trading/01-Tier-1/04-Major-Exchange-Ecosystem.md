# Major Exchange Ecosystem

> 目的不是背交易所清单，而是看到新 venue 时知道该收集哪些资料。产品、协议和机房会变，项目启动时必须以交易所最新 technical notice 为准。

## 1. 生态角色

```text
Issuer / instrument
      |
Exchange / MTF / ATS / ECN ---- market-data vendor/SIP
      |             |
Matching engine     +---- broker / market maker / prop firm
      |                               |
Clearing house / CCP -----------------+
      |
CSD / custodian / settlement

Connectivity provider / extranet / colo / cross-connect / time source
贯穿整个技术链条
```

- **Venue** 提供 matching、native order protocol、direct feed、认证和风险控制。
- **Consolidated feed** 提供跨 venue 汇总视角，但通常与 direct feed 的内容/路径/时延不同。
- **Broker/clearing member** 解决 market access、credit/risk 和清算关系；网络通了不等于获准交易。
- **Extranet/managed service** 降低接入门槛，但增加共享组件、可见性边界和 latency variation。

## 2. 面试应熟悉的代表性 venue

| 地区/资产 | 代表生态 | 常见接口心智锚点 |
|---|---|---|
| 美国股票 | Nasdaq、NYSE、Cboe、IEX 等；多 venue + SIP/NBBO | Nasdaq TotalView-ITCH / OUCH；Cboe PITCH / BOE/FIX；NYSE Pillar 系列文档 |
| 美国期权 | 多家 options exchange + OPRA consolidated feed | 高 message rate、复杂 symbology、quote/auction/risk controls |
| 美国期货 | CME Globex（CME/CBOT/NYMEX/COMEX 等市场） | MDP 3.0 market data、iLink order entry、Drop Copy |
| 英国/欧洲现金 | LSE Millennium Exchange；Xetra T7 | native binary/FIX 语义、direct market data |
| 欧洲衍生品 | Eurex T7 | ETI order entry，EOBI/EMDI market data |
| 香港 | HKEX securities/derivatives、Stock Connect | OMD-C/OMD-D data，central gateway/connectivity guides |
| 日本 | JPX/TSE arrowhead、OSE derivatives | FLEX Standard/MBO；participant/order gateway |
| 新加坡 | SGX securities/derivatives | 以最新 SGX API/connectivity circular 为准 |

截至本笔记更新，JPX 官方说明 arrowhead 4.0 于 2024-11-05 上线，并提供 FLEX Standard 与 FLEX Market by Order；这正说明不能用几年前的协议表硬背。

## 3. 每接一个 venue 的 discovery checklist

1. **商业与监管**：membership/sponsor、market data license、clearing、测试费用、port/session 订单。
2. **设施**：production/DR 地址、colo provider、MMR、cross-connect、extranet、测试环境。
3. **Market data**：MBO/MBP/top、A/B line、multicast groups/source IP、sequence、snapshot/retransmission、reference data。
4. **Order entry**：native binary/FIX、TCP/session、logon/heartbeat、sequence、throttle、cancel-on-disconnect、mass cancel、drop copy。
5. **Market model**：tick size、price/time 或 pro-rata、auction、halt、trading phases、order types、self-trade prevention。
6. **Operations**：release calendar、certification、market rehearsal、DR test、notice subscription、support/escalation。

## 4. Direct feed、consolidated feed 和 vendor feed

| 类型 | 优点 | 限制 |
|---|---|---|
| Direct/native | 最完整/直接，适合建本地 book | 每 venue 单独开发、授权和恢复逻辑 |
| Consolidated | 跨 venue 统一视图和监管基准 | 内容被标准化，路径/排队和更新顺序不同 |
| Vendor normalized | 接入快，跨市场一致 | vendor latency/故障域、字段语义和透明度 |

不要笼统说 direct 永远“更正确”。两个 feed 的观察点、内容、时间戳和市场含义不同；应说明策略需要什么，以及如何 reconciliation。

## 5. Venue 技术规格里要真正读懂的段落

- Session state diagram 和 sequence reset policy。
- Message framing、endianness、fixed/variable length、price scaling。
- Feed channel mapping、A/B 是否完全相同、gap recovery 限制。
- Order ACK/reject/replace/cancel/fill 的 correlation key。
- Throttle 计算窗口及超限行为。
- Cancel-on-disconnect、mass cancel、kill switch 的责任边界。
- Trading phase/auction/halt 对订单和行情的影响。
- DR failover 后地址、sequence、session/order state 如何变化。

## 6. 官方资料入口（面试前再次检查）

- [Nasdaq OUCH](https://classic.nasdaqtrader.com/Trader.aspx?id=ouch) 与 [UDP/IP market-data feeds](https://www.nasdaqtrader.com/Trader.aspx?id=FeedMIPS)
- [NYSE connectivity documents](https://www.nyse.com/connectivity/documents)
- [CME Globex resources](https://www.cmegroup.com/solutions/market-access/globex/globex-resources.html) 与 [Globex reference guide](https://www.cmegroup.com/content/dam/cmegroup/globex/files/GlobexRefGd.pdf)
- [Cboe US Options technical specifications](https://www.cboe.com/markets/us/options/support/technical/)
- [LSE equities technical library](https://www.londonstockexchange.com/resources/equities-trading-resources?tab=technical-library)
- [Eurex T7 connectivity](https://www.eurex.com/ex-en/support/technology/connectivity/Connectivity-Support-2393262)
- [HKEX OMD-C](https://www.hkex.com.hk/Services/Market-Data-Services/Infrastructure/HKEX-Orion-Market-Data-Platform-Securities-Market-OMD-C?sc_lang=en)
- [JPX arrowhead](https://www.jpx.co.jp/english/systems/equities-trading/01.html)

## 7. 2 分钟回答模板

> I organize exchange ecosystems by asset class and region, but I never assume two venues behave the same. For each venue I build a matrix covering commercial entitlement, physical connectivity, direct and recovery feeds, native order sessions, drop copy, market phases, risk controls and DR behavior. In US equities, for example, I expect a fragmented market with direct feeds and a consolidated view; CME Globex anchors US futures; in Europe I would expect platforms such as Millennium and T7; in Asia, HKEX OMD and JPX FLEX are examples of venue-specific feeds. The important engineering skill is translating the current exchange specification into dependencies, capacity, failure behavior, certification and an operational runbook.
