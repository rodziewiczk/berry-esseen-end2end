import BEMap.Tail
import BEMap.TypedPipeline
import BEMap.UniformTail
import BEMap.FourierFamilies

/-! Independent all-index tail assembly. The 83-panel local comparison is
numerical evidence, not an analytic scalar impossibility assumption. The
five auxiliary rows are strict resource-enclosure exports, not COUNT scores.
No sharp bound at indices1..48 occurs among the provider inputs. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

inductive TailAuxiliaryRow where | a40 | p41 | a45 | p46 | a46
deriving DecidableEq

def TailAuxiliaryRow.lower : TailAuxiliaryRow → ℕ
  | .a40 => 40 | .p41 => 41 | .a45 => 45 | .p46 => 46 | .a46 => 46
def TailAuxiliaryRow.upper : TailAuxiliaryRow → ℕ
  | .a40 => 40 | .p41 => 49 | .a45 => 45 | .p46 => 98 | .a46 => 46
def TailAuxiliaryRow.radius : TailAuxiliaryRow → ℚ
  | .a40 => 33 / 10 | .p41 => 29 / 10 | .a45 => 7 / 2 | .p46 => 7 / 2 | .a46 => 17 / 5
def TailAuxiliaryRow.scoreCap : TailAuxiliaryRow → ℚ
  | .a40 => 469 / 1000 | .p41 => 469 / 1000 | .a45 => 4431 / 10000
  | .p46 => 54 / 125 | .a46 => 1328 / 3125
def TailAuxiliaryRow.barrier : TailAuxiliaryRow → ℚ
  | .a40 => 3 / 2 | .p41 => 3 / 2 | .a45 => 7 / 10 | .p46 => 7 / 10 | .a46 => 27 / 50
def TailAuxiliaryRow.dropCap : TailAuxiliaryRow → ℚ
  | .a40 => 22 / 25 | .p41 => (3 / 2) / 40 | .a45 => 8341 / 10000
  | .p46 => (7 / 10) / 45 | .a46 => 79 / 450
def TailAuxiliaryRow.passCount : TailAuxiliaryRow → ℕ
  | .a40 => 5 | .p41 => 6 | .a45 => 12 | .p46 => 13 | .a46 => 7

inductive BarrierCoverKind where | signedMoment | probability
deriving DecidableEq

def TailAuxiliaryRow.kind (row : TailAuxiliaryRow) (i : Fin row.passCount) : BarrierCoverKind :=
  if row = .a46 ∧ 4 ≤ i.val then .probability else .signedMoment
def TailAuxiliaryRow.cellCount (row : TailAuxiliaryRow) (i : Fin row.passCount) : ℕ :=
  if row = .a40 ∨ row = .p41 then 64 else
    if row = .a46 ∧ 4 ≤ i.val then 96 else 18432

def a46RawTarget (i : Fin 7) : ℚ :=
  match i.val with
  | 0 => 11683 / 2000 | 1 => 14161 / 5000 | 2 => 18719 / 10000
  | 3 => 1441 / 1000 | 4 => 9953 / 10000 | 5 => 927 / 1250 | _ => 73 / 125
def a46DefectTarget (i : Fin 7) : ℚ :=
  match i.val with
  | 0 => 4081 / 2500 | 1 => 1239 / 2000 | 2 => 71 / 200
  | 3 => 2371 / 10000 | 4 => 1077 / 10000 | 5 => 379 / 10000 | _ => -23 / 5000

/-- The source row's supported scope; the index in every physical quantity
is the actual n. A support implication must be acquired before this input. -/
structure BarrierScope (row : TailAuxiliaryRow) {n : ℕ} (w : ContraryContact n) : Prop where
  lower : row.lower ≤ n
  upper : n ≤ row.upper
  support : AlmostBounded w.X row.radius
  current : w.X.normalizedScore n ≤ (row.scoreCap : ℝ)
  excess : (row.barrier : ℝ) ≤ (n : ℝ) * (w.X.normalizedScore n - esseenConstant)

/-- Separate all-threshold support theorem. Its exact numerical support-row
license uses K,R,q and the original wider index band, including both signed
radial covers and both infinite exterior rays. -/
structure AuxiliarySupportImplication (row : TailAuxiliaryRow) where
  sourcePin : MathematicalSourcePin
  derive : ∀ (n : ℕ) (w : ContraryContact n), row.lower ≤ n → n ≤ row.upper →
    (row.barrier : ℝ) ≤ (n : ℝ) * (w.X.normalizedScore n - esseenConstant) →
    dropSize optimalConstant n ≤ (row.dropCap : ℝ) → AlmostBounded w.X row.radius

structure BarrierCell where
  moments : MomentBox
  firstMoment : ClosedInterval
  rawThreshold : ClosedInterval

def BarrierCell.Contains {n : ℕ} (cell : BarrierCell) (w : ContraryContact n) : Prop :=
  cell.moments.Contains w.X ∧ cell.firstMoment.Contains (positiveFirstMoment w.X) ∧
    cell.rawThreshold.Contains w.rawThreshold.value

/-- Strict weighted exports may have a negative final d. They are NOT
ResourceState: that state deliberately requires a nonnegative live cap. -/
structure BarrierExport {n : ℕ} (w : ContraryContact n) (N : ℕ) (r d : ℚ) : Prop where
  raw : rawRemainder w < (r : ℝ)
  defect : (n : ℝ) * physicalDefect w.X < (N : ℝ) * (d : ℝ)

def barrierDensityFloor (n : ℕ) (r : ℚ) : ℝ :=
  (997 / 2500 : ℝ) * (1 - 5 * (r : ℝ) / (2 * n))
def barrierExtraCurvature (n : ℕ) (r d : ℚ) (rho : ℝ) : ℝ :=
  (1 - 5 * (r : ℝ) / (2 * n)) / 2 * ((819 / 2000 : ℝ) * rho - (d : ℝ) / 15)
def pairedSignedCorrection (n : ℕ) (r d : ℚ) : ℝ :=
  ((2 / 5 : ℝ) - barrierDensityFloor n r) / 2 * max ((d : ℝ) - 4 / 25) 0

/-- An accepted weight-removal implication is usable only after a strict
raw warm start r<.4n. The excess subtraction belongs only to resourceBudget. -/
structure BarrierBudgetEvidence {n : ℕ} (w : ContraryContact n) (r d : ℚ) where
  raw_warm : rawRemainder w < (r : ℝ)
  raw_small : (r : ℝ) < (2 / 5 : ℝ) * n
  previous_defect : physicalDefect w.X < (d : ℝ)
  density : barrierDensityFloor n r ≤ phi w.threshold.value
  resourceBudget : ℝ → ℝ
  budget : (n : ℝ) * (w.X.normalizedScore n - esseenConstant) * w.X.rho +
    (997 / 15000 : ℝ) * n * physicalDefect w.X ≤ resourceBudget w.rawThreshold.value

def pairedGaussianCorner (I : ℚ) (z c : ℝ) : ℝ :=
  if z * c ≤ 0 then (I : ℝ) * (|z| + 3 * |c|) else
    (I : ℝ) * abs (|z| - 3 * |c|) + 6 * Real.sqrt |z * c| * Real.exp (-|z| / (2 * |c|))

/-- Exact common-triple paired LOW recipe, including its complete rectangle
and coefficient-ordering gates. A sampler at a single z/c is insufficient. -/
structure BarrierPairedLowData where
  N : ℕ
  N_gt_two : 2 < N
  M : ℚ
  g : ℚ
  sixth : ℚ
  aStar : ℚ
  Z : ℚ
  sixth_nonneg : 0 ≤ sixth
  a_nonneg : 0 ≤ aStar
  Z_nonneg : 0 ≤ Z
  zRectangle : ClosedInterval
  cRectangle : ClosedInterval
  Iupper : ℚ
  I_ordering : Real.sqrt (Real.pi / 2) ≤ (Iupper : ℝ)
  F : ℚ
  F_ordering : ((N : ℝ) / (N - 1 : ℕ)) * Real.sqrt ((N : ℝ) / (N - 1 : ℕ)) ≤ (F : ℝ)
  damping : ℚ
  damping_pos : 0 < damping
  damping_ordering : (damping : ℝ) ≤ (45 - (M : ℝ)) * (1 - 2 / (N : ℝ)) / 96
  Jupper : ℚ
  rectangle_corners : ∀ z ∈ [zRectangle.lower, zRectangle.upper],
    ∀ c ∈ [cRectangle.lower, cRectangle.upper], pairedGaussianCorner Iupper z c ≤ (Jupper : ℝ)
  sourcePin : MathematicalSourcePin

def BarrierPairedLowData.E6 (p : BarrierPairedLowData) : ℝ :=
  (p.sixth : ℝ) / 720 + (p.g : ℝ) ^ 2 / 72 + (1 / 2 + (p.g : ℝ) ^ 2 / 144) ^ 3 / 5
def BarrierPairedLowData.B6 (p : BarrierPairedLowData) : ℝ := p.aStar + (p.Z : ℝ) / 2 + p.E6 / 4
def BarrierPairedLowData.L0 (p : BarrierPairedLowData) : ℝ :=
  p.F * (p.Jupper : ℝ) + (p.F : ℝ) * p.Iupper / (p.N - 1 : ℕ) *
    (35 * (p.aStar : ℝ) * (p.g : ℝ) ^ 3 / 48 + 35 * (p.Z : ℝ) * (p.g : ℝ) ^ 2 / 24) +
      251 * (p.g : ℝ) ^ 3 / 17280
def BarrierPairedLowData.LH (p : BarrierPairedLowData) : ℝ :=
  (p.F : ℝ) * p.Iupper * ((p.aStar : ℝ) + 5 * (p.Z : ℝ) * p.g / (2 * (p.N - 1 : ℕ))) +
    251 * (p.g : ℝ) ^ 2 / 4800
def BarrierPairedLowData.L2 (p : BarrierPairedLowData) : ℝ :=
  p.E6 / (2 * (((p.N - 1 : ℕ) : ℝ) / (2 * p.N)) ^ 2) + p.B6 ^ 2 / (2 * (p.damping : ℝ) ^ 3)

structure PairedBarrierGates where
  probability : ClosedInterval
  l_positive : 0 < probability.lower
  l_lt_u : probability.lower < probability.upper
  u_below_half : probability.upper < 1 / 2
  M : ℚ
  M_range : 1 ≤ M ∧ M ≤ 2
  g : ℚ
  g_range : 0 ≤ g ∧ g ≤ 1
  R : ℚ
  radius_gate : 2 * g < R
  innerMinus : ℚ
  innerPlus : ℚ
  bernoulli_rho_gate : ∀ p : ℝ, probability.Contains p →
    (3 / 2 : ℝ) * ((1 - 2 * p * (1 - p)) / Real.sqrt (p * (1 - p))) ≤
      3 * min (innerMinus : ℝ) innerPlus
  pairedSkewLower : ℚ
  skew_nonneg : 0 ≤ pairedSkewLower
  low : BarrierPairedLowData
  low_M_exact : low.M = M
  low_g_exact : low.g = g
  sourcePin : MathematicalSourcePin

structure PairedBarrierCorner where
  constant : ℚ
  linear : ℚ
  curvature : ℚ

/-- Maxima are taken across COMPLETE score/rho corners before square
completion. General and paired portfolios remain separate upper bounds. -/
structure PairedBarrierPacket (n : ℕ) (r d K : ℚ) where
  gates : PairedBarrierGates
  rhoUpper : ℚ
  rho_ordered : (1 - 2 * (gates.probability.upper : ℝ) * (1 - gates.probability.upper)) /
      Real.sqrt ((gates.probability.upper : ℝ) * (1 - gates.probability.upper)) ≤ (rhoUpper : ℝ)
  corners : Fin 2 → Fin 2 → PairedBarrierCorner
  corrected_positive : ∀ c j, 0 < (corners c j).curvature - pairedSignedCorrection n r d
  extra_positive : ∀ j : Fin 2, 0 < barrierExtraCurvature n r d
    (if j.val = 0 then
      (1 - 2 * (gates.probability.upper : ℝ) * (1 - gates.probability.upper)) /
        Real.sqrt ((gates.probability.upper : ℝ) * (1 - gates.probability.upper)) else (rhoUpper : ℝ))
  sourcePin : MathematicalSourcePin

def PairedBarrierPacket.rhoLower {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K) : ℝ :=
  (1 - 2 * (p.gates.probability.upper : ℝ) * (1 - p.gates.probability.upper)) /
    Real.sqrt ((p.gates.probability.upper : ℝ) * (1 - p.gates.probability.upper))

def PairedBarrierPacket.rawCorner {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K)
    (c j : Fin 2) : ℝ :=
  (p.corners c j).constant + (p.corners c j).linear ^ 2 /
    (4 * ((p.corners c j).curvature - pairedSignedCorrection n r d))
def PairedBarrierPacket.resourceCorner {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K)
    (c j : Fin 2) : ℝ :=
  let rho : ℝ := if j.val = 0 then p.rhoLower else (p.rhoUpper : ℝ)
  (p.corners c j).constant + (p.corners c j).linear ^ 2 /
    (4 * ((p.corners c j).curvature - pairedSignedCorrection n r d +
      barrierExtraCurvature n r d rho)) - (K : ℝ) * rho

def fourCornerMaximum (f : Fin 2 → Fin 2 → ℝ) : ℝ := max (max (f 0 0) (f 0 1)) (max (f 1 0) (f 1 1))

def PairedBarrierPacket.rawQuadratic {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K)
    (H : ℝ) (c j : Fin 2) : ℝ :=
  (p.corners c j).constant + (p.corners c j).linear * |H| -
    ((p.corners c j).curvature - pairedSignedCorrection n r d) * H ^ 2
def PairedBarrierPacket.resourceQuadratic {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K)
    (H : ℝ) (c j : Fin 2) : ℝ :=
  let rho : ℝ := if j.val = 0 then p.rhoLower else (p.rhoUpper : ℝ)
  (p.corners c j).constant + (p.corners c j).linear * |H| -
    ((p.corners c j).curvature - pairedSignedCorrection n r d +
      barrierExtraCurvature n r d rho) * H ^ 2 - (K : ℝ) * rho

/-- Whole-cell interpretation from the coherent source enclosure, after the
same-law moment/paired gates and endpoint convexity step. A numerical
implementation must supply these actual coefficient meanings, not merely
positive denominators or a successful source status. -/
structure PairedEnvelopeMeaning {n : ℕ} {r d K : ℚ} (p : PairedBarrierPacket n r d K)
    (w : ContraryContact n) : Prop where
  warm : Nonempty (BarrierBudgetEvidence w r d)
  actual_floor : p.gates.low.N ≤ n
  probability : p.gates.probability.Contains (positiveProbability w.X)
  support : AlmostBounded w.X p.gates.R
  actual_score_range : (819 / 2000 : ℝ) ≤ w.X.normalizedScore n ∧
    w.X.normalizedScore n ≤ 1328 / 3125
  actual_rho_range : p.rhoLower ≤ w.X.rho ∧ w.X.rho ≤ (p.rhoUpper : ℝ)
  actual_inner_floors : ∃ gap : CentralGap w.X,
    (p.gates.innerMinus : ℝ) ≤ gap.negativeEndpoint ∧
      (p.gates.innerPlus : ℝ) ≤ gap.positiveEndpoint
  actual_fourth : fourthMoment w.X ≤ (p.gates.M : ℝ)
  actual_gamma : |w.X.gamma| ≤ (p.gates.g : ℝ)
  actual_signed_gamma : (79 / 25 : ℝ) * w.X.rho - 3 - (d : ℝ) ≤ w.X.gamma
  density_upper : phi w.threshold.value ≤ 2 / 5
  actual_abs_skew_lower : (p.gates.pairedSkewLower : ℝ) ≤ |w.X.gamma|
  sixth_integrable : Integrable (fun x : ℝ => x ^ 6) (w.X.law : Measure ℝ)
  actual_sixth : (∫ x : ℝ, x ^ 6 ∂(w.X.law : Measure ℝ)) ≤ (p.gates.low.sixth : ℝ)
  actual_a : |(3 - fourthMoment w.X) / 24| ≤ (p.gates.low.aStar : ℝ)
  actual_z : p.gates.low.zRectangle.Contains ((10 * w.X.gamma - signedFifthMoment w.X) / 120)
  actual_c : p.gates.low.cRectangle.Contains (((3 - fourthMoment w.X) / 24) * w.X.gamma / 6)
  z_bound : |(10 * w.X.gamma - signedFifthMoment w.X) / 120| ≤ (p.gates.low.Z : ℝ)
  low_integrable : IntegrableOn (lowIntegrand w) (Ioo (0 : ℝ) (1 / 2))
  coherent_low : lowIntegral w halfFrequencySplit ≤
    (p.gates.low.L0 + p.gates.low.LH * |w.rawThreshold.value|) / Real.sqrt n + p.gates.low.L2 / n
  complete_high : Nonempty (HighBound w halfFrequencySplit)
  raw : rawRemainder w ≤ fourCornerMaximum (p.rawQuadratic w.rawThreshold.value)
  resource : (997 / 15000 : ℝ) * n * physicalDefect w.X ≤
    fourCornerMaximum (p.resourceQuadratic w.rawThreshold.value)

theorem quadratic_square_upper (A f q H : ℝ) (hq : 0 < q) :
    A + f * |H| - q * H ^ 2 ≤ A + f ^ 2 / (4 * q) := by
  have hs := sq_nonneg (2 * q * |H| - f)
  rw [sub_sq, mul_pow, mul_pow, sq_abs] at hs
  have hd : 0 < 4 * q := by positivity
  have he : f * |H| - q * H ^ 2 ≤ f ^ 2 / (4 * q) :=
    (le_div_iff₀ hd).mpr (by nlinarith only [hs])
  linarith

theorem four_corner_mono {f g : Fin 2 → Fin 2 → ℝ} (h : ∀ c j, f c j ≤ g c j) :
    fourCornerMaximum f ≤ fourCornerMaximum g :=
  max_le_max (max_le_max (h 0 0) (h 0 1)) (max_le_max (h 1 0) (h 1 1))

theorem paired_envelope_export {n N : ℕ} {r d K rOut dOut : ℚ}
    {p : PairedBarrierPacket n r d K} {w : ContraryContact n} (meaning : PairedEnvelopeMeaning p w)
    (raw_rounding : fourCornerMaximum p.rawCorner < (rOut : ℝ))
    (resource_rounding : fourCornerMaximum p.resourceCorner < (997 / 15000 : ℝ) * N * dOut) :
    BarrierExport w N rOut dOut := by
  have hraw : fourCornerMaximum (p.rawQuadratic w.rawThreshold.value) ≤ fourCornerMaximum p.rawCorner := by
    apply four_corner_mono
    intro c j
    exact quadratic_square_upper _ _ _ _ (p.corrected_positive c j)
  have hresource : fourCornerMaximum (p.resourceQuadratic w.rawThreshold.value) ≤
      fourCornerMaximum p.resourceCorner := by
    apply four_corner_mono
    intro c j
    have he := p.extra_positive j
    have hp := p.corrected_positive c j
    have hq : 0 < (p.corners c j).curvature - pairedSignedCorrection n r d +
        barrierExtraCurvature n r d (if j.val = 0 then p.rhoLower else (p.rhoUpper : ℝ)) := by
      simpa only [PairedBarrierPacket.rhoLower] using add_pos hp he
    have hh := quadratic_square_upper ((p.corners c j).constant : ℝ) (p.corners c j).linear _
      w.rawThreshold.value hq
    simpa only [PairedBarrierPacket.resourceQuadratic, PairedBarrierPacket.resourceCorner] using
      sub_le_sub_right hh ((K : ℝ) * (if j.val = 0 then p.rhoLower else (p.rhoUpper : ℝ)))
  refine ⟨meaning.raw.trans_lt (hraw.trans_lt raw_rounding), ?_⟩
  have h := meaning.resource.trans_lt (hresource.trans_lt resource_rounding)
  nlinarith

inductive BarrierCellOutput {n : ℕ} (w : ContraryContact n) (N : ℕ) (K rOut dOut : ℚ) : Type
  | general (exports : BarrierExport w N rOut dOut)
  | paired (r d : ℚ) (packet : PairedBarrierPacket n r d K) (meaning : PairedEnvelopeMeaning packet w)
      (raw_rounding : fourCornerMaximum packet.rawCorner < (rOut : ℝ))
      (resource_rounding : fourCornerMaximum packet.resourceCorner < (997 / 15000 : ℝ) * N * dOut)

def BarrierCellOutput.exports {n N : ℕ} {w : ContraryContact n} {K r d : ℚ} :
    BarrierCellOutput w N K r d → BarrierExport w N r d
  | .general exports => exports
  | .paired _ _ _ meaning raw resource => paired_envelope_export meaning raw resource

structure BarrierPassData (row : TailAuxiliaryRow) (i : Fin row.passCount) where
  cells : List BarrierCell
  complete_cell_count : cells.length = row.cellCount i
  rawCap : ℚ
  defectCap : ℚ
  a46_exact : ∀ h : row = .a46,
    rawCap = a46RawTarget ⟨i.val, by simpa only [h, TailAuxiliaryRow.passCount] using i.isLt⟩ ∧
    defectCap = a46DefectTarget ⟨i.val, by simpa only [h, TailAuxiliaryRow.passCount] using i.isLt⟩
  sourcePin : MathematicalSourcePin

structure BarrierResourceJob (row : TailAuxiliaryRow) where
  passes : ∀ i : Fin row.passCount, BarrierPassData row i
  terminal_negative : (passes ⟨row.passCount - 1, by cases row <;> decide⟩).defectCap < 0
  sourcePin : MathematicalSourcePin

/-- Frozen finite job meaning: every original actual law is covered before
cell exclusion; strict same-law resource outputs are chronological. Physical
state carries the complete coherent LOW/HIGH and conserved identity. -/
structure BarrierResourceMeaning {row : TailAuxiliaryRow} (job : BarrierResourceJob row) : Prop where
  physical : ∀ (n : ℕ) (w : ContraryContact n), BarrierScope row w → Nonempty (PhysicalState w)
  cover : ∀ (i : Fin row.passCount) (n : ℕ) (w : ContraryContact n), BarrierScope row w →
    ∃ cell ∈ (job.passes i).cells, cell.Contains w
  pass : ∀ (i : Fin row.passCount) (n : ℕ) (w : ContraryContact n),
    BarrierScope row w → PhysicalState w →
    (∀ j : Fin row.passCount, j.val + 1 = i.val →
      BarrierExport w row.lower (job.passes j).rawCap (job.passes j).defectCap) →
    ∀ cell ∈ (job.passes i).cells, cell.Contains w →
      Nonempty (BarrierCellOutput w row.lower row.barrier (job.passes i).rawCap (job.passes i).defectCap)
  a46_budget : ∀ (n : ℕ) (w : ContraryContact n), BarrierScope .a46 w →
    ∀ r d : ℚ, rawRemainder w < r → (r : ℝ) < (2 / 5 : ℝ) * n →
      physicalDefect w.X < d → Nonempty (BarrierBudgetEvidence w r d)

abbrev BarrierResourceChecker (row : TailAuxiliaryRow) :=
  CertificateChecker (BarrierResourceJob row) BarrierResourceMeaning

theorem barrier_resource_reject {row : TailAuxiliaryRow} {checker : BarrierResourceChecker row}
    (certificate : CheckedCertificate checker) {n : ℕ} (w : ContraryContact n)
    (scope : BarrierScope row w) : False := by
  have meaning := certificate.meaning
  obtain ⟨physical⟩ := meaning.physical n w scope
  have all : ∀ k : ℕ, ∀ hk : k < row.passCount,
      BarrierExport w row.lower (certificate.payload.passes ⟨k, hk⟩).rawCap
        (certificate.payload.passes ⟨k, hk⟩).defectCap := by
    intro k
    induction k using Nat.strong_induction_on with
    | h k ih =>
      intro hk
      obtain ⟨cell, hmem, hinside⟩ := meaning.cover ⟨k, hk⟩ n w scope
      obtain ⟨output⟩ := meaning.pass ⟨k, hk⟩ n w scope physical
        (fun j hj => ih j.val (by have hj' : j.val + 1 = k := hj; omega) j.isLt) cell hmem hinside
      exact output.exports
  have last := all (row.passCount - 1) (by cases row <;> decide)
  have hn : (0 : ℝ) < row.lower := by cases row <;> norm_num [TailAuxiliaryRow.lower]
  have hd : (certificate.payload.passes ⟨row.passCount - 1, by cases row <;> decide⟩).defectCap < (0 : ℝ) := by
    exact_mod_cast certificate.payload.terminal_negative
  have hb := mul_neg_of_pos_of_neg hn hd
  have hnonneg := mul_nonneg (Nat.cast_nonneg n) physical.gaps.defect_nonneg
  linarith [last.defect]

structure AuxiliaryBarrierProviders where
  support : ∀ row : TailAuxiliaryRow, AuxiliarySupportImplication row
  checker : ∀ row : TailAuxiliaryRow, BarrierResourceChecker row
  certificate : ∀ row : TailAuxiliaryRow, CheckedCertificate (checker row)

def smoothingRatio (n : ℕ) : ℝ := Real.sqrt ((n : ℝ) / (n - 1 : ℕ))
def smoothingScaledRemainder (n : ℕ) : ℝ :=
  smoothingRatio n ^ 3 * ((1 / 15 : ℝ) + (2 / 25 : ℝ) / Real.sqrt (n - 1 : ℕ))

/-- Accepted support-free source inequality, algebraically multiplied by n.
The defining all-law supremum, all raw thresholds/left limits and rho>=1
are included; no support, contact or higher moment hypothesis is imposed. -/
structure SupportFreeSmoothing : Prop where
  inequality : ∀ n : ℕ, 2 ≤ n →
    (n : ℝ) * optimalConstant n ≤ (n : ℝ) * smoothingRatio n * optimalConstant (n - 1) +
      smoothingScaledRemainder n

/-- Explicit scalar bracket obligations from the decreasing source terms.
They mention only n and square roots, never the target C_n conclusion. -/
structure SmoothingIndexBrackets : Prop where
  ratio_nonneg : ∀ n : ℕ, 2 ≤ n → 0 ≤ smoothingRatio n
  growth : ∀ n : ℕ, 50 ≤ n → (n : ℝ) * (smoothingRatio n - 1) ≤ 25 / 49
  remainder : ∀ n : ℕ, 50 ≤ n → smoothingScaledRemainder n ≤
    (50 / 49 : ℝ) * (1011 / 1000) / 15 + (2 / 25 : ℝ) * (50 / 49) * (1011 / 1000) / 7

def tailSmoothingRationalBound : ℚ :=
  (409733 / 1000000) * (25 / 49) + (50 / 49) * (1011 / 1000) / 15 +
    (2 / 25) * (50 / 49) * (1011 / 1000) / 7

theorem tail_smoothing_rational_bound : tailSmoothingRationalBound < 29 / 100 := by
  norm_num [tailSmoothingRationalBound]

theorem smoothing_first_failure (analytic : SupportFreeSmoothing) (brackets : SmoothingIndexBrackets)
    (constant_nonneg : 0 ≤ esseenConstant) (constant_upper : esseenConstant ≤ 409733 / 1000000)
    (n : ℕ) (hn : 50 ≤ n) (previous : optimalConstant (n - 1) ≤ esseenConstant) :
    (n : ℝ) * (optimalConstant n - esseenConstant) < 29 / 100 := by
  have hs := analytic.inequality n (by omega)
  have hmul := mul_le_mul_of_nonneg_left previous
    (mul_nonneg (Nat.cast_nonneg n) (brackets.ratio_nonneg n (by omega)))
  have hg := mul_le_mul_of_nonneg_right (brackets.growth n hn) constant_nonneg
  have hc := mul_le_mul_of_nonneg_left constant_upper (by norm_num : (0 : ℝ) ≤ 25 / 49)
  have hr := brackets.remainder n hn
  have hq : (tailSmoothingRationalBound : ℝ) < 29 / 100 := by norm_num [tailSmoothingRationalBound]
  unfold tailSmoothingRationalBound at hq
  push_cast at hq
  nlinarith

/-- Accepted source scalar composition of the five supported resource rows.
Its numerical premises are actual negative-D certificate implications, not
assumed sharp indices. The exact output is only the independent auxiliary
excess ceiling, including the separately strengthened index46. -/
structure AuxiliaryScalarReduction : Prop where
  derive : ∀ (extract : ∀ n, 40 ≤ n → ClosedIndexExtraction n esseenConstant)
    (support : ∀ row : TailAuxiliaryRow, AuxiliarySupportImplication row)
    (smoothing : SupportFreeSmoothing),
    (∀ n, 1 ≤ n → optimalConstant n ≤ 469 / 1000) →
    (4095 / 10000 : ℝ) < esseenConstant → esseenConstant ≤ 409733 / 1000000 →
    (∀ (row : TailAuxiliaryRow) (n : ℕ) (w : ContraryContact n), BarrierScope row w → False) →
      (∀ n, 45 ≤ n → n ≤ 50 → optimalConstant n - esseenConstant < (7 / 10 : ℝ) / n) ∧
        optimalConstant 46 - esseenConstant < (54 / 100 : ℝ) / 46

/-- Global-score drop is an upper bound for the SAME owner's actual deleted
law score. This creates no optimizing contact at a deleted index. -/
theorem same_law_predecessor_drop {n : ℕ} (w : ContraryContact n) :
    actualPredecessorAllowance w ≤ dropSize optimalConstant n := by
  have h := normalizedScore_le_optimalConstant w.X (n - 1)
  have hm := max_le_max_right 0 (sub_le_sub_right h (w.X.normalizedScore n))
  unfold actualPredecessorAllowance dropSize
  rw [w.optimal]
  exact mul_le_mul_of_nonneg_left (by simpa only [w.optimal] using hm) (Nat.cast_nonneg n)

theorem same_law_deleted_caps {n : ℕ} (w : ContraryContact n)
    (one : optimalConstant (n - 1) < 4253 / 10000)
    (two : optimalConstant (n - 2) < 4253 / 10000) :
    w.X.normalizedScore (n - 1) < 4253 / 10000 ∧
      w.X.normalizedScore (n - 2) < 4253 / 10000 :=
  ⟨(normalizedScore_le_optimalConstant w.X (n - 1)).trans_lt one,
    (normalizedScore_le_optimalConstant w.X (n - 2)).trans_lt two⟩

structure TailMethodProviders where
  sourcePin : MathematicalSourcePin
  extraction : ∀ n, 40 ≤ n → ClosedIndexExtraction n esseenConstant
  constant_positive : 0 ≤ esseenConstant
  constant_lower : (4095 / 10000 : ℝ) < esseenConstant
  constant_upper : esseenConstant ≤ 409733 / 1000000
  published_coarse : ∀ n, 1 ≤ n → optimalConstant n ≤ 469 / 1000
  smoothing : SupportFreeSmoothing
  smoothingBrackets : SmoothingIndexBrackets
  auxiliary : AuxiliaryBarrierProviders
  auxiliaryReduction : AuxiliaryScalarReduction
  localProvider : UniformTail.UniformLocalProvider

def TailMethodProviders.contracts (p : TailMethodProviders) : TailContracts optimalConstant esseenConstant where
  constant_upper := p.constant_upper
  auxiliary := (p.auxiliaryReduction.derive p.extraction p.auxiliary.support p.smoothing p.published_coarse
    p.constant_lower p.constant_upper (fun row _n w scope => barrier_resource_reject (p.auxiliary.certificate row) w scope)).1
  strong46 := (p.auxiliaryReduction.derive p.extraction p.auxiliary.support p.smoothing p.published_coarse
    p.constant_lower p.constant_upper (fun row _n w scope => barrier_resource_reject (p.auxiliary.certificate row) w scope)).2
  smoothing := smoothing_first_failure p.smoothing p.smoothingBrackets p.constant_positive p.constant_upper
  local_exclusion := by
    intro n hn hnonnegative hexcess hdrop hcurrent hprevious hpreviousTwo
    obtain ⟨w⟩ := (p.extraction n (by omega)).extract (by linarith)
    apply p.localProvider.reject w
    exact {
      n_ge47 := hn
      excess_nonnegative := by simpa only [w.optimal] using hnonnegative
      excess_le := by simpa only [w.optimal] using hexcess
      decrement := hdrop
      current := by simpa only [w.optimal] using hcurrent
      previousOne := hprevious
      previousTwo := hpreviousTwo }

theorem independent_tail_from_methods (p : TailMethodProviders) :
    ∀ n, 49 ≤ n → optimalConstant n ≤ esseenConstant := tail_composition p.contracts

end BEMap
