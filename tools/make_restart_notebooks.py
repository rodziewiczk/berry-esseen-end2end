"""Build the seven PREFIX2 resume notebooks against one immutable code commit."""
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
SCOPE = '''This version resumes the saved candidate with the restored PREFIX2
discovery policy, **RESTORED_PREFIX2_V1: alpha 16, depth first**.

**Switch from an earlier session:** wait for its next `backup_saved` message,
then stop that old numbered job before running this version. Keep its logs,
results ZIPs and live Drive backups. Open the corresponding new number, choose
CPU, select Run all, and authorize the SAME Google Drive. No ordinary path or
parameter edits are required. Different numbered jobs may use separate sessions;
each session runs one discovery worker.

The existing backup directory remains
`/content/drive/MyDrive/Berry-Esseen-end2end/<target>/`.
Before search, the controller reports the selected saved checkpoint, its hash,
and the restored node/leaf/pending counts. It compares validated tree ancestry;
it does not choose a branch merely because its timestamp or leaf count is larger.
Equivalent backup copies are harmless. Incomparable maximal candidates cause an
explicit incomplete diagnostic instead of a guessed choice. A missing or
incompatible cache also stops: this notebook never silently starts empty roots.

Every selected tree, saved leaf payload and pending region is retained as
UNTRUSTED candidate data. Strategy/header migration is recorded separately from
the original checkpoint bytes. No old leaf decision becomes an accepted proof.
Rerun this same notebook after an interruption to select the compatible saved
descendant. Already accepted results require full evidence revalidation before
reuse; their labels alone cannot skip verification.

The source epoch retains the 100000-node ceiling, depth 128, 2 GiB memory and
up to 12 hours of search allocation in 30-minute checkpointed slices. Fresh
native verification has a separate 12-hour CPU ceiling and a 12-hour-plus-five-
minute wall ceiling. These are limits, not an ETA or a convergence guarantee.
The existing 128 MiB checkpoint/input/backup-file cap and 256 MiB discovery disk
quota also remain. A quota stop is incomplete; files above the backup cap may be
omitted, and a later run selects the compatible checkpoint actually preserved.

The PREFIX2 change concerns discovery strategy. The native checker retains the
sealed resource-only LIMIT change from 10000 to 100000. Mathematical kernels,
contracts, exact targets, all 26 closed root domains, strict leaf comparisons and
all 24 corruption controls are unchanged. A complete candidate triggers a fresh
full native replay under the strict Linux guard, unless an already completed
native export has been revalidated. Saved search values cannot replace replay.

Conditional parent/resource and same-law analytic premises remain open. For the
portable V14 jobs 06/07, the auxiliary C24 and attained positive-closed contact
premises remain explicit too. This job cannot establish the global theorem.

Progress, one-minute Drive backups and a final evidence ZIP are automatic.
Preserve the final ZIP and its SHA-256 sidecar. Use the matching updated notebook
24 after all seven count jobs and both parent jobs 09/10 have completed. Notebook
25 is superseded by this set's 04.
'''
phase2.JOBS = {name: dict(task='count-restart-'+target, tests='test_count_*.py',
    title='PREFIX2 resume '+name[:2]+': '+target, scope=SCOPE,
    execute='from be_replay.count_recovery import DISCOVERY_STRATEGY, run_colab\n'
            'if DISCOVERY_STRATEGY != "RESTORED_PREFIX2_V1":\n'
            '    raise RuntimeError("The pinned driver does not provide the required PREFIX2 resume policy.")\n'
            'print("Restoring the saved candidate before search: RESTORED_PREFIX2_V1, alpha 16, depth first.", flush=True)\n'
            'RESULT = run_colab('+repr(target)+', durable_root=DURABLE)\n')
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
