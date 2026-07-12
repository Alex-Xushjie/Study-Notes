# Palo Alto PRISMA note
## Palo Alto Prisma 简介

### 1. Prisma 是什么？

**Prisma 不是一台具体设备，而是 Palo Alto Networks 推出的一组云网络和云安全产品。**

对于网络工程师来说，别人提到 Prisma，通常主要指：

* Prisma Access
* Prisma SASE
* Prisma Cloud

---

### 2. Prisma Access

可以把 **Prisma Access** 理解为：

> 部署在 Palo Alto 云端的下一代防火墙服务。

传统架构中，公司会在总部、数据中心或分支机构部署 Palo Alto 防火墙。

Prisma Access 则把安全检查能力放在 Palo Alto 的云基础设施中，由 Palo Alto 负责底层平台的部署和维护。

#### 2.1 远程用户接入

远程用户通常通过 **GlobalProtect** 接入 Prisma Access。

```text
Remote User
    │
    │ GlobalProtect
    ▼
Prisma Access
    │
    ├── Internet / SaaS
    │
    └── Service Connection
              │
              ▼
       Data Center / Headquarters
```

用户流量会先经过 Prisma Access 的安全检查，然后再访问 Internet、SaaS 或企业内部应用。

---

#### 2.2 分支机构接入

分支机构可以通过 IPsec Tunnel 或 SD-WAN 接入 Prisma Access。

```text
Branch Office
    │
    │ IPsec Tunnel
    ▼
Prisma Access
    │
    ├── Internet
    ├── Other Branches
    └── Data Center
```

分支机构和 Prisma Access 之间通常可以使用：

* Static Route
* BGP

---

#### 2.3 Service Connection

**Service Connection** 用于连接 Prisma Access 和企业内部网络，例如：

* Headquarters
* Data Center
* Private Cloud
* Internal Applications

```text
Mobile User / Branch Office
            │
            ▼
      Prisma Access
            │
            │ Service Connection
            ▼
     Data Center / Headquarters
```

通过 Service Connection，远程用户和分支机构可以访问企业内部应用。

---

### 3. Prisma Access 与传统 Palo Alto 防火墙的区别

| 对比项  | 传统 Palo Alto 防火墙  | Prisma Access                  |
| ---- | ----------------- | ------------------------------ |
| 部署位置 | 总部、分支或数据中心        | Palo Alto 云基础设施                |
| 产品形式 | 硬件或虚拟防火墙          | 云安全服务                          |
| 用户接入 | VPN 回到企业防火墙       | GlobalProtect 接入 Prisma Access |
| 分支接入 | MPLS、VPN 或 SD-WAN | IPsec 或 SD-WAN                 |
| 安全检查 | 企业本地防火墙执行         | Prisma Access 云节点执行            |
| 设备维护 | 企业自行维护            | Palo Alto 维护底层平台               |
| 路由方式 | Static、OSPF、BGP 等 | 主要使用 Static 或 BGP              |

---

### 4. Prisma SASE

SASE 的全称是：

> Secure Access Service Edge

Prisma SASE 可以简单理解为：

```text
Prisma SASE
├── Prisma Access
├── Prisma SD-WAN
└── ADEM
```

其中：

* **Prisma Access**：负责云端安全访问
* **Prisma SD-WAN**：负责分支和 WAN 连接
* **ADEM**：负责用户和应用体验监控

可以记成：

> Prisma Access 主要解决安全访问问题，Prisma SASE 同时解决连接、安全和体验监控问题。

---

### 5. Prisma Cloud

**Prisma Cloud 和 Prisma Access 不是同一种产品。**

* **Prisma Access**：保护用户和网络流量
* **Prisma Cloud**：保护公有云、容器、Kubernetes、云工作负载和应用

Prisma Cloud 更偏向：

* Cloud Security
* Container Security
* Kubernetes Security
* Workload Security
* DevSecOps

---

### 6. 简单记忆方法

```text
Prisma Access
= 云上的 Palo Alto 防火墙和安全接入服务

Prisma SD-WAN
= 分支网络和 WAN 连接

Prisma SASE
= Prisma Access + SD-WAN + 体验监控

Prisma Cloud
= 保护云平台、容器、应用和工作负载
```

---

### 7. 网络工程师的学习重点

对于网络工程师，学习 Prisma 时应重点关注：

* GlobalProtect
* Mobile Users
* Remote Networks
* Service Connections
* IPsec
* BGP
* Traffic Flow
* Routing Control
* High Availability
* Security Policy
