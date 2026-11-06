# PTP、时钟角色、PHC与系统时钟

[返回本部分学习目录](../Trading-and-Low-Latency.md)

## 1. 先分清钟在哪里

系统时钟供应用和操作系统使用，PHC是NIC等硬件提供的PTP时钟，外部Grandmaster（GM）提供时间参考。ptp4l通常参与PTP并可调相应PHC，phc2sys协调本机相关时钟；真实方向由角色/配置决定，不必永远“PHC到系统”。

普通时钟、边界时钟、透明时钟职责不同。透明时钟对相应经过时间提供校正，不能理解成所有设备都跟GM同步并替代误差设计。

## 2. 互通条件

PTP版本/Profile、Domain、L2/UDP传输、E2E/P2P延迟机制、单双步、时钟角色与硬件支持需匹配。能收到Sync不等于完整同步，Delay/Follow_Up与Announce等还可能受过滤/不匹配影响。

| 状态 | 检查 |
|---|---|
| GM身份 | 是否选预期源，有无意外更换 |
| 端口状态 | 是否进入期望角色，不只进程存活 |
| Offset/path delay | 单位、稳定性、采样与异常 |
| PHC/系统关系 | 谁调谁、是否多个服务争调 |
| 失败 | GM失联、Holdover、切换与恢复 |

## 3. 只读基线

Linux命令在实验主机执行，eth0是占位，ethtool查询NIC能力而非启动同步：

~~~bash
ethtool -T eth0
ls /dev/ptp*
timedatectl status
~~~

没有/dev/ptp或硬件能力就不能承诺硬件时间戳精度。不要直接启动多个phc2sys/chrony/NTP服务同时调同一时钟；先绘制时间源与控制关系。

## 4. 练习

按所用Profile准备隔离GM/客户端，采集配置、状态和源身份；测试GM故障、恢复及系统时钟关系。未有硬件/参考时钟时可分析状态，不宣称获得亚微秒绝对准确度。

[linuxptp手册](https://www.linuxptp.org/documentation/)、[ptp4l](https://www.linuxptp.org/documentation/ptp4l/)、[phc2sys](https://www.linuxptp.org/documentation/phc2sys/)。
