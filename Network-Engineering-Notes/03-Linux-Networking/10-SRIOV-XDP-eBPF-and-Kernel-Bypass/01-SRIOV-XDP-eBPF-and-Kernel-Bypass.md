# SR-IOV、eBPF/XDP与内核旁路

[Linux学习目录](../Linux-Networking.md)

## 1. 先回答为什么需要改变普通路径

前面已经学过NIC、驱动、协议栈和socket。只有确认瓶颈与目标后，才考虑虚拟化直通、内核可编程处理或用户态数据面。它们解决的问题不同，不是一套“全部打开就最快”的配置。

本篇目标是能说明组件、适用条件、观测位置和部署代价。完整驱动开发、BPF程序开发与生产级DPDK应用不属于第一次阅读的前提。

## 2. 三类机制放在一张图中

~~~text
普通路径：NIC → 驱动/内核网络处理 → socket → 应用

SR-IOV：NIC提供PF/VF等设备功能 → 分配给相应主机/虚拟环境

eBPF/XDP：在支持的内核/驱动挂点执行受约束程序

AF_XDP：通过XDP重定向与共享缓冲等机制把报文交给用户态程序

DPDK：应用使用相应驱动和库组织高性能数据面，路径依实现而异
~~~

SR-IOV关注设备虚拟化，XDP关注早期报文处理，DPDK关注用户态数据面编程模型。它们可以组合，但不互为替代。

## 3. SR-IOV、PF、VF是什么

SR-IOV是PCIe的一类I/O虚拟化能力。PF是physical function，通常承担完整设备管理等职责；VF是virtual function，提供可被分配的设备功能。不是把一个接口简单复制几个名字，也不是每个VF都拥有独立物理端口和全部链路带宽。[Linux SR-IOV文档](https://docs.kernel.org/PCI/pci-iov-howto.html)

虚拟机可通过相应平台分配使用VF，减少某些软件转发环节。但还需考虑IOMMU、驱动/固件、队列与资源分配、迁移和安全策略。IOMMU用于设备DMA地址转换/隔离等，VFIO是在Linux中提供相应用户态设备访问的框架；不能把这些名字当一个开关。[VFIO说明](https://docs.kernel.org/driver-api/vfio.html)

只读调查可用：

~~~bash
ethtool -i ens160
lspci -nn
ip -d link show dev ens160
cat /sys/class/net/ens160/device/sriov_totalvfs
cat /sys/class/net/ens160/device/sriov_numvfs
~~~

lspci的-nn显示名称与数值标识。totalvfs表示相应设备暴露的VF上限，numvfs是当前创建数；这些文件不是所有设备都有。没有文件可能是硬件、驱动、功能或当前对象条件不同。

此处不向sriov_numvfs写值，也不对管理口解绑驱动。实际创建/分配VF要按专用设备与虚拟化平台演练，确认恢复入口和业务影响。

## 4. eBPF：在受控位置运行程序

eBPF是一套可在支持位置运行受约束程序的机制。Loader是加载器，负责把程序交给内核；verifier是验证器，检查相应安全约束；map是用于保存与共享状态的数据结构。可以用于观测、过滤、路由相关处理等，能力取决于程序类型和内核支持。

验证通过不等于业务逻辑正确，也不保证零开销。程序仍可能错误丢弃合法包、统计口径不合适或增加处理成本。权限、资源和撤销方式都属于部署条件。[内核BPF入口](https://docs.kernel.org/bpf/index.html)、[maps](https://docs.kernel.org/bpf/maps.html)

安装了bpftool时可查询：

~~~bash
sudo bpftool prog show
sudo bpftool map show
sudo bpftool net
~~~

prog是程序，map是存储对象，net查看相关网络挂载。看见程序ID只能说明存在相应对象，不证明它正处理目标接口的所有报文；要核对挂点和引用。不要为排错直接卸载所有BPF程序。

## 5. XDP在哪里处理报文

XDP是eXpress Data Path。native/driver模式通常在驱动接收早期处理，generic模式走更通用的软件位置，offload模式需相应设备支持。不同模式的能力和成本不同，不能笼统宣称任何XDP都在同一个精确位置。

常见动作可理解为PASS继续相应正常路径、DROP丢弃、TX从接收设备相应发回、REDIRECT重定向。实际行为依程序与模式，部署需要完整路径设计。[Cilium项目对XDP类型的说明](https://docs.cilium.io/en/stable/reference-guides/bpf/progtypes/)

~~~bash
ip -d link show dev ens160
~~~

先查看是否有XDP关联等线索，再结合bpftool。若报文在早于普通捕获点的XDP路径丢弃，tcpdump可能看不到它；“pcap没有包”不能直接推断上游未发送。需要程序计数、设备计数或外部观测相互印证。

## 6. AF_XDP与zero-copy不是同义词

AF_XDP提供面向高性能报文处理的socket地址族。应用使用UMEM等共享缓冲区域，并通过队列/ring组织接收与发送，XDP程序可把报文重定向到对应socket。[内核AF_XDP文档](https://docs.kernel.org/networking/af_xdp.html)

copy与zero-copy模式受驱动、设备和配置支持限制。zero-copy表示减少相应数据拷贝，不代表不消耗CPU、不处理描述符或不需要内存。队列匹配、buffer生命周期和CPU位置仍会成为瓶颈。

## 7. DPDK与Poll Mode Driver

DPDK是用于构建数据面应用的一组库和框架，不是安装后普通socket程序就自动提速的服务。PMD是poll mode driver轮询模式驱动；应用常主动轮询队列以降低某些通知成本，代价可能是持续占用CPU和功耗。[DPDK架构概览](https://doc.dpdk.org/guides/prog_guide/overview.html)

EAL是environment abstraction layer，提供环境相关初始化等支持；mbuf是报文缓冲对象，mempool管理对象池，ring用于相应队列/核心之间交换工作。先认识职责，不需要立即学习全部C接口。

有些NIC/驱动采用需要不同设备绑定的模型，有些使用bifurcated等协作方式，不能统一要求所有设备先从Linux驱动解绑。队列所有权、路由、安全、监控和抓包方式也会改变，应查相应PMD和版本文档。

## 8. 内核旁路要承担哪些原有职责

普通TCP/UDP应用依赖内核提供协议、路由、缓冲与工具可观测性。改变路径后，需要明确哪些职责仍由内核承担，哪些改由应用、库、设备或控制面负责。

某些socket加速方案试图保持应用接口兼容，DPDK应用通常显式使用数据面API，不能把二者视为同一种改造。也不应给任意应用套一个启动命令就承诺微秒收益。

## 9. 选择表与反例

| 问题 | 可调查的方向 | 不能省略 |
|---|---|---|
| VM软件转发成本高 | SR-IOV等设备分配 | 隔离、迁移、交换与管理 |
| 早期过滤大量报文 | XDP | 分类正确性、计数与撤销 |
| 用户态高pps处理 | AF_XDP/DPDK等 | 驱动、内存、队列与应用模型 |
| 普通业务TCP慢 | 先查窗口、丢包、CPU和应用 | 不跳过前面性能分析 |

例：数据库磁盘慢，换成DPDK不会自动解决；单流受远端速率限制，增加VF不会创造带宽；XDP丢包后改大socket buffer也没有作用，因为包尚未走到那里。

## 10. 没有硬件也能完成的作业

画出普通、XDP、AF_XDP/DPDK和VF分配路径，标出抓包点、队列、CPU、状态管理和安全边界。列出每种方案需要的硬件/内核/驱动条件及一种不适用场景。

具备专用硬件后再做能力确认→单端点连通→固定负载→队列/CPU观察→失败恢复。不得用软件模拟结果证明物理直通或zero-copy性能。

自测：SR-IOV是否直接提供更多物理带宽？答案：不是。XDP是否等于跳过整个内核？答案：不是。DPDK是否自动加速未改造应用？答案：不能这样假定。zero-copy是否完全零开销？答案：不是。

本篇完成机制与方案边界学习，不提供未经平台确认的驱动解绑或生产部署脚本，本次也未执行这类变更。
