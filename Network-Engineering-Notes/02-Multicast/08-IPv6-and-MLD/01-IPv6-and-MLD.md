# IPv6组播、作用域与MLDv2

[返回组播学习目录](../Multicast.md)

## 1. IPv6不是把IGMP名字换掉

IPv6没有广播，组播参与邻居发现等基础功能。组播地址以ff00::/8开头，地址内含标志和作用域。ff02::1是链路所有节点，ff02::2是链路所有路由器；这类基础组不能拿来承载业务或随意屏蔽。

IPv6以太网目的MAC使用33:33加组地址低32位，也存在映射碰撞。链路本地地址和链路本地组在多接口主机上有接口作用域，日志中的地址应连同接口记录。提高Hop Limit不会把链路本地作用域变成全网可路由业务。

## 2. MLD成员管理

MLD通过ICMPv6而非独立的IGMP协议号工作。Query类型130，MLDv1 Report 131、Done 132，MLDv2 Report 143。MLDv2报告常发往ff02::16；抓包过滤IPv4的igmp看不到它。

MLDv1表达任意源接收，MLDv2支持源过滤。新的MLDv2规范RFC9777替代RFC3810。它们与IPv6 PIM建树、二层MLD Snooping分别处在不同层次；不要把禁用所有ICMPv6当安全加固。

## 3. IPv6 SSM与ASM

SSM使用带作用域的FF3x::/32范围表示相应地址结构，x表示作用域，具体分配仍需符合标准格式和域规划，不能只看前两个字节就认定任意地址合法。接收者用MLDv2指定源，网络朝源建树。

IPv6 ASM可以使用RP映射，Embedded-RP按特定地址格式携带RP信息，是一种映射机制，并非所有IPv6组都内嵌RP。地址规划、设备支持和域边界要一起确认。

## 4. 检查与抓包

以下仅是Linux只读命令，eth0替换为实际接口。

~~~bash
ip -6 addr show dev eth0
ip -6 maddr show dev eth0
cat /proc/net/igmp6
sudo tcpdump -ni eth0 -vv 'icmp6 or (ip6 and udp and dst port 5000)'
~~~

icmp6过滤范围包括ND等报文，需要在解码后确认具体类型。/proc/net/igmp6显示主机成员相关信息，不是PIM树。接收应用还需IPv6 Socket成员API及接口索引，不能复用IPv4的成员参数结构。

## 5. 实验要求

先确认ND和单播IPv6正常，再测同链路成员报告，然后跨路由测试业务组。加入一个指定源频道，分别验证正确源、错误源、MLD Snooping老化和路由切换。基础ND正常不证明业务PIM树正常；业务通也不意味着所有ICMPv6策略正确。

[MLDv2：RFC9777](https://www.rfc-editor.org/rfc/rfc9777.html)、[IPv6地址：RFC4291](https://www.rfc-editor.org/rfc/rfc4291.html)、[Embedded-RP：RFC3956](https://www.rfc-editor.org/rfc/rfc3956.html)、[SSM范围：RFC4607](https://www.rfc-editor.org/rfc/rfc4607.html)。
