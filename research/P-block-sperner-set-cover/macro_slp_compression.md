# P2 — An independent compression route: finite-transformation macros

2026-10-28. Supplements block-local Set Cover compilation from block_compilation.md. **No novelty claim:** evaluation of straight-line programs over finite transformation monoids is standard. The useful observation for this project is that macro compression is orthogonal to block-variable incidence H and yields actual O(p)-universe Set Cover reductions for some p^2-length branching programs where naive block decomposition has H=Theta(p^2).

## 1. Straight-line programs over width-w transition layers

For a width-w deterministic layered branching program, a transition layer j, after fixing Boolean input x, induces a total function F_j(x):[w]->[w]. This is still true when different states query different input bits; a single layer needs at most w input-bit references.

Let a straight-line program (SLP) of size g encode the sequence of layers. Nodes are either:
- Terminal T: a specified transition layer (with its state-dependent queries).
- Concatenation A:=BC: the layer sequence for B followed by that for C.

An SLP can share subexpressions; its expanded sequence may have length L much larger than g. Assume the grammar and terminals are supplied, or are recovered by an explicit polynomial-time compression algorithm for the promised source subclass.

**Theorem P2.** For constant width w, the acceptance predicate of an SLP-described BP has a constructible Boolean circuit of size O_w(g+p), without an extra variable for each of the L expanded transitions. Consequently a standard unique-extension Tseitin CNF and standard CNF-to-SetCover gadget produce a Set Cover instance with

    universe u=O_w(p+g),
    candidate sets t=O_w(p+g),
    budget k=O_w(p+g).

Proof: at each grammar node A, represent the complete transformation F_A(x):[w]->[w] by w output indices of ceiling(log2 w) bits. For a terminal the w next-state values are constant-size selector circuits on the queried x_i. For concatenation A:=BC compute F_A=F_C∘F_B by w lookups in the constant-size table F_C; at fixed w, each lookup has O_w(1) bounded-fanin gates. Sharing the node outputs gives O_w(g) total gates, in addition to the p designated input wires. A final O_w(1)-gate test checks whether F_root(x)(start) is an accepting state. Parsimonious Tseitin adds O_w(p+g) variables and clauses. The standard SAT-to-SetCover conversion adds one choice group per variable (two sets), one private universe element per group, and one universe element per clause; budget equals the number of Boolean variables. All sizes are O_w(p+g). QED.

This reduction works for arbitrary **SLP-compressible** polynomial-length width-w branching programs; it does NOT show that an arbitrary explicit BP admits g=O(p). In fact random instruction strings will not generally have short SLP descriptions.

## 2. A very high-H example that nevertheless has O(p) universe

Let W(x) be a width-five transition word of p layers reading x_1,...,x_p in sequence. Consider

    P(x)=W(x)^p,

i.e., repeat the entire p-layer sequence p times. The expanded program has L=p^2 layers, and each original input appears p times. A block partition into chunks of <=O(log p) distinct inputs must have H=Omega(p^2) because every chunk of <=O(log p) consecutive layers in this particular sequence reads distinct bits, apart from p wrap boundaries.

Nevertheless an SLP represents W with O(p) concatenation/terminal nodes and W^p with only O(log p) additional doubling/concatenation nodes. By Theorem P2 its predicate reduces to Set Cover universe O(p), candidate sets O(p) and budget O(p), entirely independently of H.

A stronger, explicit finite-transformation fact gives a **syntactic reduction** even without a DAG circuit. Every function F:[w]->[w] satisfies

    F^{w+lcm(1,...,w)}=F^w,

because each point enters a directed cycle of length <=w within at most w steps. Consequently for k>=w one can replace W^k pointwise (simultaneously for all x) by W^{w+((k-w) mod lcm(1,...,w))}. For w=5 the reduced exponent is <=64. For permutation-only width-five programs, F belongs to S_5, whose element orders divide 60, so k mod 60 copies suffice, even zero copies (identity).

For W of length p, the shortened explicit program has O(p) layers, hence an O(p)-variable Tseitin CNF and O(p)-universe Set Cover. The more general SLP approach works without explicit shortening and for arbitrary nested repeated macros.

The algebra of finite transformation monoids, rather than the number of distinct read variables per temporal block, is the useful compression resource.

## 3. Two axes for extending the reduction

We now have TWO different sufficient mechanisms for polynomial-size BPs to reduce to small-universe Set Cover:

1. **Locality**: B+H=O(p), max_j d_j=O(log p), w=O(1), from block_compilation.md.
2. **Algebraic sharing**: grammar/SLP size g=O(p), w=O(1), from Theorem P2.

The classes are incomparable at the syntax level. A program may be irregular but block-local, with no small grammar for its raw transition word; or it may have very dense cross-block reuse (large H) but a tiny SLP.

A prospective hybrid should partition the program into B macros whose transition maps can be computed by circuits of total size G, rather than enumerate all local assignments. This creates O_w(G+B) verifier gates and trivially yields Set Cover universe O(p+G+B). The difficult case is a generic polynomial-length BP with no short symbolic macro representation: in general G may be Omega(S).

The key global post-ETH goal — **all** polynomial-size BP/LGS with O(p) Set Cover universe and polynomially many sets — remains open. The p^2 repeat example only establishes that H-based lower bounds do not apply to every possible reduction.

## 4. Checks, limits, and literature

A Python test constructed SLP DAGs for W^k by binary doubling, evaluated their node transformations bottom-up on three random input assignments, and compared to explicit simulation for 700 random programs with p<=7, w<=5, word length <=12, and repetitions k<=25. All passed.

Standard background on compressed words/finite monoids: Lohrey, *Word Problems and Membership Problems on Compressed Words* (SIAM J. Comput., 2006), https://doi.org/10.1137/S0097539704445950 ; general discussion of power/SLP words https://doi.org/10.1007/s00224-024-10173-z .

**No hardness/circuit separation is proved**. This is a normal parameter-preserving reduction for two explicitly promised structural BP families, and standard monoid compression. No general input-efficient method for arbitrary polynomial-size branching programs is obtained.
