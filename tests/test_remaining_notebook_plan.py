"""Negative checks for scope omissions, cycles and false acceptance claims."""
import copy
import json
import unittest
from pathlib import Path

from tools.check_remaining_notebook_plan import validate

ROOT = Path(__file__).resolve().parents[1]


class RemainingPlan(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/"proof/remaining_notebooks_closed_plan.json").read_text(encoding="utf-8"))
        self.n25 = json.loads((ROOT/"proof/remaining_n25_execution_partition.json").read_text(encoding="utf-8"))
        self.old = json.loads((ROOT/"proof/obligations.json").read_text(encoding="utf-8"))

    def check(self):
        return validate(self.plan,self.n25,self.old)

    def test_valid_specification_retains_unacquired_flags(self):
        self.assertFalse(self.check()["all_index_conclusion_verified"])

    def test_missing_literal_index_rejected(self):
        next(u for u in self.plan["units"] if u["id"]=="61")["finite_indices"].remove(48)
        with self.assertRaisesRegex(ValueError,"literal index"):
            self.check()

    def test_global_as_finite_premise_rejected(self):
        next(u for u in self.plan["units"] if u["id"]=="59D")["depends_on"].append("63")
        with self.assertRaisesRegex(ValueError,"cycle"):
            self.check()

    def test_missing_or_shifted_cover_rejected(self):
        for key,index,value in [("middle_rho",0,"166/100"),("middle_beta_endpoints",3,"322/1000")]:
            with self.subTest(key=key):
                old = copy.deepcopy(self.n25)
                self.n25["physical_cover"][key][index]=value
                with self.assertRaises(ValueError): self.check()
                self.n25=old

    def test_mixed_and_original_family_omissions_rejected(self):
        for key in ["mixed_selected_components","noncount_source_entrypoint_assignments"]:
            with self.subTest(key=key):
                old=copy.deepcopy(self.n25)
                self.n25[key].pop()
                with self.assertRaises(ValueError): self.check()
                self.n25=old

    def test_missing_old_obligation_rejected(self):
        self.plan["original_obligation_assignment"].pop("c4.owner_localization")
        with self.assertRaisesRegex(ValueError,"obligation"):
            self.check()

    def test_false_success_and_wrong_budget_rejected(self):
        self.plan["all_index_conclusion_verified"]=True
        with self.assertRaisesRegex(ValueError,"acceptance flag"):
            self.check()
        self.plan["all_index_conclusion_verified"]=False
        next(u for u in self.plan["units"] if u["kind"]=="numerical")["session_wall_ceiling_seconds"]=64800
        with self.assertRaisesRegex(ValueError,"23h"):
            self.check()

    def test_finite_sampling_cannot_replace_uniform_tail(self):
        self.plan["uniform_tail"]["indices"]="49,50,51"
        with self.assertRaisesRegex(ValueError,"Uniform tail"):
            self.check()

    def test_changed_anchor_rejected(self):
        self.plan["anchors"][0]["sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"Stale source"):
            self.check()

    def test_foundation_hidden_global_cycle_or_weakened_n3_rejected(self):
        self.plan["original_obligation_assignment"]["c4.all_law"]="63"
        with self.assertRaisesRegex(ValueError,"Foundation"):
            self.check()
        self.plan["original_obligation_assignment"]["c4.all_law"]="67"
        self.plan["foundation_acquisition"]["strong_n3_side_fact"]["statement"]="C3 <= C_E"
        with self.assertRaisesRegex(ValueError,"Strong G3"):
            self.check()


if __name__=="__main__":
    unittest.main()
