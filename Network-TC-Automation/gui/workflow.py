import json,copy
from pathlib import Path
from PySide6.QtCore import QThread,Signal,QTimer
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QComboBox,QLineEdit,QTextEdit,
    QTableWidget,QTableWidgetItem,QFileDialog,QMessageBox,QInputDialog,QFormLayout,QSpinBox,QDialogButtonBox)
from gui import i18n
from services.workflows import KINDS,templates,validate,Session
from adapters.ssh import SSHAdapter
from adapters.profiles import PROFILES
from core.models import Task,Result,utcnow
from core.engine import Engine
from storage.evidence import EvidenceStore,review

def L(zh,en):return zh if i18n.language=='zh' else en
LABELS={
'collect':('状态采集','Collect status'),'manual':('人工确认','Manual confirmation'),
'fault_manual':('人工故障操作','Manual fault'),'fault_cli':('CLI 故障操作','CLI fault'),
'wait':('等待','Wait'),'restore_manual':('人工恢复','Manual restore'),
'restore_cli':('CLI 恢复','CLI restore'),'review':('最终复核','Final review')}

def label(kind):return L(*LABELS[kind])

class StepEditor(QDialog):
    def __init__(self,step,devices,parent=None):
        super().__init__(parent);self.setWindowTitle(L('编辑工作流步骤','Edit workflow step'));self.resize(720,650)
        box=QVBoxLayout(self);form=QFormLayout();box.addLayout(form)
        self.kind=QComboBox()
        for k in KINDS:self.kind.addItem(label(k),k)
        self.kind.setCurrentIndex(KINDS.index(step.get('kind','collect')));form.addRow(L('类型','Type'),self.kind)
        self.title=QLineEdit(step.get('title',''));form.addRow(L('步骤名称','Step title'),self.title)
        self.targets=QLineEdit(','.join(step.get('targets',[])));form.addRow(L('目标主机名（逗号分隔）','Target hostnames (comma separated)'),self.targets)
        help=QLabel(L('可用设备：','Available devices: ')+', '.join(devices));help.setWordWrap(True);box.addWidget(help)
        self.commands=QTextEdit();self.commands.setPlainText('\n'.join(step.get('commands',[])));form.addRow(L('命令（一行一条）','Commands (one per line)'),self.commands)
        self.instruction=QTextEdit();self.instruction.setPlainText(step.get('instruction',''));form.addRow(L('操作说明与对象','Instructions and exact target'),self.instruction)
        self.seconds=QSpinBox();self.seconds.setRange(1,3600);self.seconds.setValue(step.get('seconds',5));form.addRow(L('等待秒数','Wait seconds'),self.seconds)
        self.expected=QLineEdit(step.get('expected',''));form.addRow(L('采集预期包含文本（可空）','Expected text for collection (optional)'),self.expected)
        info=QLabel(L('CLI 步骤填写完整配置命令（例如 interface、shutdown），不得填写密码。故障后必须安排恢复步骤。','For CLI steps enter full config commands (e.g. interface, shutdown), never passwords. Add restoration after every fault.'));info.setWordWrap(True);box.addWidget(info)
        buttons=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel);buttons.accepted.connect(self.accept);buttons.rejected.connect(self.reject);box.addWidget(buttons)
    def value(self):
        return dict(kind=self.kind.currentData(),title=self.title.text().strip(),targets=[v.strip() for v in self.targets.text().replace('，',',').split(',') if v.strip()],commands=[v.strip() for v in self.commands.toPlainText().splitlines() if v.strip()],instruction=self.instruction.toPlainText(),seconds=self.seconds.value(),expected=self.expected.text())

class StepWorker(QThread):
    done=Signal(object,str)
    def __init__(self,step,devices,root,timeout):
        super().__init__();self.step=copy.deepcopy(step);self.devices=dict(devices);self.root=root;self.timeout=timeout
    def run(self):
        paths=[];error=''
        try:
            adapter=SSHAdapter('','',self.timeout);store=EvidenceStore(self.root)
            for target in self.step['targets']:
                d=self.devices[target]
                if self.step['kind']=='collect':
                    task=Task('WF',d.id,self.step['commands'][0],'quick',expected=self.step.get('expected',''),name=self.step['title'],section='Workflow',steps=self.step['commands'])
                    result=Engine(adapter,store).run(task,d)
                else:
                    started=utcnow();output=adapter.configure(d,self.step['commands'])
                    result=Result(Task('WF',d.id,self.step['commands'][0],'quick',name=self.step['title'],section='Workflow',steps=self.step['commands']),'REVIEW',output,started_at=started,finished_at=utcnow(),device_ip=d.host,device_name=adapter.hostname or d.id,prompt=adapter.prompt,execution_status='COMPLETED')
                    store.save(result)
                import re
                if re.search(r'(?im)^\s*(%\s*(Invalid|Incomplete|Ambiguous|Error)|Error:|Unrecognized command)',result.output):error+=d.id+': command rejected by device\n'
                paths.append(result.evidence_dir)
                if result.status in ('ERROR','FAIL'):error+=d.id+': '+result.status+' '+result.error+'\n'
        except Exception as exc:error+=str(exc)
        self.done.emit(paths,error)

class WorkflowDialog(QDialog):
    def __init__(self,devices,evidence_root,timeout,parent=None):
        super().__init__(parent);self.devices={d.id:d for d in devices};self.evidence_root=Path(evidence_root);self.timeout=timeout
        self.plan={'version':1,'name':'','steps':[]};self.session=None;self.worker=None;self.waiting=False;self.capture_ready=False
        self.setWindowTitle(L('冗余测试工作流','Redundancy test workflow'));self.resize(1050,800)
        box=QVBoxLayout(self);top=QHBoxLayout();box.addLayout(top)
        self.presets=templates(i18n.language);self.preset=QComboBox()
        for p in self.presets:self.preset.addItem(p['name'])
        top.addWidget(self.preset)
        self.edit_buttons=[]
        self.button(top,L('载入预置模板','Load preset'),self.load_preset,True)
        self.button(top,L('打开自定义模板','Open template'),self.open_template,True)
        self.button(top,L('另存模板','Save template as'),self.save_template,True)
        self.button(top,L('继续执行记录','Resume run'),self.resume,True)
        self.name=QLineEdit();box.addWidget(self.name)
        self.table=QTableWidget(0,4);self.table.setHorizontalHeaderLabels([L('类型','Type'),L('步骤','Step'),L('设备','Devices'),L('命令/说明','Commands / instructions')]);self.table.setSelectionBehavior(QTableWidget.SelectRows);self.table.setEditTriggers(QTableWidget.NoEditTriggers);self.table.horizontalHeader().setStretchLastSection(True);self.table.cellDoubleClicked.connect(lambda *_:self.edit_step());box.addWidget(self.table)
        row=QHBoxLayout();box.addLayout(row)
        for title,fn in [(L('新增','Add'),self.add_step),(L('编辑','Edit'),self.edit_step),(L('复制','Duplicate'),self.duplicate),(L('删除','Delete'),self.delete),(L('上移','Up'),lambda:self.move(-1)),(L('下移','Down'),lambda:self.move(1))]:self.button(row,title,fn,True)
        self.status=QLabel();self.status.setWordWrap(True);box.addWidget(self.status)
        self.details=QTextEdit();self.details.setReadOnly(True);box.addWidget(self.details)
        self.note=QLineEdit();self.note.setPlaceholderText(L('现场记录 / 实际结果 / 备注','Site notes / actual result / remarks'));box.addWidget(self.note)
        row=QHBoxLayout();box.addLayout(row)
        self.start_button=self.button(row,L('开始新执行','Start new run'),self.start,True)
        self.next_button=self.button(row,L('执行 / 确认完成本步','Execute / confirm step'),self.advance)
        self.abort_button=self.button(row,L('中止并进入恢复','Abort and restore'),self.abort)
        self.unrestored_button=self.button(row,L('无法恢复，记录未恢复','Record unable to restore'),self.unrestored)
        self.timer=QTimer(self);self.timer.setSingleShot(True);self.timer.timeout.connect(self.wait_done)
        self.load_preset()
    def button(self,row,text,fn,editor=False):
        b=QPushButton(text);b.clicked.connect(lambda:self.guard(fn));row.addWidget(b)
        if editor:self.edit_buttons.append(b)
        return b
    def guard(self,fn):
        try:fn()
        except Exception as exc:QMessageBox.warning(self,L('操作失败','Operation failed'),str(exc))
    def refresh(self):
        self.name.setText(self.plan['name']);self.table.setRowCount(len(self.plan['steps']))
        for i,s in enumerate(self.plan['steps']):
            for j,value in enumerate([label(s['kind']),s['title'],','.join(s.get('targets',[])),' ; '.join(s.get('commands',[])) or s.get('instruction','')]):self.table.setItem(i,j,QTableWidgetItem(value))
        active=self.session is not None and self.session.data['state'] not in ('completed','aborted','unrestored')
        for b in self.edit_buttons:b.setEnabled(not active and self.worker is None)
        self.name.setEnabled(not active);self.next_button.setEnabled(active and self.worker is None and not self.waiting)
        self.abort_button.setEnabled(active and self.worker is None)
        self.unrestored_button.setEnabled(active and self.session.data['needs_restore'] and self.worker is None)
    def load_preset(self):
        self.plan=copy.deepcopy(self.presets[self.preset.currentIndex()])
        # Generic baseline is a starting point, not a complete vendor-specific redundancy test.
        for s in self.plan['steps']:
            if s['kind']=='collect':
                if len(self.devices)==1:
                    d=next(iter(self.devices.values()));s['targets']=[d.id];s['commands']=[PROFILES[d.platform]['system.version'],PROFILES[d.platform]['interfaces.brief']]
        self.session=None;self.refresh();self.details.setPlainText(L('这是起始模板，请编辑采集命令、目标接口/部件、故障与恢复说明。多设备时需逐步填写目标设备。默认人工故障；VRRP 可自行改成 CLI 故障并配置 CLI 恢复。','Starter template: edit collection commands, exact interfaces/components and fault/restore instructions. Set targets for multi-device steps. Faults are manual by default; VRRP may be changed to CLI fault with CLI restoration.'))
    def open_template(self):
        p,_=QFileDialog.getOpenFileName(self,L('打开模板','Open template'),'','JSON (*.json)')
        if p:self.plan=json.loads(Path(p).read_text(encoding='utf-8'));self.session=None;self.refresh()
    def save_template(self):
        self.plan['name']=self.name.text().strip();validate(self.plan,self.devices)
        p,_=QFileDialog.getSaveFileName(self,L('保存模板','Save template'),'workflow.json','JSON (*.json)')
        if p:Path(p).write_text(json.dumps(self.plan,ensure_ascii=False,indent=2),encoding='utf-8')
    def add_step(self):
        self.edit_value({'kind':'collect','title':'','commands':[],'targets':[]},None)
    def edit_step(self):
        if self.session and self.session.data['state'] not in ('completed','aborted','unrestored'):return
        i=self.table.currentRow()
        if i>=0:self.edit_value(self.plan['steps'][i],i)
    def edit_value(self,step,index):
        dialog=StepEditor(step,self.devices,self)
        if dialog.exec()==QDialog.Accepted:
            self.plan['name']=self.name.text()
            if index is None:self.plan['steps'].append(dialog.value())
            else:self.plan['steps'][index]=dialog.value()
            self.refresh()
    def duplicate(self):
        self.plan["name"]=self.name.text()
        i=self.table.currentRow()
        if i>=0:self.plan['steps'].insert(i+1,copy.deepcopy(self.plan['steps'][i]));self.refresh()
    def delete(self):
        self.plan["name"]=self.name.text()
        i=self.table.currentRow()
        if i>=0:self.plan['steps'].pop(i);self.refresh()
    def move(self,offset):
        self.plan["name"]=self.name.text()
        i=self.table.currentRow();j=i+offset
        if i>=0 and 0<=j<len(self.plan['steps']):self.plan['steps'][i],self.plan['steps'][j]=self.plan['steps'][j],self.plan['steps'][i];self.refresh();self.table.selectRow(j)
    def check_credentials(self):
        used={d for s in self.plan['steps'] for d in s.get('targets',[])}
        if any(not self.devices[d].username or not self.devices[d].password for d in used):raise ValueError(L('请先在设备页填写目标设备账号密码','Enter credentials for target devices on the Devices page'))
    def start(self):
        self.plan['name']=self.name.text().strip();validate(self.plan,self.devices);self.check_credentials()
        if QMessageBox.question(self,L('开始工作流','Start workflow'),L('确认操作对象、变更窗口、恢复方法与独立管理路径。模板命令必须按实际设备核对。开始？','Confirm exact targets, change window, restoration and independent management access. Verify commands for your devices. Start?'))!=QMessageBox.Yes:return
        self.session=Session.create(self.evidence_root.parent/'workflow-runs',self.plan)
        self.session.data['inventory']=[{'id':d.id,'host':d.host,'platform':d.platform,'port':d.port} for d in self.devices.values()];self.session.save()
        self.capture_ready=False;self.present()
    def resume(self):
        p,_=QFileDialog.getOpenFileName(self,L('继续执行记录','Resume run'),str(self.evidence_root.parent/'workflow-runs'),'JSON (*.json)')
        if not p:return
        loaded=Session.load(p)
        for d in loaded.data.get('inventory',[]):
            if d['id'] not in self.devices or self.devices[d['id']].host!=d['host']:raise ValueError(L('设备清单与原执行记录不一致，请先核对设备地址','Inventory differs from the original run; verify device addresses first'))
        self.plan=copy.deepcopy(loaded.data['plan']);validate(self.plan,self.devices);self.check_credentials();self.session=loaded
        if self.session.data['needs_restore']:self.session.abort('Resumed after interruption; recovery required')
        self.capture_ready=False;self.present()
    def present(self):
        self.refresh();d=self.session.data;self.status.setText(str(self.session.path)+' | '+d['state'])
        if d['state'] in ('completed','aborted','unrestored'):
            self.details.setPlainText(L('执行已结束，记录保存在以上路径。','Run ended; record saved at the path above.')+'\n'+d.get('outcome','REVIEW'));return
        s=self.plan['steps'][d['index']]
        if s['kind'].startswith('fault_') and not d['needs_restore']:self.session.arm()
        self.table.selectRow(d['index'])
        self.details.setPlainText(f"{d['index']+1}/{len(self.plan['steps'])}: {s['title']}\n{s.get('instruction','')}\n"+'\n'.join(s.get('commands',[])))
        self.next_button.setText(L('执行 / 确认完成本步','Execute / confirm step'))
    def advance(self):
        if not self.session:return
        s=self.plan['steps'][self.session.data['index']];kind=s['kind']
        if kind=='review':
            codes=['REVIEW','PASS','FAIL','N/A','PASS WITH COMMENTS'];labels=codes if i18n.language=='en' else ['待复核','通过','不通过','不适用','带意见通过']
            value,ok=QInputDialog.getItem(self,L('最终复核','Final review'),L('结论','Outcome'),labels,0,False)
            if ok:value=codes[labels.index(value)] if value in labels else value
            if not ok:return
            if value=='PASS' and (self.session.data.get('failures') or self.session.data.get('aborted')):raise ValueError(L('存在失败步骤，请复测或记录带意见结论','Failed steps exist; retest or record a qualified outcome'))
            if value in ('N/A','PASS WITH COMMENTS') and not self.note.text().strip():raise ValueError(L('请填写结论原因','Enter the reason for this outcome'))
            self.session.data['outcome']=value;self.complete();return
        if kind=='wait':
            self.waiting=True;self.session.event('wait_started',seconds=s['seconds']);self.timer.start(s['seconds']*1000);self.refresh();return
        if kind in ('manual','fault_manual','restore_manual'):
            if kind=='fault_manual' and not self.session.data['needs_restore']:self.session.arm()
            reply=QMessageBox.question(self,label(kind),s.get('instruction','')+'\n\n'+L('确认已完成操作？未完成请选 No。','Confirm the operation is complete. Select No if not complete.'))
            if reply==QMessageBox.Yes:self.complete()
            else:self.present()
            return
        if kind=='collect' and self.capture_ready:
            self.capture_ready=False;self.complete();return
        if kind in ('fault_cli','restore_cli'):
            if QMessageBox.question(self,label(kind),L('将修改设备配置。确认目标与完整命令：','This changes device configuration. Confirm targets and commands:')+'\n'+','.join(s['targets'])+'\n'+'\n'.join(s['commands']))!=QMessageBox.Yes:return
            if kind=='fault_cli' and not self.session.data['needs_restore']:self.session.arm()
        self.session.event('step_started',kind=kind);self.worker=StepWorker(s,self.devices,self.evidence_root,self.timeout);self.worker.done.connect(self.step_done);self.worker.finished.connect(self.worker_finished);self.worker.start();self.refresh()
    def step_done(self,paths,error):
        self.session.event('collection_finished',evidence=paths,error=error);self.details.append('\n'+'\n'.join(paths)+'\n'+error)
        if error:
            self.session.data.setdefault('failures',[]).append({'step':self.session.data['index'],'error':error});self.session.save()
            self.capture_ready=False
            self.details.append(L('步骤失败：可重试，或中止并恢复现场。','Step failed: retry, or abort and restore.'));return
        self.capture_ready=False;self.complete(evidence=paths)
    def worker_finished(self):
        worker=self.worker;self.worker=None;worker.deleteLater();self.refresh()
    def wait_done(self):self.waiting=False;self.complete()
    def complete(self,evidence=None):
        self.session.complete(self.note.text(),evidence);self.note.clear();self.present()
    def abort(self):
        if not self.session:return
        self.timer.stop();self.waiting=False;self.session.abort(self.note.text() or 'Operator aborted');self.note.clear();self.present()
    def unrestored(self):
        if not self.note.text().strip():raise ValueError(L('请记录未恢复原因和现场交接信息','Record the reason and site handover details'))
        self.timer.stop();self.waiting=False;self.session.data['state']='unrestored';self.session.data['outcome']='FAIL';self.session.event('unable_to_restore',note=self.note.text());self.present()
    def closeEvent(self,event):
        if self.worker is not None:QMessageBox.information(self,L('执行中','Running'),L('请等待当前命令完成或超时','Wait for the current command to finish or time out'));event.ignore();return
        if self.session and self.session.data['state'] not in ('completed','aborted','unrestored'):
            QMessageBox.information(self,L('工作流未结束','Workflow active'),L('请先中止并恢复，或记录无法恢复。','Abort and restore first, or record unable to restore.'));event.ignore();return
        event.accept()
