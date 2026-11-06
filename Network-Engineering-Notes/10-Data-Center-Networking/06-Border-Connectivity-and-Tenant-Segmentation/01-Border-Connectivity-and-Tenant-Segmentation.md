# Border Leaf、租户分段与共享服务

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 出口是路由与安全边界

Border Leaf连接WAN、云、防火墙、传统网络或外部服务。定义租户VRF、L3VNI、对外前缀、默认路由、RT与访问策略。Underlay不应成为租户绕行通道，租户隔离不能只靠VNI编号。

| 需求 | 设计对象 |
|---|---|
| 租户外出 | VRF路由、Border/防火墙、NAT与回程 |
| 共享DNS/认证 | 最小前缀泄漏、检查与双向许可 |
| 访问Internet | 默认来源、出口身份与N-1容量 |
| 混合云 | 接入/云路由、地址与私有DNS |
| 传统VLAN | 明确L2延伸范围、防环与网关 |

## 2. RT与安全

导入RT让路由进入目标上下文，不提供逐应用授权。多个租户访问共享服务时防止通过共享域变相Transit。重叠地址需要转换/代理/重编号，不能把相同前缀互相导入期待自动消歧。

## 3. 服务插入

流量穿过有状态设备时确保双向经过预期状态域。对称IRB不是防火墙对称路径保证，ECMP与主备Border也可能使回程变化。记录每层路由和NAT前后五元组。

## 4. 练习

Prod/Dev仅可访问Shared与外部指定服务，分别设计允许、拒绝和共享域不许Transit。验证单Border/防火墙失败下隔离与路径不改变初衷。

[VRF与路由泄漏](../../01-Routing-and-Switching/07-VRF-and-Route-Leaking/01-VRF-and-Route-Leaking.md)、[云服务链](../../06-Cloud-and-Hybrid-Networking/04-Private-Access-Egress-and-Inspection/03-Stateful-Inspection-and-Symmetric-Paths.md)。
