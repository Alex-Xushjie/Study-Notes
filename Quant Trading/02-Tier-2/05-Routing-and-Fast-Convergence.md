# BGP, OSPF, ECMP and BFD

## 1. 各自解决什么

| 技术 | 作用 | 交易网络关注点 |
|---|---|---|
| OSPF | 域内 link-state reachability、SPF | area、cost、adjacency、LSA/SPF churn |
| BGP | policy-based inter-domain/service routing | attributes、filter、scale、failure policy |
| ECMP | 多条等价 next hop 转发 | hash、polarization、rehash、乱序 |
| BFD | 快速检测 forwarding path 故障 | timer、hardware offload、false positive |

## 2. OSPF 心智模型

Hello 建邻 → adjacency/LSDB 同步 → SPF → RIB/FIB。常见邻接故障：area、timer、auth、MTU、network type、duplicate router ID。OSPF cost 决定最短路径，但实际转发还要确认 FIB/ECMP；频繁 LSA/SPF 可能带来 control-plane churn。

设计上保持 area 和拓扑简单，passive 不需建邻的接口，汇总/过滤在合适边界；不要为了“更快”任意压 Hello/Dead timer，BFD 更适合独立快速探测。

## 3. BGP 心智模型

TCP 179/session → OPEN/KEEPALIVE → UPDATE → policy/best path → RIB/FIB。常用属性：local preference、AS path、origin、MED、eBGP/iBGP、IGP metric、router ID（具体 best-path 顺序随实现）。

生产必备：prefix filter、maximum-prefix、route policy、community、下一跳可达性、明确 primary/backup。`Established` 只证明 control session，不能证明 data-plane 每条路径转发。

## 4. BFD

检测时间粗略为协商后的接收间隔 × detect multiplier，但设备调度/offload/拥塞会影响实际。BFD 能检测 link-up blackhole，通知 OSPF/BGP/静态路由；它不修复应用 session。

过激 timer 的风险：control plane 忙或瞬时拥塞导致 false down，引发 route flap 和更大 packet loss。先确认硬件 offload/规模能力并做压力测试。协议目的可参考 [RFC 5880](https://www.rfc-editor.org/info/rfc5880/)。

## 5. ECMP/LAG 追问

- Hash 通常基于 src/dst IP、L4 ports、protocol 等；设备/封装可配置。
- 一个 TCP flow 固定在一个 member 上，因此不会把单 flow 带宽叠加。
- Member 失败/恢复会 rehash 一部分 flows；resilient hashing 可减少扰动但不是零。
- Per-packet balancing 可能乱序，TCP 和 sequenced UDP feed 通常不希望。
- Multicast ECMP 与 unicast ECMP 支持/算法可能不同，查平台实现。

## 6. 排障顺序

1. Physical/interface/ARP/ND。
2. Neighbor/session state 与最近 change。
3. Protocol database（LSDB/BGP table）是否学到预期 path。
4. Policy/best path/RIB。
5. FIB/adjacency/ECMP member 是否编程。
6. 实际 flow hash/packet counter/capture。
7. Return path、ACL/uRPF、MTU。

Control plane 正确而 data plane 错误可能是 stale FIB、ASIC programming、ARP adjacency、ACL、hash member 或 silent blackhole。

## 7. 收敛时间回答

```text
failure detect (LOS/BFD/hello)
+ protocol reaction/SPF/best path
+ RIB-to-FIB programming
+ ARP/neighbor resolution
+ application reconnect/recovery
```

报告业务实际 loss/duplicate/reorder 和 session RTO。不要把 BFD 3×50ms 直接称为“150ms 业务恢复保证”。

## 8. 30 秒回答

> OSPF gives internal topology reachability, BGP expresses routing policy, ECMP installs multiple forwarding next hops, and BFD accelerates forwarding-path failure detection. I troubleshoot them from physical state through neighbor databases, policy, RIB and hardware FIB to the actual hashed flow. Fast timers are useful only if the platform can sustain them without false positives. My convergence budget includes detection, protocol calculation, FIB programming and application session or state recovery, and I validate packet loss and tail latency during the event.

