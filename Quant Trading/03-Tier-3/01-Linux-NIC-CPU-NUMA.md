# NIC Tuning, Linux Networking, CPU Affinity and NUMA

## 1. 收包路径

```text
wire -> NIC RX queue/ring -> DMA to memory -> interrupt/NAPI poll
-> driver -> kernel network stack -> socket receive buffer -> application
```

每一段都可能排队或丢包。调优目标是 locality、少抢占、足够容量和稳定 tail，不是把所有参数调到最大。

## 2. 核心概念

- **RSS**：NIC 对 flow hash，将包放入不同 hardware RX queues。
- **IRQ affinity**：每个 queue interrupt/NAPI 主要在哪个 CPU 处理。
- **RPS/RFS**：软件侧把处理分散/引向应用 CPU；可能帮助普通负载，也可能增加 IPI/cache miss。
- **XPS**：选择 TX queue/CPU 映射。
- **Interrupt coalescing**：攒多个事件再中断，提高吞吐/降 CPU，但增加 latency/jitter；低延迟常减小或采用 adaptive，必须实测。
- **Busy polling**：CPU 主动轮询降低 wakeup 延迟，代价是高 CPU/功耗。
- **Socket buffers/rings**：过小会 burst drop，过大可能隐藏 backlog 并提高 stale latency。

## 3. CPU affinity 与 NUMA

NIC 挂在某个 PCIe/NUMA node。理想 hot path 将 NIC queue、IRQ、application thread 和 memory 放在同一 NUMA node，并给关键线程隔离 CPU，减少 remote memory、cache bouncing 和 scheduler migration。

但不要把所有工作绑一个 core：RX processing、feed handler、strategy、logging 可能互相饿死。Hyper-thread siblings 共享 execution resources；关键线程是否使用 sibling 需 benchmark。

## 4. Offload 的副作用

- GRO/LRO 合并接收包，有利吞吐但改变逐包时序/可见性，market UDP 要慎重。
- TSO/GSO 让 host capture 看到大“虚拟包”，wire 上会分段。
- Checksum offload 让发送端 host PCAP 显示 checksum 未完成。
- VLAN/filter/flow steering offload 影响包进入哪个 queue。

不是所有 offload 都要关。先明确 workload 和 capture/timestamp 语义，再 A/B benchmark。

## 5. 常用只读检查

```bash
ethtool -i eth0
ethtool -k eth0
ethtool -c eth0
ethtool -g eth0
ethtool -l eth0
ethtool -S eth0
ethtool -T eth0
cat /proc/interrupts
cat /proc/net/softnet_stat
ss -u -a -m
lscpu -e=CPU,NODE,SOCKET,CORE
cat /sys/class/net/eth0/device/numa_node
```

真实字段依 driver。任何变更前后保存：配置、p50～max、loss、CPU、功耗/温度和高峰稳定性。

## 6. 调优顺序

1. 更新/固定 BIOS、firmware、driver、kernel 基线。
2. 确认 NUMA/PCIe topology、link speed/width。
3. 将 flow/queue/IRQ/application 建立明确映射。
4. 调 coalescing、ring/socket buffer、offload，一次一个变量。
5. 在真实 PPS/burst 下测 latency tail 和 drop。
6. 记录持久化方式；重启后验证没有 drift。

## 7. 30 秒回答

> I tune the complete receive path, not isolated sysctls. I map the NIC queue, IRQ, application thread and memory to the local NUMA node, then measure whether RSS and affinity distribute the real flows as intended. Coalescing and large buffers trade throughput and burst tolerance for latency or stale queues, while offloads can change packet timing and capture semantics. I change one variable at a time under realistic PPS and report tail latency, drops and CPU, then verify persistence after reboot.

