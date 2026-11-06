# AIDC分档实验与能力边界

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 无GPU也能完成的工作

画端点—队列—反馈链、GPU/NIC/NUMA映射假设、Rail端口与N-1预算、光连接核对与RCA推演。Soft-RoCE可学习部分API/资源，不证明真实NIC、ASIC拥塞和GPU传输性能。

配套[AI/HPC实验H1–H4](../../../Network-Career-Lab/06-AI-HPC/02-Design-and-Labs.md)包含明确的1000GPU教学模型，不能标成NVIDIA参考设计或真实交付项目。

## 2. 硬件分档

| 阶段 | 环境 | 证据 |
|---|---|---|
| H1 离线 | 拓扑/数据表 | 算法/反馈方向、公式和未知项 |
| H2 两NIC | 专用Linux/RDMA端点 | 链路、Host Memory读写、消息/并发 |
| H3 GPU路径 | 兼容GPU/NIC/驱动 | 支持矩阵、实际GDR与正确性 |
| H4 Collective | 合法多节点环境 | Rank/消息/负载、busbw与作业 |
| H5 拥塞/故障 | 隔离Fabric | PFC/ECN/重试、恢复与未覆盖项 |

每阶段先基线再反例，不擅自占用共享GPU、修改驱动/固件或停止生产作业。失败恢复和还原原值是实验步骤。

## 3. 综合设计

按125台×8GPU教学输入，完成Rail、端口、光连接、管理/存储、QoS映射、端点支持与容量。补充跨Rail与节点内互联假设，列单NIC/链路/Spine失效时哪些作业行为仍需验证。

## 4. 职业定位

现阶段以“能解释、能看证据、能联合排障”为合理拓宽目标，优先投入既定组播/低延迟/Linux或企业WAN/云主线。若未来取得真实资源/项目，再用实测补充，不用纸面方案声称多年HPC经验。

## 5. 结课产物

反馈链图、拓扑与BOM假设、Host/GPU/RDMA测试矩阵、三类RCA及环境能力说明。读完不是熟练调GPU，工具通过也不是生产规模保证。

[实验报告模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。本次没有GPU/RDMA硬件实验或性能结论。
