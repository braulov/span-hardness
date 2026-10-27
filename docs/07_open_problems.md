# Open problems and research priorities

## Priority: potential algorithmic collapse via characteristic-two weighted counting
Audit whether the actual October 2026 fixed-width counting SAT technique extends to field-valued weighted counts in characteristic two without superlinear auxiliary Boolean-variable overhead. If so, exploit the nullspace parity identity and isolation to obtain randomized subexponential decision algorithms for sparse (co)graphic full-span feasibility. This is NOT yet proved.

## Priority: rank-circuit cost
Seek a uniform bounded-fanin Boolean circuit for selected-edge forestness/connectedness/full-rank on sparse graphs of size o(n sqrt(log n)/(log log n)^2). Distinguish gate cost from word operations and field operations.

## Priority: fine-grained completeness
Identify a canonical restricted rank problem with O(n)-blowup reductions *both directions* against cubic HC, bounded-degree FVS and connectivity/covering variants. Hardness of a generic class does not propagate through reverse-only encodings.

## Priority: genuine ETH replacement
Define the desired computational parameter and quantitative speedup. Prove that fast Span algorithms imply sufficiently fast SAT for arbitrary polynomial-size circuits and *then* apply an appropriate algorithms-to-circuit-lower-bounds theorem. Otherwise the project yields a useful graph source of hardness but not the requested unconditional win-win.

## Additional stress tests
- compressed group activations for general Set Cover with universe-size parameter;
- arbitrary CNF with variable-count parameter;
- preservation under dense-to-sparse transformations;
- special cases planar, bipartite, bounded-degree and bounded treewidth;
- explicit examples where simple encodings have logarithmic/superlinear overhead;
- one-sided randomized decision via isolation and sparse XOR hashing.

## Iteration protocol
For each branch maintain: proved lemma or counterexample, exact parameter audit, conditional consequences, next concrete theorem. Mark all new statements PROVED, CONDITIONAL, CONJECTURED or OPEN.