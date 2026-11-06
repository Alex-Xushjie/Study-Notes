# 训练与推理通信：先认识Rank和Collective

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 网络工程师的学习边界

AIDC不只是GPU算力，还包括节点互联、存储、调度、通信库与可观测性。本部分按职业规划作为拓宽方向，重点理解通信需求与跨团队排障，不把阅读教材当作生产GPU集群经历，也不要求优先转做模型算法工程师。

GPU负责相应计算，CPU负责系统/调度等，NIC连接节点，通信库组织设备间数据。Rank是通信参与者标识，不能简单等同某台机器的GPU序号；进程、Rank、GPU映射按作业确定。

## 2. 常见操作

| 操作 | 概念 |
|---|---|
| Broadcast | 从指定Rank分发数据 |
| Reduce | 聚合后结果在指定Rank |
| AllReduce | 聚合结果供参与Rank使用 |
| AllGather | 各Rank的数据汇集到参与者 |
| ReduceScatter | 聚合后分片分配 |
| AllToAll | 参与者之间交换各自相应分块 |

不同并行策略会使用不同操作与消息分布。训练常有迭代同步/梯度等通信，推理还涉及请求、批处理、KV/cache或分布式计算等依赖，不用一个固定AllReduce模型解释所有应用。

## 3. 正确性优先

Collective参与、顺序、数据类型/数量与作业规则要匹配，错误可能表现为挂起而非网络链路告警。慢Rank、计算不均和存储等待会让网络空闲，不是所有低带宽都是Fabric问题。

## 4. 练习

画4Rank的数据流，解释AllGather与AllReduce结果区别。给出每Rank设备、进程、NIC与消息大小表，标计算/通信/等待时间，先建立协作语言再调参数。

[NCCL Collective官方说明](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html)。实际算法和传输由版本、拓扑、消息与配置等共同决定。
