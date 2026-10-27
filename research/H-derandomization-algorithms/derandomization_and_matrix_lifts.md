# Branch H — Algorithms and partial derandomization

Research note, 2026-10-27. Based on research/6.1-winwin. **Conditional** on the October 2026 exact #3SAT theorem; external result still undergoing independent review. **No novelty or publication claim.** All rates count the variables and gate/witness objects explicitly. We deliberately set aside all hardness-conjecture questions.

## Base transfer: power-of-field witness multiplicity

Let primary choice bits x have length p and satisfy a local predicate computed by a bounded-fanin circuit of total size L with uniquely determined gate extensions. Let d(x) be the *sum* of rank deficiencies of explicitly represented matroid constraints, each defined by a sparse matrix or its sparse dual over a fixed finite field F_q, q=ell^a. Suppose all witness equations and activations are implementable using O(N) bounded-fanin Boolean gates, N>=p. There is a parsimonious fixed-width CNF encoding of the choice/witness relation for which each locally valid x has exactly q^{d(x)} extensions, and each invalid x has none. Taking the exact count modulo the characteristic ell yields

    #extensions mod ell = # {locally valid x : d(x)=0} mod ell.

Local linear-size isolation on *primary* x (not on witnesses) followed by the October claimed exact #SAT yields a one-sided randomized 2^{o(N)} poly(input) algorithm. For a sparse q-variable, O(q)-clause #3SAT black box of time 2^{O(q/sqrt(log q))}, the RP bound is 2^{O(N/sqrt(log N))} poly(input). Different fixed finite fields should be handled separately, rather than naively multiply counts modulo incompatible characteristics. The extension from fixed F_2 to any ONE fixed characteristic field is straightforward; multiple simultaneous constraints over different fields require an additional construction or separate treatment.

The same filter applies to a variable sparse linear system A(x)z=0, not only selected columns of a fixed matrix. With r witness coordinates and h potential nonzero coefficient positions whose values have aggregate O(N) Boolean evaluation circuits, the number of extensions per x is q^{r-rank(A(x))}. Thus constrained nonsingularity of sparse variable matrices belongs to the same conditional randomized subexponential family.

## Theorem H1: deterministic exact count when deficiency is bounded

Assume 0<=d(x)<=D for EVERY locally valid x. For j=0,1,...,D, make j disjoint copies of the rank witness variables and constraints, while sharing the primary x and its local circuit. Exact unweighted #3SAT then computes the integer

    M_j = sum_{x locally valid} (q^{d(x)})^j = sum_{i=0}^D a_i q^{ij},

where a_i is the number of locally valid assignments with d(x)=i. The j=0 query computes the number of local solutions, with no rank witnesses. Let

    P_D(z) = product_{i=1}^D (z-q^i)/(1-q^i) = sum_{j=0}^D c_j z^j.

Then P_D(1)=1 and P_D(q^i)=0 for i=1,...,D, so

    a_0 = sum_{j=0}^D c_j M_j.

The answer is an exact integer; the rational interpolation coefficients have bit lengths polynomial in D, and M_j have at most O(p + j*r) bits. This is D+1 deterministic #SAT queries of size O((D+1)N) each, so a deterministic 2^{o(N)} algorithm for any fixed D. With a sparse counting rate 2^{O(s/sqrt(log s))} it remains 2^{o(N)} when D=o(sqrt(log N)); using only the weaker Lean-stated rate, D=o(sqrt(log N)/(loglog N)^2) suffices. The claim is a promise result: bounding d only for YES witnesses is insufficient. For D=1:

    a_0 = (q*M_0 - M_1)/(q-1).

For binary q=2, a_0=2 M_0 - M_1.

Applications: graphic rank constraints when every locally allowed active graph has at most D additional connected components over the ground graph; cographic constraints when every locally allowed inactive subgraph has at most D independent cycles; bounded total deficiency across direct sums. This algorithm counts ALL full-rank satisfying choices, even if they are exponentially numerous.

## Theorem H2: deterministic SUBEXP with few full-span solutions

Let S={x in {0,1}^p : local(x) and fullspan(x)} and K=|S|. Given an integer upper bound K<=2^t, there exists a partial assignment fixing at most t primary variables for which an O(1)-field modulus of the number of remaining full-span solutions is nonzero; in particular it has odd count for binary matrices.

Proof: for |S|>=2, some coordinate differs among its solutions. Fix that coordinate to whichever bit is taken by a nonempty *minority* of S. The restricted set has between 1 and floor(|S|/2) elements. Repeat at most ceil(log_2 K) times to isolate a singleton. The restriction's valid-choice count is one in every characteristic.

Enumerate all partial restrictions fixing <=t coordinates. Number of queries:

    B(p,t) = sum_{i=0}^t 2^i * binom(p,i) <= (t+1)*(2p)^t   (t<=p).

For each restriction compute the exact unweighted fixed-width SAT count of the original rank-lift CNF with corresponding unit clauses, reduce mod ell, and accept if ANY count is nonzero. On NO instances all counts vanish. If S is nonempty and K<=2^t, one restriction isolates a valid x and produces residue 1. This is fully deterministic, with time B(p,t) * poly(input) * 2^{o(N)}.

With p<=N, t log N=o(N) suffices to preserve 2^{o(N)}. In particular, any polynomial upper bound K<=N^c gives an overhead 2^{O(log^2 N)}. Also applies to UNIQUE full-span instances without extra restrictions. Once a nonzero residue is found, parity-preserving self-reduction recovers an actual solution with at most p further oracle queries. The general-case deterministic conclusion is **not** established.

Note: this is a standard-style low-solution parity isolation observation, not claimed as new. For arbitrary S of exponential size, the restriction enumeration becomes exponential.

## Further algorithmic uses

* Sparse explicit graphic/cographic full-span conjunctions, including simultaneous connectivity/acyclicity constraints and degree/budget restrictions.
* Fixed-field sparse linear algebra with choice-dependent coefficients, including constrained nonsingular sparse matrix completion.
* The pre-existing checkpoint proves conditional deterministic exact #CNF in 2^{o(n+m)} via block interpolation and #IndependentSets: this already derandomizes the Set Cover, Hitting Set, and ordinary Dominating Set applications where their CNF has O(n+m) choice and coverage clauses. The global graph connectivity filters remain randomized in general.
* Hamiltonian Cycle/FVS: RP 2^{o(v+e)}; deterministic 2^{o(v+e)} when the full-span solution count is small or the rank deficiencies are uniformly bounded by the preceding theorems. For v-only on dense HC/FVS, we still lack an O(v)-variable encoding.
* Connected Dominating Set, Connected Vertex Cover, unweighted edge-budget Steiner Tree: see the preceding 6.1 checkpoint for randomized v-only algorithms, including dense graphs.

## Obstacles / next targets

1. Uniform deterministic 2^{o(N)} decision for arbitrary rank-full solution sets remains unresolved by parity lifting: an even number of successful assignments has zero residue. Derandomizing generic Valiant–Vazirani isolation is a separate hard question; see Dell–Kabanets–van Melkebeek–Watanabe (2013), https://www.cs.sfu.ca/~kabanets/Research/isolation.html.
2. Search for an efficiently representable *exact zero-deficiency projector* with near-linear #SAT variable overhead, or algebraic moment/partition-function interpolation that works without a global deficiency bound. The direct moment method uses D witness copies, which is too costly for D=Theta(N).
3. Find v-only sparse witness encodings for dense Feedback Vertex Set (current cographic cycle-space witness count uses e variables), or dense Hamiltonian Cycle (current primary edge choices use e variables).
4. For restricted graph classes, known deterministic rank-based dynamic programs and isolation schemes must be checked before novelty claims: Bodlaender–Cygan–Kratsch–Nederlof (ICALP 2013), https://research-portal.uu.nl/en/publications/deterministic-single-exponential-time-algorithms-for-connectivity-2/ ; Nederlof–Pilipczuk–Swennenhuis–Wegrzycki (STACS 2022), https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2022.50 .
5. Try integrating block interpolation (already successful for #CNF on n+m) with parity-rank projectors. No general exact counting construction is established.

## Checks

Elementary exhaustive verification of H2 on all 65,535 nonempty subsets of {0,1}^4, and 500 random bounded-deficiency moment cases with D=1,...,5, passed in the current research session. These tests are only sanity checks; they do not verify the external exact #SAT theorem or prove novelty.
