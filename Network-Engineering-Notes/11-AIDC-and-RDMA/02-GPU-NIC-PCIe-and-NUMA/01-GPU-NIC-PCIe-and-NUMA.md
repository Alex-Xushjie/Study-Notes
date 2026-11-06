# GPU、NIC、PCIe与NUMA拓扑

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 从熟悉的主机开始

PCIe连接CPU、NIC、GPU等设备；NUMA描述CPU/内存位置的访问代价。GPU内部/节点内的NVLink等互联与节点间网络是不同层次。网口400G不保证GPU到该NIC的路径同样无瓶颈。

| 对象 | 核对 |
|---|---|
| GPU | 型号、驱动、进程/Rank归属与健康 |
| NIC | 端口、PCIe位置、驱动/固件、速率和队列 |
| PCIe | 代际、通道数、实际协商、Root/交换路径 |
| CPU/内存 | NUMA节点、进程和注册内存位置 |
| 节点内互联 | 实际连接、支持和库识别 |

## 2. 只读拓扑命令

在有相应GPU/NIC的Linux实验机执行，工具缺失不代表硬件一定损坏：

~~~bash
lspci -t
lscpu
numactl --hardware
nvidia-smi -L
nvidia-smi topo -m
rdma link show
~~~

nvidia-smi依赖驱动，rdma来自相应用户态工具。输出缩写按该版本手册解释；GPU与NIC在不同Root/NUMA路径时，不能仅凭名称推断P2P可达或最佳性能。

## 3. 资源争用

NIC和GPU共享PCIe/CPU、存储读入、日志和后台任务都可能影响通信。限制管理/存储与训练混用，需要容量和实际业务证据，不单凭理论带宽。

## 4. 练习

画一台双CPU多GPU服务器到NIC的树，给出每Rank的CPU/内存/GPU/NIC映射。比较本地与跨NUMA路径的假设，未有硬件仅完成结构分析。

[GPUDirect RDMA拓扑限制](https://docs.nvidia.com/cuda/gpudirect-rdma/)、[Linux NUMA/Offload基础](../../03-Linux-Networking/08-Offload-CPU-NUMA-and-PCIe/01-Offload-CPU-NUMA-and-PCIe.md)。
