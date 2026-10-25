import BEMap.Finite
import Mathlib.Tactic.FieldSimp

/-! A scalar proof of the independent n >= 49 tail. The analytic inputs
are explicit fields. In particular, no n = 1,...,48 sharp bound is assumed. -/
namespace BEMap

def dropSize (C : ℕ → ℝ) (n : ℕ) : ℝ :=
  (n : ℝ) * max (C (n - 1) - C n) 0

structure TailContracts (C : ℕ → ℝ) (c : ℝ) : Prop where
  constant_upper : c ≤ 409733 / 1000000
  auxiliary : ∀ n, 45 ≤ n → n ≤ 50 → C n - c < (7 / 10) / (n : ℝ)
  strong46 : C 46 - c < (54 / 100) / 46
  /-- Quantitative consequence to be derived from the stated smoothing theorem.
  Only a sharp bound on the immediately preceding index is consumed. -/
  smoothing : ∀ n, 50 ≤ n → C (n - 1) ≤ c →
    (n : ℝ) * (C n - c) < 29 / 100
  /-- The supported analytic/numerical exclusion, including all own caps. -/
  local_exclusion : ∀ n, 47 ≤ n →
    0 ≤ C n - c → C n - c ≤ (7 / 10) / (n : ℝ) →
    dropSize C n ≤ 19 / 100 →
    C n < 4247 / 10000 → C (n - 1) < 4253 / 10000 →
    C (n - 2) < 4253 / 10000 → False

private theorem current_cap {C : ℕ → ℝ} {c : ℝ} {n : ℕ}
    (hc : c ≤ 409733 / 1000000) (hn : 47 ≤ n)
    (ha : (n : ℝ) * (C n - c) < 7 / 10) : C n < 4247 / 10000 := by
  have hnR : (47 : ℝ) ≤ n := by exact_mod_cast hn
  by_contra h
  have hlow : 14967 / 1000000 ≤ C n - c := by linarith
  nlinarith

private theorem deleted_cap {C : ℕ → ℝ} {c : ℝ} {n : ℕ}
    (hc : c ≤ 409733 / 1000000) (hn : 45 ≤ n)
    (ha : (n : ℝ) * (C n - c) < 7 / 10) : C n < 4253 / 10000 := by
  have hnR : (45 : ℝ) ≤ n := by exact_mod_cast hn
  by_contra h
  have hlow : 15567 / 1000000 ≤ C n - c := by linarith
  nlinarith

private theorem backward_loss {C : ℕ → ℝ} {n : ℕ} (hn : 0 < n)
    (h : 19 / 100 < dropSize C n) :
    C n + (19 / 100) / (n : ℝ) < C (n - 1) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  by_contra hbad
  have hdiff : C (n - 1) - C n ≤ (19 / 100) / (n : ℝ) := by linarith
  have hm := max_le hdiff (by positivity : (0 : ℝ) ≤ (19 / 100) / (n : ℝ))
  have hmul := mul_le_mul_of_nonneg_left hm hnR.le
  have heq : (n : ℝ) * ((19 / 100) / (n : ℝ)) = 19 / 100 := by
    field_simp
  unfold dropSize at h
  rw [heq] at hmul
  linarith

private theorem rollback {C : ℕ → ℝ} {c : ℝ} (h : TailContracts C c)
    {n : ℕ} (hn : 47 ≤ n) (hn49 : n ≤ 49) (ha : 0 ≤ C n - c) :
    C n + (19 / 100) / (n : ℝ) < C (n - 1) := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have h0 := h.auxiliary n (by omega) (by omega)
  have h1 := h.auxiliary (n - 1) (by omega) (by omega)
  have h2 := h.auxiliary (n - 2) (by omega) (by omega)
  have h1R : (0 : ℝ) < (n - 1 : ℕ) := by exact_mod_cast (show 0 < n - 1 by omega)
  have h2R : (0 : ℝ) < (n - 2 : ℕ) := by exact_mod_cast (show 0 < n - 2 by omega)
  have hdrop : 19 / 100 < dropSize C n := by
    by_contra hbad
    exact h.local_exclusion n hn ha h0.le (by linarith)
      (current_cap h.constant_upper hn (by simpa only [mul_comm] using (lt_div_iff₀ hnR).mp h0))
      (deleted_cap h.constant_upper (by omega)
        (by simpa only [mul_comm] using (lt_div_iff₀ h1R).mp h1))
      (deleted_cap h.constant_upper (by omega)
        (by simpa only [mul_comm] using (lt_div_iff₀ h2R).mp h2))
  exact backward_loss (by omega) hdrop

theorem tail_base49 {C : ℕ → ℝ} {c : ℝ} (h : TailContracts C c) : C 49 ≤ c := by
  by_contra hbad
  have a49 : 0 ≤ C 49 - c := by linarith
  have h49 := rollback h (n := 49) (by norm_num) (by norm_num) a49
  norm_num at h49
  have a48 : 0 ≤ C 48 - c := by linarith
  have h48 := rollback h (n := 48) (by norm_num) (by norm_num) a48
  norm_num at h48
  have a47 : 0 ≤ C 47 - c := by linarith
  have h47 := rollback h (n := 47) (by norm_num) (by norm_num) a47
  norm_num at h47
  have hs := h.strong46
  norm_num at hs
  linarith

theorem tail_composition {C : ℕ → ℝ} {c : ℝ} (h : TailContracts C c) :
    ∀ n, 49 ≤ n → C n ≤ c := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro hn
    by_cases e49 : n = 49
    · subst n; exact tail_base49 h
    have hn50 : 50 ≤ n := by omega
    have hp : C (n - 1) ≤ c := ih (n - 1) (by omega) (by omega)
    by_contra hbad
    have ha : 0 ≤ C n - c := by linarith
    have hs := h.smoothing n hn50 hp
    have hnR : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
    have hsmall : (n : ℝ) * (C n - c) < 7 / 10 := by linarith
    have hq : C n - c ≤ (7 / 10) / (n : ℝ) :=
      (le_div_iff₀ hnR).mpr (by simpa only [mul_comm] using hsmall.le)
    have hdrop : dropSize C n ≤ 19 / 100 := by
      have hd : C (n - 1) - C n ≤ 0 := by linarith
      simp only [dropSize, max_eq_right hd, mul_zero]
      norm_num
    have hpCap : C (n - 1) < 4253 / 10000 := by linarith [h.constant_upper]
    have hp2Cap : C (n - 2) < 4253 / 10000 := by
      by_cases e50 : n = 50
      · subst n
        have h48 := h.auxiliary 48 (by norm_num) (by norm_num)
        norm_num at h48 ⊢
        linarith [h.constant_upper]
      · have hp2 := ih (n - 2) (by omega) (by omega)
        linarith [h.constant_upper]
    exact h.local_exclusion n (by omega) ha hq hdrop
      (current_cap h.constant_upper (by omega) hsmall) hpCap hp2Cap

end BEMap
