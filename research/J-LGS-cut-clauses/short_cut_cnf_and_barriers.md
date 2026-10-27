# Research J: short separating cuts as clauses in LGS

2026-10-27. **Scope:** a proved structural algorithm (modulo the explicitly conditional October 2026 #kSAT theorem for the subexponential bound); **not** an algorithm for unrestricted LGS or a proof of NEXP not in L/poly. No novelty priority asserted. Built on branches research/I-LGS-algorithms, H, and 6.1.

## 1. Canonical cut-CNF on the ORIGINAL input bits

Let G=(V,E) with p independent switches and edge labels in {0,1,x_i,not x_i}. The selected graph G_x is connected iff every nontrivial vertex cut has some selected edge crossing it. For each cut U define C_U as the OR of the labels on crossing edges, discarding 0. A 1 label or both polarities of the same switch makes the clause a tautology. Otherwise C_U is a consistent clause on at most p literals. Therefore LGS is exactly an (initially exponential-size) CNF on the **original p variables**, without any existential variables:

  Connected(G_x) iff AND_{nonempty proper U subset V} C_U(x).

This equivalence is unconditional, including parallel edges and loops (loops never cross).

## 2. Polynomial-time oracle for short CUT implicates

For a consistent clause C (no complementary pair of literals), let H_C=(V,E_C) contain exactly the edges labeled 1 or by a variable literal NOT included in C. Edges labeled 0 and all edges with labels in C are excluded. Then

  H_C disconnected iff some graph cut has all nonzero labels in C.

Proof: if H_C disconnects, a component has no crossing edges outside C; conversely if a cut has that property, none of its crossing edges belongs to H_C. This implies the clause C is necessary for full connectivity, since any assignment falsifying all C literals activates a subgraph of H_C.

The converse 'C is a semantic implicate of the LGS predicate iff H_C disconnects' is FALSE: C could follow from interactions among several cuts even if H_C has a connected path using mutually incompatible labels. This oracle detects CUT implicates, not all semantic implicates.

Enumerate every consistent clause on at most k switches, using

  M(p,k)=sum_{i=0}^k (p choose i) 2^i <= (k+1)(2p)^k

candidate clauses, and retain precisely the C for which H_C is disconnected. Denote their conjunction F_k(x). Time to construct: O(M(p,k) * poly(S)); #variables exactly p; #clauses <=M(p,k); width <=k.

For every x, Connected(G_x) => F_k(x).

## 3. Exact promise characterization via CUT-OBSTRUCTION WIDTH

For a disconnected G_x let w(x) be the minimum distinct literal count in any *nontrivial cut* of G_x that has no active edges crossing it, ignoring constant zeros. Such a cut's labels are consistent because if both polarities of any variable crossed it, one edge would be active. Set

  kappa(I)=max_{x:G_x disconnected} w(x),

with kappa(I)=0 if all assignments are connected (edge-case convention).

**Theorem.** For every k>=0, F_k(x) equals Connected(G_x) pointwise for all x iff k >= kappa(I). More precisely, for any x with G_x disconnected,

  F_k(x)=false iff w(x)<=k.

Proof: if w(x)<=k, take a disconnected cut of width <=k and let C be its distinct nonzero labels. It is falsified by x, and H_C is disconnected (that cut has no edge in H_C), hence F_k(x)=false.

Conversely if F_k(x)=false, some retained C of width <=k is falsified by x. Since H_C is disconnected, select one of its component cuts. All nonzero crossing labels belong to C and so are false under x. Thus it is a cut of G_x with <=k distinct labels, so w(x)<=k.

**Algorithmic corollaries.**

* For inputs promised kappa<=2, build F_2 and run ordinary 2-SAT: deterministic polynomial time O(p^2 poly(S)), unconditionally.
* For any FIXED k, assuming a deterministic exact #kSAT algorithm in 2^{o(p)} poly(m,p) time (the October 2026 proposed theorem), build F_k and run that solver. The resulting deterministic complexity is 2^{o(p)} poly(S), despite arbitrary polynomial S=p^{O(1)}; the O(p^k) clauses are polynomial for fixed k. For k=1,2 the solver is already polynomial-time.
* If the largest non-tautological inclusion-minimal edge cut ('bond') has <=k distinct nonzero literal labels, kappa<=k. This follows by selecting an inclusion-minimal cut among cuts with no active crossing edges for a disconnected x. Every such cut clause is consistent.
* Every cactus multigraph has all bonds of cardinality <=2 (bridges have size 1, cycles contribute bonds of size 2), so *every* literal-labeled cactus LGS is equivalent to 2-CNF and polynomial-time solvable.
* Even on hosts with very large bonds, kappa can be small if many cuts are tautological from opposing polarities or if components admit a smaller obstruction cut.

For growing k one must explicitly account for the p^{O(k)} enumeration and the *uniform-in-k* quantitative fixed-width #SAT bound; 'for every fixed k' alone does NOT imply the desired growing-k claim.

## 4. Why the parameter cannot solve unrestricted BP-SAT this way

Parity on p bits is computed by a polynomial-size acyclic deterministic branching program (and hence by a polynomial-size LGS instance using the 6.1 reduction). But the Boolean parity predicate has **no nontrivial implicates of width below p**: for every partial assignment of fewer than p bits, there are both satisfying and unsatisfying extensions. Therefore any CNF over the same p variables recognizing odd parity must contain width-p clauses. Consequently kappa of a pointwise LGS representation of p-bit parity is p, by the exactness theorem above (assuming its ground graph connected). Restricting to short cut clauses fundamentally cannot handle even this easy-to-solve L/poly predicate.

There is a separate representation-counting barrier. With q Boolean variables total, there are at most O(q^3) distinct clauses of width at most 3, hence at most 2^{O(q^3)} syntactically distinct 3CNFs and at most this many existentially projected predicates on p designated inputs. For each fixed c>=4, arbitrary Boolean functions on t=floor(c log_2 p) inputs number 2^{2^t}=2^{Omega(p^c)}, yet can each be computed by an acyclic decision-tree BP of size O(2^t)=O(p^c). Thus no pointwise **exists-auxiliary 3CNF representation** with q=O(p polylog(p)) variables can cover *all polynomial-size BPs* across all fixed polynomial exponents. More quantitatively, to represent all size-p^c BPs pointwise one sometimes needs q=Omega(p^{c/3}).

This does NOT rule out SAT-only algorithms/reductions, many-instance methods, superpolynomial preprocessing, or algebraic algorithms operating directly on the BP. It is a reason not to rely exclusively on general auxiliary-variable compression.

## 5. Experiments

Sanity checks in the working research session:
- 500 random labeled graphs on four vertices and three switches, 4000 assignments total, checked 'F_2 falsified iff disconnected and w(x)<=2'; all passed after correcting the cut enumeration to include only cuts with **zero selected crossing edges**.
- A literal-labeled cactus on five vertices, sixteen assignments, checked equality F_2(x)=Connected(G_x); all passed.
- For parity p=2,...,5, verified that no nontrivial implied clause has width <p; width-p CNF has 2^{p-1} clauses. Tests supplement proofs; no external theorem tested.

## 6. Next attack

The clean two-track algorithmic target is now:
A. A 'small cut clause + affine constraints' inference/compilation algorithm, so that parity/XOR does not force kappa=p. The desired type of theorem should bound the size of the representation **by p**, independent of huge S, and include some classes of polynomial BP genuinely outside bounded-width CNF.
B. A direct, non-CNF symbolic matrix-product/BP evaluation method exploiting repeated input labels (Fourier, Möbius, tensor network cuts) while preserving actual 2^{o(p)} poly(S) complexity. Pure conversion to 3CNF with O(S) auxiliaries is insufficient.
C. Explore deterministic savings below 2^p with precise Williams transfer. Existing BP-SAT algorithms for o(p^2) size and syntactic read-k are precedents, not unrestricted successes.

Sources: Schuler's CNF algorithm (2005), Dantsin–Wolpert derandomization (2004), Nagao–Seto–Teruyama (ISAAC 2017), Makita et al. (2022), Chen–Kabanets–Kolokolova–Shaltiel–Zuckerman (2014), and Ryan Williams (2010/2011). All fixed-width #SAT26 dependent statements here remain conditional.
