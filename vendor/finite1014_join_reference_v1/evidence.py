"""Exact capture and pinned-source joins; no inherited evaluator is imported."""
from pathlib import Path
from copy import deepcopy
import sys
import common as c
R,N=c.R,c.N
T=R/'work/cutoff15_20261017/supplied/continuation_cutoff20_20261016/b0/full_v1/capsule42'
need=c.need

def capture_claim(m,command,cwd,stdout,expected,required):
    need(c.integer(m['returncode'])==0,'captured success')
    need(m['command']==[sys.executable]+command and m['cwd']==str(cwd),'exact selected native command and cwd')
    need(type(stdout)is str and stdout.splitlines() and stdout.splitlines()[-1]==expected,'captured final status, literal scope and output digest')
    need(type(m['input_sha256'])is dict,'captured input graph')
    for p,d in required.items():need(m['input_sha256'].get(p)==d,'required captured stable input '+p)
    for p,d in m['input_sha256'].items():
        need(type(p)is str and not Path(p).is_absolute()and '..'not in Path(p).parts,'safe capture input path')
        need(type(d)is str and len(d)==64,'capture input digest')

def exact_capture(path,command,cwd,expected,required=None):
    required={}if required is None else required
    m=c.capture(path);stdout=(path/'stdout.txt').read_text()
    capture_claim(m,command,cwd,stdout,expected,required)
    for p,d in m['input_sha256'].items():c.bind(cwd/p,d)
    for label,mutate in [('capture wrong cwd',lambda x:x.update(cwd=str(R))),('capture wrong command',lambda x:x.update(command=[sys.executable,'-B','other.py'])),('capture failed return',lambda x:x.update(returncode=1))]:
        z=deepcopy(m);mutate(z);c.reject(lambda:capture_claim(z,command,cwd,stdout,expected,required),label)
    c.reject(lambda:capture_claim(m,command,cwd,stdout+'wrong digest\n',expected,required),'capture forged final output digest')
    if required:
        z=deepcopy(m);z['input_sha256'][next(iter(required))]='0'*64
        c.reject(lambda:capture_claim(z,command,cwd,stdout,expected,required),'capture wrong stable input digest')
    return m

def count_row_claim(row,n,b,i,freeze,contract):
    need(type(row['n'])is type(row['index'])is int and row['n']==n and row['band']==b and row['index']==i,'literal whole count row identity')
    need(row['source_freeze_sha256']==freeze and row['contract_sha256']==contract,'count row bound to selected frozen source family and contract')
    need(row['status']==f'FRESH_NATIVE_ACTUAL{n}_FULL_PANEL_ACCEPTED_CONDITIONAL','accepted whole count row')

def count_capture_claim(ex,n,b,i,action,d,expected_path,path):
    command=[sys.executable,'-B','-u']+(['construct_alpha4.py']if action=='construct'else['count_protocol.py','accept'])
    need(type(ex['n'])is type(ex['index'])is int and ex['n']==n and ex['band']==b and ex['index']==i and ex['action']==action,'literal child action')
    need(c.integer(ex['returncode'])==0 and ex['timed_out']is False and ex['interrupted']is False,'successful complete child action')
    need(ex['command']==command and ex['cwd']==str(d)and path==expected_path,'exact selected child command, cwd and capture path')

def apply_ops(source,ops):
    for before,after,count in ops:
        need(source.count(before)==count,'exact literal source substitution '+before)
        source=source.replace(before,after)
    return source

def source_scope(n,b,i,d,cfg,desc,m):
    """Derive all allowed substitutions; never execute a declared transform."""
    tm=c.load(T/'KERNEL_COPY_MANIFEST.json',False);oldcfg=c.load(T/'contract.json',False)['rows'][0]
    for name in ['count_protocol.py','construct_alpha4.py']:c.bind(T/name)
    need(m['files']==tm['files']and len(m['files'])==24,'all24 unchanged mathematical modules')
    for name,digest in tm['files'].items():
        need(Path(name).name==name,'plain mathematical module name')
        c.bind(T/name,digest);c.bind(d/name,digest)
    origin={name:dict(source=str((T/name).relative_to(R)),sha256=digest)for name,digest in tm['files'].items()}
    need(c.same(m['origin'],origin),'exact module origins')
    schema=f'ACTUAL{n}_SHARP_{b}_P{i}_FRESH_COMPENSATED_RESOURCE_JOINT_CLOSED_COUNT_FOREST_V1'
    status=f'PASS_FRESH_CONDITIONAL_ACTUAL{n}_SHARP_{b}_JOINT_COUNT{i}'
    need(c.same(desc,dict(index=i,directory=str(d.relative_to(R)),schema=schema,status=status,contract_sha256=c.sha(d/'contract.json'))),'independently derived literal count descriptor')
    ops=[("CONTRACT_SHA='"+c.sha(T/'contract.json')+"'","CONTRACT_SHA='"+c.sha(d/'contract.json')+"'",1),("cfg['n']==20",f"cfg['n']=={n}",1),("cfg['index']==42","cfg['index']=="+str(i),1),('fixed actual20 feedback sharp panel42',f'fixed actual{n} {b} sharp panel{i}',1),("cfg['p']=="+repr(oldcfg['p']),"cfg['p']=="+repr(cfg['p']),1),("F(cfg['rho_lower'])==F('"+oldcfg['rho_lower']+"') and F(cfg['rho_upper'])==F('"+oldcfg['rho_upper']+"')","F(cfg['rho_lower'])==F('"+cfg['rho_lower']+"') and F(cfg['rho_upper'])==F('"+cfg['rho_upper']+"')",1),('ACTUAL20_SHARP_B0_P42_FEEDBACK_FAMILY_JOINT_CLOSED_COUNT_FOREST_V1',schema,1),('n=20,index=42',f'n={n},index={i}',2),('range(21)',f'range({n+1})',1),('len(roots)==21',f'len(roots)=={n+1}',1),('all nearest counts0 through20',f'all nearest counts0 through{n}',1),('PASS_FRESH_CONDITIONAL_ACTUAL20_SHARP_B0_FEEDBACK_FAMILY_JOINT_COUNT42',status,1),('COUNT42_FOREST.json',f'COUNT{i}_FOREST.json',2),('COUNT42_ACCEPTED.json',f'COUNT{i}_ACCEPTED.json',1)]
    cops=[('range(21)',f'range({n+1})',1),('COUNT42',f'COUNT{i}',1),('time.time()-started<=300','time.time()-started<=270',1)]
    expected=dict(template=str(T.relative_to(R)),math_files=tm['files'],protocol_operations=[list(x)for x in ops],constructor_operations=[list(x)for x in cops])
    transforms=c.load(d/'SOURCE_TRANSFORMS.json',False)
    need(c.same(transforms,expected),'only independently permitted source transformations')
    for name,operations in [('count_protocol.py',ops),('construct_alpha4.py',cops)]:
        c.bind(d/name);want=apply_ops((T/name).read_text(),operations)
        need((d/name).read_text()==want,'complete count source reconstruction '+name)
    c.bind(d/'SOURCE_PORT.diff')
    wrong=deepcopy(transforms);wrong['protocol_operations'].append(['assert','pass #',1])
    c.reject(lambda:need(c.same(wrong,expected),'extra source substitution'),'extra undeclared source weakening')
    c.reject(lambda:need((d/'count_protocol.py').read_text()+'\npass\n'==apply_ops((T/'count_protocol.py').read_text(),ops),'changed checker'),'changed complete checker source')
