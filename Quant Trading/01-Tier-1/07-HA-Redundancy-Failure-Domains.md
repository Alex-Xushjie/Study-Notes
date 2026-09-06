# HA, Redundancy and Failure Domains

## 1. HA 的对象不是设备，而是服务

先定义服务 SLO：行情可用性、book stale 最大时间、下单 RTO、订单状态 RPO、允许的 duplicate/loss、manual intervention。两台交换机并不自动得到 HA；应用、session、risk state、供电和 carrier 都可能仍是单点。

## 2. Failure-domain map

```text
component -> port/optic -> chassis -> rack/PDU -> row
-> MMR/building entrance -> facility/campus -> metro
-> carrier POP/SRLG -> region -> vendor/control plane -> human/process
```

也要考虑逻辑共同故障：同一软件版本 bug、同一错误 automation、同一 AAA/DNS/PKI、同一个 PTP GM 误报时间、相同配置模板。

## 3. 冗余模式

| 模式 | 合适场景 | 风险 |
|---|---|---|
| Active/standby | stateful service、行为简单 | state sync、standby 未经压力验证、切换慢 |
| Active/active + arbitration | A/B market feed | duplicate/reorder、两路相关故障 |
| ECMP | 无状态 unicast 多路径 | flow polarization、成员变化、stateful session |
| Dual session | OE/不同 gateway | 订单归属、throttle、duplicate、风险汇总 |
| Cold/Warm DR | 地区灾难恢复 | stale config/data、不同 latency/容量、人工步骤 |

## 4. 可用性时间线

```text
T_total_recovery = T_detect + T_control_converge + T_session_recover
                 + T_state_reconcile + T_business_resume
```

`link down` 可能立即被检测；silent blackhole 依赖 BFD/keepalive/application heartbeat。BGP/OSPF 收敛后 TCP/FIX 仍可能重连，feed handler 仍需恢复 gap/book，风险团队仍需确认 unknown orders。因此要测业务 RTO，而不是仅测 ping 恢复。

## 5. 设计规则

- 每条备用路径必须有完整 capacity；故障时不要让 2× 流量压垮剩余链路。
- Failure detection 设置要有误报预算，避免 intermittent loss 触发震荡。
- State replication 的 consistency/latency 明确：同步会增加 hot-path 延迟，异步会产生 RPO。
- **Fail closed vs fail open** 由业务/风险决定：行情 stale、风险服务不可用、PTP 超阈值时是否停止交易。
- Graceful degradation：丢一个 feed、一个 venue、一个 region 时缩小功能，而非全网崩溃。
- 维护必须能一次只动一个故障域，并验证备用路径没有 hidden fault。

## 6. Failure injection 清单

| 注入 | 观察 |
|---|---|
| 拔 optic / shut port | physical alarm、route、packet loss、session |
| Drop traffic but keep link up | BFD/heartbeat、blackhole detection |
| Reload one switch | peer/fabric、multicast rejoin、queue burst |
| Stop feed handler | VIP/service discovery、book state、duplicate consumer |
| Kill OE session | cancel-on-disconnect、unknown orders、drop copy |
| Remove GM/GNSS | BMCA、holdover、offset alarm、timestamp monotonicity |
| Pull one PDU | dual PSU/actual circuit independence |
| Withdraw carrier route | BGP policy、path latency、capacity、application recovery |

每次记录：expected、actual、detection、impact、recovery、manual step、evidence、follow-up。

## 7. Split brain 与相关故障

两套活跃 gateway/策略如果失去互联但都认为对方死了，可能重复下单或突破风险。常见控制：single writer/lease/quorum、venue-side risk/mass cancel、partition fencing、独立 drop copy。网络团队要说明 partition，而不只说“链路 down”。

相关故障例子：

- 两条 feed 经不同端口但同一 ASIC/line card。
- 两家 carrier 共用 duct/underlying wavelength provider。
- A/B PSU 接入两个 PDU，但两个 PDU 上游同一 breaker。
- 双 GM 共用同一 GNSS antenna 或错误 source。
- 双设备同时接收错误 automation push。

## 8. 2 分钟回答模板

> I design HA around service recovery objectives and failure domains rather than counting devices. I map physical and logical common modes from ports, power and MMRs through carriers, software versions, automation and timing. The recovery budget includes detection, network convergence, session recovery, state reconciliation and the business decision to resume. Active-active is useful for redundant market-data lines with sequence arbitration, while stateful order paths require explicit ownership and unknown-order handling. I test hard failures and silent blackholes at realistic load, verify remaining-path capacity, and measure application outcomes. I also define fail-open or fail-closed behavior for stale data, unavailable risk and timing faults.

