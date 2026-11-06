# 资源模块、幂等与Check Mode边界

[返回网络自动化目录](../Network-Automation.md)

## 1. 幂等是结果属性

对同一有效意图重复执行，系统不应持续产生不必要变化。但命令发送成功、第二次changed=false、最终业务满足意图是三个判断。字符串比较、动态字段与平台规范化可能影响changed报告。

仅生成配置文件的幂等不能证明设备配置幂等；Mock返回成功也不能证明NOS状态符合预期。

## 2. 资源模块的状态

| State | 主要目的 | 关注点 |
|---|---|---|
| gathered | 采集结构化资源 | 支持范围与完整性 |
| parsed | 解析所给文本 | 不代表完整设备状态 |
| rendered | 离线生成设备格式 | 不与设备通信 |
| merged | 合并所声明配置 | 不代表没有任何风险 |
| replaced | 替换相应资源子集 | 具体删除范围按模块 |
| overridden | 覆盖该类资源范围 | 可能移除未声明的管理配置 |
| deleted | 删除/恢复相应缺省 | 影响与平台默认需确认 |

实际模块支持哪些状态以该Collection版本为准。不要将不同模块的replaced/overridden范围想当然等同。

## 3. Check与Diff

--check仅在模块支持的语义内模拟，某些任务会跳过、缺少register结果或不完整预测。--diff提供变化信息，可能泄露配置秘密。既不能保证运行时不会有外部副作用，也不能代表设备接受和业务通过。

离线render、语法检查、Check Mode、实验实配和业务验证层层补充。不存在“一次--check就保证全网安全”。

## 4. 分批执行

serial控制每批主机范围，throttle/forks等在各自层次影响并发。对双机、核心、Hub等故障域不能简单按清单顺序任意分组；先定义不允许同时变化的集合。失败阈值应同时看任务失败和业务后检。

## 5. 验收

一次实验变更保存前状态、计划、实际命令、后状态和业务；第二次运行验证无额外变化；再改变一个意图字段验证最小差异。模拟半途失败，记录已生效部分与恢复，不因Play结束FAILED就假设全部已回滚。

[资源模块](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)、[Check与Diff](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html)、[执行策略](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_strategies.html)。
