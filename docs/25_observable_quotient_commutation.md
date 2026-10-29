# Checkpoint 25 — Observable-quotient commutation for two-sweep BP-SAT

Date 2026-10-29. Exact elementary algorithm and a checkable certificate for polynomial-width deterministic two-sweep branching programs. Independently derived in this project; novelty/priority not established.

## Model

A first sweep reads x_1,...,x_p via deterministic maps A_i^0,A_i^1:[w]->[w], from s_0. A second sweep reads x_{σ(1)},...,x_{σ(p)} via B_i^0,B_i^1 and accepts at states in Acc⊆[w]. The two sweeps SHARE each primary input bit. Width w can be polynomial in p; maps need not be bijections.

The first sweep output is F_x(s_0), and the second sweep from state z is V_x(z).

## 1. Semantic observation partition of second sweep (polynomial-time)

Define s ~_V t iff for every x∈{0,1}^p,
   [V_x(s)∈Acc]=[V_x(t)∈Acc].

Compute this exact equivalence with backward partition refinement through the read-once second sweep:
- At the terminal layer, states are equivalent iff both accept or both reject.
- If the next input is x_i, the before-step signature of state s is the pair of equivalence classes of B_i^0(s),B_i^1(s) at the next layer.
- Give equal signatures the same class. After p steps this is precisely ~_V.

Running time polynomial in p,w. The universal quantifier over 2^p assignments does NOT require enumeration because the second sweep is read-once.

## 2. Coarsest first-sweep congruence refining observation

The partition ~_V may fail to be preserved by first-sweep transitions. Starting from its classes, refine simultaneously by signatures

   signature(s) = (current-class(s), (current-class(A_i^b(s)))_{i∈[p],b∈{0,1}}),

until stable. At most w−1 proper refinements. The final relation ≡ is the coarsest equivalence refining ~_V such that

   s≡t -> A_i^b(s)≡A_i^b(t)  for all i,b.

Why coarsest: any stable refinement of ~_V refines every intermediate partition by induction. It is the maximum legitimate deterministic state quotient of the first sweep which still retains all behaviors that the entire second sweep may observe on every input.

Write Q=[w]/≡, d=|Q|≤w, π:[w]->Q, and ̅A_i^b for the well-defined induced maps on Q.

## 3. Theorem: commuting on observable quotient suffices for polynomial #SAT

Assume induced first-sweep maps for DISTINCT input variables commute pairwise:

   ̅A_i^b ∘ ̅A_j^c = ̅A_j^c ∘ ̅A_i^b  (i≠j; b,c∈{0,1}).

Then exact #accepted primary assignments can be computed in O(p d² w) arithmetic operations, plus the polynomial-time certificate construction and test. All counts have O(p) bits.

Proof: Reorder first-sweep maps into the second-sweep variable order; the resulting FINAL quotient class is unchanged. For each guessed quotient class c∈Q, pick any representative r_c∈[w] and run a weighted read-once DP in order σ on pairs (u,v)∈Q×[w]. Initialize (π(s_0),r_c) with count 1. At variable i add both transitions
   (u,v)->(̅A_i^b(u), B_i^b(v)), b=0,1.
Accept at end if u=c and v∈Acc. For each primary assignment x, exactly one guessed c equals π(F_x(s_0)). The observation refinement guarantees V_x(r_c) has the same acceptance as V_x(F_x(s_0)), so it is counted exactly once iff accepted. Complexity: d guesses, dw DP states, p steps, 2 transitions each.

A slightly stronger sufficient condition checks commutativity only on the forward-closed orbit of π(s_0) under all induced transitions; this orbit is computable in polynomial time. This does not claim that all such quotients yield a universal polynomial algorithm: the quotient transition monoid may be noncommutative.

## 4. Automatic parameter via quotient noncommutation graph

Build the graph C on variables [p] with edge ij iff some ̅A_i^b and ̅A_j^c fail to commute (globally on Q, or on the closed orbit for a refined criterion).

Let τ be the minimum vertex-cover size of C. Standard parameterized branching finds a vertex cover E of size τ in 2^{O(τ)}poly(p,w) time. Fix its Boolean bits (2^τ branches). The exceptions split the remaining first sweep into τ+1 contiguous segments; within each segment all transitions commute on Q. Use the segment-gluing DP of checkpoint 24 on QUOTIENT first-sweep states and original second-sweep states, together with guessed segment starts and guessed final quotient class. Each accepted primary input has unique consistent guesses.

One safe explicit bound (arith. ops) is
   2^{O(τ)} · poly(p,w) · d^{O(τ)}.
More concretely, straightforward enumeration gives O(2^τ · p · w · d^{2τ+2}) after finding E, up to polynomial initialization and bit-operation factors.

For polynomial w, τ=o(p/log p) is a sufficient condition for 2^{o(p)}poly(p,w).

## 5. A real strict example

Let states S=Z_2×[3], width w=6. The first-sweep b=0 maps are identities. The b=1 maps toggle the first coordinate and permute the second by τ_i, alternating τ_odd=(12), τ_even=(23). Then A_i^1 and A_j^1 fail to commute for every odd/even pair (complete bipartite noncommutation graph with Θ(p²) conflicts), so the checkpoint-24 exceptional-variable parameter is Θ(p).

Let the second sweep, in the prime parallel-alternation order σ=(2,4,...,p,1,3,...,p−1) for even p, ignore the second coordinate and toggle the first coordinate on x_i=1 for EVEN i only. Accept iff the first coordinate equals 1. Then the overall output is
   accept(x) iff XOR_{odd i} x_i = 1.

The second sweep's observation partition is exactly the two first-coordinate fibers, and it is preserved by the first sweep. Induced first-sweep maps commute (each toggles the first bit). Theorem 3 gives polynomial exact #SAT independent of the prime root's size, despite Θ(p²) genuinely noncommuting raw transition pairs. There are exactly 2^{p−1} accepting assignments.

The example can be inflated to polynomial width with many unobserved auxiliary states and noncommuting transition actions. The result is not simply checkpoint 24's original commuting-sweep theorem.

## 6. Fundamental limits

1. The coarsest congruence is minimal only **among state quotients that preserve all second-pass behaviors and are respected by every first-sweep transition**. It is not a lower bound on general algorithms, symbolic representations, or assignment-dependent existential interfaces.
2. Small d is NOT sufficient alone. Checkpoint 23 gives a width-three two-sweep NP-hardness construction: the first sweep checks equality of incidence-variable copies, the second sweep checks CNF clauses. Thus even d≤3 may be NP-hard if the quotient transitions do not commute.
3. Pure read-twice algebraic-PIT is NOT a valid Boolean-SAT test. A program that reads x twice and accepts iff the two observed values differ rejects all consistent Boolean x, yet replacing Boolean choices by affine matrix factors gives the formal polynomial 2x(1−x), nonzero over characteristic zero. Boolean multilinearization modulo x²=x is essential; ordinary PIT of the unquotiented polynomial can yield false positives.
4. The original aim of a universal 2^{o(p)}poly(w,p) algorithm for polynomial-width read-twice programs remains OPEN. Likewise no NEXP notsubseteq L/poly theorem follows.

## Validation and context

- A Python exhaustive comparison checked 3000 random small programs (p≤7,w≤6), including 1329 where the quotient-commutation certificate held. Every certified instance's exact DP matched exhaustive counting.
- An explicit six-state family passed for p=4,6,8,10,12; raw transitions did not commute and the quotient contained exactly two classes.
- A further 280 random instances tested the segment-modulator recurrence in every case that met its per-segment quotient commutativity test; all agreed with exhaustive counting.
These are empirical cross-checks, not novelty verification.

Related context:
- Partition refinement / DFA minimization, classical; https://doi.org/10.1016/S0304-3975(99)00150-4
- Seto–Teruyama, oblivious read-twice BP-SAT (2016); https://doi.org/10.1587/TRANSFUN.E99.A.1019
- Anderson–Forbes–Saptharishi–Shpilka–Volk, read-k algebraic ABP PIT (2016); https://doi.org/10.4230/LIPIcs.CCC.2016.30
- Checkpoints 21, 23 and 24 in this repository.

## 7. Equivalent linear-observation formulation (a promising next interface)

Let transition maps be represented by column-deterministic matrices over F_2: A_i^b e_s=e_{A_i^b(s)}, B_i^b e_s=e_{B_i^b(s)}. Let a be the row indicator vector of accepting states.

The span O of all acceptance rows a^T V_x is computable in polynomial time: start with the one-dimensional row span <a^T> at the terminal layer and, walking BACKWARDS through the second sweep, replace L by span(L B_i^0 ∪ L B_i^1). The final L is exactly O because the second-sweep reads are disjoint inputs.

Define the invisible subspace N_0=O^perp. Distinct basis states e_s,e_t are behaviorally equivalent iff e_s−e_t∈N_0 (over F_2 this is e_s+e_t). The greatest first-sweep invariant invisible subspace is found through

   N_{j+1}=N_j ∩ ∩_{i,b} (A_i^b)^{-1}(N_j),

stabilizing in at most w strict dimension drops. For deterministic first-sweep transitions, the state equivalence induced by N_infinity is precisely the coarsest behavior-preserving first-sweep congruence of Section 2. To see this, any pair difference contained in N_infinity stays invisible under arbitrary first-sweep words. Conversely the span of all differences within classes of the coarsest stable partition lies inside N_infinity.

One can test whether all projected commutators vanish:

   [A_i^b,A_j^c](F_2^w) ⊆ N_infinity.

For deterministic maps this is exactly the quotient-commutativity criterion of Section 3. For weighted or linear branching programs, the subspace and commutator formulation may generalize more naturally than state partitions, but exact counting for arbitrary weighted models is NOT proved here.

An open quantitative direction is whether low-rank *nonzero* projected commutators permit an algorithm with exponent governed by the cumulative observable defect, rather than by the number of variables. Rank-smallness alone is NOT a theorem of efficient composition.
