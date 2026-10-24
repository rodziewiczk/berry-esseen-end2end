# Proof graph: statements and dependencies

**This is the intended proof structure, with open premises visible. It is not
a declaration that the proof is complete.** An arrow means that the earlier
statement or same-law implication is needed for the next statement. A successful
computation establishes only its declared conditional numerical scope.

For standardized iid real laws with finite third absolute moment, write
`C_n = sup_P sqrt(n)/E|X|^3 * sup_H |P(S_n <= H)-Phi(H/sqrt(n))|` and
`C_E=(3+sqrt(10))/(6*sqrt(2*pi))`. The target is `sup_n C_n=C_E`.

```mermaid
flowchart TD
  subgraph Shared[Analytic and numerical meaning: required throughout]
    L["Published smoothing, Gaussian, binomial and universal-tail inputs"]
    W["Unrestricted attained contrary witness; same law and threshold; reflection and contact"]
    K["Sound exact/interval kernels and complete closed-domain covers"]
    L --> W
    K --> V["Each numerical exclusion has its stated mathematical meaning"]
    W --> V
  end

  subgraph Small[Small indices]
    G1["All-law one-summand bound: C1 <= 0.3704"]
    G23["All-law n2 and strong n3 bound: C3 <= 59 sqrt(3) / 250"]
    B4["Complete bounded n4 physical root: upper 4097/10000"]
    G23 --> G4["All-law C4 < C_E via unrestricted localization"]
    B4 --> G4
    W --> G4
    V --> G4
    G4 --> G5["All-law C5 <= C_E: support, HIGH, resources, counts, corner and complement"]
    V --> G5
  end

  subgraph Finite[Literal finite-index exclusions]
    A5["Global auxiliary C5 < 429/1000"]
    A5 --> G69["All-law bounds for each actual n6,7,8,9"]
    V --> G69
    A9["Global auxiliary and supported n9 ceilings on their exact domains"]
    A9 --> G1014["All-law bounds for each actual n10 to14"]
    V --> G1014
    G1014 --> G1519["All-law bounds for each actual n15 to19"]
    G1519 --> G2024["All-law bounds for each actual n20 to24"]
    G2024 --> OR24{"At least one acquired predecessor license"}
    A24["Alternative: complete auxiliary24 chain gives C24 < C_E + 1/80"] --> OR24
    OR24 --> Q25["Same contrary n25 witness: q25 <= 5/16"]
    Q25 --> G25["All-law C25 <= C_E: all20 physical regions"]
    U25["All n25 resource/count/mixed exclusions and exact same-law interfaces"] --> G25
    G25 --> G2630["All-law bounds for each actual n26 to30"]
    T25["Full floor25 resource transcripts plus actual26 to30 support and transfers"] --> G2630
    G2630 --> G3139["All-law bounds for each actual n31 to39"]
    T31["Eight floor31 bands; actual transfers; retained35 to39 interfaces"] --> G3139
    V --> T31
  end

  subgraph Later[Independent selected later-index routes]
    I40["Independent early38 / positive39 scalar and retained-resource route"] --> G4042["All-law bounds for each actual n40 to42"]
    I43["Independent barrier41 / actual42 and retained-resource route"] --> G4348["All-law bounds for each actual n43 to48"]
    V --> I40
    V --> I43
  end

  G1 --> BASE["All literal n1 to48 satisfy C_n <= C_E"]
  G4 --> BASE
  G23 --> BASE
  G5 --> BASE
  G69 --> BASE
  G1014 --> BASE
  G1519 --> BASE
  G2024 --> BASE
  G25 --> BASE
  G2630 --> BASE
  G3139 --> BASE
  G4042 --> BASE
  G4348 --> BASE
  R49["Complete selected tail arithmetic and all retained components"] --> IMP["Uniform analytic implication for every integer n >=49; finite-base / least-failure hypotheses explicit"]
  L --> IMP
  W --> IMP
  K --> IMP
  BASE --> TAIL["Every n >=49 satisfies C_n <= C_E"]
  IMP --> TAIL
  BASE --> UPPER["For every integer n >=1: C_n <= C_E"]
  TAIL --> UPPER
  E["External Esseen lower bound: sup_n C_n >= C_E"] --> EQ["Target equality: sup_n C_n = C_E"]
  UPPER --> EQ

  classDef open fill:#fff1d6,stroke:#986000,color:#222;
  classDef premise fill:#fce3e3,stroke:#a22525,color:#222;
  classDef target fill:#edf0ff,stroke:#394a9b,color:#222;
  class G1,G23,B4,G4,G5,A5,G69,A9,G1014,G1519,G2024,A24,OR24,Q25,G25,U25,T25,G2630,T31,G3139,I40,G4042,I43,G4348,R49,IMP,BASE,TAIL open;
  class L,W,K,V,E premise;
  class UPPER,EQ target;
```

Orange nodes are proof steps whose complete acquisition is still to be checked.
Red nodes are substantive analytic, literature or kernel/interface premises;
their placement is not a claim that they are false. Blue nodes are the target
conclusions. The diagram deliberately does not colour an all-law theorem as
proved merely because its numerical component has completed.

## How one finite-index exclusion works

For a fixed literal n, assume a contrary standardized law and threshold with
normalized discrepancy at least the target. Use the **unrestricted**
attainment/localization/contact reduction before subdividing its parameters.
Acquire support before invoking any support-dependent higher-moment or Fourier
bound. The same marginal and threshold must satisfy all facts passed onward.

```mermaid
flowchart LR
  C["Same contrary witness at actual n"] --> S["Acquired support and HIGH / owncap facts"]
  S --> I["Full INITIAL probability dispositions"]
  I --> R["Full signed resource implications"]
  R --> D{"Each closed parameter cell"}
  D --> X["Valid direct or scalar exclusion"]
  D --> F["Full COUNT or mixed-theorem exclusion under its exact contract"]
  D --> P["Applicable Fourier complement / inclusive tail"]
  X --> N["No contrary witness in the complete union"]
  F --> N
  P --> N
```

Every possibility has to be covered, including shared endpoints, both discrepancy
orientations, zero-noise/equality cases and the unbounded tails. A criterion that
fails to exclude a cell does not close that cell. A bound from another marginal,
an unsigned replacement of a signed moment, or a scalar maximum does not provide
the simultaneous resource-to-contract implication. These are the reasons the
interfaces are explicit proof steps.

## Open edges that the diagram does not hide

- The n25 union needs fresh accepted replacements for eleven ordinary cases
  and current parent epochs for two mixed routes. The reconstruction basis is
  now concrete: all eight V12 bases and combined-V14 ingredients are supplied;
  four p33 contracts/checkers match their historical hashes; all93 mixed-parent
  native files and both checkers are recoverable. Current source/registry
  adapters, fresh complete searches/replays and same-law acquisition remain
  necessary. Naming the complete20-piece cover does not close its pieces.
  The [source reconstruction is now implemented](n25_b5_reconstruction_execution.md)
  and its thirteen source capsules were actually assembled and revalidated;
  they remain inputs of the single66 delivery unit.
- Current source/capture epochs and several finite-only semantic joins remain
  to be implemented. Historical global composers sometimes import later tails;
  those full joins belong after their finite components, not as assumptions
  of the earlier components. The graph therefore has no final-theorem arrow
  back into an earlier proof.
- Analytic/literature and code-to-lemma obligations remain real work. Scoped
  successful arithmetic alone does not discharge them. In particular, n4
  consumes the **strong quantitative n3 bound**, not merely C3<=C_E.
- The predecessor input for n25 is an OR: acquired sharp24 or the complete
  weaker auxiliary24 chain. Neither choice removes attainment/contact,
  support/owncap or current resource/count obligations.
- The49+ statement must be uniform in the integer n under its precise
  hypotheses. Checking finitely many n or assuming monotonicity of C_n would
  not suffice.

The mathematical [conditional sufficiency argument](remaining_notebooks_sufficiency.md)
states the hypotheses of this graph. Notebook-to-statement assignments and exact
source inventories are maintained separately in the
[delivery specification](remaining_notebooks_closed_plan.md) and its
[machine-readable companion](remaining_notebooks_closed_plan.json).
The specification checker verifies accounting, exact endpoints and graph
consistency; it does not evaluate the original mathematics or certify this proof.
