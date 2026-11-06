# MAC移动、重复地址与控制面排障

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 移动不是所有MAC变化

VM迁移/链路切换可能让MAC出现在新VTEP；二层环路、重复配置或伪造也可能反复通告。EVPN通过相关移动信息协调位置，但检测阈值、重复/冻结保护与恢复依实现而异。不能见到MAC flap就立即关闭保护。

## 2. 分层证据

| 层次 | 查什么 |
|---|---|
| 本地接入 | Host真实连接位置、VLAN、LACP与虚拟交换 |
| EVPN | Type2来源、序列/移动、RD/RT和选优 |
| Underlay | VTEP下一跳、路由和故障变化 |
| 实际表 | 本地/远端FDB、ARP/ND和硬件 |
| 业务 | 首包、持续流、双向、重复/丢包 |

## 3. IP与MAC分别核对

相同IP对应两个MAC、同MAC被两台主机使用或多归属同一ES是不同情形。多归属合法广告不能按普通单归属重复简单判断。ARP抑制缓存也可能让位置变化只影响部分业务。

## 4. 路由反射与策略

部分路由缺失时对比发送、接收、选中、导入和安装。RR策略/RT约束、地址族能力、Next-Hop、AS_PATH与最大路由保护都可能影响。控制面正常但硬件资源不足也能黑洞，查看下发与丢弃原因。

## 5. 练习

在隔离拓扑完成Host迁移、故意重复IP与错误VNI映射，保存正常和异常时间线。恢复后验证旧位置撤销和业务，不只看邻居稳定。

[EVPN协议背景](https://www.rfc-editor.org/rfc/rfc7432.html)、[自动化期望/事实模型](../../04-Network-Automation/04-Inventory-Source-of-Truth-and-Data-Models/01-Inventory-Source-of-Truth-and-Data-Models.md)。
