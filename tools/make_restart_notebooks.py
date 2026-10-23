"""Build one coherent replacement set01–07 with automatic candidate restore."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('restart_private_phase2', ROOT/'tools/make_phase2_notebooks.py')
phase2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase2)
TARGETS = {
    '01_RESTART_n25_b3_p33': 'b3-p33',
    '02_RESTART_n25_b4_q0': 'b4-q0',
    '03_RESTART_n25_b4_q1': 'b4-q1',
    '04_RESTART_n25_b4_q2': 'b4-q2',
    '05_RESTART_n25_b4_q3': 'b4-q3',
    '06_RESTART_n25_b3_p31_v14': 'b3-p31-v14-new',
    '07_RESTART_n25_b3_p32_v14': 'b3-p32-v14-new',
}
SCOPE = '''This is the CURRENT replacement notebook for this numbered count job.
Upload it to Colab, choose CPU and Run all, and authorize the SAME Google Drive
used by the earlier01–07 runs. No path, command or parameter edits are required.
Keep every earlier results ZIP and the live backups. Do not run the old and new
version of the same numbered job simultaneously. Different numbered jobs may run
in parallel in separate sessions. Each session uses one discovery worker.

The notebook automatically locates the target's original hash-pinned sources and
most advanced compatible saved checkpoint. It preserves every existing tree,
saved leaf payload and pending region as UNTRUSTED candidate data. It does not
restart empty roots. An absent or incompatible cache produces an incomplete
diagnostic export; it cannot silently discard the saved work. The progress line
untrusted_checkpoint_migrated displays the restored leaf/node/pending counts.

The explicit resource epoch allows100000 nodes instead of10000,2GiB memory and
up to12 hours of search allocation in30-minute checkpointed slices. Fresh native
verification has its own12-hour CPU ceiling. These are limits, not an ETA or a
guarantee of convergence. New interruptions can be resumed with Run all.

The new sealed checker changes only the literal LIMIT assignment. All mathematical
kernels, contracts, exact targets, root domains, depth128, leaf comparisons and
24 corruption controls are unchanged. The original checker/design and candidate
bytes remain available. A complete candidate triggers fresh independent replay
of every leaf of all26 roots and all24controls under a strict Linux native guard.
Old saved numerical results are never substituted for that independent replay.

Conditional parent/resource and same-law analytic premises remain open. For the
portable V14 jobs06/07, the auxiliary C24 and attained positive-closed contact
premises remain explicit as well. This job cannot establish the global theorem.

Progress, one-minute Drive backups and a final evidence ZIP are automatic. Use
the UPDATED notebook24 from this same package after all seven count jobs and
both parent jobs09/10 have completed. Notebook25 is superseded by this set's04.
'''
phase2.JOBS = {name: dict(task='count-restart-'+target, tests='test_count_*.py',
    title='RESTART '+name[:2]+': '+target+' — restore saved candidate', scope=SCOPE,
    execute='from be_replay.count_recovery import run_colab\nRESULT = run_colab('+repr(target)+', durable_root=DURABLE)\n')
    for name, target in TARGETS.items()}


def build(pin, name):
    if not isinstance(pin, str) or not re.fullmatch(r'[0-9a-f]{40}', pin):
        raise ValueError('Immutable full code commit required')
    if name not in TARGETS:
        raise ValueError('Exactly one of the seven numbered restart notebooks')
    return phase2.build(pin, name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'colab')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name in TARGETS:
        path = args.output/(name+'.ipynb')
        path.write_text(json.dumps(build(args.pin, name), ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
        print(path)


if __name__ == '__main__':
    main()
