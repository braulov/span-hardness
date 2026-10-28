# V — Deterministic Fourier-sparse BP-SAT and unknown XOR-junta recovery

Checkpoint 2026-10-28. **Status:** unconditional elementary pseudorandom-hitting/rounding theorems for two **promised** semantic classes of arbitrary deterministic branching programs. Does NOT solve unrestricted polynomial-size LGS / BP-SAT or NEXP vs L/poly; no novelty claim. Main ingredients (small-bias sets, finite-field trace, Fourier uncertainty, exact learning) are classical. This checkpoint precisely combines them with p-bit input-preserving Set Cover reductions. Based on branch U.

## 1. An explicit deterministic epsilon-biased family from finite fields

Let p>=1 and choose q=2^m > (p-1)/eps, q>=2. Construct GF(q) deterministically in poly(m) time over characteristic 2 (Shoup 1990). For every (a,b) in GF(q)^2 let

    D_{a,b} ∈ F2^p,   D_{a,b}[i] = Tr_GF(q)/F2 (a b^i), i=0,...,p-1.

The multiset D has exactly q^2 members (duplicates permitted).

**Lemma V1.** For every nonzero c∈F2^p,

    |E_{a,b} (-1)^{c·D_{a,b}}| <= (p-1)/q < eps.

Proof: let P_c(t)=Σ_{i=0}^{p-1} c_i t^i ∈GF(q)[t]. It is a NONZERO polynomial (including the constant-polynomial case). By linearity of the trace, c·D = Tr(a P_c(b)). For each fixed b with P_c(b)≠0, uniform a makes this trace uniform over F2, hence conditional expectation zero. For a root P_c(b)=0 the conditional expectation is one. A nonzero degree≤p−1 polynomial has at most p−1 roots. Therefore the total bias equals #roots(P_c)/q∈[0,(p−1)/q]. QED.

Construction and enumeration cost poly(p,q); q can be chosen as the next power of two above (p−1)/eps, so |D|=O(p²/eps²), with a harmless adjustment p=1. This is a standard small-bias construction (cf. Alon–Goldreich–Håstad–Peralta, Theorem 6 in Chillara–Limaye–Srinivasan ICALP 2018).

Useful corollary: D intersects EVERY nonempty affine subspace of F2^p of codimension ≤k provided eps<2^-k, since for V={x:Ax=t} with rank r≤k, Fourier expansion of 1_V gives E_D 1_V>=2^-r−(1−2^-r)eps>0.

## 2. Fourier-sparse Boolean functions: deterministic SAT in poly(s,p,S)

For f:{0,1}^p→{0,1}, write its Walsh–Fourier expansion

    f(x)=Σ_{α∈F2^p} fhat(α) (-1)^{α·x},
    fhat(α)=2^-p Σ_x f(x)(-1)^{α·x}.

Let s be any supplied upper bound on the number of NONZERO coefficients \hat f(α) (Fourier sparsity); s≥1. No support locations/coefficient values are supplied.

**Theorem V2 (black-box hitting).** Given a deterministic BP of description size S whose predicate has Fourier sparsity ≤s, SAT and a satisfying input are computed deterministically using O(p²s²) evaluations of the original BP; hence time poly(p,S,s). No structural promise certificate or Fourier-support oracle is needed for this *promise algorithm*.

Proof: let μ=E f. If f is not identically zero, μ>0. Parseval gives μ=Σ_α fhat(α)^2 (since f²=f). Furthermore |fhat(α)|≤μ, whence μ≤s μ², or μ≥1/s: the Fourier uncertainty lower bound on support density.

Cauchy–Schwarz gives Σ_α|fhat(α)|≤√(s μ). On an eps-biased D, |E_D f−μ|≤eps√(s μ). Set eps=1/(4s). Since μ≥1/s, √(s μ)≤s μ. Thus E_D f≥(3/4) μ>0. Because f is Boolean, some d∈D satisfies f(d)=1. If f≡0, none does. Use V1's q=O(ps), |D|=O(p²s²). QED.

**Optimality at least up to the exponential scale for linear juntas:** even if a rank-k matrix A is KNOWN, a promise g:F2^k→{0,1} might be the indicator of one UNKNOWN element t∈F2^k or identically zero. Any deterministic evaluation-query decision algorithm may need all 2^k queries to distinguish the zero function from all such point indicators. This lower bound is on black-box evaluation, NOT algorithms that inspect BP syntax.

Fourier sparsity may be much smaller than 2^k and hence permit easy SAT even if the Fourier support spans a large vector subspace. The theorem does not provide exact #SAT for arbitrary Fourier-sparse Boolean f in the same stated time.

## 3. Unknown rank-k linear junta: exact #SAT by rational rounding

Assume (as a PROMISE) that there exist an unknown binary matrix A of rank r≤k and an unknown arbitrary Boolean g such that

    f(x)=g(Ax),  A∈F2^{r×p}.

The predicate may be non-symmetric under EVERY coordinate permutation and have high harmonic degree on Hamming-weight slices (e.g. parity on an arbitrary proper subset of coordinates). Its Fourier support lies in rowspace(A), so has at most 2^k elements. Its acceptance density is an exact multiple of 2^-r, hence also of 2^-k.

**Theorem V3 (nonadaptive exact counting).** With the V1 small-bias multiset for

    eps = 2^{-(3k/2+2)},

evaluate f at all |D|=O(p² 2^{3k}) points, compute μ_D=(# accepting queries)/|D| as an exact rational, and round 2^k μ_D to its nearest integer m. Then

    #f^{-1}(1) = m * 2^{p-k}

exactly, for every f satisfying the promise. The algorithm is fully deterministic and evaluates the original BP only on an input-independent multiset.

Proof: Parseval yields Σ|fhat|≤√(2^k) (since E f≤1). Thus |μ_D−μ|≤eps·2^{k/2}=2^{-k-2}. Since μ belongs to 2^-k Z and consecutive grid points are 2^-k apart, rounding to nearest grid point is uniquely correct. Multiplying by 2^p returns the exact integer count. QED.

For k=0 this specializes to a function constant over the cube. Sampling complexity as stated is polynomial in 2^k, independent of how often each input bit is reread.

## 4. Recover the unknown linear quotient by period queries

Let

    P_f = {v∈F2^p : f(x+v)=f(x) for ALL x∈F2^p}.

This is a linear subspace: the period space of f. Since f=g(Ax), ker(A)⊆P_f, hence its codimension r'=p−dim(P_f)≤k. The true minimum number of relevant XOR forms is exactly r' (a canonical *dimension*, even if the particular basis is nonunique).

For a test vector v, set h_v(x)=f(x) XOR f(x+v). Under the promise, h_v is itself a Boolean function of Ax, so if h_v is nonzero its support contains an entire nonempty affine coset of ker(A), of codimension≤k.

Take V1's explicit multiset D with eps<2^-k (e.g. eps=2^{-(k+2)}). By its affine-coset hitting property,

    v∈P_f  iff  f(d)=f(d+v) for EVERY d∈D.

This is an EXACT period-membership test **under the original rank-k promise**, using O(p²4^k) BP evaluations, and no knowledge of A.

**Theorem V4 (deterministic exact learning/compilation).** With the rank-k promise, we can produce an explicitly specified r'×p matrix B of rank r'≤k and an exact truth table h:{0,1}^{r'}→{0,1} such that f(x)=h(Bx) **pointwise**, in

    2^{O(k)} poly(p,S)

time. One implementation uses O(p 2^k) period-membership tests on the fixed small-bias D.

Algorithm: scan standard basis vectors e_1,...,e_p. Maintain indices j_1,...,j_r of standard basis vectors whose cosets form a basis of the quotient F2^p/P_f. To process e_i, enumerate all 2^r vectors e_i+Σ_t c_t e_{j_t} and ask the period oracle which belongs to P_f. If one belongs, record the quotient coordinates c_i=(c_t) of e_i; if none, append e_i to the quotient basis and set c_i to the new unit vector. At the end r≤k. The recorded coordinate columns c_i form an r×p matrix B. Then

    x+Σ_t (Bx)_t e_{j_t} ∈P_f

for every x, so h(z):=f(Σ_t z_t e_{j_t}) yields f(x)=h(Bx) exactly. Evaluate h on 2^r inputs. Exact #SAT is then

    2^{p-r} * |h^{-1}(1)|.

A Boolean circuit computing the r XOR forms plus the h lookup has O(pr + r2^r) bounded-fanin gates. Standard Tseitin→SetCover therefore yields a **pointwise equivalent** ordinary Set Cover instance with

    universe u=O(pk+k2^k), sets t=O(pk+k2^k), budget O(pk+k2^k).

In particular, for every FIXED k, even without knowing A, there is a deterministic polynomial-time reduction from this promised rank-k BP class to Set Cover with universe O(p). For k=o(p), SAT and exact #SAT are deterministic 2^{o(p)}poly(S); small-universe O(p) is only assured for k=O(1).

The quotient discovery is deterministic membership-query learning under a strong promise, and classical Fourier sparse/linear-function learning techniques exist; **do not claim priority or publication novelty**.

## 5. Barriers / precise relation to branch U and original ETH replacement

- Branch U's unknown-b-exception symmetry has an exact slice-interpolation algorithm costing 2^{O(b log(p/b))} poly(S), exploiting permutation action. V instead targets the unknown F2-linear quotient and costs 2^{O(k)}poly(S). It immediately handles parity over an arbitrary subset of the p inputs, which may have large degree on fixed-weight slices and thus be bad for U's low-slice-degree promise.
- V2 is even broader for SAT: any Boolean function with s-sparse Fourier transform is decided in poly(p,S,s). But V3/V4 need small **Fourier span rank** k for exact counts and quotient discovery; sparse Fourier support and low Fourier span rank are distinct promises.
- All algorithms are promise algorithms. Testing semantic constancy (k=0) for unrestricted width-five polynomial-length group programs is coNP-hard: use Barrington to represent z AND F(x), which is constant iff F is unsatisfiable. Therefore finite testing on D **does not certify** the promise on arbitrary BP inputs; a high-rank point indicator supported outside D can fool it.
- These algorithms do NOT yield any general 2^{o(p)} algorithm for arbitrary polynomial-size BP or LGS; no general SetCover(u=O(p)) reduction, no new ETH replacement, no NEXP outside L/poly theorem. At best, they isolate a class where an epsilon-biased universal hitting set gives a genuine deterministic shortcut without learning any structural parameters first.

## 6. Reproducible verification and prior art

Script \`verify_linear_junta.py\` implements arithmetic in GF(2^m), checks the finite-field trace generator's Fourier bias, compares exact rational counting against 2^p full enumeration, and recovers the unknown quotient B and h. It passed seeded random tests at p=4,5,6 and rank upper bounds k=1,2, with all assignments checked, including some cases where the conservative rounding guarantee holds. The script's small-case field constructor uses trial search for irreducible binary polynomials; this is adequate for tests but is not the general polynomial-time field construction used in the theorem.

Relevant literature:
- Alon–Goldreich–Håstad–Peralta, explicit small-bias sets (cited through Chillara–Limaye–Srinivasan, ICALP 2018, https://doi.org/10.4230/LIPIcs.ICALP.2018.36).
- Shoup, deterministic construction of irreducible polynomials over characteristic-two fields, *Mathematics of Computation* 54 (1990), https://doi.org/10.1090/S0025-5718-1990-0993933-0 .
- Kushilevitz–Mansour, *Learning Decision Trees Using the Fourier Spectrum*, SIAM J. Comput. 1993, https://doi.org/10.1137/0222080 .
- De–Mossel–Neeman, *Is Your Function Low Dimensional?*, COLT 2019, https://proceedings.mlr.press/v99/de19a.html — studies (a different, real-domain) notion of linear k-junta and testing; do not equate its precise model with F2 linear juntas.
- Older project: U chain-interpolation, T semantic orbits, S profile groups.


## 7. Hardness of recognizing low XOR dimension, even when k is fixed

A natural objection to the promise algorithm: can we verify that the learned quotient is actually correct on every input of an arbitrary BP? In general this is already coNP-complete.

**Theorem V5.** For EVERY FIXED k≥0, given a polynomial-length width-five A5 permutation branching program specifying f:{0,1}^p→{0,1}, deciding whether the minimum number of F2-linear forms on which f depends is at most k is coNP-complete.

Proof (hardness): from arbitrary CNF F(x), introduce k+1 fresh inputs z_1,...,z_{k+1}, and set h(x,z)=F(x) AND z_1 AND ... AND z_{k+1}. A balanced Boolean circuit for h has logarithmic depth and polynomial size, hence Barrington compiles it to a polynomial-length width-five A5 group program accepting exactly h=1. If F is UNSAT, h is zero, has XOR dimension zero. If F is SAT, choose x satisfying F and z=1^{k+1}. Any period v of h with any nonzero z-coordinate would take this accepting input to a rejecting input (regardless of the x-coordinates of v). Thus every period has its z-coordinates all zero. Its period space has codimension at least k+1, hence minimal XOR dimension>k.

Membership in coNP for FIXED k: if the period quotient F2^p/P_f has dimension>k, choose k+1 vectors v_1,...,v_{k+1} whose cosets are linearly independent. For each of the 2^{k+1}-1 nonzero combinations v=Σc_iv_i, supply a witness input x_v with f(x_v)≠f(x_v+v). The verifier checks these polynomially many (because k is fixed) input/evaluation pairs. Such a certificate exists exactly when the quotient dimension exceeds k. QED.

For variable k, the above certificate may contain 2^{k+1} pairs; do not infer a coNP upper bound uniformly in k. This theorem establishes that a universal polynomial-time, sound promise recognizer for even constant-rank linear-junta structure would imply P=NP.

## 8. Affine-certificate extension and a Fourier-rank separation

**Theorem V6 (affine positive certificates).** A deterministic epsilon-biased set with eps<2^-k (e.g. V1 with |D|=O(p²4^k)) hits every affine subspace of codimension≤k in F2^p. Consequently, it is a YES-hitting set for ANY Boolean predicate f whose accepting set, if nonempty, contains some affine subspace of codimension≤k. No common linear quotient or Fourier sparsity promise is required. The algorithm returns YES only upon finding an actual accepting assignment; it returns NO correctly under the stated positive-certificate promise. This is a direct classical corollary of small-bias sets, not a new PRG theorem.

Fourier sparsity and Fourier span dimension are genuinely different. Consider the addressing function with k address bits selecting one of m=2^k data bits: f(a,d)=d_{a}. Its Fourier expansion has at most O(m 2^k)=O(m²) nonzero terms (one for each data bit and address character, plus a constant part), while its Fourier-support span contains all m data directions and the k address directions, so its Fourier dimension is Theta(m). Theorem V2 solves SAT on such promises in polynomial time via Fourier sparsity even though Theorem V3's rank-based bound can be exponential in p=Theta(m).
