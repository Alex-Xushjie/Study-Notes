# PKI、证书链、名称与生命周期

[返回本部分学习目录](../Network-Security-and-Access.md)

## 1. 证书解决什么

证书把公钥与相应身份信息关联，由信任体系和验证规则决定是否接受。私钥需由主体安全保管；证书文件本身与私钥不是同一个对象。加密、服务器认证和客户端认证也不是同义词。

验证通常涉及信任链、有效期、预期名称、Key Usage/EKU、算法/平台策略及适用的撤销机制。浏览器信任不证明VPN客户端或Supplicant使用同一信任库。

| 对象 | 常见问题 |
|---|---|
| 服务端证书 | SAN与访问名不匹配、链不完整 |
| 客户端证书 | 身份映射、用途、私钥不可用 |
| 根/中间CA | 信任缺失、错误分发、到期/轮换 |
| 时间 | 设备时钟错误导致未生效/过期判断 |
| CRL/OCSP | 网络不可达、缓存、故障策略与隐私 |

## 2. 只读查看

OpenSSL是证书/密码工具，下面只读取你准备的实验公开证书，不读取私钥、不修改系统信任：

~~~bash
openssl x509 -in lab-server.pem -noout -subject -issuer -dates -ext subjectAltName
~~~

需已安装支持相应选项的版本。输出能展示字段，不代表已完成所有链、撤销、名称和应用用途验证。lab-server.pem不存在时是前置文件缺失，不是网络故障。

## 3. 续期与轮换

自动续期需监控实际部署和客户端信任，而不只看CA签发成功。中间CA轮换、客户端离线、旧链缓存和服务重载都可能影响。预留重叠窗口与测试用户，记录旧证书退役条件。

## 4. 练习

用隔离测试CA构造过期、缺中间链、名称错误、用途不符和不受信根，比较TLS/VPN/EAP日志。不要在生产改时钟或关闭验证，避免把-k/accept-any写成修复步骤。

[PKIX RFC5280](https://www.rfc-editor.org/rfc/rfc5280.html)、[TLS1.3 RFC8446](https://www.rfc-editor.org/rfc/rfc8446.html)、[OpenSSL x509](https://docs.openssl.org/master/man1/openssl-x509/)。
