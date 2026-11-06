# 离线测试、Fixture与设备集成验证

[返回网络自动化目录](../Network-Automation.md)

## 1. 测试分别证明什么

单元测试验证一个规则/解析器；契约测试核对输入输出结构；集成测试验证库、传输和设备协作；端到端测试验证业务。Mock只证明模拟条件下的代码路径，不证明NOS真的支持命令或回滚。

先覆盖高影响判断：错误目标、缺数据、空表、未知版本、权限失败、分页不完整和变更范围。不要只断言函数会返回自己刚拼出的字符串。

## 2. BGP规则的可运行测试

把前文函数保存为bgp_check.py，下列内容保存为同目录test_bgp_check.py，使用Python标准库unittest，无第三方依赖：

~~~python
import unittest
from bgp_check import evaluate_bgp

class TestBGPCheck(unittest.TestCase):
    def snapshot(self, rows, complete=True):
        return {"collection_status": "ok", "complete": complete, "neighbors": rows}

    def test_established_expected_peer(self):
        data = self.snapshot([{"peer": "192.0.2.1", "state": "Established"}])
        self.assertEqual(evaluate_bgp(["192.0.2.1"], data), "PASS")

    def test_idle_is_failure(self):
        data = self.snapshot([{"peer": "192.0.2.1", "state": "Idle"}])
        self.assertEqual(evaluate_bgp(["192.0.2.1"], data), "FAIL")

    def test_missing_expected_peer_in_complete_data(self):
        self.assertEqual(evaluate_bgp(["192.0.2.1"], self.snapshot([])), "FAIL")

    def test_incomplete_empty_is_unknown(self):
        self.assertEqual(evaluate_bgp(["192.0.2.1"], self.snapshot([], False)), "UNKNOWN")

    def test_duplicate_peer_is_unknown(self):
        row = {"peer": "192.0.2.1", "state": "Established"}
        self.assertEqual(evaluate_bgp(["192.0.2.1"], self.snapshot([row, row])), "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
~~~

运行python -m unittest -v test_bgp_check。测试证明缺失与不完整不混淆，不证明BGP前缀、转发或应用全部健康。

## 3. Fixture选择

保存脱敏正常/异常输出及平台版本，包含真实格式变化、分页与命令报错。Fixture要小而有代表性，不抓整个生产配置当测试数据。改变解析器时同时确认旧样本和新样本行为。

## 4. 实验设备验证

选定合法实验镜像和版本，验证主机信任、超时、驱动、结构化字段、只读完整性，再测试低影响变更和回退。失败后保留设备侧证据，区分库异常和设备拒绝。

## 5. 练习

增加认证失败、错误字段类型、未知状态枚举和计数器重置测试。设备集成用例单独标记并按显式清单执行，不让默认单元测试暗中连接生产设备。

[unittest](https://docs.python.org/3/library/unittest.html)、[pytest Fixture](https://docs.pytest.org/en/stable/how-to/fixtures.html)。框架选择次要，反例与断言应有业务意义。
