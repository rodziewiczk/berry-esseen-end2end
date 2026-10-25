"""Mathematical boundary/negative controls for the small source-conditional pilot."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import os
from tempfile import TemporaryDirectory
import unittest

from be.codec import digest, load_json, parse_rational, rational
from be.errors import ProtocolError
from be.producer import produce_request
from be.semantic import (PROOF_SCOPE, authorized_readback, derive_problem,
                         freeze_request, parse_request, sqrt_enclosure, validate_source_files, verify_request)
from be.worker import _write_atomic

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples/local-pilot"


def request_for(p=Fraction(1, 4), lower=Fraction(1), upper=Fraction(1)):
    problem = deepcopy(load_json(EX / "problem.json"))
    problem["context"]["p"] = rational(p)
    problem["context"]["rho"] = {"lower": rational(lower), "upper": rational(upper)}
    return freeze_request(problem, load_json(EX / "source-manifest.json"), load_json(EX / "trust-profile.json"))


class SemanticTests(unittest.TestCase):
    def test_quarter_probability_gives_exact_farkas_contradiction(self):
        request = request_for()
        candidate = produce_request(request)
        receipt = verify_request(request, candidate)
        self.assertEqual(receipt["core"]["outcome"], "infeasible")
        self.assertEqual(receipt["core"]["farkas_totals"]["normal"], [rational(0), rational(0)])
        self.assertLess(parse_rational(receipt["core"]["farkas_totals"]["rhs"]), 0)
        self.assertFalse(receipt["core"]["full_proof_pass"])
        self.assertEqual(receipt["core"]["proof_scope"], PROOF_SCOPE)
        self.assertEqual(authorized_readback(request, candidate, receipt), receipt)

    def test_lower_strip_can_also_prove_contradiction(self):
        request = request_for(lower=Fraction(2), upper=Fraction(2))
        self.assertEqual(verify_request(request, produce_request(request))["core"]["outcome"], "infeasible")

    def test_symmetric_bernoulli_is_not_excluded(self):
        request = request_for(p=Fraction(1, 2))
        problem = derive_problem(request)
        self.assertEqual(problem["root_enclosure"]["h3_lower"], rational(Fraction(1, 8)))
        self.assertEqual(problem["root_enclosure"]["h3_upper"], rational(Fraction(1, 8)))
        self.assertEqual(verify_request(request, produce_request(request))["core"]["outcome"], "no_contradiction")

    def test_wide_rho_containing_bernoulli_is_not_excluded(self):
        request = request_for(upper=Fraction(2))
        self.assertEqual(verify_request(request, produce_request(request))["core"]["outcome"], "no_contradiction")

    def test_nondyadic_rational_square_is_exact(self):
        self.assertEqual(sqrt_enclosure(Fraction(4, 25), 8), (Fraction(2, 5), Fraction(2, 5)))
        request = request_for(p=Fraction(1, 5), lower=Fraction(17, 10), upper=Fraction(17, 10))
        self.assertEqual(verify_request(request, produce_request(request))["core"]["outcome"], "no_contradiction")

    def test_irrational_root_bounds_are_checked_by_rational_squares(self):
        for bits in (8, 16, 128, 512):
            low, high = sqrt_enclosure(Fraction(3, 16), bits)
            self.assertLessEqual(low*low, Fraction(3, 16))
            self.assertGreaterEqual(high*high, Fraction(3, 16))
            self.assertEqual(high-low, Fraction(1, 1 << bits))

    def test_invalid_contexts_cannot_be_interpreted_as_empty(self):
        for p, lo, hi in [(0, 1, 1), (Fraction(3, 4), 1, 1), (Fraction(1, 4), Fraction(9, 10), 1),
                          (Fraction(1, 4), 2, 1)]:
            with self.assertRaises(ProtocolError):
                request_for(Fraction(p), Fraction(lo), Fraction(hi))
        problem = deepcopy(load_json(EX / "problem.json"))
        problem["context"]["conditional_variance0"] = rational(Fraction(1, 100))
        with self.assertRaises(ProtocolError):
            freeze_request(problem, load_json(EX / "source-manifest.json"), load_json(EX / "trust-profile.json"))

    def test_request_mutation_and_source_mutation_are_rejected(self):
        request = request_for()
        request["core"]["problem"]["context"]["p"] = rational(Fraction(1, 2))
        with self.assertRaises(ProtocolError):
            parse_request(request)
        request = request_for()
        request["core"]["source_manifest"]["source_files"][0]["bytes_digest"] = "sha256:" + "0"*64
        request["request_id"] = digest("request", request["core"])
        with self.assertRaises(ProtocolError):
            parse_request(request)

    def test_oversized_substituted_source_is_bounded_and_rejected(self):
        manifest = load_json(EX / "source-manifest.json")
        temporary_parent = ROOT / ".test_tmp"
        temporary_parent.mkdir(exist_ok=True)
        if not temporary_parent.resolve().is_relative_to(ROOT.resolve()):
            raise RuntimeError("Test temporary directory must remain inside the checkout")
        with TemporaryDirectory(dir=temporary_parent) as temporary:
            base = Path(temporary)
            for entry in manifest["source_files"]:
                path = base / entry["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / entry["path"]).read_bytes())
            (base / "docs/contracts/COUNT-RULES.md").write_bytes(b"x" * (1024 * 1024 + 1))
            with self.assertRaises(ProtocolError) as caught:
                validate_source_files(manifest, base)
            self.assertEqual(caught.exception.code, "source_resource_limit")

    def test_unrelated_inconsistent_problem_cannot_supply_empty(self):
        request = request_for()
        candidate = produce_request(request)
        fake_problem = derive_problem(request)
        fake_problem["rows"][0]["rhs"] = rational(-1)
        candidate["problem_digest"] = digest("derived-problem", fake_problem)
        receipt = verify_request(request, candidate)
        self.assertEqual(receipt["core"]["outcome"], "rejected")
        self.assertEqual(receipt["core"]["reason_code"], "problem_binding_mismatch")

    def test_negative_zero_and_wrong_branch_multipliers_fail(self):
        request = request_for()
        for values in [[-1, 0, 0, 0, 0, 0], [0]*6,
                       [0, Fraction(3, 4), Fraction(1, 4), 0, 0, 1]]:
            candidate = produce_request(request)
            candidate["witness"] = {"kind": "farkas", "multipliers": [rational(v) for v in values]}
            self.assertEqual(verify_request(request, candidate)["core"]["outcome"], "rejected")

    def test_forced_farkas_on_feasible_context_is_rejected(self):
        request = request_for(p=Fraction(1, 2))
        candidate = produce_request(request)
        candidate["witness"] = {"kind": "farkas", "multipliers": [rational(0)]*6}
        self.assertEqual(verify_request(request, candidate)["core"]["outcome"], "rejected")

    def test_invalid_feasible_point_and_extra_planes_are_rejected(self):
        request = request_for(p=Fraction(1, 2))
        candidate = produce_request(request)
        candidate["witness"]["point"] = [rational(1), rational(0)]
        self.assertEqual(verify_request(request, candidate)["core"]["reason_code"], "invalid_relaxed_point")
        candidate = produce_request(request)
        candidate["planes"] = []
        self.assertEqual(verify_request(request, candidate)["core"]["reason_code"], "candidate_schema_invalid")

    def test_forged_stored_receipt_is_not_authorized_by_outcome(self):
        request = request_for(p=Fraction(1, 2))
        candidate = produce_request(request)
        receipt = verify_request(request, candidate)
        receipt["core"]["outcome"] = "infeasible"
        receipt["receipt_id"] = digest("verification-receipt", receipt["core"])
        with self.assertRaises(ProtocolError):
            authorized_readback(request, candidate, receipt)

    def test_atomic_worker_output_uses_a_short_independent_temp_name(self):
        parent = ROOT / ".test_tmp"
        parent.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=parent) as temporary:
            base = Path(temporary)
            padding = 214-len(str(base))-1
            if padding < 1:
                self.skipTest("Checkout is too long for the original 214-character regression fixture")
            deep = base / ("d"*padding)
            deep.mkdir()
            output = deep / "output.json"
            _write_atomic(output, {"value": "ok"})
            self.assertEqual(load_json(output), {"value": "ok"})
            self.assertEqual([p.name for p in deep.iterdir()], ["output.json"])

    @unittest.skipUnless(os.name == "nt", "Windows path profile")
    def test_windows_output_path_limit_is_a_typed_input_error(self):
        too_long = ROOT / ("x"*200) / "output.json"
        with self.assertRaises(ProtocolError) as caught:
            _write_atomic(too_long, {"value": "ok"})
        self.assertEqual(caught.exception.code, "output_path_too_long")


if __name__ == "__main__":
    unittest.main()
