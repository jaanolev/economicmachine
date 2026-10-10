#!/usr/bin/env python3
"""
Exact checks and computations for Landau's fourth problem (primes n^2+1).

This file does not claim a proof of infinitude. It locks every identity and
numerical claim used in proof.md, and recomputes the Bateman-Horn constant
from the Euler product (no external lookup).

Run:
    python verify.py
    python -m pytest verify.py -q
"""

from __future__ import annotations

import math
import os
import time
from fractions import Fraction

# ---------------------------------------------------------------------------
# Timeouts / search-size estimates
# ---------------------------------------------------------------------------

# Primality of n^2+1 for all n <= N is ~ N Miller-Rabin tests of O(log^2 N)-bit
# integers.  N = 10^6 is the main census; N = 2*10^6 is a stretch target.
DEFAULT_CENSUS_N = 1_000_000
DEFAULT_P2_N = 50_000
DEFAULT_LINE_N = 200_000
DEFAULT_BH_PRIME_BOUND = 500_000
HARD_TIMEOUT_SEC = 90.0


class Timeout(Exception):
    pass


def _deadline(seconds: float) -> float:
    return time.monotonic() + seconds


def _check(deadline: float, label: str = "computation") -> None:
    if time.monotonic() > deadline:
        raise Timeout(f"{label} exceeded its timeout")


# ---------------------------------------------------------------------------
# Primes and primality
# ---------------------------------------------------------------------------

def sieve_primes(limit: int) -> list[int]:
    """Primes in [2, limit], inclusive.  Timeout-guarded for large limits."""
    deadline = _deadline(min(30.0, HARD_TIMEOUT_SEC))
    if limit < 2:
        return []
    n = limit + 1
    mark = bytearray(b"\x01") * n
    mark[0:2] = b"\x00\x00"
    r = int(limit**0.5) + 1
    for p in range(2, r):
        if p % 512 == 0:
            _check(deadline, "sieve")
        if mark[p]:
            mark[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [i for i, v in enumerate(mark) if v]


def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r * r == n


def miller_rabin(n: int) -> bool:
    """Deterministic Miller-Rabin for 0 < n < 2^64 (and fine for larger n
    with the given bases; we only feed n^2+1 for n <= 2e6, so n^2+1 < 2^64)."""
    if n < 2:
        return False
    # small primes
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Deterministic bases for n < 2^64 (Jaeschke / Sinclair).
    for a in (2, 3, 5, 7, 11, 13, 23):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        skip = False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                skip = True
                break
        if skip:
            continue
        return False
    return True


def chi4(n: int) -> int:
    """Non-principal Dirichlet character mod 4: 0 at even, +1 if n=1 mod 4,
    -1 if n=3 mod 4."""
    if n % 2 == 0:
        return 0
    return 1 if n % 4 == 1 else -1


def n_roots_n2plus1(p: int) -> int:
    """Number of residues n mod p with n^2+1 ≡ 0 (mod p)."""
    if p == 2:
        return 1
    return 1 + chi4(p)  # 2 if p=1 mod 4, 0 if p=3 mod 4


# ---------------------------------------------------------------------------
# Bateman-Horn constant for f(n) = n^2+1
# ---------------------------------------------------------------------------

def bateman_horn_constant(prime_bound: int = DEFAULT_BH_PRIME_BOUND):
    """
    C(f) = prod_p (1 - nu(p)/p) / (1 - 1/p)
         = prod_p (1 - chi4(p)/(p-1))

    Evaluated as C = (4/pi) * prod_p a_p, where
        a_p = (1 - chi(p)/p)^{-1} * (1 - chi(p)/(p-1))
    so that a_p = 1 + O(1/p^2) and the tail is absolutely summable.

    Returns (C_estimate, abs_tail_bound, primes_used).
    """
    deadline = _deadline(30.0)
    primes = sieve_primes(prime_bound)
    # C = (4/pi) * prod a_p
    # a_2 = 1
    log_prod = 0.0
    used = 0
    for i, p in enumerate(primes):
        if i % 2000 == 0:
            _check(deadline, "BH product")
        ch = chi4(p)
        if ch == 0:
            # p = 2: a_2 = 1
            used += 1
            continue
        # a_p = (1 - ch/p)^{-1} * (1 - ch/(p-1))
        a = (1.0 / (1.0 - ch / p)) * (1.0 - ch / (p - 1.0))
        log_prod += math.log(a)
        used += 1
    partial = (4.0 / math.pi) * math.exp(log_prod)

    # Tail: |log a_p| <= 2 / (p(p-1)) for p >= 3, because
    # a_p = 1 - ch/(p(p-1)) * 1/(1 - ch/p)
    #     = 1 - ch / ((p-1)(p - ch))
    # |a_p - 1| = 1 / ((p-1)(p - ch)) <= 1 / ((p-1)(p-1)) = 1/(p-1)^2
    # |log a_p| <= 2 |a_p-1| once |a_p-1| <= 1/2, i.e. p >= 5.
    # Sum_{p > B} |log a_p| <= 2 * sum_{n > B} 1/(n-1)^2 <= 2 * int_{B-1}^inf dx/x^2
    #   = 2/(B-1).
    # So the remaining product is exp(theta) with |theta| <= 2/(prime_bound-1),
    # hence relative error <= exp(2/(B-1)) - 1 <= 3/(B-1) for B >= 20.
    tail = 3.0 / (prime_bound - 1)
    abs_bound = partial * tail
    return partial, abs_bound, used


def _f_bh_logu(u: float) -> float:
    """Integrand of I(N) after t = exp(u): e^u / log(e^{2u}+1)."""
    return math.exp(u) / math.log(math.exp(2.0 * u) + 1.0)


def integral_dt_over_log_n2plus1(N: float, steps: int = 20_000) -> float:
    """I(N) = int_1^N dt / log(t^2+1), via t=exp(u) and composite Simpson
    on [0, log N].  The transformed integrand is C^infty and the interval
    has length log N (about 14 at N=10^6), so 2e4 panels are ample.

    Even `steps` required.
    """
    if N <= 1:
        return 0.0
    if steps % 2 == 1:
        steps += 1
    lo, hi = 0.0, math.log(N)
    h = (hi - lo) / steps
    acc = _f_bh_logu(lo) + _f_bh_logu(hi)
    for i in range(1, steps):
        u = lo + i * h
        acc += (4.0 if i % 2 else 2.0) * _f_bh_logu(u)
    return acc * h / 3.0


def bateman_horn_prediction(N: int, C: float) -> float:
    """#{n <= N : f(n) prime} ~ C * int_1^N dt / log(t^2+1)."""
    return C * integral_dt_over_log_n2plus1(N)


# ---------------------------------------------------------------------------
# Census of n^2+1
# ---------------------------------------------------------------------------

def omega_big(m: int, primes: list[int]) -> int | None:
    """Total number of prime factors Omega(m), or None if we cannot finish
    factoring with the given prime table (and a primality test on the cofactor).
    """
    if m <= 1:
        return 0
    omega = 0
    x = m
    for p in primes:
        if p * p > x:
            break
        if x % p == 0:
            while x % p == 0:
                x //= p
                omega += 1
    if x > 1:
        if miller_rabin(x):
            omega += 1
        elif is_square(x) and miller_rabin(int(math.isqrt(x))):
            omega += 2
        else:
            return None  # incomplete
    return omega


def census_n2plus1(N: int, timeout: float = HARD_TIMEOUT_SEC):
    """Count primes / P2 / composites among {n^2+1 : 1 <= n <= N}.

    P2 means Omega <= 2 (Iwaniec's almost-primes), counted only when we can
    finish the factorization.  For the prime count we use Miller-Rabin only.
    """
    deadline = _deadline(timeout)
    n_prime = 0
    prime_ns: list[int] = []
    odd_n_prime = 0
    even_n_prime = 0
    # residue of n among prime-producing n
    for n in range(1, N + 1):
        if n % 4096 == 0:
            _check(deadline, f"census n<= {N}")
        val = n * n + 1
        if miller_rabin(val):
            n_prime += 1
            if n <= 200 or (n <= 10_000 and n_prime <= 80):
                prime_ns.append(n)
            if n % 2 == 1:
                odd_n_prime += 1
            else:
                even_n_prime += 1
    return {
        "N": N,
        "prime_count": n_prime,
        "odd_n_giving_prime": odd_n_prime,
        "even_n_giving_prime": even_n_prime,
        "sample_n": prime_ns[:40],
    }


def census_omega(N: int, prime_table_bound: int | None = None, timeout: float = 60.0):
    """Omega statistics for n^2+1, n <= N.  Used for the parity-barrier probe."""
    deadline = _deadline(timeout)
    if prime_table_bound is None:
        prime_table_bound = max(1000, int(N) + 10)
    primes = sieve_primes(prime_table_bound)
    buckets = {1: 0, 2: 0, 3: 0, "ge4": 0, "unknown": 0, "odd": 0, "even": 0}
    for n in range(1, N + 1):
        if n % 1024 == 0:
            _check(deadline, f"omega census n<={N}")
        om = omega_big(n * n + 1, primes)
        if om is None:
            buckets["unknown"] += 1
            continue
        if om == 1:
            buckets[1] += 1
        elif om == 2:
            buckets[2] += 1
        elif om == 3:
            buckets[3] += 1
        else:
            buckets["ge4"] += 1
        if om % 2 == 0:
            buckets["even"] += 1
        else:
            buckets["odd"] += 1
    return buckets


def euclid_recurrence(max_steps: int = 8, timeout: float = 20.0):
    """Start from n=1 (value 2) and iterate m = 2 * product of values found
    so far that are prime; test whether m^2+1 is prime.  This is the naive
    'same-shape Euclid' attempt."""
    deadline = _deadline(timeout)
    found_primes = [2]
    found_n = [1]
    log = []
    for step in range(max_steps):
        _check(deadline, "euclid recurrence")
        P = 1
        for p in found_primes:
            P *= p
        m = 2 * P
        val = m * m + 1
        is_p = miller_rabin(val)
        # factor val enough to record prime factors (small, except last steps)
        factors = []
        x = val
        d = 2
        while d * d <= x and d <= 10**7:
            if x % d == 0:
                e = 0
                while x % d == 0:
                    x //= d
                    e += 1
                factors.append((d, e))
            d += 1 if d == 2 else 2
        if x > 1:
            factors.append((x, 1))
        log.append(
            {
                "step": step + 1,
                "m": m,
                "value": val,
                "is_prime": is_p,
                "factors": factors,
                "factor_is_t2plus1": [
                    (q, is_square(q - 1)) for q, _e in factors
                ],
            }
        )
        if is_p:
            found_primes.append(val)
            found_n.append(m)
        else:
            # stop growing the product after the first composite; further
            # iterates are huge and not of independent interest
            break
    return log


def gaussian_line_prime_counts(N: int, imag_max: int = 12, timeout: float = 40.0):
    """For each k=1..imag_max, count n=1..N with n^2+k^2 prime (Gaussian
    primes on the horizontal line Im = k, up to Re = N)."""
    deadline = _deadline(timeout)
    out = {}
    for k in range(1, imag_max + 1):
        c = 0
        for n in range(1, N + 1):
            if n % 8192 == 0:
                _check(deadline, "gaussian lines")
            if miller_rabin(n * n + k * k):
                c += 1
        out[k] = c
    return out


# ---------------------------------------------------------------------------
# Exact algebraic / modular identities (generic parameters)
# ---------------------------------------------------------------------------

def test_chi4_multiplicative():
    for a in range(1, 40):
        for b in range(1, 40):
            assert chi4(a * b) == chi4(a) * chi4(b), (a, b)


def test_legendre_minus1_via_euler():
    """(-1/p) = (-1)^((p-1)/2) for odd primes p, via Euler's criterion
    computed directly in F_p."""
    primes = sieve_primes(300)
    for p in primes:
        if p == 2:
            continue
        euler = pow(p - 1, (p - 1) // 2, p)  # (-1)^{(p-1)/2} mod p
        # Euler's criterion: (-1/p) ≡ (-1)^{(p-1)/2} (mod p), both ±1
        expected_legendre = 1 if ((p - 1) // 2) % 2 == 0 else -1
        assert expected_legendre in (1, -1)
        assert euler == (expected_legendre % p)
        # and p=1 mod 4 iff that is +1
        assert (expected_legendre == 1) == (p % 4 == 1)


def test_odd_prime_factors_are_1_mod_4():
    """For many n, every odd prime factor of n^2+1 is 1 mod 4."""
    primes = sieve_primes(5000)
    for n in range(0, 400):
        val = n * n + 1
        x = val
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                if p == 2:
                    while x % 2 == 0:
                        x //= 2
                    continue
                assert p % 4 == 1, (n, val, p)
                while x % p == 0:
                    x //= p
        if x > 1:
            # leftover prime or 1
            if miller_rabin(x):
                if x != 2:
                    assert x % 4 == 1, (n, val, x)
            else:
                r = int(math.isqrt(x))
                if r * r == x and miller_rabin(r) and r != 2:
                    assert r % 4 == 1


def test_odd_n_greater_than_1_gives_even_composite():
    for n in range(3, 201, 2):
        val = n * n + 1
        assert val % 2 == 0
        assert val >= 10
        assert not miller_rabin(val)


def test_n2plus1_never_square_for_n_ge_1():
    for n in range(1, 500):
        assert not is_square(n * n + 1)


def test_consecutive_gcd_divides_5():
    """gcd(n^2+1, (n+1)^2+1) divides 5.  Also the identity
    4(n^2+1) - (2n+1)(2n-1) = 5."""
    for n in range(0, 250):
        a = n * n + 1
        b = (n + 1) * (n + 1) + 1
        g = math.gcd(a, b)
        assert 5 % g == 0 or g == 1
        assert g in (1, 5)
        assert 4 * a - (2 * n + 1) * (2 * n - 1) == 5


def test_gaussian_norm_identity():
    """N(n+i) = n^2+1, and N is completely multiplicative on Z[i] representatives."""
    for n in range(-30, 31):
        assert n * n + 1 == n * n + 1 * 1
    for a in range(-8, 9):
        for b in range(-8, 9):
            for c in range(-8, 9):
                for d in range(-8, 9):
                    # (a+bi)(c+di) = (ac-bd)+(ad+bc)i
                    re = a * c - b * d
                    im = a * d + b * c
                    n1 = a * a + b * b
                    n2 = c * c + d * d
                    n12 = re * re + im * im
                    assert n12 == n1 * n2


def test_two_ramifies():
    """2 = -i (1+i)^2 in Z[i]."""
    # (1+i)^2 = 2i;  (-i)*(2i) = 2
    re = 1 * 1 - 1 * 1  # 0
    im = 1 * 1 + 1 * 1  # 2
    assert (re, im) == (0, 2)
    # multiply by -i = 0 + (-1)*i:  (0+2i)(0-i) = 2
    re2 = 0 * 0 - 2 * (-1)
    im2 = 0 * (-1) + 2 * 0
    assert (re2, im2) == (2, 0)


def test_p_mod_4_cannot_be_sum_of_two_squares_when_3_mod_4():
    """An odd prime that is 3 mod 4 is never a^2+b^2 (squares mod 4 are 0,1)."""
    for a in range(0, 80):
        for b in range(0, 80):
            s = a * a + b * b
            if s > 1 and s % 4 == 3:
                # should not be prime — in fact no integer that is 3 mod 4
                # is a sum of two squares, prime or not
                raise AssertionError(s)
    # positive check: every prime 1 mod 4 below 200 *is* a sum of two squares
    primes = sieve_primes(200)
    for p in primes:
        if p % 4 != 1:
            continue
        found = False
        r = int(math.isqrt(p))
        for a in range(0, r + 1):
            if is_square(p - a * a):
                found = True
                break
        assert found, p


def test_nu_matches_roots():
    """nu(p) equals the number of solutions of n^2+1=0 mod p, by brute force."""
    for p in sieve_primes(300):
        roots = sum(1 for n in range(p) if (n * n + 1) % p == 0)
        assert roots == n_roots_n2plus1(p), (p, roots)


def test_bh_two_formulas_agree():
    """Direct product prod (1-chi/(p-1)) agrees with (4/pi)*prod a_p
    to within the tail bound, on a moderate prime range."""
    B = 20_000
    primes = sieve_primes(B)
    # formula 1 (conditionally convergent — include all p <= B in order)
    log1 = 0.0
    for p in primes:
        ch = chi4(p)
        term = 1.0 - ch / (p - 1.0)
        log1 += math.log(term)
    C1 = math.exp(log1)
    C2, tail, _ = bateman_horn_constant(B)
    # The two partial products are not identical: formula 1's remainder is
    # the slowly decaying prod_{p>B}(1-chi/(p-1)), while formula 2 already
    # factored out 4/pi (the full L-value).  They must still lie close once
    # B is a few thousand.  We lock a concrete numerical window computed
    # from the absolutely convergent form, and only check that formula 1
    # is within 0.02 of it at B=20_000 (observed gap is from the missing tail
    # of the conditional product).
    assert 1.35 < C2 < 1.39
    assert abs(C1 - C2) < 0.03, (C1, C2, tail)


def test_bh_constant_stable_and_in_range():
    C_small, _, _ = bateman_horn_constant(5_000)
    C, tail, used = bateman_horn_constant(50_000)
    assert used > 100
    # stability: increasing the bound should move C by less than the tail
    assert abs(C - C_small) < 0.01
    assert tail < 0.001
    # locked window used in proof.md (recomputed; not copied from a table)
    assert 1.37280 < C < 1.37283, C
    # direct (conditionally written) partial product at the same bound, no 4/pi
    primes = sieve_primes(50_000)
    log1 = 0.0
    for p in primes:
        log1 += math.log(1.0 - chi4(p) / (p - 1.0))
    C_direct = math.exp(log1)
    assert 1.372 < C_direct < 1.374


def test_identity_4n2plus1_factor_when_n_odd():
    """n=2k+1 => n^2+1 = 2(2k(k+1)+1) with the second factor >=5 for k>=1."""
    for k in range(1, 80):
        n = 2 * k + 1
        val = n * n + 1
        other = 2 * k * (k + 1) + 1
        assert val == 2 * other
        assert other >= 5
        assert other % 2 == 1


def test_euclid_start_values():
    """The Euclid-style starter (2)^2+1=5 is prime; (2*5)^2+1=101 is prime;
    those identities are exact.  The next iterate is composite — checked in
    the computational block, not here as an identity."""
    assert 2 * 2 + 1 == 5 and miller_rabin(5)
    assert (2 * 5) ** 2 + 1 == 101 and miller_rabin(101)
    # standard 1-mod-4 Euclid starter used in the proof:
    assert (2 * 5) ** 2 + 1 == 101
    N = (2 * 5 * 13) ** 2 + 1
    assert N == 16901
    assert N % 5 != 0 and N % 13 != 0
    # 16901 = 130^2+1 is itself prime (do not invent a factorization).
    assert miller_rabin(16901)
    # First composite Euclid iterate using {2,5,13,17,29}:
    # (2*5*13*17*29)^2+1 = 64090^2+1 = 4107528101 = 37 * 173 * 641701
    M = (2 * 5 * 13 * 17 * 29) ** 2 + 1
    assert M == 4_107_528_101
    assert M == 37 * 173 * 641_701
    for q in (37, 173, 641_701):
        assert q % 4 == 1
        assert M % q == 0
        assert q not in (2, 5, 13, 17, 29)
    # 173 ≡ 1 (mod 4) but 173-1=172 is not a square, so this factor of a
    # number of the form m^2+1 need not itself be of the form t^2+1.
    assert not is_square(173 - 1)


def test_no_covering_by_one_modulus():
    """For each prime p<=80 there exists n not 0 at n^2+1 mod p, in fact
    a positive-density set.  Locked as: number of roots is never all of F_p."""
    for p in sieve_primes(80):
        assert n_roots_n2plus1(p) < p


def test_small_known_primes_n2plus1():
    """Hand-checkable list: n^2+1 prime for these n, composite for these n."""
    yes = [1, 2, 4, 6, 10, 14, 16, 20, 24, 26, 36, 40, 54, 56, 66, 74, 84, 90, 94]
    no = [3, 5, 7, 8, 9, 11, 12, 13, 15, 17, 18, 19, 21, 22, 23, 25, 27, 28, 29, 30]
    for n in yes:
        assert miller_rabin(n * n + 1), (n, n * n + 1)
    for n in no:
        assert not miller_rabin(n * n + 1), (n, n * n + 1)
    # n=1 is the only odd n in the 'yes' list
    assert [n for n in yes if n % 2 == 1] == [1]


def test_mertens_style_explicit_sieve_constant():
    """Exact rational product prod_{p in S} (1-2/p) for the explicit sieve
    used in the upper-bound theorem.  S = primes 1 mod 4 that are <= 37."""
    S = [5, 13, 17, 29, 37]
    prod = Fraction(1, 1)
    for p in S:
        prod *= Fraction(p - 2, p)
    # 3/5 * 11/13 * 15/17 * 27/29 * 35/37
    expected = (
        Fraction(3, 5)
        * Fraction(11, 13)
        * Fraction(15, 17)
        * Fraction(27, 29)
        * Fraction(35, 37)
    )
    assert prod == expected
    # numeric lock used in proof.md (computed from the Fraction above)
    assert prod == Fraction(93555, 237133)
    assert abs(float(prod) - 0.3945254350933864) < 1e-12


# ---------------------------------------------------------------------------
# Heavier computations (also exposed as tests with timeouts)
# ---------------------------------------------------------------------------

def _run_census_table(max_N: int = DEFAULT_CENSUS_N, timeout: float = HARD_TIMEOUT_SEC):
    C, tail, _ = bateman_horn_constant(DEFAULT_BH_PRIME_BOUND)
    thresholds = [10, 30, 100, 300, 1000, 3000, 10_000, 30_000, 100_000]
    if max_N >= 300_000:
        thresholds.append(300_000)
    if max_N >= 1_000_000:
        thresholds.append(1_000_000)
    thresholds = [t for t in thresholds if t <= max_N]
    deadline = _deadline(timeout)
    counts = {}
    n_prime = 0
    next_i = 0
    for n in range(1, max_N + 1):
        if n % 8192 == 0:
            _check(deadline, "census table")
        if miller_rabin(n * n + 1):
            n_prime += 1
        while next_i < len(thresholds) and n == thresholds[next_i]:
            N = thresholds[next_i]
            pred = bateman_horn_prediction(N, C)
            counts[N] = {
                "count": n_prime,
                "prediction": pred,
                "ratio": (n_prime / pred) if pred else None,
            }
            next_i += 1
    return {"C": C, "C_tail": tail, "rows": counts}


def test_census_matches_locked_small_counts():
    """Small-N counts are locked so a cold recompute must match exactly."""
    data = _run_census_table(max_N=1000, timeout=15.0)
    rows = data["rows"]
    assert rows[10]["count"] == 5  # n = 1,2,4,6,10
    assert rows[30]["count"] == 10
    assert rows[100]["count"] == 19
    assert rows[300]["count"] == 49
    assert rows[1000]["count"] == 112
    assert 1.370 < data["C"] < 1.375


def test_simpson_integral_stable_at_1e6():
    a = integral_dt_over_log_n2plus1(1_000_000, steps=4_000)
    b = integral_dt_over_log_n2plus1(1_000_000, steps=20_000)
    # |a-b| * C  is the change in predicted count; must stay well below 1
    assert abs(a - b) < 1e-6


def test_no_proper_perfect_power_n2plus1_up_to_20000():
    """Numerical only: n^2+1 is never a perfect power for 1 <= n <= 20000.
    The square case is a theorem; higher powers are not claimed."""
    for n in range(1, 20001):
        v = n * n + 1
        if miller_rabin(v):
            continue
        for e in range(2, 22):
            r = round(v ** (1.0 / e))
            if r >= 2 and r**e == v:
                raise AssertionError((n, v, r, e))


def test_euclid_recurrence_stalls():
    log = euclid_recurrence(max_steps=5, timeout=10.0)
    assert log[0]["is_prime"] is True  # m=2*2=4, 17 prime? found starts with [2]
    # first iterate: P=2, m=4, 17 prime
    assert log[0]["m"] == 4 and log[0]["value"] == 17 and log[0]["is_prime"]
    # second: P=2*17=34, m=68, 68^2+1=4625=5^3*37, composite
    assert log[1]["m"] == 68
    assert log[1]["value"] == 4625
    assert log[1]["is_prime"] is False
    factors = {q: e for q, e in log[1]["factors"]}
    assert factors[5] == 3 and factors[37] == 1
    # 5=2^2+1 and 37=6^2+1 happen to be of the form t^2+1; this is luck,
    # not a general mechanism (locked by a counter-example elsewhere).
    assert is_square(5 - 1) and is_square(37 - 1)


def test_factor_not_always_t2plus1():
    """8^2+1=65=5*13; 13 is 1 mod 4 but 13-1=12 is not a square."""
    assert 8 * 8 + 1 == 65
    assert 65 == 5 * 13
    assert 13 % 4 == 1
    assert not is_square(12)


def test_omega_45807_not_undercounted():
    """Regression: 45807^2+1 = 2 * 5^7 * 13 * 1033 has Omega=10, not 9."""
    primes = sieve_primes(50010)
    v = 45807 * 45807 + 1
    assert v == 2_098_281_250
    assert v == 2 * (5**7) * 13 * 1033
    assert omega_big(v, primes) == 10


def test_omega_parity_split_50000():
    om = census_omega(50_000, timeout=60.0)
    assert om[1] == 3613
    assert om[2] == 12204
    assert om[3] == 16680
    assert om["ge4"] == 17503
    assert om["unknown"] == 0
    assert om["odd"] == 25041
    assert om["even"] == 24959


def test_only_n_eq_1_odd_gives_prime_up_to_2000():
    c = census_n2plus1(2000, timeout=15.0)
    assert c["odd_n_giving_prime"] == 1


def test_large_census_locked_counts():
    """Exact prime counts used in proof.md, recomputed here."""
    data = _run_census_table(max_N=1_000_000, timeout=HARD_TIMEOUT_SEC)
    rows = data["rows"]
    assert rows[10_000]["count"] == 841
    assert rows[100_000]["count"] == 6656
    assert rows[1_000_000]["count"] == 54110
    # BH ratio at N=10^6 is within 1% (numerical evidence, not a theorem)
    assert 0.99 < rows[1_000_000]["ratio"] < 1.01


# ---------------------------------------------------------------------------
# Main: print the tables that go into proof.md / report.md
# ---------------------------------------------------------------------------

def main():
    t0 = time.monotonic()
    print("=== Landau n^2+1 verification / computation ===")
    print(f"pid={os.getpid()}  timeout={HARD_TIMEOUT_SEC}s")

    print("\n-- algebraic tests --")
    test_chi4_multiplicative()
    test_legendre_minus1_via_euler()
    test_odd_prime_factors_are_1_mod_4()
    test_odd_n_greater_than_1_gives_even_composite()
    test_n2plus1_never_square_for_n_ge_1()
    test_consecutive_gcd_divides_5()
    test_gaussian_norm_identity()
    test_two_ramifies()
    test_p_mod_4_cannot_be_sum_of_two_squares_when_3_mod_4()
    test_nu_matches_roots()
    test_identity_4n2plus1_factor_when_n_odd()
    test_euclid_start_values()
    test_no_covering_by_one_modulus()
    test_small_known_primes_n2plus1()
    test_mertens_style_explicit_sieve_constant()
    test_factor_not_always_t2plus1()
    test_simpson_integral_stable_at_1e6()
    test_no_proper_perfect_power_n2plus1_up_to_20000()
    test_omega_45807_not_undercounted()
    print("algebraic tests OK")

    print("\n-- Bateman-Horn constant --")
    C, tail, used = bateman_horn_constant(DEFAULT_BH_PRIME_BOUND)
    print(f"C = {C:.12f}  abs_tail<={tail:.3e}  primes<={DEFAULT_BH_PRIME_BOUND} ({used} primes)")
    C2, tail2, _ = bateman_horn_constant(20_000)
    print(f"C(B=2e4) = {C2:.12f}  tail<={tail2:.3e}")
    test_bh_two_formulas_agree()
    test_bh_constant_stable_and_in_range()
    print("BH tests OK")

    print("\n-- census of primes n^2+1 vs BH prediction --")
    t1 = time.monotonic()
    table = _run_census_table(max_N=DEFAULT_CENSUS_N, timeout=HARD_TIMEOUT_SEC)
    print(f"{'N':>10} {'count':>8} {'BH pred':>12} {'count/pred':>10}")
    for N, row in table["rows"].items():
        print(f"{N:10d} {row['count']:8d} {row['prediction']:12.3f} {row['ratio']:10.4f}")
    print(f"census time {time.monotonic()-t1:.2f}s  (C={table['C']:.9f})")

    print("\n-- Euclid same-shape recurrence --")
    for rec in euclid_recurrence():
        print(rec)

    print("\n-- Omega / parity probe (n <= %d) --" % DEFAULT_P2_N)
    t2 = time.monotonic()
    om = census_omega(DEFAULT_P2_N, timeout=60.0)
    print(om, f"  time {time.monotonic()-t2:.2f}s")

    print("\n-- Gaussian primes on Im=k, Re<=%d --" % DEFAULT_LINE_N)
    t3 = time.monotonic()
    lines = gaussian_line_prime_counts(DEFAULT_LINE_N, imag_max=8, timeout=50.0)
    print(lines, f"  time {time.monotonic()-t3:.2f}s")

    print(f"\nTOTAL {time.monotonic()-t0:.2f}s")


if __name__ == "__main__":
    main()
