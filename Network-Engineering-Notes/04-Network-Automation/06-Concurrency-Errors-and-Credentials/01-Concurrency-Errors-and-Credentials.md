# 并发、超时、重试与部分失败

[返回网络自动化目录](../Network-Automation.md)

## 1. 为什么需要限并发

轮询网络设备通常等待I/O，可通过适量并发缩短总时间；但设备CPU、AAA、跳板、API限额、控制端文件句柄和日志都有上限。1000个线程不是自动化成熟度，先用小范围基线逐步测量。

任务按站点、平台或故障域限流。每设备连接实例通常独立使用，不假定共享连接/客户端线程安全。结果集中汇总，避免多个Worker同时写同一个CSV导致损坏。

## 2. 离线线程池示例

以下独立程序只处理内存中的模拟记录，不发网络请求：

~~~python
from concurrent.futures import ThreadPoolExecutor, as_completed

def collect_simulated(device):
    if device == "lab-r2":
        raise TimeoutError("simulated timeout")
    return {"device_id": device, "status": "collected"}

results = []
with ThreadPoolExecutor(max_workers=2) as pool:
    jobs = {pool.submit(collect_simulated, device): device
            for device in ["lab-r1", "lab-r2", "lab-r3"]}
    for future in as_completed(jobs):
        device = jobs[future]
        try:
            results.append(future.result())
        except TimeoutError as exc:
            results.append({"device_id": device, "status": "unknown", "error": str(exc)})
print(sorted(results, key=lambda row: row["device_id"]))
~~~

Future表示任务结果占位，as_completed按完成顺序产出，最终按稳定ID排序方便比较。一个失败不会伪造其他成功，也不把超时设备排除出报告。

## 3. 超时层次

设置连接、认证、单命令、分页和整体任务预算。Future.result的等待超时不一定停止正在运行的网络调用；线程取消也通常不能强制终止已运行任务。必须让底层客户端有超时和关闭机制，不能以主线程不等了就认定连接已结束。

## 4. 重试规则

读取可考虑有限重试、指数退避与Jitter；认证失败、格式错误和权限拒绝通常不靠重试解决。写入超时先读回确认是否生效，再决定重试；创建/删除应使用接口支持的幂等或条件更新机制。

重试总次数与总时限有限，429遵守服务指示。故障时全网同时重试可能形成风暴，增加随机退避与全局速率约束。

## 5. 练习

模拟慢设备、认证失败、部分分页失败与单设备异常，报告每台状态及失败阶段。将并发1/2/5的耗时和错误对比；模拟无I/O工作不能证明真实设备并发性能。

[concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)。
