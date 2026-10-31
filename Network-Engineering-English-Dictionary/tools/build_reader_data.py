from pathlib import Path
import json,re,shutil,html
root=Path(__file__).resolve().parents[1]
out=root
(out/'reader').mkdir(exist_ok=True)
toc=(root/'TABLE-OF-CONTENTS.md').read_text(encoding='utf-8'); parts=[]; chapters=[]
for line in toc.splitlines():
 if line.startswith('## Part '):parts.append({'title':line[3:],'chapters':[]})
 elif line.startswith('- [Chapter '):
  m=re.match(r'- \[(Chapter (\d+) · ([^]]+))\]\(([^)]+)\)',line)
  if not m:raise SystemExit('Unexpected chapter: '+line)
  c={'number':m.group(2),'title':m.group(3),'source':m.group(4),'part':len(parts),'pages':[],'entries':[],'examples':[],'sources':[]}
  parts[-1]['chapters'].append(c['number']);chapters.append(c)
assert len(parts)==8 and len(chapters)==32
by_chapter={c['number']:c for c in chapters};entries={}; paths={}
def sec(text,name):
 m=re.search(r'^## '+re.escape(name)+r'\s*\n(.*?)(?=^## |\Z)',text,re.M|re.S)
 return m.group(1).strip() if m else ''
def inline(s):
 s=re.sub(r'!\[([^]]*)\]\([^)]+\)',r'\1',s)
 s=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',s)
 s=s.replace('**','').replace('`','').strip()
 return s
def quotes(s):return [inline(x[2:]) for x in s.splitlines() if x.startswith('> ') and inline(x[2:])]
for p in root.glob('chapters/part-*/chapter-*/entries/*.md'):
 text=p.read_text(encoding='utf-8');meta={}
 for k,v in re.findall(r'^(id|headword|chapter|type|aliases): (.+)$',text,re.M):meta[k]=json.loads(v)
 key=meta['chapter']+'/'+p.stem
 if key in entries:raise SystemExit('Duplicate entry: '+key)
 usage=inline(sec(text,'Usage and distinctions') or sec(text,'词形与用法'))
 aliases=meta.get('aliases',[])
 abbr=re.search(r'Abbreviation: ([A-Z][A-Z0-9+/-]{1,12})\.',usage)
 if abbr and abbr.group(1) not in aliases:aliases.append(abbr.group(1))
 item={'key':key,'headword':meta['headword'],'chapter':meta['chapter'],'type':meta['type'],'definition':inline(sec(text,'Definition') or sec(text,'English definition')),'usage':usage,'aliases':aliases,'combinations':inline(sec(text,'Common combinations')),'examples':quotes(sec(text,'Examples') or sec(text,'工作例句'))}
 if not item['definition'] or not item['examples']:raise SystemExit('Incomplete entry: '+str(p))
 entries[key]=item;paths[p.resolve()]=key;by_chapter[meta['chapter']]['entries'].append(key)
imagefiles=set()
for c in chapters:
 readme=root/c['source']; text=readme.read_text(encoding='utf-8')
 c['examples']=quotes(sec(text,'Say it at work'));c['sources']=[{'title':x,'url':url} for x,url in re.findall(r'\[([^]]+)\]\((https?://[^)]+)\)',sec(text,'Sources'))]
 for p in sorted(readme.parent.glob('*.md')):
  if p.name=='README.md':continue
  raw=p.read_text(encoding='utf-8'); title=re.search(r'^# (.+)$',raw,re.M).group(1)
  match=re.search(r'!\[([^]]*)\]\(([^)]+)\)',raw)
  image=None;alt='';caption=''
  if match:
   img=(p.parent/match.group(2)).resolve()
   if not img.is_file() or root/'assets' not in img.parents:raise SystemExit('Missing or unsafe image: '+str(img))
   image=img.name;alt=match.group(1);imagefiles.add(image)
   tail=raw[match.end():]; cm=re.match(r'\s*\n\s*\*([^\n]+)\*',tail)
   if cm:caption=cm.group(1)
  table=sec(raw,'Professional expressions') or sec(raw,'Picture words') or sec(raw,'Key terms'); terms=[]
  for line in table.splitlines():
   if not line.startswith('|'):continue
   cells=[x.strip() for x in line.strip('|').split('|')]
   if not cells or cells[0] in ('No.','Word') or re.match(r'^[-: ]+$',cells[0]):continue
   if len(cells)==3 and cells[0].isdigit():number,word,meaning=cells
   elif len(cells)==2:number='';word,meaning=cells
   else:raise SystemExit('Bad table: '+str(p)+' '+line)
   lm=re.search(r'\[([^]]+)\]\(([^)]+)\)',word);label=inline(word);entry=None
   if lm:
    target=(p.parent/lm.group(2).split('#')[0]).resolve();entry=paths.get(target)
    if not entry:raise SystemExit('Missing entry reference: '+str(p)+' -> '+lm.group(2))
   terms.append({'number':number,'word':label,'meaning':inline(meaning),'entry':entry})
  if not terms:raise SystemExit('No terms: '+str(p))
  more=[]
  for label,target in re.findall(r'\[([^]]+)\]\(([^)]+)\)',sec(raw,'More words') or sec(raw,'Related words')):
   key=paths.get((p.parent/target.split('#')[0]).resolve())
   if not key:raise SystemExit('Missing related entry: '+str(p)+' -> '+target)
   more.append({'label':label,'entry':key})
  extras=[]
  for heading,body in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',raw,re.M|re.S):
   if heading in ('Professional expressions','Picture words','Key terms','Examples and usage','More words','Related words'):continue
   blocks=[]
   for paragraph in re.split(r'\n\s*\n',body.strip()):
    if not paragraph.strip():continue
    quoted=paragraph.lstrip().startswith('> ')
    paragraph=re.sub(r'^> ?', '',paragraph,flags=re.M).replace('\n',' ').replace('**','').replace('`','')
    paragraph=re.sub(r'\*([^*]+)\*',r'\1',paragraph)
    segments=[];cursor=0
    for lm in re.finditer(r'\[([^]]+)\]\(([^)]+)\)',paragraph):
     if lm.start()>cursor:segments.append({'text':paragraph[cursor:lm.start()]})
     target=(p.parent/lm.group(2).split('#')[0]).resolve();key=paths.get(target)
     if not key:raise SystemExit('Missing supplementary entry reference: '+str(p)+' -> '+lm.group(2))
     segments.append({'text':lm.group(1),'entry':key});cursor=lm.end()
    if cursor<len(paragraph):segments.append({'text':paragraph[cursor:]})
    blocks.append({'quote':quoted,'segments':segments})
   extras.append({'title':heading,'blocks':blocks})
  c['pages'].append({'slug':p.stem,'title':title,'image':image,'alt':alt,'caption':caption,'terms':terms,'examples':quotes(sec(raw,'Examples and usage')),'more':more,'extras':extras})
 c['entries'].sort(key=lambda key:entries[key]['headword'].casefold())
 if not c['pages']:raise SystemExit('No reading pages for chapter '+c['number'])
payload={'parts':parts,'chapters':chapters,'entries':entries}
raw=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
(out/'reader/data.js').write_text('window.DICTIONARY_DATA = '+raw+';\n',encoding='utf-8')
print(json.dumps({'chapters':len(chapters),'entries':len(entries),'pages':sum(len(c['pages']) for c in chapters),'images':len(imagefiles)}))
