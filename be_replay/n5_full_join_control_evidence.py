"""Pure stopped-execution reader for notebook67's22 original full actions."""
from __future__ import annotations
import json,re,math
from pathlib import Path
from . import n5_full_join_sources as src,n5_remaining_evidence as old

CPU_SECONDS=WALL_SECONDS=82800
MEMORY_BYTES=2*1024**3
DISK_BYTES=512*src.MIB
LOG_BYTES=16*src.MIB
SCHEMA='N5_FULL_JOIN_GROUP_COMPLETED_V1'
OBSERVED='N5_FULL_JOIN_GROUP_OBSERVED_V1'
FLAGS=('native_arithmetic_accepted','full_n5_verified','all_index_conclusion_verified')

def same(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b

def implementation():
    names=('n5_full_join.py','n5_full_join_sources.py','n5_full_join_control_evidence.py','n5_full_join_evidence.py','linux_supervisor.py')
    extra=('n5_full_join_inputs.py','n5_full_join_semantics.py')
    src.need(src.digest(src.PLAN)==src.PLAN_SHA256,'Actual immutable full source plan')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names+extra}|{'plan':src.PLAN_SHA256}

def inventory(task):
    out={}
    for p in sorted(Path(task).rglob('*')):
        src.ordinary(p)
        if p.is_file()and p.relative_to(task).as_posix()not in('OBSERVED.json','COMPLETED.json'):
            out[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return out

def mathematical_value(value,*,integration=False):
    # The two complete integration objects have one top-level wall-time field.
    # No other nested timing, graph or proof field is silently erased.
    if type(value)is not dict:return value
    return {k:v for k,v in value.items()if k!='files_sha256'and not(integration and k=='seconds')}

def output(action,task):
    capsule=Path(task)/'capsule';summaries=[]
    for name in action['outputs']:
        d=src.read(capsule/name,8*src.MIB);reference=action['expected_outputs'][name]
        src.need(type(d)is dict and type(reference)is dict and d.keys()==reference.keys(),
            'Whole exact original native output schema, including diagnostics/graph fields')
        if action['id']in('67.complement.construct','67.complement.replay'):
            src.need(type(d.get('seconds'))in(int,float)and math.isfinite(d['seconds'])and 0<=d['seconds']<=WALL_SECONDS,
                'Only one bounded top-level integration diagnostic time is ignored')
        src.need(same(mathematical_value(d,integration=action['id']in('67.complement.construct','67.complement.replay')),
                 mathematical_value(reference,integration=action['id']in('67.complement.construct','67.complement.replay'))),
                 'All original output fields, controls, strict targets and full census: '+action['id'])
        # Dynamic graphs bind actual newly written files; old reference hashes are never relabelled.
        graph=d.get('files_sha256',{})
        src.need(set(graph)==set(reference.get('files_sha256',{})),'Complete original output graph keys')
        for rel,pin in graph.items():
            src.parts(rel);p=capsule/rel;src.ordinary(p)
            src.need(p.is_file()and src.digest(p)==pin,'Actual source/capture output graph '+rel)
        summaries.append(dict(path=name,sha256=src.digest(capsule/name),status=d.get('status'),
                              original_graph_keys=len(graph)))
    return summaries

def capture(task,action,record):
    request=src.read(Path(task)/'REQUEST.json');origin=request['original_task_root'];p=Path(task)
    execution=p/'executions'/action['id'];observed=record['observed'];launch=src.read(execution/'launch.json')
    src.need(observed==src.read(execution/'supervisor-result.json')and observed.get('status')=='completed'
             and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('proof_accepted')is False,'Actual stopped full original process')
    src.need(launch['argv']==[record['python'],*action['argv']]and launch['mode']==observed['mode']=='untrusted_search'
             and old.mapped(p,launch['cwd'],origin)==p/'capsule'/action['cwd']
             and old.mapped(p,launch['output_dir'],origin)==execution,'Exact actual command/cwd/capture')
    for key,want in [('cpu_seconds',CPU_SECONDS),('wall_seconds',WALL_SECONDS),('memory_bytes',MEMORY_BYTES),
                     ('disk_bytes',DISK_BYTES),('log_bytes',LOG_BYTES),('heartbeat_seconds',20),('sample_seconds',.2)]:
        src.need(type(launch[key])in(int,float)and launch[key]==want,'Exact explicit67 per-action resource budget '+key)
    src.need(launch['checkpoint_paths']==[]and observed.get('checkpoints')==[], 'No substituted checkpoint output')
    progress=src.read(execution/'progress.json')
    expected_progress=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,
                           elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    src.need(same(progress,expected_progress),'Exact final stopped progress event and elapsed observation')
    lines=(execution/'progress.jsonl').read_text('utf-8').splitlines()
    src.need(lines and same(json.loads(lines[-1],object_pairs_hook=src.unique),expected_progress),
             'Final actual progress journal equals stopped supervisor event')
    for stream in('stdout','stderr'):
        f=old.mapped(p,observed[stream+'_path'],origin)
        src.need(f==execution/(stream+'.txt')and f.is_file()and f.stat().st_size<=LOG_BYTES
                 and src.digest(f)==observed[stream+'_sha256'],'Whole actual captured '+stream)
    src.need((execution/'stderr.txt').stat().st_size==0,'Empty successful original stderr')
    guard=observed['guard_scope'];wanted=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=WALL_SECONDS,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,
        sampled_group_CPU_limit_seconds=CPU_SECONDS,sampled_file_limit_bytes=DISK_BYTES,sampled_log_limit_bytes=LOG_BYTES,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    src.need(type(guard)is dict and guard.keys()==wanted.keys()and all(
        (type(guard[k])in(int,float)and math.isfinite(guard[k])and guard[k]==v)if type(v)is int else same(guard[k],v)
        for k,v in wanted.items())and type(observed.get('sample_count'))is int and observed['sample_count']>0,
        'Entire truthful BASIC guard contract, no native/cgroup promotion')
    label=action.get('capture_label')
    if label:
        base=p/'capsule/runs/cutoff5_20261020/high'/label;m=src.read(base/'metadata.json')
        src.need(m['command']==launch['argv']and m['cwd']==launch['cwd']and m['returncode']==0
                 and type(m['returncode'])is int and m['changed_inputs']==[],'Real original capture metadata')
        for stream in('stdout','stderr'):
            src.need((base/(stream+'.txt')).read_bytes()==(execution/(stream+'.txt')).read_bytes()
                     and m[stream+'_sha256']==observed[stream+'_sha256'],'Original slots hold actual stopped streams')
        cwd=p/'capsule'/action['cwd']
        for rel,pin in m['input_sha256'].items():src.parts(rel);src.need(src.digest(cwd/rel)==pin,'Exact actual source inputs consumed')
    return output(action,p)

def validate_observed(task,observed):
    request,g=src.verify(task)
    src.need(observed['schema']==OBSERVED and observed['group_id']==g['id']and observed['implementation']==implementation()
             and observed['conditional_arithmetic_completed']is False and all(observed[k]is False for k in FLAGS),
             'False-before-completed observed stage')
    rows=src.actions(g['id']);src.need([r['action_id']for r in observed['actions']]==g['action_ids'],'All fixed original actions')
    return [dict(action_id=a['id'],outputs=capture(task,a,r))for a,r in zip(rows,observed['actions'])]

def validate_completed(task):
    task=Path(task);observed=src.read(task/'OBSERVED.json',8*src.MIB);complete=src.read(task/'COMPLETED.json',64*src.MIB)
    summary=validate_observed(task,observed)
    src.need(complete['schema']==SCHEMA and complete['implementation']==implementation()
        and complete['observed_sha256']==src.digest(task/'OBSERVED.json')and complete['summary']==summary
        and complete['artifacts']==inventory(task)and complete['conditional_arithmetic_completed']is True
        and all(complete[k]is False for k in FLAGS),'Complete full original action graph and evidence, no theorem promotion')
    return dict(group_id=observed['group_id'],summary=summary,completed_sha256=src.digest(task/'COMPLETED.json'),
                conditional_arithmetic_completed=True,**{k:False for k in FLAGS})
