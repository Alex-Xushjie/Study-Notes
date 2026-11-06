# Jinja2模板、严格变量与离线渲染

[返回网络自动化目录](../Network-Automation.md)

## 1. 模板只负责表达，不决定业务

Jinja2把结构化输入代入文本。变量输出常用{{ name }}，循环/条件常用{% ... %}。地址是否合法、接口归属、允许的命令和管理范围应先在数据层验证，不把所有逻辑藏进模板。

模板渲染成功只说明生成了文本，不说明NOS会接受、路由正确或业务可用。生成、差异、发布与验证是四个不同步骤。

## 2. 完整离线示例

下面保存为render_description.py，需项目虚拟环境已安装选定版本Jinja2，不连接设备、不写文件：

~~~python
from jinja2 import Environment, StrictUndefined

def render_interface(data):
    if set(data) != {"name", "description"}:
        raise ValueError("unexpected or missing fields")
    if data["name"] not in {"Ethernet1", "Ethernet2"}:
        raise ValueError("interface outside lab allowlist")
    description = data["description"]
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description is required")
    if not all(ch.isascii() and (ch.isalnum() or ch in " _-.:/") for ch in description):
        raise ValueError("description contains unsupported characters")
    if len(description) > 64:
        raise ValueError("description too long for this lab contract")
    env = Environment(undefined=StrictUndefined, autoescape=False,
                      keep_trailing_newline=True)
    template = env.from_string("""interface {{ name }}
 description {{ description }}
""")
    return template.render(**data)

print(render_interface({"name": "Ethernet1", "description": "LAB uplink"}), end="")
~~~

StrictUndefined让缺少变量报错，避免静默空值。autoescape=False用于这里的网络纯文本，不可照搬到HTML输出。字符白名单与长度只是本实验契约，不是所有NOS通用限制；阻止换行等内容进入命令可减少配置注入风险。

三引号字符串可包含实际换行。保存代码时保持缩进和模板换行，避免复制时把引号内的内容拆坏。

## 3. 确定性与差异

固定输入排序、换行和缺省值，避免每次变更无意义。保留模板/输入版本与生成物哈希，生成文件不能夹带真实口令或令牌。用语义检查辅助文本diff，不能只看行数。

## 4. 反例

缺描述应失败，不生成空description；描述带换行应失败，不能插入额外命令；未知接口应失败，不能自动扩大范围；同输入两次输出应一致。模板不应该在缺数据时自动渲染no/删除操作。

## 5. 练习

先运行正常渲染，再测试四个反例并审查diff。将模板分离成文件作为扩展，同时保留StrictUndefined和数据校验。学习完成的标准是解释每条生成命令为什么存在，而不只是能批量输出文本。

[Jinja API与Undefined](https://jinja.palletsprojects.com/en/stable/api/)、[模板语法](https://jinja.palletsprojects.com/en/stable/templates/)。
