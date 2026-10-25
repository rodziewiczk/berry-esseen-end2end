"""Notebook67 full finite composition under explicit universal analytic inputs.

Arithmetic, current same-law interfaces and exact domain coverage are checked
here. The reader cannot turn a human/JSON declaration into a universal lemma.
Consequently the explicit unresolved analytic premises remain in the sequent;
neither full_n5_verified nor all_index_conclusion_verified is produced.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from . import n5_full_join_sources as src,n5_full_join_control_evidence as control
from . import n5_full_join_inputs as inputs,n5_full_join_semantics as sem
from .colab_batch import atomic_json,event

SCHEMA='N5_FULL_JOIN_FINITE_SESSION_V1'
COMPLETE='complete_conditional_n2_n5_semantic_chain_basic'
UNIVERSAL_PREMISES=(
    'The external exact one-summand theorem and standardization inputs hold for arbitrary real iid marginals with finite third absolute moment; no selected numerical producer is substituted for this theorem.',
    'Unrestricted n2/n3 analytic reductions identify all standardized real iid laws with the exact certificate domains; in particular the quantitative conclusion is C3<=59*sqrt(3)/250.',
    'Unrestricted fixed-index attainment/contact and reflection preserve closed CDF atoms, the common actual marginal and threshold; no constrained or three-point optimizer is substituted.',
    'The ROOT4 all-law localization from quantitative G3 and the cited iid structural bound maps every contrary law into its complete physical domain, both discrepancy orientations and every real threshold.',
    'The literal actual-index5 same-law contact/support, q5=5*(R4(P)-C5)_+=0 from global C4, complete INITIAL cell/gap induction and simultaneous resource inequalities are valid for that one unrestricted contrary witness.',
    'All enabled count/interval/Fourier/LOW/HIGH kernels implement their reviewed continuous inequalities, including strict outgoing versus closed incoming events, zero-noise Bernoulli branch and unbounded threshold/phase rays.',
    'The cited pointwise closed-halfline Prawitz smoothing, Gaussian/binomial inequalities and iid Shevtsova .3031*(1+.646/rho) hold on their complete stated domains and in this exact normalization.'
)

def import_validator(number):
    if number=='08':return inputs.validate08
    if number=='11':return inputs.validate11
    if number=='13':return inputs.validate13
    if number=='35':
        def validate(path):
            frames=inputs.validate35(path)
            return dict(notebook='35',jobs=326,initial=12,resources=15,count_forests=295,count_roots=1770,count_leaves=75178,
                stage_hashes={k:v['checked']['stage_result_sha256']for k,v in frames.items()},
                session_sha256=src.digest(Path(path)/'SESSION_RESULT.json'))
        return validate
    raise ValueError('Only fixed full67 prerequisites08/11/13/35')

def import_completed_inputs(root,durable_root,status):
    from .finite_join_session_import import restore_latest
    root=Path(root);status['imports']=[];missing=[]
    for number,directory in [('08','small-indices'),('11','root4'),('13','n5-gapfree'),('35','n5-remaining')]:
        found=restore_latest(Path(durable_root)/directory,root/'imports',validator=import_validator(number),
            log=lambda name,**data:event(root,name,notebook=number,**data))
        if found:
            task,checked,archive=found
            status['imports'].append(dict(notebook=number,task_relative=task.relative_to(root).as_posix(),validated=checked,archive=archive))
        else:missing.append(dict(notebook=number,directory=directory,reason='No complete source/capture-validated final export found'))
        atomic_json(root/'SESSION_RESULT.json',status)
    return missing

def foundations(small,physical):
    src.need(small['conditional_targets']=={'n2':'2*sqrt(2)/7','n3':'59*sqrt(3)/250'}
        and physical['required_predecessor']=='C3<=59*sqrt(3)/250'and physical['bound']=='4097/10000',
        'Exact quantitative predecessor is available before the ROOT4/C5 inference')
    docs=('proof/small_indices_analytic_review.md','proof/code_root4_all_law_localization_audit.md',
          'proof/code_root4_all_law_localization_source_map.json','proof/literature_inputs.md')
    pins={name:src.digest(src.ROOT/name)for name in docs}
    return dict(schema='N5_CONDITIONAL_ALL_LAW_FOUNDATION_SEQUENT_V1',
        normalization='C_n=sup_P sqrt(n)/E|X|^3 * sup_H |P(S_n<=H)-Phi(H/sqrt(n))|; iid E X=0, E X^2=1, E|X|^3<infinity',
        proof_nodes=[
            dict(id='G2',requires=['08 complete n2 arithmetic','unrestricted n2 analytic reduction'],conclusion='ALL P: C2<=2*sqrt(2)/7'),
            dict(id='G3',requires=['08 complete n3 arithmetic','unrestricted n3 analytic reduction'],conclusion='ALL P: C3<=59*sqrt(3)/250',weaker_C3_le_CE_is_sufficient=False),
            dict(id='G4',requires=['G3','11 both entire physical ROOT4 passes','unrestricted ROOT4 localization','published iid structural bound'],
                 conclusion='ALL P: C4<=4097/10000<CE',both_orientations=True,all_thresholds=True),
            dict(id='Q5',requires=['G4','one oriented unrestricted attained contrary n5 witness'],conclusion='q5=5*(R4(P)-C5)_+=0',
                 same_marginal=True,equality_at_CE_included=True)],
        source_notes_sha256=pins,universal_analytic_premises=list(UNIVERSAL_PREMISES),
        source_notes_are_proof_assumptions_not_machine_verification=True,all_law_C4_verified=False,full_n5_verified=False)

def fresh_parent_facts(frames):
    rules=sem.parent_rules();facts=[]
    for key,method in [('support',rules.support_facts),('high',rules.high_facts),('owncaps',rules.owncap_facts)]:
        frame=frames[key]
        for i,_ in enumerate(frame['checked']['summary']['references']):
            path,d=inputs.reference(frame,i);facts.extend(method(d,src.digest(path)))
    frame=frames['owncaps'];packet=inputs.old.terminal((frame['task']/'execution/stdout.txt').read_text('utf-8'))
    ref=packet['coarse_429'];origin=src.read(frame['task']/'JOB_SOURCE.json')['original_task_root']
    path=inputs.mapped(frame['task'],ref['native_receipt'],origin)
    src.need(src.digest(path)==ref['sha256'],'Actual completed35 GLOBAL coarse429 receipt')
    upper=rules.global_coarse429(src.read(path));global_fact=rules.GlobalOwncapFact(upper,src.digest(path))
    return facts,global_fact

class PortableProofPath(type(Path())):
    """Interpret original POSIX source graph names unchanged on Windows too."""
    def __str__(self):return super().__str__().replace('\\','/')

def final_functions(cache,mirror):
    return sem.pure_module(cache,sem.BASE+'root/final_composition_v2/check.py',functions_only=True,context=dict(
        R=PortableProofPath(mirror).resolve(),GRAPH={},HASHES={},B2=F(84729828287999,250000000000000),B3=F(35139006743001,10**14),
        TARGET=F(4097,10000),COUNT_TARGET=sem.COUNT_TARGET))

def composition_mutations(cache,final,count_results,corner,complement):
    """All original final-composition malformed geometry/scalar/source controls."""
    import ast,json
    p=sem.source(cache,sem.BASE+'root/final_composition_v2/check.py');t=ast.parse(p.read_text('utf-8'))
    main=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    start=next(i for i,n in enumerate(main.body)if isinstance(n,ast.Assign)and any(isinstance(v,ast.Name)and v.id=='controls'for v in n.targets))
    stop=next(i for i,n in enumerate(main.body)if isinstance(n,ast.Assign)and any(isinstance(v,ast.Name)and v.id=='index'for v in n.targets))
    rectangles=[final.sector3(case)for case in('S0','S2','T0','T1','T2','T3lower')]+[([F(477,400),F(6,5)],[F(17,50),final.B3])]
    namespace=dict(final.__dict__,loaded=[(None,z)for z in count_results],g=corner,f=complement,rectangles=rectangles,
        F=F,json=json,deepcopy=deepcopy)
    exec(compile(ast.Module(body=main.body[start:stop],type_ignores=[]),str(p)+'#current-final-mutants','exec'),namespace)
    reference=src.read(sem.source(cache,sem.BASE+'root/final_composition_v2/C5_CHECKED.json'),16*src.MIB)
    src.need(control.same(namespace['controls'],reference['negative_controls']),'All original final25-way scalar/domain/source controls')
    return namespace['controls']

def validate_batch(root,status,*,prepare=False):
    root=Path(root);src.need(status['schema']==SCHEMA and len(status['groups'])==15,'All15 complete physical groups,22 original calls')
    src.need([r['group_id']for r in status['groups']]==[g['id']for g in src.plan()['groups']],'Exact complete original action partition')
    group_tasks={}
    for row in status['groups']:
        task=root.joinpath(*src.parts(row['task_relative']));checked=control.validate_completed(task)
        src.need(control.same(checked,row['validated']),'Revalidated original full group matches recorded complete receipt')
        group_tasks[row['group_id']]=task
    src.need([r['notebook']for r in status['imports']]==['08','11','13','35'],'Every required complete upstream family')
    imported={}
    for row in status['imports']:
        path=root.joinpath(*src.parts(row['task_relative']));value=import_validator(row['notebook'])(path)
        src.need(control.same(value,row['validated']),'Entire current imported family readback')
        imported[row['notebook']]=(path,value)
    foundation=foundations(imported['08'][1],imported['11'][1]);frames=inputs.validate35(imported['35'][0])
    facts,coarse=fresh_parent_facts(frames);cache=root/'source-cache';mirror=root/'semantic-current'
    resource_results=[];count_results=[]
    for region in sem.CASES:
        resource=sem.resource_region(region,frames,cache,parent_facts=facts,global_owncap=coarse)
        resource_results.append({k:v for k,v in resource.items()if k!='rows'})
        counted=sem.count_region(region,resource,frames,cache,mirror,prepare=prepare);count_results.append(counted)
    final=final_functions(cache,mirror);ce_lower=final.constants();rows=[]
    for region,z in zip(sem.CASES,count_results):
        if region in('B0','BN'):
            rho=[F(1),F(11,10)]if region=='B0'else[F(11,10),F(23,20)];rows.append(final.count_case(z,region,rho))
        elif region.startswith('B2-'):
            sector=int(region[-1]);rows.append(final.count_case(z,'B2',*final.sector2(sector),sector=sector))
        else:
            case=region[3:];rows.append(final.count_case(z,'B3',*final.sector3(case),case=case))
    detail=imported['13'][1]
    corner=dict(n=5,rho=detail['domain']['rho'],beta=detail['domain']['beta'],target=detail['domain']['target'],
        **detail['compact'],exteriors=detail['exteriors'])
    final.corner(corner)
    epoch=group_tasks['67.support-complement-physical-epoch'];complement=src.read(epoch/'capsule/work/cutoff5_20261020/audit/complement5_readback_v1/READBACK.json')
    final.complement(complement)
    checks=final.union([final.sector2(i)for i in range(4)],[F(23,20),F(237,200)],[-final.B2,final.B2])
    rectangles=[final.sector3(case)for case in('S0','S2','T0','T1','T2','T3lower')]+[([F(477,400),F(6,5)],[F(17,50),final.B3])]
    checks+=final.union(rectangles,[F(237,200),F(6,5)],[-final.B3,final.B3])
    src.need([rows[0]['rho'][0],rows[0]['rho'][1],rows[1]['rho'][1]]==['1','11/10','23/20']
        and sum(r['retained']for r in rows)==295 and sum(r['excluded']for r in rows)==905
        and sum(r['roots']for r in rows)==1770 and sum(r['leaves']for r in rows)==75178,'Full signed-rho-beta-p union and exact quantitative census')
    controls=composition_mutations(cache,final,count_results,corner,complement)
    result=dict(schema='N5_CURRENT_FULL_SEMANTIC_CHAIN_UNDER_ANALYTIC_PREMISES_V1',n=[2,3,4,5],
        foundation=foundation,resource_regions=resource_results,count_regions=rows,
        probability_panel_instances=1200,resource_exclusions=905,count_forests=295,count_roots=1770,count_leaves=75178,
        corner=corner,complement=dict(rho_finite=complement['rho_finite'],strips=41,attempts=42,
            maximum_upper=complement['maximum_upper'],published_tail=complement['published_tail']),
        ce_lower=str(ce_lower),original_controls=controls,closed_moment_arrangement_checks=checks,
        conditional_finite_chain_verified=True,unacquired_universal_analytic_premises=list(UNIVERSAL_PREMISES),
        conditional_conclusion='Under the explicit unrestricted analytic and published inputs, ALL standardized iid real laws satisfy C2<=2sqrt(2)/7,C3<=59sqrt(3)/250,C4<=4097/10000 and C5<=CE.',
        all_law_C4_verified=False,full_n5_verified=False,native_arithmetic_accepted=False,all_index_conclusion_verified=False)
    interfaces=dict(resources=resource_results,counts=count_results)
    if prepare:atomic_json(root/'CURRENT_RESOURCE_COUNT_INTERFACES.json',interfaces)
    else:src.need(control.same(interfaces,src.read(root/'CURRENT_RESOURCE_COUNT_INTERFACES.json',128*src.MIB)),
        'Pure readback reconstructs every saved current resource/COUNT interface')
    return result

def validate_completed(root):
    root=Path(root);status=src.read(root/'SESSION_RESULT.json',64*src.MIB)
    src.need(status['state']==COMPLETE and status['conditional_finite_chain_verified']is True
        and all(status[k]is False for k in control.FLAGS),'Complete conditional chain, never unconditional proof flags')
    computed=validate_batch(root,status)
    src.need(control.same(computed,src.read(root/'FINITE_CHAIN.json',64*src.MIB)),'Entire saved current finite family chain recomputed from actual original evidence')
    return dict(state=COMPLETE,finite_chain_sha256=src.digest(root/'FINITE_CHAIN.json'),
        jobs=22,semantic_resource_regions=12,semantic_count_regions=12,conditional_finite_chain_verified=True,
        full_n5_verified=False,native_arithmetic_accepted=False,all_index_conclusion_verified=False)
