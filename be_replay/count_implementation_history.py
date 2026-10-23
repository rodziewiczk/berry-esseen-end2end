"""Exact previously published count implementations, never an open history gate.

Discovery upgrades must not invalidate already exported native evidence. These
pins identify the pre-PREFIX2 runner at commit59bdc4d and its explicitly retained
q2 predecessor. They do not accept historical success summaries without the
existing complete source, execution, guard and arithmetic receipt checks.
"""
from __future__ import annotations

from copy import deepcopy


MIDPOINT_COUNT_IMPLEMENTATION = {
    "count_task_sha256": "63d3d1fbd415055317dc2a3640878d76e86a9b9af2980c1ccf7e48f08a890bea",
    "vendor": {
        "commit": "75a94708872e2bc053f42a279559b23ed91e4402",
        "files_sha256": {
            "count_discovery.py": "3b239119082d0d5275446beb2d38878c9a7c7988c655da6e52fd34023e485eb4",
            "prepare_missing_count.py": "b22f807a41982f017af14e88451d82fcda129ab13a2b09210ab543420f4aa410",
            "prepare_b3_v14_epoch_2026_10_22.py": "4116a054c2f725794d82cc4bd7b954023c9b8525d8f943c6cea2a8096aceb647",
        },
    },
    "supervisor_sha256": "61e71dd4a9653de2bbbee8c54928a1f5c5bffd0bf083dd324851716c3a1eaea2",
}
MIDPOINT_RECOVERY_PAIR = {
    "count_recovery_sha256": "0047c7e49d4e6b407fc6555c63602e243f6269300f007ff3432d067cae26e624",
    "count_limit_epoch_sha256": "5b3c2d17f1f566353e767c114628ac1940d6ca9f4d095771df2176589e5dfbe6",
}
LEGACY_Q2_PAIR = {
    "count_recovery_sha256": "d43057eb2f5fbf41466b74ac030491a93b72d1481cd22a3114332623b7ca64c0",
    "count_limit_epoch_sha256": "9dc980c2e23580feb9402f9f15c533cc76582808656cc7c23b1b3fc37b5082dc",
}


def ordinary():
    return deepcopy(MIDPOINT_COUNT_IMPLEMENTATION)


def recovery(*, legacy_q2=False):
    return dict(ordinary(), **(LEGACY_Q2_PAIR if legacy_q2 else MIDPOINT_RECOVERY_PAIR))


def matches(record, expected):
    """The Python version may vary; every executable pin must match as a unit."""
    return (type(record) is dict and set(record) == set(expected) | {"python"}
            and type(record.get("python")) is str and bool(record["python"])
            and all(type(record[key]) is type(value) and record[key] == value
                    for key, value in expected.items()))
