# Branch A — Boolean-circuit rank compression

Given a sparse graph with |V|+|E|=O(n), selected-edge bits y, and affine rank threshold t, seek a uniform bounded-fanin Boolean circuit computing rank_F2(B_Y)>=t with

N_gates=o(n sqrt(log n)/(log log n)^2).

Together with O(n) local Boolean gates, Tseitin expansion, and the October 2026 claimed #3-SAT algorithm with certified upper bound 2^{O(N (log log N)^2/sqrt(log N))}, this would imply 2^{o(n)} for the full sparse rank class. The concrete target O(n log^{0.49}n) gates suffices.

## Subprojects
A0: Extreme rank regimes. Forest independence rank(Y)=|Y| versus connectivity full rank(Y)=|V|-1. Either alone could yield new graph algorithms; neither implies the other without a reduction.

A1: Audit low-work algorithms and their *Boolean gate costs*: union-find, pointer jumping, sparse elimination, connectivity. Word-RAM complexity is not gate complexity. O(n log n) Boolean gates are too many for this particular SAT upper bound.

A2: Randomized algebraic sketches, determinants, one-sided rank fingerprints. Count exact Boolean gates for finite-field operations and avoid introducing too many Boolean auxiliary variables.

A3: Explore direct use of the SAT counting engine, matroid rank generating functions, Tutte evaluations, subset convolution and Fourier algebra without literal circuit compilation.

## Milestones
1. Survey currently known uniform bounded-fanin circuit sizes for sparse undirected connectivity and acyclicity.
2. Produce a gate ledger for every scheme (including indexing/memory operations).
3. Specialize to cubic Hamiltonicity and cubic FVS before tackling arbitrary rank.
4. Investigate amortized sublogarithmic gate cost per activated edge.
5. If proving a lower bound, clearly specify a restricted model. No general superlinear circuit lower bound is asserted.

## Caution
Theorem claims about the October 2026 SAT result are conditional on verification and the precise uniform model. A failure to find small rank circuits is *not* evidence of an unrestricted circuit-size lower bound.