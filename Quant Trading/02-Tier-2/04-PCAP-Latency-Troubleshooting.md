# PCAP and Latency Troubleshooting

## 1. 先写 hypothesis，再抓包

一个好问题应是：“2026-xx-xx 09:30:00～09:30:05，host H 对 `(S,G)` 出现 sequence gaps，同时 NIC/switch 哪一级开始与正常路径分叉？”而不是“网络很慢”。

先固定：时间窗、flow/session/channel、正常基线、业务症状、时钟源、capture point、谁拥有各段。

## 2. 证据优先级

```text
application sequence/log
       ^
socket/kernel counters
       ^
NIC hardware timestamp/counters
       ^
server-facing capture
       ^
switch queue/interface counters
       ^
exchange/carrier-facing capture
```

找到“最后一个正确点”和“第一个错误点”。不同点位的 PCAP 要有可比较时钟，否则只能比较 sequence/content，不能直接相减 one-way latency。

## 3. PCAP 核心能力

### Capture

```bash
tcpdump -ni eth0 -s 0 -B 4096 -w incident.pcap 'udp and host 239.1.1.1'
tcpdump -ni eth0 -s 0 -w oe.pcap 'tcp port 12345'
```

- `-n` 避免 DNS；`-s 0` 保留全包；BPF 尽量在 capture 时缩小流量。
- 高 PPS 下 tcpdump 可能自己 drop；记录结尾 dropped-by-kernel、NIC 和 packet-broker counters。
- 生产抓包注意磁盘、敏感数据、保留策略和权限。

### Inspect

```bash
tshark -r incident.pcap -q -z io,stat,0.001
tshark -r oe.pcap -Y 'tcp.analysis.retransmission || tcp.analysis.out_of_order'
capinfos incident.pcap
```

对 native feed 最重要的是 sequence decoder；通用工具只看到 UDP 包并不等于 book 正确。

## 4. 分析模式

### UDP market data

检查 sequence gap/duplicate/out-of-order、inter-arrival delta、burst density、IP fragmentation、TTL、source/group、A/B skew。UDP checksum offload 可能让 host-side outbound capture 显示“bad checksum”，需结合抓包点判断。

### TCP order entry

检查 handshake RTT、retransmission、duplicate ACK、zero window、window size、RST/FIN、delayed ACK/Nagle（是否适用）、应用 heartbeat 和 message sequence。TCP RTT 变高不证明网络拥塞，可能是接收应用未及时消费或 exchange processing。

### Latency

- 同一 clock/capture device 内：直接匹配 packet key 并相减。
- 跨 device：先证明 PTP offset/accuracy，校准 fixed cable/device delay。
- 报告 distribution，不用单个 screenshot；将异常与 queue watermark、CPU、route/event 对齐。

## 5. 常见误判

- Host PCAP 看不到包，就说 switch 丢包：包可能到 NIC 后在 ring/kernel 前丢。
- PCAP 有 sequence gap，就说网络丢包：source 也可能未发，decoder/capture 也可能 drop。
- TCP retransmission 出现在 sender PCAP，就说 receiver 丢：需要双边/中间点判断原包和 ACK 去向。
- 所有时间戳显示同一小数位，就认为 clocks synchronized。
- 抓包开始后故障消失：promiscuous/all-multicast、CPU/IRQ、timing 被改变，观察行为产生扰动。

## 6. 标准 incident 流程

1. Triage：保护交易/风险，决定 stop/degrade/failover。
2. Scope：单 host、单 feed、单 venue、单 path，还是共同问题。
3. Timeline：统一时区与 clock，记录首次/恢复/变更。
4. Evidence：应用 sequence → OS/NIC → switch/path，保存未清 counters。
5. Compare：A vs B、good host vs bad host、before vs after、old vs new path。
6. Hypothesis test：一次改变一个变量，能复现/证伪。
7. Recovery 与 RCA 分开：恢复服务后再做根因，避免无证据“修好”。

## 7. 30 秒回答

> I scope an incident to an exact flow and time window, then find the last correct and first incorrect observation point. For market data I correlate application sequence gaps with A/B captures, switch queues, NIC rings, kernel drops and feed-handler backlog. For TCP I separate handshake/network RTT, retransmission and receive-window behavior from application or exchange processing. PCAP is only evidence if the capture path did not drop and its timestamp clock is understood. I preserve counters and compare a bad path with a simultaneous good control before changing anything.

