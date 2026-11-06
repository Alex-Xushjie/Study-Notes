# 从网络任务认识Python与运行环境

[返回网络自动化目录](../Network-Automation.md)

## 1. Python在这里做什么

Python是一种编程语言，解释器负责执行程序。它可以读文件、整理设备状态、调用API或生成配置；语言本身不等于SSH、HTTP或任何网络服务。程序想访问设备，需要显式使用相应通信功能，不能从python进程存在推断服务可用。

自动化首先是可重复、可验证的工作流程，未必一开始就批量下配置。推荐顺序是离线数据处理→单设备只读→多设备采集→生成差异→实验变更→受控发布。先把输入、判断和输出讲清楚，再选择框架。

## 2. 解释器、脚本、模块与库

| 名称 | 含义 | 例子 |
|---|---|---|
| 解释器 | 执行Python代码的程序 | python.exe、python3 |
| 脚本 | 保存源代码的文件 | audit.py |
| 模块 | 可导入的一组代码 | json、ipaddress |
| 标准库 | 随Python提供的模块集合 | pathlib、csv、unittest |
| 第三方包 | 另安装并按版本使用的代码 | Netmiko、Jinja2 |
| pip | 安装/查询Python包的工具 | python -m pip |

Shell命令和Python代码是不同语言。以>>>开头的交互提示符不应原样写入.py文件，代码块标python的内容也不能直接当PowerShell命令执行。

## 3. 第一个离线程序

把下面内容保存为hello_network.py，无需设备或第三方包：

~~~python
device = "lab-r1"
interface = {"name": "Ethernet1", "admin_up": True, "oper_up": False}
print("Device:", device)
if interface["admin_up"] and not interface["oper_up"]:
    print(interface["name"], "needs investigation")
else:
    print(interface["name"], "no admin/oper mismatch")
~~~

变量保存值；字典用键找值；if根据条件选择分支，缩进表示代码块。True/False是布尔值，不是字符串。程序只处理内存中的教学状态，输出不代表真的访问过lab-r1。

## 4. 运行与隔离环境

先确认安装的Python版本。Windows PowerShell可运行：

~~~powershell
py --version
py -m venv .venv
& ./.venv/Scripts/python.exe hello_network.py
& ./.venv/Scripts/python.exe -m pip --version
~~~

py启动器若未安装，用已确认路径的python替代。Linux常用python3 -m venv .venv，再用.venv/bin/python运行。虚拟环境隔离项目依赖，不是虚拟机，也不隔离程序对文件/网络的权限。无需为激活环境去全局放宽执行策略，直接调用环境内解释器即可。

## 5. 练习

修改接口状态，预测输出再执行；故意把True写成字符串，观察为什么字符串并非可靠布尔状态。记录解释器路径、版本、运行目录和结果。不要为了练习在系统Python里安装整套网络包。

[Python教程](https://docs.python.org/3/tutorial/)、[虚拟环境](https://docs.python.org/3/library/venv.html)。本部分从编程初学者需要的概念讲起，不假设已有软件开发经验。
