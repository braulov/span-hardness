# Checkpoint 31 — Fourier-output sparsity, separable features, and the width-two exact counting threshold

Research date: 2026-10-30. Self-contained mathematical deductions in the span-hardness/LGS input-efficient BP-SAT program. The **priority/novelty of these precise statements has not been independently established**. This checkpoint extends docs/30_lowdegree_feature_span_deterministic_sat.md. It is about TWO-SWEEP deterministic oblivious BPs (each input read exactly once per pass). General width-two read-many BP-SAT is known NP-complete, so DO NOT conflate models.

## 1. Fourier support as an algorithmic parameter, over F3

Let the first pass read x_1,...,x_p with deterministic transition matrices P_i^0,P_i^1∈F3^{w×w}, column e_s mapped to e_{P_i^b(s)}. Let f_s(x)=1[F(x)=s]∈F3 and write its character/Fourier expansion

    f_s(x)=Σ_{α∈F2^p} fhat_s(α) χ_α(x),
    χ_α(x)=(-1)^{Σ_i α_i x_i}∈F3.

The characteristic is 3, so the character basis is valid (2 is invertible) and an actual Boolean indicator remains 0 or 1. Let S = union_s supp(fhat_s), m=|S|.

THEOREM. Exact Two-Sweep BP-SAT and witness search are solvable deterministically in poly(p,w,m) time, and S is computable in poly(p,w,m) time from the supplied FIRST-pass transition tables. No Fourier-support certificate is required. Thus m=2^{o(p)}, w=poly(p), gives an input-efficient 2^{o(p)}poly(p,w) algorithm despite arbitrary second-pass order/transitions.

## 2. Output-sensitive Fourier-support enumeration using a vector ROABP

Define K_i^0=P_i^0+P_i^1 and K_i^1=P_i^0-P_i^1 over F3. Exact Fourier coefficients are

    fhat_vector(α) = 2^{-p} K_p^{α_p}...K_1^{α_1} e_{s0}.

The scalar factor 2^{-p} is invertible and irrelevant for nonzero support.

For any prefix α_1,...,α_t compute v_t=K_t^{α_t}...K_1^{α_1}e_{s0}; ask if some suffix frequency has a nonzero coefficient vector. This is a WHITE-BOX read-once algebraic BP nonzeroness problem: start with the span of v_t, and for each j=t+1,...,p replace the span V by K_j^0(V)+K_j^1(V), choosing a Gaussian basis after each step. The answer is YES iff the final span is not {0}; each such span has dimension ≤w. This requires poly(p,w) field operations.

Perform DFS on the binary frequency tree, retaining exactly prefixes with a nonzero supported extension. Every retained prefix is a prefix of at least one supported α; at most O(pm) nodes are visited. Enumerate the m leaves and obtain exact S in poly(p,w,m) time. This works over F3 without any assumptions on coefficients over the reals. A Fourier coefficient that vanishes modulo 3 is omitted correctly, because the expansion over F3 remains exact.

## 3. Relative hitting sets from parity-character features

For known S={α_1,...,α_m}, define Ψ(x)=(χ_{α_j}(x))_{j=1}^m∈F3^m. For a partial assignment, set all unread variables provisionally to zero. When read-once second pass processes bit i=b, the feature vector changes via a DIAGONAL linear map

    Ψ_j ← (-1)^{b α_{j,i}} Ψ_j.

The initial feature vector is (1,...,1). At each second-pass state retain a Gaussian basis of reachable feature vectors, keeping concrete input-prefix witnesses for every basis member. Transition each basis vector for the two bit choices, select an independent subset again. At acceptance, retain ≤m ACTUAL accepting complete assignments K_s, such that

    span{Ψ(x):x∈K_s}=span{Ψ(x):second pass starting at s accepts x}.

Because every f_s is a linear functional of Ψ, a compatible input exists iff one of these representatives x∈K_s satisfies F(x)=s. Just simulate the actual first pass on all representatives, without ever computing Fourier coefficients explicitly. Complexity poly(p,w,m).

The method is deterministic and exact for SAT; it does NOT automatically count all accepting assignments as integers (span compression discards multiplicity).

## 4. A more general product-feature lemma

Let a finite field K be given and suppose we have explicit univariate factors h_{i,j}:{0,1}→K for j=1,...,m and i=1,...,p, with

    f_s(x)=Σ_{j=1}^m c_{s,j} Π_{i=1}^p h_{i,j}(x_i)

for EVERY possible middle state s. (The coefficient tables c_s need not be used by the witness-search algorithm, only existence of the representation matters.)

Define separable features Φ_j(x)=Π_i h_{i,j}(x_i). With unread bits provisionally *not included* in the partial product, the initial feature vector is all ones. When i=b is read, update by the diagonal matrix diag(h_{i,1}(b),...,h_{i,m}(b)). This is linear even if factors equal zero. The exact same relative hitting-set DP works and gives deterministic SAT and witnesses in poly(p,w,m).

Fourier sparsity is the special case h_{i,α}(b)=(-1)^{α_i b}. The degree-D monomial feature-space theorem of checkpoint 30 is another case: h_{i,S}(b)=b if i∈S and 1 otherwise. General separable rank can be small while BOTH characteristic-3 Fourier sparsity and F2 ANF degree are large.

## 5. Exact #SAT for a FIRST SWEEP of width two

A deterministic map {0,1}→{0,1} is one of I, S=(01), C0 (constant 0), C1 (constant 1).

For a given full assignment there is a UNIQUE index j∈{0,1,...,p} of the last reset C0/C1 in the FIRST sweep (j=0 if no reset).

- Case j=0: all chosen transitions are permutations I/S; the first pass output equals s0 XOR parity of their swap indicators.
- Case j≥1: before j, transitions are arbitrary; at j the chosen map must be a reset to c_j(x_j)∈{0,1}; after j all chosen maps are permutations; first pass output is c_j(x_j) XOR parity of swaps strictly after j.

For fixed j and guessed middle state z∈{0,1}, simulate the SECOND sweep in its own arbitrary variable order. Track its current state (width w), one swap-parity bit, and (for j≥1) the reset-output bit. At input i=b enforce only the UNARY condition required by its position relative to j (none before j, reset at j, permutation after j), and update parity/reset bits. At termination check second acceptance and that the computed first output is z.

Exactly one guess z and one last reset index j belong to each primary assignment, so SUM of these DP counts is the EXACT number of accepted input assignments. Time O(p² w) arithmetic operations, using O(p)-bit nonnegative integer counts; valid for arbitrary polynomial-width second pass, even with non-injective transitions. This is much stronger than SAT existence and uses neither spectral sparsity nor low algebraic degree.

An alternative proof: every endpoint indicator f_s of a width-two FIRST sweep has product-feature rank ≤2(p+1) over F3. Split by last reset j. Put p_i(b)=1 if selected map is I or S, else 0; t_i(b)=+1 for I, −1 for S, 0 for resets; r_i(b)=1 for C0 or C1, else 0; v_i(b)=+1 for C0, −1 for C1, 0 for permutations. For initial state 0,

    f_s(x) =
      (1/2) [ Π_i p_i(x_i) + (-1)^s Π_i t_i(x_i) ]
      + (1/2) Σ_{j=1}^p [
          r_j(x_j) Π_{i>j} p_i(x_i)
        + (-1)^s v_j(x_j) Π_{i>j} t_i(x_i)
        ].

Empty products equal one; factors for indices i<j equal one. The expression is exact pointwise over F3 and yields 2(p+1) pure tensor terms common to both endpoints. For initial state 1, change the sign of the no-reset signed term by (-1)^{s0}.

Thus width-two first-sweep output has small SEPARABLE rank even for AND_p, whose F2 ANF degree is p and whose Fourier support over F3 is full 2^p.

## 6. Generalization: reset + small abelian permutation group

Suppose first-sweep maps A_i^b:[w]→[w] are either a CONSTANT map C_c or a permutation from a known abelian group K≤S_w with |K|=g. The second sweep is arbitrary deterministic and read-once, in any variable order.

Again branch on the UNIQUE last constant transition j (including j=0 for no constants). At j≥1 store the reset output c; at positions i>j only K-permutations are allowed; the product g_x∈K of these later permutations is independent of ordering because K is abelian. At earlier positions allow any transition. In the second-sweep variable order maintain (second state, reset value, g_x), and check guessed middle state equals g_x(c) (or g_x(s0) for j=0). Sum counts over all last-reset choices and guessed states. This gives exact #SAT in poly(p,w,g) arithmetic operations, so polynomial time whenever |K|=poly(p,w). The group K must be explicitly and efficiently enumerated, with a multiplication/action table.

The raw first-sweep maps need not commute: C_c and a permutation g may satisfy g◦C_c ≠ C_c◦g. So this genuinely extends checkpoint 24's commuting-sweep criterion.

## 7. A width-three exact separable-rank barrier

The coalesced COPY-EQUALITY function on p=2k bits,

    E(a_1,b_1,...,a_k,b_k)=Π_{j=1}^k [a_j=b_j],

is computed by a deterministic width-three read-once first sweep in order a_1,b_1,a_2,b_2,..., with states 0,1,dead: store the first bit of each pair, reject on mismatch, reset to next pair, keeping dead absorbing.

Any decomposition of E into m pure tensor products Π_i h_{i,j}(x_i) over ANY field, with arbitrary univariate factors, must have m≥2^k. Proof: flatten the tensor with row assignment a∈{0,1}^k and column assignment b∈{0,1}^k. Its resulting 2^k×2^k matrix is I_{2^k}, of full rank 2^k, whereas each pure tensor product yields a rank-one matrix. Thus m≥2^k. Equality is attained by the obvious sum of 2^k assignments.

This is a FORMAL barrier for the explicit separable-feature representation, not a running-time lower bound on arbitrary algorithms. The full two-sweep width-three SAT problem was reduced from 3SAT in checkpoint 23; ordinary NP-hardness alone cannot disprove 2^{o(p)} algorithms.

## 8. Empirical checks and limitations

- /mnt/data/check_fourier_twosweep.py: 600 randomized two-sweep deterministic programs (p≤8,w≤6), comparing automatically enumerated F3 Fourier support to direct full Walsh transform, and actual accepted witness from the relative hitting-set DP to exhaustive SAT. All passed. A parity-accumulator example had support 2^t with t independently stored parity bits, versus 2^p possible frequencies.
- /mnt/data/check_width2_twosweep.py: 2000 random exact integer-count tests, width two first sweep, arbitrary second sweep with widths 2–8 and arbitrary read order. All passed.
- /mnt/data/check_width2_tensor.py: 1000 random width-two first sweeps, exact verification of all endpoint-indicator product decompositions over F3 for all 2^p inputs. All passed.
- /mnt/data/check_reset_abelian_twosweep.py: 1200 random exact counting tests with abelian groups of up to eight disjoint-pair permutation states, interspersed with constant resets; arbitrary second sweeps. All passed.

These brute-force checks are supporting evidence. The algebra and unique-last-reset argument constitute the proofs.

## 9. Relationship to literature and next objective

Fourier-sparse Boolean functions and their parity-decision-tree complexity have an extensive literature, e.g. Sanyal, *Fourier Sparsity and Dimension* (Theory of Computing, 2019), https://doi.org/10.4086/toc.2019.v015a011.
The Fourier-support enumeration follows standard white-box ROABP zero testing via linear-span propagation.
General deterministic width-two branching-program SAT with unrestricted repeated reads is NP-complete; see Makita–Nagao–Okada–Seto–Teruyama (IEICE 2022), https://doi.org/10.1587/transfun.2021EAP1120. This does not contradict the two-sweep width-two FIRST PASS theorem.
Exact oblivious read-twice BP-SAT algorithms: Seto–Teruyama (IEICE 2016), https://doi.org/10.1587/transfun.E99.A.1019.

The natural next attack is not another generic parameter for width two: that case is completely solved in polynomial time. The width-three first pass, even with a simple reset-and-compare automaton, can encode exponentially large tensor flattening rank and NP-hard 3SAT interfaces. A genuinely new idea would compress the INTERSECTION of a width-three read-once endpoint language with a second arbitrary-order read-once BP without preserving all multilinear or separable-product observations. Universal polynomial time would imply P=NP. A hypothetical 2^{o(p)}poly(p,w) algorithm for unrestricted polynomial-width two-sweep BP-SAT remains out of reach and could feed into larger circuit-lower-bound agendas, subject to model and parameter reductions.
