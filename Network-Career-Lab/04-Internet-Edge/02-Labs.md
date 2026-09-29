# Internet Edge 实验

## E1 最小三节点 FRR

三台专用 Linux VM，安装 FRR 并启用 zebra/bgpd，记录 `show version`。接口地址先用 Linux `ip addr` 配好，开启相关实验节点的 IPv4 forwarding；FRR 持久化方式按发行版包说明。命令参考 [FRR BGP 文档](https://docs.frrouting.org/en/latest/bgp.html)，只读本实验涉及的邻居、prefix-list 和 route-map 部分。

```text
ISP1 AS65001 .2 ---- 192.0.2.0/30 ---- .1 CE AS65000
ISP2 AS65002 .6 ---- 192.0.2.4/30 ---- .5 CE
CE loopback: 203.0.113.1/24（模拟自有前缀）
两 ISP 均用 Null0 路由起源 198.51.100.0/24（仅观察控制面）
```

CE 的教学配置，在 `vtysh` 配置模式输入；先确认本地 203.0.113.0/24 确实在 RIB：

```text
ip prefix-list OWN seq 10 permit 203.0.113.0/24
ip prefix-list ISP-IN seq 10 permit 198.51.100.0/24
route-map ISP1-IN permit 10
 match ip address prefix-list ISP-IN
 set local-preference 200
route-map ISP2-IN permit 10
 match ip address prefix-list ISP-IN
 set local-preference 100
router bgp 65000
 bgp router-id 10.255.0.1
 neighbor 192.0.2.2 remote-as 65001
 neighbor 192.0.2.6 remote-as 65002
 address-family ipv4 unicast
  network 203.0.113.0/24
  neighbor 192.0.2.2 route-map ISP1-IN in
  neighbor 192.0.2.6 route-map ISP2-IN in
  neighbor 192.0.2.2 prefix-list OWN out
  neighbor 192.0.2.6 prefix-list OWN out
 exit-address-family
```

ISP1 示例，ISP2 对应改 ASN、邻居和 router-id：

```text
ip route 198.51.100.0/24 Null0
ip prefix-list FROM-CE seq 10 permit 203.0.113.0/24
ip prefix-list TO-CE seq 10 permit 198.51.100.0/24
router bgp 65001
 bgp router-id 10.255.0.2
 neighbor 192.0.2.1 remote-as 65000
 address-family ipv4 unicast
  network 198.51.100.0/24
  neighbor 192.0.2.1 prefix-list FROM-CE in
  neighbor 192.0.2.1 prefix-list TO-CE out
 exit-address-family
```

检查 `show bgp ipv4 unicast summary`、`show bgp ipv4 unicast 198.51.100.0/24`、`show ip route`。预期：CE 接收两条路径，优选 ISP1；两 ISP 仅收到 CE 自有 /24。由于目标路由是 Null0，此步骤不以 ping 成功验收。

故障：shutdown ISP1 邻居，记录选路变更时间及 ISP2 路径是否进 FIB；恢复后记录回切。需要测业务丢包时，在 ISP 后增加真实测试主机与回程路由，不把 BGP 更新耗时当作业务恢复耗时。

## E2 属性与路由泄漏

1. 在 CE 将 ISP2 local-pref 改为 250，按平台支持进行 soft inbound refresh，再验证出口变更。
2. 给 ISP1 出方向的自有前缀增加 AS-path prepend；在 ISP1 看收到的路径。由于两个 ISP 没有共同远端，本拓扑只能验证属性传播，不能证明全网入站改走 ISP2。
3. 新建一条模拟从 ISP 收到的路由，检查 CE 的 outbound prefix-list 仍不允许转发到另一 ISP。
4. 设置与实验规模相符的 max-prefix，再故意注入更多允许的前缀；记录警告/会话关闭/恢复行为，不把平台差异写成通用结论。

验收：给出修改前后 BGP 属性、RIB/FIB、出口策略与回退 diff。每次只修改一个变量。

## E3 路由安全和 DDoS 桌面演练

ROV 手算：分别判断本阶段教材的 /24、错误 ASN、/25、无覆盖 ROA 四种输入。再构造两条覆盖 ROA，其中一条允许当前公告，解释为什么仍可 Valid。扩展实验需要真实 validator/测试数据源和支持 RPKI 的 FRR 构建；未部署时只标记纸面推演。

RTBH 演练：假设上游接受指定黑洞 community，只允许实验授权 /32。写申请→审核目标→公告→验证→限时撤销→恢复的流程。回答误把整个 /24 黑洞后如何发现和恢复。FlowSpec 演练匹配“目的前缀 + UDP + 指定目的端口”，解释规则过宽会影响哪些合法流量；不向真实 ISP 发送测试公告。

完成一页 Runbook：告警证据、影响范围、控制面入口、审批责任、命令模板、最大持续时间、回滚条件和业务验证。不要把“收到黑洞 community”当作对方一定执行的证据。
