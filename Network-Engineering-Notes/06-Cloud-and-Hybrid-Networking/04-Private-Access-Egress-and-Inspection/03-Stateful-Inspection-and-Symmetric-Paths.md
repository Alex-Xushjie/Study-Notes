# 集中检查、对称路径与NVA高可用

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 一条会话穿过哪些状态点

防火墙、NAT、LB、代理和隧道端点可能保存状态。正向经过A、回程经过不共享状态的B，可能被丢弃。云路由ECMP或故障倒换能让IP继续可达，却不保证这些状态保持。

先记录五元组的每次变化与状态所有者。NAT是否发生、LB是否保留源、代理是否终结连接，都会改变“同一条流”的观察方法。

## 2. 中央检查的依赖

AWS可能涉及TGW Appliance Mode、Gateway Load Balancer或Network Firewall等不同方案；Azure可能涉及UDR、Azure Firewall或厂商NVA。它们有各自路径与健康机制，不能以一个通用“防火墙双机”图代替设计。

| 条件 | 必须验证 |
|---|---|
| 正常 | 两方向通过预期状态域，规则命中可追踪 |
| 单AZ/节点失败 | 新会话能重建，旧会话影响明确 |
| 检查服务失败 | 按预定Fail-open/close处理 |
| 扩缩容 | Hash/连接分配和排空是否可控 |
| 备路径 | 没有绕过检查或误放宽隔离 |

## 3. 健康不只看VM存活

NVA的云网卡设置、OS转发、许可证、加密、策略加载与后端服务都可能独立失败。健康探测要尽量代表转发功能；仅TCP端口可连可能漏掉策略进程故障。

HA可能同步配置但不完整同步会话。操作系统重启、云故障迁移和厂商HA切换是不同事件，要分别说明恢复机制。

## 4. 案例与反证

App访问数据库超时，路由和NSG均允许。候选A为返回绕过防火墙，B为数据库未监听。用数据库主机抓包看SYN是否到、是否回SYN-ACK，再核对两个方向有效路由与防火墙日志。只有源端反复SYN不能区分两者。

## 5. 交付

提供服务链图、双向查表、NAT日志对应、失败矩阵与会话影响。不需要检查的流明确列为例外并说明依据；不要以性能优化为由默默绕过安全边界。

[AWS TGW机制与Appliance Mode](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html)、[Azure集中Hub设计](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke)。
