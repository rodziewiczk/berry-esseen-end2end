"""Prepare unchanged reference bytes and AST-equal typed interface projections.

This script reads original text as data. It never imports or executes an
original module, function, kernel or protocol.
"""
from pathlib import Path
from hashlib import sha256
import ast
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE_SHA='268f71662171764d7ebe116910b5df82dfd58cadb2de2a7ef82db7da98b66dae'
FILES={
 'actual15.py':'cutoff15_20261017/audit/actual15_join_v1/check.py',
 'sequential.py':'cutoff15_20261017/audit/sequential16_19_join_v2/common.py',
 'ACTUAL15_PROOF.txt':'cutoff15_20261017/audit/actual15_join_v1/PROOF.txt',
 'SEQUENTIAL_PROOF.txt':'cutoff15_20261017/audit/sequential16_19_join_v2/PROOF.txt',
}


def prepare(archive):
    archive=Path(archive)
    h=sha256()
    with archive.open('rb')as f:
        for block in iter(lambda:f.read(1024**2),b''):h.update(block)
    if h.hexdigest()!=ARCHIVE_SHA:raise ValueError('Pinned entire original source archive')
    with zipfile.ZipFile(archive)as z:raw={n:z.read(p)for n,p in FILES.items()}
    vendor=ROOT/'vendor/finite1519_join_reference_v1'
    vendor.mkdir(parents=True,exist_ok=True)
    for name,value in raw.items():(vendor/name).write_bytes(value)
    license=(ROOT/'LICENSE').read_bytes();(vendor/'LICENSE').write_bytes(license)
    provenance=dict(schema='ORIGINAL_FINITE1519_JOIN_REFERENCE_V1',
        scope='Unchanged original reference text, never imported by the new finite join.',
        archive_sha256=ARCHIVE_SHA,license_sha256=sha256(license).hexdigest(),
        files={name:dict(archive='cutoff5_10_15.zip',member=FILES[name],bytes=len(value),sha256=sha256(value).hexdigest())for name,value in raw.items()},
        original_mathematics_imported=False,arithmetic_computed=False,all_index_conclusion_verified=False)
    (vendor/'PROVENANCE.json').write_bytes((json.dumps(provenance,indent=2)+'\n').encode())
    def function(name,source,newname=None):
        text=raw[source].decode('utf-8');node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name)
        text=ast.get_source_segment(text,node)
        if newname:text=text.replace('def '+name+'(','def '+newname+'(',1)
        return text
    pieces=[
        function('floorgrid','sequential.py'),function('ceilgrid','sequential.py'),function('polymin','sequential.py'),
        function('interface','actual15.py','interface_actual15'),function('interface','sequential.py','interface_sequential'),
    ]
    header='''"""Pure source-bound resource/contract comparisons for full57H.

The two literal-index interface functions retain the complete original ASTs,
apart from their names. No original mathematical module is imported. Full
numerical evidence must already have been validated before these comparisons.
Copyright (c)2026 Kacper Rodziewicz and Bartosz Kolodziejek; MIT, see reference LICENSE.
"""
from fractions import Fraction as F
from pathlib import Path
import ast
from .finite1519_join_control_sources import need,digest,ROOT
from .finite1014_join_epoch import same
BANDS={'B0':('1','11/10','417/1000','219/2000','23/10','191/500'),
       'BN':('11/10','23/20','827/2000','57/1000','12/5','409/1000')}
'''
    refs={name:sha256(raw[name]).hexdigest()for name in('actual15.py','sequential.py')}
    header+='REFERENCE_SHA256='+repr(refs)+'\n\n'
    verify='''
def verify_reference_projection():
    root=ROOT/'vendor/finite1519_join_reference_v1'
    own={n.name:n for n in ast.parse(Path(__file__).read_text('utf-8')).body if isinstance(n,ast.FunctionDef)}
    for source,selected in(('actual15.py',{'interface':'interface_actual15'}),
            ('sequential.py',{'floorgrid':'floorgrid','ceilgrid':'ceilgrid','polymin':'polymin','interface':'interface_sequential'})):
        need(digest(root/source)==REFERENCE_SHA256[source],'Pinned complete original literal-index interface source')
        original={n.name:n for n in ast.parse((root/source).read_text('utf-8')).body if isinstance(n,ast.FunctionDef)}
        for old,new in selected.items():
            node=original[old];node.name=new
            need(ast.dump(node,include_attributes=False)==ast.dump(own[new],include_attributes=False),
                 'Every original simultaneous resource/contract condition and directed rounding retained')
    return dict(REFERENCE_SHA256)


def interface(row,cfg,band,index,n):
    need(type(n)is int and 15<=n<=19,'Literal complete finite15--19 interface domain')
    need(type(index)is int and 0<=index<100 and type(band)is str and band in BANDS,'Literal original probability panel and band')
    if n==15:return interface_actual15(row,cfg,band,index)
    return interface_sequential(row,cfg,band,index,n)


def sequential(base,local):
    need(type(base)is bool and type(local)is dict and set(local)=={15,16,17,18,19}
         and all(type(n)is int and type(v)is bool for n,v in local.items()),'Exact consecutive finite15--19 scope')
    current=base;out=[]
    for n in range(15,20):
        previous=current;current=previous and local[n]
        out.append(dict(n=n,global_predecessor=n-1,predecessor_established=previous,
            conditional_local_implication_complete=local[n],conditional_finite_result_established=current))
    return out
'''
    output=ROOT/'be_replay/finite1519_join_interfaces.py'
    output.write_bytes((header+'\n\n'.join(pieces)+'\n\n'+verify).encode('utf-8'))
    print('Prepared original text and pure interface projection; no original execution.',sha256(output.read_bytes()).hexdigest())


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('archive');args=parser.parse_args();prepare(args.archive)
