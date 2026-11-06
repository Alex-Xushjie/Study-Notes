# EVPN路由类型、RD/RT与安装

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. EVPN不只是另一种MAC表

BGP EVPN交换业务端点与连接信息，使用相应地址族。RD区分路由，RT控制导入/导出，VNI标识数据面上下文；它们用途不同，即使某平台自动按VNI生成相应值，也不能混同。

| Route Type | 学习用途 |
|---|---|
| 1 Ethernet Auto-Discovery | 多归属相关可达/撤销等信息 |
| 2 MAC/IP Advertisement | MAC及可选IP绑定等信息 |
| 3 IMET | 相应域的BUM分发成员信息 |
| 4 Ethernet Segment | 多归属ES发现/选举相关信息 |
| 5 IP Prefix | IP前缀可达，区别于单个主机MAC/IP |

本表是排障索引，不是完整状态机。多归属、IRB和不同厂商模型会带来更多属性和支持限制。

## 2. 收到到转发

邻居Established→收到EVPN路由→RT/策略匹配→下一跳/VNI可解析→安装到相应MAC/VRF/FIB→实际封装转发。每一步单独可失败。RR可以仅分发控制路由而不充当业务VTEP，Underlay和Overlay下一跳策略需明确。

## 3. 规模与安全

MAC/IP、前缀、VNI/VRF、邻居、复制与硬件表均有规模。控制面条数不等于硬件已安装数；导入过宽RT可能破坏隔离并放大资源。

## 4. 练习

跟踪一个本地主机MAC在远端从Type2到FDB的证据，再跟踪一个外部前缀Type5到VRF。错RT、不可达VTEP和缺VNI分别形成什么结果，不能只截一张show bgp证明成功。

[EVPN基础RFC7432](https://www.rfc-editor.org/rfc/rfc7432.html)、[Type5 RFC9136](https://www.rfc-editor.org/rfc/rfc9136.html)、[FRR文档](https://docs.frrouting.org/en/latest/evpn.html)。
