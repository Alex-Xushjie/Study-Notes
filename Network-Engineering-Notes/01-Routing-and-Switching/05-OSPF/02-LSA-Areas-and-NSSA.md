# OSPF的LSA、区域、Stub与NSSA

[路由交换学习目录](../Routing-and-Switching.md)

## 1. LSDB不是一张全域不分区域的路由表

LSA是link-state advertisement链路状态通告，LSDB是这些对象的数据库。OSPF按不同泛洪范围传播信息；同一区域的相应链路状态应同步，跨区域不要求每台保存完全相同的全部拓扑。

判断某LSA要看类型、Link State ID、Advertising Router、序列、Age及作用范围。Link State ID的意义依类型，不能都当业务前缀地址。

## 2. OSPFv2主要类型

| 类型 | 表达与范围 | 典型检查 |
|---|---|---|
| 1 Router | 区域内路由器链路状态 | 本节点/邻居是否按预期描述链路 |
| 2 Network | 多接入网段相关拓扑，由DR产生 | DR与参与路由器关系 |
| 3 Summary | 区域间网络可达信息 | ABR是否向相应区域生成/过滤 |
| 4 ASBR Summary | 区域间到ASBR的相关可达信息 | 外部路由所需ASBR路径 |
| 5 External | AS外部前缀信息，范围受区域类型限制 | metric、类型、Forwarding Address、Tag |
| 7 NSSA External | NSSA内引入的外部信息 | 翻译条件、出口与范围 |

Type3的Summary名称不代表必然做了地址聚合。LSA老化/序列用于管理新旧信息，不能用单次Age略有不同判定数据库失步。

## 3. 区域边界怎样改变信息

ABR连接相应区域并传播摘要化的可达信息；ASBR向OSPF引入外部来源。ABR可以同时是ASBR，但角色不等同。Area0作为骨干，正常分层设计需保证相应骨干连通关系。

Virtual Link可解决特定逻辑骨干连接问题，但增加依赖与排错复杂度，不作为长期弥补任意区域规划错误的默认方案。其可用条件按协议与平台核验。

## 4. Stub与NSSA解决的是信息边界

Stub不接收相应Type5外部信息，并通过ABR等提供默认可达模型；区域内节点的stub能力配置需一致。它不是物理上只有一条链路的同义词。

NSSA允许区域内以Type7引入外部来源，再在满足规则时由相应ABR翻译为Type5向外传播。翻译者、P-bit等条件会影响结果，不能只看到Type7就假设所有外部区域已学到。[NSSA RFC3101](https://www.rfc-editor.org/rfc/rfc3101.html)

Totally Stubby/Totally NSSA等常见实现扩展还可能限制Type3并提供默认，名称与命令支持不是跨厂商完全一致的统一标准配置。

## 5. 一个两区域例题

Area0通过ABR连接Area10，Area10有业务10.10.0.0/24。Area0节点不需要知道Area10每条链路，而应获得合适的区域间信息。如果路由缺失，依次在源区域查Type1/2相关拓扑、在ABR查计算/边界策略、在目标区域查Type3，最后查RIB/FIB。

若Area10是NSSA且向外引入198.51.100.0/24，Area10检查Type7，Area0检查相应翻译后的Type5，不能在所有设备上强求看到Type7。

## 6. 汇总与Forwarding Address

ABR/ASBR相关汇总可减少状态，也可能隐藏明细故障。缺少一个/24但大汇总仍在时，判断吸引后丢弃是否在业务允许范围。

外部LSA中Forwarding Address非零时，转发可能需解析该地址，而不简单总走向Advertising Router；相应可达性与规则影响路由是否采用。它是“LSA在但路由无”的重要检查项。

## 7. 验证与练习

FRR的show ip ospf database及其类型/明细子命令用于看数据库，show ip route看采用结果。具体过滤语法以当前版本帮助为准。

画Area0、Area10、NSSA和外部来源，标每类LSA在哪里出现、由谁产生、是否允许传播。撤明细、断ABR、改变区域类型，在隔离拓扑记录故障与恢复。自测：Type3一定汇总吗？答：不一定。NSSA是否等于禁止所有外部来源？答：不是。继续[选路与收敛](03-Path-Selection-and-Convergence.md)。
