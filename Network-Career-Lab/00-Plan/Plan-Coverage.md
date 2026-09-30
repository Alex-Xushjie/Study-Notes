# 原计划覆盖对照

来源：用户提供的 Word 历史对话；其中学习计划重复出现，内容一致，按末尾完整版本整合。原始职业目标保留为方向，不复制未经核实的个人经历、薪资或招聘现状。

| 原计划 | 新材料与定位 |
|---|---|
| Phase 1 W1–6：ip/ss/tcpdump/ethtool/neigh/DNS/traceroute | [Linux 教材](../01-Linux/01-Packet-Path.md) 命令表 |
| namespace、static route、Linux routing、VLAN、bonding | [Linux 实验](../01-Linux/02-Labs.md) L1/L4 |
| policy routing、nftables/iptables、systemd/journalctl | Linux 教材与 L2/L5 |
| BGP、MTU、非对称、TCP 重传 | MTU/重传在 L3；非对称扩展在 L5；BGP 实跑并入 Edge E1，避免重复搭建 |
| NIC queue/offload/RSS/IRQ/affinity | Linux 教材末节 + Trading T3 |
| Phase 2 W4–8：Python/JSON/YAML/regex/requests/exception | [自动化教材](../02-Automation/01-Learning-Guide.md) |
| Netmiko/NAPALM/API/Jinja2/Ansible/Git | 自动化教材与 [项目](../02-Automation/02-Project.md) |
| inventory→采集→状态分析→CSV/JSON | 可运行离线程序 + 实机 adapter 作业；不假装已连设备 |
| YAML→生成→下发→验证 | 可运行离线渲染 + 实验设备下发与回退步骤 |
| 12 项健康检查 | 项目 B 的指标/来源/判定表；起步代码实现 BGP，其余为渐进练习 |
| Phase 3 W7–12：AWS 全部列出的网络对象 | [AWS/Azure 教材](../03-Cloud/01-AWS-Azure.md) 与 C1/C4 |
| Azure 全部列出的网络对象、hub-spoke/ER | 同上与 C2/C3 |
| Phase 4 W10–15：Transit/Peering/IXP/策略/过滤 | [Edge 教材](../04-Internet-Edge/01-Design-and-Security.md) 与 E1/E2 |
| IRR/RPKI/ROA、RTBH/FlowSpec/清洗 | Edge 教材与 E3 |
| Phase 5 W13–18：eBGP/MP-BGP/VTEP/VNI/Type 2/3/5 | [DC 教材](../05-Data-Center/01-EVPN-VXLAN.md) 与 D1–D3 |
| Anycast GW、ARP suppression、BUM、MLAG/ESI/DF | DC 教材与 D4；补充 multihoming 的 Type 1/4 |
| Enterprise DC 与 L3 to server | DC 架构比较作业 |
| Phase 6 W17–22：RDMA/RoCEv2/IB/PFC/ECN/DCQCN | [HPC 教材](../06-AI-HPC/01-RDMA-and-Congestion.md) 与 H1/H3 |
| Clos/ECMP/oversubscription/rail/incast/elephant | HPC 教材与 H2 容量例题 |
| 400G/800G/QSFP-DD/OSFP/breakout/optics | H4 两端兼容与 BOM 核对表 |
| 1000 GPU 20 分钟设计 | H2 + 阶段验收 |
| Phase 7 W20–24：Market connectivity/colo/MD/OE/A-B | [Trading 教材](../07-Trading/01-Market-Data-and-Latency.md) 与 T1 |
| Multicast/PIM/IGMP | T1 复用原有组播教材与手册 |
| 延迟组成、cut-through、PTP、HW timestamp | Trading 教材与 T2/T3 |
| DPDK/Onload/NIC/CPU pinning | Trading 概念与实验变量；专用硬件实现为扩展 |
| 每周理论/Lab/排错/英文/设计 | [路线表](24-Week-Roadmap.md)、[作品集](../08-Portfolio/Design-and-Interview.md) |

## 调整说明

- 保留七阶段原始周次，重叠时明确主线/副线，总预算不叠加。
- 原计划称每周 8–10h，但所列分项合计 9–10h，给出 8h 缩减方案。
- 将“GPU 不能用 TCP”改成按工作负载比较 TCP 与 RDMA。
- 将 DX→TGW 简图补上 transit VIF/DXGW，避免照图遗漏逻辑组件。
- 不把 24 周写成全部方向达到专家级；先过验收再扩展。
- 认证、Kubernetes internals、全栈 DevOps、Java/Go、深度无线/SD-WAN 仍按原计划暂缓。
- Solutions Engineering 用原对话的目标贯穿练习，不增加每周总时长。Terraform/CI 作为自动化和云之后的选学。
