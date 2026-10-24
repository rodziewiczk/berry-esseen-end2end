"""Data-only source/capture epoch for full unchanged INITIAL/resource15--19."""
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
PLAN=ROOT/'proof/finite1519_core_source_plan.json'
PLAN_SHA256='71d755f1293efdc0438e33b5af5711775b70c05334c41ac04aef20281e628339'
SCHEMA='SEALED_FINITE1519_CORE_CURRENT_SOURCES_V1'
EPOCH='CURRENT_SOURCE_CAPTURE_EPOCH.json'
ACTIONS=('initial_construct','initial_replay','resource_construct','resource_accept')


def plan():
    need(digest(PLAN)==PLAN_SHA256,'Pinned full15--19 source/metadata epoch plan');d=read(PLAN,16*MIB)
    need(d['schema']=='FINITE1519_CORE_NEW_METADATA_EPOCH_SOURCE_PLAN_V1'and len(d['cases'])==10
         and len(d['source_files'])==1532 and len(d['unavailable_historical_captures'])==40
         and len(d['fresh_upstream_high_inputs'])==8 and d['original_python_unchanged']is True
         and all(d[k]is False for k in('arithmetic_computed','full_notebook57_completed','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Full40-action conditional original selection')
    legacy=ROOT/d['legacy_commitments_file'];need(digest(legacy)==d['legacy_commitments_sha256'],'All original3072 commitments retained')
    need(len(read(legacy,4*MIB)['commitments'])==3072,'Full original10--19 provenance map')
    for prefix,provenance_key,license_key in((d['document_vendor_directory'],'vendored_document_provenance_sha256','vendored_document_license_sha256'),
            (d['extra_document_vendor_directory'],'extra_document_provenance_sha256','extra_document_license_sha256')):
        need(digest(ROOT/prefix/'PROVENANCE.json')==d[provenance_key]and digest(ROOT/prefix/'LICENSE')==d[license_key],
             'Unchanged original document bytes/provenance/license')
    return d


def cases(band):
    need(band in('B0','BN'),'One literal full five-index band');rows=[r for r in plan()['cases']if r['band']==band]
    need([r['n']for r in rows]==[15,16,17,18,19],'All five original indices');return rows


def case(case_id):
    rows=[r for r in plan()['cases']if r['case_id']==case_id];need(len(rows)==1,'One fixed original n/band case');return rows[0]


def obtain_assets(directory,*,progress=lambda *a,**k:None):
    directory=ordinary(directory);directory.mkdir(parents=True,exist_ok=True);out={}
    for a in plan()['assets']:
        p=ordinary(directory/a['name'])
        if not p.exists():
            pending=ordinary(p.with_suffix('.zip.pending'));count=0;last=time.monotonic();at=0
            progress('finite1519_core_download_started',archive=a['name'],total_bytes=a['bytes'])
            with urllib.request.urlopen(a['url'])as source,pending.open('wb')as dest:
                while block:=source.read(MIB):
                    count+=len(block);need(count<=a['bytes'],'Bounded original source transport');dest.write(block)
                    if count-at>=16*MIB or time.monotonic()-last>=5:
                        progress('finite1519_core_download',archive=a['name'],bytes=count,total_bytes=a['bytes']);at=count;last=time.monotonic()
            need(count==a['bytes']and digest(pending)==a['sha256'],'Full original archive SHA');pending.replace(p)
        need(p.is_file()and p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Actual immutable source archive')
        out[a['name']]=p.resolve();progress('finite1519_core_archive_verified',archive=a['name'],bytes=a['bytes'],sha256=a['sha256'])
    return out


def prepare_cache(assets,output,*,upstream_high,progress=lambda *a,**k:None):
    d=plan();upstream_files(upstream_high);output=ordinary(output);output.mkdir(parents=True,exist_ok=True);opened={}
    try:
        for a in d['assets']:
            p=ordinary(assets[a['name']]);need(p.stat().st_size==a['bytes']and digest(p)==a['sha256'],'Pinned original archive bytes')
            opened[a['name']]=zipfile.ZipFile(p)
        for i,(name,row)in enumerate(d['source_files'].items()):
            p=ordinary(output.joinpath(*parts(name)))
            if not p.exists():
                p.parent.mkdir(parents=True,exist_ok=True)
                if row.get('fresh_high_input'):shutil.copyfile(Path(upstream_high)/'capsule'/name,p)
                elif 'vendor_file'in row:shutil.copyfile(ROOT/row['vendor_file'],p)
                else:
                    z=opened[row['archive']];info=z.getinfo(row['member']);need(not info.is_dir()and info.file_size==row['bytes'],'Exact selected member')
                    with z.open(info)as source,p.open('xb')as dest:shutil.copyfileobj(source,dest,MIB)
            need(p.is_file()and p.stat().st_size==row['bytes']and digest(p)==row['sha256'],'Every original source/candidate/provenance byte')
            if i%100==0:progress('finite1519_core_source_cache',files=i,total=len(d['source_files']),arithmetic_computed=False)
    finally:
        for z in opened.values():z.close()
    return output.resolve()


def capture_relative(row,action):
    need(action in ACTIONS,'Fixed original action')
    if action.startswith('initial_'):return row['initial_capture_prefix']+('_construct01'if action=='initial_construct'else'_replay01')
    return 'runs/finite1519_core_current/'+row['case_id']+'/'+action+'01'


def cwd_relative(row,action):
    need(action in ACTIONS,'One fixed original action');return row['actions'][action]['cwd']


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
    return set(row['own_outputs'])|set(row['metadata_files'])|own_captures


def prepare(case_id,cache,task,*,upstream_high):
    d=plan();row=case(case_id);task=ordinary(Path(task).resolve());need(not task.exists(),'Fresh exclusive four-action case')
    upstream_files(upstream_high)
    (task/'capsule').mkdir(parents=True);shutil.copytree(ordinary(upstream_high),task/'upstream-high')
    high_pins,high_checked=upstream_files(task/'upstream-high');static={};provenance={};special=provenance_inputs(row)
    for name,pin in row['original_source_commitments'].items():
        if name in high_pins:
            source=task/'upstream-high/capsule'/name;pin=high_pins[name]
        elif name in d['unavailable_historical_captures']:continue
        else:
            need(name in d['source_files']and d['source_files'][name]['sha256']==pin,'Original source commitment is supplied')
            source=ordinary(Path(cache).joinpath(*parts(name)))
        need(digest(source)==pin,'Actual fixed source or genuinely validated HIGH input')
        prefix='provenance'if name in special else'capsule';dest=task/prefix/name
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        (provenance if name in special else static)[name]=pin
    shutil.copyfile(ROOT/d['legacy_commitments_file'],task/'provenance/ORIGINAL3072.json')
    request=dict(schema=SCHEMA,case_id=case_id,source_plan_sha256=PLAN_SHA256,source_adapter_sha256=digest(__file__),
        original_task_root=str(task),static_inputs=static,original_provenance=provenance,
        legacy_commitments_sha256=d['legacy_commitments_sha256'],fresh_high_evidence=high_checked,
        original_python_unchanged=True,arithmetic_computed=False,parent_acquisitions_verified=False,all_index_conclusion_verified=False)
    (task/'SOURCES.json').write_bytes(dump(request))
    (task/'capsule'/row['constructor_directory']).mkdir(parents=True,exist_ok=True)
    need(all(not(task/'capsule'/capture_relative(row,a)).exists()for a in ACTIONS),'All four own capture destinations exclusive and fresh')
    (task/EPOCH).write_bytes(dump(dict(schema='FINITE1519_CORE_EXPLICIT_SOURCE_CAPTURE_EPOCH_V1',case_id=case_id,
        original3072_sha256=d['legacy_commitments_sha256'],prepared_derivations={},own_action_captures={},
        unavailable_upstream_captures='UNACQUIRED_NOT_STAGED',fresh_conditional_HIGH_evidence=high_checked,
        original_python_unchanged=True,upstream_HIGH_acquired=False,support_acquisition_verified=False,
        full_notebook57_completed=False,all_index_conclusion_verified=False)))
    verify(task);return request


def prepared_projection(task,row,kind):
    need(kind in('initial','replay','resource'),'One exact metadata phase')
    d=plan();name=row[kind+'_prepared'];need(name is not None,'Only n15 has separate replay PREPARED')
    old=read(Path(task)/'provenance'/name,16*MIB);new=copy.deepcopy(old);graph={};changes={}
    for path,pin in old['files_sha256'].items():
        p=Path(task)/'capsule'/path
        if path in d['unavailable_historical_captures']and not p.exists():
            changes[path]=dict(original_sha256=pin,current_sha256=None,reason='UNACQUIRED_NOT_STAGED');continue
        need(ordinary(p).is_file(),'No omitted mathematical/source/document/profile input: '+path)
        now=digest(p);graph[path]=now
        if now!=pin:
            need(path in row['own_outputs']or path in row['metadata_files']or path.startswith(row['initial_capture_prefix'])
                 or path in d['fresh_upstream_high_inputs'],'Only declared current own or validated upstream HIGH metadata binding')
            reason='CURRENT_VALIDATED_UPSTREAM_HIGH_INPUT'if path in d['fresh_upstream_high_inputs']else'CURRENT_OWN_EXECUTION_OR_PREPARED_METADATA'
            changes[path]=dict(original_sha256=pin,current_sha256=now,reason=reason)
    directory=row['constructor_directory'if kind=='initial'else'replay_directory'if kind=='replay'else'resource_directory']+'/'
    for path,pin in row['original_source_commitments'].items():
        if path.startswith(directory)and(path.endswith('.py')or path.endswith('/COPIED_SOURCES.json')):
            need(digest(Path(task)/'capsule'/path)==pin,'Original program/kernel unchanged')
            if path not in graph:changes[path]=dict(original_sha256=None,current_sha256=pin,reason='EXPLICIT_UNCHANGED_PROGRAM_CLOSURE')
            graph[path]=pin
    if kind=='replay':
        entry=new['candidates'][row['band']]
        need(entry['path']==row['initial_candidate']and entry['sha256']==row['original_source_commitments'][row['initial_candidate']],
             'Exact original selected candidate metadata guard')
        pin=digest(Path(task)/'capsule'/row['initial_candidate']);entry['sha256']=pin
        changes['@candidates.'+row['band']+'.sha256']=dict(original_sha256=old['candidates'][row['band']]['sha256'],current_sha256=pin,
            reason='GENUINE_CURRENT_SELECTED_CONSTRUCTOR_CANDIDATE')
    if kind in('replay','resource'):
        outputs_needed=[row['initial_candidate']]+([row['initial_receipt']]if kind=='resource'else[])
        captures=ACTIONS[:2]if kind=='resource'else ACTIONS[:1]
        paths=outputs_needed+[capture_relative(row,a)+'/'+f for a in captures for f in('metadata.json','stdout.txt','stderr.txt')]
        for path in paths:
            pin=digest(Path(task)/'capsule'/path);graph[path]=pin
            if path not in old['files_sha256']:changes[path]=dict(original_sha256=None,current_sha256=pin,reason='CURRENT_OWN_SUPERVISED_INPUT')
    new['files_sha256']=graph
    return name,old,new,changes


def derivation_record(task,name,old,new,changes):
    return dict(original_sha256=digest(Path(task)/'provenance'/name),current_sha256=digest(Path(task)/'capsule'/name),
        non_graph_fields_unchanged={k:v for k,v in old.items()if k!='files_sha256'}=={k:v for k,v in new.items()if k!='files_sha256'},
        only_declared_source_or_selected_candidate_metadata_changed=True,changes=changes)


def derive_prepared(task,row,kind):
    name,old,new,changes=prepared_projection(task,row,kind);p=Path(task)/'capsule'/name
    need(not p.exists(),'Each current PREPARED derived once before its original action')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dump(new));ledger=read(Path(task)/EPOCH,16*MIB)
    ledger['prepared_derivations'][name]=derivation_record(task,name,old,new,changes)
    (Path(task)/EPOCH).write_bytes(dump(ledger));return new


def native_graph(task,row,action):
    c=Path(task)/'capsule'
    if action=='initial_construct':
        name=row['initial_prepared'];graph=dict(read(c/name,16*MIB)['files_sha256']);graph[name]=digest(c/name)
        directory=row['constructor_directory'];copied=read(c/directory/'COPIED_SOURCES.json')
        for filename,data in copied.items():
            need(Path(filename).name==filename,'Original local copied module basename')
            pin=digest(c/directory/filename);need(pin==data['sha256']==digest(c/data['source']),'Original copied module/source pair')
            graph[directory+'/'+filename]=pin;graph[data['source']]=pin
        for filename in('pilot.py','PROOF.txt','COPIED_SOURCES.json','SOURCE_PORT.diff'):
            path=directory+'/'+filename;graph[path]=digest(c/path)
        return graph
    if action=='initial_replay':
        if row['replay_prepared']:
            name=row['replay_prepared'];graph=dict(read(c/name,16*MIB)['files_sha256']);graph[name]=digest(c/name)
        else:
            graph=dict(read(c/row['initial_candidate'],128*MIB)['files_sha256'])
            paths=[row['initial_candidate'],row['actions'][action]['script'],row['initial_prepared']]
            paths +=[capture_relative(row,'initial_construct')+'/'+f for f in('metadata.json','stdout.txt','stderr.txt')]
            for path in paths:graph[path]=digest(c/path)
        return graph
    name=row['resource_prepared'];graph=dict(read(c/name,16*MIB)['files_sha256']);graph[name]=digest(c/name);return graph


def input_map(task,row,action):
    c=Path(task)/'capsule';graph=native_graph(task,row,action)
    if action=='initial_replay':
        for p in[row['initial_candidate']]+[capture_relative(row,'initial_construct')+'/'+f for f in('metadata.json','stdout.txt','stderr.txt')]:graph[p]=digest(c/p)
    if action=='resource_accept':
        for p in outputs(row,'resource_construct')+[capture_relative(row,'resource_construct')+'/'+f for f in('metadata.json','stdout.txt','stderr.txt')]:graph[p]=digest(c/p)
    for name,pin in graph.items():need(digest(c/name)==pin,'Actual complete original action input map')
    return graph


def relative_inputs(row,action,graph):
    return {posixpath.relpath(name,cwd_relative(row,action)):pin for name,pin in graph.items()}


def upstream_files(task):
    from . import finite1519_high_evidence as high
    task=ordinary(Path(task));checked=high.validate_completed(task)
    need(checked['source_plan_sha256']==plan()['fresh_high_source_plan_sha256']and checked['conditional_compensated_high_arithmetic_completed']is True,
         'Complete genuine current57E HIGH arithmetic evidence')
    pins={name:digest(task/'capsule'/name)for name in plan()['fresh_upstream_high_inputs']}
    for name,pin in pins.items():
        if name.endswith('/RESULT.json'):
            need(pin==plan()['fresh_upstream_high_inputs'][name]and (task/'capsule'/name).stat().st_size==47474,'Exact genuine deterministic mathematical HIGH input')
    return pins,checked


def verify(task):
    task=ordinary(Path(task).resolve());d=plan();request=read(task/'SOURCES.json',16*MIB);row=case(request['case_id'])
    high_pins,high_checked=upstream_files(task/'upstream-high')
    need(request['schema']==SCHEMA and request['source_plan_sha256']==PLAN_SHA256 and request['source_adapter_sha256']==digest(__file__)
         and request['legacy_commitments_sha256']==d['legacy_commitments_sha256']and request['original_python_unchanged']is True
         and request['fresh_high_evidence']==high_checked
         and all(request[k]is False for k in('arithmetic_computed','parent_acquisitions_verified','all_index_conclusion_verified')),
         'Exact current case source and full validated upstream HIGH ledger')
    special=provenance_inputs(row);expected={k:v for k,v in row['original_source_commitments'].items()if k not in d['unavailable_historical_captures']}
    expected.update(high_pins)
    need(request['static_inputs']=={k:v for k,v in expected.items()if k not in special}
         and request['original_provenance']=={k:v for k,v in expected.items()if k in special},'No source/provenance commitment omitted')
    for prefix,field in(('capsule','static_inputs'),('provenance','original_provenance')):
        for name,pin in request[field].items():need(digest(task/prefix/name)==pin,'Every original or validated fresh input/provenance byte')
    need(digest(task/'provenance/ORIGINAL3072.json')==d['legacy_commitments_sha256'],'Original full3072 commitments retained')
    allowed=set(request['static_inputs'])|set(row['own_outputs'])|set(row['metadata_files'])
    for a in ACTIONS:allowed|={capture_relative(row,a)+'/'+n for n in('metadata.json','stdout.txt','stderr.txt')}
    actual=set()
    for p in(task/'capsule').rglob('*'):
        ordinary(p)
        if p.is_file():actual.add(p.relative_to(task/'capsule').as_posix())
    need(set(request['static_inputs'])<=actual<=allowed,'Exact original source tree plus named current metadata/outputs/captures')
    return request,row
