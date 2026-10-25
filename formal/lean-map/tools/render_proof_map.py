"""Render a source-linked mathematical map, using only the Python standard library.

This is a curated view of Lean theorem interfaces, not an extraction of kernel
proof-term dependencies. Lean checks the implications; this script checks source
anchors, the recorded source hashes, and the diagram's own edges.
"""
from __future__ import annotations

import hashlib
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

# id, status, position, title, explanation, source, declaration
NODES = [
    ("MODEL", "model", (48, 324, 1144, 106), "Concrete probability model",
     ["Probability laws on R · convolution sums · closed CDF · rho >= 1 · well-defined suprema"],
     "BEMap/Foundations/OptimalConstant.lean", "normalizedScore_le_optimalConstant"),
    ("SMALL", "open", (60, 542, 330, 128), "Small + ROOT4 + n5",
     ["Exact polynomial and physical methods", "Strong n3 -> weak ROOT4 -> n5 cover"],
     "BEMap/Assembly.lean", "EndToEndProviders"),
    ("ORDINARY", "open", (60, 720, 330, 128), "Literal finite exclusions",
     ["Every actual n = 6,...,48 except 25", "Typed state + complete count forests"],
     "BEMap/Assembly.lean", "FixedIndexMethodProvider"),
    ("FINITE", "checked", (60, 1032, 330, 112), "finite_composition",
     ["Strong induction covers all n = 1,...,48."],
     "BEMap/Finite.lean", "finite_composition"),
    ("INPUT25", "open", (454, 542, 330, 146), "Exact n25 premises",
     ["Scoped ordinary / mixed methods", "Exact signed-beta envelopes", "All 20 same-witness exclusions"],
     "BEMap/Assembly.lean", "TwentyFiveProvider"),
    ("COVER25", "checked", (454, 738, 330, 112), "n25_cover",
     ["6 rho + 7 beta + 6 beta + 1 tail", "Closed rational cuts; seams included."],
     "BEMap/Cover25.lean", "n25_cover"),
    ("UPPER25", "checked", (454, 910, 330, 112), "TwentyFiveProvider.upper",
     ["All scoped regional methods -> C25 <= C_E"],
     "BEMap/Assembly.lean", "TwentyFiveProvider.upper"),
    ("LICENSE25", "checked", (454, 1066, 330, 110), "Additional checked bridge",
     ["Sharp24 OR auxiliary24 -> q25 <= 5/16"],
     "BEMap/Finite.lean", "n25_allowance"),
    ("TAILINPUT", "open", (848, 542, 330, 146), "Independent tail premises",
     ["83 panels: positive / zero noise", "Five auxiliary resource-barrier families", "Exact smoothing + index brackets"],
     "BEMap/TailAssembly.lean", "TailMethodProviders"),
    ("BASE49", "checked", (848, 738, 330, 112), "tail_base49",
     ["Three backward losses at 49, 48, 47", "Contradiction with the strong 46 cap."],
     "BEMap/Tail.lean", "tail_base49"),
    ("SMOOTH", "checked", (848, 890, 330, 100), "smoothing_first_failure",
     ["Source smoothing -> n a_n < 0.29"],
     "BEMap/TailAssembly.lean", "smoothing_first_failure"),
    ("TAIL", "checked", (848, 1032, 330, 112), "tail_composition",
     ["First-failure induction covers n >= 49."],
     "BEMap/Tail.lean", "tail_composition"),
    ("UPPER", "checked", (60, 1270, 770, 116), "Typed all-index bound",
     ["Every positive integer: C_n <= C_E", "Concrete iid inequality follows for every standardized law."],
     "BEMap/Assembly.lean", "all_indices_from_typed_providers"),
    ("LOWER", "open", (880, 1270, 320, 116), "Separate lower bound",
     ["Bernoulli lattice approximation", "No fixed-n attainment is assumed."],
     "BEMap/Global.lean", "LowerApproximation"),
    ("SHARP", "checked", (280, 1470, 680, 126), "Typed sharpness theorem",
     ["C* = C_E = (3 + sqrt(10)) / (6 sqrt(2 pi))", "Checked conclusion, conditional on all displayed contracts."],
     "BEMap/Assembly.lean", "sharp_from_typed_providers"),
]

# Grouped mathematical prerequisite edges; membership in a record is bundled.
EDGES = [
    ("SMALL", "FINITE", "M225 670 V694 H49 V1008 H150 V1032"),
    ("ORDINARY", "FINITE", "M225 848 V1032"),
    ("INPUT25", "COVER25", "M619 688 V738"),
    ("INPUT25", "UPPER25", "M784 616 H815 V966 H784"),
    ("COVER25", "UPPER25", "M619 850 V910"),
    ("UPPER25", "FINITE", "M454 966 H416 V1088 H390"),
    ("TAILINPUT", "BASE49", "M1013 688 V738"),
    ("TAILINPUT", "TAIL", "M1178 616 H1190 V1088 H1178"),
    ("BASE49", "TAIL", "M880 850 H838 V1010 H930 V1032"),
    ("SMOOTH", "TAIL", "M1013 990 V1032"),
    ("FINITE", "UPPER", "M225 1144 V1218 H350 V1270"),
    ("TAIL", "UPPER", "M1013 1144 V1218 H730 V1270"),
    ("UPPER", "SHARP", "M445 1386 V1426 H500 V1470"),
    ("LOWER", "SHARP", "M1040 1386 V1426 H780 V1470"),
]


def source_anchor(path: str, name: str) -> int:
    text = (ROOT / path).read_text(encoding="utf-8")
    pattern = r"\b(?:theorem|def|structure|abbrev)\s+" + re.escape(name) + r"\b"
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"Missing Lean declaration: {path}: {name}")
    return text[:match.start()].count("\n") + 1


def load_checked_report() -> dict:
    report = json.loads((ROOT / "check-All.json").read_text(encoding="utf-8-sig"))
    assert report["passed"], "Recorded Lean check did not pass"
    actual = {str(p.relative_to(ROOT)).replace("\\", "/")[:-5]
              for p in list((ROOT / "BEMap").rglob("*.lean")) + list(ROOT.glob("*.lean"))}
    recorded = {row["module"] for row in report["modules"]}
    assert actual == recorded, f"Unchecked or removed sources: {actual ^ recorded}"
    for row in report["modules"]:
        path = ROOT / (row["module"] + ".lean")
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["source_sha256"], path
        assert row["exit_code"] == 0
    return report


def main() -> None:
    report = load_checked_report()
    nodes = []
    for name, status, rect, title, lines, source, declaration in NODES:
        nodes.append(dict(id=name, status=status, rect=rect, title=title,
                          explanation=lines, source=source, declaration=declaration,
                          line=source_anchor(source, declaration)))
    ids = {n["id"] for n in nodes}
    assert len(ids) == len(nodes)
    for a, b, _ in EDGES:
        assert a in ids and b in ids
    # Acyclicity of the displayed grouped graph.
    pending = set(ids)
    while pending:
        ready = {n for n in pending if not any(b == n and a in pending for a, b, _ in EDGES)}
        assert ready, "Cycle in diagram"
        pending -= ready
    manifest = dict(
        title="Berry--Esseen: detailed mathematical contracts and checked conditional composition",
        interpretation="Curated grouped view of theorem interfaces, not a kernel-exported proof-term graph",
        status_legend=dict(checked="Proved conditional implication; its premises may remain open",
                           open="Explicit accepted analytic premise or numerical evidence still to supply",
                           model="Concrete definitions and elementary proved foundation"),
        verification="check-All.json", nodes=nodes,
        edges=[dict(source=a, target=b) for a, b, _ in EDGES])
    (ROOT / "docs" / "proof-map.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="1784" viewBox="0 0 1240 1784" role="img" aria-labelledby="title desc">',
        '<title id="title">Berry--Esseen: Lean proof map</title>',
        '<desc id="desc">Green boxes are checked conditional implications. Amber boxes are explicit analytic and numerical inputs. Typed finite methods and the independent tail combine into the upper bound. A separate lower approximation gives sharpness.</desc>',
        '<defs><filter id="shadow" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#10243a" flood-opacity=".055"/></filter>',
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M1 1 L7 4 L1 7" fill="none" stroke="#8091a8" stroke-width="1.4"/></marker></defs>',
        '<style>text{font-family:"Segoe UI",Arial,sans-serif;fill:#172b44} .mono{font-family:Consolas,"DejaVu Sans Mono",monospace} .label{font-size:11px;font-weight:700;letter-spacing:1.2px} .edge{fill:none;stroke:#8091a8;stroke-width:2;stroke-linejoin:round;marker-end:url(#arrow)}</style>',
        '<rect width="1240" height="1784" rx="24" fill="#f5f7fb"/>',
        '<rect x="32" y="32" width="1176" height="218" rx="22" fill="#10243a"/>',
        '<text x="62" y="76" style="fill:#9bc7dd;font-size:12px;letter-spacing:2.2px;font-weight:600">MATHEMATICAL CONTRACTS / LEAN 4.32.0</text>',
        '<text x="62" y="124" style="fill:white;font-size:37px;font-weight:650">Berry–Esseen · the proof map</text>',
        '<text x="62" y="158" style="fill:#cfdae5;font-size:18px">Detailed mathematical interfaces. Every analytic premise stays visible.</text>',
    ]
    core = sum(r.get("last_compile_seconds", r["seconds"]) for r in report["modules"] if r["module"] in
               {"BEMap/Finite", "BEMap/Cover25", "BEMap/Tail"})
    full = round(report["total_seconds"])
    mode = "incremental" if report.get("reused_modules", 0) else "full check"
    for x, w, label in [(62, 235, f'{len(report["modules"])} modules · local check PASS'),
                         (311, 210, f'{round(core)} s · core compile'),
                         (535, 270, f'{full // 60} min {full % 60:02d} s · {mode}')]:
        svg += [f'<rect x="{x}" y="184" width="{w}" height="34" rx="17" fill="#203b50"/>',
                f'<text x="{x+14}" y="206" style="fill:#dbebe9;font-size:13px;font-weight:600">{escape(label)}</text>']
    legend = [(62, "#0b805d", "Checked implication"), (382, "#af6414", "Analytic / numerical input"), (780, "#3063c4", "Concrete law model")]
    for x, color, text in legend:
        svg += [f'<circle cx="{x}" cy="286" r="6" fill="{color}"/>',
                f'<text x="{x+15}" y="291" style="font-size:16px;font-weight:600">{text}</text>']
    for x, title, sub in [(40, "01  FINITE RANGE", "All literal indices 1 through 48"),
                           (434, "02  FOCUS: n = 25", "The special regional composition"),
                           (828, "03  INDEPENDENT TAIL", "No all-1–48 premise is needed")]:
        svg += [f'<rect x="{x}" y="474" width="370" height="722" rx="18" fill="#eaf0f7"/>',
                f'<text x="{x+20}" y="506" class="label" style="fill:#47627c">{escape(title)}</text>',
                f'<text x="{x+20}" y="527" style="fill:#61758d;font-size:12px">{escape(sub)}</text>']
    for a, b, path in EDGES:
        dashed = ' stroke-dasharray="5 5"' if next(n for n in nodes if n["id"] == a)["status"] == "open" else ""
        svg.append(f'<path class="edge" d="{path}"{dashed}/>')
    palette = dict(checked=("#f0fbf6", "#a7d9c3", "#087451", "CHECKED IMPLICATION"),
                   open=("#fffbf0", "#e6cd96", "#9d5d17", "ANALYTIC / NUMERICAL INPUT"),
                   model=("#edf4ff", "#b8d0f5", "#285cb0", "CONCRETE MODEL · CHECKED FOUNDATION"))
    for node in nodes:
        x, y, w, h = node["rect"]
        fill, stroke, color, status = palette[node["status"]]
        svg += [f'<g id="{node["id"]}">',
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="{fill}" stroke="{stroke}" filter="url(#shadow)"/>',
                f'<rect x="{x}" y="{y+18}" width="4" height="{h-36}" rx="2" fill="{color}"/>',
                f'<text x="{x+18}" y="{y+25}" class="label" style="fill:{color};font-size:10px">{status}</text>',
                f'<text x="{x+18}" y="{y+52}" style="font-size:21px;font-weight:650">{escape(node["title"])}</text>']
        for i, text in enumerate(node["explanation"]):
            svg.append(f'<text x="{x+18}" y="{y+76+19*i}" style="font-size:13.8px;fill:#405870">{escape(text)}</text>')
        if node["id"] == "LICENSE25":
            svg.append(f'<text x="{x+18}" y="{y+95}" class="mono" style="font-size:11px;fill:#4b7665">n25_allowance · same_law_n25_allowance</text>')
        svg.append('</g>')
    svg += [
        '<text x="620" y="1239" text-anchor="middle" class="label" style="fill:#59738f">FINITE + TAIL = EVERY POSITIVE INDEX</text>',
        '<rect x="48" y="1652" width="1144" height="94" rx="14" fill="white" stroke="#dce4ef"/>',
        '<text x="70" y="1682" class="label" style="fill:#446079">HOW TO READ THE GREEN BOXES</text>',
        '<text x="70" y="1707" style="font-size:15px">Lean checks the assembly. Exact analytic theorems are premises; numerical evidence remains to supply.</text>',
        '<text x="70" y="1730" style="font-size:13px;fill:#65798f">Source-linked declarations: docs/proof-map.md · Exact check and source hashes: check-All.json</text>',
        '</svg>']
    (OUT / "proof-map.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")
    mmd = ["flowchart TD"]
    for n in nodes:
        mmd.append(f'  {n["id"]}["{n["title"]}"]:::{n["status"]}')
    mmd += [f'  {a} --> {b}' for a, b, _ in EDGES]
    mmd += ["  classDef checked fill:#effbf5,stroke:#0b805d,color:#173e30",
            "  classDef open fill:#fff8e7,stroke:#b77721,color:#694314",
            "  classDef model fill:#edf4ff,stroke:#3063c4,color:#25456f"]
    (OUT / "proof-map.mmd").write_text("\n".join(mmd) + "\n", encoding="utf-8")
    print(f'Validated {len(nodes)} declaration anchors, {len(EDGES)} acyclic grouped edges, and all {len(report["modules"])} checked source hashes.')
    print("Wrote assets/proof-map.svg, assets/proof-map.mmd and docs/proof-map.json")


if __name__ == "__main__":
    main()
