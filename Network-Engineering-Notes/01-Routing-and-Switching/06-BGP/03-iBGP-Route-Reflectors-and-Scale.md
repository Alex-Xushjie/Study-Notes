# iBGP、Route Reflector与规模设计

[路由交换学习目录](../Routing-and-Switching.md)

## 1. iBGP为什么需要额外传播设计

普通iBGP学来的路由通常不会再按普通iBGP关系转给另一iBGP邻居，因此小网络可使用全互联，规模大时常采用Route Reflector等机制。全互联会话数量为n(n-1)/2，20节点是190对，100节点是4950对，不考虑多地址族等额外维度。

RR减少会话关系，不替代Underlay，也不要求业务数据经RR转发。控制面和数据面必须分开画。[RFC4456](https://www.rfc-editor.org/rfc/rfc4456.html)

## 2. 反射关系要按来源解释

| RR收到来源 | 典型可反射方向（仍受策略等条件限制） |
|---|---|
| Client | 其他Client及Non-client |
| Non-client iBGP | Client |
| eBGP | 向相应iBGP邻居正常传播 |

不要把RR理解成所有邻居之间无条件再广播。Originator ID、Cluster List等帮助防环，但不能替代正确client/cluster规划。冗余RR需要考虑独立故障域、客户端连接与路径一致性，不是简单复制router-id。

## 3. 下一跳为什么仍可能失效

iBGP传播经常保留原始下一跳。Client收到外部路由，但不认识外部下一跳时可能不能采用。可以通过规划IGP可达、边界next-hop-self或其他合法方案解决，具体放在哪里受拓扑和语义影响。

不能为了让表好看把所有RR的next-hop强改为自己：RR如果不在数据路径或不具相应转发能力，反而可能制造黑洞。部分反射场景是否改变NH也要查具体配置和版本。

## 4. Path hiding与路径视角

RR常按自身视角选择并传播最佳路径，客户端不一定看到所有候选，也不一定得到以自己位置最优的出口。客户IGP距离与RR不同，这种差异不能只靠增加RR数量自动消失。

Add-Path允许在同前缀之外用Path Identifier区分多个公告，但需协商并设计传播集合、资源与客户端选择。它不直接意味着业务逐包多路径。[RFC7911](https://www.rfc-editor.org/rfc/rfc7911.html)

## 5. 规模不只有会话数

要预算前缀数、每前缀路径数、策略计算、刷新、内存、更新突发、下装速率和监控。全表/多路径/原始副本同时开启会增加成本；不要用单邻居实验的CPU推断全网规模。

GR在协商条件下可保留相应旧路由，目标是减小重启影响，但转发状态实际未保留或路径已经坏时，旧状态可能延长黑洞。BFD与GR交互需测试，不能同时开后宣称双重无损。[RFC4724](https://www.rfc-editor.org/rfc/rfc4724.html)

## 6. 案例与验收

Client1有路由、Client2无：先比较地址族、client角色、RR最佳/发布、策略、Originator/Cluster与Client2下一跳。RR邻居UP不足以证明传播。

交付2个边界、2个RR和至少2个Client的控制/数据路径图。测试单RR失效、外部下一跳失效、重启和恢复，分别记录传播与业务。多机VM只验证逻辑，不证明生产规模。继续[BGP综合排错](04-BGP-Troubleshooting-and-Changes.md)。
