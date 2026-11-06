# Fabric设计、分层排障与证据链

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 从一个业务流定位

记录S/D、租户VRF、VLAN、VNI、源/目的Leaf、协议/端口、方向和时间。先验证主机与本地接入，再Underlay、Overlay控制、VNI/VRF安装与实际数据。不同故障可能都表现为ping失败。

| 层次 | 核查 |
|---|---|
| 主机/接入 | IP/掩码、网关、VLAN、MAC、ARP/ND与系统 |
| Underlay | VTEP路由、ECMP、链路/MTU、过滤 |
| EVPN | Type2/3/5、RD/RT、Next-Hop与选优 |
| 转发 | FDB、VRF/FIB、封装/解封及硬件安装 |
| 服务 | 防火墙/NAT、外部路由与回程 |
| 应用 | 请求/响应和依赖，不只ICMP |

## 2. 先比较范围

同Leaf正常跨Leaf失败：查封装/远端控制；同子网正常跨子网失败：查网关/IRB；仅外部失败：查Border；仅大包失败：查MTU。这是调查优先级，不是最终根因。

FRR/Linux、商用NOS和ASIC观察命令不同。Linux桥/VXLAN/VRF需先理解对象关系，不能只在FRR里贴BGP配置而不准备数据面对象。

## 3. 证据要求

保存原配置、意图、路由收到/导入/安装、实际入出计数与主机结果。累积计数取窗口差值；未采到包要先验证观察点和记录器能力。控制面大量路由不等于硬件容量充足。

## 4. 练习

设计五个单变量故障：缺Loopback路由、错RT、错VNI、IRB缺配置、回程遗漏。每个都给支持/反证和最小修复；恢复后验证无关租户仍隔离。

[FRR EVPN](https://docs.frrouting.org/en/latest/evpn.html)、[报告模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。
