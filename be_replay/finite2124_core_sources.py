"""Sealed unchanged actual21--24 INITIAL/resource sources and explicit data epoch."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import shutil,urllib.request,zipfile
from . import finite1039_sources as base

ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite2124_core_source_plan.json'
PLAN_SHA256='f799a6ce030c38f8330f8579acb6f6606ac1c6d5c213384f30578a0f78b9fb33'
PREFIX='continuation_cutoff20_20261016'
INITIAL=PREFIX+'/root/bridge21_24_initial_v1'
RESOURCE=PREFIX+'/root/bridge21_24_resources_v1'
INITIAL_REVIEW=PREFIX+'/analytic/BRIDGE_INITIAL_SOURCE_REVIEW.json'
RESOURCE_REVIEW=PREFIX+'/analytic/BRIDGE_RESOURCE_SOURCE_REVIEW.json'
INITIAL_FREEZE='ae9b7e58bdaf467b8a4b7f024f7b9f903a460ade2308e0bf90d0a45a6ba9db3d'
ACTIONS=('initial_construct','initial_accept','resource_construct','resource_accept')
BANDS={'B0':(['1','11/10'],'23/10'),'BN':(['11/10','9/8'],'12/5')}

def dump(x):return(json.dumps(x,sort_keys=True,indent=2)+'\n').encode()

def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned actual21--24 INITIAL/resource source selection');d=read(PLAN)
    need(d['schema']=='FINITE2124_CORE_SOURCE_PLAN_V1'and len(d['source_files'])==193
         and d['initial_freeze_sha256']==INITIAL_FREEZE and d['actions']==list(ACTIONS)
         and len(d['static_resource_review_graph'])==190 and len(d['removed_historical_example_graph'])==8
         and d['original_mathematical_programs_unchanged']is True and d['original_frozen_manifests_unchanged']is True
         and d['original_review_preserved']is True and d['fresh_resource_review_is_data_only_epoch']is True
         and all(d[k]is False for k in('arithmetic_computed','historical_fourier_replayed','predecessor_verified',
                                      'full_notebook58_completed','resource_count_join_verified','all_index_conclusion_verified')),
         'Original source/manifests preserved, data-only current-parent epoch and conditional conclusions')
    return d

def case(n,band):
    need(type(n)is int and n in(21,22,23,24)and type(band)is str and band in BANDS,'Literal actual n/band')
    return 'n'+str(n)+'_'+band

def review_paths(n,band):
    folder=RESOURCE+'/'+case(n,band)
    return folder+'/FRESH_SOURCE_REVIEW.json',folder+'/RESOURCE_REVIEW_BRIDGE.json'

def output_paths(action,n,band):
    need(action in ACTIONS,'Exact four-call stage');name=case(n,band)
    root=INITIAL if action.startswith('initial_')else RESOURCE
    suffix='CANDIDATE.json'if action.endswith('construct')else'ACCEPTED.json'
    values=[root+'/'+name+'/'+suffix]
    if action=='resource_construct':values += [root+'/'+name+'/CONSTRUCT_TIMINGS.json']+[root+'/'+name+'/rows/'+format(i,'03d')+'.json'for i in range(100)]
    return values

def capture_paths(action,n,band):
    need(action in ACTIONS,'Exact four-call stage')
    if not action.startswith('initial_'):return []
    folder=INITIAL+'/captures/'+case(n,band)+'_'+action.split('_')[1]
    return [folder+'/'+v for v in('EXECUTION.json','stdout.txt','stderr.txt')]

def generated_paths(n,band):
    return [v for a in ACTIONS for v in output_paths(a,n,band)+capture_paths(a,n,band)]+list(review_paths(n,band))

def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(Path(directory));directory.mkdir(parents=True,exist_ok=True);out={}
    for row in plan()['assets']:
        need(tuple(parts(row['name']))==(row['name'],),'Archive basename');p=ordinary(directory/row['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=0
            progress('finite2124_core_download_started',archive=row['name'],bytes=row['bytes'])
            with urllib.request.urlopen(row['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=row['bytes'],'Bounded source download');target.write(block)
                    if count-last>=16*MIB:progress('finite2124_core_download',archive=row['name'],bytes=count);last=count
            need(count==row['bytes']and digest(pending)==row['sha256'],'Actual whole source archive');pending.replace(p)
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Immutable source transport')
        out[row['name']]=p.resolve()
    return out

def prepare_cache(assets,output):
    d=plan();output=ordinary(Path(output));output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for row in d['assets']:
            p=ordinary(Path(assets[row['name']]))
            need(p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact source archive')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[row['name']]=z
        for name,row in d['source_files'].items():
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                info=opened[row['archive']].getinfo(row['member']);need(info.file_size==row['bytes'],'Selected source size')
                p.parent.mkdir(parents=True,exist_ok=True)
                with opened[row['archive']].open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original input byte')
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()

def prepare(cache,task,n,band):
    name=case(n,band);d=plan();task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh four-call actual-index task');task.mkdir(parents=True)
    for key,row in d['source_files'].items():
        p=ordinary(Path(cache).joinpath(*parts(key)))
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Exact cached input')
        q=task/'capsule'/key;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    m=dict(schema='SEALED_ACTUAL21_24_CORE_SOURCES_V1',n=n,band=band,case=name,original_task_root=str(task),
        source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),sources={k:v['sha256']for k,v in d['source_files'].items()},
        original_mathematical_programs_unchanged=True,original_frozen_manifests_unchanged=True,original_review_preserved=True,
        arithmetic_computed=False,historical_fourier_replayed=False,predecessor_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(m));verify_job(task,n,band);return m

def verify_job(task,n=None,band=None):
    task=ordinary(Path(task).resolve());d=plan();m=read(task/'SOURCES.json');case(m['n'],m['band'])
    need((n is None or type(n)is int and m['n']==n)and(band is None or m['band']==band),'Requested source case matches')
    need(set(m)=={'schema','n','band','case','original_task_root','source_plan_sha256','source_adapter_sha256','sources',
                 'original_mathematical_programs_unchanged','original_frozen_manifests_unchanged','original_review_preserved',
                 'arithmetic_computed','historical_fourier_replayed','predecessor_verified','all_index_conclusion_verified'}
         and m['schema']=='SEALED_ACTUAL21_24_CORE_SOURCES_V1'and m['case']==case(m['n'],m['band'])
         and type(m['original_task_root'])is str and m['source_plan_sha256']==PLAN_SHA256 and m['source_adapter_sha256']==digest(__file__)
         and m['sources']=={k:v['sha256']for k,v in d['source_files'].items()}
         and all(m[k]is True for k in('original_mathematical_programs_unchanged','original_frozen_manifests_unchanged','original_review_preserved'))
         and all(m[k]is False for k in('arithmetic_computed','historical_fourier_replayed','predecessor_verified','all_index_conclusion_verified')),
         'Whole exact unchanged source ledger and conditional case')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    need(set(m['sources'])<=found<=set(m['sources'])|set(generated_paths(m['n'],m['band'])),'Only sealed sources and declared genuine case outputs')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'Every original source/review/manifest byte unchanged')
    need(digest(task/'capsule'/INITIAL/'FROZEN_SOURCES.json')==INITIAL_FREEZE,'Unchanged hardcoded INITIAL freeze')
    return m

def fresh_parent_graph(task,n,band):
    c=Path(task)/'capsule';names=[INITIAL+'/'+case(n,band)+'/'+v for v in('CANDIDATE.json','ACCEPTED.json')]
    names += [v for a in('initial_construct','initial_accept')for v in capture_paths(a,n,band)]
    return {v:digest(c/v)for v in names}

def review_epoch(task,n,band):
    """Metadata only: caller must separately acquire genuine INITIAL evidence."""
    task=Path(task);m=verify_job(task,n,band);c=task/'capsule';d=plan();original=read(c/RESOURCE_REVIEW)
    need(original['files_sha256']==d['static_resource_review_graph']|d['removed_historical_example_graph'],'Literal old review graph')
    fresh=fresh_parent_graph(task,n,band);graph=dict(d['static_resource_review_graph']);graph.update(fresh)
    need(len(fresh)==8 and len(graph)==len(original['files_sha256']),'Exactly eight old example bindings replaced by current case')
    derived=dict(original);derived['files_sha256']=graph
    bridge=dict(schema='ACTUAL21_24_CURRENT_INITIAL_REVIEW_GRAPH_EPOCH_V1',n=n,band=band,source_plan_sha256=PLAN_SHA256,
        original_review_sha256=digest(c/RESOURCE_REVIEW),fresh_review_sha256=hashlib.sha256(dump(derived)).hexdigest(),
        removed_historical_example_graph=d['removed_historical_example_graph'],fresh_parent_graph=fresh,
        unchanged_static_review_graph=d['static_resource_review_graph'],unchanged_non_graph_metadata={k:v for k,v in original.items()if k!='files_sha256'},
        writer_sha256=digest(__file__),metadata_only=True,arithmetic_computed=False,predecessor_verified=False,all_index_conclusion_verified=False)
    return derived,bridge

def write_review_epoch(task,n,band):
    derived,bridge=review_epoch(task,n,band);c=Path(task)/'capsule';a,b=review_paths(n,band)
    for key,value in((a,derived),(b,bridge)):
        p=c/key;need(not p.exists(),'Fresh explicit metadata epoch');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dump(value))
    verify_review_epoch(task,n,band)

def verify_review_epoch(task,n,band):
    derived,bridge=review_epoch(task,n,band);a,b=review_paths(n,band);c=Path(task)/'capsule'
    need((c/a).read_bytes()==dump(derived)and(c/b).read_bytes()==dump(bridge),'Exact reversible data-only graph substitution, no old hash impersonation')
    for name,pin in derived['files_sha256'].items():need(digest(c/name)==pin,'Every fresh review dependency is actual current bytes')
    return bridge
