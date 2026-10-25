import BEMap.Cover25
import BEMap.Domain

/-! Exact n5 and floor31 region coverage. These theorems prove domain unions,
not the analytic/numerical exclusions on the individual domains. -/
namespace BEMap

def betaFive2 : ℚ := 84729828287999 / 250000000000000
def betaFive3 : ℚ := 35139006743001 / 100000000000000

theorem betaFive2_endpoint_certificate :
    (1 + betaFive2 ^ 2) ^ 2 - (237 / 200 : ℚ) ^ 2 * (1 - betaFive2 ^ 2) > 0 := by
  norm_num [betaFive2]

theorem betaFive3_endpoint_certificate :
    (1 + betaFive3 ^ 2) ^ 2 - (6 / 5 : ℚ) ^ 2 * (1 - betaFive3 ^ 2) > 0 := by
  norm_num [betaFive3]

theorem betaFive_enclosures_positive : 0 < betaFive2 ∧ betaFive2 < betaFive3 ∧ betaFive3 < 1 := by
  norm_num [betaFive2, betaFive3]

inductive LowRegion5 where
  | b0 | bn | b2s0 | b2s1 | b2s2 | b2s3
  | b3s0 | b3t0 | b3t1 | b3s2 | b3t2 | b3lower | corner
deriving DecidableEq

def LowRegion5.contains (r : LowRegion5) (rho beta : ℝ) : Prop :=
  match r with
  | .b0 => 1 ≤ rho ∧ rho ≤ 11 / 10
  | .bn => 11 / 10 ≤ rho ∧ rho ≤ 23 / 20
  | .b2s0 => 23 / 20 ≤ rho ∧ rho ≤ 467 / 400 ∧ -(betaFive2 : ℝ) ≤ beta ∧ beta ≤ 1 / 5
  | .b2s1 => 23 / 20 ≤ rho ∧ rho ≤ 467 / 400 ∧ 1 / 5 ≤ beta ∧ beta ≤ (betaFive2 : ℝ)
  | .b2s2 => 467 / 400 ≤ rho ∧ rho ≤ 237 / 200 ∧ -(betaFive2 : ℝ) ≤ beta ∧ beta ≤ 1 / 5
  | .b2s3 => 467 / 400 ≤ rho ∧ rho ≤ 237 / 200 ∧ 1 / 5 ≤ beta ∧ beta ≤ (betaFive2 : ℝ)
  | .b3s0 => 237 / 200 ≤ rho ∧ rho ≤ 477 / 400 ∧ -(betaFive3 : ℝ) ≤ beta ∧ beta ≤ 1 / 5
  | .b3t0 => 237 / 200 ≤ rho ∧ rho ≤ 477 / 400 ∧ 1 / 5 ≤ beta ∧ beta ≤ 3 / 10
  | .b3t1 => 237 / 200 ≤ rho ∧ rho ≤ 477 / 400 ∧ 3 / 10 ≤ beta ∧ beta ≤ (betaFive3 : ℝ)
  | .b3s2 => 477 / 400 ≤ rho ∧ rho ≤ 6 / 5 ∧ -(betaFive3 : ℝ) ≤ beta ∧ beta ≤ 1 / 5
  | .b3t2 => 477 / 400 ≤ rho ∧ rho ≤ 6 / 5 ∧ 1 / 5 ≤ beta ∧ beta ≤ 3 / 10
  | .b3lower => 477 / 400 ≤ rho ∧ rho ≤ 6 / 5 ∧ 3 / 10 ≤ beta ∧ beta ≤ 17 / 50
  | .corner => 477 / 400 ≤ rho ∧ rho ≤ 6 / 5 ∧ 17 / 50 ≤ beta ∧ beta ≤ (betaFive3 : ℝ)

def lowRegions5 : List LowRegion5 :=
  [.b0, .bn, .b2s0, .b2s1, .b2s2, .b2s3, .b3s0, .b3t0, .b3t1,
    .b3s2, .b3t2, .b3lower, .corner]

theorem lowRegions5_complete (r : LowRegion5) : r ∈ lowRegions5 := by
  cases r <;> simp [lowRegions5]

inductive FourierBand5 where | f0 | f1 | f2 | f3 | f4 | f5
deriving DecidableEq

def FourierBand5.contains (b : FourierBand5) (rho : ℝ) : Prop :=
  match b with
  | .f0 => 6 / 5 ≤ rho ∧ rho ≤ 5 / 4
  | .f1 => 5 / 4 ≤ rho ∧ rho ≤ 7 / 5
  | .f2 => 7 / 5 ≤ rho ∧ rho ≤ 3 / 2
  | .f3 => 3 / 2 ≤ rho ∧ rho ≤ 8 / 5
  | .f4 => 8 / 5 ≤ rho ∧ rho ≤ 17 / 10
  | .f5 => 17 / 10 ≤ rho ∧ rho ≤ 7361 / 4000

def FourierBand5.requiredRadius : FourierBand5 → ℚ
  | .f0 => 13 / 5 | .f1 => 117 / 40 | .f2 => 25 / 8
  | .f3 => 133 / 40 | .f4 => 7 / 2 | .f5 => 15 / 4

def fourierBands5 : List FourierBand5 := [.f0, .f1, .f2, .f3, .f4, .f5]

theorem fourierBands5_complete (b : FourierBand5) : b ∈ fourierBands5 := by
  cases b <;> simp [fourierBands5]

inductive Method5 where
  | resourceCount
  | gapFreeCorner
  | supportedFourier (requiredRadius : ℚ)
  | universalRhoTail
deriving DecidableEq

inductive Region5 where
  | low (r : LowRegion5)
  | fourier (b : FourierBand5)
  | tail
deriving DecidableEq

def Region5.contains (r : Region5) (rho beta : ℝ) : Prop :=
  match r with
  | .low r => r.contains rho beta
  | .fourier b => b.contains rho
  | .tail => 7361 / 4000 ≤ rho

def Region5.method : Region5 → Method5
  | .low .corner => .gapFreeCorner
  | .low _ => .resourceCount
  | .fourier b => .supportedFourier b.requiredRadius
  | .tail => .universalRhoTail

/-- The moment theorem plus outward scalar endpoint certificates must supply
these implications. They concern signed beta and remain separate obligations. -/
structure BetaEnvelope5 (rho beta : ℝ) : Prop where
  second : rho ≤ 237 / 200 → -(betaFive2 : ℝ) ≤ beta ∧ beta ≤ (betaFive2 : ℝ)
  third : rho ≤ 6 / 5 → -(betaFive3 : ℝ) ≤ beta ∧ beta ≤ (betaFive3 : ℝ)

theorem fourier5_cover (rho : ℝ) (hl : 6 / 5 ≤ rho) (hu : rho ≤ 7361 / 4000) :
    ∃ b : FourierBand5, b.contains rho := by
  by_cases h0 : rho ≤ 5 / 4
  · exact ⟨.f0, hl, h0⟩
  by_cases h1 : rho ≤ 7 / 5
  · exact ⟨.f1, by change 5 / 4 ≤ rho ∧ rho ≤ 7 / 5; constructor <;> linarith⟩
  by_cases h2 : rho ≤ 3 / 2
  · exact ⟨.f2, by change 7 / 5 ≤ rho ∧ rho ≤ 3 / 2; constructor <;> linarith⟩
  by_cases h3 : rho ≤ 8 / 5
  · exact ⟨.f3, by change 3 / 2 ≤ rho ∧ rho ≤ 8 / 5; constructor <;> linarith⟩
  by_cases h4 : rho ≤ 17 / 10
  · exact ⟨.f4, by change 8 / 5 ≤ rho ∧ rho ≤ 17 / 10; constructor <;> linarith⟩
  exact ⟨.f5, by change 17 / 10 ≤ rho ∧ rho ≤ 7361 / 4000; constructor <;> linarith⟩

theorem n5_cover (rho beta : ℝ) (hrho : 1 ≤ rho) (env : BetaEnvelope5 rho beta) :
    ∃ r : Region5, r.contains rho beta := by
  by_cases h0 : rho ≤ 11 / 10
  · exact ⟨.low .b0, hrho, h0⟩
  by_cases hn : rho ≤ 23 / 20
  · exact ⟨.low .bn, by change 11 / 10 ≤ rho ∧ rho ≤ 23 / 20; constructor <;> linarith⟩
  by_cases h2a : rho ≤ 467 / 400
  · have hb := env.second (by linarith)
    by_cases hbeta : beta ≤ 1 / 5
    · exact ⟨.low .b2s0, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h2a, hb.1, hbeta⟩⟩
    · exact ⟨.low .b2s1, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h2a, by linarith, hb.2⟩⟩
  by_cases h2b : rho ≤ 237 / 200
  · have hb := env.second h2b
    by_cases hbeta : beta ≤ 1 / 5
    · exact ⟨.low .b2s2, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h2b, hb.1, hbeta⟩⟩
    · exact ⟨.low .b2s3, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h2b, by linarith, hb.2⟩⟩
  by_cases h3a : rho ≤ 477 / 400
  · have hb := env.third (by linarith)
    by_cases hbeta : beta ≤ 1 / 5
    · exact ⟨.low .b3s0, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3a, hb.1, hbeta⟩⟩
    by_cases hbeta3 : beta ≤ 3 / 10
    · exact ⟨.low .b3t0, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3a, by linarith, hbeta3⟩⟩
    · exact ⟨.low .b3t1, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3a, by linarith, hb.2⟩⟩
  by_cases h3b : rho ≤ 6 / 5
  · have hb := env.third h3b
    by_cases hbeta : beta ≤ 1 / 5
    · exact ⟨.low .b3s2, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3b, hb.1, hbeta⟩⟩
    by_cases hbeta3 : beta ≤ 3 / 10
    · exact ⟨.low .b3t2, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3b, by linarith, hbeta3⟩⟩
    by_cases hcorner : beta ≤ 17 / 50
    · exact ⟨.low .b3lower, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3b, by linarith, hcorner⟩⟩
    · exact ⟨.low .corner, by change _ ∧ _ ∧ _ ∧ _; exact ⟨by linarith, h3b, by linarith, hb.2⟩⟩
  by_cases htail : rho ≤ 7361 / 4000
  · obtain ⟨b, hb⟩ := fourier5_cover rho (by linarith) htail
    exact ⟨.fourier b, hb⟩
  exact ⟨.tail, by change 7361 / 4000 ≤ rho; linarith⟩

theorem n5_region_inventory : lowRegions5.length = 13 ∧ fourierBands5.length = 6 ∧
    lowRegions5.length + fourierBands5.length + 1 = 20 := by decide

theorem corner_is_separate : Region5.method (.low .corner) = .gapFreeCorner := rfl

def resourceRegions5 : List LowRegion5 := lowRegions5.filter fun r => decide (r ≠ .corner)

theorem n5_resource_region_count : resourceRegions5.length = 12 := by decide

theorem FourierBand5.requiredRadius_pos (b : FourierBand5) : 0 < b.requiredRadius := by
  cases b <;> norm_num [requiredRadius]

/-- The same actual witness is used by the envelope, domain test and every
method-specific rejection. The cover cannot swap in a different extremizer. -/
theorem n5_exclude_by_cover {W : Type} (rho beta : W → ℝ)
    (hrho : ∀ w, 1 ≤ rho w)
    (env : ∀ w, BetaEnvelope5 (rho w) (beta w))
    (reject : ∀ region : Region5, ∀ w, region.contains (rho w) (beta w) → False) :
    ∀ _w : W, False := by
  intro w
  obtain ⟨region, hw⟩ := n5_cover (rho w) (beta w) (hrho w) (env w)
  exact reject region w hw

/-- The beta=17/50 seam is retained by both low-domain methods. -/
theorem n5_corner_seam (rho : ℝ) (hl : 477 / 400 ≤ rho) (hu : rho ≤ 6 / 5) :
    Region5.contains (.low .b3lower) rho (17 / 50) ∧
      Region5.contains (.low .corner) rho (17 / 50) := by
  constructor
  · exact ⟨hl, hu, by norm_num, le_rfl⟩
  · exact ⟨hl, hu, le_rfl, by norm_num [betaFive3]⟩

noncomputable def universalFiveTailEnvelope (rho : ℝ) : ℝ := (3031 / 10000) * (1 + (323 / 500) / rho)

theorem universalFiveTailEnvelope_antitone {rho small : ℝ} (hsmall : 0 < small)
    (horder : small ≤ rho) : universalFiveTailEnvelope rho ≤ universalFiveTailEnvelope small := by
  have hdiv : (323 / 500 : ℝ) / rho ≤ (323 / 500 : ℝ) / small :=
    div_le_div_of_nonneg_left (by norm_num) hsmall horder
  unfold universalFiveTailEnvelope
  linarith

theorem n5_tail_envelope_bound (rho : ℝ) (hrho : 7361 / 4000 ≤ rho) :
    universalFiveTailEnvelope rho ≤ 819 / 2000 := by
  exact (universalFiveTailEnvelope_antitone (by norm_num) hrho).trans
    (by norm_num [universalFiveTailEnvelope])

theorem n5_tail_target_gap : (819 / 2000 : ℚ) < 4097 / 10000 := by norm_num

def floor31Chain : ClosedChain 1 (7361 / 4000) :=
  .join (.leaf 1 (11 / 10)) <|
  .join (.leaf (11 / 10) (6 / 5)) <|
  .join (.leaf (6 / 5) (13 / 10)) <|
  .join (.leaf (13 / 10) (7 / 5)) <|
  .join (.leaf (7 / 5) (3 / 2)) <|
  .join (.leaf (3 / 2) (33 / 20)) <|
  .join (.leaf (33 / 20) (7 / 4)) (.leaf (7 / 4) (7361 / 4000))

def Floor31Band := {s : ℚ × ℚ // s ∈ floor31Chain.cells}
def Floor31Band.contains (b : Floor31Band) (rho : ℝ) : Prop := inCell b.val rho

theorem floor31_cover (rho : ℝ) (hl : 1 ≤ rho) (hu : rho ≤ 7361 / 4000) :
    ∃ b : Floor31Band, b.contains rho := by
  obtain ⟨s, hs, hx⟩ := floor31Chain.cover (x := rho) (by norm_num; exact ⟨hl, hu⟩)
  exact ⟨⟨s, hs⟩, hx⟩

theorem floor31_band_count : floor31Chain.cells.length = 8 := by
  norm_num [floor31Chain, ClosedChain.cells]

end BEMap
