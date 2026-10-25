import BEMap.Binary
import BEMap.Fourier
import BEMap.Prawitz
import BEMap.Certificates
import BEMap.GeneralCount
import BEMap.Mixed

/-! Concrete mathematical stage interfaces. Implementations provide proofs
of these exact statements; executable search and a Boolean PASS are not
inhabitants of these types. Every stage is indexed by the same contact. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

/-- Exact bridge between the raw and normalized CLOSED CDF conventions.
This is an analytic normalization theorem to supply, not a numerical option. -/
structure ContactNormalizationEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : Prop where
  positive_index : 0 < n
  raw_positive_closed : rawCDF w -
    ProbabilityLaw.cdf ProbabilityLaw.standardNormal w.threshold.value =
      w.X.iidKolmogorovDistance n

structure MomentBox where
  rho : ClosedInterval
  beta : ClosedInterval
  gamma : ClosedInterval
  probability : ClosedInterval
  fourth : ClosedInterval
  fifth : ClosedInterval

def MomentBox.Contains (box : MomentBox) (X : StandardizedLaw) : Prop :=
  box.rho.Contains X.rho ∧ box.beta.Contains X.beta ∧ box.gamma.Contains X.gamma ∧
  box.probability.Contains (positiveProbability X) ∧
  box.fourth.Contains (fourthMoment X) ∧ box.fifth.Contains (absoluteFifthMoment X)

def ClosedInterval.Refines (after before : ClosedInterval) : Prop :=
  before.lower ≤ after.lower ∧ after.upper ≤ before.upper

def MomentBox.Refines (after before : MomentBox) : Prop :=
  after.rho.Refines before.rho ∧ after.beta.Refines before.beta ∧
  after.gamma.Refines before.gamma ∧ after.probability.Refines before.probability ∧
  after.fourth.Refines before.fourth ∧ after.fifth.Refines before.fifth

/-- Support precedes the higher-moment proof in the dependent field order.
The canonical identity and Fourier data share this actual law and raw H. -/
structure PhysicalState {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  normalization : ContactNormalizationEvidence w
  contact : ContactMajorant w
  support : SupportedContact w
  higherMoments : HigherMomentEvidence support
  gaps : GapEvidence w
  fourier : CompleteFourierEvidence w
  conserved : ConservedIdentity w

def actualPredecessorAllowance {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : ℝ :=
  (n : ℝ) * max (w.X.normalizedScore (n - 1) - w.X.normalizedScore n) 0

/-- INITIAL is a concrete conjunction for one physical state: it includes an
own-index score cap and a separately acquired predecessor allowance. -/
structure InitialState {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  physical : PhysicalState w
  ownCap : ℚ
  ownCap_proof : ScoreCap w ownCap
  predecessorCap : ℚ
  predecessorCap_nonneg : 0 ≤ predecessorCap
  predecessor_proof : actualPredecessorAllowance w ≤ (predecessorCap : ℝ)
  moments : MomentBox
  actual_moments : moments.Contains w.X
  rawThreshold : ClosedInterval
  actual_threshold : rawThreshold.Contains w.rawThreshold.value

/-- A central gap must be acquired. Its endpoints are endpoints of the
actual closed support, not arbitrary slack variables. -/
structure CentralGap (X : StandardizedLaw) where
  negativeEndpoint : ℝ
  positiveEndpoint : ℝ
  negative_pos : 0 < negativeEndpoint
  positive_pos : 0 < positiveEndpoint
  negative_in_support : -negativeEndpoint ∈ (X.law : Measure ℝ).support
  positive_in_support : positiveEndpoint ∈ (X.law : Measure ℝ).support
  empty_interior : ∀ x ∈ Ioo (-negativeEndpoint) positiveEndpoint,
    x ∉ (X.law : Measure ℝ).support
  negative_below_mean : negativeEndpoint ≤ positiveFirstMoment X / (1 - positiveProbability X)
  positive_below_mean : positiveEndpoint ≤ positiveFirstMoment X / positiveProbability X

def CentralGap.inward {X : StandardizedLaw} (g : CentralGap X) : ℝ :=
  let Abar := positiveFirstMoment X / (1 - positiveProbability X)
  let Bbar := positiveFirstMoment X / positiveProbability X
  ((Abar - g.negativeEndpoint) + (Bbar - g.positiveEndpoint)) / (Abar + Bbar)

def CentralGap.rawInward0 {X : StandardizedLaw} (g : CentralGap X) : ℝ :=
  positiveProbability X - inverseBinaryScale X * g.negativeEndpoint

def CentralGap.rawInward1 {X : StandardizedLaw} (g : CentralGap X) : ℝ :=
  (1 - positiveProbability X) - inverseBinaryScale X * g.positiveEndpoint

/-- A zero joint budget is deterministic; it is not the vacuous plane 0<=0.
A positive budget's intercepts are not marginal coordinate caps. -/
def FrozenJointBudgetData.Holds {X : StandardizedLaw} (data : FrozenJointBudgetData)
    (gap : CentralGap X) (n : ℕ) : Prop :=
  data.AmountsHold gap.inward (weightedNoise X n)

structure JointBudget {X : StandardizedLaw} (gap : CentralGap X) (n : ℕ) where
  data : FrozenJointBudgetData
  necessary : data.Holds gap n

def AffineDefectBudgetData.Holds {X : StandardizedLaw} (data : AffineDefectBudgetData)
    (gap : CentralGap X) (n : ℕ) : Prop :=
  data.AmountsHold (physicalDefect X) gap.inward (weightedNoise X n)

def SignedDefectEnvelopeData.Holds {n : ℕ} {floor : ℝ}
    (data : SignedDefectEnvelopeData) (w : ContactAt n floor) : Prop :=
  data.AmountsHold n w.rawThreshold.value (physicalDefect w.X)

/-- Exact canonical conversion from a weighted floor export into a native
unweighted D cap. Any weaker legacy cfg.D must be explicitly licensed. -/
def derivedNativeDefectCap (actual floorIndex : ℕ) (cap : ℚ) : ℚ :=
  (floorIndex : ℚ) * cap / (actual : ℚ)

theorem weighted_to_native_defect_cap {X : StandardizedLaw} {actual floorIndex : ℕ} {cap : ℚ}
    (h : WeightedDefectCap X actual floorIndex cap) (hactual : 0 < actual) :
    UnweightedDefectCap X (derivedNativeDefectCap actual floorIndex cap) := by
  have ha : (0 : ℝ) < actual := by exact_mod_cast hactual
  refine ⟨?_⟩
  unfold derivedNativeDefectCap
  push_cast
  apply (le_div_iff₀ ha).mpr
  simpa only [mul_comm] using h.bound

/-- Every numerical field has a semantic proof concerning the actual law.
The floor index is distinct from n; the weighted cap is nD <= N d. -/
structure ResourceState {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  initial : InitialState w
  binary : BinaryModel w.X
  signedSupport : AsymmetricSupport w
  floorIndex : ℕ
  floor_positive : 0 < floorIndex
  floor_le_actual : floorIndex ≤ n
  defectCap : ℚ
  defectCap_nonneg : 0 ≤ defectCap
  weightedDefect : WeightedDefectCap w.X n floorIndex defectCap
  rawCap : ℚ
  actual_raw : rawRemainder w ≤ (rawCap : ℝ)
  thetaCap : ℚ
  theta_nonneg : 0 ≤ thetaCap
  theta_lt_one : thetaCap < 1
  actual_theta : residualTheta w.X ≤ (thetaCap : ℝ)
  lambdaCap : ℚ
  lambda_nonneg : 0 ≤ lambdaCap
  weightedNoise : WeightedNoiseCap w.X n lambdaCap
  jointBudgets : List (Σ gap : CentralGap w.X, JointBudget gap n)

/-- Conditional variances and alpha are mathematical data with exact
moment equalities. Alpha is never formed by dividing by zero noise. -/
structure ConditionalNoiseSplit {X : StandardizedLaw} (b : BinaryModel X) where
  alpha : ℝ
  alpha_nonneg : 0 ≤ alpha
  alpha_le_one : alpha ≤ 1
  negative_sq_integrable : Integrable (fun u : ℝ => u ^ 2) (b.negativeLaw : Measure ℝ)
  positive_sq_integrable : Integrable (fun u : ℝ => u ^ 2) (b.positiveLaw : Measure ℝ)
  negative_variance : (∫ u : ℝ, u ^ 2 ∂(b.negativeLaw : Measure ℝ)) =
    noiseVariance X * (1 - alpha) / (1 - positiveProbability X)
  positive_variance : (∫ u : ℝ, u ^ 2 ∂(b.positiveLaw : Measure ℝ)) =
    noiseVariance X * alpha / positiveProbability X

def CountBinomialCDF (n : ℕ) (p : ℝ) (k : Fin (n + 1)) : ℝ :=
  ∑ j : Fin (n + 1), if j.val ≤ k.val then binomialMass n p j else 0

def countIncomingArgument {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (k j : Fin (n + 1)) : ℝ := countPhase w k + (k.val : ℝ) - j.val

/-- Exact source lemma: countcore:countineq. This weak probability inequality
retains strict outgoing and closed incoming events and all n+1 roots. -/
structure CountComparisonRule {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (b : BinaryModel w.X) : Prop where
  bound : ∀ k : Fin (n + 1), rawCDF w ≤
    CountBinomialCDF n (positiveProbability w.X) k -
      binomialMass n (positiveProbability w.X) k * strictOutgoingProbability b k (countPhase w k) +
      ∑ j : Fin (n + 1), if k.val < j.val then
        binomialMass n (positiveProbability w.X) j *
          incomingProbability b j (countIncomingArgument w k j) else 0

/-- COUNT readiness includes a proved realization in an ORIGINAL root and
complete coverage. A failed confinement gate cannot construct this state. -/
structure CountReadyState {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  resources : ResourceState w
  centralGap : CentralGap w.X
  split : ConditionalNoiseSplit resources.binary
  identity : CountIdentity w resources.binary
  comparison : CountComparisonRule w resources.binary
  domain : OriginalCountDomain n
  forest : CountLeafCover domain
  root : Fin (n + 1)
  realization : CountPoint n
  root_exact : realization.root = root
  probability_exact : realization.p = positiveProbability w.X
  lambda_exact : realization.lambda = weightedNoise w.X n
  alpha_exact : realization.alpha = split.alpha
  phase_exact : realization.phase = countPhase w root
  rawInward0_exact : realization.rawInward0 = centralGap.rawInward0
  rawInward0_nonneg : 0 ≤ centralGap.rawInward0
  rawInward1_nonneg : 0 ≤ centralGap.rawInward1
  inward_sum : centralGap.rawInward0 + centralGap.rawInward1 = centralGap.inward
  total_inward : centralGap.inward ≤ (domain.totalInwardCap : ℝ)
  joint : JointBudget centralGap n
  joint_licensed : (⟨centralGap, joint⟩ : Σ gap : CentralGap w.X, JointBudget gap n) ∈ resources.jointBudgets
  affineBudget : AffineDefectBudgetData
  affine_necessary : affineBudget.Holds centralGap n
  signedEnvelope : SignedDefectEnvelopeData
  signed_necessary : signedEnvelope.Holds w
  original_membership : domain.Contains realization

/-- Interpretation of a FROZEN numerical context for a hypothetical contact.
This is a quantified mathematical proof object, never a runtime input to the
checker. The context target is independent of the contact's extraction floor. -/
structure CountTaskContext.SatisfiedBy {n : ℕ} (ctx : CountTaskContext n)
    {floor : ℝ} (w : ContactAt n floor) (point : CountPoint n) where
  ready : CountReadyState w
  same_point : ready.realization = point
  original_domain : ctx.domain.Contains point
  support : AlmostBounded w.X ctx.supportRadius
  asymmetric_support : ∀ᵐ x ∂(w.X.law : Measure ℝ),
    -(ctx.negativeRadius : ℝ) ≤ x ∧ x ≤ (ctx.positiveRadius : ℝ)
  joint : ctx.jointBudget.Holds ready.centralGap n
  affine : ctx.affineBudget.Holds ready.centralGap n
  signed : ctx.signedEnvelope.Holds w
  total_inward : ready.centralGap.inward ≤ (ctx.domain.totalInwardCap : ℝ)
  conditional_outer0 : ∀ᵐ u ∂(ready.resources.binary.negativeLaw : Measure ℝ),
    -(ctx.conditionalOuter0 : ℝ) ≤ u ∧ u ≤ ready.centralGap.rawInward0
  conditional_outer1 : ∀ᵐ u ∂(ready.resources.binary.positiveLaw : Measure ℝ),
    -ready.centralGap.rawInward1 ≤ u ∧ u ≤ (ctx.conditionalOuter1 : ℝ)
  rho : ctx.rho.Contains w.X.rho
  beta : ctx.beta.Contains w.X.beta
  gamma : ctx.gamma.Contains w.X.gamma
  mean : ctx.mean.Contains (positiveFirstMoment w.X)
  fourth : ctx.fourth.Contains (fourthMoment w.X)
  fifth : ctx.fifth.Contains (absoluteFifthMoment w.X)
  threshold : ctx.rawThreshold.Contains w.rawThreshold.value
  own : ScoreCap w ctx.ownCap
  predecessor : actualPredecessorAllowance w ≤ (ctx.predecessorCap : ℝ)
  defect : WeightedDefectCap w.X n ctx.floorIndex ctx.defectCap
  raw : rawRemainder w ≤ (ctx.rawRCap : ℝ)
  theta : residualTheta w.X ≤ (ctx.thetaCap : ℝ)
  negative_gap : (ctx.negativeGapFloor : ℝ) ≤ ready.centralGap.negativeEndpoint
  positive_gap : (ctx.positiveGapFloor : ℝ) ≤ ready.centralGap.positiveEndpoint

/-- Ordinary attained-contact scope specializes the more general same-law
COUNT scope. The numerical checker itself needs no extremality assumption. -/
def CountTaskContext.SatisfiedBy.toGeneral {n : ℕ} {ctx : CountTaskContext n}
    {floor : ℝ} {w : ContactAt n floor} {point : CountPoint n}
    (scope : ctx.SatisfiedBy w point) : GeneralCountRealization ctx w.X w.rawThreshold point := by
  let ready := scope.ready
  let gap := ready.centralGap
  let g : SupportGap w.X := ⟨(-gap.negativeEndpoint, gap.positiveEndpoint),
    by exact ⟨by linarith [gap.negative_pos, gap.positive_pos], gap.negative_in_support,
      gap.positive_in_support, gap.empty_interior⟩⟩
  have h0 : generalInward0 g = gap.rawInward0 := by
    unfold generalInward0 CentralGap.rawInward0
    dsimp [g]
    ring
  have h1 : generalInward1 g = gap.rawInward1 := by rfl
  have htotal : generalTotalInward g = gap.inward := by
    unfold generalTotalInward
    rw [h0, h1]
    exact ready.inward_sum
  have hnative := weighted_to_native_defect_cap scope.defect
    (by have hn := ctx.at_least_two; omega : 0 < n)
  have hweaken : (derivedNativeDefectCap n ctx.floorIndex ctx.defectCap : ℝ) ≤
      (ctx.nativeDefectCap : ℝ) := by
    unfold derivedNativeDefectCap
    exact_mod_cast ctx.nativeDefectCap_weakens
  refine {
    binary := ready.resources.binary
    gap := g
    crosses_zero := ⟨by dsimp [g]; linarith [gap.negative_pos], gap.positive_pos⟩
    domain := scope.original_domain
    p_exact := ?_
    lambda_exact := ?_
    phase_exact := ?_
    rawInward0_exact := ?_
    rawInward0_nonneg := by simpa only [h0] using ready.rawInward0_nonneg
    rawInward1_nonneg := by simpa only [h1] using ready.rawInward1_nonneg
    total_inward := by simpa only [htotal] using scope.total_inward
    alpha_nonneg := ?_
    alpha_le_one := ?_
    negative_variance := ?_
    positive_variance := ?_
    negative_sq_integrable := ready.split.negative_sq_integrable
    positive_sq_integrable := ready.split.positive_sq_integrable
    support := scope.asymmetric_support
    conditional_outer0 := by simpa only [h0] using scope.conditional_outer0
    conditional_outer1 := by simpa only [h1] using scope.conditional_outer1
    fourth_integrable := ready.resources.initial.physical.higherMoments.fourth
    fifth_integrable := ready.resources.initial.physical.higherMoments.fifth
    rho := scope.rho
    beta := scope.beta
    gamma := scope.gamma
    mean := scope.mean
    fourth := scope.fourth
    fifth := scope.fifth
    threshold := scope.threshold
    theta := scope.theta
    defect_nonneg := ready.resources.initial.physical.gaps.defect_nonneg
    defect := ⟨hnative.bound.trans hweaken⟩
    joint := by simpa only [FrozenJointBudgetData.Holds, htotal] using scope.joint
    affine := by simpa only [AffineDefectBudgetData.Holds, htotal] using scope.affine
    signed := scope.signed
    negative_gap := by simpa only [g, neg_neg] using scope.negative_gap
    positive_gap := scope.positive_gap
    mixture := ready.identity.mixture }
  · rw [← scope.same_point]
    exact ready.probability_exact
  · rw [← scope.same_point]
    exact ready.lambda_exact
  · rw [← scope.same_point, ready.root_exact]
    exact ready.phase_exact
  · rw [← scope.same_point, h0]
    exact ready.rawInward0_exact
  · rw [← scope.same_point, ready.alpha_exact]
    exact ready.split.alpha_nonneg
  · rw [← scope.same_point, ready.alpha_exact]
    exact ready.split.alpha_le_one
  · rw [← scope.same_point, ready.alpha_exact]
    exact ready.split.negative_variance
  · rw [← scope.same_point, ready.alpha_exact]
    exact ready.split.positive_variance

theorem contact_point_score {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (normalization : ContactNormalizationEvidence w) :
    positiveClosedPointScore w.X n w.rawThreshold = w.X.normalizedScore n := by
  have hn : (0 : ℝ) < n := by exact_mod_cast normalization.positive_index
  have hs : Real.sqrt n ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hn)
  have hz : w.rawThreshold.value / Real.sqrt n = w.threshold.value := by
    unfold ContactAt.rawThreshold
    dsimp
    field_simp [hs]
  change Real.sqrt n / w.X.rho *
    (rawCDF w - ProbabilityLaw.cdf ProbabilityLaw.standardNormal
      (w.rawThreshold.value / Real.sqrt n)) = w.X.normalizedScore n
  rw [hz, normalization.raw_positive_closed]
  unfold StandardizedLaw.normalizedScore
  ring

theorem checked_count_score_bound {n : ℕ} {ctx : CountTaskContext n}
    {checker : CountCertificateChecker ctx} (certificate : CheckedCertificate checker)
    {floor : ℝ} {w : ContactAt n floor} {point : CountPoint n}
    (scope : ctx.SatisfiedBy w point) : w.X.normalizedScore n ≤ (ctx.target : ℝ) := by
  have h := checked_count_point_bound certificate scope.toGeneral
  rw [contact_point_score scope.ready.resources.initial.physical.normalization] at h
  exact h

/-- A refinement is finite and can only tighten the specifically declared
scalar exports. The after-state independently proves all actual-law bounds. -/
structure ResourceRefinement {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (before : ResourceState w) where
  after : ResourceState w
  same_floor : after.floorIndex = before.floorIndex
  defect_tightens : after.defectCap ≤ before.defectCap
  raw_tightens : after.rawCap ≤ before.rawCap
  theta_tightens : after.thetaCap ≤ before.thetaCap
  lambda_tightens : after.lambdaCap ≤ before.lambdaCap
  joints_retained : ∀ budget ∈ before.jointBudgets, budget ∈ after.jointBudgets
  own_tightens : after.initial.ownCap ≤ before.initial.ownCap
  predecessor_tightens : after.initial.predecessorCap ≤ before.initial.predecessorCap
  moments_tighten : after.initial.moments.Refines before.initial.moments
  threshold_tightens : after.initial.rawThreshold.Refines before.initial.rawThreshold
  minus_tightens : after.signedSupport.radiusMinus ≤ before.signedSupport.radiusMinus
  plus_tightens : after.signedSupport.radiusPlus ≤ before.signedSupport.radiusPlus

inductive ResourceSchedule {n : ℕ} {floor : ℝ} {w : ContactAt n floor} : ResourceState w → Type
  | stop (state : ResourceState w) : ResourceSchedule state
  | step {state : ResourceState w} (edge : ResourceRefinement state)
      (rest : ResourceSchedule edge.after) : ResourceSchedule state

def ResourceSchedule.output {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} : ResourceSchedule state → ResourceState w
  | .stop state => state
  | .step _ rest => rest.output

theorem ResourceSchedule.lambda_tightens {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} (s : ResourceSchedule state) :
    s.output.lambdaCap ≤ state.lambdaCap := by
  induction s with
  | stop state => exact le_rfl
  | step edge rest ih => exact ih.trans edge.lambda_tightens

/-- Exact rational pricing inputs of rescore:joint-resource. `physical_price`
is a simultaneous necessary inequality, not three independently spent caps. -/
structure JointPriceInput {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (state : ResourceState w) (gap : CentralGap w.X) where
  base : ℚ
  base_nonneg : 0 ≤ base
  noisePrice : ℚ
  noisePrice_pos : 0 < noisePrice
  endpointSum : ℚ
  endpointSum_pos : 0 < endpointSum
  varianceUpper : ℚ
  varianceUpper_pos : 0 < varianceUpper
  actual_variance : binaryVariance w.X ≤ (varianceUpper : ℝ)
  actual_endpoints : (endpointSum : ℝ) ≤ gap.negativeEndpoint + gap.positiveEndpoint
  physical_price : (base : ℝ) + 6 * positiveFirstMoment w.X * (endpointSum : ℝ) *
    ((positiveFirstMoment w.X / (1 - positiveProbability w.X) - gap.negativeEndpoint) +
      (positiveFirstMoment w.X / positiveProbability w.X - gap.positiveEndpoint)) +
    (noisePrice : ℝ) * residualTheta w.X ≤ physicalDefect w.X

def JointPriceInput.residual {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap) : ℚ :=
  state.defectCap - i.base

def JointPriceInput.inwardIntercept {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap) : ℚ :=
  i.residual / (6 * (1 - state.thetaCap) * i.endpointSum)

def JointPriceInput.noiseIntercept {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap) : ℚ :=
  (state.floorIndex : ℚ) * i.varianceUpper * i.residual / ((1 - state.thetaCap) * i.noisePrice)

theorem JointPriceInput.intercepts_positive {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap)
    (hr : 0 < i.residual) : 0 < i.inwardIntercept ∧ 0 < i.noiseIntercept := by
  have ht : (0 : ℚ) < 1 - state.thetaCap := sub_pos.mpr state.theta_lt_one
  have hn : (0 : ℚ) < state.floorIndex := by exact_mod_cast state.floor_positive
  constructor
  · exact div_pos hr (mul_pos (mul_pos (by norm_num) ht) i.endpointSum_pos)
  · exact div_pos (mul_pos (mul_pos hn i.varianceUpper_pos) hr) (mul_pos ht i.noisePrice_pos)

def JointPriceInput.positiveData {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap)
    (hr : 0 < i.residual) : FrozenJointBudgetData :=
  .positive i.inwardIntercept i.noiseIntercept (i.intercepts_positive hr).1 (i.intercepts_positive hr).2

/-- Accepted analytic theorem, including the separate zero-resource case.
Its exact formulas fix the future implementation's intercept computations. -/
structure JointResourceTheorem {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : JointPriceInput state gap) : Prop where
  negative : i.residual < 0 → False
  zero : i.residual = 0 → FrozenJointBudgetData.Holds .zero gap n
  positive : ∀ hr : 0 < i.residual, (i.positiveData hr).Holds gap n

def JointResourceTheorem.zeroBudget {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : JointPriceInput state gap}
    (rule : JointResourceTheorem i) (hr : i.residual = 0) : JointBudget gap n :=
  ⟨.zero, rule.zero hr⟩

def JointResourceTheorem.positiveBudget {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : JointPriceInput state gap}
    (rule : JointResourceTheorem i) (hr : 0 < i.residual) : JointBudget gap n :=
  ⟨i.positiveData hr, rule.positive hr⟩

def acquireJointBudget {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (state : ResourceState w) {gap : CentralGap w.X} (budget : JointBudget gap n) :
    ResourceRefinement state where
  after := { state with jointBudgets := state.jointBudgets ++ [⟨gap, budget⟩] }
  same_floor := rfl
  defect_tightens := le_rfl
  raw_tightens := le_rfl
  theta_tightens := le_rfl
  lambda_tightens := le_rfl
  joints_retained := fun _ h => List.mem_append_left _ h
  own_tightens := le_rfl
  predecessor_tightens := le_rfl
  moments_tighten := by
    change state.initial.moments.Refines state.initial.moments
    simp [MomentBox.Refines, ClosedInterval.Refines]
  threshold_tightens := ⟨le_rfl, le_rfl⟩
  minus_tightens := le_rfl
  plus_tightens := le_rfl

def probabilityVarianceMin (i : ClosedInterval) : ℝ :=
  min ((i.lower : ℝ) * (1 - (i.lower : ℝ))) ((i.upper : ℝ) * (1 - (i.upper : ℝ)))

def probabilityVarianceMax (i : ClosedInterval) : ℝ :=
  if (i.lower : ℝ) ≤ 1 / 2 ∧ 1 / 2 ≤ (i.upper : ℝ) then 1 / 4
  else max ((i.lower : ℝ) * (1 - (i.lower : ℝ))) ((i.upper : ℝ) * (1 - (i.upper : ℝ)))

def intervalDistance (x : ℝ) (i : ClosedInterval) : ℝ :=
  max 0 (max ((i.lower : ℝ) - x) (x - (i.upper : ℝ)))

/-- Exact inputs of rescore:re-residual/re-geometry/re-exports. The numerical
algorithm may only round the following deterministic real formulas outwards. -/
structure GeometryInput {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (state : ResourceState w) (gap : CentralGap w.X) where
  probability : ClosedInterval
  probability_contains : probability.Contains (positiveProbability w.X)
  probability_positive : 0 < probability.lower
  probability_below_one : probability.upper < 1
  negativeFloor : ℚ
  positiveFloor : ℚ
  negative_positive : 0 < negativeFloor
  positive_positive : 0 < positiveFloor
  actual_negative : (negativeFloor : ℝ) ≤ gap.negativeEndpoint
  actual_positive : (positiveFloor : ℝ) ≤ gap.positiveEndpoint

def GeometryInput.basePrice {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  (6 + 2 * Real.sqrt 10) * (Real.sqrt (1 - (state.thetaCap : ℝ))) ^ 3 /
    Real.sqrt (probabilityVarianceMax i.probability) *
      intervalDistance ((4 - Real.sqrt 10) / 2) i.probability ^ 2

def GeometryInput.residualPrice {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  (state.defectCap : ℝ) - i.basePrice

def GeometryInput.positiveCost {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  3 * (Real.sqrt 10 + 1) * (i.positiveFloor : ℝ)

def GeometryInput.negativeCost {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  3 * (Real.sqrt 10 + 3) * (i.negativeFloor : ℝ)

def GeometryInput.minimumCost {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  min i.positiveCost i.negativeCost

def GeometryInput.firstMomentFloor {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  Real.sqrt ((1 - (state.thetaCap : ℝ)) * probabilityVarianceMin i.probability)

def GeometryInput.thetaFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  min (state.thetaCap : ℝ) (i.residualPrice / i.minimumCost)

def GeometryInput.negativeFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  max (i.negativeFloor : ℝ)
    (Real.sqrt ((1 - (state.thetaCap : ℝ)) * (i.probability.lower : ℝ) /
      (1 - (i.probability.lower : ℝ))) -
      i.residualPrice / (6 * i.firstMomentFloor * ((i.negativeFloor : ℝ) + (i.positiveFloor : ℝ))))

def GeometryInput.positiveFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  max (i.positiveFloor : ℝ)
    (Real.sqrt ((1 - (state.thetaCap : ℝ)) * (1 - (i.probability.upper : ℝ)) /
      (i.probability.upper : ℝ)) -
      i.residualPrice / (6 * i.firstMomentFloor * ((i.negativeFloor : ℝ) + (i.positiveFloor : ℝ))))

def GeometryInput.weightedNoiseFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  (state.floorIndex : ℝ) * probabilityVarianceMax i.probability * i.residualPrice /
    ((1 - (state.thetaCap : ℝ)) * i.minimumCost)

def GeometryInput.weightedThetaFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  (state.floorIndex : ℝ) * i.residualPrice / i.minimumCost

def GeometryInput.weightedInwardFormula {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : ℝ :=
  (state.floorIndex : ℝ) * i.residualPrice /
    (6 * (1 - (state.thetaCap : ℝ)) * ((i.negativeFloor : ℝ) + (i.positiveFloor : ℝ)))

/-- The exact analytic theorem contract. Proofs can be supplied from the
manuscript theorem; implementing interval evaluation does not prove it. -/
structure GeometryConsequences {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : Prop where
  theta : residualTheta w.X ≤ i.thetaFormula
  negative : i.negativeFormula ≤ gap.negativeEndpoint
  positive : i.positiveFormula ≤ gap.positiveEndpoint
  weighted_theta : (n : ℝ) * residualTheta w.X ≤ i.weightedThetaFormula
  weighted_inward : (n : ℝ) * gap.inward ≤ i.weightedInwardFormula
  weighted_noise : weightedNoise w.X n ≤ i.weightedNoiseFormula

structure GeometryRule {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) : Prop where
  negative_residual_impossible : i.residualPrice < 0 → False
  nonnegative_residual : 0 ≤ i.residualPrice → GeometryConsequences i
  zero_residual : i.residualPrice = 0 → weightedNoise w.X n = 0 ∧ gap.inward = 0

/-- The direction of every outward rounding is part of the interface. A
nonpositive endpoint floor is unresolved, not a proof of emptiness. -/
structure RoundedGeometry {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} (i : GeometryInput state gap) where
  thetaCeiling : ℚ
  negativeFloor : ℚ
  positiveFloor : ℚ
  lambdaCeiling : ℚ
  theta_outward : i.thetaFormula ≤ (thetaCeiling : ℝ)
  negative_outward : (negativeFloor : ℝ) ≤ i.negativeFormula
  positive_outward : (positiveFloor : ℝ) ≤ i.positiveFormula
  lambda_outward : i.weightedNoiseFormula ≤ (lambdaCeiling : ℝ)
  theta_nonneg : 0 ≤ thetaCeiling
  theta_below_one : thetaCeiling < 1
  negative_positive : 0 < negativeFloor
  positive_positive : 0 < positiveFloor
  lambda_nonneg : 0 ≤ lambdaCeiling

theorem RoundedGeometry.exportLambda {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : GeometryInput state gap}
    (rounded : RoundedGeometry i) (consequences : GeometryConsequences i) :
    WeightedNoiseCap w.X n rounded.lambdaCeiling :=
  ⟨consequences.weighted_noise.trans rounded.lambda_outward⟩

structure AcquiredGapFloors {X : StandardizedLaw} (gap : CentralGap X) where
  negative : ℚ
  positive : ℚ
  negative_pos : 0 < negative
  positive_pos : 0 < positive
  negative_bound : (negative : ℝ) ≤ gap.negativeEndpoint
  positive_bound : (positive : ℝ) ≤ gap.positiveEndpoint

def RoundedGeometry.exportGapFloors {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : GeometryInput state gap}
    (rounded : RoundedGeometry i) (consequences : GeometryConsequences i) : AcquiredGapFloors gap where
  negative := max i.negativeFloor rounded.negativeFloor
  positive := max i.positiveFloor rounded.positiveFloor
  negative_pos := i.negative_positive.trans_le (le_max_left _ _)
  positive_pos := i.positive_positive.trans_le (le_max_left _ _)
  negative_bound := by
    rw [Rat.cast_max]
    exact max_le i.actual_negative (rounded.negative_outward.trans consequences.negative)
  positive_bound := by
    rw [Rat.cast_max]
    exact max_le i.actual_positive (rounded.positive_outward.trans consequences.positive)

/-- One actual finite refinement using the explicit formulas. Intersections
retain previous bounds; the weighted-noise export is not N times theta. -/
def geometryRefinement {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : GeometryInput state gap}
    (rounded : RoundedGeometry i) (consequences : GeometryConsequences i) :
    ResourceRefinement state := by
  let nextTheta := min state.thetaCap rounded.thetaCeiling
  let nextLambda := min state.lambdaCap rounded.lambdaCeiling
  have ht : residualTheta w.X ≤ (nextTheta : ℝ) := by
    change residualTheta w.X ≤ ((min state.thetaCap rounded.thetaCeiling : ℚ) : ℝ)
    rw [Rat.cast_min]
    exact le_min state.actual_theta (consequences.theta.trans rounded.theta_outward)
  have hl : weightedNoise w.X n ≤ (nextLambda : ℝ) := by
    change weightedNoise w.X n ≤ ((min state.lambdaCap rounded.lambdaCeiling : ℚ) : ℝ)
    rw [Rat.cast_min]
    exact le_min state.weightedNoise.bound (consequences.weighted_noise.trans rounded.lambda_outward)
  let after : ResourceState w := { state with
    thetaCap := nextTheta
    theta_nonneg := le_min state.theta_nonneg rounded.theta_nonneg
    theta_lt_one := (min_le_left _ _).trans_lt state.theta_lt_one
    actual_theta := ht
    lambdaCap := nextLambda
    lambda_nonneg := le_min state.lambda_nonneg rounded.lambda_nonneg
    weightedNoise := ⟨hl⟩ }
  refine {
    after := after
    same_floor := rfl
    defect_tightens := le_rfl
    raw_tightens := le_rfl
    theta_tightens := min_le_left _ _
    lambda_tightens := min_le_left _ _
    joints_retained := fun _ h => h
    own_tightens := le_rfl
    predecessor_tightens := le_rfl
    moments_tighten := by
      change state.initial.moments.Refines state.initial.moments
      simp [MomentBox.Refines, ClosedInterval.Refines]
    threshold_tightens := ⟨le_rfl, le_rfl⟩
    minus_tightens := le_rfl
    plus_tightens := le_rfl }

/-- The whole geometry operation returns BOTH the tightened state and the
new licensed endpoint floors. A subsequent call uses these floors explicitly. -/
def geometryTransition {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {state : ResourceState w} {gap : CentralGap w.X} {i : GeometryInput state gap}
    (rounded : RoundedGeometry i) (consequences : GeometryConsequences i) :
    ResourceRefinement state × AcquiredGapFloors gap :=
  ⟨geometryRefinement rounded consequences, rounded.exportGapFloors consequences⟩

structure CountEnvelope {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (b : BinaryModel w.X) (k : Fin (n + 1)) where
  binomialCDFUpper : ℚ
  binomialCDF_bound : CountBinomialCDF n (positiveProbability w.X) k ≤ (binomialCDFUpper : ℝ)
  ownMassLower : ℚ
  ownMass_nonneg : 0 ≤ ownMassLower
  ownMass_bound : (ownMassLower : ℝ) ≤ binomialMass n (positiveProbability w.X) k
  outgoingLower : ℚ
  outgoing_bound : (outgoingLower : ℝ) ≤ strictOutgoingProbability b k (countPhase w k)
  incomingMassUpper : Fin (n + 1) → ℚ
  incomingMass_nonneg : ∀ j, 0 ≤ incomingMassUpper j
  incomingMass_bound : ∀ j, k.val < j.val →
    binomialMass n (positiveProbability w.X) j ≤ (incomingMassUpper j : ℝ)
  incomingUpper : Fin (n + 1) → ℚ
  incoming_nonneg : ∀ j, 0 ≤ incomingUpper j
  incoming_bound : ∀ j, k.val < j.val →
    incomingProbability b j (countIncomingArgument w k j) ≤ (incomingUpper j : ℝ)

def CountEnvelope.probabilityUpper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CountEnvelope w b k) : ℚ :=
  e.binomialCDFUpper - e.ownMassLower * e.outgoingLower +
    ∑ j : Fin (n + 1), if k.val < j.val then e.incomingMassUpper j * e.incomingUpper j else 0

theorem CountEnvelope.probability_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CountEnvelope w b k)
    (rule : CountComparisonRule w b) : rawCDF w ≤ (e.probabilityUpper : ℝ) := by
  have hout : 0 ≤ strictOutgoingProbability b k (countPhase w k) := by
    exact sub_nonneg.mpr (ProbabilityLaw.cdf_le_one _ _)
  have hmass : (0 : ℝ) ≤ e.ownMassLower := by exact_mod_cast e.ownMass_nonneg
  have ho1 := mul_le_mul_of_nonneg_right e.ownMass_bound hout
  have ho2 := mul_le_mul_of_nonneg_left e.outgoing_bound hmass
  have hsum : (∑ j : Fin (n + 1), if k.val < j.val then
      binomialMass n (positiveProbability w.X) j *
        incomingProbability b j (countIncomingArgument w k j) else 0) ≤
      ∑ j : Fin (n + 1), if k.val < j.val then
        (e.incomingMassUpper j : ℝ) * (e.incomingUpper j : ℝ) else 0 := by
    apply Finset.sum_le_sum
    intro j _hj
    split_ifs with hj
    · exact mul_le_mul (e.incomingMass_bound j hj) (e.incoming_bound j hj)
        (ProbabilityLaw.cdf_nonneg _ _) (by exact_mod_cast e.incomingMass_nonneg j)
    · exact le_rfl
  have hb := rule.bound k
  have hB := e.binomialCDF_bound
  unfold CountEnvelope.probabilityUpper
  push_cast
  simp_rw [apply_ite, Rat.cast_mul, Rat.cast_zero]
  linarith

/-- Exact normalization packet. Its result is computed from these fields;
there is no separately supplied assumption that the final score is small. -/
structure CountNormalization {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  normalLower : ℚ
  normal_bound : (normalLower : ℝ) ≤ ProbabilityLaw.cdf ProbabilityLaw.standardNormal w.threshold.value
  sqrtUpper : ℚ
  sqrt_bound : Real.sqrt n ≤ (sqrtUpper : ℝ)
  rhoLower : ℚ
  rho_positive : 0 < rhoLower
  rho_bound : (rhoLower : ℝ) ≤ w.X.rho

def normalizedCountUpper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CountEnvelope w b k)
    (p : CountNormalization w) : ℝ :=
  (p.sqrtUpper : ℝ) / (p.rhoLower : ℝ) * max 0 ((e.probabilityUpper : ℝ) - (p.normalLower : ℝ))

/-- A DIFFERENT numerical portfolio: its control is for the coherent whole
count-minus-Gaussian expression. Some native slope-cancellation controls do
not individually upper-bound incoming probabilities; this record does not
misinterpret them as such. Source: countcore:scoretheorem. -/
structure CoherentCountNormalEnvelope {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (b : BinaryModel w.X) (k : Fin (n + 1)) where
  errorUpper : ℚ
  combined_bound : CountBinomialCDF n (positiveProbability w.X) k -
    binomialMass n (positiveProbability w.X) k * strictOutgoingProbability b k (countPhase w k) +
    (∑ j : Fin (n + 1), if k.val < j.val then
      binomialMass n (positiveProbability w.X) j * incomingProbability b j (countIncomingArgument w k j) else 0) -
    ProbabilityLaw.cdf ProbabilityLaw.standardNormal w.threshold.value ≤ (errorUpper : ℝ)

structure ScoreFactorEnclosure {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  sqrtUpper : ℚ
  sqrt_bound : Real.sqrt n ≤ (sqrtUpper : ℝ)
  rhoLower : ℚ
  rho_positive : 0 < rhoLower
  rho_bound : (rhoLower : ℝ) ≤ w.X.rho

def combinedCountUpper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CoherentCountNormalEnvelope w b k)
    (p : ScoreFactorEnclosure w) : ℝ :=
  (p.sqrtUpper : ℝ) / (p.rhoLower : ℝ) * max 0 (e.errorUpper : ℝ)

theorem score_le_combined_count_upper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CoherentCountNormalEnvelope w b k)
    (p : ScoreFactorEnclosure w) (normalization : ContactNormalizationEvidence w)
    (rule : CountComparisonRule w b) : w.X.normalizedScore n ≤ combinedCountUpper e p := by
  have hd : w.X.iidKolmogorovDistance n ≤ (e.errorUpper : ℝ) := by
    linarith [normalization.raw_positive_closed, rule.bound k, e.combined_bound]
  have hd' := hd.trans (le_max_right 0 _)
  have hs : (0 : ℝ) ≤ p.sqrtUpper := (Real.sqrt_nonneg n).trans p.sqrt_bound
  have hr : (0 : ℝ) < p.rhoLower := by exact_mod_cast p.rho_positive
  have hm := mul_le_mul p.sqrt_bound hd' (w.X.iidKolmogorovDistance_nonneg n) hs
  calc
    w.X.normalizedScore n = Real.sqrt n * w.X.iidKolmogorovDistance n / w.X.rho := rfl
    _ ≤ ((p.sqrtUpper : ℝ) * max 0 (e.errorUpper : ℝ)) / w.X.rho :=
      div_le_div_of_nonneg_right hm w.X.rho_nonneg
    _ ≤ ((p.sqrtUpper : ℝ) * max 0 (e.errorUpper : ℝ)) / (p.rhoLower : ℝ) :=
      div_le_div_of_nonneg_left (mul_nonneg hs (le_max_left 0 _)) hr p.rho_bound
    _ = combinedCountUpper e p := by unfold combinedCountUpper; ring

theorem score_le_normalized_count_upper {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {b : BinaryModel w.X} {k : Fin (n + 1)} (e : CountEnvelope w b k)
    (p : CountNormalization w) (normalization : ContactNormalizationEvidence w)
    (rule : CountComparisonRule w b) : w.X.normalizedScore n ≤ normalizedCountUpper e p := by
  have hprob := e.probability_bound rule
  have hdelta : w.X.iidKolmogorovDistance n ≤
      (e.probabilityUpper : ℝ) - (p.normalLower : ℝ) := by
    linarith [normalization.raw_positive_closed, p.normal_bound]
  have hdelta' := hdelta.trans (le_max_right 0 _)
  have hs : (0 : ℝ) ≤ p.sqrtUpper := (Real.sqrt_nonneg n).trans p.sqrt_bound
  have hr : (0 : ℝ) < p.rhoLower := by exact_mod_cast p.rho_positive
  have hmul := mul_le_mul p.sqrt_bound hdelta' (w.X.iidKolmogorovDistance_nonneg n) hs
  calc
    w.X.normalizedScore n = Real.sqrt n * w.X.iidKolmogorovDistance n / w.X.rho := rfl
    _ ≤ ((p.sqrtUpper : ℝ) * max 0 ((e.probabilityUpper : ℝ) - (p.normalLower : ℝ))) / w.X.rho :=
      div_le_div_of_nonneg_right hmul w.X.rho_nonneg
    _ ≤ ((p.sqrtUpper : ℝ) * max 0 ((e.probabilityUpper : ℝ) - (p.normalLower : ℝ))) / (p.rhoLower : ℝ) :=
      div_le_div_of_nonneg_left (mul_nonneg hs (le_max_left 0 _)) hr p.rho_bound
    _ = normalizedCountUpper e p := by unfold normalizedCountUpper; ring

/-- An actual necessary-condition contradiction OR one coherent whole-box
count envelope. A failed numerical applicability guard has no constructor. -/
inductive CountLeafEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (ready : CountReadyState w) (leaf : CountBox n) : Type
  | impossible : False → CountLeafEvidence w ready leaf
  | bounded (envelope : CountEnvelope w ready.resources.binary ready.root)
      (normalization : CountNormalization w)
      (upper : normalizedCountUpper envelope normalization ≤ floor) : CountLeafEvidence w ready leaf
  | combined (envelope : CoherentCountNormalEnvelope w ready.resources.binary ready.root)
      (normalization : ScoreFactorEnclosure w)
      (upper : combinedCountUpper envelope normalization ≤ floor) : CountLeafEvidence w ready leaf
  | certified {ctx : CountTaskContext n} (checker : CountCertificateChecker ctx)
      (certificate : CheckedCertificate checker) (scope : ctx.SatisfiedBy w ready.realization)
      (target : (ctx.target : ℝ) ≤ floor) : CountLeafEvidence w ready leaf

theorem CountLeafEvidence.score_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    {ready : CountReadyState w} {leaf : CountBox n} (h : CountLeafEvidence w ready leaf) :
    w.X.normalizedScore n ≤ floor := by
  cases h with
  | impossible h => exact h.elim
  | bounded e p hu =>
    exact (score_le_normalized_count_upper e p ready.resources.initial.physical.normalization
      ready.comparison).trans hu
  | combined e p hu =>
    exact (score_le_combined_count_upper e p ready.resources.initial.physical.normalization
      ready.comparison).trans hu
  | certified checker certificate scope target =>
    exact (checked_count_score_bound certificate scope).trans target

/-- Evidence for THIS contact on the selected regional method. Unlike the
optional global convenience pipeline below, it imposes no global COUNT
assumption on contacts in the corner/Fourier/universal branches. -/
structure SupportedCountEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  ready : CountReadyState w
  leaves : ∀ leaf ∈ ready.forest.leaves,
    leaf.Contains ready.realization → CountLeafEvidence w ready leaf

theorem SupportedCountEvidence.score_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (e : SupportedCountEvidence w) : w.X.normalizedScore n ≤ floor := by
  obtain ⟨leaf, hmem, hinside⟩ := e.ready.forest.cover e.ready.realization e.ready.original_membership
  exact (e.leaves leaf hmem hinside).score_bound

/-- A provider is universally quantified over the mathematical contact, not
only over realizable moments sampled during numerical discovery. -/
structure ContactPipeline (n : ℕ) (floor : ℝ := esseenConstant) where
  physical : ∀ w : ContactAt n floor, PhysicalState w
  initializeState : ∀ w : ContactAt n floor, PhysicalState w → InitialState w
  acquire : ∀ w : ContactAt n floor, InitialState w → ResourceState w
  prepare : ∀ w : ContactAt n floor, ResourceState w → CountReadyState w
  leaves : ∀ (w : ContactAt n floor) (ready : CountReadyState w),
    ∀ leaf ∈ ready.forest.leaves, leaf.Contains ready.realization → CountLeafEvidence w ready leaf

theorem ContactPipeline.score_bound {n : ℕ} {floor : ℝ} (p : ContactPipeline n floor)
    (w : ContactAt n floor) : w.X.normalizedScore n ≤ floor := by
  let physical := p.physical w
  let initial := p.initializeState w physical
  let resources := p.acquire w initial
  let ready := p.prepare w resources
  obtain ⟨leaf, hmem, hinside⟩ := ready.forest.cover ready.realization ready.original_membership
  exact (p.leaves w ready leaf hmem hinside).score_bound

def ContactPipeline.toEvidence {n : ℕ} {floor : ℝ} (p : ContactPipeline n floor)
    (w : ContactAt n floor) : SupportedCountEvidence w :=
  let ready := p.prepare w (p.acquire w (p.initializeState w (p.physical w)))
  ⟨ready, p.leaves w ready⟩

theorem ContactPipeline.reject {n : ℕ} {floor : ℝ} (p : ContactPipeline n floor)
    (w : ContactAt n floor) (violation : floor < w.X.normalizedScore n) : False :=
  (not_lt_of_ge (p.score_bound w)) violation

/-- Separate support-free API: no SupportedContact or higher moment appears. -/
structure GapFreeEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  normalization : ContactNormalizationEvidence w
  probabilityUpper : ℚ
  probability_bound : rawCDF w ≤ (probabilityUpper : ℝ)
  normalLower : ℚ
  normal_bound : (normalLower : ℝ) ≤ ProbabilityLaw.cdf ProbabilityLaw.standardNormal w.threshold.value
  normalized_bound : Real.sqrt n / w.X.rho *
    max 0 ((probabilityUpper : ℝ) - (normalLower : ℝ)) ≤ floor

theorem GapFreeEvidence.score_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (h : GapFreeEvidence w) : w.X.normalizedScore n ≤ floor := by
  have hd : w.X.iidKolmogorovDistance n ≤
      max 0 ((h.probabilityUpper : ℝ) - (h.normalLower : ℝ)) := by
    apply le_trans _ (le_max_right 0 _)
    linarith [h.normalization.raw_positive_closed, h.probability_bound, h.normal_bound]
  have hc : 0 ≤ Real.sqrt n / w.X.rho := div_nonneg (Real.sqrt_nonneg _) w.X.rho_nonneg
  have hm := mul_le_mul_of_nonneg_left hd hc
  have he : w.X.normalizedScore n = Real.sqrt n / w.X.rho * w.X.iidKolmogorovDistance n := by
    unfold StandardizedLaw.normalizedScore
    ring
  exact (le_of_eq he).trans (hm.trans h.normalized_bound)

def universalRhoEnvelope (rho : ℝ) : ℝ :=
  min (469 / 1000) (min ((3322 / 10000) * (1 + (429 / 1000) / rho))
    ((3031 / 10000) * (1 + (646 / 1000) / rho)))

structure UniversalRhoEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  cutoff : ℚ
  cutoff_pos : 0 < cutoff
  actual_rho : (cutoff : ℝ) ≤ w.X.rho
  structural_bound : w.X.normalizedScore n ≤ universalRhoEnvelope w.X.rho
  monotone_specialization : universalRhoEnvelope w.X.rho ≤ universalRhoEnvelope cutoff
  target_comparison : universalRhoEnvelope cutoff ≤ floor

/-- Transfer references the original law at a smaller index. It deliberately
does not contain ContactAt m or an index-m contact equality. -/
structure SameLawTransfer {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  index : ℕ
  positive : 0 < index
  smaller : index < n
  lambda_scaling : (n : ℝ) * weightedNoise w.X index = (index : ℝ) * weightedNoise w.X n

/-- A probability enclosure for a transferred sum, with its own raw H.
This is not an extremizing contact and does not borrow the original contact
equation. A provider of these for every H covers its two infinite tails too. -/
structure TransferredCDFEnvelope (X : StandardizedLaw) (m : ℕ) (H : RawThreshold) where
  lower : ℚ
  upper : ℚ
  ordered : lower ≤ upper
  lower_bound : (lower : ℝ) ≤ ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow X.law m) H.value
  upper_bound : ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow X.law m) H.value ≤ (upper : ℝ)

/-- Exact numerical24 port used by AB. The context is a NEW24-sum context;
its raw-H interval is exactly the requested closed half-line clipped to the
central window. Every transferred law realization is general, not extremal.
The quantitative checker can return U above its native early-exit target. -/
structure ABGeneralCountPort {X : StandardizedLaw} {b : BinaryModel X}
    (frame : Mixed.EFrame X b) (input : Mixed.ABWindowInput) where
  context : CountTaskContext 24
  domain_exact : context.domain = Mixed.transferredDomain24 input.original
  source_exact : context.sourcePin = input.sourcePin
  clip_exact : ∀ raw : ℝ, context.rawThreshold.Contains raw ↔
    input.halfline.Contains raw ∧ |raw| ≤ (Mixed.abHstar : ℝ)
  checker : QuantitativeCountChecker context
  certificate : CheckedCertificate checker
  scope : Mixed.ABPhysicalScope frame input
  scopeTheorem : Mixed.ABWindowScopeTheorem
  identity : Mixed.ABCountIdentity X b
  realize : ∀ raw : ℝ, input.halfline.Contains raw → |raw| ≤ (Mixed.abHstar : ℝ) →
    ∀ k : Fin 25, -1 / 2 ≤ (Mixed.abCountPoint frame raw k).phase →
      (Mixed.abCountPoint frame raw k).phase ≤ 1 / 2 →
        GeneralCountRealization context X ⟨raw⟩ (Mixed.abCountPoint frame raw k)

theorem ABGeneralCountPort.window_bound {X : StandardizedLaw} {b : BinaryModel X}
    {frame : Mixed.EFrame X b} {input : Mixed.ABWindowInput}
    (port : ABGeneralCountPort frame input) (raw : ℝ)
    (halfline : input.halfline.Contains raw) (window : |raw| ≤ (Mixed.abHstar : ℝ)) :
    Mixed.positiveClosedScore X 24 raw ≤ (port.certificate.payload.upper : ℝ) := by
  obtain ⟨hl, hu⟩ := port.scopeTheorem.central X b frame input port.scope raw window
  have confined : PhaseConfinement 24 (24 * positiveProbability X + inverseBinaryScale X * raw) :=
    ⟨by linarith, by norm_num; linarith⟩
  obtain ⟨k, hphase⟩ := nearest_root_exists 24 _ confined
  have hs := port.realize raw halfline window k hphase.1 hphase.2
  exact checked_quantitative_count_point_bound port.certificate hs

def ABGeneralCountPort.toWindowPacket {X : StandardizedLaw} {b : BinaryModel X}
    {frame : Mixed.EFrame X b} {input : Mixed.ABWindowInput}
    (port : ABGeneralCountPort frame input) : Mixed.ABWindowCountPacket frame input where
  scope := port.scope
  scopeTheorem := port.scopeTheorem
  identity := port.identity
  forest := by
    simpa only [port.domain_exact] using port.certificate.payload.certificate.forest.toLeafCover
  leafUpper := fun _ => port.certificate.payload.upper
  upper := port.certificate.payload.upper
  maxima := fun _ _ => le_rfl
  leaf_meaning := fun _ _ raw halfline window _ _ _ => port.window_bound raw halfline window

/-- An actually empty clipped central window is a separate branch. It does
not force an invalid nonempty ClosedInterval; the exterior tails remain
mandatory in the later Mixed.completeHalfline operation. -/
structure ABEmptyCentralPort {X : StandardizedLaw} {b : BinaryModel X}
    (frame : Mixed.EFrame X b) (input : Mixed.ABWindowInput) where
  scope : Mixed.ABPhysicalScope frame input
  scopeTheorem : Mixed.ABWindowScopeTheorem
  identity : Mixed.ABCountIdentity X b
  empty : ∀ raw : ℝ, input.halfline.Contains raw → |raw| ≤ (Mixed.abHstar : ℝ) → False

def ABEmptyCentralPort.toWindowPacket {X : StandardizedLaw} {b : BinaryModel X}
    {frame : Mixed.EFrame X b} {input : Mixed.ABWindowInput}
    (port : ABEmptyCentralPort frame input) : Mixed.ABWindowCountPacket frame input where
  scope := port.scope
  scopeTheorem := port.scopeTheorem
  identity := port.identity
  forest := ({ roots := fun k => CountTree.leaf ((Mixed.transferredDomain24 input.original).rootBox k) } :
    CompleteCountForest (Mixed.transferredDomain24 input.original)).toLeafCover
  leafUpper := fun _ => 0
  upper := 0
  maxima := fun _ _ => le_rfl
  leaf_meaning := fun _ _ raw halfline window _ _ _ => (port.empty raw halfline window).elim

structure RefinedCountEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  initial : ResourceState w
  schedule : ResourceSchedule initial
  count : SupportedCountEvidence w
  final_state : count.ready.resources = schedule.output

inductive MethodEvidence {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : Type
  | supportedCount (evidence : SupportedCountEvidence w) : MethodEvidence w
  | certifiedCount {ctx : CountTaskContext n} (checker : CountCertificateChecker ctx)
      (certificate : CheckedCertificate checker) (point : CountPoint n)
      (scope : ctx.SatisfiedBy w point) (target : (ctx.target : ℝ) ≤ floor) : MethodEvidence w
  | gapFree (evidence : GapFreeEvidence w) : MethodEvidence w
  | supportedFourier (evidence : PrawitzScoreEvidence w) : MethodEvidence w
  | universalRho (evidence : UniversalRhoEvidence w) : MethodEvidence w
  | refinedCount (evidence : RefinedCountEvidence w) : MethodEvidence w
  | mixedRho (ceiling : Mixed.RhoCeiling w.X) (rhoLower : ℚ)
      (actual_lower : (rhoLower : ℝ) ≤ w.X.rho) (strict : ceiling.upper < rhoLower) : MethodEvidence w

theorem MethodEvidence.score_bound {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (e : MethodEvidence w) : w.X.normalizedScore n ≤ floor := by
  cases e with
  | supportedCount p => exact p.score_bound
  | certifiedCount checker certificate point scope target =>
    exact (checked_count_score_bound certificate scope).trans target
  | gapFree e => exact e.score_bound
  | supportedFourier e => exact e.score_bound
  | universalRho e => exact e.structural_bound.trans (e.monotone_specialization.trans e.target_comparison)
  | refinedCount e => exact e.count.score_bound
  | mixedRho ceiling lower actual_lower strict => exact (ceiling.excludes lower actual_lower strict).elim

end BEMap
