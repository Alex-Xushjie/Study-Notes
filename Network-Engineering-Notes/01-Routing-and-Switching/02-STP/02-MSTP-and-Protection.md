# MSTP、边界与生成树保护机制

[路由交换学习目录](../Routing-and-Switching.md)

## 1. 为什么要有多实例

每VLAN一棵树与多个VLAN映射到少量实例有不同的状态规模和负载分布。MST将VLAN映射到实例，在区域内按相应树处理。实例规划与trunk/VLAN规划必须一致，不能只追求两条上联都亮。

区域通常根据名称、修订号和VLAN映射等配置标识一致性。修订号不是“数值更大自动获胜并覆盖其他设备”的配置同步协议。区域边界还涉及CIST/外部树，不把内部实例选择直接推给整个网络。[Cisco MST说明](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24248-147.html)

## 2. 检查区域边界

确认两端完整映射与digest、端口边界状态、根角色及不在使用VLAN的映射。区域名称相同但映射不同，仍可能成为不同区域。边界行为、PVST互通和不一致状态按具体平台查证。

## 3. 保护机制分别防什么

| 机制 | 主要意图 | 不能替代 |
|---|---|---|
| BPDU Guard | 在不应收到BPDU的边缘位置发现桥接等异常 | 不能替普通互联端口规划 |
| Root Guard | 不允许指定方向成为更优根路径 | 不是停止所有BPDU |
| Loop Guard | 在应持续接收BPDU的相关端口上防止失收后错误转发 | 不等同物理单向检测 |
| UDLD等 | 检测特定单向链路/邻接异常 | 不替完整STP与业务验证 |
| BPDU Filter | 按具体实现抑制相关BPDU行为 | 误用可移除环路保护，不是Guard同义词 |

功能命名和触发/恢复方式可能不同。例如err-disable与root/loop inconsistent不是同一状态，必须区分原因与恢复条件。[Loop Guard与UDLD](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol-stp-8021d/218321-configure-stp-with-loop-guard-and-bpdu-s.html)

## 4. 故障例：保护触发后反复自动恢复

只增加自动恢复计时可能让异常环路周期性重现。先定位误接设备、单向链路或BPDU路径，保留触发日志、角色变化和现场连线，再决定恢复。运行手册要写谁确认物理条件已修复。

## 5. 设计与验收

根据网络边界选择保护，而不是全部接口启用同一模板。主备根位置、三层网关位置和故障路径应共同设计。MST实例不是默认按链路负载自动迁移，负载目标要通过映射和容量验证。

交付实例映射表、根/备根台账、边缘/互联端口保护矩阵和三个错误注入的恢复证据。没有支持该功能的平台时只标设计推演，不虚构保护状态输出。
