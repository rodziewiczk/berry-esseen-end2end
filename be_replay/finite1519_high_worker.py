"""Pinned stdlib transport for two genuine unchanged compensated-HIGH children.

No numerical module is imported by this launcher. The real child runs only in
Colab under the external BASIC process-group guard. Capture metadata is a new
explicit execution epoch, never a historical Windows/native receipt.
"""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,threading,time
from pathlib import Path,PurePosixPath
NATIVE='work/cutoff15_20261017/root/cancellation_high_v1'
RUNS='runs/cutoff15_20261017/root'
PLAN='abf04db779c5b58688381fd8894ef8e0fa7cf94ebf9f806fe713ec1c5b628664'
LIMIT=16*1024*1024

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def unique(rows):
 d={}
 for k,v in rows:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def read(p):return json.loads(Path(p).read_text('utf-8'),object_pairs_hook=unique,parse_constant=lambda v:(_ for _ in()).throw(ValueError('Nonfinite JSON')))
def dump(p,d):Path(p).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode())
def source_check(task):
 m=read(task/'SOURCES.json');need(m['source_plan_sha256']==PLAN and m['schema']=='SEALED_ORIGINAL_COMPENSATED_HIGH15_19_INPUTS_V1','Exact explicit HIGH execution source epoch')
 for name,pin in m['sources'].items():
  q=PurePosixPath(name);need(type(name)is str and q.as_posix()==name and not q.is_absolute()and not set(q.parts)&{'..','.'},'Safe original source path')
  p=task/'capsule'/name;need(not p.is_symlink()and p.is_file()and sha(p)==pin,'Every original runtime input byte')
 return m

def run(task,action):
 need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary -B worker')
 need(sys.platform=='linux'and action in('construct','replay'),'Actual Linux original HIGH child')
 task=Path(task).resolve();source_check(task);c=task/'capsule';n=c/NATIVE
 capture=c/RUNS/('cancellation_high_'+action+'01');need(not capture.exists(),'Exclusive fresh current capture');capture.mkdir(parents=True)
 result=capture/'RESULT.json';command=[sys.executable,'-B','bound.py',str(result)]
 inputs={name:sha(n/name)for name in('MANIFEST.json','bound.py','kernel.py','universal.py')}
 started=time.monotonic();process=None;errors=[];threads=[]
 try:
  process=subprocess.Popen(command,cwd=n,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  def pump(kind,pipe,forward):
   total=0
   try:
    with(capture/(kind+'.txt')).open('xb')as out:
     while block:=pipe.read1(65536):
      total+=len(block);need(total<=LIMIT,'Bounded real child stream');out.write(block);out.flush();forward.write(block);forward.flush()
   except BaseException as error:
    errors.append(type(error).__name__+': '+str(error));process.terminate()
   finally:pipe.close()
  for kind,pipe,forward in(('stdout',process.stdout,sys.stdout.buffer),('stderr',process.stderr,sys.stderr.buffer)):
   thread=threading.Thread(target=pump,args=(kind,pipe,forward));thread.start();threads.append(thread)
  code=process.wait()
  for thread in threads:thread.join(timeout=10);need(not thread.is_alive(),'Stopped bounded original child stream pump')
  need(not errors,'Actual child stream capture failure: '+str(errors));source_check(task)
  metadata=dict(schema='CURRENT_REAL_CHILD_COMPENSATED_HIGH_CAPTURE_V1',command=command,cwd=str(n),input_sha256=inputs,
   python=sys.version,returncode=code,elapsed_seconds=time.monotonic()-started,stdout_sha256=sha(capture/'stdout.txt'),
   stderr_sha256=sha(capture/'stderr.txt'),result_sha256=sha(result)if result.is_file()else None,
   outer_launch_sha256=sha(task/'executions'/action/'launch.json'),
   scope='Genuine original child under outer BASIC process-group supervision; not historical/native acceptance',proof_accepted=False)
  dump(capture/'metadata.json',metadata);need(type(code)is int and code==0,'Original HIGH child failed');return code
 finally:
  if process is not None and process.poll()is None:
   process.terminate()
   try:process.wait(timeout=5)
   except subprocess.TimeoutExpired:process.kill();process.wait()
  for thread in threads:thread.join(timeout=5)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--task',type=Path,required=True);p.add_argument('--action',choices=('construct','replay'),required=True);a=p.parse_args()
 raise SystemExit(run(a.task,a.action))
