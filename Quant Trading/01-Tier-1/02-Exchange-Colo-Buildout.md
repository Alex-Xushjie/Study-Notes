# Exchange Colo Buildout

## 1. 交付链条

```text
Commercial/legal
  -> exchange membership/data agreement/port order
  -> cage/rack/power/cross-connect/LOA-CFA
  -> hardware staging and golden config
  -> remote hands install + labeling
  -> L1/L2/L3 turn-up
  -> exchange conformance/certification
  -> market rehearsal
  -> production acceptance and handover
```

**LOA/CFA**（Letter of Authorization / Connecting Facility Assignment）授权并说明 cross-connect 两端、位置和介质。真正项目里最常见的延期往往不是 BGP，而是订单、端口、授权、光纤极性、remote hands 或错误 demarc。

## 2. 需求和 BOM

### Exchange 侧

- market data feed A/B、order entry session、drop copy、reference data、test/UAT、VPN/portal。
- 每项的物理端口、速度、介质、VLAN/IP、source/destination、multicast groups、ACL、session credentials。
- 是否必须双 switch/双 meet-me room、是否允许 LACP、静态路由还是 BGP、认证和 conformance test。

### Colo 侧

- Rack units、A/B power feed、PDU 插头/功率、散热、重量、cage access、remote hands SLA。
- Cross-connect 数量、single-mode/multi-mode、LC/MPO、polarity、patch panel、demarc。
- Out-of-band carrier、console server、LTE/独立管理备份（按场地政策）。

### 设备侧

- ULL/L1 switch、一般 L3 switch、router、server/NIC、TAP/packet broker、time appliance。
- Optics 与备件：同 vendor qualification、速率、波长、reach、DOM 支持。
- 备件不是“仓库里有”，而是明确 RMA/现场 spare、配置恢复和 remote hands 步骤。

## 3. 推荐的物理和逻辑设计

```text
Exchange MD-A -- XC/MMR-A -- Switch-A -- NIC-A server pair
Exchange MD-B -- XC/MMR-B -- Switch-B -- NIC-B server pair

Exchange OE-A -- XC/MMR-A -- OE-Switch-A -- Gateway-A
Exchange OE-B -- XC/MMR-B -- OE-Switch-B -- Gateway-B

OOB carrier ---- mgmt switch ---- console/IPMI (separate power/path)
GM-A/B ---------- timing network -- switches/NIC PHCs
TAP/replication ------------------- capture/recorder
```

不要机械复制此图。小环境可以复用交换机，关键是主动说明复用带来的 blast radius，并确保 feed A/B 不被一个组件同时切断。

## 4. 实施检查表

### Staging

- 记录序列号、资产、OS/firmware、license；烧机并测试所有端口/PSU/fan。
- 生成并 review golden config；关闭不需要的协议，设置 AAA、NTP/PTP、syslog、SNMP/streaming telemetry。
- 用流量发生器验证 line rate、frame size、multicast replication、ACL 和 failover。
- 留存 config diff、checksum、rollback image 和 console recovery 方法。

### Physical install

- 双 PSU 分别接 A/B PDU；验证而非只看标签。
- 从设备端到 patch panel、cross-connect、exchange port 统一命名并拍照。
- 清洁光纤端面；确认 Tx/Rx polarity、光功率预算和 DOM。
- 电源、光纤、管理线分开布放；不让 A/B 路径共用容易被一次操作拔掉的走线。

### Turn-up

1. L1：LOS、speed/FEC、DOM Tx/Rx、错误计数。
2. L2：VLAN/tag、MAC learning、IGMP snooping/querier（如适用）、MTU。
3. L3：ARP/ND、route、TTL、ACL、BFD/BGP session。
4. Application：multicast sequence、snapshot/retransmission、OE logon/heartbeat、ACK/drop copy。
5. Performance：不同负载/frame size 下的 latency distribution、loss、burst tolerance。
6. Failure：拔单路光、电、重启设备、停 routing/session；验证业务而不只看 ping。

## 5. Production acceptance

验收证据应包括：

- As-built diagram、rack elevation、circuit ID、LOA/CFA、port/IP/VLAN/group matrix。
- 配置版本、baseline counters/DOM、吞吐和 latency 基线。
- Conformance/UAT/market rehearsal 结果。
- Owner/contact/escalation、RMA/remote hands、MOP/rollback、known risks。
- 监控告警已经接入且有人接收；时间、capture、OOB 都测试过。

## 6. 常见失败

| 现象 | 优先检查 |
|---|---|
| Link up 但无行情 | VLAN、IGMP join、ACL、source/group、exchange entitlement |
| A feed 正常 B feed 丢包 | 物理光功率/FEC、独立路径设备 counter、应用 line arbitration |
| OE TCP 通但 logon 被拒 | session/CompID、source IP、sequence/reset policy、交易时段 |
| 延迟比 UAT 高 | 测量点、负载、production path、speed/FEC、queue、CPU/NUMA |
| 切电两路都掉 | 双 PSU 接到了同一 PDU/上游，或 chassis 有共同故障 |

## 7. 2 分钟回答模板

> A colo build starts with a dependency matrix, not rack-and-stack. I map every exchange service to its commercial order, physical demarc, network parameters, application owner and test requirement. I design A/B feeds and order paths across independent switches, power and—where offered—meet-me rooms. Hardware is staged with a reviewed golden config and load/failure tests. On site I validate power and fiber polarity, establish an L1 counter and DOM baseline, then turn up L2/L3 before application sessions. Acceptance requires sequence-level market-data validation, order-entry and drop-copy reconciliation, synchronized latency measurements, and real failure tests. The handover includes as-built documents, monitoring, escalation paths, spares and a rollback-ready MOP.

