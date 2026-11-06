# 802.11接入过程与性能开销

[返回本部分学习目录](../Campus-and-Wireless.md)

## 1. 从扫描到业务

客户端发现SSID/BSSID，选择AP，进行相应802.11认证/关联、安全认证与密钥建立，随后获取地址并访问服务。802.11帧层的认证与802.1X用户/设备认证不是同一概念；WPA3-SAE等模式的步骤也不同，不能把一种握手时序画成全部无线网络通用过程。

SSID是网络名称，BSSID标识具体基本服务集，单个AP/射频可能承载多个BSSID。只报SSID无法定位用户当时接在哪个AP、频段和信道。

## 2. 空口共享

常见Wi-Fi接入涉及竞争、退避、确认和重传，标称PHY速率不能直接当应用吞吐。管理帧、低速客户端、重传与协议首部都消耗Airtime；聚合、OFDMA/MU-MIMO等能力可能改善效率，但收益取决于终端、负载和调度支持。

| 显示值 | 正确使用 |
|---|---|
| PHY/MCS速率 | 描述某方向/时刻的物理传输能力 |
| 应用吞吐 | 包含竞争、协议、重传及主机限制 |
| 客户端数量 | 不等于同时活跃用户数 |
| Channel utilization | 需说明测量范围与窗口 |

## 3. 单方向与TCP

上/下行能力可能不同，TCP ACK也占资源。远端服务器、Internet、VPN或代理限制吞吐时，换AP不会解决。先用园区内受控测试服务，再测真实应用，区分空口与外部路径。

## 4. 练习

记录客户端关联、认证、DHCP、DNS、TCP/TLS和应用各阶段；比较近AP/远AP、低负载/高负载。测试前声明包长、方向、流数和终端能力，不能拿一个测速页面覆盖整个WLAN验收。

[园区无线架构](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html)、[EAP机制RFC3748](https://www.rfc-editor.org/rfc/rfc3748.html)。
