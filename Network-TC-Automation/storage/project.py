import json
from pathlib import Path
from dataclasses import asdict
from core.models import Device, Task
from services.tasks import validate_command
from adapters.profiles import PROFILES

def validate(devices, tasks):
    from ipaddress import ip_address
    ids=set()
    for d in devices:
        if not d.id.strip() or not d.host.strip(): raise ValueError('Hostname和地址不能为空')
        try: ip_address(d.host)
        except ValueError: raise ValueError('管理地址必须填写有效 IP: '+d.host) from None
        if d.id in ids: raise ValueError('Hostname重复: '+d.id)
        if d.platform not in PROFILES: raise ValueError('不支持的平台: '+d.platform)
        if not 1 <= int(d.port) <= 65535: raise ValueError('SSH 端口超出范围')
        ids.add(d.id)
    for t in tasks:
        if not t.id.strip(): raise ValueError('测试编号不能为空')
        if t.device_id not in ids: raise ValueError('任务引用未知设备: '+t.device_id)
        validate_command(t.command)
        if not isinstance(t.steps,list) or not all(isinstance(c,str) for c in t.steps): raise ValueError("步骤必须为命令列表")
        for command in t.steps: validate_command(command)
        if t.source not in ('excel','library','quick'): raise ValueError('未知任务来源')

def device_record(device):
    from storage.credentials import protect
    record=asdict(device); password=record.pop('password','')
    if password:record['protected_credential']=protect(password)
    return record

def restore_device(record):
    from storage.credentials import unprotect
    record=dict(record); encrypted=record.pop('protected_credential','')
    if encrypted:
        try:record['password']=unprotect(encrypted)
        except ValueError:record['password']=''
    return Device(**record)

def save(path, name, devices, tasks):
    validate(devices,tasks)
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    data={'schema_version':2,'name':name,'devices':[device_record(d) for d in devices], 'tasks':[asdict(t) for t in tasks]}
    temp=path.with_suffix('.json.tmp'); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); temp.replace(path)

def load(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('schema_version') not in (1,2): raise ValueError('项目格式版本不支持')
    devices=[restore_device(d) for d in data['devices']]; tasks=[Task(**t) for t in data['tasks']]
    validate(devices,tasks)
    return data['name'],devices,tasks
