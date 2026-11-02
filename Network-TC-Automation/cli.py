import argparse, getpass
from pathlib import Path
from adapters.ssh import SSHAdapter
from core.engine import Engine
from core.scheduler import Scheduler
from storage.evidence import EvidenceStore
from storage.project import load

def main():
    parser=argparse.ArgumentParser(description='SSH network T&C engine')
    parser.add_argument('--project',required=True)
    parser.add_argument('--username',default='')
    parser.add_argument('--timeout',type=int,default=30)
    args=parser.parse_args()
    name,devices,tasks=load(args.project)
    for t in tasks: print(t.device_id,t.command)
    if input('Type RUN to connect: ')!='RUN': return 1
    adapter=SSHAdapter(args.username,getpass.getpass('SSH password: '),args.timeout)
    results=Scheduler().run(Engine(adapter,EvidenceStore(Path(args.project).resolve().parent/'evidence')),tasks,{d.id:d for d in devices})
    for r in results: print(r.device_name,r.device_ip,r.task.id,r.status,r.error,r.evidence_dir)
    return int(any(r.status in ('FAIL','ERROR') for r in results))
if __name__=='__main__':raise SystemExit(main())
