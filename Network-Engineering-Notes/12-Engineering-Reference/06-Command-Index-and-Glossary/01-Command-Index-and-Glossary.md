# 命令索引：按问题和执行环境查找

[返回本部分学习目录](../Engineering-Reference.md)

## 1. 使用方法

先确定想验证的假设、执行环境、版本、权限和对象，再选命令。下面是只读起步索引，不是跨平台脚本。show、Linux Shell、云CLI和Python解释器不能混用；带具体参数的动作到相应正文核对。

| 问题 | 示例工具/命令 | 环境与入口 |
|---|---|---|
| 主机地址/路由 | ip -br addr、ip route get | [Linux](../../03-Linux-Networking/Linux-Networking.md) |
| 进程/监听 | ps、systemctl status、ss -lnt | Linux，管理体系需适用 |
| DNS回答 | dig、resolvectl | [DNS](../../06-Cloud-and-Hybrid-Networking/06-Hybrid-DNS/02-DNS-Troubleshooting-and-Private-Endpoint-Cases.md) |
| 具体HTTP | curl | 请求可能有业务含义，限定实验服务 |
| 有限抓包 | tcpdump | Linux，权限/过滤/空间/隐私 |
| NIC能力 | ethtool -i/-T/-l/-g/-c/-k/-S | [NIC专题](../../03-Linux-Networking/07-NIC-Queues-and-Packet-Processing/01-NIC-Queues-and-Packet-Processing.md) |
| BGP/EVPN | show bgp summary、show bgp l2vpn evpn | FRR vtysh；NOS语法另查 |
| 组播状态 | show ip pim neighbor、show ip mroute | FRR，见[组播](../../02-Multicast/Multicast.md) |
| 云路由 | AWS describe-route-tables、Azure有效路由 | [云实验](../../06-Cloud-and-Hybrid-Networking/08-Observability-Troubleshooting-and-Cost/04-Lab-Guide-and-Capstone.md) |
| RDMA对象 | rdma link show、ibv_devinfo | [RDMA](../../11-AIDC-and-RDMA/03-RDMA-RoCE-and-InfiniBand/02-QP-MR-CQ-and-Transport-Troubleshooting.md) |
| GPU拓扑 | nvidia-smi topo -m | 相应驱动/权限与硬件 |
| 代码/变化 | python、git status/diff | [自动化](../../04-Network-Automation/Network-Automation.md) |

## 2. 输出如何解释

命令不存在可能是未安装/版本/权限/平台不同；查询成功也不说明采集完整或业务成功。累计数取差值，状态有时间，聚合有窗口，字段和单位按原始文档。

## 3. 不在速查表直接给出的动作

clear/restart/shutdown、驱动解绑、改sysctl/时钟、推配置、云创建/删除和压力测试需精确对象、前提、回退及授权。不要因熟悉命令就跳过机制。只读大表/Debug也可能有资源成本。

## 4. 练习

对一个不通问题写“假设—命令—预期—反证—下一步”，禁止一次贴几十条命令而不看输出。记录脱敏原文与时间，恢复操作另开步骤。
