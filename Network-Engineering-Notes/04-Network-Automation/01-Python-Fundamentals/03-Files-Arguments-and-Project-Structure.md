# 文件、参数与可维护脚本结构

[返回网络自动化目录](../Network-Automation.md)

## 1. 路径与运行目录

相对路径相对于当前工作目录，不一定相对于脚本所在目录。双击、终端、定时任务和CI的运行目录可能不同。使用pathlib处理路径，明确输入/输出，不把设备名称原样拼成任意文件路径。

推荐小项目包含src或脚本、data输入、templates模板、tests测试、artifacts结果、依赖清单和使用说明。虚拟环境、真实凭据、生产备份与临时输出按规则排除出Git。文件名按用途，不要求README.md。

## 2. 完整命令行示例

下面保存为count_inventory.py。输入必须是后文定义的JSON对象，其中devices为列表；程序只读输入，不改任何设备：

~~~python
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Count offline inventory entries")
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        text = args.inventory.read_text(encoding="utf-8")
        data = json.loads(text)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error("cannot load inventory: " + str(exc))
    if not isinstance(data, dict) or not isinstance(data.get("devices"), list):
        parser.error("expected an object containing a devices list")
    print("devices:", len(data["devices"]))

if __name__ == "__main__":
    main()
~~~

argparse负责解析参数并显示帮助，Path负责文件操作，json把文本转换为Python对象。main组织入口；__name__条件让文件被导入时不自动执行主流程。运行方式为python count_inventory.py data/inventory.json，python需替换成实际环境解释器。

## 3. 输出与退出码

终端输出适合人看，JSON/CSV适合其他程序消费。定义schema_version、run_id、时间、来源版本、状态和错误字段。全部失败不能只打印一行error后退出码仍为0，让流水线误判通过。

退出码规则由项目约定：0表示本任务成功，非0区分输入失败、采集部分失败和检查不合规等情况。不要让调用方依赖一段随时变化的中文提示判断结果。

## 4. 写文件的边界

先生成独立新结果，校验后再发布；需要替换文件时可采用同文件系统临时文件+重命名，仍需处理权限、异常与清理。配置备份可能含秘密，不能输出到公开目录。路径需要限制在明确结果根目录下，拒绝包含越界内容的设备标识。

## 5. 练习

从不同工作目录运行脚本，分别提供正常文件、缺失文件、损坏JSON与错误顶层结构。验证错误会明确失败；空devices列表是合法输入还是错误，应由业务规则决定并写进契约。

[pathlib](https://docs.python.org/3/library/pathlib.html)、[argparse](https://docs.python.org/3/library/argparse.html)。
