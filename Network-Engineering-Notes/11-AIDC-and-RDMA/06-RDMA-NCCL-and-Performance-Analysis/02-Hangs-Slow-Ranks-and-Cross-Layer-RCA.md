# 作业挂起、慢Rank与跨层RCA

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 不先强制参数

Collective调用不一致、启动器/容器、权限/共享内存、设备错误、错误网卡、传输回退、拓扑和拥塞都可能表现为慢或挂。先确认所有Rank是否启动并到达相同操作，再查实际路径。

## 2. 分层症状

| 症状 | 区分证据 |
|---|---|
| 单机正常多机失败 | 启动/地址、网卡、RDMA/Socket与访问 |
| Host RDMA好GDR差 | GPU/NIC拓扑、注册与支持 |
| 小消息差大消息好 | 启动/同步/CPU与时延路径 |
| 单对好并发差 | 拥塞/反馈、Hash热点和端点资源 |
| 网络空闲作业慢 | 计算/存储/某Rank未到同步 |
| 调参后结果变 | 确认实际协议/算法是否也改变 |

## 3. 日志与环境变量

按官方诊断先收小范围、限时日志，关联Rank/Host/时间与作业版本。调试变量可能改变性能、回退和稳定性，不长期全局启用，也不逐条TRACE所有通信。删除临时设置后复测基线。

NCCL_SOCKET_IFNAME等控制相应接口选择，不等于所有RDMA设备与GDR路径都由同一变量决定。不要盲填固定GID索引或拷贝他人算法参数，版本/自动选择能力可能不同。

## 4. RCA练习

案例多对一吞吐下降且Pause高、ECN/CNP少。候选映射错误、标记/端点反馈失效、接收端资源不足；分别写发送、交换、接收与作业证据。恢复映射后改善还要排除负载/Rank变化。

## 5. 交付

提供版本、拓扑、启动命令/脱敏环境、消息/Rank矩阵、网络计数差值、GPU/CPU与正确性。明确网络/主机/应用谁能确认哪层事实，不把低吞吐全部归PFC。

[NCCL故障定位](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)、[环境变量与调试边界](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)。
