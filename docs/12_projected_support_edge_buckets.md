# Projected-support edge buckets for sparse-polynomial counting (2026-10-28)

**Status: proposed exact transformation, with proof below; external tensor-contraction theorem assumed, not independently certified.** This note connects the edge-bucket intuition from the HOM / subgraph-isomorphism project to the incidence-indexing argument in OpenAI's October 2026 ETH/#SAT manuscript. It is a research note, NOT a general dense-#3SAT improvement or a NEXP circuit lower bound.

## 0. Source and precise target

Primary external source: [OpenAI quantitative reduction, "Indexing the monomials" and "Tensor entries and contraction"](https://github.com/openai/math/blob/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/quantitative-reduction.tex).

After sparsification, high-incidence branching, and polynomial parity tests, the external proof counts common zeros of a=O(n) polynomials P_i over F_2, of fixed degree k, each with at most (log n)^c monomials. Write I_i for the set of Boolean variables used by test i and E={(i,v):v in I_i}, Q=|E|=n (log n)^{O(1)}.

The external proof constructs multilinear local factors Bbar_i(z_i,V) in
R=(Z/2^(n+1)Z)[V]/(V^(n+1)),
with private incidence variables z_iv, and F(z,V)=product_i Bbar_i(z_i,V).
Let c_i(S,V)=[product_{v in S} z_iv] Bbar_i, for S subset I_i.
After identifying the copies z_iv=x_v and summing over all Boolean x, the relevant ring element equals

    Z = sum_{S_i subset I_i, all i}
          (product_i c_i(S_i,V)) * 2^{#{v: no (i,v) selected}}.

A fixed coefficient-sum map on Z, plus the external high-incidence branching, recovers the exact count of zeros. The original proof proves that only incidence monomials of total degree <=K=O(n) are nonzero in R. It enumerates per-block counts d_gh whose sum is <=K, then indexes each chosen d_gh-subset of the block's E_gh using ceil(log2 binom(|E_gh|,d_gh)) wires.

**Important:** The claim here concerns this Z and the same external coefficient extraction, NOT simply the product of original polynomials P_i.

## 1. Setup: bipartite grouping and a new message alphabet

Use J=ceil(n^(1/4)) test groups T_g and J variable groups X_h exactly as in the external construction. Let

    E_gh = {(i,v) in E: i in T_g, v in X_h};
    q_gh = |E_gh|;
    V_gh = {v: (i,v) in E_gh};
    v_gh = |V_gh|.

For a chosen incidence subset S subset E_gh, define its projected support

    pi_gh(S) = {v in X_h: exists i in T_g with (i,v) in S}.

The variable-side tensor needs only whether each v is selected somewhere, not which tests selected it. Thus full S and pi_gh(S) are operationally different messages.

For fixed global degree-array d=(d_gh), with 0<=d_gh<=q_gh and sum d_gh<=K, choose on each block one of two encodings:

- **Exact:** transmit the d_gh-subset S subset E_gh, costing
      b_exact(gh)=ceil(log2 binom(q_gh,d_gh)) wires.
- **Projected:** transmit only the support U=pi_gh(S), where
      U in U_gh(d) = {pi_gh(S): S subset E_gh, |S|=d_gh}.
  Cost b_proj(gh)=ceil(log2 |U_gh(d)|); if the exact family is inconvenient to enumerate, use all U subset V_gh of size <= min(d_gh,v_gh), giving the valid upper bound

      b_proj(gh) <= ceil(log2 sum_{j=0}^{min(d_gh,v_gh)} binom(v_gh,j))
                  <= v_gh.

The hybrid chooses the cheaper message format independently for each (g,h):

    b_gh = min(b_exact(gh), b_proj(gh)),
    M(d)=sum_gh b_gh.

Unused codewords give tensor entry zero. The choice of format and array d are common, hard-coded descriptions of each network, not hidden additional wires.

## 2. Exact local tensors (the point of the bucket gadget)

For a given array of decoded block messages, the test-group tensor A_g evaluates

    A_g(messages) =
      sum over (S_i subset I_i) for i in T_g
          [ for every block (g,h):
             |S intersect E_gh|=d_gh AND
             (if exact message: S intersect E_gh equals decoded subset;
              if projected message: pi_gh(S intersect E_gh) equals decoded U) ]
          product_{i in T_g} c_i(S_i,V),

where S is the union of all selected incidences in T_g.

The variable-group tensor B_h decodes from each neighboring message the support U_gh (project the exact message if needed) and returns

    B_h(messages) = 2^{ | X_h \ union_g U_gh | } in R.

Then the contraction of the bipartite tensor network with b_gh parallel Boolean wires between T_g and X_h is precisely the sum of contributions to Z from incidence selections with block-size array d. **Proof:** Every incidence selection produces one unique message on each block; conversely A_g sums every incidence selection producing that message exactly once, while B_h depends only on the projected union. Distribute the finite sums. Summing the contractions over the enumerated d reproduces Z and hence the original count by the external extraction map.

The hybrid is exact even when both formats appear in the same network. It is not a parsimonious one-witness gadget: local summation is essential.

## 3. Parameter audit and external theorem's hypotheses

As in the original proof, after the high-incidence-variable branch each test has (log n)^{O(1)} distinct variables and each remaining variable occurs in at most (log n)^{O(1)} tests. Consequently any group of n^(3/4)+O(1) tests or variables touches at most

    L_g = n^(3/4) (log n)^{O(1)}

incidences. The degree of either group-tensor is at most the number of its incidences, since b_gh <= q_gh. For s=Theta(n), this is eventually <=s^(9/10).

Compute each A_g entry by enumerating all 2^{L_g} subsets of its incident incidences and checking message consistency. Each coefficient c_i(S,V) can also be calculated by Boolean Möbius inversion in 2^{|I_i|} time over the ring R, as in the original proof. Thus local evaluation costs at most 2^{O(n^(3/4)(log n)^{O(1)})} poly(input size), eventually at most poly(s+L) 2^{A s^(9/10)} for some fixed A. Values of B_h take polynomial time.

**Padding issue often missed:** the ring requires precision P0=n+1 and truncation ell=n+1, hence the contraction theorem needs s=Omega(n), even when the compressed network has M(d)=o(n) wires. We may pad with independent two-vertex, one-edge components of contraction value 1 until s=Theta(n). Such a component has one endpoint tensor (1,0) and another (1,1); both are degree one. Padding preserves the contraction and maximum-degree bound.

The number of degree arrays is bounded by

    (K+1)^(J^2) = 2^{O(sqrt(n) log n)},

which is 2^{o(n/sqrt(log n))}. Branching over high-incidence variables in the external proof costs 2^{O(n/sqrt(log n))}; preserve its assumptions and procedures explicitly.

**Conditional consequence for an instance with uniform M(d)<=Cn for every enumerated d:** assuming the external tensor-contraction theorem as stated, exact zero counting costs

    2^{O(n/sqrt(log n))} poly(|input|)

because every padded network has s=Theta(n), the number of networks has lower-order exponent, and the local entry procedures are allowed by the theorem.

A simple sufficient condition is

    W = sum_{g,h} |V_gh| = O(n).

Indeed use projected messages on every block, costing M(d)<=W regardless of d. In this structured case the K restriction and degree-array enumeration are actually optional: one may sum ALL incidence subsets within A_g and use an unrestricted projected support U per block, with v_gh wires; the same finite-distributivity proof gives Z directly. We retain the degree-array/hybrid construction for general systems where sparse selections save wires.

**NOT proved:** For arbitrary systems arising from dense 3-SAT, W=O(n), or max_d M(d)=O(n), or any universal o(n loglog n) wire bound. The current generic upper bound remains O(n loglog n).

## 4. Obstruction to mere extra intermediate vertices

For one variable, the two-side interaction of Boolean indicators a,b saying whether the variable was selected is

    K = [[2,1],[1,1]].

Its determinant is 1, a unit in Z/2^p Z. For q independent variables across one bipartition the matrix is K^(tensor q), which has full rank 2^q over the ring (its determinant is a unit). A single b-bit shared interface factorizable into matrices of inner dimension <=2^b therefore needs b>=q. This is a **cut-specific** lower bound for arbitrary independent support states, not a lower bound against every globally reorganized tensor network, nor against special algebraic coefficient families.

Thus an intermediate bucket cannot simply replace arbitrary independent support masks with short hashes without further structure. Possible savings must use shared supports, restricted/coherent coefficient families, cancellation, algebraic rank, or a different contraction topology.

## 5. Research problems and relation to circuit lower bounds

**A. Algebraic edge-bucket challenge (closest to a dense-#SAT improvement).** Exploit the *special* Bbar_i from the 2-adic lift, rather than treating c_i(S,V) as arbitrary. Design additional bucket vertices / summaries / a multi-stage factorization that computes Z exactly with max_d M(d)=O(n), or at least o(n loglog n), and total external branching 2^{O(n/sqrt(log n))}. Preserve computable local tensors and max degree. Seek either a proof or a concrete obstruction; first test quadratic and cubic sparse-polynomial systems. A generic injective encoding of all K-subsets among Q incidences cannot beat log2 binom(Q,K)=Theta(n loglog n) when Q=n polylog n and K=Theta(n).

**B. Input-efficient Circuit-SAT challenge (NEXP).** For every fixed k and every n-input Boolean circuit with <=n^k gates, construct uniformly, in poly(n^k) time or allowable 2^{o(n)} overhead, tensor networks that determine SAT, use s=o(n sqrt(log n)) wires, bounded local-degree <=s^(9/10), and satisfy the tensor-entry evaluation bound. If the total number of networks/overhead is 2^{o(n)} and the external tensor theorem applies with precision O(s), this gives Circuit-SAT in 2^{o(n)} and (by the appropriate Williams algorithms-to-lower-bounds theorem) NEXP not subseteq P/poly. Merely compiling to O(size(C)) wires or using one n-port global tensor with only O(n) wires does NOT suffice: the former can be n^k wires, the latter violates the degree constraint. This is an OPEN and highly ambitious target, not a theorem.

**C. Check the real bottleneck:** compare grouped support projection, coefficient-space low rank, and separator/holographic transformations. Account for all auxiliary wires, high-degree branching, local-entry computation, precision, and any loss from nonparsimonious counting.

## 6. External dependencies and status ledger

- Exact regrouping identity and projected-support local-sum construction: **PROPOSED, proof included; requires independent scrutiny**.
- Local tensor complexity and ability to pad precision parameter: **PROPOSED, audited parametrically above**.
- Tensor-contraction speed 2^{O(s/sqrt(log s))} over the specified truncated ring: **EXTERNAL 2026 MANUSCRIPT CLAIM**, not established from a new independent proof here.
- A universal O(n)-wire representation for the sparse polynomial tests: **OPEN**.
- Universal input-efficient Circuit-SAT representation and NEXP circuit lower bound: **OPEN**.
- Claimed novelty vs prior tensor network, holographic, communication matrix, and factor-graph literature: **NOT AUDITED**.

Connections: [our HOM / SubIso gadget and packing repository](https://github.com/braulov/hom-subiso-algs); [span-hardness circuit win-win](11_eth_replacement_winwin.md). The inspiration from HOM edge-buckets is methodological, not a direct reduction from HOM to these tensor networks.
