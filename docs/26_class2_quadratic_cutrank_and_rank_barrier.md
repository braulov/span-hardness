# Checkpoint 26 — Constant commutator-dimension barrier and exact quadratic-cutrank contraction

Research date: 2026-10-29. Independently derived deductions in the project's two-sweep BP-SAT investigation; novelty and prior literature status NOT established. All parameters count PRIMARY Boolean bits p, program width w, and actual second-sweep order σ. This checkpoint builds on docs/23_two_sweep_width3_prime_hardness_and_separable_distance.md and docs/25_observable_quotient_commutation.md.

## Theorem A — Dimension two of ALL commutator errors is not enough for tractability

Let A_i^b be the w×w deterministic transition matrix over F2, with column e_s sent to e_{A_i^b(s)}. For w=3, every such matrix satisfies 1^T A_i^b=1^T, hence 1^T[A_i^b,A_j^c]=0. Each image of an additive matrix commutator therefore lies in the fixed two-dimensional augmentation space

    K={v∈F2^3: 1^T v=0},

which is invariant under every deterministic transition.

Thus the smallest common invariant subspace D containing the images of ALL first-sweep commutators has dim D≤2; the same holds after projection to the observable quotient F2^w/N_* constructed in checkpoint 25. This is true for EVERY width-three deterministic two-sweep BP, including the parsimonious NP-hard family built from 3-CNF in checkpoint 23.

In the explicit first-sweep consistency-checker gadget, let states 0,1,dead and maps

    S0:(0,1,dead)↦(0,0,dead),
    S1:(0,1,dead)↦(1,1,dead),
    C0:(0,1,dead)↦(0,dead,dead),
    C1:(0,1,dead)↦(dead,1,dead).

Each individual nonzero commutator among these four matrices has rank exactly one; the union of their images spans K of dimension two. This was verified directly by F2 matrix calculation.

Consequently any universal exact BP-SAT algorithm with time 2^{f(r)}poly(p,w), with r ONLY the invariant observable commutator-image dimension and f a fixed computable function independent of p, would imply P=NP: all hard width-3 instances have r≤2. No lower bound against 2^{o(p)} is claimed; NP-hardness alone cannot supply one.

This is a concrete negative result for the initial proposal of checkpoint 25. One must additionally control HOW the errors depend on primary variables and on the read-order permutation.

## Theorem B — Central class-two permutation first sweep yields an exact quadratic discrepancy

Consider a two-sweep BP of width w on p primary bits, with arbitrary deterministic second-sweep transitions B_i^0,B_i^1, reading variables in σ-order. The first sweep reads variables in order 1,...,p, and every transition A_i^b is a PERMUTATION of [w].

Assume there is an explicitly given involutive permutation z (z²=1) which commutes with all 2p generators, and for all i,j,b,c,

    A_i^b A_j^c (A_i^b)^-1 (A_j^c)^-1 ∈ {1,z}.

The generated group is nilpotent of class at most two with commutator subgroup contained in {1,z}. This condition is polynomial-time checkable using permutation tables; if there is a nontrivial commutator, choose it as z and verify the rest. If all commute use z=1.

For each fixed Boolean assignment x, let U(x) be the first-sweep product in the ORIGINAL order, and ~U(x) be the same transition maps multiplied in σ-order. Adjacent exchanges of factors multiply the product by the central involution z if their commutator equals z. Since each inverted pair is exchanged exactly once, there is a quadratic polynomial Q(x) over F2 such that

    U(x)= z^{Q(x)} ~U(x).

More precisely, for every inversion (s,t), s<t and σ(s)>σ(t), define κ_{st}(a,b)∈F2 by the central commutator of A_{σ(s)}^a and A_{σ(t)}^b being z^{κ_{st}(a,b)}. Write the unique algebraic normal form

    κ_{st}(a,b)=α_{st}+β_{st}a+γ_{st}b+δ_{st}ab.

Then

    Q(x)=q0 + Σ_s ℓ_s x_{σ(s)} + Σ_{s<t} M_{st} x_{σ(s)}x_{σ(t)} (mod 2),

where q0,ℓ,M are obtained by summing α,β,γ,δ over inversions. Computing Q requires O(p²w) time using explicit permutation tables.

This does NOT require A_i^0=identity. A special case is A_i^0=1, A_i^1=g_i, where Q is purely quadratic with coefficient M_{st}=[σ(s)>σ(t)]ω(g_{σ(s)},g_{σ(t)}), and ω is the central commutator exponent.

## Theorem C — Exact SAT/counting in 2^r poly(p,w) using quadratic cutrank

In σ-read order, let

    r=max_{0≤t≤p} rank_F2 M[{1,...,t},{t+1,...,p}].

Then exact #accepted primary assignments and SAT can be computed in 2^{O(r)}poly(p,w) time, even if w=poly(p), the second sweep is irreversible, and σ is an arbitrary permutation. A concrete state-count bound is O(w³·2^{r+1}) per step.

Algorithm: Guess the genuine state z0∈[w] between the two sweeps. Read primary bits once in σ-order, simultaneously simulating:
  u = state of the REORDERED first sweep starting from original start s0;
  v = state of the second sweep starting at the guessed z0;
  q = the already evaluated constant/linear/internal quadratic terms of Q;
  Λ_t[j]=Σ_{s≤t} M_{s,j} x_{σ(s)} for future j>t (future linear form).

At step t+1 (bit b=x_{σ(t+1)}), update
  q ← q + b(ℓ_{t+1}+Λ_t[t+1]),
  Λ_{t+1}[j] ← Λ_t[j]+b M_{t+1,j} for j>t+1,
and update u,v with corresponding transition maps. Initialize q=q0, Λ_0=0.

The set of possible Λ_t lies in the F2 row span of the t×(p−t) cross-cut matrix, so has size at most 2^r. At the end require

    z0 = z^q(u) and v∈Accept.

For every primary assignment, exactly one guessed z0 satisfies the equality, and it is the genuine first-sweep middle state. Therefore the algorithm is parsimonious and counts accepted inputs exactly. The DP stores nonnegative integers ≤2^p, so bit complexity is polynomial times the state bound. All ranks are polynomial-time computable.

The parameter is the CUTRANK of the quadratic interaction matrix along the second sweep order, not the dimension of the matrix commutator image. Note the conceptual link to linear rank-width and quadratic-phase tensor networks.

## Strict separation: one huge prime node, Ω(p) conflicts, but r=2

Let p=2k≥6, and work in the nonabelian order-eight group UT_3(F2) of triples (a,b,c) with multiplication

    (a,b,c)(a',b',c')=(a+a',b+b',c+c'+a b') mod 2.

Let generators g=(1,0,0), h=(0,1,0). Their commutator is central z=(0,0,1). Act by left multiplication on the eight group elements, so the first sweep has width w=8. Set A_i^0=identity, and A_i^1=g for odd i (1-based), h for even i. The first-sweep variable noncommutation graph is complete bipartite K_{k,k}; its minimum vertex cover is k=p/2.

Take the SECOND-sweep order (1-based)

    σ_k=(2,4,1,6,3,8,5,...,2k,2k−3,2k−1).

Equivalently (zero-based values and positions):
    σ[0]=1;
    σ[2j−1]=2j+1, σ[2j]=2j−2 for j=1,...,k−1;
    σ[2k−1]=2k−2.

This is an 'increasing oscillation', with inversion graph a path on p vertices. The path in terms of σ-POSITIONS is

    0—2—1—4—3—6—5—...—(2k−2)—(2k−3)—(2k−1).

All inverted pairs have opposite parity ORIGINAL variable indices, hence commutator exponent one and the quadratic interaction graph M coincides with the inversion graph. Across a chronological prefix cut of σ, at most TWO left endpoints have inversion edges crossing to the future. Thus r≤2; explicit calculations give r=2 for all k≥3. Theorem C is therefore POLYNOMIAL despite dense noncommutation.

The inversion graph being a path P_p (p≥4) makes σ a SIMPLE permutation: a proper common interval would induce a nontrivial graph module, but P_p has no nontrivial modules. Its substitution decomposition has one prime root of arity p. Additionally, separable permutations have P4-free inversion graphs. Partition the path vertices into floor(p/4) disjoint consecutive 4-vertex subpaths; each induced P4 forces at least one deleted position. Hence deletion-to-separable distance is at least floor(p/4)=Ω(p).

Therefore THREE earlier parameters are all linear:
  prime arity κ=p; noncommutation vertex-cover τ=p/2; separable-deletion r_sep≥floor(p/4).
But quadratic cutrank r=2 and exact #SAT remains polynomial, for arbitrary deterministic second-sweep transitions.

This is a *genuine* strict separation of sufficient algorithmic conditions. It does not imply a universal subexponential algorithm or a circuit lower bound.

## Empirical checks (reproducible independent standard-library verifier available)

- 200 random UT3(F2) first sweeps with A_i^0=identity, arbitrary A_i^1 and random deterministic second sweeps: quadratic-cutrank DP exact #SAT counts matched exhaustive enumeration.
- 200 additional random UT3(F2) first sweeps with independent arbitrary A_i^0,A_i^1 and random deterministic second sweeps: all counts matched exhaustive enumeration.
- Increasing-oscillation family tested for p=6,8,...,24: σ simple and quadratic cutrank exactly two in all tested cases. The proof above extends to all even p≥6.
- The four width-three consistency-checker transition matrices have individual commutators of rank 0 or 1, with total image span dimension 2.

These are validation experiments, not literature novelty proofs.

## Literature checkpoints

- Increasing oscillations as simple permutations with path inversion graphs: permutation-patterns literature, e.g. https://arxiv.org/abs/1306.0807
- Separable permutations correspond to cographs/P4-free inversion graphs: https://www.numdam.org/item/10.5802/cml.92.pdf
- Cutrank and linear rank-width: https://doi.org/10.1016/j.tcs.2015.04.021
- Seto and Teruyama, exact oblivious read-twice BP-SAT: https://doi.org/10.1587/transfun.E99.A.1019
- Lee, Pyne, Vadhan, regular/permutation branching programs: https://doi.org/10.4230/LIPIcs.APPROX/RANDOM.2023.44

## Next research target

Generalize the central C2 discrepancy to first-sweep transition groups with a fixed-rank CENTRAL commutator subgroup (F_2)^c, yielding a vector-valued quadratic Q and a vector cutrank parameter. Explore class-three groups, where reorder discrepancies can depend on cubic monomials. IMPORTANT: neither bounded commutator-image dimension nor bounded nilpotency class by itself guarantees efficient #SAT; the relevant complexity measure is the online dimension of the input-dependent correction across read-order cuts. Check novelty before representing any statement here as a publishable new algorithm.
