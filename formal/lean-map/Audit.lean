import BEMap

/-! The printed lists expose logical axioms, not hypotheses supplied as theorem
arguments. Inspect theorem signatures AND these lists. A conditional theorem
may use only standard logical axioms while its analytic inputs remain open. -/
#check BEMap.all_indices_upper
#check BEMap.sharp_global_constant
#check BEMap.ContactPipeline.reject
#check BEMap.n25_upper_of_regions
#check BEMap.TailContracts
#print axioms BEMap.all_indices_upper
#print axioms BEMap.sharp_global_constant
#print axioms BEMap.n25_cover
#print axioms BEMap.tail_base49
#print axioms BEMap.tail_composition
#print axioms BEMap.same_law_n25_allowance
