## Layer 2 Technologies

Chapter 1 explains how Layer 2 technologies are used in network design, especially in campus and data-center environments. The chapter discusses several important topics, including Spanning Tree, VLAN design, first-hop redundancy protocols, and Layer 2 versus Layer 3 access designs.

Ethernet is the main Layer 2 technology used in LANs, WANs, and data centers. However, traditional Ethernet has a major limitation: it does not prevent loops by itself. Because Ethernet frames do not have a TTL field, loops can cause broadcast storms and network instability. To prevent this, Spanning Tree Protocol (STP) blocks certain links to create a loop-free topology.

A drawback of STP is that some links must be blocked, which prevents all links from being used simultaneously and limits multipath forwarding. To improve load distribution, network designers may use techniques such as VLAN-based load balancing or flow-based load balancing with protocols like GLBP.

The chapter also explains campus hierarchical design, where the network is divided into access, distribution, and core layers. In this model, the distribution layer aggregates traffic and often hosts key functions such as routing and gateway redundancy. Because most campus traffic flows north-south, the STP root bridge and first-hop redundancy gateways are usually placed at the distribution layer.  ￼

Finally, the chapter compares Layer 2 access design and Layer 3 routed access design. Layer 2 access relies on STP and FHRP but may have slower convergence. Layer 3 access removes STP between access and distribution layers and uses routing protocols and ECMP for faster convergence and better scalability.  ￼

The main design goal of this chapter is to help network engineers choose the correct Layer 2 architecture while considering scalability, convergence, and traffic patterns.


## Key Vocabulary

| Vocabulary | Meaning | Example sentence |
|:---|:---|:---|
| Topology | the structure or layout of a network | STP creates a loop-free topology by blocking redundant links. |
| Loop | a situation where frames circulate continuously in the network. | Layer 2 loops can cause broadcast storms and network instability. |
| Aggregation | combining traffic from multiple devices or networks. | The distribution layer aggregates traffic from the access switches. |
| Convergence | the time required for the network to reach a stable state after a change. | Layer 3 access design provides faster convergence than traditional spanning tree networks. |
| Redundancy | having backup paths or devices for reliability. | Redundant links increase availability but may require spanning tree to prevent loops. |
| Scalability | the ability of a network to grow without major redesign. | Routed access designs improve scalability in large networks. |
| Simultaneously | At the same time | Multiple links cannot be used simultaneously in a traditional spanning tree topology. |
| Hierarchical | Organized in multiple levels or layers. | Campus networks are usually designed using a hierarchical architecture. |

## 4 关键命令
---
## 4 关键命令

<div style="max-height:120px; overflow:auto; border:1px solid #ddd; padding:10px">

```bash
ibstat
ibv_devinfo
ibping
ibhosts
ibswitches
iblinkinfo
ibroute
##cest

```
</div>



## 测试

啊 

| 参数 | 含义 | 常用值 |
|------|------|--------|
| `-b` | 起始 buffer 大小 | `8`（8字节）或 `4K` |
| `-e` | 结束 buffer 大小 | `1M`（RoCE 受限环境） / `32M` |
| `-f` | 倍增因子 | `2`（8→16→32→...） |
| `-g` | 每进程 GPU 数 | `1` |