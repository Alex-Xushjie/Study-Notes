# Git、可审查差异与依赖复现

[返回网络自动化目录](../Network-Automation.md)

## 1. Git保存可追溯的意图

Git记录代码、模型、模板与脱敏样例，帮助对比和协作；commit不代表已部署，合并不代表业务通过。代码版本、输入快照、计划、设备执行与后检应通过run_id关联。

工作区是当前文件，暂存区是准备提交的内容，commit是版本记录，分支用于组织变化。先看差异再提交，不能把整个输出目录和秘密一起纳入。

## 2. 只读起步命令

在实际项目目录执行：

~~~bash
git status --short
git diff
git diff --cached
git log -5 --oneline
~~~

git diff默认比较工作区与暂存区，--cached比较暂存与当前提交。未跟踪文件不一定显示在普通diff里，需结合status查看。不要用git reset --hard或clean当“清理一下”的常规第一步。

## 3. 仓库内容

跟踪源代码、模板、Schema、脱敏Fixture、测试、依赖与使用说明；忽略.venv、缓存、真实备份、凭据和运行结果中的敏感内容。已有被跟踪秘密不会因新增.gitignore自动消失，需要按事件流程处理并轮换。

说明文件可命名Usage.md、Design.md等，遵循本笔记不使用README.md的约定。现有外部项目若使用该名字，不代表需要在本教材新建同名文件。

## 4. 依赖复现

记录Python、直接/间接包、Ansible Core/Collection和设备版本。requirements、锁文件与Collection清单服务不同层次；pip freeze是当前环境快照，可能混入无关包，不等于经过审查的依赖设计。

在线latest文档可能比本地版本新。只使用已验证接口，升级后运行离线回归与实验设备测试，避免为“最新”无条件升级生产控制端。

## 5. 练习

在独立练习仓库提交一项输入验证变化，展示源码、Fixture、测试和Diff。审查者无需看聊天也应知道问题、行为变化、验证与限制。不要在本笔记现有仓库随意执行全量add/commit来完成练习。

[Git基本概念](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)、[git diff](https://git-scm.com/docs/git-diff)、[Python依赖安装](https://packaging.python.org/en/latest/tutorials/installing-packages/)。
