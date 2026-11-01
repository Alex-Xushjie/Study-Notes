# Socket、TCP/UDP与缓冲

[Linux学习目录](../Linux-Networking.md)

## 1. Socket是应用与网络之间的接口

Socket常译为套接字。应用通过操作系统提供的socket接口收发数据，内核管理相应协议与缓冲。它不是网卡，也不只是一个端口号：地址族、协议、绑定地址/端口、队列和状态等共同决定行为。

应用进程是运行中的程序实例，PID是其编号。一个进程可以有多个socket，多个进程也可能按特定机制共享或分别监听相关端点。先确认具体连接，不能只看到程序名称就推断全部流量。

## 2. 应用怎样建立服务

TCP服务通常经历创建socket→bind绑定本地地址/端口→listen等待→accept接收连接→读写数据；客户端创建socket→connect→读写。首次阅读先理解职责，不要求编写C程序。

bind决定“在哪个地址和端口接收”，路由决定“包怎样到达”。应用监听127.0.0.1:8080，远端访问网卡10.20.0.2:8080时，不能把loopback监听当成已开放该地址。

0.0.0.0表示IPv4通配绑定，不是一个要配置到网卡的普通地址；它仍受namespace、VRF、过滤等条件影响。IPv6的::是IPv6通配，是否同时接受IPv4取决于socket与系统设置，不能只凭一行监听猜测。

## 3. 第一条ss命令逐个解释

ss用于查看socket统计和状态，来自iproute2。先执行：

~~~bash
ss -lntp
~~~

-l只看监听，-n不把地址/端口解析成名称，-t看TCP，-p显示进程信息。普通用户未必能看到所有进程详情，缺users字段不意味着没有程序。

教学输出：

~~~text
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      128    127.0.0.1:8080     0.0.0.0:*
~~~

State是状态，Local是本地绑定，Peer是远端；监听时*表示尚无特定对端。TCP监听的Recv-Q通常反映等待accept的已建连队列，Send-Q反映相应backlog上限口径；它们不是当前传输带宽。SYN未完成队列还有其他机制，不应与accept队列混成一个数字。

[ss手册](https://man7.org/linux/man-pages/man8/ss.8.html)可核对本机选项，输出字段随版本与协议而变。

## 4. TCP连接状态怎样连接到排错

| 状态/现象 | 第一层含义 | 不能立即得出的结论 |
|---|---|---|
| LISTEN | 等待连接 | 所有远端都可访问 |
| SYN-SENT | 本端正在发起连接 | 一定是运营商丢包 |
| ESTAB | 相应TCP连接已建立 | 应用业务成功 |
| CLOSE-WAIT | 对端关闭后，本端应用尚未完成关闭等处理 | 必然是网络路由故障 |
| TIME-WAIT | 主动关闭侧常见的协议保持状态 | 数量非零就故障 |

TCP提供可靠有序字节流，不保证一次write对应一次read，也不保证业务事务被执行一次。ACK确认传输层字节接收，不等于数据库提交或订单已被交易所接受。

## 5. 看正在传数据的连接

~~~bash
ss -tn
ss -ti
ss -tin '( dport = :8080 or sport = :8080 )'
~~~

-n保留数字，-i显示TCP内部统计，最后一条用过滤表达式只看相关端口；引号保护表达式不被Shell误解释。sport/dport是源/目的端口，过滤语法以本机ss帮助为准。

已建立TCP的Recv-Q可用来观察尚未被应用读取的数据量，Send-Q可用于观察待确认等发送积压，但不把它们与监听队列按同一单位解释。ss -m显示socket内存记账，更不是线上payload的简单等号。

ss -i可能出现rtt、cwnd、retrans等：rtt是往返时间统计，cwnd是拥塞窗口，retrans是相应重传信息。字段单位和累计口径须读当前输出说明，不把所有重传数字当作本秒事件。

## 6. 三种缓冲不要混淆

~~~text
NIC ring/描述符资源 → 内核报文处理 → socket接收缓冲 → 应用自己的队列
~~~

NIC ring承接设备收包资源；socket缓冲在协议与应用之间；应用队列在程序内部。某一层增长或丢弃，不一定反映在其他层同名计数里。

TCP接收窗口表达接收端可承接情况，拥塞窗口约束网络在途发送。接收方应用慢可能使窗口缩小甚至零窗口，优先调查消费与资源。增加缓冲能吸收一定突发，但不能使持续慢的消费者无限承载；还可能增加等待时间。

## 7. UDP与业务完整性

UDP不提供TCP式握手、重传和有序流。应用可通过bind接收特定端口，也可对UDP socket使用connect记录默认对端等信息，这仍不变成TCP连接。

~~~bash
ss -unap
ss -u -a -m
~~~

-u看UDP，-a包含相应全部socket，-m显示内存。Recv-Q或drop等字段按协议与工具口径解释；不能把应用序号gap直接等同某一层计数。

组播接收还需要应用在正确接口表达成员需求，绑定UDP端口不自动完成所有加组条件。收到网卡包也不表示socket匹配、内核缓冲与应用解析都成功。

## 8. 吞吐为什么受RTT与窗口影响

BDP是bandwidth-delay product带宽时延积，用于估计填满路径所需在途量。10Gbit/s×20ms÷8=25,000,000bytes，约25MB。若有效在途窗口仅1MB，窗口/RTT粗略上限为50MB/s，即400Mbit/s。

这只是数量级模型，实际还受拥塞控制、包损、CPU、应用、存储与实现影响。多流变快可能绕过单连接限制，不证明单流问题已解决。

## 9. MTU、MSS与重传

MTU限制相应层的包长；MSS是TCP数据部分的最大段大小，不是以太网帧长。常见无options IPv4模型中1500减20减20得1460，隧道/IPv6/options需要重新算。

小ping与握手成功、大数据卡住，可调查路径MTU、必要ICMP反馈与重传；但也保留过滤、拥塞和应用限制解释。发送主机offload可能让抓包看见大逻辑包，不能据此认定线上超MTU。

## 10. 一个完整案例：服务进程在，远端却失败

按顺序查绑定地址→客户端实际目的→SYN到达→SYN-ACK离开→客户端ACK→请求与响应。RST可来自无监听或reject；重复SYN说明缺有效回应，故障位置需双点证据。

若握手完成、Recv-Q持续上升且应用处理积压，消费不足是候选解释；若网络两端完整而应用报缺失，调查socket与解析；若大段持续重传，调查MTU和负载。每条都需要能推翻它的证据。

## 11. 内核参数不是入门调优清单

sysctl是查询/调整内核参数的工具。先只看：

~~~bash
sysctl net.core.rmem_max
sysctl net.core.wmem_max
sysctl net.ipv4.tcp_rmem
sysctl net.ipv4.tcp_wmem
~~~

rmem/wmem关联接收/发送内存限制，TCP还有自己的范围与自动调整。应用设置、内核记账与参数之间存在细节，不能简单把某个值当有效payload窗口。[socket内存说明](https://man7.org/linux/man-pages/man7/socket.7.html)与[TCP](https://man7.org/linux/man-pages/man7/tcp.7.html)、[UDP](https://man7.org/linux/man-pages/man7/udp.7.html)手册

没有瓶颈证据时不批量调大，改动要记录原值、作用范围和恢复。此篇不提供生产通用sysctl模板。

## 12. 自测与实践

自测：监听和连接是否同一状态？答案：不是。UDP socket是否会因connect获得TCP可靠性？答案：不会。ACK是否证明业务提交？答案：不是。接收缓冲越大是否延迟越低？答案：不一定。

完成[实验L2与L3](../../../Network-Career-Lab/01-Linux/02-Labs.md)，保存监听地址、握手、请求/响应与两种故障。输出是教学示例，命令和性能未在本次编写中运行验证。
