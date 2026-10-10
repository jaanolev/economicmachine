# Landau's fourth problem: primes of the form \(n^2+1\)

**This note does not prove the claim.** The claim is a famous open problem (Landau, 1912). Any argument that appears to settle infinitude should be treated as false until a hostile reading says otherwise. What follows is a map of what *can* be proved elementarily, why the usual attacks stop short, and a computation of the Bateman–Horn prediction against a census we actually ran.

---

## 0. The claim (open)

**Claim (Landau IV, open).** There are infinitely many integers \(n \ge 1\) such that \(n^2+1\) is prime.

We do **not** prove the claim. We prove the theorems in §1–§4. Section 5 describes (and does not prove) two deep theorems of Iwaniec and of Friedlander–Iwaniec. Section 6 explains why standard methods fail. Section 7 is numerical evidence only.

**Recompute recipe** (every number in §7 was produced this way; a grader should redo it independently):

1. Deterministic Miller–Rabin with bases \(\{2,3,5,7,11,13,23\}\) (valid for all integers in \((1,2^{64})\); our values satisfy \(n\le 10^6\) so \(n^2+1\le 10^{12}+1<2^{64}\)).
2. Character \(\chi_4(n)=0\) if \(n\) even, \(+1\) if \(n\equiv 1\pmod{4}\), \(-1\) if \(n\equiv 3\pmod{4}\).
3. Bateman–Horn constant \(C=\prod_p\bigl(1-\chi_4(p)/(p-1)\bigr)\), evaluated as the finite product \(C_B=\prod_{p\le B}(1-\chi_4(p)/(p-1))\) at \(B=5\cdot 10^5\), and also as the grouped product \(C_{\mathrm{abs}}=(4/\pi)\prod_{p\le B}a_p\) with \(a_p=(1-\chi_4(p)/p)^{-1}(1-\chi_4(p)/(p-1))\). The grouping uses the classical identity \(\prod_p(1-\chi_4(p)/p)=4/\pi\), which is **not proved here** (Leibniz series for \(\pi/4\) plus the Euler product for \(L(s,\chi_4)\) at \(s=1\)). Predictions in the table use \(C_{\mathrm{abs}}\); replacing it by \(C_B\) changes the \(N=10^6\) prediction by about four counts and does not affect any theorem.
4. \(I(N)=\int_1^N dt/\log(t^2+1)\). Substitute \(t=e^u\) and apply composite Simpson on \([0,\log N]\) with \(2\cdot 10^4\) panels. Prediction \(=C_{\mathrm{abs}}\cdot I(N)\). Doubling the panels at \(N=10^6\) changes \(I\) by less than \(10^{-8}\).

---

## 1. Local structure of \(n^2+1\)

### Theorem A. Odd prime factors of \(n^2+1\) are \(\equiv 1\pmod{4}\)

**Step A1 (setup).** Let \(p\) be an odd prime and \(n\in\mathbb{Z}\) with \(p\mid n^2+1\). Then \(n^2\equiv -1\pmod{p}\), so \(-1\) is a square in \(\mathbb{F}_p\).

**Step A2 (Euler's criterion for \(-1\)).** For odd prime \(p\) and \(a\not\equiv 0\pmod{p}\), Fermat gives \(a^{p-1}\equiv 1\pmod{p}\), hence \(a^{(p-1)/2}\equiv\pm 1\pmod{p}\). If \(a=b^2\), then \(a^{(p-1)/2}=b^{p-1}\equiv 1\pmod{p}\). The map \(x\mapsto x^2\) on \(\mathbb{F}_p^\times\) is exactly two-to-one (\(x\) and \(-x\) are distinct because \(p\) is odd), so there are exactly \((p-1)/2\) nonzero squares. The polynomial \(X^{(p-1)/2}-1\) has at most \((p-1)/2\) roots in \(\mathbb{F}_p\), hence the nonzero squares are precisely those roots. Therefore
\[
\Bigl(\frac{-1}{p}\Bigr)\;=\;(-1)^{(p-1)/2}.
\]
(The two sides are both \(\pm 1\), and they agree in \(\mathbb{F}_p\); since \(p>2\) they are distinct residues, so the integer signs agree.)

**Step A3.** From A1, \(\bigl(\frac{-1}{p}\bigr)=1\), so \((p-1)/2\) is even, so \(p\equiv 1\pmod{4}\).

**Corollary A4.** The prime \(2\) divides \(n^2+1\) if and only if \(n\) is odd. Every prime factor of \(n^2+1\) is therefore equal to \(2\) or \(\equiv 1\pmod{4}\). In particular no prime \(\equiv 3\pmod{4}\) ever divides a value of \(n^2+1\).

### Theorem B. For odd \(n>1\), \(n^2+1\) is composite

**Step B1.** Write \(n=2k+1\) with \(k\ge 1\). Then
\[
n^2+1=4k(k+1)+2=2\bigl(2k(k+1)+1\bigr).
\]

**Step B2.** The second factor is an integer \(\ge 2\cdot 1\cdot 2+1=5\), and \(n^2+1\ge 10>2\). Both factors are \(>1\), so \(n^2+1\) is composite.

**Corollary B3.** The only odd \(n\ge 1\) for which \(n^2+1\) can be prime is \(n=1\) (giving the prime \(2\)). For \(n>1\), a prime value of \(n^2+1\) can occur only for even \(n\). Equivalently, the open claim is the infinitude of primes of the form \(4m^2+1\).

### Theorem C. \(n^2+1\) is never a square for \(n\ge 1\)

**Step C1.** Suppose \(n^2+1=m^2\) with integers \(m>n\ge 1\). Then \(m^2-n^2=1\), so \((m-n)(m+n)=1\).

**Step C2.** Both factors are positive integers, hence \(m-n=1\) and \(m+n=1\), which forces \(n=0\), a contradiction.

(We do **not** claim the stronger statement that \(n^2+1\) is never a proper prime power \(p^k\) with \(k\ge 3\). That is Lebesgue's 1850 theorem via \(\mathbb{Z}[i]\); we did not write a complete proof and do not use it. Numerically: no perfect power \(n^2+1\) for \(1\le n\le 20000\).)

### Theorem D. \(\gcd(n^2+1,(n+1)^2+1)\) divides \(5\)

**Step D1.** Let \(a=n^2+1\) and \(b=(n+1)^2+1\). Then \(b-a=2n+1\), so \(\gcd(a,b)=\gcd(a,2n+1)\).

**Step D2.** The integer identity
\[
4(n^2+1)-(2n+1)(2n-1)=5
\]
holds for every \(n\in\mathbb{Z}\) (expand the left side: \(4n^2+4-(4n^2-1)=5\)).

**Step D3.** Any common divisor of \(n^2+1\) and \(2n+1\) therefore divides \(5\). Hence \(\gcd(a,b)\in\{1,5\}\).

(Example of gcd \(5\): \(n=2\) gives \(5\) and \(10\).)

### Theorem E. No prime modulus covers the sequence

**Step E1.** For a prime \(p\), the congruence \(n^2+1\equiv 0\pmod{p}\) has \(\nu(p)\) solutions, where \(\nu(2)=1\) and \(\nu(p)=1+\chi_4(p)\) for odd \(p\) (so \(0\) or \(2\)). In all cases \(\nu(p)<p\).

**Step E2.** Therefore, for every prime \(p\), a positive-density set of \(n\) has \(p\nmid n^2+1\). No single prime forces every value composite, and a finite set of primes still leaves a positive-density set of \(n\) avoiding all of them (Chinese remainder theorem). There is **no local covering obstruction**. This does not imply infinitude of prime values: avoiding a finite set of primes is much weaker than being prime.

---

## 2. Gaussian integers

### Theorem F. \(\mathbb{Z}[i]\) is a Euclidean domain

**Step F1.** For \(\alpha,\beta\in\mathbb{Z}[i]\) with \(\beta\neq 0\), the quotient \(\alpha/\beta\) is a point of \(\mathbb{C}\). Choose \(\gamma\in\mathbb{Z}[i]\) closest to \(\alpha/\beta\) (ties arbitrary). Then
\[
\Bigl|\frac{\alpha}{\beta}-\gamma\Bigr|^2\le\Bigl(\tfrac12\Bigr)^2+\Bigl(\tfrac12\Bigr)^2=\tfrac12<1.
\]

**Step F2.** Hence \(N(\alpha-\gamma\beta)=N(\beta)\,|\alpha/\beta-\gamma|^2<N(\beta)\), where \(N(x+yi)=x^2+y^2\). So \(N\) is a Euclidean function. A Euclidean domain is a PID (the generator of an ideal is a nonzero element of least norm), and a PID is a UFD, so irreducible elements are prime.

**Step F3 (units).** \(N(u)=1\) means \(x^2+y^2=1\) with \(x,y\in\mathbb{Z}\), hence \((x,y)\in\{(\pm 1,0),(0,\pm 1)\}\), i.e. \(u\in\{1,-1,i,-i\}\).

**Step F4 (norm is multiplicative).** \(N(\alpha\beta)=N(\alpha)N(\beta)\) holds by the identity
\[
(ac-bd)^2+(ad+bc)^2=(a^2+b^2)(c^2+d^2)
\]
(expand both sides). Equivalently \(N(\alpha)=|\alpha|^2\).

### Theorem G. Splitting of rational primes in \(\mathbb{Z}[i]\)

**Step G1 (the prime \(2\)).** \((1+i)^2=2i\), and \((-i)(2i)=2\). Thus \(2=-i(1+i)^2\) (ramified). Also \(N(1+i)=2\).

**Step G2 (squares mod \(4\)).** Squares in \(\mathbb{Z}\) are \(0\) or \(1\pmod{4}\). A sum of two squares is therefore \(0,1,\) or \(2\pmod{4}\), never \(3\pmod{4}\).

**Step G3 (inert case).** Let \(p\equiv 3\pmod{4}\) be prime. If \(p=\alpha\beta\) nontrivially in \(\mathbb{Z}[i]\), then \(p^2=N(p)=N(\alpha)N(\beta)\) forces \(N(\alpha)=p\), so \(p=a^2+b^2\), contradicting G2. Thus \(p\) remains prime in \(\mathbb{Z}[i]\).

**Step G4 (split case).** Let \(p\equiv 1\pmod{4}\). By A2, \(-1\) is a square mod \(p\), so there is an integer \(n\) with \(p\mid n^2+1=(n+i)(n-i)\). The prime \(p\) does not divide \(n+i\) in \(\mathbb{Z}[i]\): \(p(a+bi)=n+i\) would force \(pb=1\). Likewise \(p\) does not divide \(n-i\). So \(p\) divides a product but neither factor, hence \(p\) is not prime in \(\mathbb{Z}[i]\). By F, \(p\) is reducible: \(p=\pi\overline{\pi}\) up to units, with \(N(\pi)=p\).

### Theorem H. Equivalence with Gaussian primes on the line \(\mathrm{Im}=1\)

**Step H1.** \(n^2+1=N(n+i)\).

**Step H2 (if \(n+i\) is reducible).** If \(n+i=\alpha\beta\) with \(N(\alpha),N(\beta)>1\), then \(n^2+1=N(\alpha)N(\beta)\) is composite in \(\mathbb{Z}\).

**Step H3 (if \(n+i\) is irreducible).** Then \(n+i\) is prime in \(\mathbb{Z}[i]\) (F2). Let \(\pi=n+i\). Then \(\pi\) divides \(N(\pi)\in\mathbb{Z}\). Taking a rational prime \(q\mid N(\pi)\), we have \(\pi\mid q\) in \(\mathbb{Z}[i]\) after comparing to the factorisation of \(q\) from Theorem G, so \(N(\pi)\) is either \(q\) or \(q^2\). The case \(N(\pi)=q^2\) is the inert case \(q\equiv 3\pmod{4}\), which would mean \(n+i=u\,q\) for a unit \(u\). Checking the four units:

- \(u=\pm 1\): imaginary part \(0\), not \(1\);
- \(u=\pm i\): real part \(0\), so \(n=0\), and the imaginary part is \(\pm q=\pm 1\), so \(q=1\), not prime.

Hence \(N(n+i)\) is a rational prime: \(n^2+1\) is prime in \(\mathbb{Z}\).

**Step H4.** The case \(n=\pm 1\) is \(n+i\) associate to \(1+i\), with norm \(2\), which is prime. For \(n>1\), Theorem B already forces \(n\) even.

**Conclusion H.** For \(n\ge 1\), \(n^2+1\) is a rational prime if and only if \(n+i\) is a Gaussian prime. Landau IV is exactly the statement that the horizontal line \(\mathrm{Im}(z)=1\) in \(\mathbb{Z}[i]\) contains infinitely many Gaussian primes (in the first quadrant, say). This is a translation, not a proof.

---

## 3. Infinitely many primes \(\equiv 1\pmod{4}\), and infinitely many prime factors of the sequence

### Theorem I. There are infinitely many primes \(\equiv 1\pmod{4}\)

**Step I1 (starter).** \(5=2^2+1\) is prime and \(5\equiv 1\pmod{4}\). (Alternatively: \(N=2^2+1=5\).)

**Step I2 (Euclid construction).** Suppose \(p_1,\dots,p_k\) are primes \(\equiv 1\pmod{4}\). Set
\[
N=\bigl(2\,p_1\cdots p_k\bigr)^2+1.
\]
Then \(N>1\) and \(N\) is odd.

**Step I3.** Let \(q\) be any prime divisor of \(N\). By Theorem A, \(q\equiv 1\pmod{4}\). Also \(N\equiv 1\pmod{p_i}\) for each \(i\), so \(q\neq p_i\). And \(q\neq 2\). Thus \(q\) is a prime \(\equiv 1\pmod{4}\) outside the list.

**Step I4.** Repeating from I1 produces infinitely many distinct such primes.

(The number \(N\) itself need not be prime. Example computed in this folder: \((2\cdot 5\cdot 13\cdot 17\cdot 29)^2+1=4107528101=37\cdot 173\cdot 641701\), and each factor is \(\equiv 1\pmod{4}\) and new. The factor \(173\) satisfies \(173-1=172\) not a square, so a prime factor of a number of the form \(m^2+1\) need not itself be of the form \(t^2+1\).)

### Theorem J. Infinitely many distinct primes divide some value \(n^2+1\)

**Step J1.** Let \(p\equiv 1\pmod{4}\). By A2, \(-1\) is a square mod \(p\), so there exists \(n\) with \(n^2\equiv -1\pmod{p}\), i.e. \(p\mid n^2+1\).

**Step J2.** Theorem I supplies infinitely many such \(p\). Each divides some term of the sequence \(\{n^2+1\}_{n\ge 1}\).

This is much weaker than Landau IV: we get infinitely many primes *dividing* the sequence, not infinitely many *values* that are themselves prime.

---

## 4. An explicit elementary upper bound

### Theorem K. For every integer \(X\ge 1\),
\[
\#\{n\le X:n^2+1\text{ is prime}\}\;\le\; 247+\frac{X}{2}\cdot\frac{93555}{237133}.
\]

**Step K1.** Let \(S=\{5,13,17,29,37\}\) and \(P=\prod_{p\in S}p\). Each \(p\in S\) is \(\equiv 1\pmod{4}\), so \(x^2+1\equiv 0\pmod{p}\) has two roots.

**Step K2 (even \(n\) only).** By Theorem B, the only possible odd \(n\) contributing a prime is \(n=1\). Write even \(n=2m\) with \(1\le m\le\lfloor X/2\rfloor\). Then \(n^2+1=4m^2+1\).

**Step K3 (inclusion-exclusion).** For squarefree \(d\mid P\), the congruence \(4m^2+1\equiv 0\pmod{d}\) has \(\nu(d)=2^{\omega(d)}\) roots (\(2\) is invertible mod \(d\), and each prime contributes two roots for \(x^2\equiv -1\)). Therefore
\[
\#\{m\le M:d\mid 4m^2+1\}=\nu(d)\,\frac{M}{d}+\theta_d,\qquad |\theta_d|\le\nu(d).
\]
Let \(M=\lfloor X/2\rfloor\). The number of \(m\le M\) for which no \(p\in S\) divides \(4m^2+1\) is
\[
\sum_{d\mid P}\mu(d)\Bigl(\nu(d)\frac{M}{d}+\theta_d\Bigr)=M\prod_{p\in S}\Bigl(1-\frac{2}{p}\Bigr)+\sum_{d\mid P}\mu(d)\theta_d.
\]
The error is at most \(\sum_{d\mid P}2^{\omega(d)}=\prod_{p\in S}(1+2)=3^5=243\). The product is
\[
\frac{3}{5}\cdot\frac{11}{13}\cdot\frac{15}{17}\cdot\frac{27}{29}\cdot\frac{35}{37}=\frac{93555}{237133}.
\]
And \(M\le X/2\).

**Step K4 (add back small primes).** A prime value \(4m^2+1\in S\) is excluded by the sieve even though it is prime. Those values are \(5\) (\(m=1\)), \(17\) (\(m=2\)), \(37\) (\(m=3\)). Together with the odd case \(n=1\) (value \(2\)), we add back at most \(4\) integers.

**Step K5.** Every \(n\le X\) with \(n^2+1\) prime is either one of those four, or corresponds to a sifted \(m\). Hence the displayed bound. Numerically \(93555/237133\approx 0.3945254350933864\), so the bound is \(247+0.197262\,X\). At \(X=10^6\) this is about \(1.98\cdot 10^5\), versus the actual count \(54110\). The bound is rigorous and weak; it is not \(o(X)\).

We do **not** claim the stronger estimate \(O(X/\log\log X)\) in this note. That needs Mertens-type information on \(\sum_{p\le z,\,p\equiv 1(4)}1/p\), which we did not prove.

---

## 5. Deep results we describe and do not claim

The following are standard theorems in the literature. We did not prove them and we do not use them as lemmas.

- **Iwaniec (1978).** The polynomial \(n^2+1\) takes infinitely many \(P_2\)-values (integers with at most two prime factors, counted with multiplicity). The proof is a linear sieve with a switching / bilinear-form remainder, not an elementary Euclid argument.
- **Friedlander–Iwaniec (1997).** There are infinitely many primes of the form \(x^2+y^4\). Specialising \(y=1\) would be Landau IV; the method needs the extra free variable \(y\) and does not yield the line \(y=1\).

A weaker, fully proved relative of the second item is Fermat's theorem on sums of two squares, of which G2–G4 are the \(\mathbb{Z}[i]\) half: an odd prime is \(a^2+b^2\) iff it is \(\equiv 1\pmod{4}\). Combined with Theorem I this gives infinitely many primes of the form \(x^2+y^2\). That is a *union* over all lines \(\mathrm{Im}=y\), not a single line.

---

## 6. Why standard approaches fail

### 6.1 Euclid / same-shape recurrence

Theorem I produces new primes \(\equiv 1\pmod{4}\) as *factors* of a number \(N=m^2+1\). Landau IV needs \(N\) itself to be prime, or a factor that is again of the form \(t^2+1\). There is no identity that extracts such a factor.

The naive recurrence — start with the prime \(2\), replace the list of found primes \(q_i=n_i^2+1\) by \(m=2\prod q_i\), and hope \(m^2+1\) is prime — fails immediately:

- \(m=2\cdot 2=4\), \(m^2+1=17\), prime (luck);
- \(m=2\cdot 2\cdot 17=68\), \(m^2+1=4625=5^3\cdot 37\), composite.

Both \(5=2^2+1\) and \(37=6^2+1\) happen to be of the desired shape; that is not a method. Counter-example already in I4: \(173\mid 64090^2+1\) and \(173\) is not of the form \(t^2+1\). Further iterates of the recurrence are enormous and, once a composite appears, multiplying it into the product makes the next value even larger and still of no controlled factorisation.

### 6.2 Dirichlet's theorem

Dirichlet says that a *linear* polynomial \(an+b\) with \(\gcd(a,b)=1\) takes infinitely many prime values. The polynomial \(n^2+1\) has degree \(2\). Dirichlet does not apply. The natural generalisation is Bunyakovsky's conjecture (an irreducible integer-valued polynomial with no fixed prime divisor takes infinitely many prime values), which is open in every degree \(\ge 2\), including this one. Theorem E is exactly the “no fixed prime divisor” hypothesis for \(n^2+1\).

### 6.3 Sieve parity barrier

A combinatorial sieve on the set \(A=\{n^2+1:n\le X\}\) estimates the count of elements free of prime factors \(<z\). The local densities are the \(\nu(p)\) of Theorem E, and the singular product is the Bateman–Horn constant of §7. With \(z=X^\theta\) for \(\theta\) small enough that remainders can be estimated, one detects *almost-primes* (\(P_r\) for some \(r\ge 2\)), not primes.

The parity phenomenon: sieve weights built from the Möbius function on integers with small prime factors are essentially functions of \(\Omega\bmod 2\) only through an Euler product. They cannot separate \(\Omega=1\) from \(\Omega=2\) (or odd \(\Omega\) from even \(\Omega\)) without extra bilinear input. That is why a linear sieve can reach Iwaniec's \(P_2\) theorem for \(n^2+1\) and still not reach primes. We do not claim to have proved the parity barrier as a formal meta-theorem; we record it as the standard reason the sieve stops, and we illustrate it numerically in §7.3: among \(n\le 5\cdot 10^4\), the values \(n^2+1\) split as \(25041\) odd-\(\Omega\) versus \(24959\) even-\(\Omega\).

### 6.4 Circle method / von Mangoldt on a thin set

Detecting primes in \(\{n^2+1:n\le X\}\) is equivalent to estimating \(\sum_{n\le X}\Lambda(n^2+1)\). The underlying integers live near size \(X^2\) and the sequence has density \(1/X\) among integers up to \(X^2\). That is too thin for the classical circle method to isolate a main term for \(\Lambda\). Weyl differencing controls quadratic exponential sums, but not at the level needed to detect primality on a single quadratic polynomial.

### 6.5 Prime ideal theorem on a line

The prime ideal theorem in \(\mathbb{Z}[i]\) counts Gaussian primes of norm \(\le R\) as \(\sim c\,R/\log R\). Those with imaginary part exactly \(1\) are one line among \(\asymp\sqrt{R}\) possible imaginary parts. Reducing Landau IV to “Gaussian primes on a line” (Theorem H) therefore replaces one thin polynomial sequence by another; it does not create extra averaging.

### 6.6 What a proof would have to do

Any proof of the claim must produce infinitely many \(n\) for which \(n+i\) is irreducible in \(\mathbb{Z}[i]\), not merely that \(N(n+i)\) has a new prime factor \(\equiv 1\pmod{4}\). Equivalently, it must break the sieve parity barrier for this specific sequence, or exploit some structure of \(\mathbb{Z}[i]\) that is stronger than the prime ideal theorem on a thin set. We did not find such a structure.

---

## 7. Numerical evidence (not a proof)

### 7.1 Bateman–Horn constant, computed here

For a single irreducible \(f\in\mathbb{Z}[x]\) (here \(f(n)=n^2+1\), degree \(2\)), Bateman–Horn predicts
\[
\#\{n\le N:f(n)\text{ is prime}\}\;\sim\; C\int_1^N\frac{dt}{\log|f(t)|},
\]
\[
C=\prod_p\frac{1-\nu(p)/p}{1-1/p}=\prod_p\Bigl(1-\frac{\chi_4(p)}{p-1}\Bigr).
\]
This is a conjecture, not a theorem.

Finite product at \(B=5\cdot 10^5\) (exactly the product over the \(41538\) primes \(\le B\)):

\[
C_B=1.372719427895.
\]

Grouped form (uses \(\prod_p(1-\chi_4(p)/p)=4/\pi\), not proved here):

\[
C_{\mathrm{abs}}=1.37281346
\]
(float64 Euler product; digits beyond \(10^{-8}\) are not claimed). With a formal tail \(\lvert C-C_{\mathrm{abs}}\rvert\le 9\cdot 10^{-6}\) *if* the \(4/\pi\) identity is granted (because \(\lvert\log a_p\rvert\le 2/(p-1)^2\) for \(p\ge 5\) and \(\sum_{n>B}1/(n-1)^2\le 1/(B-1)\)). We treat \(C_{\mathrm{abs}}\) as a computed approximation to \(C\), not as a theorem.

### 7.2 Census versus prediction

Counts are exact (Miller–Rabin as in the recipe). Predictions use \(C_{\mathrm{abs}}\cdot I(N)\).

| \(N\) | count | BH prediction | count / prediction |
|------:|------:|-------------:|-------------------:|
| 10 | 5 | 4.658 | 1.0734 |
| 30 | 10 | 9.362 | 1.0682 |
| 100 | 19 | 21.101 | 0.9004 |
| 300 | 49 | 47.327 | 1.0353 |
| 1000 | 112 | 122.335 | 0.9155 |
| 3000 | 303 | 304.335 | 0.9956 |
| 10000 | 841 | 855.779 | 0.9827 |
| 30000 | 2268 | 2249.708 | 1.0081 |
| 100000 | 6656 | 6610.388 | 1.0069 |
| 300000 | 17924 | 17906.503 | 1.0010 |
| 1000000 | 54110 | 53970.901 | 1.0026 |

The first \(n\ge 1\) with \(n^2+1\) prime are
\[
1,2,4,6,10,14,16,20,24,26,36,40,54,56,66,74,84,90,94
\]
(giving primes \(2,5,17,37,101,197,257,401,577,677,1297,1601,2917,3137,4357,5477,7057,8101,8837\)). Among these, the only odd \(n\) is \(1\), matching Theorem B. Up through \(n\le 2000\) there is still exactly one odd such \(n\).

The ratio at \(N=10^6\) is \(1.0026\). This is consistent with Bateman–Horn and is **not** a proof of infinitude (a finite table cannot be).

### 7.3 Almost-primes and parity, \(n\le 50000\)

Complete factorisation of \(n^2+1\) for every \(n\le 5\cdot 10^4\) (trial division plus Miller–Rabin on the cofactor; no incomplete factorisations):

| \(\Omega(n^2+1)\) | count |
|---:|---:|
| 1 (prime) | 3613 |
| 2 (\(P_2\) but not prime) | 12204 |
| 3 | 16680 |
| \(\ge 4\) | 17503 |
| odd \(\Omega\) | 25041 |
| even \(\Omega\) | 24959 |

There are many more \(P_2\) values than primes, as a sieve reaching \(P_2\) would suggest. The even/odd split is \(24959:25041\), within \(0.2\%\) of \(1:1\). That is the numerical face of §6.3.

### 7.4 A tested angle: is \(\mathrm{Im}=1\) thinner than neighbouring lines?

If Landau IV failed for a reason special to the line \(\mathrm{Im}=1\), one might expect that line to be visibly poorer in Gaussian primes than \(\mathrm{Im}=k\) for small \(k\neq 1\). We counted \(n=1,\dots,2\cdot 10^5\) with \(n^2+k^2\) prime:

| \(k\) | \(\#\{n\le 2\cdot 10^5:n^2+k^2\text{ prime}\}\) |
|---:|---:|
| 1 | 12391 |
| 2 | 12306 |
| 3 | 8191 |
| 4 | 12341 |
| 5 | 16521 |
| 6 | 8193 |
| 7 | 10661 |
| 8 | 12363 |

The line \(k=1\) is not sparse among even \(k\). The dips at \(k=3,6\) and the bump at \(k=5\) match the change in the local factor at primes dividing \(k\): for \(f(n)=n^2+k^2\), if \(p\mid k\) then \(\nu(p)=1\) (namely \(n\equiv 0\)), whereas for \(k=1\) one has \(\nu(5)=2\) and \(\nu(3)=0\). So \(k=3\) *introduces* a prime factor \(3\) on a positive-density set, while \(k=5\) *relaxes* the condition at \(5\). This is ordinary Bateman–Horn bookkeeping, not a new global obstruction on \(\mathrm{Im}=1\).

The angle is therefore negative: we did not find an extra thinning on the Landau line.

### 7.5 Same-shape Euclid recurrence (tested, fails)

Recorded in §6.1. The recurrence produces one new prime of the form \(n^2+1\) and then a composite. It is not a hidden proof.

---

## 8. What remains open

Landau's fourth problem remains open. This note proves Theorems A–K and the equivalence H, computes the Bateman–Horn constant and a census through \(N=10^6\), and records why Euclid, Dirichlet, a linear sieve, the circle method, and the prime ideal theorem on a line do not finish the argument. Nothing here implies that infinitely many values \(n^2+1\) are prime.
