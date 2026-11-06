# RDMA、RoCE与InfiniBand基础

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. RDMA是访问/传输能力体系

RDMA可让兼容端点在受控内存/连接上下文中进行远程内存操作，减少相应CPU拷贝/协议处理。它不是某一种线缆或“UDP跑得快”的别名。应用与库仍需正确建立资源和处理完成/错误。

RoCEv1与以太二层相关，RoCEv2基于UDP/IP支持相应三层部署，常见UDP目的端口4791按实现核对。InfiniBand有自身链路、寻址/路由、子网管理与服务，不能把以太交换机PFC命令套到IB。

## 2. 选择维度

| 维度 | 需要比较 |
|---|---|
| 既有运维 | Ethernet/IP与IB工具、团队和供应链 |
| 应用 | 支持的库、传输、消息和规模 |
| 拓扑/拥塞 | 路由、隔离、反馈、恢复与故障域 |
| 端点 | NIC/GPU/驱动与固件支持 |
| 成本/运营 | 光连接、软件、管理与可观测性 |

端到端可靠性由所用传输和端点机制共同决定，不把“可靠传输”当永不拥塞/丢包。RoCE也不应统一断言必须开启全网PFC才能运行；可用模式与目标性能需按硬件/拥塞方案验证。

## 3. 基础验证

先链路/速率/错误，再IP/GID或IB相应寻址/子网管理，再RDMA连接和读写，最后GPU/Collective。IP ping可达不证明RDMA资源与端口正确；RDMA工具端口的TCP协商也不必代表数据全部走TCP。

## 4. 练习

对两种Fabric分别画寻址、管理、数据和拥塞/恢复链。选一种平台做合法隔离PoC，没有设备时完成模型比较，不把选型讨论当性能结论。

[rdma-core](https://github.com/linux-rdma/rdma-core)、[perftest](https://github.com/linux-rdma/perftest)、[NVIDIA RoCE文档](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/)。
