"""Render the five contract views, linked to checked Lean declarations.

The cards are grouped by interface responsibility, not presented as a claim
that the five columns are sequential hypotheses of one analytic theorem.
"""
from __future__ import annotations

import json
from html import escape

from render_proof_map import ROOT, OUT, load_checked_report, source_anchor

# title, subtitle, cards(title, lines, source, declaration, status)
GROUPS = [
    ("01  STATE", "What every quantity means", [
        ("Law + contact", ["Actual P; actual n; method floor", "Raw H and normalized y differ"],
         "BEMap/Domain.lean", "ContactAt", "model"),
        ("Physical state", ["Contact majorant; actual gaps", "D, matching defect and eta differ"],
         "BEMap/TypedPipeline.lean", "PhysicalState", "model"),
        ("Resource state", ["Asymmetric support; signed moments", "Marginal cap and joint Lambda differ"],
         "BEMap/TypedPipeline.lean", "ResourceState", "model"),
        ("Count-ready state", ["Conditional residual laws", "a0 differs from total inward dY"],
         "BEMap/TypedPipeline.lean", "CountReadyState", "model"),
    ]),
    ("02  TRANSITIONS", "Exact inputs, gates and outputs", [
        ("One finite schedule", ["Same contact at every refinement", "No unproved fixed-point step"],
         "BEMap/TypedPipeline.lean", "ResourceSchedule", "checked"),
        ("Coherent LOW / HIGH", ["Exact Fourier split and integrals", "Complete HIGH; all window terms"],
         "BEMap/HighFamilies.lean", "Window50Theorem", "analytic"),
        ("Separate Prawitz", ["Four terms; law-level score bound", "Not the physical hinge-error budget"],
         "BEMap/Prawitz.lean", "PrawitzScoreEvidence", "analytic"),
        ("Same law: 25 to 24", ["Full new roots / phases + tails", "No contact at 24 is manufactured"],
         "BEMap/TypedPipeline.lean", "ABGeneralCountPort.window_bound", "checked"),
    ]),
    ("03  COVERAGE", "Every case and endpoint", [
        ("n5 complete regions", ["13 low + 6 Fourier + rho tail", "Distinct methods and radius inputs"],
         "BEMap/Covers.lean", "n5_cover", "checked"),
        ("n25 closed cover", ["6 rho + 7 beta + 6 beta + tail", "Signed envelopes; closed seams"],
         "BEMap/Cover25.lean", "n25_cover", "checked"),
        ("Actual-index floor31", ["Eight bands; weighted nD transfer", "Actual n controls phase and mass"],
         "BEMap/Covers.lean", "floor31_cover", "checked"),
        ("Every original root", ["Both children of every tree split", "No root or closed seam disappears"],
         "BEMap/Certificates.lean", "CountTree.cover", "checked"),
    ]),
    ("04  CERTIFICATES", "What acceptance proves", [
        ("Frozen rational task", ["No unknown law in runtime data", "Law appears in semantic quantifiers"],
         "BEMap/Certificates.lean", "CountTaskContext", "model"),
        ("Quantitative meaning", ["Arbitrary same-law count problem", "Returned cap may exceed early target"],
         "BEMap/GeneralCount.lean", "GeneralCountRealization", "model"),
        ("Exact local inference", ["Rational Farkas multiplier checker", "Necessary-row binding is mandatory"],
         "BEMap/CountRules.lean", "FarkasCandidate.check_sound", "checked"),
        ("Reference registry", ["One enclosing scope; earlier licenses", "Admitted data versus selected uses"],
         "BEMap/MixedRegistry.lean", "FrozenReference", "model"),
    ]),
    ("05  ASSEMBLY", "Actual conditional composition", [
        ("Small-index providers", ["n2 tensor versus n3 null basis", "Exact row meaning + large-rho case"],
         "BEMap/Assembly.lean", "SmallPolynomialProvider", "analytic"),
        ("Weak ROOT4 output", ["Strong n3 input; chosen owner", "score <= 0.4097 is sufficient"],
         "BEMap/Root4.lean", "Root4Provider.upper", "checked"),
        ("Build finite contracts", ["All literal indices 1 through 48", "Typed methods supply every field"],
         "BEMap/Assembly.lean", "EndToEndProviders.finite", "checked"),
        ("Independent tail49+", ["Three backward losses at base49", "No all-1..48 theorem as an input"],
         "BEMap/TailAssembly.lean", "TailMethodProviders.contracts", "checked"),
    ]),
]


def main() -> None:
    report = load_checked_report()
    cards = []
    palette = {
        "model": ("#edf4ff", "#b8d0f5", "#285cb0", "CONCRETE SEMANTICS"),
        "checked": ("#effbf5", "#a7d9c3", "#087451", "CHECKED STRUCTURE / ADAPTER"),
        "analytic": ("#fffbf0", "#e6cd96", "#9d5d17", "EXPLICIT ANALYTIC INPUT"),
    }
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="1320" viewBox="0 0 1480 1320" role="img" aria-labelledby="title desc">',
        '<title id="title">Berry–Esseen: five detailed mathematical interfaces</title>',
        '<desc id="desc">Five complementary views: concrete states, exact transitions, complete coverage, certificate semantics and checked conditional assembly. Analytic correctness is an explicit premise; full analysis proofs and production numerical evidence are separate.</desc>',
        '<style>text{font-family:"Segoe UI",Arial,sans-serif;fill:#172b44}.label{font-size:10px;font-weight:700;letter-spacing:.75px}.mono{font-family:Consolas,monospace}</style>',
        '<rect width="1480" height="1320" rx="24" fill="#f5f7fb"/>',
        '<rect x="28" y="28" width="1424" height="175" rx="20" fill="#10243a"/>',
        '<text x="56" y="68" style="fill:#9bc7dd;font-size:12px;letter-spacing:2px">BERRY–ESSEEN / MATHEMATICAL INTERFACE v0.2</text>',
        '<text x="56" y="111" style="fill:white;font-size:34px;font-weight:650">Precise mathematics before implementation</text>',
        '<text x="56" y="145" style="fill:#cfdae5;font-size:17px">The law, units, gates, coverage and meaning of acceptance are already part of the contract.</text>',
        f'<text x="56" y="178" style="fill:#b9d7dc;font-size:14px">{len(report["modules"])} checked Lean sources · exact analytic assumptions remain visible · production evidence remains to supply</text>',
    ]
    for group_index, (title, subtitle, entries) in enumerate(GROUPS):
        x = 28 + group_index * 286
        svg += [
            f'<rect x="{x}" y="235" width="268" height="773" rx="16" fill="#eaf0f7"/>',
            f'<text x="{x+14}" y="265" style="fill:#355571;font-size:14px;font-weight:700">{escape(title)}</text>',
            f'<text x="{x+14}" y="287" style="fill:#62798d;font-size:12px">{escape(subtitle)}</text>',
        ]
        for i, (name, lines, source, declaration, status) in enumerate(entries):
            y = 311 + i * 169
            anchor = source_anchor(source, declaration)
            cards.append(dict(group=group_index+1, title=name, source=source,
                              declaration=declaration, line=anchor,
                              status=status, explanation=lines))
            fill, stroke, color, label = palette[status]
            svg += [
                f'<g><rect x="{x+10}" y="{y}" width="248" height="150" rx="12" fill="{fill}" stroke="{stroke}"/>',
                f'<rect x="{x+10}" y="{y+18}" width="3" height="114" rx="1" fill="{color}"/>',
                f'<text x="{x+23}" y="{y+24}" class="label" style="fill:{color};font-size:8.4px">{label}</text>',
                f'<text x="{x+23}" y="{y+52}" style="font-size:18px;font-weight:650">{escape(name)}</text>',
            ]
            for j, line in enumerate(lines):
                svg.append(f'<text x="{x+23}" y="{y+78+j*20}" style="font-size:11.7px;fill:#405870">{escape(line)}</text>')
            short_source = source.split("/")[-1]
            svg.append(f'<text x="{x+23}" y="{y+130}" class="mono" style="font-size:10.3px;fill:#65798f">{escape(short_source)}:{anchor}</text></g>')
    final_source = "BEMap/Assembly.lean"
    finals = [{"source": final_source, "declaration": name,
               "line": source_anchor(final_source, name)} for name in
              ("all_indices_from_typed_providers", "sharp_from_typed_providers")]
    svg += [
        '<rect x="28" y="1044" width="1424" height="140" rx="16" fill="#effbf5" stroke="#a7d9c3"/>',
        '<text x="56" y="1075" class="label" style="fill:#087451">FINAL CHECKED CONDITIONAL STATEMENTS</text>',
        '<text x="56" y="1110" class="mono" style="font-size:20px;font-weight:600">all_indices_from_typed_providers  →  every n ≥ 1: C_n ≤ C_E</text>',
        '<text x="56" y="1146" class="mono" style="font-size:20px;font-weight:600">sharp_from_typed_providers        →  globalConstant = C_E</text>',
        '<text x="56" y="1170" style="font-size:12px;fill:#4b7665">The second statement additionally consumes the separate lower approximation.</text>',
        '<text x="42" y="1221" style="font-size:13px;fill:#536b82">Five complementary contract views, not five sequential hypotheses of one theorem. Exact signatures are authoritative.</text>',
        '<text x="42" y="1250" style="font-size:13px;fill:#536b82">Blue = concrete meaning · Green = checked structure / implication · Amber = precisely stated analytic premise</text>',
        '<text x="42" y="1279" style="font-size:13px;fill:#536b82">Specification: docs/contracts/README.md · Source audit: docs/contracts/AUDIT.md · Verification: check-All.json</text>',
        '</svg>',
    ]
    (OUT / "interface-map.svg").write_text("\n".join(svg)+"\n", encoding="utf-8")
    (ROOT / "docs" / "interface-map.json").write_text(json.dumps(dict(
        interpretation="Five curated contract views, not a kernel proof-term graph or a serial pipeline",
        verification="check-All.json", cards=cards, final_statements=finals), indent=2)+"\n", encoding="utf-8")
    print(f"Validated {len(cards)+len(finals)} source anchors; wrote assets/interface-map.svg and docs/interface-map.json")


if __name__ == "__main__":
    main()
