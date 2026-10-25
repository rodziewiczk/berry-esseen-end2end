import BEMap.FourierFamilies

/-! Complete source HIGH families at split1/2. The six-term WINDOW50 and
supported compensated-power bounds are accepted analytic theorem parameters.
The program-facing data are frozen rational parameters/cells, while the law,
product event and whole-cell modulus assertions are semantic proof evidence. -/
noncomputable section
open MeasureTheory Set
namespace BEMap.HighFamilies

def tailL (x : ℝ) : ℝ := (x + 2) / (x ^ 2 + 4 * x + 2)
def windowB : ℚ := 9 / 10
def windowH (r : ℚ) : ℚ := 333 / 106 - (22 / 7) ^ 3 * r ^ 2 / 6
def dampingPolynomial (M u : ℚ) : ℚ := 1 - u + (M + 3) * u ^ 2 / 12
def windowC (M : ℚ) : ℚ :=
  (1 - max (dampingPolynomial M (1 / 4)) (dampingPolynomial M (81 / 100))) / 2
def windowC0 (M : ℚ) : ℚ := 1 / 8 - (M + 3) / 384
def windowSlope (M : ℚ) : ℚ := (1 - (M + 3) * 53 / 600) / 2
def windowKappa (a d0 : ℚ) : ℚ := a * (23 / 48) ^ 2 * d0 ^ 2

inductive GammaChoice where | pearson | licensed | minimum
deriving DecidableEq

structure Window50Parameters where
  fourth : ℚ
  fourth_at_least_one : 1 ≤ fourth
  eventMass : ℚ
  mass_positive : 0 < eventMass
  mass_at_most_one : eventMass ≤ 1
  distanceLower : ℚ
  distance_positive : 0 < distanceLower
  eventSecond : ℚ
  eventSecond_nonneg : 0 ≤ eventSecond
  radius : ℚ
  radius_positive : 0 < radius
  radius_upper : radius ≤ 1 / 4
  h_positive : 0 < windowH radius
  damping_positive : 0 < windowC fourth
  gamma : ℚ
  gamma_nonneg : 0 ≤ gamma
  gammaChoice : GammaChoice
  refinedFirst : Bool
  first_gate : refinedFirst = true → 0 < windowSlope fourth
  refinedZero : Bool

def Window50Parameters.gammaEnvelope (p : Window50Parameters) : ℝ :=
  match p.gammaChoice with
  | .pearson => Real.sqrt ((p.fourth : ℝ) - 1)
  | .licensed => (p.gamma : ℝ)
  | .minimum => min (p.gamma : ℝ) (Real.sqrt ((p.fourth : ℝ) - 1))

def productLaw (X : StandardizedLaw) : Measure (ℝ × ℝ) :=
  (X.law : Measure ℝ).prod (X.law : Measure ℝ)

/-- An actual measurable event under P×P. No artificial distance density or
frequency-only kernel may replace this event or its conditional second moment. -/
structure Window50LawEvidence (X : StandardizedLaw) (p : Window50Parameters) where
  fourth_integrable : Integrable (fun x : ℝ => x ^ 4) (X.law : Measure ℝ)
  fourth_bound : fourthMoment X ≤ (p.fourth : ℝ)
  gamma_bound : |X.gamma| ≤ p.gammaEnvelope
  event : Set (ℝ × ℝ)
  measurable_event : MeasurableSet event
  probability_lower : (p.eventMass : ℝ) ≤ (productLaw X).real event
  distance_lower : ∀ᵐ pair ∂(productLaw X).restrict event,
    (p.distanceLower : ℝ) ≤ |pair.1 - pair.2|
  second_integrable : IntegrableOn (fun pair : ℝ × ℝ => (pair.1 - pair.2) ^ 2) event (productLaw X)
  conditional_second : (∫ pair in event, (pair.1 - pair.2) ^ 2 ∂productLaw X) /
    (productLaw X).real event ≤ (p.eventSecond : ℝ)

theorem Window50LawEvidence.event_mass_positive {X : StandardizedLaw} {p : Window50Parameters}
    (law : Window50LawEvidence X p) : 0 < (productLaw X).real law.event := by
  have hp : (0 : ℝ) < p.eventMass := by exact_mod_cast p.mass_positive
  exact hp.trans_le law.probability_lower

def windowS3 : ℝ := (∑ j ∈ Finset.range 20, 1 / (((j + 1 : ℕ) : ℝ) ^ 3)) + 1 / 800
def windowS5 (r : ℝ) : ℝ :=
  (∑ j ∈ Finset.range 20, 1 / ((((j + 1 : ℕ) : ℝ) - r) ^ 5)) + 1 / (4 * (20 - r) ^ 4)

def windowFirst (n : ℕ) (p : Window50Parameters) : ℝ :=
  let simple := 2 * Real.sqrt n * Real.exp (-(n : ℝ) * (windowC p.fourth : ℝ))
  if p.refinedFirst then min simple
    (2 * Real.sqrt n * Real.exp (-(n : ℝ) * (windowC0 p.fourth : ℝ)) *
      tailL ((n : ℝ) * (windowSlope p.fourth : ℝ) / 4)) else simple
def windowCore (n : ℕ) (p : Window50Parameters) : ℝ :=
  (p.eventSecond : ℝ) / (4 * Real.pi * Real.sqrt Real.pi * (windowH p.radius : ℝ) * Real.sqrt (p.eventMass : ℝ)) *
    (windowS3 + 3 * windowS5 p.radius /
      ((n : ℝ) * (p.eventMass : ℝ) * (windowH p.radius : ℝ) ^ 2))
def windowWing (n : ℕ) (p : Window50Parameters) : ℝ :=
  (p.eventSecond : ℝ) * Real.sqrt n / (2 * Real.pi ^ 2) *
    Real.exp (-(n : ℝ) * p.eventMass * (windowH p.radius : ℝ) ^ 2 * (p.radius : ℝ) ^ 2)
def windowZero (n : ℕ) (p : Window50Parameters) : ℝ :=
  let x := (n : ℝ) * (windowKappa p.eventMass p.distanceLower : ℝ) * (windowB : ℝ) ^ 2
  let simple := Real.exp (-x) /
    (2 * (windowB : ℝ) ^ 4 * (windowKappa p.eventMass p.distanceLower : ℝ) * Real.sqrt n)
  if p.refinedZero then min simple (Real.sqrt n * Real.exp (-x) / (2 * (windowB : ℝ) ^ 2) * tailL x)
    else simple
def windowFar (n : ℕ) (p : Window50Parameters) : ℝ :=
  Real.sqrt n / (2 * (windowB : ℝ) ^ 2) *
    Real.exp (-(n : ℝ) * p.eventMass * (23 / 48 : ℝ) ^ 2)
def windowComparator (n : ℕ) (p : Window50Parameters) : ℝ :=
  Real.sqrt n * Real.exp (-(n : ℝ) / 8) * (2 * tailL ((n : ℝ) / 8) + p.gammaEnvelope / 3)
def window50ScaledUpper (n : ℕ) (p : Window50Parameters) : ℝ :=
  windowFirst n p + windowCore n p + windowWing n p + windowZero n p + windowFar n p + windowComparator n p

/-- Accepted source theorem HIGH_WINDOW50, including integrability of the
actual full compensated remainder and all six terms, at the fixed split1/2. -/
def Window50Theorem : Prop :=
  ∀ (n : ℕ) (floor : ℝ) (w : ContactAt n floor) (p : Window50Parameters), 5 ≤ n →
    Window50LawEvidence w.X p →
    IntegrableOn (highIntegrand w) (Ioi (halfFrequencySplit.value : ℝ)) ∧
      Real.sqrt n * highIntegral w halfFrequencySplit ≤ window50ScaledUpper n p

structure Window50UniformInputs (p : Window50Parameters) where
  lowerIndex : ℕ
  at_least_five : 5 ≤ lowerIndex
  damping_gate : 1 < 2 * (lowerIndex : ℚ) * windowC p.fourth
  wing_gate : 1 < 2 * (lowerIndex : ℚ) * p.eventMass * (windowH p.radius) ^ 2 * p.radius ^ 2
  far_gate : 1 < 2 * (lowerIndex : ℚ) * p.eventMass * (23 / 48) ^ 2
  comparator_gate : 1 < 2 * (lowerIndex : ℚ) * (1 / 8)
  refined_first_gate : p.refinedFirst = true → 1 < 2 * (lowerIndex : ℚ) * windowC0 p.fourth
  refined_zero_gate : p.refinedZero = true →
    1 / 4 ≤ (lowerIndex : ℚ) * windowKappa p.eventMass p.distanceLower * windowB ^ 2

/-- Uniformity is a theorem about these exact bounding expressions, even
when the law/event varies with the actual index. No clipped exponential
approximation or pointwise Laguerre result substitutes for these gates. -/
def Window50UniformTheorem : Prop :=
  ∀ p : Window50Parameters, ∀ i : Window50UniformInputs p, ∀ n : ℕ,
    i.lowerIndex ≤ n → window50ScaledUpper n p ≤ window50ScaledUpper i.lowerIndex p

structure ScaledHighRounding (n : ℕ) (scaledUpper : ℝ) where
  upper : ℚ
  nonneg : 0 ≤ upper
  outward : scaledUpper ≤ Real.sqrt n * (upper : ℝ)

/-- Keeps the exact source-strength scaled conclusion. The unscaled HIGH
upper is cap/sqrt(actual n), never implicitly cap/sqrt(floor N). -/
structure CompleteScaledHigh {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (cap : ℝ) : Prop where
  integrable : IntegrableOn (highIntegrand w) (Ioi (halfFrequencySplit.value : ℝ))
  bound : Real.sqrt n * highIntegral w halfFrequencySplit ≤ cap

theorem window50_uniform_scaled {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (analytic : Window50Theorem) (uniform : Window50UniformTheorem)
    (p : Window50Parameters) (i : Window50UniformInputs p) (hn : i.lowerIndex ≤ n)
    (law : Window50LawEvidence w.X p) : CompleteScaledHigh w (window50ScaledUpper i.lowerIndex p) where
  integrable := (analytic n floor w p (i.at_least_five.trans hn) law).1
  bound := ((analytic n floor w p (i.at_least_five.trans hn) law).2).trans (uniform p i n hn)

def window50_high {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (analytic : Window50Theorem) (p : Window50Parameters) (hn : 5 ≤ n)
    (law : Window50LawEvidence w.X p) (rounding : ScaledHighRounding n (window50ScaledUpper n p)) :
    HighBound w halfFrequencySplit where
  value := rounding.upper
  nonneg := rounding.nonneg
  integrable := (analytic n floor w p hn law).1
  bound := by
    have h := ((analytic n floor w p hn law).2).trans rounding.outward
    have hp : 0 < Real.sqrt n := Real.sqrt_pos.mpr (by exact_mod_cast (show 0 < n by omega))
    nlinarith

def window50_uniform_high {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (analytic : Window50Theorem) (uniform : Window50UniformTheorem)
    (p : Window50Parameters) (i : Window50UniformInputs p) (hn : i.lowerIndex ≤ n)
    (law : Window50LawEvidence w.X p)
    (rounding : ScaledHighRounding n (window50ScaledUpper i.lowerIndex p)) :
    HighBound w halfFrequencySplit where
  value := rounding.upper
  nonneg := rounding.nonneg
  integrable := (window50_uniform_scaled analytic uniform p i hn law).integrable
  bound := by
    have h := (window50_uniform_scaled analytic uniform p i hn law).bound.trans rounding.outward
    have hn5 : 5 ≤ n := i.at_least_five.trans hn
    have hp : 0 < Real.sqrt n := Real.sqrt_pos.mpr (by exact_mod_cast (show 0 < n by omega))
    nlinarith

structure SupportedPowerParameters where
  radius : ℚ
  radius_pos : 0 < radius
  rho : ℚ
  rho_pos : 0 < rho
  fourth : ℚ
  fourth_nonneg : 0 ≤ fourth
  fifth : ℚ
  fifth_nonneg : 0 ≤ fifth
  gammaSquared : ℚ
  gamma_nonneg : 0 ≤ gammaSquared
  cutoff : ℚ
  cutoff_gt_half : 1 / 2 < cutoff
  cutoff_lt_pi : (cutoff : ℝ) < Real.pi

structure SupportedPowerPartition (p : SupportedPowerParameters) where
  count : ℕ
  nonempty : 0 < count
  knots : Fin (count + 1) → ℚ
  first : knots ⟨0, by omega⟩ = 1 / 2
  last : knots ⟨count, by omega⟩ = p.cutoff
  strict : ∀ j : Fin count, knots j.castSucc < knots j.succ

def SupportedPowerPartition.cell {p : SupportedPowerParameters} (partition : SupportedPowerPartition p)
    (j : Fin partition.count) : ClosedInterval :=
  ⟨partition.knots j.castSucc, partition.knots j.succ, (partition.strict j).le⟩

def powerGaussian (u : ℝ) : ℝ := Real.exp (-u ^ 2 / 2)
def powerB (p : SupportedPowerParameters) (u : ℝ) : ℝ := Real.sqrt (p.gammaSquared : ℝ) * u ^ 3 / 6
def powerW (p : SupportedPowerParameters) (u : ℝ) : ℝ := powerGaussian u * Real.sqrt (1 + powerB p u ^ 2)
def powerD0 (u : ℝ) : ℝ := Real.cos u - powerGaussian u
def powerD1 (p : SupportedPowerParameters) (u : ℝ) : ℝ := powerD0 u + ((p.rho : ℝ) - 1) * u ^ 3 / 6
def powerA (p : SupportedPowerParameters) (u : ℝ) : ℝ := max |powerD0 u| |powerD1 p u|
def powerImaginary (p : SupportedPowerParameters) (u : ℝ) : ℝ :=
  min ((p.fourth : ℝ) * u ^ 4 / 24) ((p.fifth : ℝ) * u ^ 5 / 120) + powerB p u * (1 - powerGaussian u)
def powerRf (p : SupportedPowerParameters) (u : ℝ) : ℝ :=
  Real.sqrt (powerA p u ^ 2 + powerImaginary p u ^ 2)
def compensatedPower (n : ℕ) (p : SupportedPowerParameters) (modulus u : ℝ) : ℝ :=
  powerRf p u * (∑ j ∈ Finset.range n, modulus ^ j * powerW p u ^ (n - 1 - j)) +
    powerGaussian u ^ n * (n : ℝ) * ((n : ℝ) - 1) * powerB p u ^ 2 / 2 *
      (1 + powerB p u ^ 2) ^ (((n : ℝ) - 2) / 2 : ℝ)
def trianglePower (n : ℕ) (p : SupportedPowerParameters) (modulus u : ℝ) : ℝ :=
  modulus ^ n + powerGaussian u ^ n * Real.sqrt (1 + (n : ℝ) ^ 2 * powerB p u ^ 2)

structure SupportedPowerCells (n : ℕ) (p : SupportedPowerParameters) (partition : SupportedPowerPartition p) where
  modulus : Fin partition.count → ℚ
  modulus_nonneg : ∀ j, 0 ≤ modulus j
  upper : Fin partition.count → ℚ
  upper_nonneg : ∀ j, 0 ≤ upper j
  whole_cell : ∀ j : Fin partition.count, ∀ u : ℝ, (partition.cell j).Contains u →
    min (compensatedPower n p (modulus j) u) (trianglePower n p (modulus j) u) ≤ (upper j : ℝ)

structure SupportedPowerLawEvidence (X : StandardizedLaw) (n : ℕ)
    (p : SupportedPowerParameters) (partition : SupportedPowerPartition p)
    (cells : SupportedPowerCells n p partition) : Prop where
  support : AlmostBounded X p.radius
  rho_bound : X.rho ≤ (p.rho : ℝ)
  fourth_integrable : Integrable (fun x : ℝ => x ^ 4) (X.law : Measure ℝ)
  fifth_integrable : Integrable (fun x : ℝ => |x| ^ 5) (X.law : Measure ℝ)
  fourth_bound : fourthMoment X ≤ (p.fourth : ℝ)
  fifth_bound : absoluteFifthMoment X ≤ (p.fifth : ℝ)
  gamma_bound : X.gamma ^ 2 ≤ (p.gammaSquared : ℝ)
  modulus : ∀ j : Fin partition.count, ∀ u : ℝ, (partition.cell j).Contains u →
    ‖characteristic X u‖ ≤ (cells.modulus j : ℝ)

def supportedPowerTail (n : ℕ) (p : SupportedPowerParameters) : ℝ :=
  1 / (2 * (p.cutoff : ℝ) ^ 2) +
    Real.exp (-(n : ℝ) * (p.cutoff : ℝ) ^ 2 / 2) / ((n : ℝ) * (p.cutoff : ℝ)) *
      ((p.cutoff : ℝ)⁻¹ ^ 3 + (n : ℝ) * Real.sqrt (p.gammaSquared : ℝ) / 6)
def supportedPowerScaledUpper (n : ℕ) (p : SupportedPowerParameters)
    (partition : SupportedPowerPartition p) (cells : SupportedPowerCells n p partition) : ℝ :=
  Real.sqrt n * ((∑ j : Fin partition.count, (cells.upper j : ℝ) *
    (((partition.cell j).lower : ℝ)⁻¹ ^ 2 - ((partition.cell j).upper : ℝ)⁻¹ ^ 2) / 2) +
      supportedPowerTail n p)

/-- Accepted source theorem rescore:lem:compensated-high. Its output includes
the finite closed partition AND the entire infinite characteristic/Gaussian
tail. It does not assume a physical gap or a predecessor bound. -/
def SupportedPowerTheorem : Prop :=
  ∀ (n : ℕ) (floor : ℝ) (w : ContactAt n floor) (p : SupportedPowerParameters)
    (partition : SupportedPowerPartition p) (cells : SupportedPowerCells n p partition), 2 ≤ n →
    SupportedPowerLawEvidence w.X n p partition cells →
    IntegrableOn (highIntegrand w) (Ioi (halfFrequencySplit.value : ℝ)) ∧
      Real.sqrt n * highIntegral w halfFrequencySplit ≤ supportedPowerScaledUpper n p partition cells

def supported_power_high {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (analytic : SupportedPowerTheorem) (p : SupportedPowerParameters)
    (partition : SupportedPowerPartition p) (cells : SupportedPowerCells n p partition)
    (hn : 2 ≤ n) (law : SupportedPowerLawEvidence w.X n p partition cells)
    (rounding : ScaledHighRounding n (supportedPowerScaledUpper n p partition cells)) :
    HighBound w halfFrequencySplit where
  value := rounding.upper
  nonneg := rounding.nonneg
  integrable := (analytic n floor w p partition cells hn law).1
  bound := by
    have h := ((analytic n floor w p partition cells hn law).2).trans rounding.outward
    have hp : 0 < Real.sqrt n := Real.sqrt_pos.mpr (by exact_mod_cast (show 0 < n by omega))
    nlinarith

/-- Minimum is allowed between complete HIGH bounds for this same contact,
actual index and split. This is not a coordinatewise minimum of LOW triples. -/
def min_complete_high {n : ℕ} {floor : ℝ} {w : ContactAt n floor}
    (first second : HighBound w halfFrequencySplit) : HighBound w halfFrequencySplit where
  value := min first.value second.value
  nonneg := le_min first.nonneg second.nonneg
  integrable := first.integrable
  bound := by rw [Rat.cast_min]; exact le_min first.bound second.bound

end BEMap.HighFamilies
