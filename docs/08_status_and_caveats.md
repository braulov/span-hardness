# Status, caveats and corrections (2026-10-27)

## Mathematically established in the notebook
- For the GF(2) incidence matrix, rank(B_Y)=|V|-cc(V,Y).
- Forest iff chosen columns independent; spanning connectivity iff full graphic rank.
- Sparse bounded-degree FVS, HC, directed HC, connected dominating/vertex-cover/Steiner variants admit O(n)-size encodings in the defined rank formalism.
- A star with group-activated spokes has rank equal to the number of covered universe elements.
- Cographic full span of an activated edge set is equivalent to independence of the complementary graphic columns.
- A root gadget converts induced-subgraph connectivity into fixed full graphic rank.
- A nullspace-witness sum modulo two counts full-spanning choices modulo two.

## Conditional
If a uniformly constructed Boolean rank circuit uses O(n log^alpha n) gates for fixed alpha<1/2, compilation into fixed-width SAT plus the reported October 2026 subexponential SAT algorithm gives 2^{o(n)} for the sparse span class. This relies on the precise verified scope and future scrutiny of the external algorithm.

## OPEN, not proved
- A small rank Boolean circuit of the needed size.
- Arbitrary finite-field weighted model counting in characteristic 2 at the claimed SAT time bound.
- Converting solution parity to decision without losing parameter control.
- Truth/falsity of Sparse (Co)Graphic Span Hypothesis.
- Two-way linear-size reductions with all natural target problems.
- Parameter-preserving encodings of general Set Cover by universe size or unrestricted CNF by variable count.
- A genuinely new Williams-style circuit lower bound from falsity of a structurally meaningful span hypothesis.

## Corrections
Dominating Set can already benefit from existing Linear Monadic NP reductions. A reduction P -> Span does NOT transmit Span-hardness to P. Submodular coverage on sets is not literally matroid rank on those set indices; group activation supplies the correct lift. Dense graphs and binary weights cause size blow-up. Polynomial-time connectivity is not a small Boolean circuit. Novelty relative to matroid-CSP literature is not claimed.

## References
https://github.com/openai/math/blob/main/lean/docs/378.md
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2016.42
https://doi.org/10.1145/3417759