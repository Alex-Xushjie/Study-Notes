# 24 周路线

[返回项目首页](../README.md)

## 每周节奏

原计划给出的 2h 理论 + 3h Lab + 2h 排错 + 1h 英文 + 1–2h 设计合计为 **9–10 小时**。本项目默认按 9h；只有 8h 的周，将理论、设计各减 0.5h，不省略验证。每周只交付一个主成果，把英文和设计练习直接用于该成果。

标注“复习/预习”的副线包含在上述总时间内；优先保证主线。若阶段验收不通过，下一周先修复，后续周次顺延。不要同时购买多套课程或开始多个认证。

| 周 | 主线与阅读 | 3h 实验 + 2h 排错的具体任务 | 周交付与通过条件 |
|---|---|---|---|
| W1 | Linux 数据路径，L1 | 建 namespace 三节点路由；删除服务器回程路由并恢复 | 拓扑、双向路由、双端抓包；解释单向可达 |
| W2 | Linux L2/L3 | 建 HTTP 监听；制造 MTU 不匹配及关闭监听 | 区分 SYN 无回应、RST、ICMP 错误 |
| W3 | Linux L4/L5 | VLAN 与 active-backup bond；检查 nftables 和日志 | 说明标签、逻辑接口、状态防火墙各自作用 |
| W4 | Python 入门；Linux 复习 | 运行离线健康检查；读懂 JSON/list/dict/function | 修改一条 BGP 记录，观察告警和退出码 |
| W5 | API、异常；Linux NIC | 比较成功、缺失、失败三类采集结果；采集 NIC 信息 | 缺数据不能判健康；解释 offload 抓包现象 |
| W6 | 自动化流水线；Linux 验收 | 设计 inventory；生成配置 diff；复现 L1–L3 中任意两故障 | Linux 阶段报告 + 自动化数据契约 |
| W7 | AWS 基础；自动化主线收尾 | 完成健康检查扩展与单元测试；画 VPC 逐跳路径 | 能解释 SG/NACL/route 三类故障 |
| W8 | AWS TGW；Ansible 验收 | 完成 Ansible 离线渲染；重复执行、前后验证 | 健康检查项目 + YAML→配置→验证演示 |
| W9 | AWS 混合云 | 完成 Cloud C1，推演 DX 单连接/站点故障 | 标出 transit VIF、DXGW、TGW 和回程 |
| W10 | Azure 基础；Edge 预习 | 完成 C2 路由表和 hub-spoke；分析重叠地址 | 路由矩阵覆盖双向流量和防火墙 |
| W11 | Azure ER/HA；Edge 预习 | 完成 C3 双 DC 双区域设计 | 能区分单电路双连接和异地冗余 |
| W12 | Cloud 验收；Edge 路由策略 | 对混合云设计做 4 类故障推演 | HLD + 5 分钟英文设计说明 |
| W13 | Internet Edge；DC 预习 | Edge E1 双 ISP、前缀过滤、出口选路 | 证明没有成为 ISP 间 transit |
| W14 | Internet Edge；DC underlay | Edge E2 修改 local-pref / prepend；ROV 手算 | 区分出站控制与入站影响 |
| W15 | Edge 验收；DC overlay | Edge E3 黑洞/FlowSpec 桌面演练；DC 地址表 | 双 ISP 运行手册 + 误操作恢复方案 |
| W16 | EVPN/VXLAN | DC D1/D2：underlay→overlay→主机逐层验证 | Type 2/3 及 RT/VNI 对照表 |
| W17 | EVPN IRB；HPC 预习 | DC D3 跨子网、Type 5；破坏 RT 再恢复 | 解释 RD/RT、L2VNI/L3VNI 区别 |
| W18 | DC 验收；RDMA 入门 | DC D4 单链路/leaf 故障；比较 L3 to server | 故障矩阵 + DC 方案选择记录 |
| W19 | HPC 拥塞控制 | 完成 HPC H1 反馈链图；H2 端口容量计算 | PFC/ECN/CNP/DCQCN 不混淆 |
| W20 | HPC fabric；Trading 预习 | 完成 H3 无硬件案例或有硬件基线 | 区分链路带宽、RDMA 带宽、collective 吞吐 |
| W21 | HPC optics；Trading 数据流 | 核对 400G/800G 端口、breakout、lane/FEC；交易拓扑 | BOM 假设 + A/B 故障域清单 |
| W22 | HPC 验收；Trading 组播 | 20 分钟 1000 GPU 方案；Trading T1 | 容量表 + 性能验证计划；不冒充实测 |
| W23 | Trading 时钟与主机 | T2 延迟预算、T3 PTP/NIC 观测 | 解释 RTT/单向时延及误差预算 |
| W24 | 综合验收 | T4 故障复盘；录一场 30 分钟设计面试 | 七阶段证据索引 + 3 个可讲述案例 |

## 阶段闸门

W6、W8、W12、W15、W18、W22、W24 分别验收相应阶段。按“原理、操作/设计、排错、表达”各 0–2 分，总分至少 6/8，任何一项为 0 都要补做。硬件阶段可凭完整设计与反例分析拿设计分，但不能标记硬件操作通过。

0 分：只能复述名词；1 分：有提示能完成；2 分：独立完成且有证据。把错误写进报告，比补更多链接更有用。

优先级保持原计划：Linux/Automation/Cloud > Edge/DC > HPC > Trading。某周只有 4h，先保留当前主线实验、排错与记录，顺延副线；不要把 Linux 未过关的问题带到 DPDK。
