# Linux收包链、IRQ、队列与NUMA入门

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 先认识组件

NIC是网卡；DMA让设备把数据放到内存；Ring是驱动/硬件交换描述符的队列；IRQ是设备通知CPU的中断；NAPI是内核网络处理中结合中断与轮询的机制；Socket是应用收发接口；NUMA表示不同CPU访问不同内存位置的代价可能不同。

典型收包路径是NIC→相应队列/驱动→内核协议栈→Socket→应用，但Offload、XDP或旁路会改变路径。每层排队和调度都可能增加延迟/丢包，先识别瓶颈再改设置。

## 2. 分流与CPU

RSS由NIC按Hash分流到接收队列，RPS/RFS等在软件侧影响处理CPU，XPS影响发送队列选择。单个组播频道可能集中某队列，不能假定增加CPU就自动并行。应用线程、IRQ和内存放置需联合看，盲目全部绑同CPU也会竞争。

## 3. 只读清单

Linux实验主机执行，eth0先用ip -br link确认实际名称；某些虚拟NIC不支持全部查询：

~~~bash
ip -br link
lscpu
numactl --hardware
ethtool -i eth0
ethtool -l eth0
ethtool -g eth0
ethtool -c eth0
ethtool -k eth0
ethtool -S eth0
cat /proc/interrupts
~~~

-l查看队列/通道，-g查看Ring，-c查看中断合并，-k查看Offload，-S为驱动统计。输出单位、名字与支持因驱动而异。工具缺失是安装/能力问题，不证明网络故障。

## 4. 先做基线

保存内核、固件、驱动、NIC/PCIe与NUMA拓扑、CPU/频率、队列、Offload、进程/IRQ分布和负载。虚拟机调度可引入额外抖动，无硬件环境不要承诺真实NIC纳秒结论。

## 5. 练习

选择一个自建频道，关联队列、中断CPU、应用CPU和序号gap。先观察再做一个变量的实验，恢复原值。深入见[网卡队列](../../03-Linux-Networking/07-NIC-Queues-and-Packet-Processing/01-NIC-Queues-and-Packet-Processing.md)、[Offload/NUMA](../../03-Linux-Networking/08-Offload-CPU-NUMA-and-PCIe/01-Offload-CPU-NUMA-and-PCIe.md)。

[内核RSS/RPS等文档](https://docs.kernel.org/networking/scaling.html)、[ethtool手册](https://man7.org/linux/man-pages/man8/ethtool.8.html)。
