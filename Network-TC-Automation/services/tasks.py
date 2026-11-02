from uuid import uuid4
from core.models import Task
from adapters.profiles import PROFILES

def validate_command(command):
    if not isinstance(command, str) or not command.strip() or any(c in command for c in ('\n','\r','\x00')):
        raise ValueError('命令必须为非空的单行文本')
    return command.strip()

def library(device, library_id, test_id=None):
    return Task(test_id or uuid4().hex, device.id, PROFILES[device.platform][library_id], 'library')

def quick(device, command):
    return Task(uuid4().hex, device.id, validate_command(command), 'quick')

def deduplicate(tasks):
    seen=set(); result=[]
    for t in tasks:
        key=(t.id,t.device_id,t.section,t.command,tuple(t.steps))
        if key not in seen: result.append(t); seen.add(key)
    return result
