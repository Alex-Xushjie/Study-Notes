# 源过滤与Linux主机成员关系

[返回组播学习目录](../Multicast.md)

## 1. INCLUDE和EXCLUDE

INCLUDE集合表示只希望接收列出的源；EXCLUDE集合表示接收除列出源之外的其他源。INCLUDE空集表达不接收任何源，EXCLUDE空集表达接收任意源。它们是接收偏好，不能替代网络ACL、源真实性检查或加密。

假设同主机两个应用都接收G：A需要S1，B需要S2。链路成员报告反映主机聚合后的需求，并非一个报告严格对应一个进程。停止A后，S2仍可能需要保留。检查主机接口表只能确认聚合状态，进程级归属还要查看应用日志、Socket与程序代码。

## 2. Linux中四个不同动作

Socket是进程收发网络数据的操作系统接口；bind绑定本地地址/端口，加入组设置接收成员关系，发送接口选择决定从哪张网卡发，路由与策略再决定系统如何处理。它们不能相互替代。

IPv4 ASM常使用IP_ADD_MEMBERSHIP，SSM可使用IP_ADD_SOURCE_MEMBERSHIP。多网卡时显式指定接口，不能依赖默认路由碰巧选对。退出或关闭Socket会影响成员引用，但其他进程仍可维持订阅。

下面是Linux主机只读检查，不是NOS配置。eth0只是示例网卡名，先用ip -br link确定实际名称。

~~~bash
ip -br link
ip -br addr
ip maddr show dev eth0
cat /proc/net/igmp
ss -u -a -n -p
sudo tcpdump -ni eth0 -vv 'igmp or (udp and dst host 239.10.10.10 and dst port 5000)'
~~~

ip maddr展示接口的链路/协议成员信息，不等于列出每个应用的源过滤条件；ss能辅助看UDP Socket，却不能独自证明正确订阅。抓包需要权限，可能含业务数据，实验中只保存必要报头。

## 3. “能抓到却收不到”的解释

抓包工具可能启用混杂模式或全组播接收，使网卡接到额外数据。tcpdump看到报文只证明到达某抓包点，不证明内核防火墙允许、不证明Socket匹配或应用已读取。比较G、源S、目的端口、入接口、命名空间与进程所属VRF，并查看Socket丢包和应用序列号。

反过来，启动抓包后业务突然正常也应怀疑NIC过滤、驱动或接入状态，而不是把长期运行抓包工具当修复。用关闭混杂模式的对照、交换机端口镜像和接口计数缩小边界。

## 4. 实验要求

分别运行只bind不join、加入错误网卡、正确ASM加入、指定S1的SSM加入，记录IGMP报告和应用结果。不要预先断言所有OS下bind到G行为一致；固定内核、应用库与参数。主机组播与转发路由器是两种角色，启用普通IP转发不会自动创建完整PIM域。

[Linux ip(7)与成员Socket选项](https://man7.org/linux/man-pages/man7/ip.7.html)、[IGMPv3源过滤](https://www.rfc-editor.org/rfc/rfc9776.html)。继续阅读[Linux UDP与Socket](../../03-Linux-Networking/05-TCP-UDP-and-Sockets/01-TCP-UDP-and-Sockets.md)。
