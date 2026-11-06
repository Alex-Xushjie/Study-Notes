# RDMA、NCCL测试与指标解释

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 逐层测试

先设备/驱动/版本和拓扑，再链路/地址，再Host Memory RDMA，再GPU路径，最后多Rank/多节点Collective。单对工具高吞吐不证明大规模作业，单机多GPU成功也不证明网络RDMA。

| 层次 | 固定条件 |
|---|---|
| perftest | 设备/端口/GID、QP、消息、方向与时长 |
| GPU内存 | 驱动/CUDA、注册方式、拓扑与支持 |
| nccl-tests | Rank/GPU布局、消息、迭代、正确性和启动器 |
| 作业 | 计算、数据读入、同步与通信重叠 |

## 2. 运行前置

nccl-tests需要按项目说明构建，CUDA/NCCL/MPI等支持取决于模式。可先在专用实验GPU运行本机小规模测试；多节点需要正确启动/Rank分配与网络访问，不能只把-g改大就当跨机器测试。

示例命令仅在已构建的专用实验目录执行，消耗一块GPU，不是只读查询：

~~~bash
./build/all_reduce_perf -b 8 -e 1M -f 2 -g 1
~~~

这个单进程单GPU例子只验证部分环境/工具，不证明节点间带宽。不要在共享生产GPU上未经调度/授权运行。

## 3. 指标

同时保存time、algbw、busbw、正确性/错误、CPU/GPU状态及实际传输日志。带宽单位与归一化需查工具，不能直接与端口Gb/s对比而忽略字节单位/因子。

## 4. 练习

小/大消息、单机/多机、Host/GPU内存和不同Rank布局形成矩阵。重复测试保留最差与失败，不只截图最好一行。把工具与输出版本纳入报告。

[perftest](https://github.com/linux-rdma/perftest)、[nccl-tests](https://github.com/NVIDIA/nccl-tests)、[NCCL排障](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)。
