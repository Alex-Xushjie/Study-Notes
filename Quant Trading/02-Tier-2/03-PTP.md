# Precision Time Protocol (PTP)

## 1. 为什么交易网络需要 PTP

PTP（IEEE 1588）通过硬件时间戳和网络时钟角色实现亚微秒甚至更好的同步，用于跨设备 latency measurement、事件排序、审计和法规记录。NTP 通常适合管理面和较宽松精度；两者不是简单“新旧替代”。

## 2. 四时间戳模型

```text
Master                              Slave
  |---- Sync / Follow_Up ----------->|  t1 sent, t2 received
  |<--- Delay_Req -------------------|  t3 sent; master records t4 on receipt
  |---- Delay_Resp(t4) ------------->|  slave learns t4

mean_path_delay = ((t2-t1) + (t4-t3)) / 2
offset_from_master = ((t2-t1) - (t4-t3)) / 2
```

这假设正反向路径延迟近似对称；asymmetry 会直接变成 offset error。

## 3. Clock roles

- **Grandmaster (GM)**：通常由 GNSS/原子钟参考提供时间。
- **Ordinary clock**：单 PTP port，可作 master 或 slave。
- **Boundary clock (BC)**：上游同步，下游作为新的 master；隔离 PTP packet load/PDV。
- **Transparent clock (TC)**：不成为时间源，把自身 residence time 写入 correction field。
- **PHC**：NIC 的 PTP Hardware Clock；`ptp4l` 常同步 PHC，`phc2sys` 再同步 system clock（以实际部署为准）。

## 4. BMCA、one-step/two-step、E2E/P2P

- **BMCA** 根据 priority、clock class/accuracy、variance、identity 等 Announce 信息选 master。生产通常通过 priority 和 topology 控制候选，不应让任意 server 赢得 GM。
- **One-step** 在 Sync 中直接写精确发送时间；**two-step** 用后续 Follow_Up 携带。设备支持和 profile 必须一致。
- **E2E** 用 Delay_Req/Resp 测端到端 mean path delay；**P2P** 在每条 link 用 Pdelay 测 peer delay。不要混配 profile。

NVIDIA 的 [PTP 文档](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/System-Configuration/Date-and-Time/Precision-Time-Protocol-PTP/) 给出 one/two-step 等实际平台配置示例；实现细节以设备版本为准。

## 5. 推荐架构

```text
GNSS antenna A -> GM-A --+                 +-> BC/switch -> NIC PHC
                         +-- PTP domain ---+
GNSS antenna B -> GM-B --+                 +-> monitoring probe
```

- GM、antenna、power、cable/path 都考虑共同故障；防 GNSS spoof/jam。
- 交易与 capture 的 timestamp domain/UTC-TAI/leap-second policy 一致。
- PTP-aware switch 使用 BC/TC；普通交换网络的 queueing PDV 会损害同步。
- 明确 multicast/unicast transport、VLAN、domain、profile 和 QoS。

## 6. 监控指标

- current GM identity、parent、clock class、steps removed、port state。
- offset from master、mean path delay、frequency adjustment、RMS/max、servo state。
- Announce/Sync timeout、GM change、faulty/listening 状态。
- GNSS lock、satellite count、antenna alarm、GM holdover quality/duration。
- PHC↔system clock offset；应用实际使用的是哪个 clock。

## 7. 故障场景

### Offset 突然偏移

先看 GM 是否变更、path delay/asymmetry、interface queue、BC/TC 状态、timestamp mode、PTP profile/domain、GNSS alarm；再检查 host servo/CPU。不要用一次 `date` 对比下结论。

### GNSS 丢失

GM 进入 holdover，clock class 应反映质量下降；监控误差随时间增长并在阈值处让业务 fail closed/degrade。备用 GM 的 BMCA 切换要验证不会发生大 step 或时间倒退。

### 双 GM 都正常但 host 不准

检查它实际选中的 parent、PTP port state、hardware timestamp 是否启用、PHC 是否同步、`phc2sys` 方向、domain/profile/VLAN、asymmetry 和 NIC firmware/driver。

## 8. 30 秒回答

> PTP accuracy comes from hardware timestamps, a controlled clock hierarchy and a complete error budget. The slave estimates offset and path delay from four timestamps, so path asymmetry becomes a synchronization error. I use redundant, controlled grandmasters and PTP-aware boundary or transparent clocks, synchronize the NIC PHC and then the system clock as required, and monitor GM identity, offset, mean path delay, servo and holdover state. Failover tests include GNSS loss and GM changes, with explicit limits on time steps and application behavior.
