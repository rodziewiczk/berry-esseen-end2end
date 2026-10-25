import BEMap.Root4
import BEMap.FourierFamilies
import BEMap.Certificates

/-! Contract regression checks. These exercise the type/strictness failures
which would silently change a mathematical argument if allowed to elaborate.
They are not numerical acceptance tests and do not formalize the analysis. -/
noncomputable section
namespace BEMap

-- Expected failures refer to variables during elaboration but leave no
-- reference in the successful True proof, so the ordinary unused-variable
-- linter is intentionally disabled only in this regression-check module.
set_option linter.unusedVariables false

/-- A weak ROOT4 certificate at exactly T is admissible, with no margin. -/
example (w : ContactAt 4 bound4)
    (h : w.X.normalizedScore 4 ≤ (4097 / 10000 : ℝ)) : ScoreCap w (4097 / 10000) := by
  refine ⟨?_⟩
  norm_num at h ⊢
  exact h

/-- A strict failure may lie between two distinct targets. Extraction only
at the higher target cannot serve as the lower target's contrary argument. -/
example (lower higher : ℝ) (h : lower < higher) :
    ∃ score : ℝ, lower < score ∧ score < higher := by
  exact ⟨(lower + higher) / 2, by constructor <;> linarith⟩

example (h : RawThreshold) : True := by
  fail_if_success have _ : NormalizedThreshold := h
  trivial

example {n : ℕ} {floor : ℝ} (w₁ w₂ : ContactAt n floor) (cap : ℚ)
    (h : ScoreCap w₁ cap) : True := by
  fail_if_success have _ : ScoreCap w₂ cap := h
  trivial

example (w : ContactAt 4 bound4) : True := by
  fail_if_success have _ : ContraryContact 4 := w
  trivial

example (X : StandardizedLaw) (cap : ℚ) (h : UnweightedDefectCap X cap) : True := by
  fail_if_success have _ : WeightedDefectCap X 34 31 cap := h
  trivial

example (X : StandardizedLaw) (cap : ℚ) (h : NoiseCap X cap) : True := by
  fail_if_success have _ : WeightedNoiseCap X 25 cap := h
  trivial

example (X : StandardizedLaw) (cap : ℚ) (h : WeightedNoiseCap X 25 cap) : True := by
  fail_if_success have _ : WeightedNoiseCap X 24 cap := h
  trivial

example {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (b₁ b₂ : FrequencySplit)
    (h : LowBound w b₁) : True := by
  fail_if_success have _ : LowBound w b₂ := h
  trivial

example {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (cap : ℚ)
    (h : ScoreCap w cap) : True := by
  fail_if_success have _ : StrictScoreBound w := h
  trivial

example (b kappa : ℚ) (e : GaussianTailEvidence 0 b kappa) : False := by
  exact (Nat.not_lt_zero 0) e.positive_index

example (n : ℕ) (b : ℚ) (e : GaussianTailEvidence n b (-1)) : False := by
  have h := e.kappa_positive
  norm_num at h

example {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (accepted : Bool)
    (pass : accepted = true) : True := by
  fail_if_success have _ : ScoreCap w 0 := pass
  trivial

/-- A marginal contraction cannot replace an acquired joint intercept. -/
example : ((1 / 2 : ℝ) / 1 + 1 / 2 ≤ 1) ∧ (1 : ℝ) ≤ 1 ∧
    ¬ ((1 / 2 : ℝ) / 1 + 1 / 1 ≤ 1) := by norm_num

/-- The fifth count coordinate a0 is only one part of total inward dY. -/
example (p h A B : ℝ) : (p - h * A) + ((1 - p) - h * B) = 1 - h * (A + B) := by ring

end BEMap
