# 专线与VPN备份、混合迁移边界

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 接入冗余按故障域设计

双端口、双设备、双运营商、双接入地点、双区域分别覆盖不同故障。两条线路共用CE、入楼管道、机房电源或云接入位置时，仍可能同时失败。要求供应商提供可核对的路径与责任边界。

VPN备份成本较低但可能容量更小、时延更不稳定。它能否覆盖全部主线业务，取决于业务分类与N-1设计，不是建立隧道就完成备份。

## 2. 端到端切换

测量包含故障检测、BGP/云路由更新、状态设备影响、DNS/应用重连。BGP恢复时间不是业务恢复时间。接口UP但上游黑洞、线路Brownout、单接入点失效需分别覆盖。

测试主转备和恢复切回，明确旧会话、新连接、共享服务和私有端点表现。对备线实施业务降级，防止大规模备份占满救援路径。

## 3. 迁移并行期

搬迁到云不只是改IP：DNS、身份、NTP、证书、日志、备份和依赖服务需要同步规划。新旧地址并存时列出会话与返回路由，不让所有边界无限制双向重分发。

灰度一个网段/一组用户，保留可回退服务与DNS策略。DNS TTL到期不保证所有客户端立即更新，连接池和应用缓存也可能延长旧路径使用。

## 4. MTU与加密

专线、VPN、SD-WAN Overlay和安全服务叠加可能减少可用MTU。小ping成功不排除大包黑洞。云专用连接默认加密支持按产品核对；MACsec、IPsec与TLS保护范围不同。

## 5. 设计交付

给出正常/单线路/单CE/整接入点/区域失效的路径与容量表，列未覆盖的共享依赖。提交迁移分批、验证、回退和退役条件。

[AWS DX韧性](https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html)、[Azure ER韧性设计](https://learn.microsoft.com/en-us/azure/expressroute/design-architecture-for-resiliency)。隧道细节与MTU继续读[WAN教材](../../05-WAN-and-SD-WAN/WAN-and-SD-WAN.md)。
