"""Pure evidence readback for58G; no original numerical module imports."""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path,PurePosixPath,PureWindowsPath
import re
from . import finite1920_feedback_sources as src
from .finite1039_count_evidence import same,mapped,terminal,inventory

SCOPE='UNCHANGED_CONDITIONAL_SUPPORTED19_20_FOURIER_BASIC_SUBLANE_V1'
OBSERVED='OBSERVED_FINITE1920_FEEDBACK_SUBLANE_V1'
COMPLETED='COMPLETED_FINITE1920_FEEDBACK_SUBLANE_V1'
CPU_SECONDS,WALL_SECONDS,MEMORY_BYTES=43200,54000,2048*src.MIB
FLAGS=('native_arithmetic_accepted','full_notebook58_completed','actual20_sharp_verified','predecessor_verified','parent_acquisitions_verified',
       'support_high_initial_resource_acquired','support_acquisition_verified','resource_to_count163_interfaces_verified','all_index_conclusion_verified')


def implementation():
    names=('finite1920_feedback.py','finite1920_feedback_sources.py','finite1920_feedback_evidence.py',
           'finite1039_sources.py','finite1039_count_evidence.py','n5_remaining_sources.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|dict(source_plan_sha256=src.PLAN_SHA256)


def original_path(request,relative):
    root=request['original_task_root'];cls=PureWindowsPath if re.match(r'^[A-Za-z]:',root)else PurePosixPath
    src.need(cls(root).is_absolute(),'Recorded absolute originating task root')
    return str(cls(root)/'capsule'/relative)


def command(request,action,python):
    src.need(action in src.ACTIONS and type(python)is str and (PureWindowsPath(python).is_absolute()or PurePosixPath(python).is_absolute()),'Exact action and original interpreter')
    if action=='readback':return [python,'-B','-S',original_path(request,src.AUDIT+'/readback.py'),original_path(request,src.REQUEST)]
    argv=[python,'-B','-S',original_path(request,src.NATIVE+'/run.py'),action,src.LABELS[action]]
    if action!='plan':argv.append(original_path(request,src.RUNS+'/plan01/PLAN.json'))
    return argv


def finite(value):
    src.need(type(value)in(int,float)and math.isfinite(value)and value>=0,'Finite nonnegative execution display');return value


def transport(task,request,action,observed,report):
    task=Path(task);original=request['original_task_root'];directory=task/'executions'/action
    src.need(same(src.read(directory/'supervisor-result.json'),observed)
             and observed.get('status')=='completed'and type(observed.get('returncode'))is int and observed['returncode']==0
             and observed.get('reason')is None and observed.get('mode')=='untrusted_search'
             and observed.get('proof_accepted')is False and type(observed.get('sample_count'))is int and observed['sample_count']>0,
             'Actual successful stopped BASIC execution for '+action)
    for k in('elapsed_seconds','maximum_sampled_group_RSS_bytes','maximum_sampled_group_CPU_seconds'):finite(observed[k])
    launch=src.read(directory/'launch.json')
    fields={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
            'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
    outputs=src.output_paths(action)
    src.need(set(launch)==fields and same(launch['argv'],command(request,action,report['python_executable']))
             and mapped(task,launch['cwd'],original)==task/'capsule'
             and mapped(task,launch['output_dir'],original)==directory and launch['mode']=='untrusted_search'
             and type(launch['cpu_seconds'])is int and launch['cpu_seconds']==CPU_SECONDS
             and type(launch['memory_bytes'])is int and launch['memory_bytes']==MEMORY_BYTES
             and type(launch['wall_seconds'])in(int,float)and launch['wall_seconds']==WALL_SECONDS
             and type(launch['disk_bytes'])is int and launch['disk_bytes']==512*src.MIB
             and type(launch['log_bytes'])is int and launch['log_bytes']==16*src.MIB
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,v,original)for v in launch['checkpoint_paths']]==[task/'capsule'/p for p in outputs],
             'Exact original action, source cwd, capture requests and documented budgets')
    scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,
        external_wall_seconds=float(WALL_SECONDS),per_process_RLIMIT_AS_bytes=MEMORY_BYTES,
        per_process_RLIMIT_CPU_seconds=CPU_SECONDS,aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,
        sampled_group_RSS_limit_bytes=MEMORY_BYTES,sampled_group_CPU_limit_seconds=CPU_SECONDS,
        sampled_file_limit_bytes=512*src.MIB,sampled_log_limit_bytes=16*src.MIB,
        descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(observed['guard_scope'],scope),'Honest process-tree BASIC policy, without a native promotion')
    captures={}
    for kind in('stdout','stderr'):
        p=mapped(task,observed[kind+'_path'],original)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==observed[kind+'_sha256'],'Actual captured '+kind+' bytes')
        captures[kind]=p
    src.need(captures['stderr'].stat().st_size==0,'Successful original stderr is empty')
    checks=observed['checkpoints'];src.need(type(checks)is list and len(checks)==len(outputs),'Every stopped native output copied')
    for packet,name in zip(checks,outputs):
        p=task/'capsule'/name;copied=directory/'checkpoints'/name
        src.need(set(packet)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}
                 and packet['exists']is True and packet['trusted_certificate']is False
                 and mapped(task,packet['source_path'],original)==p and mapped(task,packet['path'],original)==copied
                 and p.is_file()and copied.is_file()and type(packet['bytes'])is int
                 and packet['bytes']==p.stat().st_size==copied.stat().st_size
                 and packet['sha256']==src.digest(p)==src.digest(copied),'Whole stopped native output identity: '+name)
    return captures['stdout'].read_text('utf-8')


def inner_capture(task,request,action,report,outer_stdout):
    c=Path(task)/'capsule';d=c/src.RUNS/src.LABELS[action];m=src.read(d/'metadata.json')
    result='PLAN.json'if action=='plan'else'RESULT.json';p=d/result
    native_manifest=src.read(c/src.NATIVE/'MANIFEST.json');inputs=dict(native_manifest['files_sha256'])
    inputs[src.NATIVE+'/MANIFEST.json']=src.digest(c/src.NATIVE/'MANIFEST.json')
    if action=='plan':argv=[report['python_executable'],'-B','planner.py',original_path(request,src.RUNS+'/plan01/PLAN.json')]
    else:
        inputs[src.RUNS+'/plan01/PLAN.json']=src.digest(c/src.RUNS/'plan01/PLAN.json')
        argv=[report['python_executable'],'-B','protocol.py',action,
              original_path(request,src.RUNS+'/plan01/PLAN.json'),original_path(request,src.RUNS+'/'+src.LABELS[action]+'/RESULT.json')]
    fields={'command','cwd','input_sha256','python','platform','started_utc','returncode','elapsed_seconds','finished_utc',
            'changed_inputs','stdout_sha256','stderr_sha256',result+'_sha256'}
    src.need(set(m)==fields and same(m['command'],argv)and m['cwd']==original_path(request,src.NATIVE)
             and same(m['input_sha256'],inputs)and m['python']==report['python_version']
             and type(m['platform'])is str and bool(m['platform'])
             and type(m['returncode'])is int and m['returncode']==0 and m['changed_inputs']==[]
             and m[result+'_sha256']==src.digest(p),'Genuine current original child command/source/result capture')
    finite(m['elapsed_seconds'])
    for key in('started_utc','finished_utc'):src.need(type(m[key])is str and bool(m[key]),'Original child time context')
    for kind in('stdout','stderr'):
        src.need(src.digest(d/(kind+'.txt'))==m[kind+'_sha256'],'Actual original child stream SHA')
    src.need((d/'stderr.txt').stat().st_size==0 and (d/'stdout.txt').read_text('utf-8')==outer_stdout,
             'Actual original child stdout propagates through the source-pinned run wrapper')
    return src.read(p,limit=128*src.MIB)


BANDS=[dict(name='B0',rho=['1','11/10'],target='831/2000'),
       dict(name='BN',rho=['11/10','9/8'],target='103/250')]
THEOREM=('For every standardized real iid marginal with |X|<=3, each literal n=19,20 '
         'has normalized Kolmogorov score <831/2000 on rho[1,11/10], and <103/250 on rho[11/10,9/8]. '
         'The support premise is explicit, not acquired here.')
MATHEMATICAL_STATUS=THEOREM+' Conditional on the external Prawitz input; no acquired support, new contact allowance or sharp20 claim.'
EXECUTION_STATUS=('Fresh independent coverage/scalar/normalization/source/capture acceptance of native construction and full replay. '
                  'Fourier quadrature was reproduced natively, not recomputed here.')


def plan_census(p):
    src.need(type(p)is dict and set(p)=={'schema','n','support_absolute_upper','bands'}
             and p['schema']=='SAME_LAW1920_SUPPORTED_B0_BN_PLAN_V1'
             and same(p['n'],[19,20])and p['support_absolute_upper']=='3'
             and type(p['bands'])is list and len(p['bands'])==2,'Complete original supported two-band untrusted plan')
    counts={}
    for band,expected in zip(p['bands'],BANDS):
        src.need(type(band)is dict and set(band)=={'name','rho','target','strips'}
                 and same({k:band[k]for k in expected},expected)and type(band['strips'])is list
                 and 0<len(band['strips'])<=10000,'Literal closed band, target and nonempty finite cover')
        cursor,right=map(F,expected['rho'])
        for row in band['strips']:
            src.need(type(row)is dict and set(row)=={'rho','c','tau','heuristic_upper'}and type(row['rho'])is list
                     and len(row['rho'])==2 and all(type(v)is str for v in row['rho']+[row['c'],row['tau']]),'Original plan strip fields')
            lo,hi=map(F,row['rho']);c,tau=F(row['c']),F(row['tau'])
            src.need(str(lo)==row['rho'][0]and str(hi)==row['rho'][1]and lo==cursor<hi<=right and 9<=lo*lo+8
                     and str(c)==row['c']and str(tau)==row['tau']and 0<c<F(3141592653589793238462643383279,10**30)
                     and F(1,1024)<tau<=F(3,10),'Exact closed seams, radius3 gate and original frequency domains')
            src.need(type(row['heuristic_upper'])in(int,float)and math.isfinite(row['heuristic_upper']),'Untrusted finite discovery display')
            cursor=hi
        src.need(cursor==right,'Complete last closed band endpoint');counts[band['name']]=len(band['strips'])
    return counts


def native_rows(result,plan):
    """Bind every reported row/attempt; interval arithmetic stays in the original readback."""
    fields={'n','rho','eta_upper','zeta_lower','imaginary_square_coefficient','kappa','c','tau',
            'epsilon','cells_per_piece','normalized_upper','normalized_upper_float','terms',
            'band','strip_index','target','strict_target_pass','support_absolute_upper'}
    allowed={'darboux_fallback'}|{'one','line','curve','coordinate'}|{
        m+'/'+side for m in('one','line','curve','coordinate')for side in('left','right','constant')}
    maxima={b['name']:{str(n):[] for n in(19,20)}for b in BANDS}
    rows=result['rows'];attempts=result['attempts'];position=0;cursor=0
    def row_check(row,band,index,strip,n,mesh):
        src.need(type(row)is dict and set(row)==fields and type(row['n'])is int and row['n']==n
                 and type(row['strip_index'])is int and row['strip_index']==index and row['band']==band['name']
                 and same(row['rho'],strip['rho'])and row['c']==strip['c']and row['tau']==strip['tau']
                 and row['target']==band['target']and row['support_absolute_upper']=='3'
                 and row['kappa']=='62/625'and row['epsilon']=='1/1024'
                 and type(row['cells_per_piece'])is int and row['cells_per_piece']==mesh,
                 'Complete actual19/20 row, literal strip/parameters and source-profile constants')
        def rational(value):
            src.need(type(value)is str,'Rational row metadata');v=F(value)
            src.need(str(v)==value,'Canonical exact row metadata');return v
        for name in('eta_upper','zeta_lower','imaginary_square_coefficient'):rational(row[name])
        src.need(type(row['terms'])is dict and set(row['terms'])=={'low','normal','high','tail'}
                 and all(rational(v)>=0 for v in row['terms'].values()),'All four exact native terms')
        upper=rational(row['normalized_upper'])
        src.need(upper>=0 and type(row['strict_target_pass'])is bool
                 and row['strict_target_pass']==(upper<F(band['target'])),'Strict per-band target truth')
        finite(row['normalized_upper_float']);return upper
    for band in plan['bands']:
        for index,strip in enumerate(band['strips']):
            final=rows[position:position+2];position+=2
            src.need(len(final)==2 and type(final[0])is dict,'Two full final actual-index rows')
            mesh=final[0].get('cells_per_piece');src.need(type(mesh)is int and mesh in(128,256,512,1024),'Original final mesh')
            values=[row_check(row,band,index,strip,n,mesh)for row,n in zip(final,(19,20))]
            src.need(all(v<F(band['target'])for v in values),'Every selected final row is strictly closed')
            for n,v in zip((19,20),values):maxima[band['name']][str(n)].append(v)
            for trial in(128,256,512,1024):
                src.need(cursor<len(attempts),'All preceding attempted meshes retained');a=attempts[cursor];cursor+=1
                src.need(type(a)is dict and set(a)=={'band','strip_index','mesh','rows','branch_statistics','strict_target_pass'}
                         and a['band']==band['name']and type(a['strip_index'])is int and a['strip_index']==index
                         and type(a['mesh'])is int and a['mesh']==trial and type(a['rows'])is list and len(a['rows'])==2,
                         'Full deterministic two-index attempt path')
                vals=[row_check(row,band,index,strip,n,trial)for row,n in zip(a['rows'],(19,20))]
                passed=all(v<F(band['target'])for v in vals);stats=a['branch_statistics']
                src.need(type(a['strict_target_pass'])is bool and a['strict_target_pass']==passed
                         and type(stats)is dict and bool(stats)and set(stats)<=allowed
                         and all(type(v)is int and v>0 for v in stats.values())and sum(stats.values())==2*trial,
                         'Typed complete attempted integration-cell accounting')
                if trial==mesh:
                    src.need(passed and same(a['rows'],final),'First successful full attempt equals final rows');break
                src.need(not passed,'No earlier successful attempt silently omitted')
    src.need(position==len(rows)and cursor==len(attempts),'No omitted, duplicated or unused native rows/attempts')
    expected={b:{n:str(max(v))for n,v in ns.items()}for b,ns in maxima.items()}
    src.need(same(result['per_band_per_n_upper'],expected),'Actual final-row maxima for both bands and indices')


def summarize(task,request,report,stdout):
    c=Path(task)/'capsule';p=inner_capture(task,request,'plan',report,stdout['plan']);strips=plan_census(p)
    construction=inner_capture(task,request,'construct',report,stdout['construct'])
    replay=inner_capture(task,request,'replay',report,stdout['replay'])
    src.need('seconds'in construction and 'seconds'in replay
             and same({k:v for k,v in construction.items()if k!='seconds'},
                      {k:v for k,v in replay.items()if k!='seconds'}),'Whole exact native construction/replay equality')
    expected_rows=[(band['name'],i,n)for band in BANDS for i in range(strips[band['name']])for n in (19,20)]
    for result in(construction,replay):
        finite(result['seconds'])
        src.need(set(result)=={'status','theorem','n','support_absolute_upper','bands','rows','attempts',
                              'per_band_per_n_upper','controls','plan_sha256','manifest_sha256','seconds'}
                 and result['status']=='EXACT_SUPPORTED_SAME_LAW1920_WHOLE_B0_BN_PASS'and result['theorem']==THEOREM
                 and same(result['n'],[19,20])and result['support_absolute_upper']=='3'and same(result['bands'],BANDS)
                 and type(result['rows'])is list and len(result['rows'])==2*sum(strips.values())
                 and type(result['attempts'])is list and len(result['attempts'])>=sum(strips.values())
                 and same(result['controls'],dict(negative_controls=17,finite_sum_identities=8))
                 and result['plan_sha256']==src.digest(c/src.RUNS/'plan01/PLAN.json')
                 and result['manifest_sha256']==src.plan()['original_manifest_sha256'],
                 'Full native exact rows, two supported targets, complete controls and input commitments')
        src.need(same([(r['band'],r['strip_index'],r['n'])for r in result['rows']],expected_rows),
                 'Every literal index in every band strip, without gaps or duplicates')
        native_rows(result,p)
        maxima=result['per_band_per_n_upper']
        src.need(type(maxima)is dict and set(maxima)=={'B0','BN'},'Both full native band maxima')
        for band in BANDS:
            values=maxima[band['name']]
            src.need(type(values)is dict and set(values)=={str(n)for n in (19,20)}
                     and all(type(v)is str and str(F(v))==v and 0<=F(v)<F(band['target'])for v in values.values()),
                     'Each literal-index exact native maximum is below its own band target')
    src.need((c/src.REQUEST).read_bytes()==src.dump(src.fresh_request(task)),'Readback request derives only from current real outputs')
    result=src.read(c/src.RESULT,limit=128*src.MIB)
    src.need(set(result)=={'status','mathematical_status','execution_status','n','support_absolute_upper','bands','strips',
                          'exact_rows','attempts','per_band_per_n_upper','negative_controls','sharp20_proved','cutoff20_proved','files_sha256'}
             and same(terminal(stdout['readback']),{k:v for k,v in result.items()if k!='files_sha256'})
             and result['status']=='PASS_INDEPENDENT_SUPPORTED_SAME_LAW1920_TWO_BAND_READBACK'
             and result['mathematical_status']==MATHEMATICAL_STATUS and result['execution_status']==EXECUTION_STATUS
             and same(result['n'],[19,20])and result['support_absolute_upper']=='3'and same(result['bands'],BANDS)
             and same(result['strips'],strips)and type(result['exact_rows'])is int and result['exact_rows']==2*sum(strips.values())
             and type(result['attempts'])is int and result['attempts']==len(construction['attempts'])
             and type(result['negative_controls'])is int and result['negative_controls']==33
             and result['sharp20_proved']is False and result['cutoff20_proved']is False
             and same(result['per_band_per_n_upper'],construction['per_band_per_n_upper']),
             'Actual independent readback terminal/whole receipt, supported domain/census and33controls')
    graph=dict(src.read(c/src.NATIVE/'MANIFEST.json')['files_sha256'])
    for name in[src.NATIVE+'/MANIFEST.json',src.RUNS+'/plan01/PLAN.json',src.REQUEST,src.AUDIT+'/readback.py',src.AUDIT+'/REVIEW.txt']+src.output_paths('construct')+src.output_paths('replay'):
        graph[name]=src.digest(c/name)
    src.need(same(result['files_sha256'],graph),'Complete original readback source/current-capture graph')
    found={p.relative_to(c).as_posix()for p in c.rglob('*')if p.is_file()}
    src.need(found==set(request['sources'])|{src.REQUEST}|{n for a in src.ACTIONS for n in src.output_paths(a)},
             'Complete final sealed74-input capsule and exactly declared fresh outputs')
    return dict(schema='CONDITIONAL_SUPPORTED19_20_ARITHMETIC_ONLY_V1',n=[19,20],support_absolute_upper='3',bands=BANDS,
                strips=strips,exact_rows=2*sum(strips.values()),native_controls=17,finite_sum_identities=8,
                independent_controls=33,per_band_per_n_upper=result['per_band_per_n_upper'],
                plan_sha256=src.digest(c/src.RUNS/'plan01/PLAN.json'),readback_sha256=src.digest(c/src.RESULT),
                original_manifest_sha256=src.plan()['original_manifest_sha256'],source_plan_sha256=src.PLAN_SHA256,
                conditional_premises=['The standardized real iid marginal has absolute support at most3',
                                      'Original pointwise Prawitz/Fourier reduction and analytic kappa lemmas'],
                **{f:False for f in FLAGS})


def validate_run(task,report):
    task=Path(task);request=src.verify_job(task)
    src.need(report['schema']==OBSERVED and report['scope']==SCOPE and same(report['implementation'],implementation())
             and report['original_task_root']==request['original_task_root']
             and report['conditional_same_law_fourier_arithmetic_completed']is False and all(report[f]is False for f in FLAGS)
             and [x['action']for x in report['actions']]==list(src.ACTIONS),'Exact4-action observed-false implementation epoch')
    context=src.read(task/'DISCOVERY_CONTEXT.json')
    src.need(same(context,report['discovery_context'])and context['distribution']=='numpy'
             and context['scope']=='UNTRUSTED_FLOATING_DISCOVERY_ONLY'and context['acceptance_arithmetic_depends_on_numpy']is False
             and same(context['thread_environment'],{n:'1'for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')})
             and type(context['version'])is str and bool(context['version'])
             and type(context['entry_sha256'])is str and re.fullmatch('[0-9a-f]{64}',context['entry_sha256']),
             'Explicit installed NumPy discovery context, without an exact-arithmetic claim')
    outputs={x['action']:transport(task,request,x['action'],x['observed'],report)for x in report['actions']}
    result=summarize(task,request,report,outputs);src.verify_job(task);return result


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_job(task)
    src.need(original_task_root is None or str(original_task_root)==request['original_task_root'],'One original absolute task context')
    report=src.read(task/'STAGE_OBSERVED.json');complete=src.read(task/'STAGE_COMPLETED.json',limit=32*src.MIB)
    summary=validate_run(task,report)
    src.need(complete['schema']==COMPLETED and complete['scope']==SCOPE
             and same(complete['implementation'],report['implementation'])
             and complete['observed_sha256']==src.digest(task/'STAGE_OBSERVED.json')
             and complete['conditional_same_law_fourier_arithmetic_completed']is True and same(complete['summary'],summary)
             and same(complete['artifacts'],inventory(task))and all(complete[f]is False for f in FLAGS),
             'All four genuine stopped actions and exact source/capture/output inventory')
    return dict(schema='REVALIDATED_CONDITIONAL_SUPPORTED19_20_SUBLANE_V1',summary=summary,
                source_plan_sha256=src.PLAN_SHA256,stage_result_sha256=src.digest(task/'STAGE_COMPLETED.json'),
                original_task_root=request['original_task_root'],conditional_same_law_fourier_arithmetic_completed=True,
                **{f:False for f in FLAGS})
