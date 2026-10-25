import BEMap.Finite
import Mathlib.Data.Rat.Cast.Order

/-! Exact rational cuts. All cells are closed; overlapping seams are intentional.
The signed-beta moment envelopes remain explicit analytic inputs. -/
namespace BEMap

inductive ClosedChain : ℚ → ℚ → Type
  | leaf (a b : ℚ) : ClosedChain a b
  | join {a b c : ℚ} : ClosedChain a b → ClosedChain b c → ClosedChain a c

def ClosedChain.cells {a b : ℚ} : ClosedChain a b → List (ℚ × ℚ)
  | .leaf a b => [(a, b)]
  | .join l r => l.cells ++ r.cells

def inCell (s : ℚ × ℚ) (x : ℝ) : Prop := (s.1 : ℝ) ≤ x ∧ x ≤ (s.2 : ℝ)

theorem ClosedChain.cover {a b : ℚ} (t : ClosedChain a b) {x : ℝ}
    (hx : (a : ℝ) ≤ x ∧ x ≤ (b : ℝ)) :
    ∃ s ∈ t.cells, inCell s x := by
  induction t with
  | leaf a b => exact ⟨(a, b), by simp [cells], hx⟩
  | @join a m b l r ihl ihr =>
    rcases le_total x (m : ℝ) with h | h
    · obtain ⟨s, hs, hx⟩ := ihl ⟨hx.1, h⟩
      exact ⟨s, List.mem_append_left _ hs, hx⟩
    · obtain ⟨s, hs, hx⟩ := ihr ⟨h, hx.2⟩
      exact ⟨s, List.mem_append_right _ hs, hx⟩

def lower25 : ClosedChain 1 (33 / 20) :=
  .join (.leaf 1 (11 / 10)) <|
  .join (.leaf (11 / 10) (6 / 5)) <|
  .join (.leaf (6 / 5) (13 / 10)) <|
  .join (.leaf (13 / 10) (7 / 5)) <|
  .join (.leaf (7 / 5) (3 / 2)) (.leaf (3 / 2) (33 / 20))

def middle25 : ClosedChain (-13 / 20) (307827 / 500000) :=
  .join (.leaf (-13 / 20) 0) <|
  .join (.leaf 0 (4 / 25)) <|
  .join (.leaf (4 / 25) (321 / 1000)) <|
  .join (.leaf (321 / 1000) (2 / 5)) <|
  .join (.leaf (2 / 5) (12 / 25)) <|
  .join (.leaf (12 / 25) (14 / 25)) (.leaf (14 / 25) (307827 / 500000))

def high25 : ClosedChain (-640471 / 1000000) (640471 / 1000000) :=
  .join (.leaf (-640471 / 1000000) 0) <|
  .join (.leaf 0 (321 / 1000)) <|
  .join (.leaf (321 / 1000) (2 / 5)) <|
  .join (.leaf (2 / 5) (12 / 25)) <|
  .join (.leaf (12 / 25) (14 / 25)) (.leaf (14 / 25) (640471 / 1000000))

inductive Region25 where
  | lower (s : ℚ × ℚ) (mem : s ∈ lower25.cells)
  | middle (s : ℚ × ℚ) (mem : s ∈ middle25.cells)
  | high (s : ℚ × ℚ) (mem : s ∈ high25.cells)
  | tail

def Region25.contains (region : Region25) (rho beta : ℝ) : Prop :=
  match region with
  | .lower s _ => inCell s rho
  | .middle s _ => 33 / 20 ≤ rho ∧ rho ≤ 7 / 4 ∧ inCell s beta
  | .high s _ => 7 / 4 ≤ rho ∧ rho ≤ 459061 / 250000 ∧ inCell s beta
  | .tail => 459061 / 250000 ≤ rho

/-- These are moment-envelope obligations, not certificate acceptance flags. -/
def MiddleEnvelope25 (rho beta : ℝ) : Prop :=
  33 / 20 ≤ rho → rho ≤ 7 / 4 → -13 / 20 ≤ beta ∧ beta ≤ 307827 / 500000

def HighEnvelope25 (rho beta : ℝ) : Prop :=
  7 / 4 ≤ rho → rho ≤ 459061 / 250000 →
    -640471 / 1000000 ≤ beta ∧ beta ≤ 640471 / 1000000

theorem n25_cover (rho beta : ℝ) (hrho : 1 ≤ rho)
    (hmid : MiddleEnvelope25 rho beta) (hhigh : HighEnvelope25 rho beta) :
    ∃ region : Region25, region.contains rho beta := by
  by_cases hlo : rho ≤ 33 / 20
  · obtain ⟨s, hs, hx⟩ := lower25.cover (by norm_num; exact ⟨hrho, hlo⟩)
    exact ⟨.lower s hs, hx⟩
  by_cases hmi : rho ≤ 7 / 4
  · have hleft : 33 / 20 ≤ rho := by linarith
    obtain ⟨s, hs, hx⟩ := middle25.cover (x := beta)
      (by norm_num; simpa only [neg_div] using hmid hleft hmi)
    exact ⟨.middle s hs, hleft, hmi, hx⟩
  by_cases hhi : rho ≤ 459061 / 250000
  · have hleft : 7 / 4 ≤ rho := by linarith
    obtain ⟨s, hs, hx⟩ := high25.cover (x := beta)
      (by norm_num; simpa only [neg_div] using hhigh hleft hhi)
    exact ⟨.high s hs, hleft, hhi, hx⟩
  exact ⟨.tail, by change 459061 / 250000 ≤ rho; linarith⟩

theorem n25_region_count :
    lower25.cells.length = 6 ∧ middle25.cells.length = 7 ∧
    high25.cells.length = 6 ∧
    lower25.cells.length + middle25.cells.length + high25.cells.length + 1 = 20 := by
  norm_num [lower25, middle25, high25, ClosedChain.cells]

/-- The same witness is passed to the domain test and the exclusion.
No extremizer from a different index can be substituted by this theorem. -/
theorem n25_exclude_by_cover {W : Type} (rho beta : W → ℝ)
    (hrho : ∀ w, 1 ≤ rho w)
    (hmid : ∀ w, MiddleEnvelope25 (rho w) (beta w))
    (hhigh : ∀ w, HighEnvelope25 (rho w) (beta w))
    (reject : ∀ region : Region25, ∀ w, region.contains (rho w) (beta w) → False) :
    ∀ _w : W, False := by
  intro w
  obtain ⟨region, hw⟩ := n25_cover (rho w) (beta w) (hrho w) (hmid w) (hhigh w)
  exact reject region w hw

/-- Equality at the high/tail seam belongs to the tail. -/
example (beta : ℝ) : Region25.tail.contains (459061 / 250000) beta := le_rfl

end BEMap
