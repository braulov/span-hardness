# Research assignment — deterministic algorithms for Literal Graphic Span-SAT

Work as a theoretical computer scientist on a concrete **algorithmic** problem. Do not propose new hardness conjectures. Your primary aim is to design and rigorously analyze a deterministic SAT/#SAT algorithm for LGS (equivalently, a graph encoding of branching-program satisfiability), with complexity measured chiefly by the number of *independent switches*, not by the size of the graph.

## Sources you MUST inspect first

Private repository: https://github.com/braulov/span-hardness

Branch: `research/I-LGS-algorithms`. Start with:
- `research/I-LGS-algorithms/README.md` — detailed problem, new small-deficiency identity, baselines, literature, research paths.
- `research/6.1-winwin/williams.md` — exact input-preserving branching-program-to-graphic-span reduction (Lemma 6) and proposed Williams-style circuit-lower-bound transfer (Theorem 10).
- `research/6.1-winwin/parity_rank.md` — parity lift and rank witnesses.
- `research/6.1-winwin/research_checkpoint_ru.md` — status and parameter ledger.
- `research/H-derandomization-algorithms/derandomization_and_matrix_lifts.md` — bounded-deficiency deterministic exact counts.

If private GitHub access fails, work from this self-contained definition: given a connected undirected multigraph G of S=|V|+|E| objects, p Boolean input bits x_1,...,x_p, each edge labeled by 0,1,x_i, or NOT x_i, ask whether some assignment makes the active edges connected. This is Literal Graphic Span-SAT (LGS), equivalently selected edges have full rank in the graphic matroid.

## Core desired theorem

Try to find a **deterministic** algorithm of time

  2^{o(p)} poly(S),

for all polynomial-size graphs S=p^{O(1)}. Another interesting goal is a nontrivial saving 2^p/p^{omega(1)} poly(S) uniformly for all fixed polynomial size bounds, but rigorously check the precise published circuit lower-bound transfer before claiming it suffices. The checkpoint claims that the strong 2^{o(p)} bound would imply NEXP not subseteq L/poly. Audit that theorem and distinguish it from the much stronger, unproved goal NEXP not subseteq P/poly.

Do not count 2^{o(S)} as progress toward this central target if S=p^k. Do not confuse p independent variables with O(S) auxiliary variables in a Tseitin encoding.

## First technical check: a very useful 0/1 rank deficit

The reduction from an acyclic deterministic BP with p inputs and S vertices to LGS produces, for every x, a selected graph having either one component (accept) or two (reject). Hence d(x)=r(E)-r(Y(x)) belongs to {0,1}. A graphic parity-witness construction has exactly 2^{d(x)} extensions. If M is the exact unweighted #3SAT model count of its O(S+p)-variable parsimonious encoding, then

  M = #accept + 2 #reject = 2^{p+1} - #accept,

so #accept = 2^{p+1}-M, **without random isolation**. This gives conditional deterministic exact BP counting in time 2^{o(S)} via the claimed October fixed-width #SAT theorem, and therefore 2^{o(p)} when S=O(p log^alpha p) with fixed alpha<1/2, using its quantitative bound.

Before claiming novelty, note that directly evaluating the BP DAG as a Boolean circuit and using unique-extension Tseitin also yields O(S) variables. The key unsolved issue is reducing the exponential dependence from S to p for arbitrary polynomial S, not avoiding randomization.

## Required research directions

A. Try genuinely input-efficient #SAT/3-CNF representations of BP acceptance, where the number of auxiliary variables is o(p sqrt(log p)/polyloglog p), even for S=p^k. Can large clause count or global linear-algebraic identities absorb the BP computation without one variable per state?

B. Analyze the graph rank/spanning encoding directly. Explore transfer-matrix products, cancellation and determinant identities, spectral or multilinear summaries, characteristic-two coefficients, and decomposition by repeated input labels. Give a concrete recurrence and its cost, or identify a precise barrier.

C. Explore nontrivial restricted classes: polynomial-length width-five permutation programs, growing width, read-k BPs, oblivious BPs, low interaction rank. Don't rediscover published width-two/read-k algorithms. Explicitly compare new bounds to them.

D. Investigate modest but consequential deterministic savings below 2^p for general polynomial-size LGS. Read exact Williams algorithm-to-lower-bound prerequisites; identify the weakest new algorithmic target that would already imply a meaningful separation.

E. If a concrete LGS avenue fails, identify an adjacent **algorithmic** consequence of the rank/parity method stronger than previous notes: dense Hamiltonian Cycle/FVS parameterized by v, exact full-span counting via compact moment projections, or general sparse-variable matrix nonsingularity.

## Strict requirements

- Verify up-to-date primary literature. October 2026 #SAT theorem is a conditional premise until independently accepted; distinguish the manuscript bound from Lean's weaker documented quantitative bound.
- Measure p, S, #SAT variables q, number of clauses and actual preprocessing time separately.
- Provide proofs of claims, and counterexamples for incorrect lemmas; don't present speculative algorithms as theorems.
- Use precise existing lower bounds and reduction directions.
- Give several mathematically serious iterations, not merely an overview.
- Output a research checkpoint with (i) proved algorithmic advances, (ii) attempted methods and exact blockers, (iii) best quantitative target and next experiments.
- Save to a new branch `research/claude-LGS` and leave main untouched, if GitHub writes are available. Otherwise output complete Markdown notes.

The goal is a robust algorithmic result, not to defend any conjecture.
