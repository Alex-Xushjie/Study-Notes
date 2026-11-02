from core.models import Result, utcnow
class Engine:
    def __init__(self, adapter, evidence):
        self.adapter, self.evidence = adapter, evidence
    def run(self, task, device):
        result=Result(task,'REVIEW','',started_at=utcnow())
        for command in task.steps or [task.command]:
            try:
                output=self.adapter.execute(device,command)
                result.output+=output+'\n'
                result.step_results.append({'command':command,'output':output,'error':''})
            except Exception as exc:
                result.step_results.append({'command':command,'output':'','error':str(exc)})
                result.error+=f'{command}: {exc}\n'
        result.execution_status='ERROR' if result.error else 'COMPLETED'
        result.status='ERROR' if result.error else (('PASS' if task.expected in result.output else 'FAIL') if task.expected else 'REVIEW')
        result.finished_at=utcnow(); result.device_ip=device.host
        result.prompt=getattr(self.adapter,'prompt',''); result.device_name=getattr(self.adapter,'hostname','') or device.id
        self.evidence.save(result)
        return result
