# O — LGS to Set Cover: exact cut reduction, size barrier, and the real post-ETH targets

Research checkpoint, 2026-10-28. **Status:** the cut-to-cover reduction and the limitations of that specific reduction are proved. A general parameter-preserving LGS(p,S) -> Set Cover(u=O(p), t=poly(S)) reduction is **NOT found**; no theorem is claimed to exclude all such reductions. User specifically asks to verify possible subexponential Hamiltonian Cycle / Subgraph Isomorphism algorithms before using HC as a hardness survivor.

## 1. Status and literature corrections

- General undirected Hamiltonian Cycle on arbitrary n-vertex graphs: our October 2026 searches did NOT confirm a 2^{o(n)} algorithm. Hamiltonian Cycle is an instance of Subgraph Isomorphism with cycle pattern C_n; Hamiltonian Path uses P_n. General subgraph-isomorphism algorithms with O*(2^{O(k)}) time for a path pattern are **not** subexponential in k. Restricted graph classes can have 2^{o(n)} algorithms, e.g. fat-object geometric intersection graphs in fixed dimension: Marin–Raymond–Watrigant, SoCG 2026, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2026.77 .
- Koana and Kumabe (arXiv:2609.39062, revised 2026-10-16) give randomized O*(1.9133^n) for **directed** HC, which remains 2^{Theta(n)}.
- Krauthgamer–Trabelsi, STACS 2019 https://doi.org/10.4230/LIPIcs.STACS.2019.45 give quantitative reductions connecting Set Cover conjectures and tree-pattern Subgraph Isomorphism (including directed Hamiltonicity consequences). The reported gain is (2-eps)^n, **not** 2^{o(n)}.
- SeCoCo (Set Cover Conjecture, bounded set size) says: for every epsilon>0 there exists a fixed k such that no O*((2-epsilon)^u) algorithm solves k-Set Cover on a u-element universe. It is *different* from our desired hardness against 2^{o(u)} for unrestricted Set Cover.
- Björklund–Kaski, STOC 2024 https://doi.org/10.1145/3618260.3649656, and Pratt, STOC 2024 https://doi.org/10.1145/3618260.3649620: SeCoCo implies explicit tensor families with asymptotic rank > N^{1.08}; equivalently, Strassen's asymptotic rank conjecture and SeCoCo cannot both hold. This is a genuine already published **truth-side algebraic lower-bound consequence**, but it does NOT prove NEXP circuit lower bounds upon falsifying SeCoCo.
- OpenAI's October 2026 exact fixed-width #SAT theorem has a posted Lean scope and pending independent human review. We use it as a **conditional premise**, not as an independently validated theorem: https://github.com/openai/math/blob/main/lean/docs/378.md .

## 2. The exact direct LGS -> Set Cover reduction

Input: an undirected connected multigraph G=(V,E), p independently assigned switches x_1,...,x_p, edge labels in {0,1,x_i,not x_i}. Denote E^+_i and E^-_i the edge identities with those variable labels; E_1 is the set of always-active edges.

Let \(\mathcal C\) consist of all nontrivial unordered vertex cuts \(\{U,V\setminus U\}\) that are NOT crossed by an always-active edge, and let \(\mathcal C_{\text{nt}}\) be their non-tautological distinct OR-clauses over edge literals (discard zeros; cuts with both signs of a switch are tautologies). A clause may be empty, in which case the LGS instance is immediately NO.

Create a Set Cover universe
\[
\mathcal U=\{d_1,\ldots,d_p\}\cup\{c_C:C\in\mathcal C_{\mathrm{nt}}\}.
\]
For each i and b in {0,1}, create ONE candidate set \(S_{i,b}\) containing d_i and all clause-elements c_C with literal \(x_i\) (b=1) or \(\neg x_i\) (b=0) in C. Set budget k=p.

**Theorem O1.** The LGS instance is YES iff the Set Cover instance admits a cover by at most p sets. Proof: each d_i is contained only in its two sets. Covering all p distinct d_i within budget p forces EXACTLY one choice of S_{i,0},S_{i,1} for each i. Clause-elements are then covered iff the corresponding literal disjunction is true. All such cut clauses hold iff every nontrivial cut has an active edge, iff G_x is connected. QED.

This reduction has:
- universe u=p+h, where h=#distinct relevant cut clauses;
- exactly t=2p candidate sets;
- set cardinality potentially Theta(h), **not bounded by a fixed constant**;
- construction time poly(S)*2^{c-1} by enumerating all cuts after contracting the components of the always-active subgraph, where c=#those components (including isolated vertices).

Here h<=min(2^{c-1}-1,3^p), but **h can be exponential in p**, so O1 does NOT solve the desired general reduction.

A forest/tree host has only singleton bridge cut requirements, and thus at most 2p distinct nonconstant clause labels after deduplication. Its LGS has a polynomial-time direct Set Cover reduction with u<=3p (and of course is also directly polynomial-time solvable). More generally, if c<=floor(log_2 p)+O(1), the full cut enumeration gives u=O(p) and polynomial reduction. If an efficiently enumerable cut family of h=O(p) distinct necessary clauses suffices for all connectivity obstructions, the same parameter-preserving construction applies.

Combining branch J's short-cut oracle: for each fixed k, enumerate all clauses on at most k literals (at most O(p^k) candidates), retain C exactly when deleting edges with labels in C disconnects the host. If every disconnected assignment violates such a retained clause and there are h=O(p) retained distinct clauses, the resulting Set Cover universe has u=p+h=O(p), in polynomial construction time. These are explicit sufficient **structural promises**, not a universal sparsification theorem.

## 3. A provable obstruction for THIS cut-cover representation: parity

Let f(x)=x_1 XOR ... XOR x_p. Polynomial-size (indeed O(p)) deterministic width-two branching programs compute this predicate, and the 6.1 two-sink construction produces LGS of size O(p) with \(G_x\) connected iff f(x)=1.

**Lemma O2.** Every CNF formula on the original p inputs, with NO auxiliary variables, representing odd parity has at least \(2^{p-1}\) distinct clauses.

Proof: every clause implied by odd parity must mention ALL p variables. Otherwise fixing fewer than p variables to falsify it leaves a free bit and hence admits an odd-parity completion, contradicting validity. A non-tautological full-width clause is falsified by exactly one assignment. All \(2^{p-1}\) even-parity assignments must falsify at least one clause, so at least \(2^{p-1}\) clauses are necessary. QED.

Every nontrivial cut is a clause on the original inputs. Thus the **direct** cut-cover reduction O1, even after removing tautologies/duplicate clauses, needs h>=2^{p-1} universe elements on the parity-BP LGS gadget. It cannot yield u=O(p) on all LGS, not even on an LGS family with O(p) graph size.

This does NOT prohibit more clever Set Cover reductions with auxiliary candidate-set choices, a different budget or gadgets. Indeed a standard parsimonious Tseitin representation of a parity circuit introduces O(p) auxiliary gates and clauses; mapping THAT formula to Set Cover creates O(p) universe elements. The obstruction is to direct cut enumeration only, not to polynomial reductions on parity.

## 4. Why the desired full reduction is genuinely hard

General CNF-SAT with p original variables and L literal occurrences embeds **pointwise** into LGS with p switches and O(L) graph objects: make a path of clause-bundles, one parallel edge per literal in each clause. The active graph connects iff every clause has a true literal. Width and clause count may grow polynomially in p.

Hence any general LGS(p,S) -> SetCover(u=O(p), t=poly(S)) reduction also yields a p-variable arbitrary-width CNF-SAT -> SetCover on O(p) universe elements for polynomial m. That would resolve a significant open compression issue in exponential-time complexity; no such theorem is established here. It still would NOT automatically yield bounded-k SeCoCo consequences because the produced sets might each have size Omega(p) and bounded-universe versus bounded-*set-size* are distinct promises.

Compression lower bounds (Fortnow–Santhanam / Dell–van Melkebeek) prohibit some strongly size-bounded polynomial-time compressions, but do NOT immediately rule out this target: the number of output sets / total description length is allowed to grow polynomially in the source size S, not in p with one universal fixed exponent, and subexponential many-query transformations are a further escape route. See inherited branch N for exact warnings.

A second serious complication: p-bit parity requires exponentially many direct cut clauses, even though an auxiliary-variable CNF has only O(p) clauses. The target Set Cover reduction must introduce auxiliary set choices that globally coordinate intermediate computation while keeping the universe O(p). This is the succinctness problem rather than merely an inefficient cut enumeration.

## 5. The exact ETH-like conditional win-win remains OPEN

If there is a deterministic SERF-style reduction for every fixed source polynomial size S=p^{O(1)} from LGS(p,S) to ordinary Set Cover(u<=Cp,t=poly(S)) using at most 2^{o(p)} poly(S) total work/queries, then any deterministic 2^{o(u)} poly(t) Set Cover algorithm yields deterministic 2^{o(p)} poly(S) LGS-SAT. The input-efficient LGS algorithm would then, under the independently audited easy-witness/Williams transfer from 6.1, imply NEXP not subseteq L/poly. Conversely, if H_L asserts no such fast deterministic LGS algorithm, its truth would imply the nonexistence of a fast **unrestricted** universe-parameter Set Cover algorithm.

No such general reduction has been constructed. This is separate from the established SeCoCo -> tensor asymptotic-rank lower bound, and no claim is made to unify the two.

## 6. Precise next experiment

Explore replacing the exponentially many cut-elements of O1 by O(p) **auxiliary consistency / computation elements**:
- choose O(p) clause tests that suffice after adding auxiliary set choices;
- parameterize by a succinct cut-CNF extended formulation (not direct CNF);
- test the construction first on width-two parity BP (where direct cut encoding fails but O(p) auxiliary gates suffice);
- then attempt growing-width/length branching programs and track the universe U, number of sets t, budget k, and actual time;
- avoid asserting a win-win from only a one-way encoding into SCGS.

Maintain a sharp distinction among fixed k-Set Cover, arbitrary-set-size Set Cover, and t-limited number-of-sets regimes.

### References

1. https://doi.org/10.4230/LIPIcs.STACS.2019.45 (Krauthgamer–Trabelsi, STACS 2019)
2. https://doi.org/10.1145/3618260.3649656 (Björklund–Kaski, STOC 2024)
3. https://doi.org/10.1145/3618260.3649620 (Pratt, STOC 2024)
4. https://borowiecki.dev/abs/2609.39062 (Koana–Kumabe, directed HC, October 2026 revision)
5. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2026.77 (restricted geometric HC)
