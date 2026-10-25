import BEMap.Physical

/-! Binary coordinates and conditional-count laws. The law parameter X is
retained across index transfers; no contact at the transferred index is assumed. -/
noncomputable section
open MeasureTheory Set
namespace BEMap

def positiveProbability (X : StandardizedLaw) : ℝ := (X.law : Measure ℝ).real (Ioi 0)
def positiveFirstMoment (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, max x 0 ∂(X.law : Measure ℝ)
def binaryVariance (X : StandardizedLaw) : ℝ :=
  positiveProbability X * (1 - positiveProbability X)
def inverseBinaryScale (X : StandardizedLaw) : ℝ :=
  binaryVariance X / positiveFirstMoment X
def signIndicator (x : ℝ) : ℝ := if 0 < x then 1 else 0
def binaryResidual (X : StandardizedLaw) (x : ℝ) : ℝ :=
  inverseBinaryScale X * x - signIndicator x + positiveProbability X
def noiseVariance (X : StandardizedLaw) : ℝ :=
  ∫ x : ℝ, binaryResidual X x ^ 2 ∂(X.law : Measure ℝ)
def weightedNoise (X : StandardizedLaw) (n : ℕ) : ℝ := (n : ℝ) * noiseVariance X
def residualTheta (X : StandardizedLaw) : ℝ := noiseVariance X / inverseBinaryScale X ^ 2

def conditionalResidualMeasure (X : StandardizedLaw) (positive : Bool) : Measure ℝ :=
  let s := if positive then Ioi (0 : ℝ) else Iic (0 : ℝ)
  Measure.map (binaryResidual X) (((X.law : Measure ℝ) s)⁻¹ • (X.law : Measure ℝ).restrict s)

/-- Both conditional laws are explicitly bound to restrictions of THIS law.
The atom at zero belongs to the nonpositive class. No division by noise is
used, so zero-noise laws remain in this interface. -/
structure BinaryModel (X : StandardizedLaw) where
  probability_pos : 0 < positiveProbability X
  probability_lt_one : positiveProbability X < 1
  first_moment_pos : 0 < positiveFirstMoment X
  residual_measurable : Measurable (binaryResidual X)
  negativeLaw : ProbabilityLaw
  positiveLaw : ProbabilityLaw
  negative_exact : (negativeLaw : Measure ℝ) = conditionalResidualMeasure X false
  positive_exact : (positiveLaw : Measure ℝ) = conditionalResidualMeasure X true
  negative_centered : ∫ u : ℝ, u ∂(negativeLaw : Measure ℝ) = 0
  positive_centered : ∫ u : ℝ, u ∂(positiveLaw : Measure ℝ) = 0
  negative_integrable : Integrable (fun u : ℝ => u) (negativeLaw : Measure ℝ)
  positive_integrable : Integrable (fun u : ℝ => u) (positiveLaw : Measure ℝ)
  residual_sq_integrable : Integrable (fun x : ℝ => binaryResidual X x ^ 2) (X.law : Measure ℝ)
  variance_identity : noiseVariance X = inverseBinaryScale X ^ 2 - binaryVariance X
  noise_nonneg : 0 ≤ noiseVariance X
  theta_nonneg : 0 ≤ residualTheta X
  theta_lt_one : residualTheta X < 1

def countLaw {X : StandardizedLaw} (b : BinaryModel X) (n : ℕ) (k : Fin (n + 1)) : ProbabilityLaw :=
  ProbabilityLaw.conv (ProbabilityLaw.convolutionPow b.negativeLaw (n - k.val))
    (ProbabilityLaw.convolutionPow b.positiveLaw k.val)

def binomialMass (n : ℕ) (p : ℝ) (k : Fin (n + 1)) : ℝ :=
  (n.choose k.val : ℝ) * p ^ k.val * (1 - p) ^ (n - k.val)

def countPhase {n : ℕ} {floor : ℝ} (w : ContactAt n floor) (k : Fin (n + 1)) : ℝ :=
  (n : ℝ) * positiveProbability w.X + inverseBinaryScale w.X * w.rawThreshold.value - k.val

/-- Incoming = closed probability. Strict outgoing = its exact complement,
including the atom-at-the-plane convention, rather than P(W >= u). -/
def incomingProbability {X : StandardizedLaw} (b : BinaryModel X)
    {n : ℕ} (k : Fin (n + 1)) (u : ℝ) : ℝ := ProbabilityLaw.cdf (countLaw b n k) u
def strictOutgoingProbability {X : StandardizedLaw} (b : BinaryModel X)
    {n : ℕ} (k : Fin (n + 1)) (u : ℝ) : ℝ := 1 - incomingProbability b k u

structure CountIdentity {n : ℕ} {floor : ℝ} (w : ContactAt n floor)
    (b : BinaryModel w.X) : Prop where
  mixture : rawCDF w = ∑ k : Fin (n + 1),
    binomialMass n (positiveProbability w.X) k *
      incomingProbability b k ((n : ℝ) * positiveProbability w.X +
        inverseBinaryScale w.X * w.rawThreshold.value - k.val)

structure NoiseCap (X : StandardizedLaw) (cap : ℚ) : Prop where
  bound : noiseVariance X ≤ (cap : ℝ)
structure WeightedNoiseCap (X : StandardizedLaw) (n : ℕ) (cap : ℚ) : Prop where
  bound : weightedNoise X n ≤ (cap : ℝ)

theorem weighted_noise_index_transfer (X : StandardizedLaw) (m n : ℕ) :
    (n : ℝ) * weightedNoise X m = (m : ℝ) * weightedNoise X n := by
  unfold weightedNoise
  ring

theorem n25_to_n24_noise (X : StandardizedLaw) :
    weightedNoise X 24 = (24 / 25 : ℝ) * weightedNoise X 25 := by
  unfold weightedNoise
  norm_num
  ring

inductive NoiseBranch (X : StandardizedLaw) (n : ℕ) : Prop
  | zero : weightedNoise X n = 0 → NoiseBranch X n
  | positive : 0 < weightedNoise X n → NoiseBranch X n

theorem noise_branches_complete {X : StandardizedLaw} (b : BinaryModel X) (n : ℕ) :
    NoiseBranch X n := by
  have hn : 0 ≤ weightedNoise X n := mul_nonneg (Nat.cast_nonneg n) b.noise_nonneg
  rcases eq_or_lt_of_le hn with h | h
  · exact .zero h.symm
  · exact .positive h

end BEMap
