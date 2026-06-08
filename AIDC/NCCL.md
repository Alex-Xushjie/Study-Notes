# NCCL通信调度环
## NCCL通信原语
我们可以把NCCL看作一个SDN控制器，NCCL是一个可以自动发现GPU间物理连接“地图”（拓扑）并规划最优“运输路线”的系统。它通过拓扑感知和自适应算法选择，在复杂的GPU互连网络（如NVLink、PCIe、InfiniBand、RoCE）中，为分布式训练任务动态规划出最优的数据传输路径。

NCCL还定义了一些计算节点之间数据交换的基本操作模式，并将其命名为——通信原语。

这些通信原语包括：Boradcast、Scatter、Gather、All-Gather、Reduce-Scatter、All-to-All等
1) Broadcast(1对多的广播)

    Broadcast是一个典型的分发、散播行为。在分布式机器学习中，Broadcast常用于模型初始化或参数同步。

2) Scatter(1对多的散发)

    Scatter也是一种分发、散播行为。它也是将主节点的数据发送至其他所有节点。只不过，Broadcast发送的是完整数据，而Scatter是将数据进行切割后，再分发。

3) Gather(多对1的收集)
    
    Gather是将多个sender上的数据收集到单个节点上，可以理解为反向的Scatter

4) All-Gather

    Gather是多个到一个，All-Gather是多个到多个。也就是将多个sender上的数据收集到多个节点上（每个节点都有所有的数据，相当于多个Gather操作，或者一个Gather操作之后，跟着一个Broadcast操作）

5) Reduce

    在CCL（集合通信）里，Reduce表示“规约”运算，是一系列简单运算操作（包括：SUM、MIN、MAX、PROD、LOR等）的统称。

6) All-Reduce(多对多的规约)

    这是AI训练最核心的通信之一！类似All-Gather和Gather的关系，All-Reduce就是多对多的Reduce

7) Reduce-Scatter(组合的规约与发散)

    先规约(Reduce)，再发散(Scatter)

8) All-to-All

    这是AI训练最核心的通信之二！


