"""Pure readback of genuine40-call conditional core; no original math imports."""
from __future__ import annotations
import math
from fractions import Fraction
from pathlib import Path
from . import finite1519_core_sources as src
from .finite1014_kappa_evidence import same,pathclass

SCOPE='UNCHANGED_FULL_INITIAL_RESOURCE15_19_CURRENT_METADATA_BASIC_V1'
OBSERVED='OBSERVED_FINITE1519_CORE_CASE_V1'
COMPLETED='COMPLETED_FINITE1519_CORE_CASE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=82800,82800,2048*src.MIB
DISK_BYTES,LOG_BYTES=512*src.MIB,16*src.MIB
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','fresh_parent_fact_joins_verified',
       'support_acquisition_verified','HIGH_acquisition_verified','full_notebook57_completed','all_index_conclusion_verified')


def implementation():
    names=('finite1519_core.py','finite1519_core_sources.py','finite1519_core_evidence.py',
           'finite1014_kappa_sources.py','finite1014_kappa_evidence.py','linux_supervisor.py','colab_batch.py','environment.py',
           'finite1519_high.py','finite1519_high_sources.py','finite1519_high_evidence.py','finite1519_high_worker.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original(request,name):
    cls=pathclass(request['original_task_root']);return str(cls(request['original_task_root']).joinpath(*src.parts(name)))


def mapped(task,value,request):
    cls=pathclass(request['original_task_root']);src.need(type(value)is str and '\0'not in value,'Recorded ordinary path')
    p=cls(value);src.need(p.is_absolute(),'Absolute original evidence path')
    try:rel=p.relative_to(cls(request['original_task_root']))
    except ValueError:raise ValueError('Evidence leaves its explicit originating task root')
    src.need(rel.parts and all(n not in('.','..')for n in rel.parts),'Contained restored path')
    return src.ordinary(Path(task).joinpath(*rel.parts))


def command(row,action,python):
    src.need(action in src.ACTIONS and type(python)is str and bool(python),'Fixed original action/current interpreter')
    pathclass(python);return[python]+row['actions'][action]['arguments']


def guard():
    return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
        per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,
        aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,
        sampled_group_CPU_limit_seconds=CPU_SECONDS,sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)


def finite(v):src.need(type(v)in(int,float)and math.isfinite(v)and v>=0,'Finite ordinary elapsed/resource measurement')


def transport(task,row,action,observed,request,python):
    task=Path(task);directory=task/'executions'/action
    src.need(same(src.read(directory/'supervisor-result.json'),observed)and observed['status']=='completed'
             and type(observed['returncode'])is int and observed['returncode']==0 and observed['reason']is None
             and observed['mode']=='untrusted_search'and observed['proof_accepted']is False
             and type(observed['sample_count'])is int and observed['sample_count']>0,'Actual stopped successful BASIC action')
    for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[k])
    launch=src.read(directory/'launch.json')
    expected={'argv','cwd','output_dir','mode','cpu_seconds','wall_seconds','memory_bytes','disk_bytes','log_bytes',
              'sample_seconds','heartbeat_seconds','checkpoint_paths'}
    src.need(set(launch)==expected and same(launch['argv'],command(row,action,python))
             and mapped(task,launch['cwd'],request)==task/'capsule'/src.cwd_relative(row,action)
             and mapped(task,launch['output_dir'],request)==directory and launch['mode']=='untrusted_search'
             and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==DISK_BYTES
             and type(launch['log_bytes'])is int and launch['log_bytes']==LOG_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
             and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
             and [mapped(task,p,request)for p in launch['checkpoint_paths']]==[task/'capsule'/p for p in src.checkpoints(row,action)],
             'Literal original command/cwd/current output requests and fixed budgets')
    src.need(same(observed['guard_scope'],guard()),'Honest BASIC scope without native promotion')
    finished=dict(event='linux_supervisor_finished',stage='untrusted_search',status=observed['status'],reason=observed['reason'],
                  elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    history=src.ordinary(directory/'progress.jsonl')
    src.need(history.is_file()and 0<history.stat().st_size<=LOG_BYTES,'Bounded genuine supervisor history')
    lines=history.read_text(encoding='utf-8').splitlines()
    src.need(lines and same(src.base.loads(lines[-1]),finished)and same(src.read(directory/'progress.json'),finished),
             'Actual final stopped supervisor progress matches its result')
    streams={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],request)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=LOG_BYTES
                 and src.digest(p)==observed[kind+'_sha256'],'Actual bounded stream bytes')
        streams[kind]=p
    src.need(streams['stderr'].stat().st_size==0,'Original successful stderr must be empty')
    outputs=src.checkpoints(row,action);src.need(type(observed['checkpoints'])is list and len(observed['checkpoints'])==len(outputs),
                                              'Every requested whole stopped output')
    cwd=task/'capsule'/src.cwd_relative(row,action)
    for packet,name in zip(observed['checkpoints'],outputs):
        current=task/'capsule'/name;copied=directory/'checkpoints'/current.relative_to(cwd)
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],request)==current and mapped(task,packet['path'],request)==copied
                 and src.ordinary(current).is_file()and src.ordinary(copied).is_file()
                 and type(packet['bytes'])is int and 0<packet['bytes']<=128*src.MIB
                 and packet['bytes']==current.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(current)==src.digest(copied),'Actual whole stopped proof/candidate output')
    return streams


def math_projection(value,action,omitted):
    out={k:v for k,v in value.items()if k not in omitted}
    if action=='initial_construct':
        finite(value['initial_seconds']);out.pop('initial_seconds')
        out['stages']=[]
        for stage in value['stages']:
            finite(stage['seconds']);out['stages'].append({k:v for k,v in stage.items()if k!='seconds'})
        out['support_attempts']=[]
        for attempt in value['support_attempts']:
            finite(attempt['seconds']);out['support_attempts'].append({k:v for k,v in attempt.items()if k!='seconds'})
        finite(value['chosen_support']['seconds'])
        out['chosen_support']={k:v for k,v in value['chosen_support'].items()if k!='seconds'}
    return out


def numerical_reference(task,row,action):
    name={'initial_construct':'initial_candidate','initial_replay':'initial_receipt',
          'resource_construct':'resource_candidate','resource_accept':'resource_receipt'}[action]
    path=row[name];current=src.read(Path(task)/'capsule'/path,128*src.MIB)
    old=src.read(Path(task)/'provenance'/path,128*src.MIB)
    omitted={'files_sha256'}
    if action in('initial_replay','resource_accept'):omitted.add('candidate_sha256')
    if action=='resource_construct':omitted|={'initial_candidate_sha256','initial_acceptance_sha256'}
    if action=='resource_accept':omitted.add('timings_seconds')
    src.need(type(current)is dict and set(current)==set(old),'Whole unchanged original result schema')
    src.need(same(math_projection(current,action,omitted),math_projection(old,action,omitted)),
             'Every original mathematical/domain/panel/control field, with explicit metadata-only rebinding')
    src.need(type(current['n'])is int and current['n']==row['n']and current['band']==row['band'],'Literal current scope')
    expected_graph=src.native_graph(task,row,action)
    src.need(same(current['files_sha256'],expected_graph),'Complete exact native source/input graph, without omitted commitments')
    for name,pin in current['files_sha256'].items():src.need(src.digest((Path(task)/'capsule').joinpath(*src.parts(name)))==pin,
                                                           'Every native source/input binding remains actual')
    if action=='initial_construct':
        src.need(len(current['stages'])==8 and len(current['export']['panels'])==100 and len(current['support_attempts'])==6,'Eight updates plus final full export')
    elif action=='initial_replay':
        src.need(current['candidate_sha256']==src.digest(Path(task)/'capsule'/row['initial_candidate'])
                 and type(current['fresh_complete_covers'])is int and current['fresh_complete_covers']==9
                 and type(current['signed_cells_per_cover'])is int and current['signed_cells_per_cover']==row['signed_cells_per_cover']
                 and type(current['original_probability_panels'])is int and current['original_probability_panels']==100
                 and type(current['support_radii'])is int and current['support_radii']==6,
                 'Current full nine-cover/100panel INITIAL identity')
        src.need(all(type(current[k])is int and current[k]==v for k,v in row['initial_controls'].items()),
                 'All literal INITIAL malformed and parser controls')
    else:
        rows=current['rows'];src.need(type(rows)is list and len(rows)==100,'All100 resource rows')
        for i,desc in enumerate(rows):
            src.need(type(desc['index'])is int and desc['index']==i and desc['n']==row['n']and desc['band']==row['band']
                     and desc['path']==f'rows/{i:03d}.json'
                     and same(desc['p'],[str(Fraction(i,100)),str(Fraction(i+1,100))]),'Original ordered closed resource panels')
            path=Path(task)/'capsule'/row['resource_directory']/row['band']/desc['path']
            src.need(src.digest(path)==desc['sha256'],'Actual whole resource row hash')
        if action=='resource_construct':
            src.need(current['initial_candidate_sha256']==src.digest(Path(task)/'capsule'/row['initial_candidate'])
                     and current['initial_acceptance_sha256']==src.digest(Path(task)/'capsule'/row['initial_receipt']),
                     'Fresh own INITIAL bound by the full resource constructor')
            timings=src.read(Path(task)/'capsule'/src.outputs(row,action)[1])
            src.need(type(timings)is list and len(timings)==100,'All100 original constructor timing records')
            for value in timings:finite(value)
        else:
            src.need(current['candidate_sha256']==src.digest(Path(task)/'capsule'/row['resource_candidate'])
                     and same(current['negative_controls'],row['resource_controls'])
                     and type(current['timings_seconds'])is list and len(current['timings_seconds'])==100,
                     'Fresh full resource acceptance and all native controls')
            for value in current['timings_seconds']:finite(value)
    return current


def inventory(task):
    task=Path(task);return{p.relative_to(task).as_posix():dict(bytes=p.stat().st_size,sha256=src.digest(p))
        for p in sorted(task.rglob('*'))if src.ordinary(p).is_file()
        and p.relative_to(task).as_posix()not in('CASE_OBSERVED.json','CASE_COMPLETED.json')}


def validate_run(task,report):
    task=Path(task).resolve();request,row=src.verify(task)
    fields={'schema','scope','case_id','original_task_root','implementation','python_executable','python_version',
            'actions','conditional_core_arithmetic_completed',*FLAGS}
    src.need(type(report)is dict and set(report)==fields and report['schema']==OBSERVED and report['scope']==SCOPE and report['case_id']==row['case_id']
             and report['original_task_root']==request['original_task_root']and same(report['implementation'],implementation())
             and report['conditional_core_arithmetic_completed']is False and all(report[k]is False for k in FLAGS)
             and type(report['python_version'])is str and bool(report['python_version'])
             and type(report['actions'])is list and [a['action']for a in report['actions']]==list(src.ACTIONS),
             'All four actual original actions and no promoted full-parent claim')
    epoch=src.read(task/src.EPOCH,16*src.MIB)
    src.need(epoch['schema']=='FINITE1519_CORE_EXPLICIT_SOURCE_CAPTURE_EPOCH_V1'and epoch['case_id']==row['case_id']
             and epoch['original3072_sha256']==request['legacy_commitments_sha256']
             and set(epoch['prepared_derivations'])==set(row['metadata_files'])
             and same(epoch['fresh_conditional_HIGH_evidence'],request['fresh_high_evidence'])
             and set(epoch['own_action_captures'])==set(src.ACTIONS)
             and epoch['unavailable_upstream_captures']=='UNACQUIRED_NOT_STAGED'and epoch['original_python_unchanged']is True
             and all(epoch[k]is False for k in('upstream_HIGH_acquired','support_acquisition_verified',
                                              'full_notebook57_completed','all_index_conclusion_verified')),'Typed acyclic current metadata/capture ledger')
    for kind in(['initial','replay','resource']if row['replay_prepared']else['initial','resource']):
        name,old,new,changes=src.prepared_projection(task,row,kind)
        src.need((task/'capsule'/name).read_bytes()==src.dump(new)
                 and same(epoch['prepared_derivations'][name],src.derivation_record(task,name,old,new,changes)),
                 'Strict PREPARED projection: only declared source/capture maps and n15 selected-candidate SHA metadata change')
    summaries=[]
    for record in report['actions']:
        src.need(type(record)is dict and set(record)=={'action','observed','inputs_before','inputs_after','outputs'},'Exact actual action record')
        action=record['action'];streams=transport(task,row,action,record['observed'],request,report['python_executable'])
        graph=src.input_map(task,row,action)
        src.need(same(record['inputs_before'],graph)and same(record['inputs_after'],graph),'All exact original inputs unchanged across the stopped action')
        outputs={name:src.digest(task/'capsule'/name)for name in src.outputs(row,action)}
        src.need(same(record['outputs'],outputs),'Every current stage output sealed after stop')
        native=numerical_reference(task,row,action)
        cap=task/'capsule'/src.capture_relative(row,action);meta=src.read(cap/'metadata.json',16*src.MIB)
        meta_fields={'schema','action','capture_origin','historical_capture_impersonated','command','cwd','input_sha256',
                     'outputs_sha256','returncode','elapsed_seconds','started_utc','finished_utc','python','platform',
                     'stdout_sha256','stderr_sha256'}
        src.need(type(meta)is dict and set(meta)==meta_fields and meta['schema']=='CURRENT_FINITE1519_CORE_GENUINE_ACTION_CAPTURE_V1'and meta['action']==action
                 and meta['capture_origin']=='CURRENT_STOPPED_LINUX_SUPERVISOR_EXECUTION'and meta['historical_capture_impersonated']is False
                 and same(meta['command'],command(row,action,report['python_executable']))
                 and meta['cwd']==original(request,'capsule/'+src.cwd_relative(row,action))
                 and type(meta['returncode'])is int and meta['returncode']==0
                 and same(meta['input_sha256'],src.relative_inputs(row,action,graph))and same(meta['outputs_sha256'],outputs)
                 and meta['python']==report['python_version']and type(meta['platform'])is str and bool(meta['platform']),
                 'Genuine current-context constructor/replay capture, never old-hash impersonation')
        finite(meta['elapsed_seconds'])
        for key in('started_utc','finished_utc'):src.need(type(meta[key])is str and bool(meta[key]),'Current execution time context')
        for stream in('stdout','stderr'):
            src.need((cap/(stream+'.txt')).read_bytes()==streams[stream].read_bytes()
                     and src.digest(cap/(stream+'.txt'))==meta[stream+'_sha256'],'Exact current copied native stream')
        text=streams['stdout'].read_text(encoding='utf-8');last=[l for l in text.splitlines()if l.strip()][-1]
        expected=(native['status']+f" {row['band']} "+src.digest(task/'capsule'/src.outputs(row,action)[0]))if action.startswith('initial_')else(
            ('RESOURCE_CANDIDATE'if action=='resource_construct'else'RESOURCE_ACCEPTED')+' '+row['band']+' '
            +str(native['status_counts'])+' '+src.digest(task/'capsule'/src.outputs(row,action)[0]))
        src.need(last==expected,'Actual original successful terminal output and whole output hash')
        src.need(same(epoch['own_action_captures'][action],dict(relative=src.capture_relative(row,action),
            metadata_sha256=src.digest(cap/'metadata.json'),stdout_sha256=src.digest(cap/'stdout.txt'),stderr_sha256=src.digest(cap/'stderr.txt'))),
            'Final epoch seals all genuine own captures')
        summaries.append(dict(action=action,status=native['status'],outputs_sha256=outputs))
    return dict(case_id=row['case_id'],n=row['n'],band=row['band'],native_actions=4,complete_INITIAL_covers=9,
        signed_cells_per_cover=row['signed_cells_per_cover'],resource_panels=100,support_radii=6,fresh_HIGH_input_evidence=request['fresh_high_evidence'],initial_controls=row['initial_controls'],
        resource_controls=row['resource_controls'],actions=summaries,metadata_epoch_sha256=src.digest(task/src.EPOCH),
        unavailable_upstream_captures='UNACQUIRED_NOT_STAGED')


def validate_completed(task):
    task=Path(task).resolve();report=src.read(task/'CASE_OBSERVED.json',32*src.MIB);summary=validate_run(task,report)
    done=src.read(task/'CASE_COMPLETED.json',32*src.MIB)
    fields={'schema','scope','case_id','implementation','observed_sha256','summary','artifacts','conditional_core_arithmetic_completed',*FLAGS}
    src.need(type(done)is dict and set(done)==fields and done['schema']==COMPLETED and done['scope']==SCOPE and done['case_id']==summary['case_id']
             and same(done['implementation'],implementation())and done['observed_sha256']==src.digest(task/'CASE_OBSERVED.json')
             and same(done['summary'],summary)and same(done['artifacts'],inventory(task))
             and done['conditional_core_arithmetic_completed']is True and all(done[k]is False for k in FLAGS),
             'Whole current four-call case, sources, provenance, captures and strict false conclusion flags')
    return dict(schema='REVALIDATED_FINITE1519_CORE_CASE_V1',scope=SCOPE,summary=summary,
        case_result_sha256=src.digest(task/'CASE_COMPLETED.json'),conditional_core_arithmetic_completed=True,**{k:False for k in FLAGS})
