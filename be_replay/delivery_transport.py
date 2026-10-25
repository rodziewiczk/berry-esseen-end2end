"""Append-only full-stage transport and durable logging for new deliveries.

Transport is not an evidence reader. A caller must supply its complete pure
validator on both saving and restoration. Never import executable ZIP entries.
"""
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib,shutil,stat,threading,time,uuid,zipfile
from .colab_batch import atomic_json,event,bundle

MIB=1024**2

def need(ok,message):
 if not ok:raise ValueError(message)

def ordinary(path):
 p=Path(path).absolute()
 for q in(p,*p.parents):need(not q.is_symlink()and not(getattr(q,'is_junction',lambda:False)()),'Ordinary nonlinked artifact ancestry')
 return p

def parts(name):
 need(type(name)is str and name and not any(c in name for c in ('\\',':','\0')),'Portable relative ZIP name')
 rows=name.split('/');need(all(x and x not in('.','..')and x==x.rstrip(' .')for x in rows),'Contained unaliased artifact name');return rows

def digest(path):
 h=hashlib.sha256()
 with ordinary(path).open('rb')as f:
  for block in iter(lambda:f.read(MIB),b''):h.update(block)
 return h.hexdigest()

def inventory(root,*,omit=()):
 root=ordinary(root);result={}
 for p in sorted(root.rglob('*')):
  ordinary(p)
  if p.is_file()and p.relative_to(root).as_posix()not in omit:
   result[p.relative_to(root).as_posix()]=dict(bytes=p.stat().st_size,sha256=digest(p))
 return result

def zip_members(z,*,max_total=2*1024**3,max_members=100000):
 rows=z.infolist();need(0<len(rows)<=max_members,'Bounded complete ZIP census');seen=set();total=0
 for r in rows:
  parts(r.filename);fold=r.filename.casefold();mode=stat.S_IFMT(r.external_attr>>16)
  need(fold not in seen and not r.is_dir()and not r.flag_bits&1 and mode in(0,stat.S_IFREG)
   and 0<=r.file_size<=256*MIB,'Unique ordinary unencrypted bounded artifact')
  seen.add(fold);total+=r.file_size
 need(total<=max_total,'Bounded whole ZIP expansion');return rows

def save(root,directory,*,validator,label='stage'):
 root=ordinary(root);checked=validator(root);directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True)
 name=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:12]+'-'+label+'-complete.zip'
 out=directory/name;pending=directory/(name+'.pending')
 with zipfile.ZipFile(pending,'x',zipfile.ZIP_DEFLATED,strict_timestamps=False)as z:
  for p in sorted(root.rglob('*')):
   ordinary(p)
   if p.is_file():z.write(p,p.relative_to(root).as_posix())
  zip_members(z)
 pin=digest(pending);pending.replace(out);out.with_suffix('.zip.sha256').write_text(pin+'  '+out.name+'\n',encoding='ascii')
 return dict(path=str(out),sha256=pin)

def restore(directory,destination,*,validator,log=lambda *a,**k:None):
 directory=ordinary(directory);destination=ordinary(destination)
 if not directory.exists():return None
 for p in sorted(directory.glob('*-complete.zip'),reverse=True)[:64]:
  try:
   ordinary(p);marker=ordinary(p.with_suffix('.zip.sha256'))
   need(p.is_file()and p.stat().st_size<=2*1024**3 and marker.is_file()and marker.stat().st_size<=1024
    and marker.read_text('ascii')==digest(p)+'  '+p.name+'\n','Exact complete-stage SHA256 sidecar')
   out=destination/('restored-'+uuid.uuid4().hex[:12])
   with zipfile.ZipFile(p)as z:
    rows=zip_members(z);out.mkdir(parents=True,exist_ok=False)
    for r in rows:
     target=out.joinpath(*parts(r.filename));target.parent.mkdir(parents=True,exist_ok=True)
     with z.open(r)as s,target.open('xb')as d:shutil.copyfileobj(s,d,MIB)
   checked=validator(out);log('complete_stage_revalidated',path=str(p),sha256=digest(p))
   return out,checked,dict(path=str(p),sha256=digest(p))
  except Exception as error:log('complete_stage_rejected',path=str(p),error=type(error).__name__+': '+str(error))
 return None

class Follow:
 def __init__(self,root,execution,action):
  self.root,self.execution,self.action=Path(root),Path(execution),action;self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,daemon=True)
 def loop(self):
  position=0;partial=b'';started=time.monotonic();last=-20;drain=False
  while True:
   try:
    with(self.execution/'stdout.txt').open('rb')as f:f.seek(position);raw=f.read(MIB)
    position+=len(raw);lines=(partial+raw).split(b'\n');partial=lines.pop()
    for line in lines:event(self.root,'original_stdout',action=self.action,line=line.decode('utf-8',errors='replace')[:4096])
   except FileNotFoundError:pass
   elapsed=time.monotonic()-started
   if elapsed-last>=20:event(self.root,'original_action_heartbeat',action=self.action,elapsed_seconds=elapsed,stdout_bytes=position);last=elapsed
   if self.stop.wait(.2):
    if drain:break
    drain=True
 def __enter__(self):self.thread.start();return self
 def __exit__(self,*unused):self.stop.set();self.thread.join(timeout=5);need(not self.thread.is_alive(),'Progress thread stopped')

class Backups:
 def __init__(self,root,durable,interval=60):
  need(type(interval)in(int,float)and 1<=interval<=300,'Bounded live backup interval')
  self.root,self.durable,self.interval=Path(root),Path(durable),interval;self.stop=threading.Event();self.error=None;self.thread=threading.Thread(target=self.loop,daemon=True)
 def copy(self):
  for p in self.root.rglob('*'):
   ordinary(p)
   if not p.is_file()or p.stat().st_size>16*MIB:continue
   rel=p.relative_to(self.root)
   if any(x in rel.parts for x in ('capsule','source','epoch','provenance','imports')):continue
   if p.suffix not in ('.json','.jsonl','.txt','.log'):continue
   dest=self.durable/'live'/rel;dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_name(dest.name+'.pending');shutil.copyfile(p,tmp);tmp.replace(dest)
 def loop(self):
  while not self.stop.wait(self.interval):
   try:self.copy()
   except Exception as error:self.error=type(error).__name__+': '+str(error)
 def start(self):self.thread.start()
 def close(self):
  self.stop.set();self.thread.join(timeout=30);need(not self.thread.is_alive(),'Backup thread stopped');self.copy()
  if self.error:raise OSError(self.error)

def final_bundle(root,durable,fallback,status):
 """Always attempt a local error ZIP when Drive cannot accept the bundle."""
 root=Path(root);atomic_json(root/'SESSION_RESULT.json',status)
 try:return str(bundle(root,durable))
 except Exception as error:
  status.update(state='INCOMPLETE',synchronization_error=type(error).__name__+': '+str(error))
  atomic_json(root/'SESSION_RESULT.json',status);return str(bundle(root,fallback))
