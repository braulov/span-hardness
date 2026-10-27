# M — Rainbow-partition certificates and matroid-nogood algorithms for LGS

**Research notebook, 2026-10-27.** Unconditional combinatorial claims, except explicitly labeled applications of the October 2026 proposed #SAT bound. No literature novelty claimed: matroid intersection, colorful/rainbow spanning tree criteria, SAT/2-SAT, and bounded-occurrence hardness are standard ingredients. This extends branches L, K, J and the original LGS/BP-SAT notes.

## 1. Removing all easy bipolar switches at once

Let a literal-controlled connected-graph instance have Boolean switches indexed by i and multigraph edges of types 0, 1, x_i, not x_i. Delete 0 edges. Fix every monopolar switch so all of its edges are active; it can be omitted (monotonicity of connectivity). Let **light** be switches with exactly one positive and one negative edge; let **heavy** be those with both polarities and at least three total occurrences. Let H be the heavy switch set, b=|H|.

Color both edge identities belonging to each light switch with the **same** color, and give every permanent edge and every heavy edge identity an **individual unique** color. For partial assignments alpha to heavy switches, delete the edges whose heavy labels are inconsistent with alpha and retain both polarities for unassigned heavy switches. Call the resulting edge-colored multigraph G_alpha.

Let R(alpha)=1 iff G_alpha has a **rainbow spanning tree**, meaning a spanning tree containing at most one edge of each color class. Matroid intersection (graphic and partition) decides R(alpha) and produces a tree/certificate in polynomial time.

**Lemma M1.** If R(alpha)=0, no completion of alpha can satisfy LGS. If alpha assigns all heavy switches, R(alpha) is equivalent to existence of a satisfying assignment to every switch. A rainbow tree is consistent in all light switches and with alpha in all heavy switches; its selected edges prescribe consistent switch values. Conversely every connected active graph contains a spanning tree, necessarily rainbow on every light pair. In unassigned heavy switches, R is a sound relaxation only; its positive answer does not guarantee a completion.

## 2. Exact multiway-partition inequalities

**Rainbow tree min–max theorem** (Schrijver/Suzuki; also Edmonds' matroid intersection): An edge-colored multigraph has a rainbow spanning tree iff for every partition pi of its vertices into q nonempty parts, at least q-1 distinct edge colors occur on edges crossing between parts.

Proof from matroid intersection: For an edge subset F, graphic rank is n-cc(V,F), partition rank of E\F is the number of colors represented in E\F. Edmonds' min–max formula for maximum common independent set size is

    min_{F subset E} [n - cc(V,F) + #colors(E\F)].

It reaches n-1 iff all values are at least n-1. If an n-way partition pi into q blocks violates the claimed color condition, take F to be all edges internal to its parts: cc(V,F)>=q and #colors(E\F) is the number of crossing colors, so the min–max quantity is <n-1. Conversely if F violates the min–max condition, choose pi to be the connected components of (V,F); all crossing edges lie in E\F and hence use at most #colors(E\F) colors. Thus the partition violates its threshold. QED.

For a partition pi of the original graph let:

* c_pi = number of available *light switch color classes* with >=1 crossing edge, plus the number of *permanently selected edge identities* crossing pi;
* a_i(pi) = number of positive edge identities of heavy switch i that cross pi;
* b_i(pi) = number of negative edge identities of heavy switch i that cross pi.

**Theorem M2 (exact Boolean linear inequality characterization).** The original LGS is satisfiable iff there exists x in {0,1}^H such that for EVERY partition pi into q parts,

    c_pi + sum_{i in H} [a_i(pi) x_i + b_i(pi)(1-x_i)] >= q-1.

For a partial assignment alpha the same inequality uses only the chosen side for fixed heavy switches and counts BOTH sides for free heavy switches. R(alpha) holds iff every partial inequality holds. Hence an unsuccessful matroid-intersection call can produce a violating multiway partition **whose threshold remains violated for every extension of alpha**. This is a polynomial-time certificate of a sound no-good partial assignment. A full heavy assignment is tested exactly.

This is a **separation oracle for the zero-one feasible assignments**, but not a polytime algorithm to FIND one, because the binary choices create NP-hardness.

## 3. Unconditional polynomial algorithm at matroid-nogood width <=2

For a complete heavy assignment x with R(x)=0, let

    mu(x) = min {|dom(alpha)| : alpha is a restriction of x, R(alpha)=0}.

Define kappa_MI(I)=max_{complete x with R(x)=0} mu(x), with 0 if all x are feasible. Clearly 0<=kappa_MI<=b; if R(empty)=0, the empty nogood certifies immediate UNSAT.

Enumerate every partial assignment alpha on at most k heavy switches (at most sum_{j=0}^k binom(b,j) 2^j), call matroid intersection R(alpha), and, for each false result, add the clause

    C_alpha = OR_{i in dom(alpha)} (x_i != alpha_i).

All such clauses are necessary: no genuine satisfying x can extend a failing alpha. If k>=kappa_MI(I), then their conjunction F_k is **pointwise equivalent** to LGS feasibility on all heavy assignments. Proof: any rejecting assignment has a failing restriction of size <=k, so falsifies C_alpha; every accepting assignment satisfies all learned clauses.

**Corollary M3.** For inputs with kappa_MI<=2, LGS is deterministic polynomial-time solvable by O(b^2) matroid-intersection calls followed by 2-SAT. Even if b=Theta(p), graph size S is p^100, and the ordinary graph vertex frontier is large. For each fixed k>=3, assuming the proposed October 2026 fixed-width SAT/#SAT algorithm, LGS with kappa_MI<=k has deterministic 2^{o(b)} poly(S) time; the number of generated clauses is polynomial in b for fixed k. This does **not** cover general LGS where kappa_MI may be b.

There is also a standard cutting-plane / counterexample-guided implementation: search for a heavy assignment satisfying learned clauses, test it via R, extract and greedily minimize a failing restriction, add its no-good, and repeat. This may require exponentially many rounds; no general speedup is claimed.

## 4. Sharpness: NP-complete already at kappa_MI<=3

Adapt the standard occurrence-3 SAT reduction in branch L. Given any 3CNF, make one fresh variable z_j per literal occurrence of each original variable z and add a cyclic sequence of implications (not z_j or z_{j+1}), requiring equal copies. For original variables appearing once, add the tautology (not z_1 or z_1) so its fresh variable also appears three times, in both polarities. Every resulting variable occurs **exactly three times** and has both signs. All clauses are width <=3, including the harmless 2-literal tautologies and the binary implications. Transform clauses into bundles of parallel literal-labeled edges along a path; the resulting LGS is satisfiable iff the original 3CNF.

All LGS switches in this reduction are heavy. Given any rejecting complete assignment x, some clause bundle is inactive. Fix the at most three switches occurring in this clause to the values of x; the bundle stays inactive regardless of other switches, so even the rainbow-tree relaxation R(alpha) is false. Hence mu(x)<=3 and kappa_MI<=3. This promise class is therefore NP-hard, while M3 gives P for kappa_MI<=2. The promise 'kappa_MI<=3' need not be efficiently recognizable; the reduction itself lies in the promise domain. LGS as a language with the promise is in NP.

This is a genuinely sharp **structural-parameter algorithmic boundary**, not a solution to unrestricted LGS.

## 5. Why the partition inequalities do not yield a free LP algorithm

Consider four 2-clauses:

    (x or y) & (x or not y) & (not x or y) & (not x or not y).

Their conjunction is unsatisfiable. Encode them as four consecutive parallel edge bundles on a 5-vertex path. Both variables appear twice in each polarity (heavy). At the fractional setting x=y=1/2, **every bundle has total fractional crossing-edge capacity exactly 1**. For any vertex partition into q parts, at least q-1 path *positions* cross its blocks, so the total fractional capacity of all crossing edge identities is >=q-1. Therefore x=y=1/2 satisfies **all** naive fractional relaxations of M2, although no Boolean solution exists. Exhaustive check: all 52 partitions of five vertices pass. Thus ordinary LP separation over these multiway inequalities is insufficient; an integrality/cutting-plane advance is required.

The parity BP gadget of branch J yields another obstruction: its acceptance predicate has accepting extensions for *every* strict subcube of {0,1}^b, so R(alpha) is YES on all such subcubes (because a genuinely accepting extension is present). Its rejecting full assignments therefore have mu(x)=b, provided every BP input remains heavy in the gadget. Hence only asking R on short partial assignments cannot resolve parity, though branch K's frontier algebra handles the same parity program efficiently. Global graph structure beyond the R-oracle remains essential.

## 6. Experimental checks and honest next work

A self-contained script `verify_matroid_partition_oracle.py` verifies the rainbow spanning tree iff partition inequalities for 770 partial heavy assignments sampled from 350 random small LGS multigraphs. It also cross-checks R(x) against original brute-force LGS SAT for complete heavy assignments. An explicit unsatisfiable 4-clause path passes all 52 partition inequalities at x=y=1/2. All checks passed. Test execution does not verify the external matroid-intersection theorem.

**Next target:** replace plain no-good clauses by the stronger pseudo-Boolean inequalities delivered by violating multiway partitions, and investigate how to combine them with the frontier cut-vector DP of branch K **without losing parameter independence from graph description size S**. Find a branching measure that guarantees savings over 2^b on broad polynomial-size instances, or prove a precise obstruction. Full polynomial-size LGS 2^{o(p)} poly(S) remains open, so there is still **no** NEXP not subseteq L/poly theorem from this research.

Sources: rainbow spanning tree criterion https://cs.du.edu/~paulhorn/pap/rain.pdf (Theorem 2); matroid intersection literature and its colored-spanning-tree corollaries https://www.sciencedirect.com/science/article/pii/S0166218X1000435X ; bounded-occurrence 3SAT C. Tovey, Discrete Applied Mathematics 1984, DOI 10.1016/0166-218X(84)90081-7.