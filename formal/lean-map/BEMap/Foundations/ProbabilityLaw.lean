import Mathlib.MeasureTheory.Group.Convolution
import Mathlib.MeasureTheory.Group.IntegralConvolution
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Probability.CDF
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Moments.Basic

/-!
# Probability-law model for iid normalized sums

The extremal constants depend only on the common law.  We therefore work
with probability measures on `ℝ` and construct the law of a sum by repeated
additive convolution.  This avoids choosing an auxiliary sample space or a
particular iid realization.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped MeasureTheory

namespace BEMap

/-- A real probability distribution, bundled with its mass-one proof. -/
abbrev ProbabilityLaw := MeasureTheory.ProbabilityMeasure ℝ

namespace ProbabilityLaw

/-- Additive convolution of two probability laws. -/
def conv (μ ν : ProbabilityLaw) : ProbabilityLaw :=
  ⟨(μ : Measure ℝ) ∗ (ν : Measure ℝ), inferInstance⟩

@[simp] theorem coe_conv (μ ν : ProbabilityLaw) :
    ((conv μ ν : ProbabilityLaw) : Measure ℝ) = (μ : Measure ℝ) ∗ (ν : Measure ℝ) := rfl

/-- Law of a sum of `n` independent variables with common law `μ`. -/
def convolutionPow (μ : ProbabilityLaw) : ℕ → ProbabilityLaw
  | 0 => ⟨Measure.dirac 0, Measure.dirac.isProbabilityMeasure⟩
  | n + 1 => conv (convolutionPow μ n) μ

@[simp] theorem convolutionPow_zero (μ : ProbabilityLaw) :
    convolutionPow μ 0 = ⟨Measure.dirac 0, Measure.dirac.isProbabilityMeasure⟩ := rfl

@[simp] theorem convolutionPow_succ (μ : ProbabilityLaw) (n : ℕ) :
    convolutionPow μ (n + 1) = conv (convolutionPow μ n) μ := rfl

/-- Law of `(X₁ + ... + Xₙ) / √n` for iid variables with common law `μ`.
For `n = 0` this is the point mass at zero. -/
def normalizedSum (μ : ProbabilityLaw) (n : ℕ) : ProbabilityLaw :=
  (convolutionPow μ n).map (by fun_prop :
    AEMeasurable (fun x : ℝ => x / Real.sqrt n) (convolutionPow μ n))

/-- Cumulative distribution function of a bundled probability law. -/
def cdf (μ : ProbabilityLaw) (x : ℝ) : ℝ := ProbabilityTheory.cdf (μ : Measure ℝ) x

/-- Kolmogorov distance between two real probability laws. -/
def kolmogorovDistance (μ ν : ProbabilityLaw) : ℝ :=
  sSup (Set.range fun x : ℝ => |cdf μ x - cdf ν x|)

/-- The standard Gaussian law. -/
def standardNormal : ProbabilityLaw := ⟨gaussianReal 0 1, inferInstance⟩

/-- Kolmogorov distance between the normalized iid sum and the standard Gaussian. -/
def iidKolmogorovDistance (μ : ProbabilityLaw) (n : ℕ) : ℝ :=
  kolmogorovDistance (normalizedSum μ n) standardNormal

end ProbabilityLaw

/-- A centered, variance-one probability law with finite third absolute moment. -/
structure StandardizedLaw where
  law : ProbabilityLaw
  integrable_absCube : Integrable (fun x : ℝ => |x| ^ 3) (law : Measure ℝ)
  mean_zero : ∫ x : ℝ, x ∂(law : Measure ℝ) = 0
  secondMoment_one : ∫ x : ℝ, x ^ 2 ∂(law : Measure ℝ) = 1

namespace StandardizedLaw

theorem integrable_cube (X : StandardizedLaw) :
    Integrable (fun x : ℝ => x ^ 3) (X.law : Measure ℝ) := by
  apply (integrable_norm_iff (by fun_prop)).mp
  simpa only [Real.norm_eq_abs, abs_pow] using X.integrable_absCube

private theorem abs_sq_le_one_add_abs_cube (x : ℝ) :
    |x| ^ 2 ≤ 1 + |x| ^ 3 := by
  by_cases hx : |x| ≤ 1
  · nlinarith [abs_nonneg x, sq_nonneg |x|]
  · have hone : 1 ≤ |x| := (lt_of_not_ge hx).le
    have hcube : |x| ^ 2 ≤ |x| ^ 3 := by
      calc
        |x| ^ 2 = |x| ^ 2 * 1 := by ring
        _ ≤ |x| ^ 2 * |x| := mul_le_mul_of_nonneg_left hone (sq_nonneg |x|)
        _ = |x| ^ 3 := by ring
    linarith

private theorem abs_le_one_add_abs_cube (x : ℝ) :
    |x| ≤ 1 + |x| ^ 3 := by
  by_cases hx : |x| ≤ 1
  · have hc : 0 ≤ |x| ^ 3 := by positivity
    linarith
  · have hone : 1 ≤ |x| := (lt_of_not_ge hx).le
    have hcubic : |x| ≤ |x| ^ 3 := by
      calc
        |x| = |x| * 1 := by ring
        _ ≤ |x| * |x| ^ 2 := by
          gcongr
          nlinarith [sq_nonneg (|x| - 1)]
        _ = |x| ^ 3 := by ring
    linarith

theorem integrable_sq (X : StandardizedLaw) :
    Integrable (fun x : ℝ => x ^ 2) (X.law : Measure ℝ) := by
  have hdom : Integrable (fun x : ℝ => 1 + |x| ^ 3) (X.law : Measure ℝ) :=
    (integrable_const (1 : ℝ)).add X.integrable_absCube
  refine hdom.mono' (by fun_prop) (ae_of_all _ fun x => ?_)
  simpa only [Real.norm_eq_abs, abs_pow] using abs_sq_le_one_add_abs_cube x

theorem integrable_id (X : StandardizedLaw) :
    Integrable (fun x : ℝ => x) (X.law : Measure ℝ) := by
  have hdom : Integrable (fun x : ℝ => 1 + |x| ^ 3) (X.law : Measure ℝ) :=
    (integrable_const (1 : ℝ)).add X.integrable_absCube
  refine hdom.mono' (by fun_prop) (ae_of_all _ fun x => ?_)
  simpa only [Real.norm_eq_abs] using abs_le_one_add_abs_cube x

def gamma (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, x ^ 3 ∂(X.law : Measure ℝ)

def rho (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, |x| ^ 3 ∂(X.law : Measure ℝ)

def iidKolmogorovDistance (X : StandardizedLaw) (n : ℕ) : ℝ :=
  ProbabilityLaw.iidKolmogorovDistance X.law n

def normalizedScore (X : StandardizedLaw) (n : ℕ) : ℝ :=
  Real.sqrt n * X.iidKolmogorovDistance n / X.rho

end StandardizedLaw

/-- The optimal fixed-`n` iid Berry--Esseen constant. -/
def optimalConstant (n : ℕ) : ℝ :=
  sSup (Set.range fun X : StandardizedLaw => X.normalizedScore n)

end BEMap
