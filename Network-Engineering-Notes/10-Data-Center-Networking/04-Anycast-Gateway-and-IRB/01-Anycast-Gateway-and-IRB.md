# Anycast Gateway与对称/非对称IRB

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 本地网关与分布式路由

Anycast Gateway让相应逻辑子网在多个Leaf提供一致的网关身份，主机可就近进入路由。网关IP/MAC一致需遵循平台模型和域边界，不是把任意两台路由器地址复制就获得正确多活。

IRB在桥接与路由间连接。L2VNI关联相应二层域，L3VNI用于相应VRF路由上下文的设计；具体设备对象和映射必须一致。

## 2. 两种IRB路径

非对称IRB通常入口完成路由、以目的子网二层VNI送到远端，远端做相应桥接；对称IRB两端参与相应路由，经租户L3VNI传输。两者对入口/出口需掌握的子网、端点与表规模要求不同，不能把名称理解成请求/返回是否经过同一台防火墙。

| 问题 | 检查 |
|---|---|
| 同子网 | L2VNI、MAC与接入映射 |
| 跨子网 | 主机网关、VRF路由、IRB模型 |
| 对称IRB | L3VNI/路由MAC/下一跳与出口VRF |
| 外部前缀 | Type5、边界路由与回程 |

## 3. 逐跳练习

Host-A和Host-B在同一租户不同子网，分别画入口网关处理、封装内外MAC/IP、VNI、出口路由与主机回包。不要只画一个VXLAN隧道箭头。实际命令依NOS而定。

## 4. 验收

同子网、跨子网、跨租户拒绝和外部访问分别测试。网关可ping不证明租户路由导入正确，VRF里有路由也不证明数据面路由MAC和VNI已一致安装。

[IRB RFC9135](https://www.rfc-editor.org/rfc/rfc9135.html)、[FRR对称/非对称模型](https://docs.frrouting.org/en/latest/evpn.html)。
