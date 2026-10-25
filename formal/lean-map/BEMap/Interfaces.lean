import BEMap.Foundations.OptimalConstant
import BEMap.Cover25

noncomputable section
open MeasureTheory

namespace BEMap

def esseenConstant : ℝ := (3 + Real.sqrt 10) / (6 * Real.sqrt (2 * Real.pi))

def StandardizedLaw.beta (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, x * |x| ∂(X.law : Measure ℝ)

def AlmostBounded (X : StandardizedLaw) (R : ℝ) : Prop :=
  ∀ᵐ x ∂(X.law : Measure ℝ), |x| ≤ R

/-- An unrestricted attained contact for the oriented law, using a CLOSED CDF.
The threshold is expressed in normalized-sum coordinates. Reflection, if used,
acts on the complete law before constructing this object. -/
structure ContraryContact (n : ℕ) where
  X : StandardizedLaw
  threshold : ℝ
  critical : esseenConstant ≤ X.normalizedScore n
  optimal : X.normalizedScore n = optimalConstant n
  positive_closed :
    ProbabilityLaw.cdf (ProbabilityLaw.normalizedSum X.law n) threshold -
      ProbabilityLaw.cdf ProbabilityLaw.standardNormal threshold =
        X.iidKolmogorovDistance n

/-- Attainment, orientation and unrestricted localization remain analytic work. -/
def ContactExtraction : Prop :=
  ∀ n, 1 ≤ n → esseenConstant ≤ optimalConstant n → Nonempty (ContraryContact n)

theorem upper_of_contact_exclusion (extract : ContactExtraction) {n : ℕ}
    (hn : 1 ≤ n) (reject : ∀ w : ContraryContact n, False) :
    optimalConstant n ≤ esseenConstant := by
  by_contra h
  obtain ⟨w⟩ := extract n hn (le_of_lt (lt_of_not_ge h))
  exact reject w

/-- An abstract mathematical interface, NOT an implemented certificate reader.
Each predicate must later be instantiated with the exact inequalities in the
mathematical contracts. Every stage concerns this one contact and this one n. -/
structure ContactPipeline (n : ℕ) where
  radius : ℝ
  High : ContraryContact n → Prop
  OwnCap : ContraryContact n → Prop
  Initial : ContraryContact n → Prop
  Resources : ContraryContact n → Prop
  compact : ∀ w : ContraryContact n, ∃ R, AlmostBounded w.X R
  support : ∀ w : ContraryContact n,
    (∃ R, AlmostBounded w.X R) → AlmostBounded w.X radius
  high : ∀ w : ContraryContact n, AlmostBounded w.X radius → High w
  ownCap : ∀ w : ContraryContact n, High w → OwnCap w
  initial : ∀ w : ContraryContact n,
    AlmostBounded w.X radius → OwnCap w → Initial w
  resources : ∀ w : ContraryContact n, Initial w → Resources w
  count : ∀ w : ContraryContact n, Resources w → False

theorem ContactPipeline.reject {n : ℕ} (p : ContactPipeline n)
    (w : ContraryContact n) : False := by
  have hs := p.support w (p.compact w)
  have hh := p.high w hs
  have ho := p.ownCap w hh
  have hi := p.initial w hs ho
  exact p.count w (p.resources w hi)

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
