"""Current35 resource/COUNT semantics, using unchanged independent pure readers.

This module calls no numerical producer, acceptor, integration kernel or search.
The small, source-pinned functions loaded below only inspect stored rational
data: full INITIAL induction, full support rays, resource histories, exact
rounding, original contract interfaces and closed count-tree geometry.
"""
from __future__ import annotations
import ast,hashlib,json,math,shutil,types,sys
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from . import n5_full_join_sources as src,n5_full_join_inputs as inputs
from .n5_full_join_control_evidence import same

BASE='work/cutoff5_20261020/'
CASES=('B0','BN','B2-S0','B2-S1','B2-S2','B2-S3','B3-S0','B3-S2','B3-T0','B3-T1','B3-T2','B3-T3lower')
COUNT_TARGET=F('76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000')
ALLOWED_IMPORTS={'pathlib','fractions','hashlib','math','copy','collections','json','sys','ast'}

def canonical_sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()

def source(cache,name):
    p=Path(cache).joinpath(*src.parts(name));row=src.plan()['files'].get(name)
    src.need(row is not None and p.is_file()and src.digest(p)==row['sha256'],'Original pure semantic source/data '+name)
    return p

def pure_module(cache,name,*,context=None,functions_only=False):
    """Load a byte-pinned stdlib-only evidence reader, without its CLI body.

    Functions-only projections preserve every selected original function AST.
    Top-level original capture/file-consumption mains are deliberately excluded;
    current source/capture admission is supplied by the separate full reader.
    """
    p=source(cache,name);tree=ast.parse(p.read_text('utf-8'));body=[]
    for node in tree.body:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            modules=[x.name.split('.')[0]for x in node.names]if isinstance(node,ast.Import)else[node.module.split('.')[0]]
            if modules in (['common'],['resource_helpers']):continue
            src.need(set(modules)<=ALLOWED_IMPORTS,'Pure independent-reader stdlib import closure')
            body.append(node)
        elif isinstance(node,ast.FunctionDef):
            if node.name!='main':body.append(node)
        elif not functions_only:
            src.need(isinstance(node,(ast.Assign,ast.Expr)),'No original pure-reader process entry executed')
            # The only non-docstring expression is a rational CE interval check.
            if isinstance(node,ast.Expr)and not isinstance(node.value,ast.Constant):
                src.need(isinstance(node.value,ast.Call)and isinstance(node.value.func,ast.Name)
                    and node.value.func.id=='need','Only fixed rational constant check at import')
            body.append(node)
    module=types.ModuleType('n5_pure_'+hashlib.sha256(name.encode()).hexdigest()[:12]);module.__file__=str(p)
    if context:module.__dict__.update(context)
    exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),module.__dict__)
    return module

def resource_spec(region):
    if region in('B0','BN'):return 'audit/resource5_readback_v4',region,None
    if region.startswith('B2-'):return 'audit/resource5_sector_readback_v1','B2_'+region[-2:],int(region[-1])
    case=region[3:];return 'high/B3_resource_readback_v1','B3_'+case,int(case[1])

def initial_id(region):return 'initial.'+region.replace('-','.')

def resource_controls(cache,relative,namespace,expected):
    """Execute the unchanged original malformed-data loops on current models."""
    p=source(cache,relative);tree=ast.parse(p.read_text('utf-8'))
    main=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    def target(n,name):return isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets)
    start=next(i for i,n in enumerate(main.body)if target(n,'controls'))
    block=[]
    for n in main.body[start:]:
        if target(n,'copy')or target(n,'out'):break
        if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id in('p','path','rel'):break
        if (isinstance(n,ast.For)and isinstance(n.target,ast.Tuple)and isinstance(n.iter,ast.Call)
            and isinstance(n.iter.func,ast.Attribute)and n.iter.func.attr=='items'):break
        block.append(n)
    src.need(block and any(isinstance(n,ast.For)for n in block),'All exact original resource mutation loops selected')
    exec(compile(ast.Module(body=block,type_ignores=[]),str(p)+'#current-mutants','exec'),namespace)
    src.need(same(namespace['controls'],expected),'Every original independent resource control, in its exact order')
    return namespace['controls']

def same_resource_answer(value,reference):
    """Only timing positions present in the externally pinned original schema.

    Inserting a new nested seconds key is rejected by the exact key comparison
    before any diagnostic value is ignored.
    """
    if type(value)is not type(reference):return False
    if type(reference)is dict:
        if value.keys()!=reference.keys():return False
        for key,want in reference.items():
            actual=value[key]
            if key in('seconds','initial_seconds'):
                if type(want)not in(int,float)or type(actual)not in(int,float)or not math.isfinite(actual)or actual<0:return False
            elif not same_resource_answer(actual,want):return False
        return True
    if type(reference)is list:return len(value)==len(reference)and all(same_resource_answer(a,b)for a,b in zip(value,reference))
    return value==reference

def resource_region(region,frames,cache,*,parent_facts,global_owncap):
    parent_module=parent_rules()
    directory,band,sector=resource_spec(region);common=pure_module(cache,BASE+directory+'/common.py')
    if region.startswith('B3-'):
        helper=pure_module(cache,BASE+directory+'/resource_helpers.py',context={'c':common},functions_only=True)
        checker=pure_module(cache,BASE+directory+'/check.py',context={'c':common,'h':helper},functions_only=True)
    else:
        checker=pure_module(cache,BASE+directory+'/check.py',context={'c':common},functions_only=True);helper=checker
    initial=frames[initial_id(region)];report_path,report=inputs.reference(initial)
    candidate=inputs.mapped(initial['task'],report['facts']['input_candidate_path'],src.read(initial['task']/'JOB_SOURCE.json')['original_task_root'])
    z=src.read(candidate,32*src.MIB);native=src.read(inputs.mapped(initial['task'],report['native_result_path'],
        src.read(initial['task']/'JOB_SOURCE.json')['original_task_root']),16*src.MIB)
    cover=checker.initial(z,native,band)
    facts=initial['checked']['summary']['facts']
    edge=parent_module.entails_profile(facts['profile'],facts['numerical_premises']['HIGH'],facts['numerical_premises']['owncap'],
        parent_facts,global_owncap)
    src.need(edge['whole_child_rho']==facts['rho_interval'],'Exact whole-child support/HIGH/owncap implication')
    reference_name=next(r['outputs'][0]for r in src.read(src.ROOT/'proof/remaining_n5_delivery_partition.json',8*src.MIB)
        ['original_resource_and_count_semantic_reference_actions']if r['id']=='67.semantic.resource.'+region)
    historical=src.read(source(cache,reference_name),32*src.MIB)
    selected=[f for f in frames.values()if f['row']['kind']=='resource'and f['row']['selection']['initial_parent']==initial_id(region)]
    src.need(len(selected)==(2 if region in('B0','BN','B2-S3')else 1),'Every original selected/gamma/endpoint resource case')
    answers={};bindings=[];endpoint=[]
    for frame in selected:
        d=src.read(frame['task']/frame['checked']['summary']['semantic_report_relative'],32*src.MIB)
        parent=d['parent_initial']
        src.need(parent['job_id']==initial_id(region)and parent['candidate_sha256']==src.digest(candidate)
            and same(parent['profile'],z['profile'])and same(parent['final_invariants'],z['final_invariants'])
            and parent['stages']==len(z['stages'])and parent['final_cover_sha256']==canonical_sha(cover),
            'Fresh resources consume the same complete current INITIAL candidate, profile and final cover')
        src.need(d['rho_interval']==facts['rho_interval']and (d['beta_interval']is None or d['beta_interval']==facts['beta_interval']),
            'Same current arbitrary-law resource moment domain')
        resource_profile=deepcopy(z['profile']);resource_profile['radius']=d['resource_radius']
        for side in('radius_minus','radius_plus'):
            if side in resource_profile:resource_profile[side]=d['resource_radius']
        resource_edge=parent_module.entails_profile(resource_profile,d['resource_HIGH'],d['resource_owncap'],parent_facts,global_owncap)
        for item in d['full_canonical_resource_rows']:
            i=item['index'];src.need(type(i)is int and i not in answers,'Disjoint whole resource panel union')
            location=historical['source_rows'][str(i)];reference=src.read(source(cache,location['path']),16*src.MIB)
            src.need(src.digest(Path(cache)/location['path'])==location['sha256']and type(reference['index'])is int
                and reference['index']==i and same_resource_answer(item['result'],reference['result']),
                'Entire current native resource answer agrees with its exact original contract-source row')
            answers[i]=reference
            bindings.append(dict(index=i,job_id=d['job_id'],current_result_sha256=item['canonical_result_sha256'],
                original_source_path=location['path'],original_source_sha256=location['sha256'],
                current_stage_sha256=frame['checked']['stage_result_sha256'],resource_parent_implication=resource_edge))
            if frame['row']['selection']['case'].endswith('_endpoint'):endpoint.append(i)
    src.need(sorted(answers)==list(range(100)),'All100 regional probability-panel resource obligations')
    rows=[answers[i]for i in range(100)]
    if region.startswith('B3-'):summary=helper.resources(rows,cover,band,range(100))
    elif region.startswith('B2-'):summary=checker.resources(rows,cover,band,endpoint)
    else:summary=checker.resources(rows,cover,band)
    src.need(summary['excluded']==historical['excluded']and summary['retained']==historical['retained'],
        'Independent complete resource semantics and preserved exact partition')
    if region.startswith('B3-'):
        wanted={'S0':[66,67,68],'S2':[67,68]}.get(region[3:],[])
        src.need([r['index']for r in summary['tangent_exclusions']]==wanted,'Every genuine nonempty B3 exclusion')
    namespace=dict(checker.__dict__,c=common,h=helper,z=z,ia=native,acq=native,b=band,band=band,sector=sector,
        rows=rows,cover=cover,summary=summary,endpoint_indices=endpoint,rl=F(facts['rho_interval'][0]),F=F,json=json,deepcopy=deepcopy)
    controls=resource_controls(cache,BASE+directory+'/check.py',namespace,historical['negative_controls'])
    return dict(region=region,band=frame['row']['selection']['band'],case=region[3:]if region.startswith('B3-')else None,
        sector=sector,initial_stage_sha256=initial['checked']['stage_result_sha256'],initial_candidate_sha256=src.digest(candidate),
        profile=z['profile'],parent_implication=edge,rows=rows,source_rows=historical['source_rows'],bindings=bindings,
        summary=summary,controls=controls,rho=facts['rho_interval'],beta=facts['beta_interval'],
        original_reader_source_sha256=src.digest(source(cache,BASE+directory+'/check.py')))

def parent_rules():
    # A pinned stdlib-only implication helper, not an original numerical kernel.
    src.basic.verify_vendor();path=src.basic.VENDOR/'reproduction/all_indices/c5_parent_facts.py'
    key='_notebook67_pure_parent_facts'
    if key in sys.modules:return sys.modules[key]
    module=types.ModuleType(key);module.__file__=str(path);sys.modules[key]=module
    try:exec(compile(path.read_text('utf-8'),str(path),'exec'),module.__dict__)
    except BaseException:sys.modules.pop(key,None);raise
    return module

def extra_count_interface(row,cfg,c,*,endpoint_product=False):
    raw=row['result']['raw_row'];r=row['result']['result']
    src.need(list(map(F,cfg['acquired_gamma']))==[c.floorgrid(raw['gamma_lo'],10**6),c.ceilgrid(raw['gamma_hi'],10**6)],
        'Whole signed gamma interval from the same acquired physical row')
    SL=F(3162277660,10**9);rl,D,gh,mu=map(F,[r['rho_lo'],r['D'],raw['gamma_hi'],raw['mean_hi']])
    price=max((SL-1)*rl,SL*rl-gh)-D
    if endpoint_product:
        price=max(price,6*F(row['result']['initial']['mean_lo'])*F(raw['A'])*F(raw['B']))
    src.need(SL*SL<10 and price>0 and mu>0,'Strict same-law physical gap price')
    gap=max(F(raw['A'])+F(raw['B']),c.sqrtlo(max(F(0),2*rl-2*D/(SL-1),2*price/(3*mu)),10**12))
    pl,pu=map(F,cfg['p']);upper=c.ceilgrid(1-gap*c.sqrtlo(min(pl*(1-pl),pu*(1-pu)),10**12),10**6)
    src.need(F(cfg['geometry_gap_lower'])==gap and F(cfg['acquired_inward_upper'])==upper,
        'Independently derived whole-gap physical inward cap')

def count_spec(region):
    if region in('B0','BN'):return 'audit/count5_readback_v1',region,None,None
    if region.startswith('B2-'):return 'audit/count5_sector_readback_v1','B2',int(region[-1]),None
    case=region[3:];return 'high/B3_count_readback_v1','B3',int(case[1]),case

def count_region(region,resource,frames,cache,mirror,*,prepare=False):
    directory,band,sector,case=count_spec(region);c=pure_module(cache,BASE+directory+'/common.py')
    if band=='B3':c.BANDS['B3']=('237/200','6/5',None,None,None,None)
    checker=pure_module(cache,BASE+directory+'/check.py',context={'c':c},functions_only=True)
    S=Path(cache)/'work/cutoff6_20261018/fourier/count6_gamma_pilot_v2/BN'
    checker.__dict__.update(S=S,template=source(cache,S.relative_to(cache).as_posix()+'/count_protocol.py').read_text('utf-8'),
        ctor=source(cache,'work/cutoff6_20261020/high/panel035_fastcap_v1/construct.py').read_text('utf-8'),n=5,band=band)
    known=src.read(source(cache,'work/cutoff6_20261020/audit/b2_count_readback_v1/FAST_SCALAR_REVIEW.json'))['new_kernel_sha256']
    retained=resource['summary']['retained'];excluded=resource['summary']['excluded'];rows=resource['rows']
    selected=[f for f in frames.values()if f['row']['kind']=='count'and f['row']['source_capsule'].split('/')[-2]==band
        and f['row']['source_capsule']in {n.rsplit('/',1)[0]for n in src.plan()['files']if n.endswith('/COUNT_ACCEPTED.json')}]
    # A band may contain several rho/beta sectors. Select only exact original row identities.
    jobs={}
    for frame in selected:
        job=frame['row'];contract=src.read(source(cache,job['source_capsule']+'/contract.json'))
        i=job['index'];location=resource['source_rows'].get(str(i))
        if location and contract['resource_path']==location['path']and contract['resource_sha256']==location['sha256']:
            src.need(i not in jobs,'No duplicate regional current COUNT');jobs[i]=frame
    src.need(sorted(jobs)==retained,'All and only the acquired retained panels have fresh full COUNT proofs')
    summaries=[];sources={};graph={};own_controls=[]
    for index in retained:
        frame=jobs[index];path,native=inputs.reference(frame);capsule=path.parent
        obj=src.read(capsule/'contract.json');cfg=obj['rows'][0];row=rows[index]
        src.need(len(obj['rows'])==1 and type(obj['n'])is int and obj['n']==5 and obj['band']==band
            and type(obj['index'])is int and obj['index']==index and obj['resource_verified']is False
            and obj['cutoff_proved']is False,'Exact original conditional native COUNT contract')
        location=resource['source_rows'][str(index)]
        src.need(obj['resource_path']==location['path']and obj['resource_sha256']==location['sha256'],
            'Current acquired resource and original COUNT contract are the same literal source row')
        endpoint_product='/count5_prepare_v4/'in frame['row']['source_capsule']
        c.interface(row,cfg,band,index,5);extra_count_interface(row,cfg,c,endpoint_product=endpoint_product)
        src.need(F(row['result']['result']['rho_hi'])<=F(cfg['rho_upper'])<=F(resource['rho'][1]),'Whole sector rho domination')
        original=Path(cache)/frame['row']['source_capsule'];checker.protocol_source(original,cfg,index)
        forest=src.read(capsule/'COUNT_FOREST.json',32*src.MIB)
        manifest=src.read(capsule/'KERNEL_COPY_MANIFEST.json')['files'];src.need(same(manifest,known),'Whole reviewed n-general COUNT numerical kernel')
        stats=c.geometry(forest,cfg,5)
        src.need(same(stats,native['statistics'])and native['fresh_leaf_evaluations']==stats['leaves']
            and native['negative_controls']==frame['row']['negative_controls']and len(native['negative_controls'])==24,
            'Entire fresh actual35 acceptance, all six closed roots and all original corruption controls')
        src.need(F(forest['target'])==COUNT_TARGET and native['forest_sha256']==src.digest(capsule/'COUNT_FOREST.json')
            and native['contract_sha256']==src.digest(capsule/'contract.json')and native['checker_sha256']==src.digest(capsule/'count_protocol.py')
            and same(native['kernel_sha256'],manifest),'Unchanged exact target and complete actual kernel source bindings')
        # Repeat the original independent geometry/resource/interface mutation loops.
        text=source(cache,BASE+directory+'/check.py').read_text('utf-8');tree=ast.parse(text)
        loop=next(n for n in tree.body if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='index'
            and isinstance(n.iter,ast.Name)and n.iter.id=='count_indices')
        start=next(i for i,n in enumerate(loop.body)if isinstance(n,ast.FunctionDef)and n.name=='leaf')
        stop=next(i for i,n in enumerate(loop.body)if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)
            and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Name)and n.value.func.value.id=='summaries')
        namespace=dict(checker.__dict__,c=c,row=row,cfg=cfg,index=index,n=5,band=band,f=forest,full={'rows':rows},F=F,deepcopy=deepcopy)
        checker.__dict__.update(full={'rows':rows},index=index)
        exec(compile(ast.Module(body=loop.body[start:stop],type_ignores=[]),str(source(cache,BASE+directory+'/check.py'))+'#current-count-mutants','exec'),namespace)
        for field in ('geometry_gap_lower','acquired_inward_upper','acquired_gamma'):
            bad=deepcopy(cfg);bad[field]=['0','0']if field=='acquired_gamma'else'0'
            try:extra_count_interface(row,bad,c,endpoint_product=endpoint_product)
            except(ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):own_controls.append(field)
            else:raise ValueError('Changed signed gamma / physical gap / inward cap accepted')
        destination=Path(mirror)/frame['row']['source_capsule']
        for parent in [destination,*destination.parents]:
            if parent==Path(mirror).parent:break
            src.ordinary(parent)
        if prepare:destination.mkdir(parents=True,exist_ok=True)
        else:src.need(destination.is_dir(),'Existing complete current semantic mirror; pure reader does not create files')
        for name in('contract.json','COUNT_FOREST.json','COUNT_ACCEPTED.json'):
            dest=destination/name
            if dest.exists():src.need(src.digest(dest)==src.digest(capsule/name),'No overwritten semantic proof mirror')
            elif prepare:shutil.copyfile(capsule/name,dest)
            else:raise ValueError('Complete semantic mirror artifact absent')
            graph[dest.relative_to(mirror).as_posix()]=src.digest(dest)
        summaries.append(dict(index=index,p=cfg['p'],target=str(COUNT_TARGET),capsule=frame['row']['source_capsule'],**stats))
        sources[index]=dict(capsule=frame['row']['source_capsule'],contract_sha256=src.digest(capsule/'contract.json'),
            forest_sha256=src.digest(capsule/'COUNT_FOREST.json'),acceptance_sha256=src.digest(capsule/'COUNT_ACCEPTED.json'))
    cover=dict(schema='CONDITIONAL_LITERAL5_CLOSED_100_PANEL_COVER_V1',n=5,band=band,rho=resource['rho'],target=str(COUNT_TARGET),rows=[])
    if band!='B0'and band!='BN':cover.update(schema='CONDITIONAL_LITERAL5_CLOSED_SECTOR_100_PANEL_COVER_V1',beta=resource['beta'],sector=sector)
    if case is not None:cover['case']=case
    for i in range(100):
        r=dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],closure='resource'if i in excluded else'count')
        if i in sources:r['source']=sources[i]
        cover['rows'].append(r)
    checker.__dict__.update(n=5,band=band,sector=sector,case=case,lo=resource['rho'][0],hi=resource['rho'][1],
        beta=resource['beta'],excluded=excluded,retained=retained,sources=sources,c=c,target=COUNT_TARGET)
    census=checker.validate(cover)
    # The exact original full-cover control block, including all seam/source/parser corruptions.
    t=ast.parse(source(cache,BASE+directory+'/check.py').read_text('utf-8'));body=t.body
    begin=next(i for i,n in enumerate(body)if isinstance(n,ast.Assign)and any(isinstance(v,ast.Name)and v.id=='changes'for v in n.targets))
    end=next(i for i,n in enumerate(body)if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)
        and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='need'and 'unchanged whole source graph'in ast.unparse(n))
    namespace=dict(checker.__dict__,cover=cover,nativepath=source(cache,next(r['outputs'][0]for r in src.read(src.ROOT/'proof/remaining_n5_delivery_partition.json',8*src.MIB)
        ['original_resource_and_count_semantic_reference_actions']if r['id']=='67.semantic.resource.'+region)),R=Path(cache),json=json,deepcopy=deepcopy)
    exec(compile(ast.Module(body=body[begin:end],type_ignores=[]),str(source(cache,BASE+directory+'/check.py'))+'#current-cover-mutants','exec'),namespace)
    return dict(n=5,band=band,case=case,sector=sector,rho=resource['rho'],rho_interval=resource['rho'],beta_interval=resource['beta'],
        excluded=excluded,retained=retained,census=census,count_roots=6*len(retained),
        count_totals={k:sum(v[k]for v in summaries)for k in('nodes','leaves')},
        maximum_count_score=str(max((F(v['maximum_score'])for v in summaries),default=F(0))),original_count_target=str(COUNT_TARGET),
        coverage=cover,count_panels=summaries,files_sha256=graph,independent_mutations=dict(c.controls),
        added_interface_mutations=len(own_controls),native_count_mutations=24*len(retained),
        current_native_stages=[jobs[i]['checked']['stage_result_sha256']for i in retained],
        constructor_provenance_bridge='Full unchanged35 native acceptance independently reevaluates every leaf of the retained complete original forest; no historical construction execution is claimed.')
