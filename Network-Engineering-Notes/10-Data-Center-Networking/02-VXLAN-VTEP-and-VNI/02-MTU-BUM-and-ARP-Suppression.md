# MTU、BUM与ARP抑制

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 计算封装预算

假设内层IP为1500字节、内层Ethernet首部14、VXLAN8、UDP8、外层IPv4首部20，则外层IP长度需1550字节。此公式未计外层Ethernet/FCS，也未计VLAN标签或其他封装；外层IPv6基首部40时对应1570。平台MTU命令的层次口径必须核对。

只ping小Loopback包不能证明业务MTU。端点、所有路径、封装/解封和故障备用都需按相同长度验证，关注ICMP反馈、分片与硬件丢弃。

## 2. BUM复制

Broadcast、Unknown Unicast、Multicast在逻辑域内需要相应复制，常见Ingress Replication或Underlay组播等方式。复制列表、远端成员与硬件资源影响容量；不是EVPN一开启就没有泛洪。

## 3. ARP/ND抑制

控制面掌握有效MAC/IP绑定时，可由适当节点代理回答以减少泛洪。绑定缺失、迁移、静默主机、重复IP和老化都需正确处理。抑制功能不能替代租户安全，不是所有ARP都应被无条件代答。

| 症状 | 区分 |
|---|---|
| 已知MAC单播通，首包失败 | BUM/ARP、绑定与复制列表 |
| 小包通大包丢 | 路径MTU/封装与错误反馈 |
| 部分远端收不到广播 | VNI/Type3、复制与过滤 |
| 迁移后到旧位置 | MAC/IP更新、移动与老化 |

## 4. 实验

验证冷启动首包、清单/绑定重建、大包与Host迁移，记录MAC、ARP、EVPN和实际数据。只在隔离实例清状态，不在现网全局clear。

[VXLAN封装](https://www.rfc-editor.org/rfc/rfc7348.html)、[FRR EVPN实现](https://docs.frrouting.org/en/latest/evpn.html)。
