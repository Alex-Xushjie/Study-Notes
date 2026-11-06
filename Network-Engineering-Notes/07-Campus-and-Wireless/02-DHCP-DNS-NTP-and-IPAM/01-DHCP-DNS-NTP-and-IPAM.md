# DHCP、DNS、NTP与地址台账

[返回本部分学习目录](../Campus-and-Wireless.md)

## 1. 连接后的基础依赖

有线或无线链路成立后，还需正确地址、网关、DNS和时间。DHCP负责相关地址参数，DNS解析名字，NTP同步时钟，IPAM维护分配与归属。它们不是一个服务，单独失败有不同症状。

DHCPv4常见Discover/Offer/Request/ACK，客户端与服务器不同子网时由Relay转送，并通过中继信息选择地址池。看见Discover只证明客户端发起，必须跟踪Offer/ACK、池使用、Relay与返回路径。IPv6的RA、DHCPv6与默认网关机制另查，不能套用v4四步。

| 症状 | 优先区分 |
|---|---|
| 自分配/无地址 | 认证后VLAN、池、Relay、服务器与过滤 |
| 有IP但网关错 | 错池、遗留静态、非授权DHCP |
| IP访问可用域名失败 | DNS配置/转发/记录，不先改RF |
| 认证/证书突然失败 | 真实时间、证书有效期与信任 |

## 2. IPAM与服务台账

记录站点、VLAN/VRF、网段、保留/动态范围、Relay、DNS、NTP、负责人和租期。不要让静态打印机与DHCP池重叠。多地址、多MAC随机化与终端更换需要稳定资产标识，不用MAC单独代表人。

## 3. 验证

从客户端保存实际地址、租约、网关、DNS结果与时间来源，再查服务端日志。NTP配置server不等于已选源同步，偏移与稳定性需观察。认证依赖DNS/时间时，把它们纳入维护和告警。

## 4. 练习

分别注入错误Relay、池耗尽、DNS转发错误和时钟偏差的纸面故障，写不同观察点。不要在生产改时钟或发送伪DHCP。实际实验限定隔离VLAN。

[DHCPv4 RFC2131](https://www.rfc-editor.org/rfc/rfc2131.html)、[NTPv4 RFC5905](https://www.rfc-editor.org/rfc/rfc5905.html)、[混合DNS](../../06-Cloud-and-Hybrid-Networking/06-Hybrid-DNS/01-Hybrid-DNS.md)。
