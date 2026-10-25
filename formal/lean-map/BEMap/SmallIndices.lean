import BEMap.Domain

/-! Exact polynomial meanings for n2 and n3. The two bases have different
normalizations. This specifies certificate semantics, not a production
Bernstein evaluator or a full formal proof of the analytic implications. -/
noncomputable section
namespace BEMap

abbrev TensorIndex2 := {ij : Fin 5 × Fin 5 // ij.1 ≤ ij.2}
abbrev NullIndex3 := {ijk : Fin 7 × Fin 7 × Fin 7 //
  ijk.1 ≤ ijk.2.1 ∧ ijk.2.1 ≤ ijk.2.2 ∧
  (ijk.2.2.val < 5 ∨ ijk.1.val = 1 ∨ ijk.1.val = 2 ∨
    ijk.2.1.val = 1 ∨ ijk.2.1.val = 2 ∨ ijk.2.2.val = 1 ∨ ijk.2.2.val = 2)}

theorem tensor_index2_count : Fintype.card TensorIndex2 = 15 := by decide
theorem null_index3_count : Fintype.card NullIndex3 = 59 := by decide

/-- Explicit lexicographic decoder keys. A JSON vector must follow these
tuples, never an implementation-dependent enumeration of the Fintype. -/
def tensorCoefficientKeys2 : List (ℕ × ℕ) :=
  (List.range 5).flatMap fun i => (List.range (5 - i)).map fun d => (i, i + d)
def nullCoefficientKeys3 : List (ℕ × ℕ × ℕ) :=
  (List.range 7).flatMap fun i =>
    (List.range (7 - i)).flatMap fun dj =>
      let j := i + dj
      (List.range (7 - j)).filterMap fun dk =>
        let k := j + dk
        if k < 5 ∨ i = 1 ∨ i = 2 ∨ j = 1 ∨ j = 2 ∨ k = 1 ∨ k = 2
        then some (i, j, k) else none

theorem small_coefficient_key_lengths :
    tensorCoefficientKeys2.length = 15 ∧ nullCoefficientKeys3.length = 59 := by decide

def tensorFeature2 (i : Fin 5) (x : ℝ) : ℝ :=
  match i.val with | 0 => 1 | 1 => x | 2 => x ^ 2 | 3 => x ^ 3 | _ => |x| ^ 3
def nullFeature3 (i : Fin 7) (x : ℝ) : ℝ :=
  match i.val with
  | 0 => 1 | 1 => x | 2 => x ^ 2 - 1 | 3 => x ^ 3 | 4 => |x| ^ 3 | 5 => x ^ 4 | _ => x ^ 5
def tensorMean2 (i : Fin 5) (gamma rho : ℝ) : ℝ :=
  match i.val with | 0 => 1 | 1 => 0 | 2 => 1 | 3 => gamma | _ => rho

def tensorTerm2 (ij : TensorIndex2) (u v : ℝ) : ℝ :=
  if ij.val.1 = ij.val.2 then tensorFeature2 ij.val.1 u * tensorFeature2 ij.val.2 v
  else tensorFeature2 ij.val.1 u * tensorFeature2 ij.val.2 v +
    tensorFeature2 ij.val.2 u * tensorFeature2 ij.val.1 v

def tensorMajorant2 (c : TensorIndex2 → ℚ) (u v : ℝ) : ℝ :=
  ∑ ij : TensorIndex2, (c ij : ℝ) * tensorTerm2 ij u v
def tensorExpectation2 (c : TensorIndex2 → ℚ) (gamma rho : ℝ) : ℝ :=
  ∑ ij : TensorIndex2, (c ij : ℝ) *
    (if ij.val.1 = ij.val.2 then tensorMean2 ij.val.1 gamma rho * tensorMean2 ij.val.2 gamma rho
     else 2 * tensorMean2 ij.val.1 gamma rho * tensorMean2 ij.val.2 gamma rho)

def distinctPermutations3 (t : Fin 7 × Fin 7 × Fin 7) : Finset (Fin 7 × Fin 7 × Fin 7) :=
  {t, (t.1, t.2.2, t.2.1), (t.2.1, t.1, t.2.2),
    (t.2.1, t.2.2, t.1), (t.2.2, t.1, t.2.1), (t.2.2, t.2.1, t.1)}

def nullTerm3 (t : NullIndex3) (u v w : ℝ) : ℝ :=
  (∑ p ∈ distinctPermutations3 t.val,
    nullFeature3 p.1 u * nullFeature3 p.2.1 v * nullFeature3 p.2.2 w) /
      ((distinctPermutations3 t.val).card : ℝ)

def nullMajorant3 (c : NullIndex3 → ℚ) (u v w : ℝ) : ℝ :=
  ∑ t : NullIndex3, (c t : ℝ) * nullTerm3 t u v w
/-- Algebraic surviving-factor helper, NOT a table of actual feature means:
features5/6 can have nonzero means. An admissible triple containing one of
them also contains feature1 or2 in another coordinate, so its product mean
vanishes by independence. No assumption EX^4=0 or EX^5=0 is made. -/
def nullSurvivingMean3 (i : Fin 7) (gamma rho : ℝ) : ℝ :=
  match i.val with | 0 => 1 | 3 => gamma | 4 => rho | _ => 0
def nullExpectation3 (c : NullIndex3 → ℚ) (gamma rho : ℝ) : ℝ :=
  ∑ t : NullIndex3, (c t : ℝ) * nullSurvivingMean3 t.val.1 gamma rho *
    nullSurvivingMean3 t.val.2.1 gamma rho * nullSurvivingMean3 t.val.2.2 gamma rho

def smallMomentDomain (cap gamma rho : ℝ) : Prop :=
  |gamma| ≤ cap ∧ 1 ≤ rho ∧ rho ≤ cap ∧ rho ^ 2 * (gamma ^ 2 + 4) - (gamma ^ 2 + 2) ^ 2 ≥ 0

def twoThresholdLower (j : Fin 70) : ℚ := -5 / 2 + (j.val : ℚ) / 20
def twoThresholdUpper (j : Fin 70) : ℚ := twoThresholdLower j + 1 / 20

structure TensorCertificate2 where
  coefficients : Fin 70 → TensorIndex2 → ℚ

structure NullCertificate3 where
  thresholds : Fin 111 → ClosedInterval
  coefficients : Fin 111 → NullIndex3 → ℚ

/-- These semantic statements are the checker outputs needed by the analytic
certificate-implication lemmas. A coefficient array or terminal PASS alone
does not inhabit them. N3 uses the larger [-7,7]^3 cube deliberately. -/
structure TensorCertificateMeaning2 (p : TensorCertificate2) : Prop where
  pointwise : ∀ j u v, |u| ≤ 6 → |v| ≤ 6 →
    (if u + v ≤ (twoThresholdUpper j : ℝ) then (1 : ℝ) else 0) ≤
      tensorMajorant2 (p.coefficients j) u v
  moment_scalar : ∀ j gamma rho, smallMomentDomain 2 gamma rho →
    tensorExpectation2 (p.coefficients j) gamma rho ≤
      ProbabilityLaw.cdf ProbabilityLaw.standardNormal ((twoThresholdLower j : ℝ) / Real.sqrt 2) +
        (2 / 7) * rho

structure NullCertificateMeaning3 (p : NullCertificate3) : Prop where
  first : (p.thresholds ⟨0, by omega⟩).lower = -7 / 2
  last : (p.thresholds ⟨110, by omega⟩).upper = 3 / 2
  adjacent : ∀ j : Fin 110,
    (p.thresholds ⟨j.val, by omega⟩).upper = (p.thresholds ⟨j.val + 1, by omega⟩).lower
  pointwise : ∀ j u v w, |u| ≤ 7 → |v| ≤ 7 → |w| ≤ 7 →
    (if u + v + w ≤ ((p.thresholds j).upper : ℝ) then (1 : ℝ) else 0) ≤
      nullMajorant3 (p.coefficients j) u v w
  moment_scalar : ∀ j gamma rho, smallMomentDomain (15 / 8) gamma rho →
    nullExpectation3 (p.coefficients j) gamma rho ≤
      ProbabilityLaw.cdf ProbabilityLaw.standardNormal (((p.thresholds j).lower : ℝ) / Real.sqrt 3) +
        (59 / 250) * rho

/-- Source-exact accepted analytic implications, including the two exterior
threshold tails and whole-law reflection. They apply only to the stated
bounded, small-rho classes. Large rho has a separate structural route. -/
structure SmallCertificateImplications : Prop where
  tensor_two : ∀ p : TensorCertificate2, TensorCertificateMeaning2 p →
    ∀ X : StandardizedLaw, AlmostBounded X 6 → X.rho ≤ 2 → X.normalizedScore 2 ≤ bound2
  null_three : ∀ p : NullCertificate3, NullCertificateMeaning3 p →
    ∀ X : StandardizedLaw, AlmostBounded X 6 → X.rho ≤ 15 / 8 → X.normalizedScore 3 ≤ bound3

end BEMap
