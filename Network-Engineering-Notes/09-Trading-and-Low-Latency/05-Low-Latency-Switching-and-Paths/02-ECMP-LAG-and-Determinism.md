# ECMP、LAG与路径确定性

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 按流Hash不是按需求均衡

LAG和ECMP常按相应字段Hash分散流，少数大频道可能集中一条成员链路。组播复制、RPF/上游选择与单播Hash又不同。不能看聚合总带宽低就排除某成员拥塞。

同流的Hash字段、内外层、分片/隧道与Resilient Hash支持按平台核对。增删成员可能改变映射和包顺序；逐包喷洒虽然可分担，却可能增加重排与接收端处理。

## 2. 确定性目标

不等于固定一条无备份路径，而是正常/故障时行为可解释、可测量。按S/G/P或业务会话记录实际端口、物理路线和路径变化。必要的显式流分配需有维护成本与故障恢复设计。

## 3. 容量与不均

例如4×10G聚合总40G，一个12G流不能假定自动分到两条10G成员；具体流拆分机制如果存在需单独验证。多个频道的速率与pps不等，仅按频道数量均分也可能失衡。

## 4. 测量

采集每成员短时间窗的利用率、队列、丢弃和实际频道映射，比较正常/成员失效/恢复。N-1还要验证剩余路径的时延与缓存，而非只确认路由可达。

## 5. 练习

为8个不同速率频道分配4条实验链路，先推导可能的最坏碰撞，再用受控流测量。没有ASIC环境时标记只推导，不用软件veth的结果宣称商用设备Hash表现。

[LAG与Hash基础](../../01-Routing-and-Switching/03-Link-Aggregation-and-Multichassis/01-Link-Aggregation-and-Multichassis.md)、[组播ECMP](../../02-Multicast/04-RPF-and-Multicast-Routing/02-ECMP-VRF-and-Asymmetric-Paths.md)。
