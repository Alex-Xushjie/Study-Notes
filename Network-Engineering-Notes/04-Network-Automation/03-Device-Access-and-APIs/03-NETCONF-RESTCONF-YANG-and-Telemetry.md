# NETCONF、RESTCONF、YANG与遥测

[返回网络自动化目录](../Network-Automation.md)

## 1. 协议、模型、编码分开

YANG描述数据结构、类型、约束与操作，不是传输协议；NETCONF是配置管理协议，通常以XML RPC交互；RESTCONF用HTTP机制访问YANG定义的数据。JSON/XML是编码，不意味着字段天然一致。

OpenConfig提供跨厂商模型，厂商原生模型可能暴露更多功能；设备是否实现某模块、修订、偏差和叶子节点，必须通过能力与文档验证。不能因都写interfaces就把路径当通用。

## 2. 数据库与能力

NETCONF可能提供running、candidate、startup等Datastore，但不是所有设备都有全部能力。get与get-config用途不同；lock、validate、commit、confirmed-commit和rollback-on-error都需确认服务器能力和语义。

| 操作阶段 | 关键问题 |
|---|---|
| 能力发现 | 模块/修订、Datastore、事务特性支持吗？ |
| 读取 | 配置与运行状态分别来自哪里？ |
| 编辑 | merge/replace/delete作用范围多大？ |
| 提交 | 是否显式commit，是否支持确认超时？ |
| 恢复 | 失败是否局部生效，锁和回滚如何处理？ |

candidate提交成功不证明业务健康。confirmed-commit可降低某些远程失联风险，但不替代业务验证和独立恢复路径，也不是所有多设备变化的全局事务。

## 3. RESTCONF边界

需要正确资源路径、命名空间、媒体类型、认证与HTTP方法。PUT替换相应资源与PATCH更新可能有不同删除风险，必须查数据模型和补丁格式；不能用普通REST经验猜测设备配置行为。

## 4. gNMI与流式遥测

gNMI提供Get/Set/Subscribe等操作与模型路径，遥测订阅可减少定期全表轮询，但要处理采样/变化事件、初始同步、断线重订阅、时间戳、删除事件与数据缺口。它不是SNMP OID换个名字，也不自动保证所有样本可靠留存。

读写接口与遥测账户按职责隔离。长连接和大规模订阅也有设备/采集端容量，先定义需要的字段与频率。

## 5. 实验

先列设备capabilities和YANG模块，读取一个小范围接口配置与状态，再在隔离设备测试候选提交、校验失败与超时恢复。没有对应镜像时完成XML/JSON响应解析即可，不能宣称验证了事务特性。

[NETCONF RFC6241](https://www.rfc-editor.org/rfc/rfc6241.html)、[RESTCONF RFC8040](https://www.rfc-editor.org/rfc/rfc8040.html)、[YANG RFC7950](https://www.rfc-editor.org/rfc/rfc7950.html)、[OpenConfig gNMI规范](https://www.openconfig.net/docs/gnmi/gnmi-specification/)。
