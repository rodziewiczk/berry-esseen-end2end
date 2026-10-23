"""Exact rational lower-n25 resource-to-contract implications.

This is a transparent new join of already observed acquisitions. It does not
evaluate a count leaf or import any archived mathematical module. The analytic
same-witness/contact/physical-marginal interpretation remains an explicit premise.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import isqrt

from . import count_task as common, n25_b012_acquisition_sources as sources

need = sources.need


def rational(value):
    need(type(value) is str, "Exact serialized rational, not a boolean or float")
    return F(value)


def minimum(a, b, c, upper):
    need(upper >= 0, "Nonnegative signed threshold interval")
    candidates = [a, a+b*upper+c*upper*upper]
    if c > 0 and 0 < -b/(2*c) < upper:
        candidates.append(a-b*b/(4*c))
    return min(candidates)


def mean_floor(pl, pu, theta, retained):
    need(0 <= pl < pu <= 1 and 0 <= theta < 1, "Actual variance-to-mean physical domain")
    value = (1-theta)*min(pl*(1-pl), pu*(1-pu))
    scale = 10**12
    floor = F(isqrt((value*scale*scale).numerator//(value*scale*scale).denominator), scale)
    return max(retained, floor)


def interface(resource, cfg, rho_upper, *, invariants=None):
    need(resource["excluded"] is False, "Actual accepted surviving acquisition")
    rr, seed, acquired = resource["raw_row"], resource["initial"], resource["result"]
    pl, pu = rational(rr["pl"]), rational(rr["pu"])
    tl, tu = map(rational, cfg["p"])
    need(type(cfg["n"]) is int and cfg["n"] == 25 and rational(cfg["K"]) == 0
         and type(cfg["index"]) is int and pl == F(cfg["index"], 100)
         and pu == F(cfg["index"]+1, 100) and pl <= tl < tu <= pu,
         "Actual index and closed selected subpanel")
    need(all(rational(row["pl"]) == pl and rational(row["pu"]) == pu for row in (seed, acquired)),
         "One same-law physical probability panel")
    lower = rational(acquired["rho_lo"])
    upper = min(rational(acquired["rho_hi"]), rho_upper)
    need(F(1) <= rational(cfg["rho_lower"]) <= lower <= upper <= rational(cfg["rho_upper"]),
         "Entire acquired rho interval fits count contract")
    for a, b in (("D", "D"), ("d0", "d0"), ("lambda_max", "Lambda"),
                 ("H_minus", "Hminus"), ("H_plus", "Hplus"), ("radius_minus", "radius_minus"),
                 ("radius_plus", "radius_plus"), ("outer0", "outer0"), ("outer1", "outer1")):
        need(0 <= rational(acquired[a]) <= rational(cfg[b]), "Acquired complete upper bound: "+b)
    for a, b in (("charge_b", "binary_charge"), ("charge_g", "gap_charge"), ("charge_h", "noise_charge")):
        need(rational(acquired[a]) >= rational(cfg[b]) >= 0, "Acquired nonnegative charge lower bound: "+b)
    need(type(cfg["quadratics"]) is list and cfg["quadratics"]
         and type(acquired["quadratics"]) is list and acquired["quadratics"], "Nonempty full signed envelopes")
    domination = []
    for sign in ("plus", "minus"):
        field, ceiling = "F"+sign, rational(cfg["H"+sign])
        for i, row in enumerate(acquired["quadratics"]):
            margins = [minimum(rational(t["A"])-rational(row["A"]),
                rational(t[field])-rational(row[field]), rational(row["Qbudget"])-rational(t["Qbudget"]), ceiling)
                for t in cfg["quadratics"]]
            margin = max(margins)
            need(margin >= 0, "Whole-interval signed quadratic domination")
            domination.append(dict(sign=sign, acquired=i, target=margins.index(margin), margin=str(margin)))
    sign = cfg["sign_premise"]
    need(sign["schema"] == "ACTUAL_SIGN_CONDITIONED_MARGINAL_V1"
         and sign["conditional_means_zero"] is True, "Literal actual centered sign-conditioned marginal premise")
    endpoints = {}
    for key, name in (("A", "negative_endpoint_lower"), ("B", "positive_endpoint_lower")):
        value = max(rational(rr[key]), rational(seed[key]))
        need(0 < rational(sign[name]) <= value, "Actual physical endpoint lower bound")
        endpoints[name] = str(value)
    if invariants is None:
        beta = [max(rational(rr["beta_lo"]), rational(seed["beta_lo"])),
                min(rational(rr["beta_hi_signed"]), rational(seed["beta"]))]
        mean = [mean_floor(pl, pu, rational(rr["theta"]), max(rational(seed["mean_lo"]),
                         rational(rr.get("mean_lo", seed["mean_lo"])))),
                min(rational(seed["mean_hi"]), rational(rr["mean_hi"]))]
    else:
        beta = [max(rational(invariants["beta_lo"]), rational(rr["beta_lo"]), rational(seed["beta_lo"])),
                min(rational(invariants["beta_hi"]), rational(rr["beta_hi_signed"]), rational(seed["beta"]))]
        mean = [mean_floor(pl, pu, rational(rr["theta"]), max(rational(invariants["mean_lo"]), rational(seed["mean_lo"]))),
                min(rational(invariants["mean_hi"]), rational(seed["mean_hi"]), rational(rr["mean_hi"]))]
    need(rational(cfg["acquired_beta"][0]) <= beta[0] <= beta[1] <= rational(cfg["acquired_beta"][1])
         and rational(cfg["acquired_mean"][0]) <= mean[0] <= mean[1] <= rational(cfg["acquired_mean"][1]),
         "Entire acquired signed beta and mean ranges fit the count contract")
    theta = None
    if "acquired_theta_upper" in cfg:
        need(0 <= rational(rr["theta"]) <= rational(cfg["acquired_theta_upper"]) < 1,
             "Separate physical theta bound; it does not replace coupled Lambda")
        theta = dict(actual=rr["theta"], target=cfg["acquired_theta_upper"])
    return dict(p_interval=cfg["p"], rho_interval=[str(lower), str(upper)],
                beta=list(map(str, beta)), mean=list(map(str, mean)), endpoints=endpoints,
                signed_quadratic_domination=domination, theta=theta)


def join(task, branch):
    from . import n25_b012_acquisition_evidence as evidence
    evidence.validate_prefix(task, branch, len(sources.stages(branch)))
    parent, local, jobs = sources.definition(branch)
    root = evidence.root(task)
    global_folder = root/parent["global_resource"]["directory"].removeprefix(sources.source.PREFIX)
    global_proof = common.read(global_folder/("RESOURCE_"+branch.upper()+"_GLOBAL_PROOF.json"), 128*1024**2)
    local_proof = None
    if local:
        folder = root/local["cwd_member_prefix"].removeprefix(sources.source.PREFIX)
        local_proof = common.read(folder/f'PANEL_{local["panel"]}_PROOF.json', 128*1024**2)
    rows = []
    for job in jobs:
        folder = root/job["capsule_member_prefix"].removeprefix(sources.source.PREFIX)
        packet = common.read(folder/"contract.json", 4*1024**2)
        need(len(packet["rows"]) == 1, "One fixed selected count contract")
        cfg = packet["rows"][0]
        use_local = local is not None and job["index"] == local["panel"]
        res = (local_proof["rows"][0]["survivor_resource"] if use_local
               else global_proof["rows"][job["index"]]["result"])
        inv = local_proof["rows"][0]["cycles"][-1]["profile"]["invariants"] if use_local else None
        result = interface(res, cfg, F(parent["rho_interval"][1]), invariants=inv)
        rows.append(dict(job_id=job["target_id"], contract_sha256=common.digest(folder/"contract.json"),
                         acquired_from="local" if use_local else "global", **result))
    # Every global survivor is covered by a disjoint literal closed partition.
    for index in parent["global_resource"]["surviving_panels"]:
        pieces = sorted((list(map(F, row["p_interval"])) for row in rows
                         if next(j for j in jobs if j["target_id"] == row["job_id"])["index"] == index))
        endpoint = F(index, 100)
        need(pieces, "No uncovered surviving global panel")
        for lo, hi in pieces:
            need(lo == endpoint and lo < hi, "Exact adjacent closed count partition")
            endpoint = hi
        need(endpoint == F(index+1, 100), "Whole surviving panel covered to its closed upper endpoint")
    return dict(schema="N25_B012_FRESH_NUMERIC_INTERFACES_V1", branch=branch, n=25, rows=rows,
        semantic_resource_to_contract_edges=len(rows), full_survivor_probability_cover=True,
        conditional_resource_interfaces_verified=True, count_forests_accepted=False,
        stronger24_premise_acquired=False, analytic_same_witness_implications_verified=False,
        native_arithmetic_accepted=False, all_index_conclusion_verified=False)
