import BEMap.Physical

/-! Coherent complete Fourier evidence. LOW and HIGH use the same contact,
raw threshold, characteristic function, remainder and positive split. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def characteristic (X : StandardizedLaw) (t : ℝ) : ℂ :=
  ∫ x : ℝ, Complex.exp (Complex.I * ((t * x : ℝ) : ℂ)) ∂(X.law : Measure ℝ)

def compensatedRemainder (X : StandardizedLaw) (n : ℕ) (t : ℝ) : ℂ :=
  characteristic X t ^ n - (Real.exp (-(n : ℝ) * t ^ 2 / 2) : ℂ) *
    (1 - Complex.I * (((n : ℝ) * X.gamma * t ^ 3 / 6 : ℝ) : ℂ))

def lowIntegrand {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (t : ℝ) : ℝ :=
  |(Complex.exp (-Complex.I * ((t * w.rawThreshold.value : ℝ) : ℂ)) *
    compensatedRemainder w.X n t).im| / t ^ 3

def highIntegrand {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (t : ℝ) : ℝ :=
  ‖compensatedRemainder w.X n t‖ / t ^ 3

structure FrequencySplit where
  value : ℚ
  positive : 0 < value

def lowIntegral {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (b : FrequencySplit) : ℝ :=
  ∫ t in Ioo 0 (b.value : ℝ), lowIntegrand w t
def highIntegral {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (b : FrequencySplit) : ℝ :=
  ∫ t in Ioi (b.value : ℝ), highIntegrand w t

structure LowBound {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (b : FrequencySplit) where
  constant : ℚ
  threshold : ℚ
  secondary : ℚ
  constant_nonneg : 0 ≤ constant
  threshold_nonneg : 0 ≤ threshold
  secondary_nonneg : 0 ≤ secondary
  integrable : IntegrableOn (lowIntegrand w) (Ioo 0 (b.value : ℝ))
  bound : lowIntegral w b ≤
    ((constant : ℝ) + (threshold : ℝ) * |w.rawThreshold.value|) / Real.sqrt n +
      (secondary : ℝ) / (n : ℝ)

def LowBound.value {n : ℕ} {floor : ℝ} {w : ContactAt n floor} {b : FrequencySplit}
    (l : LowBound w b) : ℝ :=
  ((l.constant : ℝ) + (l.threshold : ℝ) * |w.rawThreshold.value|) / Real.sqrt n +
    (l.secondary : ℝ) / (n : ℝ)

structure HighBound {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (b : FrequencySplit) where
  value : ℚ
  nonneg : 0 ≤ value
  integrable : IntegrableOn (highIntegrand w) (Ioi (b.value : ℝ))
  bound : highIntegral w b ≤ (value : ℝ)

/-- The inversion/error theorem is an explicit analytic input. The two
integrability fields rule out accepting a totalized nonintegrable integral. -/
structure CompleteFourierEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  split : FrequencySplit
  low : LowBound w split
  high : HighBound w split
  normalized_hinge_integrable : Integrable (hinge w.threshold.value)
    (ProbabilityLaw.normalizedSum w.X.law n : Measure ℝ)
  normal_hinge_integrable : Integrable (hinge w.threshold.value)
    (ProbabilityLaw.standardNormal : Measure ℝ)
  inversion_bound : |physicalError w| ≤
    2 * Real.sqrt n / Real.pi * (lowIntegral w split + highIntegral w split)

theorem CompleteFourierEvidence.error_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (f : CompleteFourierEvidence w) :
    |physicalError w| ≤ 2 * Real.sqrt n / Real.pi * (f.low.value + (f.high.value : ℝ)) := by
  have hcoef : 0 ≤ 2 * Real.sqrt n / Real.pi := by positivity [Real.pi_pos]
  exact f.inversion_bound.trans
    (mul_le_mul_of_nonneg_left (add_le_add f.low.bound f.high.bound) hcoef)

end BEMap
