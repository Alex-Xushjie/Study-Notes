# AP上线、控制器与转发模式

[返回本部分学习目录](../Campus-and-Wireless.md)

## 1. 管理位置与数据位置分开

AP受本地/远程/云管理，不表示全部客户端数据都经该管理平台转发。集中转发、AP本地转发、隧道到锚点/网关是不同数据路径。先画AP管理、控制、安全认证和用户数据四条依赖。

| 过程 | 检查对象 |
|---|---|
| AP启动 | PoE、固件、管理地址和时间 |
| 发现/加入 | DNS/DHCP或静态发现、控制端可达、证书/授权 |
| 策略绑定 | SSID、站点、RF、VLAN/角色与平台映射 |
| 客户端认证 | AP/控制器/AAA及返回属性 |
| 业务转发 | 本地交换或隧道、网关、ACL与回程 |

## 2. CAPWAP与平台差异

CAPWAP是AP与控制器交互的协议体系，隧道MTU、分片、端点过滤和认证可能阻止上线。云管理产品也可能采用其他连接机制，不能要求所有AP都跑同一组端口。

Cisco FlexConnect是产品实现例子：本地转发需要AP侧正确业务VLAN/交换端口，集中转发则需控制器/锚点侧路径。不同版本的认证、断连与HA支持要分别核对。

## 3. 常见误判

AP在线只能说明相应控制/管理状态；SSID可见不等于认证和DHCP正常。管理VLAN通过不表示业务VLAN也允许。AP重启后短时可用可能是状态/租约/策略老化，不应只反复重启。

## 4. 练习

为一个本地转发与一个集中转发SSID画正反路径，逐处标VLAN、网关、DHCP与AAA。注入业务VLAN遗漏但管理正常，说明应在何处抓包/查表。

[CAPWAP RFC5415](https://www.rfc-editor.org/rfc/rfc5415.html)、[Cisco FlexConnect解释](https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/213945-understand-flexconnect-on-9800-wireless.html)。
