from core.models import Task
# Read-only starter templates; verify commands against the actual vendor/model.
TEMPLATES={
 'Basic / Identity':('BASIC-01','设备身份与版本','Basic Configuration',['show version','show inventory'],['display version','display device']),
 'Basic / Management':('BASIC-02','管理地址与路由','Basic Configuration',['show ip interface brief','show ip route'],['display ip interface brief','display ip routing-table']),
 'Basic / NTP':('BASIC-03','时间与 NTP','Basic Configuration',['show clock detail','show ntp status','show ntp associations'],['display clock','display ntp-service status','display ntp-service sessions']),
 'L2 / VLAN':('L2-01','VLAN 配置','L2 Configuration',['show vlan brief'],['display vlan']),
 'L2 / LACP':('L2-02','链路聚合状态','L2 Configuration',['show etherchannel summary','show lacp neighbor'],['display eth-trunk']),
 'L2 / STP':('L2-03','STP 状态','L2 Configuration',['show spanning-tree'],['display stp brief']),
 'Routing / OSPF':('ROUTE-01','OSPF 邻居与接口','Routing',['show ip ospf neighbor','show ip ospf interface brief'],['display ospf peer brief','display ospf interface']),
 'Routing / Routes':('ROUTE-02','路由表','Routing',['show ip route'],['display ip routing-table'])
}
def apply(devices, keys):
    tasks=[]
    for d in devices:
        if d.platform not in ('cisco_ios','huawei_vrp'): raise ValueError('首批模板仅支持 cisco_ios / huawei_vrp: '+d.id)
        for key in keys:
            tid,name,section,cisco,huawei=TEMPLATES[key]; steps=cisco if d.platform=='cisco_ios' else huawei
            tasks.append(Task(tid,d.id,steps[0],'library',name=name,section=section,steps=list(steps),criteria='按批准设计人工核对；填写项目预期值后复核',logical_group=d.group))
    return tasks
