# Checkpoint 30 — Deterministic SAT for low-degree first-pass state indicators and arbitrary read-once second pass

Research date: 2026-10-30. This is an elementary exact algebraic algorithm derived in the project; independent novelty/prior-art verification has not been completed. This CHECKPOINT SUPERSEDES the initial randomized parity+Isolation approach: randomization is not needed. It substantially strengthens docs/28 and 29 for SAT decision, but says nothing about exact integer counting.

## Model

A deterministic two-sweep oblivious branching program has:
- p PRIMARY Boolean input bits x_1,...,x_p;
- common width w, polynomial in p in the principal application;
- first pass reads each bit exactly once, in some fixed order, from start state s0, ending in state F(x)∈[w];
- second pass reads each bit exactly once in ANY different permutation σ, applies arbitrary (possibly many-to-one) transition maps B_i^0,B_i^1:[w]→[w], and accepts if its final state is in Acc⊆[w].

For each possible middle state s define its first-pass indicator f_s(x)=[F(x)=s] over F2 and its second-pass acceptance predicate H_s(x)=[second pass starting at s accepts x]. The full program accepts iff ∨_s (f_s(x) AND H_s(x)); the cases are disjoint for each x.

Assume that EACH f_s has a multilinear Algebraic Normal Form (ANF) of F2-degree at most D, with all coefficients constructible in time p^{O(D)}poly(p,w). No promise is made that such low-degree representations exist for general BPs.

## Theorem — Deterministic p^{O(D)} polynomial-width two-sweep SAT

Under the above promise,

    TwoSweepBPSAT ∈ DTIME[p^{O(D)} poly(p,w)].

Moreover, a satisfying primary assignment can be recovered within an additional polynomial factor (e.g. p self-reductions), and one can deterministically minimize any polynomially bounded nonnegative linear input weight by augmenting the second-pass state with the accumulated weight.

Proof: Let M=sum_{j=0}^D binom(p,j), and index coordinates by monomials S⊆[p], |S|≤D. Define the evaluation feature vector

    Φ_D(x) ∈ F2^M,
    Φ_D(x)[S]=∏_{i∈S}x_i,

including the constant feature Φ_D(x)[∅]=1. For each s, let c_s∈F2^M be the ANF coefficient vector; f_s(x)=<c_s,Φ_D(x)>.

For each s, we need to determine whether ∃ x accepted by the SECOND pass started in s with <c_s,Φ_D(x)>=1.

The second pass is read-once. Process its variables one at a time. At any layer, assign unread input bits the temporary value zero, so the features of a processed partial assignment are well defined in the FULL M-dimensional feature space. When encountering previously unread bit i with choice b∈{0,1}, the feature vector transforms by the F2-LINEAR map L_{i,b}:

    (L_{i,b} v)[S] =
      v[S]                   if i∉S,
      b · v[S\{i}]            if i∈S.

Crucially this map is linear on the vector of monomial features, because the constant coordinate is present. The maps are valid on all actually reachable partial-assignment feature vectors and therefore on their span.

At each second-pass state q at each layer, store a Gaussian basis of

    V_q = span_F2 { Φ_D(partial x) : there exists a partial input assignment taking the second pass from s to q }.

Initially V_s=span{e_∅} and all other spaces zero. When variable i is read, update
    V_{B_i^b(q)} += L_{i,b}(V_q)
for b=0,1 (sum of subspaces), and row-reduce. By induction the basis spans EXACTLY the desired feature vectors; every basis has dimension at most M. At the final layer, let V_acc be the sum of spaces of accepting states. There exists an accepted x with f_s(x)=1 iff the linear functional c_s is NONZERO on V_acc, equivalently iff at least one basis vector v has <c_s,v>=1.

Proof of equivalence: If f_s is zero on all actual accepted evaluation vectors, it is zero on their span. Conversely, if nonzero on their span, it must be nonzero on at least one actual accepted evaluation vector; a linear functional cannot be nonzero on their span while vanishing on all generators.

Runtime: at most w state spaces, each dim≤M; at most 2wM candidate-image insertions per step, each O(poly(M)) F2 operations. Run separately for ≤w middle states, obtaining p^{O(D)} poly(p,w). No enumeration of 2^p assignments, and NO randomness/Isolation Lemma required. Witnesses can be kept by retaining actual independent evaluation vectors together with their input prefixes rather than reduced combinations, or via self-reduction.

**Subexponential criterion:** If D log p=o(p), then the algorithm is 2^{o(p)}poly(p,w) for polynomial w. For constant D it is POLYNOMIAL. For D=polylog(p) it is quasipolynomial and hence subexponential in p.

## Recovering f_s ANF using only low-weight input evaluations

For any promised degree-D polynomial f_s on p inputs, the multilinear ANF coefficient of monomial x_S is

    c_{s,S} = Σ_{T⊆S} f_s(1_T)  (mod 2).

Thus evaluate the original FIRST sweep on the O(p^D) assignments 1_T of Hamming weight ≤D (zero elsewhere), then perform Boolean Möbius inversion for |S|≤D. No symbolic first-pass polynomial arithmetic is required. By the DEGREE PROMISE these coefficients specify f_s on all 2^p inputs. The total number of evaluations and coefficient operations is p^{O(D)}poly(p,w).

## Application: first pass from UT_d(F2), second pass arbitrary

Assume the first-sweep transitions are explicitly given by elements of the unitriangular matrix group UT_d(F2), with an efficiently evaluable action on the width-w state set. Each transition is controlled by exactly one bit, so all its matrix entries are affine functions of that bit over F2.

For any input x, let U(x) be the UT_d group product of first-sweep transition matrices. For each i<j, its (i,j) entry is an F2 Boolean polynomial of degree ≤j−i. Indeed every nonconstant product contribution follows a strictly increasing path of matrix coordinates i=i0<i1<...<ik=j and uses at most j−i controlled factors. Repetitions of a primary bit would not increase the multilinear degree, but each bit is already read once in this model.

For each fixed g∈UT_d, its equality indicator over F2 is
    [U(x)=g]=∏_{i<j}(1+U_ij(x)+g_ij).
This is degree at most
    D_group=Σ_{i<j}(j−i)= d(d−1)(d+1)/6 = binom(d+1,3).
If the action has arbitrary state set, the middle-state indicator is
    f_s(x)=Σ_{g: g·s0=s}[U(x)=g]  (mod 2).
As the group events are disjoint, this is the exact Boolean indicator and its degree is ≤D_group. We can construct its ANF by low-weight evaluations WITHOUT enumerating all g.

Hence for any given efficient permutation action of UT_d(F2),

    TwoSweepBPSAT ∈ DTIME[2^{O(d³ log p)} poly(p,w)],

with the trivial 2^p brute-force algorithm used if the bound is worse.

If d is FIXED, this is deterministic POLYNOMIAL TIME, regardless of the read-order permutation σ, regardless of the second-sweep transitions (even arbitrary irreversible maps), and REGARDLESS of prior quadratic/cubic cutrank parameters. If d=O(log p), the bound is 2^{O(log^4 p)}poly(p,w)=2^{o(p)}poly(p,w), and the natural group actions have polynomial width.

### Better bound for the natural action on binary vectors

Let UT_d(F2) act on the homogeneous affine state space {(u_1,...,u_{d−1},1)} ≅ F2^{d−1}, of width w=2^{d−1}. For a fixed initial state u0, the output coordinate i≤d−1 of U(x)u0 has ANF degree ≤d−i. Therefore

    f_s(x)=[U(x)u0=s]=∏_{i=1}^{d−1}(1+(U(x)u0)_i+s_i)

has degree at most

    D_affine=Σ_{i=1}^{d−1}(d−i)=d(d−1)/2.

Thus

    T ≤ 2^{O(d² log p)} poly(p,w).

For d=O(log p), this is 2^{O(log³ p)}poly(p,w). For UT4 acting on 8 states, D_affine≤6, giving a DETERMINISTIC POLYNOMIAL-TIME SAT ALGORITHM even with an arbitrary second sweep.

## Contrasting with the #P-hard UT4 counting checkpoint

Checkpoint 29 gives a metric reduction from #2SAT to exact integer #accepted assignments of a width-24 two-sweep program whose first sweep is UT4(F2) on an eight-state affine register and whose second sweep checks equality of occurrence copies using three states. This does NOT conflict with the present deterministic SAT theorem: the first-sweep output indicators have constant F2 degree, so BOOLEAN EXISTENCE is easy, whereas exact integer counting remains #P-hard. Likewise parity #accepted is computable in polynomial time by expanding f_s into monomials and running mod-2 weighted read-once second-pass DP.

This is an actual DECISION-versus-EXACT-COUNT separation for a restricted computation model, not a general complexity-class separation.

## Additional exact parity-by-weight algorithm (optional)

One may calculate the polynomial over F2

    Z(z)=Σ_{x accepted} z^{Σ_i λ_i x_i},

where λ_i are random or fixed polynomially bounded positive integer weights, using expansion f_s=Σ_I c_{s,I}x_I and ordinary read-once BP counting DPs over F2[z] for each monomial x_I. The coefficient at weight t is the parity of accepting strings of that weight. The Mulmuley-Vazirani-Vazirani Isolation Lemma says random λ_i∈[1,2p] isolate the minimum-weight solution with probability ≥1/2, giving an RP algorithm. However the feature-span algorithm above is strictly stronger because it is deterministic and directly decides nonemptiness without parity cancellation or isolation.

The isolation-based derivation was the discovery path; it is not the final best algorithm.

## Verification

A standard-library Python script /mnt/data/check_lowdegree_twosweep.py independently evaluates the first sweep on all low-weight assignments, constructs ANF indicator coefficients, and propagates Gaussian feature-space bases through arbitrary read-once second sweeps. Across 91 random UT4 width-eight programs (p=1,...,7), exact SAT yes/no agreed with exhaustive 2^p search. The second sweeps used arbitrary, generally noninjective transition tables and random read-order permutations.

Separately, a full Boolean Möbius transform over all 2^p assignments for 105 random UT4 programs with p in {8,9,10} confirmed that EVERY endpoint indicator has ANF degree at most six, as the algebra predicts.

Code and tests are validation, not proof of novelty. The published PIT/ABP literature is related but does NOT itself certify priority of this exact Boolean feature-space algorithm:
- Forbes and Shpilka (FOCS 2013), https://eccc.weizmann.ac.il/report/2012/115/
- Gurjar, Korwar, Saxena (Theory of Computing 2017), https://www.theoryofcomputing.org/articles/v013a002/
- Isolation Lemma (MVV, STOC 1987), https://doi.org/10.1145/28395.383347

## Implications and next hard target

This is the first DETERMISTIC input-efficient SAT algorithm in this branch that does not require low cutrank, commutation, separable read orders, or low noncommutativity modulator. For fixed d, it handles ANY two-sweep second order and arbitrary polynomial width. For d=O(log p), it remains subexponential despite quasipolynomial degree-expansion overhead.

The obstruction to a universal algorithm for arbitrary polynomial-width branching programs is now more precise: the first-sweep endpoint indicators f_s may have F2 algebraic degree Θ(p), even for very small widths (Barrington-type AND programs). Low degree is a strong computational restriction but by no means universal.

The natural next direction is to replace monomial degree D by a smaller effectively constructible LINEAR FEATURE SPACE of functions in which all endpoint predicates f_s lie and in which each second-read update acts linearly. A polynomial-dimensional such space would yield polynomial SAT; an input-efficient 2^{o(p)} feature dimension for all polynomial-width BPs would be a major breakthrough. It is not currently known.
