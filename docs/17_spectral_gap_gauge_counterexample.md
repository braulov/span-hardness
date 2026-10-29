# Checkpoint 17 — Spectral-gap counterexample and gauge elimination for width-five programs

Date: 2026-10-29. Research checkpoint. New material here consists of elementary constructions, not a claim of new literature-level results. All output probabilities below are w.r.t. uniform independent primary input bits.

## 1. A strong no-go for a naive mixing-versus-subgroup dichotomy

Fix G=A5. Let g=(1 2 3 4 5). For each p let B_p(y) be a polynomial-length width-five group program with B_p(y)=1 if y=1^p, and B_p(y)=g otherwise. Barrington's construction for balanced AND_p, followed by inverse and fixed multiplication, supplies such B_p with O(p^2) length for p a power of two, and polynomial length in general.

Choose a=(1 2 3 4 5), b=(1 2 4 5 3) generating A5. Let

    R(z)=prod_{j=1}^{20} a^{z_{2j-1}} b^{z_{2j}}.

Each bit z_i is independent. A direct 60-state group-convolution calculation yields TV(Law(R),Uniform(A5)) < 0.004934. The distribution has full support G already after 5 pairs, so R(z) ranges over all A5. The program R has constant length 40 and 40 distinct z bits. Its inverse uses exactly the SAME z bits in reverse order.

Define

    W_p(z,y)=R(z) B_p(y) R(z)^{-1},

and accept exactly if W_p=1.

For every z,y, W_p(z,y)=1 iff y=1^p. Thus a random assignment is accepting with probability 2^{-p}; the z bits do not affect satisfiability. The total number of primary bits is p+40, and the word has polynomial length.

Let C be the A5 conjugacy class of 5-cycle g, |C|=12. Conditioned on y≠1^p, the output is ν=Law(RgR^-1), within TV distance 0.004934 of U_C because pushforward contracts TV distance. By Schur's lemma, the nontrivial Fourier transform of U_C at irrep ρ is (χρ(g)/dimρ) I; the A5 irreps have dimensions 3,3,4,5 and character ratios on a 5-cycle bounded by

    λ_C=(1+sqrt(5))/6 = 0.539344...

Therefore λ(ν) ≤ λ_C + 2*0.004934 <0.55, since the difference of operator expectations of unitary matrices is at most 2 TV.

The unconditional law of W_p is μ_p=2^{-p} δ_1+(1-2^{-p})ν, hence

    max_{ρ ≠ trivial} ||hatμ_p(ρ)||op ≤ 0.55 + 2^{-p}.

For p≥5 this is strictly <0.6, yet μ_p(1)=2^{-p}. Thus a constant spectral gap for the ENTIRE output distribution does NOT imply constant density of accepting assignments. The output support {1}∪C is not contained in any coset of a proper subgroup: since it contains 1, such a coset would be the subgroup itself; C generates all A5 by simplicity and nontriviality.

This also shows why separate marginal mixing of R and R^-1 gives NO independence: they share exactly the same input z, and R(z)R(z)^-1 is always 1. The correct Fourier identity for blocks with shared input z and private disjoint bits y_j is

    hatμ(ρ)=E_z[ M_{1,ρ}(z) ... M_{m,ρ}(z) ],
    M_{j,ρ}(z)=E_{y_j} ρ(W_j(z,y_j)).

The expectation of the product cannot be replaced by a product of expectations. One valid sufficient bound is
    ||hatμ(ρ)|| ≤ E_z prod_j ||M_{j,ρ}(z)||,
but this may be ineffective.

## 2. A positive exact normalization for conjugacy-invariant targets

Let A⊆G be invariant under conjugation (examples: {1}, G\{1}, a conjugacy class, a union of classes, a normal subgroup). For ANY group-valued programs U(x),V(x), with arbitrarily shared variables,

    U(x)V(x)U(x)^-1 ∈ A iff V(x)∈A

pointwise for every assignment x. No independence assumptions needed. Thus a potentially very large prefix/suffix can be deleted when the word is supplied in this syntactic sandwich form.

There is also a purely symbolic polynomial-time preprocessing for explicit normalized group words W(x)=prod_t h_t^{x_{i_t}} with constant interspersed factors:
* Adjacent factors a^{x_i} b^{x_i} may be replaced by (ab)^{x_i}, since x_i∈{0,1}.
* If product ab=1, erase the pair.
* If acceptance is conjugacy-invariant, the word may be cyclically rotated pointwise before such replacements, because a cyclic shift of a product is conjugate to the original output.
* Repeat until no reduction applies. Each reduction strictly decreases length, hence the routine is polynomial-time and exact for the specified acceptance model.

This is a simple but honest *gauge stripping* algorithm. It can remove Θ(p) apparently involved input variables from a padded program R(z)B(y)R(z)^-1, although their read intervals and variable-interaction graph may look complicated.

CRUCIAL LIMITATION: ordinary PBP acceptance by moving a distinguished state into an arbitrary set is generally NOT conjugacy-invariant. One may use the stripping theorem for identity/group-equation or class-function acceptance, but cannot silently apply it to arbitrary branching programs / LGS encodings.

## 3. Why this matters for the proposed algorithmic win-win

The earlier 'mixing vs. subgroup rigidity' heuristic is not sufficient: the above instance has a uniform constant nontrivial-representation spectral gap, full group-generating support, and an exponentially rare witness. A correct theorem must use quantitatively strong pointwise near-uniformity (e.g. TV < 1/(2|G|)), often achieved through convolution of genuinely independent blocks, OR exact structural cancellation.

A rigorous research target is to combine (a) noncommutative representation estimates for genuinely independent private variables conditional on a shared interface, and (b) symbolic conjugacy/gauge elimination of dependent inverse blocks, while obtaining explicit runtime in the number p of PRIMARY bits, not program length alone. Our example shows these are mathematically different mechanisms.

Sources:
- A5 character table, https://people.maths.bris.ac.uk/~matyd/GroupNames/characters.html
- Barrington, JCSS 1989, https://doi.org/10.1016/0022-0000(89)90037-8
- Diaconis-Shahshahani finite-group upper bound lemma (classical), e.g. https://page.mi.fu-berlin.de/baumeist/sommerschule/random-entire.pdf

Computational cross-check: enumerated A5 generated by a,b (order 60), and calculated the convolution of the 4-point distribution on {1,a,b,ab} exactly with floating-point tracking. At 20 pairs, TV distance from uniform = 0.0049338708304882545. The analytic argument only requires existence of some constant number of blocks, not this numerical threshold.
