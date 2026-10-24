"""Build the selected delivery specification; never import research programs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proof"


def read(name):
    return json.loads((PROOF / name).read_text(encoding="utf-8"))


def pin(name):
    data = (PROOF / name).read_bytes()
    return {"path": "proof/" + name, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def write(name, data):
    (PROOF / name).write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def n25_plan():
    cat = read("n25_retained_b5_upper_catalog.json")
    cover = read("code_n25_global_union_source_map.json")["physical_cover"]
    sections = [
        ("b34", "Lower B3/B4 supplemental and final interfaces",
         "B3 p30 S1 resource; current p31/p32 V14 contact and rounding; resolve p34 selector; all100 p outcomes for each branch and all remaining exact count interfaces.",
         "Reuse09/10,01--07,24,29/30. Two declared regional records/companion selectors are absent under their declared names; reconstruct an honest current semantic union from actual components."),
        ("b5_missing", "Eleven unavailable lower B5 ordinary capsules",
         "Seven V14 p26--32 and four V12 p33 closed quarters; recover exact sources/candidates or construct and fully accept a separately justified matching design.",
         "Original selected directories are unavailable, but complete eight-panel V12 bases and V14 additions are supplied. All four p33 contracts/checkers are exactly reconstructed; seven honest new V14 source epochs and fresh complete forests/acceptance are required."),
        ("b5_mixed", "Both lower B5 mixed p24/p25 routes",
         "Full original mixed acceptors, ordinary/scalar/derived/theorem leaves, all theorem IDs and same-law acquisition registries, plus complete37-panel B5 union.",
         "Both mixed forests/acceptors located; all93 native files, both original checkers and full mathematical rows are recoverable. New honest parent/header/registry metadata epochs and complete mixed replay are required; ordinary COUNT is not a substitute."),
        ("upper_counts", "Ten supplied additional ordinary forests",
         "High beta2 p17--23 and middle positive B3 p21--23; each full original count protocol and controls under exact selected contract.",
         "Supplied inputs, wrapper/source admission and fresh executions still required."),
        ("high_beta2", "High beta2 complete acquisitions",
         "One canonical INITIAL/global resource pair, all100 p dispositions and seven selected locals17--23: exact17/18/19, exact20_cached_v2, exact21_cached_v1, exact22_cached_v1, exact23_16 (16 cycles).",
         "Current constructor/receipt epochs and each distinct local manifest must be sealed."),
        ("middle_b3", "Middle positive B3 complete acquisitions",
         "One canonical INITIAL/global resource pair and eight selected locals20--27, including all exclusion outcomes.",
         "Current epochs and count interfaces still required; count21--23 assigned above."),
        ("middle_b012", "All three middle positive B0/B1/B2 families",
         "B0 full at-most8-cover INITIAL; B1 INITIAL plus all100 resources/12 feedback cycles; B2 INITIAL/resource/all100 local dispositions with permitted23--25 local covers.",
         "Source/child-process closure and truthful current capture admission unimplemented."),
        ("older_upper", "Five inherited upper/middle acquisition families",
         "high-negative, middle-negative, high-quarter2, high-beta0 and high-beta1 mixed. Preserve every full cover, selected resource/local loop and original control.",
         "Exact source entries located; full transitive portable closures/action admission not yet sealed. Shared kernels do not merge distinct profiles."),
        ("semantic_union", "All current n25 interfaces and physical union",
         "All reused counts/acquisitions, same-law auxiliary24/contact license, outward rounding, both signs, mixed theorem/scalar premises, all20 physical regions, all closed seams and universal rho tail.",
         "Requires actual complete stage evidence and code-to-lemma/analytic premises. Old final record has zero new native calls and cannot close this section.")]
    pins = ["n25_regional_selection.json", "n25_acquisition_queue.md", "n25_completion_scope.md",
            "n25_retained_b012_catalog.json", "n25_retained_b34_catalog.json", "n25_retained_b5_upper_catalog.json",
            "code_n25_global_union_source_map.json", "code_n25_high_beta2_interface_source_map.json",
            "code_n25_high_middle_profile_source_map.json", "code_n25_upper_initial_acquisition_source_map.json",
            "code_n25_middle_positive_acquisition_source_map.json", "code_n25_high_local_feedback_source_map.json",
            "n25_b5_reconstruction_feasibility.json", "n25_b5_reconstruction_feasibility.md",
            "n25_mixed_parent_reconstruction_feasibility.json", "n25_mixed_parent_reconstruction_feasibility.md"]
    thin = ["branch", "target_id", "archive_key", "capsule_member_prefix", "index", "selection_status",
            "capsule_member_supplied", "contract_sha256", "forest_sha256", "checker_sha256"]
    remaining = [{k: r.get(k) for k in thin} for r in cat["count_jobs"]
                 if not r.get("capsule_member_supplied") or r["branch"] == "upper-retained-graph"]
    source_assignments = []
    for r in cat["noncount_source_entrypoints"]:
        member = r["member"]
        if "/high25_beta2/" in member:
            section = "high_beta2"
        elif "/high25_beta3" in member:
            section = "reuse49"
        elif "/new_middle/" in member:
            section = "reuse47_48"
        elif "/new_root/" in member:
            section = "reuse39"
        elif "/middle_positive_b3" in member:
            section = "upper_counts" if "_counts/" in member else "middle_b3"
        elif "/middle_positive_b0" in member or "/middle_positive_b1" in member or "/middle_positive_b2" in member:
            section = "middle_b012"
        elif "/toward25/" in member:
            section = "older_upper"
        else:
            raise ValueError("Unassigned n25 original entrypoint: " + member)
        source_assignments.append({**r, "assigned_section": section,
                                   "role": "source_variant_inventory_not_distinct_call_census"})
    return {"schema": "N25_REMAINING_DELIVERY_SPEC_V1", "delivery_id": "66",
            "delivery_file": "66_n25_remaining_acquisition_and_join.ipynb",
            "sections": [{"id": a, "title": b, "full_scope": c, "blocker": d} for a,b,c,d in sections],
            "anchors": [pin(n) for n in pins], "physical_cover": cover,
            "physical_piece_count": 20, "additional_ordinary_count_jobs": remaining,
            "missing_ordinary_capsules": 11, "supplied_additional_ordinary_forests": 10,
            "mixed_selected_components": cat["mixed_selected_components"],
            "noncount_source_entrypoint_assignments": source_assignments,
            "reused_notebooks": ["01--07", "09", "10", "14--24", "26--34", "36--39", "47--49"],
            "reuse_requires_exact_complete_evidence": True,
            "runtime_source_closure_complete": False, "numerical_action_census_sealed": False,
            "runnable": False, "all_index_conclusion_verified": False,
            "arithmetic_executed_for_this_plan": False,
            "warning": "One fixed delivery container does not solve missing sources or prove that a substitute route succeeds. Its blocked cases remain mandatory."}


def main():
    n25 = n25_plan()
    write("remaining_n25_execution_partition.json", n25)
    # Dependency order is logical acquisition, not the allowed order of conditional numerical runs.
    specifications = [
        ("56I", "n10_14_finite_join", "numerical", [10,14], [],
         ["50", "56A--H", "56K"], "Seven retained original review/control outputs (including bounded mathematical controls), all1000 p dispositions,202 acquired resource/contract implications and20 restricted subpanel edges for217 forests; support/HIGH/Fourier applicability and actual10--14 induction.",
         "Exact bounded control execution, current receipt/contract bridges and finite-only replacement of old eventual15/tail join. Global n9 sharp bound is not the selected n10 base;56A/B actual same-law ceilings are required."),
        ("57F", "n15_19_initial_resource_B0", "numerical", [], [], ["57E"],
         "Five B0 cases,20 unchanged original INITIAL construct/replay/resource construct/accept calls, full100 p rows each.", "Implemented; reviewed fixtures passed; upstream mathematical assumptions remain conditional."),
        ("57G", "n15_19_initial_resource_BN", "numerical", [], [], ["57E"],
         "Five BN cases,20 unchanged original INITIAL construct/replay/resource construct/accept calls, full100 p rows each.", "Implemented; reviewed fixtures passed; upstream mathematical assumptions remain conditional."),
        ("57H", "n15_19_finite_join", "numerical", [15,19], ["56I","57F","57G"],
         ["51", "57A--E"], "Retained finite/contact/cancellation HIGH, resource/count range and actual15 mutation/control programs; all1000 p outcomes,147 resource/count edges, actual15 base then16--19 induction; no incoming eventual20.", "Bounded mathematical controls, current evidence bridges, predecessor acquisition and full finite-only join unimplemented."),
        ("58H", "n20_24_remaining_acquisition_and_join", "numerical", [20,24], ["57H"],
         ["52", "58A--G"], "All six grouped components: coarse/narrow/feedback INITIAL, all resources, actual20 interfaces and eight21--24 band joins; three closed actual20 rho regions.", "Truthful current source/capture epochs; same-law support/owncap/contact order; final semantic joins."),
        ("59D", "n26_30_support_transfers_and_join", "numerical", [26,30], ["66"],
         ["53", "64", "59A--C", "36--39", "09", "10", "56K"], "Two complete actual26--30 support families,13 fixed scalar/control/adapter calls, all floor25 resource transfers and final80-count/445-Fourier/closed-cover join.", "Portable full source epochs and typed fresh parent bridges; no incoming tail31."),
        ("60", "n31_39_parents_and_join", "numerical", [31,39], ["59D"], ["54", "55"],
         "Eight complete floor31 families, actual32--34 support/transfer and joins,45 selected finite35--39 nonCOUNT parent/interface records. Full selected counts reused.", "Current capture/constructor admission; four old metadata omit cwd. Frozen40 binder outgoing63 only."),
        ("61", "n43_48_acquisition_and_join", "numerical", [43,48], [], ["12"],
         "Cutoff44:25 calls; cutoff43:6 scopes;2 current final joins. Full LOW78+74 signed rows and all retained inputs; finite43--48 only.", "Current source/capture epochs and relocated pure12 reader; no incoming all-index conclusion."),
        ("62", "n40_42_acquisition_and_join", "numerical", [40,42], [], ["12"],
         "Six grouped sections,48 top-level/59 physical calls including9 global40 child binders and2 SINGLE39 children; full retained/LOW/LEFT/MID/CENTRAL routes.", "Current constructor/capture epochs, complete nested source/output closure and finite40--42 projection. Original global40 all-tail call waits for61; defer that full join to63."),
        ("63", "all_index_evidence_and_proof_join", "collector", [], ["67","65","56I","57H","58H","66","59D","60","62","61"],
         ["08", "11", "12", "13", "14--24"], "Explicit finite1--48 plus uniform49+ implication and external Esseen lower bound; full tail evidence/least-failure/scalar/interfaces and all analytic/literature obligations.", "No theorem acceptance until every arithmetic, analytic, literature and code-to-lemma premise is acquired."),
        ("65", "n6_9_remaining_acquisition_and_join", "numerical", [6,9], ["67"], ["40--46", "35"],
         "Both bridge/radius Fourier transactions, full12-row HIGH,36 support targets/72 signed rays, all284 COUNT edges and finite6--9 induction. Explicit4-call auxiliary5 fallback if exact35 export unavailable.", "Current source/capture and parent bridges; conditional support/Fourier order must not become a mathematical cycle."),
        ("66", "n25_remaining_acquisition_and_join", "numerical", [25,25], ["58H"], n25["reused_notebooks"],
         "All nine n25 sections in separately pinned manifest:21 ordinary remaining forests (11 missing),2 mixed routes, supplementary/resources/upper families and all20 physical regions.", "Concrete source reconstruction basis is recorded for all11 ordinary cases and both mixed parents. Honest current source/registry epochs, fresh complete searches/replays and full action closures remain to implement."),
        ("67", "n5_full_evidence_and_proof_join", "numerical", [5,5], [], ["08", "11", "13", "35"],
         "First acquire all-law n2/n3 andC4 from08/11 plus precise analytic premises, keeping strongG3. Reuse35/13 core arithmetic except exact current complement context:14 finite algebra/source-control programs,2 full support constructor/replay pairs,2 full complement integrations/accept/fullreadback;12resource+12count regional joins and finalC5 composition.",
         "Full current captures and scalar/readback gates were not supplied by35 arithmetic-prefix acceptance. Preserve strong n3 G3<=59*sqrt(3)/250 through all-law C4, not merely sharpCE.")]
    units = []
    for id, suffix, kind, interval, dependencies, reuse, scope, blocker in specifications:
        units.append({"id": id, "file": f"{id}_{suffix}.ipynb", "kind": kind,
                      "finite_indices": list(range(interval[0], interval[1]+1)) if interval else [],
                      "depends_on": dependencies, "reuse": reuse, "scope": scope,
                      "implementation_gate": blocker,
                      "maximum_original_action_wall_seconds": 82800 if kind == "numerical" else None,
                      "completed_atomic_stage_cache_only": True,
                      "implemented": id in ["57F", "57G"], "mathematically_acquired": False,
                      "delivered": id in ["57F", "57G"],
                      "delivered_runtime_commit": "99d4a016bbfe7399639b49cf131ccbae2f103f0f" if id in ["57F", "57G"] else None,
                      "delivered_notebook_sha256": hashlib.sha256((ROOT/"colab"/f"{id}_{suffix}.ipynb").read_bytes()).hexdigest() if id in ["57F", "57G"] else None})
    anchors = ["obligations.json", "remaining_n25_execution_partition.json",
               "remaining57_59_delivery_partition.json", "remaining_58_69_execution_partition.json",
               "remaining31_39_delivery_partition.json", "finite4348_source_action_plan.json",
               "finite1014_core_source_plan.json", "n5_remaining_catalog.json", "tail49_completed_export_readback.json",
               "remaining56I_control_scope.json", "remaining56I_sufficiency_review.json", "remaining57H_control_scope.json", "remaining_n5_delivery_partition.json"]
    original = read("obligations.json")["nodes"]
    mapping = {}
    for r in original:
        id = r["id"]
        if r["kind"] in ["literature", "analytic_review"]:
            owner = "NONCOMPUTE:" + id
        elif id.startswith(("n2.", "n3.")):
            owner = "EXISTING:08" if id.endswith("native") else "67"
        elif id == "c4.native_root4": owner = "EXISTING:11"
        elif id.startswith("c4."): owner = "67"
        elif id == "c5.gapfree_native": owner = "EXISTING:13"
        elif id == "c5.complement_native": owner = "67"
        elif id.startswith("c5."): owner = "EXISTING:35" if id.endswith("native") else "67"
        elif id == "n5.all_law": owner = "67"
        elif id.startswith("n25.pending."):
            owner = "EXISTING:" + {"b4-q0":"02","b4-q1":"03","b4-q2":"04","b4-q3":"05","b3-p33":"01","b3-p31-v14-new":"06","b3-p32-v14-new":"07"}[id.removeprefix("n25.pending.")]
        elif id in ["n25.parents.b3", "n25.parents.b4"]: owner = "EXISTING:" + ("09" if id.endswith("b3") else "10")
        elif id == "n25.selected_interfaces": owner = "EXISTING:24"
        elif id == "n25.remaining_native_and_acquisitions": owner = "66"
        elif id.startswith("n") and id.endswith(".all_law"):
            n = int(id[1:].split(".")[0])
            owner = next(x["id"] for x in units if n in x["finite_indices"])
        elif id == "tail31.base31_34": owner = "60"
        elif id == "tail31.bridge35_48": owner = "63"
        elif id == "tail49.full_native_suite": owner = "EXISTING:12"
        elif id in ["tail49.all_law", "proof.global"]: owner = "63"
        elif id.startswith("aux") and id.endswith(".arithmetic"):
            owner = "EXISTING:" + {"aux21.arithmetic":"14","aux22.arithmetic":"15","aux23.arithmetic":"16"}[id]
        elif id.startswith("aux") and id.endswith(".acquired"): owner = "66"
        elif id.startswith("stronger24.b") and id.endswith(".arithmetic"): owner = "EXISTING:" + str(17 + int(id.split(".")[1][1:]))
        elif id == "stronger24.numeric_join": owner = "EXISTING:23"
        elif id == "stronger24.acquired": owner = "66"
        else: raise ValueError("Unassigned original obligation: " + id)
        mapping[id] = owner
    data = {"schema":"REMAINING_SELECTED_DELIVERY_PLAN_V1", "date":"2026-10-24",
            "meaning":"Fixed operational partition for the selected route, not a proved minimal count or a promise all blocked sources can be recovered.",
            "new_delivery_file_count":len(units), "new_numerical_files":sum(r["kind"]=="numerical" for r in units),
            "new_collector_files":sum(r["kind"]=="collector" for r in units), "units":units,
            "anchors":[pin(n) for n in anchors], "original_obligation_assignment":mapping,
            "finite_index_assignment": {str(n): ("NONCOMPUTE:literature.n1" if n==1 else "EXISTING:08" if n in [2,3] else "EXISTING:11" if n==4 else next(r["id"] for r in units if n in r["finite_indices"])) for n in range(1,49)},
            "uniform_tail":{"indices":"all integers n>=49", "arithmetic":"EXISTING:12", "semantic_join":"63", "analytic_input":"NONCOMPUTE:tail49.uniform_analytic_interface"},
            "noncompute_obligations":[r for r in original if r["kind"] in ["literature","analytic_review"]],
            "foundation_acquisition":{"owner":"67", "before":"n5.all_law",
                "all_law_nodes":["n2.all_law","n3.all_law","c4.complete_root","c4.all_law"],
                "strong_n3_side_fact":{"statement":"C3 <= 59*sqrt(3)/250", "arithmetic_source":"EXISTING:08",
                    "analytic_sources":["n3.analytic_reduction","c4.owner_localization"],"cannot_replace_with":"C3 <= C_E"},
                "requires_final_all_index_collector":False},
            "auxiliary24_license":{"logic":"OR", "selected_route":"sharp24_from_58H",
                "alternatives":["Acquired global C24<=C_E implies C24<C_E+1/80", "Full14--23 auxiliary chain plus exact analytic/semantic acquisition"],
                "conclusion":"For the same contrary25 witness, q25<=5/16", "positive_gap":"1/80",
                "does_not_replace":["attainment/contact", "support/owncaps", "current sources and parent-to-contract interfaces"]},
            "additional_noncompute_requirements":["Every enabled numerical kernel and port implements its stated lemma, including interval enclosure/directed rounding, complete grids and negative controls.",
                "Unrestricted common attained positive closed contrary witness, both discrepancy signs/reflection, support before higher moments and exact index/scaling/phase.",
                "Typed current parent-to-contract dominance, source/capture epochs, same marginal/threshold and closed-domain coverage at every semantic join.",
                "Uniform tail is a universal conditional implication, not finitely many experiments or C_n monotonicity."],
            "observed_complete_reuse":{"55":{"scope":"120 selected n35--39 COUNT jobs only", "result_state":"complete_selected_conditional_count_arithmetic_basic", "drive_bundle":"finite1039-counts-n35_39/20261024T014047Z-516cc64f/20261024T014047Z-516cc64f-results.zip", "evidence_kind":"user supplied final output; full ZIP still revalidated by consumer"}},
            "existing_repairs_not_new_files":["35 complete-stage recovery", "46 compatible owncaps/INITIAL recovery", "55 finalization fixed; user reports complete", "59C Python3.13 AST metadata compatibility fix"],
            "acceptance_policy":{"old_PASS_is_provenance_only":True,"complete_source_runtime_closure_required":True,"no_partial_or_unbounded_fallback_acceptance":True,"no_wall_time_completion_guarantee":True},
            "runtime_source_closure_complete":False,"all_notebooks_ready":False,"arithmetic_computed_for_this_plan":False,
            "mathematical_sufficiency_proved":False,"formal_verification":False,"all_index_conclusion_verified":False}
    write("remaining_notebooks_closed_plan.json",data)


if __name__ == "__main__":
    main()
