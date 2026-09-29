# 官方阅读资料索引

整理日期：2026-09-26。以下核心链接在整理时通过网页工具成功取得页面内容；链接可访问不等于你使用的设备版本已支持全部功能。以正文教材为第一遍，再读指定范围。`latest` 文档随时间变化，实施时切换到实际安装版本并记录。

## 必读：控制阅读量

| 阶段 | 官方来源 | 本轮只读什么 | 阅读产出 |
|---|---|---|---|
| Linux | [Linux networking scaling](https://docs.kernel.org/networking/scaling.html) | RSS/RPS、队列与 IRQ | 画队列到 CPU 路径 |
| Linux | [Linux bonding](https://docs.kernel.org/networking/bonding.html) | active-backup、802.3ad、monitoring | 写模式差异与对端要求 |
| Python | [Python Tutorial](https://docs.python.org/3/tutorial/) | 数据结构、文件、异常、模块 | 改写健康检查输入处理 |
| Ansible | [Network Getting Started](https://docs.ansible.com/projects/ansible/latest/network/getting_started/index.html) | inventory、连接、playbook | 解释控制端与设备职责 |
| AWS | [VPC Security](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Security.html) | 沿入口读 SG/NACL | 正反五元组规则表 |
| AWS | [How TGW works](https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html) | attachments、association、propagation | C1 三张路由表 |
| AWS | [DX Resiliency Toolkit](https://docs.aws.amazon.com/directconnect/latest/UserGuide/resiliency_toolkit.html) | 多地点模型与 failover test | 故障域清单 |
| Azure | [Hub-spoke topology](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke) | peering、routing、安全路径 | C2 双向路径 |
| Azure | [ExpressRoute disaster recovery](https://learn.microsoft.com/en-us/azure/expressroute/designing-for-disaster-recovery-with-expressroute-privatepeering) | geo-redundancy、非对称与故障考虑 | C3 失败模式表 |
| Edge | [FRR BGP](https://docs.frrouting.org/en/latest/bgp.html) | prefix-list、route-map、neighbor、max-prefix | 实验版本与实际命令 |
| Edge | [RFC 6811](https://www.rfc-editor.org/rfc/rfc6811) | 验证输入、三种状态 | 4 个 ROA 手算案例 |
| Edge | [RFC 8955](https://www.rfc-editor.org/rfc/rfc8955) | match、actions、validation | FlowSpec 风险与撤销方案 |
| DC | [RFC 8365](https://www.rfc-editor.org/rfc/rfc8365) | EVPN overlay 模型 | underlay/overlay 边界图 |
| DC | [RFC 9136](https://www.rfc-editor.org/rfc/rfc9136) | Type 5 与下一跳解析 | Type 2/5 对照 |
| DC | [FRR EVPN](https://docs.frrouting.org/en/latest/evpn.html) | Linux 接口模型和完整示例 | 本版本可复现配置 |
| HPC | [DCQCN 原始论文](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/lossless.pdf) | 问题、控制环、实验 | 一页反馈链，不照搬阈值 |
| HPC | [NVIDIA RoCE](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/) | 模式、QoS 映射与观测 | PFC/ECN/NIC 指标表 |
| HPC | [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests) | 构建依赖、运行方式、性能指标 | algbw/busbw 与环境记录 |
| Trading | [linuxptp ptp4l](https://www.linuxptp.org/documentation/ptp4l/) | timestamp、clock、domain/transport | 时间戳能力和配置假设 |

每次 20–30 分钟读一个问题；卡在一条命令时再查该平台文档。CLI 实施还要查本机 `man ip`、`man ip-rule`、`man ss`、`man tcpdump`、`man ethtool`，避免照搬其他版本输出。

## 本仓库的补充材料

- [Python 基础](../../NetDevOps/Python_Basic/Python_Basic.md)：查语法与模板。
- [AIDC 实验](../../AIDC/lab.md)：已有 RDMA 环境记录，按实际版本复核。
- [组播实验手册](../../Network-Engineering-Notes/02-Multicast/14-Lab-Manual/Lab-Manual.md)：T1 指定实验。
- [交易网络 10 天冲刺](../../Quant%20Trading/00-Crash-Course-Plan.md)：W24 后或临近相关面试时使用，不替代本学习顺序。
- [PTP](../../Quant%20Trading/02-Tier-2/03-PTP.md)：时间同步补充。
- [交易网络白板题](../../Quant%20Trading/90-Interview-Drills/03-Whiteboard-Cases.md)：综合练习。

未把旧目录中只有标题或空白的文件列为必读教材。新项目正文可独立起步；旧笔记的历史厂商功能和业务接口仍需按版本复核。
