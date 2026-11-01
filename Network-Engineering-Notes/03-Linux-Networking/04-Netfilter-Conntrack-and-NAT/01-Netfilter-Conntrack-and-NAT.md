# Netfilter、nftables、连接跟踪与NAT

[Linux学习目录](../Linux-Networking.md)

## 1. Linux防火墙由哪些组件组成

你熟悉设备上的安全策略，但Linux的命令、内核机制和管理软件不是同一件事。

| 名称 | 职责 | 先避免的误解 |
|---|---|---|
| Netfilter | 内核网络路径上的报文处理框架 | 不是一条查看命令 |
| nftables | 配置规则及内核执行相关机制的一套体系 | 不等于所有链已默认存在 |
| nft | nftables的命令行工具 | 是工具，不是每包启动的程序 |
| conntrack | 为相应流跟踪状态，供过滤、NAT等使用 | UDP也可有跟踪记录，不只TCP |
| iptables | 另一套规则工具/接口，可能使用legacy或nft后端 | 与nft显示的内容不一定互不相关 |
| UFW、firewalld | 更高层管理工具 | 手工规则可能与它们管理的规则相互影响 |

第一遍先学“包经过哪个位置、谁的规则在那里执行”。不要看到工具名多就认为系统有几个互不相关的防火墙。

## 2. 三条基本路径

### 外部送给Linux本机

~~~text
网卡收到 → prerouting → 路由判断目的为本机 → input → 本机应用
~~~

### 外部经过Linux转发到另一主机

~~~text
网卡收到 → prerouting → 路由判断需要转发 → forward → postrouting → 出口
~~~

### Linux本机应用发出

~~~text
应用 → 相应路由处理 → output → postrouting → 出口
~~~

hook是处理挂点，可先理解为“包行经时可以挂规则的位置”。prerouting是入站后、路由前；input面向本机接收；forward面向转发；output面向本机发出；postrouting靠近出站。实际还有优先级、重查、bridge和特殊路径，这三图仅用于第一遍定位。

本机HTTP不可达与Linux路由器不转发，可能检查完全不同的hook。允许input不能替代forward，也不能替代开启相应IP转发能力。

## 3. Table、Chain、Rule逐层是什么

Table是规则容器，Chain是规则链，Rule是具体匹配与动作。nftables还用family区分处理范围，常见ip针对IPv4，ip6针对IPv6，inet可处理IPv4/IPv6，bridge用于相应二层桥接路径。

base chain是绑定hook的基础链，普通链需要被引用/jump等才会参与。链名可以自定义：叫input不代表已经挂到input hook，叫fwd也能实际绑定forward。必须读定义，而不能只猜名字。[链与挂点官方说明](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains)

## 4. 先学查看，别先清空规则

~~~bash
sudo nft list ruleset
sudo nft -a list ruleset
iptables -V
~~~

list ruleset列当前规则，-a附带规则handle标识；sudo用于所需权限。iptables -V只查看工具及后端标识线索，不会替你完成全部规则关系分析。正式排错还要确认规则由谁维护以及在哪个namespace。

下面是教学配置片段，不是待粘贴的宿主机配置：

~~~text
table inet ncl_demo {
    chain fwd {
        type filter hook forward priority 0; policy accept;
        ip saddr 10.10.0.2 ip daddr 10.20.0.2 tcp dport 8080 counter drop
    }
}
~~~

逐项读：inet是family，ncl_demo是表名，fwd是链名，type filter表示过滤链，hook forward说明检查转发报文，priority 0表示该hook内的相对处理位置。saddr/daddr是源/目的地址，dport是目的端口，counter记录匹配数，drop丢弃。

policy accept只描述该链未被其他终结规则处理时的默认动作，不意味着整个系统最终放行。其他基础链、不同处理阶段仍可能drop；多个链的优先级和实际路径必须一起看。

## 5. 为什么要有连接跟踪

一个TCP连接有双向数据，策略往往希望允许已授权请求的返回。conntrack以相应流信息维护状态，规则可匹配new、established、related、invalid等类别。

这些不是逐个等同TCP的SYN_SENT/ESTABLISHED状态；UDP没有TCP握手，但也可以按流量与超时维护跟踪记录。related可以涉及与已有流相关的报文，不意味着任意来源都可信。

若系统装有conntrack工具，可在实验空间查看：

~~~bash
sudo conntrack -L
~~~

-L是列出，输出可能含原方向与返回方向元组。它会涉及当前连接信息，先按需要过滤并在有权限的环境使用；不要把conntrack -F清全表当常规修复。没有该工具也不等于内核没有跟踪能力。

## 6. SNAT、DNAT与返回路径

SNAT修改源，常用于出口；DNAT修改目的，常用于端口映射。Masquerade是一种常用于动态出口地址的SNAT方式，不等于自动路由或安全许可。

教学例：内侧10.10.0.2:53000访问203.0.113.80:443，外侧变成192.0.2.10:40001→203.0.113.80:443。外侧抓包看不到原始源地址，需通过转换记录关联；返回报文还需沿能匹配相应状态的路径回来。

普通转发DNAT常在prerouting阶段改变目的，从而影响后续选路；普通出口SNAT常在postrouting处理。Linux本机流量还可能在output做DNAT，不能把转发图套给所有包。

常见有状态NAT为流建立映射，后续报文复用相应状态。修改NAT规则后，已有连接未必立刻按新规则重新映射，应区分新建/已有流，而不是全局清状态。[nftables NAT说明](https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT))

## 7. 受控故障示例：只拦一条实验业务

前提是已按[实验L1](../../../Network-Career-Lab/01-Linux/02-Labs.md)创建ncl-c/ncl-r/ncl-s，且L2 HTTP服务正常。所有修改在专用VM的ncl-r空间内，不在宿主全局执行。若已有ncl_demo同名表，先确认来源，不覆盖。

~~~bash
sudo ip netns exec ncl-r nft add table inet ncl_demo
sudo ip netns exec ncl-r nft 'add chain inet ncl_demo fwd { type filter hook forward priority 0; policy accept; }'
sudo ip netns exec ncl-r nft add rule inet ncl_demo fwd ip saddr 10.10.0.2 ip daddr 10.20.0.2 tcp dport 8080 counter drop
sudo ip netns exec ncl-r nft list table inet ncl_demo
~~~

ip netns exec已经在前篇解释；nft add table创建容器，add chain创建基础链，add rule增加精确匹配。花括号与分号可能被Shell解释，链定义放在引号内；本例不是让你手工拼接任意字符串。

访问失败的教学预期：请求匹配并增加counter；客户端可能重传SYN，而不是立即收到RST。仍应抓路由器两侧并确认实际流，计数不增加时先查空间、hook和五元组。

恢复只删除本次独立表：

~~~bash
sudo ip netns exec ncl-r nft delete table inet ncl_demo
~~~

随后重试原HTTP请求。不要使用flush ruleset。删除表不等于停止服务或拆拓扑，其他资源按实验手册清理。

## 8. 非对称、反向检查与桥接

非对称路径本身不必故障，但状态设备、NAT与源校验可能不接受。rp_filter是Linux IPv4反向路径校验相关设置，模式及all/接口的关系要按实际内核文档核对，不能看到非对称就全局关闭。

Bridge二层转发与IP三层转发不同。是否进入某些IP过滤路径还受br_netfilter等配置影响；nft bridge family也有自己的位置。排错先标出哪一层转发，再看规则，避免只查inet后宣布没有过滤。

## 9. 故障判断与练习

“计数增加”证明匹配点被走到，不证明后面的服务成功；“input全放行”不能证明forward；“NAT有记录”不能证明回程可达；“服务端收到SYN”仍需本机socket与返回证据。

自测：一条叫input的普通链是否自动拦本机？答案：不是，要看绑定或引用。规则accept后是否绝对不再被丢弃？答案：不是，还可能有其他链/阶段。UDP是否没有conntrack？答案：不是。

交付hook路径图、一次精确实验drop的计数/双点抓包/恢复记录、一个NAT前后元组表。本文示例未在本次编写过程中实跑。
