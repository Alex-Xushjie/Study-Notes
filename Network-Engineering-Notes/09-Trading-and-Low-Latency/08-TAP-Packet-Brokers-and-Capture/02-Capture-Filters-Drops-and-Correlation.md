# 抓包过滤、丢样本与证据关联

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 先定义要回答的问题

按S/G/P、方向与时间窗过滤，确认镜像位置能看见哪个阶段。抓业务G可能漏掉IGMPv3到224.0.0.22的报告，也看不到ASM Register外层完整关系。控制面和业务分开设计过滤。

## 2. 低速实验命令

以下Linux命令在隔离测试流上使用，eth0替换为实际网卡，239.10.10.10:5000是自建实验频道：

~~~bash
sudo tcpdump -ni eth0 -c 1000 -s 128 -w lab-feed.pcap 'udp and dst host 239.10.10.10 and dst port 5000'
~~~

-c限制包数，-s限制保存长度，-w写当前目录文件。128字节可能截掉序号，按自建格式调整；无流时会一直等，可Ctrl+C停止并保存统计。写文件前确认目录与空间，不在生产行情主机无边界执行。

## 3. 可信度检查

保存tcpdump结束统计，核对内核/NIC丢失、SPAN超订阅和记录器状态。Offload可能使主机抓包表现与线缆分段/校验和不同；抓包工具也可能改变网卡接收和CPU负载，启动抓包后现象变化需单独验证。

跨点关联以session/channel和序号为主，时间辅助。多个时钟未校准时不直接计算单向微秒值，SPAN重复也不能算业务重复。

## 4. 练习

保存两份自建输入，一份人为漏采一段，另一份完整，结合应用日志判断“业务丢失”还是“采集丢失”。记录采样点、过滤、snaplen、时钟、版本和已知缺口，结论不得超过观察范围。

[组播抓包可信度](../../02-Multicast/09-Design-and-Troubleshooting/03-Loss-Localization-and-RCA.md)、[tcpdump手册](https://www.tcpdump.org/manpages/tcpdump.1.html)。
