# 项目：Network Health Check 与配置渲染

## A. 先跑通离线版本

在本项目根目录执行（Windows/Linux 均可，Python 3.9+，无第三方依赖）：

```text
python labs/automation/health_check.py labs/automation/sample.json --output labs/automation/report.json
python -m unittest discover -s labs/automation -p "test_*.py"
```

样例故意包含一个 Idle 邻居和一个采集失败设备，预计程序退出码为 1，报告中同时出现 FAIL 和 UNKNOWN。退出码 0 表示所有设备通过，1 表示存在 FAIL，2 表示输入错误或仅存在 UNKNOWN；这使 CI 不会将缺数据判为成功。输出 CSV 与 JSON 同目录同文件名前缀。生成报告不应代替原始输入证据。

阅读代码时依次找到：加载 JSON → 输入验证 → 每台设备判断 → 汇总退出码 → 写两种报告。这个起步版本**只实现 BGP 状态判断**，模拟数据不是从设备采集的。

## B. 将原计划的 12 项检查逐步实现

| 检查项 | 原始数据/采集来源 | 判断与防误报设计 |
|---|---|---|
| Interface | admin/oper、速率、errors | 只检查意图要求启用的接口 |
| BGP | 预期邻居表、FSM、accepted prefixes | Established 仍要核对前缀；邻居缺失不能跳过 |
| OSPF | 邻居、接口类型、角色 | 广播网段 DROTHER 间 2-Way 可正常 |
| CPU/Memory | 用量、时间、采样间隔 | 阈值参数化，多次采样，说明平台口径 |
| CRC | 两次计数器、设备启动时间 | 算增量，避免历史值和重启误报 |
| Optical power | DOM 数值与模块阈值 | 不支持标 N/A；收发方向与单位分清 |
| Routing table | 必须存在的前缀和下一跳 | 不能只比较总数；区分 RIB/FIB |
| NTP | 选中源、reach、offset | 配置 server 不代表已同步 |
| VRRP | 预期角色与对端视图 | 单台是 backup 不等于故障 |
| MLAG | peer、peer-link、consistency | 双机联合判断，区分孤儿口 |

CPU 与 Memory 分别计为检查项，表中合并展示。每新增一项都需要“健康、异常、缺失”三类样例；把支持矩阵写进 README。先实现 Interface 和 CRC，再加一个路由协议，最后做硬件/双机特定项。完整 12 项是项目扩展目标，不要求初学第一个晚上完成。

实机接入任务：选择一台实验设备，用 Netmiko、NAPALM 或 REST 获取只读结果；口令来自环境变量或交互输入。用独立 adapter 转成样例 schema，并记录平台、版本、采集时间和错误。将预期邻居 inventory 与实际邻居集合比较，找出“完全没出现在输出里的邻居”。

## C. YAML → Jinja2 → 文件：可运行离线实验

在 Linux 控制端创建虚拟环境并安装 Ansible，记录实际版本：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ansible-core
ansible-playbook labs/automation/render.yml --check --diff
ansible-playbook labs/automation/render.yml --diff
ansible-playbook labs/automation/render.yml --diff
```

预期：真实执行第一次生成配置，第二次内容不变，template 任务不再 changed。输出是教学用 FRR 风格片段，**不会连接或修改设备**。变更 YAML 中的描述，观察 diff；删除必须字段，检查渲染失败。

下一步手工审查生成的配置，把它复制到实验 FRR 的候选配置中，补齐接口/IP/策略后才应用。保存变更前后 `show bgp summary`、路由和业务探测。此流程本身不保证原子回退；下发机制要按实际 NOS 能力设计。

## D. 验收与面试讲述

交付：代码、脱敏 inventory、schema、样例、测试、JSON/CSV、配置 diff、README、一次失败复盘。故意加入设备超时、空结果、错误类型、邻居缺失，报告应明确原因。

英文结构：*I separated collection from evaluation so that the checks can be tested offline. Missing data is reported as unknown, not healthy. Before deployment, I compare the rendered configuration and capture a baseline.*
