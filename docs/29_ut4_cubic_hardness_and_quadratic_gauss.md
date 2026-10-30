# Checkpoint 29 — Gaussian high-cutrank tractability versus cubic #P-hardness inside UT4

Date: 2026-10-30. This checkpoint is part of the input-efficient L/poly and LGS replacement-of-ETH research program. Mathematical observations and reductions are elementary/self-contained; **novelty relative to the literature is NOT established**. In particular this is a COUNTING hardness statement, NOT an ETH/#ETH fine-grained lower bound and NOT an NP-hardness result for the decision version of the restricted model.

## 1. Exact Gaussian elimination ignores arbitrarily large quadratic cutrank

Let Q:{0,1}^p→F2 be an arbitrary quadratic Boolean polynomial. Define S(Q)=Σ_x (-1)^{Q(x)}.

If Q contains a term x_i x_j with coefficient one, uniquely write
  Q=x_i x_j+x_i L(y)+x_j M(y)+R(y),
where L,M are affine in remaining variables and R quadratic. Then
  Σ_{a,b∈F2}(-1)^{ab+aL+bM}=2(-1)^{LM},
so
  S(Q)=2 S(R+LM).
This removes two variables and preserves degree≤2. A linear Q has sum zero unless it is constant, in which case sum is ±2^p. Hence S(Q) and the exact number of zeros 1/2(2^p+S(Q)) are computable deterministically in poly(p), regardless of cutrank.

Example: Q(u,v)=Σ_{i=1}^k v_iΣ_{j=1}^i u_j. The matrix of cross coefficients between v and u is a lower triangular k×k matrix with diagonal ones, of rank k. Yet S(Q)=2^k and
  # {Q=0}=2^{2k−1}+2^{k−1}.
This quadratic arises from the top-right coordinate of the UT3(F2) group word
  X^{u1}Y^{v1} ... X^{uk}Y^{vk},
with X=I+E12,Y=I+E23, using the convention of right multiplication of group elements. The coordinate is exactly Σ_{j≤i} u_j v_i. Thus high rank occurs in actual nilpotent products, not just abstract quadratic forms.

## 2. General cubic zero counting is #P-hard under arithmetic reductions

Let F=∧_{j=1}^m (ℓ_{j,1}∨ℓ_{j,2}) be a 2-CNF over n Boolean variables, m≥1. Let a_j(x),b_j(x)∈F2 be the FALSE indicators of the two literals in clause j. Introduce fresh Boolean selector y_j and define
  P(x,y)=Σ_{j=1}^m y_j a_j(x)b_j(x) mod 2.
This is multilinear of degree ≤3, with exactly one selector per clause.

For a satisfying x, all m coefficients a_jb_j vanish, so all 2^m selector assignments give P=0. For an unsatisfying x, y↦P(x,y) is a nonzero linear form, so exactly 2^{m−1} selectors give P=0. Thus
  #zeros(P)=2^{m−1}(2^n + #SAT(F)),
  #SAT(F)=#zeros(P)/2^{m−1}−2^n.
As #2SAT is #P-complete, exact zero counting for even this special cubic form is #P-hard under polynomial-time arithmetic/metric reductions.

## 3. Linear cutrank for the same hard cubic family

Start with a SIMPLE 3-regular graph H=(V,E) and monotone 2CNF
  F_H(x)=∧_{uv∈E}(x_u∨x_v).
Its satisfying assignments are vertex covers; counting them is #P-complete even on 3-regular graphs (Greenhill and Vadhan). Let n=|V| and m=|E|=3n/2. Then
  P_H(x,y)=Σ_{e=uv∈E} y_e(1+x_u)(1+x_v).

At the variable-order cut ALL x first, ALL y second, form the mixed-coefficient K matrix whose past rows include monomials x_u x_v and whose future columns include y_e. The coefficient of x_u x_v y_f equals 1 iff f={u,v}. Since H is simple, the m rows indexed by edges and the m columns indexed by edges form I_m. Therefore the cubic residual-coefficient cutrank satisfies
  r>=m = 3n/2 = (3/5)(n+m).
This is an exact LINEAR cutrank example of #P-hard counting for cubic polynomials.

IMPORTANT: This r is the coefficient cutrank of the COALESCED polynomial P(x,y) in the n+m source variables. The original BP reduction below has 10m DISTINCT occurrence-copy inputs. Do not silently equate the two rank parameters without a separate argument for the occurrence-level discrepancy tensor.

## 4. Exact UT4 commutator gadget with ten independently controllable letters

Let
  X=I+E12, Y=I+E23, Z=I+E34 ∈ UT4(F2).
These generators have order two. Their nested commutator satisfies
  [[X^a,Y^b],Z^c] = I + abc E14
for every a,b,c∈{0,1}.

Using the commutator ABA^{-1}B^{-1}, the literal word is
  X^a Y^b X^a Y^b Z^c Y^b X^a Y^b X^a Z^c.
It has ten controlled letters, four X, four Y and two Z. In the actual two-sweep model, EVERY letter is associated with a distinct primary Boolean input COPY, which will be forced consistent only by the second sweep. The first sweep groups the ten letters of each clause j consecutively, where a is the false indicator of ℓ_{j,1}, b of ℓ_{j,2}, c=y_j.

Natural faithful affine action: On the eight states (u,v,w)∈F2³ corresponding to the 4-vector (u,v,w,1), apply:
  X:(u,v,w)↦(u+v,v,w);
  Y:(u,v,w)↦(u,v+w,w);
  Z:(u,v,w)↦(u,v,w+1).
The ten-letter word sends (0,0,0) to (abc,0,0). As all gadgets end in central matrices I+abcE14 under consistent copies, concatenating the clauses yields (P(x,y),0,0).

The second sweep is a THREE-STATE verifier {0,1,dead}, reading all occurrence-copy inputs grouped by their original source variable x_i or selector y_j. At the first letter of a group it stores the read bit (unless already dead); at each later occurrence it rejects if the bit differs. A dead state is absorbing. At a new group, it resets after successfully checking the previous group. Thus exactly one occurrence-copy assignment corresponds to each assignment (x,y), and all inconsistent copies are rejected.

Take the Cartesian product of the 8-state affine group-action register and 3-state equality-checker register: the entire two-sweep program has width 24. First-sweep transitions act by elements of UT4(F2) on the 8-state register and are identity on the checker (hence permutations from a fixed class-three nilpotent group). Second-sweep transitions act only on the checker and are arbitrary deterministic maps. At the end accept iff checker≠dead and group-action register=(0,0,0).

Therefore
  #accept(BP_F)=#zeros(P)=2^{m−1}(2^n+#SAT(F)),
with exactly 10m primary occurrence-copy bits and two sweeps, each a permutation of those same input positions, each bit read once per sweep.

**Theorem (restricted exact counting hardness).** Exact #accepted-input computation for a width-24 deterministic two-sweep BP is #P-hard under a polynomial-time arithmetic/metric reduction even when first-sweep transitions belong to the fixed nilpotent class-three UT4(F2) action and the second sweep only checks equality of variable copies. The target is in #P. This is not a parsimonious reduction from #2SAT.

## 5. Positive UT3 boundary for the equality-only second sweep

Consider the SAME model with fixed UT3(F2) first-sweep transitions and second sweep ONLY checking copy consistency, while the final acceptance predicate depends on the resulting group element and whether the checker survived. After coalescing all copies of each original input bit, there is exactly one consistent assignment per original bit vector. The first-sweep product is a UT3(F2) group-valued function of the original bits.

Its three upper-triangular coordinates q12,q23,q13 are multilinear Boolean polynomials of degree ≤1,≤1,≤2 respectively, even when original bits are repeated many times in the word. To count inputs producing a given element g∈UT3(F2), use F2³ Fourier inversion:
  # {x:Q(x)=g}
     = 1/8 Σ_{λ∈F2³} (-1)^{λ·g} Σ_{x∈F2^n} (-1)^{λ·Q(x)}.
Each inner sum has quadratic phase and is polynomial-time computable by Section 1's Gaussian elimination. Since UT3 has just 8 elements, any fixed or explicitly supplied accepting subset can be handled by summing over its elements. Therefore exact #SAT for this restricted UT3 model is in P; for UT4 it is #P-hard under the stated reduction.

This is a COUNTING-only threshold, not a decision-complexity threshold. Nilpotent-group ProgramSat decision is known to be polynomial-time for fixed groups (Goldmann-Russell, surveyed in Idziak et al. ICALP 2022).

## 6. Interpretation for the original L/poly and LGS research goal

- Bounded algebraic DEGREE (even 3) and origin in fixed-depth unitriangular products do not by themselves imply polynomial exact contraction when the cutrank is large.
- Quadratic phases admit a Gaussian technique that bypasses cutrank entirely, so treating cutrank as a universal lower-bound proxy is demonstrably wrong.
- Exact counting hardness at cubic degree does NOT rule out a 2^{o(p)} decision-SAT algorithm for two-sweep polynomial-width BP, nor does it yield an ETH/#ETH lower bound (especially in the post-Oct-2026 landscape).
- The specific gadget family has easy decision satisfiability because a fixed nilpotent-group ProgramSat instance with equality-only copy checking reduces to group-word satisfiability. The new hardness result is NOT NP-hardness for that restricted decision problem.
- Further work should seek an existential interface/positivity representation for the arbitrary SECOND sweep, not only compression of a signed cubic exponential sum.

## Reproducible cross-checks

- /mnt/data/check_ut4_cubic_obstruction.py — exhaustive 8-value UT4 gadget check, 300 random 2-CNF count identities, and exhaustive 2^10 occurrence-copy assignments for a one-clause instance.
- /mnt/data/check_quadratic_gauss.py — 540 random quadratic Gauss sums and seven triangular full-cutrank families.
Both scripts were run successfully; mathematical claims follow the proofs above, not the experiments.

## Relevant sources

- Valiant, The Complexity of Enumeration and Reliability Problems (1979): https://doi.org/10.1137/0208032
- Vadhan, The Complexity of Counting in Sparse, Regular, and Planar Graphs (2001): https://doi.org/10.1137/S0097539797321602
- Catherine Greenhill, The complexity of counting colourings and independent sets in sparse graphs (2000): https://web.maths.unsw.edu.au/~csg/papers/complexity.pdf
- Idziak, Kawałek, Krzaczkowski, Weiß, Satisfiability Problems for Finite Groups (ICALP 2022): https://doi.org/10.4230/LIPIcs.ICALP.2022.127
- Earlier checkpoint: docs/28_class3_cubic_and_unitriangular_higher_degree.md
