# 临时配置与持久化：谁在管理Linux网络

[Linux学习目录](../Linux-Networking.md)

## 1. 为什么重启后地址会变

ip address与ip route直接操作当前内核网络状态。当前可用不表示重启后仍存在，也不表示管理组件不会重新覆盖。理解“配置来源→管理组件→当前状态”，才能避免反复手工补地址。

| 层次 | 是什么 | 例子 |
|---|---|---|
| 配置来源 | 保存期望设置的文件/连接配置 | Netplan YAML、NetworkManager连接配置 |
| 管理组件 | 读取配置并维护接口状态的程序 | systemd-networkd、NetworkManager |
| 当前状态 | 内核正在使用的地址与路由 | ip address、ip route输出 |

Netplan是描述网络并生成后端配置的工具，不是独立替代所有后端的转发进程。Ubuntu的某些安装用它配合networkd或NetworkManager，别的系统未必使用。

## 2. 先识别当前系统，再决定编辑什么

~~~bash
cat /etc/os-release
systemctl is-active NetworkManager.service
systemctl is-active systemd-networkd.service
ip -br address show
ip -4 route show
~~~

service名称和工具可能不存在；一个管理器active也不证明它管理每块接口。NetworkManager环境可用nmcli device status查看设备管理状态；nmcli是其命令行客户端。networkd环境可用networkctl status查看接口，-a等选项按本机手册确认。

不要为统一教材而启用两个管理器争管同一接口，也不把“所有发行版都改/etc/network/interfaces”当规则。

## 3. 读一个静态地址示例

下面只用于已经确认由Netplan管理、后端为networkd的独立实验接口，不能当成覆盖现有文件的完整配置：

~~~yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens192:
      dhcp4: false
      addresses:
        - 192.0.2.10/24
      routes:
        - to: 198.51.100.0/24
          via: 192.0.2.1
~~~

YAML通过空格缩进表达层次，不用Tab混排。network是顶层，ethernets列以太接口，ens192必须是实际接口名，addresses是地址列表，routes是路由列表。此例只指定一个文档目的前缀，没有更改默认路由或DNS，也不能与原文件冲突地重复定义。

你需要先查看并备份实际生效配置，保留管理入口，再决定如何合并。云镜像还可能由cloud-init等生成配置，应确认来源，避免下次启动被重新生成。

## 4. 校验、应用与验证

Netplan环境中的generate生成后端配置并检查相关语法，但不等于证明网关/服务可达；apply应用配置；try提供限时确认与回退机制，但不应当成任何场景都保证自动恢复的事务，尤其要了解虚拟设备等边界。

这里只解释命令职责，不提供远程生产机一键替换流程。确认控制台/带外、原文件和恢复步骤后，在实验机按本机版本执行。具体行为参考[Netplan try文档](https://netplan.readthedocs.io/en/stable/netplan-try/)。

后验至少包括地址、规则与路由、网关邻居、DNS和目标服务；最后在允许重启的实验环境确认持久性。配置文件正确、当前运行正确和重启后正确是三次不同验证。

## 5. 排错案例与作业

案例：手工路由短暂有效，数分钟后消失。调查DHCP续租、管理器重新应用、云初始化或其他自动化；比较时间与日志，不要反复增加同一路由掩盖来源问题。

交付自己的“发行版→接口管理者→配置来源→当前状态”表。自测：ip route add成功是否等于永久保存？答案：不是。管理器active是否证明某接口归它管理？答案：不是，要看设备归属。
