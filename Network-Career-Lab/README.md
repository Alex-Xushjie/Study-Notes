# 网络职业提升教材：从路由交换到系统设计

2026-10-30 重编。以已有传统路由交换基础为起点，学习 Linux、自动化、云网络、Internet Edge、现代数据中心，并进入 AI/HPC 与交易网络专项。目标是能独立解释机制、完成验证、定位故障和说明架构取舍。

本版增加七章详细教材与职业学习方法。原有概念摘要、实验、代码和个人进度继续保留。详细教材负责讲“为什么与如何判断”，实验文档负责具体操作，两者配合学习。

## 推荐阅读顺序

先读 [职业方向、起点评估与学习方法](00-Plan/01-Career-and-Study-System.md)，再准备 [实验环境](00-Plan/Lab-Environment.md)。按 [24周任务表](00-Plan/24-Week-Roadmap.md) 安排主线，使用 [详细教材周阅读表](00-Plan/02-Textbook-Reading-Map.md) 找到每周章节。

| 顺序 | 详细教材 | 配套操作与交付 |
|---|---|---|
| 1 Linux | [TCP逐包路径、主机排错、MTU与性能](01-Linux/03-Detailed-Textbook.md) | [namespace、服务、过滤、VLAN/bond实验](01-Linux/02-Labs.md) |
| 2 自动化 | [Python、数据契约、失败处理与配置流程](02-Automation/03-Detailed-Textbook.md) | [健康检查和配置渲染项目](02-Automation/02-Project.md) |
| 3 云网络 | [地址、TGW、hub-spoke、DNS与混合云](03-Cloud/03-Detailed-Textbook.md) | [AWS/Azure设计与故障推演](03-Cloud/02-Labs-and-Design.md) |
| 4 Internet Edge | [路由策略、RPKI、DDoS与运行处置](04-Internet-Edge/03-Detailed-Textbook.md) | [双ISP FRR实验](04-Internet-Edge/02-Labs.md) |
| 5 数据中心 | [underlay、封装、EVPN路由与IRB](05-Data-Center/03-Detailed-Textbook.md) | [分层验证和故障注入](05-Data-Center/02-Labs.md) |
| 6 AI/HPC | [通信模式、RDMA、拥塞、容量与测量](06-AI-HPC/03-Detailed-Textbook.md) | [1000GPU容量例题与硬件/无硬件路径](06-AI-HPC/02-Design-and-Labs.md) |
| 7 交易网络 | [行情序号、组播、A/B、时延、PTP与RCA](07-Trading/03-Detailed-Textbook.md) | [组播、预算、主机与时钟实验](07-Trading/02-Labs.md) |

每章包括学习目标、原理推导、案例、错误判断、作业和参考答案。先独立答题，再对照答案；不要把答案抄进进度表当完成。

## 怎么安排学习量

24周每周8–10小时是第一轮主线预算，重叠阶段共享时间。详细教材的必修内容配合一个完整实验完成；实机RDMA、精密PTP、复杂多归属和生产级自动化放到后续专项。没有相应平台时完成设计与模拟分析，并标明未实测项。

每周保留一个可复核成果：正常基线、故障现象、判断证据、恢复结果和讲述。原理、操作或设计、排错、表达各0–2分，至少6/8且无0分再进入下一阶段。学习任务不因文件已生成而自动完成。

## 学习记录与作品集

- [个人进度记录](08-Portfolio/Progress.md)：保留原有内容，自行填写实际完成情况。
- [实验记录模板](08-Portfolio/Lab-Report-Template.md)：记录环境、证据、注入和恢复。
- [设计与英文面试](08-Portfolio/Design-and-Interview.md)：将技术成果转成可讲述案例。
- [官方资料索引](09-References/Reading-List.md)：按问题阅读，而非用链接代替教材。
- [原计划覆盖对照](00-Plan/Plan-Coverage.md)：追溯原七阶段内容。

## 来源与验证范围

初版于2026-09-26依据原职业规划材料建立，本版按“内容不足、不够细致”的反馈扩写。职业方向不构成薪资或招聘承诺，案例为教学设计，不代表你已经完成的生产项目。

本次检查范围为文档结构、本地链接、代码围栏和示例计算；Linux、FRR、云、GPU与PTP实验未在本次编写过程中运行。旧代码保持原样，其历史验证记录见实验环境文档，不作为本次新测试结果。
