import BEMap.Domain

/-! Small exact inference kernels for COUNT leaf semantics. These seven tags
describe the selected final verifier in docs/contracts/COUNT-RULES.md, not
every historical search engine. The facts below do not by themselves bind a
matrix or cap to the actual task; that necessary semantic binding is a
separate input to each inference. -/
namespace BEMap

inductive OrdinaryCountRule where
  | emptyPhase | emptyThetaVariance | emptySharpBox | emptyJointCubics
  | emptyRhoUpper | emptyRhoVariance | passTarget
deriving DecidableEq

def OrdinaryCountRule.sourceTag : OrdinaryCountRule → String
  | .emptyPhase => "EMPTY_PHASE"
  | .emptyThetaVariance => "EMPTY_ACQUIRED_THETA_VARIANCE"
  | .emptySharpBox => "EMPTY_SHARP_BOX"
  | .emptyJointCubics => "EMPTY_JOINT_CUBICS"
  | .emptyRhoUpper => "EMPTY_RHO_UPPER"
  | .emptyRhoVariance => "EMPTY_ACQUIRED_RHO_VARIANCE"
  | .passTarget => "PASS_TARGET"

/-- Candidate rational witness for an already specified necessary system
A x <= b. Rows/columns must be bound to the actual source constraints and
unknown moment vector; an arbitrary inconsistent matrix proves nothing about
the probability law. Generation of the multipliers is untrusted. -/
structure FarkasCandidate (dimension rows : ℕ) where
  matrix : Fin rows → Fin dimension → ℚ
  rhs : Fin rows → ℚ
  multiplier : Fin rows → ℚ

def FarkasCandidate.Valid {dimension rows : ℕ} (c : FarkasCandidate dimension rows) : Prop :=
  (∀ i, 0 ≤ c.multiplier i) ∧
  (∀ j, (∑ i : Fin rows, c.multiplier i * c.matrix i j) = 0) ∧
  (∑ i : Fin rows, c.multiplier i * c.rhs i) < 0

instance {dimension rows : ℕ} (c : FarkasCandidate dimension rows) : Decidable c.Valid := by
  unfold FarkasCandidate.Valid
  infer_instance

def FarkasCandidate.check {dimension rows : ℕ} (c : FarkasCandidate dimension rows) : Bool :=
  decide c.Valid

theorem FarkasCandidate.check_sound {dimension rows : ℕ} {c : FarkasCandidate dimension rows}
    (hcheck : c.check = true) (x : Fin dimension → ℝ)
    (necessary : ∀ i, (∑ j : Fin dimension, (c.matrix i j : ℝ) * x j) ≤ (c.rhs i : ℝ)) :
    False := by
  have hv : c.Valid := of_decide_eq_true hcheck
  have hsum : (∑ i : Fin rows, (c.multiplier i : ℝ) *
      (∑ j : Fin dimension, (c.matrix i j : ℝ) * x j)) ≤
      ∑ i : Fin rows, (c.multiplier i : ℝ) * (c.rhs i : ℝ) := by
    apply Finset.sum_le_sum
    intro i _
    exact mul_le_mul_of_nonneg_left (necessary i) (by exact_mod_cast hv.1 i)
  have hzero : (∑ i : Fin rows, (c.multiplier i : ℝ) *
      (∑ j : Fin dimension, (c.matrix i j : ℝ) * x j)) = 0 := by
    calc
      _ = ∑ j : Fin dimension, ∑ i : Fin rows,
          ((c.multiplier i : ℝ) * (c.matrix i j : ℝ)) * x j := by
        simp_rw [Finset.mul_sum, ← mul_assoc]
        rw [Finset.sum_comm]
      _ = ∑ j : Fin dimension, (∑ i : Fin rows,
          (c.multiplier i : ℝ) * (c.matrix i j : ℝ)) * x j := by
        apply Finset.sum_congr rfl
        intro j _
        rw [Finset.sum_mul]
      _ = 0 := by
        apply Finset.sum_eq_zero
        intro j _
        have hj : (∑ i : Fin rows, (c.multiplier i : ℝ) * (c.matrix i j : ℝ)) = 0 := by
          exact_mod_cast hv.2.1 j
        rw [hj, zero_mul]
  have hnegative : (∑ i : Fin rows, (c.multiplier i : ℝ) * (c.rhs i : ℝ)) < 0 := by
    exact_mod_cast hv.2.2
  rw [hzero] at hsum
  linarith

theorem strict_interval_exclusion {a b : ClosedInterval} {x : ℝ}
    (ha : a.Contains x) (hb : b.Contains x)
    (separated : a.upper < b.lower ∨ b.upper < a.lower) : False := by
  rcases separated with h | h
  · have hr : (a.upper : ℝ) < b.lower := by exact_mod_cast h
    linarith [ha.2, hb.1]
  · have hr : (b.upper : ℝ) < a.lower := by exact_mod_cast h
    linarith [hb.2, ha.1]

/-- Source theta/lambda relation, then monotonicity of the exact real
expression. No monotonicity of a truncated/rounded helper is assumed. -/
theorem theta_variance_contraction {index variance varianceUpper theta thetaUpper lambda : ℝ}
    (hn : 0 ≤ index) (hv : variance ≤ varianceUpper) (hvUpper : 0 ≤ varianceUpper)
    (ht : 0 ≤ theta) (htUpper : theta ≤ thetaUpper) (htOne : thetaUpper < 1)
    (identity : lambda = index * variance * theta / (1 - theta)) :
    lambda ≤ index * varianceUpper * thetaUpper / (1 - thetaUpper) := by
  have hTheta : 0 ≤ thetaUpper := ht.trans htUpper
  have hnum := mul_le_mul (mul_le_mul_of_nonneg_left hv hn) htUpper ht
    (mul_nonneg hn hvUpper)
  rw [identity]
  exact (div_le_div_of_nonneg_right hnum (by linarith)).trans
    (div_le_div_of_nonneg_left (mul_nonneg (mul_nonneg hn hvUpper) hTheta)
      (by linarith) (by linarith))

theorem strict_rho_exclusion {X : StandardizedLaw} {lower upper : ℚ}
    (hlower : (lower : ℝ) ≤ X.rho) (hupper : X.rho ≤ (upper : ℝ))
    (strict : upper < lower) : False := by
  have hs : (upper : ℝ) < lower := by exact_mod_cast strict
  linarith

end BEMap
