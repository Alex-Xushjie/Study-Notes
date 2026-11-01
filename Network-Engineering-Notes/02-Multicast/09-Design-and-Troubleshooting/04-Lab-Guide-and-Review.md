# 组播分阶段实验与综合验收

[返回组播学习目录](../Multicast.md)

## 1. 实验环境与边界

先用两台隔离Linux测试机完成同VLAN ASM，再加入支持PIM-SM的路由设备/FRR实例完成跨子网。不要连接生产行情源或生产组地址。本篇程序只发送少量自建测试消息，不测极限性能；全部输出需要你实际执行后采集。

固定操作系统、内核、Python、FRR/NOS版本。FRR需要启用相关守护进程、内核组播路由支持与正确接口配置，容器还需要相应权限和网络能力。最新在线文档不等于已安装版本，先在vtysh中用帮助核对语法。

## 2. 实验一：同VLAN成员与应用收包

S=10.10.10.10/24，R=10.10.10.20/24，G=239.10.10.10，UDP端口5000。地址需已配置到正确测试网卡。交换机开启所需Snooping并确认查询器。先在R保存receiver.py：

~~~python
import json
import socket
import time

GROUP = "239.10.10.10"
PORT = 5000
LOCAL_IP = "10.10.10.20"  # 改为接收网卡的实际IPv4地址
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", PORT))
membership = socket.inet_aton(GROUP) + socket.inet_aton(LOCAL_IP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
s.settimeout(0.5)
seen = set()
duplicates = 0
bad = 0
end = time.monotonic() + 15
try:
    while time.monotonic() < end:
        try:
            data, peer = s.recvfrom(65535)
        except socket.timeout:
            continue
        try:
            msg = json.loads(data)
            if msg.get("channel") != "lab-1" or msg.get("session") != "run-1":
                continue
            seq = msg["sequence"]
            if not isinstance(seq, int) or not 0 <= seq < 1000:
                raise ValueError("sequence")
            duplicates += int(seq in seen)
            seen.add(seq)
        except (ValueError, KeyError, TypeError, AttributeError, UnicodeError):
            bad += 1
finally:
    s.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, membership)
    s.close()
print({"unique": len(seen), "duplicates": duplicates,
       "missing_of_1000": 1000 - len(seen), "bad": bad})
~~~

在S保存sender.py。它指定发送接口、源IP和TTL，以约100包/秒发送1000个序号：

~~~python
import json
import socket
import time

GROUP = "239.10.10.10"
PORT = 5000
LOCAL_IP = "10.10.10.10"  # 改为发送网卡的实际IPv4地址
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((LOCAL_IP, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                 socket.inet_aton(LOCAL_IP))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
    for seq in range(1000):
        payload = {"channel": "lab-1", "session": "run-1", "sequence": seq}
        s.sendto(json.dumps(payload).encode(), (GROUP, PORT))
        time.sleep(0.01)
~~~

分别用python3 receiver.py和python3 sender.py运行，接收者先启动，随后立即启动发送者。Python调度不保证精确100pps；接收端15秒窗口是教学限制，不是性能计时。1000减唯一数把未启动/窗口外序号也算缺失，必须确保窗口覆盖全部发送，并结合源日志与抓包解释。每轮改session或隔离前一轮，避免旧包混入。

程序是ASM，不提供SSM源限制、认证、乱序深度、逐包时延或补包。UDP源端口未固定；接收端只bind端口，不证明所有操作系统下的多Socket隔离行为。不要用这段小程序充当正式行情处理器。

## 3. 实验二：Snooping与离组

增加R2和无成员端口X。分别验证单接收者、双接收者、一个离开、全部离开及重新加入。观察Query、Report、成员口、mrouter口、无成员口流量。将R1/R2置于同一个下联端口后，比较Fast Leave启用前后；保存原值并恢复。

用定时器推导预期老化，再实际停止测试Querier观察。不能为了“验证成功”预先设置静态成员，让它绕过待测机制。

## 4. 实验三：跨路由ASM

拓扑：S—R1—R2(RP)—R3—R。源LAN保持10.10.10.0/24，接收LAN改成10.20.20.0/24，R改为10.20.20.20并修改程序LOCAL_IP；R1/R3网关分别为各LAN的.1。R1—R2使用10.0.12.0/30，R2—R3使用10.0.23.0/30，RP使用R2 Loopback 10.255.0.2/32。

先自行配置接口与单播路由，确保每台路由器能到源网段、接收网段和RP /32；主机配正确网关。再按对应版本启用组播/PIM、主机侧IGMP及一致的G到RP映射。此处不提供跨版本混合的一键配置。

FRR在vtysh中的只读观察示例：

~~~text
show ip pim interface
show ip pim neighbor
show ip igmp groups
show ip pim rp-info
show ip pim rpf
show ip pim upstream
show ip mroute
show ip mroute count
~~~

对照[FRR PIM官方配置与命令](https://docs.frrouting.org/en/latest/pim.html)。将每条命令绑定到问题：邻接、成员、RP映射、RPF、上游树、内核转发和计数。FRR内核表不是商用交换机ASIC表。

两种启动顺序都测。通过增加独立路径或额外路由器再测RPF错误与恢复；简单三节点链式拓扑不能证明双上联冗余。RP故障测试要包含新源/新接收者，方法见06专题。

## 5. 实验四：原生SSM

改用G=232.10.10.10，使用明确支持指定源订阅的客户端/API，而不是只改上述ASM程序的G。配置IGMPv3与一致SSM范围，明确S地址；接收者只订阅S1，第二源S2发送相同G/P作为反例。抓包及状态必须证明源集合与朝S的Join正确。

记录不依赖RP的证据，同时验证错误源地址、源迁移和版本兼容。若客户端或镜像能力不足，标记未完成，不以ASM实验替代。

## 6. 综合验收

| 能力 | 必交证据 |
|---|---|
| 逐跳解释 | S/G/P、TTL、复制位置、IIF/OIF的拓扑图 |
| 成员管理 | Query/Report及加入/离开前后的表项 |
| 建树与RPF | RP/Register或SSM源Join、实际入接口 |
| 故障定位 | 至少一个接入、一个路由、一个主机故障 |
| 行情完整性 | 采集窗口、session/序号、gap/重复及局限 |
| 冗余 | 旧流、新源、新接收者和共享故障域说明 |

结课白板题：为什么PIM邻居正常仍断流？为什么RP宕机老流正常新流失败？为什么tcpdump有包而应用缺序？为什么A/B双收仍可能同故障？回答必须带观察点和反证，不只背术语。
