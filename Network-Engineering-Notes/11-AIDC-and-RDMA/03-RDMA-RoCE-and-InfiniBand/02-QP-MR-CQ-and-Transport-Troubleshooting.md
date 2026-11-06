# QP、MR、CQ与RDMA排障

[返回本部分学习目录](../AIDC-and-RDMA.md)

## 1. 常见对象

QP是收发操作相关队列对，MR是注册内存区域，CQ接收操作完成信息；PD等对象参与资源保护。名称相似不表示普通Socket API可直接使用，应用/库需要相应资源管理。

内存键、连接与访问权限控制操作范围，不代表Fabric天然提供身份认证、加密或租户安全。NIC/DPU能力、主机权限、网络分段与作业隔离按方案设计。

## 2. 先检查事实

在Linux实验端点执行只读命令：

~~~bash
rdma link show
ibv_devinfo
ib_write_bw --help
~~~

ibv_devinfo通常来自rdma-core相关工具，ib_write_bw来自perftest。工具/版本与GID、端口、设备名均需核对，--help不执行性能测试。没有相应设备可能报错，不能据此推断Fabric配置错误。

## 3. 症状分层

| 症状 | 先区分 |
|---|---|
| 无设备/端口 | 驱动、权限、设备模式与健康 |
| 可建连但无数据 | 设备/端口/GID、路由/MTU、资源与两端参数 |
| 内存注册失败 | 大小/权限/页、驱动和GPU支持 |
| 完成错误/重试 | 传输、链路、拥塞、超时与接收资源 |
| 单对好、多对差 | 共享瓶颈、队列映射、反馈与端点 |

## 4. 练习

两端固定兼容版本和参数，先Host Memory小规模读写，再增加消息大小、QP与并发，保存正确性/错误和计数差值。生产共享集群不擅自分配大量QP/内存或压测。

[perftest参数与测试说明](https://github.com/linux-rdma/perftest)、[rdma-core](https://github.com/linux-rdma/rdma-core)。一个工具成功不证明完整作业或GPU路径。
