# Checkpoint 23 — Width-three two-sweep SAT hardness, a single prime-node obstruction, and separable-deletion FPT

Date: 2026-10-29. This note develops elementary reductions and exact algorithms; it is NOT an announcement of new published complexity classifications. Priority relative to prior work on two-order OBDDs/read-twice BPs needs an independent audit. References at end.

## Definitions

A two-sweep oblivious deterministic branching program with p primary Boolean inputs has two passes. The first reads each input once in order 1,...,p, the second reads each input once in some permutation sigma. Each test applies one of two maps [w]->[w]. Unless explicitly stated, maps need not be bijections. We study exact #accepted inputs and SAT for arbitrary initial state and accepting set. 'Simple' permutation means its substitution-decomposition tree is a single prime root, equivalently it has no nontrivial common intervals; for length >=4 this is the usual simple-permutation notion.

## Theorem A — NP/#P completeness at width three

Any CNF F with clauses of size <=3 can be encoded as a width-three, two-sweep oblivious deterministic BP P with one primary input y_o for each literal *occurrence* o, and two passes of length L each (L = #literal occurrences). The first pass groups occurrences by their original variable; the second groups occurrences by their clause. The construction is PARSIMONIOUS, provided that all declared original variables occur (unused variables can be accounted for separately by a known factor 2^u). Hence
   #accept(P) = #SAT(F).

The width-three states are {0,1,⊥}. ⊥ is absorbing.

First (variable-group) pass:
- At the first input of any variable group, replace a non-⊥ state by the read bit b (⊥ stays ⊥).
- At a subsequent input in the same group, retain current 0 or 1 if equal to b, else go to ⊥.
Thus the first pass survives exactly when all occurrence copies of each original variable agree.

Second (clause-group) pass:
- At the first input of the first clause, replace any non-⊥ state with t = truth value of the corresponding signed literal.
- At the first input of each later clause, if the previous clause state is 1 reset to t, else go to ⊥.
- At subsequent inputs in the clause, replace current state a∈{0,1} by a OR t (⊥ remains ⊥).
Final acceptance is state 1. Thus all clauses must be satisfied, and every satisfying original assignment has exactly one accepting copy assignment.

This width-three result remains valid with BOTH groups of length <=3: given arbitrary 3-CNF F0 with L0 occurrences, replace each original variable with k copies, one per occurrence, and enforce equality by the directed cycle of k implications (¬z_j OR z_{j+1}) for k>=2 (indices cyclic). Each copy occurs at most 3 times total: once in a source clause, once as antecedent, once as consequent. All clauses have length 2 or 3, total new occurrence count <=3L0, and each satisfying assignment of F0 extends uniquely. The two-sweep BP from this bounded-occurrence formula has p<=3L0 input bits and group lengths <=3. This is a self-contained parsimonious size-linear reduction from #3SAT measured by formula length.

Decision two-sweep width-3 SAT is NP-complete, and exact counting is #P-complete. We make NO ETH or #ETH claim. A general polynomial-time exact contraction for arbitrary second-sweep permutations would imply FP=#P, and polynomial-time SAT would imply P=NP.

Computational check: independently enumerated all 2^p occurrence assignments of 622 random small CNFs with 1..5 variables, 1..6 clauses of length 1..3 (p<=13) and compared #BP with #CNF after accounting for unused original variables; all counts matched.

## Theorem B — hardness persists in a SINGLE prime substitution node

Brignall, Ruškuc, Vatter, *Simple extensions of combinatorial structures*, Mathematika 57 (2011), prove constructively: every permutation sigma of length p embeds as a pattern in some simple permutation sigma' of length at most p+ceil((p+1)/2).

Use this theorem to embed the second-pass order sigma of any width-three two-sweep instance into a simple sigma'. Add d<=ceil((p+1)/2) new dummy input bits, read once per sweep at the extra positions, with identity transition in BOTH passes. The original relative orders are preserved in each sweep. Hence the new BP computes exactly the original predicate ignoring d dummy bits:
    #acc(P') = 2^d #acc(P).
Decision is unchanged, and counting reduces by division by the known 2^d.

For sigma' simple of length >=4, the substitution decomposition has a single prime root with p+d leaves, of size Θ(p). Therefore SAT remains NP-complete and exact counting #P-hard for width-three two-sweep programs with ONE prime root. This blocks any universal polynomial-time prime tensor contraction, even at w=3, unless the corresponding classical complexity collapses occur.

IMPORTANT RESTRICTION: These gadgets use irreversible transitions, and do NOT establish analogous hardness for width-three permutation branching programs or group equations over S3. Neither do they rule out 2^{o(p)} algorithms (the October 2026 #3SAT manuscript itself claims subexponential exact counting for sparse CNF).

## Theorem C — exact FPT for deletion distance to separable

Let r be the minimum number of input positions to delete from sigma to make its induced permutation separable, equivalently free of the 4-patterns 2413 and 3142. Then #two-sweep-BP-SAT is solvable in 2^{O(r)}poly(p,w) time, even for polynomially growing w and non-injective transitions.

Find a deletion set D of size <=r by branching on a forbidden occurrence of 2413 or 3142: every feasible deletion set must hit it, giving four branches and depth r. Checking for forbidden quadruples naively takes O(p^4), so time 4^r poly(p). No precomputed decomposition is required.

For each assignment to the d=|D| deleted input bits, transitions at their occurrences become constant maps. The fixed maps in each sweep can be composed into the nearest remaining variable-dependent transitions (with constant prefix/suffix treated directly). This preserves all outputs pointwise. The induced order on remaining input labels is separable by the choice of D. Apply the exact four-boundary-state recurrence of checkpoint 21:
    R_I(s,t;u,v) = #{assignments to I: U_I(s)=t and V_I(u)=v}.
For direct and reverse interval splits, contract two w^4 tensors over two shared internal state indices in O(w^6) arithmetic operations. Root readout is sum_t sum_{a∈Accept} R_all(s0,t;t,a). If no live variables remain, evaluate the fixed word directly.

Total bit-operation time is
    O(4^r poly(p) + 2^r p w^6 poly(p)),
with counts of <=2^p requiring O(p)-bit arithmetic. Thus if r=o(p) and w=poly(p), this is 2^{o(p)}poly(p). This is a complementary parameter to prime arity kappa: checkpoint 21 gives w^{O(kappa)}poly(p,w), whereas here the exponential dependence is ONLY on r and does not include log w.

Computational validation: 180 random programs with p<=7, w in {2,3}, arbitrary deterministic (possibly many-to-one) transition tables and random second-sweep orders were checked against exhaustive 2^p assignments. Branching on forbidden patterns, transition absorption, recursive separable tensor contraction, and exact #acc agreed in all cases.

## Interpretation as vertex/hyperedge inversion

For the width-three SAT reduction, each input bit is an incidence linking exactly ONE original-variable constraint and ONE clause constraint. Two sweeps check the two sides of the resulting bipartite incidence graph. This is precisely a factor-graph/hypergraph dual view: every bit is read once in each partition, yet the crossing order of the two partitions can encode all bounded-occurrence 3CNF dependencies.

Arbitrary sparse factor incidence graphs, including highly intertwined ones, therefore arise inside width-three two-sweep BP-SAT. Ordinary spatial separator or constant-boundary tensor contraction does not eliminate the global consistency cost on such inputs. The #3SAT theorem may handle the syntactically recognizable CNF subclass; its techniques do not automatically solve arbitrary non-CNF width-three BPs.

## Research consequence

The previous central open algorithmic challenge, 2^{o(k)}poly(w) contraction of an arbitrary prime node, is meaningful but complete for sparse #3SAT under linear reductions, even for width 3 and a single prime root. Theorem C gives a genuine new tractable regime measured by separable-deletion distance; it does NOT cover the fully intertwined prime nodes generated by arbitrary CNF reductions.

For the NEXP notsubseteq L/poly ambition, note two unresolved gaps:
(1) A width-3 TWO-SWEEP NONPERMUTATION reduction from CNF occurrence bits is not an input-efficient reduction from arbitrary polynomial-size Circuit-SAT on its ORIGINAL n input bits.
(2) An algorithm for constant-width two-sweep programs, even universally subexponential in p, does not immediately yield the required algorithm for arbitrary polynomial-width, read-many BPs.
No circuit lower bound follows yet.

## Sources / novelty cautions
- Brignall, Ruškuc, Vatter, Simple extensions of combinatorial structures (Mathematika 2011): https://doi.org/10.1112/S0025579310001518
- Tovey 1984 bounded-occurrence 3SAT; see Berman, Karpinski, Scott, Computational complexity of some restricted instances of 3-SAT (2007): https://doi.org/10.1016/j.dam.2006.07.009
- Seto, Teruyama, An Exact Algorithm for Oblivious Read-Twice Branching Program Satisfiability (IEICE 2016): https://doi.org/10.1587/TRANSFUN.E99.A.1019
- Nagao, Seto, Teruyama, Syntactic Read-k-times BP-SAT (ISAAC 2017): https://doi.org/10.4230/LIPIcs.ISAAC.2017.58
- Lee, Pyne, Vadhan, On the Power of Regular and Permutation Branching Programs (RANDOM 2023): https://doi.org/10.4230/LIPIcs.APPROX/RANDOM.2023.44
- Prior exact four-boundary tensor DP: docs/21_two_sweep_substitution_decomposition.md

Status: proof sketches and tests verified internally, but novelty/prior-art search for the exact width-three two-sweep formulation and separable-deletion FPT is incomplete. Do not advertise as new theorems before priority audit.
