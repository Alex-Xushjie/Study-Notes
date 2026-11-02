from dataclasses import dataclass, field
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class Device:
    id: str
    host: str
    platform: str = 'huawei_vrp'
    port: int = 22
    username: str = ''
    group: str = ''
    password: str = field(default='',repr=False,compare=False)

@dataclass(frozen=True)
class Task:
    id: str
    device_id: str
    command: str
    source: str
    expected: str = ''
    name: str = ''
    section: str = ''
    steps: list = field(default_factory=list)
    criteria: str = ''
    logical_group: str = ''
    retest_of: str = ''

@dataclass
class Result:
    task: Task
    status: str
    output: str
    error: str = ''
    started_at: str = field(default_factory=utcnow)
    finished_at: str = ''
    evidence_dir: str = ''
    device_ip: str = ''
    device_name: str = ''
    prompt: str = ''
    execution_status: str = ''
    step_results: list = field(default_factory=list)
