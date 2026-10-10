# Questions we have not asked yet

Related to Landau \(n^2+1\) and its neighbours, the functional-equation cluster (narrow \(Q\to Q\), d'Alembert, aquaesulian, Cauchy/Jensen), Collatz-to-powers-of-2, and the method (probe, finite models, grading, symmetry).

**Tags.** `[P]` an agent can try to prove now (elementary or contest-level writeup). `[N]` run a computation with a timeout. `[O]` open or research-level: reformulate or map failures, do **not** produce a fake proof. Difficulty `1` (minutes) to `5` (research).

**Already settled in `proof.md` (do not re-ask as open):** Theorems A–K and H; the \(N=10^6\) prime census and BH products we computed; Euclid stall at \(68^2+1=4625\); Im=\(k\) counts for \(k\le 8\), \(N\le 2\cdot 10^5\); \(\Omega\) split \(25041:24959\) at \(n\le 5\cdot 10^4\); Iwaniec \(P_2\) and Friedlander–Iwaniec as literature, not ours.

**Do not fabricate status.** If the literature may already contain a theorem, the question says so. A citation is not a proof. IMO 2024/6 (aquaesulian \(c=2\)) is solved; variants below are not that contest question restated as open.

**Count.** 500 distinct questions. Tags: [P]=346, [N]=129, [O]=25. Difficulties: 1:10, 2:314, 3:150, 4:12, 5:14. Starred: 20.

The 20 starred items are the default work orders. Other `[P][1–3]` items are backlog. `[O][5]` items are boundary markers, not proof assignments.

## Twenty most promising for an agent next

Execute in dependency order, not all twenty at once. Cluster by folder.

1. **Q1.** `[P][4]` Prove Lebesgue's theorem in Z[i]: the only solutions of x^2+1 = y^m with integers x>0, y>0, m>=2 are nonexistent (write every step; do not cite Mihailescu). We flagged this as unproved in proof.md.
   Why: We explicitly left \(x^2+1=y^m\) unproved; it is the next lemma on the same \(\mathbb{Z}[i]\) page.

2. **Q2.** `[P][4]` Write a complete elementary proof that #{n<=X: n^2+1 prime} = o(X), including whatever Mertens / L(1,chi_4)=pi/4 input you actually use; label external analytic facts. We refused O(X/log log X) for lack of this writeup.
   Why: Theorem K is not even \(o(X)\); a written Mertens/Leibniz argument is the next bound.

3. **Q3.** `[P][3]` Find a closed form for d = gcd(n^2+1, m^2+1) in terms of n,m (or prove d divides n-m and n+m in a precise way). Theorem D is only the consecutive case.
   Why: Feeds the Euclid-failure map; Theorem D is only the consecutive case.

4. **Q21.** `[N][3]` Extend the prime census of n^2+1 to N=2*10^6 (timeout 60s) and recompute the BH ratio. Our table stops at 10^6 (ratio 1.0026).
   Why: Cheap extension of a lock we already trust; checks whether the ratio 1.0026 stays put.

5. **Q45.** `[P][3]` Classify integers a with |a|<=100 such that f(n)=n^2+a has a fixed prime divisor (Bunyakovsky obstruction). Output the obstructed a and the prime. Status of infinitude for unobstructed a: open in general; do not claim...
   Why: Exact Bunyakovsky local picture for the whole neighbour family \(|a|\le 100\).

6. **Q50.** `[N][3]` For each a=1,2,3,5,6,7,10,11, compute the BH constant of n^2+a (product up to B=10^5) and the prime count for n<=10^5. Compare ratios. Is a=1 an outlier?
   Why: Same pipeline as `verify.py`; tests whether \(a=1\) is numerically special.

7. **Q70.** `[N][3]` Run the same prime-census-plus-BH pipeline for 2n^2+1, n<=10^5. This is the other monic-looking cousin (primes of the form 2n^2+1).
   Why: Closest monic-looking cousin; reuse the census code.

8. **Q150.** `[P][2]` Prove that the diagonal {n(1+i): n in Z} contains no Gaussian prime for |n|>1, because n(1+i) factors for |n|>1. Calibrates which lines can possibly work.
   Why: Five-minute lemma that calibrates dead lines versus Landau lines.

9. **Q151.** `[P][3]` Classify affine lines az+b (a,b in Z[i], a≠0) that contain only finitely many Gaussian primes for a trivial algebraic reason (the line is contained in a proper ideal, or all but finitely many points are composite beca...
   Why: Separates algebraically dead lines from open Landau-type lines.

10. **Q188.** `[P][3]` Write a precise, checkable statement of the parity barrier for the sequence A={n^2+1: n<=X}: any sieve weight depending only on the small-prime factorisation of N in A, with level z <= X^theta, theta<1, cannot be show...
   Why: We described parity; we did not write a checkable statement.

11. **Q189.** `[N][3]` For n<=10^5, compute Omega(n^2+1) completely and the odd/even split among (i) all n, (ii) n with n^2+1 free of primes <20, (iii) free of primes <100. Does sifting increase the even-Omega share, or keep 50-50?
   Why: Direct numerical face of parity after sifting; extends §7.3.

12. **Q244.** `[P][2]` Prove that every f:Q->Q with f(x+y)=f(x)+f(y) is f(x)=x f(1). No Hamel basis, no choice. (Agents often import the R-theory.)
   Why: Stops the Hamel-basis import: Cauchy on Q is f(x)=cx.

13. **Q260.** `[P][3]` Either-or Cauchy: for all x,y in Q, f(x+y)=f(x)+f(y) OR f(xy)=f(x)f(y). Classify f:Q->Q. Unsure whether this exact problem is in the literature; solve it anyway and do not claim novelty or a citation.
   Why: OR-equation adjacent to aquaesulian; finite-model friendly; literature status unsure.

14. **Q278.** `[P][3]` If f:Q->Q is additive and {f(x)/x : x≠0} is finite (finitely many slopes), prove f(x)=cx. This is one precise 'narrow slope' lemma.
   Why: A precise 'narrow' lemma that is actually provable.

15. **Q279.** `[P][3]` Classify all f:Q->Q satisfying f(x+y)+f(x-y)=2f(x)f(y) for all x,y in Q. Write the proof. Typical candidates: 1, cos(ax) but cos maps Q to Q only in degenerate cases, cosh, (q^x+q^{-x})/2 with q in Q, and f=0. Do not ...
   Why: Trigonometric FE on Q without pretending cos maps Q into Q.

16. **Q301.** `[P][3]` Classify all aquaesulian f:Q->Q for which f(r)+f(-r) is a single constant (the c=1 case). The contest shows c<=2 and that c=2 occurs; the equality case c=1 should be a complete list.
   Why: IMO 2024/6 is done (c=2); the equality case c=1 is a smaller complete classification.

17. **Q318.** `[N][3]` Finite models: count aquaesulian maps f:Z/n->Z/n for n=2,3,4,5,7,8. For each n record the max number of distinct values of f(r)+f(-r). Probe with finite models first.
   Why: Method first: probe Z/n before classifying Q.

18. **Q372.** `[P][2]` Characterise n such that 3n+1=2^k: n=(2^k-1)/3, requiring k even (2^k\equiv1 mod 3). List the first ten such n. These are the odd n that reach a power of 2 in one 3n+1 step.
   Why: Exact inverse-Collatz start; locks the powers-of-2 spine.

19. **Q376.** `[N][3]` From each 2^k, k<=20, grow the inverse Collatz tree of odd integers for t<=8 steps, keeping only exact integer odds. Count nodes by (k,t). Timeout 30s.
   Why: Finite model of flowing into 2^k; countable and timeout-able.

20. **Q420.** `[P][2]` Write a reusable cold-grader spec for an open-problem note: the grader sees only the claim plus proof.md, must recompute every locked integer, and FAILs if infinitude of an open problem is claimed. One page.
   Why: We already needed a grader; make the spec reusable.

## Suggested attack order (five first)

1. Lebesgue in \(\mathbb{Z}[i]\) — same ring as Theorem H.
2. \(\gcd(n^2+1,m^2+1)\) and a Mertens-based \(o(X)\) — finishes §4.
3. BH+census for \(n^2+a\), \(2n^2+1\), \(n^2+n+1\) — reuse `verify.py`.
4. Aquaesulian on \(\mathbb{Z}/n\) plus the \(c=1\) classification — finite models first.
5. Inverse Collatz tree from \(2^k\) and the \((2^k-1)/3\) lemma — new folder.

## Landau n^2+1 leftovers

**Q1.** ★ `[P][4]` Prove Lebesgue's theorem in Z[i]: the only solutions of x^2+1 = y^m with integers x>0, y>0, m>=2 are nonexistent (write every step; do not cite Mihailescu). We flagged this as unproved in proof.md.

**Q2.** ★ `[P][4]` Write a complete elementary proof that #{n<=X: n^2+1 prime} = o(X), including whatever Mertens / L(1,chi_4)=pi/4 input you actually use; label external analytic facts. We refused O(X/log log X) for lack of this writeup.

**Q3.** ★ `[P][3]` Find a closed form for d = gcd(n^2+1, m^2+1) in terms of n,m (or prove d divides n-m and n+m in a precise way). Theorem D is only the consecutive case.

**Q4.** `[P][2]` Prove that gcd(n^2+1, (n+2)^2+1) divides 8n+ something explicit; compute the exact divisor bound, analogous to the identity 4(n^2+1)-(2n+1)(2n-1)=5.

**Q5.** `[P][2]` For which n is gcd(n^2+1,(n+1)^2+1)=5 rather than 1? Give a clean congruence condition.

**Q6.** `[P][2]` Prove or refute: an odd prime p never satisfies p^2 | n^2+1. If true, a derivative argument (p divides n^2+1 and 2n) should finish it; if false, give the smallest counterexample.

**Q7.** `[N][2]` Search n<=10^6 for odd primes p with p^2 | n^2+1. Record the smallest such n if any. Do not guess.

**Q8.** `[P][3]` Prove or refute: n^2+1 is squarefree for all n>=1 except a thin explicit set. If you cannot prove it, do not claim it.

**Q9.** `[P][2]` Prove that x^2+1 divides x^{2k}+1 iff k is odd. (Polynomial identity in Z[x].)

**Q10.** `[P][2]` Factor x^4+1 and x^8+1 over Z and deduce when n^4+1 or n^8+1 can be prime.

**Q11.** `[P][3]` Prove the algebraic factorisation of n^{2^k}+1 (Fermat numbers sit at n=2). Which factors are of the form t^2+1?

**Q12.** `[N][2]` List all n<=10^5 for which n^2+1 is a prime power p^k, k>=2. (Square case is Theorem C; this is the computational half of Lebesgue.)

**Q13.** `[P][2]` Prove that 4m^2+1 is never divisible by any prime 3 mod 4 (special case of A, written directly for even n).

**Q14.** `[P][3]` Let S be a finite set of primes of the form t^2+1. Prove there exists m such that m^2+1 is coprime to every element of S and >1. (This is not infinitude of primes of that form.)

**Q15.** `[N][2]` Continue the same-shape Euclid recurrence one more documented iterate after 68^2+1=4625: if you multiply in the prime factors 5 and 37 as well, factor the next m^2+1 completely and record whether any new factor is t^2+1.

**Q16.** `[P][2]` Prove that if q | m^2+1 and q=t^2+1, then t divides m or a simple resultant vanishes: give the exact relation between m and t.

**Q17.** `[P][3]` When does a prime q=1 mod 4 dividing m^2+1 equal some t^2+1? Show this is equivalent to q-1 being a square, and estimate how often that happens among primes 1 mod 4 (heuristic only if you say so).

**Q18.** `[N][2]` Among primes q<=10^6 that are 1 mod 4, how many have q-1 a square? List them. (These are exactly the primes of the form t^2+1 up to that bound.)

**Q19.** `[P][2]` Prove there is no covering system of finitely many congruences n≡a_i (mod m_i) that forces n^2+1 to be always divisible by a prime from a fixed finite set. (Strengthening of Theorem E; still not infinitude.)

**Q20.** `[P][3]` Prove an explicit Brun-type bound #{n<=X: n^2+1 prime} <= C X / log log log X or better, with C computed, using only primes from a named finite-or-growing set you control. If you need Mertens, write it.

**Q21.** ★ `[N][3]` Extend the prime census of n^2+1 to N=2*10^6 (timeout 60s) and recompute the BH ratio. Our table stops at 10^6 (ratio 1.0026).

**Q22.** `[N][3]` For n<=10^5, count how often n^2+1 is P2 (Omega=2) versus prime versus Omega>=3, and plot the running ratio prime/P2.

**Q23.** `[P][2]` Prove that n^2+1 and (n+k)^2+1 can share a prime factor p iff n ≡ ±(n+k) (mod p), hence p|k or p|2n+k. Make this if-and-only-if.

**Q24.** `[P][2]` Show that the sequence a_n=n^2+1 satisfies a linear recurrence of order 2 for a_{n+1}+a_{n-1} in terms of n,a_n. Use it only if it helps a gcd argument.

**Q25.** `[N][2]` Compute the maximal prime factor of n^2+1 for n=1..200, and the maximal Omega. Any pattern, or just noise?

**Q26.** `[P][1]` Prove v2(n^2+1)=1 for odd n. (We used this implicitly in B.)

**Q27.** `[P][2]` Write v2(n^2+1) in all cases: 1 if n is odd, 0 if n is even. (The even case is immediate: n^2+1 is odd.)

**Q28.** `[P][3]` For an odd prime p=1 mod 4, let r be a square root of -1 mod p. The n with p|n^2+1 are n≡±r (mod p). Prove the first occurrence n in (0,p) is min(r,p-r), and that this n is not always of the form that makes n^2+1=p (only when p-1 is square).

**Q29.** `[N][2]` For each prime p=1 mod 4, p<=200, record the least n>0 with p|n^2+1, and whether n^2+1 equals p or a proper multiple.

**Q30.** `[P][2]` Prove that the least n>0 with p|n^2+1 is <= (p-1)/2, and that equality never holds (because r and p-r cannot both exceed (p-1)/2).

**Q31.** `[O][5]` Landau IV itself remains open: infinitely many primes n^2+1. Do not attack this as if a proof were near; only pose equivalent reformulations that change the attack surface.

**Q32.** `[P][3]` Reformulate Landau IV as: infinitely many prime elements of Z[i] lie in the coset i + Z. Prove the equivalence carefully (we have H for n+i; include negative n and units).

**Q33.** `[P][2]` Prove that n and -n give the same value n^2+1, so it is enough to take n>=0. How does this interact with counting Gaussian primes on Im=±1?

**Q34.** `[N][2]` Recompute C_B at B=10^6 and B=2*10^6. Does C_B move closer to C_abs=1.37281346? Record the gap.

**Q35.** `[P][3]` Justify the identity prod_p (1-chi_4(p)/p)=4/pi from Leibniz + Euler product at s=1, with a written error estimate so C_abs has a genuine tail bound. We treated 4/pi as an external analytic input.

**Q36.** `[P][2]` Prove that f(n)=n^2+1 is irreducible in Q[n] and primitive, and has content 1, so Bunyakovsky applies as a conjecture (no fixed prime divisor is Theorem E).

**Q37.** `[P][2]` Classify all n with n^2+1=2p, p prime. (This happens: n=3 gives 10=2*5. Equivalent to 2k(k+1)+1 prime when n=2k+1.)

**Q38.** `[N][2]` List all n<=10^5 with n^2+1=2p, p prime (Sophie-Germain-adjacent but quadratic). Count them versus BH-style guess if you can form one.

**Q39.** `[P][3]` Numbers n with n^2+1=2p are odd. Write  (2k+1)^2+1=2(2k(k+1)+1)=2p so 2k(k+1)+1 is prime. This is primes of the form 2k^2+2k+1. Prove this equivalence; infinitude is another open Bunyakovsky case (status: treat as open unless you find a reference you then still do not use as a proof).

**Q40.** `[P][2]` Prove n^2+1 = p q with p<q primes implies both p,q are 1 mod 4 (or p=2). Give the smallest ten such n.

**Q41.** `[N][2]` For n<=10^4, histogram the smallest prime factor of n^2+1. Compare to the model that s.p.f. is often the least p=1 mod 4 for which n ≡ ±sqrt(-1) (mod p).

**Q42.** `[P][2]` If n=k!, prove n^2+1 is composite for all k>=4 by exhibiting a factor (or by size plus a modular obstruction).

**Q43.** `[P][2]` If n is a multiple of 10, show n^2+1 ≡ 1 mod 100, and list the possible last two digits of n^2+1. Any forbidden endings that would have been  even or 5?

**Q44.** `[N][1]` Count primes n^2+1 with n<=1000 that end in 01, 17, 37, 41, 61, 97 (possible last two digits of squares-plus-one). Is the split uniform among allowed endings?

**Q462.** `[P][2]` Prove n^2+1 = C(2n,n) never for n>1 by size (central binomial ~ 4^n/sqrt(pi n)).

**Q463.** `[N][2]` For prime values p=n^2+1<=10^4, compute the order of 2 modulo p. Any pattern?

**Q464.** `[P][3]` Overlap of Landau primes and Fermat primes: n^2+1=2^{2^m}+1 iff n=2^{2^{m-1}}. List the known prime Fermat numbers F0..F4 in this dictionary (n=1 gives 2, not Fermat; n=2,4,16,256).

**Q465.** `[N][1]` Among n<=10^6, the Landau-Fermat overlaps are n=2,4,16,256 (F5 is composite so n=65536 is out). Verify 256^2+1=65537.

**Q466.** `[P][2]` For p=n^2+1>2, prove the possible residues of p mod 16: n=0 mod 4 gives p=1 mod 16; n=2 mod 4 gives p=5 mod 16 (e.g. 5,37).

**Q467.** `[N][2]` Residues of Landau primes p>2 modulo 16, 32, 40 versus the prediction from even n.

**Q468.** `[N][2]` Search n<=10^5 for n^2+1 a Carmichael number. Famous Carmichaels like 561 are not of the form t^2+1 (560 is not a square).

**Q469.** `[N][1]` List palindromic n^2+1 for n<=10^4 that are also prime.

**Q470.** `[P][3]` sqrt(n^2+1)-n=1/(sqrt(n^2+1)+n). The pair (n,1) solves x^2-(n^2+1)y^2=-1, so n+sqrt(n^2+1) is a unit of norm -1. This does not produce primes.

**Q471.** `[P][2]` The right field for the sequence n^2+1 (n varying) is the fixed field Q(i), not the moving field Q(sqrt(n^2+1)). Put this in the failure map.

**Q472.** `[N][2]` For n<=100, check that n+i is Gaussian-prime iff n^2+1 is rational-prime (lock of H).

**Q473.** `[P][2]` v2(n^2+1) is 1 if n odd and 0 if n even. We already used the odd case; write both.

## n^2+a and local pictures

**Q45.** ★ `[P][3]` Classify integers a with |a|<=100 such that f(n)=n^2+a has a fixed prime divisor (Bunyakovsky obstruction). Output the obstructed a and the prime. Status of infinitude for unobstructed a: open in general; do not claim otherwise.

**Q46.** `[P][2]` For which a is n^2+a even for all n? (None, unless you mis-read: n even => a even; n odd => a odd. So no a makes it always even. Prove there is no a with 2 | n^2+a for all n.)

**Q47.** `[P][2]` For which a is 3 | n^2+a for all n? Solve a ≡ -n^2 (mod 3) for all n, i.e. a ≡ 0 and a ≡ -1 (mod 3) simultaneously, impossible. Generalise: no prime p=3 mod 4 can divide n^2+a for all n if a is a square mod p? Write the criterion: nu_a(p)=p.

**Q48.** `[P][3]` Prove: f(n)=n^2+a has a fixed prime divisor iff there is a prime p with ( -a / p ) = -1 never, wait no: iff for some p, n^2 ≡ -a (mod p) for all n, which forces p | 1 and is impossible for p>2 unless the polynomial is 0 in F_p[n]. So the only fixed-divisor possibility is a constant factor of the values (content), or p dividing all values because f is identically 0 mod p. That happens iff -a is a square and the polynomial has p roots for all n, i.e. p=2 and a odd? Compute: n^2+a mod 2 is a + n^2, not constant unless... n^2 is 0 or 1. So identically 0 mod p iff p|a and p divides all squares, impossible, OR deg drops. Conclusion: n^2+a never has a fixed odd prime divisor. The only issue is p=2 when a is odd: then n even => odd, n odd => even. Not fixed. So Bunyakovsky local condition always holds for n^2+a, a≠0. Is that true? For a=-b^2, f(b)=0, values can be 0,-1,... 0 is not prime. Irreducibility fails when a is -square. Prove: n^2+a is irreducible over Q iff -a is not a square in Q.

**Q49.** `[P][2]` Prove n^2-d^2=(n-d)(n+d) is reducible, hence n^2-d^2 is prime only in degenerate cases (n=d+1, value 2d+1 maybe prime). This is the reducible neighbour of Landau.

**Q50.** ★ `[N][3]` For each a=1,2,3,5,6,7,10,11, compute the BH constant of n^2+a (product up to B=10^5) and the prime count for n<=10^5. Compare ratios. Is a=1 an outlier?

**Q51.** `[N][2]` Same census for a=-2 (Pell neighbour n^2-2). Count primes |n^2-2| for n<=10^5. Note n=2 gives 2.

**Q52.** `[P][2]` Odd prime factors of n^2+a are primes for which -a is a quadratic residue. Prove this, and for a=1 recover Theorem A.

**Q53.** `[P][2]` For a=2, odd prime factors of n^2+2 satisfy (-2/p)=1, i.e. p=1 or 3 mod 8. Prove it.

**Q54.** `[P][2]` For a=3, odd prime factors of n^2+3 satisfy (-3/p)=1, i.e. p=1 mod 3. Prove it.

**Q55.** `[P][3]` Identify the ring Z[sqrt(-a)] (or the maximal order of Q(sqrt(-a))) and state, without claiming deep class-number results you have not proved, the analogue of Theorem H: n^2+a prime iff n+sqrt(-a) is prime-like in that order, with the caveats when the order is not a UFD. Say so when the UFD list is something you have not proved.

**Q56.** `[P][2]` For a=1 the ring is Z[i], a UFD (we proved Euclidean). For a=2, is Z[sqrt(-2)] Euclidean? Prove or refute by the same closest-point argument (hexagonal vs square lattice).

**Q57.** `[P][3]` If Z[sqrt(-2)] is Euclidean, prove the analogue of Landau IV for n^2+2 is equivalent to infinitely many primes on the line Im=sqrt(-2) in that lattice. Infinitude itself: treat as open.

**Q58.** `[N][2]` Count n<=10^5 with n^2+2 prime, n^2+3 prime, n^2+5 prime. Record the three counts and the three BH predictions.

**Q59.** `[P][2]` Show that for a≡3 mod 4, n odd => n^2+a ≡ 0 mod 4? n odd => n^2≡1, a≡3 => n^2+a≡0 mod 4, so 4 divides n^2+a for odd n, hence for |n|>1 those values are composite if |n^2+a|>4. So only even n can work. Parallel to Theorem B.

**Q60.** `[P][2]` For a≡1 mod 4, n odd => n^2+a ≡ 2 mod 4, so exactly one factor of 2 when the value is even. Classify a mod 4 versus possible parities of n that can give primes.

**Q61.** `[N][2]` For a=7 (≡3 mod 4), verify computationally that all prime values of n^2+7 with 1<n<=200 come from even n (or from |n^2+7|=7).

**Q62.** `[P][3]` gcd(n^2+a,(n+1)^2+a) divides 2n+1 and also  something involving a. Prove it divides 4a+1 or an explicit polynomial in a. For a=1 recover the 5.

**Q63.** `[P][2]` For a=2, the consecutive gcd divides 9? Compute the identity analogous to D2.

**Q64.** `[O][5]` Are there infinitely many primes n^2+2? Treat as open (Bunyakovsky for this polynomial). Do not write a proof.

**Q65.** `[O][5]` Are there infinitely many primes n^2-2? Same warning.

**Q66.** `[P][2]` n^2+n+1 is (n^3-1)/(n-1) for n≠1. Prove this, and deduce prime factors of n^2+n+1 are 3 or 1 mod 3.

**Q67.** `[N][2]` Census of primes n^2+n+1 for n<=10^5 versus its BH constant. (Cyclotomic neighbour of Landau.)

**Q68.** `[P][2]` For f(n)=n^2+n+1, prove the only even value at integer n is when? n(n+1) always even, +1 odd. So all values odd. Contrast with n^2+1.

**Q69.** `[P][3]` Does n^2+n+1 have a fixed prime divisor? No: values 3,7,13,21,... Prove nu(p)<p for every p.

**Q70.** ★ `[N][3]` Run the same prime-census-plus-BH pipeline for 2n^2+1, n<=10^5. This is the other monic-looking cousin (primes of the form 2n^2+1).

**Q71.** `[P][2]` Prime factors of 2n^2+1: show -2 is a square twice or use (-1/p)(2/p). Give the residue classes.

**Q72.** `[P][2]` Prove 2n^2+1 is never divisible by a prime 5 or 7 mod 8? Check (-1/p)(2/p) for 2n^2≡-1.

**Q73.** `[N][2]` Compare counts: n^2+1 vs 2n^2+1 vs n^2+n+1 vs n^2+n+41 for n<=400. Which wins, and is that predicted by degree-2 BH (all degree 2, so the constant and the log(f) size decide)?

**Q74.** `[P][2]` Euler's n^2+n+41 is prime for n=0..39. Prove it is composite at n=40 (40^2+40+41=40*41+41=41*41).

**Q75.** `[N][2]` Count primes of the form n^2+n+41 for n=0..40 versus n=41..1000. Explain the drop by the factor 41, not by 'Euler polynomials are prime'.

**Q76.** `[P][2]` For which n is 41 | n^2+n+41? Solve n^2+n ≡0 mod 41, n(n+1)≡0, so n≡0 or -1. Thus n=41k and n=41k-1 make 41 divide the value. Prove this.

**Q77.** `[P][3]` Is there an integer-valued quadratic that is prime for more than 40 consecutive n starting at 0? Do not invent a record; search small leading coefficients up to a bound and report what you find, labelled computational.

**Q78.** `[P][2]` n^2+n+2: always even? n(n+1) even +2 even, so always even, >=2, and for n>=1 value >=4 even, composite except possibly n=0 value 2. Local obstruction at 2. Prove it.

**Q79.** `[P][2]` n^2+n+4: check mod 2 (always even? even+0 or 0+even +even). Classify n^2+n+a always even iff a even.

**Q80.** `[P][2]` Prove: n^2+n+a is always even iff a is even. Those a are obstructed at 2 for |n| large.

**Q81.** `[P][3]` List all quadratic monic f in Z[n] of discriminant |D|<=20 that are reducible or have a fixed prime divisor. The rest are Bunyakovsky candidates.

**Q82.** `[N][2]` For each unobstructed monic quadratic of discriminant |D|<=20, count prime values n=1..10^4 and rank them by count/BH.

**Q83.** `[P][2]` Iwaniec's method is described for n^2+1. Does the same P2 statement have an elementary special case for n^2+n+1 you can prove (not Iwaniec)? If not, say you cannot.

**Q84.** `[O][4]` Is n^2+n+1 = P2 infinitely often? Likely yes by the same sieve technology as Iwaniec; we have not proved it and should not claim it. Status unsure for a written elementary proof.

**Q474.** `[P][2]` a=-1: n^2-1=(n-1)(n+1) is reducible, prime only in degenerate cases (n=2 gives 3). Dead polynomial.

**Q475.** `[P][3]` Write a Theorem-K-style explicit upper bound for #{n<=X: n^2+n+1 prime} using a short set of primes 1 mod 3, with an exact rational product.

**Q476.** `[P][2]` Same style bound for 2n^2+1.

**Q477.** `[N][2]` Compare those explicit bounds at X=10^6 to actual counts for the three quadratics n^2+1, n^2+n+1, 2n^2+1.

**Q478.** `[P][2]` n^3+1=(n+1)(n^2-n+1) is always composite for n>1. A cubic warning, not a project.

**Q479.** `[N][2]` Count primes n^3+2 for n<=10^4 versus a degree-3 BH prediction ~ C N/(3 log N).

**Q480.** `[P][3]` Iwaniec for n^2+n+1 being P2: status unsure as a statement we have read. Do not claim it. You may still write an elementary K-bound.

## Other quadratics and simultaneous prime values

**Q85.** `[O][5]` Twin primes: infinitely many n with n and n+2 both prime. Open. Do not prove. How does BH for the pair (n,n+2) differ from BH for a single quadratic?

**Q86.** `[N][2]` Compute the twin-prime BH/Hardy-Littlewood constant as a product up to B=10^5 and compare twin counts n<=10^5 to the prediction. (Linear pair, not quadratic — a calibration of the same pipeline.)

**Q87.** `[O][5]` Are n^2+1 and (n+1)^2+1 simultaneously prime infinitely often? Open (and rarer: both ~n^2). Do not prove.

**Q88.** `[N][2]` Count n<=10^6 with both n^2+1 and (n+1)^2+1 prime. Theorem D says their gcd is 1 or 5, so they are not forced to share a factor.

**Q89.** `[N][2]` Count n<=10^6 with both n^2+1 and (n+2)^2+1 prime.

**Q90.** `[P][2]` If n^2+1 and (n+1)^2+1 are both prime and >5, prove they are distinct and not differing by a square (their difference is 2n+1).

**Q91.** `[O][5]` Sophie Germain: infinitely many p with 2p+1 prime. Open. Contrast the linear pair with n^2+1.

**Q92.** `[P][3]` Can n^2+1 and 2n+1 both be prime for infinitely many n? 2n+1 is linear, n^2+1 quadratic. If 2n+1=q and n=(q-1)/2, then ((q-1)/2)^2+1 prime. This is primes q such that (q-1)^2+4=4p. Open-looking; say so.

**Q93.** `[N][2]` Count n<=10^5 with n^2+1 prime and 2n+1 prime.

**Q94.** `[N][2]` Count n<=10^5 with n^2+1 prime and n+1 prime (so n=p-1, (p-1)^2+1=p^2-2p+2 prime).

**Q95.** `[P][2]` n^2+n+1 and n^2+1 are coprime or gcd divides n? Compute gcd(n^2+1,n^2+n+1)=gcd(n^2+1,n). If n|n^2+1 then n|1. So gcd|1 unless n|1. Prove they are coprime for |n|>1.

**Q96.** `[N][2]` Count n<=10^5 with both n^2+1 and n^2+n+1 prime.

**Q97.** `[P][2]` The pair (n, n^2+1) being both prime means n=p and p^2+1=q. For p>2, p odd, p^2+1 even >2, composite. So only p=2, q=5. Prove there is no odd prime p with p^2+1 prime. (Special case of B.)

**Q98.** `[P][2]` Primes p such that p^2+p+1 is also prime: p=3 gives 13. For p>3, ? No parity obstruction. Smallest examples; infinitude open.

**Q99.** `[N][2]` List primes p<=10^4 for which p^2+p+1 is prime.

**Q100.** `[P][3]` Schinzel's hypothesis H for the finite set {n^2+1, n+2}: write the local conditions and whether they hold. Do not claim H.

**Q101.** `[P][2]` For the pair {n^2+1, n^2+3}, show that for odd n both are even, hence no simultaneous primes for odd n>1. For even n both odd. Locally OK at 2.

**Q102.** `[N][2]` Count even n<=10^5 with n^2+1 and n^2+3 both prime (cousin pair of quadratics).

**Q103.** `[P][2]` n^2 and n^2+1 are consecutive, hence coprime, and n^2 is never prime for n>1. Useless for simultaneous primes. Record as a dead pair.

**Q104.** `[O][4]` Landau's third problem (Legendre): a prime between n^2 and (n+1)^2 for every n. Open. How is it adjacent to n^2+1 (the next integer after n^2)? n^2+1 itself is often that prime (n=1,2,4,...) but not always (n=8: 65 not prime, is there a prime in (64,81)? 67,71,73,79).

**Q105.** `[N][2]` For n=1..200, record whether n^2+1 is prime and whether at least one prime lies in (n^2,(n+1)^2). When n^2+1 is composite, name the smallest prime in the gap.

**Q106.** `[P][2]` Prove that (n+1)^2-n^2=2n+1, so the gap length is 2n+1. Landau III asks for a prime in an interval of length 2n+1 above n^2. This is much shorter than n^2 for large n; known zero-free region technology may give primes in longer intervals — do not claim Legendre is solved.

**Q107.** `[O][5]` Goldbach (Landau I) and twin primes (Landau II) are neighbours only historically. Write one sentence each on why their parity-barrier shape differs from n^2+1 (binary vs polynomial orbit).

**Q108.** `[P][2]` f(n)=n^2+n-1: irreducible? Discriminant 5, not a square, yes. Prime factors satisfy (5/p)=1 or p|f(n) analysis. Write nu(p).

**Q109.** `[N][2]` Census n<=10^4, f=n^2+n-1 prime (values may be negative for n=0; take n>=1, value >=1).

**Q110.** `[P][2]` f(n)=2n^2-1: related to Pell units. Prime values are 'Pell primes' sometimes; do not invent a theorem. Prove only the odd-prime-factor constraint via (2/p).

**Q111.** `[N][2]` Count primes 2n^2-1 for n<=10^4.

**Q112.** `[P][3]` A quadratic polynomial f in Z[n] takes both positive and negative values iff the leading coefficient and f at some integer have opposite signs or the vertex is real and the range crosses 0. For prime-values conjectures one usually takes |f(n)|. State a clean convention and stick to it in every census you run.

**Q113.** `[N][2]` For f(n)=n^2-n-1 (discriminant 5), count |f(n)| prime, n=1..10^4.

**Q114.** `[P][2]` Prove no three of {n^2+1,(n+1)^2+1,(n+2)^2+1} can be odd primes for n even: among three consecutive even n? n, n+1, n+2 have mixed parity. If n even, n+1 odd => (n+1)^2+1 even >2 composite for n+1>=3. So at most the even n's in a consecutive triple can contribute. In a window of 3 consecutive n, at most two candidates.

**Q115.** `[N][1]` Find the smallest n>1 such that three terms among {k^2+1: n<=k<=n+6} are prime.

**Q116.** `[P][3]` Can n^2+1 be a factorial p! ? For n^2+1=m! with m>=4, 4|m! but n^2+1 ≡1 or 2 mod 4. n even => 1 mod 4, n odd => 2 mod 4. m>=4 => m!≡0 mod 4. Contradiction. Prove n^2+1 is never a factorial for n>=1, m>=4. (m=1,2,3 check by hand.)

**Q117.** `[P][2]` Can n^2+1 be triangular k(k+1)/2? This is a Pell-type equation 2n^2+2=k^2+k. Complete the square and decide if infinitely many solutions (Pell). Infinitely many triangular numbers of the form n^2+1 is a different question from primality.

**Q118.** `[N][2]` Find all n<=10^6 with n^2+1 triangular. Lock the list.

**Q119.** `[P][2]` n^2+1 = binomial(k,2) is the triangular case. n^2+1=binomial(k,3) for k>=3: grow like k^3/6, so k ~ n^{2/3}. Search small solutions; prove a bound or run n<=10^4.

**Q120.** `[N][2]` Search n<=10^4 for n^2+1 equal to a binomial coefficient C(k,r) with 3<=r<=k/2<=20.

## Bateman-Horn: constants, predictions, tests

**Q121.** `[P][3]` Derive the BH constant for a single irreducible f of degree d from the local densities nu(p), and specialise to f(n)=n^2+1 to recover C=prod (1-chi_4(p)/(p-1)). This is a derivation of the formula we used, not a proof that the asymptotic holds.

**Q122.** `[P][2]` Prove nu(p) for n^2+1 equals 1+chi_4(p) for odd p, by counting roots of x^2+1 in F_p.

**Q123.** `[P][3]` For a pair of polynomials (f1,f2), write the BH product with nu(p)=number of n mod p with p dividing f1(n)f2(n). Specialise to (n, n+2) and to (n^2+1, (n+1)^2+1).

**Q124.** `[N][3]` Compute BH constants to B=10^5 for: n^2+1, n^2+2, n^2+n+1, 2n^2+1, n^2+n+41, n^2-2. Rank them.

**Q125.** `[N][2]` For each of those six polynomials, compute count/prediction at N=10^3,10^4,10^5. Which converges fastest?

**Q126.** `[P][2]` Explain why the BH main term is C int dt/log|f(t)| ~ C N / (deg(f) log N), so all degree-2 polynomials have the same N/log N order, differing only by C and by log(leading coeff).

**Q127.** `[P][2]` Show that replacing int_1^N dt/log(t^2+1) by (1/2) li(N) changes the N=10^6 prediction by O(N / log^2 N) or smaller; compute the numerical difference at N=10^6.

**Q128.** `[N][2]` Recompute I(N)=int_1^N dt/log(t^2+1) by two independent quadratures (log-Simpson vs scipy or tanh-sinh) at N=10^6. They must agree to <10^{-4}.

**Q129.** `[P][3]` Give a rigorous error bound for composite Simpson on the transformed integrand e^u / log(e^{2u}+1) on [0, log N]. We only checked doubling empirically.

**Q130.** `[N][2]` Partial products of C: plot C_B versus B=10^k for k=2..6. How monotone is it?

**Q131.** `[P][2]` Prove that the grouped factors a_p=(1-chi/p)^{-1}(1-chi/(p-1)) satisfy a_p=1+O(1/p^2), so the 4/pi grouping (granting 4/pi) makes the tail absolutely convergent.

**Q132.** `[P][3]` Without granting 4/pi, bound |log C - log C_B| using only |sum_{p>B} chi_4(p)/p| <= sum_{p>B} 1/p ~ log log infinity - log log B, which does not tend to 0 in that crude estimate. Conclude that a useful tail needs oscillation of chi_4. Honesty about why we grouped.

**Q133.** `[N][2]` Compute sum_{p<=B} chi_4(p)/p at B=10^3,10^4,10^5,10^6. Does it approach a limit near log(4/pi) plus higher Euler terms?

**Q134.** `[O][5]` Prove the BH conjecture for any single quadratic. Open. Do not try.

**Q135.** `[P][2]` If BH is true for n^2+1, deduce #{n<=X: n^2+1 prime} ~ C X / (2 log X). Check this simplified form against our table at N=10^6 (C*10^6/(2 log 10^6) vs 54110).

**Q136.** `[N][1]` Evaluate C*10^6/(2*log(10^6)) with C=1.37281346 and compare to 54110 and to our integral prediction 53970.901.

**Q137.** `[P][2]` BH requires f irreducible. Show that applying the formal BH product to the reducible f(n)=n^2-1 is meaningless for prime values (f(n)=(n-1)(n+1) composite for n>2), and compute what the formal product would be anyway as a cautionary number.

**Q138.** `[P][2]` For f(n)=n(n+1)+2 = n^2+n+2, which is always even for integer n, nu(2)=2=p, so a local factor (1-nu(2)/2)/(1-1/2)=0, BH predicts ~0 primes. Matches the obstruction. Prove nu(2)=2.

**Q139.** `[N][2]` Pick 10 random monic quadratics with coefficients in [-10,10], discard reducible/obstructed, compute BH C and counts at N=10^4. Any C that badly misfires?

**Q140.** `[P][3]` Write the BH constant for f(n)=n^2+n+1 as a product over p=1 mod 3 versus p=2 mod 3 (nu(p)=1+(-3/p) or similar). Compute C to 1e-4.

**Q141.** `[P][3]` Same for 2n^2+1: express C using chi_8 or the character of Q(sqrt(-2)). If unsure of the exact character, compute C only as a raw product over nu(p) counted by brute force mod p.

**Q142.** `[N][2]` For n^2+1, compare BH prediction using C_B versus C_abs at N=10,10^3,10^6. Confirm the note's claim that they differ by ~4 counts at 10^6.

**Q143.** `[P][2]` Hardy–Littlewood's original conjecture for n^2+1 is the same as BH for one polynomial. Record that naming equivalence; do not treat it as proved.

**Q144.** `[N][3]` Compute the predicted count of P2 values under a naive 'BH with Omega=2' model (if you do not have a standard formula, say so and only report the empirical P2 count). Do not invent a constant and call it classical.

**Q145.** `[P][2]` If two polynomials have BH constants C1>C2, both degree 2, BH predicts more prime values for f1 at large N. Is C(n^2+1)>C(n^2+2)? Compute both rather than guess.

**Q146.** `[N][2]` Verify C(n^2+1) vs C(n^2+2) vs C(n^2+n+1) numerically and check the inequality against counts at N=10^5.

**Q147.** `[P][3]` Sensitivity: if you omit all p=3 mod 4 from the product for n^2+1, how wrong is C? (Those p have nu=0, so the factor is 1/(1-1/p)=p/(p-1), not 1. Omitting them underestimates C.) Compute the omitted product's contribution at B=10^4.

**Q148.** `[N][2]` Monte Carlo: for random n<=10^5, the event 'n^2+1 is 0 mod p' for the first 20 primes p=1 mod 4 should have frequency ~2/p. Check.

**Q149.** `[P][2]` Prove independence of the events n^2+1≡0 mod p and n^2+1≡0 mod q for distinct primes, as n runs through a complete residue system mod pq (CRT). This is the local reason BH multiplies.

**Q481.** `[P][2]` Prime triplets (p,p+2,p+6): one of them is 0 mod 3 for p>3. Prove the obstruction. BH product must vanish. Negative-control for BH code.

**Q482.** `[N][2]` Implement that negative control: your BH code returns 0 on (n,n+2,n+6) and nonzero on n^2+1.

**Q483.** `[P][2]` Check local conditions for (n,n+2,n+8) at 2 and 3; if unobstructed, it is a legitimate BH pair-of-three.

**Q484.** `[N][2]` If (n,n+2,n+8) is unobstructed, compute its BH constant and count n<=10^5 with all three prime.

**Q485.** `[P][2]` Unit test: BH product is 0 on n^2+n+2 (always even) and nonzero on n^2+1.

**Q486.** `[N][2]` Recompute C_abs with primes to 10^6 and report 8 decimals only (do not fight float64's 12th digit).

## Gaussian primes on lines and Z[i] geometry

**Q150.** ★ `[P][2]` Prove that the diagonal {n(1+i): n in Z} contains no Gaussian prime for |n|>1, because n(1+i) factors for |n|>1. Calibrates which lines can possibly work.

**Q151.** ★ `[P][3]` Classify affine lines az+b (a,b in Z[i], a≠0) that contain only finitely many Gaussian primes for a trivial algebraic reason (the line is contained in a proper ideal, or all but finitely many points are composite because of a fixed Gaussian factor). Status of the remaining lines: treat infinitude as open, like Landau.

**Q152.** `[P][2]` Prove that every vertical line Re(z)=0 (pure imaginary) is associate to the horizontal Im=0 via multiplication by i, so they have the same Gaussian primes up to units. Im=0 is the rational integers: Gaussian primes on Im=0 are 3 mod 4 rational primes (inert) and ±1±i? 2 ramifies as 1+i. Rational primes 1 mod 4 are not prime in Z[i].

**Q153.** `[P][3]` On the real axis Im=0, the Gaussian primes are exactly the inert rational primes p=3 mod 4 (up to units). Infinitely many such p is Euclid (mod 4), which we can prove, unlike Im=1. Write this contrast in one deduction.

**Q154.** `[P][2]` Prove Im=k and Re=k are unit-equivalent (multiply by i). So our horizontal counts are also vertical counts.

**Q155.** `[N][3]` Extend the Im=k census to k=1..30 and Re<=10^5. Test that even k cluster and that odd k track the primes dividing k, as in proof.md §7.4.

**Q156.** `[N][2]` Count Gaussian primes with 0<=Im<=Re<=N (first octant) for N=200,500,1000, and compare to the prime-ideal main term. This is the fat set, not a line.

**Q157.** `[P][2]` Prove that if a Gaussian integer alpha is prime, then so are u*alpha for units u, and the conjugate. How many of the four lines ±Im=1, ±Re=1 are distinct up to this symmetry? They are all equivalent, so Landau is one orbit.

**Q158.** `[P][3]` The line Im=2 is n+2i. N=n^2+4=(n+2i)(n-2i). When is n+2i associate to a prime? For n even, n+2i is divisible by 1+i? Check v_{1+i}(n+2i). Prove n even => 1+i divides n+2i, so only odd n can give Gaussian primes on Im=2 except small cases.

**Q159.** `[N][2]` Verify: among n<=10^4 with n^2+4 prime, how many n are even? Predict ~0 for n>2.

**Q160.** `[P][2]` n^2+4=(n+2i)(n-2i). If this is a rational prime, then n+2i is Gaussian-prime. Same H-argument. Also n^2+4=(n^2+4), which can be prime (e.g. n=1, value 5). n=1 odd, 5 prime.

**Q161.** `[P][3]` For Im=k, prove that a fixed Gaussian prime pi divides n+ki for a positive-density set of n iff N(pi) divides some value n^2+k^2, i.e. -k^2 is a square mod N(pi) (with care when pi ramifies). Recover the BH local factor.

**Q162.** `[O][5]` Infinitely many Gaussian primes on Im=2? Equivalent to infinitely many primes n^2+4 with the Gaussian-prime side irreducible. Open; do not prove.

**Q163.** `[O][5]` Infinitely many Gaussian primes on any one fixed line Im=k, |k|>=1? For each fixed k this is a BH/Bunyakovsky instance (or dead, as in k=0's inert story which is NOT dead — k=0 is solved!). Separate k=0 from k≠0.

**Q164.** `[P][2]` Clarify the k=0 line: Gaussian primes on Im=0 are inert p=3 mod 4 (norm p^2), not values of n^2 being prime. Landau-type counts are "N(alpha) is a rational prime"; the axis uses a different statistic. Write the distinction carefully.

**Q165.** `[P][3]` Make two tables conceptually: (i) alpha Gaussian-prime on the line; (ii) N(alpha) rational-prime. For Im=1 they coincide (Theorem H). For Im=0 they do not. Prove the coincidence criterion: N(alpha) prime iff alpha is Gaussian-prime and not inert-of-norm-p^2.

**Q166.** `[N][2]` Count Gaussian primes (irreducible in Z[i]) on Im=0 with |Re|<=10^4 — i.e. how many p=3 mod 4 in that range — versus how many n with n^2 prime (only n=1). The two counts must differ wildly.

**Q167.** `[P][2]` Prove 1+i is the unique Gaussian prime of norm 2, up to units.

**Q168.** `[P][2]` List all Gaussian integers of norm <=10 and mark primes. Use as a finite model of the plane.

**Q169.** `[N][2]` Plot (or tabulate) Gaussian primes with |Re|,|Im|<=40. Visually, is Im=1 special? (Honesty: a 40x40 plot is not a theorem.)

**Q170.** `[P][3]` Hecke characters / Grossencharacters for Z[i] can detect primes in sectors (Pizza slices), which is a theorem under GRH or unconditionally in weak form (Kubilius, etc.). Sector ≠ line. Write why a sector is fat enough and a line is not, without claiming a specific deep theorem you have not read.

**Q171.** `[O][4]` Are there infinitely many Gaussian primes in the sector |arg z|<epsilon for every epsilon>0? I believe this is known (Hecke L-functions); do not claim it unless you write a proof. Status: likely known; say 'status unsure' if you do not have the proof.

**Q172.** `[P][2]` A sector with angle theta contains ~ theta R^2 / (2pi) Gaussian integers of |z|<=R, versus a line which contains ~R. Fat vs thin. This is the only comparison you need to write.

**Q173.** `[N][3]` Count Gaussian primes in the strip 1<=Im<=3, |Re|<=N, for N=10^3,10^4. A strip of bounded width is still thin ( ~ N points of each line). Compare to one line.

**Q174.** `[P][2]` The strip 1<=Im<=K with K growing slowly is a possible 'relative'. If K=log N, there are ~ N log N lattice points. Still not a proof. Just estimate the count of lattice points.

**Q175.** `[N][2]` For N=2000, count Gaussian primes with Im in {1,2,3,4,5} separately and the union (some alpha counted once). Union versus sum: overlap is empty because Im is unique. Sum=union.

**Q176.** `[P][2]` Prove two distinct horizontal lines Im=k and Im=ell are disjoint as sets of Gaussian integers.

**Q177.** `[P][3]` In Z[sqrt(-2)], the line n+sqrt(-2) has norm n^2+2. Prove the Euclidean algorithm works (N(x+y sqrt(-2))=x^2+2y^2, closest point in a rectangular lattice of height sqrt(2)).

**Q178.** `[P][3]` In Z[omega] (Eisenstein integers), the 'horizontal' line n+omega has norm n^2-n+1. Relate to primes n^2-n+1 (or n^2+n+1 after a shift). Infinitude open; the translation is [P].

**Q179.** `[P][2]` Prove Z[omega] is Euclidean with N(a+b omega)=a^2-ab+b^2.

**Q180.** `[N][2]` Census primes of the form n^2-n+1, n<=10^5, versus BH. Eisenstein-line analogue of our Landau census.

**Q181.** `[P][2]` Units of Z[omega] are 6th roots of unity. How many distinct lines are in the unit-orbit of {n+omega}?

**Q182.** `[P][3]` Dictionary: Landau asks for Gaussian primes with Im=1; Friedlander–Iwaniec asks for Im a square, because x^2+y^4=N(x+y^2 i). Prove this dictionary (uniqueness of a,b for p=1 mod 4 included).

**Q183.** `[P][2]` x^2+y^4 prime (rationally) iff x + y^2 i is Gaussian-prime (same H-argument). FI is primes on the parabola Im = t^2, not on a line.

**Q184.** `[O][5]` Infinitely many Gaussian primes on the parabola Im=t^2 is a theorem (FI). Infinitely many on the line Im=1 is open. Do not mix them.

**Q185.** `[N][2]` Count n<=10^4 with n^2+k^4 prime for k=1 (Landau) versus k=2 (n^2+16) versus k=3 (n^2+81). k=1 is the line; k>=2 is one row of the FI parabola.

**Q186.** `[P][2]` For k>=2, n^2+k^4 = n^2+(k^2)^2 can still be prime (17=1+16). No obstruction from k even? n odd, 1+even=odd. Fine.

**Q187.** `[N][3]` Count Gaussian primes with Im a perfect square, Im<=100^2, |Re|<=10^4. This is a finite FI-shaped box, not a proof of FI.

**Q487.** `[P][2]` Infinitely many Gaussian integers on Im=1 are coprime to 1+i (odd n). This is the 2-adic condition for being possibly prime.

**Q488.** `[P][3]` A random Gaussian integer of size R is prime with probability ~1/(2 log R), and a line has ~R points, recovering the BH heuristic. Write the dictionary.

**Q489.** `[N][2]` For R<=2000, compare (Gaussian primes on Im=1) / (R/(2 log R)) to C_abs.

**Q490.** `[P][3]` The line Re-Im=1 is {(n+1)+n i}, norm 2n^2+2n+1. Prove the identification, and that this line is not unit-equivalent to Im=1 (different slope).

**Q491.** `[N][2]` Census primes 2n^2+2n+1 for n<=10^4.

**Q492.** `[P][2]` Associates of n+i live on Im=+/-1 and Re=+/-1 only (units and conjugate). Write the eight images.

## Sieve parity and almost-primes

**Q188.** ★ `[P][3]` Write a precise, checkable statement of the parity barrier for the sequence A={n^2+1: n<=X}: any sieve weight depending only on the small-prime factorisation of N in A, with level z <= X^theta, theta<1, cannot be shown to correlate with 1_{Omega=1} better than with 1_{Omega even}. Do not claim a meta-theorem you have not proved; if you only illustrate, label it [N].

**Q189.** ★ `[N][3]` For n<=10^5, compute Omega(n^2+1) completely and the odd/even split among (i) all n, (ii) n with n^2+1 free of primes <20, (iii) free of primes <100. Does sifting increase the even-Omega share, or keep 50-50?

**Q190.** `[N][2]` Recompute the n<=50000 Omega buckets (3613, 12204, 16680, 17503, odd 25041, even 24959) independently. This is a lock, not a new claim.

**Q191.** `[N][3]` Extend the Omega census to n<=10^5. Lock the six numbers. Watch the n=45807-style undercount (do not early-exit factorisation).

**Q192.** `[P][2]` Prove that among odd n>1, Omega(n^2+1) is at least 2 (factor 2 and an odd part >=5). So the odd-n contribution to Omega=1 is only n=1. The 50-50 split is therefore almost entirely about even n.

**Q193.** `[N][2]` Redo the odd/even Omega split using only even n<=50000. Is it still ~50-50?

**Q194.** `[P][3]` Let P_r(X)=#{n<=X: Omega(n^2+1)<=r}. Iwaniec: P_2(X)->infinity. We do not prove that. Prove only the trivial P_r(X) >= P_1(X), and that P_1(X) is the Landau counting function.

**Q195.** `[N][2]` Tabulate P_1, P_2, P_3 at X=10^3,10^4,5*10^4,10^5.

**Q196.** `[P][2]` A number with Omega=2 is either p^2 or p q. Theorem C: n^2+1 is never a square, so never p^2. Thus P2 minus P1 counts semiprimes p q. Prove this reduction.

**Q197.** `[N][2]` For n<=10^4, among Omega=2 values, confirm none are squares (lock of C) and list a few p*q factorisations.

**Q198.** `[P][3]` Selberg's example of the parity problem is often given for the von Mangoldt function versus mu^2. Write a one-page account for the sequence n^2+1 specifically, with no unjustified claims.

**Q199.** `[N][2]` Compute the mean of mu(n^2+1) for n=1..N, N=10^3,10^4,10^5 (mu=0 when not squarefree). Is the mean near 0?

**Q200.** `[N][2]` Compute the mean of (-1)^{Omega(n^2+1)} for n=1..N. Near 0? That's Liouville lambda on the sequence.

**Q201.** `[P][2]` lambda(n)=(-1)^{Omega(n)}. The parity barrier is the statement that lambda is hard to detect by small-factor sieves. Prove only that a completely multiplicative function with values ±1 that is 1 at small primes cannot match lambda at primes (where lambda=-1) and at semiprimes (where lambda=+1) simultaneously if it depends only on small factors — make this a finite-model statement mod a primorial.

**Q202.** `[N][3]` Fix primorial M=30030. For n mod M, the pattern of whether small p divide n^2+1 is periodic. Among residue classes with no small prime dividing n^2+1, sample n<=10^5 in those classes and look at Omega parity of the remaining cofactor. Still ~50-50?

**Q203.** `[P][4]` An elementary proof that P_2(X)>> X / (log X)^c for n^2+1, for some c, would be a weak Iwaniec. Do not claim Iwaniec. Can you prove P_3(X)>> X / (log X)^c by a simple Eratosthenes argument? If yes, write it; if not, say so.

**Q204.** `[P][3]` Using only inclusion-exclusion on the first K primes p=1 mod 4, give a lower bound for the number of n<=X with n^2+1 free of those K primes. This is a lower bound for P_r with r unbounded, not for primes.

**Q205.** `[N][2]` Compare #{n<=X: n^2+1 is prime} to #{n<=X: n^2+1 has a prime factor > n} (i.e. is prime or 1). For n>1, a prime factor >n means the number is prime (since n^2+1 < (n+1)^2). So they coincide. Record this tautology so nobody 'discovers' it.

**Q206.** `[P][2]` sqrt(n^2+1) < n+1/(2n)+..., so the least prime factor of a composite n^2+1 is <=n. Equality almost: lpf <=n. Prove lpf(n^2+1) <=n if n^2+1 is composite.

**Q207.** `[N][2]` Histogram lpf(n^2+1)/n for composite n<=10^4. Is lpf typically much smaller than n?

**Q208.** `[P][2]` If lpf(n^2+1) >= n^{2/3}, then n^2+1 is either prime or P2 (because three primes would be >= n^2, and n^2+1 ~ n^2, borderline). Make a precise Omega bound from a lower bound on lpf.

**Q209.** `[N][2]` Count n<=10^5 composite with lpf(n^2+1) > n^{0.6}. These are the 'hard composites' / P2 candidates.

**Q210.** `[O][5]` Prove Iwaniec's P2 theorem. Out of scope; do not attempt a fake sieve paper.

**Q211.** `[P][2]` Define P2 exactly: Omega<=2 versus omega<=2 (distinct primes). For n^2+1, p^3 would be Omega=3, omega=1. We found 5^3 | 68^2+1. So the two definitions differ. Which did Iwaniec use? I believe Omega<=2. If unsure, say so, and report both counts.

**Q212.** `[N][2]` For n<=50000, count (i) Omega<=2, (ii) omega<=2. They differ by prime powers p^k, k>=3, and p^2 q, etc. How many n have omega<=2 but Omega>=3?

**Q213.** `[P][2]` 68^2+1=5^3*37 has Omega=4, omega=2. It is not P2 under Omega<=2. Lock this example as the distinction.

**Q214.** `[N][2]` Find all n<=10^4 where n^2+1 is a proper prime power p^k, k>=3 (if Lebesgue is true, this list is empty; then the Omega vs omega gap for 'almost-powers' comes from p^2 q and p^3 q etc. with at least two primes).

**Q215.** `[P][3]` Brun's pure sieve gives upper bounds matching BH order times a log log factor, for twins. Write a Brun upper bound for n^2+1 of the shape O( X (log log X)/ log X ) if you can; otherwise an honest weaker bound. This would improve Theorem K.

**Q216.** `[N][1]` At X=10^6, Theorem K gives <=197509, actual 54110, BH ~53971. Record the three numbers as the gap between proved / true / conjectured.

**Q493.** `[N][2]` Correlation between 1_{n even} and (-1)^{Omega(n^2+1)} for n<=10^5. Near 0?

**Q494.** `[P][2]` If a sieve could prove P1(X)->infinity it would prove Landau IV. Any honest sieve writeup that stops at P2 must say so in the first paragraph. Write that sentence.

**Q495.** `[N][3]` For n<=10^4, measure whether Omega parity of n^2+1 is independent of n mod p for the first 8 primes p=1 mod 4 (chi^2). Independence illustrates parity.

## x^2+y^4 and Friedlander–Iwaniec neighbours

**Q217.** `[P][2]` Prove the dictionary: a rational prime of the form x^2+y^4 is exactly N(x + y^2 i) with x + y^2 i Gaussian-prime. Do not claim FI.

**Q218.** `[P][2]` y=1 specialises to x^2+1, Landau IV. y=0 specialises to x^2, never prime for |x|>1. Write this.

**Q219.** `[N][2]` Count primes x^2+y^4 with 1<=x,y<=200. How many have y=1? (Those are Landau primes with n<=200.)

**Q220.** `[N][2]` Among primes of the form x^2+y^4 with y<=20, x<=10^4, what fraction have y even vs odd?

**Q221.** `[P][2]` If y is even, y=2z, x^2+16 z^4. Can this be prime >2? x must be odd. No immediate factorisation over Z. x^2+4 w^2 = (x+2wi)(...) in Z[i], still may be prime in Z.

**Q222.** `[P][3]` x^2+y^4 = (x + y^2 i)(x - y^2 i) in Z[i]. Over Z, is there a factorisation for special y? y=1 no. Some identities for y=k^2 further? x^2+k^8 is a special case of FI and of Landau if k=0. Don't invent an Aurifeuillean factorisation; check x^2+t^2 vs x^2+4t^4=(x+2t^2)^2 - (2t x)? Actually x^2 + 4 t^4 = (x+2t^2)^2 - 4 t^2 x, not helpful. The identity x^2+4t^4=(x+2t^2)^2-4xt^2 no. Known: x^2+4t^4=(2t^2+2tx+x)^? Sophie Germain: x^4+4t^4 factors. Note y^4 vs 4t^4. Prove x^4+4t^4 is always composite for |x|,|t|>=1 (Sophie Germain identity), which is x^2+(x t something) — different polynomial.

**Q223.** `[P][2]` Prove Sophie Germain's identity: x^4+4t^4=(x^2+2xt+2t^2)(x^2-2xt+2t^2), hence never prime for |x|,|t|>=1 except possibly when one factor is ±1.

**Q224.** `[P][2]` FI is x^2+y^4, not x^4+y^4 (which is (x^2+y^2)^2-2x^2 y^2 and usually composite) and not x^4+4y^4 (always composite). Keep the exponents straight.

**Q225.** `[N][2]` Count primes of the form x^4+y^4 with 1<=x<=y<=50. Expect very few (Iwaniec–Friedlander is y^4+x^2, degree 4 in two variables but one exponent 2). If you find many, you have a bug.

**Q226.** `[P][3]` Why does an extra variable y help? In sieve language, the sequence x^2+y^4 as (x,y) runs over a box has more averaging than n^2+1. Write a dimension count: ~ X^{1/2} * Y values of size X+Y^4. Choose Y=X^{1/4} so values ~X, number of sample points ~ X^{3/4}, still thin but thicker than the Landau X^{1/2} sample points of size X. Make this heuristic precise as a counting of lattice points, not a proof of FI.

**Q227.** `[O][5]` Prove FI. Out of scope.

**Q228.** `[O][4]` Are there infinitely many primes x^2+y^6? Status unsure (I believe this may still be open or known under extra hypotheses). Do not claim a theorem.

**Q229.** `[O][4]` Infinitely many primes x^3+2y^3 (Heath-Brown / Heath-Brown–Moroz cubic forms)? Status: some cubic binary forms are known to take infinitely many prime values. Do not claim a specific form unless you write a proof. If unsure, say so.

**Q230.** `[N][2]` Count primes x^2+y^4 with y=1,2,3,4,5 and x<=5000 as five separate series. y=1 should match our Landau census for n<=5000.

**Q231.** `[P][2]` If y is a square, y=k^2, then x^2+k^8, a thinner subset of FI. Infinitude for fixed y is Landau-like (open). Infinitude with y varying is FI (theorem, not ours).

**Q232.** `[N][2]` Smallest prime of the form x^2+y^4 with y=7,8,9,10. Just compute.

**Q233.** `[P][2]` x^2+y^4 even only when x and y have the same parity? y even => y^4≡0 mod 16, x even => even, x odd => odd. y odd => y^4≡1 mod 16, x even => 0+1 odd, x odd =>1+1=2 mod 16, even but v2=1. For x,y both odd, x^2+y^4≡2 mod 16, so divisible by 2 but not 4, and >2, hence composite. Prove: no prime x^2+y^4 with x and y both odd except 1+1=2.

**Q234.** `[P][2]` Thus FI primes with y>0 have x even or y even, and 1^2+1^4=2 is the odd-odd exception. Parallel to Theorem B.

**Q235.** `[N][2]` Verify among primes x^2+y^4 <= 10^6 with x,y>=1, the only both-odd pair is (1,1).

**Q236.** `[P][3]` The form x^2+y^4 is positive definite. The number of representations r(n)=#{(x,y): x^2+y^4=n} is usually 0 or 1 for prime n (up to signs). Prove that a prime p=x^2+y^4 has essentially unique such writing (signs and x -> -x), using unique Gaussian factorisation.

**Q237.** `[N][1]` 17=1^2+2^4=1+16. Also 17=4^2+1^2 but 1 is not a fourth power other than 1. So 17 is both Landau (n=4) and FI (x=1,y=2). List primes <=200 that are both n^2+1 and a^2+b^4 with b>1.

**Q238.** `[P][2]` A prime p=n^2+1=x^2+y^4 with y>1 would mean two writings as sum of a square and a fourth (or the same writing). n^2+1^4 = x^2+y^4 implies a difference of fourth powers / squares. Solve n^2 - x^2 = y^4 -1=(y^2-1)(y^2+1). Elementary factor chase: are there solutions with y>1, n>0, p prime? 17: n=4, x=1, y=2. Yes. Find all small solutions.

**Q239.** `[N][2]` Search y<=50, |x|<n, n^2+1=x^2+y^4 prime. List them.

**Q240.** `[P][3]` x^2+y^4 = (y^2+x i)(...). Compare to primes of the form x^2+y^2 with y not a square: those are the generic split primes, infinitely many (Dirichlet 1 mod 4 + Fermat). The extra 'y is a square' is the thin condition.

**Q241.** `[N][2]` Among the first 500 primes p=1 mod 4, how many have the odd part of the imaginary Gaussian factor a square? I.e. write p=a^2+b^2, 0<b<a, and ask whether b is a square. This is the FI condition. Heuristic density among those p is like 1/sqrt(p) in b, very sparse.

**Q242.** `[P][2]` Every p=1 mod 4 is a^2+b^2 uniquely (0<b<a). FI asks b=c^2. Landau asks b=1. Prove uniqueness of a,b (Fermat / Z[i]).

**Q243.** `[N][2]` For primes p=a^2+b^2<=10^6, count (i) b=1, (ii) b square, (iii) b cube. (i) is Landau, (ii) is FI-shaped.

## Cauchy, Jensen, and additive equations on Q

**Q244.** ★ `[P][2]` Prove that every f:Q->Q with f(x+y)=f(x)+f(y) is f(x)=x f(1). No Hamel basis, no choice. (Agents often import the R-theory.)

**Q245.** `[P][2]` Prove that every f:Q->Q with f((x+y)/2)=(f(x)+f(y))/2 is f(x)=f(0)+x (f(1)-f(0)). Jensen on Q, no regularity.

**Q246.** `[P][2]` From Jensen on Q, deduce mid-point convexity implies additivity of g(x)=f(x)-f(0) on the dyadic rationals, then on Q by scaling.

**Q247.** `[P][2]` Pexider on Q: f(x+y)=g(x)+h(y), f,g,h:Q->Q. Classify all triples.

**Q248.** `[P][2]` Quadratic Cauchy on Q: f(x+y)+f(x-y)=2f(x)+2f(y). Prove f(x)=c x^2.

**Q249.** `[P][3]` f(x+y)+f(x-y)=2f(x)f(y) is d'Alembert; save details for that section. Here: if you also assume f:Q->Q and f even, what polynomial/exponential candidates exist? List candidates only.

**Q250.** `[P][2]` Cauchy multiplicative on Q*: f(xy)=f(x)f(y), f:Q->Q. Classify using prime factorisation of rationals. Include f=0 on some primes.

**Q251.** `[P][3]` f:Q->Q, f(xy)+f(x+y)=f(x)f(y)+1. Classify. (A standard contest equation; write the proof, do not quote.)

**Q252.** `[P][2]` f:Q->Q, f(x+y)+f(x-y)=2f(x). This is quadratic-without-the-2f(y), i.e. Jensen/affine: solutions f(x)=a+bx? Check: left 2a+2bx, right 2a+2bx. And f(x)=x^2 fails. Prove all solutions are affine.

**Q253.** `[P][2]` f:Q->Q additive and multiplicative (field automorphism of Q). Prove f=id.

**Q254.** `[P][3]` f:Q->Q bijective and f(x+y)+f(x-y)=2f(x)f(y) (d'Alembert bijections). Postpone full class; first prove f(0) in {0,1,-1} or the usual trichotomy.

**Q255.** `[P][2]` Show that Cauchy's equation on Z, f:Z->Q, still gives f(n)=n f(1).

**Q256.** `[P][2]` Cauchy on Q but f:Q->R (codomain R). Still f(x)=x f(1), because the same induction on Z and inversion works, no completeness needed.

**Q257.** `[P][3]` Cauchy on R without extra assumptions: wild Hamel solutions exist if one assumes a Hamel basis (choice). Prove that such wild solutions, if they exist, cannot have graph that is Lebesgue measurable / cannot be Q-valued on a basis containing irrationals in a way that lands in Q for all real x unless... A Hamel solution f:R->Q would be Q-linear R->Q. Is that possible for all x in R? The image would be Q but R as Q-vector space has huge dimension, a Q-linear map R->Q is a choice of coordinates. It can exist with choice (projection onto one basis vector). Then f(R)=Q, wild. If the domain is Q, no wildness. Write this domain distinction.

**Q258.** `[P][2]` f:Q->Q, f(x+y)^2 = f(x)^2 + f(y)^2. Classify (few solutions).

**Q259.** `[P][2]` f:Q->Q, f(x+y)f(x-y)=f(x)^2 - f(y)^2 (cosine/sine addition). Find all, or all polynomial solutions first.

**Q260.** ★ `[P][3]` Either-or Cauchy: for all x,y in Q, f(x+y)=f(x)+f(y) OR f(xy)=f(x)f(y). Classify f:Q->Q. Unsure whether this exact problem is in the literature; solve it anyway and do not claim novelty or a citation.

**Q261.** `[P][2]` f:Q->Q monotone and Jensen => affine. Monotone is extra; on Q monotone still forces the Cauchy solutions to be the standard ones (already all solutions are standard). So monotonicity is redundant on Q. Record that.

**Q262.** `[P][2]` f:Q->Q, f(x)+f(y)=f(x+y)+c, constant c. Reduce to Cauchy by shifting.

**Q263.** `[P][2]` f:Q->Q bounded on an interval of Q (i.e. on Q ∩ [0,1]) and additive: still f(x)=cx, and boundedness forces nothing extra because those are already all solutions. Contrast with R.

**Q264.** `[P][3]` A function f:Q->Q is Q-linear iff it is additive (automatic, because scalars are integers then inverses). There are no exotic Q-linear endomorphisms of Q except multiplication by f(1). Prove End_Q(Q) ≅ Q.

**Q265.** `[P][2]` Jensen without the /2 written as f(x+y)+f(x-y)=2f(x), domain Q, we already have affine. Domain Z: same, f(n)=a+bn + periodic of period 2? Check: x=1,y=1: f(2)+f(0)=2f(1). Not a restriction to period 2. Prove f(n)=A+Bn on Z as well.

**Q266.** `[N][2]` Finite model: count additive maps (Z/n)->(Z/n). There are n of them if we require f(1) free and f(k)=k f(1), but only if this is well-defined, which it always is. All are f(x)=ax. Count=n. Contrast with additive maps (Z/n)^2 -> Z/n (more).

**Q267.** `[N][2]` Count functions f:Z/n->Z/n satisfying Jensen f(x+y)+f(x-y)=2f(x) for all x,y. Compare to n^2 (affine). For which n do extras appear (2-torsion issues when 2 is not invertible, i.e. n even)?

**Q268.** `[P][3]` On Z/2^k, Jensen/Cauchy can have extra solutions because 2 is not invertible. Classify additive f:Z/8->Z/8 (should still be f(x)=ax, since Z/8 is cyclic). Additive on a cyclic group is determined by f(1). So no extras. Where do extras live? On (Z/2)^k. Count additive maps F_2^k -> F_2^k.

**Q269.** `[P][2]` The first place Cauchy looks wild is an F_p-vector space of dimension >=2. Finite model: additive f: (Z/p)^2 -> Z/p is a linear form, p^2 of them, not just p. This is the 'Hamel toy'.

**Q270.** `[N][1]` Tabulate number of additive maps F_p^d -> F_p for p=2,3,5 and d=1,2,3.

**Q271.** `[P][2]` f:Q->Q, f(x+1)=f(x)+1 and f(x^2)=f(x)^2. Prove f=id. (Preserves successor and squares.)

**Q272.** `[P][3]` f:Q->Q, f(x+1)=f(x)+1 only. Many solutions (arbitrary on a fundamental domain R/Z intersect Q = {0}). Describe them: f(x)=x+p({x}) where p is periodic with period 1 on Q, p(Q) in Q, and p(0)=0? f(x+1)- (x+1)=f(x)-x, yes g=f-id is period 1. Any period-1 g:Q->Q works. So infinitely many. Contrast with adding one more equation.

**Q273.** `[P][2]` If in addition to f(x+1)=f(x)+1 one assumes f multiplicative or f odd or f polynomial, classify.

**Q274.** `[P][3]` Polynomial functions f in Q[x] satisfying Cauchy are only f(x)=cx. Prove by degree or binomial expansion.

**Q275.** `[P][2]` Rational functions f in Q(x) satisfying Cauchy on an infinite set: only f(x)=cx. Prove.

**Q276.** `[P][2]` f:Q->Q continuous at one point with respect to the real topology (restricting the domain). Then f(x)=cx even if we only assumed additivity on Q — already true without continuity. Again continuity is redundant. Write a warning note.

**Q277.** `[P][3]` A 'narrow' additive f:Q->Q whose image lies in Z. Then f=0, because f(1/n)=f(1)/n in Z for all n implies f(1)=0. Prove, and generalise: image in a finitely generated subgroup of Q forces f=0 or bounded denominator constraints.

**Q278.** ★ `[P][3]` If f:Q->Q is additive and {f(x)/x : x≠0} is finite (finitely many slopes), prove f(x)=cx. This is one precise 'narrow slope' lemma.

**Q496.** `[P][2]` Classify f:Q->Q with f(x+y)-f(x)-f(y)=xy. Answer f(x)=x^2/2 + c x.

**Q497.** `[P][3]` Classify f:Q->Q with f(x+y)+f(xy)=f(x)+f(y). Plug y=0,1,-1.

**Q498.** `[P][2]` Additive involutions of Q are f(x)=+/-x only, because they are multiplication by a with a^2=1.

**Q499.** `[P][3]` Involutions that also satisfy d'Alembert: solve or refute extras.

**Q500.** `[N][2]` Count involutions on Z/n and how many are aquaesulian, for n<=8.

## d'Alembert and trigonometric functional equations

**Q279.** ★ `[P][3]` Classify all f:Q->Q satisfying f(x+y)+f(x-y)=2f(x)f(y) for all x,y in Q. Write the proof. Typical candidates: 1, cos(ax) but cos maps Q to Q only in degenerate cases, cosh, (q^x+q^{-x})/2 with q in Q, and f=0. Do not assume continuity first; work algebraically on Q.

**Q280.** `[P][2]` For d'Alembert on Q, prove f is even, f(0)=1 or the zero/constant exceptions (compute f(0) from x=y=0: 2f(0)=2f(0)^2 so f(0) in {0,1}). If f(0)=0, classify (mostly 0).

**Q281.** `[P][3]` If f(0)=1, define a recurrence for f(n) on Z: Chebyshev. Show f(n)=T_n(f(1)) in the Chebyshev sense, so f|Z is determined by c=f(1). Which c in Q make f(Z) subset Q (automatic if c in Q) and extend to Q?

**Q282.** `[P][3]` Extension from Z to Q: f(1/2) satisfies 2f(1/2)^2 = f(1)+1, so f(1)+1 must be twice a rational square. This constrains c=f(1). Use this to list possible c.

**Q283.** `[P][2]` Constant solutions of d'Alembert on Q: f=1 and f=0 (f=-1 fails: left -2, right 2). Prove these are the only constants.

**Q284.** `[P][3]` Wilson's equation f(x+y)+f(x-y)=2f(x)g(y) on Q, with f,g:Q->Q. Reduce to d'Alembert when f is not identically 0, or classify the easy cases.

**Q285.** `[P][2]` The sine addition formula f(x+y)=f(x)g(y)+g(x)f(y) on Q. Find all rational-valued solutions you can, starting from polynomial ones.

**Q286.** `[N][2]` Finite model: count f:Z/n->Z/n satisfying d'Alembert for n=5,7,8,9,11. How many, and which look like discrete cosines?

**Q287.** `[P][3]` On F_p, d'Alembert solutions relate to characters of F_p or of the circle in F_{p^2}. Count them for p=5,7,11 by brute force and then explain.

**Q288.** `[P][3]` The function f(x)=(q^x+q^{-x})/2 with q in Q\{0}. For this to map Q to Q, q^x must be defined for all rational x, so q must be an n-th power in Q for all n, hence q=+/-1. Prove the only exponential-type d'Alembert solutions over Q are degenerate.

**Q289.** `[P][2]` Hom((Q,+),(Q*,*)): f(x+y)=f(x)f(y), f never 0. Then f(1)=a in Q*, f(n)=a^n, f(1/n)^n=a so a is an n-th power for all n, hence a=1 (a=-1 fails for even n). So f=1. Prove it.

**Q290.** `[P][3]` Therefore exponential building blocks for d'Alembert over Q are trivial. Remaining solutions should be cosine-type with algebraic constraints. Finish the classification or state exactly where you are stuck.

**Q291.** `[P][2]` The doubling map f(2x)=2f(x)^2-1 on Q is d'Alembert at y=x. Which c in Q have a full backwards orbit in Q under w |-> +/-sqrt((w+1)/2)?

**Q292.** `[N][2]` Iterate backwards from c=1, 1/2, 0, -1, 7/8 under the condition that (1+u)/2 is a square in Q, depth 8. Report surviving chains.

**Q293.** `[P][2]` d'Alembert on Z only: f:Z->Q. Classify (Chebyshev of f(1)).

**Q294.** `[P][2]` d'Alembert on R with continuity: f(x)=cos(ax), cosh(ax), constants. Quote this only as the regular case, then return to Q.

**Q295.** `[O][3]` d'Alembert on R with no regularity: wild solutions may exist using Hamel bases (status unsure). Do not construct one with choice and call it explicit.

**Q296.** `[P][2]` If f is polynomial in Q[x] and satisfies d'Alembert, prove deg f=0 (constants 0 or 1) by comparing degrees.

**Q297.** `[P][2]` If f is a rational function in Q(x) satisfying d'Alembert identically as rational functions, classify.

**Q298.** `[P][3]` Mixed: f(x+y)+f(x-y)=2g(x)h(y) with f,g,h:Q->Q. Reduce by special values.

**Q299.** `[P][2]` Test f(x)=(1-x^2)/(1+x^2) on Q where defined: does d'Alembert hold in the additive argument? (Cayley cosine is about a different group law.) Check algebraically and drop it if it fails.

## Aquaesulian functions (IMO 2024/6 and variants)

**Q300.** `[P][2]` Definition (fixed): f:Q->Q is aquaesulian if for all x,y in Q, f(x+f(y))=f(x)+y OR f(f(x)+y)=x+f(y). IMO 2024/6 asks for the max number c of distinct values of f(r)+f(-r). The contest answer is c=2. Do not re-solve the contest problem as if it were open; variants below are fair.

**Q301.** ★ `[P][3]` Classify all aquaesulian f:Q->Q for which f(r)+f(-r) is a single constant (the c=1 case). The contest shows c<=2 and that c=2 occurs; the equality case c=1 should be a complete list.

**Q302.** `[P][2]` Prove that f(x)=floor(x)-{x} (x in Q, real floor) is aquaesulian and attains two values of f(r)+f(-r), namely 0 and -2. Write the verification.

**Q303.** `[P][3]` Find all aquaesulian involutions (f composed with f is id).

**Q304.** `[P][3]` Find all aquaesulian additive maps (then f(x)=cx). Which c work?

**Q305.** `[P][2]` Prove there is no constant aquaesulian function: f=c makes c=c+y false and c=x+c false, so neither branch can cover all pairs.

**Q306.** `[P][2]` Prove that x |-> -x is aquaesulian, and {f(r)+f(-r)}={0}.

**Q307.** `[P][2]` Prove that x |-> x is aquaesulian, and {f(r)+f(-r)}={0}.

**Q308.** `[P][2]` Decide whether x |-> 1-x is aquaesulian by testing several pairs, then prove or give a counterexample pair.

**Q309.** `[P][3]` Linear/affine f(x)=ax+b, a,b in Q. Classify which are aquaesulian by substituting.

**Q310.** `[P][3]` Generalise the contest example to f(x)=n floor(x)-{x} or f(x)=floor(kx)-{kx} and prove which k,n work.

**Q311.** `[N][2]` Search f(x)=a floor(x)+b {x}+c for a,b,c in {-2,-1,0,1,2} on a rational grid (denominators <=12) for the aquaesulian OR, then prove survivors.

**Q312.** `[P][3]` Let Fix(f)={x: f(x)=x}. For aquaesulian f, prove Fix(f) is closed under addition.

**Q313.** `[P][2]` Prove that x+f(x) is always a fixpoint (from the instance x=y).

**Q314.** `[P][3]` Classify aquaesulian f with f(0)=0.

**Q315.** `[P][3]` Classify aquaesulian f with f(0)=1, or prove none / reduce to a shift.

**Q316.** `[P][2]` Is the set of aquaesulian functions closed under f |-> -f, under inverse when bijective, under affine conjugation? Check each.

**Q317.** `[P][3]` Aquaesulian on Z: f:Z->Z with the same OR. Classify or give families and prove no others if you can.

**Q318.** ★ `[N][3]` Finite models: count aquaesulian maps f:Z/n->Z/n for n=2,3,4,5,7,8. For each n record the max number of distinct values of f(r)+f(-r). Probe with finite models first.

**Q319.** `[N][2]` For p=5, enumerate all 5^5=3125 functions F_p->F_p and count aquaesulian ones. Report the number and the max |{f(r)+f(-r)}|.

**Q320.** `[N][3]` Enumerate aquaesulian maps on Z/7 (7^7=823543, feasible). Report the exact count and the max |im g|.

**Q321.** `[P][2]` If BOTH branches of the OR hold for all x,y, classify these strict aquaesulian maps on Q.

**Q322.** `[P][3]` The relation x ~ y meaning f(x)=y or f(y)=x. Prove ~ is symmetric, not necessarily transitive, and rephrase aquaesulian as x+f(y) ~ f(x)+y.

**Q323.** `[P][3]` Define g(r)=f(r)+f(-r). What can you say about g being even, or g(r)=g(r+a) for fixpoints a?

**Q324.** `[P][2]` For the floor example, compute g on Q cap [0,2] with denominators <=20 and confirm only {0,-2}.

**Q325.** `[P][3]` Aquaesulian f:R->R with continuity or monotonicity: classify, or show the floor example still works. Is c still 2 over R? Contest is over Q; treat R as a variant.

**Q326.** `[P][3]` Aquaesulian polynomials f in Q[x]. Classify (likely only degree 1).

**Q327.** `[P][2]` Aquaesulian and multiplicative f(xy)=f(x)f(y). Classify on Q.

**Q328.** `[P][3]` Aquaesulian as maps of a field K. For which small finite fields is the max |im g| still 2?

**Q329.** `[N][2]` For each p<=11, compute max_f |{f(r)+f(-r)}| over aquaesulian f on F_p (enumerate p<=7, sample larger and say you sampled).

**Q330.** `[P][3]` One-sided: always f(x+f(y))=f(x)+y (no OR). Classify on Q.

**Q331.** `[P][2]` The other one-sided equation f(f(x)+y)=x+f(y) for all x,y. Classify on Q.

**Q332.** `[P][3]` In the floor example, describe exactly which (x,y) use which branch (in terms of fractional parts).

**Q333.** `[P][2]` Is there an aquaesulian f with f(Q) a proper subgroup of (Q,+)? Example or impossibility.

**Q334.** `[P][3]` Must an aquaesulian f be surjective? For the floor example, prove yes or no.

**Q335.** `[P][2]` Must an aquaesulian f be injective? Prove or give a counterexample. The floor example is injective.

**Q336.** `[P][3]` If f is aquaesulian and bijective, is f^{-1} aquaesulian? Prove or counterexample.

**Q337.** `[P][2]` Find a conjugation f_c(x)=f(x+c)-c or similar that preserves aquaesulian, or prove none of the obvious ones work.

**Q338.** `[O][3]` Classify ALL aquaesulian f:Q->Q (not just the image of g). If you do not finish, list families and the obstruction. Do not claim a full classification you do not have.

**Q339.** `[P][3]` Replace g(r)=f(r)+f(-r) by h(r)=f(r)-f(-r). For aquaesulian f, is |im h| uniformly bounded? Prove a bound or give examples with many values.

**Q340.** `[P][2]` For f(x)=x, h(r)=2r is unbounded; for f(x)=-x, h=0. So h is not uniformly finite. Contrast with g.

**Q341.** `[P][3]` Classify aquaesulian f:Q->Z (integer-valued). The contest example is Q-valued, not Z-valued.

**Q342.** `[P][3]` Rewrite both branches as identities in the affine group of Q (translations vs conjugations) and use that language only if it shortens the proof.

## Narrow functions Q->Q (few slopes, few coboundary values, few pieces)

**Q343.** `[P][2]` Working definition (not a claim of standard terminology): f:Q->Q is slope-narrow if the set of difference quotients (f(x)-f(y))/(x-y) is finite; g-narrow if {f(x)+f(-x)} is finite; coboundary-narrow if f(x+y)-f(x)-f(y) has finite image. Do not cite a paper for the name.

**Q344.** `[P][3]` Classify slope-narrow f:Q->Q. These should be piecewise affine with finitely many slopes, possibly only globally affine. Prove the sharp statement.

**Q345.** `[P][3]` g-narrow is the aquaesulian invariant without the OR. Give examples with |im g|=1,2,3, or prove 3 is impossible under extra assumptions.

**Q346.** `[P][2]` Construct infinitely many K-Lipschitz maps Q->Q (K in Q), e.g. f(x)=Kx and f(x)=K floor(x). Which of these are aquaesulian?

**Q347.** `[P][3]` Finite-image f:Q->Q that is also aquaesulian: exist or not? (Constants are not aquaesulian.)

**Q348.** `[P][2]` Finite-image plus Jensen on Q implies constant. Prove.

**Q349.** `[P][2]` Finite-image plus Cauchy on Q implies 0. Prove.

**Q350.** `[P][3]` Jensen solutions that are affine on each of two complementary half-lines of Q (x<0 vs x>=0). Classify.

**Q351.** `[P][3]` The contest aquaesulian example has one slope (on each fractional-part fibre f(x)=x-2{x} has slope 1) and is g-narrow. Is every aquaesulian slope-narrow? Test the families you have.

**Q352.** `[P][2]` Write f(x)=x*a({x})+b({x}) and ask which a,b give aquaesulian maps.

**Q353.** `[N][2]` Test f(x)=x-2{x} vs f(x)=x-3{x} vs f(x)=2x-2{x} on a 30-by-30 rational grid for the aquaesulian OR.

**Q354.** `[P][3]` Almost additive: C_f(x,y)=f(x+y)-f(x)-f(y) takes values in a finite set F. If F={0}, f is additive. If F={0,1}, what happens on Q?

**Q355.** `[P][3]` f(x)=floor(x) has C_f in {0,1} on Q. Prove it, and list all f:Q->Q with C_f in {0,1} if you can.

**Q356.** `[P][2]` f(x)=floor(x) is not aquaesulian (test x=y=1/2). So almost-additive is a different narrowness.

**Q357.** `[P][3]` Classify f:Q->Z with C_f in {0,1} (integer-valued almost-additive maps; floor is the model).

**Q358.** `[P][2]` Odd aquaesulian maps: f(-x)=-f(x) implies g=0, so they are g-narrow with |im g|<=1. Classify odd aquaesulian f.

**Q359.** `[P][2]` Even aquaesulian maps: g=2f, so |im g|<infty implies finite image of f; constants are not aquaesulian. Resolve: no even aquaesulian maps, or find a nonconstant finite-image one.

**Q360.** `[P][3]` f:Q->Q with finitely many values of f(x)/x (x
eq0), and also Jensen or aquaesulian or polynomial: classify.

**Q361.** `[P][2]` Affine f(x)=ax+b is slope-narrow (one difference quotient) but origin-slope-narrow only if b=0.

**Q362.** `[N][2]` Among the aquaesulian maps you can write down, tabulate |im g|, number of difference quotients on a 50-point set, injective?, f(0), Fix(f).

**Q363.** `[P][2]` Contest example is slope-narrow (one slope) and g-narrow (|im g|=2) but has infinitely many fractional-part fibres. So slope-narrow is not 'finitely many fibres'. Keep the notions separate.

**Q364.** `[P][3]` Give an explicit g-narrow f:Q->Q with |im g|=2 that is not aquaesulian.

**Q365.** `[P][2]` f(x)=floor(x) has g(r)=floor(r)+floor(-r) in {-1,0}, so g-narrow with two values, and is not aquaesulian. Prove g in {-1,0}.

**Q366.** `[P][3]` Therefore g-narrow is strictly weaker than aquaesulian. What extra axiom turns floor-like maps into the contest map floor(x)-{x}?

**Q367.** `[O][3]` Is there a clean functional inequality or OR that characterises f_k(x)=k floor(x)-{x}? If you find one, prove it; if not, say stuck.

**Q368.** `[P][2]` Monotone and g-narrow f:Q->Q. Classify.

**Q369.** `[P][2]` Polynomial and g-narrow: the even part has finite image, hence is constant, so f(x)=c+bx. Recovers affine.

**Q370.** `[P][3]` Rational functions that are g-narrow: f(x)=x+1/x has g=0, so more examples than polynomials. Classify rational g-narrow maps.

**Q371.** `[P][2]` Is f(x)=x+1/x aquaesulian? Test pairs, then prove yes or no.

## Collatz and powers of 2

**Q372.** ★ `[P][2]` Characterise n such that 3n+1=2^k: n=(2^k-1)/3, requiring k even (2^k\equiv1 mod 3). List the first ten such n. These are the odd n that reach a power of 2 in one 3n+1 step.

**Q373.** `[P][2]` Fix one Collatz convention (T(n)=n/2 if even, 3n+1 if odd, or the accelerated (3n+1)/2^{v2}) and use it everywhere. State it.

**Q374.** `[P][2]` Prove that if n is odd and 3n+1 is a power of 2, then n is in the previous family. No other one-step hits.

**Q375.** `[P][3]` Numbers that hit 2^k in exactly two odd-steps: write the inverse map twice, n |-> (2^a n-1)/3 when that is an odd positive integer.

**Q376.** ★ `[N][3]` From each 2^k, k<=20, grow the inverse Collatz tree of odd integers for t<=8 steps, keeping only exact integer odds. Count nodes by (k,t). Timeout 30s.

**Q377.** `[P][2]` Every n=2^k reaches 1 by division by 2. The content is which other n flow into this ray.

**Q378.** `[O][5]` Collatz conjecture: every positive integer eventually reaches a power of 2 (equivalently 1). Open. Do not prove.

**Q379.** `[P][2]` The only cycle inside {2^k : k>=0} under the un-accelerated map is the 4-2-1 cycle. Prove it.

**Q380.** `[P][3]` Any cycle of positive integers must contain an odd term (a purely even cycle would decrease forever). Write it.

**Q381.** `[N][2]` Verify Collatz (reach 1) for all n<=10^6, with a timeout and a step cap. A check, not a proof.

**Q382.** `[N][2]` For n<=10^5, record the first power of 2 encountered and its exponent. Histogram the landing exponent.

**Q383.** `[N][2]` For n<=10^5, record the number of odd terms before hitting a power of 2. Histogram.

**Q384.** `[P][3]` The one-step family u_m=(4^m-1)/3 satisfies u_m=4 u_{m-1}+1. Prove it.

**Q385.** `[P][2]` Prove u_m=(4^m-1)/3. Related to base-4 repunits.

**Q386.** `[N][2]` Which u_m are prime for m<=20? Do not invent a primality theorem.

**Q387.** `[P][3]` If (2^a n-1)/3 is an integer, then 2^a n \equiv1 mod 3. Since 2\equiv-1 mod 3, write the exact rule on a and n mod 3.

**Q388.** `[P][2]` Prove 2^k-1 is never divisible by 3 when k is odd, hence (2^k-1)/3 is never an integer for odd k.

**Q389.** `[N][2]` For k=2,4,...,30, factor (2^k-1)/3 and say whether it is prime.

**Q390.** `[P][2]` Show there is always an a>=1 with 2^a m \equiv1 mod 3 (2 invertible mod 3). Existence of some inverse residue is easy; positivity and oddness are extra.

**Q391.** `[P][3]` Map the inverse graph locally at 1: (2^a-1)/3 for even a gives 1,5,21,85,...

**Q392.** `[N][2]` List edges of the inverse tree above 1 for all odd n<200 that flow to 1 in at most 10 odd steps.

**Q393.** `[P][2]` Every verified Collatz orbit is a path into the 2^k-spine plus the 4-2-1 cycle. Write that dictionary.

**Q394.** `[O][4]` Are there divergent Collatz trajectories? Open. Do not construct a fake one.

**Q395.** `[O][4]` Are there other cycles than 4-2-1 on the positive integers? Open.

**Q396.** `[P][2]` On the negatives, exhibit the cycle -1 -> -2 -> -1 under T(n)=3n+1 for odd n. Prove it, and do not claim this says anything about positives.

**Q397.** `[P][3]` Study the accelerated map as a function on Z/2^k and count cycles for k<=8. Finite model.

**Q398.** `[N][2]` For k=6,7,8, list cycles of the accelerated map on odd classes modulo 2^k if well-defined.

**Q399.** `[P][3]` Define T on odd 2-adics by (3x+1)/2^{v2(3x+1)} and check it is well-defined. Do not quote Lagarias/Bernstein as a lemma unless you construct the extension.

**Q400.** `[O][4]` Does that 2-adic map have attracting cycle only 1? Status unsure / related to the conjecture. Do not claim.

**Q401.** `[P][2]` Stopping time s(n)=least t with T^t(n)<n is finite for all even n (one step). For odds, a theorem of Terras says almost all n have finite s(n); if you have not proved it, say 'likely known; not used'.

**Q402.** `[N][2]` Compute s(n) for odd n<=10^5, histogram. Empirical finite stopping times are not a proof.

**Q403.** `[P][2]` If n\equiv1 mod 4, then v2(3n+1)>=2. Prove a table of v2(3n+1) for odd n mod 16.

**Q404.** `[N][2]` Among n<=10^5 that are 1 mod 16, what fraction have T^{<=3}(n)<n?

**Q405.** `[P][3]` Can a trajectory have v2(3n+1)=1 for 20 consecutive odd steps (always n\equiv3 mod 4)? Write the 2-adic / congruence obstruction hunt.

**Q406.** `[N][2]` Maximal run of consecutive odd iterates with v2(3n+1)=1, for starting n<=10^5. Record the record n and length.

**Q407.** `[P][3]` Every orbit hits a power of 2 iff every orbit hits 1, because the only positive chain from 2^k is 2^k->...->1. Prove the equivalence.

**Q408.** `[P][2]` k=1 and k=2 live on the 4-2-1 cycle, so they are not separate attractors. There is one attractor. Write this.

**Q409.** `[N][3]` Among n<=10^6, the proportion that have reached 1 by 100, 200, 400 steps. Report leftover size.

**Q410.** `[P][3]` The only odd positive fixed point of an accelerated step is 1: (3n+1)/2^a=n implies n(2^a-3)=1. Prove it.

**Q411.** `[P][2]` No period-2 cycle of distinct odd positives: write the 2-step algebra.

**Q412.** `[P][4]` Period-3 odd cycles: write the rational equation and show there is no positive integer solution (or find one — there should be none). Beyond length 3, compute rather than cite.

**Q413.** `[N][2]` Search for odd cycles of length <=5 with terms <=10^6. Report none, or any find (should be none).

**Q414.** `[P][2]` Syracuse function S(n)=(3n+1)/2^{v2(3n+1)} on odds. Same conjecture: some iterate is 1.

**Q415.** `[N][2]` Maximal hailstone value for n<=10^5. Record the winning n by computing, not by memory.

**Q416.** `[P][3]` Landing time tau(n) versus total steps to 1: they differ by the tail length k from 2^k to 1. Prove the relation in your convention.

**Q417.** `[N][2]` For n<=10^4, verify that relation numerically.

**Q418.** `[P][2]` Write a conversion between accelerated and un-accelerated step counts.

**Q419.** `[N][2]` For each k<=12, the largest odd inverse-tree ancestor of 2^k with value <=10^6. Are some 2^k poor attractors? (k>=3 all flow to the same cycle.)

## Meta: probing, finite models, grading, symmetry

**Q420.** ★ `[P][2]` Write a reusable cold-grader spec for an open-problem note: the grader sees only the claim plus proof.md, must recompute every locked integer, and FAILs if infinitude of an open problem is claimed. One page.

**Q421.** `[P][2]` List five ways an agent fabricates a number. For each, the lock that catches it. Use our three fabrications (16901=61*277, n=50 prime, 0.261166) as case studies.

**Q422.** `[P][2]` Finite-model recipe for a Diophantine claim: reduce mod p, small-N search, timeout. Apply it to 'n^2+1 never p^3' as a demo.

**Q423.** `[P][3]` Symmetry-search checklist for polynomial prime problems: Galois/complex factorisation, n |-> -n, ring of integers, units. Apply to n^2+1, n^2+n+1, n^2+2 in one table.

**Q424.** `[P][2]` A relative is allowed only if it feeds a stuck step. Score P2, x^2+y^4, p=1 mod 4, and n^2+k^2 lines as feeding or decorative.

**Q425.** `[P][2]` Write a one-screen honesty header template for any future open-problem note.

**Q426.** `[N][1]` Rerun verify.py with N=10^5 vs 10^6 and record wall times. Update search-size estimates.

**Q427.** `[P][2]` Probe-first rule: before proving an f:Q->Q classification, count solutions on Z/n for n<=11. Make this a preamble for aquaesulian and d'Alembert.

**Q428.** `[P][3]` Hostile-grader rubric for functional equations: substitute every family back; completeness paragraph required; finite-image claims need a proof not a plot.

**Q429.** `[P][2]` For Collatz notes, the grader rejects any 'proof' that only checks n<=N. Write that rule in one sentence.

**Q430.** `[P][2]` For BH notes, the grader rejects treating a ratio~1 at N=10^6 as a proof of the asymptotic. Write that rule.

**Q431.** `[P][3]` Sketch a lockfile of (claim_id, exact rational) asserts for every number in a proof.md.

**Q432.** `[P][2]` Search-size estimate template: operation count, bit size, timeout, abort policy. Fill it for census N=10^7, aquaesulian on F_7, Collatz to 10^7.

**Q433.** `[P][3]` Rubric: if the proof uses Z[i] Euclidean, demand the closest-point constant 1/2.

**Q434.** `[P][2]` Rubric: if the proof uses Euler's criterion, demand the 2-to-1 square map (we were nitted for it).

**Q435.** `[P][2]` A do-not-cite-as-proof list: Iwaniec 1978, FI 1997, Mihailescu, GRH, prime-ideal error terms, Terras stopping time, Hecke L-functions.

**Q436.** `[P][3]` Decision tree for a famous open problem: deliverable is (a) computations you ran (b) lemmas you proved (c) failure map (d) proof.md+verify.py+report.md. Confirm the Landau folder matches.

**Q437.** `[N][2]` Self-grade the Landau folder against that tree (0-2 on a,b,c,d) and name one hole (Lebesgue and o(X) are known holes).

**Q438.** `[P][2]` For an either-or FE, counting on Z/n is enumeration, hardness p^p. Put a warning.

**Q439.** `[P][3]` Aquaesulian symmetries to try before classifying: (x,y)|->(y,x), (x,y)|->(-x,-y), (x,y)|->(f(x),f(y)). Which preserve the OR?

**Q440.** `[P][2]` Symmetries of n^2+1 over Z are n |-> -n and residue symmetries. In Z[i], units and conjugation. Name any we missed (if none, say none).

**Q441.** `[P][2]` Stuck-step log template: stuck because X, relative Y tried, result Z. Fill one for 'Euclid does not produce t^2+1 factors'.

**Q442.** `[P][3]` A relative is illegal if deleting it changes no lemma and no computation. Audit x^2+y^4 in our proof.md (described neighbour, not a fake proof).

**Q443.** `[P][2]` Three bad Landau conclusions and one-line rebuttals: (1) 54110 primes so infinitely many (2) Z[i] UFD so infinitely many Gaussian primes on every line (3) Iwaniec P2 is almost the claim.

**Q444.** `[P][2]` Three bad Collatz conclusions and rebuttals: (1) checked to 10^20 hence true (2) 2-adic map exists hence no divergence (3) no cycle of length <=N hence no cycle.

**Q445.** `[P][2]` Three bad aquaesulian conclusions and rebuttals: (1) floor example is the only map (2) c=2 on Q implies c=2 on every ring (3) finite-field count is the Q classification.

**Q446.** `[P][3]` Generic-parameters rule: identities must be tested at n=0,1,2,-3,17 and FE at x=0,1,-1,1/2.

**Q447.** `[P][2]` Timeout policy: every loop over N has a deadline; on timeout write incomplete, not a guessed number.

**Q448.** `[P][2]` Postmortem of n=45807 Omega undercount (early exit at max_omega=8) for future factorisation code.

**Q449.** `[P][3]` Why one deterministic MR base set is enough below 2^64 if the bases are Jaeschke/Sinclair. Do not verify the census by recalling OEIS.

**Q450.** `[P][2]` OEIS allowed only to name a sequence after you computed it, never as a source of locked values.

**Q451.** `[P][2]` Literature allowed for names and for 'do not claim this deep theorem', never for a constant you could product yourself.

**Q452.** `[P][3]` Design an eval of 10 short proof.md snippets, some sneakily claiming Landau/Collatz/twins. A grader must FAIL the sneaks. Write the 10 snippets.

**Q453.** `[N][2]` Tiny eval: our proof.md §0 versus a doctored version that adds 'therefore infinitely many'. FAIL the doctoring in one sentence.

**Q454.** `[P][2]` Probe order sticker: finite fields first for FE; residue classes first for polynomials; inverse trees first for Collatz; small Gaussian box first for Z[i].

**Q455.** `[P][3]` What would earlier symmetry search have changed in the Landau note? We did n |-> -n, parity, Z[i]. If nothing was missed, say so; do not invent a missed symmetry.

**Q456.** `[P][2]` Add to the method: do not lock a number you have not printed in this session (our probe overran because of fabricated locks).

**Q457.** `[P][2]` Write a 5-item execution order for the starred list, with dependencies (Lebesgue before prime-power interpretation; Mertens before o(X); Z/n aquaesulian before or after c=1).

**Q458.** `[P][2]` Done vs not-done for Landau: done = A-K + H + census 10^6 + BH product + line k<=8 + Omega 5e4 + cold-grade PASS; not done = Lebesgue writeup, o(X), gcd(n,m), N=2e6, P2 to 1e5.

**Q459.** `[P][2]` A question tagged [O][5] is a boundary marker, not a work order. Agents may only spend time on [O][5] to reformulate or map failures.

**Q460.** `[P][2]` If two starred items belong in one future folder, send one agent not two. Cluster the 20 by folder.

**Q461.** `[P][3]` Propose future folder names that do not touch the Dalio simulator: math/lebesgue-n2plus1/, math/bh-quad-census/, math/aquaesulian-finite/, math/collatz-inverse-tree/, math/dalembert-on-q/. One line each on scope.

## Notes on status (so we do not fabricate)

- Landau IV, twin primes, Goldbach, Legendre, Bunyakovsky for any degree \(\ge 2\), Collatz, and BH as a theorem are **open**.
- Iwaniec \(P_2\) for \(n^2+1\) (1978) and Friedlander–Iwaniec primes \(x^2+y^4\) (1997) are **theorems in the literature**, not proved here and not to be sketched as ours.
- IMO 2024/6 aquaesulian \(c=2\) is **solved**. Variants (the \(c=1\) list, \(\mathbb{Z}/n\) counts, full classification of all \(f\)) are separate.
- Cauchy/Jensen on \(\mathbb{Q}\) (not \(\mathbb{R}\)) are standard and should be fully provable without choice.
- d'Alembert on \(\mathbb{Q}\) without regularity: treat classification as a writeup problem; if stuck, say stuck. Continuous d'Alembert on \(\mathbb{R}\) is classical.
- 'Narrow function' is a working definition in this file, not a claim that a paper uses that name.
- Several items say **status unsure** on purpose (e.g. \(x^2+y^6\), Hecke sectors, 2-adic Collatz folklore, Iwaniec for \(n^2+n+1\)). Look it up if needed; still write the proof if you claim it.

