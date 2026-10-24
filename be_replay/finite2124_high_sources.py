"""Exact unchanged40-input source closure for the conditional58A support pass."""
from __future__ import annotations
import json
from pathlib import Path
import shutil,time,urllib.request,zipfile
from . import finite1039_sources as base

ROOT,MIB=base.ROOT,base.MIB
need,digest,read,ordinary,parts=base.need,base.digest,base.read,base.ordinary,base.parts
PLAN=ROOT/'proof/finite2124_high_source_plan.json'
PLAN_SHA256='ac6f7d8e130b40d88e49a53aaa00bf9070c0a47d954d1a49b046251b4d93d417'
NATIVE='continuation_cutoff20_20261016/root/bridge21_24_high_rho_v1'
REVIEW='continuation_cutoff20_20261016/analytic/BRIDGE_HIGH_RHO_SOURCE_REVIEW.json'
ACTIONS=('construct','accept')
OUTPUTS=dict(construct='CANDIDATE.json',accept='ACCEPTED.json')

def dump(value):return(json.dumps(value,sort_keys=True,indent=2)+'\n').encode('utf-8')

def loads(value):
    def invalid(value):raise ValueError('Nonfinite JSON number')
    return json.loads(value,object_pairs_hook=base.unique,parse_constant=invalid)

def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned actual21--24 support source plan');d=read(PLAN)
    need(d['schema']=='FINITE2124_HIGHRHO_SOURCE_PLAN_V1'and len(d['source_files'])==40
         and d['native']==NATIVE and d['review']==REVIEW and d['actions']==list(ACTIONS)
         and d['actual_n']==[21,22,23,24]and d['negative_controls']==10
         and d['original_source_programs_unchanged']is True and d['original_manifests_and_reviews_unchanged']is True
         and all(d[k]is False for k in('historical_fourier_replayed','arithmetic_computed','full_actual20_24_verified',
                                       'parent_acquisitions_verified','all_index_conclusion_verified')),
         'Exact original conditional support selection, without a sharp20--24 claim')
    return d

def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(Path(directory));directory.mkdir(parents=True,exist_ok=True);out={}
    for row in plan()['assets']:
        need(tuple(parts(row['name']))==(row['name'],),'Archive basename')
        p=ordinary(directory/row['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=0
            progress('finite2124_high_download_started',archive=row['name'],bytes=row['bytes'])
            with urllib.request.urlopen(row['url'])as source,pending.open('wb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=row['bytes'],'Bounded source download');target.write(block)
                    if count-last>=16*MIB:
                        progress('finite2124_high_download',archive=row['name'],bytes=count);last=count
            need(count==row['bytes']and digest(pending)==row['sha256'],'Whole source asset identity');pending.replace(p)
        need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Immutable actual source asset')
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
                info=opened[row['archive']].getinfo(row['member']);need(info.file_size==row['bytes'],'Source member size')
                p.parent.mkdir(parents=True,exist_ok=True)
                with opened[row['archive']].open(info)as source,p.open('xb')as target:shutil.copyfileobj(source,target,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original source byte')
        base.verify_cache(output,d['source_files'])
    finally:
        for z in opened.values():z.close()
    return output.resolve()

def prepare(cache,task):
    task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh actual21--24 support task');task.mkdir(parents=True)
    d=plan()
    for name,row in d['source_files'].items():
        source=ordinary(Path(cache).joinpath(*parts(name)))
        need(source.is_file()and source.stat().st_size==row['bytes']and digest(source)==row['sha256'],'Exact cached source')
        dest=task/'capsule'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    m=dict(schema='SEALED_ACTUAL21_24_HIGH_RHO_SOURCES_V1',source_plan_sha256=PLAN_SHA256,
        source_adapter_sha256=digest(__file__),original_task_root=str(task),
        sources={n:r['sha256']for n,r in d['source_files'].items()},
        original_source_programs_unchanged=True,historical_fourier_replayed=False,arithmetic_computed=False)
    (task/'SOURCES.json').write_bytes(dump(m));verify_job(task);return m

def verify_job(task):
    task=ordinary(Path(task).resolve());d=plan();m=read(task/'SOURCES.json')
    need(set(m)=={'schema','source_plan_sha256','source_adapter_sha256','original_task_root','sources',
                 'original_source_programs_unchanged','historical_fourier_replayed','arithmetic_computed'}
         and m['schema']=='SEALED_ACTUAL21_24_HIGH_RHO_SOURCES_V1'and m['source_plan_sha256']==PLAN_SHA256
         and m['source_adapter_sha256']==digest(__file__)and type(m['original_task_root'])is str
         and m['sources']=={n:r['sha256']for n,r in d['source_files'].items()}
         and m['original_source_programs_unchanged']is True and m['historical_fourier_replayed']is False
         and m['arithmetic_computed']is False,'Unchanged original conditional source ledger')
    found=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(task/'capsule').as_posix())
    need(set(m['sources'])<=found<=set(m['sources'])|{NATIVE+'/'+n for n in OUTPUTS.values()},
         'Exactly original sources plus genuine declared current outputs')
    for name,pin in m['sources'].items():need(digest(task/'capsule'/name)==pin,'All mathematical/source/review bytes unchanged')
    return m
