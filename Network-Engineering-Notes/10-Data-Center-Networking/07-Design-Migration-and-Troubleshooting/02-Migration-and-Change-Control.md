# 传统网络迁移、扩容与回退

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 并行期的隐形风险

传统VLAN、旧网关、新Anycast Gateway、双Border和服务设备同时存在时，易出现重复网关、环路、错误RT和路由反馈。先选明确迁移边界，不将所有旧网段一次延伸全Fabric。

## 2. 迁移顺序

1. 清点应用、地址、MAC/静态依赖、网关、DNS、安全和负载。
2. 验证目标支持/容量及Underlay和基本Overlay。
3. 建立受控旧新互通，明确网关唯一/多活模型与防环。
4. 灰度少量测试业务，验证正常、拒绝、首包、大包和回程。
5. 演练失败与回退，再分批迁移。
6. 确认遗留流量和管理依赖后退役旧路径。

## 3. 扩容不是只插链路

新Spine/Leaf引入路由和Hash变化，可能搬流。验证地址/ASN/VNI台账、模板、版本与许可，分批并保留故障域独立。设备启动、全表重收和MAC/IP重学习也是负载。

## 4. 回退

恢复包含网关、路由、MAC/ARP、租户映射、安全和应用，不只撤新设备。不能在未知状态全网clear解决，先限定测试对象。明确哪些连接需重建、哪些状态无法原子恢复。

## 5. 交付

提交迁移前后图、前缀来源与网关矩阵、分批/止损条件、备份与恢复、正常/故障验证。代码审查与配置语法检查不是业务验收。

[安全变更方法](../../04-Network-Automation/07-Backup-Compliance-and-Safe-Changes/03-Prechecks-Canary-Postchecks-and-Rollback.md)、[工程迁移参考](../../12-Engineering-Reference/03-Migration-Changes-and-Rollback/01-Migration-Changes-and-Rollback.md)。
