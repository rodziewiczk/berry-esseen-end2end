import BEMap.Binary
import BEMap.Physical
import BEMap.Certificates

/-! Source-specific mixed n25 contracts. E and chord return a rho ceiling;
AB transfers the SAME law to24 and returns a ray-local predecessor allowance.
None assumes the final n25 score bound. `p24` names a probability panel,
not a summand count. Analytic theorem records below are accepted inputs with
exact statements, not new project axioms. -/
noncomputable section
open MeasureTheory Set
namespace BEMap.Mixed

def variance0 {X : StandardizedLaw} (b : BinaryModel X) : ℝ :=
  ∫ u : ℝ, u ^ 2 ∂(b.negativeLaw : Measure ℝ)
def variance1 {X : StandardizedLaw} (b : BinaryModel X) : ℝ :=
  ∫ u : ℝ, u ^ 2 ∂(b.positiveLaw : Measure ℝ)
def third0 {X : StandardizedLaw} (b : BinaryModel X) : ℝ :=
  ∫ u : ℝ, u ^ 3 ∂(b.negativeLaw : Measure ℝ)
def third1 {X : StandardizedLaw} (b : BinaryModel X) : ℝ :=
  ∫ u : ℝ, u ^ 3 ∂(b.positiveLaw : Measure ℝ)

def binaryMomentBase (p : ℝ) : ℝ := p * (1 - p) * (1 - 2 * p * (1 - p))
def inwardPhi (a0 a1 : ℝ) : ℝ := a0 + a1 - a0 ^ 2 - a1 ^ 2 - a0 * a1

def directedOuter0 (oldCap negativeRadius sqrtUpper probabilityLower : ℚ) : ℚ :=
  min oldCap (negativeRadius * sqrtUpper - probabilityLower)
def directedOuter1 (oldCap positiveRadius sqrtUpper probabilityUpper : ℚ) : ℚ :=
  min oldCap (positiveRadius * sqrtUpper - 1 + probabilityUpper)

/-- Uses the JOINT noise intercept, not the marginal lambdaCap. Negative
results are only contradictory after the same-law resource license is supplied. -/
def directedInwardProposal {n : ℕ} (ctx : CountTaskContext n) (lambdaLower : ℚ) : ℚ :=
  match ctx.jointBudget with
  | .zero => 0
  | .positive d0 Lambda _ _ =>
    min (d0 * (1 - lambdaLower / Lambda))
      ((ctx.nativeDefectCap - ctx.affineBudget.binaryCharge -
        ctx.affineBudget.noiseCharge * lambdaLower) / ctx.affineBudget.gapCharge)

/-- Actual conditional moments are definitions, not independently chosen
coordinates. The physical halfplane is the explicit analytic license from
the source; it must be supplied for the same actual endpoints and D. -/
structure EFrame (X : StandardizedLaw) (b : BinaryModel X) where
  alpha : ℝ
  alpha_nonneg : 0 ≤ alpha
  alpha_le_one : alpha ≤ 1
  outer0 : ℝ
  outer1 : ℝ
  outer0_pos : 0 < outer0
  outer1_pos : 0 < outer1
  a0 : ℝ
  a1 : ℝ
  a0_nonneg : 0 ≤ a0
  a1_nonneg : 0 ≤ a1
  negative_support : ∀ᵐ u ∂(b.negativeLaw : Measure ℝ), -outer0 ≤ u ∧ u ≤ a0
  positive_support : ∀ᵐ u ∂(b.positiveLaw : Measure ℝ), -a1 ≤ u ∧ u ≤ outer1
  square0 : Integrable (fun u : ℝ => u ^ 2) (b.negativeLaw : Measure ℝ)
  square1 : Integrable (fun u : ℝ => u ^ 2) (b.positiveLaw : Measure ℝ)
  cube0 : Integrable (fun u : ℝ => u ^ 3) (b.negativeLaw : Measure ℝ)
  cube1 : Integrable (fun u : ℝ => u ^ 3) (b.positiveLaw : Measure ℝ)
  variance0_exact : variance0 b = noiseVariance X * (1 - alpha) / (1 - positiveProbability X)
  variance1_exact : variance1 b = noiseVariance X * alpha / positiveProbability X
  inward0_variance : variance0 b ≤ outer0 * a0
  inward1_variance : variance1 b ≤ outer1 * a1
  zero0 : a0 = 0 → variance0 b = 0 ∧ third0 b = 0
  rho_identity : X.rho * inverseBinaryScale X ^ 3 = binaryMomentBase (positiveProbability X) +
    3 * binaryVariance X * (variance0 b + variance1 b) -
      (1 - positiveProbability X) * third0 b + positiveProbability X * third1 b
  physical_halfplane :
    let p := positiveProbability X
    let q := 1 - p
    let v := p * q
    let sigma := Real.sqrt 10
    v * ((sigma - 1) + 2 * p - (2 * sigma + 6) * v) +
      6 * v * inwardPhi a0 a1 + q * variance0 b * (3 * p * (sigma + 3) - 6 * a0) +
      p * variance1 b * (3 * q * (sigma + 1) - 6 * a1) -
      (sigma + 1) * q * third0 b + (sigma - 1) * p * third1 b ≤
        physicalDefect X * inverseBinaryScale X ^ 3

structure FrozenEBox where
  probability : ClosedInterval
  probability_pos : 0 < probability.lower
  probability_lt_one : probability.upper < 1
  noise : ClosedInterval
  noise_nonneg : 0 ≤ noise.lower
  alpha : ClosedInterval
  alpha_unit : 0 ≤ alpha.lower ∧ alpha.upper ≤ 1
  outer0 : ℚ
  outer1 : ℚ
  outer0_pos : 0 < outer0
  outer1_pos : 0 < outer1
  totalInward : ℚ
  inward_nonneg : 0 ≤ totalInward
  inward_lt_half : totalInward < 1 / 2
  a0Upper : ℚ
  a1Upper : ℚ
  a0_nonneg : 0 ≤ a0Upper
  a1_nonneg : 0 ≤ a1Upper
  factor0_nonneg : 0 ≤ 1 - totalInward - a0Upper
  factor1_nonneg : 0 ≤ 1 - totalInward - a1Upper
  whole_path0 : noise.upper * (1 - alpha.lower) / (1 - probability.upper) ≤
    probability.lower * (1 - totalInward - a0Upper)
  whole_path1 : noise.upper * alpha.upper / probability.lower ≤
    (1 - probability.upper) * (1 - totalInward - a1Upper)
  sourcePin : MathematicalSourcePin

structure EBoxRealization {X : StandardizedLaw} {b : BinaryModel X}
    (box : FrozenEBox) (frame : EFrame X b) : Prop where
  probability : box.probability.Contains (positiveProbability X)
  noise : box.noise.Contains (noiseVariance X)
  alpha : box.alpha.Contains frame.alpha
  outer0 : frame.outer0 = (box.outer0 : ℝ)
  outer1 : frame.outer1 = (box.outer1 : ℝ)
  inward : frame.a0 + frame.a1 ≤ (box.totalInward : ℝ)
  a0 : frame.a0 ≤ (box.a0Upper : ℝ)
  a1 : frame.a1 ≤ (box.a1Upper : ℝ)

def eBase (p : ℝ) : ℝ := 2 * p - 6 * p ^ 3 + 4 * p ^ 4
def eK0 (O0 p : ℝ) : ℝ := 6 * (p + O0) / ((1 - p) * O0 ^ 2)
def eK1 (O1 p : ℝ) : ℝ := (6 * (1 - p) + 4 * O1) / (p * O1 ^ 2)
def eK01 (O0 O1 : ℝ) : ℝ := 6 / (O0 * O1)
def eM (O0 O1 p alpha : ℝ) : ℝ :=
  -6 * p * (1 - alpha) * (1 + 1 / O0) + alpha * (2 * O1 - 6 * (1 - p) / O1)
def eC (O0 O1 p alpha : ℝ) : ℝ :=
  eK0 O0 p * (1 - alpha) ^ 2 + eK1 O1 p * alpha ^ 2 +
    eK01 O0 O1 * alpha * (1 - alpha)
def eNumerator (box : FrozenEBox) (p s alpha : ℝ) : ℝ :=
  eBase p + s * eM box.outer0 box.outer1 p alpha + s ^ 2 * eC box.outer0 box.outer1 p alpha
def eRatio (box : FrozenEBox) (p s alpha : ℝ) : ℝ :=
  eNumerator box p s alpha / Real.sqrt (p * (1 - p) + s) ^ 3

/-- Accepted analytic theorem: source pointwise_inward_v2 and physical
before-cubic halfplane, under all whole-path gates of FrozenEBox. -/
structure EPointwiseTheorem : Prop where
  necessary : ∀ (X : StandardizedLaw) (b : BinaryModel X) (frame : EFrame X b)
      (box : FrozenEBox), EBoxRealization box frame →
    (Real.sqrt 10 + 1) * X.rho ≤ physicalDefect X +
      eRatio box (positiveProbability X) (noiseVariance X) frame.alpha

structure ERatioBound (box : FrozenEBox) where
  upper : ℚ
  uniform : ∀ p s alpha : ℝ, box.probability.Contains p → box.noise.Contains s →
    box.alpha.Contains alpha → eRatio box p s alpha ≤ (upper : ℝ)

structure RhoCeiling (X : StandardizedLaw) where
  upper : ℚ
  bound : X.rho ≤ (upper : ℝ)

theorem RhoCeiling.excludes {X : StandardizedLaw} (ceiling : RhoCeiling X)
    (lower : ℚ) (actual_lower : (lower : ℝ) ≤ X.rho) (strict : ceiling.upper < lower) : False := by
  have hs : (ceiling.upper : ℝ) < lower := by exact_mod_cast strict
  linarith [ceiling.bound]

def RhoCeiling.refinedInterval {X : StandardizedLaw} (ceiling : RhoCeiling X)
    (prior : ClosedInterval) (notEmpty : prior.lower ≤ ceiling.upper) : ClosedInterval :=
  ⟨prior.lower, min prior.upper ceiling.upper, le_min prior.ordered notEmpty⟩

theorem RhoCeiling.refinement_valid {X : StandardizedLaw} (ceiling : RhoCeiling X)
    (prior : ClosedInterval) (notEmpty : prior.lower ≤ ceiling.upper) (actual : prior.Contains X.rho) :
    (ceiling.refinedInterval prior notEmpty).Contains X.rho := by
  refine ⟨actual.1, ?_⟩
  change X.rho ≤ ((min prior.upper ceiling.upper : ℚ) : ℝ)
  rw [Rat.cast_min]
  exact le_min actual.2 ceiling.bound

def eRhoCeiling {X : StandardizedLaw} {b : BinaryModel X} {frame : EFrame X b}
    {box : FrozenEBox} (realization : EBoxRealization box frame) (analytic : EPointwiseTheorem)
    (ratio : ERatioBound box) (defectCap : ℚ) (defect_bound : physicalDefect X ≤ (defectCap : ℝ))
    (rounded : ℚ) (outward : ((defectCap : ℝ) + (ratio.upper : ℝ)) /
      (Real.sqrt 10 + 1) ≤ (rounded : ℝ)) : RhoCeiling X := by
  have h := analytic.necessary X b frame box realization
  have hr := ratio.uniform _ _ _ realization.probability realization.noise realization.alpha
  have hp : 0 < Real.sqrt 10 + 1 := by positivity
  refine ⟨rounded, ?_⟩
  apply le_trans _ outward
  apply (le_div_iff₀ hp).mpr
  nlinarith

def cubicB (s alpha : ℝ) : ℝ := s * (1 - alpha)
def cubicC (s alpha : ℝ) : ℝ := s * alpha
def compatibleT (p s alpha : ℝ) : ℝ :=
  binaryMomentBase p + 3 * (p * cubicB s alpha + (1 - p) * cubicC s alpha)
def cubicUpper0 (O0 p s alpha : ℝ) : ℝ :=
  cubicB s alpha * O0 - cubicB s alpha ^ 2 / ((1 - p) * O0)
def cubicUpper1 (O1 p s alpha : ℝ) : ℝ :=
  cubicC s alpha * O1 - cubicC s alpha ^ 2 / (p * O1)
def compatibleG0 (p s alpha a z : ℝ) : ℝ :=
  2 * p * (1 - p) ^ 2 * (1 + 2 * p) - 6 * p * (1 - p) * inwardPhi a z +
    6 * cubicB s alpha * (a - p) + 6 * cubicC s alpha * z
def chordZ (box : FrozenEBox) (p s alpha : ℝ) : ℝ := cubicC s alpha / (p * (box.outer1 : ℝ))
def chordConstant (box : FrozenEBox) (p s alpha : ℝ) : ℝ :=
  let z := chordZ box p s alpha
  2 * p * (1 - p) ^ 2 * (1 + 2 * p) - 6 * p * (1 - p) * (z - z ^ 2) +
    6 * cubicC s alpha * z - 6 * cubicB s alpha * p - 2 * compatibleT p s alpha
def chordLinear (box : FrozenEBox) (p s alpha : ℝ) : ℝ :=
  6 * p * (1 - p) * (chordZ box p s alpha - 1) + 8 * cubicB s alpha
def chordQuadratic (p : ℝ) : ℝ := 6 * p * (1 - p)
def chordReciprocal (p s alpha : ℝ) : ℝ := 2 * cubicB s alpha ^ 2 / (1 - p)
def chordNumerator (box : FrozenEBox) (p s alpha a : ℝ) : ℝ :=
  chordConstant box p s alpha + chordLinear box p s alpha * a + chordQuadratic p * a ^ 2 -
    (if a = 0 then 0 else chordReciprocal p s alpha / a)

def rawMomentRatio (box : FrozenEBox) (p s alpha : ℝ) : ℝ :=
  (compatibleT p s alpha + cubicUpper0 box.outer0 p s alpha + cubicUpper1 box.outer1 p s alpha) /
    Real.sqrt (p * (1 - p) + s) ^ 3
def compatiblePlusRatio (box : FrozenEBox) (p s alpha a : ℝ) : ℝ :=
  (compatibleG0 p s alpha a (chordZ box p s alpha) + 2 * cubicUpper1 box.outer1 p s alpha) /
    Real.sqrt (p * (1 - p) + s) ^ 3
def compatibleMinusRatio (box : FrozenEBox) (p s alpha a : ℝ) : ℝ :=
  chordNumerator box p s alpha a / Real.sqrt (p * (1 - p) + s) ^ 3

def retainedLower (box : FrozenEBox) : ℚ :=
  box.noise.lower * (1 - box.alpha.upper) / ((1 - box.probability.lower) * box.outer0)
def retainedUpper (box : FrozenEBox) : ℚ :=
  box.totalInward - box.noise.lower * box.alpha.lower / (box.probability.upper * box.outer1)

structure ChordFeasiblePoint (box : FrozenEBox) (p s alpha a : ℝ) : Prop where
  nonnegative : 0 ≤ a
  variance_lower : s * (1 - alpha) / ((1 - p) * (box.outer0 : ℝ)) ≤ a
  inward_upper : a ≤ (box.totalInward : ℝ) - chordZ box p s alpha
  zero : a = 0 → s * (1 - alpha) = 0

/-- Exactly32 closed retained-a0 cells. The certificate checks their exact
endpoints/seams and supplies the stated union; equality/zero-width cells stay. -/
structure ChordPartition (box : FrozenEBox) where
  cells : List ClosedInterval
  parts : cells.length = 32
  covers : ∀ a : ℝ, (retainedLower box : ℝ) ≤ a → a ≤ (retainedUpper box : ℝ) →
    ∃ cell ∈ cells, cell.Contains a

def reciprocalMaximum (A Z U Bmin : ℝ) : ℝ :=
  if Bmin = 0 then max (U * A) (U * Z)
  else if 0 ≤ U then U * Z - Bmin / Z
  else if Bmin ≤ (-U) * A ^ 2 then U * A - Bmin / A
  else if (-U) * Z ^ 2 ≤ Bmin then U * Z - Bmin / Z
  else -2 * Real.sqrt ((-U) * Bmin)

structure ReciprocalMaximumTheorem : Prop where
  upper : ∀ A Z U Bmin a : ℝ, 0 ≤ A → A ≤ Z → 0 ≤ Bmin →
    (0 < Bmin → 0 < Z) → A ≤ a → a ≤ Z → (Bmin = 0 ∨ 0 < a) →
    U * a - (if Bmin = 0 then 0 else Bmin / a) ≤ reciprocalMaximum A Z U Bmin

structure ChordConsequences {X : StandardizedLaw} {b : BinaryModel X}
    (frame : EFrame X b) (box : FrozenEBox) : Prop where
  retained_lower : (retainedLower box : ℝ) ≤ frame.a0
  retained_upper : frame.a0 ≤ (retainedUpper box : ℝ)
  feasible : ChordFeasiblePoint box (positiveProbability X) (noiseVariance X) frame.alpha frame.a0
  raw : X.rho ≤ rawMomentRatio box (positiveProbability X) (noiseVariance X) frame.alpha
  plus : (Real.sqrt 10 + 1) * X.rho ≤ physicalDefect X +
    compatiblePlusRatio box (positiveProbability X) (noiseVariance X) frame.alpha frame.a0
  minus : (Real.sqrt 10 - 1) * X.rho ≤ physicalDefect X +
    compatibleMinusRatio box (positiveProbability X) (noiseVariance X) frame.alpha frame.a0

structure ChordPathGates (box : FrozenEBox) : Prop where
  negative : box.noise.upper * (1 - box.alpha.lower) / (1 - box.probability.upper) ≤
    box.probability.lower * (1 - 2 * box.totalInward)
  positive : box.noise.upper * box.alpha.upper / box.probability.lower ≤
    (1 - box.probability.upper) * (1 - 2 * box.totalInward)

structure CompatibleChordTheorem : Prop where
  necessary : ∀ (X : StandardizedLaw) (b : BinaryModel X) (frame : EFrame X b)
    (box : FrozenEBox), EBoxRealization box frame → ChordPathGates box → ChordConsequences frame box

structure ChordRatioBounds (box : FrozenEBox) (partition : ChordPartition box) where
  rawUpper : ClosedInterval → ℚ
  plusUpper : ClosedInterval → ℚ
  minusUpper : ClosedInterval → ℚ
  uniform : ∀ cell ∈ partition.cells, ∀ p s alpha a : ℝ,
    box.probability.Contains p → box.noise.Contains s → box.alpha.Contains alpha → cell.Contains a →
    ChordFeasiblePoint box p s alpha a →
    rawMomentRatio box p s alpha ≤ (rawUpper cell : ℝ) ∧
    compatiblePlusRatio box p s alpha a ≤ (plusUpper cell : ℝ) ∧
    compatibleMinusRatio box p s alpha a ≤ (minusUpper cell : ℝ)

def chordRhoCeiling {X : StandardizedLaw} {b : BinaryModel X} {frame : EFrame X b}
    {box : FrozenEBox} (realization : EBoxRealization box frame) (analytic : CompatibleChordTheorem)
    (gates : ChordPathGates box)
    (partition : ChordPartition box) (ratio : ChordRatioBounds box partition)
    (defectCap : ℚ) (defect_bound : physicalDefect X ≤ (defectCap : ℝ))
    (rounded : ℚ) (outward : ∀ cell ∈ partition.cells,
      min (ratio.rawUpper cell : ℝ)
        (min (((defectCap : ℝ) + (ratio.plusUpper cell : ℝ)) / (Real.sqrt 10 + 1))
          (((defectCap : ℝ) + (ratio.minusUpper cell : ℝ)) / (Real.sqrt 10 - 1))) ≤ (rounded : ℝ)) :
    RhoCeiling X := by
  refine ⟨rounded, ?_⟩
  have h := analytic.necessary X b frame box realization gates
  obtain ⟨cell, hmem, ha⟩ := partition.covers frame.a0 h.retained_lower h.retained_upper
  obtain ⟨hr, hp, hm⟩ := ratio.uniform cell hmem _ _ _ _
    realization.probability realization.noise realization.alpha ha h.feasible
  have hplus : 0 < Real.sqrt 10 + 1 := by positivity
  have hminus : 0 < Real.sqrt 10 - 1 := by nlinarith [Real.sqrt_nonneg 10, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 10)]
  have bp : X.rho ≤ ((defectCap : ℝ) + (ratio.plusUpper cell : ℝ)) / (Real.sqrt 10 + 1) := by
    apply (le_div_iff₀ hplus).mpr
    nlinarith [h.plus]
  have bm : X.rho ≤ ((defectCap : ℝ) + (ratio.minusUpper cell : ℝ)) / (Real.sqrt 10 - 1) := by
    apply (le_div_iff₀ hminus).mpr
    nlinarith [h.minus]
  exact (le_min (h.raw.trans hr) (le_min bp bm)).trans (outward cell hmem)

def positiveClosedScore (X : StandardizedLaw) (m : ℕ) (raw : ℝ) : ℝ :=
  Real.sqrt m / X.rho * (ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow X.law m) raw -
    ProbabilityLaw.cdf ProbabilityLaw.standardNormal (raw / Real.sqrt m))

inductive ClosedRawHalfline where | atMost (cut : ℚ) | atLeast (cut : ℚ)

def ClosedRawHalfline.Contains (line : ClosedRawHalfline) (raw : ℝ) : Prop :=
  match line with | .atMost cut => raw ≤ (cut : ℝ) | .atLeast cut => (cut : ℝ) ≤ raw

def abHstar : ℚ := 47 / 4
def abEta : ℚ := 1 / 1000000000000

/-- Exact central raw scope for ONE requested halfline. None means strictly
empty central intersection; equality produces a singleton, never an omission. -/
def clippedRawWindow (line : ClosedRawHalfline) : Option ClosedInterval :=
  match line with
  | .atMost cut =>
    if h : -abHstar ≤ min cut abHstar then some ⟨-abHstar, min cut abHstar, h⟩ else none
  | .atLeast cut =>
    if h : max cut (-abHstar) ≤ abHstar then some ⟨max cut (-abHstar), abHstar, h⟩ else none
def abWeakA (Dcap : ℚ) : ℚ := (997 * 24 / 15000) * Dcap + abEta * abHstar ^ 2
def abWeakBudget (Dcap : ℚ) (raw : ℝ) : ℝ :=
  (15000 / (997 * 24)) * ((abWeakA Dcap : ℝ) - (abEta : ℝ) * raw ^ 2)

theorem abWeakBudget_valid (Dcap : ℚ) (raw : ℝ) (h : |raw| ≤ (abHstar : ℝ)) :
    (Dcap : ℝ) ≤ abWeakBudget Dcap raw := by
  have hs : raw ^ 2 ≤ (abHstar : ℝ) ^ 2 := by
    have hp : 0 ≤ (abHstar : ℝ) := by norm_num [abHstar]
    have hm := mul_self_le_mul_self (abs_nonneg raw) h
    simpa only [← pow_two, sq_abs] using hm
  unfold abWeakBudget abWeakA
  push_cast
  norm_num [abEta, abHstar] at *
  nlinarith

def abJointLambda24 (Lambda25 : ℚ) : ℚ := (24 / 25) * Lambda25
def abNoisePrice24 (price25 : ℚ) : ℚ := (25 / 24) * price25

theorem ab_noise_price_preserved (price25 lambda25 : ℝ) :
    ((25 / 24) * price25) * ((24 / 25) * lambda25) = price25 * lambda25 := by ring

theorem ab_joint_ratio_preserved (Lambda25 lambda25 : ℝ) (h : Lambda25 ≠ 0) :
    ((24 / 25) * lambda25) / ((24 / 25) * Lambda25) = lambda25 / Lambda25 := by
  field_simp

/-- Uniform quantitative predecessor result on the ENTIRE requested closed
raw halfline. Its m=24 is fixed; it does not assert contact/optimality at24. -/
structure ABHalflineBound (X : StandardizedLaw) (line : ClosedRawHalfline) where
  upper : ℚ
  bound : ∀ raw : ℝ, line.Contains raw → positiveClosedScore X 24 raw ≤ (upper : ℝ)

/-- Numerical/analytic meaning of the window plus both exterior tails. These
are three separate quantitative obligations, not the trivial CDF<=1 bound. -/
structure ABWindowAndTails (X : StandardizedLaw) (line : ClosedRawHalfline) where
  windowUpper : ℚ
  leftUpper : ℚ
  rightUpper : ℚ
  window : ∀ raw : ℝ, line.Contains raw → |raw| ≤ (abHstar : ℝ) →
    positiveClosedScore X 24 raw ≤ (windowUpper : ℝ)
  left : ∀ raw : ℝ, line.Contains raw → raw ≤ -(abHstar : ℝ) →
    positiveClosedScore X 24 raw ≤ (leftUpper : ℝ)
  right : ∀ raw : ℝ, line.Contains raw → (abHstar : ℝ) ≤ raw →
    positiveClosedScore X 24 raw ≤ (rightUpper : ℝ)

def ABWindowAndTails.toHalfline {X : StandardizedLaw} {line : ClosedRawHalfline}
    (packet : ABWindowAndTails X line) : ABHalflineBound X line where
  upper := max packet.windowUpper (max packet.leftUpper packet.rightUpper)
  bound := by
    intro raw hline
    rw [Rat.cast_max, Rat.cast_max]
    by_cases hw : |raw| ≤ (abHstar : ℝ)
    · exact (packet.window raw hline hw).trans (le_max_left _ _)
    have hout : raw ≤ -(abHstar : ℝ) ∨ (abHstar : ℝ) ≤ raw := by
      by_cases hn : raw ≤ 0
      · left; rw [abs_of_nonpos hn] at hw; linarith
      · right; rw [abs_of_nonneg (by linarith : 0 ≤ raw)] at hw; linarith
    rcases hout with hl | hr
    · exact (packet.left raw hline hl).trans ((le_max_left _ _).trans (le_max_right _ _))
    · exact (packet.right raw hline hr).trans ((le_max_right _ _).trans (le_max_right _ _))

def abRayAllowance (upper CElo : ℚ) : ℝ := 25 * max ((upper : ℝ) - (CElo : ℝ)) 0

theorem ab_predecessor_allowance {floor : ℝ} (w : ContactAt 25 floor)
    {line : ClosedRawHalfline} (predecessor : ABHalflineBound w.X line) (CElo : ℚ)
    (lower_constant : (CElo : ℝ) ≤ esseenConstant)
    (current : esseenConstant ≤ w.X.normalizedScore 25)
    (raw : ℝ) (inside : line.Contains raw) :
    25 * max (positiveClosedScore w.X 24 raw - w.X.normalizedScore 25) 0 ≤
      abRayAllowance predecessor.upper CElo := by
  have hs := predecessor.bound raw inside
  have hsub : positiveClosedScore w.X 24 raw - w.X.normalizedScore 25 ≤
      (predecessor.upper : ℝ) - (CElo : ℝ) := by linarith
  exact mul_le_mul_of_nonneg_left (max_le_max_right 0 hsub) (by norm_num)

def jointBudgetHolds (data : FrozenJointBudgetData) (totalInward lambda : ℝ) : Prop :=
  match data with
  | .zero => totalInward = 0 ∧ lambda = 0
  | .positive d0 Lambda _ _ => totalInward / (d0 : ℝ) + lambda / (Lambda : ℝ) ≤ 1

def transferredJoint24 : FrozenJointBudgetData → FrozenJointBudgetData
  | .zero => .zero
  | .positive d0 Lambda hd hL => .positive d0 ((24 / 25) * Lambda) hd (by positivity)

theorem ab_joint_budget_preserved (data : FrozenJointBudgetData) (d lambda : ℝ)
    (hbudget : jointBudgetHolds data d lambda) :
    jointBudgetHolds (transferredJoint24 data) d ((24 / 25) * lambda) := by
  cases data with
  | zero =>
    obtain ⟨hd, hl⟩ := hbudget
    simpa [transferredJoint24, jointBudgetHolds, hl] using hd
  | positive d0 Lambda hd hL =>
    have hLR : (Lambda : ℝ) ≠ 0 := by exact_mod_cast hL.ne'
    change d / (d0 : ℝ) + ((24 / 25) * lambda) /
      (((24 / 25 : ℚ) * Lambda : ℚ) : ℝ) ≤ 1
    push_cast
    rw [ab_joint_ratio_preserved _ _ hLR]
    exact hbudget

def jointNoiseIntercept : FrozenJointBudgetData → ℚ
  | .zero => 0
  | .positive _ Lambda _ _ => Lambda

theorem joint_noise_upper (data : FrozenJointBudgetData) (d lambda : ℝ)
    (hd : 0 ≤ d) (hbudget : jointBudgetHolds data d lambda) :
    lambda ≤ (jointNoiseIntercept data : ℝ) := by
  cases data with
  | zero => simpa [jointNoiseIntercept] using hbudget.2.le
  | positive d0 Lambda hd0 hL =>
    have hd0R : (0 : ℝ) < d0 := by exact_mod_cast hd0
    have hLR : (0 : ℝ) < Lambda := by exact_mod_cast hL
    have hn : 0 ≤ d / (d0 : ℝ) := div_nonneg hd hd0R.le
    have hdiv : lambda / (Lambda : ℝ) ≤ 1 := by
      change d / (d0 : ℝ) + lambda / (Lambda : ℝ) ≤ 1 at hbudget
      linarith
    simpa only [one_mul, jointNoiseIntercept] using (div_le_iff₀ hLR).mp hdiv

def transferredDomain24 (ctx : CountTaskContext 25) : OriginalCountDomain 24 where
  probability := ctx.domain.probability
  probability_unit := ctx.domain.probability_unit
  lambdaCap := (24 / 25) * jointNoiseIntercept ctx.jointBudget
  lambda_nonneg := by
    cases ctx.jointBudget with
    | zero => norm_num [jointNoiseIntercept]
    | positive d0 Lambda hd hL => exact mul_nonneg (by norm_num) hL.le
  totalInwardCap := ctx.domain.totalInwardCap
  totalInward_nonneg := ctx.domain.totalInward_nonneg

def abVarianceUpper (ctx : CountTaskContext 25) : ℚ :=
  ctx.domain.probability.upper * (1 - ctx.domain.probability.upper)

/-- Finite numerical input for the same-law24 window. No n25 phase/quadratic
is imported: the domain is new, with all25 roots and the full central phase. -/
structure ABWindowInput where
  original : CountTaskContext 25
  halfline : ClosedRawHalfline
  probability_pos : 0 < original.domain.probability.lower
  probability_lt_half : original.domain.probability.upper < 1 / 2
  noisePrice25 : ℚ
  noisePrice_nonneg : 0 ≤ noisePrice25
  noisePrice_source : noisePrice25 = original.affineBudget.noiseCharge
  leftWindowGate : abHstar ^ 2 *
    (abVarianceUpper original + (transferredDomain24 original).lambdaCap / 24) <
      (24 * original.domain.probability.lower) ^ 2
  rightWindowGate : abHstar ^ 2 *
    (abVarianceUpper original + (transferredDomain24 original).lambdaCap / 24) <
      (24 * (1 - original.domain.probability.upper)) ^ 2
  sourcePin : MathematicalSourcePin

structure ABPhysicalScope {X : StandardizedLaw} {b : BinaryModel X}
    (frame : EFrame X b) (input : ABWindowInput) : Prop where
  probability : input.original.domain.probability.Contains (positiveProbability X)
  rho : input.original.rho.Contains X.rho
  beta : input.original.beta.Contains X.beta
  gamma : input.original.gamma.Contains X.gamma
  fourth : input.original.fourth.Contains (fourthMoment X)
  fifth : input.original.fifth.Contains (absoluteFifthMoment X)
  mean : input.original.mean.Contains (positiveFirstMoment X)
  fourth_integrable : Integrable (fun x : ℝ => x ^ 4) (X.law : Measure ℝ)
  fifth_integrable : Integrable (fun x : ℝ => |x| ^ 5) (X.law : Measure ℝ)
  negative_support : ∀ᵐ x ∂(X.law : Measure ℝ), -(input.original.negativeRadius : ℝ) ≤ x
  positive_support : ∀ᵐ x ∂(X.law : Measure ℝ), x ≤ (input.original.positiveRadius : ℝ)
  conditional_outer0 : ∀ᵐ u ∂(b.negativeLaw : Measure ℝ),
    -(input.original.conditionalOuter0 : ℝ) ≤ u ∧ u ≤ frame.a0
  conditional_outer1 : ∀ᵐ u ∂(b.positiveLaw : Measure ℝ),
    -frame.a1 ≤ u ∧ u ≤ (input.original.conditionalOuter1 : ℝ)
  physical_gap : ∃ gap : SupportGap X, gap.val.1 < 0 ∧ 0 < gap.val.2 ∧
    frame.a0 = positiveProbability X + inverseBinaryScale X * gap.val.1 ∧
    frame.a1 = (1 - positiveProbability X) - inverseBinaryScale X * gap.val.2
  lambda : weightedNoise X 25 ≤ (input.original.domain.lambdaCap : ℝ)
  inward : frame.a0 + frame.a1 ≤ (input.original.domain.totalInwardCap : ℝ)
  weighted_defect : WeightedDefectCap X 25 input.original.floorIndex input.original.defectCap
  native_defect : physicalDefect X ≤ (input.original.nativeDefectCap : ℝ)
  joint : jointBudgetHolds input.original.jointBudget (frame.a0 + frame.a1) (weightedNoise X 25)
  affine : (input.original.affineBudget.binaryCharge : ℝ) +
    (input.original.affineBudget.gapCharge : ℝ) * (frame.a0 + frame.a1) +
    (input.original.affineBudget.noiseCharge : ℝ) * weightedNoise X 25 ≤ physicalDefect X

theorem ab_affine_budget_preserved {X : StandardizedLaw} {b : BinaryModel X}
    {frame : EFrame X b} {input : ABWindowInput} (scope : ABPhysicalScope frame input) :
    (input.original.affineBudget.binaryCharge : ℝ) +
      (input.original.affineBudget.gapCharge : ℝ) * (frame.a0 + frame.a1) +
      ((abNoisePrice24 input.noisePrice25 : ℚ) : ℝ) * weightedNoise X 24 ≤ physicalDefect X := by
  rw [n25_to_n24_noise]
  unfold abNoisePrice24
  push_cast
  rw [ab_noise_price_preserved]
  rw [input.noisePrice_source]
  exact scope.affine

def abCountPoint {X : StandardizedLaw} {b : BinaryModel X}
    (frame : EFrame X b) (raw : ℝ) (k : Fin 25) : CountPoint 24 :=
  ⟨k, positiveProbability X, weightedNoise X 24, frame.alpha,
    24 * positiveProbability X + inverseBinaryScale X * raw - k.val, frame.a0⟩

theorem ab_point_membership {X : StandardizedLaw} {b : BinaryModel X}
    {frame : EFrame X b} {input : ABWindowInput} (scope : ABPhysicalScope frame input)
    (raw : ℝ) (k : Fin 25)
    (phase : -1 / 2 ≤ (abCountPoint frame raw k).phase ∧ (abCountPoint frame raw k).phase ≤ 1 / 2) :
    (transferredDomain24 input.original).Contains (abCountPoint frame raw k) := by
  refine ⟨rfl, ?_⟩
  intro c
  cases c with
  | probability => exact scope.probability
  | weightedNoise =>
    have hl : (0 : ℝ) ≤ weightedNoise X 24 := mul_nonneg (by norm_num) b.noise_nonneg
    have hj : weightedNoise X 25 ≤ (jointNoiseIntercept input.original.jointBudget : ℝ) :=
      joint_noise_upper _ _ _ (add_nonneg frame.a0_nonneg frame.a1_nonneg) scope.joint
    have hu : weightedNoise X 24 ≤ (24 / 25 : ℝ) * (jointNoiseIntercept input.original.jointBudget : ℝ) := by
      rw [n25_to_n24_noise]
      exact mul_le_mul_of_nonneg_left hj (by norm_num)
    simpa [CountPoint.coordinate, abCountPoint, transferredDomain24,
      OriginalCountDomain.rootBox, ClosedInterval.Contains] using And.intro hl hu
  | alpha =>
    simpa [CountPoint.coordinate, abCountPoint, transferredDomain24,
      OriginalCountDomain.rootBox, ClosedInterval.Contains] using
      And.intro frame.alpha_nonneg frame.alpha_le_one
  | phase =>
    norm_num [CountPoint.coordinate, abCountPoint, transferredDomain24,
      OriginalCountDomain.rootBox, ClosedInterval.Contains] at phase ⊢
    exact phase
  | rawInward0 =>
    have hu : frame.a0 ≤ (input.original.domain.totalInwardCap : ℝ) := by
      linarith [scope.inward, frame.a1_nonneg]
    simpa [CountPoint.coordinate, abCountPoint, transferredDomain24,
      OriginalCountDomain.rootBox, ClosedInterval.Contains] using And.intro frame.a0_nonneg hu

/-- Count conditioning for every raw24 threshold; no optimality or contact
at24 is present. The accepted count source theorem supplies this identity. -/
structure ABCountIdentity (X : StandardizedLaw) (b : BinaryModel X) : Prop where
  identity : ∀ raw : ℝ, ProbabilityLaw.cdf (ProbabilityLaw.convolutionPow X.law 24) raw =
    ∑ k : Fin 25, binomialMass 24 (positiveProbability X) k * incomingProbability b k
      (24 * positiveProbability X + inverseBinaryScale X * raw - k.val)

structure ABWindowScopeTheorem : Prop where
  central : ∀ (X : StandardizedLaw) (b : BinaryModel X) (frame : EFrame X b)
    (input : ABWindowInput), ABPhysicalScope frame input → ∀ raw : ℝ,
    |raw| ≤ (abHstar : ℝ) →
      0 ≤ 24 * positiveProbability X + inverseBinaryScale X * raw ∧
        24 * positiveProbability X + inverseBinaryScale X * raw ≤ 24

/-- The semantic numerical output of complete native24 window calls. Every
leaf bound is quantitative, for the same unreflected law and full new phase.
An unresolved native score may be used if its returned upper bound is valid;
the early-exit target CE_LO+1/100 is not substituted for that returned bound. -/
structure ABWindowCountPacket {X : StandardizedLaw} {b : BinaryModel X}
    (frame : EFrame X b) (input : ABWindowInput) where
  scope : ABPhysicalScope frame input
  scopeTheorem : ABWindowScopeTheorem
  identity : ABCountIdentity X b
  forest : CountLeafCover (transferredDomain24 input.original)
  leafUpper : CountBox 24 → ℚ
  upper : ℚ
  maxima : ∀ leaf ∈ forest.leaves, leafUpper leaf ≤ upper
  leaf_meaning : ∀ leaf ∈ forest.leaves, ∀ raw : ℝ, input.halfline.Contains raw →
    |raw| ≤ (abHstar : ℝ) → ∀ k : Fin 25,
      leaf.Contains (abCountPoint frame raw k) → ABCountIdentity X b →
        positiveClosedScore X 24 raw ≤ (leafUpper leaf : ℝ)

theorem ABWindowCountPacket.window_bound {X : StandardizedLaw} {b : BinaryModel X}
    {frame : EFrame X b} {input : ABWindowInput} (packet : ABWindowCountPacket frame input)
    (raw : ℝ) (halfline : input.halfline.Contains raw) (window : |raw| ≤ (abHstar : ℝ)) :
    positiveClosedScore X 24 raw ≤ (packet.upper : ℝ) := by
  obtain ⟨hl, hu⟩ := packet.scopeTheorem.central X b frame input packet.scope raw window
  have confined : PhaseConfinement 24
      (24 * positiveProbability X + inverseBinaryScale X * raw) :=
    ⟨by linarith, by norm_num; linarith⟩
  obtain ⟨k, hphase⟩ := nearest_root_exists 24 _ confined
  have inside := ab_point_membership packet.scope raw k hphase
  obtain ⟨leaf, hmem, hleaf⟩ := packet.forest.cover (abCountPoint frame raw k) inside
  have hm : (packet.leafUpper leaf : ℝ) ≤ packet.upper := by exact_mod_cast packet.maxima leaf hmem
  exact (packet.leaf_meaning leaf hmem raw halfline window k hleaf packet.identity).trans hm

def abNegativeTailScalar (rhoLower negativeRadius : ℚ) : ℝ :=
  let R := (negativeRadius : ℝ)
  let M := 1 + (Real.exp (R / 3) - 1 - R / 3) / R ^ 2
  (49 / 10) / (rhoLower : ℝ) * M ^ 24 * Real.exp (-(abHstar : ℝ) / 3)
def abPositiveTailScalar (rhoLower : ℚ) : ℝ :=
  ((49 / 10) ^ 2 / (rhoLower : ℝ)) * (2 / (5 * (abHstar : ℝ))) *
    Real.exp (-(abHstar : ℝ) ^ 2 / 48)

structure ABExteriorTailTheorem : Prop where
  negative : ∀ (X : StandardizedLaw) (rhoLower Rminus : ℚ), 0 < rhoLower → 0 < Rminus →
    (rhoLower : ℝ) ≤ X.rho → (∀ᵐ x ∂(X.law : Measure ℝ), -(Rminus : ℝ) ≤ x) →
    ∀ raw : ℝ, raw ≤ -(abHstar : ℝ) →
      positiveClosedScore X 24 raw ≤ abNegativeTailScalar rhoLower Rminus
  positive : ∀ (X : StandardizedLaw) (rhoLower : ℚ), 0 < rhoLower →
    (rhoLower : ℝ) ≤ X.rho → ∀ raw : ℝ, (abHstar : ℝ) ≤ raw →
      positiveClosedScore X 24 raw ≤ abPositiveTailScalar rhoLower

structure ABTailNumericalBounds (input : ABWindowInput) where
  negativeUpper : ℚ
  positiveUpper : ℚ
  negative : abNegativeTailScalar input.original.rho.lower input.original.negativeRadius ≤ (negativeUpper : ℝ)
  positive : abPositiveTailScalar input.original.rho.lower ≤ (positiveUpper : ℝ)

def ABWindowCountPacket.completeHalfline {X : StandardizedLaw} {b : BinaryModel X}
    {frame : EFrame X b} {input : ABWindowInput} (packet : ABWindowCountPacket frame input)
    (analytic : ABExteriorTailTheorem) (tails : ABTailNumericalBounds input) :
    ABHalflineBound X input.halfline :=
  ABWindowAndTails.toHalfline {
    windowUpper := packet.upper
    leftUpper := tails.negativeUpper
    rightUpper := tails.positiveUpper
    window := packet.window_bound
    left := fun raw _hline hraw =>
      (analytic.negative X _ _ input.original.rho_positive input.original.negativeRadius_pos
        packet.scope.rho.1 packet.scope.negative_support raw hraw).trans tails.negative
    right := fun raw _hline hraw =>
      (analytic.positive X _ input.original.rho_positive packet.scope.rho.1 raw hraw).trans tails.positive }

inductive SupportRay where | positive (radius : ℚ) | negative (radius : ℚ)

def SupportRay.Contains (ray : SupportRay) (y : ℝ) : Prop :=
  match ray with | .positive R => (R : ℝ) ≤ y | .negative R => y ≤ -(R : ℝ)
def SupportRay.requiredHalfline (ray : SupportRay) (rawH : ClosedInterval) : ClosedRawHalfline :=
  match ray with
  | .positive R => .atMost (rawH.upper - R)
  | .negative R => .atLeast (rawH.lower + R)

theorem SupportRay.predecessor_inside (ray : SupportRay) (rawH : ClosedInterval)
    (H y : ℝ) (hH : rawH.Contains H) (hy : ray.Contains y) :
    (ray.requiredHalfline rawH).Contains (H - y) := by
  cases ray with
  | positive R =>
    change H - y ≤ ((rawH.upper - R : ℚ) : ℝ)
    push_cast
    change (R : ℝ) ≤ y at hy
    linarith [hH.2]
  | negative R =>
    change ((rawH.lower + R : ℚ) : ℝ) ≤ H - y
    push_cast
    change y ≤ -(R : ℝ) at hy
    linarith [hH.1]

end BEMap.Mixed
