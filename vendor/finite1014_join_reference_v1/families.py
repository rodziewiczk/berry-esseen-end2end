"""Fresh native resource/count readback; no oracle execution."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from collections import Counter
import common as c
import evidence as e
from selection import selected
import composites
H=Path(__file__).resolve().parent;R=H.parents[3];N=H.parents[1]
need=c.need;load=c.load;bind=c.bind;sha=c.sha;same=c.same
pending=c.pending;negative=c.controls
waitfor=c.missing;reject=c.reject
def count(n,b,i,desc,cfg,freeze):
    if composites.selected_override(n,b,i):return composites.count(n,b,i,desc,cfg,freeze)
    s=selected(n,b);d=s['count']/b/f'capsule{i}';rp=d/'ROW_RESULT.json'
    if waitfor(rp,f'n{n} {b} p{i} full count'):return None
    row=load(rp,False)
    if row['status']!=f'FRESH_NATIVE_ACTUAL{n}_FULL_PANEL_ACCEPTED_CONDITIONAL':pending.append(dict(edge=f'n{n} {b} p{i} full count',path=str(rp.relative_to(R)),status=row['status']));return None
    e.count_row_claim(row,n,b,i,sha(freeze),sha(d/'contract.json'))
    for key,val in [('source_freeze_sha256','0'*64),('contract_sha256','0'*64),('n',n+1),('band','XX'),('index',i+1)]:
        bad=deepcopy(row);bad[key]=val;reject(lambda:e.count_row_claim(bad,n,b,i,sha(freeze),sha(d/'contract.json')),'count row '+key)
    fp=d/f'COUNT{i}_FOREST.json';ap=d/f'COUNT{i}_ACCEPTED.json';f,a=load(fp,False),load(ap,False);m=load(d/'KERNEL_COPY_MANIFEST.json',False)
    e.source_scope(n,b,i,d,cfg,desc,m)
    need(a['status']==desc['status']and c.integer(a['n'])==n and c.integer(a['index'])==i and f['schema']==desc['schema'],'literal fixed native count theorem')
    need(a['forest_sha256']==row['forest_sha256']==sha(fp)and row['accepted_sha256']==sha(ap),'selected native forest identity')
    need(f['contract_sha256']==a['contract_sha256']==row['contract_sha256']==sha(d/'contract.json'),'same exact acquired contract')
    need(f['checker_sha256']==a['checker_sha256']==sha(d/'count_protocol.py')and f['kernel_sha256']==a['kernel_sha256']==m['files'],'frozen native source')
    stats=c.geometry(f,cfg,n);need(same(stats,a['statistics'])and same(stats,row['statistics']),'independent n+1-root geometry and strict stored scores')
    need(c.integer(a['fresh_leaf_evaluations'])==stats['leaves']and len(set(a['negative_controls']))==len(a['negative_controls'])==24,'native fresh all-leaf arithmetic and controls')
    construction=load(d/'CONSTRUCTION_RUN.json',False)
    need(construction['status']=='STORED_CONDITIONAL_FOREST_CONSTRUCTED_NOT_ACCEPTED'and construction['forest_sha256']==sha(fp),'complete captured construction')
    for action in ['construct','accept']:
        rr=row['runs'][action];cap=R/rr['path'];ex=load(cap/'EXECUTION.json',False);need(sha(cap/'EXECUTION.json')==rr['execution_sha256'],'selected count capture')
        expected_path=s['count']/f'captures/{b}_p{i}_{action}'
        e.count_capture_claim(ex,n,b,i,action,d,expected_path,cap)
        for stream in ['stdout','stderr']:bind(cap/(stream+'.txt'),ex[stream+'_sha256'])
        need(not(cap/'stderr.txt').read_bytes(),'empty native count stderr')
        expected=a if action=='accept'else construction
        need(same(c.read(cap/'stdout.txt'),expected),'whole captured native action output')
        for key,val in [('cwd',str(R)),('command',['python','-B','other.py']),('n',n+1),('index',i+1),('band','XX')]:
            bad=deepcopy(ex);bad[key]=val;reject(lambda:e.count_capture_claim(bad,n,b,i,action,d,expected_path,cap),'count child '+key)
    for label,mutate in [('missing root',lambda z:z['roots'].pop()),('duplicate root',lambda z:z['roots'].__setitem__(1,deepcopy(z['roots'][0]))),('wrong literal forest n',lambda z:z.update(n=15)),('inflated target',lambda z:z.update(target='1'))]:
        bad=deepcopy(f);mutate(bad);reject(lambda:c.geometry(bad,cfg,n),label)
    return stats
def family(n,b,init):
    s=selected(n,b);d=s['resource']/b;cp=d/'CANDIDATE.json';ap=d/'ACCEPTED.json'
    if waitfor(cp,f'n{n} {b} original100 resource candidate')or waitfor(ap,f'n{n} {b} full resource replay'):return dict(original_panels=100,closed_panels=0,complete=False)
    z,a=load(cp),load(ap)
    need(z['status']==f'COMPLETE_CONDITIONAL_ACTUAL{n}_REFRESHED_RESOURCE_INVENTORY'and a['status']==f'PASS_FRESH_FULL_CONDITIONAL_ACTUAL{n}_REFRESHED_RESOURCE_REPLAY','full literal resource epoch')
    need(type(z['n'])is type(a['n'])is int and z['n']==a['n']==n and z['band']==a['band']==b and z['q']==init['q']and z['K']=='0'and z['rho_interval']==init['rho_interval']and z['owncap']==init['owncap'],'literal sequential resource premises')
    need(a['candidate_sha256']==sha(cp)and same(a['rows'],z['rows'])and same(a['files_sha256'],z['files_sha256'])and same(a['status_counts'],z['status_counts']),'complete original resource replay identity')
    need(len(z['rows'])==len(a['timings_seconds'])==100 and a['negative_controls']==dict(malformed_inventories=12,parser_controls=2),'full100-row native acceptance')
    id=s['initial'];need(z['initial_candidate_sha256']==sha(id/f'{b}_RESULT.json')and z['initial_acceptance_sha256']==sha(id/f'{b}_REPLAY_CHECKED.json'),'same selected INITIAL edge')
    for obj in [z,a]:
        for field in ['predecessor_verified','owncap_verified','global_bound_proved',f'cutoff{n}_proved']:need(obj[field]is False,'native conditional scope retained')
    for action,obj,path,label in [('construct',z,cp,'RESOURCE_CANDIDATE'),('accept',a,ap,'RESOURCE_ACCEPTED')]:
        required={'resources.py':sha(d.parent/'resources.py'),'PREPARED.json':sha(d.parent/'PREPARED.json')}
        if action=='accept':required[f'{b}/CANDIDATE.json']=sha(cp)
        e.exact_capture(R/f"runs/cutoff10_20261018/root/{s['resource_capture_prefix']}_{action}01",['-B','resources.py',action,b],d.parent,f"{label} {b} {obj['status_counts']} {sha(path)}",required)
    freeze=s['count']/b/'FROZEN.json';frozen=load(freeze)if freeze.exists()else None
    if frozen:
        need(frozen['status']==f'FROZEN_ACTUAL{n}_COMPENSATED_CONDITIONAL_COUNT_FAMILY_NOT_EXECUTED'and frozen['K']=='0'and frozen['rho']==init['rho_interval'],'exact count source epoch')
        need(frozen['n']==n and frozen['band']==b and frozen['parent_candidate_sha256']==sha(cp)and frozen['parent_acceptance_sha256']==sha(ap),'count family same resources')
        need(len(frozen['dispositions'])==100,'complete100 count dispositions')
        for i,dd in enumerate(frozen['dispositions']):need(c.integer(dd['index'])==i,'ordered count dispositions')
        descs={x['index']:x for x in frozen['rows']};need(len(descs)==len(frozen['rows']),'unique count panels')
    else:descs={}
    closed=0;counts=[];dispositions=[];totals=Counter();acquired=[]
    for i,desc in enumerate(z['rows']):
        need(c.integer(desc['n'])==n and c.integer(desc['index'])==i and desc['band']==b and desc['p']==[str(F(i,100)),str(F(i+1,100))]and desc['path']==f'rows/{i:03d}.json','all original closed p panels')
        rp=d/desc['path'];bind(rp,desc['sha256']);row=c.read(rp);need(row['n']==n and row['band']==b and row['index']==i and row['status']==desc['status'],'whole row identity')
        source=deepcopy(init['export']['panels'][i]);source['rho_lo']=c.BANDS[b][0];need(same(source,row['source']),'same original INITIAL p interval')
        status=row['status'];totals[status]+=1
        if status=='EXCLUDED_BY_SAME_LAW_RESOURCE':need(row['result']['excluded']is True,'proved resource exclusion');closed+=1
        elif status=='RESOURCE_ROW_ACQUIRED_FOR_COUNT':
            acquired.append(i);need(row['result']['excluded']is False,'acquired actual row')
            if i not in descs:
                disposition=frozen['dispositions'][i]if frozen else None
                status_pending=disposition['status']if disposition else'MISSING_COUNT_FAMILY'
                need(status_pending in ['CONTRACT_DOMAIN_FAILED_NO_EXCLUSION','MISSING_COUNT_FAMILY'],'missing acquired panel remains explicit failed contract')
                pending.append(dict(edge=f'n{n} {b} p{i}',path=str(rp.relative_to(R)),status=status_pending,reason=disposition.get('reason')if disposition else None))
            else:
                need(frozen['dispositions'][i]['status']=='PREPARED_CONDITIONAL_COUNT_NOT_EXECUTED','selected prepared count disposition')
                cd=s['count']/b/f'capsule{i}';contract=load(cd/'contract.json',False)
                need(len(contract['rows'])==1 and contract['resource_candidate_sha256']==sha(cp)and contract['resource_replay_sha256']==sha(ap)and contract['resource_row_sha256']==sha(rp),'actual resource to count edge')
                cfg=contract['rows'][0];c.interface(row,cfg,b,i,n)
                bad=deepcopy(cfg);bad['Lambda']=str(F(cfg['Lambda'])/2);bad['acquired_lambda_upper']=bad['Lambda'];reject(lambda:c.interface(row,bad,b,i,n),'replacing original Lambda')
                stats=count(n,b,i,descs[i],cfg,freeze)
                if stats:closed+=1;counts.append(dict(index=i,**stats))
        else:
            need(status=='RESOURCE_CRITERION_FAILED_NO_EXCLUSION','known unresolved resource status');pending.append(dict(edge=f'n{n} {b} p{i}',path=str(rp.relative_to(R)),status=status))
        dispositions.append(dict(index=i,p=desc['p'],status=status))
    need(dict(totals)==z['status_counts']and set(descs)<=set(acquired),'independent complete disposition accounting')
    return dict(original_panels=100,closed_panels=closed,complete=closed==100,resource_statuses=dict(totals),acquired_panels=acquired,count_statistics=counts,dispositions=dispositions)
