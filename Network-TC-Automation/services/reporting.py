import csv,json
from pathlib import Path
from storage.evidence import history

def export_index(root,path):
    fields=['Run','Hostname','IP','Section','Test ID','Test Name','Logical Group','Execution','Auto Result','Review','Actual Result','Remark','Criteria','Retest Of','Commands','TXT','PNG','Metadata']
    with open(path,'w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream); writer.writerow(fields)
        for r in history(root):
            folder=Path(r['evidence_dir']); t=r['task']
            try: manual=json.loads((folder/'review.json').read_text(encoding='utf-8'))
            except (OSError,ValueError): manual={}
            writer.writerow([folder.parent.name,r.get('device_name',t['device_id']),r.get('device_ip',''),t.get('section',''),t['id'],t.get('name',''),t.get('logical_group',''),r.get('execution_status') or ('ERROR' if r['status']=='ERROR' else 'COMPLETED'),r['status'],manual.get('status','REVIEW'),manual.get('actual',''),manual.get('note',''),t.get('criteria',''),t.get('retest_of',''),' | '.join(t.get('steps') or [t['command']]),' | '.join(str(p.resolve()) for p in folder.glob('*.txt')),' | '.join(str(p.resolve()) for p in folder.glob('*.png')),str(folder/'result.json')])
