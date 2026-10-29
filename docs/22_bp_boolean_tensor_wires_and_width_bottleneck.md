# Checkpoint 22 — Boolean tensorization of branching programs and the polynomial-width bottleneck

Date 2026-10-29. An explicit deduction from the October 25, 2026 Boolean tensor contraction theorem, conditional on its stated correctness and external review. Not a general L/poly SAT breakthrough.

## Tensor network for an oblivious deterministic branching program

Let P have p primary Boolean inputs, width w, length T, and binary-valued transition tables f_t^0,f_t^1:[w]->[w]. Use h=ceil(log_2 w) Boolean wires for each state boundary, and one Boolean variable wire per input occurrence. For each step t place a local tensor with 2h+1 ports:
  T_t(a,b,x)=[a,b∈[w] and b=f_t^x(a)].
Add an initial unary/bounded-arity tensor forcing the fixed starting state, and a final tensor indicating acceptance. Repeated reads of one primary input must share a bit: link all its occurrence ports with an equality tree of trivalent Boolean-copy tensors (O(d_i) wires for d_i occurrences). For two-read BPs this is simply a single edge connecting the two occurrences. Subdivide edges with binary equality tensors to make the tensor graph bipartite if necessary.

The resulting Boolean tensor network has O(T log w + p) wires for T≥p when all p variables are used, local max degree O(log w), and locally computable entries in time poly(T,w). Each accepted primary assignment has a unique compatible assignment to all state and equality wires; rejected ones contribute zero. Therefore the scalar contraction is exactly #accepted inputs. Work over Z/2^{p+1}Z, where the residue is #accept because 0≤#accept≤2^p.

## Consequence of the October 2026 claimed tensor theorem

The theorem in quantitative-reduction.tex covers bipartite Boolean tensor networks with O(s) bit-wires and max degree ≤s^{9/10}, locally computable tensor entries, with time poly(s,description length) 2^{O(s/sqrt(log s))} and polynomial space. Here s=O(T log w+p), max local degree O(log w), and the hypotheses hold for polynomial w,T.

Thus one obtains the conditional exact counting bound
  time = poly(p,T,w) 2^{O((T log w+p)/sqrt(log(T log w+p)))}.

For read-twice programs T=2p, this specializes to
  poly(p,w) 2^{O(p log w/sqrt(log(p log w)))}.
If log w=o(sqrt(log p)), this is 2^{o(p)}poly(p,w), even for arbitrary second-pass permutation, and more generally arbitrary read-twice orders. For w=poly(p), log w=Theta(log p), and the exponent becomes O(p sqrt(log p)), which is WORSE than 2^p; this does not solve the L/poly case.

The sharper tensor theorem is stated in OpenAI's October 25 manuscript. A weaker exact #CNF theorem has been recorded as Lean-checked, but this document does not claim that the entire tensor theorem is covered by that selected formalization.

## Contrast with checkpoint 21

Checkpoint 21's four-boundary-state exact counting for separable two-sweep read orders takes poly(p,w), including w=poly(p), and needs no 2026 #SAT/tensor theorem. Its extension via prime substitution arity kappa has complexity poly(p,w) w^{O(kappa)} and is input-efficient when kappa log w=o(p).

The tensor-contraction bound covers arbitrary read patterns for constant and modest width, while the substitution-order DP handles polynomial width but needs nontrivial order structure. Their union identifies a sharp algorithmic frontier: large width combined with large prime/order complexity.

## Sources

OpenAI quantitative tensor theorem: https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/quantitative-reduction.tex
OpenAI Lean scope (a weaker selected #CNF statement): https://github.com/openai/math/blob/main/lean/docs/378.md
Prior checkpoint docs/21_two_sweep_substitution_decomposition.md.
