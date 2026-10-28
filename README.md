# Graphic Rank and Global-Obstruction Complexity

**Research notebook — 2026-10-27.** Preliminary, not a theorem announcement. Independent review of the 2026 OpenAI ETH-refutation manuscript is ongoing.

## Research question

Can a *restricted*, fine-grained-preserving graphic-rank feasibility problem act as a single source of hardness for graph problems involving connectedness, acyclicity, covers, and tours? Can a circuit representation of its rank predicate instead yield genuinely new subexponential algorithms?

We deliberately distinguish **exact encodings** from **parameter-preserving reductions** and **unproved hypotheses**.

### Canonical core: Sparse Graphic Rank-CSP (SGR-CSP)

Input with size parameter `n`:

1. An undirected (multi)graph `G=(V,E)` with `|V|+|E|=O(n)`.
2. `O(n)` Boolean variables `z`, including one activation bit `y_e` per edge; a 3-CNF `phi(z)` with `O(n)` clauses.
3. Affine integer threshold `t(z)=c+sum_i a_i z_i`, with `O(n)` terms and coefficients in `{-1,0,1}`. Optionally a fixed number of linearly computable cardinality constraints is compiled into `phi` using linear-size Boolean circuits.

Question:

```
exists z: phi(z) = 1 and rank_F2(B_G[:, {e: y_e=1}]) >= t(z) ?
```

Here `B_G` is the unsigned `vertex x edge` incidence matrix over `F_2`. For every activated subset `Y`,
`rank(B_Y) = |V| - cc(V,Y)`.

The number `n` counts ALL the core graph objects and variables/clauses up to constant factors, not a chosen one-dimensional parameter after a polynomial blow-up. This prevents vacuous claims of `2^{o(n)}` from being transported across polynomial-size encodings.

### Stronger unifying formulation: one FULL-SPAN matroid constraint

**New central result of the notebook:** after taking the cographic dual and using a root gadget, all the graph families below can use the same **full-spanning** rank predicate rather than different affine thresholds. The underlying binary matroid is graphic, cographic, or a direct sum. The star instance also exactly represents SAT and Set Cover, with important parameter-loss caveats. See [`docs/09_full_span_matroid_conjecture.md`](docs/09_full_span_matroid_conjecture.md).

### Why this core matters

- **FVS** in bounded-degree graphs: retained vertices induce an acyclic graph iff `rank(Y) >= |Y|`.
- **Undirected Hamiltonian Cycle** in bounded-degree graphs: selected degree-two subgraph is Hamiltonian iff `rank(Y) >= |V|-1`.
- **Directed Hamiltonian Cycle** in bounded-(total-)degree digraphs: selected arcs form directed cycle cover; weak connectivity, certified by graphic rank, forces one tour.
- **Connected Dominating Set, Connected Vertex Cover, unweighted node-Steiner connectivity** in bounded-degree graphs: `rank(Y) >= |S|-1` for the subgraph induced by chosen vertices `S`, plus local feasibility.
- **Connected FVS**: two separate rank requirements can be combined into a *single* rank bound on the disjoint union of two graph copies.

Full proofs, special cases and corner conditions are in [`docs/01_core_formalism.md`](docs/01_core_formalism.md) and [`docs/02_encoding_registry.md`](docs/02_encoding_registry.md).

### Important second layer: a rank representation of Set Cover and SAT

Set Cover's union-cardinality function is graphic rank on a **star with repeated/activated parallel edges**. The number of activated distinct star spokes is the coverage size. A CNF can also use a star spoke per clause, activated when that clause is satisfied.

**This is an exact algebraic representation, not a linear-parameter reduction for unrestricted instances.** General Set Cover may have `m >> |U|` sets; arbitrary CNF may have many clauses and incidences. See [`docs/03_rank_coverage_envelope.md`](docs/03_rank_coverage_envelope.md).

### Parity-based route without rank circuits

A second exact identity: the number of nullspace certificates for a fixed assignment is `2^(rank deficit)`; modulo two it is 1 iff full span. Graphic-cut and cographic-cycle certificates have linear-size local Boolean verifiers. **Therefore the parity of the number of solutions** for the bounded-degree graph families reduces to exact #3-SAT on O(n) variables. Whether one can turn this parity algorithm into a decision algorithm is unresolved; a promising conditional route is arbitrary-field **weighted #SAT** plus polynomial identity testing. See [`docs/10_obstruction_parity_and_weighted_counting.md`](docs/10_obstruction_parity_and_weighted_counting.md).

## ETH-replacement / Williams win–win

The present SCGS hypothesis is **not yet** a strong ETH replacement: its failure implies at most the already available linear-circuit lower bound from 3-SAT. A substantially stronger circuit-lower-bound payoff would require **input-efficient compilation of polynomial-size Circuit-SAT** into a syntactically restricted span class, with 2^{o(n)} depending on genuine input bits rather than all auxiliary gates. The resulting conditional program, with correct reduction arrows and no dummy-matroid encodings, is in [`docs/11_eth_replacement_winwin.md`](docs/11_eth_replacement_winwin.md).

## New: edge-bucket projection for counting tensors (2026-10-28)

A proposed exact regrouping of incidence-indexed polynomial-counting tensors replaces per-block selected-incidence sets by their projected variable supports, with internal summation inside test-bucket tensors. On structured grouped-support instances this reduces the wire budget from the generic O(n loglog n) to O(n), *conditional on the October 2026 external tensor-contraction theorem* giving 2^{O(n/sqrt(log n))} counting time. There is **no universal dense-#SAT improvement** and **no NEXP lower bound** yet. Full proof, hybrid encoding, local-entry/precision audit, communication-rank obstruction, and concrete SAT/Circuit-SAT open problems: [`docs/12_projected_support_edge_buckets.md`](docs/12_projected_support_edge_buckets.md).

## Research branches

All branches are also documented on `main`; independent Git topic branches keep experimental approaches apart.

- **A — rank-to-SAT circuit compression**: [`docs/04_branch_A_algorithms.md`](docs/04_branch_A_algorithms.md). Design `o(n sqrt(log n)/(log log n)^2)`-gate circuits (or analogous Tseitin 3-CNF) for graphic-rank predicates.
- **B — hardness and parameter-preserving reductions**: [`docs/05_branch_B_hardness.md`](docs/05_branch_B_hardness.md). Find a restricted canonical problem and nontrivial linear-preserving reductions.
- **C — common rank/coverage envelope**: [`docs/03_rank_coverage_envelope.md`](docs/03_rank_coverage_envelope.md). Capture CNF and Set Cover without hiding the parameter loss.
- **E — parity and weighted #SAT**: [`docs/10_obstruction_parity_and_weighted_counting.md`](docs/10_obstruction_parity_and_weighted_counting.md). A proved cancellation identity and a conditional randomized-decision route.
- **G — ETH-replacement / circuit win–win**: [`docs/11_eth_replacement_winwin.md`](docs/11_eth_replacement_winwin.md). A stronger input-efficient class, not yet established complete for Circuit-SAT.
- **D — structural/logical boundary**: [`docs/06_branch_D_logic.md`](docs/06_branch_D_logic.md). Relate Linear Monadic NP, MSO2, graphic rank and succinct global constraints.

For the distinction between **SCGS as a candidate hardness core** and an **ETH replacement with new circuit-lower-bound win-win**, see [`docs/11_eth_replacement_and_circuit_winwin.md`](docs/11_eth_replacement_and_circuit_winwin.md).

See [`docs/07_open_problems.md`](docs/07_open_problems.md), [`docs/08_status_and_caveats.md`](docs/08_status_and_caveats.md), and [`SUMMARY_RU.md`](SUMMARY_RU.md).

## Validation

Run `python3 scripts/check_small_instances.py`. This enumerates small graphs and checks the elementary rank equivalences via independent GF(2) elimination and brute-force graph checks.

## Status

Verified elementary rank identities and direct encodings **do not** establish a novel complexity conjecture, a fast rank circuit, or equivalence of the natural hard problems. The claim 'one conjecture -> all lower bounds' would additionally require reductions FROM the canonical problem TO every target problem. Conversely, a universal SGR-CSP subexponential algorithm immediately accelerates all the direct special cases.

## Sources

- OpenAI (2026), *The Exponential Time Hypothesis is False* — manuscript: https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
- OpenAI Lean formalization scope: https://github.com/openai/math/blob/main/lean/docs/378.md
- OpenAI release and external review plan: https://openai.com/index/building-scientific-understanding-with-academic-communities/
- Ganian, de Haan, Kanj, Szeider (2016; journal 2020), *On Existential MSO and Its Relation to ETH*: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2016.42 ; https://doi.org/10.1145/3417759