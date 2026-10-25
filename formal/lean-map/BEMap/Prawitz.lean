import BEMap.Fourier

/-! Complete four-term Prawitz score semantics, separate from the physical hinge ledger. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

structure PrawitzParameters where
  scale : ℚ
  scale_positive : 0 < scale
  split : ℚ
  split_positive : 0 < split
  split_below_one : split < 1

def prawitzK (t : ℝ) : ℂ :=
  ((1 - t : ℝ) : ℂ) + Complex.I *
    (((1 - t) * Real.cos (Real.pi * t) / Real.sin (Real.pi * t) + 1 / Real.pi : ℝ) : ℂ)

def prawitzGaussian (n : ℕ) (p : PrawitzParameters) (t : ℝ) : ℝ :=
  Real.exp (-(n : ℝ) * ((p.scale : ℝ) * t) ^ 2 / 2)

def prawitzFirst {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (p : PrawitzParameters) (t : ℝ) : ℝ :=
  ‖prawitzK t‖ * ‖characteristic w.X ((p.scale : ℝ) * t) ^ n - (prawitzGaussian n p t : ℂ)‖
def prawitzSecond {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (p : PrawitzParameters) (t : ℝ) : ℝ :=
  ‖prawitzK t‖ * ‖characteristic w.X ((p.scale : ℝ) * t)‖ ^ n
def prawitzThird (n : ℕ) (p : PrawitzParameters) (t : ℝ) : ℝ :=
  ‖prawitzK t - Complex.I / ((Real.pi * t : ℝ) : ℂ)‖ * prawitzGaussian n p t
def prawitzFourth (n : ℕ) (p : PrawitzParameters) (t : ℝ) : ℝ :=
  prawitzGaussian n p t / (Real.pi * t)

def prawitzIntegral1 {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (p : PrawitzParameters) : ℝ :=
  ∫ t in Ioo 0 (p.split : ℝ), prawitzFirst w p t
def prawitzIntegral2 {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (p : PrawitzParameters) : ℝ :=
  ∫ t in Ioo (p.split : ℝ) 1, prawitzSecond w p t
def prawitzIntegral3 (n : ℕ) (p : PrawitzParameters) : ℝ :=
  ∫ t in Ioo 0 (p.split : ℝ), prawitzThird n p t
def prawitzIntegral4 (n : ℕ) (p : PrawitzParameters) : ℝ :=
  ∫ t in Ioi (p.split : ℝ), prawitzFourth n p t

/-- The n5 supported Fourier complement uses this FOUR-TERM Prawitz
inequality, not CompleteFourierEvidence's compensated-hinge error ledger. -/
structure PrawitzScoreEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  support : SupportedContact w
  parameters : PrawitzParameters
  firstUpper : ℚ
  secondUpper : ℚ
  thirdUpper : ℚ
  fourthUpper : ℚ
  uppers_nonnegative : 0 ≤ firstUpper ∧ 0 ≤ secondUpper ∧ 0 ≤ thirdUpper ∧ 0 ≤ fourthUpper
  first_integrable : IntegrableOn (prawitzFirst w parameters) (Ioo 0 (parameters.split : ℝ))
  second_integrable : IntegrableOn (prawitzSecond w parameters) (Ioo (parameters.split : ℝ) 1)
  third_integrable : IntegrableOn (prawitzThird n parameters) (Ioo 0 (parameters.split : ℝ))
  fourth_integrable : IntegrableOn (prawitzFourth n parameters) (Ioi (parameters.split : ℝ))
  first_bound : prawitzIntegral1 w parameters ≤ (firstUpper : ℝ)
  second_bound : prawitzIntegral2 w parameters ≤ (secondUpper : ℝ)
  third_bound : prawitzIntegral3 n parameters ≤ (thirdUpper : ℝ)
  fourth_bound : prawitzIntegral4 n parameters ≤ (fourthUpper : ℝ)
  smoothing : w.X.iidKolmogorovDistance n ≤ prawitzIntegral1 w parameters +
    prawitzIntegral2 w parameters + prawitzIntegral3 n parameters + prawitzIntegral4 n parameters
  sqrtUpper : ℚ
  sqrt_bound : Real.sqrt n ≤ (sqrtUpper : ℝ)
  rhoLower : ℚ
  rho_positive : 0 < rhoLower
  rho_bound : (rhoLower : ℝ) ≤ w.X.rho
  target_comparison : (sqrtUpper : ℝ) / (rhoLower : ℝ) *
    ((firstUpper : ℝ) + secondUpper + thirdUpper + fourthUpper) ≤ floor

theorem PrawitzScoreEvidence.score_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (e : PrawitzScoreEvidence w) : w.X.normalizedScore n ≤ floor := by
  have hd : w.X.iidKolmogorovDistance n ≤
      (e.firstUpper : ℝ) + e.secondUpper + e.thirdUpper + e.fourthUpper := by
    linarith [e.smoothing, e.first_bound, e.second_bound, e.third_bound, e.fourth_bound]
  have hs : (0 : ℝ) ≤ e.sqrtUpper := (Real.sqrt_nonneg n).trans e.sqrt_bound
  have hr : (0 : ℝ) < e.rhoLower := by exact_mod_cast e.rho_positive
  have hsum : 0 ≤ (e.firstUpper : ℝ) + e.secondUpper + e.thirdUpper + e.fourthUpper :=
    (w.X.iidKolmogorovDistance_nonneg n).trans hd
  have hm := mul_le_mul e.sqrt_bound hd (w.X.iidKolmogorovDistance_nonneg n) hs
  have hdiv := (div_le_div_of_nonneg_right hm w.X.rho_nonneg).trans
    (div_le_div_of_nonneg_left (mul_nonneg hs hsum) hr e.rho_bound)
  calc
    w.X.normalizedScore n = Real.sqrt n * w.X.iidKolmogorovDistance n / w.X.rho := rfl
    _ ≤ ((e.sqrtUpper : ℝ) * ((e.firstUpper : ℝ) + e.secondUpper + e.thirdUpper + e.fourthUpper)) /
        (e.rhoLower : ℝ) := hdiv
    _ = (e.sqrtUpper : ℝ) / (e.rhoLower : ℝ) *
        ((e.firstUpper : ℝ) + e.secondUpper + e.thirdUpper + e.fourthUpper) := by ring
    _ ≤ floor := e.target_comparison

end BEMap
