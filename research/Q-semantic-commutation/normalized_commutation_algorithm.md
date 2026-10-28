# Q — Semantic compression by normalized noncommutation (width-five permutation programs)

Checkpoint 2026-10-28. **Status:** exact elementary identities, a deterministic \(2^{O(k)}\mathrm{poly}(L,p)\) algorithm for a structural class, and a polynomial-size Set Cover reduction under a quantified promise. This is NOT an algorithm for all polynomial-size LGS, and NOT a NEXP lower bound. These ideas are in the established tradition of programs over finite groups/monoids; **no priority or literature novelty claim**. Source branch \`research/P-block-sperner-set-cover\`; prior block/SLP results are inherited.

## 1. Group programs and an exact baseline normalization

Take a width-\(w\) **permutation** branching program with \(L\) sequential instructions \((i_t,g_t(0),g_t(1))\), where \(g_t(b)\in S_w\); only input bit \(x_{i_t}\) controls the \(t\)th permutation. Let group multiplication be associative, with \(P(x)=g_1(x_{i_1})\cdots g_L(x_{i_L})\). Fix the zero-input baseline

\[
 A_t=g_1(0)\cdots g_t(0), \qquad A=A_L.
\]

Define a conjugated delta

\[
 h_t=A_t\bigl(g_t(0)^{-1}g_t(1)\bigr)A_t^{-1}.
\]

**Lemma Q1 (pointwise identity).** For every \(x\in\{0,1\}^p\),

\[
 \boxed{P(x)=\Big(\prod_{t=1}^L h_t^{x_{i_t}}\Big)A.}
\]

Proof: \(g_t(x)=g_t(0)d_t^{x_{i_t}}\) with \(d_t=g_t(0)^{-1}g_t(1)\). Each \(d_t\) can be transported past its zero-baseline neighbors by conjugation with \(A_t\). Formally the ordered product of the first \(j\) normalized deltas equals \(g_1(x)\cdots g_j(x)A_j^{-1}\), by induction on \(j\). Multiplying by \(A_j\) gives the formula. QED.

The baseline permutations \(g_t(0)\) can have arbitrary noncommutation and no short SLP; what matters in Q is the family of **normalized deltas** \(h_t\), computed in \(\mathrm{poly}(L,w)\).

## 2. Interaction graph and unconditional algorithm

Build the **cross-variable noncommutation graph** \(J\) on the \(p\) input indices. Put \(\{i,j\}\in E(J)\) if some normalized deltas \(h_s,h_t\) with \(i_s=i,i_t=j\) do not commute (\(h_sh_t\ne h_th_s\)). Let its connected components be \(C_1,\ldots,C_c\), and let \(k=\max_j|C_j|\).

All delta elements belonging to *different* components commute with each other. Therefore we may stably sort the normalized word by component, without affecting its product:

\[
 P(x)=F_{C_1}(x|_{C_1})\cdots F_{C_c}(x|_{C_c})A,
\]
where \(F_C\) is the ordered product of just the normalized deltas whose variables lie in \(C\).

**Theorem Q2.** For constant width \(w\), satisfiability of **any fixed final-output predicate** \(P(x)\in T\subseteq S_w\) is decidable deterministically in

\[
 \boxed{\left(L\sum_C2^{|C|}+\mathrm{poly}(L,p)\right)O_w(1)
       \ \subseteq\  2^{k}\mathrm{poly}(L,p).}
\]

Proof: enumerate all assignments to the variables of a component \(C\) (at most \(2^{|C|}\)), scan its subsequence of normalized deltas and record the resulting permutation. This yields an attainable-value set \(V_C\subseteq S_w\) with at most \(w!\) elements. Combine the attainable sets sequentially by group multiplication, keeping at most \(w!\) outputs at every step; multiply by the constant \(A\) at the end and check \(T\). Independence of variable sets across components and pairwise commutation across components make this exact. Generating \(J\) naively costs \(O(L^2)\) group-commutation checks, polynomial in the input. QED.

- If \(k=O(\log p)\), this is deterministic **polynomial time** even for explicit programs of length \(p^{100}\).
- If \(k=o(p)\), it is deterministic \(2^{o(p)}\mathrm{poly}(L)\).
- There is **no SLP promise** and **no block-locality promise**. Even a raw instruction sequence with no useful syntactic repetitions can satisfy Q2.
- Barrington's polynomial-length width-five permutation programs fit the *model*, but generic hard programs need not have small interaction components. This is a structural subclass, not a general NC1-SAT speedup.

### Set Cover compression as a corollary

Given the complete truth table \(F_C:\{0,1\}^{|C|}\to S_w\) for each component, construct a fan-in-two multiplexer/decision-tree circuit with \(O_w(2^{|C|})\) gates computing its output encoding. Combine component outputs by \(O_w(c)\) group-multiplication gates and check the fixed acceptance predicate. With the original input wires, total gate size is

\[
 g=O_w\left(p+\sum_C2^{|C|}\right).
\]

A standard parsimonious Tseitin CNF and variable/clause-to-SetCover conversion (see branch P) yield an ordinary Set Cover instance with

\[
 \boxed{u,t,\text{budget}=O_w\left(p+\sum_C2^{|C|}\right).}
\]

Hence **\(u=O(p)\)** whenever \(\sum_C2^{|C|}=O(p)\), for instance if **every component contains at most a fixed constant number of variables**. A component of size \(O(\log p)\) guarantees polynomial construction but may yield a superlinear Set Cover universe; distinguish these thresholds.

## 3. Extensions and literature boundary

The group normalization also works for deterministic finite-state transformations \(g_t(b):[w]\to[w]\), provided one **baseline branch** \(g_t(b_t)\) is a permutation for every instruction. Choose that branch as a baseline, set \(d_t=g_t(b_t)^{-1}g_t(1-b_t)\) (possibly noninvertible), and conjugate by the accumulated permutation baseline. Then

\[
 P(x)=\prod_t h_t^{[x_{i_t}\ne b_t]}\,A.
\]

Noninvertible \(h_t\) are in the finite transformation monoid \(T_w\) of size \(w^w\); all cross-variable commutativity, component enumeration and the \(2^k\mathrm{poly}(L)\) algorithm carry over. Grouping components does NOT require invertibility of deltas, only of baseline maps used to normalize. For a given variable, local \(F_C\) simply tests its actual 0/1 value, rather than assuming every factor is \(h_t^{x_i}\). This extension does not cover arbitrary BP layers lacking an invertible branch.

**Important prior art:** Goldmann–Russell proved polynomial-time ProgramSat for fixed finite nilpotent groups and NP-completeness for non-solvable groups. See Idziak–Kawałek–Krzaczkowski–Weiß, *Satisfiability Problems for Finite Groups*, ICALP 2022, https://doi.org/10.4230/LIPIcs.ICALP.2022.127 . Barrington's width-five programs compute NC1 using a non-solvable subgroup of \(S_5\), https://doi.org/10.1016/0022-0000(89)90037-8 . Do not present a polynomial algorithm for purely nilpotent group programs as novel.

**Stronger corollary from existing nilpotent-ProgramSat literature:** replace enumeration of a component \(C\) by the existing polynomial-time ProgramSat algorithm whenever the subgroup \(\langle h_t:i_t\in C\rangle\) is nilpotent. For fixed width, subgroup detection and per-target feasibility can be done effectively on a constant-size group; run the solver once per each of at most \(w!\) target permutations. Only components generating non-nilpotent subgroups must be enumerated. Thus time is \(2^{k_{\mathrm{hard}}}\mathrm{poly}(L,p)\), where \(k_{\mathrm{hard}}\) is the largest **nonnilpotent** component size (0 if none), subject to the exact published deterministic ProgramSat theorem. This is a synthesis/structural corollary, not a claimed new group-SAT theorem.

## 4. Tests and an illustrative high-H instance

A deterministic Python verifier tested the normalization formula on 450 seeded random width-five permutation programs, \(1\le p\le8\), \(1\le L\le25\), for **every input assignment**. It also verified equality of the attainable output sets computed by independent component enumeration and direct full assignment enumeration. Half of the programs used arbitrary random baseline permutations together with controlled normalized deltas supported either on \(S_3\) acting on \(\{0,1,2\}\) or on the commuting transposition \((3\,4)\), so the interaction graph has components of size at most two despite arbitrary-looking input instructions. All 450 cases passed.

To construct arbitrarily long examples: choose an arbitrary sequence of zero-input permutations \(g_t(0)\), and independently choose desired normalized delta \(h_t\) from a fixed abelian subgroup (for instance powers of a five-cycle). Put \(A_t=g_1(0)\cdots g_t(0)\), and define

\[
 g_t(1)=g_t(0)\,A_t^{-1}h_t A_t.
\]

Then the normalized delta is exactly \(h_t\) and all variables commute in the normalized representation, no matter how irregular the baseline is. If L=p² and every input is queried in Theta(p) layers scattered throughout the word, the branch P block-incidence H may be Theta(p²), while Q yields an O(p)-size circuit and O(p)-universe Set Cover. This avoids the **syntactic** SLP mechanism of P2.

## 5. Where to attack next

1. Instead of requiring disjoint commuting components, exploit **bounded nilpotent class / low-degree commutator corrections**. If the delta subgroup has nilpotency class two, sorting factors introduces only central terms of degree at most two in input bits. Seek a near-linear-size circuit for the induced sparse or low-rank quadratic interaction, even when the noncommutation graph is one giant component. But compare with the known full polynomial-time nilpotent ProgramSat theorem before claiming a new solver.
2. For non-solvable S5 hard cores (A5), find an algorithm that exploits the *complexity of interleaving noncommuting variable families*, not merely their membership in one interacting component.
3. Check whether any subexp-width semantic decomposition applies to arbitrary **non-permutation** deterministic BPs, which require the NEXP vs L/poly transfer; the results here alone only address permutation/partially invertible layers, hence a weaker verifier class.
4. Test Set Cover construction rigorously on small transformed circuits, but do not conflate a semantic proof of circuit size with a new complexity separation.

Primary literature: Barrington (JCSS 1989); Idziak et al. (ICALP 2022); Szegedy, programs over commutative monoids (JCSS 1993), https://doi.org/10.1016/0022-0000(93)90039-Y.


## 6. A stronger hard-core parameter via a nilpotent normal subgroup

The plain component-size parameter \(k\) misses the case of a giant noncommutation component whose normalized deltas lie in a **nilpotent group**; these cases are already polynomial-time by Goldmann–Russell. Here is a strictly stronger structural corollary combining normalization with that published algorithm.

For each interaction component \(C\), let \(K_C\le S_w\) be the subgroup generated by its normalized deltas, and let \(N_C\triangleleft K_C\) be a fixed **nilpotent normal subgroup**. (For a canonical choice take the Fitting subgroup \(F(K_C)\), the largest nilpotent normal subgroup.) Define

\[
B_C=\{i\in C:\exists t\;(i_t=i,\ h_t\notin N_C)\},\quad b_C=|B_C|,
\qquad b_*=\max_C b_C.
\]

**Theorem Q3 (structural synthesis).** At fixed width \(w\), satisfiability of a finite-group program with an arbitrary constant-size output acceptance condition is deterministic in

\[
\boxed{2^{b_*}\mathrm{poly}(L,p).}
\]

Proof: for each component \(C\), enumerate assignments to its \(b_C\) exceptional variables. Within one assignment, the factors \(h_t^{x_i}\) of exceptional variables become fixed group constants in \(K_C\), while all remaining variable-controlled factors lie in \(N_C\). Let \(C_t\) be the product of the exceptional constants encountered up to the current position. Moving these fixed factors to the right conjugates the remaining variable factors by \(C_t\). By **normality** \(C_t h C_t^{-1}\in N_C\) for all \(h\in N_C\). Thus the component word becomes a standard Boolean-input **program over the nilpotent group \(N_C\)** followed by a constant group element. By the established polynomial-time nilpotent ProgramSat theorem, for each target \(g\in K_C\) one can determine in polynomial time whether the component can output \(g\); there are only \(O_w(1)\) possibilities. Union those possible outputs across all exceptional branches, at cost \(2^{b_C}\mathrm{poly}(L,p)\). Then combine the independent component output sets by finite-group multiplication as in Q2, in \(O_w(p)\) time. Total \(2^{b_*}\mathrm{poly}(L,p)\). QED.

This can give polynomial time even when \(J\) consists of ONE component of size \(p\), so Q2's component-size bound is useless. It also gives subexponential time when \(b_*=o(p)\).

The normality condition is essential to this argument: an exceptional fixed word can conjugate ordinary variable factors out of an arbitrary nonnormal nilpotent subgroup, possibly generating nonnilpotent behavior. Do not state a bound merely from being close to **some** nilpotent subgroup unless normality (or a substitute) is established.

For \(K_C=S_5\) or \(A_5\), the Fitting subgroup is trivial, so arbitrary Barrington-style hard cores are NOT handled. This is exactly where the approach must be strengthened to address the post-ETH project.

**Verification:** 400 seeded random \(D_8\) group words acting on five states, with a normal Klein-four subgroup \(V_4\), were exhaustively checked over every input assignment for the exceptional/normal factorization; all passed. This does not implement or independently audit Goldmann–Russell's general nilpotent-group algorithm. Primary reference: Idziak–Kawałek–Krzaczkowski–Weiß, ICALP 2022, https://doi.org/10.4230/LIPIcs.ICALP.2022.127 .


## 7. Exact obstruction at the Barrington A5 core

The normalized component method has a sharp limitation in \(S_5\).

**Lemma Q4.** If some interaction component \(C\) generates a subgroup containing \(A_5\), then every delta of every variable *outside* \(C\) is the identity. In particular, after dropping dummy variables, the interaction graph has just that one component.

Proof: by definition any delta outside \(C\) commutes with every delta in \(C\), and hence lies in the centralizer \(C_{S_5}(\langle h_t:i_t\in C\rangle)\subseteq C_{S_5}(A_5)\). The latter centralizer is trivial: an element commuting with all 3-cycles must preserve every 3-element subset of \(\{1,\ldots,5\}\), and therefore fix every point. Thus the outside delta is identity. QED.

Moreover the Fitting subgroup of \(A_5\) and of \(S_5\) is trivial, so the nilpotent-normal-core parameter of Q3 also offers no reduction in this case. These are algebraic obstructions **for our structural methods**, not lower bounds against arbitrary SAT algorithms.

This points the research toward *partial A5/S5 noncommutative behavior* and a new way to summarize nested commutators, not simply more commuting-group components. Barrington's theorem explicitly uses a non-solvable group to simulate general logarithmic-depth computation.
