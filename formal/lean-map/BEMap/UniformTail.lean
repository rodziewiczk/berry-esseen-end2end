import BEMap.Binary
import BEMap.Certificates

/-! The all-index local-comparison contract. Frozen packets contain only
rational data. Unknown laws, contact thresholds and actual indices are proof
quantifiers. Analytic acquisition/normalization/kernel premises are explicit;
the final zero/positive-noise composition is checked below. -/
noncomputable section
open MeasureTheory Set
namespace BEMap.UniformTail

def calculationFloor : ℕ := 47
def localEpsilon : ℚ := 1 / 1000

structure UniformLocalAssumptions {n : ℕ} (w : ContraryContact n) : Prop where
  n_ge47 : 47 ≤ n
  excess_nonnegative : 0 ≤ w.X.normalizedScore n - esseenConstant
  excess_le : w.X.normalizedScore n - esseenConstant ≤ (7 / 10 : ℝ) / n
  decrement : (n : ℝ) * max (optimalConstant (n - 1) - optimalConstant n) 0 ≤ 19 / 100
  current : w.X.normalizedScore n < 4247 / 10000
  previousOne : optimalConstant (n - 1) < 4253 / 10000
  previousTwo : optimalConstant (n - 2) < 4253 / 10000

/-- 38 left rows followed by 45 central rows. Row38 is the .38 seam.
These panels cover an ACQUIRED probability range, not every law. -/
def panelProbability (j : Fin 83) : ClosedInterval where
  lower := (152 + (j.val : ℚ)) / 500
  upper := (153 + (j.val : ℚ)) / 500
  ordered := by linarith

private theorem closed_grid_cover (m : ℕ) (a step x : ℝ) (_hs : 0 ≤ step)
    (hx : a ≤ x ∧ x ≤ a + ((m : ℝ) + 1) * step) :
    ∃ j : Fin (m + 1), a + (j.val : ℝ) * step ≤ x ∧
      x ≤ a + ((j.val : ℝ) + 1) * step := by
  induction m with
  | zero => exact ⟨⟨0, by omega⟩, by simpa using hx⟩
  | succ m ih =>
    by_cases h : x ≤ a + ((m : ℝ) + 1) * step
    · obtain ⟨j, hj⟩ := ih ⟨hx.1, h⟩
      exact ⟨j.castSucc, hj⟩
    · refine ⟨⟨m + 1, by omega⟩, ?_, ?_⟩
      · push_cast; linarith
      · push_cast at hx ⊢; linarith

theorem panel_probability_cover {p : ℝ} (hp : 38 / 125 ≤ p ∧ p ≤ 47 / 100) :
    ∃ j : Fin 83, (panelProbability j).Contains p := by
  obtain ⟨j, hj⟩ := closed_grid_cover 82 (152 / 500) (1 / 500) p (by norm_num)
    (by norm_num; constructor <;> linarith [hp.1, hp.2])
  refine ⟨j, ?_⟩
  simp only [ClosedInterval.Contains, panelProbability, Rat.cast_div,
    Rat.cast_add, Rat.cast_natCast, Rat.cast_ofNat]
  constructor <;> linarith [hj.1, hj.2]

def conditionalSecond {X : StandardizedLaw} (b : BinaryModel X) (positive : Bool) : ℝ :=
  ∫ u : ℝ, u ^ 2 ∂(if positive then b.positiveLaw else b.negativeLaw : Measure ℝ)

def bernoulliRho (p : ℝ) : ℝ := (1 - 2 * p * (1 - p)) / Real.sqrt (p * (1 - p))
def binomialCDF (n : ℕ) (p : ℝ) (k : Fin (n + 1)) : ℝ :=
  ∑ j : Fin (n + 1), if j.val ≤ k.val then binomialMass n p j else 0
def normalCDF (z : ℝ) : ℝ := ProbabilityLaw.cdf ProbabilityLaw.standardNormal z

/-- All coordinates belong to the actual same oriented law. The two
conditional supports include atoms and deterministic conditional laws. -/
structure LocalFrame {n : ℕ} (w : ContraryContact n) where
  binary : BinaryModel w.X
  at_least_47 : 47 ≤ n
  probability_half : positiveProbability w.X ≤ 1 / 2
  a0 : ℝ
  a1 : ℝ
  a0_nonneg : 0 ≤ a0
  a1_nonneg : 0 ≤ a1
  negative_second_integrable : Integrable (fun u : ℝ => u ^ 2) (binary.negativeLaw : Measure ℝ)
  positive_second_integrable : Integrable (fun u : ℝ => u ^ 2) (binary.positiveLaw : Measure ℝ)
  variance_mixture : noiseVariance w.X =
    (1 - positiveProbability w.X) * conditionalSecond binary false +
      positiveProbability w.X * conditionalSecond binary true
  negative_inward : ∀ᵐ u ∂(binary.negativeLaw : Measure ℝ), u ≤ a0
  positive_inward : ∀ᵐ u ∂(binary.positiveLaw : Measure ℝ), -a1 ≤ u
  root : Fin (n + 1)
  root_positive : 1 ≤ root.val
  root_below_n : root.val < n
  phase_lower : -1 / 2 ≤ countPhase w root
  phase_upper : countPhase w root ≤ 1 / 2
  scale_positive : 0 < inverseBinaryScale w.X
  score_positive : (2 / 5 : ℝ) ≤ w.X.normalizedScore n
  count_identity : CountIdentity w binary

def LocalFrame.p {n : ℕ} {w : ContraryContact n} (_f : LocalFrame w) := positiveProbability w.X
def LocalFrame.v {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) := f.p * (1 - f.p)
def LocalFrame.ell {n : ℕ} {w : ContraryContact n} (_f : LocalFrame w) := (inverseBinaryScale w.X)⁻¹
def LocalFrame.noise {n : ℕ} {w : ContraryContact n} (_f : LocalFrame w) := weightedNoise w.X n
def LocalFrame.phase {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) := countPhase w f.root
def LocalFrame.delta {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) := (f.root.val : ℝ) - n * f.p
def LocalFrame.mass {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) := binomialMass n f.p f.root
def LocalFrame.massScaled {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) := Real.sqrt n * f.mass
def LocalFrame.bernoulliScore {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) :=
  Real.sqrt n / bernoulliRho f.p *
    (binomialCDF n f.p f.root - normalCDF (f.delta / Real.sqrt ((n : ℝ) * f.v)))
def LocalFrame.normalPhase {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) :=
  (normalCDF ((f.delta + f.phase) / Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X))) -
    normalCDF (f.delta / Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X)))) / f.mass
def LocalFrame.cdfCorrection {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) :=
  rawCDF w - binomialCDF n f.p f.root
def LocalFrame.repair {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) :=
  Real.sqrt n * (normalCDF (f.delta / Real.sqrt ((n : ℝ) * f.v)) -
    normalCDF (f.delta / Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X)))) +
      w.X.normalizedScore n * (bernoulliRho f.p - w.X.rho)
def LocalFrame.comparison {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) :=
  bernoulliRho f.p * (w.X.normalizedScore n - f.bernoulliScore)

def signedQuadratic (q : SignedDefectQuadraticData) (H : ℝ) : ℝ :=
  (q.constant : ℝ) + (if 0 ≤ H then q.positiveLinear else q.negativeLinear) * |H| -
    (q.curvature : ℝ) * H ^ 2

structure PanelData where
  sourcePin : MathematicalSourcePin
  actualRadius : ℚ
  radius_positive : 0 < actualRadius
  radius_le_entry : actualRadius ≤ 96 / 25
  rho : ClosedInterval
  beta : ClosedInterval
  gamma : ClosedInterval
  mean : ClosedInterval
  mean_positive : 0 < mean.lower
  fourth : ℚ
  fifth : ℚ
  threshold : ClosedInterval
  inverseScale : ClosedInterval
  scale_positive : 0 < inverseScale.lower
  theta : ℚ
  theta_nonneg : 0 ≤ theta
  theta_lt_one : theta < 1
  inward : ℚ
  inward_positive : 0 < inward
  inward_lt_p : inward < 38 / 125
  amplitude : ℚ
  amplitude_positive : 0 < amplitude
  inward_le_amplitude : inward ≤ amplitude
  noiseUpper : ℚ
  noise_positive : 0 < noiseUpper
  weightedDefect : ℚ
  weightedDefect_nonneg : 0 ≤ weightedDefect
  budgetCeiling : ℚ
  quadratics : Fin 4 → SignedDefectQuadraticData
  affine : AffineDefectBudgetData

/-- MAX of the four coherent corner quadratics, then MIN with the scalar
ceiling. The phase price is already included in every curvature. -/
def PanelData.budget (row : PanelData) (H : ℝ) : ℝ :=
  min (row.budgetCeiling : ℝ)
    (max (max (signedQuadratic (row.quadratics 0) H) (signedQuadratic (row.quadratics 1) H))
      (max (signedQuadratic (row.quadratics 2) H) (signedQuadratic (row.quadratics 3) H)))

structure PanelScope {n : ℕ} {w : ContraryContact n} (f : LocalFrame w)
    (index : Fin 83) (row : PanelData) : Prop where
  gaps : GapEvidence w
  probability : (panelProbability index).Contains f.p
  entry_support : AlmostBounded w.X (96 / 25)
  support : AlmostBounded w.X row.actualRadius
  rho : row.rho.Contains w.X.rho
  beta : row.beta.Contains w.X.beta
  gamma : row.gamma.Contains w.X.gamma
  mean : row.mean.Contains (positiveFirstMoment w.X)
  fourth_integrable : Integrable (fun x : ℝ => x ^ 4) (w.X.law : Measure ℝ)
  fifth_integrable : Integrable (fun x : ℝ => |x| ^ 5) (w.X.law : Measure ℝ)
  fourth : fourthMoment w.X ≤ (row.fourth : ℝ)
  fifth : absoluteFifthMoment w.X ≤ (row.fifth : ℝ)
  threshold : row.threshold.Contains w.rawThreshold.value
  inverseScale : row.inverseScale.Contains (inverseBinaryScale w.X)
  theta : residualTheta w.X ≤ (row.theta : ℝ)
  inward : f.a0 + f.a1 ≤ (row.inward : ℝ)
  negative_amplitude : ∀ᵐ u ∂(f.binary.negativeLaw : Measure ℝ), |u| ≤ (row.amplitude : ℝ)
  positive_amplitude : ∀ᵐ u ∂(f.binary.positiveLaw : Measure ℝ), |u| ≤ (row.amplitude : ℝ)
  weighted_noise : f.noise ≤ (row.noiseUpper : ℝ)
  weighted_defect : (n : ℝ) * physicalDefect w.X ≤ 47 * (row.weightedDefect : ℝ)
  strict_budget : (n : ℝ) * physicalDefect w.X < (15000 / 997 : ℝ) * row.budget w.rawThreshold.value
  affine_budget : (row.affine.binaryCharge : ℝ) + row.affine.gapCharge * (f.a0 + f.a1) +
    row.affine.noiseCharge * residualTheta w.X ≤ physicalDefect w.X

/-- Selected source regimes; the geometric domains are closed except that
the tiny branch explicitly requires strictly positive noise. -/
inductive Family where | tiny | centralMid | leftMid | centralLow | leftLow | leftPositiveLow
deriving DecidableEq

structure LocalCell where
  panel : Fin 83
  family : Family
  threshold : ClosedInterval
  noise : ClosedInterval
  noise_nonneg : 0 ≤ noise.lower
  noise_upper_positive : 0 < noise.upper
  phase : ClosedInterval
  phase_lower : -1 / 2 ≤ phase.lower
  phase_upper : phase.upper ≤ 1 / 2

def LocalCell.Contains {n : ℕ} {w : ContraryContact n} (cell : LocalCell) (f : LocalFrame w) : Prop :=
  cell.threshold.Contains w.rawThreshold.value ∧ cell.noise.Contains f.noise ∧ cell.phase.Contains f.phase

structure FrozenLocalContext where
  rows : Fin 83 → PanelData
  cells : List LocalCell
  cover : ∀ (j : Fin 83) (H noise phase : ℝ),
    (rows j).threshold.Contains H → 0 < noise → noise ≤ ((rows j).noiseUpper : ℝ) →
    -1 / 2 ≤ phase → phase ≤ 1 / 2 →
    ∃ cell ∈ cells, cell.panel = j ∧ cell.threshold.Contains H ∧
      cell.noise.Contains noise ∧ cell.phase.Contains phase

/-- Exact Stirling/normal-CDF normalization packet, all evaluated at N=47.
The semantic theorem below licenses these constants for every actual n>=N. -/
structure Normalizer where
  probability : ClosedInterval
  p_positive : 0 < probability.lower
  p_below_half : probability.upper < 1 / 2
  delta : ℚ
  delta_ge_one : 1 ≤ delta
  segment : ClosedInterval
  segment_positive : 0 < segment.lower
  segment_below_half : segment.upper < 1 / 2
  segment_left : segment.lower < probability.lower - delta / 47
  segment_right : probability.upper + delta / 47 < segment.upper
  entropyThird : ℚ
  logVarianceDerivative : ℚ
  factorialRemainder : ℚ
  entropy_positive : 0 < entropyThird
  log_positive : 0 < logVarianceDerivative
  factorial_positive : 0 < factorialRemainder
  varianceLower : ℚ
  variance_positive : 0 < varianceLower
  variance_licensed : ∀ p : ℝ, probability.Contains p → (varianceLower : ℝ) ≤ p * (1 - p)
  mass : ℚ
  mass_positive : 0 < mass
  logCoefficient : ℚ
  logCap : ℚ
  logCap_positive : 0 < logCap
  logCap_lt_one : logCap < 1
  noiseUpper : ℚ
  noise_positive : 0 < noiseUpper
  inward : ℚ
  inward_nonneg : 0 ≤ inward
  inward_lt_p : inward < probability.lower
  cv : ℚ
  cv_positive : 0 < cv
  cv_licensed : 1 ≤ cv * probability.lower
  derivativeLower : ℚ
  derivativeUpper : ℚ
  derivative_lower_positive : 0 < derivativeLower
  derivative_ordered : derivativeLower ≤ derivativeUpper
  repairMultiplier : ℚ
  repairPositive : ℚ
  cubicBracket : ℚ
  multiplier_positive : 0 < repairMultiplier
  normal_positive : 0 < repairPositive
  cubic_positive : 0 < cubicBracket

def Normalizer.zeta (c : Normalizer) (D : ℝ) : ℝ :=
  c.logVarianceDerivative * D / 2 + c.factorialRemainder + c.entropyThird * D ^ 3 / (6 * 47)
def Normalizer.phaseError (c : Normalizer) (D a : ℝ) : ℝ :=
  (2 * D * a + a ^ 2) / (2 * (c.varianceLower : ℝ)) + c.zeta D
def Normalizer.expFactor (c : Normalizer) : ℝ := (1 - (c.logCap : ℝ))⁻¹

/-- Named analytic normalizer contract. Exact scalar source inequalities,
including mode coverage, are retained rather than an arbitrary mass premise. -/
structure NormalizerGates (c : Normalizer) : Prop where
  entropy : ∀ r : ℝ, c.segment.Contains r →
    (1 - 2 * r) / (r ^ 2 * (1 - r) ^ 2) ≤ (c.entropyThird : ℝ)
  log_variance : ∀ r : ℝ, c.segment.Contains r →
    (1 - 2 * r) / (r * (1 - r)) ≤ (c.logVarianceDerivative : ℝ)
  factorial : ∀ r : ℝ, c.segment.Contains r →
    1 / (12 * r * (1 - r)) ≤ (c.factorialRemainder : ℝ)
  mass : (c.mass : ℝ) < (39886 / 100000 : ℝ) /
    Real.sqrt ((c.probability.upper : ℝ) * (1 - c.probability.upper)) *
      (1 - ((c.delta : ℝ) ^ 2 / (2 * c.varianceLower) + c.zeta c.delta) / 47)
  all_modes : (c.varianceLower : ℝ) * (1 - c.zeta c.delta / 47) ^ 2 > (2 / 5 : ℝ) ^ 2
  mode_error : c.zeta c.delta < 47
  logCoefficient : (c.logCoefficient : ℝ) >
    1 / (2 * c.varianceLower) + (c.delta : ℝ) ^ 2 / (2 * 47 * (c.varianceLower : ℝ) ^ 2)
  logCap : ((c.logCoefficient : ℝ) * c.noiseUpper + c.phaseError c.delta (1 / 2)) / 47 < c.logCap
  derivativeLower : (c.derivativeLower : ℝ) ≤ 1 - c.expFactor *
    ((c.logCoefficient : ℝ) * c.noiseUpper + c.phaseError c.delta (1 / 2)) / 47
  derivativeUpper : 1 + c.expFactor *
    ((c.logCoefficient : ℝ) * c.noiseUpper + c.phaseError c.delta (1 / 2)) / 47 ≤ c.derivativeUpper
  repairMultiplier : (c.repairMultiplier : ℝ) ≤ (2 / 5 : ℝ) /
    (((c.probability.upper : ℝ) * (1 - c.probability.upper) + c.noiseUpper / 47) ^ (3 / 2 : ℝ))
  repairPositive : (2 / 5 : ℝ) / (2 * (c.varianceLower : ℝ) ^ (3 / 2 : ℝ)) ≤ c.repairPositive
  cubicLower : ∀ p s : ℝ, c.probability.Contains p → 0 ≤ s → s ≤ (c.noiseUpper : ℝ) / 47 →
    (c.cubicBracket : ℝ) ≤ 6 * p - 3 * p ^ 2 - 3 / 2 - c.inward -
      3 * (1 - 2 * p * (1 - p)) * s / (8 * p * (1 - p))
  ratio_denominator : 0 < 1 - (c.delta - 1) / (47 * c.probability.lower)
  ratio_all_counts : c.probability.upper + c.delta < 2

/-- Positive-noise normalizations concern the actual count and all binomial
modes. The separate all-modes upper bound is used by whole-count kernels. -/
structure Normalization {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) (c : Normalizer) : Prop where
  p_scope : c.probability.Contains f.p
  delta_scope : |f.delta| ≤ (c.delta : ℝ)
  noise_scope : f.noise ≤ (c.noiseUpper : ℝ)
  inward_scope : f.a0 + f.a1 ≤ (c.inward : ℝ)
  mass_lower : (c.mass : ℝ) ≤ f.massScaled
  mass_upper : f.massScaled ≤ 1
  all_modes_upper : ∀ j : Fin (n + 1), Real.sqrt n * binomialMass n f.p j ≤ 1
  normal_derivative : ∀ u : ℝ, -1 / 2 ≤ u → u ≤ 1 / 2 →
    (c.derivativeLower : ℝ) ≤
      phi ((f.delta + u) / Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X))) /
        (Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X)) * f.mass) ∧
    phi ((f.delta + u) / Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X))) /
        (Real.sqrt ((n : ℝ) * (f.v + noiseVariance w.X)) * f.mass) ≤ (c.derivativeUpper : ℝ)

def MasterIdentityTheorem : Prop :=
  ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w),
    f.comparison = f.massScaled * (f.cdfCorrection / f.mass - f.normalPhase) + f.repair

/-- SMALL/TINY stores bounds proportional to lambda; MID stores absolute
bounds. A zero lower endpoint never turns into a positive lambda floor. -/
structure NearestPacket where
  scaled : Bool
  own : ℚ
  incoming : ℚ
  ratio : ℚ
  repair : ℚ
  own_nonneg : 0 ≤ own
  incoming_nonneg : 0 ≤ incoming
  ratio_nonneg : 0 ≤ ratio
  repair_nonneg : 0 ≤ repair
  mass : ℚ
  mass_positive : 0 < mass
  noiseUpper : ℚ
  noise_positive : 0 < noiseUpper
  bracket_positive : 0 < own - ratio * incoming
  acceptance : if scaled then mass * (own - ratio * incoming) - repair / 47 > localEpsilon
    else mass * (own - ratio * incoming) - repair * noiseUpper / 47 > localEpsilon * noiseUpper

def NearestPacket.factor (packet : NearestPacket) (noise : ℝ) : ℝ := if packet.scaled then noise else 1

structure NearestMeaning {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) (packet : NearestPacket) : Prop where
  noise_positive : 0 < f.noise
  noise_upper : f.noise ≤ (packet.noiseUpper : ℝ)
  mass_lower : (packet.mass : ℝ) ≤ f.massScaled
  own : (packet.own : ℝ) * packet.factor f.noise ≤
    strictOutgoingProbability f.binary f.root f.phase + f.normalPhase
  incoming : (∑ j : Fin (n + 1), if f.root.val < j.val then
    incomingProbability f.binary j (f.phase - ((j.val : ℝ) - f.root.val)) else 0) ≤
      (packet.incoming : ℝ) * packet.factor f.noise
  ratios : ∀ j : Fin (n + 1), f.root.val < j.val →
    binomialMass n f.p j / f.mass ≤ (packet.ratio : ℝ)
  repair : f.repair ≤ (packet.repair : ℝ) * f.noise / n

/-- Source nearest-count conditioning and sign-aware N relaxation. This is
an accepted analytic theorem, not a final score field in a certificate. -/
def NearestComparisonTheorem : Prop := MasterIdentityTheorem →
  ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w) (packet : NearestPacket),
    NearestMeaning f packet → f.comparison < -(localEpsilon : ℝ) * f.noise

structure WholePacket where
  noise : ClosedInterval
  noise_lower_positive : 0 < noise.lower
  mass : ℚ
  mass_positive : 0 < mass
  amplitude : ℚ
  inward : ℚ
  cv : ℚ
  omegaLower : ℚ
  omegaUpper : ℚ
  deltaBound : ℚ
  delta_nonnegative : 0 ≤ deltaBound
  varianceLower : ℚ
  amplitude_positive : 0 < amplitude
  inward_positive : 0 < inward
  inward_lt_half : inward < 1 / 2
  inward_le_amplitude : inward ≤ amplitude
  span_lt_half : amplitude + inward < 1 / 2
  omegaLower_positive : 0 < omegaLower
  omegaUpper_positive : 0 < omegaUpper
  omegaLower_exact : omegaLower = 1 - cv * deltaBound / 47
  omegaUpper_exact : omegaUpper = 1 + cv * deltaBound / 47
  variance_positive : 0 < varianceLower
  cv_positive : 0 < cv
  inwardWeighted : ℚ
  inwardWeighted_positive : 0 < inwardWeighted
  inward_variance_gate : inwardWeighted ^ 2 < cv * 47 * noise.lower
  markScale : ℚ
  mark_positive : 0 < markScale
  mark_upper : markScale * noise.upper ≤ 1
  kernel : ℚ
  kernel_nonnegative : 0 ≤ kernel
  rate : ℚ
  rate_positive : 0 < rate
  rate_upper : rate * noise.upper < 3
  gain : ℚ
  curvature : ℚ
  phaseRadius : ℚ
  normalVariance : ℚ
  normalPhase : ℚ
  repairPositive : ℚ
  deltaPositive : ℚ
  repairMultiplier : ℚ
  cubicBracket : ℚ
  curvature_nonnegative : 0 ≤ curvature
  normalVariance_nonnegative : 0 ≤ normalVariance
  normalPhase_nonnegative : 0 ≤ normalPhase
  phaseRadius_nonnegative : 0 ≤ phaseRadius

def WholePacket.B (packet : WholePacket) (noise : ℝ) : ℝ :=
  packet.markScale + (packet.omegaUpper : ℝ) * packet.kernel * packet.cv * packet.inwardWeighted /
    (packet.markScale * ((packet.cv : ℝ) * 47 * noise + (packet.inwardWeighted : ℝ) ^ 2)) -
      5 * (packet.rate : ℝ) / 23 + 5 * (packet.rate : ℝ) ^ 2 * noise / 46 - packet.gain
def WholePacket.I (packet : WholePacket) (noise : ℝ) : ℝ :=
  packet.curvature + (packet.phaseRadius : ℝ) * packet.normalVariance +
    (packet.phaseRadius : ℝ) * packet.normalPhase / noise +
      packet.repairPositive * packet.deltaPositive - packet.repairMultiplier * packet.cubicBracket

structure WholeAcceptance (packet : WholePacket) : Prop where
  B_left : packet.B packet.noise.lower < 0
  B_right : packet.B packet.noise.upper < 0
  I_right : 0 ≤ packet.I packet.noise.upper
  test_left : (packet.mass : ℝ) * packet.B packet.noise.lower + packet.I packet.noise.lower / 47 < -(localEpsilon : ℝ)
  test_right : (packet.mass : ℝ) * packet.B packet.noise.upper + packet.I packet.noise.upper / 47 < -(localEpsilon : ℝ)

/-- This semantic output is the source's quantitative whole-count bound,
before any n->47 relaxation. It preserves the signs needed for relaxation. -/
structure WholeMeaning {n : ℕ} {w : ContraryContact n} (f : LocalFrame w) (packet : WholePacket) : Prop where
  noise_scope : packet.noise.Contains f.noise
  mass_lower : (packet.mass : ℝ) ≤ f.massScaled
  negative_B : packet.B f.noise < 0
  nonnegative_I : 0 ≤ packet.I f.noise
  test : (packet.mass : ℝ) * packet.B f.noise + packet.I f.noise / 47 < -(localEpsilon : ℝ)
  whole_bound : f.comparison ≤ f.massScaled * f.noise * packet.B f.noise + f.noise * packet.I f.noise / n

theorem whole_comparison {n : ℕ} {w : ContraryContact n} {f : LocalFrame w}
    {packet : WholePacket} (meaning : WholeMeaning f packet) :
    f.comparison < -(localEpsilon : ℝ) * f.noise := by
  have h47 : (47 : ℝ) ≤ n := by exact_mod_cast f.at_least_47
  have hn : (0 : ℝ) < n := by linarith
  have hl : (0 : ℝ) < packet.noise.lower := by exact_mod_cast packet.noise_lower_positive
  have hnoise : 0 < f.noise := hl.trans_le meaning.noise_scope.1
  have hneg : f.noise * packet.B f.noise ≤ 0 := (mul_neg_of_pos_of_neg hnoise meaning.negative_B).le
  have hmass := mul_le_mul_of_nonpos_right meaning.mass_lower hneg
  have hindex : packet.I f.noise / (n : ℝ) ≤ packet.I f.noise / 47 :=
    div_le_div_of_nonneg_left meaning.nonnegative_I (by norm_num) h47
  have hscaled := mul_le_mul_of_nonneg_left hindex hnoise.le
  have htest := mul_lt_mul_of_pos_right meaning.test hnoise
  have hb := meaning.whole_bound
  simp only [div_eq_mul_inv] at hscaled htest hb
  nlinarith

/-- Exact scalar functions used by the marked-crossing kernel. -/
def fractionalGain (rate L : ℝ) : ℝ :=
  5 / 23 * (rate ^ 3 * L ^ 2 / 6 - rate ^ 4 * L ^ 3 / 24 + rate ^ 5 * L ^ 4 / 120 - rate ^ 6 * L ^ 5 / 720)
def independentMarkKernel (TL b1 b2 : ℝ) (tail1 tail2 : ℝ) : ℝ :=
  min (1 / (b1 ^ 2 + TL)) (tail1 / TL) + min (1 / (b2 ^ 2 + TL)) (tail2 / TL)
def commonMarkKernel (TL alpha beta center : ℝ) : ℝ :=
  (1 + center ^ 2 / TL) / (min (center + alpha) (beta - center)) ^ 2
def markTailKernel (amplitude TU c ul uh : ℝ) : ℝ :=
  (amplitude ^ 2 + 3 * TU) / (3 * c) *
    (1 / ((5 / 2) * c - amplitude - uh) ^ 3 + 1 / ((5 / 2) * c - amplitude + ul) ^ 3)

/-- Finite Poisson cubic identity, not a truncated infinite probability.
All anchors below are nonnegative and have positive final denominator. -/
def poissonCubic (mu anchor : ℝ) : ℝ :=
  mu ^ 3 + 3 * (1 - anchor) * mu ^ 2 + (1 - 3 * anchor + 3 * anchor ^ 2) * mu - anchor ^ 3 +
    Real.exp (-mu) * ∑ h ∈ Finset.range (⌊anchor⌋₊ + 1), mu ^ h * (anchor - h) ^ 3 / (h.factorial : ℝ)
def bennett (A V b : ℝ) : ℝ :=
  Real.exp (b / A) * (V / (V + A * b)) ^ (b / A + V / A ^ 2 : ℝ)
def commonTail (A V b anchor : ℝ) : ℝ :=
  min 1 (min (V / (V + b ^ 2))
    (min (bennett A V b) (poissonCubic (V / A ^ 2) anchor / (b / A + V / A ^ 2 - anchor) ^ 3)))

structure MarkCell (packet : WholePacket) where
  phase : ClosedInterval
  centers : Fin 2 → ℚ
  anchors : Fin 2 → Fin 2 → ℚ
  tails : Fin 2 → Fin 2 → ℚ

def MarkCell.b1 {packet : WholePacket} (cell : MarkCell packet) (i : Fin 2) : ℚ :=
  (1 - packet.inward) * (i.val + 1) - packet.inward - cell.phase.upper
def MarkCell.b2 {packet : WholePacket} (cell : MarkCell packet) (i : Fin 2) : ℚ :=
  (i.val + 1) - packet.amplitude + cell.phase.lower
def MarkCell.alpha {packet : WholePacket} (cell : MarkCell packet) (i : Fin 2) : ℚ :=
  (1 - packet.inward) * (i.val + 1) - 2 * packet.inward - cell.phase.upper
def MarkCell.beta {packet : WholePacket} (cell : MarkCell packet) (i : Fin 2) : ℚ :=
  (i.val + 1) - packet.amplitude - packet.inward + cell.phase.lower
def MarkCell.bound {packet : WholePacket} (cell : MarkCell packet) (i : Fin 2) : ℝ :=
  min (independentMarkKernel ((packet.omegaUpper : ℝ) * packet.noise.lower) (cell.b1 i) (cell.b2 i)
    (cell.tails i 0) (cell.tails i 1))
    (commonMarkKernel ((packet.omegaUpper : ℝ) * packet.noise.lower) (cell.alpha i) (cell.beta i) (cell.centers i))

structure MarkCellGates {packet : WholePacket} (cell : MarkCell packet) : Prop where
  b1 : ∀ i, 0 < cell.b1 i
  b2 : ∀ i, 0 < cell.b2 i
  alpha : ∀ i, 0 < cell.alpha i
  beta : ∀ i, 0 < cell.beta i
  center_lower : ∀ i, -cell.alpha i < cell.centers i
  center_upper : ∀ i, cell.centers i < cell.beta i
  anchors_nonnegative : ∀ i j, 0 ≤ cell.anchors i j
  anchor_first : ∀ i, (cell.anchors i 0 : ℝ) < (cell.b1 i : ℝ) / packet.amplitude +
    (packet.omegaUpper : ℝ) * packet.noise.upper / (packet.amplitude : ℝ) ^ 2
  anchor_second : ∀ i, (cell.anchors i 1 : ℝ) < (cell.b2 i : ℝ) / packet.amplitude +
    (packet.omegaUpper : ℝ) * packet.noise.upper / (packet.amplitude : ℝ) ^ 2
  first_tail : ∀ i, commonTail packet.amplitude ((packet.omegaUpper : ℝ) * packet.noise.upper)
    (cell.b1 i) (cell.anchors i 0) ≤ (cell.tails i 0 : ℝ)
  second_tail : ∀ i, commonTail packet.amplitude ((packet.omegaUpper : ℝ) * packet.noise.upper)
    (cell.b2 i) (cell.anchors i 1) ≤ (cell.tails i 1 : ℝ)

def wholeCurvature (packet : WholePacket) (chiOffset u : ℝ) : ℝ :=
  (packet.omegaUpper : ℝ) / packet.varianceLower *
    (max (chiOffset + u - 1) 0 / (1 - (packet.inward : ℝ) - u) ^ 2 +
      max (chiOffset + u) 0 / (1 - (packet.inward : ℝ) + min u ((1 - (packet.inward : ℝ)) / 3)) ^ 2 +
        Real.sqrt ((packet.amplitude : ℝ) ^ 2 + 3 * packet.omegaUpper * packet.noise.upper) /
          (2 * (1 - (packet.inward : ℝ)) - 1 / 2) ^ 3)

/-- Frozen scalar license for the full source marked-crossing kernel. These
are mathematical obligations for a finite evaluator, not a free B/I oracle. -/
structure WholeKernelLicense (normalizer : Normalizer) (cell : LocalCell) (packet : WholePacket) where
  probability_same : normalizer.probability = panelProbability cell.panel
  mass_same : packet.mass = normalizer.mass
  variance_same : packet.varianceLower = normalizer.varianceLower
  cv_same : packet.cv = normalizer.cv
  delta_enclosed : packet.deltaBound ≤ normalizer.delta
  inward_lt_probability : packet.inward < normalizer.probability.lower
  noise_enclosed : packet.noise.upper ≤ normalizer.noiseUpper
  normalVariance : (packet.normalVariance : ℝ) = normalizer.expFactor * normalizer.logCoefficient
  normalPhase : (packet.normalPhase : ℝ) = normalizer.expFactor *
    normalizer.phaseError packet.deltaBound packet.phaseRadius
  repairPositive_same : packet.repairPositive = normalizer.repairPositive
  repairMultiplier_same : packet.repairMultiplier = normalizer.repairMultiplier
  cubicBracket_same : packet.cubicBracket = normalizer.cubicBracket
  phase_lower : -packet.phaseRadius ≤ cell.phase.lower
  phase_upper : cell.phase.upper ≤ packet.phaseRadius
  phase_half : packet.phaseRadius ≤ 1 / 2
  chiOffset : ℚ
  chi_upper : chiOffset + cell.phase.upper < 2
  tail_first_denominator : 0 < (5 / 2) * (1 - packet.inward) - packet.amplitude - cell.phase.upper
  tail_second_denominator : 0 < (5 / 2) * (1 - packet.inward) - packet.amplitude + cell.phase.lower
  rate : (packet.rate : ℝ) ≤ packet.omegaLower *
    (2 * Real.sin (Real.pi * (packet.amplitude + packet.inward)) ^ 2 /
      (packet.amplitude + packet.inward : ℝ) ^ 2)
  gain : (packet.gain : ℝ) ≤ fractionalGain packet.rate packet.noise.lower
  marks : List (MarkCell packet)
  marks_cover : ∀ u : ℝ, cell.phase.Contains u → ∃ mark ∈ marks, mark.phase.Contains u
  mark_gates : ∀ mark ∈ marks, MarkCellGates mark
  firstKernel : ℚ
  secondKernel : ℚ
  firstKernel_bound : ∀ mark ∈ marks, mark.bound 0 ≤ (firstKernel : ℝ)
  secondKernel_bound : ∀ mark ∈ marks, mark.bound 1 ≤ (secondKernel : ℝ)
  kernel : (firstKernel : ℝ) + secondKernel +
    markTailKernel packet.amplitude ((packet.omegaUpper : ℝ) * packet.noise.upper)
      (1 - (packet.inward : ℝ)) cell.phase.lower cell.phase.upper ≤ (packet.kernel : ℝ)
  curvature : ∀ u : ℝ, cell.phase.Contains u → wholeCurvature packet chiOffset u ≤ (packet.curvature : ℝ)

structure WholeApplicability {n : ℕ} {w : ContraryContact n} (f : LocalFrame w)
    {normalizer : Normalizer} {cell : LocalCell} {packet : WholePacket}
    (license : WholeKernelLicense normalizer cell packet) : Prop where
  noise : packet.noise.Contains f.noise
  delta : |f.delta| ≤ (packet.deltaBound : ℝ)
  deltaPositive : max f.delta 0 ≤ (packet.deltaPositive : ℝ)
  chi : ((n : ℝ) + 1) * f.p - f.root.val ≤ license.chiOffset + f.phase
  inward : f.a0 + f.a1 ≤ (packet.inward : ℝ)
  weighted_inward : (n : ℝ) * (f.a0 + f.a1) < (packet.inwardWeighted : ℝ)
  negative_amplitude : ∀ᵐ u ∂(f.binary.negativeLaw : Measure ℝ), |u| ≤ (packet.amplitude : ℝ)
  positive_amplitude : ∀ᵐ u ∂(f.binary.positiveLaw : Measure ℝ), |u| ≤ (packet.amplitude : ℝ)

/-- Accepted source marked-crossing/curvature/harmonic theorem. Its inputs
fix the quantitative B/I kernel and every scalar and actual-law gate. It
does not accept a free final score cap. -/
def WholeCountAnalyticTheorem : Prop := MasterIdentityTheorem →
  ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w) (normalizer : Normalizer)
    (cell : LocalCell) (packet : WholePacket), NormalizerGates normalizer →
    ∀ license : WholeKernelLicense normalizer cell packet,
      WholeAcceptance packet → Normalization f normalizer → WholeApplicability f license →
      cell.Contains f → WholeMeaning f packet

inductive CellPacket (cell : LocalCell) where
  | nearest (normalizer : Normalizer) (gates : NormalizerGates normalizer) (packet : NearestPacket)
  | whole (normalizer : Normalizer) (gates : NormalizerGates normalizer)
      (packet : WholePacket) (acceptance : WholeAcceptance packet)
      (license : WholeKernelLicense normalizer cell packet)
  | resourceEmpty (inwardUpper : ℚ) (nonpositive : inwardUpper ≤ 0)

/-- Applicability and kernel outputs are quantified over every law in the
same frozen cell. A scalar receipt, failed guard or hash cannot inhabit this.
Whole-count output uses the full marked-crossing kernel, not a free cap. -/
def CellMeaning (ctx : FrozenLocalContext) (cell : LocalCell) (packet : CellPacket cell) : Prop :=
  ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w),
    PanelScope f cell.panel (ctx.rows cell.panel) → cell.Contains f → 0 < f.noise →
    match packet with
    | .nearest normalizer _ packet => Normalization f normalizer ∧ NearestMeaning f packet
    | .whole normalizer _ _ _ license =>
      Normalization f normalizer ∧ WholeApplicability f license
    | .resourceEmpty G _ => (n : ℝ) * (f.a0 + f.a1) < (G : ℝ)

structure LocalCertificate (ctx : FrozenLocalContext) where
  packet : ∀ cell ∈ ctx.cells, CellPacket cell
  meaning : ∀ cell (hc : cell ∈ ctx.cells), CellMeaning ctx cell (packet cell hc)

/-- Source acquisition consumes the exact global caps, same contact and
both predecessor bounds. It returns support and panel resources, not the
local comparison conclusion that will later consume them. -/
def UniformAcquisitionMeaning (ctx : FrozenLocalContext) : Prop :=
  ∀ (n : ℕ) (w : ContraryContact n), UniformLocalAssumptions w →
    ∃ f : LocalFrame w, ∃ j : Fin 83, PanelScope f j (ctx.rows j)

/-- Acquisition of concrete numerical row caps is a combined analytic AND
numerical obligation. Metadata identifies every independent source lane;
none of these strings, or a worker's success bit, proves `meaning`. -/
structure UniformAcquisitionLicense (ctx : FrozenLocalContext) where
  sourcePin : MathematicalSourcePin
  supportCertificateDigest : String
  entryResourceManifestDigest : String
  phasePremisesDigest : String
  confinementCertificateDigest : String
  amplitudeProfileDigest : String
  meaning : UniformAcquisitionMeaning ctx

/-- Accepted published all-parameter Bernoulli input plus the source's
zero-noise exact-law argument. At zero noise no division by lambda occurs. -/
structure BernoulliTheorem : Prop where
  positive_closed : ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w), f.bernoulliScore < esseenConstant
  zero_noise : ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w),
    f.noise = 0 → w.X.normalizedScore n = f.bernoulliScore
  rho_positive : ∀ (n : ℕ) (w : ContraryContact n) (f : LocalFrame w), 0 < bernoulliRho f.p

structure UniformLocalProvider where
  context : FrozenLocalContext
  acquisition : UniformAcquisitionLicense context
  certificate : LocalCertificate context
  master : MasterIdentityTheorem
  nearest : NearestComparisonTheorem
  whole : WholeCountAnalyticTheorem
  bernoulli : BernoulliTheorem

theorem UniformLocalProvider.reject (provider : UniformLocalProvider) {n : ℕ}
    (w : ContraryContact n) (inputs : UniformLocalAssumptions w) : False := by
  obtain ⟨f, j, scope⟩ := provider.acquisition.meaning n w inputs
  have hnoise_nonneg : 0 ≤ f.noise := mul_nonneg (Nat.cast_nonneg n) f.binary.noise_nonneg
  rcases eq_or_lt_of_le hnoise_nonneg with hz | hp
  · have h := provider.bernoulli.zero_noise n w f hz.symm
    have hb := provider.bernoulli.positive_closed n w f
    exact (not_lt_of_ge w.critical) (h.trans_lt hb)
  · obtain ⟨cell, hc, hj, hH, hnoise, hphase⟩ := provider.context.cover j w.rawThreshold.value f.noise f.phase
      scope.threshold hp scope.weighted_noise f.phase_lower f.phase_upper
    have hscope : PanelScope f cell.panel (provider.context.rows cell.panel) := by simpa [hj] using scope
    have meaning := provider.certificate.meaning cell hc n w f hscope ⟨hH, hnoise, hphase⟩ hp
    have comparison : f.comparison < -(localEpsilon : ℝ) * f.noise := by
      cases hpacket : provider.certificate.packet cell hc with
      | nearest normalizer gates packet =>
        rw [hpacket] at meaning
        exact provider.nearest provider.master n w f packet meaning.2
      | whole normalizer gates packet acceptance license =>
        rw [hpacket] at meaning
        exact whole_comparison (provider.whole provider.master n w f normalizer cell packet gates license
          acceptance meaning.1 meaning.2 ⟨hH, hnoise, hphase⟩)
      | resourceEmpty G nonpositive =>
        rw [hpacket] at meaning
        have hG : (G : ℝ) ≤ 0 := by exact_mod_cast nonpositive
        have hd : 0 ≤ (n : ℝ) * (f.a0 + f.a1) :=
          mul_nonneg (Nat.cast_nonneg n) (add_nonneg f.a0_nonneg f.a1_nonneg)
        exact False.elim (by linarith)
    have he : (0 : ℝ) < localEpsilon := by norm_num [localEpsilon]
    have hr := provider.bernoulli.rho_positive n w f
    have hb := provider.bernoulli.positive_closed n w f
    have hcpos : 0 ≤ w.X.normalizedScore n - f.bernoulliScore := by linarith [w.critical]
    have hcomp : 0 ≤ f.comparison := mul_nonneg hr.le hcpos
    nlinarith

end BEMap.UniformTail
