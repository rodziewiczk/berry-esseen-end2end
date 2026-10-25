"""Pure complete08/11/13/35 admission for67; never execute an original kernel."""
from __future__ import annotations
from pathlib import Path,PurePosixPath
from . import n5_full_join_sources as src,n5_remaining_evidence as old
from .n5_full_join_control_evidence import same

def mapped(root,value,origin):return old.mapped(Path(root),value,origin)

def stopped(root,origin,execution,observed):
    execution=Path(execution)
    src.need(same(src.read(execution/'supervisor-result.json'),observed)
        and observed.get('status')=='completed'and type(observed.get('returncode'))is int
        and observed['returncode']==0 and observed.get('reason')is None
        and observed.get('proof_accepted')is False,'Actual complete upstream stopped execution')
    for stream in('stdout','stderr'):
        p=mapped(root,observed[stream+'_path'],origin)
        src.need(p==execution/(stream+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
            and src.digest(p)==observed[stream+'_sha256'],'Actual upstream stream SHA and context')
    src.need((execution/'stderr.txt').stat().st_size==0,'Empty successful upstream stderr')
    launch=src.read(execution/'launch.json')
    src.need(launch['mode']==observed['mode']and type(launch['argv'])is list and '-B'in launch['argv']
        and not any(a in launch['argv']for a in('-O','-OO')),'Exact ordinary upstream Python command')
    src.need(mapped(root,launch['output_dir'],origin)==execution,'Same upstream execution slot')
    return launch,(execution/'stdout.txt').read_text('utf-8')

def validate08(root):
    from . import small_indices as small
    root=Path(root);session=src.read(root/'SESSION_RESULT.json');d=session['arithmetic_result'];origin=session['work']
    src.need(session['scope']=='COLAB_N2_N3_ARITHMETIC_NOT_ALL_INDEX_PROOF'
        and d['all_selected_stages_computed']is True and d['all_required_stages_selected']is True
        and d['context']['selected_stages']==list(small.STAGES)
        and d['context']['source_manifest_sha256']==small.MANIFEST_SHA256
        and d['context']['driver_sha256']==src.digest(src.ROOT/'be_replay/small_indices.py'),
        'Entire quantitative n2/n3 source epoch and all six physical stages')
    small.verify_vendor(root/'arithmetic/work/source')
    driver=root/'arithmetic/work/small_indices_driver.py'
    src.need(src.digest(driver)==d['context']['driver_sha256'],'Actual complete small-index driver')
    src.need(d['conditional_bound_targets']=={'n2':'2*sqrt(2)/7','n3':'59*sqrt(3)/250'},
        'Strong quantitative G3; CE-only predecessor is insufficient')
    src.need([r['stage']for r in d['rows']]==list(small.STAGES),'Every quantitative08 stage in order')
    for row in d['rows']:
        stage=row['stage'];execution=root/'arithmetic/stages'/stage
        launch,text=stopped(root,origin,execution,row['execution'])
        checked=small.validate_output(stage,text)
        src.need(all(same(row[k],v)for k,v in checked.items()),'Full observed small-index cell/control census')
        config=root/'arithmetic/work'/(stage+'-worker.json');cfg=src.read(config)
        src.need(launch['argv']==[launch['argv'][0],'-B','-S',str(PurePosixPath(origin)/'arithmetic/work/small_indices_driver.py'),
            '--_worker',str(PurePosixPath(origin)/'arithmetic/work'/(stage+'-worker.json'))]
            and mapped(root,launch['cwd'],origin)==root/'arithmetic/work','Exact original stage worker and cwd')
        src.need(cfg['stage']==stage,'Same selected actual small-index worker')
        if stage=='n3-full':
            expected=[src.digest(root/'arithmetic/work/source/n3/certificate'/f'{i:03d}.json')for i in range(111)]
            src.need(checked['n3_source_cell_hashes']==expected,'All111 actual n3 certificate cell identities')
    return dict(notebook='08',conditional_targets=d['conditional_bound_targets'],stages=6,n2_cells=70,n3_cells=111,
                statement='C2<=2*sqrt(2)/7 and C3<=59*sqrt(3)/250 under the explicit unrestricted analytic reductions',
                all_law_theorems_verified=False,session_sha256=src.digest(root/'SESSION_RESULT.json'))

def validate11(root):
    from . import root4
    root=Path(root);session=src.read(root/'SESSION_RESULT.json');origin=session['work'];report=src.read(root/'arithmetic/ROOT4_RESULT.json')
    src.need(same(report,session['arithmetic_result'])and report['schema']=='ROOT4_TWO_FRESH_FULL_PASSES_V1'
        and report['source_epoch_sha256']==root4.EPOCH_SHA256 and report['all_required_stages_computed']is True,
        'Actual complete two-pass ROOT4 source epoch')
    capsule=root/'arithmetic/capsule';root4.verify_capsule(capsule)
    src.need([r['stage']for r in report['stages']]==['produce','replay'],'Both entire ROOT4 passes')
    for row in report['stages']:
        launch,text=stopped(root,origin,root/'arithmetic'/(row['stage']+'-execution'),row['observed'])
        packet=old.json_suffix(text)
        src.need(same(packet,row['terminal_result']),'Entire ROOT4 actual terminal packet')
        checked=root4.validate_terminal(packet,row['stage'],PurePosixPath(origin)/'arithmetic/capsule')
        src.need(checked['conditional_target_closed']is True and checked['unresolved_geometry_indices']==[]
            and checked['root_bound_exact']==row['root_bound_exact'],'All260 closed ROOT4 parents and target')
        src.need(root4.guard_verified(row['observed'],capsule),'Full actual ROOT4 single-process guard')
        for key,file in [('worker_guard','native-worker-guard.json'),('supervisor_guard','native-controller-guard.json')]:
            src.need(same(row['observed']['guard_scope'][key],src.read(root/'arithmetic'/(row['stage']+'-execution')/file)),
                'Actual upstream kernel guard receipt')
        src.need(src.digest(capsule/root4.OUTPUT_NAME)==row['receipt_sha256'],'Both passes bind the entire ROOT4 certificate')
        execution=root/'arithmetic'/(row['stage']+'-execution');native_launch=src.read(execution/'native-launch.json')
        entry=str(PurePosixPath(origin)/'arithmetic/capsule'/root4.ENTRY)
        expected=[native_launch['argv'][0],'-B','-S',entry,'--produce'if row['stage']=='produce'else'--replay-existing']
        src.need(native_launch['argv']==expected and mapped(root,native_launch['cwd'],origin)==capsule
            and mapped(root,native_launch['output_dir'],origin)==execution
            and launch['argv'][1:3]==['-B','-S']and launch['argv'][-2]=='--_native-controller'
            and mapped(root,launch['argv'][-1],origin)==execution/'native-launch.json',
            'Actual outer guard controller and exact whole ROOT4 native payload')
    return dict(notebook='11',full_passes=2,parents=260,HIGH_slots=1300,bound='4097/10000',
        required_predecessor='C3<=59*sqrt(3)/250',all_law_C4_verified=False,session_sha256=src.digest(root/'SESSION_RESULT.json'))

def validate13(root):
    from . import n5_gapfree as gap
    root=Path(root);session=src.read(root/'SESSION_RESULT.json');task=root/'task';report=src.read(task/'EXECUTION_RESULT.json')
    src.need(same(report,session['result'])and report['status']==gap.ACCEPTED,'Complete actual corner result')
    # The original runtime paths remain unchanged in the archive. Interpret the
    # one originating task prefix instead of rewriting capture JSON.
    launch=src.read(task/'execution/launch.json');origin=str(PurePosixPath(launch['cwd']).parents[2])
    launch,text=stopped(task,origin,task/'execution',report['observed'])
    capsule=task/'arithmetic/private/capsule';manifest=gap.verify_sources(capsule,capsule=True,outputs={gap.OLD_RESULT,gap.RESULT})
    gap.census(capsule);details=gap.validate_original(src.read(capsule/gap.OLD_RESULT),manifest)
    native=src.read(capsule/gap.RESULT);src.need(same(native,report['native_result'])and same(old.json_suffix(text),native),
        'Whole actual stopped corner native packet')
    from .small_indices import trusted_guard
    src.need(trusted_guard(report['observed'],script_sha=src.digest(capsule/gap.ENTRY),
        supervisor_sha=src.digest(src.ROOT/'be_replay/linux_supervisor.py'),memory_bytes=512*src.MIB,cpu_seconds=report['cpu_seconds']),
        'Actual entire corner native guard')
    native_launch=src.read(task/'execution/native-launch.json')
    src.need(native_launch['argv'][1:]==['-B','-S',str(PurePosixPath(origin)/'arithmetic/private/capsule'/gap.ENTRY),'--_worker']
        and launch['argv'][-2]=='--_native-controller'and mapped(task,launch['argv'][-1],origin)==task/'execution/native-launch.json',
        'Exact original corner payload and guarded controller')
    src.need(native['original_controls']==gap.ORIGINAL_CONTROLS and native['added_controls']==gap.ADDED_CONTROLS
        and native['domain']==gap.DOMAIN and native['census']==gap.CENSUS and type(native['control_count'])is int
        and native['control_count']==21 and all(same(native[k],v)for k,v in details.items()),'All corner roots, both rays and controls')
    return dict(notebook='13',domain=gap.DOMAIN,census=gap.CENSUS,**details,session_sha256=src.digest(root/'SESSION_RESULT.json'))

def validate35(root):
    root=Path(root);session=src.read(root/'SESSION_RESULT.json',64*src.MIB)
    src.need(session['schema']=='CONDITIONAL_N5_REMAINING_BATCH_V1'and len(session['jobs'])==326,
        'Full326-stage35 export; an incomplete prefix cannot be promoted')
    declared=[r['job_id']for r in session['jobs']];expected=[r['job_id']for r in old.src.jobs()]
    src.need(declared==expected,'Every selected support/HIGH/owncap/INITIAL/resource/COUNT/complement stage')
    selected_pins={r['job_id']:r['validated']['stage_result_sha256']for r in session['jobs']}
    candidates={key:[]for key in expected}
    for ledger in(root/'jobs').rglob('STAGE_COMPLETED.json'):
        src.ordinary(ledger);pin=src.digest(ledger)
        # restore_stage retains rejected cache attempts for diagnosis. Only the
        # exact ledger selected by the final326-job session can be an input.
        for job,wanted in selected_pins.items():
            if pin==wanted:candidates[job].append(ledger.parent)
    src.need(all(candidates.values()),'All326 exact final-selected35 ledgers exist')
    checked={}
    for declared_row in session['jobs']:
        job=declared_row['job_id'];chosen=None
        for task in sorted(candidates[job],key=lambda p:p.as_posix()):
            try:
                value=old.validate_completed(task)
                src.need(same(value,declared_row['validated']),'Whole current35 stage readback matches exported original summary')
                chosen=dict(task=task,checked=value,row=old.src.job(job));break
            except (ValueError,KeyError,TypeError,OSError):continue
        src.need(chosen is not None,'The exact final-selected35 stage is fully source/capture-valid: '+job)
        checked[job]=chosen
    src.need(sum(r['row']['census']['leaves']for r in checked.values()if r['row']['kind']=='count')==75178,
        'All75178 accepted current35 leaves')
    return checked

def reference(frame,position=0):
    r=frame['checked']['summary']['references'][position];p=frame['task']/r['path'];src.ordinary(p)
    src.need(src.digest(p)==r['sha256'],'Bound actual fresh35 semantic artifact')
    return p,src.read(p,32*src.MIB)
