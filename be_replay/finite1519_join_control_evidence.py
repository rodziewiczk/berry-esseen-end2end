"""Pure full stopped-execution readback for the six bounded57H controls."""
from __future__ import annotations
import math
from pathlib import Path
from . import finite1519_join_control_sources as src
from .finite1014_join_epoch import same
from .finite1014_kappa_evidence import pathclass

SCOPE='FINITE1519_SIX_BOUNDED_CONTROLS_CURRENT_METADATA_BASIC_23H_V1'
OBSERVED='OBSERVED_FINITE1519_JOIN_CONTROLS_V1'
COMPLETED='COMPLETED_FINITE1519_JOIN_CONTROLS_V1'
CPU_SECONDS=WALL_SECONDS=82800
MEMORY_BYTES=2048*src.MIB
DISK_BYTES=512*src.MIB
LOG_BYTES=16*src.MIB
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','full_notebook57_completed',
       'all_law_conclusion_verified','all_index_conclusion_verified')


def read(path,limit=16*src.MIB):
    p=src.ordinary(path);src.need(p.is_file()and p.stat().st_size<=limit,'Bounded ordinary control evidence file')
    return src.parsed(p.read_bytes())


def implementation():
    names=('finite1519_join_control_sources.py','finite1519_join_control_evidence.py','finite1519_join_controls.py',
           'finite1014_join_epoch.py','finite1039_count_evidence.py','finite1039_sources.py',
           'finite1014_kappa_evidence.py','linux_supervisor.py','colab_batch.py','environment.py')
    return{n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def mapped(task,value,original):
    cls=pathclass(original);src.need(type(value)is str and '\0'not in value,'Recorded ordinary evidence path')
    p=cls(value);src.need(p.is_absolute(),'Absolute originating control context')
    try:rel=p.relative_to(cls(original))
    except ValueError:raise ValueError('Control evidence leaves its explicit originating task root')
    src.need(rel.parts and all(x not in('.','..')for x in rel.parts),'Contained restored evidence path')
    return src.ordinary(Path(task).joinpath(*rel.parts))


def command(row,python):
    src.need(type(python)is str and bool(python),'Actual recorded Python interpreter')
    return[python,*row['command_tail']]


def guard():
    return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
        per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,
        aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,
        sampled_group_CPU_limit_seconds=CPU_SECONDS,sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)


def finite(value):
    src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite ordinary observed execution/resource value')


def inventory(task):
    root=src.ordinary(task);out={}
    for p in sorted(root.rglob('*')):
        src.ordinary(p)
        if not p.is_file():continue
        name=p.relative_to(root).as_posix()
        if name=='CONTROLS_COMPLETED.json':continue
        src.need(p.stat().st_size<=128*src.MIB,'Bounded full control artifact')
        out[name]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    src.need(len(out)<=10000 and sum(r['bytes']for r in out.values())<=512*src.MIB,'Bounded full stopped control inventory')
    return out


def fixture(task):
    """Validate a genuine complete COUNT transaction, never a substituted PASS."""
    from . import finite1039_count_evidence as count_ev
    task=src.ordinary(task);d=src.plan()['fresh_geometry_fixture']
    packet=read(task/'CURRENT_GEOMETRY_FIXTURE.json');upstream=task/'upstream/count56'
    checked=count_ev.validate_completed(upstream)
    src.need(checked['job_id']==d['job_id']and checked['conditional_arithmetic_completed']is True
             and same(checked,packet['validated_native_count'])and packet['schema']=='FINITE1519_CURRENT_GENUINE_COUNT56_FIXTURE_V1'
             and packet['catalog_sha256']==d['catalog_sha256']and packet['historical_acceptance_promoted']is False
             and packet['current_execution_required']is True,'Actual complete current selected COUNT56 evidence')
    directory=upstream/'capsule'/d['directory'];prefix='work/'+d['directory']+'/'
    expected={d['contract_name']:d['contract_sha256'],d['forest_name']:d['forest_sha256'],
              d['acceptance_name']:src.digest(directory/d['acceptance_name'])}
    src.need(same(packet['files_sha256'],expected),'Exact genuine upstream fixture payload commitments')
    for name,pin in expected.items():
        original=src.child(directory,name);current=src.child(task,'capsule/'+prefix+name)
        src.need(src.digest(original)==src.digest(current)==pin,'Whole genuine COUNT56 payload without receipt editing')
    return expected[d['acceptance_name']]


def source_task(task):
    task=src.ordinary(task);d=src.plan();request=read(task/'SOURCES.json')
    excluded=set(d['own_outputs_never_staged_from_history'])|set(d['generated_engine_copies_not_staged_before_native_calls'])
    f=d['fresh_geometry_fixture'];prefix='work/'+f['directory']+'/'
    excluded|={prefix+f[k]for k in('contract_name','forest_name','acceptance_name')}
    src.need(request['schema']=='FINITE1519_JOIN_CONTROL_TASK_V1'and request['source_plan_sha256']==src.PLAN_SHA256
             and type(request['original_task_root'])is str and pathclass(request['original_task_root'])(request['original_task_root']).is_absolute()
             and request['static_sources_staged']==sorted(set(d['source_files'])-excluded)
             and request['absent_until_real_execution']==sorted(excluded)and request['original_python_unchanged']is True
             and all(request[k]is False for k in src.FALSE_FLAGS),'Exact current source request and false theorem flags')
    for name,row in d['source_files'].items():
        original=src.child(task,'provenance/original/'+name)
        src.need(original.stat().st_size==row['bytes']and src.digest(original)==row['sha256'],'Every unchanged original provenance byte')
        if name not in excluded and name not in d['metadata_documents']:
            current=src.child(task,'capsule/'+name)
            src.need(current.stat().st_size==row['bytes']and src.digest(current)==row['sha256'],'All original control/helper/math/source inputs unchanged')
    for row in d['cases']:
        p=src.child(task,'provenance/reference/'+row['id']+'.json')
        src.need(p.stat().st_size==row['reference']['bytes']and src.digest(p)==row['reference']['sha256'],'Whole immutable original control reference output')
    return request


def transport(task,row,record,request,python):
    task=src.ordinary(task);observed=record['observed'];directory=task/'executions'/row['id'];origin=request['original_task_root']
    src.need(same(read(directory/'supervisor-result.json'),observed)and observed['status']=='completed'
             and type(observed['returncode'])is int and observed['returncode']==0 and observed['reason']is None
             and observed['mode']=='untrusted_search'and observed['proof_accepted']is False
             and type(observed['sample_count'])is int and observed['sample_count']>0,'Actual stopped successful BASIC bounded control')
    for key in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[key])
    launch=read(directory/'launch.json');fields={'argv','cwd','output_dir','mode','cpu_seconds','wall_seconds','memory_bytes',
        'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds','checkpoint_paths'}
    src.need(set(launch)==fields and same(launch['argv'],command(row,python))
             and mapped(task,launch['cwd'],origin)==task/'capsule'/row['cwd']
             and mapped(task,launch['output_dir'],origin)==directory and launch['mode']=='untrusted_search'
             and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
             and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list and len(launch['checkpoint_paths'])==1
             and mapped(task,launch['checkpoint_paths'][0],origin)==task/'capsule'/row['output'],
             'Literal unchanged original command, cwd, full checkpoint and actual output context')
    for key,value in(('cpu_seconds',CPU_SECONDS),('wall_seconds',WALL_SECONDS),('memory_bytes',MEMORY_BYTES),
                      ('disk_bytes',DISK_BYTES),('log_bytes',LOG_BYTES)):
        allowed=(int,float)if key=='wall_seconds'else(int,)
        src.need(type(launch[key])in allowed and launch[key]==value,'Exact documented bounded-control execution policy')
    src.need(same(observed['guard_scope'],guard()),'Honest per-process/sampled-group BASIC scope, without native promotion')
    finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,
                  elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    progress=src.ordinary(directory/'progress.jsonl')
    src.need(progress.is_file()and 0<progress.stat().st_size<=LOG_BYTES,'Bounded actual stopped control history')
    lines=progress.read_bytes().splitlines()
    src.need(lines and same(src.parsed(lines[-1]),finished)and same(read(directory/'progress.json'),finished),'Actual final stopped supervisor history')
    streams={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],origin)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=LOG_BYTES
                 and src.digest(p)==observed[kind+'_sha256'],'Actual whole bounded stdout/stderr capture')
        streams[kind]=p
    src.need(streams['stderr'].stat().st_size==0,'Successful original control has empty stderr')
    checkpoints=observed['checkpoints'];src.need(type(checkpoints)is list and len(checkpoints)==1,'One entire current stopped control output')
    cp=checkpoints[0];output=task/'capsule'/row['output'];cwd=task/'capsule'/row['cwd'];copy=directory/'checkpoints'/output.relative_to(cwd)
    src.need(set(cp)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}and cp['exists']is True
             and cp['trusted_certificate']is False and mapped(task,cp['source_path'],origin)==output
             and mapped(task,cp['path'],origin)==copy and src.ordinary(output).is_file()and src.ordinary(copy).is_file()
             and type(cp['bytes'])is int and 0<cp['bytes']<=16*src.MIB and cp['bytes']==output.stat().st_size==copy.stat().st_size
             and cp['sha256']==src.digest(output)==src.digest(copy),'Exact whole native result and actual stopped checkpoint bytes')
    return streams


def mathematical_reference(task,row,inputs,streams):
    task=src.ordinary(task);output=task/'capsule'/row['output'];current=read(output)
    old=read(task/'provenance/reference'/str(row['id']+'.json'))
    src.need(type(current)is dict and type(old)is dict and set(current)==set(old)
             and same({k:v for k,v in current.items()if k!='files_sha256'},
                      {k:v for k,v in old.items()if k!='files_sha256'}),
             'All original mathematical/control/status/domain fields unchanged; no arbitrary timing erasure')
    graph=src.output_graph(task,row['id'],inputs)
    src.need(same(current['files_sha256'],graph),'Complete actual native source graph with only declared current metadata binding')
    for key,value in row['expected_reference_fields'].items():src.need(same(current[key],value),'Every original explicit bounded-control census')
    text=streams['stdout'].read_text('utf-8').strip()
    if row['id']=='resource-range':
        src.need(text==current['status']+' '+src.digest(output),'Original resource-range terminal and whole current output SHA')
    elif row['id']=='join-geometry':
        src.need(text==current['status']+' '+str(len(current['geometry_mutations_rejected']))+' '+src.digest(output),
                 'Original whole geometry-control terminal, mutation count and result SHA')
    else:
        omitted={'finite-high':{'quartic_rows','modulus_rows','files_sha256'},
                 'contact-high':{'rows','files_sha256'},'compensated-high':{'rows','files_sha256'},
                 'count-range':set()}[row['id']]
        expected={k:v for k,v in current.items()if k not in omitted}
        src.need(same(src.parsed(text.encode('utf-8')),expected),'Whole original bounded-control stdout object equals actual output')
    return dict(id=row['id'],output_sha256=src.digest(output),status=current['status'],original_python_unchanged=True,
                mathematical_projection_identical=True,current_source_graph_rows=len(graph),
                expected_control_fields=row['expected_reference_fields'])


def validate_run(task,report):
    task=src.ordinary(task);request=source_task(task);acceptance=fixture(task)
    fields={'schema','scope','original_task_root','implementation','python_executable','python_version','actions',
            'conditional_controls_completed',*FLAGS}
    src.need(type(report)is dict and set(report)==fields and report['schema']==OBSERVED and report['scope']==SCOPE
             and report['original_task_root']==request['original_task_root']and same(report['implementation'],implementation())
             and type(report['python_executable'])is str and bool(report['python_executable'])
             and type(report['python_version'])is str and bool(report['python_version'])
             and report['conditional_controls_completed']is False and all(report[k]is False for k in FLAGS)
             and type(report['actions'])is list and [r['id']for r in report['actions']]==list(src.IDS),
             'Exactly all six complete actual bounded actions with false full-proof scope flags')
    prior={};summaries=[]
    for record,row in zip(report['actions'],src.cases()):
        src.need(type(record)is dict and set(record)=={'id','observed','inputs_before','inputs_after','metadata_epoch','output_sha256'},'Exact stopped control action record')
        inputs=src.input_map(task,row['id'],validated_prior_actions=prior,fixture_acceptance_sha256=acceptance)
        epoch=src.metadata_projection(task,validated_prior_actions=prior)['ledger']
        src.need(same(record['inputs_before'],inputs)and same(record['inputs_after'],inputs)
                 and same(record['metadata_epoch'],epoch),'Whole actual inputs unchanged across the stopped action')
        streams=transport(task,row,record,request,report['python_executable']);summary=mathematical_reference(task,row,inputs,streams)
        src.need(record['output_sha256']==summary['output_sha256'],'Current completed output hash')
        prior[row['id']]=summary;summaries.append(summary)
    expected=set(src.plan()['source_files'])-set(request['absent_until_real_execution'])
    expected|={r['output']for r in src.cases()}
    expected|=set(src.plan()['generated_engine_copies_not_staged_before_native_calls'])
    f=src.plan()['fresh_geometry_fixture'];expected|={'work/'+f['directory']+'/'+f[k]for k in('contract_name','forest_name','acceptance_name')}
    actual={p.relative_to(task/'capsule').as_posix()for p in(task/'capsule').rglob('*')if p.is_file()}
    src.need(actual==expected,'Entire exact six-control capsule inventory; no hidden helper or old output')
    return dict(scope=SCOPE,native_actions=6,source_files=161,metadata_documents=5,actions=summaries,
                geometry_fixture_native_job=f['job_id'],current_geometry_acceptance_sha256=acceptance,
                original_math_imported_by_controller=False,**{k:False for k in FLAGS})


def validate_completed(task):
    task=src.ordinary(task);report=read(task/'CONTROLS_OBSERVED.json',32*src.MIB);summary=validate_run(task,report)
    done=read(task/'CONTROLS_COMPLETED.json',32*src.MIB)
    fields={'schema','scope','implementation','observed_sha256','summary','artifacts','conditional_controls_completed',*FLAGS}
    src.need(type(done)is dict and set(done)==fields and done['schema']==COMPLETED and done['scope']==SCOPE
             and same(done['implementation'],implementation())and done['observed_sha256']==src.digest(task/'CONTROLS_OBSERVED.json')
             and same(done['summary'],summary)and same(done['artifacts'],inventory(task))
             and done['conditional_controls_completed']is True and all(done[k]is False for k in FLAGS),
             'Whole six-action completion requires actual sources, full controls and genuine stopped upstream evidence')
    return dict(schema='REVALIDATED_FINITE1519_SIX_CONTROLS_V1',summary=summary,
                controls_result_sha256=src.digest(task/'CONTROLS_COMPLETED.json'),conditional_controls_completed=True,
                **{k:False for k in FLAGS})
