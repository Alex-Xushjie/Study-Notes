# 离线序号分析与反例验证

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 限定教学模型

下面程序仅分析同一channel/session的有限整数序号列表，已知期望区间，区分最终缺失、重复与相对最高已见序号的迟到。它不是线上A/B仲裁、协议解码或完整恢复引擎。先分离会话和频道，特殊协议标记不能塞进普通序号。

保存为sequence_audit.py，无第三方依赖，不发网络请求：

~~~python
def analyze_sequences(events, first, last):
    if type(first) is not int or type(last) is not int or not 0 <= first <= last:
        raise ValueError("invalid expected range")
    if last - first > 10000:
        raise ValueError("range too large for this teaching example")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    seen = set()
    duplicate = 0
    late = 0
    high = first - 1
    for seq in events:
        if type(seq) is not int or not first <= seq <= last:
            raise ValueError("sequence outside expected range")
        if seq in seen:
            duplicate += 1
            continue
        if seq < high:
            late += 1
        seen.add(seq)
        high = max(high, seq)
    return {"unique": len(seen), "duplicate": duplicate, "late": late,
            "missing": sorted(set(range(first, last + 1)) - seen)}

if __name__ == "__main__":
    print(analyze_sequences([100, 102, 101, 102, 104], 100, 104))
~~~

预期unique=4、duplicate=1、late=1、missing=[103]。101只是相对先到的102迟到，最终不缺101。已知区间尾部未收到也被算缺失，所以必须声明采集窗口完整覆盖。

## 2. 必测反例

正常连续、相同包重复、先乱序后补齐、真正缺口、空采样、非法类型和超大范围。重复不能推进期待序号，日切数据必须另开会话分析。不同Feed的重复可能是正常冗余，不应只报错误而不说明业务意义。

## 3. 工程扩展

真实流需要有限重排窗口、时间/数量上限、序号回绕/特殊值、消息计数、会话切换、持久化与Recovery状态。不要把离线全量set用于无限在线流，也不根据这个样例自动触发真实重传。

## 4. 交付

提供输入、区间、采集/过滤规则与结果，注明日志/抓包自身是否缺失。本次可验证标准库逻辑，不代表验证交易所协议或真实行情完整性。

[Python集合](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)、[自动化测试方法](../../04-Network-Automation/08-Git-Testing-and-CI/02-Offline-Tests-Fixtures-and-Device-Validation.md)。
