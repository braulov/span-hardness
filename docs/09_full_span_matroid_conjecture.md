# Sparse (Co)Graphic Span-CSP (SCGS-CSP)

**Central structural candidate, not yet an ETH replacement.**

## Graphic and cographic duality
For a graph G with n vertices, m edges and c components, let M(G) be the binary cycle matroid, with r_M(E)=n-c. Its dual M*(G) has rank m-n+c. For A subseteq E,

r_M*(A)=|A|-r_M(E)+r_M(E\A).

In particular, for Y subseteq E:

Y is a forest  iff  r_M(Y)=|Y|  iff  r_M*(E\Y)=r_M*(E).

A cographic representation uses a cycle-space basis (the GF(2) kernel of graph incidence). It need not be explicitly sparse, but the graph supplies a sparse *implicit* description; size measurements must distinguish the two.

## Definition
SCGS-CSP is Boolean feasibility with O(n) variables and O(n) width-three clauses or bounded-fanin local gates, whose activation bits select elements of a graphic or cographic matroid (or their direct sum) of total sparse graph-description size O(n), and with one global requirement

r_M(Y)=r_M(E).

The parameter n counts *all* graph vertices, edges, Boolean variables and local gates/clauses, not just some convenient subset.

## FVS
Let x_v mean vertex v is retained, and Y={uv:x_u=x_v=1}. Activate A=E\Y in M*(G); equivalently a_uv=(NOT x_u) OR (NOT x_v). Requiring A to span M*(G) iff G[retained] is acyclic. Enforce |retained|>=n-k locally. Linear-size for sparse instances.

## Hamiltonian Cycle
On connected G with at least three vertices, choose edges y_e, enforce degree exactly two at every vertex, and require selected edges to span M(G). The selected 2-factor is connected iff it is a Hamiltonian cycle. The local degree constraints have linear total size on bounded-degree input.

## Root gadget for connectivity of selected vertices
For chosen nonempty S, introduce exactly-one root r_v, with r_v -> x_v. Add new hub h with original edges uv and spokes hv. Activate y_uv=x_u AND x_v; activate spoke hv when (NOT x_v) OR r_v. All excluded vertices connect to h, exactly one chosen root connects to h, and every other chosen vertex connects to h precisely via paths in G[S]. Thus the activated spanning graph is connected iff G[S] is connected.

Replace high-degree h by an always-activated binary tree with one leaf per v, to obtain O(n) extra vertices/edges and bounded degree when the original graph had bounded degree. This is a rigorous full-rank encoding for connected dominating set, connected vertex cover, node Steiner and connected FVS (combined via matroid direct sum).

## Star coverage
The star graphic matroid with a spoke for each universe element and activations by selected sets / satisfied clauses encodes Set Cover and CNF-SAT exactly. HOWEVER its representation can have many more than O(original-parameter) elements. It is not a fine-grained-preserving reduction for unrestricted Set Cover or arbitrary CNF.

## Composition
A direct sum M=M_1+...+M_t satisfies Y spans M iff Y meets every component in a spanning set. Any number of conditions can be conjoined if their total description cost stays O(n).

## Candidate Structural Hypothesis
The sparse, locally activated SCGS-CSP as above requires 2^{Omega(n)} in the weak asymptotic sense of no uniform 2^{o(n)} poly-size-time algorithm. This is neither a proved statement nor a published standard conjecture.

If false, a generic subexponential solver accelerates every natural P with P <=_lin SCGS-CSP. If true, hardness transfers only to targets Q for which SCGS-CSP <=_lin Q is shown. Reverse reductions are open.

## Algorithmic challenge
A uniform Boolean circuit of size O(n log^alpha n), alpha<1/2, for sparse activated graphic AND cographic full-spanning, plus the new fixed-width SAT algorithm, would refute the hypothesis. The implicit cographic representation cannot be expanded to a dense explicit basis for free.

## Cautions
Cographic cycle basis may be dense. Exactly-one-root must be encoded in linear size, not by all pairs. A binary root tree can increase degrees by one. Do not claim canonical completeness or novelty before a literature audit.