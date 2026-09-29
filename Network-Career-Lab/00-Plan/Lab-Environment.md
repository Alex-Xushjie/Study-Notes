# 实验环境与证据管理

## 最小环境

当前工作站是 Windows。本教材的 `bash`、`ip`、`nft`、`ethtool` 命令均在**专用 Linux 实验 VM**运行，不在 PowerShell 中执行。建议 Ubuntu 24.04 LTS VM，2 vCPU、4 GB RAM、20 GB 磁盘作为起点；这是教学预算，不是性能基准。为 VM 做初始快照。WSL2 可尝试基础 namespace，但驱动、systemd、硬件队列与时间戳能力须自行核验；NIC/RDMA/PTP 性能实验用物理机。

Linux 基础实验只需要一台 VM。Edge 实验用三台运行 FRR 的 VM，DC 可用 EVE-NG 中合法取得的厂商镜像，或 FRR/Linux VXLAN。大型虚拟拓扑的内存需求由所用镜像决定；先跑最小两 leaf、一 spine，再扩展。

VM 内安装基础工具：

```bash
sudo apt update
sudo apt install -y iproute2 iputils-ping tcpdump ethtool dnsutils \
  traceroute mtr-tiny nftables iperf3 python3 python3-venv git
uname -r
ip -V
python3 --version
```

记录发行版、内核、虚拟化平台、FRR/NOS、NIC/驱动/固件版本。命令中的接口名、MAC、硬件功能按实际环境替换。硬件不支持的命令返回“不支持”也是有效观察，不能据此认为配置错误。

## 三种实验类型

| 类型 | 本项目提供 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| 可本地运行 | Linux namespace 脚本、离线 Python 样例、Ansible 渲染 | 数据路径、逻辑和异常处理 | ASIC、真实云、RDMA 性能 |
| 需要平台 | FRR/NOS、云账户、真实 NIC 实验步骤 | 对应平台功能和故障行为 | 其他版本/设备上的相同性能 |
| 纸面设计 | 云、1000 GPU、时延预算、故障表 | 需求推导、容量与取舍 | 实际吞吐或恢复时间 |

云课程的核心作业可以离线完成。可选云实验只创建小规模测试资源，先检查区域价格、预算和资源清单；NAT Gateway、TGW、VPN、Firewall 等存在持续计费。不要为了学习去订购真实专线。删除计算实例不等于删除所有计费资源。

## 证据组织

自己创建 `08-Portfolio/evidence/W01/` 等目录，保存脱敏后的命令输出、拓扑、配置 diff 和实验报告。输出中注明 UTC 时间、版本、观测点和“实测/模拟/设计”。抓包可能含地址和业务内容，只保留实验流量。

项目中的 IP 使用实验私网或文档地址，ASN 使用私有 ASN。故障注入只在专用 VM / namespace / 测试租户里执行。Linux 脚本以 `ncl-` 前缀创建 namespace，清理只涉及这三个明确命名的对象；不要改写为宿主全局 `flush`。

## 当前交付的验证边界

材料是在 Windows 工作区编写；Python 样例可在此直接验证。Linux、FRR、云、GPU 和 PTP 实验提供操作与验收步骤，不预先声称在这些平台实跑通过。执行前后填写实验记录，完成自己的环境验证。

2026-09-26 交付检查：7 项 Python 单元测试通过；命令行的健康、UNKNOWN、坏输入三种情形退出码与预期一致；带故障的样例生成 JSON/CSV，并返回预期的非零退出码。22 篇 Markdown 的 53 个本地链接、代码围栏配对和非空内容检查通过。当前没有可用的已确认 Bash/Ansible 实验运行环境，因此没有把 shell 脚本、playbook 或网络实验标成实跑通过。
