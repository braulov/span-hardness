# LGS: variable-interface width, structural obstruction, and exact DP

Research checkpoint — 2026-10-29. Proofs below are elementary deductions and should not be advertised as novel without a literature review. LGS means: each graph edge has a label 1, x_i, or ¬x_i; decide whether some Boolean assignment activates a connected spanning graph. Parameter p counts distinct Boolean variables, S counts graph vertices/edges and label occurrences.

## Proposition 1 — constant-width graph obstruction

For every CNF formula F with clauses of size at most 3, construct a labeled graph G_F with 6m vertices and at most 8m−1 edges (m clauses), such that for every assignment x:

    G_F[x] is connected iff F(x) is true.

For each clause j create two three-vertex paths a_{j,1}−a_{j,2}−a_{j,3} and c_{j,1}−c_{j,2}−c_{j,3}, all edges permanent. Link a_{j,3} to a_{j+1,1} permanently. For the k-th literal of clause j add the switchable rung a_{j,k} c_{j,k}, labeled by that literal. Clauses shorter than three simply omit rungs. The permanent top path joins all a-vertices. The bottom clause paths are disjoint and each joins the top iff some literal in its clause is true. Thus connectivity is equivalent to satisfying every clause.

Properties:
* All switchable edges form a matching.
* Permanent edges induce one global path plus one independent length-two path per clause.
* Maximum degree is at most three; the graph is outerplanar.
* Pathwidth is at most two. For each ladder block use bags {a1,a2,c1}, {a2,c1,c2}, {a2,a3,c2}, {a3,c2,c3}; between blocks add {a_{j,3},a_{j+1,1}}. This is a valid path decomposition of width 2.
* Number of primary Boolean variables is unchanged.
* Using bounded-occurrence 2/3-CNF-SAT (Tovey 1984), NP-hardness holds when each variable labels at most three edges. CAUTION: *exactly* three literals per clause with each variable occurring at most three times is always satisfiable, so allow two-literal clauses.

Therefore ordinary pathwidth, degree, and structural edge cut size cannot alone provide a polynomial-time algorithm for general LGS unless P=NP. This is NOT an ETH lower bound and does not rule out 2^{o(p)} algorithms.

## Proposition 2 — augmented graph width and exact rank-based DP

Contract the components of permanently active edges to obtain Q. Let X be variable nodes. Form the augmented primal graph A on V(Q)∪X, adding the triangle {u,v,x_i} for every switchable uv labeled x_i or ¬x_i. Put t=tw(A).

Given a width-t decomposition, LGS is solvable deterministically in 2^{O(t)} poly(S) time, using standard rank-based connectivity DP. At a bag, let b be the number of graph vertices and q the number of variables. For each assignment to live variables, store a representative family of partitions π of the b graph vertices recording connectivity via processed active edges. Prevent premature completion of components (or keep a distinguished root in all bags).

The cut-vector C_π∈GF(2)^{2^{b−1}} is indexed by subsets of the b boundary vertices containing a fixed root; C_π(S)=1 iff S is a union of blocks of π. Then

    <C_π,C_σ> = [π∨σ is the one-block partition] mod 2.

Indeed the number of cuts simultaneously compatible with π and σ equals 2^{#blocks(π∨σ)−1}. A row basis of the cut vectors represents all possible completions, leaving at most 2^{b−1} representatives per assignment to q live variables; total ≤ 2^{b+q−1}=2^{O(t)}. The standard introduce/forget/join routines retain this property after rank reduction; polynomial overhead per state gives 2^{O(t)} poly(S).

For the CNF encoding in Proposition 1, contraction of permanent paths leaves a hub r and one node for each clause. After adding variable vertices, A−r is exactly the CNF clause-variable incidence graph (up to duplicate occurrences). Thus the correct structural width tracks variable correlations, not the source graph alone.

## Proposition 3 — exponential interface *rank* despite tiny graph separator

For each bit vector a∈{0,1}^p, let L_a be a connectedness gadget representing the conjunction of p unit clauses that force x=a. Build R_b analogously. Join their permanent backbones by a single permanent bridge. There exists an assignment making the union connected iff a=b. Thus the matrix of compatibility of gadget families is I_{2^p} and has rank 2^p over every field. This rules out a generic polynomial-rank linear-separable interface with only the one boundary graph vertex.

IMPORTANT: This does not prove a computational lower bound or forbid succinct symbolic encodings: equality itself has a compact expression and is easy to check. It is a format-specific obstruction.

## Complementary algorithmic regime

For variables whose *remaining* nontrivial occurrence set contains no opposing polarity, activate all their edges permanently. Let b_3 be the number of remaining mixed-polarity variables occurring on ≥3 edges. Branch over these b_3 variables; after fixing them, every remaining mixed-polarity variable has at most one positive and one negative occurrence. A spanning-tree basis can then be selected with a partition-matroid restriction (at most one of each opposite pair), so matroid intersection solves each branch in polynomial time:

    T = 2^{b_3} poly(S).

This can be much smaller than 2^{O(t)} even for high-width variable-incidence graphs.

## Research implication

The hard regime for a universal 2^{o(p)} poly(S) algorithm needs *both* large effective mixed-polarity repetition and large variable-augmented treewidth. A useful next attack is to find a representation of globally reused switching variables that stays small under gluing even when the cut-vector/partition representation and matroid-intersection simplifications are insufficient.

No universal subexponential-in-p algorithm or circuit lower bound is claimed.

## Checked computations

A Python brute-force experiment compared satisfaction of 52,920 (formula, assignment) pairs to connectivity of the corresponding labeled graph (p,m≤6). All agreed. Explicit pathwidth-2 bag sequences were checked through m=14. This is supporting validation, not a proof of complexity claims.

## Literature checkpoints

- Tovey, A Simplified NP-Complete Satisfiability Problem (1984): https://www.sciencedirect.com/science/article/pii/0166218X84900817
- Bodlaender, Cygan, Kratsch, Nederlof, Deterministic Single Exponential Time Algorithms for Connectivity Problems Parameterized by Treewidth (Information and Computation 2015): https://doi.org/10.1016/j.ic.2014.12.008
