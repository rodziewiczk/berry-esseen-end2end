import BEMap.Foundations.ProbabilityLaw

/-!
# Elementary bounds for the optimal iid constant

This file supplies the order-theoretic API needed to use the conditional
supremum in `optimalConstant`.  In particular, the defining set is nonempty
and bounded above, so every application of `le_csSup` and `csSup_le` below
carries the hypotheses required by the conditionally complete order on `ℝ`.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal Topology

namespace BEMap

namespace ProbabilityLaw

/-- The CDF of a probability law is nonnegative. -/
theorem cdf_nonneg (μ : ProbabilityLaw) (x : ℝ) : 0 ≤ μ.cdf x := by
  exact ProbabilityTheory.cdf_nonneg (μ : Measure ℝ) x

/-- The CDF of a probability law is at most one. -/
theorem cdf_le_one (μ : ProbabilityLaw) (x : ℝ) : μ.cdf x ≤ 1 := by
  exact ProbabilityTheory.cdf_le_one (μ : Measure ℝ) x

/-- The CDF of a probability law takes values in the unit interval. -/
theorem cdf_mem_Icc (μ : ProbabilityLaw) (x : ℝ) :
    μ.cdf x ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨cdf_nonneg μ x, cdf_le_one μ x⟩

/-- The pointwise absolute difference of two CDFs is at most one. -/
theorem abs_cdf_sub_le_one (μ ν : ProbabilityLaw) (x : ℝ) :
    |μ.cdf x - ν.cdf x| ≤ 1 := by
  rw [abs_le]
  constructor
  · linarith [cdf_nonneg μ x, cdf_le_one ν x]
  · linarith [cdf_le_one μ x, cdf_nonneg ν x]

/-- The range used in the definition of Kolmogorov distance is bounded above. -/
theorem kolmogorovDistance_bddAbove (μ ν : ProbabilityLaw) :
    BddAbove (Set.range fun x : ℝ => |μ.cdf x - ν.cdf x|) := by
  refine ⟨1, ?_⟩
  rintro y ⟨x, rfl⟩
  exact abs_cdf_sub_le_one μ ν x

/-- Kolmogorov distance is nonnegative. -/
theorem kolmogorovDistance_nonneg (μ ν : ProbabilityLaw) :
    0 ≤ kolmogorovDistance μ ν := by
  calc
    0 ≤ |μ.cdf 0 - ν.cdf 0| := abs_nonneg _
    _ ≤ kolmogorovDistance μ ν := by
      apply le_csSup (kolmogorovDistance_bddAbove μ ν)
      exact Set.mem_range_self 0

/-- Kolmogorov distance between probability laws is at most one. -/
theorem kolmogorovDistance_le_one (μ ν : ProbabilityLaw) :
    kolmogorovDistance μ ν ≤ 1 := by
  apply csSup_le (Set.range_nonempty _)
  rintro y ⟨x, rfl⟩
  exact abs_cdf_sub_le_one μ ν x

/-- Kolmogorov distance between probability laws belongs to `[0,1]`. -/
theorem kolmogorovDistance_mem_Icc (μ ν : ProbabilityLaw) :
    kolmogorovDistance μ ν ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨kolmogorovDistance_nonneg μ ν, kolmogorovDistance_le_one μ ν⟩

/-- The iid Kolmogorov error is nonnegative. -/
theorem iidKolmogorovDistance_nonneg (μ : ProbabilityLaw) (n : ℕ) :
    0 ≤ μ.iidKolmogorovDistance n := by
  exact kolmogorovDistance_nonneg _ _

/-- The iid Kolmogorov error is at most one. -/
theorem iidKolmogorovDistance_le_one (μ : ProbabilityLaw) (n : ℕ) :
    μ.iidKolmogorovDistance n ≤ 1 := by
  exact kolmogorovDistance_le_one _ _

/-- The iid Kolmogorov error belongs to `[0,1]`. -/
theorem iidKolmogorovDistance_mem_Icc (μ : ProbabilityLaw) (n : ℕ) :
    μ.iidKolmogorovDistance n ∈ Set.Icc (0 : ℝ) 1 :=
  ⟨iidKolmogorovDistance_nonneg μ n, iidKolmogorovDistance_le_one μ n⟩

end ProbabilityLaw

private theorem three_mul_sq_le_two_mul_abs_cube_add_one (x : ℝ) :
    3 * x ^ 2 ≤ 2 * |x| ^ 3 + 1 := by
  have hnonneg : 0 ≤ 2 * |x| + 1 := by positivity
  have hfactor : 0 ≤ (|x| - 1) ^ 2 * (2 * |x| + 1) :=
    mul_nonneg (sq_nonneg _) hnonneg
  nlinarith [sq_abs x]

namespace StandardizedLaw

/-- For a centered variance-one law, the third absolute moment is at least one. -/
theorem rho_ge_one (X : StandardizedLaw) : 1 ≤ X.rho := by
  have hleft : Integrable (fun x : ℝ => 3 * x ^ 2) (X.law : Measure ℝ) :=
    X.integrable_sq.const_mul 3
  have hcubic : Integrable (fun x : ℝ => 2 * |x| ^ 3) (X.law : Measure ℝ) :=
    X.integrable_absCube.const_mul 2
  have hone : Integrable (fun _ : ℝ => (1 : ℝ)) (X.law : Measure ℝ) :=
    integrable_const 1
  have hright : Integrable (fun x : ℝ => 2 * |x| ^ 3 + 1) (X.law : Measure ℝ) :=
    hcubic.add hone
  have hint :
      (∫ x : ℝ, 3 * x ^ 2 ∂(X.law : Measure ℝ)) ≤
        ∫ x : ℝ, 2 * |x| ^ 3 + 1 ∂(X.law : Measure ℝ) :=
    integral_mono hleft hright three_mul_sq_le_two_mul_abs_cube_add_one
  rw [integral_const_mul, integral_add hcubic hone, integral_const_mul,
    integral_const, probReal_univ] at hint
  simp only [one_smul] at hint
  change 3 * (∫ x : ℝ, x ^ 2 ∂(X.law : Measure ℝ)) ≤ 2 * X.rho + 1 at hint
  rw [X.secondMoment_one] at hint
  linarith

/-- The third absolute moment of a standardized law is strictly positive. -/
theorem rho_pos (X : StandardizedLaw) : 0 < X.rho :=
  lt_of_lt_of_le zero_lt_one X.rho_ge_one

/-- The third absolute moment of a standardized law is nonnegative. -/
theorem rho_nonneg (X : StandardizedLaw) : 0 ≤ X.rho := X.rho_pos.le

/-- The iid Kolmogorov error of a standardized law is nonnegative. -/
theorem iidKolmogorovDistance_nonneg (X : StandardizedLaw) (n : ℕ) :
    0 ≤ X.iidKolmogorovDistance n := by
  exact ProbabilityLaw.iidKolmogorovDistance_nonneg X.law n

/-- The iid Kolmogorov error of a standardized law is at most one. -/
theorem iidKolmogorovDistance_le_one (X : StandardizedLaw) (n : ℕ) :
    X.iidKolmogorovDistance n ≤ 1 := by
  exact ProbabilityLaw.iidKolmogorovDistance_le_one X.law n

/-- Every normalized Berry--Esseen score is nonnegative. -/
theorem normalizedScore_nonneg (X : StandardizedLaw) (n : ℕ) :
    0 ≤ X.normalizedScore n := by
  unfold normalizedScore
  exact div_nonneg
    (mul_nonneg (Real.sqrt_nonneg _) (X.iidKolmogorovDistance_nonneg n))
    X.rho_nonneg

/-- The elementary universal bound on a normalized score. -/
theorem normalizedScore_le_sqrt (X : StandardizedLaw) (n : ℕ) :
    X.normalizedScore n ≤ Real.sqrt n := by
  unfold normalizedScore
  rw [div_le_iff₀ X.rho_pos]
  calc
    Real.sqrt n * X.iidKolmogorovDistance n ≤ Real.sqrt n * 1 :=
      mul_le_mul_of_nonneg_left (X.iidKolmogorovDistance_le_one n)
        (Real.sqrt_nonneg _)
    _ ≤ Real.sqrt n * X.rho :=
      mul_le_mul_of_nonneg_left X.rho_ge_one (Real.sqrt_nonneg _)

/-- Every normalized score belongs to `[0, √n]`. -/
theorem normalizedScore_mem_Icc (X : StandardizedLaw) (n : ℕ) :
    X.normalizedScore n ∈ Set.Icc (0 : ℝ) (Real.sqrt n) :=
  ⟨X.normalizedScore_nonneg n, X.normalizedScore_le_sqrt n⟩

end StandardizedLaw

/-- The standard Gaussian, packaged as a standardized law. -/
def standardNormalStandardized : StandardizedLaw where
  law := ProbabilityLaw.standardNormal
  integrable_absCube := by
    simpa only [ProbabilityLaw.standardNormal, ProbabilityMeasure.coe_mk,
      Real.norm_eq_abs, id_eq] using
      (memLp_id_gaussianReal
        (μ := (0 : ℝ)) (v := (1 : NNReal)) (3 : NNReal)).integrable_norm_pow
        (by norm_num : (3 : ℕ) ≠ 0)
  mean_zero := by
    simp [ProbabilityLaw.standardNormal]
  secondMoment_one := by
    have hv := variance_fun_id_gaussianReal (μ := (0 : ℝ)) (v := (1 : NNReal))
    rw [variance_eq_integral measurable_id'.aemeasurable] at hv
    simpa [ProbabilityLaw.standardNormal] using hv

instance : Nonempty StandardizedLaw := ⟨standardNormalStandardized⟩

/-- The set whose conditional supremum defines `optimalConstant n`. -/
def optimalScoreSet (n : ℕ) : Set ℝ :=
  Set.range fun X : StandardizedLaw => X.normalizedScore n

@[simp] theorem optimalConstant_eq_sSup_scoreSet (n : ℕ) :
    optimalConstant n = sSup (optimalScoreSet n) := rfl

/-- The defining score set is nonempty. -/
theorem optimalScoreSet_nonempty (n : ℕ) : (optimalScoreSet n).Nonempty := by
  exact Set.range_nonempty _

/-- The defining score set is bounded above by `√n`. -/
theorem optimalScoreSet_bddAbove (n : ℕ) : BddAbove (optimalScoreSet n) := by
  refine ⟨Real.sqrt n, ?_⟩
  rintro y ⟨X, rfl⟩
  exact X.normalizedScore_le_sqrt n

/-- Every admissible score is bounded by the optimal constant. -/
theorem normalizedScore_le_optimalConstant (X : StandardizedLaw) (n : ℕ) :
    X.normalizedScore n ≤ optimalConstant n := by
  rw [optimalConstant_eq_sSup_scoreSet]
  apply le_csSup (optimalScoreSet_bddAbove n)
  exact ⟨X, rfl⟩

/-- To bound the optimal constant, it suffices to bound every admissible score. -/
theorem optimalConstant_le_of_forall (n : ℕ) (c : ℝ)
    (h : ∀ X : StandardizedLaw, X.normalizedScore n ≤ c) :
    optimalConstant n ≤ c := by
  rw [optimalConstant_eq_sSup_scoreSet]
  apply csSup_le (optimalScoreSet_nonempty n)
  rintro y ⟨X, rfl⟩
  exact h X

/-- Universal-property characterization of an upper bound for `optimalConstant`. -/
theorem optimalConstant_le_iff (n : ℕ) (c : ℝ) :
    optimalConstant n ≤ c ↔
      ∀ X : StandardizedLaw, X.normalizedScore n ≤ c := by
  constructor
  · intro h X
    exact (normalizedScore_le_optimalConstant X n).trans h
  · exact optimalConstant_le_of_forall n c

/-- The optimal iid constant is nonnegative. -/
theorem optimalConstant_nonneg (n : ℕ) : 0 ≤ optimalConstant n :=
  (standardNormalStandardized.normalizedScore_nonneg n).trans
    (normalizedScore_le_optimalConstant standardNormalStandardized n)

/-- The elementary finite upper bound for the optimal iid constant. -/
theorem optimalConstant_le_sqrt (n : ℕ) : optimalConstant n ≤ Real.sqrt n :=
  optimalConstant_le_of_forall n (Real.sqrt n) fun X => X.normalizedScore_le_sqrt n

/-- The optimal iid constant belongs to `[0, √n]`. -/
theorem optimalConstant_mem_Icc (n : ℕ) :
    optimalConstant n ∈ Set.Icc (0 : ℝ) (Real.sqrt n) :=
  ⟨optimalConstant_nonneg n, optimalConstant_le_sqrt n⟩

end BEMap
