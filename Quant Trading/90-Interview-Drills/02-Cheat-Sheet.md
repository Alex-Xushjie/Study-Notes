# 面试前 15 分钟速查表

## 一张图

```text
MD A/B -> ULL/L1 -> NIC RX -> feed handler/book -> strategy -> risk/gateway
  ^                                                            |
  |                                                            v
exchange <- public update / ACK/fill <- matching engine <- OE TCP
                                             |
                                          drop copy

GM/GNSS -> PTP BC/TC -> NIC PHC       TAP/FPGA -> recorder
OOB/console independent               WAN/DCI routed + diverse
```

## 六个万能词

`latency · determinism · loss · failure domain · observability · operability`

任何题都说：需求 → traffic classes → 正常路径 → 故障路径 → 测量 → 取舍 → 运维。

## 关键公式

```text
serialization = frame_bits / line_rate
fiber propagation ≈ 5 µs/km one-way (粗略)
queue bytes ≈ (ingress_rate - egress_rate) × burst_time
recovery = detection + convergence + session + state + business resume

PTP path delay = ((t2-t1)+(t4-t3))/2
PTP offset     = ((t2-t1)-(t4-t3))/2
```

64-byte Ethernet frame若加 8B preamble/SFD + 12B IFG，链路占用 84B：约 672ns@1G、67.2ns@10G、6.72ns@100G（不含 PHY/FEC/设备）。

## 常见协议锚点

| 协议 | 锚点 |
|---|---|
| BGP | TCP 179，policy，filter/max-prefix，RIB/FIB |
| OSPF | IP protocol 89，link state/LSDB/SPF |
| IGMP | IP protocol 2，host membership |
| PIM | IP protocol 103，multicast tree/RPF |
| BFD | 常见 UDP 3784 single-hop、4784 multihop、3785 echo |
| PTP | 常见 UDP 319 event、320 general；profile/transport 可不同 |
| NTP | UDP 123 |

IPv4 multicast 为 `224.0.0.0/4`；SSM 常用 `232.0.0.0/8`。地址范围会背不等于会设计，仍要确认 venue 的 `(S,G)`、TTL 和交付边界。

## A/B 行情恢复

```text
both lines receive -> first sequence wins -> de-duplicate
gap -> mark stale -> other line/cache -> retransmit -> snapshot
-> replay incrementals -> validate -> healthy
```

## 三个不能混淆

- Network convergence ≠ application/session recovery。
- Timestamp resolution/precision ≠ UTC accuracy。
- Redundant device/carrier name ≠ independent failure domain。

## 丢包排查链

`source → optic/CRC/FEC → switch ingress/fabric/egress queue → NIC ring → softnet/socket → app sequence/backlog`

比较：A vs B、good vs bad host、before vs after、old vs new path。

## 延迟回答限定词

先问清：one-way/RTT、wire/app、frame size、load/PPS、feature、p50/p99/p99.9/max、clock source、normal/failover。

## Colo 交付链

`order/agreement → LOA/CFA → rack/power/XC → stage → L1/L2/L3 → feed/session → certification/rehearsal → performance/failure → handover`

## Migration MOP

`precondition · one action/owner · expected result · evidence · checkpoint · abort trigger · rollback · reconciliation · soak`

## Linux 快速锚点

- RSS/queue、IRQ、application、memory 同 NUMA locality。
- Coalescing/buffer：吞吐与 burst tolerance 对 latency/staleness。
- GRO/LRO/TSO/checksum offload 会改变 capture/packet semantics。
- Kernel bypass：更少 syscall/copy/scheduling；更高 CPU/复杂性/可观测成本。

## 五句高分表达

1. “I would first define the measurement point and percentile before quoting a latency number.”
2. “I design redundancy against common failure modes, not just component failure.”
3. “A routing failover is only one part of the application recovery timeline.”
4. “For market data, sequence continuity and book freshness are the service indicators.”
5. “I would preserve evidence and compare a bad path against a simultaneous good control before changing anything.”

## 五句不要说

- “UDP 不可靠，所以行情应该用 TCP。”
- “双机/双运营商就是完全冗余。”
- “BFD 50×3，所以 150ms 一定恢复。”
- “Ping 正常说明网络正常。”
- “把 buffer 调大/把所有 offload 关掉就会更快。”

