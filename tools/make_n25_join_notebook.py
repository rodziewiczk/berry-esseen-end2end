"""Build queued notebook24: fresh seven-count n25 interface evidence join."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('n25_private_phase2',ROOT/'tools/make_phase2_notebooks.py')
phase2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase2)
NAME = '24_n25_seven_count_interfaces'
phase2.JOBS = {NAME: dict(
    task='n25-seven-interfaces', tests='test_n25_*.py',
    title='n25: fresh parent evidence and the seven selected count interfaces',
    scope='''This is a queued evidence join. Run it after notebooks 01–07 and 09/10
have completed and saved their successful results ZIPs on the same Google Drive.
Upload this notebook, choose a CPU runtime, and select Run all. No parameter edits
are required. Existing calculations and their pinned source code need no changes.

The job discovers the completed exports automatically, checks their actual source,
native execution, capture, forest, corruption-control and complete parent-stage
bindings, and verifies the simultaneous resource-to-count contract implications.
Original evidence bytes and original execution contexts are preserved. It does
not repeat numerical leaf replay, search, INITIAL covers or resource calculations.

The B4 q0–q3 contracts are four closed probability quarters of the original p29
panel. The B3 p31/p32 jobs are explicitly new conditional V14 source epochs. Their
extra attained-contact premise and the global auxiliary24 acquisition remain
explicit analytic obligations. This job does not acquire those facts by setting
contract fields or by copying historical receipt hashes.

If inputs are missing or incompatible, the result is WAITING_FOR_N25_EVIDENCE.
Rerun after the missing jobs finish. A successful result verifies only these seven
selected interfaces; it does not complete all n25 branches or the global proof.
Progress, one-minute Drive copies and a final evidence ZIP are automatic.
''',
    execute='from be_replay.n25_collect import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n')}


def build(pin):
    if not isinstance(pin,str) or not re.fullmatch(r'[0-9a-f]{40}',pin):
        raise ValueError('Immutable full code commit required')
    return phase2.build(pin,NAME)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin',required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'colab')
    args=parser.parse_args()
    notebook=build(args.pin)
    args.output.mkdir(parents=True,exist_ok=True)
    path=args.output/(NAME+'.ipynb')
    path.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(path)


if __name__=='__main__':
    main()
