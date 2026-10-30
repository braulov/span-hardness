# Checkpoint 32 — Affine-group first sweep, width-three reversible SAT, and S3 exact-counting hardness

Date: 2026-10-30. Independently derived results and checks for the two-sweep BP-SAT program in span-hardness. Priority relative to previous literature remains unverified. This note supersedes an overly narrow focus on separable variable orders and low Fourier sparsity. Neither theorem yields an unrestricted 2^{o(p)} algorithm for polynomial-width branching programs or an NEXP circuit lower bound.

## Model

A two-sweep deterministic oblivious BP on p PRIMARY binary variables first reads x_1,...,x_p and then reads each variable once in an arbitrary order sigma. The first pass has a distinguished start and some possible middle states; the second pass may have ANY deterministic, including irreversible, transitions. For some theorems the first pass is the action of a fixed subgroup of permutations on its state set, potentially extended trivially to auxiliary state coordinates. Satisfiability asks whether ANY primary assignment causes acceptance. Exact counting asks how many primary assignments accept.

## 1. AGL(1,q) affine first sweep: deterministic SAT and witnesses in p^{O(q)}

Let K=F_q, q a prime power. Let first-pass transitions be invertible affine maps

    z -> a_i(b) z + t_i(b),   a_i(b) in K*, t_i(b) in K

for each bit b∈{0,1}; the first-pass initial point is z0∈K. After the first pass,

    F(x) = z0 Π_{i=1}^p a_i(x_i)
           + Σ_{i=1}^p t_i(x_i) Π_{j=i+1}^p a_j(x_j).

Thus F is a sum of p+1 PRODUCTS OF UNIVARIATE BIT FUNCTIONS over K. For each target s∈K the indicator equals

    f_s(x)=[F(x)=s]=1−(F(x)−s)^{q−1},

because z^{q−1}=1 for z∈K*. Add the constant-1 product as a base term. The above expression lies in the linear span of the (q−1)-fold products, with repetition, of p+2 base separable terms and the constant-1 function. By commutativity of scalar multiplication, a shared explicit product-feature list of dimension at most

    M = 1 + binom(p+q, q−1)

suffices for ALL s. Each product feature Φ_j(x) has the form Π_i h_{i,j}(x_i), over K, and each h_{i,j} is efficiently given.

The relative hitting-set lemma of checkpoint 30/31: for any read-once BP H, in any order, propagate a GAUSSIAN BASIS of concrete reachable partial feature vectors Φ via the diagonal linear maps diag(h_{i,j}(b)). Retain actual assignment witnesses at each state. At the end there are at most M ACTUAL accepted assignments K_H such that every linear functional of Φ nonzero at some accepted assignment is also nonzero at some element of K_H. Construct K_s for second-pass started at each s, run the REAL first sweep on every element of K_s, and accept iff some candidate ends at s. This is deterministic, produces an actual satisfying primary assignment, and takes poly(p,q,w,M) = p^{O(q)}poly(p,q,w), regardless of second-pass read order and transition maps. If q log p=o(p) and w=poly(p), the runtime is 2^{o(p)}poly(p,w).

Special case q=3: AGL(1,3)=S3 is the FULL three-state permutation group. Consequently any reversible first sweep of width THREE is tractable against an arbitrary second read-once sweep of polynomial width. For an arbitrary permutation action of a subgroup of S3 on a larger state set, output-state indicators are unions of at most six group-element predicates, also of polynomial separable rank, so the theorem extends to the subgroup action on (e.g.) a product state register.

This SAT result is NOT an exact integer #counting algorithm; Gaussian span compression loses multiplicities.

## 2. Strict separation from older criteria at q=5

Take p=2k and first-pass order x_1,y_1,x_2,y_2,...,x_k,y_k, with operations (bit zero is identity):
   x_i=1 -> scale z->2z in F5;
   y_i=1 -> translate z->z+1 in F5.
Start at z0=1 and distinguish final output 1.

Each scaling fails to commute with each translation. The first-pass noncommutation graph is K_{k,k}, whose minimum vertex cover has size k.

Choose second-pass order as the parallel-alternation simple permutation

   sigma=(2,4,...,2k, 1,3,...,2k−1).

The substitution decomposition has a single prime root of arity p, and the deletion distance to separable permutations equals k−1 (see checkpoint 24). Consequently prime arity, deletion distance, and noncommutation vertex-cover parameters are all Θ(p).

The F5 Fourier-support size can also be exponential. Restrict all translation bits y to zero. The endpoint predicate becomes

   h(x)=[Σ_i x_i = 0 (mod 4)].

For every ODD k all 2^k Walsh coefficients of h over F5 are NONZERO. A short proof: choose primitive 4th root 2∈F5. For Walsh-character index subset S, |S|=s, the UNNORMALIZED Walsh coefficient times 4 is

  C_{k,s} = Σ_{j=0}^3 (1−2^j)^s(1+2^j)^{k−s} (mod 5).

For 1≤s≤k−1, the j=0 and j=2 terms vanish, leaving

    C_{k,s}=(-1)^k(2^{k−s}+2^s).

It vanishes iff 2^{k−2s}=−1=2², impossible when k is odd (the exponent k−2s is odd mod4). At s=0 and s=k the sum similarly equals ±1 modulo5, and is nonzero. Restricting coordinates of a character expansion cannot INCREASE its support, hence the full first-pass endpoint predicate has at least 2^k=2^{p/2} nonzero F5 Walsh characters. Thus checkpoint 31's Fourier-sparsity parameter can be exponential.

The F2 multilinear algebraic degree of endpoint predicates can be linear. Restrict all scaling bits x to zero, obtaining

    g(y)=[Σ_i y_i =0 (mod5)].

Take k=2^{4t}+1, t≥1. The coefficient of the full degree-k monomial in the F2 ANF is Σ_{j≡0 mod5} binom(k,j) mod2. Lucas theorem makes binom(k,j) odd only at j∈{0,1,2^{4t},2^{4t}+1}; among these, only j=0 is divisible by5, because 2^{4t}≡1 mod5. Thus the coefficient is 1 and deg_F2(g)=k. Degree of full f(x,y) is at least degree of its restriction, so checkpoint 30's low-degree criterion is also exponential.

Despite all these bad parameters, p+2 term scalar separable decomposition yields M=1+binom(p+5,4)=O(p⁴), hence deterministic polynomial-time SAT/witness search against ANY second-pass read-once BP. This is a genuine separation of structural sufficient conditions, although not a complexity-class separation.

## 3. Counting barrier already within the smallest nonabelian group S3

We strengthen checkpoint 29's #P-hard UT4 counting construction.

Let A=(12), B=(23), C=(12) in S3. Adopt commutator [g,h]=ghg^{-1}h^{-1}. Put r=[A,B], a 3-cycle. Because C conjugates r to r^{-1},

    [[A^a,B^b], C^c]=r^{2abc},  for a,b,c∈{0,1}.

One 10-letter word expanding the LHS is (all A,B,C involutions)

    A^a B^b A^a B^b C^c B^b A^a B^b A^a C^c.

The word's inverse, using the same control bits on the appropriate reversed letters, realizes r^{abc} instead of r^{2abc}. We explicitly checked all eight input triples by permutation multiplication.

Take any 2-CNF F=∧_{j=1}^m (ℓ_{j,1}∨ℓ_{j,2}) on n original input bits, with m≥1; assume all n original bits appear, or account for unused bits by a known power of two. Let a_j(x),b_j(x) be the FALSE indicators of its two literals. Introduce a selector y_j∈F3, represented by two Boolean bits u_j,v_j with VALID encodings 00,10,01 and invalid 11. Place two commutator gadgets for clause j:
  * one controlled by (a_j,b_j,u_j), giving r^{2a_jb_j u_j};
  * the INVERSE controlled by (a_j,b_j,v_j), giving r^{a_jb_j v_j}.

For valid selector codes, the exponent 2u_j+v_j ranges exactly over F3. Thus the entire first sweep outputs r^{Σ_j (2u_j+v_j)a_jb_j}; all clause factors lie in the abelian 3-cycle subgroup and commute.

IMPORTANT COPY CONSTRUCTION: Each letter of each gadget reads a DIFFERENT PRIMARY Boolean bit. A letter whose logical argument is x_i or selector u_j/v_j is controlled by its own occurrence-copy input. For signed source literals, which bit value activates a generator is chosen according to literal falsity. So all first-sweep transitions are permutations from one fixed copy of S3, and the first sweep reads EVERY occurrence-copy input exactly ONCE.

The second sweep reads those same occurrence-copy bits ONCE EACH, but groups them by their original source bit. A fixed-width comparator verifies that all copies of a source x_i (or u_j/v_j) are equal and rejects forbidden selector code 11. Group start/end positions and selector-pair boundaries are known in the oblivious second-sweep instruction sequence, so a deterministic checker needs only FIVE states: four for retaining at most the preceding selector bit and the currently checked bit, plus an absorbing dead state. It ignores the group register. The first sweep ignores the checker register. Their Cartesian product is a fixed-width 3×5=15 state BP. The final acceptance requires the checker to be alive and the first-sweep 3-state register to have returned to its start; a nonidentity 3-cycle moves that start, so this enforces the exponent=0 mod3.

Every assignment to the n original source bits and the m ternary selectors has exactly ONE valid consistent assignment to the occurrence copies. If original x satisfies F, all 3^m selectors give exponent zero. If it violates any clause, the exponent is a nonzero linear functional of the F3 selector vector and therefore exactly 3^{m−1} selectors yield zero. Hence

   #BP_F = 3^{m−1}(2^n + 2·#SAT(F)),
   #SAT(F) = ( #BP_F/3^{m−1}−2^n ) /2.

This is a linear-size POLYNOMIAL-TIME METRIC/ARITHMETIC REDUCTION from #2SAT to exact #accepted-PRIMARY-input counting for fixed-width two-sweep BPs with first-sweep group S3 and second sweep a constant-width equality/validity checker. #2SAT is #P-complete. Thus exact counting is #P-hard in this restricted class and belongs to #P. This is NOT a parsimonious reduction, nor a result about SAT decision hardness.

The earlier polynomial SAT theorem extends to this product-state action, since the first-sweep transformations are from a six-element group S3 acting on the 3-state factor, identity on the checker factor. Thus in one fixed width-15 class we have **deterministic polynomial SAT but #P-hard exact counting**, unless FP=#P.

## 4. Explicit checks

- Random 200 affine-first/second programs over F3 and 32 analogous programs over F5; an independently implemented product-feature relative hitting-set DP found an accepting witness iff exhaustive 2^p enumeration did (p≤7 for q3, p≤5 for q5).
- The nested S3 commutator identity was checked on ALL 8 triples (a,b,c).
- 300 random 2-CNF source examples (n≤5,m≤5) were counted by enumerating valid ternary selectors and actual S3 gadget outputs, then compared to 3^{m−1}(2^n+2#F); every identity matched.
- The explicit 20-letter gadget for one binary clause was checked at the occurrence-copy level: 8 copies for each literal and two copies per selector bit, with exactly 10 accepting consistent assignments in the example x∨y. Inputs with inconsistent copies are rejected by the second verifier by construction.
- Walsh-support sizes over F5 for odd k=5,7,9,11 were 2^k, as the root-of-unity proof predicts.
- Random 5-state examples with alternating scale/translation exhibited F2 ANF degree up to p and near-full F5 Fourier support, despite p^{O(1)} product-feature dimension. These are checks, not proof necessities.

## 5. Context and cautions

S3 polynomial-time PolSat is known (Földvári–Horváth and extensions; see Idziak et al.), but the first-sweep S3 + arbitrary second deterministic ROBP INTERSECTION problem studied here is a specific different model. Do NOT claim a new result without a full novelty audit.

References:
- Idziak, Kawałek, Krzaczkowski, Weiß (ICALP 2022), https://doi.org/10.4230/LIPIcs.ICALP.2022.127
- Equation Satisfiability in Solvable Groups (Theory Comput. Syst. 2024), https://doi.org/10.1007/s00224-022-10082-z
- Valiant, The Complexity of Enumeration and Reliability Problems (1979), https://doi.org/10.1137/0208032
- Seto & Teruyama, exact read-twice oblivious BP-SAT (2016), https://doi.org/10.1587/transfun.E99.A.1019
- Prior checkpoints docs/30_lowdegree_feature_span_deterministic_sat.md and docs/31_fourier_product_features_width2_threshold.md

## 6. Main research lesson

The right input-efficient sufficient condition is not low F2 degree, low Fourier support, low commutator rank, or small substitution nodes separately. It is an efficiently constructible family of separable PRODUCT FEATURES that spans the first-pass endpoint predicates, and thus admits diagonal updates in ANY second-pass read order. Affine first sweeps over F_q provide a large NONNILPOTENT example with p^{O(q)} features. The hardness construction shows that integer multiplicities can remain #P-hard even when Boolean satisfiability is polynomial. Extending compact features to substantially wider, genuinely arbitrary first-pass transition monoids remains open. Any lower-bound implication toward NEXP notsubseteq L/poly still requires a universal algorithm for arbitrary polynomial-width read-many branching programs, not merely the two-sweep or affine subclasses.

## 7. Audit addenda: what is truly stronger and what is not

The q=3 (S3) case was ALREADY COVERED by checkpoint 31's low-F3-Fourier-sparsity algorithm: in F3 each factor a_i(x_i)∈{±1} is a constant times a parity character, and b_i(x_i) is a linear combination of TWO parity characters. Thus F(x) has at most O(p) nonzero Fourier characters, and its quadratic indicator 1−(F−s)^2 has at most O(p²). The new affine proof gives a simpler and more structural explanation for q=3, not a disjoint algorithmic regime.

For q=5, in contrast, affine scaling factors a_i(x_i) can be 1 or 2, which are not ±1, so ONE product term can have exponentially many Walsh frequencies over F5. The strict scale/translation family in Section 2 therefore GENUINELY extends the prior Fourier-sparsity bound as well as low-F2-degree, commutation, and permutation-order criteria.

The #P reduction has now been checked end-to-end for one clause with two source variables and a trit selector: all 2^20 assignments to 20 individual occurrence-copy bits were enumerated. Exactly 12 were consistent and selector-valid, and exactly 10 also returned the S3 register to its initial state, agreeing with #BP=3^0(2²+2·3)=10. A reusable standard-library test is scripts/check_affine_s3_hardness.py, which also checks the nested commutator on all 8 triples and 300 randomized source #2CNFs.

A useful related reduction (not a claimed new theorem): Any Boolean finite-group ProgramSat instance W(x) with T occurrences can be converted to a two-sweep instance with T PRIMARY occurrence-copy bits, first-sweep permutation transitions implementing the word, and a constant-width second sweep checking equality among occurrences of each source bit. It is a linear-size decision reduction; for exact counting, each valid original input corresponds to a unique copy assignment. This means the two-sweep model contains the GROUP-PROGRAM satisfiability problem as a syntactically restricted case. However the parameter p for the target two-sweep problem equals T (number of occurrences), not the original number of source bits; do not use this as an automatic input-efficient fine-grained reduction.

Natural next mathematical boundary: the first-sweep subgroup S4 (solvable but not AGL(1,3)), or variable-size affine groups with q comparable to p. Prior PolSat/ProgramSat group results should be studied carefully, as the problems are NOT identical and ETH-based hardness conclusions need revision if ETH has been refuted. Do not claim that S4 is NP-hard in the current model without proof.
