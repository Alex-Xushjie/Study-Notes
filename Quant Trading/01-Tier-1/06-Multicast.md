# Multicast for Trading Networks

## 1. 数据面与控制面

```text
Source S -> L3 multicast routing/PIM -> receiver VLAN gateway
                                      |
                         IGMP snooping switch
                         /        |         \
                 joined host   joined host  no copy

Host -- IGMP Report/Leave --> local router/querier
Router -- PIM Join/Prune --> upstream multicast topology
```

- **IGMP**：host 与本地 L3 multicast router 之间表达 group membership。
- **IGMP snooping**：L2 switch 监听 IGMP，建立 group→port，避免把组播当未知流量到处 flood。
- **Querier**：周期 query 维持 membership；VLAN 内无 multicast router 时常需 snooping querier。
- **PIM**：路由器之间建立 multicast tree。
- **RPF check**：组播包必须从到 source 的正确反向路径接口到达，防止环路。

## 2. ASM 与 SSM

- **ASM**：receiver join `(*,G)`，PIM-SM 常依赖 RP 发现 source，再可转 SPT；状态和运维更复杂。
- **SSM**：receiver 明确 join `(S,G)`，通常用 IGMPv3；不需要 RP，适合 source 已知的 market feed。

实际 exchange feed 可能只在直接 L2 handoff 内交付；不要强行套 PIM。先确认 demarc 和是否需要 routed multicast。

## 3. A/B feed 的正确理解

许多 venue 从两条独立路径发送内容相同或可对应的 feed：

- 两条都接收，应用按 sequence 采用先到者并去重，称 line arbitration。
- A/B 的“独立”必须覆盖 exchange handoff、cross-connect、switch/NIC/host failure domains。
- A 比 B 快不是故障；关注 skew distribution、是否同 sequence、是否有一边持续 gap。
- 网络不能替应用完成业务级 gap recovery；应用必须懂 sequence/snapshot/retransmission。

## 4. 推荐设计

### L2-only handoff

- 独立 VLAN、明确 querier；限制 VLAN 范围和 receiver port。
- 配置静态 multicast group/port 还是动态 IGMP，由 venue和平台行为决定。
- 防止 unknown multicast flooding、TCAM exhaustion、querier election 变化。

### Routed multicast

- 优先小 failure domain；SSM `(S,G)` + IGMPv3/PIM-SSM 通常比 ASM 简洁。
- 明确 RP（如 ASM）、RPF route、ECMP 行为、source filtering、TTL。
- Anycast RP/MSDP 等只在需求支持时使用，不因“高级”而引入。

### Fan-out

交换机 replication 简单，但大量 receiver/downstream capture 可造成 egress oversubscription。也可用 feed handler/software/FPGA fan-out；代价是新故障域和额外延迟。设计时计算每端口实际复制带宽。

## 5. 丢包位置与证据

```text
exchange -> XC -> switch ingress -> fabric -> switch egress
-> NIC MAC/ring -> driver/NAPI -> socket buffer -> application queue
```

| 层 | 证据 |
|---|---|
| 光/PCS | LOS、CRC/FCS、symbol error、FEC corrected/uncorrected、DOM |
| Switch | ingress/egress discard、queue/watermark、multicast state、ACL |
| NIC | missed/no-buffer/discard、ring stats、PCIe/driver counters |
| Kernel | UDP receive buffer errors、softnet drops、socket buffer |
| App | sequence gap、receive queue depth、processing time、GC/pause |
| Source/path | A/B 同 sequence 同时缺失、upstream capture |

## 6. 排障流程：服务器收不到某个组

1. 限定 `(S,G,VLAN,receiver,time window)`，不要只说“组播坏了”。
2. 应用是否成功 bind/join，interface 和 source filter 是否正确？
3. Host 发出 IGMPv2/v3 report 吗？交换机 group→port 状态存在吗？
4. Querier 是否存在、是否变化；membership timer 是否过期？
5. Switch ingress 看得到 `(S,G)` 吗，正确 receiver egress 有复制吗？
6. Routed 时查 PIM neighbor、`(S,G)`、IIF/OIF、RPF route、TTL/ACL。
7. Host NIC 前后的 capture/counter 是否分叉？应用 sequence 是否连续？

常见陷阱：capture 工具自己触发 promiscuous/all-multicast 使问题消失；SPAN oversubscription 让“证据”本身丢包；IGMP snooping 开启但无 querier 导致老化后间歇中断。

## 7. Microburst

平均 2 Gbps 的 feed 仍可在微秒窗口打满 10G egress。`queue_depth ≈ (ingress_rate - egress_rate) × burst_duration`，再换算为 bytes/packets。浅 buffer ULL switch 可能很快 discard；deep buffer 可能不丢但增加排队尾延迟。选择取决于策略是否更怕 loss 还是 stale latency，并需用 watermark 与硬件时间戳证明。

## 8. 高频追问短答

- **UDP 为什么适合行情？** 无连接、支持一对多、发送端不因慢 receiver 阻塞；可靠/有序状态由 feed protocol 的 sequence/recovery 实现。
- **IGMP snooping 是 routing 吗？** 不是，是 L2 根据 IGMP 控制报文约束复制端口。
- **RPF 看什么？** 到 source 的单播/指定 multicast 路由决定期望入接口；包从错误接口来会被丢。
- **TTL=1？** 不能跨 L3 hop；先看 venue 交付设计，不要随意改。
- **能用 ECMP 搬一个组流量吗？** 取决于平台 multicast ECMP/hash；一个 `(S,G)` 通常固定路径，且切换可能带来短暂 loss/duplicate/reorder。

## 9. 2 分钟回答模板

> In a trading network I treat multicast as an end-to-end state and loss problem. IGMP expresses receiver membership, snooping limits Layer-2 replication, PIM builds routed trees, and RPF validates the incoming path toward the source. Where source addresses are known, SSM is operationally simpler than ASM. Redundant exchange lines are normally consumed concurrently and arbitrated by sequence; they are not merely an active/standby link. For troubleshooting I identify the exact source, group, VLAN and time, then follow the packet from switch ingress and multicast state through egress queues, NIC rings, kernel socket buffers and application sequence numbers. Average bandwidth is insufficient—I size for PPS and microbursts, and validate gaps with independent capture points.

