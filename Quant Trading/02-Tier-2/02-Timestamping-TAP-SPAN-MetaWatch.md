# Hardware Timestamping, TAP, SPAN and MetaWatch

## 1. Timestamp 越靠近 wire，包含的未知越少

| 点位 | 包含/遗漏 | 用途 |
|---|---|---|
| Application timestamp | 包含 NIC、kernel、scheduler；受暂停影响 | 业务可见延迟 |
| Kernel software timestamp | 靠近协议栈，仍受 driver/queue 影响 | host stack 分段 |
| NIC hardware timestamp | MAC/PHY 附近，绕过多数 host jitter | 精确 RX/TX wire boundary |
| Switch/FPGA timestamp | 网络内特定 ingress/egress | hop/segment 和独立取证 |

**Precision** 是分辨率/重复性，**accuracy** 是接近真实 UTC/TAI，**synchronization** 是设备之间对齐；三者不能混用。

Linux 的 `SO_TIMESTAMPING` 能请求 RX/TX 软件或硬件时间戳；TX hardware timestamp 通常从 socket error queue 读取。先用 `ethtool -T <iface>` 看 NIC/driver 能力。参考 [Linux kernel timestamping](https://kernel.org/doc/html/latest/networking/timestamping.html)。

## 2. TAP vs SPAN

| | Passive optical TAP | Switch SPAN/mirror |
|---|---|---|
| Production impact | 光分光损耗，设备不供电也可透传（视型号） | 占 ASIC/端口资源，配置错误可影响设备 |
| Fidelity | 通常高，可见 physical errors 的范围依工具 | 拥塞时 mirror copy 可丢；可能不保留坏帧/精确时序 |
| Timestamp | TAP 自身不一定打时间戳，由后端设备完成 | switch timestamp 能力视平台 |
| 部署 | 需光预算、额外布线、A/B 方向 | 灵活、便宜、适合临时诊断 |

一个全双工链路的两个方向通常要分别复制。把两方向聚合到低速 capture port 会 oversubscribe；监控口无 drop 不等于 SPAN 内部没丢。

## 3. Packet broker / FPGA capture

功能可能包括 aggregation、filter、replication、truncation、metadata trailer、deep buffering 和 hardware timestamp。它们能构建可重复证据链，但要知道：

- Timestamp 在 ingress 还是 egress？
- 时钟如何同步、holdover 如何、误差预算是多少？
- Aggregation 拥塞时 drop/pause/shaping 行为？
- Metadata trailer 是否会被 decoder 识别？原始 frame 是否保留？
- A/B capture path 是否引入共同故障？

Arista [MetaWatch](https://www.arista.com/en/products/7130-meta-watch) 是典型 FPGA 网络观测方案：可做 tap/aggregation、深缓存和高精度时间戳，并把时间及端口等 metadata 附在 frame 后。它是观测工具，不等于应用 book sequence 永远正确。

## 4. 测量例子

```text
T1: exchange-facing capture ingress
T2: server NIC RX hardware
T3: server NIC TX hardware
T4: exchange-facing capture egress

network_rx = T2 - T1        (时钟需对齐)
host_tick_to_trade = T3-T2
order_network = T4-T3
```

若设备时钟未同步，仍可在同一个 clock domain 内测 segment 或 RTT；不要把 clock offset 当网络延迟。

## 5. 面试陷阱

- “纳秒时间戳”只说明格式/精度，不证明纳秒 accuracy。
- Software timestamp 的 p99 抖动可能来自 scheduling，不代表 wire 抖动。
- NIC RX timestamp 与应用收到包之间仍有 PCIe/DMA/ring/kernel/queue 延迟。
- TAP 增加 optical loss budget；装入已有弱光链路前必须算预算。
- SPAN 适合快速诊断，但不能默认作为无损 latency ground truth。

## 6. 30 秒回答

> I choose the timestamp point based on the question. Application timestamps show user-visible performance, while NIC or FPGA hardware timestamps remove most host scheduling noise and locate wire boundaries. Passive TAPs provide high-fidelity independent copies but consume optical budget; SPAN is convenient but the mirrored copy can be dropped or re-timed under load. A device such as MetaWatch combines tapping, aggregation and precise timestamps. Before trusting any result I validate the timestamp location, clock synchronization and accuracy, aggregation capacity, drop counters and metadata handling.

