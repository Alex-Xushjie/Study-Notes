# Namespace、veth与Linux Bridge

[Linux学习目录](../Linux-Networking.md)

## 1. 为什么一台Linux会像有多台主机

前面查看的是你登录后所在环境的接口和路由。同一台机器还可以为不同进程提供不同的网络视图，例如容器有自己的网卡和地址，宿主上运行另一个服务。要解释它们之间怎样通信，需要认识Namespace、veth和bridge。

本篇先建立对象关系，再做一个两个端点的最小示例。你已经懂二层与三层，不需要重学交换原理，但需要知道Linux用什么对象实现它们。

## 2. 三个新组件分别是什么

| 组件 | 用普通语言解释 | 与网络设备的联系 |
|---|---|---|
| Network namespace，网络命名空间 | 给进程提供一套独立的网络设备、地址、路由、socket等网络状态 | 可以先想成另一套主机网络环境，而不是整台虚拟机 |
| veth，虚拟以太网设备对 | 两个互相连接的虚拟接口，一端发送的数据由另一端接收 | 像连接两个端点的一根虚拟网线 |
| Linux bridge，网桥 | 内核实现的二层转发设备，可接入多个接口 | 像软件交换机，但性能与硬件特性不能直接等同ASIC |

网络命名空间不隔离所有CPU、文件系统和进程信息，因此不等于完整容器或VM；容器通常组合多种隔离机制。VRF侧重三层路由域，namespace则能隔离更多网络状态。

[网络命名空间说明](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)与[veth原理](https://man7.org/linux/man-pages/man4/veth.4.html)可用来核对边界。

## 3. 命令在哪里执行，决定你看到哪张表

~~~text
宿主默认网络环境：lo、ens160、main表

ncl-left命名空间：lo、ncl-l0、自己的main表

ncl-right命名空间：lo、ncl-r0、自己的main表
~~~

三个环境里的main都是普通路由表名称，但不是同一套条目。主机有一张到互联网的默认路由，不会自动使新建命名空间也能上网。虚拟端点之间也不会因为在同一CPU上就自动可达。

进程通常继承父进程的网络命名空间。进入命名空间执行一个命令，是让该命令使用那套网络状态，不是登录另一台物理机器。[ip-netns手册](https://man7.org/linux/man-pages/man8/ip-netns.8.html)

## 4. 怎样查看命名空间

~~~bash
ip netns list
readlink /proc/self/ns/net
~~~

第一条的netns是network namespace的缩写，list列出通过该命名约定管理的空间。输出可能是空的，也可能有ncl-left等名称。空列表不能证明没有容器网络空间，因为并非所有空间都有这种名字。

第二条中readlink用于读取符号链接指向；/proc/self指执行该命令的进程自身。结果可能类似net:[4026532000]，方括号中的数字用于标识该网络空间，不是IP或进程编号。

有util-linux工具集时，还可用lsns -t net查看网络类型的namespace；lsns表示列出命名空间，-t net限制类型。可见结果受当前权限和进程可见范围影响。此处先知道“观察位置可查”，不必背标识数字。

## 5. 先读懂进入空间的命令

~~~bash
sudo ip netns exec ncl-left ip -br address show
~~~

| 片段 | 意义 |
|---|---|
| sudo | 按系统授权取得执行所需权限 |
| ip netns exec | 在指定网络命名空间运行后续程序 |
| ncl-left | 目标空间名称，是本例自定义的名字 |
| ip -br address show | 真正要在其中执行的地址查询 |

这行里两个ip分工不同：前一个组织执行环境，后一个读取其中的地址。命令运行结束后回到原终端；它不会把当前Shell永久搬进目标空间。

## 6. 最小示例：两端用一对veth通信

以下仅用于专用Linux实验VM。先运行ip netns list和ip link show确认没有本次同名对象；如果已有ncl-left、ncl-right、ncl-l0或ncl-r0，不要覆盖，应先确认来源。这里只创建新的虚拟对象，不使用实际管理网卡。示例未在本次编写中实跑。

~~~text
ncl-left                              ncl-right
ncl-l0 10.200.1.1/24 ←── veth对 ──→ ncl-r0 10.200.1.2/24
~~~

第一步创建两套网络环境：

~~~bash
sudo ip netns add ncl-left
sudo ip netns add ncl-right
~~~

add表示创建，两个名称可自定义。空间刚创建时没有外部连线，也没有默认路由。它有自己的lo回环接口，但通常需要启用。

第二步创建一对接口，并把每端移入对应空间：

~~~bash
sudo ip link add ncl-l0 type veth peer name ncl-r0
sudo ip link set ncl-l0 netns ncl-left
sudo ip link set ncl-r0 netns ncl-right
~~~

type veth指定设备类型，peer name给另一端命名，set ... netns把接口交给目标空间管理。移动后，宿主ip link show不再直接列出这两端，应进入目标空间查询。

第三步给端点配置地址并启用：

~~~bash
sudo ip netns exec ncl-left ip address add 10.200.1.1/24 dev ncl-l0
sudo ip netns exec ncl-right ip address add 10.200.1.2/24 dev ncl-r0
sudo ip netns exec ncl-left ip link set dev lo up
sudo ip netns exec ncl-right ip link set dev lo up
sudo ip netns exec ncl-left ip link set dev ncl-l0 up
sudo ip netns exec ncl-right ip link set dev ncl-r0 up
~~~

address add配置地址，link set ... up启用接口。它们是不同操作：有地址不代表接口已启用。两端同网段，不需要为这次直连通信添加默认网关，也不需要宿主开启IP转发。

第四步测试并观察：

~~~bash
sudo ip netns exec ncl-left ping -c 3 10.200.1.2
sudo ip netns exec ncl-left ip route show
sudo ip netns exec ncl-left ip neigh show
~~~

ping的-c 3限制发送次数，避免持续占用终端。成功的预期是3次回应；路由表应包含10.200.1.0/24的直连路径；邻居表可能出现对端IP与MAC。若失败，依次查接口所在空间、双方状态、地址与邻居，而不是立刻修改宿主默认路由。

## 7. Linux bridge怎样把多个端点接起来

两个端点可直接接veth；三个以上端点需要一个二层连接点时，可让多对veth的一端接到bridge，另一端分别放入端点空间。

~~~text
端点A的接口 ─ veth对 ─ 网桥端口a ┐
端点B的接口 ─ veth对 ─ 网桥端口b ├─ br-lab
端点C的接口 ─ veth对 ─ 网桥端口c ┘
~~~

br-lab是示例网桥名称，不是Linux固定关键字。网桥可以按源MAC学习、按目的MAC转发。若它只承担二层交换，未必需要给网桥配IP；若Linux自身要成为该网络的三层端点，地址才放在相应三层设计位置。

ip命令管理接口；bridge命令查询二层转发/VLAN等状态，也来自iproute2工具集：

~~~bash
ip -d link show type bridge
bridge link show
bridge fdb show
bridge vlan show
~~~

-d要求详细输出，type bridge限制设备类型；bridge link列端口，fdb是forwarding database转发表，vlan显示相应VLAN信息。请在网桥所在空间执行，命令不会替你穿越所有namespace。[Linux bridge文档](https://docs.kernel.org/networking/bridge.html)

## 8. 三张表仍然分工不同

网桥FDB回答MAC在哪个端口；端点邻居表回答下一跳IP对应什么链路地址；路由表回答目的前缀怎么走。网桥学到MAC不能证明端点默认网关或应用正确。

bridge的VLAN filtering是二层域控制，VRF是三层域控制，namespace是网络状态隔离。一个master字段也不能直接解释成“VRF成员”：它可能指向bridge、bond或VRF等不同上层对象，需看类型。

## 9. 完整排错例：宿主正常，端点不能上网

当前最小示例本来没有提供互联网接入，失败是设计边界，不是Linux故障。要增加外部访问，至少补端点出口路由、路由/网桥设计、宿主相应转发与策略、回程；需要NAT时还要明确转换位置。

不要把“创建namespace”理解成“自动建立容器网络”。也不要为了上网随意把物理管理口加入实验网桥。先画路径，再按后续防火墙/NAT专题逐项验证。

## 10. 清理、练习与验收

本例没有后台服务，ping也会自行结束。清理前检查是否有后来启动的进程：

~~~bash
sudo ip netns pids ncl-left
sudo ip netns pids ncl-right
~~~

若有PID，应确认并停止自己启动的实验进程，再删除这两个明确对象：

~~~bash
sudo ip netns del ncl-left
sudo ip netns del ncl-right
~~~

网络空间及其中veth的释放取决于是否仍被进程等持有；删除名字不等于杀死全部进程。清理后检查ip netns list和宿主接口，不能使用全局删除所有namespace的命令。

自测：两个空间都叫main是否共用路由？答案：不是。veth是否提供ASIC buffer仿真？答案：不提供。多端点网桥是否自动是网关？答案：不是。ip netns list空是否排除所有隔离空间？答案：不能。

交付：对象关系图、两端地址/路由/邻居、一次端点关闭引发的故障观察与恢复。进一步VLAN和bond见本专题的[第二篇](02-VLAN-and-Bonding.md)。
