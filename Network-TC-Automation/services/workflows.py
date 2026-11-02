"""UI-independent workflow validation, templates and durable execution journal."""
import json,copy
from pathlib import Path
from datetime import datetime
from core.models import utcnow
KINDS=('collect','manual','fault_manual','fault_cli','wait','restore_manual','restore_cli','review')

def validate(plan,devices):
    if not plan.get('name','').strip() or not plan.get('steps'):raise ValueError('Workflow name and steps are required')
    fault=False
    for i,s in enumerate(plan['steps']):
        kind=s.get('kind')
        if kind not in KINDS:raise ValueError('Unknown step type')
        if not s.get('title','').strip():raise ValueError('Step title is required')
        if kind in ('collect','fault_cli','restore_cli'):
            if not s.get('targets'):raise ValueError('Select target devices for each command step')
            if any(d not in devices for d in s['targets']):raise ValueError('Unknown target device')
            if not s.get('commands'):raise ValueError('At least one command is required')
            for c in s['commands']:
                if not c.strip() or any(x in c for x in ('\n','\r','\x00','{','}')):raise ValueError('Commands must be complete single lines without placeholders')
        if kind in ('manual','fault_manual','restore_manual') and not s.get('instruction','').strip():raise ValueError('Enter operation instructions')
        if kind=='wait' and not 1<=int(s.get('seconds',1))<=3600:raise ValueError('Wait must be 1 to 3600 seconds')
        if kind.startswith('fault_'):
            if fault:raise ValueError('Restore the previous fault before injecting another')
            fault=True
            if not any(x.get('kind') in ('restore_manual','restore_cli') for x in plan['steps'][i+1:]):raise ValueError('Every fault requires a later restore step')
        if kind in ('restore_manual','restore_cli'):fault=False
    if fault:raise ValueError('Missing restoration')
    if plan['steps'][-1]['kind']!='review':raise ValueError('The last step must be review')

def templates(language='zh'):
    names=[('堆叠链路故障','Stack link failure'),('M-LAG Peer-Link 故障','M-LAG peer-link failure'),('上联故障','Uplink failure'),('下联故障','Downlink failure'),('聚合成员链路故障','LAG member failure'),('主控板故障','Supervisor failure'),('电源故障','Power supply failure'),('整台设备故障','Whole device failure'),('VRRP 接口故障','VRRP interface failure')]
    result=[]
    for zh,en in names:
        name=zh if language=='zh' else en
        def step(kind,title,instruction=''):
            return dict(kind=kind,title=title,targets=[],commands=[],instruction=instruction,seconds=5,expected='')
        steps=[step('manual','准备与恢复方案 / Readiness','确认操作对象、影响范围、独立管理路径、恢复方法和现场负责人。主控板操作须符合型号热插拔规程。 / Confirm exact asset, impact, management path, restoration and operator; follow vendor procedures.'),step('collect','正常基线 / Baseline'),step('fault_manual',name,'按批准方案操作指定对象；记录设备、接口/部件及操作时间。 / Follow the approved procedure; record device, interface/component and operation time.'),step('wait','稳定等待 / Settle'),step('collect','故障状态 / Fault state'),step('restore_manual','恢复现场 / Restore','恢复刚才操作的线缆、电源或部件，并确认现场状态。 / Restore the affected cable, power or component and confirm the site state.'),step('collect','恢复检查 / Recovery checks'),step('review','最终复核 / Final review')]
        for s in steps:
            for field in ('title','instruction'):
                value=s.get(field,'')
                if ' / ' in value:s[field]=value.split(' / ',1)[0 if language=='zh' else 1]
        result.append({'version':1,'name':name,'steps':steps})
    return result

class Session:
    def __init__(self,path,data):self.path=Path(path);self.data=data
    @classmethod
    def create(cls,root,plan):
        root=Path(root);root.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now().strftime('%Y%m%d-%H%M%S-%f');folder=root/stamp;folder.mkdir()
        session=cls(folder/'workflow.json',{'version':1,'plan':copy.deepcopy(plan),'index':0,'state':'ready','needs_restore':False,'events':[],'outcome':'REVIEW','started_at':utcnow()});session.save();return session
    @classmethod
    def load(cls,path):
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if data.get('version')!=1:raise ValueError('Unsupported workflow record')
        if not isinstance(data.get('index'),int) or not 0<=data['index']<=len(data.get('plan',{}).get('steps',[])):raise ValueError('Invalid workflow position')
        return cls(path,data)
    def save(self):
        temp=self.path.with_suffix('.tmp');temp.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(self.path)
    def event(self,event,**details):
        self.data['events'].append({'time':utcnow(),'event':event,'step':self.data['index'],**details});self.save()
    def arm(self):
        self.data['needs_restore']=True;self.event('fault_may_be_applied')
    def complete(self,note='',evidence=None):
        s=self.data['plan']['steps'][self.data['index']]
        if s['kind'].startswith('restore_'):self.data['needs_restore']=False
        self.event('step_completed',note=note,evidence=evidence or [])
        self.data['index']+=1
        if self.data['index']>=len(self.data['plan']['steps']):
            self.data['state']='unrestored' if self.data['needs_restore'] else 'completed';self.data['finished_at']=utcnow()
        self.save()
    def abort(self,reason):
        self.event('abort_requested',note=reason);self.data['outcome']='REVIEW';self.data['aborted']=True
        if self.data['needs_restore']:
            remaining=self.data['plan']['steps'][self.data['index']:]
            offset=next((i for i,s in enumerate(remaining) if s['kind'].startswith('restore_')),None)
            if offset is None:self.data['state']='unrestored'
            else:self.data['index']+=offset;self.data['state']='recovering'
        else:self.data['state']='aborted'
        self.save()
