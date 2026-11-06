# Clos、Leaf-Spine与Underlay

[返回本部分学习目录](../Data-Center-Networking.md)

## 1. 拓扑和职责

Leaf接服务器/业务边界，Spine连接Leaf形成多条等价路径。典型两层Clos中Leaf经一个Spine到另一Leaf，Spine间通常不直接互连；多Pod、Super-Spine、存储或服务Leaf有各自扩展，不能把一种图当全部数据中心。

Underlay负责VTEP等端点IP可达，Overlay承载租户L2/L3。Underlay可采用eBGP或IGP，选择依据是规模、运维与收敛要求，不因EVPN使用BGP就强制所有层都同一协议。

| 对象 | 需要定义 |
|---|---|
| 点到点链路 | 地址/接口、MTU、速率、邻接与BFD |
| Loopback | 唯一性、VTEP/路由ID用途与发布范围 |
| ASN/区域 | 编号、聚合与防环策略 |
| ECMP | 下一跳数量、Hash、硬件和故障重选 |
| 管理 | 独立访问、遥测、备份与恢复 |

## 2. 路由发布边界

Underlay只发布需要的基础端点/链路，不默认导入全部租户前缀。Loopback可达不代表VXLAN封装允许或EVPN路由已安装；BGP邻居UP也不证明FIB完整。

eBGP设计需明确AS_PATH、防环、最大跳数、Next-Hop与聚合；不要为了让路由出现全局打开允许自身AS或忽略AS_PATH。特定部署可有受控策略，但须解释边界。

## 3. 故障域

单Spine失败不应完全隔离Leaf，但剩余链路容量、Hash重映射和队列可能变差。光模块、板卡、电源、线缆路径与管理平台共同依赖要画出。

## 4. 练习

画2Spine/3Leaf，标所有链路、Loopback与ASN，推导任一链路/Spine失效的RIB/FIB与业务路径。虚拟拓扑可验证逻辑，不证明ASIC吞吐和真实板卡故障。

[BGP数据中心经验RFC7938](https://www.rfc-editor.org/rfc/rfc7938.html)、[BGP基础](../../01-Routing-and-Switching/06-BGP/01-BGP.md)。
