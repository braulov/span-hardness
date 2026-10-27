# L — Occurrence threshold for LGS via matroid intersection

Research checkpoint, 2026-10-27. Research objective: deterministic algorithms for literal-controlled graphic full-span, independent of (randomized) rank-isolation and of the October 2026 #SAT announcement. **No claim of literature novelty**: the polynomial case is the standard spanning tree with disjoint conflict pairs, solvable by matroid intersection; the occurrence-three hardness corresponds to Tovey's classic bounded-occurrence SAT constructions. This note combines them in the LGS formalism and gives a broad FPT generalization.

## 1. Spanning-tree consistency characterization

In LGS, an undirected multigraph G=(V,E) has edge labels in {0,1,x_i,not x_i}. Each assignment activates its true-labeled edges. Let E_i^+ and E_i^- be edge identities labeled x_i and not x_i.

**Lemma 1 (unconditional).** An LGS instance is satisfiable iff it has a spanning tree T with no selected edge labeled 0 and, for every i, NOT BOTH (T intersects E_i^+) and (T intersects E_i^-).

Proof: From any satisfying assignment, choose a spanning tree of its active graph, which has no conflicting labels. Conversely, the selected edges of any consistent spanning tree prescribe at most one truth value for each switch; extend these requirements arbitrarily to a full assignment. Every edge of T becomes active; extra active edges cannot destroy connectivity. Handles graph loops, parallel edges, and labels 1. If |V|=1 the empty tree suffices. QED.

This is graphic-matroid basis feasibility with a **conflict graph** on edge identities: two edges conflict when their labels are opposite polarities of the same switch. Its connected components are complete bipartite graphs K_{|E_i^+|,|E_i^-|}, possibly with isolated edges.

## 2. Polynomial tractability for at most two *bipolar* occurrences

A variable is MONOPOLAR if all its appearances have the same sign. Set every monopolar switch so ALL its labeled edges are active; this cannot turn a YES into a NO because graph connectivity is monotone in enabled edges. These edges may now be treated as label 1, no matter how many times a monopolar switch appears.

A variable is LIGHT BIPOLAR if it has exactly one positive-labeled and one negative-labeled edge identity. Every such variable contributes one forbidden pair of edge identities. The pairs for distinct switches are edge-disjoint. Build:
- Graphic matroid M_G: edge subsets forming forests on V.
- Partition matroid M_P: each opposite-polarity pair is one capacity-one block; each other available edge is a singleton capacity-one block. Label-0 edges are deleted. Monopolar/label-1 edges have singleton blocks.

**Theorem 2 (unconditional).** When every bipolar switch has precisely one appearance per polarity, LGS decision and witness construction are polynomial-time: find a maximum common independent set of M_G and M_P via Edmonds' matroid intersection, and accept iff its size is |V|-1.

Proof: Every common independent set is a forest containing no forbidden pair. If it has |V|-1 edges, it is a compatible spanning tree, so Lemma 1 gives a satisfying assignment. Conversely, Lemma 1's compatible spanning tree is independent in both matroids. The independence oracles are polynomial-time (DSU for graphics, group counters for partition), so matroid intersection is polynomial-time. QED.

In particular, at most TWO occurrences per switch => P, regardless of graph size/edge order/frontier width. The theorem also holds for **full-spanning of any polynomial-time independence-oracle matroid** in place of the graphic matroid, by finding a basis in its intersection with the same partition matroid; it is not limited to graphs.

Special cases with an unbounded number of occurrences of a monopolar variable are already solved: those variables are simply fixed to activate all their edges.

## 3. FPT via the number of genuinely hard switches

Let

  b = |{i: E_i^+ != empty, E_i^- != empty, |E_i^+|+|E_i^-| >= 3}|.

**Theorem 3 (unconditional).** Arbitrary LGS is solvable in time 2^b * poly(S), with a constructive witness, for this parameter b.

Proof: Fix monopolar switches greedily as in Theorem 2. Enumerate all 2^b truth assignments to the remaining HEAVY BIPOLAR switches. In each branch, discard their false-labeled edges and treat their true-labeled edges as constantly active; now every remaining switch is light bipolar. Apply Theorem 2's polynomial-time matroid-intersection procedure to the residual instance. By Lemma 1 and exhaustive consideration of the heavy switches, one branch is YES iff the original instance is YES. Output the assignment recovered from a common basis. QED.

Therefore b=o(p) yields **unconditional deterministic** 2^{o(p)} poly(S) even when S=p^{100} and the host graph's frontier width is Omega(p). This algorithm is complementary to branch K: a parity BP can have b=Theta(p) but tiny joint frontier width, whereas a biclique with one monotone switch per left vertex has b=0 but may have frontier width Omega(p).

This is a simple "distance to matroid intersection" parameter, not a claimed novel FPT result.

## 4. NP-completeness already at three appearances, on path multigraphs

**Theorem 4.** LGS-SAT is NP-complete even when (i) every switch appears on at most THREE edges, (ii) the underlying simple graph is a PATH (consecutive vertices only), (iii) every parallel bundle has at most THREE edges, and (iv) labels are literals (no constants). Thus the two-versus-three occurrence distinction is sharp, notwithstanding the P special cases.

Proof: Start with arbitrary 3CNF. For every occurrence of an original variable z, introduce a separate copy z_j, keeping the original sign in the original clause. For a variable with d>=2 occurrences, enforce all its copies equal by adding the cyclic implication clauses (not z_j OR z_{j+1}) for j modulo d. A directed cycle of implications forces all copies to agree (either all zero or all one), so the transformed CNF is equisatisfiable. Each copy appears once in an original (<=3)-clause, once as antecedent (negative) in one implication, and once as consequent (positive) in another; it appears at most three times. Each clause is nonempty and width at most three.

For transformed clauses C_1,...,C_m, create graph vertices v_0,...,v_m and one parallel edge v_{j-1}v_j labeled l for each literal l in C_j. The active graph is connected precisely if every consecutive bundle has at least one active edge, i.e., iff all clauses are true. Thus satisfiability is preserved. Number of edges/vertices is linear in the transformed CNF size. NP membership follows from testing connectivity after guessing the switches. QED.

This is a direct reformulation of the bounded-occurrence SAT reduction of C. A. Tovey, "A simplified NP-complete satisfiability problem" (Discrete Applied Mathematics 8(1), 1984), DOI https://doi.org/10.1016/0166-218X(84)90081-7 . The all-three-literal 3SAT-with-max-3-occurrences variant has additional restrictions; Tovey's point is that SAT with clauses of sizes 2 and 3 remains NP-complete when max occurrences is 3. Do NOT conflate this with exact-3-CNF.

A complementary perspective: in this hard subclass the edge-conflict graph is a vertex-disjoint union of single edges K_1,1, paths K_1,2, and isolated edges (since each switch appears at most three times). Hence even a FORBIDDEN-EDGE conflict graph that is a collection of short paths has NP-hard spanning tree feasibility. A matching conflict graph, on the other hand, gives the partition-matroid intersection algorithm.

## 5. Verified algorithms and experiments

- Implemented the standard augmenting-path matroid-intersection method with graphic/partition independence oracles (on outside->inside arcs use **partition** exchange feasibility; inside->outside use **graphic** exchange feasibility when sources mean graphic-addable and targets mean partition-addable). Reversing those arc labels is incorrect; this was caught by a failing assertion and corrected.
- Compared the resulting decision procedure with brute-force assignment evaluation on 2,500 seeded random LGS multigraph instances, 1–7 vertices and 0–4 switches, each switch appearing at most twice. **All passed after correcting the exchange graph orientation.**
- Tested the variable-splitting reduction on 800 random CNFs with clause width <=3 and up to four source variables; exhaustive satisfiability of the original and transformed formulas agreed in all cases. A graph consisting of the corresponding parallel bundles realizes precisely the transformed CNF.

The finite tests do not constitute proof or priority evidence. The tests exist as local Python scripts, with source in the research working environment; rigorous correctness follows from the lemmas above.

## 6. What this says about the NEXP goal

These theorems do NOT yield a deterministic 2^{o(p)} poly(S) algorithm on all polynomial-size LGS. Indeed, the reduction in Theorem 4 produces NP-complete instances with b=Theta(p) even on an underlying simple path, whereas the width method from K has potentially Omega(p) live switches due to nonlocal occurrences.

Thus unrestricted LGS requires new methods handling **many genuinely bipolar, multiply occurring switches**, not just graph topology. A promising analytic next step is to combine matroid-intersection preprocessing (which handles all light bipolar switches exactly) with:
- the joint vertex/switch frontier DP (K);
- global cut-implicate propagation (J);
- a nontrivial branching recurrence in which each heavy switch assignment provably makes more progress than reducing b by one.

Because the 2026 exact #SAT theorem is provisional, distinguish conditional RP subexponential algorithms on size O(p) from these unconditional decision results.

## Sources and priority warning

- Conflict-pair spanning tree via matroid intersection was studied explicitly in "Paths, trees and matchings under disjunctive constraints" (2011), https://www.sciencedirect.com/science/article/pii/S0166218X1000435X ; disjoint conflict pairs are a standard polynomial case.
- Tovey (1984), cited above.
- General matroid intersection references: https://sites.math.washington.edu/~rothvoss/514-fall-2022/matroidintersection.pdf .
- Bounded-read BP-SAT: Nagao–Seto–Teruyama (2017), https://doi.org/10.4230/LIPIcs.ISAAC.2017.58 .
