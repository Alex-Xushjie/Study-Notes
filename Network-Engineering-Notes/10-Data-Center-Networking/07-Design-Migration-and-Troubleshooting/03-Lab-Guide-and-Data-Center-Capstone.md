# 数据中心实验与综合设计

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 分档环境

离线先完成地址/ASN/VNI/RT与业务路径；Linux/FRR验证部分Underlay/EVPN逻辑；合法NOS/硬件验证多归属、硬件安装、性能与故障。软件可达不能代替ASIC容量、速率转换或真实HA。

已有[数据中心实验](../../../Network-Career-Lab/05-Data-Center/02-Labs.md)可作为配套，运行前按其中实际支持范围核对，不把后续扩展目标当已实现。

## 2. 最小拓扑

2Spine/2Leaf，各Leaf接一台测试主机；先完成端点IP可达，再一个L2VNI，随后同租户两子网IRB，最后Border和租户隔离。Loopback、链路、主机网段与VNI均使用隔离实验规划。

| 阶段 | 验证 |
|---|---|
| D1 Underlay | 邻接、VTEP路由、ECMP、MTU和单链路失败 |
| D2 L2 Overlay | Type2/3、FDB/BUM、首包与大包 |
| D3 IRB | VRF/L3VNI、Type2/5及跨子网返回 |
| D4 边界 | 外部前缀、防环、共享服务与拒绝 |
| D5 多归属 | 仅在支持平台验证ES/DF/LACP与故障 |

## 3. 只读观察

FRR示例在vtysh，需前置BGP/EVPN配置；参数按版本帮助确认：

~~~text
show bgp summary
show bgp l2vpn evpn
show evpn vni
~~~

Linux数据面对象另用ip/bridge等工具核查，不把控制面输出当已完成所有对象和硬件。命令不存在先查版本/功能，不能等同网络失败。

## 4. 综合交付

为两租户、Shared、双Border与N-1设计容量、RT/前缀来源、服务链和故障矩阵。至少保留五类RCA与一个迁移回退案例，数据/图中标“推演/软件/设备实测”。

结课解释为什么Type2已收到仍不通、为什么Anycast Gateway不保证安全对称、为什么DF不是所有单播主设备、为什么1:1也会拥塞。

[FRR EVPN官方文档](https://docs.frrouting.org/en/latest/evpn.html)、[实验报告模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。本次未运行Fabric或设备命令。
