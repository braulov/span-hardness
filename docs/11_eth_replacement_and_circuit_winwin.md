# Toward an ETH replacement with a REAL win-win

2026-10-27 research agenda, NOT a theorem.

## Required properties
(1) A naturally restricted problem U able to underpin conditional fine-grained lower bounds for multiple still-open parameter regimes.
(2) Parameter-preserving *U -> target* reductions (not only target -> U).
(3) A **new** unconditional circuit lower bound if U admits a specified faster algorithm. Without (3), we have a structural source of hardness, not the desired replacement for ETH.

## What SCGS-CSP actually provides
SCGS is O(N)-size local 3-CNF plus one full-span constraint in an O(N)-size graphically specified graphic/cographic matroid. It captures bounded-degree FVS, HC and connected-subgraph tasks by direct encodings *into* SCGS.

General CNF and Set Cover also have exact star-matroid descriptions, but the source-parameter (SAT variables; cover universe size) is NOT preserved linearly in general. The rank aspect cannot simply be a dummy gate for a purported nontrivial circuit theorem.

## Established Williams-style benchmark
Ryan Williams: ETH false implies E^NP notsubseteq SIZE(O(n)), as already cited by the October 2026 ETH manuscript. Since SCGS contains sparse 3-SAT as a trivial special case, falsifying SCGS via a uniform generic 2^{o(N)} solver would imply this already-available lower bound; not a NEW win-win.

A stronger benchmark: sufficiently fast SAT for every polynomial-size Boolean circuit family (e.g. Circuit-SAT on n inputs and n^k gates in O(2^n/n^{10}) for every constant k with appropriate uniformity) implies NEXP notsubseteq P/poly. This conclusion is presently open.

## Input-efficient span feasibility: proposed TWO-scale problem
Let IESF(n,s) have:
- n PRIMARY existential Boolean input bits;
- a graphically specified matroid full-span condition of structural description size s=poly(n);
- local activation with syntactically restricted, explicitly charged Boolean operations;
- auxiliary variables uniquely determined by the primary bits, with costs charged to s.

For the circuit-lower-bound tier, conjecture no solver with a specified genuinely nontrivial saving in the exponent of n and poly(s) dependence. For transferring hardness to graph tasks, demand separate source-to-target reductions which preserve the graph parameter itself.

Caution: if arbitrary polynomial-size Boolean circuits are accepted as activation maps, IESF simply becomes disguised Circuit-SAT. Instead seek a nontrivial rank-normal-form compilation where matroid full-span does real work.

## Aspirational bridge (currently OPEN)
For each fixed k, find a polynomial-time input-efficient reduction

Circuit-SAT(n inputs, n^k gates) -> IESF(O(n) primary bits, poly(n) structure),

preserving YES/NO, and prove that a sufficiently fast IESF solver yields the quantitative Circuit-SAT savings required by Williams. This would imply NEXP notsubseteq P/poly if the solver exists. Both the nonvacuous compilation and corresponding sharp solver bound are currently unknown.

## Two directions of the desired win-win
If U is hard and U <=_lin Q for natural target Q, we obtain conditional lower bounds for Q. If U is easy and the circuit compilation/quantitative bridge is proved, we obtain new circuit lower bounds and likely new graph algorithms.

Without the reductions this diagram is a conjectured research strategy, not a theorem.

## Tasks
G1: Find rank-normal forms for restricted circuit classes NC1/AC0 first.
G2: Prevent hiding polynomial arbitrary circuits in activations.
G3: Audit precise input/structure sizes for CNF, Set Cover and dense HC.
G4: Prove *reverse* reductions U->HC, U->FVS, etc.
G5: Analyze weighted-#SAT and nullspace isolation as possible algorithms.

References: Williams ICM 2014, Improving Exhaustive Search Implies Superpolynomial Lower Bounds; Williams Self-Improvement for Circuit-Analysis Problems; Williams OVC and Nonuniform Circuit Lower Bounds (2024/2025).