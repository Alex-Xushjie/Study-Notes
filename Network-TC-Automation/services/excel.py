from core.models import Device, Task
from services.tasks import library, validate_command
from storage.project import validate

def load(path):
    from openpyxl import load_workbook
    book=load_workbook(path,read_only=True,data_only=True)
    try:
        def rows(name):
            if name not in book.sheetnames: raise ValueError('缺少工作表: '+name)
            data=iter(book[name].values); headers=next(data,())
            return [dict(zip(headers,row)) for row in data if any(v is not None for v in row)]
        devices=[]
        for r in rows('Devices'):
            devices.append(Device(str(r.get('Hostname') or r.get('Device ID') or '').strip(),str(r.get('Management IP') or '').strip(),str(r.get('Platform') or 'huawei_vrp').strip(),int(r.get('Port') or 22),str(r.get('Username') or ''),str(r.get('Group') or ''),str(r.get('Password') or '')))
        validate(devices,[]); lookup={d.id:d for d in devices}; tasks=[]
        for rownum,r in enumerate(rows('Test Cases') if 'Test Cases' in book.sheetnames else [],2):
            try:
                d=lookup[str(r.get('Hostname') or r.get('Device ID') or '').strip()]
                command=r.get('Command') or library(d,str(r.get('Library ID') or '')).command
                tasks.append(Task(str(r.get('Test ID') or '').strip(),d.id,validate_command(command),'excel',str(r.get('Expected') or ''),str(r.get('Test Name') or ''),str(r.get('Section') or ''),[validate_command(c) for c in str(r.get('Steps') or '').splitlines() if c.strip()],str(r.get('Criteria') or ''),str(r.get('Logical Group') or '')))
            except (KeyError,ValueError) as exc: raise ValueError(f'Test Cases 第 {rownum} 行无效: {exc}') from None
        validate(devices,tasks)
        return lookup,tasks
    finally: book.close()

def template(path):
    from openpyxl import Workbook
    book=Workbook(); ws=book.active; ws.title='Devices'
    ws.append(['Hostname','Management IP','Platform','Port','Username','Group','Password'])
    ws.append(['R1','192.168.100.101','cisco_ios',22,'lab','EVE-NG'])
    ws=book.create_sheet('Test Cases'); ws.append(['Test ID','Hostname','Command','Library ID','Expected','Test Name','Section','Steps','Criteria','Logical Group'])
    ws.append(['TC-001','R1','show version',None,None]); ws.append(['TC-002','R1',None,'interfaces.brief',None])
    for ws in book:
        ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
        for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=26
    book.save(path)
