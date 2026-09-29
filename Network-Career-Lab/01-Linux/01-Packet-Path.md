# Linux：从应用一直看到网线

## 1. 把已有路由知识延伸到主机

交换机能把帧送到服务器，不表示应用已经收到数据。接收方向可以先画成：NIC → 接收队列/DMA → IRQ/NAPI → 协议栈 → 路由与 netfilter → socket → 应用。发送方向从应用写 socket 开始，经过协议栈、路由、邻居解析、发送队列和 NIC。实际钩子顺序受本机/转发、bridge、offload 影响，这张图用于定位责任层，不是内核函数调用图。

访问 `http://10.20.0.2:8080` 的必要条件包括：应用监听正确地址和端口；客户端有路由；下一跳邻居解析成功；中间节点允许转发；安全策略放行；服务器有回程路由。DNS 是访问域名时额外的一层，不能用“IP 可以 ping”证明 DNS 正常。

## 2. 每条命令回答一个问题

| 问题 | 命令 | 关键字段 / 误区 |
|---|---|---|
| 网口与地址是否正确？ | `ip -br link`、`ip -br addr` | UP 不等于端到端通；carrier 与 admin state 不同 |
| 这个目的地实际怎么走？ | `ip route get 10.20.0.2` | 不只看默认路由；源地址和策略可能改变结果 |
| 下一跳 MAC 找到了吗？ | `ip neigh` | INCOMPLETE/FAILED 是线索；STALE 本身不是故障 |
| 服务在监听吗？ | `ss -lntp`、`ss -unap` | `127.0.0.1` 监听不接收远端连接 |
| TCP 正在经历什么？ | `ss -ti` | RTT、重传等数据属于该 socket，不代表全部流量 |
| 包在哪一侧消失？ | `tcpdump -ni eth0 -s 0 -w case.pcap` | 记录接口和方向；抓到不等于应用接收 |
| DNS 是否正常？ | `dig example.com` | 区分超时、NXDOMAIN、SERVFAIL |
| 哪段路径值得调查？ | `traceroute`、`mtr` | 中间跳 ICMP 限速不等于转发丢包 |
| 服务为什么没起来？ | `systemctl status 服务名`、`journalctl -u 服务名` | 对齐故障时间，检查退出码、绑定端口和权限 |

`netstat`/`arp` 是旧工具；优先使用 `ss`/`ip neigh`。练习时先写出“我预计会看到什么”，再执行命令。

## 3. Routing、policy routing 与 namespace

普通 IP 转发按最长前缀匹配查路由。Linux policy routing 先按 `ip rule` 选择表，规则可以匹配源地址、mark 等，之后才在表内查目的前缀。先看 `ip rule show`，再看相关 `ip route show table ...`，最后用包含 `from` 的 `ip route get` 验证实际决策。

namespace 提供独立的接口视图、路由表等网络状态；veth 两端像一根虚拟网线。namespace 不是设备硬件仿真，不模拟交换 ASIC buffer。VRF 则用于同一 namespace 中分离三层路由域，两者不能直接画等号。

非对称路由本身不一定故障；状态防火墙、NAT 或严格反向路径检查可能使它变成故障。分析 `rp_filter` 时同时记录 `all` 和接口配置，不把“关闭所有检查”当作默认修复。

## 4. VLAN、bond 与安全策略

VLAN subinterface 如 `eth0.100` 负责 VLAN 100 标签处理。底层口 MTU 和交换侧 trunk 必须兼容；配置子接口不会自动配置对端交换机。

bond active-backup 使用一条活动成员链路；802.3ad/LACP 则要求对端正确形成聚合。多条链路的总容量不意味着单个流拥有链路总带宽。练习先观察 active-backup 切换，再学习 LACP、hash 和对端 MLAG 故障域。参考 [Linux bonding 官方说明](https://docs.kernel.org/networking/bonding.html)。

nftables 是 Linux 过滤/NAT 框架的配置接口之一；旧 iptables 命令可能使用 nft 后端。不要把两个工具显示的规则简单视为互不相关。INPUT 处理目的为本机的包，FORWARD 处理经本机转发的包；允许 INPUT 不会自动允许 FORWARD。查看 `nft list ruleset`、规则 counter 和连接状态，按路径定位。

## 5. MTU 和 offload

IPv4 普通 ICMP echo 数据 1472 字节 + IP 头 20 + ICMP 头 8 = 1500 字节 IP 包；因此 `ping -M do -s 1472` 是一个无 IP options 情况下的 MTU 检查例子。它不是 TCP MSS 测试。PMTUD 需要相关 ICMP 返回；小包通、大流量卡住时考虑 MTU 黑洞，但还要排除拥塞和接收端问题。

TSO/GSO 让主机以较大的逻辑数据块交给后续分段环节；GRO 把接收包聚合后再交给上层。发送 checksum offload 可能令主机抓包显示“校验和错误”，因为抓包时 NIC 尚未完成校验。不要直接据此判定线上的包坏了；对比远端抓包和开关前后的结果，修改前保存原值。

## 6. 为 HPC/低延迟打基础

RSS 将接收流映射到硬件队列；RPS 在软件中选择后续处理 CPU。查看 `ethtool -l/-x/-S eth0`、`/proc/interrupts`、`/proc/softirqs`，把“队列→IRQ→CPU→应用线程”画出来。同一流通常落在一个队列，因此增加总队列数并不能保证单流提速。NUMA 远端内存、CPU 争用和 IRQ 分布都可能影响尾延迟。先测基线再改一个变量。参考 [Linux 网络扩展机制](https://docs.kernel.org/networking/scaling.html) 的 RSS、RPS 两节。

## 自测

1. ping 通但 TCP 连接失败，下一步至少有哪些观测？参考：监听地址、SYN/RST/重传、过滤与回程，不是直接改路由。
2. 为什么抓到 SYN-ACK 还不能证明客户端应用完成连接？参考：抓包点、客户端 ACK、socket 和应用日志仍需关联。
3. `ip route` 看起来正确为何仍走错出口？参考：策略表、源地址、VRF/namespace。
4. 关闭 GRO 后吞吐下降能否认定 GRO 导致丢包？参考：不能，处理开销和测量条件都变了。

下一步：[动手实验](02-Labs.md)。
