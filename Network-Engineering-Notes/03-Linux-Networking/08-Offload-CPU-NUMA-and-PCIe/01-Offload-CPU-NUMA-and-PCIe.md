# Offload、CPU、NUMA与PCIe

[Linux学习目录](../Linux-Networking.md)

## 1. Offload是什么意思

Offload可译为卸载：把某些工作交给更合适的位置完成，例如让NIC计算校验和或完成分段。它不是“绕过所有内核”的统一功能，也不是一组永远应该关闭的开关。

先理解正常目标：减少重复处理和CPU成本，提高批量效率。然后理解代价：主机观测位置看到的可能是未完成分段/校验的逻辑对象，批量处理也可能改变等待。

## 2. 常见功能逐个解释

| 名称 | 第一遍的理解 | 对观测的影响 |
|---|---|---|
| TX checksum offload | 发出前让设备完成相应校验工作 | 本机抓包可能早于实际完成 |
| TSO | TCP segmentation offload，让设备分割较大数据块 | 本机可能看到大逻辑包 |
| GSO | generic segmentation offload，在软件路径延后分段 | 不等于所有分段都由NIC完成 |
| GRO | generic receive offload，在接收路径聚合相应包 | 上层看到的处理单元可能更大 |
| VLAN相关offload | 某些标签处理/信息由设备辅助 | 本机抓包中标签可见性可能变化 |

这些是职责模型，不是说任何设备都支持。TSO和checksum等可能存在依赖，驱动也可能标记某些能力fixed不可改。原理见[分段卸载](https://docs.kernel.org/networking/segmentation-offloads.html)与[校验卸载](https://docs.kernel.org/networking/checksum-offloads.html)。

## 3. 怎样查看而不是盲目关闭

~~~bash
ethtool -k ens160
ethtool -c ens160
ethtool -i ens160
~~~

-k显示特性，-c显示中断合并，-i显示驱动。小写查询与大写-K/-C配置不同，大小写不能混用。ens160必须替换为实际接口。[ethtool手册](https://man7.org/linux/man-pages/man8/ethtool.8.html)

教学片段：

~~~text
tx-checksumming: on
tcp-segmentation-offload: on
generic-receive-offload: on
~~~

on只说明该项当前启用，不能证明它是性能问题来源。某些条目还会有子项、fixed或unsupported，记录完整输出而非只摘一个开关。

## 4. 抓包“校验和错误”案例

发送主机抓到TCP checksum提示异常，接收端业务正常。候选解释是抓包发生在NIC填充校验之前。对比接收侧或适当外部观测，再核对offload；不能只在发送端看到提示就更换光模块。

若确有线上错误、接收校验丢弃与异常相关，才继续调查真实损坏和处理链。反例很重要：不是所有checksum错误都可被offload解释。

同理，主机pcap有超过1500的逻辑数据块，不证明线上发出了相同大小帧。MTU、分段点与抓包点必须一起说明。

## 5. CPU核心与逻辑CPU

Socket在硬件拓扑里可指处理器插槽，与网络socket不同；Core是物理核心；Thread/logical CPU是系统调度可见的逻辑执行单元。SMT使一个物理核心可能对应多个逻辑CPU，但共享部分执行资源，不等同再增加一颗完整物理核心。

~~~bash
lscpu
lscpu -e=CPU,CORE,SOCKET,NODE
~~~

lscpu读取处理器信息，-e以扩展格式列出指定列。先建立逻辑CPU→Core→Socket→NUMA node关系，再选亲和性。VM显示的是虚拟配置，未必反映宿主真实拓扑。[lscpu说明](https://man7.org/linux/man-pages/man1/lscpu.1.html)

## 6. NUMA为什么影响网卡访问

NUMA是non-uniform memory access非一致内存访问。不同CPU访问不同内存位置的成本可能不同；NIC也经某个PCIe路径连接系统。应用线程、内存与NIC跨节点时，可能产生额外访问开销。

~~~bash
cat /sys/class/net/ens160/device/numa_node
~~~

/sys是内核向用户空间呈现设备对象的接口，numa_node说明相应设备的节点信息。-1通常表示未提供已知节点，不能当作“节点-1”；虚拟网卡可能根本没有这个文件。先确认能力，不随意把结果改写为0。

有numactl工具时，numactl --hardware可查看节点/CPU/内存信息；这是查询，不是给进程迁移内存。绑CPU也不保证已有内存随之移动，内存策略和分配时机需要独立观察。[CPU拓扑资料](https://docs.kernel.org/admin-guide/cputopology.html)

## 7. 亲和性：固定在哪里运行

Affinity是允许某个任务运行的CPU集合。Linux调度器在允许集合内安排执行。查看实际PID的亲和性：

~~~bash
taskset -cp 1234
~~~

这里1234是待替换的PID，-p针对已有任务，-c用CPU列表而非位掩码。查询主线程不代表已核对所有线程，多线程应用应检查各TID及其职责；TID是thread ID线程编号。

同一个物理核心的两个SMT线程也会争用资源。不要把IRQ、接收处理和繁忙应用全部机械地压在同一逻辑CPU。[taskset参考](https://man7.org/linux/man-pages/man1/taskset.1.html)

本篇不下发生产绑核模板。调整前保存允许集合与服务配置，确认应用/管理器是否会重设，固定负载只改一个变量并恢复。

## 8. PCIe：线速之外还有主机总线

PCIe是设备与系统通信的高速互连。代际描述每lane传输能力，x8/x16描述lane数量；网卡接口100G并不保证主机侧一定能同时供给该流量。

~~~bash
lspci
lspci -s 0000:03:00.0 -vv
~~~

lspci列PCI设备；-s选实际设备地址，-vv显示较详细信息，可能需要权限。0000:03:00.0只是示例，先用ethtool -i的bus-info等关联真实NIC。LnkCap与LnkSta可帮助区分支持能力和当前协商状态，也要检查上游桥路径。

数量级例题：PCIe3每lane 8GT/s、128/130编码，x8每方向理论约8×128/130×8÷8=7.88GB/s，尚未扣传输协议开销。100Gbit/s相当于12.5GB/s线速数量级。普通主机数据路径若受此前者限制，不能只看100G端口就承诺满速。真实还受协议开销、读写路径及共享资源影响，不把算式当实测。

## 9. 调优对比应该怎样做

先保存驱动/固件、offload、coalescing、队列、CPU/NUMA/PCIe与负载模型。固定消息大小、并发、时长和观察点，比较吞吐、pps、丢包、CPU与p99，而不是只挑一个变好的数字。

关闭GRO后吞吐下降，可能是CPU批处理成本变化，不证明原来GRO损坏包。绑核后平均延迟改善但尾延迟恶化，也不能宣布整体优化成功。

## 10. 作业与自测

交付硬件/虚拟拓扑图、能力查询表、一个调优假设及反证、原值和恢复计划。暂无物理机时仅做能力调查，明确不能证明真实NIC收益。

自测：两逻辑CPU是否一定两物理核？答案：不是。绑CPU是否自动移动全部内存？答案：不应假定。抓到大包是否一定MTU错误？答案：不是。NIC线速是否唯一吞吐上限？答案：不是。

本次未运行ethtool修改、绑核或硬件性能测试。
