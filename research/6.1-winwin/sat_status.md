# SAT status and a local-isolation bridge for span constraints

Date: 27 October 2026. This note distinguishes published claims, standard ingredients, and deductions proved here. No Lean build or independent verification of the October manuscripts was performed in this task.

## 1. What the October artifacts actually say

The primary artifacts are publicly accessible. OpenAI's [26 October announcement](https://openai.com/index/building-scientific-understanding-with-academic-communities/) calls its manuscript raw research data and describes an independent group led by Impagliazzo, Paturi, and Williams organizing examination. This is evidence of a public claim and an examination process, not of completed external validation.

OpenAI's [main TeX source](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex), dated 17 October and revised 25 October, states its main theorem as follows: for each fixed k >= 2, exact #k-CNF on n declared variables and m clauses takes

    (n+m)^{O_k(1)} 2^{O_k(n log log n / sqrt(log n))}

bit operations and polynomial space. For each fixed D with m <= Dn, its stronger bound is

    (n+m)^{O_{k,D}(1)} 2^{O_{k,D}(n / sqrt(log n))}.

Its earlier interpolation analysis gives exponent n(log log n)^2/sqrt(log n), still sublinear. Do not substitute the sharper manuscript bound for a separately audited formal statement.

Anthropic's current directory is [formal-math/eth](https://github.com/anthropics/formal-math/tree/main/eth), not the stale eth2h link appearing in initial secondary reporting. The [README](https://github.com/anthropics/formal-math/blob/main/eth/README.md) describes a 2^{o(n)} #3-SAT result and explicitly distinguishes machine checking a proof from checking that its statement matches the prose. Its [MainResults.lean](https://github.com/anthropics/formal-math/blob/main/eth/MainResults.lean) defines one finite-alphabet multitape-stack machine and one constant C, uniform in k, counting in time

    2^{C min{km/sqrt(log m), k^2 n log log n/sqrt(log n)}}.

The displayed formal scope assumes k >= 1, n >= 4, m >= 2, no duplicate clauses, and every declared variable occurring. Duplicate removal and accounting for unused variables are routine preprocessing; the scope should nevertheless be reported accurately.

The OpenAI manuscript already states an infinitely-often Omega(n sqrt(log n)) unrestricted fan-in-two circuit lower bound for a language in E^NP. Its [quantitative-circuits appendix](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/quantitative-circuits.tex) gives its Williams/Jahanjou-Miles-Viola witness argument. That particular consequence must not be advertised as a new result of this checkpoint.

All deductions below are conditional on the stated exact fixed-width #SAT algorithm being correct. Ordinary exact integer counts suffice; weighted counting and finite-field extensions are not assumed.

## 2. The crucial existing ingredient: linear-size pairwise-independent hashing

The useful source is Benny Applebaum, *Exponentially-Hard gap-CSP and local PRG via Local Hardcore Functions*, [ECCC TR17-063](https://eccc.weizmann.ac.il/report/2017/063/), [full text](https://eccc.weizmann.ac.il/report/2017/063/download), especially Theorem 2.3, Theorem 3.2, Remark 3.3, Claim 2.2, and Construction 4.4/Lemma 4.6. Theorem 2.3, attributed there to IKOS08/BIO14, supplies pairwise-independent hashes with input, output, key, and arithmetic-circuit size O(p). The arithmetic is over F_2, so after fixing the key the circuit has O(p) Boolean XOR/AND gates. This is substantially more efficient than the naive dense binary-matrix hash.

Only this hashing fact is needed below. The original unconditional [IKOS08 construction, Theorem 3.3](https://web.cs.ucla.edu/~rafail/PUBLIC/91.pdf) gives linear-size Boolean evaluation circuits; Applebaum's polynomial-time Local Isolation Lemma and Construction 4.4 make the uniform sampler explicit. The perfect randomized encoding in Theorem 3.2 provides an independent alternative implementation. We give the simple circuit implementation first and then specify the encoding alternative. The one-point domain p=0 is handled by directly checking its sole choice, rather than invoking hashing.

### Lemma 1 (local isolation of an arbitrary subset)

For p >= 1 there is a polynomial-time randomized sampler producing a 3-CNF H(x,a), with p distinguished variables x, O(p) auxiliary variables a and O(p) clauses, such that for every subset S of {0,1}^p:

1. For every x, at most one a satisfies H(x,a).
2. If S is nonempty, the probability that exactly one pair (x,a), x in S, satisfies H is at least 1/(8p).

The sampler does not need to know S or decide membership in it.

**Proof.** Choose s uniformly from {2,...,p+1}. Obtain a pairwise-independent hash family h_w:{0,1}^p -> {0,1}^s with O(p)-size binary arithmetic circuit from the cited theorem; its constants are uniform over this range of s by the linear output bound. Choose its key w uniformly, choose y uniformly from {0,1}^s, hardwire w, and apply the parsimonious gate-by-gate 3-CNF encoding to the equation h_w(x)=y. Every gate output is uniquely determined by x, proving (1). There are O(p) variables and clauses.

Fix nonempty S, let K=|S|, and select the favorable value

    s_* = max(2, ceil(log_2 K)+1).

It lies in {2,...,p+1}, including when K=1. Put Z=|{x in S:h_w(x)=y}| and lambda=K/2^{s_*}. For K>=2, lambda lies in [1/4,1/2]; for K=1 it equals 1/4. Pairwise independence gives

    E Z = lambda,
    E[Z(Z-1)] = K(K-1)/2^{2s_*} <= lambda^2.

For every nonnegative integer z, 1[z=1] >= z-z(z-1). Therefore

    Pr[Z=1] >= lambda-lambda^2 >= 3/16 >= 1/8.

Multiplying by Pr[s=s_*]=1/p proves (2). The singleton endpoint is handled explicitly because the paper's displayed ceil(log|S|)+1 value would equal 1, outside its sampled range beginning at 2. No substantive change to the isolation construction is needed. QED.

### The perfect-randomized-encoding implementation, if desired

For the chosen s,w, Applebaum's Theorem 3.2 supplies a 3-local perfect randomized encoding hat(h)_w(x;r) with rho=O(p) random bits and hat(s)=s+rho=O(p) output bits. Sample y uniformly, sample hat(y) using Sim_w(y), and require every coordinate of hat(h)_w(x;r)=hat(y). Each requirement is a Boolean constraint of arity <=3 and expands to at most eight width-three clauses, without additional variables.

For targets sampled from Sim_w(y) in a nonempty bucket, unique randomness gives, for **every subset S**,

    |{(x,r):x in S, hat(h)_w(x;r)=hat(y)}|
      = |S intersect h_w^{-1}(y)|.

The reason is unique randomness: for each x with h_w(x)=y and each hat(y) in the simulator's support, there is exactly one r; for other x there is none. An unreachable y has no encoding preimages from x, so its bucket is empty. The direct circuit implementation above avoids any decoder convention on unused outputs. In particular, we do not need a blanket claim about Dec on every unreachable encoded target: the abstract PRE axioms require care there. Isolating only the choice variables, before adding rank witnesses, is essential.

## 3. A general parity-filter theorem

Suppose a Boolean predicate P(x) on p bits is accompanied by a fixed-width CNF F(x,z) such that

    #{z:F(x,z)} = 2^{d(x)}

for all locally valid x, and is zero for locally invalid x, where d(x)>=0 and P(x) holds exactly when x is locally valid and d(x)=0. Suppose F has q variables in total and poly(input-size) clauses. Add the independent local hash H(x,a) of Lemma 1 and count F AND H exactly.

For each x passing H there is a unique a, and that x contributes 2^{d(x)}. Thus

    # (F AND H) mod 2 = |{x:P(x) and H has an extension}| mod 2.

If no P-solution exists, the count is even for every random choice. If a solution exists, it is odd with probability at least 1/(8p), by isolation of S={x:P(x)}. O(p) independent trials give constant one-sided success probability. The final CNF has q+O(p) variables, the same fixed maximum clause width up to max(k,3), and only O(p) extra clauses. Therefore the October exact #SAT theorem yields randomized one-sided subexponential decision time in q+p. This inference uses no assumption about weighted #SAT.

If both variables and clauses are O(N), the sharper claimed bound is

    poly(|I|) 2^{O(N/sqrt(log N))}.

If the variable count is much smaller than the clause count, add O(N) **pinned** dummy variables and unit clauses to reach constant clause/variable density. Their unique extension preserves the integer count. Unconstrained dummy variables would multiply the count by a power of two and destroy its parity. Finite sizes below a theorem's threshold are handled directly or with pinned padding.

Using only a slower n(loglog n)^2/sqrt(log n) theorem still yields 2^{o(N)}.

## 4. Graphic and cographic filters with linear overhead

### Long-clause filter (one extra bit per clause, independent of width)

For a clause C=l_1 OR ... OR l_d introduce a bit t_C and the binary clauses

    (NOT t_C OR NOT l_i), for i=1,...,d.

For fixed x, t_C has exactly one admissible value if C(x)=1 and exactly two values if C(x)=0. Hence a family of arbitrary-width clauses has extension multiplicity 2^{number of violated clauses}. An empty clause is handled by an unconstrained t_C, giving multiplicity two. Tautologies correctly force t_C=0. Keep any already fixed-width exact constraints as they are; only the long clauses need filter bits. Combining their multiplicity with rank witnesses adds their deficiencies. The clauses here do not enforce C pointwise; they enforce it only after taking parity, which is sufficient for the isolation argument.

Consequently parity of an arbitrary CNF on n variables and m clauses reduces to parity of 2-CNF on n+m variables, using polynomially many clauses (one per literal occurrence). With local isolation on the original n bits first, this gives RP 2^{o(n+m)} decision time. It gives no n-only result when m is superlinear in n.

### Graphic spanning

Let G have v vertices, e edges, and c(G) components. Pin one potential b_v=0 in each host component. For every selected/activated edge uv, impose b_u=b_v. For a choice x activating Y(x), the number of potentials is

    2^{c(V,Y(x))-c(G)} = 2^{r_M(E)-r_M(Y(x))}.

An implication y_uv -> (b_u=b_v) takes two width-three clauses. Potentials require only v-c(G) variables, even for dense G. If activation is a constant-arity predicate in x, expand its truth table directly with these equalities, yielding fixed-width clauses without one extra activation variable per edge. If activations instead come from a circuit of L gates, use L uniquely determined gate variables.

### Cographic spanning

For G, introduce one circulation bit z_e per edge. Impose z_e=0 on each activated edge e in Y(x), and impose even incidence parity at every vertex. Over F_2 the solutions are exactly the cycle space of (V,E\Y(x)), so their number is

    2^{|E\Y(x)|-v+c(V,E\Y(x))}
      = 2^{r_{M^*}(E)-r_{M^*}(Y(x))}.

This also handles loops (their two incidences cancel); parallel edges are harmless. A chain of XOR gates encodes a degree-d vertex parity using O(d) gates and uniquely determined gate variables. Summed over all vertices the overhead is O(v+e). Consequently the cographic filter has O(e+v) variables and clauses before local choice constraints. Unlike the graphic filter, its variable count generally depends on e even when the input graph is dense.

For direct sums, use independent potential/circulation variables on components. Multiplicities multiply, and deficiencies add. Together with Lemma 1, this proves that **explicit sparse graph/cograph span-CSP with total local/activation description O(N) has a randomized 2^{o(N)} algorithm**, conditional on the October #SAT theorem. A randomized hardness hypothesis for exactly this sparse class is therefore untenable under that theorem. A deterministic hardness assertion is a separate matter: the construction has one-sided randomization.

## 5. Natural targets: what is actually excluded as a candidate

The table records deductions, not a claim that every algorithm was previously in the literature.

| Problem and parameter | What follows from the SAT theorem and the deductions above |
| --- | --- |
| General fixed-k SAT/#SAT, n variables | Claimed deterministic 2^{o(n)} algorithm, including polynomial input-size factor. |
| Unrestricted-width CNF-SAT, n variables | No general 2^{o(n)} consequence is established. Gate conversion costs total literal occurrences. |
| Hamiltonian Cycle, v+e | RP 2^{o(v+e)} via the graphic filter, edge bits and linear degree-exactly-two circuit. Thus RP 2^{o(v)} for bounded-degree or sparse graphs. Dense v-only case is not settled by this encoding. |
| Feedback Vertex Set, v+e | RP 2^{o(v+e)} via vertex deletion bits, edge activation x_u OR x_v and the cographic filter; cardinality has a linear-size Boolean circuit. Dense v-only case is not settled. |
| Set Cover, universe u | No u-only consequence is established. Choice bits depend on number of sets, coverage on incidence description. A 2^{o(total sparse description)} consequence is easy but changes the parameter. |
| Fixed-q Coloring, v | Claimed deterministic 2^{o(v)} for each fixed q, even dense graphs: qv one-hot bits and fixed-width clauses. |
| Chromatic Number, v | Arbitrary q is not fixed-q Coloring. No v-only subexponential consequence is established here. |
| Connected Vertex Cover, v | RP 2^{o(v)} even dense graphs, by the explicit encoding below. This should be removed from a randomized v-hardness candidate list. |
| Connected Dominating Set, v | RP 2^{o(v)} even dense graphs: one parity-filter bit per closed-neighborhood domination clause and the same O(v)-variable connectivity filter. |
| Steiner Tree (unweighted edge-budget version), v | RP 2^{o(v)} even dense graphs: equivalent to a connected vertex set containing all terminals with at most k+1 vertices when the edge budget is k. Weighted edge budgets and terminal-only parameters are not covered. |

Cardinality circuits really can have linear size: repeatedly compress triples of same-weight bits with full adders, reducing their number by one per constant-size compressor. There are O(t) compressors for t input bits. Add/compare the remaining O(log t)-bit words using O(log t) further gates. This avoids an unnecessary t log t bound for unweighted cardinality. Binary-weighted sums need separate bit accounting.

### Full proof for dense Connected Vertex Cover

Given simple G=(V,E), budget k, and chosen root r, use choice bits x_v meaning selected. Require x_r=1, at most k selected vertices, and x_u OR x_v for every edge uv. The budget circuit has O(v) gates with unique extensions.

On the same vertex set form an augmented host: retain an edge uv active when x_u=x_v=1; add a root-star edge rv active when x_v=0. Every unselected vertex then attaches directly to r; no unselected vertex links two selected vertices. Since r is selected, this augmented active graph is connected exactly when G[{v:x_v=1}] is connected.

Pin b_r=0. For each original edge uv impose

    (x_u AND x_v) -> (b_u=b_v),

which expands to two clauses of width four. For every v != r impose

    (NOT x_v) -> (b_v=0),

one width-two clause. There are O(v) variables, O(v+e) clauses of width at most four, and all non-budget constraints need no auxiliary variable per edge. For a fixed x, potential multiplicity is 2^{number of selected components minus 1}. Apply local isolation to x only and exact #4SAT; odd count is a sound certificate that some connected vertex cover exists. Try all roots r. For edgeless graphs handle the empty cover convention directly. The arbitrary-density theorem gives randomized

    poly(v+e) 2^{O(v log log v / sqrt(log v))}

time. This proof does not claim the sparse-density improvement for dense graphs.

For **Connected Dominating Set**, replace the vertex-cover clauses by the v closed-neighborhood clauses OR_{u in N[v]} x_u. Apply one long-clause filter bit per neighborhood. A choice x contributes an odd multiplicity precisely when it dominates every vertex and its selected graph is connected. There are still O(v) variables, and O(v+e) clauses of width at most four, before the O(v)-size local hash. The same randomized bound follows, including on dense graphs.

For **unweighted Steiner Tree**, first handle zero terminals directly. Choose a terminal as fixed root, require all terminals selected, and require a connected selected vertex set of size at most k+1. If a tree with at most k edges exists, its vertex set qualifies. Conversely, a qualifying connected vertex set has a spanning tree with at most k edges. The same connectivity/cardinality construction therefore proves the v-only bound for arbitrary graphs. An edge-weighted cost cannot be replaced by this vertex cardinality argument.

## 6. What compact rank circuits do and do not follow

For any constructible fan-in-two verifier of size O(N log^alpha N), alpha<1/2, parsimonious Tseitin encoding and the claimed sparse #3SAT bound give exponent

    O(N log^{alpha-1/2} N) = o(N).

This is a sufficient condition, not a proved existence theorem for connectivity/acyclicity circuits. Graph algorithms stated in RAM time, small-space algorithms, NC algorithms, and distributed proof-labeling schemes cannot be silently converted to circuits of this size. No such required general construction was verified in the searches conducted here. Conversely no general Boolean-circuit lower bound excluding it has been established here.

The parity filters above bypass the need for deterministic compact rank-verification circuits: they encode a power-of-two multiplicity and use integer counting plus local isolation. They should be analyzed before making compact verifier circuits the central research obstacle.

## 7. Remaining mathematical boundaries

1. Sparse graphical and cographical rank predicates do not presently support a randomized exponential-hardness conjecture if the new #SAT theorem holds. This conclusion is stronger than the observation that fixed-width local CSPs became easy.
2. Dense vertex-only Hamiltonian Cycle/FVS, universe-only Set Cover, arbitrary-width CNF-SAT parameterized only by variables, and unrestricted Chromatic Number remain unhandled by these particular reductions. Arbitrary CNF with only O(n) clauses is handled in RP by the clause filter. This is not a literature-wide proof that no other algorithm exists.
3. The algorithm is randomized. Derandomizing the local-isolation reduction at sufficiently small cost is a genuine extra requirement if deterministic complexity is the intended hypothesis.
4. The proved bridge costs O(number of choice bits + graph filter variables + local gates), never O(number of original circuit inputs) independently of verifier size. It does not repair the n-input, n^k-gate Circuit-SAT parameter mismatch for a Williams NEXP lower bound.

## 8. Optional stronger consequence: exact unrestricted #CNF in n+m

The parity clause filter already suffices for RP decision. For exact counting, standard [block interpolation (Curticapean, 2015/2017)](https://arxiv.org/abs/1511.02910), implemented explicitly below, removes negative vertex activities without assuming a weighted #SAT theorem. This section is a deduction from established interpolation machinery and the claimed October unweighted #2SAT bound, not a claim to have invented block interpolation.

### Theorem 2

If unweighted independent sets of a q-vertex graph can be counted in time poly(|G|) 2^{O(q loglog q/sqrt(log q))}, then arbitrary-width CNF on n variables and m clauses can be counted deterministically in

    poly(|F|) 2^{O((n+m) loglog(n+m)/log^{1/4}(n+m))}.

**Proof.** Construct literal vertices T_i,F_i, with an edge T_i F_i. Add a vertex p_i adjacent to both T_i,F_i, and a clause vertex c_j adjacent to the literal vertices that satisfy clause j. Literal vertices have activity 1; the n+m special vertices p_i,c_j have activity -1. There are 3n+m vertices, and the number of edges is at most n+2n plus the number of literal occurrences after duplicate removal.

Fix an independent set A of literal vertices. Every special vertex is independent of every other special vertex. If a special vertex has a neighbor in A, it is forced absent and contributes 1. If it has no neighbor in A, summing its two possibilities contributes 1+(-1)=0. Consequently A contributes nonzero precisely when it chooses exactly one of T_i,F_i for every i and at least one satisfying literal for every clause. Each such A contributes 1. The weighted partition function is therefore exactly #F.

Let N=n+m, take block size b=ceil(log^{1/4}(max(N,16))), and partition the special vertices into B=ceil(N/b) groups of at most b. Give all special vertices in group j a formal activity z_j. The resulting independence polynomial P(z_1,...,z_B) has degree at most b in each coordinate. Our target is P(-1,...,-1).

For each coordinate interpolate at the b+1 distinct values

    lambda_t = 2^t-1,  t=0,...,b.

To implement activity lambda_t at a special vertex, replace it by t independent false twins, each with its original literal neighbors. There are exactly 2^t-1 nonempty choices of the twins, reproducing the selected-vertex activity. At t=0 remove the vertex. Every evaluation is thus an ordinary unweighted independent-set count on at most 2n+b(n+m)=O(bN) vertices. The edge count remains polynomial in the original input and b.

Tensor-product Lagrange interpolation expresses P(-1,...,-1) as a rational linear combination of all (b+1)^B evaluations. These weights can be generated as products of univariate interpolation weights. Each univariate weight has numerator and denominator of O(b^2) bits; all accumulated intermediate values have polynomial bit length in N and b. The grid can be streamed, so polynomial space suffices when the counting oracle does.

The number of evaluations has base-two logarithm O(N log b/b). Each evaluation costs exponential time with exponent O(bN loglog(Nb)/sqrt(log(Nb))). With the displayed b, both terms are O(N loglog N/log^{1/4}N). This proves the claimed bound. QED.

The ordinary #2SAT theorem counts independent sets through one variable per graph vertex and a clause (NOT x_u OR NOT x_v) per edge. Thus the premise follows directly from its arbitrary-density bound. In particular, arbitrary CNF with m=O(n) admits deterministic subexponential **exact counting**, not merely the RP decision consequence of the one-bit parity filter. For example, ordinary Dominating Set admits such a vertex-parameter subexponential algorithm using its n neighborhood clauses and a cardinality circuit. Connectivity still uses the separate parity/isolation bridge above.

## 9. Supplementary exhaustive checks

All 819 normalized two-clause CNFs on one to three variables, including empty clauses, passed both the one-bit clause parity identity and the negative-weight independent-set cancellation identity. All 760 simple-host-graph/edge-subset cases on up to four vertices passed the graphic and cographic exact multiplicity identities. A separate check of the three-state width-three connectivity encoding in research_parity_rank.md passed all 549 graph/selected-subset cases on up to four vertices with a fixed selected root. These are falsification checks supplementing the proofs, not a substitute for verification of the October SAT algorithms.

