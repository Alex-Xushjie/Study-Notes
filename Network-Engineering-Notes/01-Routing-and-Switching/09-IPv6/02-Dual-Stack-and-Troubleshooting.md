# 双栈选路、PMTU与IPv6排错

[路由交换学习目录](../Routing-and-Switching.md)

## 1. 双栈是两套路径与策略

一个域名有A和AAAA，客户端可能按地址选择和Happy Eyeballs等机制尝试不同路径。IPv4成功而域名慢，不能立即认定DNS慢；可能IPv6连接失败后回退。[RFC8305](https://www.rfc-editor.org/rfc/rfc8305.html)

要记录实际目标地址族，分别验证IPv4/IPv6路由、安全、负载均衡、服务监听和回程。自动回退可能掩盖长期IPv6故障，也可能让不同客户端体验不一致。

## 2. OSPFv3与BGP地址族

OSPFv3保留链路状态、区域等思想，但邻接、LSA与地址表达有区别。它还存在地址族扩展，不应把版本号简单当只支持一种地址族。BGP会话可承载多个AFI/SAFI，IPv4 Established不证明IPv6路径已交换。

FRR或NOS查询时明确IPv6地址族，最终在IPv6 RIB/FIB核对，不能只看IPv4表。[OSPFv3 RFC5340](https://www.rfc-editor.org/rfc/rfc5340.html)

## 3. IPv6 PMTU

IPv6路由器不替源端分片，Packet Too Big等反馈对路径MTU学习重要。隧道减少内层预算，小包通/大数据挂的推理与IPv4类似，但不能照搬IPv4 DF和中间分片规则。[RFC8201](https://www.rfc-editor.org/rfc/rfc8201.html)

检查封装、反馈、源端行为和实际包长，避免只改TCP MSS而忽略UDP或其他业务。

## 4. 案例A：有地址，无互联网

先查地址是否可用、默认路由是否存在、路由器生命周期、链路本地邻居，再看上游。DNS与服务独立验证。有global格式地址不意味着已被运营商路由。

## 5. 案例B：命令行IPv4快，浏览器慢

比较A/AAAA返回、实际连接、IPv6 SYN/回应、证书与应用。curl等可限定地址族做区分，但不把强制IPv4作为所有用户的最终修复。

## 6. 案例C：部分源地址访问失败

同接口多个地址、临时地址、源策略与上游过滤可能造成差异。记录实际source、生命周期和返回前缀，不只检查你期望使用的稳定地址。

## 7. 作业

提交双栈正反路径、地址来源、DNS及允许/拒绝策略矩阵，验证IPv6正常、IPv6单独失败和恢复。抓包位置与时钟边界按Linux观测章节记录。未具备IPv6实验时标记推演，不虚构邻居输出。
