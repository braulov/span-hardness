# U — Hidden symmetry: an optimal universal query basis for exact BP-SAT

Checkpoint: 2026-10-28. **Main result:** deterministic, exact #SAT for arbitrary polynomial-size branching programs whose Boolean function is invariant under permuting all but b **unknown** input variables, using at most \((p+1)\binom p b\) membership queries for \(b\le p/2\), followed by \(2^{O(b\log(p/b))}\operatorname{poly}(p,S)\) arithmetic. It also supplies a constructive *promise* learning procedure recovering some suitable exceptional-coordinate set and, for b=O(1), a Set Cover compilation with universe O(p). **Important:** This is a promise-based structural theorem, not a general BP-SAT/LGS algorithm, and the promise is coNP-hard to verify in general. No claim that the underlying slice interpolation techniques are novel: compare classical inclusion-matrix ranks and Johnson-scheme harmonic analysis (Filmus 2016, cited below). Branch inherits T/S/R/... and does not change main.

## 1. Setup and a sharper structural promise

Let f:{0,1}^p -> {0,1} be given by a deterministic polynomial-size BP (evaluation takes poly(S)). For 0<=w<=p let \(\Omega_{p,w}=\{x:|x|=w\}\).

**Slice degree ≤b promise** \((\mathrm{SLD}_b)\): for every w, the restriction \(f|_{\Omega_{p,w}}\) is representable by a multilinear polynomial \(P_w(x)\) over Q of total degree ≤b (the polynomial can depend on w).

This is stronger algorithmically and broader than the *hidden b-exception symmetry* promise \(f(x)=g(x_B,|x_{\overline B}|)\) for some UNKNOWN B⊆[p], |B|≤b: on each fixed-weight slice, the function depends only on coordinates B and is a multilinear polynomial in those |B| bits of degree ≤b. It also covers sums/combinations of such functions with different B (if the output is Boolean), as long as their slice degrees are ≤b.

The degree promise is semantic and is NOT claimed efficiently recognizable from general BPs. All algorithms below are *unconditionally correct for inputs satisfying the promise*, but could silently give wrong results if the promise fails. Acceptance of a genuine witness is always sound, irrespective of the promise.

## 2. A universal, optimally sized interpolation set on each Hamming slice

Fix once and for all the coordinate order 1,...,p. Define the length-t prefix string \(s_t=1^t0^{p-t}\), t=0,...,p.

For d≥0, define

\[
Q_{p,d}=\{x\in\{0,1\}^p:\min_{0\le t\le p}\mathrm{Ham}(x,s_t)\le d\}.
\]

On layer w, let \(Q_{p,w,d}=Q_{p,d}\cap\Omega_{p,w}\). Write \(e=\min(d,w,p-w)\).

**Theorem U1 (slice interpolation / optimal point basis).**

(a) \(|Q_{p,w,d}|=\binom p e\).

(b) Evaluation on \(Q_{p,w,d}\) is a linear isomorphism from the space \(V_{p,w,d}\) of degree-≤d polynomial functions on the w-slice to \(\mathbb Q^{Q_{p,w,d}}\). In particular, every polynomial of degree≤d on the slice is UNIQUELY DETERMINED, as a function on that slice, by its values at precisely \(\binom p e\) canonical points.

(c) The matrix of evaluations of the square-free monomials \(\prod_{i\in T}x_i\) for all |T|=e, with rows Q_{p,w,d}, is a nonsingular \(\binom p e\times\binom p e\) matrix over Q.

The point count is thus optimal for recovering **all** degree-≤d functions on this slice by linear evaluations: the space has dimension exactly \(\binom p e\).

**Classical rank fact used.** Over Q, the inclusion matrix with rows the w-subsets and columns the e-subsets has full column rank \(\binom p e\) whenever e≤min(w,p-w). Equivalently \(\dim V_{p,w,d}=\binom p{\min(d,w,p-w)}\). This is the standard rank theorem for subset inclusion matrices (also follows from the harmonic basis of Boolean slices, Filmus, Electronic J. Combin. 2016); it is NOT asserted new here. Monomials of degree below e lie in the span of degree-e monomials on the weight-w slice because, for |A|≤e,

\[
\sum_{T\supseteq A,\ |T|=e} x_T = \binom{w-|A|}{e-|A|}x_A,
\]

and the binomial factor is nonzero when w≥e.

**Inductive proof of U1 (including exact cardinality).** If d≥min(w,p-w), Q contains the entire w-slice: every x is within w flips of s_0=0^p and within p-w flips of s_p=1^p. The claim follows because e=min(w,p-w) and the polynomial functions of that degree span ALL functions on the w-slice.

Suppose 0≤d<min(w,p-w). We split a weight-w input x according to its final bit x_p.

- If x_p=0, the closest prefix has t≤p−1, as the all-ones prefix s_p is at distance p-w>d. Thus the permitted first p−1 bits are EXACTLY \(Q_{p-1,w,d}\).
- If x_p=1, every prefix s_t with t≤p−1 has one mandatory final-bit mismatch, while s_p is at distance p-w>d. Thus the permitted first p−1 bits are EXACTLY \(Q_{p-1,w-1,d-1}\). For d=0 this set is empty, and the corresponding \(Q_{p,w,0}=\{s_w\}\) base case is immediate. For d≥1, both sets are defined.

For d≥1, inductive cardinalities and Pascal's identity give

\[
|Q_{p,w,d}|=\binom{p-1}{d}+\binom{p-1}{d-1}=\binom p d.
\]

For injectivity, let f∈V_{p,w,d} vanish on Q. First its x_p=0 restriction lies in V_{p-1,w,d}, and vanishes on Q_{p-1,w,d}, so by induction it vanishes throughout the x_p=0 slice. The linear restriction map \(R_0:V_{p,w,d}\to V_{p-1,w,d}\) is surjective (just use polynomials independent of x_p); the domain and range dimensions are \(\binom p d\) and \(\binom{p-1}d\), respectively, by the standard rank fact. Therefore its kernel has dimension \(\binom{p-1}{d-1}\).

Multiplication by x_p defines an injective map from \(V_{p-1,w-1,d-1}\) into this kernel; its dimension is the same \(\binom{p-1}{d-1}\). Hence the kernel is exactly \(x_p V_{p-1,w-1,d-1}\) on the combined w-slice. In particular the x_p=1 restriction of f has degree≤d−1. It vanishes on \(Q_{p-1,w-1,d-1}\), so by induction also on the entire x_p=1 slice. Thus f=0 throughout \(\Omega_{p,w}\). Combined with the point count/dimension equality, evaluation is an isomorphism. QED.

**Exact global query count.** If 0≤b≤p/2, the total number of query points is

\[
\boxed{|Q_{p,b}|=2\sum_{j=0}^{b-1}\binom pj +(p-2b+1)\binom pb \le (p+1)\binom pb .}
\]

For b=0, interpret the empty sum as 0; there are exactly p+1 prefix queries. For b≥floor(p/2), all 2^p points are queried. For b=o(p), \(\log_2|Q_{p,b}|=O(b\log(p/b)+\log p)=o(p)\).

(The cruder swap-ball scheme used during exploration queried \(\sum_j\binom{p+1}{2j+1}\) inputs; U1 reduces the exponent approximately by a factor of two and is optimal per slice.)

## 3. Exact counting and constructive SAT algorithm WITHOUT knowing exceptional coordinates

**Theorem U2.** Given BP f satisfying \(\mathrm{SLD}_b\), exact \(\#f^{-1}(1)\), BP-SAT and a witness are deterministic in

\[
\boxed{\binom pb^{O(1)}\operatorname{poly}(p,S)}
\]

for b≤p/2 (with the convention \(\binom p0=1\)). A simple explicit bound is \(O((p+1)\binom pb \cdot S+\operatorname{poly}(p)\binom pb^3)\) arithmetic operations over rationals with polynomial-bit-length numerators/denominators. In particular, if b=o(p) this is deterministic \(2^{o(p)}\operatorname{poly}(S)\), even when S=p^{100}. No exception set B is an algorithm input.

**Algorithm.** For every w, set e=min(b,w,p-w), let Q=Q_{p,w,b} and let \(\mathcal T=\binom{[p]}e\). Both have N=\(\binom pe\) members. Evaluate f on every x∈Q, recording vector y∈{0,1}^N. Build the square N×N inclusion matrix

\[
M_{x,T}=\prod_{i\in T}x_i=\mathbf 1[T\subseteq \mathrm{supp}(x)].
\]

Theorem U1 says M is invertible. Solve M c=y over Q. Under the promise, the degree-e polynomial \(P_w(x)=\sum_{|T|=e}c_T x_T\) agrees with f on the ENTIRE weight-w slice. Every degree-e monomial has exactly \(\binom{p-e}{w-e}\) satisfying weight-w assignments, so the exact number of acceptances at weight w is

\[
\boxed{N_w=\binom{p-e}{w-e}\sum_{|T|=e}c_T.}
\]

Sum over w. A YES witness is supplied by any queried x where f(x)=1: if f accepts somewhere, no slice's polynomial can be zero on the query set by U1, hence a queried acceptance exists.

All matrix entries are 0/1, all dimensions ≤binom(p,b). Fraction-free elimination or rational Gaussian elimination has polynomial bit complexity in p and matrix dimension (Hadamard bound on determinants of 0/1 matrices). This gives the asserted runtime. All output N_w are exact integers under the promise.

Notice that this uses only **evaluation queries of f**, not a symbolic manipulation of the input BP. It is a genuine *black-box exact-counting algorithm for the promised class*.

## 4. Recovering SOME unknown exception set and O(p)-universe Set Cover for fixed b

**Theorem U3 (promise representation discovery).** Suppose f is known to have some unknown exceptional set B of size ≤b such that f(x)=g(x_B,|x_{\overline B}|). Then one can deterministically find such an exceptional set B' of size exactly b, together with its complete truth table g', in

\[
\binom pb \cdot 2^b(p+1)\cdot |Q_{p,b}|\cdot\operatorname{poly}(S,p)
=2^{O(b\log(p/b)+\log p)}\operatorname{poly}(S)
\]

for b≤p/2 (a deliberately loose upper bound). This is polynomial time for fixed b, and \(2^{o(p)}\mathrm{poly}(S)\) for b=o(p).

Algorithm: enumerate candidate B'⊂[p] of size b. For each z∈{0,1}^{B'} and k∈{0,...,p-b}, evaluate f on the canonical input with B' bits z and the first k variables outside B' set to 1, thereby defining a candidate function

    h_{B'}(x)=g'(x_{B'},|x_{outside B'}|).

Compare h_{B'} with f on the entire universal query set Q_{p,b}. If all values match, ACCEPT B' and its table. The actual exceptional B (extended arbitrarily to size b) passes. Moreover both f and h_{B'} have slice degree≤b; by U1, agreement on Q implies global equality. Hence any accepted candidate is globally correct, *assuming the original hidden-exception promise*. No coNP equivalence oracle is used.

For any **constant** b, construct a circuit for h_{B'} by (i) O(p)-gate carry-save Hamming-weight computation outside B'; (ii) O(p)-gate one-hot decoding of the weight; (iii) a 2^b-by-(p-b+1) truth-table multiplexer using O(2^b p) gates. Total size O(2^b p). Standard Tseitin and CNF→SetCover give a pointwise reduction with universe u=O(2^b p)=O(p) and O(p) candidate sets for each fixed b. Unlike branch T, **B need not be provided**.

**Crucial qualification:** this is a reduction for a promised class. On arbitrary BPs not satisfying the promise, the finite query comparison may validate a WRONG candidate h. We DO NOT assert a sound general BP-SAT → Set Cover reduction or a polynomial-time semantic-symmetry verifier. Indeed T proved that checking even one swap invariance is coNP-complete.

## 5. Near-optimality in the black-box membership-query model

**Theorem U4 (membership-query lower bound).** Any deterministic algorithm that distinguishes f≡0 from promised hidden-b-exception functions with a satisfying assignment requires at least \(\binom pb\) evaluations in the worst case, for 0≤b≤p.

Proof: for each b-subset B⊂[p], consider the point indicator

\[
f_B(x)=\mathbf 1[x=\mathbf 1_B],
\]

where \(\mathbf 1_B\) has ones precisely on B. The function f_B is symmetric on the outside p-b coordinates (it accepts only when ALL outside bits are 0), so it belongs to the promised class with |B|=b. On any query x other than \(\mathbf1_B\), f_B(x)=0. Thus to distinguish all such f_B from the identically zero function on the all-zero answer path, the algorithm must query every one of the \(\binom pb\) candidates. QED.

For b≤p/2 the U1 query set has size at most \((p+1)\binom pb\): optimal up to a factor p+1 in this black-box decision setting. In particular, the exponent \(b\log(p/b)\) for small b cannot be improved in general merely by a cleverer selection of membership queries.

This lower bound applies to algorithms that access f ONLY by evaluation queries. A structural algorithm that reads the BP source can sometimes identify B or exploit its syntax much more quickly (e.g. the point-indicator BP exposes its own target).

## 6. A striking b=1 shortcut: cyclic-shift quadrature

When f is symmetric outside ONE unknown input position, exact counting needs only p(p+1) evaluations, with the beautifully simple integer formula

\[
\boxed{
\#f^{-1}(1)
=\frac1p\sum_{w=0}^p\binom pw
  \sum_{t=0}^{p-1} f(\operatorname{rot}_t(1^w0^{p-w})).
}
\]

Proof: within the weight-w slice, the value of f depends only on whether the unknown distinguished bit i equals 0 or 1. Uniform cyclic rotation of s_w makes that bit equal to one in exactly w of the p rotations, the same hypergeometric probability as in the complete weight-w slice. Thus the orbit average equals the slice average. The identity holds for EVERY choice of the unknown i, with no identification of i. QED.

For p=1 interpret the formula trivially. This is a special case of exact quadrature/designs on the Johnson scheme; not claimed novel.

## 7. Scope, experimental audit, and relation to post-ETH goals

- The initial exchange-ball rational interpolation algorithm was independently checked on 315 small random instances, p≤9.
- The much smaller **prefix Hamming-ball** evaluation matrices were confirmed full rank with the predicted exact cardinalities for all p≤8 and b≤3 and every weight, over Q. The exact theorem follows from the induction in §2, not from tests.
- Hidden exceptional-set recovery using these universal evaluations was independently checked on 225 random promised functions, p≤9, b≤3, with exhaustive comparison of the recovered function on the entire Boolean cube.
- A reproducible source test for U1/U2/U3 is supplied in this branch.

**What we gained:** for the promised class of BPs invariant outside an *unknown* b-set, exact counting and SAT are deterministic subexponential whenever b=o(p); for constant b, a polynomial-time, pointwise O(p)-universe Set Cover reduction follows with the unknown set discovered. This is qualitatively stronger than T's "supplied symmetry partition" promise.

**What remains open:** finding a general efficient, SOUND (non-promise) BP-SAT or LGS algorithm exploiting unverified semantic candidate representations. U1–U4 do not imply unrestricted \(2^{o(p)}\) LGS-SAT, do not yield the desired general LGS→SetCover(u=O(p)) reduction, and do not prove NEXP not in L/poly. The known coNP-completeness of symmetry recognition (T) remains a barrier to upgrading this promise solver into a sound general preprocessing routine.

### Sources
- Filmus, *An Orthogonal Basis for Functions over a Slice of the Boolean Hypercube*, Electronic Journal of Combinatorics (2016), https://doi.org/10.37236/4567 .
- Filmus et al., *Harmonicity and Invariance on Slices of the Boolean Cube*, https://doi.org/10.1007/s00440-019-00900-w .
- Classical full-rank subset inclusion matrices over characteristic zero (Gottlieb rank theorem).
- Parent project: \`research/T-semantic-orbits/semantic_orbit_reduction_and_recognition_barrier.md\`.


## 8. Extension beyond a single hidden exceptional set: moving dictatorships

An instructive example with **no common small exceptional set** is

\[
f(x)=x_{|x|} \quad\text{for }|x|\ge1,\qquad f(0^p)=0,
\]

where indices are 1-based. On the weight-w slice it equals the single coordinate x_w, hence has slice degree one for EVERY w. However, the distinguished coordinate changes with w; the union of relevant coordinates over weights is \(\Omega(p)\), and there need not be one B of size o(p) making the whole function symmetric outside B. The U1/U2 exact-count algorithm still applies with b=1.

For this function, at each w≥1 the number of accepting weight-w inputs is \(\binom{p-1}{w-1}\), so the total count is \(\sum_{w=1}^p\binom{p-1}{w-1}=2^{p-1}\). Thus \(\mathrm{SLD}_b\) is a genuinely broader semantic condition than hidden b-exception symmetry.

### Theorem U5 (cyclic quadrature for ALL Boolean slice-degree-one functions)

The b=1 cyclic formula from §6 in fact holds for **every Boolean f satisfying \(\mathrm{SLD}_1\)**, even if a different relevant coordinate occurs at every Hamming weight.

Proof: on interior weight layers 2≤w≤p−2, a Boolean degree-one function on a Johnson slice is necessarily a constant, a dictator x_i, or its negation 1−x_i (the classical degree-one slice junta theorem; see Filmus–Ihringer 2019, Theorem 1.2). The cyclic rotations of s_w put coordinate i in state one for exactly w of the p rotations, so cyclic and full-slice averages agree for every such function. On extreme layers w∈{0,1,p−1,p}, cyclic shifts of s_w range over the ENTIRE layer (possibly with repetitions), so the averages agree for arbitrary Boolean functions. Summing layers proves the same p(p+1)-query formula for all \(\mathrm{SLD}_1\) Boolean functions, without any fixed B. QED.

Finite test: 250 seeded random families of independently chosen weight-by-weight dictators/negated dictators/constants, with arbitrary Boolean functions at the w=1 and w=p−1 extreme layers, p≤11; the cyclic formula matched full enumeration in every case.

## 9. A second group-design shortcut for degree two (prime number of inputs)

**Theorem U6 (affine quadrature).** Suppose p is prime and f has slice degree ≤2, with no hidden-B assumption and without requiring f to be Boolean for the identity. Let \(\pi_{a,c}(i)=ai+c\pmod p\) on index set F_p, for a∈F_p^× and c∈F_p. Then

\[
\boxed{
\sum_{x\in\{0,1\}^p} f(x)
= \frac1{p(p-1)}\sum_{w=0}^p\binom pw
    \sum_{a\ne0,\ c\in F_p} f(\pi_{a,c}\cdot s_w).
}
\]

There are \(p(p-1)(p+1)=O(p^3)\) evaluation queries.

Proof: AGL(1,p) acts **sharply two-transitively** on the p positions. Thus, for every weight-w base string and every fixed set T of at most two coordinate positions, the fraction of affine permutations sending all positions of T into the support of the permuted base equals (w)_{\underline{|T|}}/(p)_{\underline{|T|}}, exactly the average of the monomial x_T under the uniform weight-w slice. By linearity of expectation, the affine orbit average equals the full slice average for EVERY degree≤2 polynomial, proving the identity. QED.

This is a conventional 2-design / sharply 2-transitive group argument and is not asserted novel. It gives a particularly simple exact #BP-SAT formula under the \(\mathrm{SLD}_2\) promise for prime p, with almost the same number of queries as our information-theoretically minimal chain-neighborhood interpolation, but no Gaussian elimination. For arbitrary p, U1 remains valid unconditionally.
