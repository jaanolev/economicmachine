# Report: Landau \(n^2+1\) (open)

## Verdict

Landau's fourth problem is **open**. This folder does not contain a proof of infinitude. A hostile reading of `proof.md` should fail any attempt to smuggle one in; none is made.

## What is proved (Theorems A–K in `proof.md`)

| Tag | Statement |
|-----|-----------|
| A | Odd prime factors of \(n^2+1\) are \(\equiv 1\pmod{4}\). |
| B | Odd \(n>1\) makes \(n^2+1\) composite. Only \(n=1\) among odd \(n\) can work. |
| C | \(n^2+1\) is never a square for \(n\ge 1\). |
| D | \(\gcd(n^2+1,(n+1)^2+1)\) divides \(5\). |
| E | No prime modulus covers the sequence (no local obstruction). |
| F | \(\mathbb{Z}[i]\) is Euclidean. |
| G | \(2\) ramifies; \(p\equiv 3\pmod{4}\) is inert; \(p\equiv 1\pmod{4}\) splits. |
| H | \(n^2+1\) is prime in \(\mathbb{Z}\) iff \(n+i\) is prime in \(\mathbb{Z}[i]\). Equivalence only. |
| I | Infinitely many primes \(\equiv 1\pmod{4}\). |
| J | Infinitely many distinct primes divide some \(n^2+1\). |
| K | Explicit upper bound \(\#\{n\le X:n^2+1\text{ prime}\}\le 247+(X/2)(93555/237133)\). |

Every identity used in those proofs is locked in `verify.py` at generic parameters.

## What is only numerical evidence

- Bateman–Horn constant: \(C_B=1.372719427895\) (direct product, \(B=5\cdot 10^5\)); \(C_{\mathrm{abs}}=1.372813462812\) (grouped with \(4/\pi\)).
- Census through \(N=10^6\): **54110** primes \(n^2+1\), versus BH prediction **53970.901**, ratio **1.0026**.
- Table of counts at \(N=10,30,100,\dots,10^6\) in `proof.md` §7.2; all exact as integers, predictions from Simpson quadrature.
- \(\Omega\)-statistics for \(n\le 5\cdot 10^4\): 3613 primes, 12204 proper \(P_2\), odd/even \(\Omega\) split \(25041:24959\).
- Gaussian-prime counts on \(\mathrm{Im}=k\) for \(k=1..8\), \(\mathrm{Re}\le 2\cdot 10^5\): the line \(k=1\) is not thinner than neighbouring even \(k\).
- Euclid same-shape recurrence: one lucky prime \(17\), then \(68^2+1=4625=5^3\cdot 37\).
- No perfect power \(n^2+1\) for \(1\le n\le 20000\) (the square case is Theorem C; higher powers are not a theorem here).

A finite table, however close to a conjecture, is not infinitude.

## What remains open

Infinitely many primes of the form \(n^2+1\). Also not proved here: Iwaniec's \(P_2\) theorem, Friedlander–Iwaniec primes \(x^2+y^4\), Lebesgue's theorem that \(n^2+1\) is never \(p^k\) for \(k\ge 3\), and any \(o(X)\) upper bound.

## New angle tested

Question: is \(\mathrm{Im}=1\) specially sparse among horizontal lines in \(\mathbb{Z}[i]\)? Counted Gaussian primes on \(\mathrm{Im}=k\) for \(k\le 8\). Result: **no**. Differences follow the local factor at primes dividing \(k\). Negative, but it was a real stuck-step test (the reformulation H might have hidden a line-specific obstruction). The same-shape Euclid recurrence was the other test; it dies at the second iterate.

## Time per phase

| Phase | Budget | Actual | Note |
|-------|--------|--------|------|
| Probe (finite models, BH, census design) | \(\le 15\) min | \(\sim 20\) min | Over: first locks used invented numbers; had to recompute. |
| Climb (proofs, failure map, line census) | \(\le 30\) min | \(\sim 25\) min | Stayed elementary; refused Lebesgue and \(O(X/\log\log X)\). |
| Write-up (`proof.md`, `report.md`) | \(\le 15\) min | \(\sim 15\) min | |
| Self-grade + cold grader | \(\le 10\) min | \(\sim 10\) min | Cold grader is a fresh agent on statement + `proof.md` only. |

Search-size estimate: \(N=10^6\) Miller–Rabin tests of \(40\)-bit integers, plus an \(\Omega\)-census at \(5\cdot 10^4\) and eight lines at \(2\cdot 10^5\). Every loop has a wall-clock deadline. Observed total runtime of `verify.py` is about \(6.6\) seconds.

## Errors and who caught them

The honesty rule caught the author, not the cold grader, on the first pass:

1. **Fabricated factorization** \(16901=61\cdot 277\). False (\(16901\) is prime). Caught by `test_euclid_start_values` on the first run. Replaced by the computed identity \(64090^2+1=37\cdot 173\cdot 641701\).
2. **Fabricated prime** \(50^2+1=2501\). Composite (\(41\cdot 61\)). Caught by `test_small_known_primes_n2plus1`. Replaced by the computed list of \(n\le 94\).
3. **Fabricated sieve constant** \(0.261166\). The exact product is \(93555/237133\approx 0.3945254350933864\). Caught by evaluating the `Fraction` before locking.

The cold grader then caught a real census bug:

4. **Undercounted \(\Omega\)** for \(n=45807\): \(n^2+1=2\cdot 5^7\cdot 13\cdot 1033\) has \(\Omega=10\), but `omega_big` returned \(9\) because it early-exited at `max_omega=8` before the last prime. That flipped one even/odd count (\(25042:24958\) instead of \(25041:24959\)). Buckets \(\Omega=1,2,3,\ge 4\) were already correct. Fixed by removing the early exit; locked by `test_omega_45807_not_undercounted` and `test_omega_parity_split_50000`.

The first three never reached `proof.md` as published claims. Item 4 did, and was corrected after the first cold-grade FAIL.

## Self-grade (before cold grader)

- Claimed proof of Landau IV: **0 / 10** (correctly not claimed).
- Elementary theorems A–K: **8 / 10** (complete named steps; K is weak; no \(o(X)\)).
- Numerical work: **8 / 10** (\(N=10^6\), two forms of \(C\), timeouts, exact locks).
- Honesty / anti-fabrication: **9 / 10** after the three catches above.
- New angle: **6 / 10** (real, negative, not decorative).

Overall as checkable progress on an open problem: **pass only if the cold grader finds no false theorem and recomputes the table**.

## Cold grader

Round 1 (statement + first `proof.md` only): **FAIL**. Theorems A–K accepted; infinitude not claimed; all prime counts through \(N=10^6\) matched; sieve product and Euclid identities matched. Failed solely on the §7.3 odd/even \(\Omega\) split (see error 4). Nits on A2/F/H wording and the last digit of \(C_{\mathrm{abs}}\) were also addressed.

Round 2 is required after the fix.

## How to rerun

From this folder, with the current directory on `PYTHONPATH`:

```
python verify.py
python -m pytest verify.py -q
```

On Windows PowerShell use `;` between commands, not `&&`.
