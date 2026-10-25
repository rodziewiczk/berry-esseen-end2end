import BEMap.Foundations.OptimalConstant
import BEMap.Finite

/-! Semantic domain types. There is deliberately no implicit coercion between
raw/normalized thresholds, different contacts, or differently weighted caps. -/
noncomputable section
open MeasureTheory
namespace BEMap

def esseenConstant : ℝ := (3 + Real.sqrt 10) / (6 * Real.sqrt (2 * Real.pi))
def bound2 : ℝ := 2 * Real.sqrt 2 / 7
def bound3 : ℝ := 59 * Real.sqrt 3 / 250
def bound4 : ℝ := 4097 / 10000

def StandardizedLaw.beta (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, x * |x| ∂(X.law : Measure ℝ)

def AlmostBounded (X : StandardizedLaw) (R : ℝ) : Prop :=
  ∀ᵐ x ∂(X.law : Measure ℝ), |x| ≤ R

structure ClosedInterval where
  lower : ℚ
  upper : ℚ
  ordered : lower ≤ upper
deriving DecidableEq

def ClosedInterval.Contains (i : ClosedInterval) (x : ℝ) : Prop :=
  (i.lower : ℝ) ≤ x ∧ x ≤ (i.upper : ℝ)

structure RawThreshold where
  value : ℝ

structure NormalizedThreshold where
  value : ℝ

/-- The threshold is normalized; `rawThreshold` is the ONLY designated
conversion used by the raw-sum and Fourier interfaces below. The critical
floor is a parameter, not hard-coded to C_E. -/
structure ContactAt (n : ℕ) (floor : ℝ) where
  X : StandardizedLaw
  threshold : NormalizedThreshold
  critical : floor ≤ X.normalizedScore n
  optimal : X.normalizedScore n = optimalConstant n
  positive_closed :
    ProbabilityLaw.cdf (ProbabilityLaw.normalizedSum X.law n) threshold.value -
      ProbabilityLaw.cdf ProbabilityLaw.standardNormal threshold.value =
        X.iidKolmogorovDistance n

def ContactAt.rawThreshold {n : ℕ} {floor : ℝ} (w : ContactAt n floor) : RawThreshold :=
  ⟨Real.sqrt n * w.threshold.value⟩

abbrev ContraryContact (n : ℕ) := ContactAt n esseenConstant

/-- Minimal attainment obligation for proving an upper bound: extract an
unrestricted contact at this SAME floor from a strict violation. This does
not silently assume attainment at the equality case. -/
structure FixedIndexExtraction (n : ℕ) (floor : ℝ) : Prop where
  positive_index : 1 ≤ n
  extract : floor < optimalConstant n → Nonempty (ContactAt n floor)

/-- Stronger optional extraction input, when equality attainment is required. -/
structure ClosedIndexExtraction (n : ℕ) (floor : ℝ) : Prop where
  positive_index : 1 ≤ n
  extract : floor ≤ optimalConstant n → Nonempty (ContactAt n floor)

theorem ClosedIndexExtraction.toStrict {n : ℕ} {floor : ℝ}
    (e : ClosedIndexExtraction n floor) : FixedIndexExtraction n floor :=
  ⟨e.positive_index, fun h => e.extract h.le⟩

def ContactExtractionAt (floor : ℝ) : Prop :=
  ∀ n, 1 ≤ n → floor < optimalConstant n → Nonempty (ContactAt n floor)

abbrev ContactExtraction := ContactExtractionAt esseenConstant

theorem upper_of_contact_exclusion_at {n : ℕ} {floor : ℝ}
    (extract : FixedIndexExtraction n floor)
    (reject : ∀ _w : ContactAt n floor, False) : optimalConstant n ≤ floor := by
  by_contra h
  obtain ⟨w⟩ := extract.extract (lt_of_not_ge h)
  exact reject w

theorem upper_of_contact_exclusion (extract : ContactExtraction) {n : ℕ}
    (hn : 1 ≤ n) (reject : ∀ _w : ContraryContact n, False) :
    optimalConstant n ≤ esseenConstant :=
  upper_of_contact_exclusion_at ⟨hn, extract n hn⟩ reject

/-- Semantic proof of an all-law fixed-index bound, with its index and cap
in the type. Numerical output alone is not an inhabitant of this structure. -/
structure FixedIndexBound (n : ℕ) (cap : ℝ) : Prop where
  bound : optimalConstant n ≤ cap

structure ScoreCap {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (cap : ℚ) : Prop where
  bound : w.X.normalizedScore n ≤ (cap : ℝ)

structure SupportedContact {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  radius : ℚ
  radius_pos : 0 < radius
  bounded : AlmostBounded w.X radius

/-- Acquired signed support is separate data. A larger symmetric radius can
lose the hypotheses of a regional native rule even when it remains valid. -/
structure AsymmetricSupport {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  radiusMinus : ℚ
  radiusPlus : ℚ
  minus_positive : 0 < radiusMinus
  plus_positive : 0 < radiusPlus
  bounded : ∀ᵐ x ∂(w.X.law : Measure ℝ),
    -(radiusMinus : ℝ) ≤ x ∧ x ≤ (radiusPlus : ℝ)

def AsymmetricSupport.toSymmetric {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (s : AsymmetricSupport w) : SupportedContact w where
  radius := max s.radiusMinus s.radiusPlus
  radius_pos := lt_of_lt_of_le s.minus_positive (le_max_left _ _)
  bounded := by
    filter_upwards [s.bounded] with x hx
    have hm : (s.radiusMinus : ℝ) ≤ ((max s.radiusMinus s.radiusPlus : ℚ) : ℝ) := by
      exact_mod_cast (le_max_left s.radiusMinus s.radiusPlus)
    have hp : (s.radiusPlus : ℝ) ≤ ((max s.radiusMinus s.radiusPlus : ℚ) : ℝ) := by
      exact_mod_cast (le_max_right s.radiusMinus s.radiusPlus)
    exact abs_le.mpr ⟨by linarith, hx.2.trans hp⟩

def SupportedContact.toAsymmetric {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (s : SupportedContact w) : AsymmetricSupport w where
  radiusMinus := s.radius
  radiusPlus := s.radius
  minus_positive := s.radius_pos
  plus_positive := s.radius_pos
  bounded := s.bounded.mono fun _ hx => abs_le.mp hx

/-- Strictness is explicit evidence, not inferred from a closed domain cover. -/
structure StrictScoreBound {n : ℕ} {floor : ℝ} (w : ContactAt n floor) where
  margin : ℚ
  margin_pos : 0 < margin
  bound : w.X.normalizedScore n ≤ floor - (margin : ℝ)

theorem StrictScoreBound.reject {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (h : StrictScoreBound w) : False := by
  have hp : (0 : ℝ) < h.margin := by exact_mod_cast h.margin_pos
  linarith [h.bound, w.critical]

end BEMap
