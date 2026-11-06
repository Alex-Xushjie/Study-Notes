# 无线分层排障与证据链

[返回本部分学习目录](../Campus-and-Wireless.md)

## 1. 固定一个用户与时间窗

收集终端型号/OS/驱动、SSID/BSSID、AP、频段/信道、位置、业务、时间、MAC/会话标识。用户“Wi-Fi慢”可能指认证、DNS、SaaS或RF，先描述具体失败动作。

| 层次 | 观察 |
|---|---|
| 有线/供电 | AP端口、PoE、错误、VLAN、上联 |
| RF | 双向RSSI/SNR、竞争、重传、信道事件 |
| 802.11接入 | 扫描/关联、安全握手与拒绝原因 |
| 身份 | EAP/RADIUS、证书、授权属性 |
| IP服务 | DHCP、网关、DNS、NTP |
| 路径/应用 | 隧道、ACL、WAN、TLS与事务 |

## 2. 按范围缩小

一台终端所有位置异常，比较客户端与凭据；同AP多用户异常，查接入/RF；同SSID跨AP异常，查策略/AAA；仅Internet慢，先区分WAN与外部服务。这是优先级，不是根因结论。

AP/控制器抓包与客户端抓包位置不同，无线加密和监控模式也影响可见内容。不能将有线抓到包等同空口交付成功，或把控制面日志缺失当真实事件未发生。

## 3. 只读主机检查

Linux新手先认识ip查看系统地址/路由，resolvectl查看适用系统的DNS，curl测试具体HTTP；这些不是无线控制器命令。Windows可用系统Wi-Fi连接报告及网络命令，注意报告含内部信息。

~~~bash
ip -br addr
ip route
resolvectl status
~~~

系统不使用systemd-resolved时，第三条可能不适用；它失败不能证明DNS整体失效。

## 4. RCA练习

分别调查“满员会议室卡顿”“漫游后无IP”“认证通过但访客能进内网”。列事实、候选、区分实验和反证，再做单变量修复。恢复后验证无关终端与拒绝矩阵，不能只测一台成功。

[Linux观测工具](../../03-Linux-Networking/06-Network-Observation-Tools/01-Network-Observation-Tools.md)、[实验报告模板](../../../Network-Career-Lab/08-Portfolio/Lab-Report-Template.md)。
