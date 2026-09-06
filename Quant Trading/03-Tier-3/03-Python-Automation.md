# Python Automation for Trading Networks

## 1. 高价值场景

- 从 source of truth 生成 colo port/IP/VLAN/multicast/circuit matrix。
- Pre/post-check：接口、DOM、BGP/BFD、IGMP/PIM、PTP、config diff。
- 批量解析 PCAP/sequence gap、counter snapshot 和 latency CSV。
- Exchange technical notice 与 config inventory 对照（仍需人工审批）。
- 生成 MOP evidence bundle、as-built 和审计记录。

低延迟 packet hot path 通常不是 Python 的场景；Python 更适合控制面、验证与分析。

## 2. 安全自动化原则

- Read-only discovery 与 write action 分离；默认 dry-run。
- 输入使用 schema/type validation；拒绝未知字段和越界目标。
- 幂等（重复运行不产生额外副作用），限制 concurrency 和 blast radius。
- 先 canary，再分批；每批有 health gate 和 rollback。
- Secret 来自 vault/env integration，不写日志/仓库。
- 保存 request ID、operator、timestamp、before/after、device response。

## 3. 一个面试级结构

```text
inventory/source-of-truth
        -> validate schema and topology invariants
        -> render candidate config
        -> offline lint/unit tests
        -> device diff / dry-run
        -> approval
        -> canary deploy
        -> network + application post-check
        -> batch or rollback
```

交易网络的 post-check 必须含业务指标：feed sequence、A/B skew、OE session/drop copy、PTP offset、latency tail，而不只 `show interface up`。

## 4. 编码关注点

- `dataclass`/Pydantic 类模型，明确 IP/network、enum、optional 字段。
- API timeout、bounded retry with backoff；write 请求是否可安全重试要区分。
- Structured logging，时间统一，correlation ID。
- Unit test 验证 renderer/parser；用 golden files 测 config diff；mock device API。
- 大规模 I/O 可用 asyncio/threading，但对单设备限速，避免控制面 storm。

## 5. 示例：验证而非配置

```python
def validate_feed(expected, observed):
    assert observed.link_up
    assert observed.vlan == expected.vlan
    assert expected.source_group in observed.multicast_state
    assert observed.sequence_gap_rate <= expected.max_gap_rate
    assert observed.ptp_offset_ns <= expected.max_ptp_offset_ns
```

面试时说明真实实现不会用裸 `assert` 处理生产错误，而会产生 typed result、证据和清晰 exit code。

## 6. 30 秒回答

> I use Python for control-plane automation, validation and evidence collection rather than the latency-sensitive packet path. My workflow validates typed inventory, renders and lints a candidate, shows a dry-run diff, requires approval, deploys to a canary and checks both network and trading health before batching. Writes are idempotent where possible, retries are bounded, secrets are external, and every action is audited. For a feed migration, post-checks include sequence continuity, PTP offset and application health—not only interface state.

