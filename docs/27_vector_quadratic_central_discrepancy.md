# Checkpoint 27 — Vector-valued quadratic discrepancy for central elementary-abelian commutators

2026-10-29. Generalization of checkpoint 26 (docs/26_class2_quadratic_cutrank_and_rank_barrier.md). Elementary exact algebra; independent novelty/prior-art verification NOT completed.

## Setting

Consider a deterministic two-sweep BP of width w on p primary bits. First pass reads x_1,...,x_p using permutation maps A_i^0,A_i^1∈S_w. Second pass reads variables in permutation order σ using arbitrary deterministic maps B_i^0,B_i^1. Let C ≤ S_w be an explicitly generated central subgroup isomorphic to F2^c, so each element z(v) for v∈F2^c is a permutation, z(v)z(u)=z(v+u).

Assume every pairwise commutator [A_i^a,A_j^b] lies in C and C commutes with ALL first-pass generators. This gives a class-two first-pass group with central elementary-abelian commutator subgroup (the rest of the group may be large or nonabelian). We assume an explicit F2-basis for C, and that the F2^c coordinates of each commutator can be found in polynomial time. If c is constant this is immediate; if c grows, naive 2^c subgroup enumeration can be used and charged in runtime.

## Vector quadratic correction

As in checkpoint 26, reorder first-sweep factors into σ-order using adjacent exchanges. Because every swapping error lies in central C, the discrepancy is an explicitly computable vector-valued quadratic polynomial

    Q(x)=q0 + Σ_i ℓ_i x_i + Σ_{i<j} D_{ij} x_i x_j ∈ F2^c,

where D_{ij} ∈ F2^c, and indices i,j here refer to positions in σ-order. All coefficients are obtained from the four commutator values of each inverted input pair; O(p²) group commutator computations and F2-coordinate operations.

For every assignment x the ORIGINAL first-sweep transformation and the σ-REORDERED transformation satisfy

    U(x)=z(Q(x)) · ~U(x).

This equality is pointwise (not only distributional).

## Streaming quadratic-correction rank

At a cut t define the matrix

    K_t ∈ F2^{t × (c·(p−t))}

whose row s≤t concatenates the c-bit blocks D_{s,j} over future positions j>t. Define

    r=max_t rank_F2(K_t).

For a fixed prefix assignment, the vector-valued future linear form is

    Λ_t(j)=Σ_{s≤t} D_{s,j} x_s ∈F2^c,    j>t.

Because the mapping from the prefix bits to the concatenated Λ_t vector is K_t, there are at most 2^r possible signatures at any cut.

A weighted read-once DP in σ-order guesses the correct middle state z0∈[w] and tracks:
- u∈[w], state of ~U on the genuine initial state;
- v∈[w], state of the second sweep initialized at z0;
- q∈F2^c, already evaluated contribution of Q;
- Λ_t∈(F2^c)^{p−t}, the future-coefficient signature.

For bit x_{t+1}=b:
    q ← q + b(ℓ_{t+1}+Λ_t(t+1)),
    Λ_{t+1}(j) ← Λ_t(j)+bD_{t+1,j} for j>t+1,
    u,v ← respective maps for that bit.
Initialize q=q0 and Λ=0. At the end require
    z0 = z(q)(u),  v∈Accept.

Every accepting primary assignment has exactly one correct guessed middle state z0. All DP weights are exact nonnegative integer assignment counts. The total number of states is O(w³·2^{c+r}), giving

    #TwoSweepBPSAT ∈ 2^{O(c+r)} poly(p,w).

This bound includes all deterministic second-sweep transitions, arbitrary σ and polynomial width, provided the central group operations and coordinate representations are available within the stated bound.

For c+r=o(p), this is an input-efficient 2^{o(p)}poly(p,w) algorithm. For c=1, it specializes to checkpoint 26's theorem.

## Why this parameter is mathematically distinct from checkpoint 25's dimension

The commutator-image invariant subspace dimension by itself is powerless: all width-three deterministic two-sweep BPs have that dimension ≤2, yet SAT is NP-complete (checkpoint 26). The quantity r here instead measures the dimension of the SPACE OF FUTURE INPUT-DEPENDENT CORRECTIONS. It can be large even with c=1. For example, the same UT3(F2) first-sweep generators with even/odd parity types and the parallel-alternation second order σ=(2,4,...,2k,1,3,...,2k−1) have c=1 but r=k=Θ(p), since the inversion interaction cross-matrix contains a k×k triangular full-rank block. So the algorithm correctly fails to trivialize these hard-looking interleavings.

Conversely, the increasing-oscillation simple-order family in checkpoint 26 has c=1, rank r=2, noncommutation vertex cover Θ(p), prime-arity p and separable deletion Ω(p). There the vector-quadratic algorithm is polynomial and demonstrably stronger than those earlier sufficient criteria.

## Forward research task

The natural extension beyond nilpotency class two asks for online representations of the INPUT-DEPENDENT discrepancy under reorderings. In class three, swapping operations introduces noncentral commutators and their conjugations; resulting corrections may include cubic input interactions. One can attempt a higher-degree tensor analogue using the dimension of the space of residual polynomials on unprocessed inputs at each cut.

A formal generic statement: for ANY explicitly evaluable Boolean polynomial Q in p bits, define for each prefix assignment a the residual function Q(a, y_future) minus its constant term at y=0. If these residuals lie in an r-dimensional F2-linear space, a streaming exact DP can have ≤2^r residual states, provided their coefficient vectors and update maps can be computed in poly(p,2^r) time. This is a representation-size condition, not automatically satisfied for class-three groups; computing Q or its residual spaces may itself be the hard part.

No universal subexponential BP-SAT algorithm or circuit lower bound follows from this checkpoint.
