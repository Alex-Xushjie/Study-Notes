# DNS排障、缓存与私有端点案例

[返回云与混合网络目录](../Cloud-and-Hybrid-Networking.md)

## 1. 先记录谁问谁

记录客户端实际DNS配置、查询名/类型、指定服务器、CNAME链、最终地址、TTL、状态码与耗时。系统Resolver、浏览器安全DNS、容器DNS与应用内部缓存可能不同，不只查/etc/resolv.conf就下结论。

Linux中dig是DNS查询工具，resolvectl用于支持systemd-resolved的系统；没有该服务时用系统对应工具。10.100.0.53是实验DNS地址，实际替换为隔离环境解析器。

~~~bash
resolvectl status
dig @10.100.0.53 app.cloud.example.com A
dig @10.100.0.53 app.cloud.example.com AAAA
dig @10.100.0.53 app.cloud.example.com A +tcp
~~~

example.com为保留示例域，本教材未创建这些记录。NXDOMAIN表示相应名称不存在，NOERROR但无A记录可能是没有该记录类型，SERVFAIL与超时也不同。查询不一定因网络失败才没有地址。

## 2. 私有端点三类故障

| 现象 | 首先区分 |
|---|---|
| 云VM解析私网，本地解析公网 | 私有区可见性与条件转发，不先改路由 |
| 两边解析相同私网IP，只有本地超时 | 私网路由、规则、端点服务与回程 |
| TCP/TLS正常，服务拒绝 | 身份、资源/端点策略、服务授权 |

多子资源服务可能需要多个私有区/记录。手工只改一个A记录会让部分API通、另一些失败。保存完整CNAME链并核对服务文档。

## 3. 保留TLS主机名的测试

若隔离实验HTTPS服务证书覆盖app.cloud.example.com，可临时指定解析来区分DNS与业务路径：

~~~bash
curl --resolve app.cloud.example.com:443:10.30.1.10 --connect-timeout 3 --max-time 10 https://app.cloud.example.com/
~~~

此命令仍校验证书并保留主机名；环境没有对应服务/证书时失败是前置条件问题。不用-k掩盖证书错误，不把直接访问IP当作同等测试。

## 4. 缓存与切换

DNS TTL、负缓存、应用连接池和客户端缓存各有生命周期。权威记录更改不等于所有旧会话立即换目标。对比指定解析器与应用实际结果，先收集证据再有范围清缓存，避免清理后失去定位线索。

## 5. 实验交付

注入错误转发、缺失私有区关联、过宽私有区、TCP53被阻断和旧缓存五种条件。每次固定查询点/解析器并恢复，提交查询链、响应码、业务请求及差异。无真实云环境时仅能证明模拟DNS逻辑。

[DNS基本机制：RFC1034](https://www.rfc-editor.org/rfc/rfc1034.html)、[负缓存：RFC2308](https://www.rfc-editor.org/rfc/rfc2308.html)、[curl官方手册](https://curl.se/docs/manpage.html)。
