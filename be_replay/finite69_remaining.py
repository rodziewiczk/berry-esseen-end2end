"""All19 remaining65 producer calls, with genuine captures and full readers.

Each complete original family is a cache transaction. The23h limits apply to
each invocation. An interrupted transaction is retained in the session ZIP,
but never resumed as accepted numerical state. No heavy oracle runs on import.
"""
from pathlib import Path,PureWindowsPath,PurePosixPath
from fractions import Fraction as F
from copy import deepcopy
import ast,json,math,os,re,shutil,sys
from . import finite69_join_sources as src,action_supervisor as supervisor,delivery_transport as tx
from .finite1039_count_evidence import same,mapped,terminal
from .colab_batch import atomic_json,event,utc
CPU_SECONDS=WALL_SECONDS=82800
MEMORY_BYTES=2048*src.MIB
DISK_BYTES=2048*src.MIB
LOG_BYTES=32*src.MIB
FALSE=dict(global_proof_accepted=False,all_index_conclusion_verified=False,analytic_premises_acquired=False)
def implementation():
 return {n:src.digest(src.ROOT/'be_replay'/n)for n in('finite69_remaining.py','finite69_join_sources.py',
  'action_supervisor.py','delivery_transport.py')}|dict(source_plan_sha256=src.PLAN_SHA256)
def value_context(r,report):
 return {'python':report['python_executable'],'capsule':original(r,'')}
def argv(r,a,report):return [s.format(**value_context(r,report))for s in a['argv']]
def originating(r,*parts):
 root=r['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
 src.need(cls(root).is_absolute(),'One original absolute execution context')
 return str(cls(root).joinpath(*parts))

def original(r,path):return originating(r,'capsule',path)if path else originating(r,'capsule')
def guard_scope():
 return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
  per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,
  aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
  sampled_group_CPU_includes_waited_descendants=True,sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,
  descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
def finite(x):src.need(type(x)in(int,float)and math.isfinite(x)and x>=0,'Finite nonnegative execution observation')
def transport(task,r,a,item,report):
 task=Path(task);o=item['observed'];d=task/'executions'/a['id'];origin=r['original_task_root']
 src.need(same(src.read(d/'supervisor-result.json'),o)and o['status']=='completed'and type(o['returncode'])is int
  and o['returncode']==0 and o['reason']is None and o['mode']=='untrusted_search'and o['proof_accepted']is False
  and type(o['sample_count'])is int and o['sample_count']>0 and same(o['guard_scope'],guard_scope()),'Whole actual successful stopped original execution')
 for n in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(o[n])
 launch=src.read(d/'launch.json');cwd=task/'capsule'/a['cwd']
 expected=dict(argv=argv(r,a,report),cwd=original(r,a['cwd']),output_dir=originating(r,'executions',a['id']),
  mode='untrusted_search',wall_seconds=float(WALL_SECONDS),cpu_seconds=CPU_SECONDS,memory_bytes=MEMORY_BYTES,
  disk_bytes=DISK_BYTES,log_bytes=LOG_BYTES,sample_seconds=.2,heartbeat_seconds=20.,
  checkpoint_paths=[original(r,p)for p in a['outputs']])
 src.need(same(launch,expected),'Exact original command, cwd and independent23h action budget')
 for stream in('stdout','stderr'):
  p=mapped(task,o[stream+'_path'],origin)
  src.need(p==d/(stream+'.txt')and p.stat().st_size<=LOG_BYTES and src.digest(p)==o[stream+'_sha256'],'Actual complete original '+stream)
 src.need((d/'stderr.txt').stat().st_size==0,'Successful original stderr must be empty')
 src.need(type(o['checkpoints'])is list and len(o['checkpoints'])==len(a['outputs']),'Every stopped complete output')
 for packet,name in zip(o['checkpoints'],a['outputs']):
  p=task/'capsule'/name;copy=d/'checkpoints'/p.relative_to(cwd)
  src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}and packet['exists']is True
   and packet['trusted_certificate']is False and mapped(task,packet['source_path'],origin)==p
   and mapped(task,packet['path'],origin)==copy and type(packet['bytes'])is int
   and packet['bytes']==p.stat().st_size==copy.stat().st_size and packet['sha256']==src.digest(p)==src.digest(copy),
   'Entire stopped native output: '+name)
 return (d/'stdout.txt').read_text('utf-8')
def capture_metadata(task,r,a,item,report):
 """Truthful new metadata, derived only from an actual stopped native call."""
 s=src.plan()['stages'][r['stage']];prefix=s['native']+'/';c=Path(task)/'capsule';o=item['observed']
 pins={n[len(prefix):]:p for n,p in r['sources'].items()if n.startswith(prefix)}
 if s['kind']=='support'and a['id']=='replay':pins['CONSTRUCTED.json']=src.digest(c/s['native']/'CONSTRUCTED.json')
 return dict(schema='ACTUAL_STOPPED_COMPLETE65_ORIGINAL_CAPTURE_V1',command=argv(r,a,report),cwd=original(r,a['cwd']),
  input_sha256=pins,python=report['python_version'],returncode=o['returncode'],changed_inputs=[],
  started_utc=item['started_utc'],finished_utc=item['finished_utc'],elapsed_seconds=o['elapsed_seconds'],
  stdout_sha256=o['stdout_sha256'],stderr_sha256=o['stderr_sha256'],
  supervisor_result_sha256=src.digest(Path(task)/'executions'/a['id']/'supervisor-result.json'),proof_accepted=False)
def graph(c,packet,expected=None):
 g=packet['files_sha256'];src.need(type(g)is dict and bool(g),'Whole nonempty original source/capture graph')
 if expected is not None:src.need(same(g,expected),'Exact complete original dependency graph')
 for n,pin in g.items():src.parts(n);src.need(src.digest(Path(c)/n)==pin,'Every actual source or capture graph byte')
 return g
def no_times(x):
 if type(x)is dict:return {k:no_times(v)for k,v in x.items()if k!='seconds'}
 if type(x)is list:return [no_times(v)for v in x]
 return x
def namespace(path):
 """Pinned independent parsing/coverage reader; no quadrature oracle imports."""
 tree=ast.parse(Path(path).read_bytes());allowed={'__future__','copy','json','math','sys','fractions','hashlib','pathlib','collections'}
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):src.need(all(n.name in allowed for n in node.names),'Only stdlib independent reader imports')
  if isinstance(node,ast.ImportFrom):src.need(node.module in allowed,'Only stdlib independent reader imports')
 ns=dict(__file__=str(path),__name__='complete65_pure_independent_readback')
 exec(compile(tree,str(path),'exec'),ns);return ns
def inner(task,r,s,a,report,stdout):
 c=Path(task)/'capsule';label=a['id']+'01';d=c/s['runs']/label;m=src.read(d/'metadata.json')
 file='PLAN.json'if a['id']=='plan'else'RESULT.json';p=d/file
 manifest=src.read(c/s['native']/'MANIFEST.json');pins=dict(manifest['files_sha256'])
 pins[s['native']+'/MANIFEST.json']=src.digest(c/s['native']/'MANIFEST.json')
 cmd=[report['python_executable'],'-B','planner.py',original(r,s['runs']+'/plan01/PLAN.json')]
 if a['id']!='plan':
  pins[s['runs']+'/plan01/PLAN.json']=src.digest(c/s['runs']/'plan01/PLAN.json')
  cmd=[report['python_executable'],'-B','protocol.py',a['id'],original(r,s['runs']+'/plan01/PLAN.json'),original(r,s['runs']+'/'+label+'/RESULT.json')]
 src.need(m['command']==cmd and m['cwd']==original(r,s['native'])and same(m['input_sha256'],pins)
  and type(m['returncode'])is int and m['returncode']==0 and m['changed_inputs']==[]and m[file+'_sha256']==src.digest(p)
  and m['python']==report['python_version'],'Actual whole original run.py child capture')
 finite(m['elapsed_seconds'])
 for n in('stdout','stderr'):src.need(src.digest(d/(n+'.txt'))==m[n+'_sha256'],'Original child stream SHA')
 src.need(not(d/'stderr.txt').read_bytes()and(d/'stdout.txt').read_text('utf-8')==stdout,'Whole original inner/outer streams')
 return src.read(p,128*src.MIB)
def fourier_summary(task,r,s,report,stdout):
 c=Path(task)/'capsule';p,construct,replay=[inner(task,r,s,a,report,stdout[a['id']])for a in s['actions'][:3]]
 src.need(same(no_times(construct),no_times(replay)),'Every original construction/replay field')
 ns=namespace(c/s['audit']/'readback.py');plan_pin=src.digest(c/s['runs']/'plan01/PLAN.json');manifest=src.digest(c/s['native']/'MANIFEST.json')
 args=[plan_pin,manifest]+([]if r['stage']=='auxiliary'else[r['stage']])
 maxima=ns['validate_result'](construct,p,*args)
 src.need(ns['validate_result'](replay,p,*args)==maxima,'Entire independently revalidated exact native replay')
 controls=ns['controls'](p,construct,*args)
 need_fields=['status','mathematical_status','execution_status','n','negative_controls','actual_support_acquired','cutoff6_proved']
 actual=src.read(c/s['result'],128*src.MIB);ref=s['reference']
 src.need(actual.keys()==ref.keys()and same({n:actual[n]for n in need_fields},{n:ref[n]for n in need_fields})
  and actual['negative_controls']==controls,'Full original independent theorem/controls/domain')
 if r['stage']=='auxiliary':
  expected=deepcopy(ref);expected.update(strips=len(p['strips']),exact_rows=len(construct['rows']),attempts=len(construct['attempts']),
   per_n_upper={n:str(v)for n,v in maxima.items()},uniform_upper=str(max(maxima.values())))
 else:
  expected=deepcopy(ref);expected.update(strips=len(ns['plan_rows'](p,r['stage'])),exact_rows=len(construct['rows']),
   attempts=len(construct['attempts']),per_band_per_n_upper={b:{n:str(v)for n,v in vals.items()}for b,vals in maxima.items()})
 expected.pop('files_sha256');src.need(same({k:v for k,v in actual.items()if k!='files_sha256'},expected),'Every fresh independent readback field')
 g=dict(src.read(c/s['native']/'MANIFEST.json')['files_sha256'])
 for n in[s['native']+'/MANIFEST.json',s['runs']+'/plan01/PLAN.json',s['request'],s['audit']+'/readback.py',s['audit']+'/REVIEW.txt']+sum([a['outputs']for a in s['actions'][1:3]],[]):g[n]=src.digest(c/n)
 graph(c,actual,g);src.need(same(terminal(stdout['readback']),expected),'Actual independent original readback stdout')
 src.need(same(src.read(c/s['request']),src.request(task)),'Only current real capture identities in the request')
 return actual
def high_summary(task,r,s,report,stdout):
 c=Path(task)/'capsule';actual=src.read(c/s['result']);expected={k:v for k,v in s['reference'].items()if k!='files_sha256'}
 src.need(same({k:v for k,v in actual.items()if k!='files_sha256'},expected),'Every original12 HIGH rows and all original controls')
 for n,ref in s['output_references'].items():src.need(same(src.read(c/n),ref),'Whole deterministic original HIGH output')
 src.need((c/s['native']/'RESULT.json').read_bytes()==(c/s['native']/'REPLAY_RESULT.json').read_bytes(),'Byte-identical full HIGH replay')
 g=dict(src.read(c/s['native']/'MANIFEST.json')['files_sha256'])
 for n in [s['native']+'/MANIFEST.json',s['native']+'/RESULT.json',s['native']+'/REPLAY_RESULT.json',s['audit']+'/check.py',s['audit']+'/REVIEW.txt']:
  g[n]=src.digest(c/n)
 for n in ('bound.py','kernel.py','universal.py'):
  dest=s['audit']+'/engine/'+n;src.need((c/dest).read_bytes()==(c/s['native']/n).read_bytes(),'Exact copied HIGH numerical helper');g[dest]=src.digest(c/dest)
 for a,item in zip(s['actions'],report['actions']):
  if 'capture'not in a:continue
  dest=c/a['capture'];src.need(same(src.read(dest/'metadata.json'),capture_metadata(task,r,a,item,report)),'Both genuine HIGH metadata captures')
  for name in('metadata.json','stdout.txt','stderr.txt'):
   path=a['capture']+'/'+name;g[path]=src.digest(c/path)
  for stream in('stdout','stderr'):src.need((dest/(stream+'.txt')).read_bytes()==(Path(task)/'executions'/a['id']/(stream+'.txt')).read_bytes(),'Whole genuine HIGH streams')
 graph(c,actual,g);src.need(same(terminal(stdout['readback']),{k:v for k,v in expected.items()if k not in('rows','cell_tests')}),'Complete actual HIGH independent terminal')
 return actual
def support_summary(task,r,s,report,stdout):
 c=Path(task)/'capsule';refs=s['output_references'];construction=src.read(c/s['native']/'CONSTRUCTED.json',128*src.MIB)
 replay=src.read(c/s['native']/'REPLAY_CHECKED.json',128*src.MIB)
 # All36 complete two-ray proofs are deterministic original data. Only the
 # separately validated current Fourier maxima and their graph may differ.
 for n,ref in refs.items():
  actual=src.read(c/n,128*src.MIB);ignored={'seconds','files_sha256','fourier_interfaces','construction_sha256'}
  src.need(same({k:v for k,v in actual.items()if k not in ignored},{k:v for k,v in ref.items()if k not in ignored}),
   'All original support proof rows, equality scalars and native19 controls')
  if 'seconds'in actual:finite(actual['seconds'])
 src.need(replay['construction_sha256']==src.digest(c/s['native']/'CONSTRUCTED.json'),'Current native construction is actual replay input')
 fourier={}
 for key,path in [('auxiliary','work/cutoff6_20261018/audit/auxiliary5_readback_v1/RESULT.json'),
  ('own','work/cutoff6_20261018/audit/supported_fourier_readback_v1/OWN_RESULT.json'),
  ('bridge','work/cutoff6_20261018/audit/supported_fourier_readback_v1/BRIDGE_RESULT.json'),
  ('radius','work/cutoff6_20261018/audit/supported_fourier_readback_v1/RADIUS_RESULT.json')]:fourier[key]=src.read(c/path)
 joins=[];g=src.read(c/s['native']/'SOURCES.json')
 for n in[s['native']+'/'+x for x in('SOURCES.json','protocol.py','PROOF.txt')]:g[n]=src.digest(c/n)
 for key,packet in fourier.items():
  for n,pin in graph(c,packet).items():src.need(n not in g or g[n]==pin,'Consistent current acquisition graph');g[n]=pin
  n=('work/cutoff6_20261018/audit/auxiliary5_readback_v1/RESULT.json'if key=='auxiliary'else
   'work/cutoff6_20261018/audit/supported_fourier_readback_v1/'+key.upper()+'_RESULT.json');g[n]=src.digest(c/n)
 for row in construction['rows']:
  n,name=row['n'],row['region'];kind='own'if name in('B0','BN','B2')else'bridge'if name=='bridge'else'radius'
  band=('BC'if name=='B2'else name)if kind=='own'else'BH_BRIDGE'if kind=='bridge'else name
  packet=fourier[kind];entry=next(v for v in packet['bands']if v['name']==band)
  cap=packet['per_band_per_n_upper'][band][str(n)];target=({'B0':'423/1000','BN':'209/500','B2':'83/200'}[name]if kind=='own'else'4097/10000')
  src.need(F(entry['rho'][0])<=F(row['rho'][0])<F(row['rho'][1])<=F(entry['rho'][1])
   and F(row['radius'])<=F(entry['support_absolute_upper'])and F(cap)<F(target),'Same literal n, closed rho and support licence')
  joins.append(dict(n=n,region=name,support=row['radius'],rho=row['rho'],fourier_upper=cap,target=target))
 src.need(same(construction['fourier_interfaces'],joins)and same(replay['fourier_interfaces'],joins),'All36 actual same-law Fourier interfaces')
 graph(c,construction,g);graph(c,replay,g)
 for a,item in zip(s['actions'],report['actions']):
  if 'capture'not in a:continue
  d=c/a['capture'];meta=src.read(d/'metadata.json')
  src.need(same(meta,capture_metadata(task,r,a,item,report)),'Support metadata is derived from actual stopped execution')
  for stream in('stdout','stderr'):src.need((d/(stream+'.txt')).read_bytes()==(Path(task)/'executions'/a['id']/(stream+'.txt')).read_bytes(),'Whole genuine copied support stream')
  lines=['SUPPORT '+str(v['n'])+' '+v['region']+' PASS'for v in construction['rows']]
  lines.append((construction if a['id']=='construct'else replay)['status'])
  src.need(stdout[a['id']].splitlines()==lines,'Every actual support target progress line')
 actual=src.read(c/s['result']);expected={k:v for k,v in s['reference'].items()if k!='files_sha256'}
 src.need(same({k:v for k,v in actual.items()if k!='files_sha256'},expected),'Entire independent72-ray support receipt and24controls')
 # The original independent reader adds every parsed source, both captures,
 # construction/replay, equality and its source copy to the native graph.
 native_ref=refs[s['native']+'/CONSTRUCTED.json']['files_sha256']
 for n in set(s['reference']['files_sha256'])-set(native_ref):
  g[n]=src.digest(c/n)
 graph(c,actual,g);src.need(same(terminal(stdout['readback']),expected),'Actual independent support readback terminal')
 return actual
def validate_run(task,report):
 task=Path(task);r=src.verify(task);s=src.plan()['stages'][r['stage']]
 src.need(report['schema']=='OBSERVED_COMPLETE65_ORIGINAL_STAGE_V1'and report['original_task_root']==r['original_task_root']
  and report['stage']==r['stage']and same(report['implementation'],implementation())
  and [x['action']for x in report['actions']]==[a['id']for a in s['actions']]
  and all(report[k]is False for k in FALSE),'Exact full action list and unaccepted observed ledger')
 stdout={a['id']:transport(task,r,a,item,report)for a,item in zip(s['actions'],report['actions'])}
 return {'fourier':fourier_summary,'high':high_summary,'support':support_summary}[s['kind']](task,r,s,report,stdout)
def validate_completed(task):
 task=Path(task);p=src.read(task/'STAGE_COMPLETED.json',128*src.MIB);report=src.read(task/'STAGE_OBSERVED.json');result=validate_run(task,report)
 src.need(p['schema']=='COMPLETED_COMPLETE65_ORIGINAL_STAGE_V1'and p['arithmetic_completed']is True
  and all(p[k]is False for k in FALSE)and p['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
  and same(p['summary'],result)and same(p['artifacts'],tx.inventory(task,omit=('STAGE_COMPLETED.json',))),
  'Entire completed stage, source/capture/original output inventory')
 return dict(stage=report['stage'],summary=result,stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),arithmetic_completed=True,**FALSE)
def execute(cache,task,stage,*,root,parents=()):
 r=src.prepare(cache,task,stage,parents);task=Path(task);s=src.plan()['stages'][stage]
 for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[n]='1'
 report=dict(schema='OBSERVED_COMPLETE65_ORIGINAL_STAGE_V1',stage=stage,original_task_root=r['original_task_root'],
  python_executable=sys.executable,python_version=sys.version,implementation=implementation(),actions=[],**FALSE)
 for a in s['actions']:
  src.verify(task)
  if a['id']=='readback'and s['kind']=='fourier':atomic_json(task/'capsule'/s['request'],src.request(task))
  src.need(all(not(task/'capsule'/p).exists()for p in a['outputs']),'Only genuinely fresh native outputs')
  start=utc();event(root,'finite69_original_action_started',stage=stage,action=a['id'],cpu_seconds=CPU_SECONDS,
   wall_seconds=WALL_SECONDS,budget_scope='each action; no shared family or batch deadline')
  d=task/'executions'/a['id']
  with tx.Follow(root,d,stage+':'+a['id']):
   observed=supervisor.run(argv(r,a,report),cwd=task/'capsule'/a['cwd'],output_dir=d,mode='untrusted_search',
    cpu_seconds=CPU_SECONDS,wall_seconds=WALL_SECONDS,memory_bytes=MEMORY_BYTES,disk_bytes=DISK_BYTES,
    log_bytes=LOG_BYTES,sample_seconds=.2,heartbeat_seconds=20,checkpoint_paths=[task/'capsule'/p for p in a['outputs']])
  item=dict(action=a['id'],observed=observed,started_utc=start,finished_utc=utc());report['actions'].append(item)
  atomic_json(task/'ACTIONS_PARTIAL.json',report);transport(task,r,a,item,report)
  if 'capture'in a:
   dest=task/'capsule'/a['capture'];dest.mkdir(parents=True,exist_ok=False)
   for n in('stdout','stderr'):shutil.copyfile(d/(n+'.txt'),dest/(n+'.txt'))
   atomic_json(dest/'metadata.json',capture_metadata(task,r,a,item,report))
  src.verify(task);event(root,'finite69_original_action_completed',stage=stage,action=a['id'])
 atomic_json(task/'STAGE_OBSERVED.json',report);summary=validate_run(task,report)
 atomic_json(task/'STAGE_COMPLETED.json',dict(schema='COMPLETED_COMPLETE65_ORIGINAL_STAGE_V1',arithmetic_completed=True,
  observed_sha256=src.digest(task/'STAGE_OBSERVED.json'),summary=summary,artifacts=tx.inventory(task),**FALSE))
 return validate_completed(task)
