# PIM邻接、DR与ASM建树

[返回组播学习目录](../Multicast.md)

## 1. PIM为何叫协议无关

PIM不绑定某一种单播路由协议，可以借助静态、OSPF、IS-IS或BGP等提供的路由信息计算上游，但它依赖有效的RPF信息。PIM不是另一个负责发现全网单播前缀的IGP。

IPv4 PIM使用IP协议号103。Hello等本地控制报文通常到224.0.0.13，Register则是FHR到RP的单播PIM报文。允许224.0.0.13并不等于允许全部PIM过程。

| 角色/事件 | 作用 | 常见误区 |
|---|---|---|
| PIM邻居 | 同链路控制协议关系 | 邻居UP不证明数据树正确 |
| DR | 多路由器LAN上的指定角色，含源注册等职责 | 不等于IGMP Querier或VRRP Master |
| Join/Prune | 建立/撤销上游接收需求 | 不是向源发UDP订阅 |
| Assert | 多路由器共享LAN上协调重复转发 | 不等于DR重新选举 |

支持DR Priority时按更高优先级优先，再比较地址；兼容旧邻居等情况以协议规则和设备状态为准。DR变化的影响要分别看源LAN和接收LAN，不能仅从虚拟网关当前Master推断。

## 2. ASM的三条关键方向

接收者的Join沿RPF(RP)形成共享树；FHR把源数据封装成Register发往RP；RP发现源后可以沿RPF(S)Join源树。必须分别核对，不是只检查一条“去RP的路”。

当RP已能通过原生路径接收数据，或不需要该注册流时，可以发送Register-Stop控制注册过程。看到Register-Stop不一定是错误，也不等于源业务停止。

## 3. 冷启动过程

先让接收者加入G，记录LHR共享树和朝RP的上游。再启动源：记录FHR是否收到真实源包、Register是否到达RP、RP是否产生源相关状态、原生数据如何抵达接收者。若随后SPT切换，记录切换前后路径。

源先启动时，再等待接收者加入并重复观察。两种顺序均成功才能覆盖冷启动需求。只测试“已经运行很久的业务继续收包”，会漏掉RP源发现问题。

## 4. 模式边界

Sparse Mode按需求建树；Dense Mode使用不同的泛洪/剪枝机制，不能把ASM理解成Dense Mode。BIDIR-PIM使用双向共享树与DF机制，适合不同流量模型，不按普通PIM-SM的Register和SPT切换过程运作。本教材主线是PIM-SM与SSM，BIDIR作为识别范围。

[规范：RFC7761](https://www.rfc-editor.org/rfc/rfc7761.html)、[BIDIR-PIM：RFC5015](https://www.rfc-editor.org/rfc/rfc5015.html)。
