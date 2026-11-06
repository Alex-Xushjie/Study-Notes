# 进程、服务、软件包与配置文件

[Linux学习目录](../Linux-Networking.md)

## 1. 为什么网工还要看进程和服务

地址、路由都正确时，SSH或HTTP仍可能无法连接，因为提供服务的程序根本没启动。Linux网络排错不只查看网卡，还要确认应用由谁运行、监听哪里、日志记录了什么。

程序是已安装的代码，进程是它运行后的实例。PID是process ID进程编号；一个服务可能包含多个进程，也可能只在某个动作期间运行。systemd是很多发行版的服务管理组件，systemctl是与它交互的工具，不是每个Linux都必然使用的唯一体系。

## 2. 先读进程列表

~~~bash
ps -ef
~~~

ps用于显示进程，-e列出相应可见的全部进程，-f使用完整格式。典型列包括UID、PID、PPID、时间和CMD；PPID是父进程编号，CMD是启动命令。

进程列表只能帮助确认某个程序实例是否存在，不能单独证明它提供的服务正常。判断网络服务是否可用，需要分层检查：

1. **进程**：提供该服务的程序是否已启动、是否仍在运行？
2. **监听**：程序是否监听了预期的地址和端口？下一步可用ss核对。
3. **实际请求**：客户端能否连接，并完成预期操作？

例如，sshd是提供SSH服务的程序。看到sshd进程，只能说明该程序实例存在；还需检查监听地址和端口，并通过实际SSH连接与认证，确认指定用户能否登录。进程、监听和请求结果是不同层次的证据。

有权限限制或容器隔离时，可见进程范围不同。不要把自己没看到进程等同于全系统没有该程序。网络监听仍要用后续介绍的ss核对。

## 3. systemctl：状态、启动与开机启动是三件事

以Ubuntu常见的SSH服务名ssh.service为例：

~~~bash
systemctl status ssh.service --no-pager
systemctl is-active ssh.service
systemctl is-enabled ssh.service
~~~

status查看综合状态，--no-pager直接输出而不进入分页界面。is-active查看当前活动状态，is-enabled查看启动配置。其他系统可能叫sshd.service，应先确认实际名字；Unit not found可能只是名字不对或未安装。

| 结果 | 先怎样解释 |
|---|---|
| active (running) | 管理器认为该服务当前运行；还需业务验证 |
| active (exited) | 某些一次性任务已完成并保持活动标记，不必有常驻进程 |
| inactive | 当前未活动，不必然是故障，需结合用途 |
| failed | 启动或运行结果被标为失败，需要看原因 |

start启动当前服务；enable配置相应开机启动关系，通常不等同立即启动；restart会中断并重新运行。先识别状态，本篇不要求重启SSH或网络管理服务，特别不能依赖正在修改的唯一远程会话。[systemctl文档](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)

## 4. journalctl：按服务和时间找日志

~~~bash
journalctl -u ssh.service --since "10 minutes ago" --no-pager
journalctl -k -b --no-pager
~~~

journalctl读取系统journal日志；-u限定服务单元；--since限定开始时间；-k读取内核消息；-b限定本次启动。内核日志可能包含网卡驱动、链路变化等信息，服务日志可能包含端口占用、配置错误或认证失败。普通用户可见范围受授权影响。

示例消息“Address already in use”表示绑定地址/端口冲突线索，不表示交换机路由故障。应继续用ss定位监听者。日志必须与故障时间窗对应，旧的启动失败不能解释所有后续流量。[journalctl文档](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)

## 5. 软件包、工具与服务并非一一对应

软件包是发行版安装/更新的软件单元。ip工具通常在iproute2包里，ss也来自同一工具集；安装工具不代表启动新服务。不同发行版包名、仓库和工具路径可能不同。

~~~bash
command -v ip
ip -V
cat /etc/os-release
~~~

command -v查询当前Shell能找到的工具位置，-V查询ip版本，os-release确认发行版。Ubuntu常见apt，其他系统可能用dnf；仅在实际缺工具时按发行版文档安装，不为复制笔记把一批包盲目装进生产机。

## 6. 配置与当前状态怎样对应

/etc下常见配置文件；/run下常见运行时对象；日志可能在journal或/var/log。不要以“找到一个文件”就认定它控制当前服务。确认管理者、加载位置、是否被生成工具覆盖、变更怎样应用，再判断持久性。

例：网络由NetworkManager管理，而你编辑了一个未被读取的networkd文件，当前状态不会因此正确改变。下一篇[持久化配置](../02-Interfaces-Routing-and-VRF/03-Persistent-Network-Configuration.md)会把网络管理关系单独解释。

## 7. 练习与参考答案

选一个已存在服务，只做status、日志和监听三类观察，记录服务名、PID、端口和时间。不要求你先安装HTTP服务器。

自测：enabled是否等于正在运行？答案：不等于。running是否等于对用户健康？答案：不等于，还需监听、认证、依赖与请求验证。command not found是否证明网络断？答案：通常先是工具查找/安装问题。
