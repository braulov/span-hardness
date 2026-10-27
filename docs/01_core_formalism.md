# Core formalism and exact lemmas

## Sparse Graphic Rank-CSP (SGR-CSP)
Let G=(V,E) be a multigraph with |V|+|E|=O(n), O(n) Boolean variables z including activation bits y_e, and a width-three CNF phi(z) with O(n) clauses. The threshold t(z)=c+sum_i a_i z_i is affine with bounded coefficients and O(n) terms. Decide whether there exists z with phi(z)=1 and rank over F_2 of the incidence columns indexed by Y={e:y_e=1} at least t(z).

The fine-grained parameter counts *all* base vertices, edges, Boolean variables and clauses. A reduction with a quadratic incidence blow-up is NOT linear-parameter-preserving.

## Exact rank identities
1. rank(B_Y)=|V|-cc(V,Y). Every spanning tree contributes a basis for the even-parity subspace of a component.
2. Y is a forest iff rank(B_Y)=|Y|, equivalently rank(B_Y)>=|Y|.
3. The spanning subgraph (V,Y) is connected iff rank(B_Y)=|V|-1.
4. If Y contains *all* induced edges of G[S] for S nonempty, then rank(B_Y)=|S|-cc(G[S]); thus G[S] connected iff rank(B_Y)>=|S|-1.

## Conjunction by disjoint union
If r_1<=u_1(z) and r_2<=u_2(z) hold unconditionally for two disjoint graphic rank systems, then r_1+r_2>=u_1+u_2 iff both are saturated. This combines extreme-rank constraints, but it cannot combine arbitrary lower bounds.

## Cardinality constraints
An unweighted population count and comparison can be realized in O(n) constant-fan-in Boolean gates with carry-save compression and a final small-width adder. Tseitin conversion introduces O(n) variables/clauses. Do not equate O(n) word-RAM operations with O(n) Boolean gates; weighted bit lengths matter.

Loops are excluded. Parallel edges are allowed and produce duplicate incidence columns. This distinction is important for coverage encodings.