# Checkpoint 24 — Two-sweep BP-SAT with a commuting sweep, and a noncommuting-transition modulator

2026-10-29. Research note. These are self-contained exact algorithms; novelty relative to all prior literature is NOT established. The goal is to handle polynomial width w, not only constant width. Experiments are supporting checks, not substitutes for the proofs.

## Crucial correction to earlier target

Fixed-width (say w=5) **read-twice** programs have length T=2p and encode parsimoniously in 3-CNF with N=O(p) declared variables and O(p) clauses, since each deterministic state transition has constant arity. The October 25, 2026 OpenAI #CNF manuscript states exact counting in 2^{O(N/sqrt(log N))} poly(N) for constant clause density; a slightly weaker subexponential result is in the accompanying Lean scope. Conditional on that work, there is already a 2^{o(p)} algorithm for arbitrary width-five read-twice BPs, reversible or not. The meaningful remaining target is w=poly(p): a standard Boolean state encoding incurs Θ(p log w) extra variables and does not yield subexponential-in-p time from those bounds alone.

Source: https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex

## Model

p primary variables; first sweep reads x_1,...,x_p, second sweep reads x_{σ(1)},...,x_{σ(p)}. On reading x_i=b in sweep one, apply map A_i^b:[w]->[w]; in sweep two, apply B_i^b:[w]->[w]. Arbitrary deterministic maps are allowed, not necessarily permutations. Initial state s0 and accepting final-state set Acc. Exact #SAT is required.

## Theorem 1: commuting first sweep implies polynomial exact #SAT for any σ

Suppose all first-sweep transition maps A_i^b commute pairwise across different variables i (this can be weakened to commutativity on the forward-closed orbit of s0). Then the effect of the first sweep on s0 is unchanged if its operations are reordered into σ-order.

For every guess z∈[w] of the intermediate state between sweeps, process variables in the SECOND sweep order σ and maintain a weighted DP indexed by (u,v)∈[w]^2. Initialize DP_z(s0,z)=1. At the occurrence of variable i, update:
  DP'_z(A_i^b(u), B_i^b(v)) += DP_z(u,v), for each b∈{0,1}.
At the end, sum DP_z(z,v) over v∈Acc and all guessed z. For each assignment x, u=U_x(s0), while v=V_x(z); exactly one guess z=U_x(s0) passes the equality test. Therefore the algorithm counts each accepting x exactly once.

Complexity O(p w^3) arithmetic operations and O(w^3) DP entries if guesses are batched; counts contain at most p+1 bits, so polynomial bit-time. This holds for w=p^{O(1)}, arbitrary σ (including a simple prime permutation of size Θ(p)), and arbitrary (even irreversible) second-sweep transitions. Symmetrically it works when the second-sweep transition maps commute pairwise; process variables in first-sweep order and guess the input to the commuting sweep.

Orbit variant: let O⊆[w] be the smallest set containing s0 and closed under all A_i^b. It is computable in polynomial time. It suffices that the maps commute on O. This may hold even if they do not commute on [w].

## General lemma: a change-of-order certificate

Suppose the state-valued function F(x)=U_x(s0) computed by sweep one has a known ordered branching program C of width d, reading the variables in σ-order and outputting F(x)∈[w] at the end. The second-sweep state is V_x(z) for a guessed starting state z∈[w]. Process the two programs C and V simultaneously, tracking C's state and V's state, for each z. At termination check output_C=z and V-state∈Acc.

Time O(p d w^2) arithmetic operations (up to the representation of C). This is exact for arbitrary deterministic maps in both sweeps and arbitrary σ. Theorem 1 instantiates d≤w by reordering commuting operations. Such a certificate is not always small: OBDD reordering can incur exponential blowup.

## Theorem 2: q exceptional variables separating commuting first-sweep segments

Let E={e_1<...<e_q} be q exceptional indices in the FIRST pass. The remaining first-pass positions form q+1 consecutive segments S_0,...,S_q. Assume that for each segment S_j all maps A_i^b, i∈S_j, commute pairwise with maps of *other* indices in that SAME segment. Nothing is assumed about exceptional transitions, interactions across different segments, the second sweep, or σ.

Branch on the 2^q values of the exceptional variables, freezing both of their occurrences. For each such branch guess the entry states z_1,...,z_q of first-sweep segments 1,...,q, and the intermediate state z after the entire first sweep. Segment zero begins at z_0=s0. In σ-order, maintain each segment's current state u_j (initialized to z_j) and the second-sweep current state v (initialized to z). For a private variable i∈S_j, branch over b∈{0,1}, update u_j←A_i^b(u_j) and v←B_i^b(v). For an exceptional variable its value is fixed and only v is updated.

At the end enforce v∈Acc, z=u_q, and for each j=0,...,q−1:
  z_{j+1}=A_{e_{j+1}}^{fixed-value}(u_j).
These equations guarantee that the guessed states equal the true first-sweep segment boundaries. Each assignment has a unique set of guesses, so counts are exact. A direct, unoptimized bound is
  O(2^q p w^{2q+3}) arithmetic operations,
polynomial space for each q, if q constant. For w=poly(p), q=o(p/log p) gives 2^{o(p)} poly(p,w), independently of the second order's prime decomposition. Symmetric statement holds if we modulate the second sweep instead.

This is an FPT/XP-type upper bound in (q,log w), NOT a universal subexponential algorithm. For q=0 it reduces to Theorem 1. Finding the smallest eligible exceptional set is a separate combinatorial optimization problem; the theorem accepts E as a certificate.

## Explicit family with a linear-size prime root

Take p=2k and second-sweep order
  σ=(2,4,...,2k,1,3,...,2k−1).
For all k≥2 this 'parallel alternation' permutation is simple (there are no nontrivial common intervals), hence its substitution tree has a single prime root of size p. Set all first-sweep maps to powers of one common permutation a (so they commute), while choosing arbitrary second-sweep transition maps, even noncommuting and irreversible. Then exact #SAT is solvable in O(p w^3) independently of this largest-possible prime root.

With one exceptional first-sweep instruction b that does not commute with a, Theorem 2 applies with q=1 and gives O(p w^5) arithmetic operations, even though the complete first sweep is not abelian.

In fact the deletion-to-separable distance of this permutation is **exactly k−1 = p/2−1**, so the new polynomial algorithm covers a family where BOTH prior structural parameters are linear. Proof: Partition the values into k adjacent pairs {2j−1,2j}. If a subsequence retains both values of two distinct pairs i<j, then its four selected elements 2i,2j,2i−1,2j−1 appear in this relative order and form pattern 2413. Hence any separable subsequence retains both values of at most one pair, so has length ≤k+1. Equality is achieved by all k even values plus the odd value 1: their induced permutation is (2,3,...,k+1,1), a skew sum of an increasing list and a singleton and therefore separable. Thus the minimum number deleted is 2k−(k+1)=k−1. Also σ is simple: any proper contiguous interval confined to one half has gaps in its values, while any interval crossing the halves contains both 1 and 2k and therefore cannot have consecutive values unless it is the whole permutation.

## Proof/implementation checks

Python brute force against all 2^p input assignments:
- 2000 randomly generated programs with 1≤p≤8, 2≤w≤6, commuting first sweep (powers of a common cycle), arbitrary random second-sweep deterministic maps and random σ: exact #SAT counts matched.
- 200 random programs with 2≤p≤7, 2≤w≤4, and q≤2 exceptional first-sweep variables separating commuting blocks. Matrices of transitions in each block were powers of randomly chosen cycles; exceptional and second-sweep transitions were arbitrary random maps. Exact counts matched.
Neither test is a literature-novelty audit.

## What this suggests for the main NEXP/L/poly research program

The right object to compress is not a prime permutation alone; it is the *cost of rearranging one sweep's state-valued computation into the other sweep's variable order*, or finding a smaller existential interface preserving only consistency with the second sweep. Explicit order-reordering can have exponential OBDD blowup, and a large prime root can be trivially handled when one sweep commutes. No universal 2^{o(p)}poly(w,p) algorithm or circuit lower bound has been proved.

Related sources:
- Lee, Pyne, Vadhan, RANDOM 2023, https://doi.org/10.4230/LIPIcs.APPROX/RANDOM.2023.44
- Krause, Savicky, Wegener, OBDD variable ordering, https://eccc.weizmann.ac.il/report/1999/011/
- Seto, Teruyama, 2016 exact read-twice BP-SAT, https://doi.org/10.1587/TRANSFUN.E99.A.1019
- Earlier checkpoints docs/21_two_sweep_substitution_decomposition.md and docs/23_two_sweep_width3_prime_hardness_and_separable_distance.md
