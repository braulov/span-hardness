# Branch C: rank, Set Cover and General CNF-SAT

## Star-rank identity
Build a star with center c and one leaf for every universe element u in U. The spoke incidence columns b_u=e_c+e_u are linearly independent over F_2. Parallel occurrences of one spoke give equal columns. For activated occurrences Y,

rank(B_Y)=number of distinct leaves touched by Y.

## Set Cover
For every selected family member S_i, activate a parallel copy of spoke (c,u) for every incidence u in S_i, controlled by bit x_i. Then

rank(B_Y)=|union_{i:x_i=1} S_i|.

Thus Set Cover is exactly feasible iff there exist x with sum_i x_i<=k and rank(B_Y)=|U|.

COST: m selection bits, |U|+1 vertices, and sum_i |S_i| edge occurrences. This is NOT linear in the universe parameter n=|U| for general instances. Using one spoke per element with an OR activation circuit still incurs incidence complexity.

## General CNF-SAT
For clauses C_1,...,C_m, create one leaf per clause, and activate its spoke iff that clause is satisfied. The rank equals the number of satisfied clauses. Requiring rank=m is exact CNF satisfiability.

COST: at least m leaves plus an activation computation for clauses. Long clauses and many clauses can make the encoding far larger than the number of SAT variables.

## Mathematical subtlety
The coverage function on SET INDICES is generally not a matroid rank function (a singleton may cover more than one item). The correct construction is a group-activation *lift* to an ordinary graphic matroid on incidence occurrences.

## Open questions
Can group activations be compressed with genuine parameter preservation? Does the answer change for dense Set Cover, arbitrary-width CNF or restricted incidence patterns? Do not claim these are subexponential consequences without an explicit size audit.