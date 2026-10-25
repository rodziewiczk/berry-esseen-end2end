import BEMap.TypedPipeline
import BEMap.Mixed
import BEMap.GeneralCount

/-! Source-scoped acquired reference semantics for the selected mixed n25
registry. A reference is a proved local theorem, not a receipt/hash/status.
Lookup requires containment in ONE acquired scope with exact cfg identity.
The original25 contact is retained for support-feedback rules; no24 contact
is invented. Numerical checkers quantify unknown laws only semantically. -/
noncomputable section
namespace BEMap.MixedRegistry

structure LawProjectionBox where
  probability : ClosedInterval
  weightedNoise : ClosedInterval
  alpha : ClosedInterval

def LawProjectionBox.Contains (box : LawProjectionBox) (point : CountPoint 25) : Prop :=
  box.probability.Contains point.p ∧ box.weightedNoise.Contains point.lambda ∧ box.alpha.Contains point.alpha

def LawProjectionBox.Covers (box : LawProjectionBox) (candidate : CountBox 25) : Prop :=
  (candidate.bounds .probability).Refines box.probability ∧
  (candidate.bounds .weightedNoise).Refines box.weightedNoise ∧
  (candidate.bounds .alpha).Refines box.alpha

def BoxCovers (acquired candidate : CountBox 25) : Prop :=
  candidate.root = acquired.root ∧ ∀ c, (candidate.bounds c).Refines (acquired.bounds c)

theorem interval_contains_of_refines {small large : ClosedInterval} {x : ℝ}
    (h : small.Refines large) (hx : small.Contains x) : large.Contains x := by
  have hl : (large.lower : ℝ) ≤ small.lower := by exact_mod_cast h.1
  have hu : (small.upper : ℝ) ≤ large.upper := by exact_mod_cast h.2
  exact ⟨hl.trans hx.1, hx.2.trans hu⟩

theorem box_contains_of_covers {acquired candidate : CountBox 25} {point : CountPoint 25}
    (h : BoxCovers acquired candidate) (hx : candidate.Contains point) : acquired.Contains point := by
  exact ⟨hx.1.trans h.1, fun c => interval_contains_of_refines (h.2 c) (hx.2 c)⟩

theorem law_projection_contains_of_covers {box : LawProjectionBox} {candidate : CountBox 25}
    {point : CountPoint 25} (h : box.Covers candidate) (hx : candidate.Contains point) : box.Contains point :=
  ⟨interval_contains_of_refines h.1 (hx.2 .probability),
    interval_contains_of_refines h.2.1 (hx.2 .weightedNoise),
    interval_contains_of_refines h.2.2 (hx.2 .alpha)⟩

inductive ReferenceScope where
  | phaseFree (box : LawProjectionBox)
  | fullBox (box : CountBox 25)

def ReferenceScope.Contains (scope : ReferenceScope) (point : CountPoint 25) : Prop :=
  match scope with | .phaseFree box => box.Contains point | .fullBox box => box.Contains point

def ReferenceScope.Covers (scope : ReferenceScope) (candidate : CountBox 25) : Prop :=
  match scope with | .phaseFree box => box.Covers candidate | .fullBox box => BoxCovers box candidate

theorem ReferenceScope.contains_of_covers {scope : ReferenceScope} {candidate : CountBox 25}
    {point : CountPoint 25} (h : scope.Covers candidate) (hx : candidate.Contains point) : scope.Contains point := by
  cases scope with
  | phaseFree box => exact law_projection_contains_of_covers h hx
  | fullBox box => exact box_contains_of_covers h hx

inductive ReferenceFamily where | a | b | c | d | f
deriving DecidableEq

inductive ProbabilityPanel where | p24 | p25 | p26
deriving DecidableEq

structure ReferenceId where
  family : ReferenceFamily
  key : String
deriving DecidableEq

structure FrozenReference where
  id : ReferenceId
  panel : ProbabilityPanel
  context : CountTaskContext 25
  scope : ReferenceScope
  cfgIdentity : String
  sourceEpoch : String
  sourcePin : MathematicalSourcePin
  epoch_matches_context : sourceEpoch = context.sourcePin.sourceEpoch
  epoch_matches_source : sourceEpoch = sourcePin.sourceEpoch

/-- All external numeric data are frozen in packet. Only the accepted
analytic builder below interprets them for the hypothetical actual law. -/
structure EArithmeticPacket (ctx : CountTaskContext 25) where
  box : Mixed.FrozenEBox
  ratio : Mixed.ERatioBound box
  analytic : Mixed.EPointwiseTheorem
  defectCap : ℚ
  rhoUpper : ℚ
  outward : ((defectCap : ℝ) + (ratio.upper : ℝ)) / (Real.sqrt 10 + 1) ≤ (rhoUpper : ℝ)
  strict : rhoUpper < ctx.rho.lower
  sourcePin : MathematicalSourcePin

structure EArguments {ctx : CountTaskContext 25} (packet : EArithmeticPacket ctx)
    {X : StandardizedLaw} (binary : BinaryModel X) where
  frame : Mixed.EFrame X binary
  realization : Mixed.EBoxRealization packet.box frame
  defect_bound : physicalDefect X ≤ (packet.defectCap : ℝ)

theorem EArguments.excludes {ctx : CountTaskContext 25} {packet : EArithmeticPacket ctx}
    {X : StandardizedLaw} {binary : BinaryModel X} (arguments : EArguments packet binary)
    (rhoLower : (ctx.rho.lower : ℝ) ≤ X.rho) : False := by
  let ceiling := Mixed.eRhoCeiling arguments.realization packet.analytic packet.ratio
    packet.defectCap arguments.defect_bound packet.rhoUpper packet.outward
  exact ceiling.excludes ctx.rho.lower rhoLower packet.strict

/-- C/F share the E theorem on their own phase-free p/lambda/alpha boxes.
The finite scalar box uses s=lambda/25, not weighted lambda itself. -/
structure PhaseFreeEAcquisition (ctx : CountTaskContext 25) (lawBox : LawProjectionBox) where
  packet : EArithmeticPacket ctx
  probability_exact : packet.box.probability = lawBox.probability
  alpha_exact : packet.box.alpha = lawBox.alpha
  noise_lower : packet.box.noise.lower = lawBox.weightedNoise.lower / 25
  noise_upper : packet.box.noise.upper = lawBox.weightedNoise.upper / 25
  arguments : ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint 25)
    (scope : GeneralCountRealization ctx X H point), lawBox.Contains point → EArguments packet scope.binary

theorem PhaseFreeEAcquisition.excludes {ctx : CountTaskContext 25} {lawBox : LawProjectionBox}
    (acquisition : PhaseFreeEAcquisition ctx lawBox) {X : StandardizedLaw} {H : RawThreshold}
    {point : CountPoint 25} (scope : GeneralCountRealization ctx X H point)
    (inside : lawBox.Contains point) : False :=
  (acquisition.arguments X H point scope inside).excludes scope.rho.1

def nativeRawThreshold (n k : ℕ) (p lambda phase : ℝ) : ℝ :=
  ((k : ℝ) + phase - (n : ℝ) * p) / Real.sqrt (p * (1 - p) + lambda / n)

/-- Accepted normalization consequence of the exact binary representation.
This is a source theorem, not a new choice for a numeric implementation. -/
structure NativePhaseNormalization : Prop where
  identity : ∀ (ctx : CountTaskContext 25) (X : StandardizedLaw) (H : RawThreshold)
    (point : CountPoint 25), GeneralCountRealization ctx X H point →
      H.value = nativeRawThreshold 25 point.root.val point.p point.lambda point.phase

structure EmptyPhasePacket (ctx : CountTaskContext 25) (box : CountBox 25) where
  rawInterval : ClosedInterval
  normalization : NativePhaseNormalization
  enclosure : ∀ p lambda phase : ℝ, (box.bounds .probability).Contains p →
    (box.bounds .weightedNoise).Contains lambda → (box.bounds .phase).Contains phase →
      0 < p → p < 1 → 0 ≤ lambda →
        rawInterval.Contains (nativeRawThreshold 25 box.root.val p lambda phase)
  strict_disjoint : rawInterval.upper < ctx.rawThreshold.lower ∨
    ctx.rawThreshold.upper < rawInterval.lower

theorem EmptyPhasePacket.excludes {ctx : CountTaskContext 25} {box : CountBox 25}
    (packet : EmptyPhasePacket ctx box) {X : StandardizedLaw} {H : RawThreshold}
    {point : CountPoint 25} (scope : GeneralCountRealization ctx X H point)
    (inside : box.Contains point) : False := by
  have hlambda : 0 ≤ point.lambda := by
    rw [scope.lambda_exact]
    exact mul_nonneg (by norm_num) scope.binary.noise_nonneg
  have hp : 0 < point.p := by rw [scope.p_exact]; exact scope.binary.probability_pos
  have hq : point.p < 1 := by rw [scope.p_exact]; exact scope.binary.probability_lt_one
  have hr := packet.enclosure point.p point.lambda point.phase (inside.2 .probability)
    (inside.2 .weightedNoise) (inside.2 .phase) hp hq hlambda
  have heq := packet.normalization.identity ctx X H point scope
  rw [inside.1] at heq
  rw [← heq] at hr
  rcases packet.strict_disjoint with hleft | hright
  · have hs : (packet.rawInterval.upper : ℝ) < ctx.rawThreshold.lower := by exact_mod_cast hleft
    linarith [hr.2, scope.threshold.1]
  · have hs : (ctx.rawThreshold.upper : ℝ) < packet.rawInterval.lower := by exact_mod_cast hright
    linarith [scope.threshold.2, hr.1]

structure PrefixCaps where
  rhoUpper : ℚ
  radiusMinus : ℚ
  radiusPlus : ℚ
  outer0 : ℚ
  outer1 : ℚ

def PrefixCaps.initial (ctx : CountTaskContext 25) : PrefixCaps :=
  ⟨ctx.rho.upper, ctx.negativeRadius, ctx.positiveRadius, ctx.conditionalOuter0, ctx.conditionalOuter1⟩

def PrefixCaps.Refines (after before : PrefixCaps) : Prop :=
  after.rhoUpper ≤ before.rhoUpper ∧ after.radiusMinus ≤ before.radiusMinus ∧
  after.radiusPlus ≤ before.radiusPlus ∧ after.outer0 ≤ before.outer0 ∧ after.outer1 ≤ before.outer1

def PrefixCaps.Valid {ctx : CountTaskContext 25} (caps : PrefixCaps)
    {X : StandardizedLaw} {H : RawThreshold} {point : CountPoint 25}
    (scope : GeneralCountRealization ctx X H point) : Prop :=
  X.rho ≤ (caps.rhoUpper : ℝ) ∧
  (∀ᵐ x ∂(X.law : MeasureTheory.Measure ℝ), -(caps.radiusMinus : ℝ) ≤ x ∧ x ≤ (caps.radiusPlus : ℝ)) ∧
  (∀ᵐ u ∂(scope.binary.negativeLaw : MeasureTheory.Measure ℝ), -(caps.outer0 : ℝ) ≤ u) ∧
  (∀ᵐ u ∂(scope.binary.positiveLaw : MeasureTheory.Measure ℝ), u ≤ (caps.outer1 : ℝ))

inductive PrefixRecipe where | preflight | fixedOuterRatio | variableSupportCoupled | contactRay
deriving DecidableEq

/-- Saved D prefixes keep the original count, u, a0, cfg and H/beta scope.
Only the five upper caps can change. This interface is finite, chronological
and includes proof of each named source callback's necessary consequences. -/
structure FinitePrefixLicense (ctx : CountTaskContext 25) (box : CountBox 25) where
  length : ℕ
  at_most_preflight_plus_three : length ≤ 4
  caps : Fin (length + 1) → PrefixCaps
  initial : caps ⟨0, by omega⟩ = PrefixCaps.initial ctx
  recipe : Fin length → PrefixRecipe
  source : Fin length → MathematicalSourcePin
  tightens : ∀ i : Fin length,
    (caps ⟨i.val + 1, by omega⟩).Refines (caps ⟨i.val, by omega⟩)
  step_sound : ∀ i : Fin length, ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), box.Contains point →
      (caps ⟨i.val, by omega⟩).Valid owner.toGeneral →
        (caps ⟨i.val + 1, by omega⟩).Valid owner.toGeneral
  initial_sound : ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), box.Contains point → (PrefixCaps.initial ctx).Valid owner.toGeneral

theorem FinitePrefixLicense.final_valid {ctx : CountTaskContext 25} {box : CountBox 25}
    (chain : FinitePrefixLicense ctx box) {w : ContraryContact 25} {point : CountPoint 25}
    (owner : ctx.SatisfiedBy w point) (inside : box.Contains point) :
    (chain.caps ⟨chain.length, by omega⟩).Valid owner.toGeneral := by
  have all : ∀ i : ℕ, ∀ hi : i ≤ chain.length,
      (chain.caps ⟨i, by omega⟩).Valid owner.toGeneral := by
    intro i
    induction i with
    | zero =>
      intro hi
      change (chain.caps ⟨0, by omega⟩).Valid owner.toGeneral
      rw [chain.initial]
      exact chain.initial_sound w point owner inside
    | succ i ih =>
      intro hi
      exact chain.step_sound ⟨i, by omega⟩ w point owner inside (ih (by omega))
  exact all chain.length (le_refl _)

/-- D's finished-prefix scalar uses the same E ratio, but its necessary
whole-path gates use the prefix's V0/V1 UPPER bounds. They must not be
silently strengthened to the looser independent p/s/alpha estimates. -/
structure FinishedScalarData where
  rho : ClosedInterval
  rho_positive : 0 < rho.lower
  probability : ClosedInterval
  noise : ClosedInterval
  alpha : ClosedInterval
  probability_pos : 0 < probability.lower
  probability_lt_one : probability.upper < 1
  noise_nonneg : 0 ≤ noise.lower
  alpha_unit : 0 ≤ alpha.lower ∧ alpha.upper ≤ 1
  outer0 : ℚ
  outer1 : ℚ
  outer0_pos : 0 < outer0
  outer1_pos : 0 < outer1
  totalInward : ℚ
  total_nonneg : 0 ≤ totalInward
  total_lt_half : totalInward < 1 / 2
  a0Floor : ℚ
  a0Floor_nonneg : 0 ≤ a0Floor
  V0 : ClosedInterval
  V1 : ClosedInterval
  V0_nonneg : 0 ≤ V0.lower
  V1_nonneg : 0 ≤ V1.lower
  U0 : ℚ
  U1 : ℚ
  U0_nonneg : 0 ≤ U0
  U1_nonneg : 0 ≤ U1
  lower_ordered : max a0Floor (V0.lower / outer0) ≤ U0 ∧ V1.lower / outer1 ≤ U1
  floors_fit : max a0Floor (V0.lower / outer0) + V1.lower / outer1 ≤ totalInward
  factor0_nonneg : 0 ≤ 1 - totalInward - U0
  factor1_nonneg : 0 ≤ 1 - totalInward - U1
  path0 : V0.upper ≤ probability.lower * (1 - totalInward - U0)
  path1 : V1.upper ≤ (1 - probability.upper) * (1 - totalInward - U1)
  sourcePin : MathematicalSourcePin

def FinishedScalarData.L0 (data : FinishedScalarData) : ℚ := max data.a0Floor (data.V0.lower / data.outer0)
def FinishedScalarData.L1 (data : FinishedScalarData) : ℚ := data.V1.lower / data.outer1

def FinishedScalarData.ratio (data : FinishedScalarData) (p s alpha : ℝ) : ℝ :=
  (Mixed.eBase p + s * Mixed.eM data.outer0 data.outer1 p alpha +
    s ^ 2 * Mixed.eC data.outer0 data.outer1 p alpha) / Real.sqrt (p * (1 - p) + s) ^ 3

structure FinishedScalarRealization {X : StandardizedLaw} {b : BinaryModel X}
    (data : FinishedScalarData) (frame : Mixed.EFrame X b) : Prop where
  rho : data.rho.Contains X.rho
  p : data.probability.Contains (positiveProbability X)
  s : data.noise.Contains (noiseVariance X)
  alpha : data.alpha.Contains frame.alpha
  outer0 : frame.outer0 = (data.outer0 : ℝ)
  outer1 : frame.outer1 = (data.outer1 : ℝ)
  variance0 : data.V0.Contains (Mixed.variance0 b)
  variance1 : data.V1.Contains (Mixed.variance1 b)
  inward_lower : (data.L0 : ℝ) ≤ frame.a0 ∧ (data.L1 : ℝ) ≤ frame.a1
  inward_upper : frame.a0 ≤ (data.U0 : ℝ) ∧ frame.a1 ≤ (data.U1 : ℝ)
  total : frame.a0 + frame.a1 ≤ (data.totalInward : ℝ)

/-- Accepted exact pointwise_inward_v2 rule at the prefix's coherent V caps.
L0/L1 are validated input bounds; the numerator itself uses O0/O1, p,s,alpha. -/
structure AcceptedFinishedPointwiseTheorem : Prop where
  necessary : ∀ (X : StandardizedLaw) (b : BinaryModel X) (frame : Mixed.EFrame X b)
    (data : FinishedScalarData), FinishedScalarRealization data frame →
      (Real.sqrt 10 + 1) * X.rho ≤ physicalDefect X +
        data.ratio (positiveProbability X) (noiseVariance X) frame.alpha

structure FinishedPointwiseAcquisition (ctx : CountTaskContext 25) (box : CountBox 25) where
  chain : FinitePrefixLicense ctx box
  data : FinishedScalarData
  acquired_rho_refines : ctx.rho.lower ≤ data.rho.lower ∧ data.rho.upper ≤ ctx.rho.upper
  analytic : AcceptedFinishedPointwiseTheorem
  ratioUpper : ℚ
  uniform : ∀ p s alpha, data.probability.Contains p → data.noise.Contains s → data.alpha.Contains alpha →
    data.ratio p s alpha ≤ (ratioUpper : ℝ)
  defectCap : ℚ
  rhoUpper : ℚ
  outward : ((defectCap : ℝ) + (ratioUpper : ℝ)) / (Real.sqrt 10 + 1) ≤ (rhoUpper : ℝ)
  strict : rhoUpper < data.rho.lower
  arguments : ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), box.Contains point →
      (chain.caps ⟨chain.length, by omega⟩).Valid owner.toGeneral →
      ∃ frame : Mixed.EFrame w.X owner.ready.resources.binary,
        FinishedScalarRealization data frame ∧ physicalDefect w.X ≤ (defectCap : ℝ)

theorem FinishedPointwiseAcquisition.excludes {ctx : CountTaskContext 25} {box : CountBox 25}
    (a : FinishedPointwiseAcquisition ctx box) {w : ContraryContact 25} {point : CountPoint 25}
    (owner : ctx.SatisfiedBy w point) (inside : box.Contains point) : False := by
  obtain ⟨frame, realization, hD⟩ := a.arguments w point owner inside (a.chain.final_valid owner inside)
  have h := a.analytic.necessary w.X owner.ready.resources.binary frame a.data realization
  have hu := a.uniform _ _ _ realization.p realization.s realization.alpha
  have hden : 0 < Real.sqrt 10 + 1 := by positivity
  have hupper : w.X.rho ≤ (a.rhoUpper : ℝ) := by
    apply le_trans _ a.outward
    apply (le_div_iff₀ hden).mpr
    linarith
  have hs : (a.rhoUpper : ℝ) < a.data.rho.lower := by exact_mod_cast a.strict
  linarith [realization.rho.1]

/-- Source-exact unused normalized-defect scalar numerator, kept separate
from E's inward-endpoint replacement. Its alpha quadratic is concave. -/
def normalizedDefectNumerator (p s alpha L0 L1 U0 U1 O1 : ℝ) : ℝ :=
  Mixed.eBase p - 6 * p * (1 - p) * Mixed.inwardPhi L0 L1 +
    s * (6 * (U0 - p) * (1 - alpha) + (6 * U1 + 2 * O1) * alpha) -
      2 * s ^ 2 * alpha ^ 2 / (p * O1)

structure NormalizedScalarData where
  rho : ClosedInterval
  rho_positive : 0 < rho.lower
  probability : ClosedInterval
  noise : ClosedInterval
  alpha : ClosedInterval
  p_positive : 0 < probability.lower
  p_below_one : probability.upper < 1
  noise_nonneg : 0 ≤ noise.lower
  alpha_unit : 0 ≤ alpha.lower ∧ alpha.upper ≤ 1
  L0 : ℚ
  L1 : ℚ
  U0 : ℚ
  U1 : ℚ
  O1 : ℚ
  lower_nonneg : 0 ≤ L0 ∧ 0 ≤ L1
  ordered : L0 ≤ U0 ∧ L1 ≤ U1
  totalInward : ℚ
  total_nonneg : 0 ≤ totalInward
  total_lt_half : totalInward < 1 / 2
  floors_fit : L0 + L1 ≤ totalInward
  outer_positive : 0 < O1
  sourcePin : MathematicalSourcePin

def NormalizedScalarData.ratio (data : NormalizedScalarData) (p s alpha : ℝ) : ℝ :=
  normalizedDefectNumerator p s alpha data.L0 data.L1 data.U0 data.U1 data.O1 /
    Real.sqrt (p * (1 - p) + s) ^ 3

structure NormalizedScalarRealization {X : StandardizedLaw} {b : BinaryModel X}
    (data : NormalizedScalarData) (frame : Mixed.EFrame X b) : Prop where
  rho : data.rho.Contains X.rho
  p : data.probability.Contains (positiveProbability X)
  s : data.noise.Contains (noiseVariance X)
  alpha : data.alpha.Contains frame.alpha
  inward_lower : (data.L0 : ℝ) ≤ frame.a0 ∧ (data.L1 : ℝ) ≤ frame.a1
  inward_upper : frame.a0 ≤ (data.U0 : ℝ) ∧ frame.a1 ≤ (data.U1 : ℝ)
  total : frame.a0 + frame.a1 ≤ (data.totalInward : ℝ)
  outer : frame.outer1 = (data.O1 : ℝ)

structure AcceptedNormalizedDefectTheorem : Prop where
  necessary : ∀ (X : StandardizedLaw) (b : BinaryModel X) (frame : Mixed.EFrame X b)
    (data : NormalizedScalarData), NormalizedScalarRealization data frame →
      (Real.sqrt 10 + 1) * X.rho ≤ physicalDefect X +
        data.ratio (positiveProbability X) (noiseVariance X) frame.alpha

structure NormalizedAcquisition (ctx : CountTaskContext 25) (box : CountBox 25) where
  chain : FinitePrefixLicense ctx box
  data : NormalizedScalarData
  acquired_rho_refines : ctx.rho.lower ≤ data.rho.lower ∧ data.rho.upper ≤ ctx.rho.upper
  analytic : AcceptedNormalizedDefectTheorem
  ratioUpper : ℚ
  uniform : ∀ p s alpha, data.probability.Contains p → data.noise.Contains s → data.alpha.Contains alpha →
    data.ratio p s alpha ≤ (ratioUpper : ℝ)
  defectCap : ℚ
  rhoUpper : ℚ
  outward : ((defectCap : ℝ) + (ratioUpper : ℝ)) / (Real.sqrt 10 + 1) ≤ (rhoUpper : ℝ)
  strict : rhoUpper < data.rho.lower
  arguments : ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), box.Contains point →
      (chain.caps ⟨chain.length, by omega⟩).Valid owner.toGeneral →
      ∃ frame : Mixed.EFrame w.X owner.ready.resources.binary,
        NormalizedScalarRealization data frame ∧ physicalDefect w.X ≤ (defectCap : ℝ)

theorem NormalizedAcquisition.excludes {ctx : CountTaskContext 25} {box : CountBox 25}
    (a : NormalizedAcquisition ctx box) {w : ContraryContact 25} {point : CountPoint 25}
    (owner : ctx.SatisfiedBy w point) (inside : box.Contains point) : False := by
  obtain ⟨frame, realization, hD⟩ := a.arguments w point owner inside (a.chain.final_valid owner inside)
  have h := a.analytic.necessary w.X owner.ready.resources.binary frame a.data realization
  have hu := a.uniform _ _ _ realization.p realization.s realization.alpha
  have hden : 0 < Real.sqrt 10 + 1 := by positivity
  have hupper : w.X.rho ≤ (a.rhoUpper : ℝ) := by
    apply le_trans _ a.outward
    apply (le_div_iff₀ hden).mpr
    linarith
  have hs : (a.rhoUpper : ℝ) < a.data.rho.lower := by exact_mod_cast a.strict
  linarith [realization.rho.1]

/-- New-q feedback is a finite source-licensed cap chain on the ORIGINAL
owner and box. It starts at the old-q output, uses the same-law24 ray bounds,
and cannot call a future post-context to justify an earlier contraction. -/
structure ABNewAllowanceLicense (ctx : CountTaskContext 25) (box : CountBox 25)
    (old : FinitePrefixLicense ctx box) (rays : List Mixed.SupportRay) where
  length : ℕ
  at_most_three : length ≤ 3
  caps : Fin (length + 1) → PrefixCaps
  initial : caps ⟨0, by omega⟩ = old.caps ⟨old.length, by omega⟩
  source : Fin length → MathematicalSourcePin
  tightens : ∀ i : Fin length,
    (caps ⟨i.val + 1, by omega⟩).Refines (caps ⟨i.val, by omega⟩)
  CElo : ℚ
  lower_constant : (CElo : ℝ) ≤ esseenConstant
  step_sound : ∀ i : Fin length, ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), box.Contains point →
      (∀ ray ∈ rays, Mixed.ABHalflineBound w.X (ray.requiredHalfline ctx.rawThreshold)) →
      (caps ⟨i.val, by omega⟩).Valid owner.toGeneral →
        (caps ⟨i.val + 1, by omega⟩).Valid owner.toGeneral

theorem ABNewAllowanceLicense.ray_allowance {ctx : CountTaskContext 25} {box : CountBox 25}
    {old : FinitePrefixLicense ctx box} {rays : List Mixed.SupportRay}
    (chain : ABNewAllowanceLicense ctx box old rays) {w : ContraryContact 25}
    {point : CountPoint 25} (owner : ctx.SatisfiedBy w point) (ray : Mixed.SupportRay)
    (predecessor : Mixed.ABHalflineBound w.X (ray.requiredHalfline ctx.rawThreshold))
    (y : ℝ) (inside : ray.Contains y) :
    25 * max (Mixed.positiveClosedScore w.X 24 (w.rawThreshold.value - y) -
      w.X.normalizedScore 25) 0 ≤ Mixed.abRayAllowance predecessor.upper chain.CElo :=
  Mixed.ab_predecessor_allowance w predecessor chain.CElo chain.lower_constant w.critical _
    (ray.predecessor_inside ctx.rawThreshold _ y owner.threshold inside)

def rayContactExpression (lineUpper cubicTerm rhoScale allowance : ℝ) : ℝ :=
  lineUpper + cubicTerm + rhoScale * allowance

/-- The old-q subtraction is licensed by this explicit affine decomposition;
it is never subtraction from an opaque Gaussian/contact upper bound. -/
theorem ray_contact_replacement (lineUpper cubicTerm rhoScale allowance : ℝ) :
    rayContactExpression lineUpper cubicTerm rhoScale (5 / 16) + rhoScale * (allowance - 5 / 16) =
      rayContactExpression lineUpper cubicTerm rhoScale allowance := by
  unfold rayContactExpression
  ring

theorem ABNewAllowanceLicense.final_valid {ctx : CountTaskContext 25} {box : CountBox 25}
    {old : FinitePrefixLicense ctx box} {rays : List Mixed.SupportRay}
    (chain : ABNewAllowanceLicense ctx box old rays) {w : ContraryContact 25}
    {point : CountPoint 25} (owner : ctx.SatisfiedBy w point) (inside : box.Contains point)
    (halfline : ∀ ray ∈ rays, Mixed.ABHalflineBound w.X (ray.requiredHalfline ctx.rawThreshold)) :
    (chain.caps ⟨chain.length, by omega⟩).Valid owner.toGeneral := by
  have all : ∀ i : ℕ, ∀ hi : i ≤ chain.length,
      (chain.caps ⟨i, by omega⟩).Valid owner.toGeneral := by
    intro i
    induction i with
    | zero =>
      intro hi
      simpa only [chain.initial] using old.final_valid owner inside
    | succ i ih =>
      intro hi
      exact chain.step_sound ⟨i, by omega⟩ w point owner inside halfline (ih (by omega))
  exact all chain.length (le_refl _)

/-- The final AB ordinary25 proof covers one ORIGINAL count5 ancestor.
Requiring a complete all26-root forest here would strengthen the source
claim. Both children of every closed strict split are nevertheless mandatory. -/
structure ScopedCountPayload (ctx : CountTaskContext 25) (ancestor : CountBox 25) where
  tree : CountTree ancestor
  entries : List (CountBox 25 × CountLeafConclusion)
  boxes_match : entries.map Prod.fst = tree.leaves

theorem ScopedCountPayload.entry_cover {ctx : CountTaskContext 25} {ancestor : CountBox 25}
    (payload : ScopedCountPayload ctx ancestor) {point : CountPoint 25}
    (inside : ancestor.Contains point) : ∃ entry ∈ payload.entries, entry.1.Contains point := by
  obtain ⟨leaf, hleaf, hpoint⟩ := payload.tree.cover inside
  have hmap : leaf ∈ payload.entries.map Prod.fst := by rw [payload.boxes_match]; exact hleaf
  obtain ⟨entry, hentry, heq⟩ := List.mem_map.mp hmap
  exact ⟨entry, hentry, heq.symm ▸ hpoint⟩

/-- Fixed numerical interpretation over arbitrary same-law signed point
scores. The law is universally quantified, never a numerical runtime input. -/
def ScopedCountMeaning {ctx : CountTaskContext 25} {ancestor : CountBox 25}
    (payload : ScopedCountPayload ctx ancestor) : Prop :=
  ∀ entry ∈ payload.entries,
    match entry.2 with
    | .infeasible => ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint 25),
        GeneralCountRealization ctx X H point → entry.1.Contains point → False
    | .scoreUpper cap relation =>
        relation.Transfers ctx.targetRelation (cap : ℝ) (ctx.target : ℝ) ∧
        ∀ (X : StandardizedLaw) (H : RawThreshold) (point : CountPoint 25),
          GeneralCountRealization ctx X H point → entry.1.Contains point →
            relation.Holds (positiveClosedPointScore X 25 H) (cap : ℝ)

abbrev ScopedCountChecker (ctx : CountTaskContext 25) (ancestor : CountBox 25) :=
  CertificateChecker (ScopedCountPayload ctx ancestor) ScopedCountMeaning

theorem scoped_count_score_bound {ctx : CountTaskContext 25} {ancestor : CountBox 25}
    {checker : ScopedCountChecker ctx ancestor} (certificate : CheckedCertificate checker)
    {w : ContraryContact 25} {point : CountPoint 25} (owner : ctx.SatisfiedBy w point)
    (inside : ancestor.Contains point) : w.X.normalizedScore 25 ≤ (ctx.target : ℝ) := by
  obtain ⟨entry, hentry, hpoint⟩ := certificate.payload.entry_cover inside
  have meaning := checker.sound certificate.payload certificate.accepted entry hentry
  rcases entry with ⟨box, conclusion⟩
  cases conclusion with
  | infeasible => exact False.elim (meaning w.X w.rawThreshold point owner.toGeneral hpoint)
  | scoreUpper cap relation =>
    have h := BoundRelation.transfer (meaning.2 w.X w.rawThreshold point owner.toGeneral hpoint) meaning.1
    have hclosed : positiveClosedPointScore w.X 25 w.rawThreshold ≤ (ctx.target : ℝ) := by
      cases hr : ctx.targetRelation with
      | closed => exact (by simpa only [hr, BoundRelation.Holds] using h)
      | strict => exact (show positiveClosedPointScore w.X 25 w.rawThreshold < (ctx.target : ℝ) by
          simpa only [hr, BoundRelation.Holds] using h).le
    rw [contact_point_score owner.ready.resources.initial.physical.normalization] at hclosed
    exact hclosed

/-- AB's final registry object is an ORIGINAL count5 ancestor exclusion,
not merely a predecessor allowance. Full numerical25 composition follows
the finite old-q -> same-law24 -> new-q refinement chain. -/
structure CompletedABAcquisition (ctx : CountTaskContext 25) (ancestor : CountBox 25) where
  original_count_five : ancestor.root.val = 5
  oldPrefix : FinitePrefixLicense ctx ancestor
  old_three_stages : oldPrefix.length = 3
  postContext : CountTaskContext 25
  same_original_domain : postContext.domain = ctx.domain
  sourcePin : MathematicalSourcePin
  requestedRays : List Mixed.SupportRay
  rays_nonempty : requestedRays ≠ []
  sameLaw24 : ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (_owner : ctx.SatisfiedBy w point), ancestor.Contains point →
      ∀ ray ∈ requestedRays, Mixed.ABHalflineBound w.X (ray.requiredHalfline ctx.rawThreshold)
  newPrefix : ABNewAllowanceLicense ctx ancestor oldPrefix requestedRays
  new_three_stages : newPrefix.length = 3
  final_caps_exact : PrefixCaps.initial postContext = newPrefix.caps ⟨newPrefix.length, by omega⟩
  refinement : ∀ (w : ContraryContact 25) (point : CountPoint 25)
    (owner : ctx.SatisfiedBy w point), ancestor.Contains point →
      (newPrefix.caps ⟨newPrefix.length, by omega⟩).Valid owner.toGeneral →
        postContext.SatisfiedBy w point
  checker : ScopedCountChecker postContext ancestor
  certificate : CheckedCertificate checker
  output_below_critical : (postContext.target : ℝ) < esseenConstant

theorem CompletedABAcquisition.excludes {ctx : CountTaskContext 25} {box : CountBox 25}
    (a : CompletedABAcquisition ctx box) {w : ContraryContact 25} {point : CountPoint 25}
    (owner : ctx.SatisfiedBy w point) (inside : box.Contains point) : False := by
  let post := a.refinement w point owner inside
    (a.newPrefix.final_valid owner inside (a.sameLaw24 w point owner inside))
  have hbound := scoped_count_score_bound a.certificate post inside
  exact (not_lt_of_ge w.critical) (hbound.trans_lt a.output_below_critical)

inductive ReferenceAcquisition (spec : FrozenReference) : Type
  | phaseFreeE (box : LawProjectionBox) (family : spec.id.family = .c ∨ spec.id.family = .f)
      (scope : spec.scope = .phaseFree box) (proof : PhaseFreeEAcquisition spec.context box) : ReferenceAcquisition spec
  | emptyPhase (box : CountBox 25) (family : spec.id.family = .d)
      (scope : spec.scope = .fullBox box) (proof : EmptyPhasePacket spec.context box) : ReferenceAcquisition spec
  | finishedPointwise (box : CountBox 25) (family : spec.id.family = .d)
      (scope : spec.scope = .fullBox box) (proof : FinishedPointwiseAcquisition spec.context box) : ReferenceAcquisition spec
  | normalizedDefect (box : CountBox 25) (family : spec.id.family = .d)
      (scope : spec.scope = .fullBox box) (proof : NormalizedAcquisition spec.context box) : ReferenceAcquisition spec
  | completedAB (box : CountBox 25) (family : spec.id.family = .a ∨ spec.id.family = .b)
      (scope : spec.scope = .fullBox box) (proof : CompletedABAcquisition spec.context box) : ReferenceAcquisition spec

theorem ReferenceAcquisition.excludes {spec : FrozenReference} (a : ReferenceAcquisition spec)
    {w : ContraryContact 25} {point : CountPoint 25} (owner : spec.context.SatisfiedBy w point)
    (inside : spec.scope.Contains point) : False := by
  cases a with
  | phaseFreeE box family hscope proof =>
    rw [hscope] at inside
    exact proof.excludes owner.toGeneral inside
  | emptyPhase box family hscope proof =>
    rw [hscope] at inside
    exact proof.excludes owner.toGeneral inside
  | finishedPointwise box family hscope proof =>
    rw [hscope] at inside
    exact proof.excludes owner inside
  | normalizedDefect box family hscope proof =>
    rw [hscope] at inside
    exact proof.excludes owner inside
  | completedAB box family hscope proof =>
    rw [hscope] at inside
    exact proof.excludes owner inside

structure ReferenceUse (caller : CountTaskContext 25) (candidate : CountBox 25)
    (spec : FrozenReference) where
  exact_cfg : caller = spec.context
  single_acquired_scope : spec.scope.Covers candidate
  cfg_identity : String
  cfg_identity_exact : cfg_identity = spec.cfgIdentity
  source_epoch : String
  source_epoch_exact : source_epoch = spec.sourceEpoch

theorem ReferenceUse.excludes {caller : CountTaskContext 25} {candidate : CountBox 25}
    {spec : FrozenReference} (use : ReferenceUse caller candidate spec)
    (acquired : ReferenceAcquisition spec) {w : ContraryContact 25} {point : CountPoint 25}
    (owner : caller.SatisfiedBy w point) (inside : candidate.Contains point) : False := by
  have howner : spec.context.SatisfiedBy w point := by simpa only [use.exact_cfg] using owner
  exact acquired.excludes howner (ReferenceScope.contains_of_covers use.single_acquired_scope inside)

/-- The builder can consume only declared earlier semantic acquisitions.
Completeness of the declaration relative to a source program is a separate
source-manifest obligation, not something Lean infers from byte hashes. -/
structure SemanticRegistry where
  length : ℕ
  specs : Fin length → FrozenReference
  unique : Function.Injective (fun i => (specs i).id)
  premises : Fin length → List (Fin length)
  earlier : ∀ i, ∀ j ∈ premises i, j.val < i.val
  acquire : ∀ i, (∀ j, j ∈ premises i → ReferenceAcquisition (specs j)) →
    ReferenceAcquisition (specs i)

def SemanticRegistry.acquired (r : SemanticRegistry) (i : Fin r.length) :
    ReferenceAcquisition (r.specs i) :=
  r.acquire i (fun j _hj => r.acquired j)
termination_by i.val
decreasing_by exact r.earlier i j _hj

inductive ReferenceRule where
  | phaseFreeE | emptyPhase | finishedPointwise | normalizedDefect | completedAB
deriving DecidableEq

def ReferenceAcquisition.rule {spec : FrozenReference} : ReferenceAcquisition spec → ReferenceRule
  | .phaseFreeE .. => .phaseFreeE
  | .emptyPhase .. => .emptyPhase
  | .finishedPointwise .. => .finishedPointwise
  | .normalizedDefect .. => .normalizedDefect
  | .completedAB .. => .completedAB

/-- The expected entries freeze the complete contexts, exact acquired scopes,
identifiers, source epochs and source pins. This table is an explicit input;
the present interface does not manufacture missing canonical capsule bytes. -/
structure SourceManifest where
  entries : List FrozenReference
  unique : Function.Injective (fun i : Fin entries.length => (entries[i.val]).id)
  dependencies : Fin entries.length → List ReferenceId
  rules : Fin entries.length → ReferenceRule
  sourceEpoch : String
  epoch_exact : ∀ i : Fin entries.length, (entries[i.val]).sourceEpoch = sourceEpoch
  sourcePin : MathematicalSourcePin

structure SelectedUse (registry : SemanticRegistry) where
  references : List (Fin registry.length)

def SemanticRegistry.familyIndices (r : SemanticRegistry) (family : ReferenceFamily) : Finset (Fin r.length) :=
  Finset.univ.filter fun i => (r.specs i).id.family = family

/-- Cardinalities are historical cross-checks, never admission proofs. -/
structure OriginalP25Cardinalities (r : SemanticRegistry) : Prop where
  a : (r.familyIndices .a).card = 1
  b : (r.familyIndices .b).card = 1
  c : (r.familyIndices .c).card = 2
  d : (r.familyIndices .d).card = 92
  f : (r.familyIndices .f).card = 32
  d_p25 : ((r.familyIndices .d).filter fun i => (r.specs i).panel = .p25).card = 45

/-- Exact admission is a bijection with the frozen source table, not merely
an equality of family counts. Dependency completeness relative to the
accepted source interface is represented by exact table equality. -/
structure OriginalP25Admission (r : SemanticRegistry) (manifest : SourceManifest) where
  entryBijection : Fin r.length ≃ Fin manifest.entries.length
  entry_exact : ∀ i, r.specs i = manifest.entries[(entryBijection i).val]
  dependencies_exact : ∀ i,
    (r.premises i).map (fun j => (r.specs j).id) = manifest.dependencies (entryBijection i)
  rule_exact : ∀ i, (r.acquired i).rule = manifest.rules (entryBijection i)
  cardinalities : OriginalP25Cardinalities r

def SelectedUse.familyOccurrences {r : SemanticRegistry} (used : SelectedUse r)
    (family : ReferenceFamily) : ℕ :=
  (used.references.filter fun i => decide ((r.specs i).id.family = family)).length

structure OriginalP25SelectedUsage {r : SemanticRegistry} (used : SelectedUse r) : Prop where
  all_occurrences : used.references.length = 76
  a : used.familyOccurrences .a = 1
  b : used.familyOccurrences .b = 1
  c : used.familyOccurrences .c = 0
  d : used.familyOccurrences .d = 18
  f_occurrences : used.familyOccurrences .f = 56
  f_distinct : ((used.references.toFinset).filter fun i => (r.specs i).id.family = .f).card = 7

/-- Selected D is seventeen distinct whole-box EMPTY_PHASE statements at
counts 9..25 and one finished scalar statement at count5. These are not
phase-free statements and the unused normalized rules remain admitted. -/
structure SelectedDShape {r : SemanticRegistry} (used : SelectedUse r) where
  empty : Fin 17 → Fin r.length
  empty_distinct : Function.Injective empty
  empty_family : ∀ k, (r.specs (empty k)).id.family = .d
  empty_rule : ∀ k, (r.acquired (empty k)).rule = .emptyPhase
  empty_scope : ∀ k, ∃ box : CountBox 25,
    (r.specs (empty k)).scope = .fullBox box ∧ box.root.val = k.val + 9
  pointwise : Fin r.length
  pointwise_family : (r.specs pointwise).id.family = .d
  pointwise_rule : (r.acquired pointwise).rule = .finishedPointwise
  pointwise_scope : ∃ box : CountBox 25,
    (r.specs pointwise).scope = .fullBox box ∧ box.root.val = 5
  selected_exact : ((used.references.toFinset).filter fun i => (r.specs i).id.family = .d) =
    insert pointwise (Finset.univ.image empty)

end BEMap.MixedRegistry
