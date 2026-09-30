# 自动化：把一次成功操作变成可重复流程

## 1. Python 只学当前项目会用到的部分

按 [Python 官方教程](https://docs.python.org/3/tutorial/) 的数据结构、输入输出、异常、模块顺序学习。每天把例子换成设备数据：字符串是 hostname，list 是设备列表，dict 是邻居属性，函数是一个检查项。已有的 [Python 基础笔记](../../NetDevOps/Python_Basic/Python_Basic.md) 可用于查语法。

```python
neighbors = [{"peer": "192.0.2.2", "state": "Established"},
             {"peer": "192.0.2.6", "state": "Idle"}]
failed = [n["peer"] for n in neighbors if n["state"] != "Established"]
print({"failed_peers": failed})
```

先预测输出，再运行；之后把 `state` 删除，观察 KeyError。理解“输入不符合契约”与“设备真的异常”是不同情况，不能用 `except: pass` 把它们都变成成功。

| 知识 | 对应任务 | 完成标准 |
|---|---|---|
| variables/list/dict/loop/function | 遍历设备与接口 | 写出返回结果的函数，不依赖全局状态 |
| file/JSON/YAML | 读 inventory 与保存报告 | 知道 JSON 的布尔值、空值与 Python 不同 |
| regex | 解析不可避免的 CLI 文本 | 输入包括空行、变化的空白、错误输出；优先结构化 API |
| exception | 区分超时、认证失败、坏输入 | 失败设备不导致其他设备丢失报告 |
| requests/REST | 读取 API | 指定 timeout、验证 TLS、检查 HTTP 状态、分页和 schema |
| Git | 保存代码与设计变化 | 每次变更可看 diff、可定位原因，不提交口令 |

HTTP 200 也可能返回缺字段的数据；401、403、429、5xx 不能全部归为网络不通。读取请求可有限重试；写请求要考虑幂等性，超时后先查询实际状态，避免重复创建资源。

## 2. 采集、标准化、判断、报告分开

```text
inventory → SSH/API collector → normalized data → checks → JSON/CSV
                                     ↑
                             offline fixtures
```

Netmiko 适合 SSH CLI；NAPALM 用统一 getter 封装多平台，但支持范围依驱动和版本而异；原生 API 可避免文本解析，仍要核对分页、字段和权限。不要把某平台的命令输出直接作为跨厂商通用格式。

健康检查至少有三种状态：PASS、FAIL、UNKNOWN。没有读到 optical power 不是 0 dBm，也不是健康；已知不支持的检查可标 N/A，并给原因。累计 CRC 总数大于零不一定意味着当前故障，要采集两次、处理计数器重置，再看增量与速率。

## 3. 从读取升级为配置流水线

先做只读采集，再做离线渲染，最后在实验设备下发：

1. YAML 保存意图：接口、地址、邻居、允许的前缀。
2. Jinja2 渲染模板，严格处理未定义变量。
3. 保存生成文件并检查 diff，验证地址重复、接口缺失等输入问题。
4. 保存 pre-check 和设备原配置，分小批次部署。
5. 运行 post-check：会话状态、前缀、业务探测都要比对。
6. 失败时按已验证的回退步骤恢复，确认业务恢复后结束。

“执行没有报错”不是业务验证；Ansible 的 changed 也不是证明结果正确。幂等性是重复表达相同意图不引入额外变化。设备模块的 check mode/diff 支持依实现而异；不支持时不能把它当作已完成预演。

## 4. Ansible 的最小阅读顺序

读 [Network Getting Started](https://docs.ansible.com/projects/ansible/latest/network/getting_started/index.html) 中 inventory、连接方式、playbook 概念。理解 control node、managed node、collection、`network_cli`、`httpapi` 的角色，再选你的实验 NOS 对应 collection。网络设备通常不需要安装 Python，但控制端及模块运行环境需要满足文档条件。

本项目的 [离线渲染实验](02-Project.md) 使用 localhost，不需要真实设备账号。完成后才扩展 network_cli，不盲目粘贴 Cisco 命令到 FRR。

## 5. Git / Terraform / CI 的边界

Git 每周最少做一次有意义的提交练习：看 `git status`、`git diff`，明确文件后 `git add 路径`，再提交。拉取之前检查工作区，遇到分叉先看双方提交；不要用 force push 解决普通同步错误。

Terraform 是扩展项：在云网络课程后学习 provider、resource、plan、state、destroy。state 可能含敏感数据；plan 显示的变更仍需读懂。CI 先自动运行 schema 检查、离线单元测试和模板渲染，不把真实设备下发放进初学者的自动流水线。

自测：某设备 SSH 超时，报告该写 Down 还是 UNKNOWN？参考：只能证明采集失败，应 UNKNOWN，并保留原因；设备业务面可能仍健康。
