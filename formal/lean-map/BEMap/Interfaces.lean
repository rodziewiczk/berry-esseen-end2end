import BEMap.Domain
import BEMap.Cover25

noncomputable section
namespace BEMap

/-- Lower-rho n25 allowance for the very same law. The global predecessor
license bounds the score of any law at index 24, even if it is not extremal. -/
theorem same_law_n25_allowance (X : StandardizedLaw)
    (h : PredecessorLicense optimalConstant esseenConstant) :
    25 * max (X.normalizedScore 24 - esseenConstant) 0 ≤ 5 / 16 := by
  have hglobal := n25_allowance h
  have hscore := normalizedScore_le_optimalConstant X 24
  have hm := max_le_max_right 0 (sub_le_sub_right hscore esseenConstant)
  have hscaled := mul_le_mul_of_nonneg_left hm (by norm_num : (0 : ℝ) ≤ 25)
  exact hscaled.trans hglobal

/-- All 20 n25 domains must be rejected for the original oriented contact.
There is no assumption restricting the law to a three-atom family. -/
theorem n25_upper_of_regions (extract : ContactExtraction)
    (hmid : ∀ w : ContraryContact 25, MiddleEnvelope25 w.X.rho w.X.beta)
    (hhigh : ∀ w : ContraryContact 25, HighEnvelope25 w.X.rho w.X.beta)
    (reject : ∀ region : Region25, ∀ w : ContraryContact 25,
      region.contains w.X.rho w.X.beta → False) :
    optimalConstant 25 ≤ esseenConstant := by
  apply upper_of_contact_exclusion extract (by norm_num)
  exact n25_exclude_by_cover (fun w : ContraryContact 25 => w.X.rho)
    (fun w : ContraryContact 25 => w.X.beta) (fun w => w.X.rho_ge_one)
    hmid hhigh reject

end BEMap
