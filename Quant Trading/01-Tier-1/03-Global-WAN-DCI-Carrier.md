# Global WAN / DCI / Carrier Design

## 1. 先区分距离和用途

- **Campus/colo 内**：专注 ns～µs、物理跳数、cut-through、精确测量。
- **Metro DCI**：dark fiber/wavelength/low-latency Ethernet，关注真实路由、放大器/中继、保护切换。
- **Regional/global WAN**：leased line/MPLS/IP transit/SD-WAN 等，传播时延占主导，关注可用性和业务恢复。

不要用同一方案解决所有流量。极低延迟 signal/order path 与 bulk replication、management、backup feed 可以使用不同产品和路由策略。

## 2. Carrier diversity 的真相

“两家 carrier”只代表合同多样性，不自动代表物理多样性。逐层验证：

```text
router port -> patch panel -> cross-connect -> MMR
-> building entrance -> metro conduit/manhole -> carrier POP
-> long-haul route/amplifier hut -> destination entrance/MMR -> port
```

要求 carrier 提供可审计的 route map/SRLG 信息、demarc、保护方式、planned maintenance 通知和 escalation。两条线路可能租用同一 underlying fiber provider，或在最后一公里、桥梁、海缆、building entrance 汇合。

## 3. 产品选择

| 产品 | 适用 | 主要取舍 |
|---|---|---|
| Dark fiber | Metro 极致控制/延迟 | 自备 optics/DWDM、运维和保护复杂 |
| Wavelength | 低延迟大带宽 DCI | carrier 光层不可见，确认真实路由和保护 |
| Ethernet private line | 快速交付、L2 handoff | provider bridge/failure domain、MTU/OAM |
| MPLS/L3VPN | 多点企业 WAN | 路径和排队不透明，不是最低延迟 |
| Internet + encryption | OOB/备份/非关键 | jitter/loss/路径不可控 |
| Microwave/mmWave | 特定 metro/长距离低延迟 | 天气、容量、许可和 availability 取舍 |

## 4. L2 还是 L3 DCI

默认倾向 routed DCI：

- 故障域小、loop 风险低、ECMP/traffic engineering 明确。
- 变更和排障有清晰 next hop；不把 STP/MAC flood 延伸全球。
- 缺点是应用需要支持 routed multicast/地址变化，且 routing design 更重要。

只有在应用/venue 强制邻接、迁移期或特定集群需求时延伸 L2，并限制 VLAN、加 loop guard/storm control、定义 split-brain 行为。

## 5. Routing design

- IGP 管基础 reachability；BGP 管 policy、站点/服务前缀和边界，避免把所有东西塞入一个协议。
- ECMP 要知道 hash fields；单一 5-tuple 不会自动分散，per-packet load balancing 会导致乱序。
- BFD 的目标是快速检测 forwarding path，不是越快越好；定时器需结合设备能力、链路质量和 false positive 风险。
- 用 local-pref/community/AS-path 等表达 primary/backup；防止 route leak，设置 prefix/maximum-prefix 过滤。
- 对 stateful TCP/FIX 会话，路由恢复不代表会话恢复。必须计算 detection + convergence + TCP/session reconnect + sequence recovery。

## 6. Latency 与容量验收

必须在合同/SLA之外自己测：

- RTT/one-way 的 p50、p99、p99.9、max；one-way 需要同步时钟。
- 不同 packet size/load/time-of-day；微突发下 loss 和 jitter。
- 实际 hop/path 与变化，protection switch 前后差异。
- CIR/policing、burst size、MTU、QoS remark、FEC 和 provider handoff counter。

物理路径长度通常比设备优化重要。`RTT/10 µs ≈ fiber route km` 只能作非常粗糙 sanity check（光纤约 5 µs/km 单程），还包含设备延迟且真实线路会绕行。

## 7. 故障和演练矩阵

| 故障 | 必须观察 |
|---|---|
| 客户侧 port/optic down | LOS→BFD/routing→应用影响时间 |
| Carrier 黑洞但 link up | BFD/OAM 能否检测；静态路由是否卡死 |
| 路径 flap | damping/hold-down、session storm、重复切换 |
| 单 MMR/entrance 失效 | 另一条是否真正独立 |
| Provider maintenance | 路由是否悄悄变长、latency SLO 是否越界 |
| 双向不对称 | one-way latency、ACL/uRPF、PTP 误差影响 |

## 8. 2 分钟回答模板

> I classify DCI traffic first because a latency-sensitive signal path, position replication and OOB management do not need the same service. For low-latency metro paths I evaluate dark fiber, wavelengths or private Ethernet based on measured route length, protection and operations. I prefer routed boundaries to contain L2 failure domains. Diversity is verified end to end—ports, MMRs, building entrances, conduits, carrier POPs and long-haul SRLGs—not inferred from two carrier names. Routing policy makes primary and backup intent explicit, while BFD timers are tuned to avoid false failovers. Acceptance measures percentile latency, loss and jitter under realistic load, then tests hard-down and silent-blackhole failures through application session recovery.

