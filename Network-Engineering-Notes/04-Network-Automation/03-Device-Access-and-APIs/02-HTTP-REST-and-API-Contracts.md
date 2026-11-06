# HTTP API、认证、分页与超时

[返回网络自动化目录](../Network-Automation.md)

## 1. HTTP不是Python的附属功能

HTTP是通信协议；Python的requests等库可作为HTTP客户端，其他语言与curl同样可以。REST是一类接口设计风格，不等于所有HTTPS接口都提供相同资源、字段或操作语义。

请求包含方法、URL、首部和可能的请求体；响应包含状态码、首部和内容。GET通常用于读取，POST/PUT/PATCH/DELETE按接口契约产生相应效果，不能把所有POST都理解为相同创建行为。

## 2. 区分各层成功

TCP/TLS连接成功、HTTP2xx、JSON解析成功、业务返回成功是不同条件。200也可能携带业务错误或不完整分页；202可能只表示任务被接受，需要查询异步任务完成状态。

| 状态/异常 | 常见处置 |
|---|---|
| 401/403 | 核对认证/权限，不盲目重试 |
| 404 | 查URL、资源与API版本 |
| 409/412 | 冲突/前置条件，重新核对版本与状态 |
| 429 | 按Retry-After及限流规则退避 |
| 5xx/网络超时 | 区分读写与是否已生效，再决定重试 |
| 非预期响应类型 | 保存脱敏诊断，不把登录HTML当JSON |

## 3. 只读请求片段

以下是独立脚本，需requests、已验证HTTPS API、环境变量LAB_API_URL和只读Token。路径与认证格式由目标接口定义，示例仅适用于Bearer认证的测试端点：

~~~python
import os
import requests

def main():
    url = os.environ["LAB_API_URL"]
    if not url.startswith("https://"):
        raise ValueError("use a verified HTTPS lab endpoint")
    token = os.environ["LAB_API_TOKEN"]
    response = requests.get(
        url,
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
        timeout=(3, 10),
        allow_redirects=False,
    )
    if not 200 <= response.status_code < 300:
        raise RuntimeError("unexpected HTTP status: " + str(response.status_code))
    data = response.json()
    print("top-level type:", type(data).__name__)

if __name__ == "__main__":
    main()
~~~

不使用verify=False。内网CA应通过受控CA文件/环境配置建立信任。timeout元组限制连接与读取等待，不等于完整任务总时限；还要考虑分页总量、重试次数和响应大小。

## 4. 分页与并发更新

列表可能按offset/limit、cursor或next分页。必须按契约取完、验证页数/重复ID并保存完整性状态；第一页空或失败不能作为全网不存在资源的证据。跟随next时校验同一受信来源，不把Token发到任意URL。

写入考虑ETag/If-Match、版本号与幂等键等接口支持。超时后请求可能已生效，应读回或查任务状态，不能无条件重发创建/删除。

## 5. 练习

用脱敏响应Fixture或本地Mock验证分页、429、403、HTML响应、202任务与写入超时。接口文档中的只读筛选参数需实测，不靠猜字段名。

[Requests官方快速入门](https://requests.readthedocs.io/en/latest/user/quickstart/)、[HTTP语义RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html)。
