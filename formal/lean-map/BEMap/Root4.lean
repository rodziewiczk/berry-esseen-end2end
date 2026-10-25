import BEMap.Binary
import BEMap.Fourier

/-! The physical ROOT4 family has its OWN canonical Q3 and excess eta.
It is neither the physical gap defect D nor the matching two-point defect.
Source anchors: n4all:eq:reference, n4all:lem:excess,
n4all:lem:common-measure, n4all:prop:certificate. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def root4a (X : StandardizedLaw) : ℝ := (1 - X.beta) / (2 * positiveFirstMoment X)
def root4b (X : StandardizedLaw) : ℝ := (1 + X.beta) / (2 * positiveFirstMoment X)
def root4w (X : StandardizedLaw) : ℝ :=
  4 * positiveFirstMoment X ^ 2 / (1 - X.beta ^ 2)
def root4ReferenceRho (X : StandardizedLaw) : ℝ :=
  (1 + X.beta ^ 2) / Real.sqrt (root4w X * (1 - X.beta ^ 2))
def root4Excess (X : StandardizedLaw) : ℝ := X.rho - root4ReferenceRho X

def root4ReferenceMeasure (X : StandardizedLaw) : Measure ℝ :=
  ENNReal.ofReal (positiveFirstMoment X / root4a X) • Measure.dirac (-root4a X) +
  ENNReal.ofReal (1 - root4w X) • Measure.dirac 0 +
  ENNReal.ofReal (positiveFirstMoment X / root4b X) • Measure.dirac (root4b X)

def root4Weight (X : StandardizedLaw) (x : ℝ) : ℝ :=
  max x 0 * (max x 0 - root4b X) ^ 2 +
    max (-x) 0 * (max (-x) 0 - root4a X) ^ 2

structure Root4CanonicalEvidence (X : StandardizedLaw) : Prop where
  first_moment_pos : 0 < positiveFirstMoment X
  signed_beta : -1 < X.beta ∧ X.beta < 1
  geometry : 0 < root4w X ∧ root4w X ≤ 1
  reference_probability : IsProbabilityMeasure (root4ReferenceMeasure X)
  reference_mean : ∫ x : ℝ, x ∂root4ReferenceMeasure X = 0
  reference_second : ∫ x : ℝ, x ^ 2 ∂root4ReferenceMeasure X = 1
  reference_rho : ∫ x : ℝ, |x| ^ 3 ∂root4ReferenceMeasure X = root4ReferenceRho X
  weight_integrable : Integrable (root4Weight X) (X.law : Measure ℝ)
  excess_integral : root4Excess X = ∫ x, root4Weight X x ∂(X.law : Measure ℝ)
  excess_nonneg : 0 ≤ root4Excess X
  zero_characterization : root4Excess X = 0 ↔ (X.law : Measure ℝ) = root4ReferenceMeasure X

def root4DefectMeasure (X : StandardizedLaw) : Measure ℝ :=
  (X.law : Measure ℝ).withDensity (fun x => ENNReal.ofReal (root4Weight X x / root4Excess X))

inductive Root4Tag where | negative | positive
deriving DecidableEq

def Root4Tag.sign : Root4Tag → ℝ | .negative => -1 | .positive => 1
def Root4Tag.atom (X : StandardizedLaw) : Root4Tag → ℝ | .negative => root4a X | .positive => root4b X
def Root4Tag.Contains (tag : Root4Tag) (x : ℝ) : Prop := 0 < tag.sign * x
def root4ContactMagnitude (X : StandardizedLaw) (x : ℝ) : ℝ :=
  if 0 < x then root4b X else root4a X

def root4K0 (X : StandardizedLaw) (x : ℝ) : ℝ :=
  if root4Weight X x = 0 then 0 else 1 / (root4ContactMagnitude X x ^ 2 * |x|)
def root4K1 (X : StandardizedLaw) (tag : Root4Tag) (x : ℝ) : ℝ := by
  classical
  exact if tag.Contains x ∧ root4Weight X x ≠ 0 then 1 / (|x| - tag.atom X) else 0
def root4K2 (X : StandardizedLaw) (tag : Root4Tag) (x : ℝ) : ℝ := by
  classical
  exact if tag.Contains x ∧ root4Weight X x ≠ 0 then 1 / (|x| - tag.atom X) ^ 2 else 0

/-- Entire Hermite divided difference exp(i sigma q .)[0,c,c,y]. The
power series retains removable contact values; no singular quotient is used.
Summability is an explicit part of the analytic representation interface. -/
def root4ResponseTerm (X : StandardizedLaw) (q x : ℝ) (k : ℕ) : ℂ :=
  let c := root4ContactMagnitude X x
  let sigma : ℝ := if 0 < x then 1 else -1
  (Complex.I * (sigma : ℂ) * (q : ℂ)) ^ (k + 3) / (Nat.factorial (k + 3) : ℂ) *
    ((∑ j ∈ Finset.range (k + 1), ((j + 1 : ℕ) : ℝ) * c ^ j * |x| ^ (k - j) : ℝ) : ℂ)
def root4Response (X : StandardizedLaw) (q x : ℝ) : ℂ := ∑' k : ℕ, root4ResponseTerm X q x k

def root4ReferenceCharacteristic (X : StandardizedLaw) (q : ℝ) : ℂ :=
  ∫ x : ℝ, Complex.exp (Complex.I * ((q * x : ℝ) : ℂ)) ∂root4ReferenceMeasure X

/-- Exactly ONE canonically weighted measure is used at EVERY frequency.
An independently selected nu_q is not an inhabitant of this interface. -/
structure Root4CommonMeasure (X : StandardizedLaw) : Prop where
  excess_positive : 0 < root4Excess X
  probability : IsProbabilityMeasure (root4DefectMeasure X)
  response_summable : ∀ q x, Summable (root4ResponseTerm X q x)
  response_integrable : ∀ q, Integrable (root4Response X q) (root4DefectMeasure X)
  response_bound : ∀ q x, ‖root4Response X q x‖ ≤ |q| ^ 3 / 6
  representation : ∀ q : ℝ, characteristic X q - root4ReferenceCharacteristic X q =
    (root4Excess X : ℂ) * ∫ x, root4Response X q x ∂root4DefectMeasure X
  cost0_integrable : Integrable (root4K0 X) (root4DefectMeasure X)
  cost1_integrable : ∀ tag, Integrable (root4K1 X tag) (root4DefectMeasure X)
  cost2_integrable : ∀ tag, Integrable (root4K2 X tag) (root4DefectMeasure X)
  cost0_budget : root4Excess X * (∫ x, root4K0 X x ∂root4DefectMeasure X) =
    1 - root4w X - (X.law : Measure ℝ).real {0}
  cost2_budget : ∀ tag, root4Excess X * (∫ x, root4K2 X tag x ∂root4DefectMeasure X) =
    positiveFirstMoment X - tag.atom X * (X.law : Measure ℝ).real {tag.sign * tag.atom X}
  cost1_equality : ∀ tag, (∫ x, root4K1 X tag x ∂root4DefectMeasure X) = 0

structure Root4PhysicalClass (w : ContactAt 4 bound4) where
  canonical : Root4CanonicalEvidence w.X
  support : SupportedContact w
  support_radius : support.radius = 17 / 4
  rho_cap : w.X.rho < 46 / 25
  geometry_lower : (625 / 2116 : ℝ) ≤ root4w w.X
  geometry_upper : root4w w.X ≤ 1
  beta_cap : |w.X.beta| ≤ 13 / 20
  positive_excess_measure : 0 < root4Excess w.X → Root4CommonMeasure w.X

abbrev Root4Parent := Fin 20 × Fin 13
def root4ParentWLower (p : Root4Parent) : ℚ :=
  625 / 2116 + (1 - 625 / 2116) * (p.1.val : ℚ) / 20
def root4ParentWUpper (p : Root4Parent) : ℚ :=
  625 / 2116 + (1 - 625 / 2116) * ((p.1.val + 1 : ℕ) : ℚ) / 20
def root4ParentBetaLower (p : Root4Parent) : ℚ := (p.2.val : ℚ) / 20
def root4ParentBetaUpper (p : Root4Parent) : ℚ := ((p.2.val + 1 : ℕ) : ℚ) / 20
def root4ParentContains (p : Root4Parent) (X : StandardizedLaw) : Prop :=
  (root4ParentWLower p : ℝ) ≤ root4w X ∧ root4w X ≤ (root4ParentWUpper p : ℝ) ∧
  (root4ParentBetaLower p : ℝ) ≤ |X.beta| ∧ |X.beta| ≤ (root4ParentBetaUpper p : ℝ)

theorem root4_parent_count : Fintype.card Root4Parent = 260 := by
  simp [Root4Parent]

def root4Threshold (i : Fin 58) : ℚ := -4 + (i.val : ℚ) / 8
abbrev Root4ThresholdJoin := Fin 57
abbrev Root4ExcessBin := Fin 16
abbrev Root4Child := Fin 4

/-- Source-bound accepted analytic/numerical interface. Localization returns
ONE owner together with its actual bounded-law class. It does not require
every unlocalized ContactAt to satisfy a numerical-domain contract.
The bounded physical certificate conclusion is WEAK (<=T). -/
structure Root4Provider where
  localize : FixedIndexBound 3 bound3 → bound4 < optimalConstant 4 →
    Nonempty (Σ w : ContactAt 4 bound4, Root4PhysicalClass w)
  certificate_bound : ∀ w : ContactAt 4 bound4, Root4PhysicalClass w →
    ScoreCap w (4097 / 10000)

theorem Root4Provider.upper (p : Root4Provider) (h3 : FixedIndexBound 3 bound3) :
    optimalConstant 4 ≤ bound4 := by
  by_contra hbad
  have hviolation : bound4 < optimalConstant 4 := lt_of_not_ge hbad
  obtain ⟨⟨w, owner⟩⟩ := p.localize h3 hviolation
  have hcap := (p.certificate_bound w owner).bound
  have hweak : w.X.normalizedScore 4 ≤ bound4 := by
    norm_num [bound4] at hcap ⊢
    exact hcap
  rw [w.optimal] at hweak
  exact (not_lt_of_ge hweak) hviolation

end BEMap
