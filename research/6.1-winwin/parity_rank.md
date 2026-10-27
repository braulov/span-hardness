# Parity lifts, local isolation, and a conditional algorithm for sparse span-CSP

Research checkpoint, 27 October 2026. These notes establish conditional implications; they do not certify the October 2026 SAT preprints. No assertion of literature novelty is made.

## Main conclusion

If ordinary unweighted #3SAT on `q` variables and `O(q)` clauses has a deterministic `2^{o(q)}` algorithm, sparse graphic/cographic span-CSP has a randomized, one-sided-error `2^{o(N)} poly(|I|)` decision algorithm. Here

\[
N=b+L+\sum_i(n_i+m_i)
\]

counts primary Boolean variables, the total size of local Boolean computations, and vertices/edges of the represented graphic and cographic summands. More generally, replace the graph-size sum by the total size of sparse binary representations of the summands or their duals.

The proof needs neither weighted #SAT nor a field-valued extension of a counting algorithm. It combines a linear-size parity lift with a known linear-size pairwise-independent hash construction. If the sharp sparse counting bound is `2^{O(q/sqrt(log q))}`, the resulting decision bound is

\[
\operatorname{poly}(|I|)2^{O(N/\sqrt{\log N})}.
\]

An independent small-range isolation argument gives the slightly weaker explicit exponent `O(N log log N / sqrt(log N))` without the linear-size hashing theorem. Both arguments isolate the primary choices and leave all rank witnesses unisolated.

This rules out sparse span-CSP as a hardness hypothesis against randomized subexponential algorithms under the stated counting premise. It does **not** refute deterministic hardness or establish any circuit lower bound. Dense-input consequences require the separate variable counts below.

**Sharper parameter refinement.** A one-bit parity filter for each long clause, together with inlining vertex-controlled edge activations, also gives conditional randomized subexponential algorithms in the vertex count for **dense Connected Dominating Set, Connected Vertex Cover, and unweighted Steiner Tree**. These refinements are proved in Section 6a. Dense Hamiltonian Cycle and dense Feedback Vertex Set are not covered by that refinement.

## 1. Precise input model

There are `b` primary variables `x`. Local constraints and activation functions `y_e(x)` have total bounded-fanin Boolean circuit size `L`. A list of bounded-arity truth-table constraints or a CNF with total literal count `L` fits this model with linear overhead. Every circuit is converted by equivalences at its gates, so all added gate variables have a unique extension for a fixed primary assignment.

The predicate of interest is

\[
F_I(x)=\varphi(x)\prod_i
\mathbf 1[r_{M_i}(Y_i(x))=r_{M_i}(E_i)].
\]

All size statements below include activation computations, local checks, rank witnesses, and gate variables. The raw bit encoding can have an additional logarithmic factor for names and endpoints; this affects the allowed polynomial input factor rather than the object-count exponent. A statement with a different parameter, such as only `b`, needs separate analysis.

## 2. Linear parity lift for a binary representation

**Lemma 1 (primal representation).** Let `A` represent a binary matroid `M`, and let `r=rank(A)`. There is an unweighted 3-CNF `Psi(x,z,a)` of size

\[
O(b+L+|E|+r+\operatorname{nnz}(A))
\]

whose number of extensions for each fixed `x` is

\[
\varphi(x)2^{r-r_M(Y(x))}.
\]

Consequently,

\[
\#\Psi\bmod2=\sum_xF_I(x)\bmod2.
\]

**Proof.** Choose a basis of the rows of `A`, obtaining an `r`-row matrix `B`. Selecting existing rows does not increase the number of nonzero entries. Since the rows of `B` span those of `A`, the two matrices have the same column dependencies. Introduce `z in F_2^r` and impose, for each element `e`,

\[
y_e(x)=1\quad\Longrightarrow\quad (B^Tz)_e=0.
\]

For fixed `x`, this system has `2^{r-rank(B_Y)}` solutions by rank-nullity. Compute each column parity by a chain of two-input XOR gates; the number of gates is at most the number of nonzeros, up to a linear overhead for constants and outputs. XOR gate equivalences have four width-three clauses and unique output values. The implications add at most one width-two clause per column. Convert all local circuits by unique-extension gate equivalences and require their checking outputs. Every admissible pair `(x,z)` has exactly one assignment to all gate variables `a`. Reduction modulo two leaves exactly the assignments with zero rank deficiency. This proves the claims. ∎

**Lemma 2 (dual representation).** Suppose instead a binary matrix `D` represents `M*`. Introduce one variable `q_e` per element and impose

\[
Dq=0,\qquad q_e y_e(x)=0\quad(e\in E).
\]

For fixed `x`, the number of witnesses is again `2^{r_M(E)-r_M(Y(x))}`. The corresponding unique-extension 3-CNF has size `O(b+L+|E|+nnz(D))`, plus the explicitly supplied row/dimension data.

**Proof.** The support restriction makes `q` a kernel vector of `D_{E\setminus Y}`. Its space has dimension

\[
|E\setminus Y|-r_{M^*}(E\setminus Y)
=r_M(E)-r_M(Y),
\]

where the equality is the dual-rank formula. Row XOR chains and the width-two clauses `(not q_e or not y_e)` implement the system with the claimed size and unique gate extension. ∎

These two lemmas show that moving from graphic/cographic matroids to arbitrary binary matroids with a sparse representation of either the matroid or its dual does not escape the parity algorithm.

## 3. Concrete graph witnesses

**Lemma 3 (graphic cuts).** In a graph `G=(V,E)`, fix one vertex in each connected component of `G` and set its Boolean label to zero. For every selected edge `uv`, require `z_u=z_v`. The number of labelings is

\[
2^{c(V,Y)-c(G)}
=2^{r_{M(G)}(E)-r_{M(G)}(Y)}.
\]

**Proof.** Labels are constant on every component of `(V,Y)`. Exactly `c(G)` of these components contain one of the fixed vertices; no two fixed vertices belong to the same component of `(V,Y)` because they belong to different original components. All other labels are independently free. For an edge with activation `y`, the implication is the pair of clauses

\[
(\neg y\lor\neg z_u\lor z_v)\land
(\neg y\lor z_u\lor\neg z_v).
\]

Thus the lift uses `O(n+m)` variables and clauses, including activations. ∎

The anchors are essential. Without an anchor, even a connected selected graph has two labelings, so every count is even. On a disconnected input, one global anchor is insufficient: one anchor is needed in each original component.

**Lemma 4 (cographic even subgraphs).** For `M=M*(G)`, rank witnesses are the even subgraphs of `G` supported on `E\Y`. Their number is

\[
2^{|E\setminus Y|-|V|+c(V,E\setminus Y)}
=2^{r_M(E)-r_M(Y)}.
\]

**Proof.** Use `D` equal to the vertex-edge incidence matrix over `F_2`, which represents `M*(G)*=M(G)`, and apply Lemma 2. The kernel equations say that the selected witness edges have even incidence at every vertex. Rank-nullity for the incidence matrix gives the exponent. Its total number of nonzeros is at most `2m`, so the XOR encoding is linear. Loops have zero incidence columns, hence give independent witness bits when not activated; this agrees with their dual coloop behavior. Parallel edges are also handled correctly. ∎

For a direct sum, introduce independent witnesses for its summands. The number of witnesses multiplies and the rank deficiencies add. The full-span parity identity survives without modification.

This is related to the cancellation principle in [Cut&Count, Cygan et al., 2011](https://arxiv.org/abs/1103.0534). The cographic lift here uses even subgraphs directly; replacing them by ordinary consistent cuts would test the wrong property.

## 4. Linear local isolation: the sharper bridge to decision

The external black box is the existence, for `s=O(b)`, of pairwise-independent hashes

\[
h_w:\{0,1\}^b\longrightarrow\{0,1\}^s
\]

with `O(b)` key bits and a uniform `O(b)`-size binary arithmetic circuit. This is stated as Theorem 2.3, items 1 and 3, in [Applebaum, *Exponentially-Hard gap-CSP and local PRG via Local Hardcore Functions*, 2017](https://eccc.weizmann.ac.il/report/2017/063/download/), citing IKOS08 and BIO14. His Theorem 3.2 and Claim 2.2 provide an independent route through a 3-local perfect randomized encoding. In particular, its randomness has a unique extension for each passing primary assignment. Fixing `w` and directly encoding the linear-size hash circuit already suffices here.

**Lemma 5 (isolation of an arbitrary solution set).** For any nonempty set `S subset {0,1}^b`, the following procedure produces a bucket containing exactly one member of `S` with probability at least `3/(16b)` (for `b>=1`): choose `s` uniformly from `{2,...,b+1}`, choose a uniform hash key `w`, and choose an independent uniform target `y in {0,1}^s`.

**Proof.** Put `K=|S|` and choose

\[
s_* = \max(2,\lceil\log_2K\rceil+1).
\]

It belongs to the sampled range. For this `s`, let `Z=|S intersect h_w^{-1}(y)|` and `lambda=K/2^s`. Then `1/4<=lambda<=1/2`, including the singleton case. Pairwise independence gives

\[
\mathbb EZ=\lambda,\qquad
\mathbb E[Z(Z-1)]=K(K-1)/2^{2s}\le\lambda^2.
\]

For every nonnegative integer `z`, `1[z=1]>=z-z(z-1)`. Therefore

\[
\Pr[Z=1]\ge\lambda-\lambda^2\ge3/16.
\]

Multiplying by the `1/b` probability of `s=s_*` proves the lemma. The set `S` need not have a local membership test. ∎

The `max(2,...)` repairs a harmless singleton boundary issue in the literal formula for `s` in the published proof of Applebaum's Lemma 4.6: sampling starts at two, while `ceil(log 1)+1=1`.

**Theorem 6 (parity-lift transfer).** Suppose `F_I(x)` has the linear parity lift of Lemmas 1–4, of size `O(N)`. If ordinary unweighted #3SAT on `q` variables and `O(q)` clauses can be computed deterministically in time `T(q) poly(|I|)`, then existence of `x` with `F_I(x)=1` has a one-sided-error randomized algorithm in time

\[
\operatorname{poly}(|I|)T(CN)
\]

for an absolute constant `C` depending only on the fixed gate/constraint basis. Success can be amplified to `1-delta` with an additional factor `O(log(1/delta))`.

**Proof.** Let `S={x:F_I(x)=1}`. In one trial, sample the bucket from Lemma 5. Add the constraint `h_w(x)=y` to the parity lift. The key and target are constants in the formula, not existential variables. A unique-extension gate encoding adds only `O(b)` variables and clauses. The parity of the resulting ordinary model count equals

\[
|S\cap h_w^{-1}(y)|\bmod2.
\]

Indeed, each invalid primary assignment still contributes either zero extensions or an even number of rank witnesses, while each valid one contributes one. If `S` is empty, every trial has even count. If `S` is nonempty, a singleton bucket gives odd count, with probability at least `3/(16b)`. Accept on any odd count; repeat `O(b log(1/delta))` times. All formulas have `O(N)` variables and clauses. If necessary, add uniquely fixed dummy variables to obtain an explicit constant clause-to-variable ratio without changing the model count. ∎

There is also a search guarantee. Given an odd bucket, fix primary variables successively. Query the parity with `x_i=0`; retain zero if it is odd, and otherwise retain one. The two restricted parities sum to the current odd parity, so one branch is odd. After `b` queries one obtains a valid full-span assignment. A final ordinary rank computation verifies it. On a yes-instance, repeating trials until an odd bucket is found gives expected `poly(|I|) T(CN)` search time. This does not supply a Las Vegas terminating no-instance algorithm.

**Conditional corollary.** If sparse ordinary #3SAT has time `2^{O(q/sqrt(log q))}`, the decision and expected successful-search bounds are `poly(|I|)2^{O(N/sqrt(log N))}`. If its bound is only `2^{o(q)}`, the conclusion is still `poly(|I|)2^{o(N)}`. No weighted model counting statement has been used.

## 5. Independent backup: small-range integer isolation

This route is useful if one prefers not to import the linear-size hash construction.

**Lemma 7 (small-range isolation).** For a nonempty family of subsets of a `b`-element universe, independent uniform weights in `{1,...,R}` have a unique minimum-weight member with probability at least `(1-1/R)^b`, for any integer `R>=2`.

**Proof.** Remove members that properly contain another member; positive weights make them irrelevant to minimum weight. For each weight vector `w in {2,...,R}^b`, choose a minimum member `S` and subtract one from the weights of its elements. The resulting vector `w'` has `S` as its unique minimum: for every other remaining `T`, `S` is not contained in `T`, and

\[
w'(T)-w'(S)=w(T)-w(S)+|S\setminus T|>0.
\]

The map `w -> w'` is injective: recover its unique minimum `S` and add one back on `S`. Therefore at least `(R-1)^b` of the `R^b` weight vectors isolate. ∎

This proof is the strengthened isolation lemma of [Noam Ta-Shma, 2015](https://eccc.weizmann.ac.il/report/2015/080/download/), whose probability remains useful even when `R<b`.

**Lemma 8 (size of the weight-sum circuit).** For prescribed integer weights `w_i in [R]`, the sum `W(x)=sum_i w_i x_i` can be computed with `O(b(log R+1))` bounded-fanin Boolean gates; equality to any prescribed target needs no asymptotically larger circuit.

**Proof.** Let `ell=ceil(log_2(R+1))`. Each conditional leaf word has bits either `x_i` or zero and needs no gates. Pad the number of leaves to a power of two smaller than `2b`, and add balanced pairs. At level `j`, there are at most `2b/2^j` additions of words of width at most `ell+j`. Ripple-carry addition uses a constant number of gates per bit. Hence the total is bounded by a constant times

\[
b\sum_{j\ge1}(\ell+j)2^{-j}=O(b(\ell+1)).
\]

The final equality test fixes the output bits, and the same gate bound dominates their number. Gate equivalences give a unique-extension 3-CNF of the same size. ∎

For each weight vector, query the parity lift with `W(x)=t` for every `0<=t<=bR`. If the weights isolate the valid full-span family, its unique minimum-weight member makes one query odd. Invalid primary choices still cancel because the weight constraint does not touch the rank witnesses.

Writing `T(q)=2^{f(q)}`, the time is at most

\[
\operatorname{poly}(|I|,bR)\,
2^{O(b/R)}\,T(C(N+b\log R)),
\]

for constant error probability. Here `(1-1/R)^{-b}<=exp(2b/R)` for `R>=2`. With `R=ceil(sqrt(log N))` and `f(q)=O(q/sqrt(log q))`, the exponent is `O(N log log N/sqrt(log N))`.

Qualitatively, any known effective subexponential `T` suffices: choose `R(N)` tending to infinity sufficiently slowly that `log R(N)` times the vanishing rate of `T(CN log R(N))` still tends to zero. Equivalently, for each desired exponent `epsilon`, choose a sufficiently large constant `R`, then use the subexponential #3SAT algorithm on the constant-factor larger formula. This gives the usual subexponential reduction interpretation without assuming a quantitative rate.

The naive choice `R=2b` and a black-box `2^{o(q)}` theorem is inadequate by itself: it creates `Theta(b log b)` extra objects, and `2^{o(N log N)}` need not be subexponential in `N`. Small-range isolation explicitly pays for its reduced success probability and avoids this gap.

## 6. Natural graph consequences and exact parameters

All implications here are conditional on the ordinary counting premise and are randomized unless another decision reduction is supplied.

### Hamiltonian Cycle

Choose an edge bit `y_e` for each of the `m` edges. Enforce selected degree exactly two at every vertex. A bounded-fanin circuit can count `d` one-bit inputs in `O(d)` gates using the balanced addition calculation with `ell=1`, or use a counter capped at three. Thus all local degree checks take `O(n+m)` gates even without bounded degree. Graphic full span in a connected input then says the selected 2-factor is connected, exactly a Hamiltonian cycle. This yields subexponential time in `n+m`; when `m=O(n)`, it is subexponential in `n`.

### Feedback Vertex Set

Use vertex bits `s_v`, set `y_uv=s_u or s_v`, and require `sum_v s_v<=k`. Balanced summation of one-bit leaves and comparison uses `O(n)` gates. Activation costs `O(m)`. By the dual-rank formula,

\[
r_{M^*(G)}(Y)=r_{M^*(G)}(E)
\iff r_{M(G)}(E\setminus Y)=|E\setminus Y|
\iff G-S\text{ is a forest}.
\]

The size parameter is `O(n+m)`, not automatically `O(n)` on dense graphs.

### Connected vertex subsets, Connected Dominating Set, Connected Vertex Cover

Fix a vertex `r` required to belong to the selected set `S`. Let a fixed graph `H` contain all original edges and, additionally, one star edge `rv` for each `v!=r`, allowing parallel edges. Activate an original edge iff both endpoints belong to `S`; activate a star edge iff `v` does not belong to `S`. Every unselected vertex is then attached directly to `r`, while no star edge connects two selected components. Therefore

\[
H[Y]\text{ is connected}\iff G[S]\text{ is connected}.
\]

The gadget has `n` vertices and `m+n-1` edges. Domination is a conjunction of neighborhood ORs of total size `O(n+m)`. Vertex cover adds the clauses `s_u or s_v`. Cardinality adds `O(n)` gates. Enumerate `r` if no root was specified, adding a polynomial factor; handle the empty-set edge cases separately. Consequently both connected problems have randomized subexponential algorithms in `n+m`, and in `n` on sparse graphs.

### Steiner connectivity

For ordinary edge-budget Steiner Tree with nonempty terminal set `T`, fix a terminal `r`. Choose original edge bits `y_e`, and set `s_v` to true precisely when `v` is a terminal or touches a chosen edge. In the same star gadget, activate the star edge `rv` iff `not s_v`, and activate the original edge according to `y_e`. Full graphic span is equivalent to connectivity of all active vertices and hence of the terminals. The budget `sum_e y_e<=k` has `O(m)` gates. A connected selected subgraph with at most `k` edges contains a Steiner tree of at most that size; a Steiner tree supplies such a selection. The complete size is `O(n+m)`.

These constructions are precise reductions into the source problem. They do not prove hardness of the natural targets from hardness of the source: that would require reverse reductions.

## 6a. Long-clause filters and dense connectivity problems

The coarse size `N=b+L+sum(n_i+m_i)` is not always necessary. Counting theorems with a polynomial clause-count factor allow many bounded-width clauses provided the **number of variables** remains small.

**Lemma 9 (one-bit long-clause parity filter).** Let `C=l_1 or ... or l_d` be an arbitrarily long clause over primary variables. Add one variable `t_C` and the width-two clauses

\[
\bigwedge_{j=1}^d(\neg t_C\lor\neg l_j).
\]

For each fixed primary assignment there is one extension if `C` is satisfied, and two extensions if it is violated. For a conjunction of `a` long clauses, independent filter bits therefore enforce the conjunction modulo two with only `a` extra variables and as many width-two clauses as literal occurrences.

**Proof.** The value `t_C=0` always works. The value `t_C=1` works exactly when all `l_j` are false. Counts multiply for the independent filter bits, so a violated clause contributes a factor two; with no violated clauses every filter bit is forced to zero. ∎

This filter can be multiplied with any of the rank-witness filters above, and with a unique-extension hash constraint on the primary variables. For every fixed primary choice, all violations still contribute even multiplicity and all valid choices contribute one. Thus Theorem 6 has the following refinement: if the resulting fixed-width formula has `Q` variables and `C` clauses, the decision cost is polynomially many calls to ordinary `#kSAT(Q,C)` for a **fixed** `k`. Only the first argument controls the exponential part. No conversion of every width-four clause to width three should be made if that would add an edge-proportional number of variables.

### General CNF with few clauses

An arbitrary-width CNF on `n` variables and `a` clauses has a parity 2-CNF encoding on `n+a` variables. The number of 2-clauses is its original total literal count. Add an `O(n)`-variable local hash to decide satisfiability randomly. Hence the ordinary fixed-width counting premise gives subexponential time in `n+a` with a polynomial factor in the input length. In particular, arbitrary-width CNF with `a=O(n)` clauses has a randomized subexponential algorithm in `n`, even when the total literal count is quadratic. This does not cover General CNF-SAT parameterized only by `n` when `a` is much larger.

### Dense Connected Dominating Set and Connected Vertex Cover

Use only vertex-choice variables `s_v`, potential variables `z_v`, the rooted star gadget from Section 6, and a linear-size cardinality circuit. Fix a selected root `r`, anchoring `z_r=0`.

For each original edge `uv`, inlining its activation `s_u and s_v` yields exactly the width-four clauses

\[
(\neg s_u\lor\neg s_v\lor\neg z_u\lor z_v)
\land
(\neg s_u\lor\neg s_v\lor z_u\lor\neg z_v).
\]

For each star edge `rv`, activation `not s_v` and the root anchor simply require `(s_v or not z_v)`. For fixed nonempty `S` containing `r`, the number of potential assignments is `2^{c(G[S])-1}`: every unselected vertex is forced to zero; the selected component containing `r` is zero; every other selected component has an independent label. This is odd precisely for a connected selected set.

One can keep width three without adding a variable per edge. Replace each vertex potential by two witness bits `a_v^0,a_v^1`. Impose

\[
(\neg s_v\lor a_v^0\lor a_v^1),\quad
(s_v\lor\neg a_v^0),\quad
(s_v\lor\neg a_v^1),\quad
(\neg a_v^0\lor\neg a_v^1).
\]

An unselected vertex has the unique state `(a^0,a^1)=(0,0)`; a selected vertex has exactly one of its two label bits true. Each original edge `uv` now needs only the two width-two clauses

\[
(\neg a_u^0\lor\neg a_v^1),\qquad
(\neg a_u^1\lor\neg a_v^0).
\]

They forbid unequal labels exactly when both endpoints are selected. Require the selected root's label to be zero, i.e. `a_r^1=0`. There are still precisely `2^{c(G[S])-1}` witnesses. This three-state encoding is the familiar local viewpoint behind consistent-cut cancellation; no claim of novelty is intended.

Connected Vertex Cover adds the original width-two clauses `s_u or s_v`. Connected Dominating Set adds one long domination clause `s_v or OR_{u in N(v)}s_u` per vertex and implements these with Lemma 9, using just `n` additional variables. Thus both reductions have `Q=O(n)` variables, width at most three, and `C=O(n+m)` clauses. Enumeration of the root is polynomial. Hash the vertex choices only.

Consequently, an ordinary #3SAT bound

\[
\operatorname{poly}(Q+C)\,
2^{O(Q\log\log Q/\sqrt{\log Q})}
\]

implies the same asymptotic randomized exponent in `n`, **also on dense graphs**. If only the sharper linear-density counting theorem is available, it does not by itself justify this dense-input conclusion; here the clause count can be quadratic in `Q`.

The same long-clause argument, without the rank witnesses, gives a randomized subexponential algorithm for ordinary Dominating Set on dense graphs under that ordinary counting premise.

### Dense unweighted Steiner Tree

For a nonempty terminal set `T`, an edge-budget Steiner tree of at most `k` edges exists if and only if a connected vertex set `S` exists with `T subset S` and `|S|<=k+1`. One direction uses the vertex count of a tree; for the other, take a spanning tree of `G[S]`. Choose a terminal as the fixed root. The preceding three-state vertex-choice connectivity filter, terminal unit clauses, and the `O(n)`-gate cardinality circuit give `O(n)` variables, `O(n+m)` clauses, and fixed width three. Therefore the dense graph version has the same conditional randomized subexponential bound in `n`. This equivalence concerns unweighted edge-budget Steiner Tree; arbitrary edge weights are not handled by the vertex-count substitution.

### A narrowly specified weighted extension that would settle dense FVS

The following is an exact identity, not an assertion that the ordinary #SAT theorem supports its weights.

Let `R` be the retained vertex set, `H=G[R]`, and `beta(H)=|E(H)|-|R|+c(H)` its cycle-space dimension. Use the three-state cut encoding above, but do **not** anchor a root. Its number of witnesses is `2^{c(H)}`, including the empty-set convention `c(empty)=0`. Give weight two to every original edge whose endpoints both lie in `R`, and weight two to each vertex outside `R`; all other such factors have weight one. For each retained primary assignment, the weighted sum over its cut witnesses is exactly

\[
2^{|E(H)|}\,2^{n-|R|}\,2^{c(H)}=2^{n+\beta(H)}.
\]

Since `beta(H)>=0`, the total weighted count `Z` over any budget-and-hash-restricted family of retained sets is divisible by `2^n` and satisfies

\[
(Z/2^n)\bmod2
=\#\{R\text{ in the family}:G[R]\text{ is a forest}\}\bmod2.
\]

This gives an `O(n)`-variable construction even for dense FVS if one has a subexponential algorithm for exact bounded-arity weighted Boolean partition functions with weights only in `{0,1,2}`, with a polynomial dependence on the number of factors. The hard constraints have width at most three, and the nontrivial positive edge factors have arity two. Linear local isolation then yields randomized decision in the vertex count. The weighted output has only polynomially many bits, since its largest exponent is `O(n+m)`.

That weighted theorem is an additional requirement. The direct black-box conversion of an edge weight two into a free conditional Boolean bit costs one variable per edge and returns to the coarse `n+m` parameter. A proof that the October 2026 algebraic counting machinery handles exactly this finite weight alphabet would therefore be a concrete and potentially decisive next step; no such proof is supplied here.

## 7. Failure modes and remaining barriers

1. **Parity alone does not decide existence.** One graphic edge activated by `x=1` and a completely free primary bit `t` has two valid assignments. Its full-span count is even despite existence. Isolation must act on all genuine primary choices.

2. **Do not isolate the rank witnesses.** Take the same one-edge graph but force `x=0`. There is no full-span solution. Its two rank witnesses cancel. If a hash or weight condition singles out just one witness, the resulting count can become odd and produce a false positive. Hash only `x`; all witnesses for a fixed `x` must remain together.

3. **Unique gate extension matters.** Mere equisatisfiable CNF encodings may introduce variable-dependent multiplicity. Gate equivalences, rather than one-direction implications, preserve the precise counts needed in the proof.

4. **The coarse `n+m` bound alone says nothing subexponential in dense graphs' vertex count.** At `m=Theta(n^2)`, even `2^{O((n+m)/sqrt(log(n+m)))}` does not improve on `2^{O(n)}`. Section 6a supplies separate `O(n)`-variable constructions for several vertex-selection connectivity problems. Dense HC and FVS still retain their edge-variable/witness obstacle in the constructions here. Neither a sparse decision algorithm nor a sparsification lower bound automatically resolves what an exponential-time sparsifier can do.

5. **The result is not integer counting.** It computes full-span solution parity and gives randomized existence/search through isolation. Recovering the exact integer number is not established. For example, `k` independent copies of the rank witnesses give the value of `P(2^k)`, where `P(t)=sum_x phi(x)t^{deficiency(x)}`; extracting its constant coefficient by the straightforward interpolation can require quadratic total formula size.

6. **Randomization has not been removed.** Therefore deterministic span-CSP hardness is not logically contradicted by this theorem. A deterministic isolating family of appropriate construction cost would change that conclusion, but no such family is supplied here.

7. **No Williams conclusion follows from this argument.** The established algorithms concern parity projections of linear-size local descriptions. An `n`-input circuit of size `n^k` naturally produces size `Theta(n^k)`, leading only to a bound such as `2^{O(n^k/sqrt(log n))}`. This is not an improvement over `2^n` for arbitrary fixed `k>1`. Moreover, the decision bridge here is randomized. Neither gap is repaired merely by invoking an algorithm-to-lower-bounds theorem.

The mathematical progress is therefore an algorithmic obstruction to the original sparse randomized hardness candidate, rather than the sought circuit-lower-bound win-win. A viable next candidate must preserve information that this parity lift and linear local isolation do not already make accessible, while still overcoming the separate input-count versus verification-size barrier.

## 8. Finite sanity checks

Independent exhaustive checks in the research session verified the clause filter on all 819 normalized two-clause CNFs over one to three variables (including empty clauses); the three-state selected-subset witness count on all 549 graph/subset cases with at most four vertices and a fixed selected root; and the rooted graphic/cographic witness counts on all 760 graph/edge-subset cases with at most four vertices. These checks supplement, and do not replace, the proofs above.
