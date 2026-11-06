# 802.1X、EAP、RADIUS与授权

[返回本部分学习目录](../Network-Security-and-Access.md)

## 1. 三个角色

Supplicant是终端认证组件，Authenticator是交换机/AP等接入控制点，Authentication Server通常通过RADIUS等与接入点协作。EAP是认证框架，EAP-TLS是一种方法，不等于802.1X本身。

终端到接入点可通过EAPOL交互，接入点再与AAA交换相关信息。认证证明什么身份，授权决定放入什么VLAN/角色/ACL，计费/审计记录会话，三者不能混为一条“成功”。

| 阶段 | 证据 |
|---|---|
| 终端发起 | 适用配置、EAP方法、信任与证书 |
| 接入点转送 | 端口/SSID、AAA源地址与可达 |
| 服务端判断 | 身份、证书、策略命中与拒绝原因 |
| 授权落地 | VLAN/角色/ACL实际存在并应用 |
| 网络使用 | DHCP、DNS、路由与访问矩阵 |

## 2. EAP方法与服务器验证

EAP-TLS依赖证书身份与信任，TLS1.3的EAP行为有专门规范。终端需要验证服务器信任和预期名称，不能提示什么证书都接受。其他EAP方法有各自安全与部署边界，按组织基线选用，不把密码方式当所有终端的默认最佳方案。

## 3. RADIUS与传输

传统RADIUS不能简单理解成整包已加密；现代安全部署应核对认证/完整性及所支持的受保护传输。客户端/NAS身份、共享秘密、时间与防火墙路径按平台配置，日志中Access-Accept也不证明交换机授权成功。

## 4. 练习

在隔离端口完成一台受管终端认证，分别注入不受信服务器、错误用户证书、错误返回VLAN和AAA不可达。给出每种失败发生层次，不以全局MAB回退掩盖问题。

[EAP RFC3748](https://www.rfc-editor.org/rfc/rfc3748.html)、[EAP-TLS1.3 RFC9190](https://www.rfc-editor.org/rfc/rfc9190.html)、[RADIUS RFC2865](https://www.rfc-editor.org/rfc/rfc2865.html)。部署时核对更新和厂商安全公告。
