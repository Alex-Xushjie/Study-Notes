# 通信模式、算法带宽与总线带宽

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 延迟与带宽两个区域

小消息更易受启动/同步开销影响，大消息更易受持续带宽、拓扑和拥塞限制。集合通信算法可能采用Ring、Tree或层次结构，通信库会按条件选择，不能用单一算法公式当所有结果标准。

## 2. Ring教学模型

假设n个Rank，每Rank待聚合数据M字节，理想Ring AllReduce中每Rank传输量可按2(n−1)/n×M理解。n=8、M=1GB十进制时为1.75GB，未计协议开销、重传或层次结构。这是指定算法模型，不是整个集群物理总线字节计量。

nccl-tests的algbw与busbw具有不同归一化定义；AllReduce常按busbw=algbw×2(n−1)/n换算。busbw不是直接读取某端口实际吞吐，也不能不分操作种类套同一因子。

## 3. 模式与瓶颈

| 模式 | 关注 |
|---|---|
| 同步迭代 | 最慢Rank与尾部放大 |
| 多对一/Incast | 出口排队、端点接收与反馈 |
| 多对多 | Bisection、Hash与链路热点 |
| 节点内+节点间 | 本地互联与NIC分配的协作 |
| 计算通信重叠 | 时序、CPU与异步执行能力 |

## 4. 验证

对相同Rank数/布局、消息大小与类型比较，并保留warmup、迭代数、正确性和工具版本。改变GPU数同时改变通信量时，不把吞吐差直接归网络。

## 5. 练习

计算n=2/4/8时Ring因子，并解释单GPU本机测试为什么无法证明节点间RDMA。报告公式假设和未测部分，不承诺达到端口标称值。

[nccl-tests及带宽说明](https://github.com/NVIDIA/nccl-tests)、[NCCL操作](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html)。
