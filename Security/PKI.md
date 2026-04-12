# PKI

## Overview
PKI(Public Key Infrastructure) is a comprehenscive security framework of technology, policies, and procedures used to manage digital certificates and public-key encryption. It authenticates identities—users, devices, or servers—over untrusted networks like the internet, securing data through encryption and ensuring integrity via digital signatures.

## Concepts
### Key Components
1) CA(证书颁发机构): 负责颁发和管理数字证书。CA是PKI体系中最受信任的部分。  
2) RA（注册机构）:是CA的一个子集，负责接受请求并验证个体的身份，然后由CA颁发证书。  
3) Digital Certificates: 是一个由CA签名的小型数据文件，其中包含用户或服务器的公钥以及其他身份信息。  
4) public/private keys: 一对非对称的加密密钥。公钥是公开的，用于加密数据或验证签名；私钥是私有的，用于解密或签名数据。

### 散列函数
1. 定义：
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


非对称密钥算法
1. 定义

