# Checkpoint 19 — Character-trace tensor interface for A5 equation SAT

Date: 2026-10-29. Exact classical representation-theoretic identity, specialized to our algorithmic research context. Not a SAT breakthrough.

Let W(x)=prod_{t=1}^T h_t^{x_{i_t}} be a group-program word over G=A5, with p PRIMARY Boolean inputs. Let Irr(G) be the irreducible complex representations. Dimensions are 1,3,3,4,5.

## Exact acceptance-count identity

The regular character identity states, for every g∈G,

    1[g=1] = (1/|G|) sum_{ρ∈Irr(G)} d_ρ tr(ρ(g)).

Consequently, for the word W,

    # {x : W(x)=1} = (1/60) sum_{ρ∈Irr(A5)} d_ρ Z_ρ,
    Z_ρ = sum_{x∈{0,1}^p} tr( prod_{t=1}^T ρ(h_t^{x_{i_t}}) ).

The trivial representation contributes exactly 2^p. This formula is exact over characteristic zero, with eventual integral cancellation. For a conjugacy-invariant accepting subset A⊆G, expand the class function 1_A in the character basis to obtain an analogous linear combination of the same Z_ρ. Arbitrary state-based permutation-BP acceptance need not be a class function; this qualification is essential for the long-term L/poly program.

## Tensor-network form

For representation dimension d≤5, write

    Z_ρ = sum_{x∈{0,1}^p} sum_{s_0,...,s_{T-1}∈[d]}
           prod_{t=1}^T [ρ(h_t^{x_{i_t}})]_{s_{t-1},s_t},

with s_T=s_0. This is a cycle tensor network of fixed bond dimension d, coupled by equality hyperedges that identify all occurrences of each Boolean input x_i. Here hyperedges encode repeated reads, providing a concrete hypergraph interface to the user's original vertex-versus-edge activation question.

The hard part is NOT matrix dimension (≤5). It is eliminating repeated high-arity Boolean equality nodes while retaining a compact exact representation of the contracted quantity.

## Why spectral gaps do not detect rare witnesses

Let C be an A5 conjugacy class of a 5-cycle. The irrep character values on C are

    d=(1,3,3,4,5),
    χ(g)=(1,φ,φ',-1,0),
    φ=(1+sqrt5)/2,  φ'=(1-sqrt5)/2.

For uniform distribution U_C, the average irrep matrix is (χ(g)/d) I, with norm at most φ/3≈0.539344 in each nontrivial representation. Yet

    60 U_C({1}) = 1+3φ+3φ' -4 = 0.

All of the (constant-sized) nontrivial Fourier terms cancel the trivial contribution exactly. Thus a constant Fourier spectral gap does not guarantee ANY mass on a desired point. In checkpoint 17, a polynomial-length word W_p has max nontrivial Fourier norm <0.6 and identity acceptance probability 2^{-p}.

To infer positive mass at every group element from Fourier operator norms, one needs a sufficiently strong bound such that the accumulated error is <1/|G|, e.g. the independent-block spectral product bound from checkpoint 16. Merely bounding each transform by 0.6 once does not suffice.

Similarly, an additive approximation to normalized accepting probability with constant accuracy cannot distinguish 0 from 2^{-p}. Exact character contraction or exponentially precise estimates would be required for general decision SAT.

## Gauge cancellation appears algebraically in each trace

If W(x)=U(x)V(x)U(x)^-1, then

    tr(ρ(W(x))) = tr(ρ(V(x)))

for each x, by trace cyclicity, even when U,V share variables. Thus gauge stripping from checkpoint 17 is automatically visible in the tensor trace representation.

This is a rigorous candidate target for structural compression: find tensor contractions that detect and eliminate conjugate/shared-input correlations without expanding 2^p assignments, then understand whether the method extends beyond conjugacy-invariant group equations.

References:
- A5 character table: https://people.maths.bris.ac.uk/~matyd/GroupNames/characters.html
- Finite-group representation Fourier methods and upper-bound lemma: https://page.mi.fu-berlin.de/baumeist/sommerschule/random-entire.pdf
- Barrington: https://doi.org/10.1016/0022-0000(89)90037-8
