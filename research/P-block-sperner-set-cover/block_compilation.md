# P — Block-local BP → small-universe Set Cover via optimal consistency codes

2026-10-28. **Status:** a proved, explicit polynomial-time reduction for a structural subclass of polynomial-length branching programs. It does **not** solve the unrestricted LGS(p,S) → Set Cover(u=O(p)) objective. No literature novelty or peer review is claimed. Inherits prior LGS checkpoints through research/O-LGS-to-set-cover.

## 1. Model and parameters

A deterministic layered branching program (BP) has p Boolean inputs, L transition layers, at most w states in each layer, a designated start state and a set of accepting final states. Each state transition at each layer queries one of the p bits and chooses one of two successor states (the query may depend on the state). Layering is without loss at polynomial overhead but the resulting L must be counted.

Partition the L successive layers into B nonempty **consecutive** blocks, indexed j=1,...,B. Let I_j ⊆[p] be the set of *distinct* variables queried anywhere in block j, across all its states, and d_j=|I_j|. Let

    H = sum_j d_j = sum_i r_i,
    r_i = number of blocks in which x_i appears.

No constraint on the number of repeated reads of a variable *within* one block. Let p_used be the number of input bits that occur in any block.

Define

    q(w) = min{q >= 0 : binomial(q, floor(q/2)) >= w}.

For w=5, q(w)=4. For w=1 we may take q=0. For w>=2, q(w)=log_2 w+O(log log w).

## 2. Main theorem: explicit Set Cover reduction

**Theorem P1.** In deterministic time polynomial in S=Lw+p and in the number of generated candidate sets, one can construct an ordinary unweighted Set Cover instance with

    universe size u = p+B+H+p_used + q(w)*(B-1),
    budget k=p+B,
    number of candidate sets t <= 2p + w * sum_j 2^{d_j},

such that the BP has an accepting input iff there is a cover of size <=k.

Consequently, if w=O(1), B+H=O(p), and max_j d_j=O(log p), the reduction is polynomial time, has u=O(p) and t=p^{O(1)}, **even for original length L=p^100** (or any other fixed polynomial in p). This is a structural-class implication, not a universal BP-SAT completeness result.

### 2a. Candidate-set groups and forcing exact selection

Create p groups X_i with two candidate sets X_{i,0} and X_{i,1}, corresponding to global input bits.

Create B groups T_j. For every assignment a∈{0,1}^{I_j} and every possible entry state s∈[w], simulate the block under a to compute its uniquely determined exit state e=T_{j,a}(s). Add one candidate set T_{j,a,s,e}. Discard first-block candidates with s different from the BP's fixed start state and last-block candidates with e not accepting.

Give every group g a distinct private universe element d_g, covered by **all sets of group g and no others**. Since there are p+B groups and budget k=p+B, a covering family must select exactly one set from every group.

The only remaining issue is ensuring that all block-local choices agree with the global bit choices, and that consecutive exit/entry states coincide.

### 2b. Optimal cyclic implication code for repeated-variable consistency

For each used variable i, let its r_i local copies be associated with the r_i blocks where it appears; together with the global bit X_i there are n_i=r_i+1 distinct group-chosen Boolean values.

Arrange these n_i groups in a directed cycle. For every directed arc a→b introduce **one universe element** e_{a→b}, covered exactly when the selected set for a chooses 0 **or** the selected set for b chooses 1. Equivalently, this enforces the clause

    (not value_a) OR value_b.

All elements of the directed cycle are covered iff there is no directed 1→0 transition around the cycle. A finite cyclic binary word without 1→0 transitions is constant, so all copies and the master bit agree.

Cost: exactly r_i+1 universe elements. Total across all inputs: H+p_used.

**Optimality in the natural pure equality gadget model.** Let n independent groups each choose exactly one of sets S_{j,0} and S_{j,1}; demand coverage iff all chosen bits are equal. Consider all-zero choices and, for each j, the assignment which flips ONLY group j to one. The all-zero selection covers the universe, each single-flip selection fails. A universe element that becomes uncovered on single flip j must be covered by S_{j,0} and by none of the other all-zero chosen sets. The same element cannot become uncovered for any single flip k≠j, because S_{j,0} remains chosen there. Hence at least n distinct universe elements are necessary; the directed-cycle construction uses exactly n and is optimal. This lower bound applies only to this exact-one-group coverage representation of pure equality, not to all possible extended Set Cover encodings for arbitrary BP acceptance.

### 2c. Optimal Sperner-antichain code for finite-state equality

For each boundary between blocks j and j+1, pick w pairwise incomparable sets C_1,...,C_w ⊆[q(w)], each of cardinality floor(q(w)/2). Existence follows from the central binomial coefficient.

Introduce q(w) universe elements for that boundary.

A candidate for block j with *exit* state s covers the complement [q]\C_s on that boundary. A candidate for block j+1 with *entry* state t covers the elements of C_t. The entire boundary universe is covered iff

    ([q]\C_s) ∪ C_t = [q]  iff  C_s ⊆ C_t  iff  s=t,

where the last iff is antichain incomparability.

Cost: q(w) universe elements per boundary; total q(w)*(B-1).

**Optimality for two categorical groups.** Suppose a universe U of q elements and set choices L_s,R_t (s,t∈[w]) achieve full coverage exactly when s=t. Put M_s=U\L_s. The equality case requires M_s⊆R_s. The nonequality case s≠t requires M_s ⊄ R_t, and since M_t⊆R_t this implies M_s ⊄ M_t. Thus {M_s} is an antichain of size w in 2^U. By Sperner's theorem w ≤ binomial(q, floor(q/2)). Our construction attains the bound.

This is a local gadget optimality statement, not a lower bound on general BP-to-Set-Cover reductions.

### 2d. Proof of correctness and construction cost

A BP accepting input x determines exactly one choice X_{i,x_i} per bit, exactly one local assignment a_j=x|_{I_j}, and a coherent sequence of BP boundary states. Select these candidate sets. The private elements, variable-cycle elements and state-boundary elements are all covered.

Conversely any cover with at most p+B sets chooses exactly one set from each group. Every variable-cycle is fully covered, hence all local copies agree with their global bit; every state-boundary is fully covered, hence the selected block transitions concatenate into a genuine run on that global input. First start and last acceptance restrictions imply the run accepts.

For each block, enumerating 2^{d_j} local assignments and simulating w possible entries takes O(w L_j 2^{d_j}) elementary steps. Candidate sets are constructed by iterating over O(d_j+q(w)) consistency-elements plus one private element. Thus the construction is polynomial in the input and output size when max d_j=O(log p), B and w polynomially bounded; in the desired w=5 regime, t<=2p+5B p^{O(1)}. The universe count is exactly p+B+(H+p_used)+q(w)(B-1).

## 3. Concrete quadratic-length example

Let p=16, w=5, L=256, B=4, with 64 transition layers in each block. Suppose each block queries only 4 distinct switches, and the four support sets partition the 16 global inputs. Each input may be queried many times inside its 64-layer block.

Then H=16, p_used=16, q(5)=4, so

    u=16+4+16+16+4*3=64;
    k=16+4=20;
    t<=2*16 + 5*4*2^4 = 352.

Thus 256 transition layers can be compiled into a Set Cover instance of universe 64 and at most 352 sets. These precise constants are an illustration, not a hardness claim. If variables occur in two blocks on average, H=32 and u=80.

More generally for L=p², take B≈p/log p blocks of length ≈p log p. If every block reads at most C log p distinct variables (allowing arbitrarily many rereads), then H<=C p and u=O(p), with t polynomial in p.

## 4. Subexponential Turing-reduction extension by exceptional switches

Fix a set F of k exceptional input variables. Enumerate their 2^k possible Boolean assignments and simplify every transition, obtaining 2^k residual BPs. Suppose each residual BP admits a block decomposition with B+H'=O(p) and max_j |I_j\F|=O(log p), with width w=O(1). Then each residual instance reduces in polynomial time to Set Cover with universe O(p) and polynomially many sets. The entire transformation is deterministic and costs 2^k poly(S) plus Set Cover oracle calls. In particular k=o(p) produces a SERF-style 2^{o(p)}-instance reduction for such almost-block-local programs.

This does **not** show that every polynomial-size BP has a small exceptional set, or that all polynomial-size BP-SAT can be reduced to Set Cover with O(p) universe. The source's *total block-variable incidence* H remains the technical bottleneck.

## 5. Why naive consistency batching fundamentally pays Omega(H)

Theorem P1 uses H+p_used universe elements for variable consistency. The optimality proof in §2b shows that, in an exact-one-choice **independent bit-copy group** encoding, Omega(H) elements are unavoidable: each single flipped occurrence relative to the globally consistent all-zero assignment requires its own distinct uncovered universe element.

It does **not** follow that every possible BP-to-SetCover reduction must use Omega(H) universe. Such a sweeping lower bound would require new complexity/circuit methods, potentially allowing auxiliary global candidate choices, many-instance reductions, or structure in transition matrices.

Research direction: replace explicit copy-by-copy consistency with a stronger algebraic/batched certificate using O(p) Set Cover elements, without introducing Theta(H) uncoordinated auxiliary choices. Even probabilistic fingerprints need a faithful *coverability* (OR-of-set-memberships) realization and rigorous soundness.

## 6. Tests, audit, and next experiments

- Independently constructed a Python verifier for the cyclic consistency code and the Sperner state code.
- Ran 650 seeded random layered deterministic BPs (p=1..3, w=2..5, length=1..6, random consecutive block partitions). Exhaustively compared original BP acceptance with Set Cover covering under the one-set-per-group budget. All passed.
- Enumerated state code pairs for every w=2..21; antichain coverage iff equal in every case, all passed.
- A simpler two-elements-per-incidence / two-per-state-bit implementation was independently tested on 320 random BPs; all passed.

Tests supplement and do not replace the proofs. No general LGS(p,S) -> Set Cover(O(p)) reduction has been established; no claim to have proved NEXP not in L/poly.

### Immediate next questions

1. Can the variable-block incidence H be compressed below linear in the canonical set-choice gadget by **adding a small number of auxiliary global groups**, not merely changing the local coverage pattern?
2. Find a structurally meaningful class with H≫p but still polynomial-time reducible to Set Cover universe O(p), beyond the obvious constant-width commuting-permutation case.
3. Attempt a 2^{o(p)}-time branching/instance-splitting lemma reducing arbitrary width-five polynomial-length group programs to 2^{o(p)} block-local instances. Any claim needs actual time and count accounting.
4. Compare with known CSP-to-SetCover and LabelCover-to-SetCover constructions before claiming novelty.

References: Sperner's theorem (central binomial antichain bound); classical CNF/constraint consistency reductions to Set Cover; width-five group programs via Barrington's theorem; user project branch O.
