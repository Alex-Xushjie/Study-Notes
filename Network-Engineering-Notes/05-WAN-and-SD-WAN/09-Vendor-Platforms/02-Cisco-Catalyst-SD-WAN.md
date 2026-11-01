# Cisco Catalyst SD-WAN的OMP、TLOC与排障

[返回WAN与SD-WAN目录](../WAN-and-SD-WAN.md)

## 1. 名称与职责

现行文档使用Manager、Controller、Validator与WAN Edge等名称；旧资料常见vManage、vSmart、vBond。先按管理、控制、引导/编排、数据职责识别，再对照对应版本名称，避免把控制器理解为业务中转Hub。

OMP用于Overlay控制信息交换。业务前缀路由、传输定位与服务信息属于不同对象；业务前缀存在但关联的传输下一跳无效时，不一定能安装成可用转发路径。

TLOC由System IP、Color与封装类型标识。System IP是逻辑设备标识，不应简单当作外层公网地址；Color表达传输属性/类别，不是链路质量评分。外层私网/公网地址、NAT映射和Underlay可达还需另查。

## 2. 分层诊断

| 症状 | 要查的问题 |
|---|---|
| 设备未建立控制连接 | Underlay、组织/身份、证书、时间和控制端点 |
| 控制正常，BFD不通 | 数据端点、NAT/过滤、隧道和对端传输 |
| OMP有前缀，业务无路由 | 路由选优、TLOC可达、策略与服务VPN |
| 路由正常，应用走错线 | AAR/Data Policy命中、分类、SLA和会话 |
| 故障后旧流通新流失败 | 缓存/保留状态与控制依赖，不能直接下结论 |

IOS XE SD-WAN常见只读命令如下，具体参数用目标版本帮助确认。它们不是vEdge全部通用语法。

~~~text
show sdwan control connections
show sdwan omp routes
show sdwan bfd sessions
show sdwan app-route stats
~~~

分别用来观察控制连接、Overlay路由、数据隧道检测与质量。还需服务VRF路由、业务会话、策略命中与接口计数，四条命令不能替代完整证据链。

## 3. 策略与SLA

控制策略可影响路由分发/拓扑，数据策略与AAR影响业务执行；集中与本地策略作用位置不同。匹配顺序、默认动作及策略之间交互应按目标版本验证。

AAR不等于BFD一旦探测质量异常就立即搬流。统计窗口、增强AAR、SLA规则、Preferred Color、Strict/Drop与Fallback等影响结果。特别验证所有路径Out-of-SLA时是继续、回退还是丢弃，不能从“Preferred”一词猜测强制行为。

## 4. 专题练习

单分支双传输到双Hub：证明控制连接、路由、TLOC和BFD分别正常；故意让一条数据隧道不可达但控制在线，解释差别。再对测试业务设置SLA并制造Brownout，观察新旧会话、窗口与回退。

不在未授权设备上启用Debug或推策略。本篇没有实际运行厂商镜像，命令输出需自行采集。

[OMP路由通告](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/routing/ios-xe-17/routing-configuration-guide-17-x/OMP-routing-protocol-ref.html)、[增强AAR](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/ios-xe-17/policies-book-xe/m-enhanced-application-aware-routing.html)、[SLA与回退](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/26x-later/policies/policies-configuration-guide/AAR/sla-aar.html)、[IOS XE排障命令](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/command/iosxe/qualified-cli-command-reference-guide/m-troubleshooting-commands.html)。
