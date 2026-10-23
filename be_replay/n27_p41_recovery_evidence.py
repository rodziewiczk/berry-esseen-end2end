"""Pure source/process/geometry readback for the new conditional n27/p41 epoch."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import math
from pathlib import Path
from . import n27_p41_recovery_sources as src
from .finite1039_count_evidence import same,mapped,terminal

CPU_SECONDS=7200
WALL_SECONDS=7260
MEMORY_BYTES=2048*src.MIB
SCOPE='ORIGINAL_ALPHA4_CONSTRUCT_AND_FULL_N27_P41_BASIC_V1'
# Literal metadata cross-read from the source-pinned n10/B0/p36 forest with
# the identical finite_gaussian.py CE_LO definition; never imported/evaluated.
TARGET=('76824784444199314310731654405729617052063596250011448874609/'
        '187500000000000000000000000000000000000000000000000000000000')
FLAGS=('native_arithmetic_accepted','parent_acquisitions_verified','semantic_replacement_join_verified',
       'lane53_ready','all_index_conclusion_verified')
ACTIONS={'construct':('construct_alpha4.py',[],['COUNT41_FOREST.json','CONSTRUCTION_RUN.json']),
         'accept':('count_protocol.py',['accept'],['COUNT41_ACCEPTED.json'])}
CONTROLS=['wrong n','boolean n','wrong index','boolean index','wrong target','wrong contract',
          'missing kernel source','wrong checker','missing count','reordered counts','wrong count','boolean count',
          'missing child','invalid axis','boolean axis','outside cut','nontext cut','changed leaf box','false decision',
          'false leaf arithmetic','missing result','unknown node','extra success claim','extra leaf claim']
EMPTY={'EMPTY_SUPPORT_GAP_VARIANCE','EMPTY_ACQUIRED_THETA_VARIANCE','EMPTY_ACQUIRED_MEAN_VARIANCE',
       'EMPTY_PHASE','EMPTY_NEGATIVE_BUDGET','EMPTY_PHASE_RESOURCE','EMPTY_SUPPORT_VARIANCE','EMPTY_SHARP_BOX',
       'EMPTY_SHARP_GAP','EMPTY_RHO_BRANCH','EMPTY_RHO_UPPER','EMPTY_VARIANCE_IDENTITY','EMPTY_JOINT_CUBICS',
       'EMPTY_ACQUIRED_RHO_VARIANCE','EMPTY_ACQUIRED_BETA_VARIANCE','EMPTY_ACQUIRED_BETA','EMPTY_ACQUIRED_MEAN','EMPTY_ACQUIRED_ALPHA'}
CONSTRUCTION_SCOPE=('Conditional bounded discovery only. This constructor changes splitting priority, never leaf decisions '
                    'or the fixed original-box acceptor.')
ACCEPT_SCOPE=('Conditional fixed count proof only. Exact same-law resource acquisition and parent proof composition remain '
              'separate obligations. Every original root box and leaf is reconstructed; rho/beta/alpha contractions are '
              'recomputed by the frozen wrapper.')


def implementation():
    names=('n27_p41_recovery.py','n27_p41_recovery_sources.py','n27_p41_recovery_evidence.py',
           'finite1039_count_evidence.py','finite1039_sources.py','n5_remaining_sources.py','n5_remaining_bridge.py',
           'linux_supervisor.py','colab_batch.py')
    return {n:src.digest(src.ROOT/'be_replay'/n)for n in names}|{'source_plan_sha256':src.PLAN_SHA256}


# Complete published64 runtime b8631631e1772de83187701ddbdd9ef972870ea8.
# Its pure metadata dependency later gained COUNT batch-finish compatibility;
# the original whole pair and every source/capture/leaf binding remain checked.
ORIGINAL64_IMPLEMENTATION={
    'colab_batch.py':'136bc2bb9b25cb8cd36118041bf593821f3cbdea5debee82b27ccb7626c0d1e6',
    'finite1039_count_evidence.py':'6e38c9c99ecebcfce7d1c09d8233da1b5905bbd9f46e60c4a73883fdcd8f03e9',
    'finite1039_sources.py':'6a34be3e362d2a9cfe34b52bf1c0f1872cd4fe45afa8cf2acf82a232b4da1c95',
    'linux_supervisor.py':'61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2',
    'n27_p41_recovery.py':'fe0aeeed15e9d432144f2ced96c3cf5130650fa0fa789ce27c1a4394ec983cfe',
    'n27_p41_recovery_evidence.py':'38a8729842f8f70cdb2e59e1c550e8783fbd59a88322c8fd26ae1f61682bef65',
    'n27_p41_recovery_sources.py':'ddfb9869826c59bf9e0fec213462e54f39de8da3a2c4796587c20e20f11b0183',
    'n5_remaining_bridge.py':'f0459a0570ca9a4fc11e507f25474e67bf5e3e958a60513bb7be364d707a069a',
    'n5_remaining_sources.py':'17f8d9b3bcdce510574901be83684a630d54cc8d2f6251856b7737bbd85aaaab',
    'source_plan_sha256':'94d5a0048c619a86666c94fc7ba93d7cb5bfee602c3e505e663d5ee2583fc814',
}


def known_implementation(packet):
    return same(packet,implementation())or same(packet,ORIGINAL64_IMPLEMENTATION)


def command(request,action,python):
    from pathlib import PureWindowsPath,PurePosixPath
    root=request['original_task_root'];cls=PureWindowsPath if len(root)>1 and root[1]==':'else PurePosixPath
    src.need(type(python)is str and cls(python).is_absolute(),'Recorded absolute Python interpreter')
    script,args,_=ACTIONS[action]
    return [python,'-B','-S',str(cls(root)/'capsule'/script),*args]


def forest_census(capsule):
    """Reconstruct every closed box, never call the original leaf evaluator."""
    capsule=Path(capsule);p=src.read(capsule/'COUNT41_FOREST.json',limit=128*src.MIB)
    manifest=src.read(capsule/'KERNEL_COPY_MANIFEST.json')['files'];cfg=src.read(capsule/'contract.json')['rows'][0]
    header=dict(schema='ACTUAL27_FLOOR25_B0_P41_CLOSED_COUNT_FOREST_V1',n=27,index=41,
                contract_sha256=src.digest(capsule/'contract.json'),kernel_sha256=manifest,
                checker_sha256=src.digest(capsule/'count_protocol.py'))
    src.need(type(p)is dict and set(p)==set(header)|{'target','roots'}
             and all(same(p[k],v)for k,v in header.items()),'Exact original native forest header')
    src.need(type(p['target'])is str and p['target']==TARGET,
             'Literal original exact target, also recomputed by the unchanged native acceptor')
    roots=p['roots'];src.need(type(roots)is list and len(roots)==28,'All28 original nearest-count roots')
    box=[cfg['p'],['0',cfg['Lambda']],['0','1'],['-1/2','1/2'],['0',cfg['d0']]]
    nodes=leaves=depthmax=0;statuses=Counter();maximum=F(0)
    for k,root in enumerate(roots):
        src.need(type(root)is dict and set(root)=={'k','tree'}and type(root['k'])is int and root['k']==k,
                 'Ordered exact roots0through27')
        todo=[(root['tree'],box,0)]
        while todo:
            node,b,depth=todo.pop();nodes+=1;depthmax=max(depthmax,depth)
            src.need(nodes<=10000 and depth<=128 and type(node)is dict,'Unchanged full native node/depth cap')
            if node.get('kind')=='split':
                src.need(set(node)=={'kind','axis','cut','left','right'}and type(node['axis'])is int
                         and 0<=node['axis']<5 and type(node['cut'])is str,'Complete native binary split')
                axis=node['axis'];cut=F(node['cut']);src.need(str(cut)==node['cut']and F(b[axis][0])<cut<F(b[axis][1]),'Strict interior rational split')
                left=[list(v)for v in b];right=[list(v)for v in b];left[axis][1]=str(cut);right[axis][0]=str(cut)
                todo.extend(((node['left'],left,depth+1),(node['right'],right,depth+1)))
            else:
                src.need(set(node)=={'kind','box','decision','result'}and node['kind']=='leaf'and same(node['box'],b)
                         and type(node['result'])is dict and node['decision']in EMPTY|{'PASS_TARGET'},
                         'Every original closed leaf box and named complete payload')
                leaves+=1;statuses[node['decision']]+=1
                if node['decision']=='PASS_TARGET':
                    score=node['result']['score_upper'];src.need(type(score)is str and F(score)<F(p['target']),'Stored exact strict leaf target')
                    maximum=max(maximum,F(score))
    return dict(roots=28,nodes=nodes,leaves=leaves,maximum_depth=depthmax,closed_statuses=dict(statuses),maximum_score=str(maximum),target=p['target'])


def process(task,action,record):
    task=Path(task);request=src.verify_task(task);original=request['original_task_root'];directory=task/'execution'/action
    src.need(record['schema']=='OBSERVED_NEW_N27_P41_ACTION_V1'and record['scope']==SCOPE and record['action']==action
             and known_implementation(record['implementation'])and all(record[f]is False for f in FLAGS),
             'One complete exact implementation epoch and honest conditional action scope')
    o=record['observed'];src.need(same(src.read(directory/'supervisor-result.json'),o),'Actual stopped supervisor result')
    src.need(o['status']=='completed'and type(o['returncode'])is int and o['returncode']==0 and o['reason']is None
             and o['mode']=='untrusted_search'and o['proof_accepted']is False
             and type(o['sample_count'])is int and o['sample_count']>0,'Actual successful stopped BASIC process')
    for k in('elapsed_seconds','maximum_sampled_group_CPU_seconds','maximum_sampled_group_RSS_bytes'):
        src.need(type(o[k])in(int,float)and math.isfinite(o[k])and o[k]>=0,'Finite actual process diagnostic')
    launch=src.read(directory/'launch.json');_,_,outputs=ACTIONS[action]
    src.need(set(launch)=={'argv','cwd','output_dir','mode','wall_seconds','cpu_seconds','memory_bytes','checkpoint_paths',
                          'disk_bytes','log_bytes','sample_seconds','heartbeat_seconds'}
             and same(launch['argv'],command(request,action,record['python_executable']))
             and mapped(task,launch['cwd'],original)==task/'capsule'
             and mapped(task,launch['output_dir'],original)==directory and launch['mode']=='untrusted_search'
             and launch['sample_seconds']==.2 and launch['heartbeat_seconds']==20
             and type(launch['checkpoint_paths'])is list
             and [mapped(task,v,original)for v in launch['checkpoint_paths']]==[task/'capsule'/n for n in outputs],
             'Exact unchanged command/cwd/action and full stopped-capture request')
    for k,v in(('cpu_seconds',CPU_SECONDS),('wall_seconds',WALL_SECONDS),('memory_bytes',MEMORY_BYTES),
               ('disk_bytes',256*src.MIB),('log_bytes',16*src.MIB)):
        src.need(type(launch[k])in((int,float)if k=='wall_seconds'else(int,))and launch[k]==v,'Exact documented BASIC budgets')
    scope=dict(kind='UNTRUSTED_SEARCH_POSIX_PROCESS_GROUP',proof_acceptance=False,external_wall_seconds=float(WALL_SECONDS),
               per_process_RLIMIT_AS_bytes=MEMORY_BYTES,per_process_RLIMIT_CPU_seconds=CPU_SECONDS,
               aggregate_kernel_memory_limit=False,aggregate_kernel_cpu_limit=False,sampled_group_RSS_limit_bytes=MEMORY_BYTES,
               sampled_group_CPU_limit_seconds=CPU_SECONDS,sampled_file_limit_bytes=256*src.MIB,sampled_log_limit_bytes=16*src.MIB,
               descendants_changing_session_are_contained=False,equivalent_to_Windows_Job_or_cgroup=False)
    src.need(same(o['guard_scope'],scope),'Honest exact BASIC process-group policy')
    for kind in('stdout','stderr'):
        p=mapped(task,o[kind+'_path'],original)
        src.need(p==directory/(kind+'.txt')and p.is_file()and p.stat().st_size<=16*src.MIB
                 and src.digest(p)==o[kind+'_sha256'],'Actual source-bound '+kind+' capture')
    src.need((directory/'stderr.txt').stat().st_size==0,'Empty successful original stderr')
    captures=o['checkpoints'];src.need(type(captures)is list and len(captures)==len(outputs),'Every whole fresh output captured')
    for c,name in zip(captures,outputs):
        native=task/'capsule'/name;copied=directory/'checkpoints'/name
        src.need(set(c)=={'source_path','exists','trusted_certificate','path','bytes','sha256'}and c['exists']is True
                 and c['trusted_certificate']is False and mapped(task,c['source_path'],original)==native
                 and mapped(task,c['path'],original)==copied and copied.is_file()and native.is_file()
                 and type(c['bytes'])is int and c['bytes']==native.stat().st_size==copied.stat().st_size
                 and c['sha256']==src.digest(native)==src.digest(copied),'Complete stopped native output bytes and hash')
    text=(directory/'stdout.txt').read_text('utf-8');packet=terminal(text)
    src.need(src.digest(directory/'stdout.txt')==o['stdout_sha256'],'Stable original stdout while parsing')
    return packet


def validate_constructor(task):
    task=Path(task);record=src.read(task/'CONSTRUCT_OBSERVED.json');out=process(task,'construct',record)
    packet=src.read(task/'capsule/CONSTRUCTION_RUN.json');src.need(same(out,packet),'Whole actual constructor terminal equals its fresh receipt')
    capsule=task/'capsule';census=forest_census(capsule)
    fixed=dict(scope=CONSTRUCTION_SCOPE,status='STORED_CONDITIONAL_FOREST_CONSTRUCTED_NOT_ACCEPTED',
               contract_sha256=src.digest(capsule/'contract.json'),fixed_acceptor_sha256=src.digest(capsule/'count_protocol.py'),
               constructor_sha256=src.digest(capsule/'construct_alpha4.py'),forest_sha256=src.digest(capsule/'COUNT41_FOREST.json'))
    src.need(set(packet)==set(fixed)|{'visited','seconds'}and all(same(packet[k],v)for k,v in fixed.items())
             and type(packet['visited'])is int and packet['visited']==census['nodes']
             and type(packet['seconds'])in(int,float)and math.isfinite(packet['seconds'])and packet['seconds']>=0,
             'Original constructor exact success, actual new forest and complete visited count; rc0 alone is insufficient')
    return dict(census=census,constructor_receipt_sha256=src.digest(capsule/'CONSTRUCTION_RUN.json'),
                candidate_sha256=src.digest(capsule/'COUNT41_FOREST.json'))


def inventory(task):
    result={}
    for p in sorted(Path(task).rglob('*')):
        src.ordinary(p)
        if p.is_file()and p.name!='COMPLETED.json':result[p.relative_to(task).as_posix()]=dict(bytes=p.stat().st_size,sha256=src.digest(p))
    return result


def validate_pair(task):
    task=Path(task);constructed=validate_constructor(task);record=src.read(task/'ACCEPT_OBSERVED.json')
    src.need(same(record['implementation'],src.read(task/'CONSTRUCT_OBSERVED.json')['implementation']),
             'Construction and acceptance belong to the same whole implementation epoch')
    packet=process(task,'accept',record);capsule=task/'capsule';receipt=src.read(capsule/'COUNT41_ACCEPTED.json')
    src.need(same(packet,receipt),'Whole actual acceptor stdout equals the fresh acceptance receipt')
    c=constructed['census'];expected=dict(status='PASS_FRESH_CONDITIONAL_ACTUAL27_EXACT_COUNT41',n=27,index=41,
        forest_sha256=constructed['candidate_sha256'],contract_sha256=src.digest(capsule/'contract.json'),
        checker_sha256=src.digest(capsule/'count_protocol.py'),kernel_sha256=src.read(capsule/'KERNEL_COPY_MANIFEST.json')['files'],
        statistics={k:c[k]for k in('nodes','leaves','closed_statuses','maximum_score','maximum_depth')},
        negative_controls=CONTROLS,fresh_leaf_evaluations=c['leaves'],scope=ACCEPT_SCOPE)
    src.need(set(receipt)==set(expected)|{'seconds'}and all(same(receipt[k],v)for k,v in expected.items())
             and type(receipt['seconds'])in(int,float)and math.isfinite(receipt['seconds'])and receipt['seconds']>=0,
             'Full unchanged native acceptance, all24 original controls and every fresh leaf')
    d=src.plan()
    return dict(schema='NEW_N27_P41_CONDITIONAL_COUNT_EVIDENCE_V1',n=27,index=41,contact_allowance='0',
        p=['41/100','21/50'],rho=['1','11/10'],new_candidate_epoch=True,
        source_plan_sha256=src.PLAN_SHA256,contract_sha256=expected['contract_sha256'],
        candidate_sha256=constructed['candidate_sha256'],constructor_receipt_sha256=constructed['constructor_receipt_sha256'],
        acceptance_receipt_sha256=src.digest(capsule/'COUNT41_ACCEPTED.json'),census=c,
        historical_candidate_sha256=d['historical_selected_forest']['sha256'],
        historical_acceptance_sha256=d['historical_selected_acceptance']['sha256'],
        conditional_arithmetic_completed=True,**{f:False for f in FLAGS})


def validate_completed(task, *,original_task_root=None):
    task=Path(task);request=src.verify_task(task)
    src.need(original_task_root is None or str(original_task_root)==request['original_task_root'],'One explicit originating task root')
    report=src.read(task/'COMPLETED.json');summary=validate_pair(task)
    src.need(report['schema']=='COMPLETED_NEW_N27_P41_PAIR_V1'
             and same(report['implementation'],src.read(task/'CONSTRUCT_OBSERVED.json')['implementation'])
             and same(report['summary'],summary)and same(report['artifacts'],inventory(task))
             and report['conditional_arithmetic_completed']is True and all(report[f]is False for f in FLAGS),
             'Full completed new-candidate source/process/capture/output inventory')
    return dict(schema='REVALIDATED_NEW_N27_P41_PAIR_V1',summary=summary,original_task_root=request['original_task_root'],
                completed_sha256=src.digest(task/'COMPLETED.json'),conditional_arithmetic_completed=True,**{f:False for f in FLAGS})
