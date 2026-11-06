# 健康检查、预期集合与UNKNOWN

[返回网络自动化目录](../Network-Automation.md)

## 1. 检查必须有意图

接口oper_down不一定异常，可能本来停用；BGP Established不代表所需前缀都存在；OSPF广播网段两个DROTHER保持2-Way可以正常。健康标准依赖拓扑角色与业务要求，而不是把字符串UP全部判通过。

PASS表示已获得足够证据且符合规则，FAIL表示可靠事实违反规则，UNKNOWN表示采集/解析不完整等导致不能判断，N/A表示明确不适用。缺数据不自动转成PASS。

## 2. 比较预期与实际集合

只遍历实际输出会漏掉完全没出现的预期邻居。先读预期集合，再核对对应事实；采集完整时缺预期邻居可判FAIL，采集不完整时应UNKNOWN或按项目明确的分项策略处理。

下面保存为bgp_check.py，是离线教学函数；只检查FSM，不证明路由或业务完整健康：

~~~python
def evaluate_bgp(expected, snapshot):
    if not isinstance(expected, list) or not expected:
        return "UNKNOWN"
    if any(not isinstance(peer, str) or not peer for peer in expected):
        return "UNKNOWN"
    if len(set(expected)) != len(expected):
        return "UNKNOWN"
    if not isinstance(snapshot, dict):
        return "UNKNOWN"
    if snapshot.get("collection_status") != "ok" or snapshot.get("complete") is not True:
        return "UNKNOWN"
    rows = snapshot.get("neighbors")
    if not isinstance(rows, list):
        return "UNKNOWN"
    actual = {}
    for row in rows:
        if not isinstance(row, dict):
            return "UNKNOWN"
        peer, state = row.get("peer"), row.get("state")
        if not isinstance(peer, str) or not peer or not isinstance(state, str) or not state:
            return "UNKNOWN"
        if peer in actual:
            return "UNKNOWN"
        actual[peer] = state
    if any(actual.get(peer) != "Established" for peer in expected):
        return "FAIL"
    return "PASS"
~~~

函数要求归一化层已按目标平台验证状态枚举及完整性。没有配置检查项时返回UNKNOWN是本示例选择，不表示所有项目都必须如此；真实项目可明确采用N/A。

## 3. 汇总与退出码

报告保留每设备、每检查项、证据、状态与原因，不只给全局红绿灯。FAIL与UNKNOWN并存时如何汇总由契约决定；退出码非0让CI不会把未知当全通过。N/A需要原因，不能用来逃避平台适配失败。

## 4. 练习

至少准备完整健康、Idle、完整空表、采集超时、截断和重复邻居。扩展到前缀检查时要定义预期前缀/下一跳，不能只看路由总数。CRC类检查用采样增量，MLAG/VRRP类结合角色与双端。

现有[Network Health Check项目](../../../Network-Career-Lab/02-Automation/02-Project.md)提供更完整的BGP离线报告与退出码示例；它尚不等于全套12项设备检查已实现。
