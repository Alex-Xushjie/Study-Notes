# 数据类型、循环、函数与输入验证

[返回网络自动化目录](../Network-Automation.md)

## 1. 用业务含义选择类型

设备名是字符串，VLAN ID是整数，接口集合是列表，设备属性常用字典，唯一标识集合可用set。None表示缺失/未知，不能随意当成False或0。"false"是非空字符串，在if中会被视为真，必须先正确解析。

列表适合顺序处理，字典适合按稳定键查找。两个设备名称相同却处于不同站点时，不能随便用名称覆盖；先确定device_id等唯一标识。

## 2. 循环与函数

for逐项处理，函数把一个明确任务封装为输入和返回结果。下面程序独立可运行，只验证教学清单，不连接设备：

~~~python
from ipaddress import ip_address

def validate_device(device):
    if not isinstance(device, dict):
        raise ValueError("device must be an object")
    name = device.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name is required")
    address = device.get("management_ip")
    if not isinstance(address, str):
        raise ValueError("management_ip must be text")
    ip_address(address)
    vlan = device.get("vlan")
    if type(vlan) is not int or not 1 <= vlan <= 4094:
        raise ValueError("vlan must be an integer in 1..4094")
    return name

sample = {"name": "lab-r1", "management_ip": "192.0.2.10", "vlan": 100}
print("valid:", validate_device(sample))
~~~

import导入模块，def定义函数，return返回值，raise报告无效输入。get缺键时通常返回None，不能把缺失管理IP悄悄替换成某个生产地址。type(vlan) is int这里还排除Python中属于int子类的bool。

## 3. 验证层次

格式正确只是第一层：192.0.2.10可解析为IP，不说明它可达、属于允许站点或是正确设备；VLAN 100合法，不代表该平台/业务允许创建。还需范围、唯一性、引用关系与业务约束。

| 层次 | 例子 |
|---|---|
| 类型/格式 | VLAN必须为整数，IP可解析 |
| 范围 | VLAN合法、描述长度与字符约束 |
| 唯一性 | 管理IP、设备ID不能冲突 |
| 引用 | 接口所属设备存在，VRF已定义 |
| 业务 | 生产与访客不允许互通 |

## 4. 错误与异常

拼写错误可能产生NameError，类型不合适可能TypeError，非法值可用ValueError。异常是“本次操作没有按正常路径完成”的信号，不应except后假装成功。展示给用户的错误可简洁，但报告要保留设备ID、阶段和原因。

## 5. 练习

测试缺name、非法IP、VLAN字符串、True、0、4095，以及重复地址。分别区分单条数据格式和整批清单约束。先做这些离线反例，再考虑设备操作。

[Python控制流](https://docs.python.org/3/tutorial/controlflow.html)、[ipaddress](https://docs.python.org/3/library/ipaddress.html)、[异常](https://docs.python.org/3/tutorial/errors.html)。
