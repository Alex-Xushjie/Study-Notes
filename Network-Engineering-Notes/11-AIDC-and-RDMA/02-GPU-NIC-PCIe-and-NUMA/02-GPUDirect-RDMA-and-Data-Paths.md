# GPUDirect RDMA与实际数据路径

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 避免把名字当保证

GPUDirect RDMA让兼容第三方设备与GPU内存之间进行相应数据传输，减少某些主机内存中转。仍需CPU/系统设置和内存注册等工作，不是“完全不经CPU”或任意NIC/GPU组合都可用。

驱动、CUDA、内核、NIC固件、PCIe拓扑、IOMMU/ACS与内存共享机制支持都会影响；DMA-BUF与nvidia-peermem等路径有不同条件。按当前版本官方支持验证，不从旧教程抄全局禁用IOMMU等参数。

## 2. 三种成功不同

GPU计算成功、主机内存RDMA成功、GPU内存RDMA成功分别证明不同链条。通信库可能回退到Socket或其他路径，吞吐正常也不代表用到了期望的GDR。

| 测试 | 能证明与不能证明 |
|---|---|
| 本机多GPU | 节点内部分能力，不证明网络 |
| 两机Host Memory RDMA | NIC/Fabric部分路径，不证明GPU注册 |
| GPU Memory RDMA | 相关组合路径，还需多机Collective |
| NCCL端到端 | 作业场景表现，需核对实际传输/拓扑 |

## 3. 排障

从设备健康、版本/支持、拓扑、内存注册、权限和实际传输日志逐级看。小消息与大消息可能走不同路径，不用一条环境变量强制“开GDR”就认为问题解决。

## 4. 练习

建立支持矩阵和证据表，比较Host/GPU内存、单机/跨机、不同NUMA位置。没有相应硬件时只写待验证，不能用Soft-RoCE或普通TCP冒充GDR性能。

[GPUDirect RDMA官方手册](https://docs.nvidia.com/cuda/gpudirect-rdma/)、[NVIDIA GPU Operator的RDMA条件](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-operator-rdma.html)。
