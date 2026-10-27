# Branch G — Circuit lower bound win-win, roadmap

## Distinction
Sparse (Co)Graphic Span-CSP is a precise structural envelope containing many graph tasks, but not a complete successor to ETH.

The generic no-2^{o(N)} SCGS hypothesis (if true) supports lower bounds for targets only after SCGS -> target linear reductions. Its falsity includes a faster sparse 3-SAT algorithm (by dummy matroid), so the Ryan Williams E^NP linear-circuit lower bound follows — but that is not a new implication after the 2026 SAT announcement.

## Stronger desired payoff
Williams's Circuit-SAT acceleration theorem gives NEXP notsubseteq P/poly if SAT on n input bits and n^k circuit gates can be uniformly solved in O(2^n/n^{10}) for each fixed k. This is qualitatively stronger than the lower bounds obtained merely by refuting ETH.

## Proposed Input-Efficient Span Feasibility IESF(n,s)
n primary free bits, graphically represented (co)graphic full-span condition with structural size s=poly(n), and a sharply restricted activation language. Deterministic auxiliary bits must be uniquely fixed and counted in s. Cannot simply include arbitrary Circuit-SAT as a local predicate; full-span should be essential.

Seek a reduction for every k:
Circuit-SAT(n,n^k) -> IESF(O(n),poly(n))
whose syntactic restrictions are meaningful, plus solver complexity strong enough to transfer the Williams savings. In parallel obtain size-preserving reverse reductions from the structural core to named graph problems.

## Open challenges
- Whether arbitrary Boolean circuits can be represented by this highly structured full-rank language without losing the required parameter.
- Whether the resulting class stays natural and nonvacuous.
- Whether the win-win can be proved with a less universal circuit class.
- Whether weighted #SAT + characteristic-two parity yields a direct generic algorithm (unweighted #SAT only supports parity, not decision).
- Whether a harder source than the narrow span core is needed to capture dense graphs, universe-parameter Set Cover and general-width CNF.

## Status labels
Exact matroid identities: PROVED.
Graph encodings for sparse instances: PROVED.
Generic subexponential span algorithm: OPEN.
Parameter-preserving hardness completeness: OPEN.
New NEXP/Ppoly win-win for Span: OPEN.

Reference: https://people.csail.mit.edu/rrw/ICM-survey.pdf and https://www.cs.cmu.edu/~ryanw/improved-algs-lbs2.pdf