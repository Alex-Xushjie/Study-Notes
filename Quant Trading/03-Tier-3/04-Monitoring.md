# Monitoring with Prometheus and Grafana

## 1. 从 service SLO 向下监控

```text
Business: can we trade safely?
  order ACK/fill/drop-copy mismatch, book stale, venue/session health
Application:
  sequence gaps, recovery duration, queue depth, processing latency
Host/NIC:
  ring/socket/softnet drops, IRQ/CPU/NUMA, PHC offset
Network:
  loss/errors/discards, queue watermark, BGP/BFD/PIM/IGMP, optics
Facility/carrier/time:
  circuit/path, power/temp, GM/GNSS/holdover
```

## 2. Prometheus 数据模型要点

- Counter：单调累计，如 packets/drops/gaps；用 `rate()`/`increase()`，注意重启 reset。
- Gauge：当前值，如 queue depth、PTP offset、optical power。
- Histogram：latency distribution，可跨实例聚合；bucket 要覆盖真正 SLO。
- Summary：客户端计算 quantile，通常不能正确跨实例聚合。

避免高 cardinality label：order ID、symbol、source IP 任意组合会拖垮系统。按 venue/channel/session 聚合，细粒度事件放日志/trace/专用时序系统。

## 3. 关键 dashboard

- **Market open cockpit**：venue/session、feed A/B、gap/stale、OE ACK latency、drop copy、PTP。
- **Latency**：p50/p99/p99.9 + traffic/load + queue watermark，能按 deploy/change 标注。
- **Multicast**：每 channel PPS/rate/gap/A-B skew，switch/NIC/kernel/app 同屏。
- **Routing/carrier**：BGP/BFD change、path/RTT/one-way、loss、circuit maintenance。
- **Physical/time**：DOM/FEC trend、temperature/power、GM identity/offset/holdover。

## 4. 告警设计

- Page actionable symptoms：关键 feed stale、OE session down、drop-copy mismatch、PTP 超安全阈值。
- Ticket/observe early causes：FEC corrected 上升、光功率趋势、容量增长。
- 使用持续时间、multi-window burn rate 或复合条件抑制瞬态噪声，但关键硬故障立即 page。
- 告警中含 site/venue/channel、影响、runbook、dashboard 和 owner。
- 监控系统本身独立于 production path，remote write/抓包不能制造拥塞。

## 5. Latency histogram 陷阱

- Average 无法显示双峰/tail。
- Prometheus histogram bucket 太粗会让 p99 失真；ns/µs 工作负载要专门设计 bucket。
- Client、NIC、FPGA 指标 measurement point 不同，不能画在同一轴上假装等价。
- Sampling 会漏 rare tail；记录 sampling ratio，并用硬件设备保留 incident window。

## 6. 30 秒回答

> I monitor from the trading service down to the infrastructure. The primary signals are book freshness, sequence recovery, order-session and drop-copy consistency, and latency percentiles; network, NIC, PTP and optical metrics explain those symptoms. In Prometheus I use counters, gauges and deliberately bucketed histograms while controlling label cardinality. Alerts are actionable and tied to a runbook, and dashboards correlate latency with traffic, queues, route events and clock health. Monitoring and packet capture capacity are isolated so observability cannot harm the production path.

