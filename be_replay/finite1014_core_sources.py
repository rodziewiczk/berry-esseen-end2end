"""Data-only source/capture epoch for full unchanged INITIAL/resource10--14."""
from __future__ import annotations
import copy
from pathlib import Path,PurePosixPath
import posixpath
import shutil
import time
import urllib.request
import zipfile
from . import finite1014_kappa_sources as base

ROOT,MIB=base.ROOT,base.MIB
need,digest,read,dump,ordinary,parts=base.need,base.digest,base.read,base.dump,base.ordinary,base.parts
PLAN=ROOT/'proof/finite1014_core_source_plan.json'
PLAN_SHA256='ab37696011048ae407a8e7f43e576efe12563d8bc1dde47b469e91ab0dbb7ff6'
SCHEMA='SEALED_FINITE1014_CORE_CURRENT_SOURCES_V1'
EPOCH='CURRENT_SOURCE_CAPTURE_EPOCH.json'
ACTIONS=('initial_construct','initial_replay','resource_construct','resource_accept')


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned full10--14 source/metadata epoch plan');d=read(PLAN,16*MIB)
    need(d['schema']=='FINITE1014_CORE_NEW_METADATA_EPOCH_SOURCE_PLAN_V1'and len(d['cases'])==10
         and len(d['source_files'])==1558 and len(d['unavailable_historical_captures'])==50
         and d['original_python_unchanged']is True and all(d[k]is False for k in('arithmetic_computed',
             'full_notebook56_completed','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Full40-action conditional original selection')
    legacy=ROOT/d['legacy_commitments_file'];need(digest(legacy)==d['legacy_commitments_sha256'], 'All original3072 commitments retained')
    need(len(read(legacy,4*MIB)['commitments'])==3072,'Full original10--19 provenance map, not a new acquisition')
    need(digest(ROOT/'vendor/finite1014_core_documents/PROVENANCE.json')==d['vendored_document_provenance_sha256'],
         'Exact original document aliases/provenance')
    need(digest(ROOT/'vendor/finite1014_core_documents/LICENSE')==d['vendored_document_license_sha256'],'Document license identity')
    return d


def cases(band):
    need(band in('B0','BN'),'One literal full five-index band');rows=[r for r in plan()['cases']if r['band']==band]
    need([r['n']for r in rows]==[10,11,12,13,14],'All five original indices');return rows


def case(case_id):
    rows=[r for r in plan()['cases']if r['case_id']==case_id];need(len(rows)==1,'One fixed original n/band case');return rows[0]


def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);out={}
    for a in plan()['assets']:
        p=ordinary(directory/a['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1014_core_download_started',archive=a['name'],total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as dest:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source transport');dest.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1014_core_download',archive=a['name'],bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Full original archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Actual immutable source archive')
        out[a['name']]=p.resolve();progress('finite1014_core_archive_verified',archive=a['name'],bytes=a['bytes'],sha256=a['sha256'])
    return out


def prepare_cache(assets,output,*,progress=lambda *a,**k:None):
    d=plan();output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d['assets']:
            p=ordinary(assets[a['name']]);need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned original archive bytes')
            opened[a['name']]=zipfile.ZipFile(p)
        for i,(name,row)in enumerate(d['source_files'].items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                p.parent.mkdir(parents=True,exist_ok=True)
                if 'vendor_file'in row:shutil.copyfile(ROOT/row['vendor_file'],p)
                else:
                    z=opened[row['archive']];info=z.getinfo(row['member']);need(not info.is_dir()and info.file_size==row['bytes'],'Exact selected member')
                    with z.open(info)as source,p.open('xb')as dest:shutil.copyfileobj(source,dest,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original source/candidate/provenance byte')
            if i%100==0:progress('finite1014_core_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def capture_relative(row,action):
    need(action in ACTIONS,'Fixed original action')
    if action.startswith('initial_'):return row['initial_capture_prefix']+('_construct01'if action=='initial_construct'else'_replay01')
    return 'runs/finite1014_core_current/'+row['case_id']+'/'+action+'01'


def cwd_relative(row,action):
    return row['initial_directory']+'/n'+str(row['n'])if action.startswith('initial_')else row['resource_directory']


def outputs(row,action):
    if action=='initial_construct':return[row['initial_candidate']]
    if action=='initial_replay':return[row['initial_receipt']]
    if action=='resource_construct':
        prefix=row['resource_directory']+'/'+row['band']
        return[row['resource_candidate'],prefix+'/CONSTRUCT_TIMINGS.json']+[prefix+f'/rows/{i:03d}.json'for i in range(100)]
    need(action=='resource_accept','One fixed original action');return[row['resource_receipt']]


def checkpoints(row,action):
    # Candidate contains all100 row hashes; every row is also sealed after stop.
    return outputs(row,action)[:2]if action=='resource_construct'else outputs(row,action)


def provenance_inputs(row):
    # Some supplied historical own captures contain only empty stderr. Keep
    # their bytes, but never populate a fresh current capture destination.
    own_captures={capture_relative(row,action)+'/'+name for action in ACTIONS[:2]
                  for name in('metadata.json','stdout.txt','stderr.txt')}
    return set(row['own_outputs'])|{row['initial_prepared'],row['resource_prepared']}|own_captures


def prepare(case_id,cache,task):
    d=plan();row=case(case_id);task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh exclusive four-action case')
    (task/'capsule').mkdir(parents=True);static={};provenance={}
    special=provenance_inputs(row)
    for name,pin in row['original_source_commitments'].items():
        if name in d['unavailable_historical_captures']:continue
        need(name in d['source_files']and d['source_files'][name]['sha256']==pin,'Original source commitment is supplied')
        source=ordinary(Path(cache).joinpath(*parts(name)));need(digest(source)==pin,'Exact source cache byte')
        prefix='provenance'if name in special else'capsule';dest=task/prefix/name
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        (provenance if name in special else static)[name]=pin
    legacy=task/'provenance/ORIGINAL3072.json';shutil.copyfile(ROOT/d['legacy_commitments_file'],legacy)
    request=dict(schema=SCHEMA,case_id=case_id,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
        original_task_root=str(task),static_inputs=static,original_provenance=provenance,
        legacy_commitments_sha256=d['legacy_commitments_sha256'],original_python_unchanged=True,
        arithmetic_computed=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(request))
    (task/'capsule'/row['initial_directory']/('n'+str(row['n']))).mkdir(parents=True,exist_ok=True)
    need(all(not(task/'capsule'/capture_relative(row,action)).exists()for action in ACTIONS),
         'All four own capture destinations are exclusive and fresh')
    (task/EPOCH).write_bytes(dump(dict(schema='FINITE1014_CORE_EXPLICIT_SOURCE_CAPTURE_EPOCH_V1',case_id=case_id,
        original3072_sha256=d['legacy_commitments_sha256'],prepared_derivations={},own_action_captures={},
        unavailable_upstream_captures='UNACQUIRED_NOT_STAGED',original_python_unchanged=True,
        upstream_HIGH_acquired=False,support_acquisition_verified=False,full_notebook56_completed=False,all_index_conclusion_verified=False)))
    verify(task);return request


def prepared_projection(task,row,kind):
    d=plan();name=row[kind+'_prepared'];old=read(Path(task)/'provenance'/name,16*MIB);new=copy.deepcopy(old);graph={};changes={}
    for path,pin in old['files_sha256'].items():
        p=Path(task)/'capsule'/path
        if path in d['unavailable_historical_captures']and not p.exists():
            changes[path]=dict(original_sha256=pin,current_sha256=None,reason='UNACQUIRED_NOT_STAGED');continue
        need(ordinary(p).is_file(),'No omitted mathematical/source/document/profile input: '+path)
        now=digest(p);graph[path]=now
        if now!=pin:
            need(path in row['own_outputs']or path in(row['initial_prepared'],row['resource_prepared'])
                 or path.startswith(row['initial_capture_prefix']),'Only current own output/source-metadata rebinding')
            changes[path]=dict(original_sha256=pin,current_sha256=now,reason='CURRENT_OWN_EXECUTION_OR_PREPARED_METADATA')
    # Seal every original current-program/kernel copy, including the replay driver.
    directory=row[kind+'_directory']+'/'
    for path,pin in row['original_source_commitments'].items():
        if path.startswith(directory)and(path.endswith('.py')or path.endswith('/COPIED_SOURCES.json')):
            need(digest(Path(task)/'capsule'/path)==pin,'Original program/kernel unchanged')
            if path not in graph:changes[path]=dict(original_sha256=None,current_sha256=pin,reason='EXPLICIT_UNCHANGED_PROGRAM_CLOSURE')
            graph[path]=pin
    if kind=='resource':
        for action in ACTIONS[:2]:
            for filename in('metadata.json','stdout.txt','stderr.txt'):
                path=capture_relative(row,action)+'/'+filename;pin=digest(Path(task)/'capsule'/path)
                graph[path]=pin
                if path not in old['files_sha256']:changes[path]=dict(original_sha256=None,current_sha256=pin,reason='CURRENT_OWN_SUPERVISED_CAPTURE')
    new['files_sha256']=graph
    return name,old,new,changes


def derive_prepared(task,row,kind):
    need(kind in('initial','resource'),'One fixed prepared metadata phase')
    name,old,new,changes=prepared_projection(task,row,kind);p=Path(task)/'capsule'/name
    need(not p.exists(),'Each current PREPARED is derived once, never migrated after construction')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dump(new))
    ledger=read(Path(task)/EPOCH,16*MIB)
    ledger['prepared_derivations'][name]=dict(original_sha256=digest(Path(task)/'provenance'/name),current_sha256=digest(p),
        non_graph_fields_unchanged=True,changes=changes)
    (Path(task)/EPOCH).write_bytes(dump(ledger));return new


def input_map(task,row,action):
    capsule=Path(task)/'capsule';kind='initial'if action.startswith('initial_')else'resource';prepared=row[kind+'_prepared']
    graph=dict(read(capsule/prepared,16*MIB)['files_sha256']);graph[prepared]=digest(capsule/prepared)
    script=row[kind+'_directory']+('/construct.py'if action=='initial_construct'else'/replay.py'if action=='initial_replay'else'/resources.py')
    graph[script]=digest(capsule/script)
    if action=='initial_replay':
        graph[row['initial_candidate']]=digest(capsule/row['initial_candidate'])
        for name in('metadata.json','stdout.txt','stderr.txt'):
            p=capture_relative(row,'initial_construct')+'/'+name;graph[p]=digest(capsule/p)
    if action=='resource_accept':
        for p in outputs(row,'resource_construct'):graph[p]=digest(capsule/p)
        for name in('metadata.json','stdout.txt','stderr.txt'):
            p=capture_relative(row,'resource_construct')+'/'+name;graph[p]=digest(capsule/p)
    for name,pin in graph.items():need(digest(capsule/name)==pin,'Actual complete action input map')
    return graph


def relative_inputs(row,action,graph):
    return {posixpath.relpath(name,cwd_relative(row,action)):pin for name,pin in graph.items()}


def verify(task):
    task=ordinary(Path(task).resolve());d=plan();request=read(task/'SOURCES.json',16*MIB);row=case(request['case_id'])
    need(request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256 and request['source_adapter_sha256']==digest(__file__)
         and request['legacy_commitments_sha256']==d['legacy_commitments_sha256']and request['original_python_unchanged']is True
         and all(request[k]is False for k in('arithmetic_computed','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Exact current case source ledger')
    special=provenance_inputs(row)
    expected={k:v for k,v in row['original_source_commitments'].items()if k not in d['unavailable_historical_captures']}
    need(request['static_inputs']=={k:v for k,v in expected.items()if k not in special}
         and request['original_provenance']=={k:v for k,v in expected.items()if k in special},'No source/provenance commitment omitted')
    for prefix,field in(('capsule','static_inputs'),('provenance','original_provenance')):
        for name,pin in request[field].items():need(digest(task/prefix/name)==pin,'Every actual unchanged original input/provenance byte')
    need(digest(task/'provenance/ORIGINAL3072.json')==d['legacy_commitments_sha256'],'Original full3072 commitments retained')
    allowed=set(request['static_inputs'])|set(row['own_outputs'])|{row['initial_prepared'],row['resource_prepared']}
    for action in ACTIONS:allowed|={capture_relative(row,action)+'/'+n for n in('metadata.json','stdout.txt','stderr.txt')}
    actual=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(task/'capsule').as_posix())
    need(set(request['static_inputs'])<=actual<=allowed,'Exact source tree plus named current outputs/captures')
    return request,row
