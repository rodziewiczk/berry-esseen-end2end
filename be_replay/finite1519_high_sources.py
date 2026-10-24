"""Sealed original compensated-HIGH sources with one explicit capture epoch."""
from __future__ import annotations
import ast,copy,hashlib,json,re,shutil,time,urllib.request,zipfile
from pathlib import Path
from . import finite1039_sources as base
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite1519_high_source_plan.json'
PLAN_SHA256='abf04db779c5b58688381fd8894ef8e0fa7cf94ebf9f806fe713ec1c5b628664'
SCHEMA='SEALED_ORIGINAL_COMPENSATED_HIGH15_19_INPUTS_V1'
NATIVE='work/cutoff15_20261017/root/cancellation_high_v1'
AUDIT='work/cutoff15_20261017/fourier/cancellation_high_readback_v1'
RUNS='runs/cutoff15_20261017/root'
ACTIONS=('construct','replay','readback')
LABELS={a:'cancellation_high_'+a+'01'for a in('construct','replay')}
FRESH=AUDIT+'/FRESH_CHECK.py'
RESULT=AUDIT+'/CHECKED.json'
WORKER='runtime/finite1519_high_worker.py'
def dump(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def plan():
 need(digest(PLAN)==PLAN_SHA256,'Externally pinned complete compensated-HIGH closure');d=read(PLAN)
 need(d['schema']=='FINITE1519_COMPENSATED_HIGH_SOURCE_PLAN_V1'and len(d['source_files'])==74
  and d['original_manifest_graph_rows']==71 and d['original_numerical_programs_unchanged']is True
  and d['only_derived_capture_hash_dictionary_replaced']is True,'Exact original71-row manifest and new capture-only epoch')
 need(all(d[k]is False for k in('arithmetic_computed','support_acquisition_verified','full_notebook57_completed',
                               'parent_acquisitions_verified','all_index_conclusion_verified')),'Explicit unacquired support/framework premises')
 return d
def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for a in plan()['assets']:
        name=a['name'];need(tuple(parts(name))==(name,),'Pinned source archive basename');p=ordinary(directory/name)
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1519_high_download_started',archive=name,total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source download');target.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1519_high_download',archive=name,bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Actual full source archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact immutable source transport')
        result[name]=p.resolve();progress('finite1519_high_archive_verified',archive=name,bytes=a['bytes'],sha256=a['sha256'])
    return result


def prepare_cache(assets,output, *,progress=lambda *a,**k:None):
    d=plan();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d['assets']:
            p=ordinary(assets[a['name']]);need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned source transport')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[a['name']]=z
        for i,(name,row)in enumerate(d['source_files'].items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                z=opened[row['archive']];info=z.getinfo(row['member']);need(info.file_size==row['bytes'],'Exact selected original input size')
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original input byte')
            if i%20==0:progress('finite1519_high_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()




def output_paths(action):
 need(action in ACTIONS,'One whole compensated-HIGH action')
 if action=='readback':return[RESULT]
 return[RUNS+'/'+LABELS[action]+'/'+n for n in('metadata.json','stdout.txt','stderr.txt','RESULT.json')]
def prepare(cache,task):
 d=plan();task=ordinary(task);need(not task.exists(),'Fresh private compensated-HIGH capsule');task.mkdir(parents=True)
 for name,row in d['source_files'].items():
  p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact original HIGH input bytes')
  out=task/'capsule'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
 dest=task/WORKER;dest.parent.mkdir(parents=True);shutil.copyfile(ROOT/'be_replay/finite1519_high_worker.py',dest)
 m=dict(schema=SCHEMA,original_task_root=str(task.resolve()),source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),worker_sha256=digest(task/WORKER),
  sources={n:r['sha256']for n,r in d['source_files'].items()},original_numerical_sources_unchanged=True,
  explicit_capture_hash_epoch=True,arithmetic_computed=False,full_notebook57_completed=False,
  support_acquisition_verified=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
 (task/'SOURCES.json').write_bytes(dump(m));verify_job(task);return m

def derive_check(original,pins):
 d=plan();need(type(original)is bytes and hashlib.sha256(original).hexdigest()==d['original_readback_sha256'],'Exact frozen original readback bytes')
 need(type(pins)is dict and set(pins)=={'construct','replay'}and all(type(v)is str and re.fullmatch('[0-9a-f]{64}',v)for v in pins.values()),'Both actual current capture metadata hashes')
 text=original.decode('utf-8');tree=ast.parse(text)
 assignments=[n for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='CAPTURE_SHA']
 need(len(assignments)==1,'Exactly one literal top-level CAPTURE_SHA dictionary');value=assignments[0].value
 need(isinstance(value,ast.Dict)and ast.literal_eval(value)==d['original_capture_sha256'],'Exact original two-capture configuration')
 lines=original.splitlines(keepends=True);start=sum(map(len,lines[:value.lineno-1]))+value.col_offset;end=sum(map(len,lines[:value.end_lineno-1]))+value.end_col_offset
 replacement=json.dumps(pins,sort_keys=True,separators=(',',':')).encode('ascii');derived=original[:start]+replacement+original[end:]
 need(derived[:start]+original[start:end]+derived[start+len(replacement):]==original,'Byte-exact inverse of one configuration-value replacement')
 after=ast.parse(derived.decode('utf-8'))
 for module in(tree,after):
  a=[n for n in module.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='CAPTURE_SHA']
  need(len(a)==1,'Unique unchanged configuration target');a[0].value=ast.Constant(value='CAPTURE_CONFIGURATION_ONLY')
 need(ast.dump(tree,include_attributes=False)==ast.dump(after,include_attributes=False),'Complete AST identity except capture-hash dictionary; all mathematical functions unchanged')
 return derived,dict(schema='COMPENSATED_HIGH15_19_ACTUAL_CAPTURE_HASH_EPOCH_V1',original_readback_sha256=d['original_readback_sha256'],
  derived_readback_sha256=hashlib.sha256(derived).hexdigest(),original_capture_sha256=d['original_capture_sha256'],
  actual_capture_sha256=pins,only_top_level_capture_sha_dictionary_changed=True,all_other_bytes_unchanged=True,
  all_mathematical_function_asts_unchanged=True,original_result_sha256=d['original_native_result_sha256'],
  native_arithmetic_accepted=False,full_notebook57_completed=False,all_index_conclusion_verified=False)

def current_derivation(task):
 c=Path(task)/'capsule';pins={a:digest(c/RUNS/LABELS[a]/'metadata.json')for a in('construct','replay')}
 return derive_check((c/AUDIT/'check.py').read_bytes(),pins)
def prepare_readback(task):
 p=Path(task)/'capsule'/FRESH;need(not p.exists()and not(Path(task)/'CAPTURE_EPOCH.json').exists(),'Fresh explicit capture epoch')
 b,report=current_derivation(task);p.write_bytes(b);(Path(task)/'CAPTURE_EPOCH.json').write_bytes(dump(report));return report

def verify_job(task):
 task=ordinary(task);d=plan();m=read(task/'SOURCES.json')
 need(m['schema']==SCHEMA and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
  and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}and m['original_numerical_sources_unchanged']is True
  and m['worker_sha256']==digest(ROOT/'be_replay/finite1519_high_worker.py')==digest(task/WORKER)
  and m['explicit_capture_hash_epoch']is True and all(m[k]is False for k in('arithmetic_computed','full_notebook57_completed',
   'support_acquisition_verified','parent_acquisitions_verified','all_index_conclusion_verified')),'Exact sealed original HIGH source epoch')
 runtime=list((task/'runtime').rglob('*'));need({p.relative_to(task).as_posix()for p in runtime if p.is_file()}=={WORKER},'Exact own launcher closure')
 for p in runtime:ordinary(p)
 found=set()
 for p in(task/'capsule').rglob('*'):
  ordinary(p)
  if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
 allowed={FRESH}|{p for a in ACTIONS for p in output_paths(a)}
 need(set(m['sources'])<=found<=set(m['sources'])|allowed,'Only exact sealed source inputs and explicitly named current HIGH outputs')
 for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'All original HIGH/kernel/manifest source bytes unchanged')
 need(digest(task/'capsule'/NATIVE/'MANIFEST.json')==d['original_manifest_sha256'],'Original71-row native manifest unchanged')
 if FRESH in found:
  b,epoch=current_derivation(task);need((task/'capsule'/FRESH).read_bytes()==b and read(task/'CAPTURE_EPOCH.json')==epoch,'Exact source-only current capture-hash derivation')
 return m
