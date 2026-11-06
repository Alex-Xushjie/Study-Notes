# JSON、YAML、CSV与数据契约

[返回网络自动化目录](../Network-Automation.md)

## 1. 文件格式不等于数据模型

JSON/YAML描述数据，CSV描述行列。格式能解析不等于业务有效：管理IP可能重复，平台字段可能错拼，某接口可能引用不存在的VRF。数据契约要规定字段、类型、必填、缺失含义、允许值和版本。

下面保存为inventory.json，可供前文count_inventory.py读取。192.0.2.0/24为文档示例网段，不是可连接设备：

~~~json
{
  "schema_version": 1,
  "devices": [
    {"device_id": "lab-r1", "name": "lab-r1", "management_ip": "192.0.2.10", "platform": "cisco_ios", "site": "lab"},
    {"device_id": "lab-r2", "name": "lab-r2", "management_ip": "192.0.2.11", "platform": "cisco_ios", "site": "lab"}
  ]
}
~~~

device_id应稳定，name是可读标签；platform在此为连接驱动示例，不是通用标准平台编码。凭据不放进这个文件，使用credential_ref等引用由运行时解析。

## 2. 类型陷阱

JSON的true/false/null转换成Python的True/False/None。CSV字段通常先是字符串；"100"要显式转整数。YAML缩进和隐式类型行为与解析器版本有关，IP、版本号、标识等建议明确为字符串。

YAML需要选定解析器并使用安全加载接口，例如PyYAML的safe_load；它减少任意对象构造风险，不替代资源大小限制与业务校验。不要对不可信文本使用eval，也不要把解析成功当成输入可信。

## 3. CSV的适用场景

适合简单资产表和报表，嵌套接口/VRF关系通常更适合结构化对象。用csv模块处理引号、逗号和换行，不用split(',')假装CSV解析器。导出供表格软件打开时还需考虑以=、+等开头的非预期公式内容，按消费方式转义而非修改原始事实。

## 4. 版本和缺失

schema_version用于显式区分结构，不能只是装饰字段。未知版本应拒绝或走受控转换。将“不适用”“未知”“采集失败”“明确为空”分开，不能全部填空字符串。缺关键字段时不默认下发删除配置。

## 5. 练习

把教学清单转CSV再读回，确认类型变化；增加重复device_id和管理IP，验证整批约束。设计旧字段mgmt_ip迁移到management_ip的显式转换，保留转换来源和错误。

[JSON模块](https://docs.python.org/3/library/json.html)、[CSV模块](https://docs.python.org/3/library/csv.html)、[PyYAML安全加载](https://pyyaml.org/wiki/PyYAMLDocumentation)。
