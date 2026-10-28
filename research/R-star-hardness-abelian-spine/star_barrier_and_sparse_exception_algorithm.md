# R — A5 star-interaction hardness versus an abelian-spine algorithm

Checkpoint 2026-10-28. **Status:** two unconditional, explicitly proved structural statements. (R1) NP-completeness of a target-5-cycle width-five permutation-program SAT subclass whose normalized variable-noncommutation graph has vertex-cover number ONE. (R2) a deterministic \(2^{O(r)}\mathrm{poly}(L,p)\) algorithm and a \(O(p(r+1))\)-universe Set Cover compilation when there are only \(r\) exceptional nonabelian **instruction occurrences**. These are a mathematical barrier and a positive special-case bound, **not** a general \(2^{o(p)}\) algorithm for all LGS, **not** a proof of NEXP versus L/poly, and **not** a claim of prior-art novelty. Based on research/Q-semantic-commutation.

## 1. Formal group-program model

We work in \(G=A_5\), acting on five states. A normalized program is a word
\[
W(x)=h_1^{x_{i_1}}\cdots h_L^{x_{i_L}},\quad h_t\in A_5,
\]
with input bits \(x_1,\ldots,x_p\). An instruction is the group-program transition \((i_t,1,h_t)\), so the zero-input baseline is **exactly identity** and the normalized deltas from branch Q equal \(h_t\). Define \(J_W\) on the input bits, with an edge \(ij\) iff some \(h_s\) labeled \(x_i\) fails to commute with some \(h_t\) labeled \(x_j\) (\(i\ne j\)).

Fix a specific 5-cycle \(\gamma\in A_5\). The decision question is whether \(W(x)=\gamma\) for some \(x\). This is equivalent via Barrington's ring graph to a graphic-LGS connectivity instance, because the ring is connected iff its permutation product is a 5-cycle. In reductions where the word can also take other 5-cycle values, the target equality should be maintained explicitly; the reduction below produces only \(1\) or \(\gamma\) on its intended \(y=1\) branch and at most 3-cycles when \(y=0\). Add permanently **inactive** graph edges to ensure the *ground graph* is connected without changing selected graph connectivity if necessary.

## 2. Universal star normal form

Fix a 3-cycle \(a=(1\,2\,3)\in A_5\) and its cyclic group \(H=\langle a\rangle\) of order 3.

**Lemma R1 (constant-length factorization).** Every \(h\in A_5\) is a product of at most TWO 3-cycles, each of which is \(c a c^{-1}\) for some \(c\in A_5\). This is a constant-size finite-group fact: the 20 conjugates of \(a\) generate \(A_5\), and their products together with identity already cover all 60 elements. A full exhaustive finite enumeration is included in the test script; alternatively classify the elements into identity, 3-cycles, double transpositions and 5-cycles.

**Theorem R2 (star normalization, input-preserving).** For every normalized A5 word \(W(x)\) of length L and p variables, construct a new normalized A5 word \(Q(x,y)\) using **just one new Boolean variable** \(y\) and at most \(6L\) instruction positions such that:

1. \(Q(x,1)=W(x)\) pointwise for every \(x\);
2. \(Q(x,0)\in H\) for every \(x\);
3. \(J_Q\) has vertex-cover number at most ONE, covered by \(\{y\}\). In fact every instruction controlled by an original \(x_i\) uses the SAME nonidentity permutation \(a\).

Construction: for every original factor \(h_t^{x_i}\), take its R1 decomposition \(h_t=\prod_{j=1}^{k_t}c_j a c_j^{-1}\), \(k_t\le2\), and substitute, for each \(j\), three instructions
\[
     \boxed{c_j^{y}\;a^{x_i}\;(c_j^{-1})^{y}.}
\]
For y=1, this is \((c_j a c_j^{-1})^{x_i}\): if x_i=0 the outer c's cancel, and if x_i=1 the intended conjugate remains. For y=0, it is \(a^{x_i}\). Thus Q reproduces W on y=1 and lies in H on y=0. All original-variable deltas equal a and hence commute with each other, giving the asserted star \(J_Q\). Length at most \(3\cdot2L=6L\). Construction time O(L) after hard-coding 60 group decompositions. QED.

Because \(\gamma\) has order 5 and \(H\) has order 3, \(Q(x,y)=\gamma\) is satisfiable iff \(W(x)=\gamma\). This is a direct p->p+1, L->6L satisfiability reduction.

**Corollary R3 (NP-completeness at interaction vertex-cover one).** Target-5-cycle A5-program SAT is NP-complete even on the promised class where \(J_W\) has a vertex cover of size 1 and all other variable-controlled deltas are the SAME 3-cycle a. To see NP-hardness, take a 3CNF formula F on p inputs, add one independent input z and use \(F(x)\land z\). Barrington's theorem constructs a polynomial-length width-five A5 group program P returning \(\gamma\) on true and 1 on false. Its all-zero assignment is false because z=0, hence P(0)=1. Apply the exact baseline normalization from branch Q to P, obtaining the normalized delta word W with \(W(x)=P(x)\), length unchanged. Finally apply R2 to get Q and target \(\gamma\). Then Q accepts iff F is satisfiable. Membership in NP is immediate by evaluating the group word on a guessed assignment. The number of independent variables increases only by 2: p original, one z, one y. This reduction is polynomial-time (the formula is a balanced log-depth AND of width-3 clauses). QED.

**Implications and sharp scope.** Any algorithm depending only polynomially on p,L and exponentially on the **number of exceptional variables** (a vertex cover of J), e.g. \(2^{O(\mathrm{vc}(J))}\mathrm{poly}(p,L)\), would imply P=NP. This result does NOT yield a \(2^{\Omega(p)}\) lower bound and does not contradict a hoped-for \(2^{o(p)}\) algorithm. It is a barrier to the *structural parameter*, not to the post-ETH project. In an associated LGS ring gadget, the graph is connected iff the product is a 5-cycle, so the same class includes NP-hard LGS instances; generic branching programs are still more expressive than permutation-only programs.

## 3. A positive converse when exceptional occurrences are few

Let \(W(x)\) now be a normalized group word over any **fixed finite group** G, with a supplied subset \(B\subseteq[p]\) of exceptional variables (\(b=|B|\)) such that **every instruction belonging to a non-exceptional variable** has its delta in the same fixed abelian subgroup \(H\le G\). No normality assumption on H is needed.

Let \(r\) count **instruction positions** whose variable belongs to B (including repeated appearances). Divide W at these r positions:
\[
W(x)=F_0(x)\,c_1(x_B)\,F_1(x)\cdots c_r(x_B)\,F_r(x),
\]
where each \(c_j\) is a single B-variable-controlled group element and each \(F_j\) consists only of factors in H.

Since H is abelian, within each segment j all factors of a given ordinary variable can be grouped:
\[
  F_j(x)=\prod_{i\notin B}g_{ij}^{x_i},\qquad
  g_{ij}\in H,
\]
and the \(g_{ij}\) values are computable by one O(L)-time pass.

**Theorem R4 (abelian spine, bounded exceptional occurrence).** Given B and H as above, target-set satisfiability \(W(x)\in T\subseteq G\) is decidable deterministically in

\[
 \boxed{2^b|H|^{r+1}\operatorname{poly}(L,p)=2^{O_w(b+r)}\operatorname{poly}(L,p)}
\]
for fixed group G. In particular, if all exceptional variables appear at least once then b<=r and this is \(2^{O_w(r)}\operatorname{poly}(L,p)\).

Proof: enumerate all 2^b values of x_B, fixing c_1,...,c_r. For each other variable i, its contributions to the r+1 segments form a fixed vector \(\mathbf g_i=(g_{i0},...,g_{ir})\in H^{r+1}\). Maintain the reachable subset of H^{r+1}, initialized to the identity tuple. For each i, update \(D\leftarrow D\cup\{d\mathbf g_i:d\in D\}\); at most |H|^{r+1} tuples exist. Every reachable tuple equals exactly the possible vector of simultaneous segment products for some assignment to all nonexceptional variables, by induction. For each tuple evaluate \(F_0 c_1 F_1\cdots c_r F_r\) in the constant group and check membership in T. The total time is bounded as claimed. QED.

For width-five A5 programs one may take |H|≤5. Thus r=O(log p) already gives a polynomial-time solver for polynomial-length programs, **even when the noncommutation graph has one giant component and H is not normal in A5**. When r=o(p), we get deterministic \(2^{o(p)}\operatorname{poly}(L)\).

### Pointwise compilation and Set Cover

In fact the same factorization yields a **Boolean circuit for the whole acceptance function**, without enumerating B or the possible segment-value tuples: compute each F_j by at most p lookups/multiplications in the **fixed** finite group H (after O(L) preprocessing for g_ij), then interleave the O(r) original exceptional controlled factors and check the desired output. The circuit has size

\[
  g=O_G(p(r+1)+r).
\]

Thus by standard parsimonious Tseitin + SAT-to-SetCover construction, the program admits a **deterministic pointwise** Set Cover reduction with
\[
\boxed{u,t,\text{budget}=O_G(p(r+1))}
\]
and polynomial construction time, even if L=p^100. When r=O(1), this is a genuine **O(p)-universe** reduction for programs with arbitrarily dense, irregular rereads of nonexceptional variables.

Observe carefully that Theorem R4's stronger 2^{O(r)} decision rate does **not** make the Set Cover universe O(p) when r grows; the direct circuit has size O(pr). Neither theorem handles the NP-hard star instances from R3, whose sole exceptional variable y occurs \(\Theta(L)\) times.

## 4. What this teaches for LGS -> Set Cover and NEXP goals

The earlier Q algorithm parameterized by the largest noncommutation component is not salvageable by replacing "component size" with "size of a vertex cover of the interaction graph": R3 shows NP-hardness for vertex cover 1. The missing complexity is the **number and order of context-changing occurrences**, not just the number of variables creating those changes.

For small exceptional occurrence r, R4 handles **non-normal abelian spines**, improving the structural coverage of Q3, which required a nilpotent *normal* subgroup and counted exceptional variables. For arbitrary r, the NP-hard star construction gives an explicit hard family, so a universal polynomial algorithm for "one exceptional variable" cannot exist unless P=NP.

This advances the structural map but does NOT yield the desired general LGS(p,S)->SetCover(u=O(p)) reduction, any new ETH replacement, or any circuit lower bound. The next research target should attack the ordering/interaction complexity of the exceptional factors themselves, rather than treating each variable's total group support as an invariant.

## 5. Audit and sources

- Barrington, *Bounded Width Branching Programs*, MIT 1986 / JCSS 1989: https://dspace.mit.edu/entities/publication/7b16f29b-5ef5-4614-95c8-3546518e4ece
- Idziak–Kawałek–Krzaczkowski–Weiß, *Satisfiability Problems for Finite Groups*, ICALP 2022: https://doi.org/10.4230/LIPIcs.ICALP.2022.127
- Goldmann–Russell nilpotent-group ProgramSat theorem: cited and discussed in the preceding paper.
- Reproducible local Python checks: all 60 A5 elements are products of <=2 conjugate 3-cycles; 120 seeded random normalized A5 words (all assignments, with and without y); 220 seeded random abelian-spine words, comparing R4 to exhaustive satisfiability. All passed. These tests do not certify literature priority or prove NC1 versus NEXP facts.
