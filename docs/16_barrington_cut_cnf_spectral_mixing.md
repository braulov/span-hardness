# Checkpoint: Barrington syntax, parity cut-CNF blowup, and spectral mixing for A5 programs

2026-10-29. Research notes. Elementary deductions are explicitly separated from established results; no general subexponential SAT algorithm is claimed.

## 1. Barrington CNF syntax does not produce a new open case

Barrington's theorem supplies a fixed 5-cycle g and a width-five group-program compiler for any fan-in-two formula F, such that W_F(x) is identity if F(x)=0 and g if F(x)=1. Choose 5-cycles a,b with [a,b] also a 5-cycle; conjugate each child (taking values 1/g) to 1/a and 1/b; the commutator is 1 unless both children accept, and is a fixed 5-cycle otherwise; conjugate back. Inversion and multiplying by g implement NOT.

An AND gate uses two copies of each child's word, so L(F1 AND F2) <= 2 L(F1)+2 L(F2). A depth-d formula compiles to length O(4^d). In particular a balanced AND over m constant-size clause gadgets has polynomial length m^{O(1)} and preserves primary input count p.

However, if the compilation's syntax tree is explicitly supplied, solving SAT of the resulting group program is just solving SAT of the source CNF. The October 25, 2026 OpenAI fixed-width exact #SAT manuscript claims a deterministic 2^{O(p loglog p/sqrt(log p))} poly(p,m) algorithm, hence already a 2^{o(p)} algorithm for syntactically supplied Barrington encodings of k-CNF formulas, even when m is polynomial in p. This does not cover general NC1 formulas or arbitrary unannotated width-5 words. The manuscript's strongest quantitative bounds and ongoing review are separate from our deductions.

References: Barrington (1989), https://doi.org/10.1016/0022-0000(89)90037-8 ; OpenAI (2026), https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex

## 2. Parity as linear-size, constant-pathwidth LGS with exponentially many essential cut clauses

For p inputs, construct vertices (t,s) for t=0,...,p, s∈{0,1}, and an extra vertex r. At each transition t and state s, put edges ((t-1,s),(t,s)) labeled NOT x_t and ((t-1,s),(t,1-s)) labeled x_t. Add permanent edges r--(0,1), r--(p,0). The active edges at any assignment comprise two vertex-disjoint source-to-final paths. The path from (0,0) ends at (p, parity(x)), so the whole graph is connected exactly for EVEN parity. It has 2p+3 vertices and 4p+2 edges, and pathwidth at most 4 (bags containing r and consecutive layers).

Connectivity has a cut-CNF:
    AND_{∅≠S⊊V} OR_{e∈δ(S)} label(e).
For every odd assignment a define S_a = {(t,a_1 XOR ... XOR a_t): t=0,...,p}. The cut δ(S_a) contains, for each i, the two opposing-matching edges whose label is x_i if a_i=0, or NOT x_i if a_i=1, and no permanent edge. The cut-clause is false exactly at a. Hence the cut CNF contains >=2^{p-1} distinct essential clauses.

More generally ANY equivalent CNF over only the primary variables x_1,...,x_p, with no auxiliaries, needs >=2^{p-1} clauses: every non-tautological implicate of even parity mentions all p variables, since leaving any one free produces both parities. Each such full clause excludes exactly one odd assignment.

This is a representation-specific exponential barrier, NOT computational hardness: parity SAT is O(p). We brute-force checked connectivity and cut polarity identity for p=1,...,7 across all 254 assignments. General parity-CNF lower bound appears in Emdin et al., MFCS 2022: https://doi.org/10.4230/LIPIcs.MFCS.2022.47

## 3. A positive regime beyond abelian-block and commutation-component algorithms

Let W(x)=W_1(x_{X_1})...W_m(x_{X_m}) be a group program over a FIXED finite group G, where X_1,...,X_m are pairwise disjoint sets of primary Boolean variables (inside a block, variables may be reused arbitrarily). Let μ_j be the probability distribution of W_j under uniform independent inputs in X_j; the output distribution is μ=μ_1*...*μ_m.

For every nontrivial irreducible unitary representation ρ of G set
    hatμ_j(ρ)=E_{x_{X_j}}[ρ(W_j(x_{X_j}))],
    λ_j=max_{ρ nontrivial} ||hatμ_j(ρ)||_op.
Noncommutative Plancherel and the Diaconis-Shahshahani upper-bound lemma give
    ||μ-U_G||_TV <= (1/2) sqrt(|G|-1) product_j λ_j.
In particular, if product_j λ_j < 1/(|G|sqrt(|G|-1)), then every g∈G has output probability >=1/(2|G|), hence any acceptance predicate containing at least one element of G has a solution with probability >=1/(2|G|) under a random uniform assignment. Random testing therefore yields a bounded-error polynomial-time algorithm ON THIS PROMISE CLASS, regardless of internal complexity of blocks; it is enough to sample full inputs and evaluate the word. We do NOT assume λ_j efficiently given, only the guarantee.

Proof: Fourier transform of convolution is the ordered product of Fourier matrices. For nontrivial ρ, ||hatμ(ρ)||_F <= sqrt(dimρ) product_j λ_j. Then TV <= 1/2 sqrt(sum_{ρ!=1} dimρ ||hatμ(ρ)||_F^2) <= 1/2 sqrt((|G|-1) product_j λ_j^2).

Exact structural observation: λ(μ)=1 iff support of μ is contained in a coset of a proper subgroup H<G. Forward: a nontrivial ρ and a vector v achieving norm 1 for the average of unitaries imply all ρ(g)v coincide on support; support differences stabilize v and generate a proper subgroup. Backward: the permutation representation on G/H has a nontrivial constituent with H-fixed vector, giving operator norm 1 for μ supported in gH. For a full-support, well-spread distribution λ<1.

## 4. Explicit example over A5 with old parameters both linear

Let
    a=(1 2 3 4 5), b=(1 2 4 5 3)
be 5-cycles generating A5 (checked by explicit enumeration, subgroup order 60; [a,b]=(1 5 2 4 3) with composition convention).

Take
    W(x,y)=prod_{j=1}^m a^{x_j} b^{y_j}.
Each two-bit block has independent input variables and output distribution μ_j uniform on {1,a,b,ab}. In every nontrivial irrep of A5, ||(I+ρ(a))/2 (I+ρ(b))/2||op < 1: equality would yield a common invariant vector of both a,b, impossible because they generate A5. Hence μ_j has a uniform spectral gap; after O(1) blocks the total distribution is bounded below at every group element by a constant.

However the normalized word alternates noncommuting a and b, so the number of consecutive abelian blocks is 2m, while the variable noncommutation graph is connected and has 2m vertices. Thus old bounds 6^r and 2^c are exponential while the mixing criterion gives polynomial randomized satisfiability for any nonempty accepting subset of A5.

Direct exact convolution computation shows all 60 elements are reachable after m=5 blocks; for m=20 every group's probability is between 0.01629 and 0.01725 (uniform is 1/60). This is a demonstration of the promise result, not a universal width-five SAT algorithm.

## Next target

Study a structural win-win for arbitrary width-five group words:
(A) enough *approximately independent* strongly mixing segments to guarantee non-negligible acceptance probability;
(B) otherwise, a succinct description of repeated-variable correlations or restrictions to cosets of proper subgroups.
Do NOT assume independent blocks exist in general; Barrington's sparse-witness words can defeat random sampling. Need an actual quantitative certificate and runtime to move toward input-efficient 2^{o(p)} poly(T).

Sources: Diaconis-Shahshahani upper-bound lemma / finite-group harmonic analysis (standard); see standard references.
