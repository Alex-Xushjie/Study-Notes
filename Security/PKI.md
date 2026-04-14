# PKI

## Overview
PKI(Public Key Infrastructure) is a comprehenscive security framework of technology, policies, and procedures used to manage **digital certificates** and **public-key** encryption. It authenticates identities—users, devices, or servers—over untrusted networks like the internet, securing data through encryption and ensuring integrity via digital signatures.

## Concepts
### Key Components
1) CA(证书颁发机构): 负责颁发和管理数字证书。CA是PKI体系中最受信任的部分。  
2) RA（注册机构）:是CA的一个子集，负责接受请求并验证个体的身份，然后由CA颁发证书。  
3) Digital Certificates: 是一个由CA签名的小型数据文件，其中包含用户或服务器的公钥以及其他身份信息。  
4) public/private keys: 一对非对称的加密密钥。公钥是公开的，用于加密数据或验证签名；私钥是私有的，用于解密或签名数据。

### 散列函数
1. 定义  
散列函数也叫做HASH函数，主流的散列算法有MD5，SHA-1，SHA-2。散列函数的主要任务是验证数据的**完整性**。通过散列函数计算得到的结果叫做散列值，这个散列值也常常被称为数据的指纹。
*tips：有些debug信息中显示的指纹就是HASH值。

2. 特点：
- 固定大小(Fixed Size)：无论原始数据多大，最后得出的结果都是固定大小。
- 雪崩效应(Avalanche Effect)：原始数据有一点微小的改变，最终的结果都会完全不一样。
- 单向性(One-Way)：从原始数据计算HASH值非常简单，反向却无法由HASH值推导出原始数据（逆推出任何一位都不行）。
- 冲突避免(Collision Resistance)：两组不同的原始数据不能计算出同一个HASH值。
*因为MD5和SHA-1目前已经被证明无法满足冲突避免，所以这两个算法被认为是不安全的散列算法。
  
3. python实战
```python
#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# pip install pycryptodome

from Crypto.Hash import SHA256

# 需要HASH的消息（需要二进制数据）
plain_text = b'Hello, World!'
# 生成消息的哈希值
plain_test_hash = SHA256.new(plain_text)

print("明文消息的哈希值:", plain_test_hash.digest())
print("明文消息的哈希值（16进制）:", plain_text_hash.hexdigest())

with open("./msg/plain.hash", "wb") as f:
    f.write(plain_text_hash.digest())
```

### 对称与非对称密钥算法
**对称密钥算法**
1. 定义  
使用相同密钥与算法进行加解密运算的算法就叫做对称密钥算法。
2. 优点：
- 速度快
- 安全
- 紧凑
3. 缺点：
- 缺少安全交换密钥的方式。
- 随着参与者数量的增加，密钥数量急剧膨胀。
- 因为密钥数量过多，对密钥的管理和存储是一个很大的问题。
- 不支持数字签名和不可否认性。


**非对称密钥算法**
1. 定义  
使用一对密钥（公钥和私钥）来执行加密和解密操作。这两个密钥是相关联的，但是从一个密钥计算出另一个密钥是非常困难的。
- 公钥：可以公开给任何人，用于加密信息。
- 私钥：必须保密，用于解密信息。

2. 主要用法  
- 数字签名和身份验证：使用私钥创建数字签名，可以验证信息的来源和完整性。接收者可以用公钥验证签名，以确保信息是由预期的发送者创建并且未被篡改。
- 密钥交换：通常使用非对称密钥算法安全地交换对称密钥，例如通过Diffie-Hellman密钥交换协议。

3. 常见的非对称密钥算法：
- RSA
- DSA
- ECC

4. 缺点：
- 运行速度慢
- 密文会变长

5. 优点：
- 安全
- 密钥的数量与参与者数量相同
- 在交换公钥前不需要预先建立某种信任关系，不必担心公钥被劫持
- 支持数字签名和不可否认性

### 数字签名
1. 定义  
数字签名是发送方使用私钥**加密**明文数据的**散列值**，用于接收方验证发送方的身份。

2. 工作流程：  
- 发送方先对明文数据进行hash计算，得到散列值1；
- 发送方使用私钥对散列值进行加密，得到数字签名；
- 发送方将要发送的数据和数字签名一起发送给接收方；
- 接受方解密后得到明文数据，并对该数据进行hash计算，得到散列值2
- 接收方使用公钥对数字签名进行解密得到散列值1，比较散列值1与散列值2，如果相同，则数字签名验证通过。

### CA（证书授权颁发机构）
CA就是网络中各个实体共同认可的受信任的机构，后续的公钥统一由该机构确认、审核。  
每个实体都要获取CA的公钥（认证CA的过程）  
每个实体都要提交自己的公钥给CA（注册到CA）  
这个初始步骤，必须手动认证或通过一个可信赖的传输网络来执行[都需要手动校验]  

数字证书仅仅只是解决"这个公钥的持有者到底是谁"的问题  
数字证书是明文的  
证书里面包含公钥  
证书类似身份证  

**证书的标准：**  
X.500：定义了一个全球统一的目录服务 / 名称空间 / 信息模型，是一种目录服务体系标准。 
主题信息包含：
- CN
- OU
- O
- L
- ST
- DC
- MAIL  

X.509V3：定义了身份公钥证书的结构与校验规则，X.509 是 X.500 体系中的一个组成部分。  
X.509V3定义了证书基本结构：
- Subject（主体）
- Issuer（颁发者）
- Public Key
- Validity（有效期）
- Signature（签名）

### IKE数字签名认证
- 校验证书有效性
- 确认主体信息匹配
- 校验数字签名
- 确认散列值是否匹配


