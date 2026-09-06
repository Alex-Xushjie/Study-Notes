# Low Latency Networking

## 1. 四个指标一起看

- **Latency**：端到端耗时；明确 one-way/RTT 和起止点。
- **Jitter**：延迟变化；交易系统更关注 distribution/tail，而不只是平均值。
- **Loss**：显性 discard 或 sequence gap；重传/恢复会造成巨大业务延迟。
- **Throughput/capacity**：Gbps、pps 和 burst absorption。

只说“交换机 300ns”是不完整的：测试 frame size、负载、端口组合、功能开启情况、cut-through/store-and-forward 和 percentile 都会改变结果。

## 2. 延迟来源

```text
propagation + serialization + PHY/FEC + switching
+ queueing + NIC/PCIe/DMA + kernel + scheduling + application
```

- 光纤传播粗略约 **5 µs/km 单程**。
- Serialization delay：`frame_bits / line_rate`。例如 1500-byte 仅按 frame 计算，在 10G 约 1.2 µs，在 100G 约 0.12 µs；严格链路占用还应算 preamble、IFG 等 overhead。
- Queueing 是最不确定的一项。没有拥塞时几乎为零，microburst 时可主导 tail。
- FEC 提高链路可靠性但增加固定延迟；不同速率/optic/FEC mode 差异需查平台并实测。

## 3. Cut-through vs store-and-forward

- **Cut-through**：收到足够 header 即开始转发，降低小/大 frame 的 switching latency；可能传播坏帧，且速率转换/拥塞时仍需 buffering。
- **Store-and-forward**：收完整帧并检查 FCS 后转发；延迟含完整 serialization，但隔离坏帧更好。

不要假设设备宣传 cut-through 就在所有 feature/path 下保持同样延迟。ACL、routing、timestamp、speed conversion、congestion 和不同 ASIC pipeline 需验证。

## 4. Buffer 取舍

- ULL switch 常以 shallow buffer 换低、稳定延迟，适合无拥塞的精心容量设计。
- Deep-buffer switch 吸收 WAN/burst/速度不匹配，但排队可使数据变 stale。
- 对 market data，过期 500 µs 的包可能比明确丢包更难处理；策略需求决定取舍。
- PFC/“lossless Ethernet”会引入 pause propagation 和 head-of-line blocking，不能默认用于交易网。

## 5. ECMP、LAG 与 hash

ECMP/LAG 通常按 flow hash，不会把一个 UDP `(S,G)` 或 TCP session 的包均匀铺到所有链路。成员变化可能 rehash；per-packet 模式可能乱序。对于极敏感流，应知道它会落在哪条物理路径，并监控 polarization。

## 6. Benchmark 方法

1. 定义测量点（wire/NIC/app）、方向、clock source。
2. 用真实 frame-size mix、pps、multicast fan-out、burst profile 和 feature config。
3. 预热，测 p50/p99/p99.9/p99.99/max、loss、reorder；同时采 queue watermark/counters。
4. 分别测 idle、expected peak、overload 和 failover。
5. 保存 firmware/config/topology，使结果可复现。

常见错误：两端软件时钟未同步却测 one-way；SPAN capture oversubscribe；平均值掩盖长尾；只测 64B 单流；把 generator 自身限制归因于 DUT。

## 7. 30 秒回答

> Low latency means a predictable distribution, not only a low average. I decompose propagation, serialization, switching, queuing and host processing, then optimize the dominant term. I use cut-through and shallow-buffer designs only where capacity prevents congestion, because a microburst can trade packet loss for tail latency. Every claim is qualified by packet size, load, features, percentile and timestamp boundary, and I re-test during failover because the backup path often has different capacity and latency.

