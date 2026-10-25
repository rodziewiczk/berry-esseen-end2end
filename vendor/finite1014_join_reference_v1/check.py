"""Fresh base10 and sequential11..14 check-only join; no prior closure flags."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,sys
import common as c
import families
import composites
from evidence import exact_capture
from selection import selected,inventory
H=Path(__file__).resolve().parent;R=H.parents[3];N=H.parents[1]
need=c.need;bind=c.bind;load=c.load;sha=c.sha;same=c.same;waitfor=c.missing;reject=c.reject
NS=list(range(10,15));BANDS=c.BANDS
summary={}
def checked(path,status):
    if waitfor(path,status):return None
    z=load(path);need(z['status']==status,'exact named audit receipt');return z
def support_scope(p,n,rho,radius,q):
    need(type(p['n'])is int and p['n']==n and p['K']=='0'and p['schema']=='DIRECT_SAME_LAW_CONTACT_SUPPORT_DISCOVERY_V1','literal same-law contact support')
    need(p['rho_upper']==rho and p['radius']==radius and p['q_contact']==q and type(p['support_sign'])is int and p['support_sign']==0,'exact complete two-ray premises')
    need([r['sign']for r in p['ray_rows']]==[-1,1]and all(type(r['sign'])is int and F(r['contact_upper'])<0 for r in p['ray_rows']),'both strictly excluded complete support rays')
    for r in p['ray_rows']:
        need(F(r['coefficient_at_R'])<0 and F(r['contact_derivative_at_R'])<0 and F(r['contact_derivative_slope_at_R'])<0,'strict outward ray extension')
def coarse():
    d=N/'analytic/coarse_support10_14_v1';cp=d/'RESULT.json';ap=d/'REPLAY_CHECKED.json'
    if waitfor(cp,'complete coarse support')or waitfor(ap,'fresh coarse support replay'):return False
    z,a=load(cp),load(ap)
    need(z['status']=='COMPLETE_CONDITIONAL_COARSE_SUPPORT10_14'and a['status']=='PASS_FRESH_CONDITIONAL_COARSE_SUPPORT10_14_REPLAY','coarse support theorem')
    need(z['n']==a['n']==NS and z['rho_interval']==a['rho_interval']==['1','71/50']and z['radius']==a['radius']=='3','coarse complete index/moment scope')
    need(a['candidate_sha256']==sha(cp)and a['complete_index_band_rows']==10 and a['malformed_controls']==20 and a['parser_controls']==2,'full coarse native replay identity')
    need(a['both_support_rays']is True and a['full_threshold_line_and_tails']is True and a['predecessor_caps_verified']is False and a['cutoff_proved']is False,'conditional native coarse scope')
    need(len(z['rows'])==10,'all index-band pairs')
    for index,row in enumerate(z['rows']):
        n=10+index//2;band,lo,hi,cap=('global','1','7/5','423/1000')if index%2==0 else('localized','7/5','71/50','209/500')
        q=n*(F(cap)-F(4097,10000));beta=F(row['beta_upper'])
        need(type(row['n'])is int and row['n']==n and row['band']==band and row['rho_interval']==[lo,hi]and row['predecessor_cap']==cap and row['q']==str(q),'independently reconstructed coarse hypotheses')
        need(0<beta<1 and (1+beta*beta)**2>=F(hi)**2*(1-beta*beta),'universal signed beta cover')
        support_scope(row['proof'],n,hi,'3',str(q))
    for action,obj,path in [('construct',z,cp),('replay',a,ap)]:
        required={action+'.py':sha(d/(action+'.py'))}
        if action=='replay':required['RESULT.json']=sha(cp)
        exact_capture(R/f'runs/cutoff10_20261018/analytic/coarse_support_{action}01',['-B',action+'.py'],d,obj['status']+' '+sha(path),required)
    summary['coarse_support']=dict(indices=NS,rho=['1','71/50'],radius='3',native_replay=True,predecessor_caps_discharged_by_Fourier=False)
    return True
def analytic_inputs():
    inputs=[('audit/range10_v1/CHECKED.json','PASS_BOUNDED_CONDITIONAL_ACTUAL10_14_RANGE_AUDIT_WITH_OLD_HIGH_OBSTRUCTION'),('audit/refined_high_review_v1/READBACK.json','PASS_SUPPORTED_MOMENT_CENTERED_HIGH10_14_COMPLETE_NATIVE_REPLAY_AND_BOUNDED_INDEPENDENT_AUDIT'),('audit/signed_low_review_v1/CHECKED.json','PASS_CONDITIONAL_SIGNED_CELL_LOW10_14_SOURCE_AND_BOUNDED_EXACT_CONTROLS'),('audit/resource_count_port_review_v2/CHECKED.json','PASS_CONDITIONAL_RESOURCE_COUNT_PORT10_14_SOURCE_AND_BOUNDED_INTERFACES')]
    inputs.append(('analytic/subpanel_native_review_v1/CHECKED.json','PASS_INDEPENDENT_STATIC_SUBPANEL_PROTOCOL_REVIEW_NO_NATIVE_ORACLE'))
    inputs.append(('analytic/subpanel_native_review_v2/n10_BN_fine_p42_CHECKED.json','PASS_INDEPENDENT_STATIC_SUBPANEL_PROTOCOL_REVIEW_NO_NATIVE_ORACLE'))
    inputs.extend([('audit/fine_initial_review_v1/CHECKED.json','PASS_BOUNDED_FINE_INITIAL10_BN_SOURCE_GRID_REVIEW'),('analytic/fine_bn_port_review_v1/CHECKED.json','SOURCE_REVIEW_ONLY_FINE_BN_RESOURCE_COUNT_PORT_NO_DEFECT_FOUND')])
    okay=True
    for path,status in inputs:
        z=checked(N/path,status)
        if z is None:okay=False;continue
        if 'subpanel_native_review'in path:
            expected_n=10 if '/n10_BN_fine_p42_CHECKED.json'in path else 11
            need(z['n']==expected_n and z['nearest_count_roots_per_component']==expected_n+1 and z['index']==42 and z['components']==4 and z['original_contract_unchanged']is True and z['all_other_root_axes_unchanged']is True and z['strict_target_unchanged']is True and z['native_node_limit']==10000 and z['native_depth_limit']==128,'reviewed representative subpanel source scope')
            need(all(z[k]is False for k in ['native_count_oracle_executed_here','component_acceptance_claimed','whole_panel_closed','cutoff_claimed']),'source review cannot replace native component proofs')
        if 'fine_initial_review'in path:
            need(z['n']==10 and z['band']=='BN'and z['grid']==[12,24,12,3]and z['cells_per_cover']==10368 and z['unchanged_common_modules']==9 and z['physical_D_seed_used']is False and z['numerical_stage_calls']==0 and z['cutoff10_proved']is False,'exact bounded fine INITIAL review scope')
        if 'fine_bn_port_review'in path:
            need(all(z[k]is False for k in ['native_preparation_executed_here','mathematical_oracle_executed','generated_contracts_accepted','cutoff10_proved']),'fine source review does not replace native evidence')
        if 'refined_high'in path:
            need(z['n']==NS and z['complete_native_rows']==20 and len(z['rows'])==10 and z['actual_support_acquired']is False and z['physical_D_seed_used']is False,'supported HIGH exact scope')
            for n in NS:
                for b,(lo,hi,cap,q,radius,hcap)in BANDS.items():
                    rows=[r for r in z['rows']if type(r['n'])is int and r['n']==n and r['band']==b]
                    need(len(rows)==1 and rows[0]['rho_upper']==hi and rows[0]['support_radius']==radius and rows[0]['target']==hcap and F(rows[0]['upper'])<F(hcap),'literal supported HIGH target')
    return okay
def scope_initial(z,n,b):
    select=selected(n,b)
    lo,hi,cap,q10,radius,hcap=BANDS[b];q=q10 if n==10 else'0';pcap={'B0':'1049/2500','BN':'52/125'}[b]if n==10 else'CE'
    need(z['status']==select['initial_status']and type(z['n'])is int and z['n']==n and z['K']=='0'and z['target']=='CE','sharp literal selected INITIAL epoch')
    need(type(z['profile']['grid'])is list and all(type(x)is int for x in z['profile']['grid'])and z['profile']['grid']==select['grid']and'p_interval'not in z['profile'],'exact whole-band selected signed grid')
    need(z['band']==b and z['rho_interval']==[lo,hi]and z['q']==q and z['owncap']==cap and z['high_cap']==hcap and z['predecessor_cap']==pcap,'distinct fixed score/contact/HIGH premises')
    need(type(z['predecessor_globally_sharp_assumed'])is bool and z['predecessor_globally_sharp_assumed']==(n!=10),'GLOBAL predecessor assumption')
    text='GLOBAL C9<.423; then SAME-law supported C9 cap'if n==10 else f'ASSUMED GLOBAL C_{n-1}<CE at every threshold and standardized iid law'
    need(z['predecessor']==text,'all-threshold exact predecessor scope')
    for key in['predecessor_discharged_here','owncap_verified','high_acceptance_joined','physical_defect_seed_imported','full_cutoff_proved']:need(z[key]is False,'no native premise promotion')
    need('universal_moment_defect_seed'not in z and len(z['stages'])==8 and z['stages'][0]['input_D']is None and z['stages'][0]['input_raw']is None,'genuinely unseeded eight updates')
    need(z['profile']['radius']==radius and z['profile']['radius_minus']==radius and z['profile']['radius_plus']==radius and z['profile']['cap']==cap,'selected acquired support before moments')
def initial(n,b):
    select=selected(n,b);d=select['initial'];cp=d/f'{b}_RESULT.json';ap=d/f'{b}_REPLAY_CHECKED.json'
    if waitfor(cp,f'n{n} {b} INITIAL')or waitfor(ap,f'n{n} {b} full INITIAL replay'):return None
    z,a=load(cp),load(ap);scope_initial(z,n,b)
    need(a['status']==select['initial_replay_status']and a['candidate_sha256']==sha(cp),'fresh selected INITIAL replay')
    for key in['n','band','rho_interval','q','owncap','predecessor_cap','high_cap','predecessor_globally_sharp_assumed']:need(same(z[key],a[key]),'same native INITIAL parameters '+key)
    need(a['fresh_complete_covers']==9 and a['signed_cells_per_cover']==select['cells']and a['original_probability_panels']==100 and a['malformed_controls']==select['scope_controls']and a['parser_controls']==2,'complete selected INITIAL replay and negative controls')
    need(same(a['profile'],z['profile']),'native replay same exact selected grid/profile')
    need(a['numerical_cap_join_complete']is False and a['physical_defect_seed_imported']is False and a['full_cutoff_proved']is False,'explicit conditional replay scope')
    prep=load(d.parent/'PREPARED.json');expected=dict(prep['files_sha256']);expected[str((d.parent/'PREPARED.json').relative_to(R))]=sha(d.parent/'PREPARED.json')
    need(z['files_sha256']==expected,'entire selected INITIAL frozen source graph')
    previous=(None,None)
    for stage in z['stages']:
        need((stage['input_raw'],stage['input_D'])==previous,'ordered same-law INITIAL feedback')
        vals=[]
        for field,old in [('R',previous[0]),('D',previous[1])]:
            v=c.ceilgrid(stage['cover'][field],10**8)+F(1,100000)
            if old is not None:v=min(v,F(old))
            vals.append(v)
        need(list(map(F,[stage['next_raw'],stage['next_D']]))==vals and 0<vals[0]<F(2*n,5)and 0<vals[1]<6,'actual first-raw license and directed feedback')
        previous=stage['next_raw'],stage['next_D']
    for cover in [s['cover']for s in z['stages']]+[z['export']]:
        need(c.integer(cover['total'])==select['cells']and c.integer(cover['active'])+c.integer(cover['excluded'])==select['cells']and sum(c.integer(v)for v in cover['reasons'].values())==cover['excluded'],'all selected signed cells accounted')
        need(len(cover['panels'])==100,'complete original p cover')
        for i,row in enumerate(cover['panels']):need([row['pl'],row['pu']]==[str(F(i,100)),str(F(i+1,100))]and c.integer(row['cells'])>=0,'ordered closed p seams')
    need(z['final_invariants']==a['final_invariants']==dict(raw=previous[0],D=previous[1])and F(previous[1])<c.sqrtlo(F(10),10**50)-1,'final physical gap and invariant identity')
    lo,hi,cap,q10,radius,hcap=BANDS[b];q=q10 if n==10 else'0'
    support_scope(z['refined_support'],n,hi,radius,q)
    if n==10:
        need(F(q)==n*(F(z['predecessor_cap'])-F(4097,10000)),'predecessor allowance, not owncap allowance')
        support_scope(z['coarse_support'],n,hi,'3',str(n*(F(423,1000)-F(4097,10000))))
    else:need(z['coarse_support']is None and q=='0','GLOBAL sharp predecessor gives direct refined support')
    for action,obj,path in [('construct',z,cp),('replay',a,ap)]:
        required={f'{b}_RESULT.json':sha(cp)}if action=='replay'else{}
        exact_capture(R/f"runs/cutoff10_20261018/analytic/{select['initial_capture_prefix']}_{action}01",['-B','../'+action+'.py',str(n),b],d,f"{obj['status']} {n} {b} {sha(path)}",required)
    for key,value in [('n',True),('q','1'),('predecessor','same-law-only sharp predecessor'),('predecessor_globally_sharp_assumed',n==10),('physical_defect_seed_imported',True),('owncap','1')]:
        bad=deepcopy(z);bad[key]=value;reject(lambda:scope_initial(bad,n,b),'INITIAL '+key)
    for label,mutate in [('wrong selected grid',lambda z:z['profile'].update(grid=[1,1,1,1])),('restricted probability export',lambda z:z['profile'].update(p_interval=['2/5','41/100'])),('noninteger grid',lambda z:z['profile']['grid'].__setitem__(0,12.0))]:
        bad=deepcopy(z);mutate(bad);reject(lambda:scope_initial(bad,n,b),label)
    bad=deepcopy(z);bad['status']='COMPLETE_UNSEEDED_SIGNED_INITIAL10_14_CONDITIONAL'if select['fine']else'COMPLETE_UNSEEDED_SIGNED_INITIAL10_BN_FINE_CONDITIONAL'
    reject(lambda:scope_initial(bad,n,b),'wrong selected INITIAL epoch label')
    return z
def fourier():
    specs=[('auxiliary9_14','PASS_INDEPENDENT_GLOBAL_AUXILIARY9_14_READBACK'),('supported9_14','PASS_INDEPENDENT_SUPPORTED_SAME_LAW9_14_TWO_BAND_READBACK'),('highrho10_14','PASS_INDEPENDENT_GLOBAL_HIGHRHO10_14_READBACK'),('corner10_14','PASS_INDEPENDENT_SUPPORTED_CORNER10_14_BH_READBACK')]
    records={};okay=True
    for name,status in specs:
        p=N/f'fourier/{name}_readback_v1/RESULT.json';z=checked(p,status)
        if z is None:okay=False;continue
        need(z['n']==(list(range(9,15))if name in['auxiliary9_14','supported9_14']else NS)and all(type(n)is int for n in z['n']),'literal full Fourier indices')
        need(type(z['negative_controls'])is int and z['negative_controls']>=24,'complete independent Fourier malformed controls')
        records[name]=z
    if 'auxiliary9_14'in records:
        z=records['auxiliary9_14'];need(z['finite_rho']==['1','19/10']and z['target']=='423/1000'and F(z['uniform_upper'])<F(423,1000),'global auxiliary with infinite tail')
        need(set(z['per_n_upper'])==set(map(str,range(9,15)))and all(F(v)<F(423,1000)for v in z['per_n_upper'].values()),'global predecessor ceilings')
        need(z['regional_rho']==['7/5','71/50']and set(z['regional_per_n_upper'])==set(map(str,range(9,15)))and all(F(v)<F(209,500)for v in z['regional_per_n_upper'].values()),'localized all-threshold predecessor support cap')
    if 'supported9_14'in records:
        z=records['supported9_14'];need(z['support_absolute_upper']=='3'and z['sharp10_proved']is False and z['cutoff10_proved']is False,'support is external to Fourier')
        for b,(lo,hi,own,_,_,_)in BANDS.items():
            hits=[t for t in z['bands']if t['name']==b]
            need(len(hits)==1 and hits[0]['rho']==[lo,hi],'complete low-band Fourier seams')
            values=z['per_band_per_n_upper'][b];need(set(values)==set(map(str,range(9,15))),'all supported literal indices')
            prior=F(1049,2500)if b=='B0'else F(52,125)
            need(F(values['9'])<prior and all(F(values[str(n)])<F(own)for n in NS),'separate supported predecessor and own ceilings')
    if 'highrho10_14'in records:
        z=records['highrho10_14'];need(z['finite_rho']==['71/50','15/8']and z['target']=='4097/10000'and set(z['per_n_upper'])==set(map(str,NS))and all(F(v)<F(4097,10000)for v in z['per_n_upper'].values()),'universal complete high-rho sharp complement')
    if 'corner10_14'in records:
        z=records['corner10_14'];need(z['rho']==['23/20','71/50']and z['support_absolute_upper']=='3'and z['target']=='4097/10000'and set(z['per_n_upper'])==set(map(str,NS))and all(F(v)<F(4097,10000)for v in z['per_n_upper'].values()),'complete supported BH complement')
    summary['Fourier']={name:{k:v for k,v in z.items()if k in['n','target','rho','finite_rho','support_absolute_upper','per_n_upper','per_band_per_n_upper','regional_rho','regional_per_n_upper','negative_controls']}for name,z in records.items()}
    return okay
def sequential(base,local):
    need(type(base)is bool and set(local)=={11,12,13,14}and all(type(k)is int and type(v)is bool for k,v in local.items()),'exact sequential scope')
    current=base;rows=[]
    for n in range(11,15):
        predecessor=current;current=predecessor and local[n]
        rows.append(dict(n=n,global_predecessor=n-1,predecessor_established=predecessor,local_implication_complete=local[n],sequential_result_established=current))
    return rows
def validate_base_claim(claim,fresh):
    need(type(claim)is dict and set(claim)=={'actual10_base_freshly_derived'},'only an explicit base claim')
    need(type(claim['actual10_base_freshly_derived'])is bool and type(fresh)is bool and claim['actual10_base_freshly_derived']==fresh,'base claim equals freshly reconstructed evidence')
def main():
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize and len(sys.argv)==2,'ordinary-B output basename')
    name=sys.argv[1];need(Path(name).name==name and name.endswith('.json')and not(H/name).exists(),'new immutable snapshot')
    for p in H.iterdir():
        if p.is_file()and p.suffix in['.py','.txt','.diff']:bind(p)
    port=load(H/'SOURCE_PORT.json',False)
    for path,d in port['sources'].items():bind(R/path,d)
    for path,d in port['copies'].items():bind(H/path,d)
    analytic=analytic_inputs();support=coarse();complement=fourier()
    summary['selected_source_epochs']=inventory()
    summary['composite_overrides']=composites.initialize()
    for n in NS:
        summary[str(n)]={}
        for b in BANDS:
            z=initial(n,b);summary[str(n)][b]=families.family(n,b,z)if z else dict(original_panels=100,closed_panels=0,complete=False)
    composites.finish(summary)
    # Actual10 closure is recomputed in this same invocation, never imported.
    local={n:analytic and support and complement and all(summary[str(n)][b]['complete']for b in BANDS)for n in NS}
    base=local[10];chain=sequential(base,{n:local[n]for n in range(11,15)})
    need(not any(x['sequential_result_established']for x in sequential(False,{n:True for n in range(11,15)})),'missing base never propagates');c.controls['missing base blocks all']=1
    need([x['sequential_result_established']for x in sequential(True,{11:True,12:False,13:True,14:True})]==[True,False,False,False],'no jump over failed local implication');c.controls['failed step blocks successors']=1
    reject(lambda:sequential(True,{11:True,13:True,14:True}),'omitted predecessor index')
    reject(lambda:sequential(1,{n:True for n in range(11,15)}),'nonboolean base')
    # A deliberately falsified partial claim cannot establish a base. No
    # previous snapshot is an input; the fresh local evidence is authoritative.
    reject(lambda:validate_base_claim({'actual10_base_freshly_derived':True},False),'incomplete base falsely promoted by public flag')
    validate_base_claim({'actual10_base_freshly_derived':base},local[10])
    tailpath=R/'work/cutoff15_20261017/audit/sequential16_19_join_v2/FINAL_READBACK.json';tail=load(tailpath)
    need(tail['status']=='PASS_CONDITIONAL_SEQUENTIAL16_19_READBACK_WITH_RETAINED20_EDGE'and tail['conditional_cutoff15_with_retained20_edge']is True and tail['unqualified_cutoff15_proved']is False and tail['retained_analytic_A']is True,'explicit retained eventual15 theorem')
    closed=chain[-1]['sequential_result_established']
    out=dict(status='PASS_CONDITIONAL_CUTOFF10_CHAIN_WITH_RETAINED_A_F_T15'if closed else'PASS_AVAILABLE_CUTOFF10_CHAIN_WITH_PENDING_EDGES',actual10_base_freshly_derived=base,sequential_chain=chain,all10_14_conditionally_closed=closed,conditional_cutoff10_with_retained15_edge=closed,unqualified_cutoff10_proved=False,retained_analytic_A=True,retained_published_Fourier_inputs_F=['Prawitz smoothing','Shevtsova finite bounds and infinite-rho tail'],retained_eventual15_T15=dict(receipt=str(tailpath.relative_to(R)),receipt_sha256=sha(tailpath),freshly_reproved_here=False,retained20_edge=tail['retained_eventual20_historical_edge']),summary=summary,pending=c.pending,negative_controls=dict(c.controls),native_leaf_evaluator_calls=0,Fourier_integrations=0,mathematical_status='Conditional base10 plus consecutive GLOBAL-predecessor implications11..14, with retained A, published F, and eventual15 theorem T15',execution_status='Fresh independent check-only source/capture/scope/panel/interface/forest-geometry join; native complete semantic replays supply numerical arithmetic',files_sha256=c.G)
    need(not closed or not c.pending,'no closure with pending evidence')
    for p,d in c.G.items():need(sha(R/p)==d,'all bound sources unchanged')
    with(H/name).open('x')as f:json.dump(out,f,indent=2);f.write('\n')
    print(out['status'],'PENDING',len(c.pending),'FILES',len(c.G),sha(H/name))
if __name__=='__main__':main()
