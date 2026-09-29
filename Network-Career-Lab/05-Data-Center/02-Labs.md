# 数据中心实验：先最小闭环，再增加冗余

本阶段是平台适配实验，使用 EVE-NG 合法 NOS 镜像或 Linux/FRR。FRR 的完整 Linux VRF、bridge、VXLAN 接口创建方式以 [官方 EVPN 配置示例](https://docs.frrouting.org/en/latest/evpn.html) 为准；先固定版本并从该版本示例构建，不能把厂商 CLI 混成“通用可执行配置”。

## D1 Underlay

最小拓扑：L1—S1—L2，H1 接 L1，H2 接 L2；通过后增加 S2 并让每个 leaf 同时连两 spine。Spine 可不作为 VTEP。

| 节点 | Underlay ASN | Loopback/VTEP | 连接网段 |
|---|---|---|---|
| S1 | 65100 | 10.255.0.1/32（仅 loopback） | L1:10.0.0.0/31，L2:10.0.0.2/31 |
| L1 | 65101 | 10.255.1.1/32 | S1 取 10.0.0.0，L1 取 10.0.0.1 |
| L2 | 65102 | 10.255.1.2/32 | S1 取 10.0.0.2，L2 取 10.0.0.3 |

步骤：配置端口与 loopback → eBGP 相邻节点会话 → 明确允许连接网段/loopback 的策略 → 查看 RIB/FIB → 指定 VTEP 源地址 ping 对端 VTEP → 用大包验证 underlay MTU。

预期：VTEP /32 双向可达；不能只用物理接口地址 ping 判定通过。注入：撤销 L2 VTEP /32，观察物理邻居仍正常而 overlay 数据面受损；恢复公告再验证。

## D2 同子网 EVPN/VXLAN

为简化实验，overlay 可使用 leaf loopback 间 eBGP EVPN multihop；spine 只转发 underlay。开启 l2vpn evpn 地址族，设置明确 RT，按平台配置 VXLAN/bridge/SVI。生产方案可另选 spine RR/iBGP 模式，两种模式的 next-hop 与策略不同，不在同一个小实验中混用。

租户 A：VLAN 10 ↔ VNI 10100，RT 65000:10100。H1=10.10.10.11/24，H2=10.10.10.12/24。先生成 ARP/流量再查看 Type 2；Type 3 反映 VNI 参与信息。

检查顺序：EVPN 邻居 → advertised/received routes → 导入后的 EVPN 路由 → 本地 MAC/FDB/邻居 → VXLAN 远端端点 → 主机 ping。Linux 侧可查看 `bridge fdb show`、`ip -d link show`；FRR 侧参考 `show bgp l2vpn evpn`。underlay 抓 `udp port 4789`，记录外层 VTEP 与内层主机地址。

故障：只修改 L2 的导入 RT，预期 BGP 邻居仍 up，但目标租户路由不被正确导入；恢复后对比控制面和主机连通性。解释为什么不能通过重启所有 BGP 来定位问题。

## D3 跨子网与 Type 5

增加 VLAN 20/VNI 10200，网段 10.20.20.0/24，租户 VRF `TENANT-A`，示例 L3VNI 50000。明确选 symmetric IRB，配置平台所需 anycast gateway 和 VRF 路由。先在两个 leaf 上逐步验证 SVI、本地跨子网，再做远端跨子网。

另接一个边界路由器公告 10.90.0.0/24，按平台把该前缀导出为 Type 5；记录 prefix、RT、next-hop 及解析依赖。不要用同子网 Type 2 实验冒充 Type 5 验证。

故障：去掉外部前缀导出策略，预期本地 RIB 仍存在但远端 EVPN 不再学习；恢复策略后核对业务。第二故障：缩小 underlay MTU，验证小包和大包差异。

## D4 冗余与验收

增加 S2 与独立链路，写出新增 /31 和 ASN 策略。比较单流/多流，解释 ECMP hash；关一条 uplink，记录业务丢包和剩余容量。删除整个 leaf 的影响不能用单 uplink 故障替代。

扩展：有支持 EVPN multihoming 的镜像时，为一台主机配置双归属 ESI，观察 Type 1/4 和 DF 状态，分别断 member/leaf。没有镜像时提交 DF/BUM/已知单播的逐向转发图，并标注未实跑。

交付：地址/VNI/RD/RT 台账、控制面和数据面基线、至少三种故障记录、Enterprise DC 与 L3-to-server 选择说明。通过条件：能在 15 分钟内把一次不通归到 underlay、overlay、租户映射、主机四层之一并出示证据。
