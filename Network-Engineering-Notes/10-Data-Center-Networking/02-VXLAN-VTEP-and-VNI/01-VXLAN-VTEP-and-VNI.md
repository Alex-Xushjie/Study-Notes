# VXLAN封装、VTEP与VNI

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 内外层分开

VTEP负责封装/解封VXLAN，VNI标识相应逻辑网络。VLAN通常是本地接入映射，VNI是Overlay标识，二者可以映射但不能把数值相同当成协议要求。VNI字段24位不代表设备真的支持同数量业务对象。

内层包含业务以太帧，外层IP负责到远端VTEP，UDP与VXLAN首部携带隧道信息。常见目的端口4789需按实际部署核对；外层UDP源端口可提供Hash熵，不是业务应用源端口的直接替身。

| 检查层 | 内容 |
|---|---|
| 接入 | VLAN、MAC、接口与租户归属 |
| 映射 | Bridge Domain、L2VNI、VRF/L3VNI |
| 控制 | 远端MAC/IP与VTEP来源 |
| 传输 | 外层源/目的、路由、MTU和过滤 |
| 解封 | VNI是否存在、目标FIB/FDB与本地出口 |

## 2. 数据与控制

VXLAN本身描述数据封装，不等于EVPN。静态/Flood-and-learn与BGP EVPN学习方式不同，不能认为建了VXLAN接口就自动有远端MAC控制面。

## 3. 身份与隔离

VNI区分逻辑域，不是加密或源真实性保证。VTEP接入与Underlay安全、租户路由/ACL仍需设计，不能允许任意外部主机送VXLAN报文进入生产Fabric。

## 4. 练习

画同网段Host-A→远端Host-B的内外地址、MAC、VNI和封装点。分别故意错VLAN映射、VNI、远端端点和MTU，预测两端计数/抓包差异。

[VXLAN RFC7348](https://www.rfc-editor.org/rfc/rfc7348.html)、[EVPN Overlay RFC8365](https://www.rfc-editor.org/rfc/rfc8365.html)。
