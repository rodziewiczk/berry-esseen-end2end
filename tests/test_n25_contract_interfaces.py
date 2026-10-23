"""Small synthetic rational fixtures only: never import or run proof kernels."""
from copy import deepcopy
from fractions import Fraction as F
import unittest

from be_replay import n25_contract_interfaces as subject


def fixture(target="b3-p33"):
    spec = subject.target_spec(target)
    branch, index = spec["branch_number"], spec["index"]
    pl, pu = spec["resource_p_interval"]
    rho_lo, rho_hi = spec["rho_interval"]
    x = dict(N=25, K="0", index=index, pl=pl, pu=pu,
             rho_lo=rho_lo, rho_hi=rho_hi, D="1", d0="1/2", lambda_max="1/3",
             H_minus="2", H_plus="3", radius_minus="2", radius_plus="3",
             outer0="1", outer1="2", charge_b="1/5", charge_g="2", charge_h="3",
             quadratics=[dict(A=str(j + 1), Fplus=str(j + 2), Fminus=str(j + 3), Qbudget="1/2")
                         for j in range(6)])
    rr = dict(pl=pl, pu=pu, A="1/3", B="3/4", beta_lo="-1/10",
              beta_hi_signed="1/2", theta="1/4", mean_hi="12/25")
    seed = dict(pl=pl, pu=pu, A="1/4", B="1/2", beta_lo="-1/5", beta="2/5",
                mean_lo="9/20", mean_hi="49/100")
    proof = dict(schema=f"EXACT_SHARP25_B{branch}_GLOBAL_RESOURCES_V1",
                 profile=dict(n=25, barrier="0", invariants=dict(rho_lo=rho_lo, rho=rho_hi)),
                 rows=[dict(index=j, result=dict(excluded=True)) for j in range(100)])
    proof["rows"][index]["result"] = dict(excluded=False, result=x, raw_row=rr, initial=seed)
    # Independent explicit answers, including the extra outward unit on integers.
    cfg = dict(n=25, K="0", index=index, p=spec["expected_p_interval"],
               rho_lower=rho_lo, rho_upper=rho_hi, D="1000001/1000000",
               d0="500001/1000000", Lambda="66667/200000",
               Hminus="2000001/1000000", Hplus="3000001/1000000",
               radius_minus="2000001/1000000", radius_plus="3000001/1000000",
               outer0="1000001/1000000", outer1="2000001/1000000",
               binary_charge="199999/1000000", gap_charge="1999999/1000000",
               noise_charge="2999999/1000000",
               quadratics=[dict(A=str(F((j + 1) * 10**6 + 1, 10**6)),
                                Fplus=str(F((j + 2) * 10**6 + 1, 10**6)),
                                Fminus=str(F((j + 3) * 10**6 + 1, 10**6)),
                                Qbudget="499999/1000000") for j in range(6)],
               sign_premise=dict(schema="ACTUAL_SIGN_CONDITIONED_MARGINAL_V1",
                   resource_status="ASSUMED_ACQUIRED_FOR_CONDITIONAL_TEST",
                   conditional_means_zero=True, negative_endpoint_lower="83333/250000",
                   positive_endpoint_lower="749999/1000000"),
               acquired_beta=["-100001/1000000", "400001/1000000"],
               acquired_mean=["449999/1000000", "480001/1000000"],
               acquired_theta_upper="250001/1000000")
    contract = dict(status="EXACT_GLOBAL_GUARDS_CONDITIONAL_UNTIL_FULL_COMPOSITION",
                    branch=branch, index=index, rows=[cfg],
                    source_inputs_sha256={"historical/resource_receipt.json": "a" * 64},
                    scope="Synthetic conditional fixture")
    if spec["quarter"] is not None:
        contract["quarter_partition"] = dict(parent=["29/100", "3/10"], quarter=spec["quarter"],
            subpanel=spec["expected_p_interval"], source_contract_sha256=subject.QUARTER_PARENT_SHA256)
    original = None
    if spec["is_new_v14"]:
        original = deepcopy(contract)
        cfg.update(local_contact_allowance="5/16", local_contact_premise=deepcopy(subject.PREMISE))
    return proof, contract, original


class Interfaces(unittest.TestCase):
    def check(self, target="b3-p33", mutate=None):
        proof, contract, original = fixture(target)
        if mutate:
            mutate(proof, contract, original)
        return subject.validate(target, resource_proof=proof, contract=contract,
                                original_v12_contract=original)

    def reject(self, mutate, target="b3-p33"):
        with self.assertRaises(ValueError):
            self.check(target, mutate)

    def test_all_seven_small_fixtures(self):
        for target in subject.TARGETS:
            with self.subTest(target=target):
                result = self.check(target)
                self.assertEqual(result["schema"], "N25_RESOURCE_COUNT_INTERFACE_V1")
                self.assertTrue(result["numeric_interface_verified"])
                self.assertEqual(len(result["checked_signed_quadratic_planes"]), 12)
                self.assertEqual(len(result["checked_fields"]), 43)
                self.assertFalse(result["analytic_attained_contact_premise_acquired"])
                self.assertFalse(result["fresh_parent_execution_validated"])
                self.assertFalse(result["full_n25_conclusion_verified"])

    def test_every_mapped_scalar_and_plane_is_required(self):
        fields = [dst for _, dst in subject.UPPER_FIELDS + subject.LOWER_FIELDS]
        fields += ["acquired_theta_upper"]
        for key in fields:
            with self.subTest(key=key):
                self.reject(lambda p, c, o: c["rows"][0].__setitem__(key, "0"))
        for j in range(6):
            for key in ("A", "Fplus", "Fminus", "Qbudget"):
                with self.subTest(plane=j, field=key):
                    self.reject(lambda p, c, o: c["rows"][0]["quadratics"][j].__setitem__(key, "0"))

    def test_no_defect_rescale_or_joint_intercept_swap(self):
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("D", "1000001/25000000"))
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("Lambda", "500001/1000000"))

    def test_extra_outward_unit_is_mandatory(self):
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("D", "1"))
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("gap_charge", "2"))

    def test_same_law_panel_and_complete_global_selector(self):
        self.reject(lambda p, c, o: p["rows"].reverse())
        self.reject(lambda p, c, o: p["rows"].pop())
        self.reject(lambda p, c, o: p["rows"][33]["result"]["raw_row"].__setitem__("pl", "1/3"))
        self.reject(lambda p, c, o: p["rows"][33]["result"].__setitem__("excluded", True))

    def test_literal_rho_intersection_and_profile(self):
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("rho_upper", "3/2"))
        self.reject(lambda p, c, o: p["profile"]["invariants"].__setitem__("rho", "3/2"))
        self.reject(lambda p, c, o: p["rows"][33]["result"]["result"].__setitem__("rho_hi", "1"))
        result = self.check(mutate=lambda p, c, o: p["rows"][33]["result"]["result"].__setitem__("rho_hi", "2"))
        self.assertEqual(result["literal_rho_intersection"], ["13/10", "7/5"])

    def test_physical_sign_endpoint_guards(self):
        self.reject(lambda p, c, o: c["rows"][0]["sign_premise"].__setitem__("conditional_means_zero", 1))
        self.reject(lambda p, c, o: c["rows"][0]["sign_premise"].__setitem__("negative_endpoint_lower", "0"))
        self.reject(lambda p, c, o: c["rows"][0]["sign_premise"].__setitem__("schema", "OTHER"))

    def test_beta_mean_theta_and_empty_intersections(self):
        for key in ("acquired_beta", "acquired_mean"):
            for j in (0, 1):
                self.reject(lambda p, c, o: c["rows"][0][key].__setitem__(j, "0"))
        self.reject(lambda p, c, o: p["rows"][33]["result"]["raw_row"].__setitem__("theta", "1"))
        self.reject(lambda p, c, o: p["rows"][33]["result"]["raw_row"].__setitem__("beta_lo", "3/4"))
        self.reject(lambda p, c, o: p["rows"][33]["result"]["initial"].__setitem__("mean_lo", "3/4"))

    def test_b4_closed_seams_and_original_panel_mean_floor(self):
        results = [self.check("b4-q" + str(j)) for j in range(4)]
        self.assertEqual(results[0]["expected_p_interval"][0], "29/100")
        self.assertEqual(results[-1]["expected_p_interval"][1], "3/10")
        for left, right in zip(results, results[1:]):
            self.assertEqual(left["expected_p_interval"][1], right["expected_p_interval"][0])
        self.assertEqual(len({r["mean_floor"]["square"] for r in results}), 1)
        self.assertTrue(all(r["mean_floor"]["original_whole_panel"] == ["29/100", "3/10"] for r in results))
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("p", ["29/100", "3/10"]), "b4-q0")
        self.reject(lambda p, c, o: c["quarter_partition"].__setitem__("quarter", True), "b4-q1")

    def test_exact_integer_sqrt_floor_and_strict_upper_neighbor(self):
        result = self.check()
        mf, sq = map(F, (result["mean_floor"]["value"], result["mean_floor"]["square"]))
        self.assertLessEqual(mf * mf, sq)
        self.assertLess(sq, (mf + F(1, 10**12))**2)

    def test_v14_entire_original_dictionary_plus_exact_two_fields(self):
        target = "b3-p31-v14-new"
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("local_contact_allowance", "0"), target)
        self.reject(lambda p, c, o: c["rows"][0]["local_contact_premise"].__setitem__("same_unrestricted_attained_witness", False), target)
        self.reject(lambda p, c, o: c.__setitem__("scope", "Changed unrelated field"), target)
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("new_cap", "1"), target)
        p, c, _ = fixture(target)
        with self.assertRaises(ValueError):
            subject.validate(target, resource_proof=p, contract=c)
        self.assertEqual(subject.target_spec(target)["original_v12_reference_filename"], "ORIGINAL_V12_CONTRACT.json")

    def test_provenance_does_not_force_historical_timing_receipt(self):
        result = self.check(mutate=lambda p, c, o: c["source_inputs_sha256"].__setitem__("historical/resource_receipt.json", "b" * 64))
        self.assertTrue(result["historical_source_hashes_are_provenance_only"])
        self.assertEqual(result["historical_source_inputs_sha256"]["historical/resource_receipt.json"], "b" * 64)

    def test_object_binding_no_mutation_and_exact_types(self):
        p, c, _ = fixture()
        before = deepcopy((p, c))
        r = subject.validate("b3-p33", resource_proof=p, contract=c)
        self.assertEqual((p, c), before)
        self.assertEqual(r["resource_proof_canonical_sha256"], subject.canonical_sha256(p))
        self.assertEqual(r["contract_canonical_sha256"], subject.canonical_sha256(c))
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("D", 1.0))
        self.reject(lambda p, c, o: p["rows"][33].__setitem__("index", True))
        self.reject(lambda p, c, o: c["rows"][0].__setitem__("unknown", "1"))
        with self.assertRaises(ValueError):
            subject.validate("foreign", resource_proof=p, contract=c)

    def test_rational_clamps_and_exact_polymin_interior(self):
        self.assertEqual(subject._upper("1"), F(1000001, 1000000))
        self.assertEqual(subject._lower("-1/3"), F(-66667, 200000))
        self.assertEqual(subject._polymin(F(1), F(-4), F(4), F(1)), 0)
        self.assertEqual(subject._polymin(F(0), F(-4), F(4), F(1)), -1)


if __name__ == "__main__":
    unittest.main()
