import BEMap.Domain
import Mathlib.Data.List.OfFn

/-! Mathematical certificate semantics. Search/parsing/execution are outside
the trust boundary; a checker is usable only together with its soundness proof.
The count-tree layer below proves the original-product coverage structurally. -/
namespace BEMap

inductive CountCoordinate where
  | probability | weightedNoise | alpha | phase | rawInward0
deriving DecidableEq

structure CountPoint (n : ℕ) where
  root : Fin (n + 1)
  p : ℝ
  lambda : ℝ
  alpha : ℝ
  phase : ℝ
  rawInward0 : ℝ

def CountPoint.coordinate {n : ℕ} (x : CountPoint n) : CountCoordinate → ℝ
  | .probability => x.p | .weightedNoise => x.lambda | .alpha => x.alpha
  | .phase => x.phase | .rawInward0 => x.rawInward0

structure CountBox (n : ℕ) where
  root : Fin (n + 1)
  bounds : CountCoordinate → ClosedInterval

def CountBox.Contains {n : ℕ} (b : CountBox n) (x : CountPoint n) : Prop :=
  x.root = b.root ∧ ∀ c, (b.bounds c).Contains (x.coordinate c)

structure StrictBoxCut {n : ℕ} (b : CountBox n) (c : CountCoordinate) where
  value : ℚ
  interior : (b.bounds c).lower < value ∧ value < (b.bounds c).upper

def CountBox.left {n : ℕ} (b : CountBox n) (c : CountCoordinate) (cut : StrictBoxCut b c) : CountBox n :=
  ⟨b.root, fun d => if d = c then
    ⟨(b.bounds c).lower, cut.value, cut.interior.1.le⟩ else b.bounds d⟩

def CountBox.right {n : ℕ} (b : CountBox n) (c : CountCoordinate) (cut : StrictBoxCut b c) : CountBox n :=
  ⟨b.root, fun d => if d = c then
    ⟨cut.value, (b.bounds c).upper, cut.interior.2.le⟩ else b.bounds d⟩

theorem CountBox.split_cover {n : ℕ} (b : CountBox n) (c : CountCoordinate)
    (cut : StrictBoxCut b c) {x : CountPoint n} (hx : b.Contains x) :
    (b.left c cut).Contains x ∨ (b.right c cut).Contains x := by
  rcases hx with ⟨hroot, hcoords⟩
  by_cases hcut : x.coordinate c ≤ (cut.value : ℝ)
  · left
    refine ⟨hroot, ?_⟩
    intro d
    by_cases hd : d = c
    · subst d
      simpa [left, ClosedInterval.Contains] using
        (show ((b.bounds c).lower : ℝ) ≤ x.coordinate c ∧ x.coordinate c ≤ (cut.value : ℝ)
          from ⟨(hcoords c).1, hcut⟩)
    · simpa only [left, if_neg hd] using hcoords d
  · right
    refine ⟨hroot, ?_⟩
    intro d
    by_cases hd : d = c
    · subst d
      simpa [right, ClosedInterval.Contains] using
        (show (cut.value : ℝ) ≤ x.coordinate c ∧ x.coordinate c ≤ ((b.bounds c).upper : ℝ)
          from ⟨by linarith, (hcoords c).2⟩)
    · simpa only [right, if_neg hd] using hcoords d

/-- A complete finite binary tree. Both closed children and a strict interior
cut are mandatory constructor arguments; there is no one-child/pruned node. -/
inductive CountTree {n : ℕ} : CountBox n → Type
  | leaf (b : CountBox n) : CountTree b
  | split {b : CountBox n} (c : CountCoordinate) (cut : StrictBoxCut b c)
      (left : CountTree (b.left c cut)) (right : CountTree (b.right c cut)) : CountTree b

def CountTree.leaves {n : ℕ} {b : CountBox n} : CountTree b → List (CountBox n)
  | .leaf b => [b]
  | .split _ _ left right => left.leaves ++ right.leaves

theorem CountTree.cover {n : ℕ} {b : CountBox n} (tree : CountTree b)
    {x : CountPoint n} (hx : b.Contains x) : ∃ leaf ∈ tree.leaves, leaf.Contains x := by
  induction tree with
  | leaf b => exact ⟨b, by simp [leaves], hx⟩
  | @split b c cut left right ihl ihr =>
    rcases b.split_cover c cut hx with hl | hr
    · obtain ⟨leaf, hleaf, hpoint⟩ := ihl hl
      exact ⟨leaf, List.mem_append_left _ hleaf, hpoint⟩
    · obtain ⟨leaf, hleaf, hpoint⟩ := ihr hr
      exact ⟨leaf, List.mem_append_right _ hleaf, hpoint⟩

structure OriginalCountDomain (n : ℕ) where
  probability : ClosedInterval
  probability_unit : 0 ≤ probability.lower ∧ probability.upper ≤ 1
  lambdaCap : ℚ
  lambda_nonneg : 0 ≤ lambdaCap
  totalInwardCap : ℚ
  totalInward_nonneg : 0 ≤ totalInwardCap

def OriginalCountDomain.rootBox {n : ℕ} (domain : OriginalCountDomain n)
    (k : Fin (n + 1)) : CountBox n :=
  ⟨k, fun c => match c with
    | .probability => domain.probability
    | .weightedNoise => ⟨0, domain.lambdaCap, domain.lambda_nonneg⟩
    | .alpha => ⟨0, 1, by norm_num⟩
    | .phase => ⟨-1 / 2, 1 / 2, by norm_num⟩
    | .rawInward0 => ⟨0, domain.totalInwardCap, domain.totalInward_nonneg⟩⟩

def OriginalCountDomain.Contains {n : ℕ} (domain : OriginalCountDomain n)
    (x : CountPoint n) : Prop := (domain.rootBox x.root).Contains x

/-- An extensional coverage interface for any future decoded representation.
Its proof covers the ORIGINAL products, before necessary-condition contraction. -/
structure CountLeafCover {n : ℕ} (domain : OriginalCountDomain n) where
  leaves : List (CountBox n)
  cover : ∀ x : CountPoint n, domain.Contains x → ∃ leaf ∈ leaves, leaf.Contains x

structure CompleteCountForest {n : ℕ} (domain : OriginalCountDomain n) where
  roots : ∀ k : Fin (n + 1), CountTree (domain.rootBox k)

def CompleteCountForest.leaves {n : ℕ} {domain : OriginalCountDomain n}
    (forest : CompleteCountForest domain) : List (CountBox n) :=
  (List.ofFn fun k : Fin (n + 1) => (forest.roots k).leaves).flatten

def CompleteCountForest.toLeafCover {n : ℕ} {domain : OriginalCountDomain n}
    (forest : CompleteCountForest domain) : CountLeafCover domain where
  leaves := forest.leaves
  cover := by
    intro x hx
    obtain ⟨leaf, hleaf, hpoint⟩ := (forest.roots x.root).cover hx
    refine ⟨leaf, ?_, hpoint⟩
    apply List.mem_flatten.mpr
    refine ⟨(forest.roots x.root).leaves, ?_, hleaf⟩
    exact List.mem_ofFn.mpr ⟨x.root, rfl⟩

/-- Structural composition is independent of the leaf method. `P` is the
mathematical statement interpreted for this SAME point, not a search flag. -/
theorem CountLeafCover.conclude {n : ℕ} {domain : OriginalCountDomain n}
    (cover : CountLeafCover domain) (P : CountPoint n → Prop)
    (leafSound : ∀ leaf ∈ cover.leaves, ∀ x, leaf.Contains x → P x)
    {x : CountPoint n} (hx : domain.Contains x) : P x := by
  obtain ⟨leaf, hleaf, hpoint⟩ := cover.cover x hx
  exact leafSound leaf hleaf x hpoint

inductive BoundRelation where | closed | strict
deriving DecidableEq

def BoundRelation.Holds (relation : BoundRelation) (value cap : ℝ) : Prop :=
  match relation with | .closed => value ≤ cap | .strict => value < cap

/-- A strict global conclusion may come either from a strict numerical gap
between caps, or from a separately proved strict source bound at an equal cap. -/
def BoundRelation.Transfers (source target : BoundRelation) (cap targetCap : ℝ) : Prop :=
  match target with
  | .closed => cap ≤ targetCap
  | .strict => cap < targetCap ∨ (cap ≤ targetCap ∧ source = .strict)

theorem BoundRelation.transfer {source target : BoundRelation} {value cap targetCap : ℝ}
    (hvalue : source.Holds value cap) (hcap : source.Transfers target cap targetCap) :
    target.Holds value targetCap := by
  cases source with
  | closed =>
    cases target with
    | closed => exact hvalue.trans hcap
    | strict =>
      have hlt : cap < targetCap := by simpa [Transfers] using hcap
      exact lt_of_le_of_lt hvalue hlt
  | strict =>
    cases target with
    | closed => exact hvalue.le.trans hcap
    | strict =>
      rcases hcap with hlt | ⟨hle, _⟩
      · exact hvalue.trans hlt
      · exact hvalue.trans_le hle

/-- Provenance labels select the intended statement and source epoch. A hash
string is metadata, not a proof of an analytic or arithmetic conclusion. -/
structure MathematicalSourcePin where
  manuscriptDigest : String
  analyticInterfaceRevision : String
  numericalKernelRevision : String
  sourceEpoch : String

/-- The joint intercept is not a marginal lambda upper bound. At zero
residual resource both dY and lambda vanish; the positive branch licenses
the coupled budget dY/dIntercept + lambda/Lambda <= 1. -/
inductive FrozenJointBudgetData where
  | zero
  | positive (totalInwardIntercept noiseIntercept : ℚ)
      (total_positive : 0 < totalInwardIntercept) (noise_positive : 0 < noiseIntercept)

structure AffineDefectBudgetData where
  binaryCharge : ℚ
  gapCharge : ℚ
  noiseCharge : ℚ
  binary_nonneg : 0 ≤ binaryCharge
  gap_positive : 0 < gapCharge
  noise_positive : 0 < noiseCharge

structure SignedDefectQuadraticData where
  constant : ℚ
  positiveLinear : ℚ
  negativeLinear : ℚ
  curvature : ℚ
  curvature_positive : 0 < curvature

/-- One complete coherent corner family. Its semantics uses MAX over all
quadratics; independent complete families may subsequently be intersected. -/
structure SignedDefectEnvelopeData where
  quadratics : List SignedDefectQuadraticData
  nonempty : quadratics ≠ []

/-- Frozen runtime mathematical input. All numerical fields are rational or
natural; no unknown extremizing law, contact, measure or real parameter value
is an input to the future numerical checker. Proof fields validate only
decidable index/rational side conditions. `target` is a numerical OUTPUT cap,
not the extraction floor stored in ContactAt. -/
structure CountTaskContext (n : ℕ) where
  at_least_two : 2 ≤ n
  target : ℚ
  target_pos : 0 < target
  targetRelation : BoundRelation
  sourcePin : MathematicalSourcePin
  domain : OriginalCountDomain n
  rho : ClosedInterval
  rho_positive : 0 < rho.lower
  beta : ClosedInterval
  gamma : ClosedInterval
  fourth : ClosedInterval
  fifth : ClosedInterval
  mean : ClosedInterval
  mean_positive : 0 < mean.lower
  rawThreshold : ClosedInterval
  supportRadius : ℚ
  support_positive : 0 < supportRadius
  negativeRadius : ℚ
  positiveRadius : ℚ
  negativeRadius_pos : 0 < negativeRadius
  positiveRadius_pos : 0 < positiveRadius
  radii_enclosed : negativeRadius ≤ supportRadius ∧ positiveRadius ≤ supportRadius
  conditionalOuter0 : ℚ
  conditionalOuter1 : ℚ
  outer0_nonneg : 0 ≤ conditionalOuter0
  outer1_nonneg : 0 ≤ conditionalOuter1
  jointBudget : FrozenJointBudgetData
  affineBudget : AffineDefectBudgetData
  signedEnvelope : SignedDefectEnvelopeData
  ownCap : ℚ
  predecessorCap : ℚ
  predecessor_nonneg : 0 ≤ predecessorCap
  floorIndex : ℕ
  floor_positive : 0 < floorIndex
  floor_le_actual : floorIndex ≤ n
  defectCap : ℚ
  defect_nonneg : 0 ≤ defectCap
  nativeDefectCap : ℚ
  nativeDefectCap_nonneg : 0 ≤ nativeDefectCap
  nativeDefectCap_weakens : (floorIndex : ℚ) * defectCap / (n : ℚ) ≤ nativeDefectCap
  rawRCap : ℚ
  thetaCap : ℚ
  theta_nonneg : 0 ≤ thetaCap
  theta_lt_one : thetaCap < 1
  negativeGapFloor : ℚ
  negativeGap_positive : 0 < negativeGapFloor
  positiveGapFloor : ℚ
  positiveGap_positive : 0 < positiveGapFloor

inductive CountLeafConclusion where
  | scoreUpper (cap : ℚ) (relation : BoundRelation)
  | infeasible
deriving DecidableEq

/-- Candidate data plus its checked geometric interpretation. Entries are
aligned EXACTLY with increasing-root, left-first depth-first forest leaves.
They carry no proof of the numerical/analytic leaf conclusions. That is the
separate concrete CountCertificateMeaning defined with the physical-state API. -/
structure CountCertificatePayload {n : ℕ} (ctx : CountTaskContext n) where
  forest : CompleteCountForest ctx.domain
  entries : List (CountBox n × CountLeafConclusion)
  boxes_match : entries.map Prod.fst = forest.leaves

theorem CountCertificatePayload.entry_cover {n : ℕ} {ctx : CountTaskContext n}
    (payload : CountCertificatePayload ctx) {x : CountPoint n} (hx : ctx.domain.Contains x) :
    ∃ entry ∈ payload.entries, entry.1.Contains x := by
  obtain ⟨leaf, hleaf, hpoint⟩ := payload.forest.toLeafCover.cover x hx
  change leaf ∈ payload.forest.leaves at hleaf
  rw [← payload.boxes_match] at hleaf
  obtain ⟨entry, hentry, heq⟩ := List.mem_map.mp hleaf
  refine ⟨entry, hentry, ?_⟩
  simpa only [heq] using hpoint

structure PhaseConfinement (n : ℕ) (z : ℝ) : Prop where
  lower : -1 / 2 ≤ z
  upper : z ≤ (n : ℝ) + 1 / 2

/-- Closed nearest-root coverage, including ties. This theorem has a
confinement hypothesis; it cannot silently drop the two exterior rays. -/
theorem nearest_root_exists (n : ℕ) : ∀ z : ℝ, PhaseConfinement n z →
    ∃ k : Fin (n + 1), -1 / 2 ≤ z - (k.val : ℝ) ∧ z - (k.val : ℝ) ≤ 1 / 2 := by
  induction n with
  | zero =>
    intro z hz
    exact ⟨⟨0, by omega⟩, by simpa using hz.lower, by simpa using hz.upper⟩
  | succ n ih =>
    intro z hz
    by_cases hsmall : z ≤ (n : ℝ) + 1 / 2
    · obtain ⟨k, hk⟩ := ih z ⟨hz.lower, hsmall⟩
      exact ⟨k.castSucc, hk⟩
    · refine ⟨⟨n + 1, by omega⟩, ?_, ?_⟩
      · norm_num only [Nat.cast_add, Nat.cast_one]
        linarith
      · have hu := hz.upper
        norm_num only [Nat.cast_add, Nat.cast_one] at hu ⊢
        linarith

inductive ThresholdLocation (n : ℕ) (z : ℝ) : Prop
  | central : PhaseConfinement n z → ThresholdLocation n z
  | leftTail : z < -1 / 2 → ThresholdLocation n z
  | rightTail : (n : ℝ) + 1 / 2 < z → ThresholdLocation n z

theorem threshold_locations_complete (n : ℕ) (z : ℝ) : ThresholdLocation n z := by
  by_cases hl : -1 / 2 ≤ z
  · by_cases hu : z ≤ (n : ℝ) + 1 / 2
    · exact .central ⟨hl, hu⟩
    · exact .rightTail (lt_of_not_ge hu)
  · exact .leftTail (lt_of_not_ge hl)

inductive CheckFailure where
  | malformed | unsupported | guardFailed | incomplete | rejected
deriving DecidableEq

inductive CheckResult where
  | accepted
  | failure (reason : CheckFailure)
deriving DecidableEq

/-- `Meaning` is the full mathematical proposition for a payload under its
fixed analytic interface. Executing check is untrusted without `sound`.
Parsing, source-binding, completeness and rounding obligations belong in
that theorem; they cannot be inferred from an opaque accepted Boolean. -/
structure CertificateChecker (Payload : Type) (Meaning : Payload → Prop) where
  check : Payload → CheckResult
  sound : ∀ payload, check payload = .accepted → Meaning payload

structure CheckedCertificate {Payload : Type} {Meaning : Payload → Prop}
    (checker : CertificateChecker Payload Meaning) where
  payload : Payload
  accepted : checker.check payload = .accepted

theorem CheckedCertificate.meaning {Payload : Type} {Meaning : Payload → Prop}
    {checker : CertificateChecker Payload Meaning} (cert : CheckedCertificate checker) :
    Meaning cert.payload := checker.sound cert.payload cert.accepted

theorem failure_is_not_acceptance (reason : CheckFailure) :
    CheckResult.failure reason ≠ CheckResult.accepted := by simp

end BEMap
