# Quant Trading Network Engineer 面试冲刺笔记

> 目标：不是背出定义，而是能从 **latency、determinism、loss、failure domain、operability、cost** 六个维度解释设计取舍。

## 最短使用路径

1. 先读 [冲刺学习计划](00-Crash-Course-Plan.md)，建立端到端心智模型。
2. Tier 1 按顺序读完并口述每章末尾的 2 分钟答案。
3. Tier 2 重点掌握测量与排障：时间戳、PTP、PCAP、路由和物理层。
4. Tier 3 学到“能说明为什么、怎么验证、有什么副作用”，不要陷入参数背诵。
5. 最后用 [高频问题与场景演练](90-Interview-Drills/01-Question-Bank.md) 和 [一页速查表](90-Interview-Drills/02-Cheat-Sheet.md) 闭卷练习。

## 目录

### Tier 1 — 必须能深入讨论

- [Global trading network architecture](01-Tier-1/01-Global-Trading-Network.md)
- [Exchange colo buildout](01-Tier-1/02-Exchange-Colo-Buildout.md)
- [Global WAN / DCI / carrier design](01-Tier-1/03-Global-WAN-DCI-Carrier.md)
- [Major exchange ecosystem](01-Tier-1/04-Major-Exchange-Ecosystem.md)
- [Market Data / Order Entry architecture](01-Tier-1/05-Market-Data-Order-Entry.md)
- [Multicast](01-Tier-1/06-Multicast.md)
- [HA / redundancy / failure domains](01-Tier-1/07-HA-Redundancy-Failure-Domains.md)
- [Network migration / cutover](01-Tier-1/08-Migration-Cutover.md)

### Tier 2 — 必须有扎实理解

- [Low latency networking](02-Tier-2/01-Low-Latency-Networking.md)
- [Hardware timestamping / TAP / SPAN / MetaWatch](02-Tier-2/02-Timestamping-TAP-SPAN-MetaWatch.md)
- [PTP](02-Tier-2/03-PTP.md)
- [PCAP / latency troubleshooting](02-Tier-2/04-PCAP-Latency-Troubleshooting.md)
- [BGP / OSPF / ECMP / BFD](02-Tier-2/05-Routing-and-Fast-Convergence.md)
- [Physical infrastructure / optics / cabling](02-Tier-2/06-Physical-Optics-Cabling.md)

### Tier 3 — 能讨论即可

- [NIC tuning / Linux networking / CPU affinity / NUMA](03-Tier-3/01-Linux-NIC-CPU-NUMA.md)
- [Kernel bypass](03-Tier-3/02-Kernel-Bypass.md)
- [Python automation](03-Tier-3/03-Python-Automation.md)
- [Monitoring / Prometheus / Grafana](03-Tier-3/04-Monitoring.md)

### Interview drills

- [30 道高频问题](90-Interview-Drills/01-Question-Bank.md)
- [面试前 15 分钟速查表](90-Interview-Drills/02-Cheat-Sheet.md)
- [6 道白板场景题](90-Interview-Drills/03-Whiteboard-Cases.md)

## 贯穿所有题目的答题框架

面对任何架构题，按这个顺序说：

1. **Requirements**：交易品种、venue、峰值 PPS/bandwidth、latency/jitter/loss SLO、RTO/RPO、合规和预算。
2. **Traffic classes**：market data、order entry、drop copy、risk/control、management、time sync，绝不笼统说“交易流量”。
3. **Design**：画出正常路径和备用路径，明确 L1/L2/L3 边界、路由和组播状态。
4. **Failure domains**：设备、链路、光路、机柜、供电、meet-me room、运营商、园区、metro、地区逐层枚举。
5. **Failure behavior**：检测时间、收敛时间、会丢多少数据、session 是否重建、订单状态如何确认。
6. **Observability**：在哪些点采集 packet、hardware timestamp、interface counter、routing event 和 application log。
7. **Operations**：测试、变更、回滚、容量管理、文档、厂商升级和演练。

一句能拉开差距的话：

> Low latency is not just the lowest median. I optimize the tail, determinism and failure behavior, and I prove the result with synchronized hardware timestamps at clearly defined measurement points.

## 自测标准

- **深入讨论**：能画图，能说取舍，能处理两种以上故障，能说明如何测量。
- **扎实理解**：能解释机制，能读常见输出/PCAP，能给出验证步骤。
- **能讨论**：知道作用、典型方案、主要风险，不装作精通实现细节。
