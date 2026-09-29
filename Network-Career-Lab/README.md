# Network Career Lab：24 周网络工程师进阶学习项目

从传统路由交换出发，依次补齐 Linux、自动化、云网络、Internet Edge、现代数据中心、AI/HPC 和交易网络。面向 Network Architect / Principal / Solutions Engineer 等方向，学习目标是能设计、验证、排错并解释取舍。

本项目依据《我的目标就是百万年薪.docx》中的学习计划整理，2026-09-26 建立。文档内两次出现的相同计划已合并；以你明确说的“只有传统路由交换技术栈”为起点，不预设你已经掌握 RoCE、Python 或云网络。原对话中的薪资、招聘状态和“已设置追踪任务”不是本项目核实或执行的内容。

## 从这里开始

1. 阅读 [24 周路线与周任务](00-Plan/24-Week-Roadmap.md)，按相对周数开始，不必等待某个日期。
2. 按 [实验环境](00-Plan/Lab-Environment.md) 准备一台 Linux VM。
3. 学习 [Linux 数据路径](01-Linux/01-Packet-Path.md)，完成 [Linux 实验](01-Linux/02-Labs.md) 的 L1。
4. 每周填写 [进度记录](08-Portfolio/Progress.md)，每个实验保存一份 [实验记录](08-Portfolio/Lab-Report-Template.md)。

## 学习入口

| 阶段 | 原计划时间 | 教材 | 实验 / 交付物 |
|---|---|---|---|
| 1 Linux | W1–6 | [数据路径、命令与 NIC](01-Linux/01-Packet-Path.md) | [路由、MTU、VLAN、bond、排错](01-Linux/02-Labs.md) |
| 2 Automation | W4–8 | [Python 到 Ansible](02-Automation/01-Learning-Guide.md) | [网络健康检查与配置流水线](02-Automation/02-Project.md) |
| 3 Cloud | W7–12 | [AWS / Azure 网络](03-Cloud/01-AWS-Azure.md) | [混合云设计实验](03-Cloud/02-Labs-and-Design.md) |
| 4 Internet Edge | W10–15 | [运营商互联与路由安全](04-Internet-Edge/01-Design-and-Security.md) | [双 ISP 实验](04-Internet-Edge/02-Labs.md) |
| 5 Modern DC | W13–18 | [EVPN/VXLAN 与 Clos](05-Data-Center/01-EVPN-VXLAN.md) | [分层验证与故障注入](05-Data-Center/02-Labs.md) |
| 6 AI/HPC | W17–22 | [RDMA 与拥塞控制](06-AI-HPC/01-RDMA-and-Congestion.md) | [容量设计与测量](06-AI-HPC/02-Design-and-Labs.md) |
| 7 Trading | W20–24 | [交易链路与延迟](07-Trading/01-Market-Data-and-Latency.md) | [组播、测量与时钟](07-Trading/02-Labs.md) |

每周总计 8–10 小时，阶段重叠时共享这个预算，不是每阶段各花 8–10 小时。正文是第一遍教材；每篇末尾的官方文档只按指定主题阅读，不要求通读数百页。

## 完成的定义

每阶段留下一个可复核成果：拓扑、假设、配置或代码、验证输出、故障复现、恢复记录、5 分钟英文说明。只读完文章不算阶段通过。建议先完成所有核心题，再选做扩展；硬件不足时完成替代作业，并如实标记“设计验证”或“模拟数据”，不记录成实机性能结果。

- [设计与英文面试练习](08-Portfolio/Design-and-Interview.md)
- [官方资料索引与阅读范围](09-References/Reading-List.md)
- [与原计划的覆盖对照](00-Plan/Plan-Coverage.md)

本目录独立维护。已有笔记仅作为补充链接，未复制私人对话全文。24 周是入门到综合应用的训练周期，不代表所有方向都能在此时长内达到专家水平，也不是薪资承诺。
