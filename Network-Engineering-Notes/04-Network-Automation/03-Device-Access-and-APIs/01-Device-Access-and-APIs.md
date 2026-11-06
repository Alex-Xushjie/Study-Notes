# SSH与Netmiko：从单设备只读开始

[返回网络自动化目录](../Network-Automation.md)

## 1. 连接库解决什么

SSH提供加密远程连接，CLI命令由目标设备解释；Netmiko在SSH客户端基础上处理多种网络设备的交互、提示符等问题。它不会自动理解全部业务意图，也不保证任意show命令无性能影响。

接入前确认实验地址、设备类型、只读账号、主机密钥、权限、管理路径和命令白名单。先人工验证一次正确目标身份，再建立可信known_hosts；主机密钥变化需要核查，不设置无条件接受来掩盖错误。

## 2. 只读教学脚本

下面保存为collect_version.py。需在虚拟环境按项目选定版本安装Netmiko，准备已验证的known_hosts与合法隔离IOS实验设备。环境变量只提供目标/用户名，不含固定密码：

~~~python
import os
from getpass import getpass
from netmiko import ConnectHandler

def main():
    host = os.environ["LAB_DEVICE_HOST"]
    user = os.environ["LAB_DEVICE_USER"]
    with ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=user,
        password=getpass("Device password: "),
        ssh_strict=True,
        system_host_keys=True,
        conn_timeout=10,
        auth_timeout=10,
        banner_timeout=15,
    ) as connection:
        output = connection.send_command("show version", read_timeout=20)
        print(output)

if __name__ == "__main__":
    main()
~~~

getpass在交互终端隐藏输入，不适合无人值守CI。上下文管理器在结束时关闭连接；连接、认证、Banner与命令读取超时是不同阶段。目标类型与命令仅针对这个示例，不能当Linux或其他NOS通用语法。

## 3. 失败分类

连接失败查路由/端口/设备负载，认证失败查账号权限与AAA，主机密钥失败查身份，命令失败查驱动/模式/权限，解析失败查原文与版本。发生错误时需要明确失败，不能输出空文本作为成功报告。

show version可能包含序列号/资产信息，输出不宜直接提交公开仓库。更高负载命令如大表导出、诊断包或debug需另外评估，不因归为“只读”就全网并发执行。

## 4. 练习

分别用正确目标、错误凭据、未信任主机密钥和不支持命令测试。保存阶段与错误分类，不记录密码。只有在单设备正常/异常都能解释后，才增加清单和并发。

[Netmiko官方入口](https://ktbyers.github.io/netmiko/)、[Netmiko API](https://ktbyers.github.io/netmiko/docs/netmiko/)。本次未连接设备，示例需按安装版本验证。
