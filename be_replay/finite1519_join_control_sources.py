"""Data-only sources for the six bounded57H controls; no native math imports.

This is an internal component of57H, not a delivered standalone notebook.
Current COUNT56 and scalar execution dependencies need independent stopped-run
validation by the runtime. Historical output bytes remain reference data.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile

from . import finite1039_sources as base
from . import finite1014_join_epoch as epoch

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'proof/finite1519_join_control_source_plan.json'
PLAN_SHA256='8491bb9b07fbacb2739c26a070ff6c6c5b05863fdf6112b816cc32e064e254fc'
EPOCH_HELPER_SHA256='fa60de887116e1d08b75878bb8c49fc096d5dffc61fafcc95aa100eaa04366b4'
IDS=('finite-high','contact-high','compensated-high','resource-range','count-range','join-geometry')
MIB=1024**2
FALSE_FLAGS=dict(arithmetic_computed=False,parent_acquisitions_verified=False,
                 full_notebook57_completed=False,all_index_conclusion_verified=False)

need=base.need


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as f:
        for block in iter(lambda:f.read(MIB),b''):h.update(block)
    return h.hexdigest()


def encoded(value):return(json.dumps(value,indent=2,allow_nan=False)+'\n').encode('utf-8')
def parsed(raw):return epoch.loads(raw)


def ordinary(path):
    p=Path(path).absolute()
    for q in(p,*p.parents):
        need(not q.is_symlink()and not(hasattr(q,'is_junction')and q.is_junction()),'Ordinary source task ancestry')
    return p


def child(root,name):return ordinary(ordinary(root).joinpath(*base.parts(name)))


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned six-control source plan')
    d=parsed(PLAN.read_bytes())
    need(d['schema']=='FINITE1519_JOIN_BOUNDED_CONTROL_SOURCE_PLAN_V1'
         and tuple(r['id']for r in d['cases'])==IDS and len(d['source_files'])==161
         and len(d['metadata_documents'])==5 and d['original_python_unchanged']is True
         and d['full_finite_join_implemented']is False and all(d[k]is False for k in FALSE_FLAGS),
         'Complete bounded-control source scope and false proof flags')
    need(digest(ROOT/'be_replay/finite1014_join_epoch.py')==EPOCH_HELPER_SHA256,'Reviewed data-only graph adapter')
    need(d['fresh_geometry_fixture']['current_execution_required']is True
         and d['fresh_geometry_fixture']['job_id']=='n15.B0.p56.3ccb81760515',
         'Geometry control requires genuine current selected native COUNT')
    for name,row in d['source_files'].items():
        base.parts(name)
        need(row['sha256']==d['original_files_sha256'][name]
             and type(row['bytes'])is int and 0<=row['bytes']<=32*MIB,'Exact source commitment')
    return d


def cases():return plan()['cases']
def case(action):
    need(type(action)is str and action in IDS,'One selected bounded control')
    return next(r for r in cases()if r['id']==action)


def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);out={}
    for a in plan()['assets']:
        p=child(directory,a['name'])
        if not p.exists():
            pending=ordinary(p.with_name(p.name+'.pending'));count=0
            with urllib.request.urlopen(a['url'])as source,pending.open('xb')as target:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded source transport');target.write(block)
                    if count%(16*MIB)==0:progress('finite1519_join_control_download',archive=a['name'],bytes=count,total_bytes=a['bytes'])
            need(count==a['bytes']and digest(pending)==a['sha256'],'Complete immutable source archive');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Exact whole source archive')
        out[a['name']]=p
    return out


def cache_inventory(d):
    rows={'original/'+name:dict(bytes=r['bytes'],sha256=r['sha256'])for name,r in d['source_files'].items()}
    rows.update({'reference/'+r['id']+'.json':dict(bytes=r['reference']['bytes'],sha256=r['reference']['sha256'])for r in d['cases']})
    return rows


def verify_cache(cache):
    d=plan();cache=ordinary(cache);rows=cache_inventory(d);found=set()
    need(cache.is_dir(),'Existing original bounded-control source cache')
    for p in cache.rglob('*'):
        ordinary(p)
        if p.is_file():found.add(p.relative_to(cache).as_posix())
    need(found==set(rows)|{'SOURCE_CACHE.json'},'Exact source/reference cache inventory')
    for name,r in rows.items():
        p=child(cache,name);need(p.is_file()and p.stat().st_size==r['bytes']and digest(p)==r['sha256'],'Actual original control source/reference byte')
    request=parsed((cache/'SOURCE_CACHE.json').read_bytes())
    need(request==dict(schema='FINITE1519_JOIN_CONTROL_CACHE_V1',source_plan_sha256=PLAN_SHA256,files=rows,**FALSE_FLAGS),
         'Source cache cannot acquire controls or parents')
    return rows


def prepare_cache(assets,output,*,progress=lambda *a,**k:None):
    d=plan();output=ordinary(output)
    if output.exists():verify_cache(output);return output
    opened={};buffers={}
    try:
        for a in d['assets']:
            p=ordinary(assets[a['name']]);need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned archive transport')
            z=zipfile.ZipFile(p);base.zip_index(z);opened[a['name']]=z
        selected=[('original/'+name,row)for name,row in d['source_files'].items()]
        selected += [('reference/'+r['id']+'.json',r['reference'])for r in d['cases']]
        for name,row in selected:
            if 'vendor_file'in row:raw=child(ROOT,row['vendor_file']).read_bytes()
            else:
                z=opened[row['archive']];info=z.getinfo(row['member'])
                need(not info.is_dir()and info.file_size==row['bytes'],'Bounded exact selected archive member');raw=z.read(info)
            need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'Exact archived control/source/reference byte')
            buffers[name]=raw
        need(sum(map(len,buffers.values()))<64*MIB,'Bounded full original control source cache')
    finally:
        for z in opened.values():z.close()
    output.mkdir(parents=True,exist_ok=False)
    for name,raw in buffers.items():
        p=child(output,name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    request=dict(schema='FINITE1519_JOIN_CONTROL_CACHE_V1',source_plan_sha256=PLAN_SHA256,files=cache_inventory(d),**FALSE_FLAGS)
    (output/'SOURCE_CACHE.json').write_bytes(encoded(request));verify_cache(output)
    progress('finite1519_join_control_sources_prepared',original_sources=161,original_programs_imported=False,arithmetic_computed=False)
    return output


def prepare_task(cache,task):
    d=plan();verify_cache(cache);task=ordinary(task);need(not task.exists(),'Exclusive new control task')
    cache=ordinary(cache);task.mkdir(parents=True,exist_ok=False)
    excluded=set(d['own_outputs_never_staged_from_history'])|set(d['generated_engine_copies_not_staged_before_native_calls'])
    fixture=d['fresh_geometry_fixture'];fixture_prefix='work/'+fixture['directory']+'/'
    excluded|={fixture_prefix+fixture[k]for k in('contract_name','forest_name','acceptance_name')}
    for name in d['source_files']:
        source=child(cache,'original/'+name)
        old=child(task,'provenance/original/'+name);old.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,old)
        if name not in excluded:
            p=child(task,'capsule/'+name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,p)
    for row in d['cases']:
        p=child(task,'provenance/reference/'+row['id']+'.json');p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(child(cache,'reference/'+row['id']+'.json'),p)
    request=dict(schema='FINITE1519_JOIN_CONTROL_TASK_V1',source_plan_sha256=PLAN_SHA256,
        original_task_root=str(task),static_sources_staged=sorted(set(d['source_files'])-excluded),
        absent_until_real_execution=sorted(excluded),original_python_unchanged=True,**FALSE_FLAGS)
    (task/'SOURCES.json').write_bytes(encoded(request))
    return request


def metadata_projection(task,*,validated_prior_actions):
    """Data operation only; caller independently validates every prior execution.

    COUNT56's genuine current acceptance is bound separately; it is never a
    permissible source-graph override. The five manifests contain only scope
    text and source graphs, with no numerical theorem or contract payload.
    """
    d=plan();task=ordinary(task)
    need(type(validated_prior_actions)is dict and set(validated_prior_actions)<=set(IDS),'Explicit current prior control selection')
    documents={n:child(task,'provenance/original/'+n).read_bytes()for n in d['metadata_documents']}
    names=set(documents)
    for raw in documents.values():
        doc=parsed(raw);need(set(doc)=={'scope','files_sha256'},'Only non-numerical manifest documents')
        names.update(doc['files_sha256'])
    original={n:d['original_files_sha256'][n]for n in names};current=dict(original);allowed=[]
    for row in d['cases']:
        if row['id']not in validated_prior_actions:continue
        path=row['output'];p=child(task,'capsule/'+path);h=digest(p)
        need(h==validated_prior_actions[row['id']]['output_sha256'],'Actual validated preceding control output')
        if path in names:
            need(path not in documents,'Current control output cannot masquerade as source metadata')
            current[path]=h;allowed.append(path)
    return epoch.derive_metadata_epoch(documents,original,current,{},allowed_overrides=allowed)


def derive_current_metadata(task,*,validated_prior_actions):
    result=metadata_projection(task,validated_prior_actions=validated_prior_actions)
    for name,raw in result['derived'].items():
        p=child(task,'capsule/'+name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    return result['ledger']


def input_map(task,action,*,validated_prior_actions,fixture_acceptance_sha256=None):
    """Return the entire input graph, with only named current metadata changes.

    The caller supplies prior control summaries only after stopped-run validation.
    Geometry's numerical acceptance is never a graph-epoch override: its genuine
    upstream execution is separately validated by the evidence reader.
    """
    d=plan();row=case(action);task=ordinary(task)
    need(set(row['dependencies'])<=set(validated_prior_actions),'Every preceding native control completed')
    projected=metadata_projection(task,validated_prior_actions=validated_prior_actions)
    for name,raw in projected['derived'].items():
        if name in row['input_reference_graph']:
            need(child(task,'capsule/'+name).read_bytes()==raw,'Exact declared current non-numerical source epoch')
    allowed={name:hashlib.sha256(raw).hexdigest()for name,raw in projected['derived'].items()}
    for earlier in d['cases']:
        if earlier['id']in validated_prior_actions:
            allowed[earlier['output']]=validated_prior_actions[earlier['id']]['output_sha256']
    if action=='join-geometry':
        epoch.pin(fixture_acceptance_sha256)
        f=d['fresh_geometry_fixture'];allowed['work/'+f['directory']+'/'+f['acceptance_name']]=fixture_acceptance_sha256
    graph={}
    for name,pin in row['input_reference_graph'].items():
        if name in row['generated_engine_copies']:continue
        p=child(task,'capsule/'+name);h=digest(p)
        need(h==allowed.get(name,pin),'Exact original input or explicitly validated current execution: '+name)
        graph[name]=h
    need(graph.get(row['script'])==row['original_python_sha256'],'Unchanged entire original bounded control program')
    return graph


def output_graph(task,action,inputs):
    row=case(action);task=ordinary(task);graph=dict(inputs)
    for name,record in row['generated_engine_copies'].items():
        p=child(task,'capsule/'+name)
        need(p.is_file()and p.stat().st_size==record['bytes']and digest(p)==record['sha256'],
             'Native-created exact unchanged mathematical helper copy')
        graph[name]=record['sha256']
    need(set(graph)==set(row['input_reference_graph']),'Whole original output source graph')
    return graph
