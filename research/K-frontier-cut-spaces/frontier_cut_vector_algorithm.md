# K — Deterministic LGS via frontier cut-vector spaces

Research checkpoint, 2026-10-27. **Main claim:** a rigorously specified deterministic LGS decision algorithm with running time \(2^{O(f+\ell)}\mathrm{poly}(S)\) for a *given edge order*. It is a structural special-case algorithm, **not** a general \(2^{o(p)}\) algorithm, not a NEXP lower-bound proof, and not a claim of literature novelty. The cut-vector reduction is closely related to rank-based connectivity dynamic programming (Bodlaender–Cygan–Kratsch–Nederlof, ICALP 2013 / Information and Computation 2015, https://doi.org/10.1016/j.ic.2014.12.008).

## 1. Joint frontier parameter

An LGS instance consists of an undirected multigraph \(G=(V,E)\), \(S=|V|+|E|\), and every edge labeled \(0,1,x_i,\neg x_i\) for one of \(p\) free switches. A full-span assignment is an assignment with connected active graph (the ground graph is assumed connected, though the algorithm handles arbitrary hosts).

Fix an **ordering of edge identities** \(e_1,\ldots,e_m\). After processing the first \(t\) edge identities:

- \(B_t\) consists of a fixed root \(r\), plus vertices incident to at least one processed and one unprocessed edge. Write \(f=\max_t(|B_t|-1)\).
- \(L_t\) consists of switches with at least one occurrence among the processed edge labels and at least one among the unprocessed. Write \(\ell=\max_t |L_t|\).

During the processing of one edge, introduce at most two new vertices and (temporarily) one new switch. Thus these transient increases only add an absolute constant. Isolated vertices of a graph with \(>1\) vertices can be rejected immediately. A switch that never occurs is irrelevant for decision.

Define the **joint frontier width** \(w=f+\ell\). It is the vertex-boundary size (up to root and constants) of the 3-uniform incidence-hypergraph edge order with a hyperedge \(\{u,v,x_i\}\) for each switch-labeled graph edge (or \(\{u,v\}\) for a constant edge). The distinction between graph vertices and switches is essential.

## 2. Main theorem

**Theorem K1.** Given any edge order of joint frontier width \(w\), LGS decision is solvable deterministically in \(2^{O(w)}\mathrm{poly}(S)\) time. More explicitly, a straightforward bit-vector basis implementation uses at most \(2^{\ell+O(1)}\) independent live-switch groups, each with a binary vector-space basis of dimension at most \(2^{f+O(1)}\). Hence any class admitting a *provided or efficiently constructible* order \(w=o(p)\) has deterministic \(2^{o(p)}\mathrm{poly}(S)\) satisfiability, including for \(S=p^k\) with any fixed \(k\).

The algorithm does not use the October 2026 SAT theorem or randomized isolation.

### Cut vectors

For a set \(B\ni r\), let \(\Omega_B\) be the \(2^{|B|-1}\) Boolean assignments \(\sigma:B\to\mathbb F_2\) with \(\sigma(r)=0\). For a partition \(\pi\) of \(B\), define its **compatible-cut vector**

\[
v_\pi\in\mathbb F_2^{\Omega_B},\qquad
v_\pi(\sigma)=1
\iff
\sigma\text{ is constant on every block of }\pi.
\]

For a fixed partial switch assignment, the processed *active* graph induces a partition \(\pi\) of the currently exposed vertices by connected components. Forgetting a component which has no remaining boundary vertex and does not contain the root makes this partial solution unusable forever. We represent this case by the **zero vector**, rather than a separate death flag.

All three graph update operations are **linear maps on compatible-cut vectors**:

1. **Introduce an unused vertex** \(a\) as a singleton. For each cut assignment on \(B\cup\{a\}\), duplicate the old coordinate for its restriction to \(B\). This is the linear map \(I_a\).
2. **Activate an edge \(uv\).** Merge the blocks of \(u,v\). On cuts, multiply coordinates by \(\mathbf 1[\sigma(u)=\sigma(v)]\). This diagonal linear map is \(J_{uv}\). An inactive edge applies the identity.
3. **Forget a non-root vertex \(a\).** For a cut \(\sigma\) of the remaining boundary, sum both extensions \(\sigma(a)=0,1\) modulo 2. This is the linear projection \(F_a\).

The forgetting identity is particularly important. If \(a\) was the last boundary vertex of its component, both cut labels are possible, so the sum is \(1+1=0\) in \(\mathbb F_2\). If the block has another surviving boundary vertex, exactly one label extends consistently, so the vector becomes precisely that of the restricted partition. Thus forgetting automatically annihilates a prematurely closed component.

### Dynamic program

At each edge prefix \(t\) and each assignment \(\tau\in\{0,1\}^{L_t}\) to the **live switches**, store only a **basis** of a vector space \(W_{t,\tau}\). It is the span of cut vectors of all feasible partial assignments of switches already encountered that induce \(\tau\) on still-live switches. An irrelevant closed component contributes the zero vector.

Initially \(B_0=\{r\}\), \(L_0=\varnothing\), \(W_{0,\varnothing}=\mathrm{span}\{[1]\}\).

When processing the next edge, if its switch has not been seen before, branch on its 0/1 value. Otherwise use the stored live value. Apply \(I_a\) for previously unseen endpoints, apply \(J_{uv}\) if the edge is activated, and apply \(F_a\) for vertices whose last edge has just been processed. Forget the switch's assigned value after its final occurrence, merging both possibilities into the same live-state by taking **linear span of their images**. Each operation is linear, so a basis suffices to preserve the exact span of all possible underlying partial assignments.

At the end, the boundary consists of \(\{r\}\), so the cut-vector dimension is one. A complete assignment contributes \([1]\) iff the active graph is connected and \([0]\) otherwise. Therefore the answer is YES iff the final stored span is nonzero.

### Proof of correctness

Use induction on the processed edge prefix. Initially the sole partial assignment and its pinned cut vector are correct. The three maps above implement exactly the component partition changes, including automatic cancellation of sealed components. Splitting on a fresh switch considers both values; retaining a live switch maintains global consistency across arbitrarily many occurrences. Since all graph maps are \(\mathbb F_2\)-linear and taking spans commutes with their application,

\[
T\bigl(\operatorname{span} X\bigr)=\operatorname{span}\{T(x):x\in X\}.
\]

Merging switch states takes a union of feasible assignments, whose vector-span is the span of the union of state bases. Thus the invariant holds. At the final one-coordinate space, a nonzero span exists iff at least one connected assignment exists. Importantly, **we are not summing the vectors over assignments** (which would lose an even number of solutions); we keep their linear span. This is the deterministic replacement for global parity isolation when the boundary is small. QED.

### Running time

The boundary vector dimension at step \(t\) is \(D_t=2^{|B_t|-1}\le2^{f+O(1)}\), and every basis has at most \(D_t\) vectors. There are at most \(2^{\ell+O(1)}\) live-switch assignments. Introduce/join/forget act by explicit deterministic linear maps on \(D_t\)-coordinate bit vectors; Gaussian elimination reduces the basis after each step in \(D_t^{O(1)}\) time. The \(m\) edge steps cost

\[
m\cdot2^{\ell+O(1)}D^{O(1)}\operatorname{poly}(S)=2^{O(f+\ell)}\operatorname{poly}(S).
\]

## 3. Why the method handles XOR

A width-two layered, read-once parity BP has two states at each layer, with the switch \(x_i\) controlling the two outgoing transitions between layers \(i\) and \(i+1\). The direct two-sink BP-to-LGS gadget in `research/6.1-winwin/williams.md` adds one permanent selected edge from the start to the reject sink and one permanently unselected edge between the sinks. Process the selected permanent edge first, and then the BP transition edges layer by layer, placing all occurrences of \(x_i\) consecutively. The host vertex frontier has constant size (two neighboring layers plus the sink/root), and only one switch is temporarily live. Thus \(w=O(1)\), giving a polynomial-time LGS solver.

By comparison, the cut-clause representation from branch J has minimum necessary clause width \(p\) for the same parity predicate. The new algorithm therefore genuinely overcomes the **specific** obstruction in J.


### Corollary: layered branching programs with many rereads

Suppose a layered *deterministic* BP has at most \(W\) vertices per layer and all outgoing transitions in layer \(j\) query the same variable \(x_{i_j}\) (an oblivious variable schedule). Let \(a\) be the maximum, over layer cuts, of the number of variables queried both before and after the cut. No bound on the total read count of one variable is required. Encode BP through the exact two-sink LGS gadget from `research/6.1-winwin/williams.md` and process its edges layer by layer, with permanent selected sink edge first. The vertex frontier is \(O(W)\) (the two neighboring state layers plus at most the two sinks), and the live switch frontier is at most \(a+1\). Hence **BP-SAT is deterministic in**

\[
2^{O(W+a)}\operatorname{poly}(S).
\]

This is polynomial for constant \(W,a\), and \(2^{o(p)}\operatorname{poly}(S)\) whenever \(W+a=o(p)\), even for length \(p^{100}\) and variables read a superconstant or polynomial number of times. The condition differs from constant syntactic read-\(k\), but should be compared carefully with classical automata/variable-elimination dynamic programming before claiming novelty.

## 4. Why this does NOT solve unrestricted LGS

The width can be \(\Omega(p)\) even for easy LGS predicates. Take \(K_{p,p}\), with left vertices \(a_1,\ldots,a_p\) and right vertices \(b_1,\ldots,b_p\), and label every edge \(a_ib_j\) by \(x_i\). Connectedness is equivalent to \(\bigwedge_i x_i\), a trivially easy predicate.

Nevertheless **every edge ordering has \(f\ge p\)**: at the first moment any vertex has had all its incident edges processed, call it \(v\). All \(p\) of its neighbors have had an incident edge processed; because \(v\) is the *first* completed vertex, none of those neighbors has finished its incident edges. Thus all \(p\) neighbors belong to the frontier.

This is not a hardness proof; it is a counterexample to bounding the joint frontier width of arbitrary LGS by \(o(p)\), even for easily solvable instances.

## 5. Hybrid with the short-cut method from J

The same \(K_{p,p}\) example is disposed of immediately by **unit cut clauses**: the cut at singleton vertex \(a_i\) gives the necessary clause \(x_i\). The H_C connectivity oracle in J detects each such clause in polynomial time; setting all switches to 1 leaves an obviously connected graph.

A sound hybrid algorithm is therefore:

1. Enumerate all width-one (or width-two) cut implicates using the J connectivity oracle, building necessary 1-CNF or 2-CNF \(F_k\).
2. If \(F_2\) is unsatisfiable, output NO. Substitute any variable values forced in all \(F_2\) solutions (optionally identify variables forced equivalent/opposite via 2-SAT implications). These substitutions preserve all LGS YES assignments, since every connected assignment satisfies \(F_2\).
3. Simplify constant edges, contract permanently active edges, and run the frontier-vector-space algorithm on a selected edge order of the residual instance.

If preprocessing leaves width \(w=o(p)\), this is an unconditional deterministic \(2^{o(p)}\operatorname{poly}(S)\) algorithm. There is no general guarantee that the residual width is small; the two easy classes merely show the **methods are complementary** (XOR: frontier method; large biclique AND: cut implication method). Finding a reduction measure that guarantees progress from either step is the next real research problem.

## 6. Checks, status, and next goals

Proof-of-concept Python implementation independently compared the cut-vector basis DP with full assignment enumeration on **3,000 random** labeled graphs with 2–6 vertices, 1–4 switches, up to 12 edges (including repeated edge identities, loops and constants), and on explicit two-state parity BP gadgets for \(p=1,\ldots,10\). All cases agreed, including all-false parity restrictions. This does not replace the correctness proof.

**Next serious tasks**: (A) characterize a natural graph/variable separation decomposition yielding a *provable* reduction of the width on unrestricted BP-derived instances; (B) combine local cut propagation with nonlocal **affine** reductions/equivalences of switches, not merely CNF; (C) find a general progress lemma for recursive assignment that yields a deterministic \(2^{p-\omega(\log p)}\mathrm{poly}(S)\) algorithm; (D) check literature for a prior explicit formulation of this particular joint vertex/switch frontier, as the underlying rank-based technique is established.

**Caveat:** Theorem K1 does NOT imply \(\mathrm{NEXP}\not\subseteq\mathrm{L/poly}\); that consequence requires an algorithm with the target time bound for **all polynomial-size LGS instances**, and the transfer in the 6.1 checkpoint requires a separate careful audit.
