# BGP属性与策略：从意图表到可验证配置

[路由交换学习目录](../Routing-and-Switching.md)

## 1. 先说控制谁的哪一方向

Import影响本地接受与选择，export决定向对端发布哪些信息。企业把A学来的路由设高local-pref，主要表示自己倾向把相应出站流量交A，不代表远端回包也经A。

| 属性/机制 | 主要作用 | 边界 |
|---|---|---|
| Local Preference | 表达本AS内部偏好 | 不作为普通eBGP属性向所有AS传递 |
| AS_PATH | 记录AS传播路径并参与防环/选择 | prepend不覆盖对方所有更高策略 |
| ORIGIN | 路由起源类别属性 | 不是RPKI origin授权验证 |
| MED | 表达相应入口偏好 | 默认比较范围和配置条件要核对 |
| NEXT_HOP | 指出转发解析对象 | 地址存在不等于可达 |
| Community | 携带约定的策略标记 | 只有接收方识别并执行才有相应效果 |

标准、大型、扩展Community有不同编码和用途，不把所有community都当RT。Weight等本地属性属于实现/本地选择能力，不是跨厂商通用BGP传播属性。

## 2. 不背一张脱离平台的完整口诀

先排除不具资格/下一跳不可达路径，再按实际实现比较。Local-pref、起源、AS长度、ORIGIN、MED、eBGP/iBGP、内部到下一跳代价及平局规则等可能参与；具体顺序、可选设置和多路径条件要查NOS。

例题在其他条件都不构成先前差异时：A local-pref200、AS长度4；B local-pref100、AS长度2，A可优先。把两者local-pref改相等后，短AS路径可能胜出。MED不是不管来自哪个AS都简单全球取最小。

## 3. Prefix-list表达的集合

203.0.113.0/24单独permit通常只匹配该精确前缀；ge/le可约束覆盖范围内更具体长度，按平台语法解释。允许10.0.0.0/8 le 32会覆盖大量更具体地址，不等于只允许10/8这一条。

路由过滤匹配的是被公告前缀，不是正在转发的每个数据包；不要把prefix-list与接口ACL概念混为一体。

## 4. FRR教学例：白名单与主出口

假设CE AS65010用192.0.2.1/30连接A AS65001的192.0.2.2；实验自有前缀203.0.113.0/24在RIB，A只应给198.51.100.0/24。地址、进程和回程已另行准备，在vtysh配置模式阅读以下示例：

~~~text
ip prefix-list FROM-A seq 10 permit 198.51.100.0/24
ip prefix-list OWN seq 10 permit 203.0.113.0/24
route-map A-IN permit 10
 match ip address prefix-list FROM-A
 set local-preference 200
router bgp 65010
 bgp router-id 10.255.0.1
 neighbor 192.0.2.2 remote-as 65001
 address-family ipv4 unicast
  network 203.0.113.0/24
  neighbor 192.0.2.2 route-map A-IN in
  neighbor 192.0.2.2 prefix-list OWN out
 exit-address-family
~~~

seq是规则序列，permit是允许，match选择前缀，set修改属性，in/out给出相对本设备的方向。此处没有最终permit-any，未匹配对象按相应策略缺省处理；须核对route-map、prefix-list组合语义。

这是单侧教学片段，不会自动配置ISP和Linux接口，也不证明公网授权。完整三节点思路见[边界实验E1/E2](../../../Network-Career-Lab/04-Internet-Edge/02-Labs.md)。

## 5. 修改策略后怎样验证

保存候选diff、前后目标前缀属性和实际发布集合，再按平台支持使用Route Refresh/soft方式重新处理。入方向修改未必自动重处理历史结果，hard reset会影响会话和业务，不能作为默认第一步。

确认local-pref已进入目标路径，再查best、RIB/FIB与实际出站；export白名单还需在接收侧确认。只有配置文本正确不算验收。

## 6. 常见陷阱与自测

route-map追加一条permit-any可能扩大授权范围；修改Community但对端不支持不会产生预期选路；prepend后入站不变可能是远端策略优先，不应无限加长路径。

自测：ORIGIN的IGP标记是否证明路由来自OSPF？答：不是。local-pref能直接命令远端回包走A吗？答：不能。Community收到是否等于执行？答：不是。

交付意图→匹配集合→属性→传播→实际路径的五层对应表。继续[iBGP与RR](03-iBGP-Route-Reflectors-and-Scale.md)。
