import BEMap.Global
import BEMap.Root4
import BEMap.TypedPipeline
import BEMap.Covers
import BEMap.SmallIndices
import BEMap.TailAssembly

/-! Actual conditional assembly from scoped methods. No all-index theorem
is imported as a provider assumption. Strict global failures are retained
while numerical components may establish weak upper bounds. -/
noncomputable section
namespace BEMap

structure FixedIndexMethodProvider (n : ℕ) (floor : ℝ) where
  extraction : FixedIndexExtraction n floor
  method : ∀ w : ContactAt n floor, floor < w.X.normalizedScore n → MethodEvidence w

theorem FixedIndexMethodProvider.upper {n : ℕ} {floor : ℝ}
    (p : FixedIndexMethodProvider n floor) : optimalConstant n ≤ floor := by
  by_contra hbad
  have hfailure := lt_of_not_ge hbad
  obtain ⟨w⟩ := p.extraction.extract hfailure
  have hw : floor < w.X.normalizedScore n := by rw [w.optimal]; exact hfailure
  exact (not_lt_of_ge (p.method w hw).score_bound) hw

inductive PolynomialFamily where | tensorTwo | independenceNullThree

def PolynomialFamily.index : PolynomialFamily → ℕ | .tensorTwo => 2 | .independenceNullThree => 3
def PolynomialFamily.target : PolynomialFamily → ℝ | .tensorTwo => bound2 | .independenceNullThree => bound3
def PolynomialFamily.rhoCap : PolynomialFamily → ℚ | .tensorTwo => 2 | .independenceNullThree => 15 / 8

/-- The two small-index polynomial portfolios use their own exact targets
and the acquired support [-6,6]. They do not require a physical COUNT state. -/
structure SmallPolynomialProvider (family : PolynomialFamily) where
  extraction : FixedIndexExtraction family.index family.target
  localize : ∀ w : ContactAt family.index family.target,
    family.target < w.X.normalizedScore family.index → AlmostBounded w.X 6
  polynomial_bound : ∀ X : StandardizedLaw, AlmostBounded X 6 →
    X.rho ≤ (family.rhoCap : ℝ) → X.normalizedScore family.index ≤ family.target
  large_rho_bound : ∀ X : StandardizedLaw, (family.rhoCap : ℝ) ≤ X.rho →
    X.normalizedScore family.index ≤ family.target

theorem SmallPolynomialProvider.upper {family : PolynomialFamily}
    (p : SmallPolynomialProvider family) : optimalConstant family.index ≤ family.target := by
  by_contra hbad
  have hfailure := lt_of_not_ge hbad
  obtain ⟨w⟩ := p.extraction.extract hfailure
  have hw : family.target < w.X.normalizedScore family.index := by rw [w.optimal]; exact hfailure
  by_cases hrho : w.X.rho ≤ (family.rhoCap : ℝ)
  · exact (not_lt_of_ge (p.polynomial_bound w.X (p.localize w hw) hrho)) hw
  · exact (not_lt_of_ge (p.large_rho_bound w.X (le_of_not_ge hrho))) hw

/-- Canonical n2 construction: numerical tensor semantics and the exact
accepted analytic implication are supplied separately from localization and
the structural large-rho complement. -/
theorem SmallPolynomialProvider.tensorFromCertificate
    (extraction : FixedIndexExtraction 2 bound2)
    (localize : ∀ w : ContactAt 2 bound2, bound2 < w.X.normalizedScore 2 → AlmostBounded w.X 6)
    (payload : TensorCertificate2) (meaning : TensorCertificateMeaning2 payload)
    (analytic : SmallCertificateImplications)
    (largeRho : ∀ X : StandardizedLaw, (2 : ℝ) ≤ X.rho → X.normalizedScore 2 ≤ bound2) :
    SmallPolynomialProvider .tensorTwo where
  extraction := extraction
  localize := localize
  polynomial_bound := analytic.tensor_two payload meaning
  large_rho_bound := largeRho

theorem SmallPolynomialProvider.nullFromCertificate
    (extraction : FixedIndexExtraction 3 bound3)
    (localize : ∀ w : ContactAt 3 bound3, bound3 < w.X.normalizedScore 3 → AlmostBounded w.X 6)
    (payload : NullCertificate3) (meaning : NullCertificateMeaning3 payload)
    (analytic : SmallCertificateImplications)
    (largeRho : ∀ X : StandardizedLaw, (15 / 8 : ℝ) ≤ X.rho → X.normalizedScore 3 ≤ bound3) :
    SmallPolynomialProvider .independenceNullThree where
  extraction := extraction
  localize := localize
  polynomial_bound := by
    simpa [PolynomialFamily.index, PolynomialFamily.target, PolynomialFamily.rhoCap] using
      analytic.null_three payload meaning
  large_rho_bound := by
    simpa [PolynomialFamily.index, PolynomialFamily.target, PolynomialFamily.rhoCap] using largeRho

structure FiveTailEvidence (w : ContactAt 5 esseenConstant) : Prop where
  structural_bound : w.X.normalizedScore 5 ≤ universalFiveTailEnvelope w.X.rho

/-- Separate constructors preserve the n5 method split. In particular the
corner carries no support or physical-gap prerequisite. -/
inductive FiveRegionEvidence (w : ContactAt 5 esseenConstant) : Region5 → Type
  | count (region : LowRegion5) (not_corner : region ≠ .corner)
      (evidence : SupportedCountEvidence w) : FiveRegionEvidence w (.low region)
  | corner (evidence : GapFreeEvidence w) : FiveRegionEvidence w (.low .corner)
  | fourier (band : FourierBand5) (evidence : PrawitzScoreEvidence w)
      (radius : evidence.support.radius = band.requiredRadius)
      (source_cap : (evidence.sqrtUpper : ℝ) / (evidence.rhoLower : ℝ) *
        ((evidence.firstUpper : ℝ) + evidence.secondUpper + evidence.thirdUpper + evidence.fourthUpper)
          ≤ bound4) : FiveRegionEvidence w (.fourier band)
  | tail (evidence : FiveTailEvidence w) : FiveRegionEvidence w .tail

theorem FiveRegionEvidence.score_bound {w : ContactAt 5 esseenConstant} {region : Region5}
    (e : FiveRegionEvidence w region) (inside : region.contains w.X.rho w.X.beta)
    (constant_comparison : bound4 ≤ esseenConstant) : w.X.normalizedScore 5 ≤ esseenConstant := by
  cases e with
  | count region not_corner evidence => exact evidence.score_bound
  | corner evidence => exact evidence.score_bound
  | fourier band evidence radius source_cap => exact evidence.score_bound
  | tail evidence =>
    have htail : 7361 / 4000 ≤ w.X.rho := inside
    have hn := evidence.structural_bound.trans (n5_tail_envelope_bound w.X.rho htail)
    have hsmall : (819 / 2000 : ℝ) ≤ bound4 := by norm_num [bound4]
    exact hn.trans (hsmall.trans constant_comparison)

structure FiveProvider where
  extraction : FixedIndexBound 4 bound4 → FixedIndexExtraction 5 esseenConstant
  envelopes : FixedIndexBound 4 bound4 → ∀ w : ContactAt 5 esseenConstant,
    BetaEnvelope5 w.X.rho w.X.beta
  regions : FixedIndexBound 4 bound4 → ∀ region : Region5,
    ∀ w : ContactAt 5 esseenConstant, region.contains w.X.rho w.X.beta → FiveRegionEvidence w region

theorem FiveProvider.upper (p : FiveProvider) (h4 : FixedIndexBound 4 bound4)
    (constant_comparison : bound4 ≤ esseenConstant) : optimalConstant 5 ≤ esseenConstant := by
  by_contra hbad
  have hfailure := lt_of_not_ge hbad
  obtain ⟨w⟩ := (p.extraction h4).extract hfailure
  obtain ⟨region, inside⟩ := n5_cover w.X.rho w.X.beta w.X.rho_ge_one (p.envelopes h4 w)
  have hbound := (p.regions h4 region w inside).score_bound inside constant_comparison
  have hw : esseenConstant < w.X.normalizedScore 5 := by rw [w.optimal]; exact hfailure
  exact (not_lt_of_ge hbound) hw

structure TwentyFiveProvider where
  extraction : Earlier optimalConstant esseenConstant 25 → FixedIndexExtraction 25 esseenConstant
  predecessor : Earlier optimalConstant esseenConstant 25 →
    PredecessorLicense optimalConstant esseenConstant
  middleEnvelope : ∀ w : ContactAt 25 esseenConstant, MiddleEnvelope25 w.X.rho w.X.beta
  highEnvelope : ∀ w : ContactAt 25 esseenConstant, HighEnvelope25 w.X.rho w.X.beta
  regions : Earlier optimalConstant esseenConstant 25 → ∀ region : Region25,
    ∀ w : ContactAt 25 esseenConstant, region.contains w.X.rho w.X.beta →
    (25 * max (w.X.normalizedScore 24 - esseenConstant) 0 ≤ (5 / 16 : ℝ)) → MethodEvidence w

theorem TwentyFiveProvider.upper (p : TwentyFiveProvider)
    (earlier : Earlier optimalConstant esseenConstant 25) : optimalConstant 25 ≤ esseenConstant := by
  by_contra hbad
  have hfailure := lt_of_not_ge hbad
  obtain ⟨w⟩ := (p.extraction earlier).extract hfailure
  obtain ⟨region, inside⟩ := n25_cover w.X.rho w.X.beta w.X.rho_ge_one
    (p.middleEnvelope w) (p.highEnvelope w)
  have hallowance := same_law_n25_allowance w.X (p.predecessor earlier)
  have hbound := (p.regions earlier region w inside hallowance).score_bound
  have hw : esseenConstant < w.X.normalizedScore 25 := by rw [w.optimal]; exact hfailure
  exact (not_lt_of_ge hbound) hw

/-- Single end-to-end mathematical input interface. Analytic/numerical
providers remain explicit assumptions; the assembly below is checked Lean.
The tail provider is independent of the finite providers. -/
structure EndToEndProviders where
  constants : ConstantComparisons
  one : FixedIndexBound 1 (3704 / 10000)
  two : SmallPolynomialProvider .tensorTwo
  three : SmallPolynomialProvider .independenceNullThree
  four : Root4Provider
  five : FiveProvider
  twentyFive : TwentyFiveProvider
  ordinary : ∀ n, 6 ≤ n → n ≤ 48 → n ≠ 25 →
    Earlier optimalConstant esseenConstant n → FixedIndexMethodProvider n esseenConstant
  tail : TailMethodProviders

theorem EndToEndProviders.finite (p : EndToEndProviders) :
    FiniteContracts optimalConstant esseenConstant bound2 bound3 bound4 where
  one := p.one.bound.trans ((by norm_num [bound4] : (3704 / 10000 : ℝ) ≤ bound4).trans p.constants.four)
  two := p.two.upper
  three := p.three.upper
  four := fun h3 => p.four.upper ⟨h3⟩
  five := fun h4 => p.five.upper ⟨h4⟩ p.constants.four
  ordinary := fun n hn hn48 h25 earlier => (p.ordinary n hn hn48 h25 earlier).upper
  twentyFive := fun earlier => p.twentyFive.upper earlier

theorem all_indices_from_typed_providers (p : EndToEndProviders) :
    ∀ n, 1 ≤ n → optimalConstant n ≤ esseenConstant :=
  all_indices_upper p.constants p.finite p.tail.contracts

theorem sharp_from_typed_providers (p : EndToEndProviders)
    (lower : LowerApproximation) : globalConstant = esseenConstant :=
  sharp_global_constant p.constants p.finite p.tail.contracts lower

end BEMap
