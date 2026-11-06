# 低延迟实验、统计与综合作品

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 分阶段验证

L1离线序号/统计；L2自建低速UDP组播和故障；L3真实NIC队列/时间戳；L4专用设备/时钟下测路径与突发。没有真实硬件时仍可完成前两级，但不声称证明交易所接入或微秒准确度。

使用[组播实验指引](../../02-Multicast/09-Design-and-Troubleshooting/04-Lab-Guide-and-Review.md)自建频道，不连接真实行情/下单服务。已有[交易实验](../../../Network-Career-Lab/07-Trading/02-Labs.md)可延续T1–T4，其旧归档组播链接不作为本教材依赖。

## 2. 离线统计示例

下面nearest-rank程序处理同一测量定义下的整数纳秒样本，不测网络，不接受负值/空表。保存为latency_summary.py：

~~~python
from math import ceil

def summarize_ns(samples):
    if not isinstance(samples, list) or not samples:
        raise ValueError("non-empty sample list required")
    if any(type(value) is not int or value < 0 for value in samples):
        raise ValueError("samples must be non-negative integer nanoseconds")
    ordered = sorted(samples)
    def percentile(p):
        return ordered[ceil(p * len(ordered)) - 1]
    return {"count": len(ordered), "p50_ns": percentile(0.50),
            "p99_ns": percentile(0.99), "p999_ns": percentile(0.999),
            "max_ns": ordered[-1]}

if __name__ == "__main__":
    print(summarize_ns([100, 110, 120, 130, 140, 150, 160, 170, 180, 500]))
~~~

10个样本的P99/P99.9都落在最大值，不能据此描述稳定尾部。超时/缺包需另外统计，不能删掉后只报成功样本。比较方法、单位、样本量与采样窗口一致。

## 3. 实验矩阵

| 阶段 | 内容 | 证据 |
|---|---|---|
| L1 | 序号连续/重复/乱序/缺失与统计反例 | 固定输入、预期和自动断言 |
| L2 | A/B逻辑流、RPF/订阅/消费慢故障 | 树、主机与应用序号 |
| L3 | 队列/IRQ/NUMA与单变量调优 | 原值、资源、尾延迟与丢包 |
| L4 | PTP/硬件时间戳、突发/路径失败 | 能力、时钟误差和采集可信度 |

两VLAN模拟A/B只能证明逻辑，不证明物理独立。普通VM的调度抖动与软件时间戳不足以验证硬件级纳秒结论。

## 4. 综合交付

频道与服务台账、A/B共因图、端到端预算/测量契约、抓包链容量、队列/NIC/应用RCA、时钟依赖、单变量调优报告及开盘Runbook。至少保留一个无改善或失败结果，并解释限制。

结课回答：为什么平均带宽低仍丢包？为什么重复包可能正常？为什么PHC同步不证明应用准确？为什么旁路不必然更快？为什么pcap缺序不等于网络丢包？

[实验报告模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。本次不注入真实网络故障、不改时钟/NIC配置、不创建生产服务连接。
