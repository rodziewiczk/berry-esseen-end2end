import BEMap.Fourier

/-! Source-specific constructors. A generic LOW/HIGH semantic result does not
license every source formula. Each named family carries its own exact gates.
Source: rescore:lem:finite-low and HIGH_LAGUERRE2 in the pinned manuscript. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def halfFrequencySplit : FrequencySplit := ⟨1 / 2, by norm_num⟩
def signedFifthMoment (X : StandardizedLaw) : ℝ := ∫ x : ℝ, x ^ 5 ∂(X.law : Measure ℝ)
def finiteGaussianIntegral (j : ℕ) (A : ℝ) : ℝ :=
  ∫ t in Icc (0 : ℝ) (1 / 2), t ^ j * Real.exp (-A * t ^ 2)

structure FiniteWindowLowInputs {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (s : SupportedContact w) where
  index_gt_two : 2 < n
  radius_lower : (1 : ℚ) ≤ s.radius
  radius_upper : s.radius ≤ 6
  moments : HigherMomentEvidence s
  M : ℚ
  gammaUpper : ℚ
  gammaLower : ℚ
  fifthUpper : ℚ
  A : ℚ
  Z : ℚ
  fourth_bound : fourthMoment w.X ≤ (M : ℝ)
  M_upper : M ≤ 111 / 10
  gamma_bound : |w.X.gamma| ≤ (gammaUpper : ℝ)
  gamma_upper_gate : gammaUpper ≤ 37 / 20
  gamma_lower_nonneg : 0 ≤ gammaLower
  gamma_lower_bound : (gammaLower : ℝ) ≤ |w.X.gamma|
  pearson_gate : gammaLower ^ 2 ≤ M - 1
  fifth_bound : absoluteFifthMoment w.X ≤ (fifthUpper : ℝ)
  fifth_nonneg : 0 ≤ fifthUpper
  A_nonneg : 0 ≤ A
  A_bound : |(3 - fourthMoment w.X) / 24| ≤ (A : ℝ)
  Z_nonneg : 0 ≤ Z
  Z_bound : |(10 * w.X.gamma - signedFifthMoment w.X) / 120| ≤ (Z : ℝ)

def FiniteWindowLowInputs.sixthUpper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  min ((s.radius : ℝ) * (i.fifthUpper : ℝ))
    (1 + 3 * (i.gammaUpper : ℝ) ^ 2 + (i.gammaUpper : ℝ) ^ 4 +
      ((s.radius : ℝ) ^ 2 + 2 * (s.radius : ℝ) * (i.gammaUpper : ℝ) +
        3 * (i.gammaUpper : ℝ) ^ 2 + 2) *
          ((i.M : ℝ) - 1 - (i.gammaLower : ℝ) ^ 2))

def FiniteWindowLowInputs.errorCoefficient {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  i.sixthUpper / 720 + (i.gammaUpper : ℝ) ^ 2 / 72 +
    (1 / 2 + (i.gammaUpper : ℝ) ^ 2 / 144) ^ 3 / 5

def FiniteWindowLowInputs.remainderCoefficient {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  (i.A : ℝ) + (i.Z : ℝ) / 2 + i.errorCoefficient / 4

def FiniteWindowLowInputs.L0 {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  Real.sqrt n * ((n : ℝ) * i.Z * finiteGaussianIntegral 2 (((n : ℝ) - 1) / 2) +
    (n : ℝ) * ((n : ℝ) - 1) * i.A * i.gammaUpper / 6 *
      finiteGaussianIntegral 4 (((n : ℝ) - 1) / 2) +
    (n : ℝ) ^ 3 * (i.gammaUpper : ℝ) ^ 3 / 1296 * finiteGaussianIntegral 6 ((n : ℝ) / 2))

def FiniteWindowLowInputs.LH {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  Real.sqrt n * ((n : ℝ) * i.A * finiteGaussianIntegral 2 (((n : ℝ) - 1) / 2) +
    (n : ℝ) ^ 2 * (i.gammaUpper : ℝ) ^ 2 / 72 * finiteGaussianIntegral 4 ((n : ℝ) / 2))

def FiniteWindowLowInputs.L2 {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) : ℝ :=
  (n : ℝ) * ((n : ℝ) * i.errorCoefficient * finiteGaussianIntegral 3 (((n : ℝ) - 1) / 2) +
    (n : ℝ) * ((n : ℝ) - 1) * i.remainderCoefficient ^ 2 / 2 *
      finiteGaussianIntegral 5 (((n : ℝ) - 2) * (45 - (i.M : ℝ)) / 96))

/-- Accepted analytic theorem, stated exactly at split b=1/2. It is a
parameter, not a project axiom or a claim that this analysis was formalized. -/
def FiniteWindowLowTheorem : Prop :=
  ∀ (n : ℕ) (floor : ℝ) (w : ContactAt n floor) (s : SupportedContact w)
    (i : FiniteWindowLowInputs w s),
    IntegrableOn (lowIntegrand w) (Ioo 0 (halfFrequencySplit.value : ℝ)) ∧
    lowIntegral w halfFrequencySplit ≤
      (i.L0 + i.LH * |w.rawThreshold.value|) / Real.sqrt n + i.L2 / (n : ℝ)

/-- One rational enclosure of the ENTIRE triple. Three components from
different strategies must not be assembled under this constructor. -/
structure FiniteWindowLowRounding {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (i : FiniteWindowLowInputs w s) where
  constant : ℚ
  threshold : ℚ
  secondary : ℚ
  nonneg : 0 ≤ constant ∧ 0 ≤ threshold ∧ 0 ≤ secondary
  bounds : i.L0 ≤ (constant : ℝ) ∧ i.LH ≤ (threshold : ℝ) ∧ i.L2 ≤ (secondary : ℝ)

def finite_window_low {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {s : SupportedContact w} (analytic : FiniteWindowLowTheorem)
    (i : FiniteWindowLowInputs w s) (r : FiniteWindowLowRounding i) :
    LowBound w halfFrequencySplit where
  constant := r.constant
  threshold := r.threshold
  secondary := r.secondary
  constant_nonneg := r.nonneg.1
  threshold_nonneg := r.nonneg.2.1
  secondary_nonneg := r.nonneg.2.2
  integrable := (analytic n floor w s i).1
  bound := by
    apply (analytic n floor w s i).2.trans
    apply add_le_add
    · apply div_le_div_of_nonneg_right _ (Real.sqrt_nonneg _)
      exact add_le_add r.bounds.1 (mul_le_mul_of_nonneg_right r.bounds.2.1 (abs_nonneg _))
    · exact div_le_div_of_nonneg_right r.bounds.2.2 (Nat.cast_nonneg n)

def gaussianTailIntegrand (n : ℕ) (kappa t : ℝ) : ℝ :=
  Real.exp (-(n : ℝ) * kappa * t ^ 2) / t ^ 3
def laguerre2Upper (n : ℕ) (b kappa : ℝ) : ℝ :=
  let x := (n : ℝ) * kappa * b ^ 2
  Real.sqrt n * Real.exp (-x) / (2 * b ^ 2) * (x + 2) / (x ^ 2 + 4 * x + 2)

def Laguerre2Theorem : Prop :=
  ∀ (n : ℕ) (b kappa : ℝ), 0 < n → 0 < b → 0 < kappa →
    IntegrableOn (gaussianTailIntegrand n kappa) (Ioi b) ∧
    Real.sqrt n * (∫ t in Ioi b, gaussianTailIntegrand n kappa t) ≤ laguerre2Upper n b kappa

/-- Uniform reuse is separately gated; pointwise Laguerre2 does not imply
monotonicity on an arbitrary index band. -/
structure Laguerre2UniformInputs where
  lowerIndex : ℕ
  positive_index : 0 < lowerIndex
  split : FrequencySplit
  kappa : ℚ
  kappa_pos : 0 < kappa
  monotonicity_gate : (1 / 4 : ℝ) ≤ (lowerIndex : ℝ) * (kappa : ℝ) * (split.value : ℝ) ^ 2

def Laguerre2UniformTheorem : Prop :=
  ∀ i : Laguerre2UniformInputs, ∀ n : ℕ, i.lowerIndex ≤ n →
    laguerre2Upper n i.split.value i.kappa ≤
      laguerre2Upper i.lowerIndex i.split.value i.kappa

/-- This scalar Gaussian-tail theorem is NOT a complete HighBound for V_n.
No coercion or conversion between those types is provided. A complete HIGH
family must also cover the actual law contribution and compensation terms. -/
structure GaussianTailEvidence (n : ℕ) (b kappa : ℚ) where
  positive_index : 0 < n
  split_positive : 0 < b
  kappa_positive : 0 < kappa
  bound : ℚ
  integrable : IntegrableOn (gaussianTailIntegrand n kappa) (Ioi (b : ℝ))
  integral_bound : Real.sqrt n * (∫ t in Ioi (b : ℝ), gaussianTailIntegrand n kappa t) ≤ (bound : ℝ)

def laguerre2_gaussian_tail (analytic : Laguerre2Theorem) (n : ℕ) (b kappa upper : ℚ)
    (hn : 0 < n) (hb : 0 < b) (hk : 0 < kappa)
    (rounding : laguerre2Upper n b kappa ≤ (upper : ℝ)) : GaussianTailEvidence n b kappa where
  positive_index := hn
  split_positive := hb
  kappa_positive := hk
  bound := upper
  integrable := (analytic n b kappa hn (by exact_mod_cast hb) (by exact_mod_cast hk)).1
  integral_bound :=
    ((analytic n b kappa hn (by exact_mod_cast hb) (by exact_mod_cast hk)).2).trans rounding

end BEMap
