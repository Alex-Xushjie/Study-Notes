# IPsec、IKEv2、身份与安全关联

[返回本部分学习目录](../Network-Security-and-Access.md)

## 1. 控制和数据分开

IKEv2协商认证与相关安全参数，IKE SA保护控制交互，Child SA承载相应数据保护，ESP处理业务报文。IPsec SA具有方向性，控制成功不代表业务双向可用。

站点VPN的网络设计还需端点可达、身份、算法兼容、业务范围、路由、NAT例外、安全和MTU。每个检查项各自提供证据，不能只写“隧道UP”。

| 层次 | 常见失败 |
|---|---|
| 外层路径 | 地址/路由、UDP500/4500或ESP协议过滤 |
| IKE身份 | ID、证书链/用途、PSK与时间 |
| Child SA | 提案/Selector与对端支持不一致 |
| 内层业务 | 路由、NAT、许可、目标与回程 |
| 长期运行 | Rekey、DPD、映射老化与证书轮换 |

## 2. NAT-T与重放

NAT-T常将ESP封装到UDP4500，ESP原本是IP协议号50，不是UDP50。NAT保活、DPD和隧道内业务探测测试对象不同。

反重放窗口用于防止重放，正常网络的极端乱序也可能触发相关丢弃。扩大窗口或关闭检查不应作为默认修复，先查多路径、平台支持与实际重排；按安全基线评估。

## 3. 算法与身份管理

本篇不提供永久通用密码套件。根据组织基线、当前标准/平台能力与双方兼容选择，淘汰弱项有正式迁移计划。PSK与证书生命周期、权限及审计需设计，学习仓库不保留真实秘密。

## 4. 练习

画IKE控制路径、ESP/NAT-T数据路径与内层地址，分别解释IKE正常但无Child SA、双SA正常但单向、周期性Rekey时断流。保留两端日志和计数增量，不用一次重启代替根因。

[IKEv2 RFC7296](https://www.rfc-editor.org/rfc/rfc7296.html)、[IPsec架构RFC4301](https://www.rfc-editor.org/rfc/rfc4301.html)、[NAT-T RFC3948](https://www.rfc-editor.org/rfc/rfc3948.html)。
