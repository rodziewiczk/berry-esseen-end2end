"""Named original-panel unions, independently checked from native component evidence."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import sys
import common as c
import evidence as e
import composite_core as g
from selection import selected
H=Path(__file__).resolve().parent;R,N=c.R,c.N
P=N/'fourier/subpanel_native_v1'
need=c.need
OVERRIDES={};USED=set()

def initialize():
    z=c.load(H/'OVERRIDES.json',False)
    need(type(z)is dict and set(z)=={'schema','selection_frozen','rows'},'exact original-panel override selection')
    need(z['schema']=='FOUR_CLOSED_P_COMPONENTS_PER_SELECTED_ORIGINAL_PANEL_V1'and z['selection_frozen']is True,'reviewed frozen composite selection')
    need(type(z['rows'])is list and z['rows'],'nonempty explicit override selection')
    last=None
    for row in z['rows']:
        need(type(row)is dict and set(row)=={'n','band','index'},'literal selected original panel')
        n,b,i=row['n'],row['band'],row['index']
        need(type(n)is type(i)is int and 10<=n<=14 and b in c.BANDS and 0<i<99,'selected original scope')
        key=n,b,i;need(last is None or last<key,'ordered unique override scopes');last=key
        family=f'n{n}_{b}'+('_fine'if selected(n,b)['fine']else'')+f'_p{i}'
        OVERRIDES[key]=P/family
    return [dict(n=n,band=b,index=i,directory=str(d.relative_to(R)),component_forests=4)for(n,b,i),d in OVERRIDES.items()]

def selected_override(n,b,i):return(n,b,i)in OVERRIDES

def finish(summary):
    for n,b,i in set(OVERRIDES)-USED:
        need(summary[str(n)][b]['complete']is False,'selected override cannot silently disappear into a complete original family')
        c.pending.append(dict(edge=f'n{n} {b} p{i} selected composite',path=str(OVERRIDES[n,b,i].relative_to(R)),status='ORIGINAL_SELECTED_RESOURCE_CHAIN_NOT_REACHED'))

def parent_scope(n,b,i,cfg,contract,src,freeze,m):
    z=dict(n=n,band=b,index=i,original_p=cfg['p'],parent_capsule=str(src.relative_to(R)),contract_sha256=c.sha(src/'contract.json'),parent_protocol_sha256=c.sha(src/'count_protocol.py'),parent_constructor_sha256=c.sha(src/'construct_alpha4.py'),kernel_manifest_sha256=c.sha(src/'KERNEL_COPY_MANIFEST.json'),kernel_sha256=m['files'],source_freeze=str(freeze.relative_to(R)),source_freeze_sha256=c.sha(freeze))
    for k in ['resource_candidate_sha256','resource_replay_sha256','resource_row_sha256']:z[k]=contract[k]
    return z

def subdomain_scope(parent,part,cuts):
    z=dict(schema='ORIGINAL_CONTRACT_FOUR_CLOSED_P_SUBPANELS_V1',n=parent['n'],band=parent['band'],index=parent['index'],part=part,parts=4,original_p=parent['original_p'],cuts=cuts,p=cuts[part:part+2])
    for k in ['contract_sha256','parent_capsule','parent_protocol_sha256','parent_constructor_sha256','kernel_manifest_sha256','resource_candidate_sha256','resource_replay_sha256','resource_row_sha256']:z[k]=parent[k]
    return z

def protocol_scope(src,d,parent,sub,root):
    """Reconstruct the finite approved port, without executing SOURCE_OPERATIONS."""
    original=(src/'count_protocol.py').read_text();want=original;ops=[]
    def rep(before,after):
        nonlocal want
        need(want.count(before)==1,'single independent subpanel source substitution '+before[:90]);want=want.replace(before,after);ops.append([before,after])
    rep('import json,sys,time','import json,sys,time\nimport subdomain_scope as restriction')
    rep("CONTRACT_SHA='"+parent['contract_sha256']+"'","CONTRACT_SHA='"+parent['contract_sha256']+"'\nSUBDOMAIN_SHA='"+c.sha(d/'SUBDOMAIN.json')+"'\nPARENT_SHA='"+c.sha(d/'PARENT.json')+"'\nRESTRICTION_SHA='"+c.sha(d/'subdomain_scope.py')+"'\nPART="+str(sub['part']))
    extra="""def subdomain(cfg):
 need(sha(HERE/'SUBDOMAIN.json')==SUBDOMAIN_SHA and sha(HERE/'PARENT.json')==PARENT_SHA,'fixed original lineage and subdomain')
 need(sha(HERE/'subdomain_scope.py')==RESTRICTION_SHA,'fixed restriction implementation')
 z=json.loads((HERE/'SUBDOMAIN.json').read_text(),object_pairs_hook=unique)
 parent=json.loads((HERE/'PARENT.json').read_text(),object_pairs_hook=unique)
 contract=json.loads((HERE/'contract.json').read_text(),object_pairs_hook=unique)
 need(parent['contract_sha256']==CONTRACT_SHA and parent['kernel_sha256']==json.loads((HERE/'KERNEL_COPY_MANIFEST.json').read_text(),object_pairs_hook=unique)['files'],'same original contract and24 kernels')
 return restriction.validate(z,cfg,contract,parent,PART)
"""
    rep('def load():',extra+'def load():')
    rep(' return cfg,bound',' subdomain(cfg)\n return cfg,bound')
    rep("def rootbox(cfg):return[[F(x)for x in cfg['p']],[F(0),F(cfg['Lambda'])],[F(0),F(1)],[-F(1,2),F(1,2)],[F(0),F(cfg['d0'])]]","def rootbox(cfg):\n s=subdomain(cfg)\n return[[F(x)for x in s['p']],[F(0),F(cfg['Lambda'])],[F(0),F(1)],[-F(1,2),F(1,2)],[F(0),F(cfg['d0'])]]")
    oldheader=next(x for x in original.splitlines()if x.startswith('def header(bound):'))
    newheader=f"def header(bound):return dict(schema='ORIGINAL_CONTRACT_CLOSED_P_SUBPANEL_COUNT_FOREST_V1',n={parent['n']},index={parent['index']},target=str(CE_LO),contract_sha256=sha(HERE/'contract.json'),kernel_sha256=bound,checker_sha256=sha(Path(__file__)),subdomain_sha256=SUBDOMAIN_SHA,parent_sha256=PARENT_SHA,restriction_sha256=RESTRICTION_SHA,part=PART,parts=4,root_domain={root!r})"
    rep(oldheader,newheader)
    rep(' began=time.time();cache={};stats=replay(candidate,cfg,bound,cache)'," began=time.time();cache={};stats=replay(candidate,cfg,bound,cache)\n subdomain_controls=restriction.controls(subdomain(cfg),cfg,json.loads((HERE/'contract.json').read_text(),object_pairs_hook=unique),json.loads((HERE/'PARENT.json').read_text(),object_pairs_hook=unique),PART)")
    additions=""" mutations.extend([('wrong subdomain hash',lambda x:x.update(subdomain_sha256='0'*64)),('wrong parent lineage',lambda x:x.update(parent_sha256='0'*64)),('wrong restriction source',lambda x:x.update(restriction_sha256='0'*64)),('wrong component',lambda x:x.update(part=(PART+1)%4)),('boolean component',lambda x:x.update(part=False)),('wrong component count',lambda x:x.update(parts=5)),('changed original noise domain',lambda x:x['root_domain'][1].__setitem__(1,'0')),('changed original alpha domain',lambda x:x['root_domain'][2].__setitem__(1,'0')),('changed original phase domain',lambda x:x['root_domain'][3].__setitem__(0,'0')),('changed original inward domain',lambda x:x['root_domain'][4].__setitem__(1,'0'))])
"""
    rep(' controls=[]',additions+' controls=[]')
    oldout=next(x for x in original.splitlines()if x.startswith(' out=dict(status='))
    newout=oldout.replace(oldout.split("status='")[1].split("'")[0],'PASS_FRESH_CONDITIONAL_CLOSED_P_SUBPANEL')
    newout=newout.replace('seconds=time.time()-began,scope=',"seconds=time.time()-began,part=PART,parts=4,subdomain_sha256=SUBDOMAIN_SHA,parent_sha256=PARENT_SHA,restriction_sha256=RESTRICTION_SHA,root_domain=header(bound)['root_domain'],subdomain_negative_controls=subdomain_controls,scope=")
    newout=newout.replace('Every original root box and leaf is reconstructed;','Every restricted-p root box and leaf is reconstructed, keeping all four other original coordinates;')
    rep(oldout,newout)
    need((d/'count_protocol.py').read_text()==want,'entire independently reconstructed native subpanel protocol')
    expected=dict(parent_protocol_sha256=parent['parent_protocol_sha256'],operations=ops)
    need(c.same(c.load(d/'SOURCE_OPERATIONS.json',False),expected),'no undeclared component source operation')
    c.bind(d/'count_protocol.py');c.bind(d/'PORT.diff')
    bad=deepcopy(expected);bad['operations'].append(['assert','pass #'])
    c.reject(lambda:need(c.same(bad,expected),'extra source edit'),'composite extra source weakening')
    c.reject(lambda:need((d/'count_protocol.py').read_text()+'\npass\n'==want,'changed source'),'composite changed complete checker')

def header_scope(obj,n,i,j,d,m,root,forest=False):
    expected=dict(n=n,index=i,part=j,parts=4,contract_sha256=c.sha(d/'contract.json'),kernel_sha256=m['files'],checker_sha256=c.sha(d/'count_protocol.py'),subdomain_sha256=c.sha(d/'SUBDOMAIN.json'),parent_sha256=c.sha(d/'PARENT.json'),restriction_sha256=c.sha(d/'subdomain_scope.py'),root_domain=root)
    for k,v in expected.items():need(k in obj and c.same(obj[k],v),'exact component header '+k)
    if forest:
        need(obj['schema']=='ORIGINAL_CONTRACT_CLOSED_P_SUBPANEL_COUNT_FOREST_V1','named restricted forest theorem')
        need(set(obj)==set(expected)|{'schema','target','roots'},'no undeclared forest fields')
    else:need(obj['status']=='PASS_FRESH_CONDITIONAL_CLOSED_P_SUBPANEL','complete literal component native acceptance')

def row_scope(row,n,b,i,j,d,freeze,part):
    for k,v in dict(n=n,band=b,index=i,part=j,parts=4,p=part['p'],source_freeze_sha256=c.sha(freeze),contract_sha256=c.sha(d/'contract.json'),subdomain_sha256=c.sha(d/'SUBDOMAIN.json'),parent_sha256=c.sha(d/'PARENT.json')).items():need(k in row and c.same(row[k],v),'literal component row '+k)
    need(row['status']=='FRESH_NATIVE_CLOSED_P_SUBPANEL_ACCEPTED_CONDITIONAL','fresh complete component status')

def capture_scope(ex,n,b,i,j,action,d,freeze,graph,path,expectedpath):
    for k,v in dict(n=n,band=b,index=i,part=j,action=action,source_freeze_sha256=c.sha(freeze)).items():need(k in ex and c.same(ex[k],v),'component child '+k)
    need(c.integer(ex['returncode'])==0 and ex['timed_out']is False and ex['interrupted']is False,'complete successful native component child')
    command=[sys.executable,'-B','-u']+(['construct_alpha4.py']if action=='construct'else['count_protocol.py','accept'])
    need(ex['command']==command and ex['cwd']==str(d)and path==expectedpath,'exact component command/cwd/capture')
    need(c.same(ex['input_sha256'],graph),'complete captured native source graph')
    need(c.integer(ex['budget_seconds'])==(300 if action=='construct'else 900)and c.integer(ex['termination_grace_seconds'])==5,'unchanged named discovery/replay capture budgets')

def count(n,b,i,desc,cfg,freeze):
    key=n,b,i;USED.add(key);family=OVERRIDES[key];fp=family/'FROZEN.json'
    if c.missing(fp,f'n{n} {b} p{i} four-component source freeze'):return None
    frozen=c.load(fp);src=selected(n,b)['count']/b/f'capsule{i}'
    contract=c.load(src/'contract.json',False);m=c.load(src/'KERNEL_COPY_MANIFEST.json',False)
    e.source_scope(n,b,i,src,cfg,desc,m)
    failed=c.load(src/'CONSTRUCTION_RUN.json',False)
    need(failed['status']=='BOUNDED_CONSTRUCTION_NOT_COMPLETE','original failed attempt retained; no old forest promoted')
    parent=parent_scope(n,b,i,cfg,contract,src,freeze,m)
    flavor='fine'if selected(n,b)['fine']else'baseline'
    for k,v in dict(status='PREPARED_FOUR_CLOSED_P_SUBPANELS_NOT_EXECUTED',family=family.name,n=n,band=b,index=i,flavor=flavor,original_contract_sha256=parent['contract_sha256'],original_capsule=str(src.relative_to(R)),original_p=cfg['p']).items():need(k in frozen and c.same(frozen[k],v),'literal selected composite family '+k)
    need(type(frozen['parts'])is list and len(frozen['parts'])==4,'all four prepared components')
    parts=[dict(component=z['part'],p=z['p'])for z in frozen['parts']];g.partition(cfg,parts);g.controls(cfg)
    cuts=[parts[0]['p'][0]]+[z['p'][1]for z in parts];need(frozen['cuts']==cuts,'complete canonical cuts')
    statistics=[];outputs=[];complete=True
    for j,dd in enumerate(frozen['parts']):
        d=family/f'part{j:02d}';p=parts[j]['p'];sub=subdomain_scope(parent,j,cuts)
        wantdesc=dict(part=j,directory=str(d.relative_to(R)),p=p,subdomain_sha256=c.sha(d/'SUBDOMAIN.json'),parent_sha256=c.sha(d/'PARENT.json'),protocol_sha256=c.sha(d/'count_protocol.py'),constructor_sha256=c.sha(d/'construct_alpha4.py'))
        need(c.same(dd,wantdesc),'exact prepared component descriptor')
        need(c.same(c.load(d/'PARENT.json',False),parent)and c.same(c.load(d/'SUBDOMAIN.json',False),sub),'independently derived original lineage and restricted domain')
        for name,h in m['files'].items():c.bind(d/name,h)
        c.bind(d/'KERNEL_COPY_MANIFEST.json',parent['kernel_manifest_sha256']);c.bind(d/'contract.json',parent['contract_sha256']);c.bind(d/'construct_alpha4.py',parent['parent_constructor_sha256'])
        c.bind(P/'subdomain_scope.py');c.bind(d/'subdomain_scope.py',c.sha(P/'subdomain_scope.py'))
        root=[p,['0',cfg['Lambda']],['0','1'],['-1/2','1/2'],['0',cfg['d0']]]
        protocol_scope(src,d,parent,sub,root)
        rp=d/'ROW_RESULT.json'
        if c.missing(rp,f'n{n} {b} p{i} component{j} full native replay'):complete=False;continue
        row=c.load(rp,False)
        if row['status']!='FRESH_NATIVE_CLOSED_P_SUBPANEL_ACCEPTED_CONDITIONAL':
            need(row['status']in['INTERRUPTED_OR_FAILED_SUBPANEL_CONSTRUCTION','BOUNDED_SUBPANEL_CONSTRUCTION_INCOMPLETE','SUBPANEL_FRESH_ACCEPTANCE_INCOMPLETE'],'known incomplete component status')
            c.pending.append(dict(edge=f'n{n} {b} p{i} component{j}',path=str(rp.relative_to(R)),status=row['status']));complete=False;continue
        row_scope(row,n,b,i,j,d,fp,parts[j])
        fpath=d/f'COUNT{i}_FOREST.json';apath=d/f'COUNT{i}_ACCEPTED.json'
        forest,accepted=c.load(fpath,False),c.load(apath,False)
        header_scope(forest,n,i,j,d,m,root,True);header_scope(accepted,n,i,j,d,m,root)
        need(accepted['forest_sha256']==row['forest_sha256']==c.sha(fpath)and row['accepted_sha256']==c.sha(apath),'selected complete component proof objects')
        stat=g.geometry(forest,cfg,n,parts[j])
        need(c.same(stat,accepted['statistics'])and c.same(stat,row['statistics'])and c.same(row['root_domain'],root),'independent full restricted-root geometry')
        need(c.integer(accepted['fresh_leaf_evaluations'])==stat['leaves'],'native fresh evaluation of every component leaf')
        for field,total in [('negative_controls',34),('subdomain_negative_controls',22)]:need(type(accepted[field])is list and len(accepted[field])==len(set(accepted[field]))==total,'complete component malformed controls '+field)
        construction=c.load(d/'CONSTRUCTION_RUN.json',False)
        need(construction['status']=='STORED_CONDITIONAL_FOREST_CONSTRUCTED_NOT_ACCEPTED'and construction['forest_sha256']==c.sha(fpath)and construction['contract_sha256']==parent['contract_sha256']and construction['fixed_acceptor_sha256']==c.sha(d/'count_protocol.py')and construction['constructor_sha256']==parent['parent_constructor_sha256'],'complete native construction bound to exact source')
        for action,expected in [('construct',construction),('accept',accepted)]:
            rr=row['runs'][action];cap=R/rr['path'];xp=cap/'EXECUTION.json';ex=c.load(xp,False)
            need(c.sha(xp)==rr['execution_sha256'],'selected component capture identity')
            expectedpath=R/'runs/cutoff10_20261018/fourier/subpanel_native_v1'/family.name/f'part{j:02d}_{action}01'
            capture_scope(ex,n,b,i,j,action,d,fp,frozen['files_sha256'],cap,expectedpath)
            for stream in ['stdout','stderr']:c.bind(cap/(stream+'.txt'),ex[stream+'_sha256'])
            need(not(cap/'stderr.txt').read_bytes()and c.same(c.read(cap/'stdout.txt'),expected),'complete native component output identity')
            started=c.load(cap/'STARTED.json',False)
            need(started['command']==ex['command']and started['cwd']==ex['cwd']and c.integer(started['pid'])>0 and started['pgid']==started['pid'],'captured exact native child start')
            for field,value in [('n',n+1),('part',j+1),('source_freeze_sha256','0'*64),('cwd',str(R)),('command',[sys.executable,'-B','other.py']),('returncode',1)]:
                bad=deepcopy(ex);bad[field]=value;c.reject(lambda:capture_scope(bad,n,b,i,j,action,d,fp,frozen['files_sha256'],cap,expectedpath),'component capture '+field)
        for field,value in [('part',j+1),('source_freeze_sha256','0'*64),('contract_sha256','0'*64),('p',cfg['p'])]:
            bad=deepcopy(row);bad[field]=value;c.reject(lambda:row_scope(bad,n,b,i,j,d,fp,parts[j]),'component row '+field)
        for axis in range(1,5):
            bad=deepcopy(forest);bad['root_domain'][axis]=['0','0'];c.reject(lambda:header_scope(bad,n,i,j,d,m,root,True),'component narrowed original root coordinate')
        for label,mutate in [('missing component count root',lambda z:z['roots'].pop()),('duplicate component count root',lambda z:z['roots'].__setitem__(1,deepcopy(z['roots'][0]))),('inflated component target',lambda z:z.update(target='1'))]:
            bad=deepcopy(forest);mutate(bad);c.reject(lambda:g.geometry(bad,cfg,n,parts[j]),label)
        statistics.append(stat);outputs.append(dict(directory=str(d.relative_to(R)),forest_sha256=c.sha(fpath),accepted_sha256=c.sha(apath)))
    if not complete:return None
    out=g.aggregate(n,parts,statistics)
    for row,extra in zip(out['component_statistics'],outputs):row.update(extra)
    out['composite_directory']=str(family.relative_to(R));out['composite_source_freeze_sha256']=c.sha(fp)
    return out
