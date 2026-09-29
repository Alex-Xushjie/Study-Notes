# Internet Edge：从 BGP 会话到运营策略

## 1. Transit、Peering 与 IXP

Transit 购买到互联网其他网络的可达性；peering 在约定范围交换彼此及客户路由；IXP 提供互联基础设施，接入 IXP 并不等于所有成员都和你互联，也不等于获得完整 Internet transit。ASN 表示策略域，不是设备编号。

Default-only、partial、full table 的选择取决于出口控制粒度、内存/FIB、收敛和运营能力。两条默认路由可以满足某些双 ISP 需求，接收全表也不自动等于更高可用性。先定义自己是否只对外发布自有前缀，避免成为免费 transit。

## 2. 两个方向分开设计

出站是“我去别人”，可在本 AS 内用 local preference 等策略选择出口；入站是“别人来我”，只能通过公告、运营商 community、prepend 等影响对方决策，不能保证对方采用。MED 的比较条件、是否跨不同邻 AS 比较都要按策略/平台核实。

| 工具 | 主要用途 | 边界 |
|---|---|---|
| Local preference | 本 AS 出站优先级 | 需要内部一致传播 |
| AS-path prepend | 影响远端选路 | 对方 local-pref 可能优先于路径长度 |
| Communities | 向运营商请求策略或标记路由 | 数值语义需查该运营商文档 |
| Selective advertisement | 选择向谁发布什么 | 更具体路由可能被过滤；注意容灾撤销 |
| Max-prefix | 限制接收规模 | 动作/计数口径依平台，不替代前缀过滤 |

先用正向 prefix-list 明确允许出口的自有前缀，再做属性修改。将“允许宣告”和“怎么宣告”分为两层，便于审查。

## 3. IRR、ROA、RPKI/ROV

IRR route/route6 与相关对象用于表达注册路由策略和生成过滤器；数据库内容质量和更新流程影响结果。RPKI ROA 将前缀、允许 origin ASN、maxLength 关联到可验证授权。路由器通过验证缓存取得验证数据，再对所见路由做 origin validation。

ROV 的手算规则：没有覆盖该路由前缀的授权数据 → NotFound；存在覆盖且至少一条同时允许 origin ASN 和长度 → Valid；存在覆盖但没有任何一条允许 → Invalid。它不验证整条 AS_PATH，也不能替代防路由泄漏策略。参见 [RFC 6811](https://www.rfc-editor.org/rfc/rfc6811) 的验证过程。

例：文档前缀 203.0.113.0/24 的模拟 ROA 为 AS65000，maxLength=24。AS65000 宣告 /24 有效；AS65001 宣告 /24 无效；AS65000 宣告其中 /25 也无效。另一个没有覆盖授权的前缀是 NotFound，不能偷换为 Valid。仅为离线练习，不向公网发布私有 ASN/文档前缀。

运维还要考虑 validator 失联、缓存过期、双缓存和变更流程；不能把“缓存连不上”机械等同于所有路由 Invalid。

## 4. DDoS 的三个处置层次

RTBH 是把匹配目标的流量丢弃，保护链路/其他业务，但被黑洞目标的正常服务通常也不可达。若入口链路已被打满，只在本地路由器丢包无法释放上游链路容量，必须与上游配合。

FlowSpec 发布带匹配条件和动作的规则，例如匹配目的前缀、协议、端口后限速或丢弃。必须限制规则来源、匹配范围、动作和传播，并设计撤销/失效处理。阅读 [RFC 8955](https://www.rfc-editor.org/rfc/rfc8955) 的 match、traffic filtering actions、validation，而不是只记“比黑洞更精细”。

清洗中心通过牵引、过滤和回注保留正常业务，需设计隧道、MTU、回程和容量。选择之前确认攻击是带宽、pps、协议状态还是应用层瓶颈。

## 5. 把 HA 问题问完整

双 ISP 架构还要覆盖 CE、光纤物理路径、电源、边界防火墙状态、内网路由。故障检测可能是物理 down、BGP hold、BFD 或业务探测，各自覆盖范围不同。ISP 时延高但 BGP 正常时，BGP 不会自动知道“更慢”；使用测量驱动策略要考虑阈值、抖动、回切和误判。

面试题：如何优先让入站走 ISP2？参考：先查该 ISP community 能控制的策略，再考虑 prepend/selective announcement；解释无法完全控制全网选路，并从多个外部观测点验证。
