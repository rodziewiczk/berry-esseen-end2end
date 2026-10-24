"""Pure stopped evidence for59A; no original mathematical module is imported."""
from __future__ import annotations
import math,re
from fractions import Fraction
from pathlib import Path,PurePosixPath,PureWindowsPath
from . import finite2630_b1_sources as s

SCOPE='FULL_ORIGINAL_ACTUAL26_30_B1_SINE_FOURIER_CURRENT_LOCATION_BASIC_V1'
CPU,WALL,MEMORY=43200,54000,2048*s.MIB
DISK,LOG=512*s.MIB,16*s.MIB
FLAGS=('native_arithmetic_accepted','full_notebook59_completed','parent_acquisitions_verified',
       'global_predecessors_verified','all_index_conclusion_verified')
CONTROL_NAMES=['missingstrip','duplicatestrip','reorderstrips','missingn','wrongn','falseupper','changedrho',
 'false_D','false_A','false_zeta','weaktarget','wrongmesh','missingterms','missingmap','falsecutoff',
 'falsepredecessor','unknownfield','duplicatejsonkey']
ACCEPT='PASS_FRESH_EXACT_ACTUAL26_30_ALL_B1_SCALAR_SINE_PHASE_FOURIER'

def same(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b

def implementation():
    names=('finite2630_b1.py','finite2630_b1_sources.py','finite2630_b1_evidence.py',
           'finite1039_sources.py','n5_remaining_sources.py','linux_supervisor.py','colab_batch.py','environment.py')
    return {n:s.digest(s.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=s.PLAN_SHA256)

def pathclass(request):
    value=request['original_task_root'];s.need(type(value)is str and '\0'not in value,'Original task path')
    cls=PureWindowsPath if re.match(r'^[A-Za-z]:',value)else PurePosixPath
    s.need(cls(value).is_absolute()and '..'not in cls(value).parts,'Absolute originating task root');return cls

def original(request,name):return str(pathclass(request)(request['original_task_root']).joinpath(*s.parts(name)))

def mapped(task,request,value):
    cls=pathclass(request);s.need(type(value)is str and '\0'not in value,'Recorded path string')
    p=cls(value);s.need(p.is_absolute(),'Absolute originating path')
    try:rel=p.relative_to(cls(request['original_task_root']))
    except ValueError:raise ValueError('Evidence outside originating task root')
    s.need(rel.parts and all(x not in('.','..')for x in rel.parts),'Contained evidence path')
    return s.ordinary(Path(task).joinpath(*rel.parts))

def command(request,action,python):
    s.need(action in s.ACTIONS and type(python)is str and
           (PurePosixPath(python).is_absolute()or PureWindowsPath(python).is_absolute()),'Exact action and interpreter')
    return[python,'-B','-S',original(request,'capsule/'+s.NATIVE+'/protocol.py'),action]

def guard():
    return dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL),per_process_RLIMIT_AS_bytes=MEMORY,per_process_RLIMIT_CPU_seconds=CPU,
        aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY,
        sampled_group_CPU_limit_seconds=CPU,sampled_file_limit_bytes=DISK,sampled_log_limit_bytes=LOG,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)

def transport(task,request,action,observed,python):
    task=Path(task);directory=task/'executions'/action
    s.need(same(s.read(directory/'supervisor-result.json'),observed)and observed.get('status')=='completed'
           and type(observed.get('returncode'))is int and observed['returncode']==0
           and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
           and observed.get('proof_accepted')is False and same(observed.get('guard_scope'),guard())
           and type(observed.get('sample_count'))is int and observed['sample_count']>0,'Actual complete BASIC execution')
    for key in('elapsed_seconds','maximum_sampled_group_CPU_seconds','maximum_sampled_group_RSS_bytes'):
        value=observed[key];s.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite actual measurement')
    launch=s.read(directory/'launch.json');name=s.OUTPUTS[action];output=task/'capsule'/s.NATIVE/name
    s.need(set(launch)=={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes',
                        'checkpoint_paths','disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
           and same(launch['argv'],command(request,action,python))
           and mapped(task,request,launch['cwd'])==task/'capsule'/s.NATIVE
           and mapped(task,request,launch['output_dir'])==directory and launch['mode']=='untrusted_search'
           and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU
           and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY
           and type(launch['disk_bytes'])is int and launch['disk_bytes']==DISK
           and type(launch['log_bytes'])is int and launch['log_bytes']==LOG
           and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL
           and type(launch['sample_seconds'])in(int,float)and launch['sample_seconds']==.2
           and type(launch['heartbeat_seconds'])in(int,float)and launch['heartbeat_seconds']==20
           and type(launch['checkpoint_paths'])is list
           and [mapped(task,request,p)for p in launch['checkpoint_paths']]==[output],
           'Exact unchanged original command, working directory and output/budgets')
    paths={}
    for kind in('stdout','stderr'):
        p=mapped(task,request,observed[kind+'_path']);s.need(p==directory/(kind+'.txt')and p.is_file()
          and p.stat().st_size<=LOG and s.digest(p)==observed[kind+'_sha256'],'Actual bounded '+kind+' bytes');paths[kind]=p
    s.need(paths['stderr'].stat().st_size==0,'Successful original support stderr must be empty')
    packets=observed['checkpoints'];s.need(type(packets)is list and len(packets)==1,'One whole stopped original output')
    packet=packets[0];copied=directory/'checkpoints'/name
    s.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
           and packet['exists']is True and packet['trusted_certificate']is False
           and mapped(task,request,packet['source_path'])==output and mapped(task,request,packet['path'])==copied
           and s.ordinary(output).is_file()and s.ordinary(copied).is_file()
           and type(packet['bytes'])is int and 0<packet['bytes']<=128*s.MIB
           and packet['bytes']==output.stat().st_size==copied.stat().st_size
           and packet['sha256']==s.digest(output)==s.digest(copied),'Whole stopped output identity')
    final=dict(event='linux_supervisor_finished',stage='untrusted_search',status='completed',reason=None,
               elapsed_seconds=observed['elapsed_seconds'],proof_accepted=False)
    history=s.ordinary(directory/'progress.jsonl');s.need(history.is_file()and 0<history.stat().st_size<=LOG,'Bounded supervisor history')
    last=history.read_text(encoding='utf-8').splitlines()[-1]
    s.need(same(s.loads(last),final)and same(s.read(directory/'progress.json'),final),'Actual stopped supervisor progress')
    return s.read(output)

def results(task,request,candidate,receipt):
    c=Path(task)/'capsule';proof=c/s.NATIVE/'COVER.json';accepted=c/s.NATIVE/'ACCEPTED.json'
    record=s.read(c/s.RECORD)
    expected={k:v for k,v in record.items()if k not in('controls','input_sha256')}
    manifest=s.read(c/s.MANIFEST);source=dict(manifest_sha256=s.digest(c/s.MANIFEST),files_sha256=manifest['files_sha256'])
    s.need(set(candidate)=={'schema','target','inputs','pieces','source','mathematical_status','cutoff25_proved','global_predecessors_proved'}
           and candidate['schema']=='ACTUAL26_30_ALL_B1_SCALAR_SINE_PHASE_FOURIER_V1'
           and candidate['target']=='4097/10000'and same(candidate['inputs'],expected)and same(candidate['source'],source)
           and candidate['cutoff25_proved']is False and candidate['global_predecessors_proved']is False,
           'Complete original target, exact recomputed55-scope/23-strip inputs and current source map')
    s.need(type(candidate['pieces'])is list and len(candidate['pieces'])==23 and len(expected['acquired_scopes'])==55,
           'All original55 resources and all23 closed rational strips')
    uppers=[];previous=Fraction(11,10)
    for ordinal,(piece,row)in enumerate(zip(candidate['pieces'],expected['rows'])):
        lo,hi=map(Fraction,row['rho'])
        s.need(lo==previous and lo<hi<=Fraction(6,5),'Exact full closed B1 rho coverage');previous=hi
        s.need(set(piece)=={'id','cells_per_piece','result'}and piece['id']==row['id']==f'B1_sine_strip{ordinal:02d}'
               and type(piece['cells_per_piece'])is int and piece['cells_per_piece']in(256,512,1024),
               'Original ordered strip identities and full native mesh rule')
        rows=piece['result']['rows']
        s.need(type(rows)is list and len(rows)==5 and all(type(r['n'])is int for r in rows)
               and [r['n']for r in rows]==[26,27,28,29,30],'Every original actual index on every strip')
        for r in rows:
            s.need(type(r['normalized_upper'])is str,'Exact rational normalized upper');upper=Fraction(r['normalized_upper'])
            s.need(upper<Fraction(4097,10000),'Every exact normalized bound strictly below target');uppers.append(upper)
    s.need(previous==Fraction(6,5)and len(uppers)==115,'All115 exact Fourier rows and final closed seam')
    fields={'status','proof_sha256','source','target','maximum_upper','maximum_upper_float','exact_rows','rho_strips',
            'acquired_scopes','negative_controls','seconds','cutoff25_proved','global_predecessors_proved'}
    s.need(set(receipt)==fields and receipt['status']==ACCEPT and receipt['proof_sha256']==s.digest(proof)
           and same(receipt['source'],source)and receipt['target']=='4097/10000'
           and receipt['maximum_upper']==str(max(uppers))and type(receipt['maximum_upper_float'])is float
           and receipt['maximum_upper_float']==float(max(uppers))
           and type(receipt['exact_rows'])is int and receipt['exact_rows']==115
           and type(receipt['rho_strips'])is int and receipt['rho_strips']==23
           and same(receipt['acquired_scopes'],expected['acquired_scopes'])
           and same(receipt['negative_controls'],CONTROL_NAMES)
           and receipt['cutoff25_proved']is False and receipt['global_predecessors_proved']is False,
           'Full genuine original acceptance, complete native controls, unchanged conditional claims')
    finite(receipt['seconds'])
    for action in s.ACTIONS:
        lines=(Path(task)/'executions'/action/'stdout.txt').read_text('utf-8').splitlines()
        s.need(len([line for line in lines if line.startswith('EXACT_SCALAR_B1_STRIP ')])==23,'Actual full strip progress in each original pass')
        words=lines[-1].split()
        if action=='construct':
            s.need(len(words)==3 and words[:2]==['CONSTRUCTED_NOT_ACCEPTED',s.digest(proof)],'Original constructor terminal binds whole new proof')
        else:
            s.need(len(words)==5 and words[:2]==[ACCEPT,'115']and words[2]==str(receipt['maximum_upper_float'])
                   and words[3]=='18'and float(words[4])==receipt['seconds'],'Original full acceptance terminal')
        finite(float(words[-1]))
    return dict(actual_n=[26,27,28,29,30],rho=['11/10','6/5'],rho_strips=23,exact_rows=115,full_original_passes=2,
                native_negative_controls=18,selected_resource_scopes=55,maximum_upper=receipt['maximum_upper'],
                proof_sha256=s.digest(proof),acceptance_sha256=s.digest(accepted),location_epoch_sha256=s.digest(Path(task)/'LOCATION_EPOCH.json'))

def finite(value):s.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite ordinary elapsed value')
def inventory(task):
    task=Path(task);out={}
    for p in sorted(task.rglob('*')):
        s.ordinary(p);rel=p.relative_to(task).as_posix()
        if p.is_file()and rel not in('STAGE_OBSERVED.json','STAGE_COMPLETED.json'):
            out[rel]=dict(bytes=p.stat().st_size,sha256=s.digest(p))
    return out
def validate_run(task,report):
    task=Path(task).resolve();request=s.verify_job(task)
    s.need(set(report)=={'schema','scope','implementation','python_executable','python_version','actions',
                        'conditional_fourier_arithmetic_completed',*FLAGS}
           and report['schema']=='OBSERVED_FINITE2630_B1_V1'and report['scope']==SCOPE
           and same(report['implementation'],implementation())and report['conditional_fourier_arithmetic_completed']is False
           and all(report[k]is False for k in FLAGS)and type(report['python_version'])is str
           and type(report['actions'])is list and len(report['actions'])==2,'Whole actual two-pass conditional ledger')
    outputs=[]
    for action,row in zip(s.ACTIONS,report['actions']):
        s.need(set(row)=={'action','observed'}and row['action']==action,'Exactly both ordered original actions')
        outputs.append(transport(task,request,action,row['observed'],report['python_executable']))
    return results(task,request,*outputs)
def validate_completed(task):
    task=Path(task).resolve();observed=s.read(task/'STAGE_OBSERVED.json');summary=validate_run(task,observed)
    done=s.read(task/'STAGE_COMPLETED.json')
    s.need(set(done)=={'schema','scope','implementation','observed_sha256','summary','artifacts',
                      'conditional_fourier_arithmetic_completed',*FLAGS}
           and done['schema']=='COMPLETED_FINITE2630_B1_V1'and done['scope']==SCOPE
           and same(done['implementation'],implementation())and done['observed_sha256']==s.digest(task/'STAGE_OBSERVED.json')
           and same(done['summary'],summary)and same(done['artifacts'],inventory(task))
           and done['conditional_fourier_arithmetic_completed']is True and all(done[k]is False for k in FLAGS),
           'Whole stopped source/metadata/capture/output transaction without parent/global promotion')
    return dict(schema='REVALIDATED_FINITE2630_B1_V1',summary=summary,
                stage_result_sha256=s.digest(task/'STAGE_COMPLETED.json'),conditional_fourier_arithmetic_completed=True,
                **{k:False for k in FLAGS})
