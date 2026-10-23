"""Explicit fresh CAPS metadata epoch; no Fourier/resource arithmetic here.

The caller must separately validate the actual complete INITIAL, owncap
construct/replay, original readback and check_caps executions. Hash rebinding
alone neither acquires their premises nor completes a numerical action.
Existing finite69_metadata and notebooks40--45 remain unchanged.
"""
from __future__ import annotations
import copy
from fractions import Fraction
import hashlib
import json
import re

from . import finite69_metadata as initial_epoch

CAPS_PATH="work/cutoff6_20261020/entry/resource7_9_v2/CAPS_CHECKED.json"
ORIGINAL_CAPS_SHA="616bb25496af353963f74f9165342cd5fe85ba387bc5cb49e161199955b5ac08"
OWN="runs/cutoff6_20261018/fourier/owncaps6_9_v1/"
READBACK="work/cutoff6_20261018/audit/supported_fourier_readback_v1/"
DYNAMIC=frozenset([OWN+"plan01/PLAN.json",READBACK+"OWN_REQUEST.json",READBACK+"OWN_RESULT.json"]+
    [OWN+label+"/"+name for label in("construct01","replay01")
     for name in("metadata.json","RESULT.json","stdout.txt","stderr.txt")])
CAPS={"B0":{"7":"2107/5000","8":"1051/2500","9":"4197/10000"},
      "BN":{"7":"4163/10000","8":"2077/5000","9":"1037/2500"},
      "B2":{"7":"4119/10000","8":"1027/2500","9":"41/100"}}
TARGETS={"B0":Fraction(423,1000),"BN":Fraction(209,500),"BC":Fraction(207,500)}


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(raw):
    need(type(raw)is bytes,"Literal source/receipt byte stream")
    return hashlib.sha256(raw).hexdigest()


def read(raw):
    def unique(pairs):
        out={}
        for key,value in pairs:
            need(key not in out,"No duplicate metadata keys");out[key]=value
        return out
    def bad(value):raise ValueError("Nonfinite metadata: "+value)
    need(type(raw)is bytes and len(raw)<=32*1024**2,"Bounded literal metadata bytes")
    return json.loads(raw,object_pairs_hook=unique,parse_constant=bad)


def dump(packet):return(json.dumps(packet,indent=2)+"\n").encode("utf-8")


def same(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
    return a==b


def cap_binding(old_caps,fresh_caps,source_pins,fresh_files_sha256):
    """Check only a declared metadata transformation, never its execution."""
    need(sha(old_caps)==ORIGINAL_CAPS_SHA==source_pins[CAPS_PATH],"Externally pinned original CAPS statement")
    old,fresh=read(old_caps),read(fresh_caps)
    need(type(old)is dict and type(fresh)is dict and old.keys()==fresh.keys(),"Entire original CAPS schema")
    changing={"files_sha256","accepted_upper","strips_per_band"}
    need(same({k:v for k,v in old.items()if k not in changing},
              {k:v for k,v in fresh.items()if k not in changing}),
         "Only fresh source commitments, exact maxima and strip allocation may vary")
    need(fresh["status"]=="PASS_EXACT_TIGHTER_LITERAL7_9_OWNCAPS"and fresh["caps"]==CAPS
         and type(fresh["whole_accepted_rows"])is int and fresh["whole_accepted_rows"]==344
         and type(fresh["selected_n_rows"])is int and fresh["selected_n_rows"]==258,
         "Original fixed86-strip/344-row scope and nine exact tighter caps")
    old_graph,new_graph=old["files_sha256"],fresh["files_sha256"]
    need(type(old_graph)is dict and type(new_graph)is dict and len(old_graph)==182
         and old_graph.keys()==new_graph.keys()and DYNAMIC<=old_graph.keys(),
         "Complete182-row original ancestor graph and explicit dynamic subset")
    need(type(fresh_files_sha256)is dict and fresh_files_sha256.keys()==new_graph.keys()|{CAPS_PATH},
         "Whole actual fresh ancestor/caps byte inventory, not selected hashes")
    for path,old_pin in old_graph.items():
        pin=new_graph[path]
        need(type(pin)is str and re.fullmatch(r"[0-9a-f]{64}",pin)is not None,
             "Literal source or fresh-capture SHA256")
        need(old_pin==source_pins[path],"Original ancestor equals its external fixed pin")
        need(pin==fresh_files_sha256[path],"Fresh graph equals whole actual file inventory")
        if path not in DYNAMIC:need(pin==old_pin,"Every arithmetic/source/static byte remains unchanged")
    need(fresh_files_sha256[CAPS_PATH]==sha(fresh_caps),"Actual complete fresh CAPS bytes")
    counts=fresh["strips_per_band"]
    need(type(counts)is dict and counts.keys()==TARGETS.keys()
         and all(type(v)is int and v>0 for v in counts.values())and sum(counts.values())==86,
         "Literal complete three-band86-strip allocation")
    upper=fresh["accepted_upper"]
    need(type(upper)is dict and upper.keys()==TARGETS.keys(),"All exact fresh band maxima")
    for band,values in upper.items():
        need(type(values)is dict and values.keys()=={"6","7","8","9"},"All four literal indices")
        for n,value in values.items():
            need(type(value)is str,"Exact rational maximum")
            rational=Fraction(value)
            need(str(rational)==value and 0<rational<TARGETS[band],"Canonical maximum below original strict target")
            if n!="6":
                cap_band="B2"if band=="BC"else band
                need(Fraction(819,2000)<rational<Fraction(CAPS[cap_band][n]),
                     "Same strict original tighter-cap range")
    return old_graph,new_graph


def derive_resource_epoch(original_replay,prepared,source_result,fresh_initial,old_caps,fresh_caps,
                          *,n,band,source_pins,fresh_files_sha256):
    """Bind the unchanged resource replay to actual fresh INITIAL and CAPS.

    All original templates are retained elsewhere. The base helper performs
    its full exact original-template/INITIAL checks. This layer permits only
    the11 named fresh owncap/readback ancestor commitments and CAPS receipt
    commitment to change, retaining every original numerical resource row,
    nested duration, cap, support plan and mathematical source byte.
    """
    old_graph,new_graph=cap_binding(old_caps,fresh_caps,source_pins,fresh_files_sha256)
    derived=initial_epoch.derive_resource_epoch(original_replay,prepared,source_result,fresh_initial,
                                                n=n,band=band,source_pins=source_pins)
    before_source=read(derived["fresh_source_result_bytes"])
    before_prepared=read(derived["fresh_prepared_bytes"])
    fresh_source,fresh_prepared=copy.deepcopy(before_source),copy.deepcopy(before_prepared)
    replacements={path:new_graph[path]for path in DYNAMIC}|{CAPS_PATH:sha(fresh_caps)}
    for packet in(fresh_source,fresh_prepared):
        graph=packet["files_sha256"]
        need(old_graph.keys()<=graph.keys()and CAPS_PATH in graph,"Every original CAPS dependency remains explicit")
        for path in old_graph:need(graph[path]==old_graph[path],"No preexisting unreviewed CAPS rebind")
        need(graph[CAPS_PATH]==sha(old_caps),"Exact old CAPS reference before new epoch")
        for path,pin in replacements.items():graph[path]=pin
    new_source_bytes=dump(fresh_source)
    source_path=f"work/cutoff6_20261020/entry/resource7_9_accept_v2/n{n}_{band}/FRESH_SOURCE_RESULT.json"
    need(fresh_prepared["source_sha256"]==sha(derived["fresh_source_result_bytes"])
         and fresh_prepared["files_sha256"][source_path]==sha(derived["fresh_source_result_bytes"]),
         "Exact previous source template binding")
    fresh_prepared["source_sha256"]=sha(new_source_bytes)
    fresh_prepared["files_sha256"][source_path]=sha(new_source_bytes)
    # Reverse the whole permitted difference. Nothing numeric is discarded.
    reversed_source,reversed_prepared=copy.deepcopy(fresh_source),copy.deepcopy(fresh_prepared)
    for packet in(reversed_source,reversed_prepared):
        for path in replacements:packet["files_sha256"][path]=source_pins[path]
    reversed_prepared["source_sha256"]=before_prepared["source_sha256"]
    reversed_prepared["files_sha256"][source_path]=before_prepared["files_sha256"][source_path]
    need(same(reversed_source,before_source)and same(reversed_prepared,before_prepared),
         "Whole numeric/profile/plan/duration payload preserved under the exact metadata reverse map")
    result=dict(derived)
    result.update(fresh_source_result_bytes=new_source_bytes,fresh_prepared_bytes=dump(fresh_prepared))
    result["cap_epoch_report"]=dict(schema="FRESH_FINITE69_TIGHTER_CAP_SOURCE_EPOCH_V1",n=n,band=band,
        original_caps_sha256=sha(old_caps),fresh_caps_sha256=sha(fresh_caps),
        dynamic_ancestor_paths=sorted(DYNAMIC),complete_ancestor_rows=182,
        fresh_source_result_sha256=sha(result["fresh_source_result_bytes"]),
        fresh_prepared_sha256=sha(result["fresh_prepared_bytes"]),
        resource_replay_source_unchanged_from_initial_epoch=True,
        entire_original_resource_numeric_payload_unchanged=True,
        fresh_caps_execution_evidence_verified=False,fresh_initial_execution_evidence_verified=False,
        mathematical_arithmetic_computed=False,actual_support_acquired=False,
        full_finite69_verified=False,all_index_conclusion_verified=False)
    # Keep the base transformation as named intermediate provenance. The
    # canonical report must always bind the final byte streams returned here.
    result["intermediate_initial_epoch_report"]=copy.deepcopy(derived["report"])
    result["report"]=dict(derived["report"],
        schema="FRESH_FINITE69_INITIAL_AND_CAPS_RESOURCE_METADATA_EPOCH_V1",
        fresh_source_result_sha256=sha(result["fresh_source_result_bytes"]),
        fresh_prepared_sha256=sha(result["fresh_prepared_bytes"]),
        original_caps_sha256=sha(old_caps),fresh_caps_sha256=sha(fresh_caps),
        fresh_caps_execution_evidence_verified=False)
    return result
