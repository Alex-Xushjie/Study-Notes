# 安全平台映射与版本化诊断

[返回本部分学习目录](../Network-Security-and-Access.md)

## 1. 选择一套平台做闭环

本篇用FortiGate、Palo Alto和Cisco ISE等作机制映射，不做采购排名。先掌握会话/NAT/策略/身份，再查产品对象与包流程；考试命令表不能替代业务验证。

| 通用能力 | 产品例子 | 必须核对 |
|---|---|---|
| 有状态过滤/NAT/HA | FortiGate、Palo Alto等 | 区、虚拟上下文、处理顺序与同步范围 |
| 远程用户接入 | 对应VPN客户端/网关 | 协议、版本、OS、MFA与许可证 |
| NAC/AAA | Cisco ISE等 | 认证/授权、设备支持、CoA与角色落地 |
| ZTNA/SASE | 产品对应模块 | 连接器、资源协议、PoP与日志 |

## 2. 版本和上下文

FortiOS VDOM、Palo Alto VSYS/虚拟路由等是各自模型，不能当同名命令通用。记录设备、系统、客户端、授权、签名与集中管理版本。SSL VPN等功能可能随版本/型号改变支持，不照旧教程假定所有新版本都保留。

## 3. 诊断方法

固定流量五元组与时间，在正确上下文查路由、命中、NAT、会话和丢弃，再对照两端。Debug可能影响性能、泄露数据，先用只读状态和有限过滤；需要时按厂商操作流程限制对象和窗口并停用。

ISE Live Logs等显示服务器判断，仍需接入口实际授权与业务验证。GlobalProtect等产品的Portal与Gateway有不同职责，不能把门户登录成功当数据隧道可用。

## 4. 学习验收

一套合法隔离平台完成允许/拒绝、SNAT/DNAT、站点VPN、测试用户接入、日志/RCA与HA矩阵，再迁移另一平台比较差异。没有镜像只做设计，标明未实操。

[Fortinet官方文档](https://docs.fortinet.com/)、[Palo Alto GlobalProtect](https://docs.paloaltonetworks.com/globalprotect)、[Cisco ISE支持文档](https://www.cisco.com/c/en/us/support/security/identity-services-engine/series.html)。按目标版本打开对应配置和已知问题资料。
