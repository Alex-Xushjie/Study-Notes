# Network Migration / Cutover

## 1. 成功迁移的定义

不是“新端口 up”，而是：业务状态正确、latency/loss 不退化、无 unknown orders、监控和回退可用，并在约定窗口内得到业务 owner 的明确 sign-off。

## 2. 四阶段方法

### Discover

- 当前 physical/logical/application flow，含隐藏依赖：source IP allowlist、multicast join、ACL、DNS/NTP/PTP、license、hard-coded interface、capture/monitoring。
- Baseline：p50/p99/p99.9、sequence gaps、interface/NIC/kernel counters、BGP/IGMP/PIM state、CPU。
- Owner/RACI：exchange、carrier、colo remote hands、network、server、trading、risk、compliance。

### Build and prove in parallel

- 新路径尽量 dark/parallel build；做 config peer review、lab/UAT、exchange certification、synthetic traffic。
- 比较 old/new A/B feed 内容、sequence、latency；OE 用 test session/certification，不在生产盲测。
- 预置 dashboard、capture、OOB 和 rollback config。

### Cut over

- Freeze unrelated changes；确认 bridge call、ticket、contact、时间同步、备份和权限。
- 每一步只有一个动作、一个执行人、expected output、验证人、预计耗时。
- Canary：一个 non-critical channel/session/host，观察后逐批扩展，避免 big bang。
- 业务验证包括行情连续性、book health、order ACK/fill/drop copy，而非 ping。

### Stabilize and decommission

- 经过完整高峰/交易阶段 soak；对比 baseline 和 tail。
- 更新 as-built、CMDB、监控、on-call；关闭旧路径前验证没有流量/依赖。
- 旧线路/端口/合同 decommission 另开受控变更，避免当天失去回滚。

## 3. MOP 最小模板

| 字段 | 内容 |
|---|---|
| Scope | 哪些 venue/feed/session/device，不包含什么 |
| Preconditions | UAT、备份、OOB、人员、change freeze、health |
| Step | 精确命令/操作、owner、expected、evidence |
| Validation | network + application + business 指标 |
| Abort trigger | 明确阈值和观察窗口 |
| Rollback | 恢复顺序、state reconciliation、耗时 |
| Communications | start/checkpoint/abort/complete 通知 |

## 4. Rollback 不是一句话

必须回答：

- 谁宣布 abort，按什么阈值？例如 gap 连续超过基线、p99.9 退化、drop copy 不一致、关键 session 未在 N 分钟恢复。
- 回退是否仍物理存在、配置是否未漂移、旧 session/sequence 能否恢复？
- 新旧两边同时活跃是否会 duplicate multicast/order？
- 迁移后产生的订单/状态如何 reconciliation？
- 回退需要多长时间，是否仍在安全交易窗口？

数据库/订单等有状态迁移常常不能简单“切回电缆”。网络回退必须与应用和风险回退共同设计。

## 5. 常用迁移技术和风险

| 方法 | 用途 | 风险 |
|---|---|---|
| Parallel A/B / line arbitration | 比较 market feed | duplicate、sequence 映射、capture 容量 |
| BGP local-pref/community | 分批引流 | route leak、非对称、收敛影响 session |
| DNS/VIP | 服务切换 | cache/TTL、existing connection 不迁移 |
| L2 stretch | 临时保留地址 | loop、MAC move、failure domain 扩大 |
| Host route/static change | 小范围 canary | 配置碎片化、回退遗漏 |
| Optical/L1 patch | 最低开销路径切换 | 人工错误、短暂 loss、无状态感知 |

## 6. Cutover 当天检查表

```text
[ ] 所有人/厂商在线，OOB/console 可用
[ ] old/new configs 与端口状态已采集
[ ] exchange/carrier 无 active incident/maintenance
[ ] PTP offset、feed sequence、order/drop-copy state healthy
[ ] rollback target 和物理路径仍保留
[ ] canary -> checkpoint -> batch progression
[ ] 每步记录时间、输出和批准
[ ] final business sign-off；进入 soak 而非立即拆旧
```

## 7. 失败场景回答

“切换后 ping 正常但 order ACK 没有”：立即停止扩大范围；检查 TCP/session/CompID/source allowlist/sequence，而不是以 IP reachability 判成功。若超过 abort threshold，按应用 session 与订单状态的安全顺序回退并用 drop copy 对账。

“新 feed 无 gap 但策略结果不同”：比较 reference data、channel mapping、message decode、book initial state 和 timestamp/order，不只对比 packet count。

## 8. 2 分钟回答模板

> I prefer a parallel, reversible migration with application-level validation. Discovery maps physical paths, multicast and routing state, source allowlists, session semantics, timing, monitoring and ownership, then records a performance baseline. The new environment is built dark and proven in UAT or exchange certification. During cutover I use a canary and checkpoints; every step has an expected result, evidence, owner and time limit. Abort criteria are objective—such as sequence gaps, tail-latency regression or order/drop-copy mismatch. Rollback includes session and order-state reconciliation, not just restoring routes. I retain the old path through a realistic soak period and decommission it in a separate controlled change.

