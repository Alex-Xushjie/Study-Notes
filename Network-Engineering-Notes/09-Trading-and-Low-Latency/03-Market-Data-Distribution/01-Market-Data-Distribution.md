# 行情频道、组播与复制路径

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 业务频道与网络流映射

建立channel→feed/session→S/G/UDP端口→VRF/接口→接收进程映射。一个组可能承载多个业务对象，一个包也可能装多条消息；网络树(S,G)通常不按UDP端口或证券代码独立建立。

发送端、网络、NIC、Socket与Feed Handler分别可能丢弃。行情完整性需应用序号证据，不能只看网口字节数增长。

## 2. 分发拓扑

源或边界到机架分叉应结合容量、故障域和观察点。组播节省分叉前重复传输，却仍需在每个出口复制；一个10Gb/s源流到8个出口，总出口复制量可达80Gb/s，具体按订阅和线速开销计算。

| 位置 | 检查 |
|---|---|
| 接入边界 | 提供方源/组、入流与授权 |
| 路由树 | RPF、Join、IIF/OIF与硬件 |
| 服务器接入 | Snooping、LAG/Hash、出口队列 |
| 主机 | 正确网卡/VRF订阅、NIC/内核/Socket |
| 应用 | 频道/session、消息序列与处理积压 |

## 3. SSM与ASM

优先依据实际交付能力选择，不擅自把提供方ASM地址改成SSM。SSM需要精确源和主机/网络支持，ASM则需相应RP依赖。路径迁移/源切换时维护频道目录和订阅。

## 4. 练习

用自建UDP频道画每跳状态与复制点，分别测试无订阅、错源、RPF错口和接收线程变慢。每个故障都要有不同证据，不把全部gap归交换机。

[组播完整教材](../../02-Multicast/Multicast.md)、[Linux UDP与Socket](../../03-Linux-Networking/05-TCP-UDP-and-Sockets/01-TCP-UDP-and-Sockets.md)。
