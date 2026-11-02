class Scheduler:
    """Sequential scheduling; cancellation is checked between tasks."""
    def run(self, engine, tasks, devices, cancelled=lambda: False, on_result=lambda r: None):
        results = []
        for task in tasks:
            if cancelled(): break
            result = engine.run(task, devices[task.device_id])
            results.append(result)
            on_result(result)
        return results
