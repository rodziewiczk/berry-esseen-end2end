"""Check scope accounting and dependency consistency, not research arithmetic."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"56I", "57F", "57G", "57H", "58H", "59D", "60", "61", "62", "63", "65", "66", "67"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate(plan, n25, obligations, root=ROOT):
    units = plan["units"]
    byid = {u["id"]: u for u in units}
    require(len(units) == len(byid) == plan["new_delivery_file_count"] == 13, "Delivery census")
    require(set(byid) == EXPECTED, "Selected delivery IDs")
    require(len({u["file"] for u in units}) == 13, "Duplicate delivery filename")
    require(sum(u["kind"] == "numerical" for u in units) == plan["new_numerical_files"] == 12, "Numerical/control file census")
    require(sum(u["kind"] == "collector" for u in units) == plan["new_collector_files"] == 1, "Collector census")
    for u in units:
        require(u["completed_atomic_stage_cache_only"] is True, "Partial stage reuse")
        require(u["mathematically_acquired"] is False, "Plan cannot acquire mathematics")
        if u["kind"] == "numerical":
            require(u["session_wall_ceiling_seconds"] == 82800, "23h numerical session ceiling")
        require(all(dep in byid for dep in u["depends_on"]), "Unassigned predecessor")
    visiting, done = set(), set()
    def visit(id):
        require(id not in visiting, "Dependency cycle: " + id)
        if id in done:
            return
        visiting.add(id)
        for dep in byid[id]["depends_on"]:
            visit(dep)
        visiting.remove(id)
        done.add(id)
    for id in byid:
        visit(id)
    for id in EXPECTED - {"63"}:
        require("63" not in byid[id]["depends_on"], "Global theorem cannot be finite premise")
    require(set(byid["63"]["depends_on"]) == {"67","65","56I","57H","58H","66","59D","60","62","61"}, "Final finite conjunction")
    actual = {1: "NONCOMPUTE:literature.n1", 2: "EXISTING:08", 3: "EXISTING:08", 4: "EXISTING:11"}
    for u in units:
        for n in u["finite_indices"]:
            require(n not in actual, "Duplicate literal index")
            actual[n] = u["id"]
    require(set(actual) == set(range(1, 49)), "Missing or out-of-range literal index")
    require(plan["finite_index_assignment"] == {str(n): actual[n] for n in range(1,49)}, "Literal-index ledger mismatch")
    require(plan["uniform_tail"] == {"indices":"all integers n>=49", "arithmetic":"EXISTING:12", "semantic_join":"63", "analytic_input":"NONCOMPUTE:tail49.uniform_analytic_interface"}, "Uniform tail replaced or omitted")
    ids = {r["id"] for r in obligations["nodes"]}
    require(set(plan["original_obligation_assignment"]) == ids, "Original obligation omitted or invented")
    for id, owner in plan["original_obligation_assignment"].items():
        require(owner in byid or owner.startswith("EXISTING:") or owner == "NONCOMPUTE:"+id, "Invalid obligation owner")
    analytic_ids = {r["id"] for r in obligations["nodes"] if r["kind"] in ["literature","analytic_review"]}
    require({r["id"] for r in plan["noncompute_obligations"]} == analytic_ids, "Analytic/literature premise lost")
    f = plan["foundation_acquisition"]
    require(f["owner"] == "67" and f["before"] == "n5.all_law" and f["requires_final_all_index_collector"] is False, "C4 foundation must precede C5")
    require(f["strong_n3_side_fact"]["statement"] == "C3 <= 59*sqrt(3)/250", "Strong G3 cannot be weakened to sharpCE")
    require(all(plan["original_obligation_assignment"][id] == "67" for id in f["all_law_nodes"]), "Foundation assigned to final global collector")
    require(plan["original_obligation_assignment"]["c5.complement_native"] == "67", "35 prefix is not full complement acceptance")
    require(plan["auxiliary24_license"]["logic"] == "OR" and plan["auxiliary24_license"]["selected_route"] == "sharp24_from_58H", "Auxiliary24 alternate scalar license")
    require(25*Q(plan["auxiliary24_license"]["positive_gap"]) == Q(5,16), "Contact allowance scaling")
    for flag in ["runtime_source_closure_complete", "all_notebooks_ready", "arithmetic_computed_for_this_plan", "mathematical_sufficiency_proved", "formal_verification", "all_index_conclusion_verified"]:
        require(plan[flag] is False, "Unestablished acceptance flag: "+flag)
    # Closed finite regions, including exact signed-beta outer guards and the inclusive tail.
    c = n25["physical_cover"]
    require(c["lower_rho_endpoints"] == ["1","11/10","6/5","13/10","7/5","3/2","33/20"], "Lower rho seam")
    require(c["middle_rho"] == ["33/20","7/4"] and c["high_rho"] == ["7/4","459061/250000"], "Middle/high rho seam")
    require(c["middle_beta_endpoints"] == ["-13/20","0","4/25","321/1000","2/5","12/25","14/25","307827/500000"], "Middle signed-beta cover")
    require(c["high_beta_endpoints"] == ["-640471/1000000","0","321/1000","2/5","12/25","14/25","640471/1000000"], "High signed-beta cover")
    require(c["lower_each_all_p"] == ["0","1"] and c["finite_intervals_closed"] is True, "Closed probability/finite cover")
    require(c["universal_tail_rho_lower_included"] == "459061/250000", "Inclusive n25 rho tail")
    require(n25["physical_piece_count"] == 6+7+6+1 == 20, "Physical pieces are not historical record count")
    for r,b in [(Q(7,4),Q(307827,500000)),(Q(459061,250000),Q(640471,1000000))]:
        require((1+b*b)**2-r*r*(1-b*b)>0, "Exact outer beta guard")
    r = Q(459061,250000)
    t = min(Q(469,1000),Q(1661,5000)*(1+Q(429,1000)/r),Q(3031,10000)*(1+Q(323,500)/r))
    require(t <= Q(40973218,100000000), "Inclusive n25 rho-tail scalar bound")
    rows = n25["additional_ordinary_count_jobs"]
    require(len(rows) == 21 and sum(not r["capsule_member_supplied"] for r in rows) == 11, "Additional ordinary forest census")
    require(n25["missing_ordinary_capsules"] == 11 and n25["supplied_additional_ordinary_forests"] == 10, "Missing sources hidden")
    require(len(n25["mixed_selected_components"]) == 2 and {r["index"] for r in n25["mixed_selected_components"]} == {24,25}, "Mixed route omitted")
    require(all(r["ordinary_count_protocol_compatible"] is False for r in n25["mixed_selected_components"]), "Mixed route mislabeled ordinary")
    require(len(n25["noncount_source_entrypoint_assignments"]) == 53, "Original n25 source family omitted")
    require({s["id"] for s in n25["sections"]} == {"b34","b5_missing","b5_mixed","upper_counts","high_beta2","middle_b3","middle_b012","older_upper","semantic_union"}, "n25 section omitted")
    require(n25["runtime_source_closure_complete"] is False and n25["numerical_action_census_sealed"] is False, "Source/action closure overclaim")
    anchors = plan["anchors"] + n25["anchors"]
    for a in anchors:
        p = root / a["path"]
        require(p.is_file(), "Source specification unavailable: "+a["path"])
        data = p.read_bytes()
        require(len(data) == a["bytes"] and hashlib.sha256(data).hexdigest() == a["sha256"], "Stale source specification: "+a["path"])
    return {"scope":"SPECIFICATION_ACCOUNTING_ONLY", "delivery_files":13, "numerical_or_control_files":12,
            "collector_files":1,"literal_indices":48,"n25_physical_pieces":20,
            "original_obligations_assigned":len(ids), "dependency_graph_acyclic":True,
            "source_runtime_closure_complete":False, "all_index_conclusion_verified":False}


def main():
    def load(name):
        return json.loads((ROOT/"proof"/name).read_text(encoding="utf-8"))
    print(json.dumps(validate(load("remaining_notebooks_closed_plan.json"),
                              load("remaining_n25_execution_partition.json"),
                              load("obligations.json")), indent=2))


if __name__ == "__main__":
    main()
