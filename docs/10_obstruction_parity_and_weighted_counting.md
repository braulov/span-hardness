# Branch E: nullspace witnesses, parity, weighted #SAT

Status: exact algebraic parity identity PROVED. The finite-field weighted-model-counting extension is OPEN.

## Rank nonspanning certificates
Represent a binary matroid by full-row-rank A of rank r. For activated column set Y(x), define K(x)=#{w in GF(2)^r: A_Y^T w=0}=2^{r-rank(A_Y)}. The set spans iff K(x)=1. Nonzero deficiency witnesses number K(x)-1.

## Graphic = consistent cuts
Use a reduced incidence matrix with one anchored vertex per base connected component. A kernel witness labels vertices by bits such that activated edges join equal labels. The witness space has 2^{cc(V,Y)-cc(G)} elements. It has odd cardinality iff activated edges span the graphic matroid. An O(n) sparse local formula represents the pair (x,w).

## Cographic = Eulerian subgraphs
For retained induced edges Y and activated complement E\Y in M*(G), dual witnesses are binary even-degree edge subsets z supported entirely inside Y. Impose z_e => e in Y, and XOR incident z_e=0 at every vertex. There are 2^{|Y|-rank(B_Y)} such z. Odd cardinality iff Y is a forest. A sparse graph yields O(n) total XOR gates.

## Star = uncovered elements
For each universe element u introduce witness bit z_u, and for every set incidence impose NOT x_i OR NOT z_u. For any choice of sets, uncovered elements have free witness bits, covered elements have z_u=0. Thus there are 2^{#uncovered} witness choices; the parity is one iff coverage is full.

## The parity identity
For ANY binary matroid full-row-rank representation A and local predicate phi(x),

sum_{x:phi(x)} #{w:A_{Y(x)}^T w=0} mod 2
= #{x:phi(x) and rank(A_Y)=rank(A)} mod 2.

Each summand is a power of two: it vanishes mod 2 unless the rank deficiency is zero. This is elementary and exact. In sparse (co)graphic cases it reduces to the parity of the number of satisfying assignments of an O(n)-size 3-CNF (using deterministic Tseitin auxiliaries). Conditional on correct exact #3-SAT, the *parity* of eligible full-span assignments admits 2^{o(n)} time.

CRUCIAL: PARITY IS NOT DECISION. A positive even number of solutions looks zero.

## Proposed weighted-field route (conditional)
Weight each genuine existential bit x_i with an independent indeterminate a_i in F_{2^b}. Let

P(a)=sum_{feasible x} product_{i:x_i=1} a_i.

Distinct assignments give distinct monomials; P is nonzero iff a feasible assignment exists. Its total degree <=p. The nullspace parity identity extends to characteristic two:

P(a)=sum_{x,w:phi(x), A_Y^T w=0} product_{i:x_i=1} a_i.

With an algorithm for arbitrary-field weighted #3-SAT at 2^{o(n)} poly(log q) cost, evaluate at random a_i in a field q>2p. Schwartz-Zippel gives error at most p/q<1/2; repeating gives randomized 2^{o(n)} decision for all sparse (co)graphic span problems.

NO SUCH GENERAL WEIGHTED #SAT EXTENSION IS ESTABLISHED by the unweighted OpenAI statement. Encoding weights by extra Boolean bits naively costs Omega(n log n) auxiliary variables and can defeat the desired subexponential transfer. Characteristic 2 may break algebraic identities/interpolation used by a counting algorithm.

## Next work
Audit actual #SAT proof for field-semiring generality. Seek sparse isolation/hashing with fewer than n sqrt(log n)/(log log n)^2 added gates. Keep rooted solutions distinct or canonicalize roots when counting connected structures. Compare existing XOR-SAT and isolation literature before any novelty claim.