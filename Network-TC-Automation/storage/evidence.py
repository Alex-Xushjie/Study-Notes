from pathlib import Path
from datetime import datetime

def safe(value, limit=48):
    value=re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(value))
    value=re.sub(r"\s+", "_", value).strip(" ._")
    return (value or "unknown")[:limit]

from dataclasses import asdict
import json, re, textwrap

class EvidenceStore:
    def __init__(self,root):
        base=Path(root).resolve(); base.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
        for i in range(1,10000):
            self.root=base/(stamp if i==1 else f'{stamp}-{i:02}')
            try: self.root.mkdir(); break
            except FileExistsError: continue
        else: raise OSError('运行目录重名过多')
    def save(self,result):
        from PIL import Image,ImageDraw,ImageFont
        label=f'{safe(result.device_name,32)}-{safe(result.device_ip,40)}-{safe(result.task.name or result.task.command,48)}'
        task_id=safe(result.task.id,20)
        for i in range(1,10000):
            folder=self.root/f'{label}-{task_id}-{i:02}'
            try: folder.mkdir(); break
            except FileExistsError: continue
        else: raise OSError('任务目录重名过多')
        result.evidence_dir=str(folder)
        (folder/(label+'.txt')).write_bytes(result.output.encode('utf-8'))
        metadata=asdict(result)
        (folder/'result.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
        header=f'| {result.device_name} | {result.device_ip} | {result.task.name or result.task.command} |'
        text=result.output+'\n'+result.error
        text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text).expandtabs(4)
        font=None
        for name in ('C:/Windows/Fonts/consola.ttf','DejaVuSansMono.ttf','C:/Windows/Fonts/msyh.ttc'):
            try: font=ImageFont.truetype(name,16); break
            except OSError: pass
        if font is None: font=ImageFont.load_default()
        lines=[part for line in text.splitlines() for part in (textwrap.wrap(line,100,replace_whitespace=False,drop_whitespace=False) or [''])]
        for start in range(0,len(lines),70):
            chunk=textwrap.wrap(header,160,replace_whitespace=False,drop_whitespace=False) + [''] + lines[start:start+70]
            image=Image.new('RGB',(1700,80+28*len(chunk)),'#101820')
            ImageDraw.Draw(image).multiline_text((20,20),'\n'.join(chunk),font=font,fill='white',spacing=9)
            image.save(folder/f'{label}-{start//70+1:03}.png')

def history(root):
    found=[]
    for path in Path(root).glob('*/*/result.json'):
        try:
            data=json.loads(path.read_text(encoding='utf-8'));
            if data.get('simulated',False): continue
            data.setdefault('started_at',data.get('timestamp','')); data.setdefault('error',''); data['evidence_dir']=str(path.parent.resolve()); found.append(data)
        except (ValueError,OSError): continue
    return sorted(found,key=lambda r:r.get('started_at',''),reverse=True)

def review(folder,status,note,actual=""):
    from core.models import utcnow
    if status not in ('PASS','FAIL','REVIEW','N/A','PASS WITH COMMENTS'): raise ValueError('无效复核状态')
    path=Path(folder)/'review.json'
    path.write_text(json.dumps({'status':status,'note':note,'actual':actual,'reviewed_at':utcnow()},ensure_ascii=False,indent=2),encoding='utf-8')
