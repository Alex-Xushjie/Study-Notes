# Network T&C Automation

Windows PySide6 桌面工具与独立 Python SSH 执行引擎。Excel、内置库、Quick Command 统一任务模型。只执行真实 SSH；测试中的替身仅用于自动化测试。

双击 start.bat 或运行 `.\.venv312\Scripts\python.exe -m gui.main`。

详细操作见 [中文使用说明](docs/使用说明.md)。证据使用设备名称-IP-命令命名，保留真实 SSH 提示符、命令回显，输出 TXT、分页 PNG 和 JSON。旧证据不重命名；旧模拟结果在界面和导出中隐藏。

新环境：Python 3.12，创建 .venv312，安装 requirements.txt。旧 Cisco IOL 镜像需要 requirements-legacy.txt；本机已配置。精确依赖见 requirements-lock.txt。

CLI：`.\.venv312\Scripts\python.exe cli.py --project projects/eve-lab/project.json --username lab`，确认后交互输入密码。

测试：`.\.venv312\Scripts\python.exe -m unittest discover -s tests -v`。

core、adapters、services、storage 不依赖 Qt，可供后续 Web 服务调用。目前为顺序执行；不含定时任务、并发、Word 报告、自动 enable 提权或 EXE 打包。

第一轮已加入多命令测试项、章节与验收标准、批量模板、勾选执行、复测来源、N/A 和带意见通过、实际结果与 CSV 证据索引。旧项目可读，保存为版本 2。详见使用说明末尾。

SSH 凭据现由设备页逐台维护，支持 Excel Devices 表的 Username/Password 列；项目密码使用当前 Windows 用户 DPAPI 加密保存，跨电脑使用需重新填写。设置页不再提供统一账号密码。

冗余工作流：执行页提供九类可编辑起始模板，支持多设备采集、人工故障/恢复确认、显式 CLI 配置、等待、最终复核、模板保存和执行日志续接。详见使用说明。当前不含持续打流和远程测试端。
