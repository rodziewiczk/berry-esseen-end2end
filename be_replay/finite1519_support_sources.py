"""Exact original full-ray support sources for57D; no numerical imports."""
from __future__ import annotations
import json
from pathlib import Path
import shutil,time,urllib.request,zipfile
from . import finite1039_sources as base
ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite1519_support_source_plan.json'
PLAN_SHA256='0b17b5b7cad29f401a07073562971acba6d8b3725b928443c6b67d4a208e7cf2'
SCHEMA='SEALED_ORIGINAL_SUPPORT15_19_INPUTS_V1'
NATIVE='work/cutoff15_20261017/analytic/initial15_v1'
AUDIT='work/cutoff15_20261017/analytic/support15_19_replay_v1'
RUNS='runs/cutoff15_20261017/analytic/support15_19_bridge01'
CANDIDATE=NATIVE+'/SUPPORT15_19_BRIDGE.json'
RESULT=AUDIT+'/REPLAY_CHECKED.json'
ENGINES=('direct_gaussian_support.py','finite_binomial_core.py','small_index_support.py','heat_support50.py')
ACTIONS=('construct','replay')
def dump(d):return(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def plan():
 need(digest(PLAN)==PLAN_SHA256,'Externally pinned full-ray support closure');d=read(PLAN)
 need(d['schema']=='FINITE1519_FULL_RAY_SUPPORT_SOURCE_PLAN_V1'and len(d['source_files'])==26
      and len(d['original_candidate_source_graph'])==23 and d['original_mathematical_programs_unchanged']is True
      and d['original_candidate_is_not_an_execution_input']is True,'Complete original support source selection')
 need(all(d[k]is False for k in('arithmetic_computed','support_acquisition_verified','full_notebook57_completed',
                               'parent_acquisitions_verified','all_index_conclusion_verified')),'Conditional support premises remain unacquired')
 return d

def obtain_assets(directory, *,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);result={}
    for a in plan()['assets']:
        name=a['name'];need(tuple(parts(name))==(name,),'Pinned source archive basename');p=ordinary(directory/name)
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1519_support_download_started',archive=name,total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source download');target.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1519_support_download',archive=name,bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Actual full source archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact immutable source transport')
        result[name]=p.resolve();progress('finite1519_support_archive_verified',archive=name,bytes=a['bytes'],sha256=a['sha256'])
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
            if i%20==0:progress('finite1519_support_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()



def output_paths(action):
 need(action in ACTIONS,'One original support action')
 return [CANDIDATE]if action=='construct'else[RESULT]+[AUDIT+'/engine/'+n for n in ENGINES]
def capture_paths():return[RUNS+'/'+n for n in('metadata.json','stdout.txt','stderr.txt')]
def prepare(cache,task):
 d=plan();task=ordinary(task);need(not task.exists(),'Fresh private support capsule');task.mkdir(parents=True)
 for name,row in d['source_files'].items():
  p=ordinary(Path(cache).joinpath(*parts(name)));need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Original support input bytes')
  dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 m=dict(schema=SCHEMA,original_task_root=str(task.resolve()),source_plan_sha256=PLAN_SHA256,
  source_adapter_sha256=digest(__file__),sources={n:r['sha256']for n,r in d['source_files'].items()},
  original_programs_unchanged=True,arithmetic_computed=False,full_notebook57_completed=False,
  support_acquisition_verified=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
 (task/'SOURCES.json').write_bytes(dump(m));verify_job(task);return m
def verify_job(task):
 task=ordinary(task);d=plan();m=read(task/'SOURCES.json')
 need(m['schema']==SCHEMA and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
  and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}and m['original_programs_unchanged']is True
  and all(m[k]is False for k in('arithmetic_computed','full_notebook57_completed','support_acquisition_verified',
                               'parent_acquisitions_verified','all_index_conclusion_verified')),'Sealed genuine-current support source epoch')
 found=set()
 for p in(task/'capsule').rglob('*'):
  ordinary(p)
  if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
 allowed=set(capture_paths()+[p for a in ACTIONS for p in output_paths(a)])
 need(set(m['sources'])<=found<=set(m['sources'])|allowed,'Exact source closure plus only named current support outputs')
 for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Original support source unchanged')
 return m
