# LGS algorithms — focused research handoff (2026-10-27)

## What to read, in order

This branch is **based on** \`research/H-derandomization-algorithms\`, which itself is based on \`research/6.1-winwin\`; all inherited files are present in the branch.

1. [The core BP -> literal graphic full-span construction and Williams consequence](../6.1-winwin/williams.md), especially §§4–7, Lemma 6, Theorem 10, and the exact quantifiers on \(p,S\).
2. [Algorithmic research checkpoint](../6.1-winwin/research_checkpoint_ru.md), especially §11 and the parameter ledger in §§3, 9, 12.
3. [Parity lifts](../6.1-winwin/parity_rank.md), especially the primal graphic witness.
4. [Branch H's bounded-deficiency deterministic exact counting](../H-derandomization-algorithms/derandomization_and_matrix_lifts.md).
5. This document, then [CLAUDE_TASK.md](CLAUDE_TASK.md).

The user's goal is **an algorithm for LGS**, not new hardness conjectures. A sufficiently fast deterministic algorithm for polynomial-size LGS/BP-SAT would imply a strong nonuniform lower bound; the implication in the checkpoint is a *research claim with a detailed argument*, not independently peer reviewed.

## Formal target

**Literal Graphic Span-SAT (LGS)**: connected undirected (multi)graph \(G=(V,E)\) with \(S=|V|+|E|\) and each edge \(e\) labeled by \(0,1,x_i,\neg x_i\), for \(p\) independent Boolean switches \(x_1,\ldots,x_p\). Given \(x\), activate exactly those edges whose labels are true. Decide whether some \(x\) makes the active graph connected (equivalently full rank in graphic matroid of \(G\)). No unrestricted activation circuits and no free extra existential bits.

**Dream target:** deterministic \(2^{o(p)} S^{O(1)}\) for every polynomial relation \(S=p^{O(1)}\), uniformly for each fixed polynomial bound, or a strong enough \(2^p/p^{\omega(1)}\) improvement satisfying an exact Williams-style transfer. Do **not** confuse \(2^{o(S)}\) with \(2^{o(p)}\).

Literal LGS includes BP-SAT by a precise linear-size input-preserving reduction; BP-SAT includes arbitrary CNF formula evaluation by sequential scanning, with the same \(p\) and size proportional to literal occurrences. Therefore \(p\)-only progress is significantly harder than the sparse-total-size result. Whether an intermediate saving transfers to \(\mathrm{NEXP}\not\subseteq\mathrm{L/poly}\) must be proved with correct uniformity and hypotheses. The straightforward sufficient implication in the checkpoint is \(2^{o(p)} S^{O(1)}\) **deterministic** LGS-SAT \(\Longrightarrow \mathrm{NEXP}\not\subseteq\mathrm{L/poly}\).

## New observation for the BP reduction: deficiency is ALWAYS 0 or 1

The proof in \`williams.md\`, Lemma 6, builds an active forest of exactly two components (accept and reject sinks) plus the permanent selected edge \((s,r)\), where \(s\) is the BP start and \(r\) its reject sink. A never-selected edge \((a,r)\) (accept and reject sinks) connects the *ground* graph, without changing active choices. For every input \(x\),

\[
d(x):=r_G(E)-r_G(Y(x))=
\begin{cases}
0 & B(x)=1\\
1 & B(x)=0.
\end{cases}
\]

Use an anchored graphic witness: binary vertex potentials satisfying equality across active edges, one original ground anchor fixed at zero. For each \(x\), it has exactly \(2^{d(x)}\) extensions. If \(M\) is the number of solutions of the resulting **unweighted #3CNF**, after parsimonious Tseitin encoding,

\[
M=\#B^{-1}(1)+2\#B^{-1}(0)=2^{p+1}-\#B^{-1}(1).
\]
Therefore \(\#B^{-1}(1)=2^{p+1}-M\): exact **deterministic** BP counting, using **one** #3SAT call of \(q=O(S+p)\) variables and \(O(S+p)\) clauses, conditional on the October exact-counting theorem. More generally, the bounded-deficiency moment algorithm applies.

**Important non-novelty check:** a polynomial-size BP is already a size-\(O(S)\) Boolean circuit by bottom-up evaluation of DAG nodes, and a parsimonious Tseitin encoding also yields #3SAT with \(O(S)\) auxiliary variables. The rank identity is structurally neat, but **does not yet beat the obvious \(O(S)\)-variable conversion or give any \(p\)-only speedup**. Do not claim otherwise.

For \(S=O(p\log^\alpha p)\) with fixed \(\alpha<1/2\), this is nonetheless a conditional deterministic \(\#\mathrm{BP}\)-SAT algorithm with time \(2^{o(p)}\operatorname{poly}(S)\), using the manuscript's sparse #3SAT bound \(2^{O(q/\sqrt{\log q})}\) or its documented weaker Lean bound with polyloglog factors. For arbitrary polynomial \(S=p^k\), the reduction falls far short.

## Existing SAT/BP-SAT work to check before claiming novelty

- Makita, Nagao, Okada, Seto, Teruyama, *A Satisfiability Algorithm for Deterministic Width-2 Branching Programs* (2022): \(\mathrm{poly}(p)2^{(1-\mu(c))p}\) for width two and size \(cp\), \(\mu(c)=2^{-O(c\log c)}\). https://doi.org/10.1587/transfun.2021EAP1120
- Nagao, Seto, Teruyama, *SAT for Syntactic Read-k Branching Programs* (ISAAC 2017): \(2^{(1-\mu(k))p}\) for constant syntactic reads, with other factors. https://doi.org/10.4230/LIPIcs.ISAAC.2017.58
- Kabanets–Kolokolova, *Compression of Boolean Functions*, 2013: #SAT / compression for restricted roughly quadratic-size branching programs. https://eccc.weizmann.ac.il/report/2013/024/
- Abboud, Hansen, Vassilevska Williams, Williams, *Simulating Branching Programs with Edit Distance and Friends* (STOC 2016), on BP-SAT to P problems and conditional circuit consequences. https://doi.org/10.1145/2897518.2897653
- Williams, *Improving Exhaustive Search Implies Superpolynomial Lower Bounds*, Theorems 1.1 and 6.1, and *Non-Uniform ACC Circuit Lower Bounds*: check exactly what BP-SAT savings permit, whether deterministic/co-nondeterministic is needed, and constants/uniformity. https://people.csail.mit.edu/rrw/improved-algs-lbs2.pdf

**New 2026 theorem premise is provisional.** OpenAI's exact fixed-width #SAT result is posted and formalized, but external review is ongoing; stronger sparse-rate statement in the manuscript and weaker verified-formulation rate must be distinguished. Never conflate a public claim, a Lean formal statement, and independent endorsement.

## Candidate algorithmic lines

1. **Input-efficient compilation of BP-SAT to #SAT:** preserve dependence on \(p\), allowing poly(S) clauses but only \(q=O(p\,\mathrm{polylog}^{<1/2}p)\) existential variables. Audit information barriers: predicate-preserving \(p\)-input O(p)-object encodings have counting obstacles, and all polynomial-size BP predicates encompass nonuniform logspace. Is SAT-only or many-query compilation possible?
2. **Matrix products / Fourier / semiring techniques:** encode accept as a reachability of active edges or product of literal-controlled transition matrices; exploit shared variable dependencies without expanding one gate per BP state. Try algebraic block decompositions, Möbius transforms and multilinearization, low-rank transfer operators.
3. **Restriction/decomposition methods:** generalize SAT algorithms for width two, bounded-read, oblivious/ordered BP, bounded interaction width. Establish structural parameter(s) which improve under branching and lead to exact recurrences with honest cost bounds.
4. **Parity, moments, and certificates:** try to use the rank deficiency 0/1 to express exact \(\#\mathrm{BP}\) with near-p input variables rather than S witnesses; locate where independent potentials cost S and whether a sparse basis of components or partial evaluation reduces them.
5. **Intermediate goals:** deterministic \(2^{p-\omega(\log p)}\mathrm{poly}(S)\) for all \(S=p^{O(1)}\); or \(2^{o(p)}\) for \(S=p^{1+\epsilon}\), growing width, or more than constant reads. Check which goals would already yield nonuniform lower bounds using a precise published transfer theorem.
6. **Algorithm consequences beyond LGS:** conditional RP-SUBEXP for sparse graphic/cographic full-span and for sparse variable-rank systems; deterministic exact counts for small deficiency / few solutions; dense graph \(v\)-only HC and FVS still unhandled. These are backup objectives, not excuses to abandon LGS.

## Deliverables and working rules

Produce exact theorems/lemmas with explicit \(p,S,q,m\) and running times. Try constructions or counterexamples, not just surveys. Track proven/conditional/speculative claims. If the general goal is blocked, extract one nontrivial wider BP class. Tests on tiny BPs are useful but not substitutes for proofs. Keep all work on a new research branch, preferably \`research/claude-LGS\`; do not modify main or the 6.1/H checkpoints without permission. Leave one reproducible Markdown checkpoint with failed attempts and next experiments.

## Conspicuous open audit point

The \`williams.md\` argument \(\mathrm{LGS}\text{-}\mathrm{SAT}\in2^{o(p)}\mathrm{poly}(S)\Rightarrow \mathrm{NEXP}\not\subseteq\mathrm{L/poly}\) uses a logspace indexed tableau and an easy-witness transfer. Check every quantifier/closure and whether this precise circuit separation is already established via prior SAT algorithms. Do not treat the implication or novelty as peer-reviewed fact.
