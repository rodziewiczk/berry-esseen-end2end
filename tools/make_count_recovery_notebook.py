"""Build notebook25: resume the stopped q2 forest in a declared resource epoch."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recovery_private_phase2', ROOT/'tools/make_phase2_notebooks.py')
phase2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase2)
NAME = '25_n25_b4_q2_checkpoint_recovery'
phase2.JOBS = {NAME: dict(
    task='b4-q2-node-limit-recovery', tests='test_count_*.py',
    title='b4-q2: recover the saved candidate after the 10000-node stop',
    scope='''Run this notebook after notebook04 stopped at its original 10000-node
limit. Select a CPU runtime and Run all, and authorize the SAME Google Drive.
No parameters, paths or command edits are needed. Keep the earlier result ZIP
and live Drive backups. Other running notebooks need no changes.

The notebook automatically reads the original pinned source closure and the most
advanced compatible saved q2 checkpoint. It preserves every existing tree and leaf
payload as UNTRUSTED candidate data. It never restarts empty roots. Later runs can
also resume this recovery profile's own saved checkpoints.

This is an explicitly NEW resource epoch with a global 100000-node ceiling. The
old 10000-node checker and its design remain unchanged. Exactly one literal LIMIT
assignment is changed in a new sealed checker copy; all mathematical kernels,
contracts, root domains, targets, depth128, leaf tests and24controls remain the same.
Old source and original candidate evidence are retained separately.

After candidate completion, a fresh independent native checker recomputes EVERY
leaf of ALL26 roots and runs ALL24 corruption controls. Partial search progress
cannot accept arithmetic. The original strict Linux native guard remains required;
there is no BASIC fallback for acceptance. Parent acquisitions and the all-index
proof remain unverified here.

Progress, one-minute Drive backups and the final results ZIP are automatic. Search
uses bounded slices with a three-hour allocation, followed by up to two hours of
native verification. These are limits, not an ETA or a convergence guarantee.
Use the updated notebook24 supplied with this recovery when joining the results;
its older pinned version does not recognize the explicitly new source identity.
''',
    execute='from be_replay.count_recovery import run_colab\nRESULT = run_colab(durable_root=DURABLE)\n')}


def build(pin):
    if not isinstance(pin, str) or not re.fullmatch(r'[0-9a-f]{40}', pin):
        raise ValueError('Immutable full code commit required')
    return phase2.build(pin, NAME)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'colab')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output/(NAME+'.ipynb')
    path.write_text(json.dumps(build(args.pin), ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(path)


if __name__ == '__main__':
    main()
