import BEMap.Binary
import BEMap.Certificates

/-! Numerical COUNT semantics for an arbitrary SAME law and raw threshold.
No extremality, attained contact, or optimalConstant occurs in this interface.
It is consequently usable at the transferred index24 in the AB argument. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def generalRawCDF (X : StandardizedLaw) (n : ℕ) (H : RawThreshold) : ℝ :=
  ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow X.law n) H.value

/-- Positive orientation, SIGNED point discrepancy. This is not Delta_n,
not its absolute value, and not an assumption that H attains a supremum. -/
def positiveClosedPointScore (X : StandardizedLaw) (n : ℕ) (H : RawThreshold) : ℝ :=
  Real.sqrt n / X.rho * (generalRawCDF X n H -
    ProbabilityLaw.cdf ProbabilityLaw.standardNormal (H.value / Real.sqrt n))

def generalInward0 {X : StandardizedLaw} (gap : SupportGap X) : ℝ :=
  positiveProbability X + inverseBinaryScale X * gap.val.1
def generalInward1 {X : StandardizedLaw} (gap : SupportGap X) : ℝ :=
  (1 - positiveProbability X) - inverseBinaryScale X * gap.val.2
def generalTotalInward {X : StandardizedLaw} (gap : SupportGap X) : ℝ :=
  generalInward0 gap + generalInward1 gap

def FrozenJointBudgetData.AmountsHold (data : FrozenJointBudgetData) (totalInward lambda : ℝ) : Prop :=
  match data with
  | .zero => totalInward = 0 ∧ lambda = 0
  | .positive d noise _ _ => 0 ≤ totalInward ∧ 0 ≤ lambda ∧
      totalInward / (d : ℝ) + lambda / (noise : ℝ) ≤ 1

def AffineDefectBudgetData.AmountsHold (data : AffineDefectBudgetData)
    (defect totalInward lambda : ℝ) : Prop :=
  (data.binaryCharge : ℝ) + (data.gapCharge : ℝ) * totalInward +
    (data.noiseCharge : ℝ) * lambda ≤ defect

def SignedDefectQuadraticData.value (q : SignedDefectQuadraticData) (H : ℝ) : ℝ :=
  (q.constant : ℝ) +
    (if 0 ≤ H then (q.positiveLinear : ℝ) else (q.negativeLinear : ℝ)) * |H| -
      (q.curvature : ℝ) * H ^ 2

def signedQuadraticMaximum (quadratics : List SignedDefectQuadraticData) (H : ℝ) : ℝ :=
  match quadratics with
  | [] => 0
  | q :: rest => rest.foldl (fun acc q => max acc (q.value H)) (q.value H)

def SignedDefectEnvelopeData.AmountsHold (data : SignedDefectEnvelopeData)
    (n : ℕ) (H defect : ℝ) : Prop :=
  defect ≤ 15000 / (997 * (n : ℝ)) * signedQuadraticMaximum data.quadratics H

/-- The exact native-kernel scope. The hypothetical law is a semantic
quantifier, not checker input. Owner-contact acquisition fields in ctx
(ownCap, predecessorCap, rawRCap) are deliberately not reinterpreted as
new index-m extremality assumptions; COUNT consumes the acquired law data.
Those owner fields remain checked in the ordinary Contact SatisfiedBy. -/
structure GeneralCountRealization {n : ℕ} (ctx : CountTaskContext n)
    (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint n) where
  binary : BinaryModel X
  gap : SupportGap X
  crosses_zero : gap.val.1 < 0 ∧ 0 < gap.val.2
  domain : ctx.domain.Contains point
  p_exact : point.p = positiveProbability X
  lambda_exact : point.lambda = weightedNoise X n
  phase_exact : point.phase = (n : ℝ) * positiveProbability X + inverseBinaryScale X * H.value - point.root.val
  rawInward0_exact : point.rawInward0 = generalInward0 gap
  rawInward0_nonneg : 0 ≤ generalInward0 gap
  rawInward1_nonneg : 0 ≤ generalInward1 gap
  total_inward : generalTotalInward gap ≤ (ctx.domain.totalInwardCap : ℝ)
  alpha_nonneg : 0 ≤ point.alpha
  alpha_le_one : point.alpha ≤ 1
  negative_variance : (∫ u : ℝ, u ^ 2 ∂(binary.negativeLaw : Measure ℝ)) =
    noiseVariance X * (1 - point.alpha) / (1 - positiveProbability X)
  positive_variance : (∫ u : ℝ, u ^ 2 ∂(binary.positiveLaw : Measure ℝ)) =
    noiseVariance X * point.alpha / positiveProbability X
  negative_sq_integrable : Integrable (fun u : ℝ => u ^ 2) (binary.negativeLaw : Measure ℝ)
  positive_sq_integrable : Integrable (fun u : ℝ => u ^ 2) (binary.positiveLaw : Measure ℝ)
  support : ∀ᵐ x ∂(X.law : Measure ℝ), -(ctx.negativeRadius : ℝ) ≤ x ∧ x ≤ (ctx.positiveRadius : ℝ)
  conditional_outer0 : ∀ᵐ u ∂(binary.negativeLaw : Measure ℝ),
    -(ctx.conditionalOuter0 : ℝ) ≤ u ∧ u ≤ generalInward0 gap
  conditional_outer1 : ∀ᵐ u ∂(binary.positiveLaw : Measure ℝ),
    -generalInward1 gap ≤ u ∧ u ≤ (ctx.conditionalOuter1 : ℝ)
  fourth_integrable : Integrable (fun x : ℝ => x ^ 4) (X.law : Measure ℝ)
  fifth_integrable : Integrable (fun x : ℝ => |x| ^ 5) (X.law : Measure ℝ)
  rho : ctx.rho.Contains X.rho
  beta : ctx.beta.Contains X.beta
  gamma : ctx.gamma.Contains X.gamma
  mean : ctx.mean.Contains (positiveFirstMoment X)
  fourth : ctx.fourth.Contains (fourthMoment X)
  fifth : ctx.fifth.Contains (absoluteFifthMoment X)
  threshold : ctx.rawThreshold.Contains H.value
  theta : residualTheta X ≤ (ctx.thetaCap : ℝ)
  defect_nonneg : 0 ≤ physicalDefect X
  defect : UnweightedDefectCap X ctx.nativeDefectCap
  joint : ctx.jointBudget.AmountsHold (generalTotalInward gap) (weightedNoise X n)
  affine : ctx.affineBudget.AmountsHold (physicalDefect X) (generalTotalInward gap) (weightedNoise X n)
  signed : ctx.signedEnvelope.AmountsHold n H.value (physicalDefect X)
  negative_gap : (ctx.negativeGapFloor : ℝ) ≤ -gap.val.1
  positive_gap : (ctx.positiveGapFloor : ℝ) ≤ gap.val.2
  mixture : generalRawCDF X n H = ∑ k : Fin (n + 1),
    binomialMass n (positiveProbability X) k * incomingProbability binary k
      ((n : ℝ) * positiveProbability X + inverseBinaryScale X * H.value - k.val)

/-- One fixed numerical certificate meaning, also valid for AB's arbitrary
same-law24 sums. A payload must work for every real law and threshold in its
frozen scope. Whole-box combined controls are allowed; individual incoming
probability bounds are not required by this semantic output type. -/
def CountCertificateMeaning {n : ℕ} (ctx : CountTaskContext n)
    (payload : CountCertificatePayload ctx) : Prop :=
  ∀ entry ∈ payload.entries,
    match entry.2 with
    | .infeasible => ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint n),
        GeneralCountRealization ctx X H point → entry.1.Contains point → False
    | .scoreUpper cap relation =>
        relation.Transfers ctx.targetRelation (cap : ℝ) (ctx.target : ℝ) ∧
        ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint n),
          GeneralCountRealization ctx X H point → entry.1.Contains point →
            relation.Holds (positiveClosedPointScore X n H) (cap : ℝ)

/-- Quantitative validity is separate from reaching a requested target. AB
may use a valid returned upper even when a native early-exit target was not
reached. No early-exit target is substituted for the returned number. -/
def CountBoundCertificateMeaning {n : ℕ} (ctx : CountTaskContext n)
    (payload : CountCertificatePayload ctx) : Prop :=
  ∀ entry ∈ payload.entries,
    match entry.2 with
    | .infeasible => ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint n),
        GeneralCountRealization ctx X H point → entry.1.Contains point → False
    | .scoreUpper cap relation =>
        ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint n),
          GeneralCountRealization ctx X H point → entry.1.Contains point →
            relation.Holds (positiveClosedPointScore X n H) (cap : ℝ)

theorem CountCertificateMeaning.toBound {n : ℕ} {ctx : CountTaskContext n}
    {payload : CountCertificatePayload ctx} (meaning : CountCertificateMeaning ctx payload) :
    CountBoundCertificateMeaning ctx payload := by
  intro entry hentry
  have h := meaning entry hentry
  rcases entry with ⟨box, conclusion⟩
  cases conclusion with
  | infeasible => exact h
  | scoreUpper cap relation => exact h.2

structure QuantitativeCountPayload {n : ℕ} (ctx : CountTaskContext n) where
  certificate : CountCertificatePayload ctx
  upper : ℚ
  dominates : ∀ entry ∈ certificate.entries, ∀ cap relation,
    entry.2 = .scoreUpper cap relation → cap ≤ upper

def QuantitativeCountMeaning {n : ℕ} (ctx : CountTaskContext n)
    (payload : QuantitativeCountPayload ctx) : Prop :=
  CountBoundCertificateMeaning ctx payload.certificate

abbrev QuantitativeCountChecker {n : ℕ} (ctx : CountTaskContext n) :=
  CertificateChecker (QuantitativeCountPayload ctx) (QuantitativeCountMeaning ctx)

theorem quantitative_count_point_bound {n : ℕ} {ctx : CountTaskContext n}
    {payload : QuantitativeCountPayload ctx} (meaning : QuantitativeCountMeaning ctx payload)
    {X : StandardizedLaw} {H : RawThreshold} {point : CountPoint n}
    (scope : GeneralCountRealization ctx X H point) :
    positiveClosedPointScore X n H ≤ (payload.upper : ℝ) := by
  obtain ⟨entry, hmem, hinside⟩ := payload.certificate.entry_cover scope.domain
  have hmeaning := meaning entry hmem
  have hdom := payload.dominates entry hmem
  rcases entry with ⟨box, conclusion⟩
  cases conclusion with
  | infeasible => exact (hmeaning X H point scope hinside).elim
  | scoreUpper cap relation =>
    have h := hmeaning X H point scope hinside
    have hc : (cap : ℝ) ≤ payload.upper := by exact_mod_cast hdom cap relation rfl
    cases relation with
    | closed => exact h.trans hc
    | strict => exact h.le.trans hc

theorem checked_quantitative_count_point_bound {n : ℕ} {ctx : CountTaskContext n}
    {checker : QuantitativeCountChecker ctx} (certificate : CheckedCertificate checker)
    {X : StandardizedLaw} {H : RawThreshold} {point : CountPoint n}
    (scope : GeneralCountRealization ctx X H point) :
    positiveClosedPointScore X n H ≤ (certificate.payload.upper : ℝ) :=
  quantitative_count_point_bound certificate.meaning scope

theorem CountCertificateMeaning.point_bound {n : ℕ} {ctx : CountTaskContext n}
    {payload : CountCertificatePayload ctx} (meaning : CountCertificateMeaning ctx payload)
    {X : StandardizedLaw} {H : RawThreshold} {point : CountPoint n}
    (scope : GeneralCountRealization ctx X H point) :
    ctx.targetRelation.Holds (positiveClosedPointScore X n H) (ctx.target : ℝ) := by
  obtain ⟨entry, hmem, hinside⟩ := payload.entry_cover scope.domain
  have hmeaning := meaning entry hmem
  rcases entry with ⟨box, conclusion⟩
  cases conclusion with
  | infeasible => exact (hmeaning X H point scope hinside).elim
  | scoreUpper cap relation =>
    exact BoundRelation.transfer (hmeaning.2 X H point scope hinside) hmeaning.1

abbrev CountCertificateChecker {n : ℕ} (ctx : CountTaskContext n) :=
  CertificateChecker (CountCertificatePayload ctx) (CountCertificateMeaning ctx)

theorem checked_count_point_bound {n : ℕ} {ctx : CountTaskContext n}
    {checker : CountCertificateChecker ctx} (certificate : CheckedCertificate checker)
    {X : StandardizedLaw} {H : RawThreshold} {point : CountPoint n}
    (scope : GeneralCountRealization ctx X H point) :
    positiveClosedPointScore X n H ≤ (ctx.target : ℝ) := by
  have h := certificate.meaning.point_bound scope
  cases hr : ctx.targetRelation with
  | closed => simpa [hr, BoundRelation.Holds] using h
  | strict => exact (show positiveClosedPointScore X n H < (ctx.target : ℝ) by
      simpa [hr, BoundRelation.Holds] using h).le

end BEMap
