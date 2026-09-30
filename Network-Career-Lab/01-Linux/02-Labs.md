# Linux 实验：建立基线，再制造故障

前提：[实验环境](../00-Plan/Lab-Environment.md)。所有命令在专用 Linux VM 内执行。下面的 `sudo ip netns exec` 已使后续命令在目标 namespace 中运行。

## L1 三节点路由与回程

```text
ncl-c c0 10.10.0.2/24 ---- 10.10.0.1/24 r0 ncl-r
                                         r1 10.20.0.1/24 ---- 10.20.0.2/24 s0 ncl-s
```

在本项目根目录运行：

```bash
sudo bash labs/linux/netns.sh up
sudo ip netns exec ncl-c ping -c 3 10.20.0.2
sudo ip netns exec ncl-r ip route
sudo ip netns exec ncl-c ip route get 10.20.0.2
```

预期：两端经 `ncl-r` 通信，路由器有两条直连路由；客户端下一跳是 10.10.0.1。在两个终端分别抓 `c0`、`s0`：

```bash
sudo ip netns exec ncl-c tcpdump -ni c0 icmp
sudo ip netns exec ncl-s tcpdump -ni s0 icmp
```

注入：`sudo ip netns exec ncl-s ip route del default`。再次 ping，观察服务器收到请求而没有成功返回。恢复：`sudo ip netns exec ncl-s ip route add default via 10.20.0.1`。验收：用路由输出和两端抓包说明故障，不接受只写“ping 不通”。

## L2 应用、socket 与过滤

在一个终端启动，仅提供临时目录中的实验文件：

```bash
mkdir -p /tmp/ncl-http
printf 'network-career-lab\n' > /tmp/ncl-http/index.html
sudo ip netns exec ncl-s python3 -m http.server 8080 --bind 10.20.0.2 --directory /tmp/ncl-http
```

另一个终端：

```bash
sudo ip netns exec ncl-s ss -lntp
sudo ip netns exec ncl-c python3 -c "import urllib.request; print(urllib.request.urlopen('http://10.20.0.2:8080', timeout=3).read())"
```

抓 TCP 8080 的包后依次尝试：停止服务、改为监听 127.0.0.1、恢复正常监听。预期前两者无法完成远端服务访问；通常会收到 RST，若存在过滤规则则可能表现不同。用监听输出解释，不仅靠超时猜测。

可选过滤实验：在路由 namespace 内建独立表，丢弃转发到 8080 的流量；完成后删除这张表。

```bash
sudo ip netns exec ncl-r nft add table inet ncl_lab
sudo ip netns exec ncl-r nft 'add chain inet ncl_lab forward { type filter hook forward priority 0; policy accept; }'
sudo ip netns exec ncl-r nft add rule inet ncl_lab forward tcp dport 8080 counter drop
sudo ip netns exec ncl-r nft list table inet ncl_lab
# 再次访问并抓包：预计 SYN 重传且 counter 增加
sudo ip netns exec ncl-r nft delete table inet ncl_lab
```

## L3 MTU、重传与证据

```bash
sudo ip netns exec ncl-r ip link set r1 mtu 1400
sudo ip netns exec ncl-s ip link set s0 mtu 1400
sudo ip netns exec ncl-c ping -c 3 -M do -s 1472 10.20.0.2
sudo ip netns exec ncl-c ping -c 3 -M do -s 1372 10.20.0.2
```

预期：第一个测试因 MTU 无法成功，第二个可通过；捕获的 ICMP 或本地错误要说明来自哪里。每次测试记录 payload 长度、IP 包长度和出口 MTU。恢复两端 MTU 为 1500。进阶：`tc netem` 在实验接口引入丢包，用 TCP 传输观察重传；TCP 的序号是字节序号，不把重复 ACK 直接等同于丢包位置。

## L4 VLAN 和 bond

VLAN：在 L1 的 c0/r0 两端分别建 VLAN 100 子接口，使用新的 10.100.0.0/24。

```bash
sudo ip netns exec ncl-c ip link add link c0 name c0.100 type vlan id 100
sudo ip netns exec ncl-r ip link add link r0 name r0.100 type vlan id 100
sudo ip netns exec ncl-c ip addr add 10.100.0.2/24 dev c0.100
sudo ip netns exec ncl-r ip addr add 10.100.0.1/24 dev r0.100
sudo ip netns exec ncl-c ip link set c0.100 up
sudo ip netns exec ncl-r ip link set r0.100 up
sudo ip netns exec ncl-c ping -c 3 10.100.0.1
```

在父口用 `tcpdump -eni c0 vlan` 观察标签；虚拟化/offload 可能改变抓包所见，必要时对比子接口。把对端 VLAN 改成 200 后，预计 ARP 失败。删除子接口再以 100 重建以恢复。

bond 独立实验使用两台 VM，各有两块接到同一隔离二层域的实验 NIC，管理 NIC 不参与。先检查驱动，再在一侧把无地址的 `ens4/ens5` 加入 `bond0`：

```bash
sudo ip link add bond0 type bond mode active-backup miimon 100
sudo ip link set ens4 down
sudo ip link set ens5 down
sudo ip link set ens4 master bond0
sudo ip link set ens5 master bond0
sudo ip addr add 192.0.2.10/24 dev bond0
sudo ip link set ens4 up
sudo ip link set ens5 up
sudo ip link set bond0 up
cat /proc/net/bonding/bond0
```

对端实验接口配 192.0.2.20/24。持续 ping，关闭当前活动成员，再查看 active slave 与丢包数量，恢复后记录是否回切。不要假设 active-backup 要求对端 LACP。清理时移除本次地址、对成员执行 `nomaster`，删除 `bond0` 并恢复原状态；这些 NIC 必须是预先确定的实验口。

## L5 policy routing、日志与 NIC

在 `ncl-c` 中建一张源地址策略表，故意指向隔离的黑洞路由：

```bash
sudo ip netns exec ncl-c ip route add blackhole 10.20.0.0/24 table 100
sudo ip netns exec ncl-c ip rule add priority 100 from 10.10.0.2/32 table 100
sudo ip netns exec ncl-c ip route get 10.20.0.2 from 10.10.0.2
# 清理本次规则和路由
sudo ip netns exec ncl-c ip rule del priority 100 from 10.10.0.2/32 table 100
sudo ip netns exec ncl-c ip route del blackhole 10.20.0.0/24 table 100
```

补充任务：在 VM 上为一个已有 systemd 服务保存 `status` 与 `journalctl -u ... --since ...` 输出，解释启动失败和链路失败的差别；采集 `ethtool -k/-l/-S` 和 IRQ 数据，标明不支持的能力。非对称路由扩展用第二条隔离路径重画正反路径，再观察状态防火墙行为，不在原三节点拓扑中声称模拟了双出口。

## 收尾与验收

先在服务/抓包终端按 Ctrl+C 停止进程，再运行 `sudo bash labs/linux/netns.sh down`。脚本发现 namespace 内还有进程会拒绝清理，先结束你启动的进程再重试。

随机选“回程缺失、监听错误、转发过滤、MTU、策略路由”两种故障，在 20 分钟内给出观测→假设→验证→恢复。英文练习：*The packet reaches the server interface, but the response has no valid return route.*
