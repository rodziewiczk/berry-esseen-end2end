import BEMap.Domain
import Mathlib.MeasureTheory.Measure.Support

/-! Actual contact, support-gap and conserved-budget semantics. Totalized
integrals/tsums are definitions only; integrability/summability is mandatory
evidence before the analytic interfaces can consume them. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def phi (x : ℝ) : ℝ := Real.exp (-x ^ 2 / 2) / Real.sqrt (2 * Real.pi)

def rawCDF {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow w.X.law n) w.rawThreshold.value

def contactPolynomial {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (y : ℝ) : ℝ :=
  let s := Real.sqrt n
  let H := w.rawThreshold.value
  let C := w.X.normalizedScore n
  let F := rawCDF w
  let d := phi w.threshold.value
  ((n : ℝ) * F + (H * d + C * w.X.rho) / (2 * s)
    - (s * d + 3 * C * w.X.beta / s) * y
    - (H * d + 3 * C * w.X.rho) * y ^ 2 / (2 * s)
    + (C / s) * |y| ^ 3) / (n : ℝ)

def previousCDF {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (y : ℝ) : ℝ :=
  ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow w.X.law (n - 1))
    (w.rawThreshold.value - y)

structure ContactMajorant {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : Prop where
  at_least_two : 2 ≤ n
  positive_score : 0 < w.X.normalizedScore n
  dominates : ∀ y : ℝ, previousCDF w y ≤ contactPolynomial w y
  touches : ∀ y ∈ (w.X.law : Measure ℝ).support,
    previousCDF w y = contactPolynomial w y

def fourthMoment (X : StandardizedLaw) : ℝ := ∫ x : ℝ, x ^ 4 ∂(X.law : Measure ℝ)
def absoluteFifthMoment (X : StandardizedLaw) : ℝ := ∫ x : ℝ, |x| ^ 5 ∂(X.law : Measure ℝ)
def signedAbsoluteFourth (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, x * |x| ^ 3 ∂(X.law : Measure ℝ)

structure HigherMomentEvidence {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (_support : SupportedContact w) : Prop where
  fourth : Integrable (fun x : ℝ => x ^ 4) (w.X.law : Measure ℝ)
  fifth : Integrable (fun x : ℝ => |x| ^ 5) (w.X.law : Measure ℝ)
  signedFourth : Integrable (fun x : ℝ => x * |x| ^ 3) (w.X.law : Measure ℝ)

/-- Endpoints in the actual closed support and an empty open interior specify
one bounded complementary component; arbitrary subgaps are not admitted. -/
def SupportGap (X : StandardizedLaw) :=
  {s : ℝ × ℝ // s.1 < s.2 ∧ s.1 ∈ (X.law : Measure ℝ).support ∧
    s.2 ∈ (X.law : Measure ℝ).support ∧
    ∀ x ∈ Ioo s.1 s.2, x ∉ (X.law : Measure ℝ).support}

def tau (X : StandardizedLaw) (t : ℝ) : ℝ := ∫ x in Ici t, x ∂(X.law : Measure ℝ)
def gapWeight {X : StandardizedLaw} (g : SupportGap X) : ℝ :=
  tau X ((g.val.1 + g.val.2) / 2)

def gapJTerm {X : StandardizedLaw} (g : SupportGap X) : ℝ :=
  gapWeight g * (g.val.2 - g.val.1) ^ 2
def gapJ1Term {X : StandardizedLaw} (g : SupportGap X) : ℝ :=
  gapWeight g * ∫ t in Icc g.val.1 g.val.2, (t - g.val.1) * t
def gapJ2Term {X : StandardizedLaw} (g : SupportGap X) : ℝ :=
  gapWeight g * ∫ t in Icc g.val.1 g.val.2, (t - g.val.1) * t * |t|

def previousReflectedLaw {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ProbabilityLaw :=
  (ProbabilityLaw.convolutionPow w.X.law (n - 1)).map (by fun_prop :
    AEMeasurable (fun x : ℝ => w.rawThreshold.value - x)
      (ProbabilityLaw.convolutionPow w.X.law (n - 1)))

def gapLTerm {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (g : SupportGap w.X) : ℝ :=
  gapWeight g * ∫ t in Ico g.val.1 g.val.2, (t - g.val.1)
    ∂(previousReflectedLaw w : Measure ℝ)

def physicalJ (X : StandardizedLaw) : ℝ := ∑' g : SupportGap X, gapJTerm g
def physicalJ1 (X : StandardizedLaw) : ℝ := ∑' g : SupportGap X, gapJ1Term g
def physicalJ2 (X : StandardizedLaw) : ℝ := ∑' g : SupportGap X, gapJ2Term g
def physicalL {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  ∑' g : SupportGap w.X, gapLTerm w g

def physicalDefect (X : StandardizedLaw) : ℝ :=
  (3 + Real.sqrt 10) * X.rho - X.gamma - 3 * physicalJ X

/-- Different semantics from physicalDefect; no conversion theorem is assumed. -/
def matchingMomentDefect (X : StandardizedLaw) : ℝ :=
  X.rho - (X.gamma ^ 2 + 2) / Real.sqrt (X.gamma ^ 2 + 4)

structure GapEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : Prop where
  summableJ : Summable (gapJTerm (X := w.X))
  summableJ1 : Summable (gapJ1Term (X := w.X))
  summableJ2 : Summable (gapJ2Term (X := w.X))
  summableL : Summable (gapLTerm w)
  defect_nonneg : 0 ≤ physicalDefect w.X
  leak_nonneg : 0 ≤ physicalL w

def hinge (z x : ℝ) : ℝ := (x - z) * |x - z|
def hingeError {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  (∫ x, hinge w.threshold.value x
    ∂(ProbabilityLaw.normalizedSum w.X.law n : Measure ℝ)) -
  (∫ x, hinge w.threshold.value x ∂(ProbabilityLaw.standardNormal : Measure ℝ)) -
    2 * w.X.gamma * phi w.threshold.value / (3 * Real.sqrt n)

def physicalError {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  -(n : ℝ) * Real.sqrt n * hingeError w / 2

def rawRemainder {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  let C := w.X.normalizedScore n
  let H := w.rawThreshold.value
  let d := phi w.threshold.value
  let Kq := absoluteFifthMoment w.X / 4 - w.X.rho * fourthMoment w.X / 2
    - 3 * w.X.beta * w.X.gamma / 2 + w.X.rho / 2
  let K1 := signedAbsoluteFourth w.X - 3 * w.X.beta - 3 * w.X.rho * w.X.gamma / 2
  let U := physicalJ1 w.X + (fourthMoment w.X - 3) / 6
  C * (3 * w.X.beta * physicalJ w.X / 2 + 3 * w.X.rho * physicalJ1 w.X
    - 3 * physicalJ2 w.X - Kq) + H * (C * K1 + d * U)
    - H ^ 2 * (C * w.X.rho + w.X.gamma * d / 2) + physicalError w

def conservedBudget {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  let W := w.rawThreshold.value ^ 2 / (2 * (n : ℝ))
  (n : ℝ) * (w.X.normalizedScore n - esseenConstant) * w.X.rho +
  (n : ℝ) * esseenConstant * w.X.rho * (1 - Real.exp (-W)) +
  (n : ℝ) * phi 0 * Real.exp (-W) * physicalDefect w.X / 6 +
  (n : ℝ) * Real.sqrt n * physicalL w

structure ConservedIdentity {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : Prop where
  identity : conservedBudget w = rawRemainder w

structure UnweightedDefectCap (X : StandardizedLaw) (cap : ℚ) : Prop where
  bound : physicalDefect X ≤ (cap : ℝ)

structure WeightedDefectCap (X : StandardizedLaw) (actual floorIndex : ℕ) (cap : ℚ) : Prop where
  bound : (actual : ℝ) * physicalDefect X ≤ (floorIndex : ℝ) * (cap : ℝ)

theorem weighted_to_unweighted {X : StandardizedLaw} {actual floorIndex : ℕ} {cap : ℚ}
    (h : WeightedDefectCap X actual floorIndex cap) (hactual : 0 < actual)
    (hfloor : floorIndex ≤ actual) (hcap : 0 ≤ cap) : UnweightedDefectCap X cap := by
  have ha : (0 : ℝ) < actual := by exact_mod_cast hactual
  have hf : (floorIndex : ℝ) ≤ actual := by exact_mod_cast hfloor
  have hc : (0 : ℝ) ≤ cap := by exact_mod_cast hcap
  have hmul := mul_le_mul_of_nonneg_right hf hc
  refine ⟨?_⟩
  exact (mul_le_mul_iff_right₀ ha).mp (h.bound.trans hmul)

end BEMap
