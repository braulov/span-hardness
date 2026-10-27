# Williams transfer: exact requirements and a genuine graphical bridge

Research checkpoint, 27 October 2026. These are mathematical deductions and source checks, not a claim that the requested full win-win has been established.

## 1. Literature statements that can safely be used

Write `n` for independent circuit inputs and `s` for gates. Keep these distinct from a target graph's vertices `v`, edges `m`, and the total number `N` of combinatorial objects.

**Williams, full version of STOC 2010, Theorem 1.1.** If, for every constant `k`, Circuit-SAT with `n` inputs and `n^k` gates has a deterministic or co-nondeterministic algorithm taking `2^n poly(n^k)/g(n)`, where `g` is superpolynomial, then `NEXP` is not contained in `P/poly`. A deterministic `2^{o(n)} poly(s)` algorithm is more than sufficient. Theorem 1.2 gives an exponential circuit-size lower bound for a language in `E^NP` from a deterministic/co-nondeterministic `2^{(1-delta)n} poly(s)` algorithm for unrestricted Circuit-SAT. Theorem 6.1 explicitly proves: the falsity of ETH implies `E^NP` has no linear-size circuit family.

Source: [Williams, Improving Exhaustive Search Implies Superpolynomial Lower Bounds](https://people.csail.mit.edu/rrw/improved-algs-lbs2.pdf), Theorems 1.1, 1.2, 6.1.

**Williams, ACC paper, Theorem 1.3.** For a circuit class `C` containing `AC0` and closed under composition, there is a constant `a` such that SAT for every polynomial-size `C` family in `O(2^n/n^a)` implies `NTIME[2^n]` does not have polynomial-size `C` circuits. Boolean formulas/nonuniform `NC1` are an explicit permitted example. In particular, a deterministic `2^{o(n)} poly(s)` Formula-SAT algorithm implies `NEXP` is not contained in nonuniform `NC1`.

Source: [Williams, Non-Uniform ACC Circuit Lower Bounds](https://people.csail.mit.edu/rrw/acc-lbs.pdf), §1, Theorem 1.3 and §2 definition of circuit class.

These requirements do **not** license replacing `n` by a polynomial in `n` in the exponent. Ordinary bounded-error randomized SAT also does not automatically satisfy the quoted co-nondeterministic requirement: nondeterministically guessing a random seed could certify a false claim of unsatisfiability. Any randomized extension needs its own correct theorem or a derandomization step. The deterministic implications stated below avoid that issue.

If the October fixed-width SAT theorem is correct and genuinely deterministic subexponential in the ordinary variable count, the linear-size lower bound in Theorem 6.1 is already a consequence. It is not a new payoff obtainable only from a span hypothesis.

## 2. A parameter-preserving graphical encoding of NC1

This construction needs neither gate variables nor a Boolean circuit inside the activation rule. Every active edge is controlled by a single input literal or constant. All logical computation occurs through the topology of the selected graph.

### Definition: a cyclic permutation switching graph

An instance consists of `n` Boolean switches and `L >= 3` layers, each containing five vertices. At layer `i`, input `x_{j_i}` chooses one of two perfect matchings from that layer to the next; the last layer connects back to the first. The matchings are specified by two permutations `p_{i,0}, p_{i,1}` of `[5]`. When the two options use the same edge, it can be merged into a constantly present edge. Equivalently, use a multigraph with edge labels `x_j`, `not x_j`, or constants.

For every assignment the selected graph is 2-regular. The decision problem asks whether some assignment makes it connected. Potential but permanently absent edges can be added to make the ground graph connected, so the test is exactly full graphic span against the ground rank.

### Lemma 1: permutation cycles equal graph components

Let

`P_x = p_{L-1,x_{j_{L-1}}} ... p_{0,x_{j_0}}`.

Then the selected graph has exactly `c(P_x)` connected components, where `c` denotes the number of permutation cycles. Therefore

`rank_M(Y(x)) = 5L - c(P_x)`.

**Proof.** Each vertex has exactly one selected edge to the next layer and one to the preceding layer. Starting at `(0,a)`, move successively forward around the layers. After one circuit the walk reaches `(0,P_x(a))`. Its intersection with layer zero is exactly the orbit of `a` under `P_x`. Distinct orbits cannot connect, since each selected vertex has degree two and the forward and backward moves are inverses. Every component meets layer zero. Thus components are in bijection with permutation cycles. The usual graphic rank formula gives the displayed equality. ∎

### Lemma 2: exact preservation of independent input bits

For every fan-in-two depth-`d` Boolean circuit `F(x_1,...,x_n)`, one can construct a cyclic permutation switching graph with exactly the same `n` switches, `O(4^d)` vertices and edges, and no local CSP constraints, such that for every assignment `x`,

`F(x)=1 iff rank_M(Y(x))=rank_M(E)`.

The underlying graph can be required to be connected. It uses only literal and constant edge labels. The construction is polynomial in its output length.

**Proof.** Barrington's theorem constructs a width-five permutation program of length at most `4^d` whose product is a fixed five-cycle `alpha` when `F(x)=1` and the identity when `F(x)=0`. Its instructions read only the original variables. Add identity instructions if necessary to obtain `L >= 3`. Form the cyclic graph of Lemma 1. If `F(x)=1`, then `c(P_x)=1`; otherwise `c(P_x)=5`. Hence the selected graph is connected exactly when `F(x)=1`. Add at most `5L-1` never-selected edges forming a spanning tree of the vertex set. These ensure the ground graph has rank `5L-1` and leave every selected graph unchanged. Lemma 1 now proves the full-span equivalence. There are `5L` vertices and at most `10L + (5L-1)` potential edges. No switch variable was introduced. ∎

The black-box input is [Barrington's original paper](https://doi.org/10.1016/0022-0000(89)90037-8); the five-cycle-versus-identity theorem and the `4^d` bound also appear explicitly in the [STOC version, Theorem 1](https://cctbio.ece.umn.edu/wiki/images/3/3f/Barrington_Bounded-Width_Polynomial-Size_Branching_Programs_Recognize_Exactly_Those_Languages_in_NC1.pdf). This graph adaptation is proved here; no novelty claim is made.

### Theorem 3: an actual algorithm-to-lower-bound implication

If literal-controlled graphic full-span is deterministically decidable in

`2^{o(n)} poly(v+m)`

where `n` counts independent switches, even just on the cyclic width-five instances above, then

`NEXP is not contained in nonuniform NC1`.

**Proof.** Every `NC1` circuit on `n` inputs has depth `c log n`, for some fixed `c`, so Lemma 2 produces at most `O(n^{2c})` objects. The assumed algorithm therefore decides its satisfiability in `2^{o(n)} n^{O(c)}`. For each fixed `c` this is eventually at most `2^n/n^a`, for every constant `a`. Apply Williams's Theorem 1.3 for `C=NC1`. ∎

The same proof works if one assumes sufficiently large inverse-polynomial savings, uniformly for every polynomial description size. A `2^{o(N)}` algorithm where `N=Theta(v+m+n)` does **not** suffice: Lemma 2 may have `N=n^{2c}`.

This is a real, restricted graphical bridge and a weaker target than the requested `NEXP` versus `P/poly` separation. Its truth-side limitation is serious: hardness of this switching problem does not imply hardness of Hamiltonian Cycle, FVS, or Set Cover in their ordinary parameters. No reduction in that direction has been proved here.

### Observation: this subfamily is exactly an NC1 predicate model

For the reverse direction, represent each of the 120 elements of `S5` using a constant number of bits. Evaluate the selected permutation product by a balanced binary tree of constant-size multiplication circuits. This uses `O(L)` gates and `O(log L)` depth. A constant-size final circuit decides whether the product is a five-cycle. Thus the cyclic width-five graph predicate has linear-size, logarithmic-depth Boolean circuits, without auxiliary inputs.

Combined with Lemma 2, polynomial-length cyclic width-five switching graphs and nonuniform `NC1` have the same predicate expressiveness. This identifies the correct circuit target for this model. Extending its Williams conclusion to `P/poly` would require an additional new argument, not just an appeal to genericity of the rank predicate.

It also means that a valid SAT theorem handling `O(n)`-gate Boolean circuits in `2^{o(n)}` could eliminate the **linear-description** version of this graph hypothesis immediately. The polynomial-description, input-bit-parameter version remains quantitatively different.

## 3. Two rigorous barriers, with carefully limited conclusions

### Lemma 4: predicate-preserving linear compression is impossible by counting

Fix constants bounding local arity and the total number of local predicates, graph vertices, edges, and switch variables by `C n`. Permit explicit graphic/cographic direct sums, literal or constant-arity activations, and explicit constant-arity truth tables. The number of predicates on `n` named input bits representable by such instances is at most `2^{O(n log n)}`.

In contrast, polynomial-size circuits on `n` inputs realize at least `2^{Omega(n^2)}` distinct predicates. Hence not every polynomial-size circuit predicate has such an `O(n)`-object representation.

**Proof.** Graph incidence, component/type information, input indices for bounded-arity activations, and local scopes require `O(n log n)` bits altogether. Constant-size truth tables contribute only `O(n)` bits. The number of representations bounds the number of represented predicates. For the second statement, take `q=floor(2 log_2 n)` input bits. There are `2^{2^q}=2^{Omega(n^2)}` distinct Boolean functions of those `q` bits. Every one has a disjunctive-normal-form circuit with at most `O(q 2^q)=O(n^2 log n)` gates, so all are among polynomial-size `n`-input circuit predicates. The counts differ for sufficiently large `n`. ∎

This is an unconditional obstruction to **exact predicate** compression, not to satisfiability-only reductions. A satisfiability reduction need preserve only one bit, so the counting argument does not prohibit it. It also does not cover succinct/implicit graph descriptions.

### Lemma 5: a computational barrier for polynomial graph compilation

Suppose every `n`-input polynomial-size Boolean circuit can be compiled into a polynomial-size explicit graphic/cographic span instance with precisely those input bits, no extra existential bits, and constant-arity local/activation predicates, preserving acceptance for **every** assignment. Then

`P/poly is contained in L/poly`.

**Proof.** The compiled instance can be stored as polynomial advice. Given an input assignment, its local constraints and edge membership are computable in logarithmic workspace. Graphic full-span means the selected graph has the same connected components as the ground graph; this can be tested in logarithmic space using undirected reachability. Cographic full-span is equivalent to acyclicity of the complement edge set. Acyclicity is logarithmic-space decidable: a loop rejects; for each nonloop edge, delete that edge and test whether its endpoints remain connected. Parallel edges are handled individually. Iterate over direct-sum components and local predicates. The whole predicate therefore lies in `L/poly`, and the assumed compilation gives the claimed inclusion. ∎

The external ingredient is [Reingold, Undirected Connectivity in Log-Space](https://doi.org/10.1145/1391289.1391291). An author-hosted version is [available here](https://www.cs.princeton.edu/courses/archive/fall09/cos528/reingold.pdf).

This is a conditional barrier, not an impossibility theorem: the inclusion `P/poly subseteq L/poly` is open. Again, SAT-only or many-instance reductions might evade it. Allowing auxiliary variables avoids the predicate barrier but returns the exponent problem: there may be `Theta(s)` auxiliary bits for a circuit with `s` gates.

## 4. A simpler, linear-size bridge to arbitrary branching programs

The following direct construction needs neither reversible simulations nor permutation-program normalizations. Its proof is elementary and preserves both the independent inputs and the branching program's linear description size.

### Lemma 6: deterministic branching programs are graphic full-span predicates

Let `B` be an acyclic deterministic branching program with `p` input bits, `S` vertices, designated start `s`, and two distinct sinks `a` (accept) and `r` (reject). Every internal vertex queries an input bit and has one zero transition and one one transition. There is a connected undirected multigraph `G_B` with `S` vertices and at most `2S-2` edge identities, each activated by a single original literal or a constant, such that for **every** input `x`,

`B(x)=1 iff rank_M(G_B)(Y(x))=rank_M(G_B)(E)`.

No new input bits and no local constraints are introduced. The construction takes linear time apart from writing vertex/input indices.

**Proof.** Replace each directed zero/one transition by an undirected edge with the same identity, activated by the corresponding literal. For each fixed `x`, exactly one outgoing transition from each internal vertex is selected. Since the program is acyclic, following selected outgoing edges always terminates at `a` or `r`. Its selected undirected graph `F_x` is a forest: an undirected cycle would have exactly as many edges as vertices, and each of its vertices has at most one outgoing selected edge, forcing a directed cycle. Each component contains exactly one sink, so there are exactly two components and `S-2` selected edges.

Add one always-selected edge `e={s,r}`. If `B(x)=1`, `s` belongs to the component rooted at `a`, so `e` joins the two components and `F_x+e` is a spanning tree. If `B(x)=0`, its endpoints are in the same component, so the component rooted at `a` remains separate. Finally add a never-selected edge `{a,r}`. This makes the ground graph connected, hence its rank is `S-1`, without changing the selected graph. The two rank values are `S-1` on acceptance and `S-2` on rejection. There are `2(S-2)+2=2S-2` ground edge identities. Parallel edges and loops are allowed; in particular this handles `s=r` or a transition already joining `s` and `r`. The constant case `s=a` is handled too. ∎

The number `S` measures vertices, whereas the binary input description has `O(S log(S+p))` bits. These logarithmic encoding factors stay outside the exponential dependence on `p`.

### Corollary 7: the same construction works cographically

Use the same ground graph as in Lemma 6, but activate the **complement** of `F_x+e` in the ground edge identities. This just negates every literal/constant activation. Cographic full-span holds exactly when `F_x+e` is a forest. It has exactly `S-1` edges, so this is equivalent to its being a spanning tree, which by Lemma 6 is equivalent to `B(x)=1`. Thus the representation holds separately for graphic and cographic matroids.

### Theorem 8: exact predicate expressiveness

Polynomial-size explicit literal-controlled graphic full-span families have exactly the predicate expressiveness of `L/poly`. The same is true of cographic full-span and of either model augmented by polynomially many constant-arity local predicates.

**Proof.** Polynomial-size deterministic branching programs are the standard nonuniform model of logarithmic workspace. Lemma 6 gives one inclusion, and Corollary 7 gives its cographic counterpart. The opposite inclusion is the logarithmic-space verification argument in Lemma 5. For the augmented case, iterate over the constant-arity local predicates using logarithmic counters. ∎

This is a structural characterization, and it honestly identifies the problem as an alternative graphical presentation of branching-program satisfiability at the two-parameter level. It does not establish arbitrary-circuit expressiveness.

### Lemma 9: a regular exponential tableau has a logspace local-index verifier

Fix a nondeterministic multitape machine running in time `2^n`. For each input `x` of length `n`, one can define a 3-CNF `Phi_x` with `2^{O(n)}` variables and clauses such that:

- `Phi_x` is satisfiable iff the machine accepts `x`;
- a clause is indexed by `q=O(n)` bits;
- each bit of the three signed variable indices of that clause is computable using `O(log n)` workspace, with the clause index and `x` read-only;
- the local-index computation takes `poly(n)` time and can be expanded explicitly into a `poly(n)`-size branching program.

**Proof.** Convert the fixed machine to a single-tape machine with `2^{O(n)}` time and space. Pad time and tape bounds to powers of two, and arrange that acceptance is copied to a specified cell by the final time. The usual tableau has exponentially many rows and columns, each cell holding a constant-alphabet symbol that includes the head/state information when appropriate. Variables are indexed by a row index, a column index, a constant-size symbol-bit tag, and a constant-size auxiliary tag. Each transition checks a fixed finite relation among a constant number of adjacent cells in two consecutive rows. Write this relation as a constant-size CNF and convert it to 3-CNF with a constant number of auxiliary variables per cell. Add the prescribed initial row, boundary clauses, and final acceptance condition. The number of variables and clauses is `2^{O(n)}`.

A clause index consists of a clause-family tag, row/column indices, and a constant-size within-gadget clause tag. The three output variable indices are obtained by copying index bits, adding or subtracting a fixed constant to the row/column, testing boundary conditions, and choosing a constant-size local template. To compute one output bit of addition, scan lower input bits to recover its carry, with an `O(log n)`-bit scan counter; comparison and copying need the same workspace. Initial-row clauses fetch `x_j` only for `j<n`, otherwise use a blank symbol; testing this and reading that input position also use `O(log n)` workspace. Unused binary clause indices output a fixed tautological clause. All loops scan at most polynomially many index bits. This proves the workspace and time bounds. Expanding configurations of this fixed polynomial-time logspace computation gives a polynomial-size branching program, effectively and uniformly in `n` and the hardwired `x`. ∎

This uses a deliberately regular, possibly larger tableau. Constant-factor blow-up in `q=O(n)` is harmless for a genuinely subexponential algorithm; tight `n+O(log n)` clause indexing is unnecessary here.

### Theorem 10: a direct and representation-safe lower-bound transfer

If literal-controlled graphic full-span has a deterministic algorithm taking

`2^{o(p)} poly(S)`

on `p` switches and `S` graph objects, including arbitrary polynomial relations `S=p^{O(1)}`, then

`NEXP is not contained in L/poly`.

The same conclusion holds for the cographic-only model. This theorem does not assert `NEXP` versus `P/poly`.

**Proof.** Lemma 6 (or Corollary 7) turns the assumed algorithm into a satisfiability algorithm for `p`-input polynomial-size branching programs taking `2^{o(p)} poly(S)` time. We give the transfer explicitly rather than identify branching-program syntax with a circuit syntax in a metatheorem.

Assume for contradiction that `NEXP subseteq L/poly`. In particular `NEXP subseteq P/poly`. The universal easy-witness theorem of Impagliazzo-Kabanets-Wigderson/Williams, stated in Williams's ACC paper Theorem 5.2, implies that for every fixed exponential-time verifier and each accepted input `x`, some accepting exponential-length witness has a Boolean circuit of size `n^{O(1)}` encoding its indexed bits. Apply this to the verifier that checks a satisfying assignment for the tableau formula `Phi_x` of Lemma 9.

These witness circuits can existentially be replaced by polynomial-size branching programs: the hypothesis also implies `P subseteq L/poly`, and universal Circuit Evaluation is in `P`. Take a polynomial-size branching program for Circuit Evaluation and hardwire the particular witness-circuit description. The result is a polynomial-size branching program `W` that returns its witness bit on its `O(n)`-bit index. The polynomial bound is fixed for this machine/verifier; no effective circuit-to-BP compiler is assumed.

Now simulate a language in `NTIME[2^n]` as follows. Nondeterministically guess an acyclic witness branching program `W` of this fixed polynomial size, with `O(n)` input bits. Check its syntax. Uniformly construct a branching program `D_W` on the `q=O(n)` clause-index bits which outputs one precisely when the indexed clause of `Phi_x` is violated by the assignment encoded by `W`. Derive the three signed variable indices using Lemma 9, evaluate `W` on each implicit index, and test the three literal values. During a step of `W`, keep its current node number in `O(log n)` bits; recompute the requested index bit instead of storing the entire `O(n)`-bit query. The clause-index generator also uses `O(log n)` workspace. With `W` and `x` hardwired, this is an explicit polynomial-time logarithmic-space computation and can be expanded into an acyclic branching program of size `n^{O(1)}` in polynomial time.

Call the assumed BP-SAT algorithm on `D_W` and accept the guessed witness iff `D_W` is unsatisfiable. On a yes-instance, the compressed witness guaranteed above gives an accepting branch. On a no-instance, every `W` encodes an assignment and every assignment violates some clause of `Phi_x`; thus `D_W` is satisfiable and no branch accepts. The simulation takes `poly(n)+2^{o(q)}poly(n)=2^{o(n)}` time.

Consequently every language in `NTIME[2^n]` would have a nondeterministic `2^{o(n)}`-time algorithm, contradicting the nondeterministic time hierarchy. ∎

The only non-elementary lower-bound ingredient here is the universal easy-witness theorem; see [Williams, Non-Uniform ACC Circuit Lower Bounds](https://people.csail.mit.edu/rrw/acc-lbs.pdf), Theorems 5.1–5.2. No generic circuit-class closure claim, reversible simulation, oblivious-program conversion, or constructive consequence of a nonuniform inclusion is used in this proof.

The proof uses the strong `2^{o(p)}` premise. For a mere inverse-polynomial saving over `2^p`, the factor in `q=O(n)` would matter: use tighter Williams reductions rather than quote this proof unchanged.

## 5. A stronger obstruction to the desired natural-problem reductions

The following obstruction concerns satisfiability-preserving reductions, so it is stronger in that respect than the predicate-counting obstruction in Lemma 4. It is conditional on the standard assumption `NP not subseteq coNP/poly`.

### Lemma 11: arbitrary CNF-SAT embeds with unchanged input count

A CNF formula on `p` variables and `ell` literal occurrences has a deterministic acyclic branching program on the same `p` input bits with `ell+2` vertices. Consequently Lemma 6 gives a literal-controlled graphic full-span instance with `ell+2` vertices and at most `2ell+2` edge identities.

**Proof.** Scan clauses in order. At a vertex testing a literal, its false edge goes to the next literal of that clause, or to rejection if this is the last literal. Its true edge skips to the first literal of the next clause, or to acceptance after the last clause. Every transition goes forward in this order, except transitions directly to a sink. Empty clauses or an empty conjunction give the corresponding constant program. The program accepts exactly the satisfying assignments, not merely the same satisfiability bit. Apply Lemma 6. ∎

### Theorem 12: polynomially short targets face an instance-compression barrier

Suppose there is a deterministic polynomial-time many-one reduction from arbitrary literal-controlled graphic full-span instances with `p` switches to an ordinary decision language whose **entire output encoding** has at most `p^c` bits for some fixed constant `c`, preserving whether a solution exists. Then

`NP subseteq coNP/poly`.

This excludes, under the standard noncollapse assumption, any such reduction to an unweighted simple graph problem on `p^{O(1)}` vertices with a fixed polynomial vertex bound independent of the source description size. In particular it excludes an `O(p)`-vertex reduction to ordinary Hamiltonian Cycle or Feedback Vertex Set.

**Proof.** Lemma 11 followed by the supposed reduction would compress arbitrary CNF-SAT parameterized by its number `p` of variables into `p^c` bits. Fortnow-Santhanam, Corollary 3.2, says that such compression implies `coNP subseteq NP/poly`, equivalently `NP subseteq coNP/poly`. ∎

Primary source: [Fortnow-Santhanam, Infeasibility of Instance Compression and Succinct PCPs for NP](https://lance.fortnow.com/papers/files/compress.pdf), Theorem 3.1 and Corollary 3.2.

### Quantitative form covering polynomial-size source promises

There is a useful version even if the source domain is restricted to polynomial descriptions. Dell-van Melkebeek prove that a polynomial-time reduction from `d`-CNF-SAT on `p` variables cannot issue `O(p^b)` queries of `O(p^c)` bits to **any** target language when `b+c<d`, unless the same collapse holds.

Thus a source-to-Hamiltonian-Cycle or source-to-FVS reduction producing `O(p)`-vertex simple graphs would compress **3-CNF-SAT** into `O(p^2)` bits. Taking `b=0,c=2,d=3` contradicts their theorem. The source instances in this argument have only `O(p^3)` objects after duplicate 3-clauses are removed, so arbitrary exponential source descriptions are unnecessary. If an output graph has `O(p^a)` vertices for a fixed `a`, choose fixed `d>2a`; Lemma 11 still creates polynomial-size source instances, and their outputs have `O(p^{2a})` bits.

Primary source: [Dell-van Melkebeek, Satisfiability Allows No Nontrivial Sparsification Unless The Polynomial-Time Hierarchy Collapses](https://pages.cs.wisc.edu/~dieter/Papers/sparsification-stoc.pdf), Theorem 1 and Corollary 1.

### Scope and escape routes

For Set Cover, a universe of `O(p)` elements **and** at most `p^c` sets for a fixed constant `c` gives an incidence encoding of `p^{O(1)}` bits, so the same barrier applies. Merely bounding the number of sets polynomially in the **source description length** does not give a fixed polynomial in `p`: those sets might preserve the large description. No such automatic compression contradiction applies in that case. The same warning applies to weighted targets with long numeric encodings.

Neither theorem prohibits subexponential-time reductions or reductions making `2^{o(p)}` queries. These may still transfer subexponential hardness if all output parameters and preprocessing costs are controlled. Polynomial-time reductions with a bounded polynomial number of sufficiently short queries face Dell-van Melkebeek's quantitative bound; arbitrary polynomial Turing compressions require separate care. Also, neither obstruction prohibits a reduction to general CNF-SAT with `O(p)` variables but potentially very many clauses.

This changes the research priority: polynomial-time compilation from the entire two-parameter source into `O(p)`-vertex ordinary graph problems is conditionally ruled out, not merely unproved. Any proposed broad truth-side theorem must evade the compression barrier explicitly.

## 6. The strongest honest formulation at this checkpoint

A particularly transparent restricted hypothesis with a rigorously established circuit consequence is:

> `H_5`: There is no deterministic algorithm deciding satisfiability of literal-controlled cyclic width-five permutation switching graphs in `2^{o(n)} poly(L)` time, where `n` is the number of switches and arbitrary polynomial lengths `L=n^{O(1)}` are allowed.

Then `not H_5 => NEXP not subseteq NC1` by Theorem 3. This has genuine graphic rank computation and no arbitrary Boolean verifier hidden in its input format. However, `H_5` currently supplies only a common hardness hypothesis for this model and polynomial-size logarithmic-depth circuit/formula SAT; it does not yield the user's desired simultaneous natural-problem lower bounds. Declaring that full win-win proved would be wrong.

The stronger general candidate is:

> `H_L`: There is no deterministic `2^{o(n)} poly(v+m)` algorithm for satisfiability of explicit literal-controlled graphic full-span instances, where `n` is the number of independent switches and polynomial-size graph descriptions are allowed.

By Theorem 10, `not H_L => NEXP not subseteq L/poly`. The forward reduction theory to ordinary natural problems remains missing. In particular, a separate lower bound for Hamiltonian Cycle does not follow from its encoding into the source.

A sparse-total-size hypothesis for SCGS has the opposite strength profile: it can organize natural encodings with `N=Theta(n)` on bounded-degree graph families, but the falsity-side connection to arbitrary polynomial-size circuit satisfiability is absent. The branching-program construction makes this two-parameter tension explicit rather than resolving it.

## 7. Next mathematical steps

1. Investigate subexponential-time or many-instance reductions that evade Theorem 12, or restrict the source family enough to avoid its embedded dense fixed-width SAT instances. Polynomial-time many-one compilation from the whole source to an `O(p)`-vertex ordinary graph target contradicts known compression lower bounds under `NP not subseteq coNP/poly`.
2. Identify which larger structural verification classes can be represented by literal-controlled graphic or binary-matroid span while preserving input bits. Any proposed arbitrary-circuit compilation should be audited against Lemma 5 before investing in gadgets.
3. A hypothesis with both a sparse-natural problem branch and a polynomial-description switching branch needs a genuine equivalence/reduction linking the branches. A conjunction of two hardness assumptions does not obtain the desired win-win: its falsity may witness the easy branch that supplies no circuit consequence.
