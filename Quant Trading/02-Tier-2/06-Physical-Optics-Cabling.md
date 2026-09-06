# Physical Infrastructure, Optics and Cabling

## 1. 你必须能读懂 optic 参数

- Form factor/速度：SFP+/SFP28/QSFP28/QSFP-DD 等只是外形/代际线索，仍需核对 host compatibility。
- Reach/介质：SR 常配 multimode，LR/ER 等常配 single-mode；具体波长/reach 以 datasheet。
- Connector：LC duplex、MPO/MTP；breakout 时确认 lane mapping/polarity。
- FEC：双方模式必须兼容；corrected error 增加是链路退化信号，uncorrectable 会丢帧。
- DOM/DDM：Tx power、Rx power、temperature、voltage、bias current。

## 2. Optical power budget

```text
received_power ≈ transmitter_power
               - fiber_loss
               - connector/splice loss
               - splitter/TAP loss
               - engineering margin
```

验收要同时满足接收灵敏度与最大输入，太强也可能过载。TAP 分光比会给两侧带来不同损耗；不能只看 link up。记录 baseline，趋势往往比单次“仍在范围”更有价值。

## 3. 常见物理错误

- Tx/Rx polarity 反、A/B 标签交换、错误 patch-panel position。
- 单模/多模或 optic 类型不匹配，脏端面、弯曲半径过小。
- 两端 speed/FEC/autoneg 配置不一致。
- Breakout lane/port mapping 错。
- Duplex link 只坏一个方向；link 可能 up 但 CRC/FEC 持续增长。
- 备线与主线共走一个 tray，被一次施工同时影响。

## 4. Counter 的含义

| Counter/状态 | 常见方向 |
|---|---|
| LOS / link flap | 光功率、patch、optic、远端端口 |
| CRC/FCS | 物理信号、optic/fiber、端口；也可能坏设备 |
| FEC corrected | 链路 margin 下降，尚可修正但需趋势告警 |
| FEC uncorrected | 数据不可恢复，packet loss |
| input discard | buffer/ACL/资源，不一定物理层 |
| output discard | egress congestion/microburst |

先记录 counter delta 和时间，不要看累计大数字就判定当前故障。清 counter 前保存证据并获准。

## 5. Copper/DAC/AOC/fiber 取舍

- DAC：短距、低成本/功耗，粗重且 vendor/长度限制。
- AOC：比 DAC 轻、距离更长，端头不可更换。
- MMF：短距数据中心，MPO polarity/清洁要求高。
- SMF：通用长距、未来扩展好，optic 成本/功率可能更高。

低延迟项目不要只追求理论最快：兼容性、可获得的现场 spare、诊断能力和稳定性通常更重要；任何差异都用平台/optic/长度实测。

## 6. Rack/power/cabling

- 双 PSU 到真正独立 A/B PDU；按 nameplate/实测做 power budget 和 breaker margin。
- Front-to-back airflow 对齐，避免热风回流；监控 inlet temperature。
- 统一 cable ID：`site-rack-device-port__to__site-rack-device-port`，两端一致。
- 交易、管理、capture、time cable 颜色可区分，但以标签/记录为权威。
- 留 service loop 但不堆压光纤；保护弯曲半径；端口变更后更新图和照片。

## 7. Link turn-up 顺序

1. 核对 part number/兼容矩阵和两端 config。
2. 清洁、插入、确认 polarity。
3. 读两端 DOM 与 LOS/FEC/PCS 状态。
4. 跑 traffic/BERT（能力允许）并观察 counter delta。
5. 拔插/切备验证告警、冗余和文档。
6. 保存正常 baseline。

## 8. 30 秒回答

> For a link turn-up I verify the complete compatibility chain: platform, optic, wavelength, medium, reach, connector, speed and FEC. I calculate the optical budget including connectors, splices, TAP loss and margin, then record DOM and error-counter baselines at both ends. Link-up alone is not acceptance; I test traffic and failure behavior and watch CRC and corrected or uncorrectable FEC deltas. I also validate physical diversity, power feeds, polarity and end-to-end labeling because many apparent protocol incidents are actually layer-one or documentation failures.

