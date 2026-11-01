# 抓包、日志与网络观测

[Linux学习目录](../Linux-Networking.md)

## 1. 工具怎样组成证据链

你已经能查接口和路由，现在要知道某个失败发生在哪一段。先定义业务五元组、时间窗、执行机器与namespace，再挑观测工具。工具输出是某个位置、某种口径的事实，不是“网络正常”的全局证明。

| 工具 | 主要问题 | 不能单独证明 |
|---|---|---|
| ip | 接口、地址、路由与邻居 | 应用请求成功 |
| ss | 监听、连接、队列与协议统计 | 报文经过全路径 |
| tcpdump | 抓包点实际看到哪些报文 | 应用已消费、记录器绝不漏采 |
| dig/resolvectl | 名称怎样解析 | 返回地址一定可达 |
| curl | HTTP等请求到哪一步 | 网络以外所有依赖正常 |
| ethtool/ip -s | 网卡/接口能力与计数 | 某条业务必然受影响 |
| systemctl/journalctl | 服务状态与日志 | 远端路径可用 |

部分工具需要额外软件包；先用command -v 工具名检查，不把缺工具等同故障。

## 2. tcpdump先抓哪里

tcpdump通过抓包接口记录报文。接口可以是实际网卡、veth或其他逻辑设备，位置不同、封装不同，看到的内容就可能不同。网卡名按ip -br link实际结果替换。

~~~bash
sudo tcpdump -i ens160 -nn -c 20 'tcp port 8080'
~~~

| 部分 | 含义 |
|---|---|
| -i ens160 | 指定捕获接口 |
| -nn | 不解析地址与服务端口名称，保留数字 |
| -c 20 | 收到20个匹配包后退出；没有匹配时仍可能等待 |
| tcp port 8080 | 匹配相关TCP端口的过滤表达式 |

过滤表达式用引号保护，Ctrl+C停止前台捕获。开始时可不加很窄的过滤，以免丢掉ARP、ICMP或另一个端口的证据。-i any可看当前空间多个接口，但不等于所有namespace；链路头形式、重复观察和方向也要理解。

## 3. 读一次TCP建连

教学输出的关键部分可能是：

~~~text
10.10.0.2.53000 > 10.20.0.2.8080: Flags [S]
10.20.0.2.8080 > 10.10.0.2.53000: Flags [S.]
10.10.0.2.53000 > 10.20.0.2.8080: Flags [.]
~~~

地址最后点号后的数字是端口，不是第五个IPv4字节。S表示SYN，S.为SYN加ACK，单独.表示ACK；其他字段还可能有seq、ack、win和length。seq是TCP字节序号，不是IP包编号。

重复SYN没有回应，只能说明缺有效回应；RST可能来自无监听或策略拒绝。看到握手完成后才继续读请求和应用响应，不把三次握手当全部成功。

## 4. 保存与读取pcap文件

pcap是常见抓包文件格式，可后续用tcpdump或Wireshark分析。先用pwd确认Linux当前目录，再在可写的实验目录执行：

~~~bash
sudo tcpdump -i ens160 -nn -s 0 -c 100 -w case-http.pcap 'tcp port 8080 or icmp'
tcpdump -nn -r case-http.pcap
~~~

-s指定捕获长度，0采用工具规定的较大默认快照长度；-w写文件，通常不再像实时文本那样逐包显示；-r读取已有文件。抓包数据可能包含业务内容，应使用实验流量并按需要脱敏。不要把后续读文件的时间当报文发生时间。

只在ncl-s内抓服务侧时：

~~~bash
sudo ip netns exec ncl-s tcpdump -i s0 -nn 'tcp port 8080 or icmp or arp'
~~~

先确认该空间与接口已由实验L1创建。过滤里的or表示任选一种，and表示同时满足，括号控制组合；它不是Shell管道。

语法、计数与时间戳详见[tcpdump手册](https://manpages.debian.org/bookworm/tcpdump/tcpdump.8.en.html)。

## 5. 抓包自己的丢包也要记录

结束时tcpdump可能显示captured、received by filter、dropped by kernel。它们依捕获后端和平台有不同口径，不应要求前三项简单相加完全对应线上包数。

记录器CPU、磁盘、镜像超订阅和过滤位置可能造成漏采。主机发送offload可能显示逻辑大包或校验提示；不同点的时间戳也可能属于不同时间域。抓包中没看到某序号，先确认采集覆盖再宣称业务丢包。

## 6. 名称解析要独立于IP连通

~~~bash
dig app.test
cat /etc/resolv.conf
~~~

dig是DNS查询工具，app.test是示例名称，实际使用你的实验或业务域名。看查询服务、状态码、Answer与耗时：NXDOMAIN是不存在的响应，SERVFAIL是解析失败，timeout是没有按期收到有效响应。

如果系统使用systemd-resolved，可再用resolvectl status看接口相关DNS，resolvectl query 名称作查询。resolvectl是该组件的客户端；没有这个组件时命令可能不存在。/etc/resolv.conf指向本地stub地址并不能直接告诉你所有上游与条件转发行为。

应用可能使用缓存、不同resolver或不同地址族。因此dig成功后，还需确认应用实际连的地址。

## 7. curl把连接与应用阶段连起来

~~~bash
curl -v --connect-timeout 3 --max-time 5 http://10.20.0.2:8080/
~~~

-v显示详细过程，--connect-timeout限制建连阶段，--max-time限制整次操作时间。地址仅对应已建好的实验HTTP服务，没有该服务时不要期待成功。

连接拒绝、连接超时、TLS失败与HTTP500是不同层次。HTTP错误说明收到了应用层响应，不应直接归因三层不通。HTTPS排错要核对主机名、证书、SNI与信任链，不用关闭证书校验掩盖问题。

只在当前请求指定名称对应地址可用curl的--resolve能力；它用于区分DNS与连接，不等于修复全局DNS。参数按本机curl --help核验。

## 8. 计数器：先读单位与累计方式

~~~bash
ip -s link show dev ens160
nstat -az
~~~

ip的-s显示统计，可能含bytes、packets、errors与dropped。每一层的dropped不一定同义，比较同窗口增量，不把历史值直接归因当前事件。

nstat查看内核网络统计；-a读取绝对值，-z也显示零。默认行为可能使用历史增量，所以教材采用明确口径。名称如TCP重传、UDP接收缓冲错误应结合内核与工具说明，不能把不同计数无脑相加。[nstat参考](https://man7.org/linux/man-pages/man8/nstat.8.html)

## 9. 日志与抓包怎样对齐

systemctl status说明服务管理状态，journalctl -u 服务名按服务过滤。时间窗要包括故障之前和之后，记录主机时区；不同主机未同步时，不用微秒级时间差下结论。基础用法见[进程与服务](../01-Linux-Essentials/02-Processes-Services-and-Packages.md)。

例如某端口冲突发生在09:01、抓包故障在09:10，需核对服务后来是否启动，而不能把第一条错误一直当根因。

## 10. 一个跨层案例

客户端curl超时。先确认解析/目的，再查客户端route get。客户端抓SYN，服务端无SYN时沿路径取证；服务端有SYN无回应时查监听、过滤、回程；已发SYN-ACK而客户端无时查反向；握手后卡住则观察请求、窗口、重传与日志。

每次观测应减少不确定性。不要同时抓所有接口、重启服务、关闭防火墙、改MTU，然后凭恢复就猜一个根因。

## 11. 自测与交付

自测：any能看到全部namespace吗？答案：不能。-w是否继续逐包打印同样文本？答案：通常写文件取代该显示。curl收到500是否表示没有建连？答案：不是。抓包无报文是否绝对证明链路丢包？答案：还需核对捕获。

交付一份接口/路由、socket、pcap、日志和时间窗对应的实验报告。配套[Linux实验L1–L3](../../../Network-Career-Lab/01-Linux/02-Labs.md)。本次仅编写与核对文档，没有实跑捕获或性能测试。
