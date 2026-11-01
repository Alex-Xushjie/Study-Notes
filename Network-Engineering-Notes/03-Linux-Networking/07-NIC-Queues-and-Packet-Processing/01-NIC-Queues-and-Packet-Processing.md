# 网卡、队列、中断与NAPI

[Linux学习目录](../Linux-Networking.md)

## 1. 先认识CPU、内存与网卡的分工

CPU执行指令，内存保存程序处理的数据，NIC是network interface card网卡。驱动让内核与设备协作。网卡不是“包来了就直接送给应用”，两者之间还有资源分配、协议处理和调度。

DMA是direct memory access直接内存访问，设备按相应机制读写内存，减少逐字节由CPU搬运的需要。它仍需要内存、总线、驱动与同步，不代表完全没有CPU工作。

## 2. 接收队列与描述符是什么

队列用于组织待处理工作。NIC的ring常指环状描述符等管理资源，描述符可以记录数据buffer的位置、长度和状态。不要把ring直接理解为交换机共享buffer，也不要把“4096项”误认成4096MB。

~~~text
线上报文
  ↓
NIC识别与接收队列
  ↓ DMA及描述符交互
驱动/NAPI取出工作
  ↓
协议栈 → socket缓冲 → 应用读取
~~~

这是普通接收路径的责任模型，实际受驱动、offload、XDP与虚拟化影响。每一层都可能排队或丢弃，网络设备零丢包不证明主机无损。

## 3. 中断与NAPI怎样合作

IRQ是中断请求，可理解为设备通知CPU“有事件待处理”。如果每个包都产生独立处理通知，高包速下开销可能很大。

NAPI是Linux的网络事件处理机制，常见模式中设备通知后调度NAPI按预算批量处理；也存在busy polling等方式。它不是要求你安装的新服务。SoftIRQ是内核组织某些延后工作的一种执行机制，常见网络处理会在相应上下文发生，繁忙时也可能涉及ksoftirqd线程。

不能简单背成“永远一个包一个中断”或“NAPI永远只有一种CPU执行路径”。本机驱动、内核与配置决定细节。[内核NAPI说明](https://docs.kernel.org/networking/napi.html)

## 4. 多队列与RSS为什么有用

RSS是receive side scaling，网卡可根据流相关字段的hash，把接收流映射到不同队列。Hash是把一组字段映射为值的计算，再通过相应表选队列；常见字段含源/目的地址、端口，实际支持需核对NIC。

同一流一般保持队列归属，有助于维持处理顺序。增加队列数不意味着一条TCP流同时跑满所有核心；隧道、UDP组播和内外层hash能力还可能改变分布。

| 机制 | 工作位置 | 目标 |
|---|---|---|
| RSS | NIC接收分流 | 将流分配到硬件队列 |
| RPS | 软件接收处理 | 选择后续处理CPU |
| RFS | 软件相关引导 | 结合应用位置改善处理局部性 |
| XPS | 软件发送选择 | 帮助选择发送队列等 |

它们不是四个相同开关，也不应不看现有配置就全部启用。[Linux scaling](https://docs.kernel.org/networking/scaling.html)

## 5. ethtool命令先看小写查询

ethtool用于查询/配置网卡和驱动能力。以下ens160替换为真实实验口：

~~~bash
ethtool -i ens160
ethtool -l ens160
ethtool -x ens160
ethtool -g ens160
ethtool -S ens160
~~~

-i查驱动、固件与总线信息；-l查channel能力/现值；-x查RSS相关表；-g查ring能力/现值；-S查驱动统计。不是每个驱动都支持所有查询，Operation not supported首先是能力边界，不必然是故障。

channel、队列与中断向量并非在所有NIC上都严格一一对应。输出的Pre-set maximums表示支持上限，Current hardware settings才是当前设置；不要把最大值当已经启用的值。大写-L/-G等可能改变配置，和查询不是一回事。[ethtool参考](https://man7.org/linux/man-pages/man8/ethtool.8.html)

## 6. 怎样看中断与CPU分布

~~~bash
cat /proc/interrupts
cat /proc/softirqs
~~~

cat读取内核提供的统计。interrupts通常按CPU列展示中断累计计数及事件名称；softirqs展示相应软件中断类别，NET_RX/NET_TX与网络相关，但计数不是“这一核收了多少线上包”的简单等号。

先采样t1，再采样t2，比增量。找到驱动/设备相关行，再关联队列、IRQ和CPU。网卡向量名随驱动不同，不能拿一份固定正则覆盖所有平台。

有sysstat工具时可用mpstat -P ALL 1观察各逻辑CPU每秒情况；mpstat是处理器统计工具，-P ALL选择所有CPU，1是采样间隔秒。总CPU均值不够，因为一个繁忙核心可被几十个空闲核心稀释。

## 7. 发送方向还要认识qdisc

qdisc是queueing discipline队列规则，用于Linux发送调度等控制。tc是traffic control工具。它与NIC Tx ring不同，不是看其中一个就排除所有发送积压。

~~~bash
tc -s qdisc show dev ens160
~~~

-s显示统计，qdisc show查询队列规则。关注类型、backlog与drops，并核对是否存在整形、虚拟设备或流分类；不能因某次drop非零直接解释为物理链路丢包。[tc手册](https://manpages.debian.org/bookworm/iproute2/tc.8.en.html)

## 8. Interrupt Coalescing与ring的取舍

Coalescing是中断合并：累计若干事件或等待一段时间再通知，可降低通知成本，也可能增加等待。调小不保证更快，CPU过载可能让尾延迟更差。

增加ring可吸收某些短时处理落后，但不能无限弥补持续服务不足，也可能增加排队。应同时看pps、CPU、丢弃与应用延迟，不以“值越大越好”选择。

## 9. 案例：一核100%，总CPU只有5%

候选解释：单流集中某队列、RSS分布偏斜、IRQ分配不合理、应用单线程或其他竞争。先确认高占用属于IRQ/softirq还是用户应用，再看队列与流模型。

如果多流总吞吐上升而单流不变，支持存在单路径/单流限制，但仍要排除TCP窗口、应用等其他原因。不要直接写“再加几个队列即可解决”。

## 10. 观察作业与自测

先交付驱动/队列/ring上限与当前值、两次IRQ采样、每核负载，以及一张NIC→队列→IRQ→CPU→应用关系图；没有物理NIC时标“虚拟能力观察”。

自测：ring项数是否等于bytes？答案：不是。RSS是否保证单流多核？答案：不保证。低平均CPU是否排除主机瓶颈？答案：不能。NAPI是否需启动systemd服务？答案：不是。

本篇先建立观测能力，实际修改参数必须在隔离环境保存原值、单变量验证并恢复。本次未执行硬件测试。
