import json
from pathlib import Path
from PySide6.QtCore import QSettings
CATALOG=json.loads(Path(__file__).with_name('translations.json').read_text(encoding='utf-8'))
ZH={'Hostname':'主机名','Test ID':'测试编号','Quick Command（单行）':'临时命令（单行）','逻辑设备组 / Stack':'逻辑设备组 / 堆叠',
    'Basic / Identity':'基础 / 身份与版本','Basic / Management':'基础 / 管理地址','Basic / NTP':'基础 / 时间与 NTP','L2 / VLAN':'二层 / VLAN','L2 / LACP':'二层 / 链路聚合','L2 / STP':'二层 / STP','Routing / OSPF':'路由 / OSPF','Routing / Routes':'路由 / 路由表'}
ZH['Hostname被任务引用后不允许修改；需要先删除关联任务。SSH 测试结果也会保存证据。']='主机名被任务引用后不允许修改；需要先删除关联任务。SSH 测试结果也会保存证据。'
settings=QSettings('NetworkTC','Desktop')
language=settings.value('language','zh')
def set_language(value):
    global language
    language=value if value in ('zh','en') else 'zh'
    settings.setValue('language',language)
def tr(text):
    if language=='zh':return ZH.get(text,text)
    return CATALOG.get(text,text)
def message(text):
    if language=='zh':return text
    for source in sorted(CATALOG,key=len,reverse=True):
        if source and source in text:text=text.replace(source,CATALOG[source])
    return text
