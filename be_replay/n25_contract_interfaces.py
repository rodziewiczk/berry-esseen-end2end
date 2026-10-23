"""Exact metadata/rational n25 resource-to-count interfaces; no kernel imports.

The caller must first validate the fresh parent/count executions and bind the
actual input file bytes. This module checks their mathematical parameter edge,
not an acquisition, leaf replay, physical-law theorem, or global conclusion.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
import re

SCHEMA = "N25_RESOURCE_COUNT_INTERFACE_V1"
MAPPING_SOURCE = "cutoff25_20261011/new_root/prepare_global_theta_count_v2.py"
MAPPING_SOURCE_SHA256 = "57977808d95691aec623ccde4c209a8e0e15c711c70281a72d0419f2b1b7dcd0"
QUARTER_SOURCE_SHA256 = "07efb2d7e05c00eeaed26747d8ad0c682f282419f1aef9ca7bd58ebad16f999a"
PREMISE = {
    "schema": "ATTAINED_POSITIVE_CLOSED_CONTACT_V1", "sample_size": 25,
    "same_unrestricted_attained_witness": True,
    "positive_closed_threshold": True, "score_at_least_CE": True,
}
UPPER_FIELDS = (
    ("D", "D"), ("d0", "d0"), ("lambda_max", "Lambda"),
    ("H_minus", "Hminus"), ("H_plus", "Hplus"),
    ("radius_minus", "radius_minus"), ("radius_plus", "radius_plus"),
    ("outer0", "outer0"), ("outer1", "outer1"),
)
LOWER_FIELDS = (("charge_b", "binary_charge"), ("charge_g", "gap_charge"),
                ("charge_h", "noise_charge"))
TARGETS = {
    "b4-q0": (4, 29, ["29/100", "117/400"], 0),
    "b4-q1": (4, 29, ["117/400", "59/200"], 1),
    "b4-q2": (4, 29, ["59/200", "119/400"], 2),
    "b4-q3": (4, 29, ["119/400", "3/10"], 3),
    "b3-p33": (3, 33, ["33/100", "17/50"], None),
    "b3-p31-v14-new": (3, 31, ["31/100", "8/25"], None),
    "b3-p32-v14-new": (3, 32, ["8/25", "33/100"], None),
}
V12_REFERENCES = {
    31: "8efeda84e286785b13016738d88bf229d1386f3ce8194dfee868e319fe53862c",
    32: "69a5b51120045874f3a02514aac3d258a7842f33502c05157e08486c9895fe16",
}
QUARTER_PARENT_SHA256 = "e7274cc690ea04ae3b9ce837986e006b9c538dd42d70c42cca5ecd87b23a1934"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    """Reject floats and booleans rather than silently reinterpret them."""
    need(type(value) in (str, int), "Exact rational string or integer required")
    if type(value) is str:
        need(re.fullmatch(r"-?\d+(?:/\d+)?", value) is not None,
             "Integer/fraction notation required")
        need(len(value) <= 20000, "Bounded rational required")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid rational") from exc


def _json_tree(value):
    if type(value) is dict:
        need(all(type(k) is str for k in value), "String JSON keys required")
        for item in value.values():
            _json_tree(item)
    elif type(value) is list:
        for item in value:
            _json_tree(item)
    else:
        need(value is None or type(value) in (str, int, bool),
             "Only exact JSON values are permitted")


def canonical_bytes(value):
    """Object binding, distinct from the caller's original file-byte binding."""
    _json_tree(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def target_spec(target):
    need(type(target) is str and target in TARGETS, "Unknown n25 interface target")
    branch, index, p, quarter = TARGETS[target]
    v14 = target.endswith("-v14-new")
    return dict(target=target, branch="b" + str(branch), branch_number=branch,
                index=index, expected_p_interval=list(p),
                resource_p_interval=[str(F(index, 100)), str(F(index + 1, 100))],
                rho_interval=["13/10", "7/5"] if branch == 3 else ["7/5", "3/2"],
                quarter=quarter, is_new_v14=v14,
                original_v12_reference_filename="ORIGINAL_V12_CONTRACT.json" if v14 else None,
                original_v12_archive_member=(
                    f"cutoff25_20261011/new_root/global_alpha_stoploss2_b3_p{index}_v12/contract.json"
                    if v14 else None),
                original_v12_reference_file_sha256=V12_REFERENCES[index] if v14 else None)


def _upper(q):
    q = rational(q)
    return F(-((-q.numerator * 10**6) // q.denominator) + 1, 10**6)


def _lower(q):
    q = rational(q)
    return F(q.numerator * 10**6 // q.denominator - 1, 10**6)


def _polymin(a, b, c, h):
    need(h >= 0, "Nonnegative closed threshold cap required")
    values = [a, a + b * h + c * h * h]
    if c > 0 and 0 < -b / (2 * c) < h:
        values.append(a - b * b / (4 * c))
    return min(values)


def _validate(target, resource_proof, contract, original_v12_contract):
    spec = target_spec(target)
    branch, index = spec["branch_number"], spec["index"]
    # Hash before any checks and never alter the caller's objects.
    resource_hash = canonical_sha256(resource_proof)
    contract_hash = canonical_sha256(contract)
    need(type(resource_proof) is dict and type(contract) is dict, "JSON objects required")
    if spec["is_new_v14"]:
        need(type(original_v12_contract) is dict, "Original V12 reference is mandatory")
        expected_v14 = deepcopy(original_v12_contract)
        need(type(expected_v14.get("rows")) is list and len(expected_v14["rows"]) == 1,
             "One original V12 row required")
        row = expected_v14["rows"][0]
        need(type(row) is dict and "local_contact_allowance" not in row
             and "local_contact_premise" not in row, "Unmodified original V12 reference required")
        row.update(local_contact_allowance="5/16", local_contact_premise=deepcopy(PREMISE))
        need(canonical_bytes(contract) == canonical_bytes(expected_v14),
             "V14 must equal the entire original V12 dictionary plus exactly two fields")
        baseline = original_v12_contract
    else:
        need(original_v12_contract is None, "V12 targets take no alternate reference")
        baseline = contract
    top_keys = {"status", "branch", "index", "rows", "source_inputs_sha256", "scope"}
    if spec["quarter"] is not None:
        top_keys.add("quarter_partition")
    need(set(baseline) == top_keys, "Complete known contract shape required")
    need(baseline["status"] == "EXACT_GLOBAL_GUARDS_CONDITIONAL_UNTIL_FULL_COMPOSITION"
         and type(baseline["branch"]) is int and baseline["branch"] == branch
         and type(baseline["index"]) is int and baseline["index"] == index,
         "Literal conditional contract branch/index required")
    provenance = baseline["source_inputs_sha256"]
    need(type(provenance) is dict and provenance
         and all(type(k) is str and type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v)
                 for k, v in provenance.items()), "Historical source-hash provenance map required")
    need(type(baseline["scope"]) is str, "Contract scope required")
    need(type(baseline["rows"]) is list and len(baseline["rows"]) == 1,
         "Exactly one count row required")
    cfg = baseline["rows"][0]
    need(type(cfg) is dict, "Count row object required")
    if spec["quarter"] is not None:
        need(baseline["quarter_partition"] == dict(parent=["29/100", "3/10"],
             quarter=spec["quarter"], subpanel=spec["expected_p_interval"],
             source_contract_sha256=QUARTER_PARENT_SHA256), "Exact closed p29 quarter metadata required")
        need(type(baseline["quarter_partition"]["quarter"]) is int, "Integer quarter required")
    need(resource_proof.get("schema") == f"EXACT_SHARP25_B{branch}_GLOBAL_RESOURCES_V1",
         "Whole matching resource proof schema required")
    profile = resource_proof["profile"]
    need(type(profile["n"]) is int and profile["n"] == 25
         and rational(profile["barrier"]) == 0, "Resource n25 zero-barrier profile required")
    rho_lo, rho_hi = map(rational, spec["rho_interval"])
    need(rational(profile["invariants"]["rho_lo"]) == rho_lo
         and rational(profile["invariants"]["rho"]) == rho_hi,
         "Literal matching branch rho profile required")
    rows = resource_proof["rows"]
    need(type(rows) is list and len(rows) == 100
         and all(type(r) is dict and type(r.get("index")) is int and r["index"] == j
                 for j, r in enumerate(rows)), "100 ordered global resource rows required")
    acquired = rows[index]["result"]
    need(acquired["excluded"] is False, "The selected row must be a surviving acquired row")
    x, rr, seed = (acquired[k] for k in ("result", "raw_row", "initial"))
    pl, pu = map(rational, spec["resource_p_interval"])
    need(all(rational(z["pl"]) == pl and rational(z["pu"]) == pu for z in (x, rr, seed)),
         "All simultaneous resource objects must concern the same whole p panel")
    need(type(x["N"]) is int and x["N"] == 25 and rational(x["K"]) == 0
         and type(x["index"]) is int and x["index"] == index,
         "Literal resource export sample size/barrier/index required")
    need(rational(x["rho_lo"]) == rho_lo, "Resource rho floor must match the literal branch")
    checked = []

    def record(path, actual, expected, relation, source_value=None):
        need(type(actual) is str and actual == str(expected), "Exact original mapping: " + path)
        checked.append(dict(field=path, value=actual, expected=str(expected),
                            relation=relation, source=None if source_value is None else str(source_value)))

    expected = dict(n=25, K="0", index=index, p=spec["expected_p_interval"],
                    rho_lower=str(rho_lo), rho_upper=str(rho_hi))
    literal_rho = min(rational(x["rho_hi"]), rho_hi)
    need(rho_lo <= literal_rho <= rho_hi, "Nonempty literal resource rho intersection required")
    for src, dst in UPPER_FIELDS:
        value = rational(x[src]); bound = _upper(x[src])
        need(value >= 0 and (value > 0 if dst in ("d0", "Lambda", "radius_minus", "radius_plus", "outer0", "outer1") else True),
             "Physical nonnegative/positive resource divisor: " + src)
        expected[dst] = str(bound)
        record(dst, cfg[dst], bound, "resource <= target (ceil on 1e6 grid, plus one unit)", value)
    for src, dst in LOWER_FIELDS:
        value = rational(x[src]); bound = _lower(x[src])
        if dst == "binary_charge":
            bound = max(F(0), bound)
            need(value >= bound >= 0, "Nonnegative binary price required")
        else:
            need(value >= bound > 0, "Positive acquired gap/noise price required")
        expected[dst] = str(bound)
        record(dst, cfg[dst], bound, "target <= resource (floor on 1e6 grid, minus one unit)", value)
    need(type(x["quadratics"]) is list and len(x["quadratics"]) == 6
         and type(cfg["quadratics"]) is list and len(cfg["quadratics"]) == 6,
         "All six simultaneous quadratic planes required")
    expected["quadratics"] = []
    for j, q in enumerate(x["quadratics"]):
        mapped = {}
        for key in ("A", "Fplus", "Fminus", "Qbudget"):
            value = rational(q[key])
            bound = _lower(q[key]) if key == "Qbudget" else _upper(q[key])
            if key == "Qbudget":
                need(value >= bound > 0, "Strict positive quadratic budget required")
            mapped[key] = str(bound)
            record(f"quadratics[{j}].{key}", cfg["quadratics"][j][key], bound,
                   "target <= resource" if key == "Qbudget" else "resource <= target", value)
        expected["quadratics"].append(mapped)
    negative = max(rational(rr["A"]), rational(seed["A"]))
    positive = max(rational(rr["B"]), rational(seed["B"]))
    expected["sign_premise"] = dict(schema="ACTUAL_SIGN_CONDITIONED_MARGINAL_V1",
        resource_status="ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST", conditional_means_zero=True)
    for key, value in (("negative_endpoint_lower", negative), ("positive_endpoint_lower", positive)):
        bound = _lower(str(value)); need(0 < bound <= value, "Strict physical endpoint floor required")
        expected["sign_premise"][key] = str(bound)
        record("sign_premise." + key, cfg["sign_premise"][key], bound, "0 < target <= acquired endpoint", value)
    beta = [max(rational(rr["beta_lo"]), rational(seed["beta_lo"])),
            min(rational(rr["beta_hi_signed"]), rational(seed["beta"]))]
    theta = rational(rr["theta"])
    need(0 <= theta < 1, "Physical between-sign variance domain required")
    # The original whole panel is intentional, including for B4 quarters.
    square = (1 - theta) * min(pl * (1 - pl), pu * (1 - pu))
    mean_floor = F(isqrt(square.numerator * 10**24 // square.denominator), 10**12)
    need(mean_floor**2 <= square < (mean_floor + F(1, 10**12))**2,
         "Exact outward lower square-root enclosure required")
    mean = [max(rational(seed["mean_lo"]), rational(rr.get("mean_lo", seed["mean_lo"])), mean_floor),
            min(rational(rr["mean_hi"]), rational(seed["mean_hi"]))]
    need(-1 <= beta[0] <= beta[1] <= 1 and 0 <= mean[0] <= mean[1] <= F(1, 2),
         "Nonempty physical signed beta/mean intersections required")
    expected["acquired_beta"] = [str(max(-F(1), _lower(str(beta[0])))), str(min(F(1), _upper(str(beta[1]))))]
    expected["acquired_mean"] = [str(max(F(0), _lower(str(mean[0])))), str(min(F(1, 2), _upper(str(mean[1]))))]
    for key, bounds in (("acquired_beta", beta), ("acquired_mean", mean)):
        need(type(cfg[key]) is list and len(cfg[key]) == 2, "Closed acquired interval required")
        for j in (0, 1):
            record(f"{key}[{j}]", cfg[key][j], rational(expected[key][j]),
                   "target lower <= acquired lower" if j == 0 else "acquired upper <= target upper", bounds[j])
    expected["acquired_theta_upper"] = str(_upper(str(theta)))
    need(theta <= rational(expected["acquired_theta_upper"]) < 1, "Outward theta cap below one required")
    record("acquired_theta_upper", cfg["acquired_theta_upper"], rational(expected["acquired_theta_upper"]),
           "resource theta <= target theta < 1", theta)
    # Entire row equality also checks n/K/index, exact closed p/rho domains,
    # premise schema/booleans, and rejects every unexpected or missing field.
    need(canonical_bytes(cfg) == canonical_bytes(expected), "Complete exact reconstructed contract row required")
    signed_planes = []
    for sign in ("plus", "minus"):
        field, h = "F" + sign, rational(cfg["H" + sign])
        for j, q in enumerate(x["quadratics"]):
            choices = [(_polymin(rational(t["A"]) - rational(q["A"]),
                                rational(t[field]) - rational(q[field]),
                                rational(q["Qbudget"]) - rational(t["Qbudget"]), h), k)
                       for k, t in enumerate(cfg["quadratics"])]
            margin, k = max(choices)
            need(margin >= 0, "Whole closed signed quadratic-envelope domination required")
            signed_planes.append(dict(sign=sign, source_plane=j, target_plane=k,
                                      threshold_interval=["0", str(h)], margin=str(margin)))
    return dict(schema=SCHEMA, status="VERIFIED_CONDITIONAL_RESOURCE_COUNT_INTERFACE",
        **spec, resource_proof_canonical_sha256=resource_hash, contract_canonical_sha256=contract_hash,
        original_v12_contract_canonical_sha256=(canonical_sha256(original_v12_contract)
                                               if spec["is_new_v14"] else None),
        canonicalization="ASCII JSON, sorted keys, compact separators; floats forbidden",
        mapping_source=MAPPING_SOURCE, mapping_source_sha256=MAPPING_SOURCE_SHA256,
        historical_source_inputs_sha256=deepcopy(provenance),
        historical_source_hashes_are_provenance_only=True,
        checked_fields=checked, checked_signed_quadratic_planes=signed_planes,
        checked_domains=dict(sample_size=25, barrier="0", ordered_global_resource_rows=100,
            selected_resource_row=index, selected_row_survives=True,
            simultaneous_resource_panel=spec["resource_p_interval"],
            closed_count_panel=spec["expected_p_interval"],
            literal_branch_rho=spec["rho_interval"],
            sign_conditioned_zero_mean_dictionary_verified=True,
            both_endpoint_floors_strictly_positive=True,
            signed_beta_and_mean_intersections_nonempty=True,
            acquired_theta_below_one=True, all_contract_fields_reconstructed=True),
        original_resource_rho_upper=str(rational(x["rho_hi"])),
        literal_rho_intersection=[str(rho_lo), str(literal_rho)],
        mean_floor=dict(value=str(mean_floor), square=str(square),
                        grid="1/1000000000000", original_whole_panel=spec["resource_p_interval"]),
        numeric_interface_verified=True, original_v12_dictionary_preserved=spec["is_new_v14"],
        local_contact_allowance="5/16" if spec["is_new_v14"] else None,
        analytic_attained_contact_premise_acquired=False,
        physical_same_law_premises_acquired=False, fresh_parent_execution_validated=False,
        fresh_count_execution_validated=False, native_arithmetic_accepted=False,
        full_n25_conclusion_verified=False, all_index_conclusion_verified=False,
        conditional_premises=[
            "Fresh complete whole-parent resource and INITIAL acceptance, bound by the caller",
            "All simultaneous bounds apply to the same physical sign-conditioned zero-mean law",
            "Retained analytic resource/count and scalar/physical implications",
        ] + (["Same unrestricted attained positive-closed contrary witness with score at least CE",
              "Matching global auxiliary C24 < CE + 1/80, giving q25 <= 5/16"]
             if spec["is_new_v14"] else []),
        scope="Exact conditional parameter implication only; caller must bind original file bytes and fresh execution evidence. Same-law physical, attained-contact and global analytic premises remain separate.")


def validate(target, *, resource_proof: dict, contract: dict,
             original_v12_contract: dict | None = None) -> dict:
    """Fail closed on missing/unknown/incompatible inputs, without kernel calls."""
    try:
        return _validate(target, resource_proof, contract, original_v12_contract)
    except (KeyError, TypeError, IndexError, AttributeError) as exc:
        raise ValueError("Malformed or incomplete resource/count interface input") from exc
