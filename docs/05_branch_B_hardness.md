# Branch B — Fine-grained completeness and the circuit win-win

## Candidate SGR hypothesis (unproved)
The syntactically restricted SGR-CSP of total structural size n (constant-degree base graph, O(n) Boolean variables/3-CNF clauses, one graphic-rank threshold) cannot be decided in 2^{o(n)}poly(|I|).

Variants restricted to induced acyclicity, induced connectivity or selected 2-factors might not be equivalent.

## The reduction-direction trap
If P <=_lin SGR-CSP, a generic fast algorithm for SGR-CSP accelerates P. It does *not* follow from hardness of SGR-CSP that P is hard. To derive hardness for P, establish SGR-CSP <=_lin P (or for a hard restricted core).

## Program
B1: Build linear-size gadgets that encode rank and O(n) local constraints within bounded-degree FVS or Hamiltonian Cycle.
B2: Search for a canonical natural RANK-CORE complete for many graph problems.
B3: Conjoin rank constraints by direct sums and saturation upper bounds where justified.
B4: Identify the exact step beyond Linear Monadic NP that breaks known linear SAT compilation.
B5: Treat dense source instances and parameter-preserving sparsification as separate central challenges.

## A real ETH replacement needs more
The structural SGR conjecture is not automatically the circuit-lower-bound win-win. A genuine analogue of the Williams implication would require enough expressive/completeness power to accelerate sufficiently general Circuit-SAT on n INPUT bits and arbitrary polynomial-size circuits. Merely retaining O(n) *free* bits while hiding polynomially many local gates is vacuous unless their processing cost is controlled.

Aim for verified reductions from Circuit-SAT(n,n^k) to a structurally restricted Span instance preserving O(n) principal bits, plus a solver whose running time is fast enough, uniformly over each fixed k. Ideally get NEXP not subseteq P/poly through known algorithm-to-lower-bound theorems.

## Status
No two-way reductions between the rank core and all natural graph tasks have been established. No unconditional reduction showing a new Williams-style circuit lower bound from falsity of a proposed Span hypothesis has been established.