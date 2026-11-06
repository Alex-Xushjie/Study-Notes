# 包、消息、会话与解析完整性

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 三个层次

以太帧/IP包、传输报文、业务消息有不同边界。一个UDP报文可包含多条消息，协议序号可能表示首消息号或包号，Heartbeat/结束标记也可能有专门语义。不能把tcpdump包计数差直接当丢失消息数。

Nasdaq MoldUDP64与ITCH可作为传输封装/业务消息分层的例子；其他提供方可能按频道或报文定义不同序列空间。实现前固定协议修订和授权文档，不能用一个通用seq++解析所有行情。

## 2. 解析器检查

检查包/消息长度、字段编码、网络字节序、消息数量与边界，不在长度不足时继续读。Session/频道隔离，重启/日切和重放按协议转换状态。未知消息类型要有版本策略，不能悄悄当正常空消息。

| 数据 | 需要定义 |
|---|---|
| session | 唯一性、重置与重连规则 |
| sequence | 包/消息单位、递增与特殊值 |
| timestamp | 提供方事件时刻还是本地接收，时间尺度 |
| message_count | 是否包含控制报文，如何验证长度 |
| recovery | 重传/快照和实时流的衔接 |

## 3. 证据保留

记录解析失败、未知类型、会话变化、序号gap/重复/乱序及最后有效点。不要全量TRACE打印每条消息来监控高速流，会增加CPU/磁盘争用；选择聚合计数、有限采样和触发窗口。

## 4. 练习

用自建固定格式数据，构造截断、长度错误、多个消息、session切换与重复。教学协议必须标自定义，不能写成真实ITCH兼容实现。本部分不实现交易所生产解码器。

[MoldUDP64原始规范](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf)、[ITCH接口](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification_5.0.pdf)。
