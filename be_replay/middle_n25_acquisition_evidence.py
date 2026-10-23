"""Pure JSON/source/capture readback for complete middle-n25 acquisitions.

No original mathematical kernel is imported. BASIC process-group observations
remain conditional arithmetic evidence; no count, analytic or theorem join is
promoted by this module.
"""
from __future__ import annotations
from fractions import Fraction as F
import math
from pathlib import Path
import shutil
from . import aux24_evidence as paths,count_task as common
from . import middle_n25_acquisition_sources as sources

MIB=1024**2
CPU=WALL=64800
MEMORY=2*1024**3
DISK=512*MIB
need=sources.need
same=paths.same


def implementation():
    base=Path(__file__).resolve().parent
    return {name:common.digest(base/name)for name in(
        'middle_n25_acquisition.py','middle_n25_acquisition_sources.py','middle_n25_acquisition_evidence.py',
        'aux24_sources.py','aux24_evidence.py','linux_supervisor.py','count_task.py','colab_batch.py','small_indices.py')}


def root(task):return Path(task)/'epoch'/sources.source.PREFIX.rstrip('/')


def aliases(branch):
    packet=sources.definition(branch);band=packet['band']
    return [(folder.removeprefix(sources.source.PREFIX),name)for folder in packet['alias_directories']
            for name in(f'INITIAL_MIDDLE_B{band}_ACCEPTED.json','GLOBAL_RESOURCES_PROOF.json','GLOBAL_RESOURCES_ACCEPTED.json')]


def alias_bindings(task,branch):
    packet=sources.definition(branch);base=root(task)
    canonical=base/packet['canonical_directory'].removeprefix(sources.source.PREFIX)
    result={}
    for folder,name in aliases(branch):
        path=base/folder/name
        need(path.is_file()and not path.is_symlink()and common.digest(path)==common.digest(canonical/name),
             'Fresh canonical parent copied byte-for-byte to the selected local alias')
        result[folder+'/'+name]=common.digest(path)
    return result


def synchronize_parents(task,branch):
    """Copy freshly validated parents; never change receipt or candidate bytes."""
    packet=sources.definition(branch);base=root(task)
    canonical=base/packet['canonical_directory'].removeprefix(sources.source.PREFIX)
    for folder,name in aliases(branch):
        output=base/folder/name
        need(not output.exists()and not output.is_symlink(),'Exclusive fresh parent alias')
        with (canonical/name).open('rb')as incoming,output.open('xb')as outgoing:
            shutil.copyfileobj(incoming,outgoing,MIB)
    return alias_bindings(task,branch)


def outputs(branch,count):
    result=set()
    for stage in sources.stages(branch)[:count]:
        prefix=stage['folder']+'/'
        if stage['kind']=='global_resource':result.add(prefix+stage['proof'])
        if stage['receipt']:result.add(prefix+stage['receipt'])
        if stage['kind']=='local':result.add(prefix+f"PANEL{stage['index']}_accept_CACHE_RUNTIME.json")
    if count>=3:result.update(folder+'/'+name for folder,name in aliases(branch))
    return result


def progress_files(branch):
    result=set()
    for stage in sources.stages(branch):
        name=f"PANEL{stage['index']}_PROGRESS.json"if stage['kind']=='local'else'PROGRESS.json'
        result.add(stage['folder']+'/'+name)
    return result


def verify_epoch(task,branch,count):
    sources.verify(task,branch);base=root(task)
    need(base.is_dir()and not base.is_symlink(),'Ordinary current middle epoch')
    sealed={n.removeprefix(sources.source.PREFIX):r for n,r in sources.selected(branch).items()}
    derived=outputs(branch,count);allowed=set(sealed)|derived|progress_files(branch)
    directories={p.as_posix()for n in allowed for p in Path(n).parents if p.as_posix()!='.'}
    actual=set()
    for p in base.rglob('*'):
        need(not p.is_symlink()and not(hasattr(p,'is_junction')and p.is_junction()),'No linked epoch artifact')
        name=p.relative_to(base).as_posix()
        if p.is_dir():
            need(name in directories,'No unknown epoch directory');continue
        need(p.is_file()and name in allowed,'Only sealed inputs and named current outputs')
        actual.add(name)
        if name in sealed:
            r=sealed[name]
            need(p.stat().st_size==r['bytes']and common.digest(p)==r['sha256'],'Unchanged exact source/candidate '+name)
        else:need(p.stat().st_size<=128*MIB,'Bounded current output')
    need(set(sealed)|derived<=actual,'Complete sealed inputs and completed-stage artifacts')
    if count>=3:alias_bindings(task,branch)
    return base


def read(base,name):return common.read(base/name,128*MIB)


def _bindings(base,mapping):
    need(type(mapping)is dict and mapping,'Nonempty complete original source commitment')
    for name,pin in mapping.items():
        p=base/paths.relative(name)
        need(p.is_file()and not p.is_symlink()and common.digest(p)==pin,'Actual full source/input byte binding')


def _cover(cover):
    need(type(cover['total'])is int and cover['total']==9216 and type(cover['active'])is int
         and type(cover['excluded'])is int and cover['active']>=0 and cover['excluded']>=0
         and cover['active']+cover['excluded']==9216 and sum(cover['reasons'].values())==cover['excluded'],
         'Every exact signed rectangle accounted once')
    need(len(cover['panels'])==100 and all(r['pl']==str(F(i,100))and r['pu']==str(F(i+1,100))for i,r in enumerate(cover['panels'])),
         'All100 ordered closed panel metadata rows')


def _decode(value):
    if type(value)is str:
        try:return F(value)
        except ValueError:return value
    if type(value)is dict:return {k:_decode(v)for k,v in value.items()}
    if type(value)is list:return [_decode(v)for v in value]
    return value


def _typed(value):
    if value is None:return ('none',)
    if type(value)in(bool,int,str):return (type(value).__name__,value)
    if type(value)is F:return ('fraction',value.numerator,value.denominator)
    if type(value)in(list,tuple):return (type(value).__name__,tuple(_typed(v)for v in value))
    if type(value)is dict:
        need(all(type(k)is str for k in value),'Exact typed-key string fields')
        return ('dict',tuple((k,_typed(value[k]))for k in sorted(value)))
    raise ValueError('Unsupported exact cache argument type')


def artifact(task,branch,stage):
    packet=sources.definition(branch);band=packet['band'];base=root(task);folder=base/stage['folder']
    proof=read(folder,stage['proof'])
    need(same(proof['profile'],packet['profile']),'Exact fixed literal n25 rho/beta/support profile')
    mf='COPY_MANIFEST.json'if stage['kind']=='initial'else'PANEL_COPY_MANIFEST.json'
    expected=read(folder,mf)['files']
    if stage['kind']=='global_resource':expected=dict(expected,**{'global_resources.py':common.digest(folder/'global_resources.py')})
    need(same(proof['source_sha256'],expected),'Complete original proof source keyset')
    _bindings(folder,expected)
    receipt=read(folder,stage['receipt'])if stage['receipt']else None
    local=next((r for r in packet['locals']if stage.get('index')==r['index']),None)if stage['kind']=='local'else None
    section=local or packet[stage['kind']]
    if receipt is not None:
        checker='acquire_panel.py'if local else stage['script']
        need(receipt['status']==section['expected_status']and receipt['proof_sha256']==common.digest(folder/stage['proof'])
             and receipt['checker_sha256']==common.digest(folder/checker)and same(receipt['source_sha256'],expected)
             and same(receipt['negative_controls'],section['negative_controls']),
             'Exact full original acceptance, all corruption controls and current proof/source hashes')
        seconds=receipt['seconds']
        need(type(seconds)in(int,float)and math.isfinite(seconds)and seconds>=0,'Finite fresh original action time')
    initial=base/packet['canonical_directory'].removeprefix(sources.source.PREFIX)
    if stage['kind']=='initial':
        need(proof['schema']==f'EXACT_MIDDLE25_MIDDLE_B{band}_INITIAL_COARSENED_HIGH_V1'
             and proof['contact_allowance']==packet['contact_allowance']=='441991/2000000'
             and len(proof['stages'])==12 and type(receipt['signed_rectangles'])is int and receipt['signed_rectangles']==119808
             and type(receipt['probability_panels'])is int and receipt['probability_panels']==100
             and same(receipt['profile'],packet['profile']),'All13 complete global covers under the universal predecessor')
        for item in proof['stages']:_cover(item['cover'])
        _cover(proof['export'])
    elif stage['kind']=='global_resource':
        need(proof['schema']==f'EXACT_MIDDLE25_MIDDLE_B{band}_GLOBAL_RESOURCES_V1'
             and proof['initial_proof_sha256']==common.digest(initial/f'INITIAL_MIDDLE_B{band}_PROOF.json')
             and proof['initial_acceptance_sha256']==common.digest(initial/f'INITIAL_MIDDLE_B{band}_ACCEPTED.json'),
             'Global resources bind the actual fresh timed INITIAL acceptance')
        need(len(proof['rows'])==100 and all(type(r['index'])is int and r['index']==i
             and type(r['derivation']['excluded'])is bool for i,r in enumerate(proof['rows'])),'All100 typed exact global resource rows')
        survivors=[r['index']for r in proof['rows']if r['derivation']['excluded']is False]
        need(same(survivors,packet['global_resource']['survivors']),'Exact selected global survivor set')
        if receipt is not None:
            need(type(receipt['probability_panels'])is int and receipt['probability_panels']==100
                 and same(receipt['survivors'],survivors)
                 and receipt['initial_proof_sha256']==proof['initial_proof_sha256']
                 and receipt['initial_acceptance_sha256']==proof['initial_acceptance_sha256'],
                 'Complete global receipt preserves the fresh parent edges')
    else:
        index=stage['index'];limit=local['cycle_limit'];cycles=proof['cycles']
        need(type(proof['index'])is int and proof['index']==index and proof['p_interval']==[str(F(index,100)),str(F(index+1,100))]
             and proof['cycle_limit']==limit and proof['initial_covers_per_cycle']==4 and proof['mean_floor_grid']==10**12
             and proof['initial_proof_sha256']==receipt['initial_proof_sha256']==common.digest(initial/f'INITIAL_MIDDLE_B{band}_PROOF.json')
             and type(proof['excluded'])is bool and proof['excluded']is local['excluded']and receipt['excluded']is proof['excluded'],
             'Exact selected local closed domain, schedule, INITIAL proof and outcome')
        glob=read(initial,'GLOBAL_RESOURCES_PROOF.json')
        need(same(proof['global_resource'],glob['rows'][index]),'Local recalculated global row equals the fresh whole global resource row')
        need(len(cycles)==local['cycles']and 1<=len(cycles)<=limit,'Every selected finite local cycle')
        keys=[];calls=0
        for i,cycle in enumerate(cycles):
            need(type(cycle['cycle'])is int and cycle['cycle']==i+1 and 1<=len(cycle['stages'])<=4,'Ordered complete local cycles')
            for item in cycle['stages']:
                _cover(item['cover']);calls+=1
                keys.append(_typed((_decode(cycle['profile']),F(item['input_raw']),F(item['input_D']))))
        need(calls==local['mathematical_cover_calls']and type(receipt['local_signed_rectangles'])is int
             and receipt['local_signed_rectangles']==calls*9216 and type(receipt['cycles'])is int and receipt['cycles']==len(cycles),
             'Complete original local mathematical cover census')
        cache=read(folder,f'PANEL{index}_accept_CACHE_RUNTIME.json');distinct=len(set(keys))
        helper=base/'new_middle/stage_cache_v2'
        need(cache['status']=='PASS_FRESH_NAMED_EXACT_LOCAL_CACHE'and type(cache['index'])is int and cache['index']==index
             and cache['action']=='accept'and same(cache['cache_before'],dict(hits=0,misses=0,size=0,maxsize=128))
             and same(cache['cache_after'],dict(hits=calls-distinct,misses=distinct,size=distinct,maxsize=128))
             and type(cache['mathematical_cover_calls'])is int and cache['mathematical_cover_calls']==calls
             and type(cache['full_stage_evaluations'])is int and cache['full_stage_evaluations']==distinct
             and type(cache['memoized_calls'])is int and cache['memoized_calls']==calls-distinct
             and cache['wrapper_sha256']==common.digest(folder/stage['script'])
             and cache['original_checker_sha256']==common.digest(folder/'acquire_panel.py')
             and cache['helper_sha256']==common.digest(helper/'exact_stage_cache.py')
             and cache['helper_review_sha256']==common.digest(helper/'INDEPENDENT_REVIEW.json')
             and same(cache['source_sha256'],expected)
             and same(cache['output_sha256'],{stage['proof']:common.digest(folder/stage['proof']),stage['receipt']:common.digest(folder/stage['receipt'])}),
             'Fresh empty exact-stage memoization, all calls and actual outputs accounted')
    return dict(kind=stage['kind'],action=stage['action'],index=stage.get('index'),
        proof_sha256=common.digest(folder/stage['proof']),receipt_sha256=common.digest(folder/stage['receipt'])if receipt else None,
        conditional_arithmetic_replayed=receipt is not None,native_arithmetic_accepted=False,all_index_conclusion_verified=False)


def transport(task,branch,stage,report):
    task=Path(task).resolve();original=paths.original_path(report['original_task_root']);execution='execution/'+stage['name']
    launch=paths.read(task,execution+'/launch.json');observed=paths.read(task,execution+'/supervisor-result.json')
    need(same(observed,report['observed'])and observed['status']=='completed'and type(observed['returncode'])is int
         and observed['returncode']==0 and observed['reason']is None and observed['mode']=='untrusted_search'
         and observed['proof_accepted']is False and type(observed['sample_count'])is int and observed['sample_count']>0,
         'Actual completed BASIC observation with integer zero exit')
    cwd='epoch/'+sources.source.PREFIX+stage['folder'];argv=launch['argv']
    need(type(argv)is list and len(argv)==4+len(stage['args'])and paths.original_path(argv[0]).is_absolute()
         and argv[1:3]==['-B','-S']and paths.mapped(argv[3],original)==cwd+'/'+stage['script']
         and argv[4:]==stage['args']and paths.mapped(launch['cwd'],original)==cwd
         and paths.mapped(launch['output_dir'],original)==execution,'Exact original stage argv/cwd and contained capture paths')
    expected=dict(argv=argv,cwd=launch['cwd'],output_dir=launch['output_dir'],mode='untrusted_search',wall_seconds=float(WALL),
        cpu_seconds=CPU,memory_bytes=MEMORY,checkpoint_paths=[],disk_bytes=DISK,log_bytes=16*MIB,sample_seconds=.2,heartbeat_seconds=20.)
    need(same(launch,expected)and same(observed['guard_scope'],paths._group_scope(launch)),'Exact18h2GiB BASIC scope, without native/cgroup promotion')
    for kind in('stdout','stderr'):
        name=execution+'/'+kind+'.txt';p=paths.inside(task,name)
        need(paths.mapped(observed[kind+'_path'],original)==name and p.stat().st_size<=16*MIB
             and common.digest(p)==observed[kind+'_sha256'],'Actual complete captured bytes and supervisor hashes')
    need((task/execution/'stderr.txt').stat().st_size==0,'Empty successful native stderr')
    lines=(task/execution/'stdout.txt').read_text('utf-8').splitlines();last=lines[-1]if lines else''
    band=sources.definition(branch)['band']
    if stage['kind']=='initial':prefix=f'INITIAL_MIDDLE_B{band}_ACCEPTED '
    elif stage['kind']=='global_resource':
        prefix='GLOBAL_RESOURCES_CONSTRUCTED 'if stage['action']=='construct'else 'GLOBAL_RESOURCES_ACCEPTED '+str(read(root(task)/stage['folder'],stage['receipt'])['survivors'])+' '
    else:
        index=stage['index'];cache=read(root(task)/stage['folder'],f'PANEL{index}_accept_CACHE_RUNTIME.json')
        need(last==f'PASS_FRESH_NAMED_EXACT_LOCAL_CACHE {index} accept '+str(cache['cache_after']),
             'Actual original memoized-wrapper terminal protocol')
        prior=[s for s in lines[:-1]if s.startswith(f'PANEL_ACCEPTED {index} ')]
        need(len(prior)==1,'One complete original local terminal before wrapper status');last=prior[0];prefix=f'PANEL_ACCEPTED {index} '
    need(last.startswith(prefix),'Original successful terminal marker')
    value=float(last[len(prefix):]);need(math.isfinite(value)and value>=0,'Finite nonnegative original terminal time')


def validate_prefix(task,branch,count):
    stages=sources.stages(branch)
    need(type(count)is int and 0<=count<=len(stages),'Exact completed-stage prefix')
    verify_epoch(task,branch,count);previous={};results=[]
    for stage in stages[:count]:
        name='ledgers/'+stage['name']+'.json';report=paths.read(Path(task).resolve(),name,16*MIB)
        need(report['schema']=='MIDDLE_N25_ACQUISITION_BASIC_STAGE_V1'and report['branch']==branch
             and same(report['stage'],stage)and same(report['implementation'],implementation())
             and same(report['preceding_ledger_sha256'],previous)and report['source_manifest_sha256']==sources.selection_sha(branch)
             and report['native_arithmetic_accepted']is False and report['all_index_conclusion_verified']is False,
             'Exact current stage/source implementation and preceding evidence chain')
        transport(task,branch,stage,report);result=artifact(task,branch,stage)
        expected_aliases=alias_bindings(task,branch)if stage['kind']=='global_resource'and stage['action']=='accept'else{}
        need(same(report['fresh_parent_aliases'],expected_aliases)and same(report['validated_artifact'],result),
             'Actual stage outputs and fresh canonical parent alias bytes')
        previous[name]=common.digest(Path(task)/name);results.append(result)
    return results


def validate_completed(task,branch):
    packet=sources.definition(branch);results=validate_prefix(task,branch,len(sources.stages(branch)))
    return dict(schema='REVALIDATED_MIDDLE_N25_ACQUISITIONS_V1',branch=branch,n=25,
        contact_allowance=packet['contact_allowance'],selected_full_actions=len(results),stages=results,
        source_manifest_sha256=sources.selection_sha(branch),conditional_acquisition_arithmetic_replayed=True,
        native_arithmetic_accepted=False,sharp24_required=False,resource_interfaces_verified=False,
        count_forests_accepted=False,full_n25_verified=False,all_index_conclusion_verified=False)
