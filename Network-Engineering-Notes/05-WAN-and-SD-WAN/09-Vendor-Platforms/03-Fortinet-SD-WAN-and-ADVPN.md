# Fortinet的Member、SLA、Rule与ADVPN

[返回WAN与SD-WAN目录](../WAN-and-SD-WAN.md)

## 1. 四类对象先分开

Member是加入SD-WAN的接口/隧道等成员，Zone把相关成员组织成策略引用边界，Performance SLA测量特定路径质量，Rule/Service按匹配与策略选择出口。仅把两条WAN加入Member，不意味着业务已按应用质量选择，也不替代路由、NAT与防火墙策略。

FortiGate集成安全与转发，FortiManager可集中管理，但其控制体系不能直接照搬另一家平台的Controller/OMP概念。底层IPsec、BGP与SD-WAN选路应分别诊断。

## 2. Alive不等于满足业务SLA

Health-check可能仍能探测目标，但测得质量超过某SLA目标。同一Member可对不同业务呈现不同可用性；还要区分路由是否有效、规则候选是否满足以及会话是否已选定出口。

未匹配显式规则时存在Implicit Rule，其行为与负载算法、有效路由及版本设置有关，不是防火墙的“隐式拒绝”。若想阻断某业务，必须通过相应安全/策略机制明确实现并验证。

## 3. 只读观察与版本区别

在正确VDOM/上下文中核对状态，以下为FortiOS 7.6系列常见命令。service4/service6是新版拆分后的形式，旧资料中的service不能不加核对直接复制。

~~~text
get system status
get router info routing-table all
diagnose sys sdwan health-check
diagnose sys sdwan service4
diagnose sys sdwan service6
~~~

关联Member序号、健康目标、SLA位图、规则ID和选中出口；再查具体会话、IPsec收发、策略及SNAT。输出中一个selected只在相应规则/候选语境有效，不代表全设备所有业务都走同一路。

## 4. ADVPN与Shortcut

ADVPN可在Hub-Spoke基础上按需形成Spoke之间的直接隧道，减少绕Hub。初始流量、Shortcut建立、路由下一跳与SD-WAN选择、老化后的回退，需要分阶段验证。

ADVPN不同代际/版本的发现和选路设计有差异。Shortcut存在但业务仍经Hub，可能是路由、规则、SLA、现有会话或策略条件；不应立即反复重建IPsec。两个Spoke均在CGNAT后时，也不能预先保证可直连。

## 5. 实验

先双WAN本地Internet出口，再双Hub Overlay，最后测试Spoke直连。每阶段覆盖显式命中、未命中兜底、Out-of-SLA、Hard Down与恢复。比较新会话和旧会话，记录实际版本及是否启用ADVPN 2.0等能力。

[Performance SLA](https://docs.fortinet.com/document/fortigate/7.6.0/administration-guide/584396/performance-sla)、[规则与Implicit行为](https://docs.fortinet.com/document/fortigate/7.6.6/administration-guide/716691/sd-wan-rules)、[7.6.6诊断命令](https://docs.fortinet.com/document/fortigate/7.6.6/cli-reference/235530229/diagnose-sys)、[ADVPN与Shortcut](https://docs.fortinet.com/document/fortigate/7.6.6/administration-guide/985659/advpn-and-shortcut-paths)。
