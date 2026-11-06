# 容量模型、N-1与离线检查

[返回本部分学习目录](../Engineering-Reference.md)

## 1. 容量模型要写流量切面

端口相加、单流、聚合、加密、检查、包速率、CPU/PCIe与应用有效吞吐有不同约束。先列业务方向和路径，再计算正常、单故障及区域故障下的最坏切面；保留协议开销、突发和增长假设。

下面程序只算并联链路的简化N-1容量，不验证Hash、路径、设备、状态或业务恢复。需求应已包含你选定的开销/余量。保存为capacity_review.py，无第三方依赖：

~~~python
from math import isfinite

def review_capacity(links_mbps, demand_mbps):
    if not isinstance(links_mbps, list) or not links_mbps:
        raise ValueError("provide at least one link")
    values = links_mbps + [demand_mbps]
    if any(type(value) not in (int, float) or not isfinite(value) or value <= 0
           for value in values):
        raise ValueError("capacities and demand must be positive finite numbers")
    normal = sum(links_mbps)
    worst_remaining = normal - max(links_mbps)
    return {"normal_mbps": normal, "worst_n1_mbps": worst_remaining,
            "normal_meets": normal >= demand_mbps,
            "n1_meets": worst_remaining >= demand_mbps}

if __name__ == "__main__":
    print(review_capacity([200, 100], 180))
~~~

预期normal=300、worst_n1=100，正常可容纳180而最坏N-1不满足。只有一条链路时剩余0，应明确不能提供该冗余。

## 2. 不能遗漏的条件

两条线路若共享同一CE，CE故障不属于简单单链路模型；LAG某单流不能用总带宽；ECMP不均和出口队列可能在总量未满时失败。GPU/无线等场景还需特定通信/空口模型。

## 3. 单位与统计

注明十进制/二进制、bit/byte、时段和聚合方法，比较平均/峰值/分位数时保持口径。丢失/超时样本单列，不删除后再宣布延迟改善。

## 4. 练习

检查双100、200+100、单100、零/负/无限值和布尔错误输入。然后将模型扩展为按故障域剩余容量，先写假设和测试，不把并联求和结果直接用于采购。

[WAN容量案例](../../05-WAN-and-SD-WAN/08-Capacity-Failover-and-Operations/01-Capacity-Failover-and-Operations.md)、[Clos容量](../../10-Data-Center-Networking/01-Clos-Underlay-and-ECMP/02-Oversubscription-ECMP-and-N-1.md)。
