import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Conditional finite composition. No numerical exclusion is evaluated here. -/
namespace BEMap

def Earlier (C : ℕ → ℝ) (c : ℝ) (n : ℕ) : Prop :=
  ∀ m, 1 ≤ m → m < n → C m ≤ c

/-- Each field is a remaining mathematical obligation, not an asserted theorem.
The arguments to `four` and `five` preserve their stronger predecessor bounds.
`ordinary` is a sufficient sequential route; it does not impose that route on
the independently licensed numerical implementations. -/
structure FiniteContracts (C : ℕ → ℝ) (c b2 b3 b4 : ℝ) : Prop where
  one : C 1 ≤ c
  two : C 2 ≤ b2
  three : C 3 ≤ b3
  four : C 3 ≤ b3 → C 4 ≤ b4
  five : C 4 ≤ b4 → C 5 ≤ c
  ordinary : ∀ n, 6 ≤ n → n ≤ 48 → n ≠ 25 → Earlier C c n → C n ≤ c
  twentyFive : Earlier C c 25 → C 25 ≤ c

theorem finite_composition {C : ℕ → ℝ} {c b2 b3 b4 : ℝ}
    (h : FiniteContracts C c b2 b3 b4)
    (h2 : b2 ≤ c) (h3 : b3 ≤ c) (h4 : b4 ≤ c) :
    ∀ n, 1 ≤ n → n ≤ 48 → C n ≤ c := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro hn hn48
    by_cases e1 : n = 1
    · subst n; exact h.one
    by_cases e2 : n = 2
    · subst n; exact h.two.trans h2
    by_cases e3 : n = 3
    · subst n; exact h.three.trans h3
    by_cases e4 : n = 4
    · subst n; exact (h.four h.three).trans h4
    by_cases e5 : n = 5
    · subst n; exact h.five (h.four h.three)
    have hearlier : Earlier C c n := by
      intro m hm hmn
      exact ih m hmn hm (by omega)
    by_cases e25 : n = 25
    · subst n; exact h.twentyFive hearlier
    exact h.ordinary n (by omega) hn48 e25 hearlier

/-- Sharp and auxiliary predecessor licenses are alternatives. -/
inductive PredecessorLicense (C : ℕ → ℝ) (c : ℝ) : Prop
  | sharp : C 24 ≤ c → PredecessorLicense C c
  | auxiliary : C 24 < c + 1 / 80 → PredecessorLicense C c

def excessAllowance (C : ℕ → ℝ) (c : ℝ) (n : ℕ) : ℝ :=
  (n : ℝ) * max (C (n - 1) - c) 0

theorem n25_allowance {C : ℕ → ℝ} {c : ℝ}
    (h : PredecessorLicense C c) : excessAllowance C c 25 ≤ 5 / 16 := by
  unfold excessAllowance
  norm_num
  cases h with
  | sharp h => rw [max_eq_right (by linarith : C 24 - c ≤ 0)]; norm_num
  | auxiliary h =>
    have hm : max (C 24 - c) 0 ≤ (1 / 80 : ℝ) :=
      max_le (by linarith) (by norm_num)
    linarith

end BEMap
