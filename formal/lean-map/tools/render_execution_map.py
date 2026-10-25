"""Render the architecture graph from one source; no runtime verification claim."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
NODES = [
    {"id": "project", "label": "One CLI + frozen project", "x": 52, "y": 292,
     "lines": ["be run project.toml --resume", "Exact theorem, sources, trust and policy"],
     "doc": "docs/architecture/01-protocol-and-types.md", "kind": "control"},
    {"id": "plan", "label": "Planner + dependency graph", "x": 536, "y": 292,
     "lines": ["Mathematical AND / OR coverage", "Separate runtime jobs; no cycles"],
     "doc": "docs/architecture/02-execution.md", "kind": "control"},
    {"id": "schedule", "label": "Parallel scheduler", "x": 1020, "y": 292,
     "lines": ["Legal chunks; measured CPU scaling", "Reserve time, memory and money"],
     "doc": "docs/architecture/05-compute-and-deployment.md", "kind": "control"},
    {"id": "produce", "label": "Numerical producers", "x": 52, "y": 520,
     "lines": ["Independent roots / panels / cells", "Candidate bytes; no proof authority"],
     "doc": "docs/architecture/02-execution.md", "kind": "candidate"},
    {"id": "verify", "label": "Independent verification", "x": 536, "y": 520,
     "lines": ["Exact statement + complete replay", "Source / arithmetic / trust bindings"],
     "doc": "docs/architecture/04-checkers-and-lean.md", "kind": "acceptance"},
    {"id": "cover", "label": "Complete coverage + assembly", "x": 1020, "y": 520,
     "lines": ["Every required root, seam and tail", "Exact dependency receipt closure"],
     "doc": "docs/architecture/04-checkers-and-lean.md", "kind": "acceptance"},
    {"id": "premises", "label": "Explicit analytic premises", "x": 52, "y": 748,
     "lines": ["Exact source statements and gates", "Accepted premises remain visible"],
     "doc": "docs/contracts/README.md", "kind": "premise"},
    {"id": "lean", "label": "Lean interface + trust bridge", "x": 536, "y": 748,
     "lines": ["Checked conditional composition", "JSON decoding is not a proof term"],
     "doc": "docs/architecture/04-checkers-and-lean.md", "kind": "premise"},
    {"id": "verdict", "label": "Final report: PASS / NO PASS", "x": 1020, "y": 748,
     "lines": ["PASS only for the requested whole", "Otherwise: reasons + remaining work"],
     "doc": "docs/architecture/02-execution.md", "kind": "acceptance"},
    {"id": "cas", "label": "Immutable bytes + exact cache", "x": 52, "y": 1040,
     "lines": ["Local CAS / Cloud Storage", "Candidates, receipts and checkpoints differ"],
     "doc": "docs/architecture/03-storage-and-recovery.md", "kind": "infra"},
    {"id": "ledger", "label": "Transactional runtime ledger", "x": 536, "y": 1040,
     "lines": ["SQLite / Firestore; fenced attempts", "Outbox, reservations and recovery"],
     "doc": "docs/architecture/03-storage-and-recovery.md", "kind": "infra"},
    {"id": "stop", "label": "Independent stop + liability", "x": 1020, "y": 1040,
     "lines": ["Absolute deadline; resource inventory", "Confirm shutdown; retain cost reserve"],
     "doc": "docs/architecture/05-compute-and-deployment.md", "kind": "infra"},
]
EDGES = [
    {"from": "project", "to": "plan", "meaning": "freeze and validate", "class": "runtime"},
    {"from": "plan", "to": "schedule", "meaning": "ready legal work", "class": "runtime"},
    {"from": "schedule", "to": "produce", "meaning": "dispatch admitted tasks", "class": "runtime"},
    {"from": "produce", "to": "verify", "meaning": "untrusted candidate", "class": "candidate"},
    {"from": "verify", "to": "cover", "meaning": "accepted scoped receipts", "class": "acceptance"},
    {"from": "premises", "to": "lean", "meaning": "explicit analytic assumptions", "class": "premise"},
    {"from": "cover", "to": "verdict", "meaning": "complete numerical evidence", "class": "acceptance"},
    {"from": "lean", "to": "verdict", "meaning": "conditional theorem linkage", "class": "premise"},
    {"from": "cas", "to": "produce", "meaning": "immutable inputs and candidate reuse", "class": "support"},
    {"from": "cas", "to": "verify", "meaning": "exact verification-key reuse", "class": "support"},
    {"from": "ledger", "to": "schedule", "meaning": "transactional dispatch authority", "class": "support"},
    {"from": "stop", "to": "schedule", "meaning": "close admission and cancel owned resources", "class": "support"},
]


def main() -> None:
    for node in NODES:
        if not (ROOT / node["doc"]).is_file():
            raise SystemExit(f"Missing linked specification: {node['doc']}")
    graph = {"format": "be-execution-map-v1", "status": "specified-not-implemented",
             "nodes": NODES, "edges": EDGES}
    (OUT / "execution-map.json").write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8", newline="\n")
    mmd = ["flowchart TB"]
    mmd += [f'  {n["id"]}["{n["label"]}"]' for n in NODES]
    mmd += [f'  {e["from"]} -->|"{e["meaning"]}"| {e["to"]}' for e in EDGES]
    mmd += [f'  click {n["id"]} "../{n["doc"]}"' for n in NODES]
    (OUT / "execution-map.mmd").write_text("\n".join(mmd) + "\n", encoding="utf-8", newline="\n")
    palette = {
        "control": ("#edf4ff", "#b5cbea", "#285a94", "EXECUTION CONTRACT"),
        "candidate": ("#fff5e9", "#e4c295", "#9a5614", "UNTRUSTED OUTPUT"),
        "acceptance": ("#eaf8f1", "#a6d4be", "#087451", "ACCEPTANCE CONTRACT"),
        "premise": ("#fffae8", "#dfcb86", "#8a651c", "DECLARED LOGICAL BOUNDARY"),
        "infra": ("#f2f1fb", "#c4bfdf", "#65568e", "SUPPORTING AUTHORITY"),
    }
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1370" viewBox="0 0 1500 1370" role="img" aria-labelledby="title desc">',
        '<title id="title">Berry-Esseen execution architecture: one CLI, complete proof acceptance</title>',
        '<desc id="desc">Specified architecture, not a running proof. Planning and parallel candidate production feed independent verification and complete coverage. Analytic assumptions and the Lean trust bridge remain explicit. Immutable storage, a transactional ledger and an independent shutdown mechanism support execution.</desc>',
        '<style>text{font-family:"Segoe UI",Arial,sans-serif;fill:#172b44}.eyebrow{font-size:10px;font-weight:700;letter-spacing:1px}.title{font-size:21px;font-weight:650}.body{font-size:15px}.edge{fill:none;stroke:#7b91a7;stroke-width:2;marker-end:url(#arrow)}.support{fill:none;stroke:#adadc4;stroke-width:1.6;stroke-dasharray:5 5}</style>',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9Z" fill="#7b91a7"/></marker></defs>',
        '<rect width="1500" height="1370" rx="24" fill="#f5f7fb"/>',
        '<rect x="28" y="28" width="1444" height="190" rx="20" fill="#10243a"/>',
        '<text x="56" y="65" style="fill:#9bc7dd;font-size:12px;letter-spacing:2px">BERRY-ESSEEN / EXECUTION ARCHITECTURE v1</text>',
        '<text x="56" y="110" style="fill:white;font-size:33px;font-weight:650">One command. Parallel compute. Complete acceptance.</text>',
        '<text x="56" y="148" style="fill:#cfdae5;font-size:17px">Specify the interfaces first, implement vertical slices, then scale on Google Cloud.</text>',
        '<text x="56" y="185" style="fill:#b9d7dc;font-size:15px">PLN75 startup + PLN550 main / 12 hours · cache and resume · architecture specified, production runner pending</text>',
        '<text x="52" y="263" class="eyebrow">01 / FREEZE AND SCHEDULE</text>',
        '<text x="52" y="491" class="eyebrow">02 / PRODUCE, CHECK AND COVER</text>',
        '<text x="52" y="719" class="eyebrow">03 / EXPLICIT PREMISES AND FINAL CONCLUSION</text>',
        '<rect x="28" y="968" width="1444" height="266" rx="20" fill="#eaeaf4"/>',
        '<text x="52" y="1008" class="eyebrow">CROSS-CUTTING SERVICES / SUPPORT EXECUTION, DO NOT PROVE MATHEMATICS</text>',
    ]
    # Route arrows through the row gutters. Dashed service links are represented
    # by the service band + captions below to keep the visible proof path clear.
    paths = [
        "M472 360H530", "M956 360H1014",
        "M1230 428V452H34V588H46",
        "M472 588H530", "M956 588H1014",
        "M472 816H530", "M1230 656V742", "M956 816H1014",
    ]
    svg += [f'<path class="edge" d="{p}"/>' for p in paths]
    for n in NODES:
        fill, border, ink, tag = palette[n["kind"]]
        x, y = n["x"], n["y"]
        svg += [
            f'<a href="../{escape(n["doc"])}"><g id="{n["id"]}">',
            f'<rect x="{x}" y="{y}" width="420" height="136" rx="14" fill="{fill}" stroke="{border}"/>',
            f'<text x="{x+20}" y="{y+26}" class="eyebrow" style="fill:{ink}">{escape(tag)}</text>',
            f'<text x="{x+20}" y="{y+58}" class="title">{escape(n["label"])}</text>',
        ]
        for i, line in enumerate(n["lines"]):
            svg.append(f'<text x="{x+20}" y="{y+86+i*24}" class="body">{escape(line)}</text>')
        svg.append('</g></a>')
    svg += [
        '<text x="52" y="1210" style="font-size:14px;fill:#615b7d">These services bind every dispatch, checkpoint, publication and resume. Resource shutdown is reported independently.</text>',
        '<text x="52" y="1284" style="font-size:17px;font-weight:650">PASS requires the whole requested conclusion under the declared trust profile.</text>',
        '<text x="52" y="1317" style="font-size:15px">A candidate, historical PASS, cache hit, successful VM or green conditional Lean build cannot replace missing evidence.</text>',
        '</svg>',
    ]
    (OUT / "execution-map.svg").write_text("\n".join(svg) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
