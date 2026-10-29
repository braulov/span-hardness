# Checkpoint 20 — Input-efficient PBP-SAT via 2026 #3-SAT and computable separator certificates

Date 2026-10-29. This notebook records deductions from the October 25, 2026 OpenAI fixed-width #CNF algorithm (externally under review) and standard state encoding. No unconditional universal 2^{o(p)} PBP-SAT algorithm is claimed.

## 1. Arbitrary acceptance is a constant-size disjunction of group equations at fixed width

Let G≤S_w be the finite group of permutation transitions and W(x)∈G the program output (p primary bits). Let s∈[w] be the initial state and A⊆[w] accepting states. Then

  ∃x:W(x)(s)∈A  iff  OR_{g∈G:g(s)∈A} ∃x:W(x)g^{-1}=1.

This uses at most |G|≤w! instances without any new input bits. For fixed width w=5 this is constant overhead (≤120), and identity/group-equation algorithms suffice for all state predicates. This DOES NOT preserve a constant overhead when w grows with p (the L/poly target).

Equivalently, #accepting inputs has an exact natural-representation matrix coefficient:
  N_acc = 1_A^T [sum_{x∈{0,1}^p} P_T(x_{i_T})...P_1(x_{i_1})] e_s.
This extends the exact tensor network viewpoint from conjugacy-invariant traces to arbitrary state acceptance.

## 2. Parsimonious fixed-width PBP-to-3-CNF compilation

For a permutation BP with p declared inputs, width w fixed, and T steps, introduce a state symbol s_t∈[w] for t=0,...,T, encoded with O_w(1) Boolean bits. For each t impose the deterministic transition s_t=P_t(x_{i_t})s_{t-1}; also impose initial and accepting conditions. Each transition is a constant-arity Boolean relation, represented by O_w(1) width-3 CNF clauses/auxiliary gates, all auxiliary bits deterministically defined. Every primary input extends to exactly one full assignment of valid states and auxiliary gate outputs; hence #3-CNF exactly equals #accepted inputs. Number of variables N=O_w(p+T), clauses M=O_w(p+T), with M≤D_w N.

The stronger October 25 manuscript states deterministic exact #3-CNF in polynomial space, time poly(N+M) 2^{O(N/sqrt(log N))} when M=O(N). The published Lean scope establishes the weaker O(N(loglog N)^2/sqrt(log N)) exponent; both are o(N). Statements depending on the sharper bound should be marked conditional on the corresponding manuscript theorem.

Therefore for fixed w:
  PBP-SAT(p,T) ≤ poly_w(p,T) 2^{O_w((p+T)/sqrt(log(p+T)))}.
If T=o(p sqrt(log p)) and all input bits are counted, this is 2^{o(p)} poly(T). Under only the weaker formalized exponent, a sufficient condition is T=o(p sqrt(log p)/(loglog p)^2).

## 3. High-frequency variable modulator

Let d_i be number of reads of primary variable x_i. Choose H⊆[p], |H|=q, and let L=sum_{i∉H}d_i. Enumerate 2^q assignments to H. Once fixed, all their transitions become constants. Multiply maximal consecutive constant stretches and absorb them into adjacent instructions, leaving a permutation program of length at most O(L+1) on the remaining primary inputs. The constant transitions may change step tables but not semantics.

Apply the fixed-width parsimonious CNF algorithm to each branch:
  time ≤ 2^{q+O_w((p+L)/sqrt(log(p+L)))} poly_w(p,T).
In particular, q=o(p) and L=o(p sqrt(log p)) imply 2^{o(p)} poly(T), regardless of total T. This can include arbitrarily high read-frequency for o(p) of the variables.

One can optimize a computable sufficient bound by choosing H as all variables with d_i>threshold and checking q and L; this is not necessarily the optimal H.

## 4. A separator certificate from the variable-occurrence hypergraph

View positions [T] as vertices of a line. For each Boolean variable i, create a hyperedge consisting of ALL positions reading i. For a boundary t∈{1,...,T−1}, define the live-crossing load

  lambda(t)=|{i:first(i)≤t<last(i)}|; lambda(T)=0.

Fix a maximum block length B. Consider contiguous block partitions
  0=t_0<t_1<...<t_m=T, with t_j−t_{j−1}≤B.

Let H be the set of variables whose hyperedges meet at least two blocks. If q=|H| then q≤sum_{j=1}^{m−1}lambda(t_j). Define the computable upper-bound certificate

  Q_B=min_partition sum_{j=1}^{m−1}lambda(t_j).

The minimum is computed by a simple DP:
  F(0)=0;
  F(t)=lambda(t)+min_{max(0,t−B)≤s<t}F(s), for t=1,...,T.
Then F(T)=Q_B. This takes O(TB) time or O(T) with sliding-window minimum per fixed B; recover boundaries by parent pointers.

Given the minimizing partition, identify H and enumerate its 2^q assignments. After fixing H, every remaining variable occurs inside a SINGLE block. For each block and each possible output group element g∈G (constant-size group, |G|≤w!), use the parsimonious O_w(B)-size #3-CNF encoding and the #SAT solver to decide whether that block can output g. Combine the resulting support sets in the original noncommutative order using a DP over G. This yields an exact deterministic solver with time

  poly_w(p,T) · 2^{Q_B+O_w(B/sqrt(log(B+2)))}

under the stronger manuscript bound. The exponent can also be capped by p using trivial exhaustive search. The exact number q of crossing variables (often <Q_B) can replace Q_B after recovering the partition. For the weaker Lean bound substitute B(loglog(B+O(1)))^2/sqrt(log(B+O(1))).

When Q_B=o(p) and B=o(p sqrt(log p)), one has 2^{o(p)}poly(T) for polynomial T. The result is input-efficient even when T is polynomially larger than p, because the expensive computations are confined to individual blocks, and group-output support has size at most w!.

IMPORTANT: q must count DISTINCT variables crossing ANY boundary; sum lambda overcounts a variable crossing many boundaries. This is why Q_B is a convenient upper-bound certificate rather than an optimal partition parameter for the true q. Also, this exact algorithm does not require spectral mixing or group commutativity; it relies only on conditional independence of the private input variables.

## 5. Checked small instances

A Python brute-force verifier generated 450 random width-three permutation programs with 1≤p≤7 and 1≤T≤23, for each testing 7 maximum block lengths B. It compared the set of all whole-word outputs under all assignments with the output set computed by branching over globally crossing variables and independently enumerating private assignments within the DP-chosen blocks. All 3150 comparisons matched; in every case q≤Q_B. These tests support the elementary algebra but do not check the external #3-SAT theorem.

## 6. Open hard regime

Neither proposition yields a universal 2^{o(p)}poly(T) algorithm for width five. Difficult instances may have Ω(p) variables with Ω(sqrt(log p)) occurrences, no affordable small set H of global crossing variables, and every useful bounded-length block partition has Q_B=Ω(p). An interleaved word a^{x_1}...a^{x_p} b^{x_1}...b^{x_p} can already have huge Q_B, yet is easy by the earlier abelian-block theorem; therefore large Q_B does not imply computational hardness.

The target should be a symbolic representation that combines (i) finite-group identities/gauge stripping, (ii) local #SAT contraction for long but bounded blocks, and (iii) repeated-variable hyperedges that overlap many temporal blocks. This is the point where the user's hypergraph inversion idea becomes algorithmically substantive.

A truly universal input-efficient PBP-SAT improvement for polynomial width (not only fixed five) would be needed for the full Williams-style route to NEXP notsubseteq L/poly; general BP-to-permutation-BP simulation and the exact applicable lower-bound transfer theorem should also be stated carefully.

## Literature and verified sources

OpenAI manuscript (25 October 2026): https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex
Lean formalization scope: https://github.com/openai/math/blob/main/lean/docs/378.md
Idziak--Kawałek--Krzaczkowski--Weiß, Satisfiability Problems for Finite Groups, ICALP 2022: https://doi.org/10.4230/LIPIcs.ICALP.2022.127
Barrington, Bounded-width polynomial-size branching programs recognize exactly those languages in NC1, JCSS 1989: https://doi.org/10.1016/0022-0000(89)90037-8
Williams, Improving Exhaustive Search Implies Superpolynomial Lower Bounds: https://doi.org/10.1137/10080703X
