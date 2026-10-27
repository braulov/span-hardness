# Post-ETH replacement: an exact win-win target and the missing completeness lemma

Research checkpoint, 2026-10-27. This is a **program and conditional implication**, not a completed new hardness hypothesis spanning natural graph problems. Most substantial existing proofs are in inherited `research/6.1-winwin/williams.md`, `research/6.1-winwin/parity_rank.md`, and branches H–M. The October 2026 fixed-width #SAT result is publicly announced and Lean-scope documented; independent human expert review is ongoing.

## 1. The two axes one must NOT conflate

**Total-size or sparse SCGS:** (N=\Theta(\#\mathrm{Boolean\ objects}+|V|+|E|+\#\mathrm{local\ gates})). Binary matroid (or cographic) full spanning is tested by parity of a **linear-size extension count** equal to (2^{d(x)}). An existing linear-size pairwise-independent isolation construction and exact sparse fixed-width #SAT imply **conditionally** a randomized one-sided (2^{o(N)}\mathrm{poly}(|I|)) decision algorithm. Thus a randomized sparse-total-size exponential-hardness conjecture is a bad post-ETH replacement. It does NOT make dense Hamiltonian Cycle/FVS (2^{o(v)}), Set Cover (2^{o(u)}), or polynomial-size BP-SAT (2^{o(p)}).

**Input-efficient (two-parameter) LGS:** (p) independent switches, (S=|V|+|E|\le p^{O(1)}); each edge is activated by (0,1,x_i,\neg x_i), and ask if the active graph is connected. It exactly encodes polynomial-size branching-program acceptance without adding independent input switches (the simple two-sink gadget of 6.1). LGS-SAT is a natural graphical presentation of BP-SAT. Its desired deterministic bound is (2^{o(p)}\mathrm{poly}(S)), uniformly for every fixed polynomial relation. A subexp-in-**S** algorithm does not achieve this.

The October fixed-width #SAT sparse rate applied to a standard size-(O(S)) circuit/Tseitin encoding gives a deterministic time (2^{O(S/\sqrt{\log S})}\mathrm{poly}(S)) for appropriate sparse instances, conditional on the manuscript's sharpened bound. This beats (2^{\varepsilon p}) if (S=o(p\sqrt{\log p})), but not for (S=p^k) with (k>1). The weaker Lean-scope exponent (O(S(\log\log S)^2/\sqrt{\log S})) gives the conservative threshold (S=o(p\sqrt{\log p}/(\log\log p)^2)).

## 2. The useful candidate hypothesis

(H_L): There does NOT exist a **deterministic** uniform algorithm for all polynomial-size LGS instances running in (2^{o(p)}\mathrm{poly}(S)).

The conditional algorithm-to-lower-bound transfer in `williams.md` claims

[
\neg H_L \Longrightarrow \mathrm{NEXP}\not\subseteq\mathrm{L/poly}.
]

The proof uses input-preserving branching-program encoding, an easy-witness theorem and a succinct indexed tableau. It is logically detailed but is NOT independently peer reviewed. Crucially this is a lower bound against polynomial-size **branching programs/nonuniform logspace**, NOT (\mathrm{NEXP}\not\subseteq\mathrm{P/poly}). Extending to the latter cannot follow by treating L/poly as equal to P/poly.

## 3. The exact missing ETH-style *truth-side* theorem

Fix a natural parameterized problem (Q): dense (v)-parameter Hamiltonian Cycle, dense (v)-parameter Feedback Vertex Set, (u)-parameter Set Cover with arbitrary polynomial-size family, or general CNF-SAT parameterized by original variable count.

Find a deterministic **subexponential parameter-preserving Turing reduction** (R_Q) from LGS(p,S) to Q. Desiderata, uniformly for any fixed (S\le p^k):

- preprocessing, total number of oracle instances and total output size all bounded by (2^{o(p)}\mathrm{poly}(S));
- every query has Q's natural parameter (q\le Cp), with universal or fixed-k bounded C;
- the reduction's correctness includes adaptive answers, and all running time promises are uniform.

**Conditional win-win theorem (elementary composition).** If (R_Q) exists and the transfer in Section 2 holds, then:

- (H_L\) true: (Q\notin\mathrm{DTIME}(2^{o(q)}\mathrm{poly}(|I|))). Proof: a faster Q solver composed with (R_Q) would produce an input-efficient LGS solver, contradicting (H_L).
- (H_L\) false: (\mathrm{NEXP}\not\subseteq\mathrm{L/poly}) by the separate LGS transfer.

This gives the precise desired ETH-like win-win **provided (R_Q) can actually be constructed**. Such a reduction is NOT presently known. A mere reduction (Q\to\mathrm{LGS}) has the wrong direction for truth-side lower bounds.

A full replacement with many natural consequences would require (R_Q) for many (Q). This is much stronger than a common matroid encoding.

## 4. Why ordinary polynomial-time compression is the wrong goal

LGS with (p) switches already accepts general polynomial-size CNF on (p) variables through a linear-size BP scanner. A polynomial-time reduction of *all* LGS(p,S) descriptions to a simple graph with (O(p)) vertices and polynomial-length encoding bounded by a fixed polynomial in (p), independent of source description complexity, would yield forbidden general SAT instance compression under the standard (\mathrm{NP}\not\subseteq\mathrm{coNP/poly}) assumption. Stronger fixed-width quantitative bounds: Dell–van Melkebeek, sparsification lower bounds.

**This does NOT rule out** (2^{o(p)}\mathrm{poly}(S))-time *many-instance* sparsification/reductions: compression barriers assume polynomial-time preprocessing and/or bounded communication. Nor does it automatically rule out Set Cover with (u=O(p)) but number of sets growing as an arbitrarily high fixed polynomial in (S), rather than a fixed polynomial in (p). This makes Set Cover a potentially useful FIRST test target, though no reduction is established.

## 5. Which survivors occupy the high-description-density regime?

| Q | Natural parameter | Why sparse #SAT does not immediately settle it |
|---|---|---|
| Dense Hamiltonian Cycle | (v) vertices | current edge switches number (e=\Theta(v^2)); sparse-case RP (2^{o(v+e)}) says nothing about (2^{o(v)}) in dense graphs |
| Dense Feedback Vertex Set | (v) vertices | cographic cycle-space witnesses use (\Theta(e)) bits; again sparse (v+e) not dense (v) |
| General CNF-SAT | (p) independent variables | unbounded clause width and (m=p^{\Omega(1)}), so long-clause filters give (O(p+m)) variables, not (O(p)) |
| Set Cover | (u) universe elements | arbitrary number of sets (t\gg u), so the known representation needs (\Theta(u+t)) variable/filter objects |
| Unrestricted Chromatic Number | (v) vertices | cannot assume fixed number of colors; fixed-q Coloring already follows from constant-width CNF |

Conditional developments from 6.1 also yield RP (2^{o(v)}) for connected dominating set, connected vertex cover and unweighted edge-budget Steiner Tree even on dense graphs, by (O(v)) **variables** but possibly (O(v^2)) **clauses**. Thus those should NOT be asserted as survivors of randomized vertex-parameter SUBEXP in this model without checking.

The common phenomenon is **high description density relative to independent choices / native parameter**, not merely “graphness” or matroid rank. A useful two-scale taxonomy should track the number of *independently chosen bits* (p), verification-description size (S), and shortest known exact-counting/parity-lift variable count (q) separately. Avoid claims that this alone proves hardness.

## 6. Three mathematically concrete next tasks, ranked

1. **Two-scale source equivalence / Set Cover test.** Attempt an LGS(p,S) \(\to\) SetCover(u=O(p), t=S^{O(1)}) reduction using multiple instances and subexp preprocessing if needed. Check compression barriers and exact universe-vs-number-of-sets complexity. If impossible, prove a restricted impossibility theorem under a standard assumption. No known theorem here.
2. **SERF sparsification for LGS.** Find a (2^{o(p)}\mathrm{poly}(S))-time procedure producing (2^{o(p)}\mathrm{poly}(S)) instances each represented by a graph of (O(p)) relevant vertices, or show explicit families resisting a well-defined restricted version. In contrast with old k-SAT sparsification this has to handle arbitrary polynomial-size BP evaluation and should not be assumed possible.
3. **Potentially stronger source.** Generalize LGS from L/poly verifier predicates toward larger circuit classes without hiding arbitrary circuits in “local constraints”; exact input-parameter preservation and meaningful structural restriction are essential. A generic full (\mathrm{CircuitSAT}) speedup would imply (\mathrm{NEXP}\not\subseteq\mathrm{P/poly}), stronger than current LGS falsity-side consequence.

## 7. Status and warning

- No new replacement hypothesis with BOTH all-natural hardness and circuit-lower-bound consequences is currently proved.
- The implication from a fast LGS solver to a NEXP-vs-L/poly separation is a conditional mathematical argument in the existing checkpoint, not a lower bound already established.
- The OpenAI/Anthropic October results are announced with machine-checked scope, but expert assessment remains ongoing as of this checkpoint.
- The work's strongest current contribution to the *program design* is identifying the **required reduction direction** and the **subexponential/superpolynomial-description gap**.

### Primary references

- OpenAI Lean scope: https://github.com/openai/math/blob/main/lean/docs/378.md
- OpenAI external review statement: https://openai.com/index/building-scientific-understanding-with-academic-communities/
- Williams, Improving Exhaustive Search Implies Superpolynomial Lower Bounds: https://people.csail.mit.edu/rrw/improved-algs-lbs2.pdf
- Fortnow–Santhanam instance compression: https://lance.fortnow.com/papers/files/compress.pdf
- Dell–van Melkebeek sparsification/compression barrier: https://pages.cs.wisc.edu/~dieter/Papers/sparsification-stoc.pdf
