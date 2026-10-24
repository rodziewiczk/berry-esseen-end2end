"""Source-only enumeration of complete selected cutoff43/global40 routes.

This reads archived source ASTs, metadata and JSON only. It never imports an
original mathematical program. Current capture epochs still require an
implementation; historical records in this inventory are never fresh evidence.
"""
import argparse,ast,hashlib,json,posixpath,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RELEASE='BE_cutoff35_release_20261007/work/cutoff40_release_20261007/'
WORK=RELEASE+'work/toward40_20261007/'
AUDIT=WORK+'audit43/'
CAP=AUDIT+'capsule/'
RUN=RELEASE+'runs/toward40_20261007/'
CLOSURE_SHA='68eb555e08ee7509f9d136df6fae5e354aff816ec4f77cc8426698c479b205a0'
CLOSURE_BYTES=135288952
OLD_SHA='17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb'
OLD_BYTES=514958998

def need(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as f:
  while b:=f.read(1024**2):h.update(b)
 return h.hexdigest()
def dump(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def final_json(text):
 decoder=json.JSONDecoder()
 for i in reversed([i for i,c in enumerate(text)if c=='{'and(i==0 or text[i-1]=='\n')]):
  try:v,n=decoder.raw_decode(text[i:])
  except ValueError:continue
  if type(v)is dict and not text[i+n:].strip():return v
 raise ValueError('No complete original final JSON object')
def literal(raw,name):
 return ast.literal_eval(next(n.value for n in ast.parse(raw).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)))

def build(closure,old_archive=None):
 closure=Path(closure);need(closure.stat().st_size==CLOSURE_BYTES and digest(closure)==CLOSURE_SHA,'Exact complete closure31 source transport')
 with zipfile.ZipFile(closure)as z:
  names=set(z.namelist());read=lambda p:json.loads(z.read(p))
  manifest_raw=z.read(CAP+'CHECKSUMS.json');manifest=json.loads(manifest_raw)
  need(sha(manifest_raw)=='9bf2f27565ec33623c3be9368422f54fc8424aa3361f51bba5f115bd5d7a1a69'and len(manifest['files'])==1825,'Exact full retained44 capsule')
  files={}
  for row in manifest['files']:
   member=CAP+row['path'];raw=z.read(member);need(len(raw)==row['bytes']and sha(raw)==row['sha256'],'Every original1825 capsule input byte')
   files[member]=dict(bytes=len(raw),sha256=sha(raw))
  for member in sorted(n for n in names if n.startswith(AUDIT)and'/'not in n[len(AUDIT):]and n.endswith('.py')):
   raw=z.read(member);files[member]=dict(bytes=len(raw),sha256=sha(raw))
  source_records={};actions={}
  def original_relative(value):
   if '/work/toward40_20261007'in value:return 'work/toward40_20261007'+value.split('/work/toward40_20261007',1)[1]
   if '/work/below49_20261006'in value:return 'work/toward40_20261007/audit43/capsule/work/below49_20261006'+value.split('/work/below49_20261006',1)[1]
   raise ValueError('Unknown original selected workspace prefix')
  def source(member):
   raw=z.read(member);source_records[member]=dict(bytes=len(raw),sha256=sha(raw));return raw
  def from_capture(key,folder):
   m=read(folder+'metadata.json');stdout=z.read(folder+'stdout.txt');stderr=z.read(folder+'stderr.txt')
   need(type(m['returncode'])is int and m['returncode']==0 and not stderr and sha(stdout)==m['stdout_sha256']and sha(stderr)==m['stderr_sha256'],'Complete original reference capture only')
   cwd=original_relative(m['cwd'])
   argv=[a for a in m['command'][1:]if a!='-B'];entry=argv[0]
   if entry.startswith('/'):entry=original_relative(entry)
   else:entry=posixpath.normpath(cwd+'/'+entry)
   member=RELEASE+entry;raw=source(member);text=stdout.decode('utf-8')
   try:result=final_json(text);rule=dict(kind='whole_typed_final_json',expected=result)
   except ValueError:rule=dict(kind='exact_terminal',terminal=text.rstrip().splitlines()[-1])
   actions[key]=dict(id=key,cwd=cwd,script=entry,arguments=argv[1:],source_member=member,script_sha256=sha(raw),stdout_rule=rule,
    reference_capture={k:dict(member=folder+k,sha256=sha(z.read(folder+k)))for k in('metadata.json','stdout.txt','stderr.txt')},
    original_snapshot_rows=len(m.get('input_sha256',{})),historical_capture_is_fresh_evidence=False)
   return key
  bsource=source(CAP+'work/below49_20261006/entry/cutoff44/bind_ready_edges44.py')
  jobs=literal(bsource,'JOBS')
  extras=[('local/left42_source_bind01','PASS_EXACT_LEFT42_ACTUAL_RESOURCE_INTERFACE'),('local/left42_mid_exact01','PASS_EXACT_CONDITIONAL_LEFT42_SIGNED_PHASE_MID'),('local/left42_low_accept01','PASS_FRESH_EXACT_REPLAY'),('package_audit/left42_accept02',None),('package_audit/left42_confinement_accept01',None),('package_audit/left42_profiles_accept01',None)]
  a61=[]
  for run,_ in jobs+extras:
   key='44.'+run;from_capture(key,CAP+'runs/below49_20261006/'+run+'/');a61.append(key)
  b61=[]
  for label in('anchor_support01','anchor_accept01','initial_support01','scalar01','left_fixed01','central_fixed01'):
   key='43.'+label;from_capture(key,RUN+'audit43/'+label+'/');b61.append(key)
  native62={}
  def capture62(run):
   run=run.removeprefix('runs/toward40_20261007/');key='40.'+run
   if key not in actions:from_capture(key,RUN+run+'/')
   native62[run]=key;return key
  early=read(WORK+'entry/early_ceiling_evidence.json');single=read(WORK+'entry/single39_evidence.json')
  early_ids=[capture62('entry/'+r['run'])for r in early['selected']]
  single_ids=[capture62('entry/'+r['run'])for r in single['selected']]
  core_ids=[capture62('root/'+n)for n in('support_chain01','initial40_accept01')]
  for folder,runs in(('left40_accept',('acquisition_accept02','confinement_accept01','profile_accept01','interface_accept01')),('central40',('acquisition_accept01','confinement_accept01','profile_accept01','interface_accept01'))):
   core_ids +=[capture62(folder+'/'+n)for n in runs]
  left_runs=literal(source(WORK+'local/accept_actual_left40_join_v3.py'),'EXPECTED_RUNS')
  for n in left_runs:capture62(n)
  central_ids=[capture62('root/'+n)for n in('central_low_execute01','central_tiny_accept01','central_mid_accept01','central_low_bind01','binomial_accept02')]
  left_ids=[native62[n.removeprefix('runs/toward40_20261007/')]for n in left_runs if '/local/'in n]
  # Preserve the literal ten-component catalogue too. Its full LEFT MID is
  # deliberately retained in addition to the three selected parallel parts.
  full_mid='40.left40_full_mid';member=WORK+'local/actual_left40_final/accept_mid40.py';raw=source(member)
  actions[full_mid]=dict(id=full_mid,cwd='work/toward40_20261007/local/actual_left40_final',script='work/toward40_20261007/local/actual_left40_final/accept_mid40.py',
   arguments=[],source_member=member,script_sha256=sha(raw),stdout_rule=dict(kind='original_full_mid_acceptance',status='PASS_EXACT_FINITE_LEFT40_42_SIGNED_PHASE_MID'),
   historical_capture_is_fresh_evidence=False,reason='Conservative preservation of the literal ten-component catalogue; no unverified substitution of partition receipts')
  left_ids.append(full_mid)
  global_member=WORK+'root/global40/accept_cutoff40_join.py';components=literal(source(global_member),'COMPONENTS')
  binders=[]
  for key,relative,status in components:
   member=WORK+relative;raw=source(member);binders.append(dict(id=key,cwd='work/toward40_20261007/'+str(Path(relative).parent).replace('\\','/'),source_member=member,script=relative,arguments=[],script_sha256=sha(raw),expected_status=status))
  joins=[CAP+'work/below49_20261006/entry/cutoff44/check_cutoff44_composition.py',AUDIT+'accept_cutoff43_join.py',global_member]
  for p in joins:source(p)
  parent_graph=read('continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json')['files_sha256']
  missing=[p for p in parent_graph if p not in names]
  need(not missing,'Every original9518 source/candidate/record member physically supplied')
  if old_archive is not None:
   old_archive=Path(old_archive);need(old_archive.stat().st_size==OLD_BYTES and digest(old_archive)==OLD_SHA,'Exact public old source asset')
   with zipfile.ZipFile(old_archive)as old:
    for member,row in {**files,**source_records}.items():
     raw=old.read('cutoff25_20261011/'+member);need(len(raw)==row['bytes']and sha(raw)==row['sha256'],'Exact public old-archive source alias')
  packages={
   '61A':dict(name='cutoff44_complete_components',actions=a61,standalone_native_calls=25),
   '61B':dict(name='cutoff43_six_complete_scopes',actions=b61,standalone_native_calls=6),
   '61C':dict(name='cutoff44_cutoff43_current_capture_joins',source_members=joins[:2],standalone_native_calls=2,requires=['61A','61B','actual_completed12']),
   '62A':dict(name='early36_40_ceilings_support',actions=early_ids,standalone_native_calls=12),
   '62B':dict(name='single39_complete_positive_barrier',actions=single_ids,standalone_native_calls=9,requires=['62A']),
   '62C':dict(name='initial40_left_central_acquisition',actions=core_ids,standalone_native_calls=10),
   '62D':dict(name='central40_comparison_full_low_binomial',actions=central_ids,standalone_native_calls=5,requires=['62C']),
   '62E':dict(name='left40_comparison_full_low_mid',actions=left_ids,standalone_native_calls=11,requires=['62C']),
   '62F':dict(name='global40_nine_binders_current_capture_join',source_members=[global_member],standalone_native_calls=1,nested_component_calls=9,nested_single39_calls=2,
      component_bindings=binders,requires=['61C','62A','62B','62C','62D','62E'])}
  need([packages[p]['standalone_native_calls']for p in packages]==[25,6,2,12,9,10,5,11,1],'Closed proposed partition')
  low=[]
  for key in(a61[16],next(k for k in a61 if k.endswith('local/left42_low_accept01'))):
   r=actions[key];v=r['stdout_rule']['expected'];need(r['arguments']==['--replay'],'Mandatory complete LOW evaluator switch')
   low.append(dict(action=key,rows=v['rows'],strict_gates=v['strict_gates'],negative_controls=v['negative_controls'],full_original_evaluate_replay=True))
  source_tree={'files':files,'selected_sources':source_records}
  return dict(schema='FINITE4348_AND_GLOBAL40_REQUIRED_NATIVE_ACTION_PLAN_V1',source_only=True,arithmetic_computed=False,
   original_mathematical_modules_imported_or_evaluated=False,all_index_conclusion_verified=False,
   original_transport=dict(name='closure31.zip',bytes=CLOSURE_BYTES,sha256=CLOSURE_SHA),
   public_source_asset=dict(name='cutoff25_20261011.zip',bytes=OLD_BYTES,sha256=OLD_SHA,url='https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/download/cutoff20-sources-2026-10-17/cutoff25_20261011.zip',member_prefix='cutoff25_20261011/'),
   source_tree=source_tree,retained44_capsule=dict(files=1825,bytes=61214940,manifest_member=CAP+'CHECKSUMS.json',manifest_sha256=sha(manifest_raw),all1825_byte_hashes_verified=True),
   full_parent_graph=dict(member='continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json',sha256='33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9',source_files=9518,all_members_physically_present=True,all9518_byte_hashes_freshly_verified=False),
   actions=actions,sections=packages,proposed_notebook_files=2,notebooks_currently_runnable=0,
   ten_literal_component_actions={
    'central40_acquisition':'40.central40/acquisition_accept01','central40_confinement':'40.central40/confinement_accept01','central40_profile':'40.central40/profile_accept01',
    'left40_acquisition':'40.left40_accept/acquisition_accept02','left40_confinement':'40.left40_accept/confinement_accept01','left40_profile':'40.left40_accept/profile_accept01',
    'central40_tiny':'40.root/central_tiny_accept01','central40_mid':'40.root/central_mid_accept01',
    'left40_tiny':'40.local/actual_left40_tiny_accept01','left40_mid':full_mid},
   planned_notebooks={'61':dict(sections=['61A','61B','61C'],standalone_original_calls=33),
    '62':dict(sections=['62A','62B','62C','62D','62E','62F'],standalone_original_calls=48,nested_original_calls=11)},
   session_policy=dict(maximum_session_wall_seconds=82800,stop_between_complete_actions=True,completed_stage_cache=True,partial_numerical_acceptance=False,total_runtime_fit_is_not_measured=True),
   cutoff44_nested_full_LOW=low,
   global40_nested_LOW=dict(central=dict(constructor='40.root/central_low_execute01',binder='40.root/central_low_bind01',signed_rows=70,strict_gates=10894486),
    left=dict(constructors=['40.local/actual_left40_low_execute_'+p+'01'for p in('a','b','c')],binder='40.local/actual_left40_low_bind02',signed_rows_by_part=[18,34,30],total_signed_rows=82),
    single39=dict(action=next(k for k in single_ids if k.endswith('entry/local39_low_accept02')),signed_rows=90,strict_gates=2281144),
    left_MID=dict(part_actions=['40.local/actual_left40_mid_part_'+p+'01'for p in('a','b','c')],binder='40.local/actual_left40_mid_bind01',whole_contexts=5126,extra_full_ten_catalogue_action=full_mid)),
   shared_completed12=dict(numerical_replay_required=False,zip_sha256='51640e38549bf8ebe05e09953622e1f8526063f7a03b2f2c48756b782d17fd63',
    zip_bytes=16921310,top_level_executions=14,retained_components=41,source_manifest_sha256='58a770705c6e0bc500813ed37299753a16f6245ebea6ade238ad98078d7b4e26',
    verify_sha256='766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375',new_jobs_sha256='edb42eef2e7e4110533173cc384ecb94167bf5c312fea8f371916fbdd6f013d6',retained_jobs_sha256='d92f0017fadc5c2f9601de599f2e1f97eb9c1042b02a17a695065c040f09d7ad'),
   remaining_implementation_boundaries=['Genuine current source/launch/capture epochs for31 component calls; historical captures remain provenance only',
    'Explicit metadata-only rebinding of cutoff44/cutoff43 joins; preserve all mathematical functions, domains and original controls',
    'Fresh constructor output slots and capture epochs for both40 LOW families and parallel LEFT MID parts',
    'Explicit source/manifest/capture epochs beneath all nine global40 binders, including new accepted-status files and literal evidence-SHA gates',
    'Public pure full actual12 export reader/import; never rerun its14/41 suite solely to satisfy these parents',
    'Full per-lane current source preparation, Linux process-tree execution, typed stopped evidence and negative infrastructure fixtures'],
   unacquired_mathematical_premises=['Attained positive closed maximizing witness and same-law contact/resource calculus','Published analytic/Fourier/Gaussian inputs and strict Bernoulli theorem','All predecessor, same-witness and final global semantic acquisition joins'])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--closure',type=Path,required=True);p.add_argument('--old-archive',type=Path);p.add_argument('--output',type=Path,default=ROOT/'proof/finite4348_source_action_plan.json');a=p.parse_args()
 d=build(a.closure,a.old_archive);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(dump(d))
 print(json.dumps(dict(sections=9,planned_notebooks=2,actions=len(d['actions']),capsule_byte_verified=1825,source_plan_sha256=digest(a.output))))
