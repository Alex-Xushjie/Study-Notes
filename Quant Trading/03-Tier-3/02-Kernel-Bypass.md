# Kernel Bypass

## 1. 是什么

Kernel bypass 让用户态应用直接/近直接访问 NIC queues 与 DMA memory，绕过通用 socket stack 的部分开销。常见生态包括 DPDK、AF_XDP、vendor user-space stacks（如 Onload/XLIO）和 RDMA 类方案；API、兼容性和 bypass 程度不同。

```text
Traditional: NIC -> driver/NAPI -> kernel stack -> socket -> app
Bypass:      NIC -> mapped queue/shared memory -> polling user app
```

## 2. 为什么更快

- 减少 syscall/context switch、data copy 和通用协议处理。
- Poll-mode driver 避免 interrupt/wakeup 抖动。
- Batch/vector processing 提高每周期效率。
- 应用直接控制 queue、buffer 和 CPU locality。

但 kernel bypass 不减少光纤传播、交换机排队或 exchange processing，也不会自动修复糟糕的 NUMA/PCIe/代码。

## 3. 代价

- 独占 CPU、高功耗；busy loop 会影响共享环境。
- 应用/运维复杂，标准工具（iptables/tcpdump/socket metrics）可见性可能下降。
- 自己承担 buffer ownership、flow steering、协议栈/重传的更多责任。
- NIC/driver/firmware/kernel 兼容矩阵和升级风险。
- HA、bonding、namespace、安全策略和 capture 需要专门集成。

## 4. 方案讨论

| 方案类型 | 特征 | 适合表达 |
|---|---|---|
| DPDK | poll-mode、hugepages、用户态 driver | 极致可控，应用改造/运维大 |
| AF_XDP | Linux XDP/UMEM，与内核生态较近 | 灵活，性能依 zero-copy/driver 支持 |
| Onload/XLIO 类 | 加速现有 socket API 的用户态 stack | 应用改动较小，vendor/NIC 依赖 |
| FPGA/SmartNIC | 在 NIC 前/上处理部分 pipeline | 最低延迟潜力，开发验证难度高 |

## 5. 评估标准

- p50/p99/p99.9/max 与 loss under burst，不只单包 benchmark。
- CPU cores、power、NUMA、hugepage 和 memory footprint。
- Multicast join、TCP semantics、hardware timestamp、capture 能力。
- Failure/restart/session recovery、upgrade rollback、observability。
- 团队能否 24×7 运维，收益是否覆盖复杂度。

## 6. 30 秒回答

> Kernel bypass reduces syscall, copy and scheduler overhead by giving user space direct control of NIC queues and usually polling dedicated cores. DPDK gives maximum control, AF_XDP stays closer to the Linux ecosystem, and accelerated socket stacks can reduce application changes. The trade-off is CPU and power cost, operational complexity, weaker visibility and tighter hardware compatibility. I would choose it only after profiling shows the host stack is material, then benchmark the actual multicast or TCP workload including timestamps, burst loss, failover and observability.

