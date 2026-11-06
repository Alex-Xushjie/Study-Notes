# Rail、容量与故障后的通信

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. Rail依据节点内部映射

Rail设计常按GPU/NIC/节点内互联和通信模式组织相应网络。不能把“两张NIC接两Leaf”自动等同Rail-optimized，更不能默认双路透明无损切换。作业Rank、GPU、NIC与网络平面应有明确映射。

## 2. 教学端口模型

假设125台服务器、每台8个400G端点映到8个独立Rail，每Rail125端点；每Leaf有32下行/32上行400G，则每Rail至少ceil(125/32)=4Leaf。每Rail若4Spine、每Leaf向每Spine8链，Leaf上行共32条。

每Rail Leaf-Spine链为4×32=128，8Rail为1024；服务器链共1000，合计2024。每链两端独立可插拔收发器的假设下为4048个。DAC/AOC/Breakout会改变BOM，不直接用于采购。

## 3. 正常与N-1

满接入Leaf下行32×400G=12.8Tb/s，上行相同。失去一个Spine后上行24条，下行/上行=32/24≈1.33:1。一个Rail的第4Leaf仅接29端点，实际切面负载又不同。

这些仅为指定拓扑端口可行性。真正Bisection、芯片/Hash、端点、跨Rail通信、库调度与作业恢复必须验证，不因算出1:1就宣称无阻塞性能。

## 4. 练习

画GPU→NIC→Rail→Leaf/Spine和跨Rail需求，给出扩容单位、布线、故障后容量与管理/存储独立性。失败一个NIC/链路时，作业是否重试/重启/绕行由实际软件和设计决定。

[1000GPU教学方案与完整假设](../../../Network-Career-Lab/06-AI-HPC/02-Design-and-Labs.md)、[Clos容量基础](../../10-Data-Center-Networking/01-Clos-Underlay-and-ECMP/02-Oversubscription-ECMP-and-N-1.md)。
