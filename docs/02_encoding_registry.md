# Exact reductions, with parameter audit

All listed reductions are deterministic. Their parameter cost is O(|V|+|E|), and hence O(n) only for sparse input classes; for Hamiltonicity, bounded degree makes local degree constraints constant size.

| Source task | Activation | Local constraints | Graphic rank bound |
|---|---|---|---|
| Undirected FVS | y_uv=x_u AND x_v for retained vertices | retain >= n-k vertices | rank(Y)>=|Y| |
| Hamiltonian Cycle | chosen edges y_e | each vertex degree exactly 2 | rank(Y)>=n-1 |
| Directed HC | chosen arcs, incidence on underlying undirected multigraph | indegree=outdegree=1 | rank(Y)>=n-1 |
| Hamiltonian Path | chosen edges | exactly two degree-1 endpoints and other vertices degree 2 | rank(Y)>=n-1 |
| Connected Dominating Set | induced edges on chosen S | S nonempty, |S|<=k, domination | rank(Y)>=|S|-1 |
| Connected Vertex Cover | induced edges on S | S nonempty, |S|<=k, every edge covered | rank(Y)>=|S|-1 |
| Node Steiner connectivity | induced edges on S | terminals included, |S|<=k | rank(Y)>=|S|-1 |
| Connected FVS | direct sum: retained induced edges + deleted induced edges | deletion nonempty, <=k | sum rank >= |E(retained)|+|deleted|-1 |

## Proof details
In undirected HC, 2-regularity forces a disjoint union of cycles. Full incidence rank forces the union to be connected, hence one Hamiltonian cycle. The directed version uses indegree and outdegree exactly one.

In FVS, retaining S leaves the induced subgraph G[S]. The selected edge columns are independent iff G[S] is a forest.

For Connected Dominating Set, Connected Vertex Cover and node Steiner, the local conditions enforce the non-connectivity demands, and the rank threshold forces induced connectivity.

For Connected FVS, the graphic rank of retained induced edges is bounded by the number of those edges, whereas the rank of deleted induced edges is bounded by |D|-1 for D nonempty. Summing both ranks and requiring saturation enforces simultaneously acyclicity of retained vertices and connectedness of deleted vertices.

## Do not infer
An encoding P -> rank-CSP transfers a generic algorithm *to* P. It does not transfer a hardness conjecture about rank-CSP *to* P. The latter needs reductions in the reverse direction. Dense graph HC is not covered by bounded-degree parameter claims. All results here are exact representations, not new subexponential algorithms.