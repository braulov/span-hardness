# T — Semantic orbit compression beyond noncommutative A5 profile rank

Checkpoint: 2026-10-28. This is a **promise-based** tractable class of arbitrary polynomial-size branching programs, plus a sharp coNP-completeness barrier to recognizing the promise and a provable large-rank example. It is **not** a general LGS-to-SetCover reduction and does **not** establish NEXP outside L/poly. Most component results (linear-size symmetric-function circuits, permutation-orbit evaluation, Barrington AND construction) are classical; **do not claim novelty** without a literature audit. Based on branch research/S-profile-rank-compression.

## 1. Orbit compression of a Boolean branching-program predicate

Let B be an **arbitrary** deterministic branching program on p Boolean variables, of description size S, with acceptance predicate f:{0,1}^p->{0,1}. There is no width, read-number, group or graph restriction. Partition the original variable indices into c known, disjoint blocks U_1,...,U_c, of cardinalities n_1,...,n_c. Assume the promised semantic invariance:

    f(x)=f(y) whenever sum_{i in U_j}x_i=sum_{i in U_j}y_i for every j.

Equivalently f is invariant under the natural action of S_{n_1} x ... x S_{n_c} by permuting variables inside blocks. Put

    M=product_j (n_j+1).

**Theorem T1 (orbit counting).** With this semantic promise, exact #BP-SAT and a satisfying assignment (if any) are computed deterministically in M*poly(S,p), specifically O(M*S)+poly(p,M) bit operations up to usual integer arithmetic. No appeal to October 2026 SAT results.

Proof: for each count vector a=(a_1,...,a_c), 0<=a_j<=n_j, evaluate B on the canonical assignment with the first a_j variables of U_j set to 1 and the rest 0. Call its Boolean output g(a). By invariance, each of the product_j binomial(n_j,a_j) assignments in the orbit has the same output. Thus

    #f^{-1}(1) = sum_a g(a) product_j binomial(n_j,a_j).

A YES witness is any canonical representative with g(a)=1. Number of samples M, each BP evaluation is poly(S). QED.

**Theorem T2 (small-universe Set Cover compilation).** Still under the promise, f has an explicit fan-in-two Boolean circuit of O(p+cM) gates constructible with M*poly(S,p) time, and therefore admits a standard polynomial-time (in S and M) pointwise Tseitin→SetCover reduction with

    universe u=O(p+cM), number of sets t=O(p+cM),
    budget O(p+cM).

Proof: independently compute the Hamming weight a_j of each block using O(n_j) Boolean gates. For the weighted binary sums, use 3-to-2 carry-save compressors, each replacing three same-weight bits by a sum bit and a carry bit of twice the weight; at most O(n_j) such compressors suffice, then a single O(log n_j)-bit final addition. Next decode the log(n_j+1)-bit result to all n_j+1 exact-weight one-hot indicators using a doubling decoder tree with O(n_j) AND/NOT gates: each binary prefix yields its two extensions. For every one of the M count vectors a with g(a)=1, compute the conjunction of its c relevant one-hot indicators using c-1 AND gates; OR the results. Total O(p+cM). Unique-extension Tseitin produces O(p+cM) Boolean variables and clauses. Standard CNF-to-SetCover: private elements force a single 0/1 choice set for each CNF variable; clause elements test disjunctions; budget equals number of Boolean variables. The universe, candidate-set count and budget are O(p+cM), and acceptance is preserved pointwise. QED.

**Corollary T3: one giant symmetric class and a few exceptions.** If all but b variables are freely exchangeable and the remaining b variables are singletons, then

    M=(p-b+1)2^b.

Decision/exact counting is 2^b poly(S,p), hence deterministic 2^{o(p)}poly(S) when b=o(p), *even if* the original group program is over A5 and has arbitrarily many repetitions and noncommuting transitions. At b=O(1) we additionally get a SetCover universe O(p). At b=O(log p) the SetCover universe is merely polynomial in p, NOT generally O(p); keep those claims separate.

When c=1 (complete input symmetry), M=p+1, hence exact #BP-SAT and SetCover universe O(p) regardless of BP size S=p^{100}. Every *symmetric* Boolean function has a linear-size bounded-fanin circuit, so the compression technique itself is classical; the point here is that it bypasses the profile-rank metric of S.

## 2. Concrete A5 example on which the canonical profile rank is LINEAR

The following example demonstrates rigorously why high canonical profile rank is **not** a semantic hardness certificate.

Use a fixed nontrivial 5-cycle γ in A5. A finite exhaustive A5 computation (or elementary conjugacy-class calculation) shows that every 5-cycle γ admits a pair of 5-cycles a,b with group commutator [a,b]=a b a^{-1} b^{-1}=γ. Fix one pair for each of the 24 five-cycles in a constant lookup table.

Define group words W(n,γ) for n a power of two, with n distinct independent switches:

    W(1,γ) = γ^{x_1},
    W(n,γ) = U V U^{-1} V^{-1},

where U=W(n/2,a) and V=W(n/2,b) depend on disjoint input halves and [a,b]=γ.

By induction W(n,γ)(x) equals γ iff all n input bits are 1, and equals 1 otherwise; U,V each output either their designated 5-cycle or the identity. Every group instruction is controlled by one input switch, all nontrivial deltas are **5-cycles**, and the word length obeys L(n)=4L(n/2)=n^2. Thus we have explicit polynomial-length width-five A5 group programs computing AND_n, with n inputs and n² instructions.

Consider ANY partition of such a word into consecutive commuting runs as in branch S. Since every delta has order 5, each abelian run lies in C5, and the input profile group K is elementary abelian C5^k, for some rank k. The **sparse-witness theorem S3** from the previous checkpoint states: every attainable group output has an input witness with at most (5-1)k=4k ones. But γ can be obtained ONLY when all n inputs are 1, of Hamming weight n. Hence

    n <= 4k,   or  k >= n/4,
    |K|=5^k >= 5^{n/4}=2^{Omega(n)}.

This is a theorem about *every commuting-run profile representation* of this particular word, **not** just the canonical segmentation. So the exact subgroup-state algorithm of S is intrinsically exponential on these BP instances. Conversely, the symmetric-function algorithm of T1 recognizes the accepting weight n in only n+1 evaluations, gives exact acceptance count 1, and T2 produces O(n)-universe Set Cover.

The actual canonical A5 profile ranks computed on the explicit Barrington words were:

    n=2: length 4, 4 runs, rank_5 = 2;
    n=4: length 16, 15 runs, rank_5 = 4;
    n=8: length 64, 61 runs, rank_5 = 8;
    n=16: length 256, 237 runs, rank_5 = 16.

These are finite experiments, not a proof that rank equals n for every power-of-two size; the lower bound k>=n/4 is fully proved for all powers of two.

This example is important: a program can be syntactically heavily noncommutative, have maximal-looking S-profile rank, and yet compute the trivial symmetric predicate AND_n. A stronger general LGS reduction must exploit **semantic information beyond a full profile rank**, not merely refine commuting segment boundaries.

## 3. An unconditional coNP-completeness barrier to AUTOMATIC symmetry detection

A natural reaction is to test whether a given A5 program computes a symmetric function, and then apply T1/T2. But recognizing such semantic simplicity is hard in the worst case.

**Theorem T4.** Given a polynomial-length width-five A5 group program and two distinguished input variables z,t, deciding whether the computed Boolean acceptance predicate is invariant under swapping z and t is coNP-complete. Consequently deciding full input symmetry is also coNP-complete.

Proof: membership in coNP follows because nonsymmetry has an NP witness x with f(x)≠f(swap_{z,t}x), checkable by evaluating the program twice.

For coNP-hardness, start from arbitrary CNF F(x_1,...,x_p), and introduce z,t. Define

    f_F(x,z,t) = z AND F(x),

where t is an independent dummy input. Since F is a CNF of polynomial size, a balanced AND tree gives a log-depth circuit for F; conjoin z. By Barrington's theorem, in polynomial time construct a polynomial-length width-five A5 group program whose output is γ on true inputs and 1 on false inputs (fixed 5-cycle γ). If F is UNSAT, f_F is identically zero, hence invariant under swapping z,t and fully symmetric. If F is SAT, choose satisfying x and z=1,t=0: f_F(x,1,0)=1, but f_F(x,0,1)=0. Thus even invariance under the SINGLE prescribed swap is equivalent to UNSAT.

For FULL symmetry, the same instance works: if F unsatisfiable it is identically zero; if satisfiable it is not even invariant under that transposition. Therefore testing either property is coNP-hard, and (by the witness argument for full symmetry using equal-weight permutations) coNP-complete. QED.

**Corollary T5.** Deciding if one distinguished input bit is *semantically inessential* for a polynomial-length A5 program is coNP-complete (reduce UNSAT through f_F=z AND F, with no t needed). Hence a universal polynomial-time routine that recognizes all eliminable variables would imply P=NP. This is an obstacle to automatically finding semantic compressions, **not** an ETH-time lower bound on LGS-SAT itself.

This theorem explains why a promise or efficiently checkable SUFFICIENT certificate is unavoidable for a straightforward orbit-based solver. It is consistent with T1 being fully constructive once invariance is known.

## 4. A checkable sufficient symmetry certificate

One tractable, intentionally incomplete certification method: supply, for each generator of the desired input permutation group, an explicit directed labeled automorphism of the branching program mapping query labels according to that generator, mapping 0/1 outgoing transitions accordingly, fixing the start state, and preserving accepting/rejecting terminal sets. Check each supplied vertex permutation and edge/query mapping in polynomial time. It then follows by induction on computations that the accepted predicate is invariant under the corresponding input permutations.

This certificate may fail to exist for a perfectly symmetric function represented by an asymmetric program; coNP-completeness of full semantic recognition implies no complete general polynomial-time recognizer unless P=NP. One can also accept formal proof traces of suitable group-word identities, verified stepwise; do not assert polynomial-length proofs exist for every symmetric word.

## 5. State of the original post-ETH win-win task

- Positive: a promised subclass of **arbitrary** polynomial-size BPs (not only width five) reduces pointwise to Set Cover with universe O(p) when its semantic orbit count M and number of blocks c satisfy cM=O(p). This is independent of the October 2026 #SAT announcement.
- Barrier: even a single requested input-swap invariance is coNP-complete to recognize for general A5 programs, so semantic quotient detection cannot be a free polynomial preprocessing step.
- Crucial negative example: on Barrington AND_n, rank-state DP from S requires 2^{Omega(n)} states while orbit compression uses O(n) evaluations.
- This does NOT imply a general LGS(p,S)→SetCover(u=O(p)) reduction; no ETH replacement or NEXP not in L/poly separation has been established.

A next target worth considering is a family of *checkable* semantic certificates for small orbit spaces, beyond literal graph automorphisms, or an algorithm for programs with "approximate" orbit symmetry coupled to a bounded number of exceptional assignments. But dense exceptional sets may encode arbitrary CNF satisfiability, so all promises and running times must be explicit.

## 6. Tests and sources

The accompanying \`verify_semantic_orbits.py\` is actually executed (Python standard library): constructs and evaluates linear-size Boolean counting + one-hot decoder circuits for 12 randomly chosen symmetric functions per p=1,...,32 (exhaustive on small inputs, randomized additional checks on larger p), and constructs exact recursive width-five Barrington AND_n words for n=2,4,8,16, comparing outputs to AND on all n<=8 inputs and targeted n=16 inputs. It also computes the canonical A5 profile rank for those words and confirms the k>=n/4 lower bound.

Relevant established literature:
- Barrington, *Bounded Width Branching Programs*, JCSS 1989, https://doi.org/10.1016/0022-0000(89)90037-8 .
- Idziak, Kawałek, Krzaczkowski, *Nonuniform Deterministic Finite Automata over Finite Algebraic Structures*, ICALP 2025, https://doi.org/10.4230/LIPIcs.ICALP.2025.161 (group ProgramSat and identity-checking context).
- Lee and Viola, *Pseudorandom bits for non-commutative programs*, ECCC TR25-071 rev July 2026, https://eccc.weizmann.ac.il/report/2025/071/ (relevant PRGs restricted to read-once products; they do NOT solve repeated-input A5 programs).
- Elementary symmetric function linear-size circuits and Hamming-count combinatorics, standard background.
