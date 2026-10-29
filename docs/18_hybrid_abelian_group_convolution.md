# Checkpoint 18 — Exact hybrid SAT via local abelian compression and group convolution

Date: 2026-10-29. Elementary closure theorem; not a universal improvement for NC1-SAT.

## Theorem (shared-variable modulator + independent abelian-compressible blocks)

Let G be a fixed finite group and consider a group-program word

    W(z,y)=W_1(z,y_1) W_2(z,y_2) ... W_m(z,y_m),

where z is a set of q shared Boolean variables and the private variable sets y_1,...,y_m are pairwise disjoint. We seek whether W lies in a specified accepting subset A⊆G. No independence of the *group elements* is assumed except conditional independence of private Boolean assignments after fixing z.

For each assignment z, assume each normalized private word W_j(z,y_j) has a decomposition into r_j(z) consecutive abelian blocks. Let h(G) be the maximum size of an abelian subgroup of G, and let r=max_{j,z} r_j(z).

For fixed z, compute exactly the set S_j(z)⊆G of possible outputs of W_j by the abelian-block subset-product algorithm from checkpoint 14. This uses at most h(G)^{r_j(z)} tuple states, and time O(T_j+(|y_j|+r_j(z))h(G)^{r_j(z)}) up to constant group operation overhead. Then combine block-output supports in their original noncommutative order:

    R_0={1}, R_j = {u v : u∈R_{j-1}, v∈S_j(z)}.

Each R_j has at most |G| elements. Exact SAT follows by checking R_m∩A≠∅ for some z. Total runtime is

    O(2^q [T + sum_j (|y_j|+r_j) h(G)^r + m |G|^2]),

where T is original word length and all parameters in brackets are polynomial in input length unless r is large.

For G=S5, |G|=120 and h(G)=6; for G=A5, |G|=60 and h(G)=5 (maximum abelian subgroup order 5, except V4 order 4). In either group q+r=o(p), with T=poly(p), yields an exact 2^{o(p)} poly(T) algorithm. If q,r=O(log p), runtime is polynomial.

This is an exact SAT algorithm; spectral gap is unnecessary since group-support convolution works whenever each local support S_j is computable efficiently. Witness assignments may be retained as backpointers throughout both DPs.

## An example where earlier *individual* parameters all fail

Let a,b∈A5 be noncommuting generators, and p=2n. Define

    W(x,y)= (prod_{i=1}^n a^{x_i}) (prod_{i=1}^n b^{x_i}) (prod_{j=1}^n h_j^{y_j}),
    h_j=a for odd j and b for even j.

Segment the word into one long x-only block and n singleton y-blocks. The large x-block has exactly two consecutive abelian subblocks; each y-block has one. So the hybrid algorithm solves SAT in polynomial time (O(p) for constant group).

However:
* The global number of abelian consecutive blocks is Θ(n), due to alternating a,b tail.
* The variable noncommutation graph has a single connected component of size 2n, because each x_i appears with both a and b, and a,b do not commute.
* The read-order variable liveness is n=Θ(p), because x_1,...,x_n all appear in the first a-section and again in the later b-section.
Thus the hybrid combines prior techniques nontrivially; none of the three previous global parameter bounds alone yields polynomial time. In this particular example, the x-block outputs have the especially simple form a^s b^s for s=Σ_i x_i mod 5.

## Limitations and next target

This decomposition criterion is syntactic. An arbitrary polynomial-length width-five program may have many variables crossing every proposed block boundary. A small q or small r is NOT guaranteed. The gauge-padding construction in checkpoint 17 shows the opposite danger: many repeated shared variables can arise purely from conjugation and should be stripped symbolically first when acceptance is conjugacy invariant.

A robust research direction is an adaptive algorithm alternating exact symbolic gauge cancellation with (1) detection of low-shared-variable block cuts and (2) abelian-block DP or group-support convolution on remaining private factors. This is a provably correct hybrid, not a universal 2^{o(p)} result or a new circuit lower bound.

Source/related checkpoint: docs/14_width5_abelian_blocks_and_commutators.md ; docs/17_spectral_gap_gauge_counterexample.md.
