import BEMap.Interfaces
import BEMap.Tail
import BEMap.Covers
import BEMap.Root4
import BEMap.SmallIndices
import BEMap.CountRules
import BEMap.TypedPipeline
import BEMap.FourierFamilies
import BEMap.InterfaceChecks

noncomputable section
namespace BEMap

/-- Small real-number comparisons are explicit obligations too. They are kept
separate from the numerical exclusion kernels. -/
structure ConstantComparisons : Prop where
  two : bound2 ≤ esseenConstant
  three : bound3 ≤ esseenConstant
  four : bound4 ≤ esseenConstant

/-- Conditional assembly: every positive integer lies in exactly one of the
finite/tail ranges. The independent tail does not consume `finite`. -/
theorem all_indices_upper
    (constants : ConstantComparisons)
    (finite : FiniteContracts optimalConstant esseenConstant bound2 bound3 bound4)
    (tail : TailContracts optimalConstant esseenConstant) :
    ∀ n, 1 ≤ n → optimalConstant n ≤ esseenConstant := by
  intro n hn
  by_cases h48 : n ≤ 48
  · exact finite_composition finite constants.two constants.three constants.four n hn h48
  · exact tail_composition tail n (by omega)

theorem universal_iid_inequality
    (constants : ConstantComparisons)
    (finite : FiniteContracts optimalConstant esseenConstant bound2 bound3 bound4)
    (tail : TailContracts optimalConstant esseenConstant)
    (X : StandardizedLaw) (n : ℕ) (hn : 1 ≤ n) :
    Real.sqrt n * X.iidKolmogorovDistance n ≤ esseenConstant * X.rho := by
  have hscore := (normalizedScore_le_optimalConstant X n).trans
    (all_indices_upper constants finite tail n hn)
  exact (div_le_iff₀ X.rho_pos).mp hscore

def globalScoreSet : Set ℝ := {r | ∃ n : ℕ, 1 ≤ n ∧ r = optimalConstant n}
def globalConstant : ℝ := sSup globalScoreSet

/-- The independent lower-bound obligation. It requires arbitrarily good
indices/laws; it does not assert attainment at any fixed finite n. -/
def LowerApproximation : Prop :=
  ∀ b : ℝ, b < esseenConstant → ∃ n : ℕ, 1 ≤ n ∧ b < optimalConstant n

theorem sharp_global_constant
    (constants : ConstantComparisons)
    (finite : FiniteContracts optimalConstant esseenConstant bound2 bound3 bound4)
    (tail : TailContracts optimalConstant esseenConstant)
    (lower : LowerApproximation) : globalConstant = esseenConstant := by
  have hu := all_indices_upper constants finite tail
  have hne : globalScoreSet.Nonempty := ⟨optimalConstant 1, 1, by norm_num, rfl⟩
  have hbd : BddAbove globalScoreSet := by
    refine ⟨esseenConstant, ?_⟩
    rintro r ⟨n, hn, rfl⟩
    exact hu n hn
  apply le_antisymm
  · apply csSup_le hne
    rintro r ⟨n, hn, rfl⟩
    exact hu n hn
  · by_contra hbad
    obtain ⟨n, hn, hlarge⟩ := lower globalConstant (lt_of_not_ge hbad)
    have hle : optimalConstant n ≤ globalConstant := le_csSup hbd ⟨n, hn, rfl⟩
    linarith

end BEMap
