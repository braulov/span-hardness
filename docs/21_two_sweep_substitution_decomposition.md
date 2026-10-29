# Checkpoint 21 — Two-sweep branching programs, separable permutations, and four-boundary-state contraction

Date: 2026-10-29. Elementary exact algorithms, not yet audited for priority relative to existing read-twice BP literature. This is independent of the October 2026 #SAT theorem.

## Model

A deterministic oblivious branching program of width w reads p Boolean variables exactly once in each of two passes:
- Pass U reads x_1,x_2,...,x_p.
- Pass V reads x_{sigma(1)},...,x_{sigma(p)} for a permutation sigma∈S_p.

On the first pass, variable i chooses one of two transition functions u_i^0,u_i^1:[w]->[w]; on the second pass it chooses v_i^0,v_i^1:[w]->[w]. The transitions need NOT be injective. Initial state s0 and accepting final states A⊆[w] are arbitrary. The task is to count primary assignments x for which the composed two-pass computation accepts.

## Four-boundary-state tensor

For any set I of consecutive first-pass variable labels that is ALSO a contiguous block of the second-pass order (a common interval), define U_I(x_I) and V_I(x_I) as the state-transformations in the respective restricted orders. Store the nonnegative-integer 4-index tensor

  R_I(s,t;u,v) =
  #{x_I∈{0,1}^I : U_I(x_I)(s)=t AND V_I(x_I)(u)=v}.

The table has w^4 entries and each integer has at most |I|+1 bits.

Leaf i:
  R_{i}(s,t;u,v)=sum_{b∈{0,1}} [u_i^b(s)=t][v_i^b(u)=v].

For a binary common-interval split I=A∪B with A before B in the first pass:

DIRECT (A then B in the second pass):
  R_I(s,t;u,v)=sum_{a,b∈[w]} R_A(s,a;u,b) R_B(a,t;b,v).

REVERSE (B then A in the second pass):
  R_I(s,t;u,v)=sum_{a,b∈[w]} R_A(s,a;b,v) R_B(a,t;u,b).

These are exact integer equalities: each full assignment splits uniquely across disjoint child inputs and has uniquely determined intermediate states a,b. Either contraction uses O(w^6) additions/multiplications of O(p)-bit integers.

At the root, after the first sweep the intermediate state is t, which is also the starting state of the second sweep. Thus:
  #ACC=sum_{t∈[w], v∈A} R_{[p]}(s0,t;t,v).

## Theorem 1 — separable-order two-pass #BP-SAT is polynomial

If sigma is separable, i.e. recursively formed from direct and skew sums (equivalently avoids permutation patterns 2413 and 3142), there exists a binary common-interval decomposition whose internal nodes are direct or reverse. Hence the formula above computes EXACT #accepted assignments in O(p w^6) arithmetic operations after obtaining the decomposition, with O(p)-bit integer arithmetic. Runtime and memory are polynomial in p,w; w may be poly(p). No permutation-group assumption and no externally claimed #SAT theorem needed.

Separable permutation decomposition is polynomial-time computable; the stronger literature gives linear-time routines for substitution decomposition/common-interval structures.

## Theorem 2 — parameterization by largest prime substitution node

Every permutation has a substitution decomposition tree with monotone (direct/reverse) nodes and prime nodes whose children are common intervals. Let kappa be the maximum number of children of a PRIME node; set kappa=2 when there are no prime nodes.

For a monotone node of arbitrary arity, process its child tensors one by one using the same direct or reverse binary rules. This takes O(number of children * w^6).

For a prime node with k children, denote their independent tensors by R_1,...,R_k. To compute each of the w^4 outer boundary entries, sum over the 2(k−1) internal state boundaries: k−1 along first-sweep child order and k−1 along second-sweep child order. Each assignment of internal boundary states determines the four interfaces of all child tensors, so multiply their values and sum. The cost is O(k w^{2k+2}) arithmetic operations. This is a direct fixed-network tensor contraction with no hidden Boolean assignment enumeration.

The substitution decomposition has O(p) nodes, so the total time is
  poly(p,w) * w^{O(kappa)}
with O(p)-bit integer arithmetic. For w fixed, kappa=o(p) implies 2^{o(p)}poly(p); for w=p^{O(1)}, kappa=o(p/log p) suffices.

This is a parameterized tractable subclass of TWO-SWEEP read-twice programs, not a general poly-width BP-SAT algorithm. The root can be prime with kappa=p and then no speedup follows. Arbitrary read-twice BPs also need not be expressible as two complete sweeps.

## Independent checks

A Python brute-force checker generated 630 random deterministic two-sweep programs with 1≤p≤7, width 2-4 and arbitrary, often non-injective transitions. For 281 of these with separable second-pass order, it computed the complete four-boundary-state tensor using direct/reverse recursion and independently enumerated all 2^p input assignments, collecting exact boundary outcomes. All 281 tensor comparisons matched. Remaining 349 programs with nonseparable order were intentionally skipped by the *binary separable-only* test, not falsely marked incorrect.

A separate test over 630 random two-sweep permutation BPs of width three with 1≤p≤7 compared the reachable pairs of first/second-sweep group elements to brute force, checking 282 separable cases with no mismatch.

These checks validate the recurrences empirically; the mathematical proof is the unique-assignment/unique-intermediate-state bijection described above.

## Conceptual significance

This deals with an input-consistency hypergraph in which every Boolean variable occurs twice and all p variables may be simultaneously live in the chronological read order. The restriction is on the RELATIVE PERMUTATION OF OCCURRENCES, rather than occurrence count or ordinary source-graph treewidth.

The algorithm keeps four boundary-state indices instead of the full transformation chosen by a block. This is exactly why it extends from width-five permutation programs to arbitrary polynomial-width deterministic programs, unlike the earlier group-output DP with w! states.

The next target is an algorithm for large prime substitution nodes: obtain a contraction bound better than w^{Theta(k)} by exploiting the special two-pass crossing structure, or extract structural subfamilies where rank/Fourier techniques reduce the interface dimension without losing exactness. An improvement to 2^{o(p)} for arbitrary order and polynomial width could connect to the proposed L/poly circuit-lower-bound program, but we have NOT obtained such an algorithm.

## Context and literature

Separable permutations and pattern avoidance 2413,3142: https://www.sciencedirect.com/science/article/pii/S0097316511001014
Common intervals/substitution decomposition: https://doi.org/10.1137/060651331
Nagao–Seto–Teruyama, Syntactic Read-k-times BP-SAT: https://doi.org/10.4230/LIPIcs.ISAAC.2017.58
Exact algorithm for oblivious read-twice BPs: https://doi.org/10.1587/TRANSFUN.E99.A.1019
